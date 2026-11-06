# Report 2

I used Python's ast module to split files by functions and classes. Each definition stays in one chunk, so its code is not cut in the middle. Imports before the first definition form a separate chunk.

chunks.json contains 134 chunks from 26 nonempty files, including tests. Each record stores the text, file, name and line range. The largest chunk has 153 lines.
