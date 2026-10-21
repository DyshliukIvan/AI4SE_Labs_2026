Requirements refinement network

Design

I used Python and LangGraph to turn the source documents into one requirements document. Codex helped write, debug and test the code.

| Node | Model or code | Task |
| --- | --- | --- |
| ingest | Python | Read the input documents |
| extract | gpt-4.1-nano | Extract requirements and source evidence |
| refine | gpt-5-mini | Combine requirements and handle conflicts |
| coverage | Python and gpt-5-mini | Find and repair missing candidate references |
| review | gpt-4o-mini | Compare the result with the sources |
| check_findings | gpt-5-mini | Check whether reviewer findings need a correction |
| render | Python | Save the final document |

I chose a small model for extraction to keep the cost down, a reasoning model for combining requirements, and a different model for review. Python handles file loading, reference checks and formatting without LLM calls.

How it works

The program reads .txt, .eml and .md files from an input directory. The filenames are not hard-coded. Long documents are split into overlapping chunks.

The extractor selects source lines. Python copies these lines as evidence and checks the references. The refinement node merges related requirements, adds descriptions and priorities, and records rejected requirements with reasons.

The coverage node checks that every extracted candidate is linked to a requirement or a blacklist entry. The reviewer then compares the document with the original texts. Missing details go back to refinement. Missing extraction goes back to the extractor. This is the feedback loop.

The network also checks reviewer findings against quotations from the sources or specification. A pass limit stops repeated corrections. Any remaining findings stay visible in the output.

The final document includes unique IDs, names, descriptions, sources, a glossary and open questions. Priorities are Must, Should and Could, with the scale explained in the document. Refinement and review check for duplicates, conflicting requirements and inconsistent terms.

Result and limitations

The corpus has 20 documents. The network extracted 307 candidates and produced 45 requirements and 2 blacklist entries. All candidate references are accounted for. The final workflow reached pass 6 using resumed runs and saved API responses.

All 31 offline tests passed during development. They check the code with mocked responses, not the quality of the generated requirements.

The submitted requirements.md was generated through the API. It still needs human review: one financial-reporting finding remains unresolved. Some descriptions are broad, and one blacklist entry describes merged content rather than a rejected requirement. Reference checks alone cannot prove that every source detail was preserved.

Running

main.py contains the network. paid_run.py adds a cost limit and saved responses for resuming. The later API continuation cost about $0.44, excluding earlier calls. The API key is not submitted.

From the Task_1 directory, set OPENAI_API_KEY in the environment or a local .env file, then run:

```text
python -m pip install -r requirements.txt
python paid_run.py data/corpus --max-cost-usd 1 --max-api-calls 12 --max-iterations 3 --review-batch-size 5
```

This starts a new paid run. Add --resume to continue after a call limit. The submitted requirements.md can be read without running the program again.

Sources

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
