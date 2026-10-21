Requirements refinement network

Purpose and result

The program converts a directory of source texts into one structured requirements document. It uses Python, LangGraph and the OpenAI API. Codex helped implement, debug and test it, as required by the assignment.

The supplied corpus contains 20 documents. Initial extraction produced 228 candidates; targeted recovery increased this to 307. The final document contains 45 requirements and 2 blacklist entries. All 307 candidate IDs are accounted for, and structural checks found no unknown references or duplicate requirement names.

The final status is NEEDS HUMAN REVIEW: one financial-reporting finding remains visible. I do not claim perfect semantic correctness. The assignment explicitly allows imperfect generated output, provided the network addresses every output specification.

Nodes and models

| Node | Model or implementation | Purpose |
| --- | --- | --- |
| ingest | Python | Read documents and retain relative source paths |
| extract | gpt-4.1-nano | Extract candidates with source evidence |
| refine | gpt-5-mini | Merge duplicates, explain priorities and handle conflicts |
| coverage | Python; gpt-5-mini when needed | Account for unassigned candidates and add missing details |
| review | gpt-4o-mini; Python checks | Compare the specification with original sources |
| check_findings | gpt-5-mini in the bounded runner | Check reviewer findings against exact quotations |
| render | Python | Produce Markdown, unique IDs, source lists and review status |

The small extractor handles repeated local tasks. The reasoning model handles consolidation. A different model reviews the result. These are design choices, not proof that this combination is optimal.

All three model names occur in the assignment's allowed list. The live run used actual API responses, not only configured model labels. The extraction caches came from earlier API calls; later refinement, recovery and review also used the API. A manually consolidated chat draft was not substituted for the API-generated output.

Workflow and feedback

```text
ingest -> extract -> refine -> coverage -> review -> check_findings
                     ^                     |
                     +-- refinement -------+
extract <--------------- genuine gaps -----+
render <--------------- pass or pass limit
```

The loader recursively reads nonempty UTF-8 .txt, .eml and .md files from the supplied directory. Input filenames are not hard-coded. Text is split into approximately 16,000-character chunks with 1,200-character overlap.

Extraction selects numbered source lines. Python copies and validates the evidence instead of trusting reproduced quotations. Invalid ranges receive a bounded correction attempt; persistent failures stop processing rather than silently discarding requirements. Literal evidence checks do not prove that every interpretation is entailed.

The reviewer checks up to five documents at a time against the whole specification. Documents longer than 20,000 characters are reviewed separately. Source-specific coverage notes make omissions in the review visible.

Alleged extraction gaps are checked against existing candidates and original sources. Already captured behavior becomes refinement feedback instead of triggering repeated extraction. Genuine gaps return to extraction for the named sources.

A separate coverage step repairs unassigned references, extends paragraphs when details are missing, or adds requirements and justified exclusions. Python rejects a repair that still leaves candidates unaccounted for. Linking an ID is not itself proof of semantic coverage.

Reviewer findings are also checked for false positives. Rejecting a finding requires a reason and a quotation present in the specification or source text. Raw findings and decisions remain in the local review log. This check uses a model and is not an independent human assessment.

A configurable pass limit prevents endless corrections. Remaining findings are printed in the final document. Final workflow pass 6 included resumed checks; this does not mean six independent generations. Successful API responses were reused where requests were identical.

Output requirements

One Markdown document contains sequential REQ-NNNN IDs, short names, paragraph explanations, source paths, candidate references and priorities. The priority scale is printed: Must means essential or explicitly mandatory, Should means important, and Could means optional or tentative.

Refinement and review address semantic deduplication, terminology and contradictions. A glossary explains terms, and unresolved stakeholder choices remain open questions. Discarded candidates have a separate blacklist and reasons. IDs are unique within a document, but may change after a new generation.

This addresses ANS1–ANS5 through three distinct LLM models, deterministic processing, feedback routes and Python LangGraph. OS1–OS9 are addressed by the schemas, prompts, coverage checks, review and renderer. Semantic quality is not guaranteed by schema validity.

Verification and limitations

All 31 API/core offline tests passed during development. They cover evidence validation, chunking, graph feedback, targeted recovery, source-path checks, response reuse, usage recording, budgets, coverage repair and review findings. These tests use mocked model responses and do not measure model accuracy. The test files are not part of this minimal submission.

The separate live execution produced the submitted requirements.md. The final review still records one broad financial-accountability/export finding. Other limitations include broad merged paragraphs and a blacklist entry that describes consolidation rather than a clean rejection. These are reviewable weaknesses, not hidden by a perfect-score claim.

Historical platform and browser versions are preserved from the corpus. They are not recommendations for a new production deployment. Genuine source ambiguities, such as reporting-store architecture and retention policy details, require stakeholder decisions rather than invented answers.

Cost, recovery and safety

paid_run.py uses a cumulative local USD 1 budget, request/output limits and disabled automatic retries. It reserves conservative cost before a request and records returned token usage afterwards. Unknown transport costs retain their reservation. This is an application guard using published standard prices, not an invoice, tax calculation or provider hard limit.

The bounded continuation cost approximately USD 0.44 at published rates. Earlier extraction and unlogged historical calls are not included in that figure. Successful responses are saved by request identity for reuse. Resume checks candidate counts and source excerpts; a changed corpus should use a fresh output directory.

The key is loaded locally from .env and is not included in the submission. The existing key worked, so no credits were purchased. Its ownership was not inferred from API access. The assignment asks for the instructor-supplied key.

Submission

The submission contains main.py, paid_run.py, requirements.txt, this report and the API-generated requirements.md. It excludes credentials, the virtual environment, tests, intermediate JSON, raw responses and the chat-only draft. Original input documents are supplied with the assignment.

Run from the Task_1 directory after setting OPENAI_API_KEY in the environment or a local .env file:

```text
python -m pip install -r requirements.txt
python paid_run.py data/corpus --max-cost-usd 1 --max-api-calls 12 --max-iterations 3 --review-batch-size 5
```

This starts a new paid API run. The saved requirements.md is already the generated result; it does not need to be regenerated to read the submission. If the per-invocation API-call limit stops a run, repeat the command with --resume to continue using saved responses.

References

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OpenAI model documentation](https://developers.openai.com/api/docs/models)
