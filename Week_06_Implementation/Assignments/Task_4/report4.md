# Report 4

I used cosine similarity to compare the query vector with each chunk's code and description vectors. The final score is the average of these two similarities. The function returns the n chunks with the highest scores.

Python scans all 134 records in SQLite. For an inventory query, the results included InventoryLedger and related reservation code and tests.
