"""Run from repository root: python -m unittest discover -s tools/tests -v."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "generate_sources", ROOT / "tools/scripts/generate_sources.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.stage = Path(self.tmp.name)
        self.sources = self.stage / "sources"
        self.sources.mkdir()
        self.target = self.stage / "sources.md"
        self.original = "Before\n" + generator.BEGIN + "\nold\n" + generator.END + "\nAfter\n"
        self.target.write_text(self.original, encoding="utf-8")
        p = patch.object(generator, "STAGE", self.stage)
        p.start()
        self.addCleanup(p.stop)

    def record(self, ident="S001", filename=None, **changes):
        data = dict(id=ident, title="Title | detail", publisher="Publisher",
                    kind="dictionary entry", url=None, status="retrieved", selection_rationale="Reason",
                    limitations="Limit")
        data.update(changes)
        path = self.sources / (filename or ident + ".md")
        path.write_text("---\n" + yaml.safe_dump(data) + "---\n", encoding="utf-8")
        return path

    def test_generation_and_idempotency(self):
        self.record("S002", url="https://example.org")
        self.record("S001")
        generator.generate()
        result = self.target.read_text(encoding="utf-8")
        self.assertTrue(result.startswith("Before\n" + generator.BEGIN))
        self.assertTrue(result.endswith(generator.END + "\nAfter\n"))
        self.assertLess(result.index("| S001 |"), result.index("| S002 |"))
        self.assertIn(r"| S001 | Publisher — Title \| detail | dictionary entry |", result)
        self.assertIn("](https://example.org)", result)
        before = self.target.stat().st_mtime_ns
        generator.generate()
        self.assertEqual(result, self.target.read_text(encoding="utf-8"))
        self.assertEqual(before, self.target.stat().st_mtime_ns)

    def assert_rejected(self):
        before = self.target.read_bytes()
        with self.assertRaises((ValueError, yaml.YAMLError)):
            generator.generate()
        self.assertEqual(before, self.target.read_bytes())

    def test_no_records(self):
        self.assert_rejected()

    def test_blank_kind(self):
        self.record(kind=" ")
        self.assert_rejected()

    def test_invalid_url(self):
        self.record(url="invalid")
        self.assert_rejected()

    def test_mismatched_id(self):
        self.record(filename="S002.md")
        self.assert_rejected()

    def test_missing_key(self):
        path = self.record()
        path.write_text("---\nid: S001\n---\n", encoding="utf-8")
        self.assert_rejected()

    def test_malformed_yaml(self):
        path = self.record()
        path.write_text("---\nid: [\n---\n", encoding="utf-8")
        self.assert_rejected()

    def test_missing_markers(self):
        self.record()
        self.target.write_text("No markers", encoding="utf-8")
        self.assert_rejected()

    def test_duplicate_markers(self):
        self.record()
        self.target.write_text(self.original + generator.BEGIN, encoding="utf-8")
        self.assert_rejected()

    def test_actual_repository_records(self):
        for path in (ROOT / "01-controlled-vocabulary/sources").glob("*.md"):
            (self.sources / path.name).write_bytes(path.read_bytes())
        generator.generate()
        result = self.target.read_text(encoding="utf-8")
        for path in self.sources.glob("*.md"):
            self.assertIn(f"| {path.stem} |", result)
        self.assertGreaterEqual(len(list(self.sources.glob("*.md"))), 6)


if __name__ == "__main__":
    unittest.main()
