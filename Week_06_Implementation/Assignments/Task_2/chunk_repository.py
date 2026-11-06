import ast
import json
from pathlib import Path


def split_file(path, text):
    lines = text.splitlines(keepends=True)
    if not lines:
        return []

    boundaries = [(0, "module")]
    if path.suffix.lower() == ".py":
        tree = ast.parse(text, filename=str(path))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                first_line = node.lineno
                for decorator in node.decorator_list:
                    first_line = min(first_line, decorator.lineno)
                start = first_line - 1
                if start == 0:
                    boundaries[0] = (0, node.name)
                else:
                    boundaries.append((start, node.name))

    parts = []
    for i, (start, name) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(lines)
        parts.append((start, end, name, "".join(lines[start:end])))
    return parts


def chunk_repository(repository):
    chunks = []
    ignored = {".git", "__pycache__", ".venv", "venv", ".pytest_cache"}
    extensions = {".py", ".md", ".txt", ".toml", ".json", ".yaml", ".yml"}

    for path in sorted(repository.rglob("*")):
        relative = path.relative_to(repository)
        if any(part in ignored for part in relative.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue

        text = path.read_text(encoding="utf-8")
        for start, end, name, content in split_file(path, text):
            chunks.append({
                "id": f"{relative.as_posix()}:{start + 1}-{end}",
                "file": relative.as_posix(),
                "start_line": start + 1,
                "end_line": end,
                "name": name,
                "content": content,
            })

    return chunks


if __name__ == "__main__":
    task_folder = Path(__file__).resolve().parent
    repository = task_folder.parents[1] / "AI4SE_Playground"
    if not repository.is_dir():
        raise SystemExit(f"Repository not found: {repository}")

    chunks = chunk_repository(repository)
    output = task_folder / "chunks.json"
    output.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(chunks)} chunks to {output}")
