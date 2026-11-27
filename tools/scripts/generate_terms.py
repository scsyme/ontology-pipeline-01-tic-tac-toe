"""Generate the term register from standalone Markdown records.

Run: python tools/scripts/generate_terms.py
Requires PyYAML.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "01-controlled-vocabulary"
BEGIN = "<!-- BEGIN GENERATED TERMS -->"
END = "<!-- END GENERATED TERMS -->"
KEYS = {"id", "term", "status", "evidence"}
EVIDENCE_KEYS = {"source_id", "observed_form", "locator", "excerpt"}


def cell(value):
    return value.replace("|", r"\|").replace("\n", " ")


def generate():
    records = {}
    for path in sorted((STAGE / "terms").glob("*.md")):
        parts = path.read_text(encoding="utf-8").splitlines()
        if not parts or parts[0] != "---" or "---" not in parts[1:]:
            raise ValueError(f"Missing frontmatter: {path}")
        data = yaml.safe_load("\n".join(parts[1:parts.index("---", 1)]))
        if not isinstance(data, dict) or set(data) != KEYS:
            raise ValueError(f"Invalid frontmatter keys: {path}")
        for key in KEYS - {"evidence"}:
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f"Invalid {key}: {path}")
        evidence = data["evidence"]
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"Expected evidence entries: {path}")
        for entry in evidence:
            if not isinstance(entry, dict) or set(entry) != EVIDENCE_KEYS:
                raise ValueError(f"Invalid evidence keys: {path}")
            for key in EVIDENCE_KEYS:
                if not isinstance(entry[key], str) or not entry[key].strip():
                    raise ValueError(f"Invalid evidence {key}: {path}")
            source_id = entry["source_id"]
            if not re.fullmatch(r"S[0-9]+", source_id):
                raise ValueError(f"Invalid source ID: {path}")
            if not (STAGE / "sources" / f"{source_id}.md").is_file():
                raise ValueError(f"Unknown source {source_id}: {path}")
        ident = data["id"]
        if not re.fullmatch(r"T[0-9]+", ident) or ident != path.stem or ident in records:
            raise ValueError(f"Invalid or duplicate ID: {path}")
        records[ident] = data
    if not records:
        raise ValueError("No term records found")
    lines = ["| ID | Term | Status | Source | Observed form | Passage | Excerpt |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for ident, data in sorted(records.items()):
        for entry in data["evidence"]:
            source_id = entry["source_id"]
            values = [
                f"[{ident}](terms/{ident}.md)",
                cell(data["term"]),
                cell(data["status"]),
                f"[{source_id}](sources/{source_id}.md)",
                cell(entry["observed_form"]),
                cell(entry["locator"]),
                cell(entry["excerpt"]),
            ]
            lines.append("| " + " | ".join(values) + " |")
    target = STAGE / "terms.md"
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
