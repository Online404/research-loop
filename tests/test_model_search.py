"""Model search initialization stays local, empty, resumable, and non-destructive."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / "skills" / "research-loop" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from init_model_search import init_model_search
from init_project import init_project


class ModelSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.workspace = init_project(self.root, "Example domain", "Evaluate transferable modules")

    def read_json(self, file):
        return json.loads(file.read_text(encoding="utf-8"))

    def test_default_initialization_is_pending_and_empty(self):
        original = {file: file.read_bytes() for file in self.workspace.rglob("*") if file.is_file()}
        target = init_model_search(self.root, "Example baseline")
        search = self.read_json(target / "search.json")
        variant = self.read_json(target / "variants.jsonl")
        self.assertEqual(search["target_module_count"], [2, 3])
        self.assertEqual(search["current_incumbent"], "B0")
        self.assertEqual(search["baseline_id"], variant["id"])
        self.assertIsNone(search["selection_protocol"])
        self.assertTrue(search["next_action"])
        self.assertEqual((target / "candidates.jsonl").read_text(), "")
        self.assertEqual(variant["baseline_name"], "Example baseline")
        self.assertEqual(variant["modules"], [])
        self.assertEqual(variant["module_count"], 0)
        self.assertEqual(variant["reading_status"], "unread")
        self.assertEqual(variant["execution_status"], "planned")
        self.assertEqual(variant["evidence_status"], "unvalidated")
        self.assertIsNone(variant["results"])
        self.assertEqual(variant["experiment_ids"], [])
        self.assertIsNone(variant["code_ref"])
        self.assertEqual(variant["decision"], "baseline_pending")
        self.assertEqual({file.name for file in target.iterdir()}, {"baseline.md", "candidates.jsonl", "variants.jsonl", "search.json", "STATE.md"})
        for file, contents in original.items():
            self.assertEqual(file.read_bytes(), contents)
        self.assertEqual(list((self.workspace / "experiments").iterdir()), [])

    def test_templates_do_not_assert_reading_or_validation(self):
        target = init_model_search(self.root, "Unread baseline")
        baseline = (target / "baseline.md").read_text(encoding="utf-8")
        state = (target / "STATE.md").read_text(encoding="utf-8")
        self.assertIn("Paper reading: unread", baseline)
        self.assertIn("Reproduction: not_started", baseline)
        self.assertIn("Evidence: unvalidated", baseline)
        self.assertIn("Results: none", baseline)
        self.assertIn("Validated evidence: none", state)
        self.assertIn("pending reproduction", state)

    def test_refuses_existing_search_without_touching_files(self):
        target = init_model_search(self.root, "Original baseline")
        (target / "STATE.md").write_text("Existing decision and real research notes", encoding="utf-8")
        before = {file.name: file.read_bytes() for file in target.iterdir()}
        with self.assertRaises(FileExistsError):
            init_model_search(self.root, "Replacement", (4, 5))
        self.assertEqual({file.name: file.read_bytes() for file in target.iterdir()}, before)
        self.assertFalse(list(self.workspace.glob(".model-search-init-*")))

    def test_refuses_empty_existing_search(self):
        target = self.workspace / "model-search"
        target.mkdir()
        with self.assertRaises(FileExistsError):
            init_model_search(self.root, "Baseline")
        self.assertEqual(list(target.iterdir()), [])

    def test_missing_workspace_rejected_without_creating_it(self):
        missing = Path(self.temp.name) / "missing-project"
        with self.assertRaisesRegex(ValueError, "existing .research workspace required"):
            init_model_search(missing, "Baseline")
        self.assertFalse(missing.exists())
        empty = Path(self.temp.name) / "empty-project"
        (empty / ".research").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "project.json required"):
            init_model_search(empty, "Baseline")
        self.assertEqual(list((empty / ".research").iterdir()), [])

    def test_explicit_module_targets_and_parent_relative_cli_path(self):
        child = self.root / "working"
        child.mkdir()
        result = subprocess.run(
            [sys.executable, str(SKILL_SCRIPTS / "init_model_search.py"), "--path", "..", "--baseline", "CLI baseline", "--target-modules", "1", "4"],
            cwd=child, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        search = self.read_json(self.workspace / "model-search" / "search.json")
        self.assertEqual(search["target_module_count"], [1, 4])

    def test_equal_target_bounds_are_allowed(self):
        target = init_model_search(self.root, "Baseline", (2, 2))
        self.assertEqual(self.read_json(target / "search.json")["target_module_count"], [2, 2])

    def test_invalid_targets_or_baseline_do_not_write(self):
        for modules in ((0, 3), (3, 2), (1,), (True, 3), (1, 2, 3), ("2", "3")):
            with self.subTest(modules=modules):
                with self.assertRaises(ValueError):
                    init_model_search(self.root, "Baseline", modules)
        for baseline in ("", " ", "Baseline\nOther"):
            with self.subTest(baseline=baseline):
                with self.assertRaises(ValueError):
                    init_model_search(self.root, baseline)
        self.assertFalse((self.workspace / "model-search").exists())
        self.assertFalse(list(self.workspace.glob(".model-search-init-*")))

    def test_incompatible_project_version_rejected(self):
        config = self.workspace / "project.json"
        config.write_text('{"schema_version": 2}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "schema_version 1"):
            init_model_search(self.root, "Baseline")
        self.assertEqual(self.read_json(config), {"schema_version": 2})
        self.assertFalse((self.workspace / "model-search").exists())

    def test_failed_staging_does_not_expose_partial_search(self):
        original_write = Path.write_text

        def fail_second_file(path, content, *args, **kwargs):
            if path.name == "candidates.jsonl":
                raise OSError("Simulated write failure")
            return original_write(path, content, *args, **kwargs)

        with patch.object(Path, "write_text", fail_second_file):
            with self.assertRaisesRegex(OSError, "Simulated write failure"):
                init_model_search(self.root, "Baseline")
        self.assertFalse((self.workspace / "model-search").exists())
        self.assertFalse(list(self.workspace.glob(".model-search-init-*")))

    def test_installed_skill_runs_independently(self):
        destination = Path(self.temp.name) / "skills"
        installation = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"), "--dest", str(destination)],
            capture_output=True, text=True,
        )
        self.assertEqual(installation.returncode, 0, installation.stderr)
        script = destination / "research-loop" / "scripts" / "init_model_search.py"
        result = subprocess.run(
            [sys.executable, str(script), "--path", str(self.root), "--baseline", "Installed baseline"],
            cwd=self.temp.name, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.workspace / "model-search"
        self.assertEqual(self.read_json(target / "search.json")["target_module_count"], [2, 3])
        self.assertEqual(self.read_json(target / "variants.jsonl")["baseline_name"], "Installed baseline")

    def test_symlink_workspace_rejected_when_available(self):
        link = Path(self.temp.name) / "linked-project"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted on this platform")
        with self.assertRaises(ValueError):
            init_model_search(link, "Baseline")
        self.assertFalse((self.workspace / "model-search").exists())


if __name__ == "__main__":
    unittest.main()
