import argparse
import json
import math
import sqlite3
import sys
from pathlib import Path


TASK_FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_FOLDER.parent / "Task_3"))
from create_embeddings import DIMENSIONS, EMBEDDING_MODEL, embed_texts, read_key


def cosine_similarity(first, second):
    if len(first) != len(second):
        raise ValueError("Vectors must have the same length")
    dot = sum(a * b for a, b in zip(first, second))
    first_length = math.sqrt(sum(a * a for a in first))
    second_length = math.sqrt(sum(b * b for b in second))
    if first_length == 0 or second_length == 0:
        raise ValueError("Cannot compare a zero vector")
    return dot / (first_length * second_length)


def find_chunks(query_embedding, n=5, database=None):
    if n <= 0:
        raise ValueError("n must be positive")
    if len(query_embedding) != DIMENSIONS or not all(
        isinstance(x, (int, float)) and math.isfinite(x) for x in query_embedding
    ):
        raise ValueError(f"Expected {DIMENSIONS} finite numbers")
    if not any(query_embedding):
        raise ValueError("The query vector must not be zero")

    database = Path(database) if database else TASK_FOLDER.parent / "Task_3/embeddings.sqlite"
    with sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        settings = dict(connection.execute("SELECT key, value FROM metadata").fetchall())
        if settings.get("embedding_model") != EMBEDDING_MODEL or settings.get("dimensions") != str(DIMENSIONS):
            raise ValueError("The database uses different embedding settings")
        rows = connection.execute("SELECT * FROM chunks ORDER BY id").fetchall()

    results = []
    for row in rows:
        if row["code_embedding"] is None or row["description_embedding"] is None:
            raise ValueError(f"Missing embeddings for {row['id']}")
        code_score = cosine_similarity(query_embedding, json.loads(row["code_embedding"]))
        description_score = cosine_similarity(query_embedding, json.loads(row["description_embedding"]))
        results.append({
            "id": row["id"],
            "file": row["file"],
            "name": row["name"],
            "start_line": row["start_line"],
            "end_line": row["end_line"],
            "content": row["content"],
            "description": row["description"],
            "code_score": code_score,
            "description_score": description_score,
            "score": (code_score + description_score) / 2,
        })

    results.sort(key=lambda item: (-item["score"], item["id"]))
    return results[:n]


def embed_query(text):
    if not text.strip():
        raise ValueError("The query must not be empty")
    project = TASK_FOLDER.parents[1]
    key = read_key(project / "gemini.env", "GEMINI_API_KEY")
    return embed_texts([text], key, task_type="RETRIEVAL_QUERY")[0]


def main():
    parser = argparse.ArgumentParser(description="Find relevant repository chunks")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--query", help="Text to embed with Gemini")
    source.add_argument("--vector", type=Path, help="JSON file containing a query vector")
    parser.add_argument("-n", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--output", type=Path, help="Save full results as JSON")
    args = parser.parse_args()

    vector = json.loads(args.vector.read_text(encoding="utf-8")) if args.vector else embed_query(args.query)
    results = find_chunks(vector, args.n)
    for rank, item in enumerate(results, 1):
        print(f"{rank}. {item['name']} | {item['file']}:{item['start_line']}-{item['end_line']} | {item['score']:.4f}")
    if args.output:
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
