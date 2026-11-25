"""Generate the source register from standalone Markdown records.

Run: python tools/scripts/generate_sources.py
Requires PyYAML.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "01-controlled-vocabulary"
BEGIN = "<!-- BEGIN GENERATED SOURCES -->"
END = "<!-- END GENERATED SOURCES -->"
KEYS = {"id", "title", "kind", "publisher", "url", "status",
        "selection_rationale", "limitations"}


def cell(value):
    return value.replace("|", r"\|").replace("\n", " ")


def generate():
    records = {}
    for path in sorted((STAGE / "sources").glob("*.md")):
        parts = path.read_text(encoding="utf-8").splitlines()
        if not parts or parts[0] != "---" or "---" not in parts[1:]:
            raise ValueError(f"Missing frontmatter: {path}")
        data = yaml.safe_load("\n".join(parts[1:parts.index("---", 1)]))
        if not isinstance(data, dict) or set(data) != KEYS:
            raise ValueError(f"Invalid frontmatter keys: {path}")
        for key in KEYS - {"url"}:
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f"Invalid {key}: {path}")
        if data["url"] is not None and (not isinstance(data["url"], str)
                or not data["url"].startswith(("https://", "http://"))):
            raise ValueError(f"Invalid URL: {path}")
        ident = data["id"]
        if not re.fullmatch(r"S[0-9]+", ident) or ident != path.stem or ident in records:
            raise ValueError(f"Invalid or duplicate ID: {path}")
        records[ident] = data
    if not records:
        raise ValueError("No source records found")
    lines = ["| ID | Source | Kind | Selection rationale | Limitations / status |",
             "| --- | --- | --- | --- | --- |"]
    for ident, data in sorted(records.items()):
        name = cell(f'{data["publisher"]} — {data["title"]}')
        source = f'[{name}]({data["url"]})' if data["url"] else name
        status = cell(data["status"].capitalize() + "; " + data["limitations"])
        lines.append(f'| {ident} | {source} | {cell(data["kind"])} | {cell(data["selection_rationale"])} | {status} |')
    target = STAGE / "sources.md"
    original = target.read_bytes().decode("utf-8")
    if original.count(BEGIN) != 1 or original.count(END) != 1:
        raise ValueError("Expected exactly one pair of generated-content markers")
    start = original.index(BEGIN) + len(BEGIN)
    end = original.index(END)
    if end < start:
        raise ValueError("Generated-content markers out of order")
    newline = "\r\n" if "\r\n" in original else "\n"
    updated = original[:start] + newline * 2 + newline.join(lines) + newline * 2 + original[end:]
    if updated != original:
        target.write_bytes(updated.encode("utf-8"))


if __name__ == "__main__":
    generate()
