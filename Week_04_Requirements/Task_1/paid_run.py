"""Run the API network with resumable responses and a conservative dollar budget."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from openai import APIError, OpenAI

from main import Network, ROOT, Specification, load_documents, save_json

# Standard text prices in USD per million tokens, checked 2026-10-21.
RATES = {"gpt-4.1-nano": (0.10, 0.40), "gpt-5-mini": (0.25, 2.00),
         "gpt-4o-mini": (0.15, 0.60)}
OUTPUT_LIMITS = {"gpt-4.1-nano": 32768, "gpt-5-mini": 32768, "gpt-4o-mini": 12000}


class BudgetNetwork(Network):
    def __init__(self, args, client):
        super().__init__(args, client)
        self.budget_path = self.output / "paid_budget.json"
        self.budget = (json.loads(self.budget_path.read_text(encoding="utf-8"))
                       if self.budget_path.exists() else {"entries": []})

    def charged_or_reserved(self):
        return sum(item.get("charged_usd", item["reserved_usd"])
                   for item in self.budget["entries"])

    def ask(self, model, schema, instruction, payload):
        if model not in RATES:
            raise ValueError(f"No verified price configured for {model}; no request sent.")
        limit = min(self.args.max_output_tokens, OUTPUT_LIMITS[model])
        request = {"model": model, "schema": schema.model_json_schema(),
                   "instruction": instruction, "payload": payload,
                   "max_output_tokens": limit, "reasoning_effort": "low" if model.startswith("gpt-5") else None,
                   "api_prompt_version": 1}
        serialized = json.dumps(request, sort_keys=True, ensure_ascii=False)
        identity = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        checkpoint = self.output / "api_checkpoints" / f"{schema.__name__}_{identity}.json"
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_text(encoding="utf-8"))
            if saved.get("origin") != "openai_api" or saved.get("request_hash") != identity:
                raise ValueError(f"Invalid API checkpoint: {checkpoint}")
            result = schema.model_validate(saved["result"]).model_dump()
            print(f"[resume API] {schema.__name__}", flush=True)
            return result

        input_rate, output_rate = RATES[model]
        # UTF-8 byte count overestimates text BPE tokens. Add room for framing/schema
        # expansion. This is a local cost guard, not a provider billing guarantee.
        input_bound = len(serialized.encode("utf-8")) + 8192
        reserved = (input_bound * input_rate + limit * output_rate) / 1_000_000
        if self.charged_or_reserved() + reserved > self.args.max_cost_usd:
            raise ValueError(f"Budget would exceed ${self.args.max_cost_usd:.2f}; no request sent. "
                             f"Charged/reserved: ${self.charged_or_reserved():.4f}; "
                             f"next conservative reservation: ${reserved:.4f}.")
        if self.api_calls >= self.args.max_api_calls:
            raise ValueError("Request limit reached; no request sent. Completed responses are saved.")
        entry = {"request_hash": identity, "model": model, "stage": schema.__name__,
                 "reserved_usd": reserved, "status": "reserved",
                 "timestamp": datetime.now(timezone.utc).isoformat()}
        self.budget["entries"].append(entry)
        save_json(self.budget_path, self.budget)
        print(f"[budget] {schema.__name__}: reserve ${reserved:.4f}; "
              f"ceiling ${self.args.max_cost_usd:.2f}", flush=True)
        previous_usage = len(self.usage)
        old_limit = self.args.max_output_tokens
        self.args.max_output_tokens = limit
        try:
            result = super().ask(model, schema, instruction, payload)
        except BaseException:
            entry["status"] = "failed_or_interrupted"
            # Transport failures may still be billable; retain their full reservation.
            self.settle(entry, previous_usage)
            raise
        else:
            entry["status"] = "completed"
            self.settle(entry, previous_usage)
            record = self.usage[-1]
            save_json(checkpoint, {"origin": "openai_api", "request_hash": identity,
                                  "model": model, "response_id": record["response_id"],
                                  "result": result})
            return result
        finally:
            self.args.max_output_tokens = old_limit

    def settle(self, entry, previous_usage):
        if len(self.usage) > previous_usage:
            record = self.usage[-1]
            usage = record.get("usage", {})
            if "prompt_tokens" in usage and "completion_tokens" in usage:
                rates = RATES[entry["model"]]
                entry["charged_usd"] = (usage["prompt_tokens"] * rates[0]
                                        + usage["completion_tokens"] * rates[1]) / 1_000_000
                entry["usage"] = usage
                entry["response_id"] = record["response_id"]
        save_json(self.budget_path, self.budget)


def main():
    load_dotenv(ROOT / ".env")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    parser.add_argument("--max-cost-usd", type=float, default=1.0)
    parser.add_argument("--max-api-calls", type=int, default=12)
    parser.add_argument("--max-output-tokens", type=int, default=32768)
    parser.add_argument("--max-iterations", type=int, default=3)
    parser.add_argument("--review-batch-size", type=int, default=5)
    parser.add_argument("--resume", action="store_true",
                        help="Repair and review the latest completed API specification, preserving its candidates")
    parser.add_argument("--extract-model", default="gpt-4.1-nano")
    parser.add_argument("--refine-model", default="gpt-5-mini")
    parser.add_argument("--review-model", default="gpt-4o-mini")
    args = parser.parse_args()
    if not math.isfinite(args.max_cost_usd) or args.max_cost_usd <= 0:
        parser.error("--max-cost-usd must be finite and positive")
    if min(args.max_api_calls, args.max_output_tokens, args.max_iterations, args.review_batch_size) < 1:
        parser.error("Request, token and iteration limits must be positive")
    if len({args.extract_model, args.refine_model, args.review_model}) != 3:
        parser.error("Three distinct models are required")
    if not {args.extract_model, args.refine_model, args.review_model} <= RATES.keys():
        parser.error("Use models with verified prices in RATES")
    if urlsplit(os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).hostname != "api.openai.com":
        parser.error("This cost guard uses direct OpenAI prices, not custom endpoint prices")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        parser.error("Set your API key locally in .env; do not paste it into a chat")
    args.file = None
    args.extract_only = False
    args.evidence_retries = 1
    args.validate_extraction_gaps = True
    args.adjudicate_findings = True
    network = BudgetNetwork(args, OpenAI(timeout=300, max_retries=0))
    try:
        initial = {}
        if args.resume:
            summary = json.loads((network.output / "run_summary.json").read_text(encoding="utf-8"))
            previous = summary["iterations"]
            candidates = json.loads((network.output / "candidates.json").read_text(encoding="utf-8"))
            if len(candidates) != summary["candidates"]:
                raise ValueError("Candidate file differs from the last completed run; use a fresh run.")
            documents = load_documents(args.input.resolve())
            source_text = {d["source"]: " ".join(d["text"].split()) for d in documents}
            for candidate in candidates:
                evidence = " ".join(candidate["evidence"].split())
                if not evidence or evidence not in source_text.get(candidate["source"], ""):
                    raise ValueError("Source evidence changed; do not resume this output directory.")
            spec = Specification.model_validate_json(
                (network.output / f"specification_{previous}.json").read_text(encoding="utf-8")).model_dump()
            history_path = network.output / "reviews.json"
            history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
            initial = {"documents": documents, "candidates": candidates, "irrelevant": [],
                       "specification": spec, "iteration": previous + 1,
                       "issues": history[-1]["issues"] if history else [],
                       "review_history": history, "extraction_requests": []}
            args.start_node = "coverage"
        network.graph().invoke(initial, {"recursion_limit": 8 + args.max_iterations * 5})
    except APIError as exc:
        code = str(getattr(exc, "code", None))
        safe_code = code if re.fullmatch(r"[A-Za-z0-9_.:-]{1,80}", code) else "redacted"
        print(f"API error: {type(exc).__name__}; HTTP {getattr(exc, 'status_code', 'n/a')}; "
              f"code {safe_code}. No automatic retry.", file=sys.stderr)
        return 1
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted. Saved API responses will be reused on restart.", file=sys.stderr)
        return 130
    finally:
        print(f"[budget] cumulative paid continuation charged/reserved: "
              f"${network.charged_or_reserved():.4f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
