# Report 3

I used Gemini's gemini-embedding-001 model for embeddings, with 768 dimensions. Each chunk has two vectors: code and description. Descriptions come from docstrings or gpt-4o-mini when no docstring is available.

I chose SQLite because it stores the chunks and vectors in one file and works with Python's standard library. embeddings.sqlite contains 134 chunks and 268 vectors.
