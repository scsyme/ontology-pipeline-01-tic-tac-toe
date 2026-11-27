"""Regression checks for term evidence and generated-register preservation."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "generate_terms", ROOT / "tools/scripts/generate_terms.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class TermGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.stage = Path(self.tmp.name)
        (self.stage / "terms").mkdir()
        (self.stage / "sources").mkdir()
        (self.stage / "sources/S005.md").write_text("---\nid: S005\n---\n")
        self.target = self.stage / "terms.md"
        self.original = "Before\r\n" + generator.BEGIN + "\r\nold\r\n" + generator.END + "\r\nAfter\r\n"
        self.target.write_bytes(self.original.encode())
        self.data = dict(id="T001", term="square", status="candidate", evidence=[
            dict(source_id="S005", observed_form="squares",
                 locator="p. 1", excerpt="nine squares | on\nthe board")])
        self.patcher = patch.object(generator, "STAGE", self.stage)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def record(self, data, filename="T001.md"):
        (self.stage / "terms" / filename).write_text(
            "---\n" + yaml.safe_dump(data) + "---\n", encoding="utf-8")

    def test_multiple_occurrences_order_escaping_and_idempotency(self):
        self.data["evidence"].append(dict(
            source_id="S005", observed_form="square", locator="p. 2",
            excerpt="a square"))
        self.record(self.data)
        second = copy.deepcopy(self.data)
        second["id"] = "T002"
        self.record(second, "T002.md")
        generator.generate()
        result = self.target.read_bytes()
        self.assertTrue(result.startswith(("Before\r\n" + generator.BEGIN).encode()))
        self.assertTrue(result.endswith((generator.END + "\r\nAfter\r\n").encode()))
        self.assertIn(b"nine squares \\| on the board", result)
        self.assertIn(b"[S005](sources/S005.md)", result)
        self.assertEqual(result.count(b"[T001](terms/T001.md)"), 2)
        self.assertLess(result.index(b"[T001]"), result.index(b"[T002]"))
        modified = self.target.stat().st_mtime_ns
        generator.generate()
        self.assertEqual(self.target.read_bytes(), result)
        self.assertEqual(self.target.stat().st_mtime_ns, modified)

    def test_invalid_records_preserve_register(self):
        mutations = [
            lambda d: d.update(id="T002"),
            lambda d: d.update(id="../T001"),
            lambda d: d.update(term=" "),
            lambda d: d.pop("status"),
            lambda d: d.update(evidence=[]),
            lambda d: d.update(evidence={}),
            lambda d: d["evidence"][0].update(source_id="S999"),
            lambda d: d["evidence"][0].update(source_id="../S005"),
            lambda d: d["evidence"][0].update(locator=None),
            lambda d: d["evidence"][0].pop("excerpt"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.data)
                mutation(data)
                self.record(data)
                with self.assertRaises(ValueError):
                    generator.generate()
                self.assertEqual(self.target.read_bytes(), self.original.encode())

    def test_invalid_markers_preserve_register(self):
        self.record(self.data)
        for text in ["Missing", generator.END + generator.BEGIN,
                     self.original + generator.BEGIN]:
            with self.subTest(text=text):
                self.target.write_bytes(text.encode())
                with self.assertRaises(ValueError):
                    generator.generate()
                self.assertEqual(self.target.read_bytes(), text.encode())

    def test_actual_records(self):
        for folder in ["sources", "terms"]:
            for path in (ROOT / "01-controlled-vocabulary" / folder).glob("*.md"):
                (self.stage / folder / path.name).write_bytes(path.read_bytes())
        generator.generate()
        for path in (self.stage / "terms").glob("*.md"):
            self.assertIn(f"[{path.stem}](terms/{path.name})",
                          self.target.read_text())


if __name__ == "__main__":
    unittest.main()
