"""Observable invariants for local initialization, evidence memory, and installation."""

from __future__ import annotations

import importlib.util
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
from init_project import init_project
from validate_project import validate_project

spec = importlib.util.spec_from_file_location("research_loop_install", ROOT / "scripts" / "install.py")
installer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(installer)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.workspace = init_project(self.root, "Example domain", "Test a research hypothesis")

    def ledger(self, name, records):
        (self.workspace / "memory" / f"{name}.jsonl").write_text(
            "".join(json.dumps(record) + "\n" for record in records), encoding="utf-8"
        )

    def experiment(self, **changes):
        record = {"id": "E1", "execution_status": "completed", "evidence_status": "unvalidated", "protocol": "Hold out evaluation data; compare the predefined baseline.", "artifacts": ["outputs/result.json"]}
        record.update(changes)
        (self.workspace / "experiments" / "E1.json").write_text(json.dumps(record), encoding="utf-8")

    def paper(self, **changes):
        record = {"id": "P1", "title": "Example paper", "source": "https://example.org/paper", "reading_depth": "partial", "source_anchors": ["Section 4, Table 2"]}
        record.update(changes)
        self.ledger("papers", [record])

    def claim(self, **changes):
        record = {"id": "C1", "text": "A testable claim", "kind": "empirical", "status": "supported", "evidence": [{"type": "experiment", "id": "E1", "locator": "outputs/result.json"}]}
        record.update(changes)
        self.ledger("claims", [record])

    def result_file(self):
        (self.root / "outputs").mkdir(exist_ok=True)
        (self.root / "outputs" / "result.json").write_text('{"fixture": true}\n', encoding="utf-8")

    def test_init_is_empty_and_has_no_permissions(self):
        self.assertEqual(validate_project(self.root), [])
        config = json.loads((self.workspace / "project.json").read_text(encoding="utf-8"))
        self.assertIsNone(config["resource_budget"])
        self.assertIsNone(config["local_capabilities"])
        self.assertEqual(config["stage"], "intake")
        self.assertEqual((self.workspace / "memory" / "papers.jsonl").read_text(), "")

    def test_no_clobber(self):
        state = self.workspace / "STATE.md"
        state.write_text("Existing research state", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            init_project(self.root, "New", "New")
        self.assertEqual(state.read_text(), "Existing research state")

    def test_invalid_init_does_not_create_workspace(self):
        target = Path(self.temp.name) / "bad"
        with self.assertRaises(ValueError):
            init_project(target, " ", "Objective")
        self.assertFalse(target.exists())
        with patch("init_project.validate_project", return_value=["fixture failure"]):
            with self.assertRaises(ValueError):
                init_project(target, "Domain", "Objective")
        self.assertFalse((target / ".research").exists())
        self.assertEqual(list(target.iterdir()), [])

    def test_malformed_records_and_duplicate_ids(self):
        file = self.workspace / "memory" / "papers.jsonl"
        file.write_text('{"id":"P1","id":"P2"}\n[]\nnot-json\n', encoding="utf-8")
        self.assertEqual(len(validate_project(self.root)), 3)
        self.paper()
        self.claim(id="P1", status="hypothesis", evidence=[])
        self.assertTrue(any("duplicate id" in e for e in validate_project(self.root)))

    def test_invalid_field_types_produce_diagnostics(self):
        self.paper(reading_depth=["partial"])
        self.claim(kind="literature", evidence=[{"type": "paper", "id": "P1", "locator": "Section 4, Table 2"}])
        self.assertTrue(any("reading_depth must be" in e for e in validate_project(self.root)))
        self.ledger("papers", [])
        self.claim(evidence=[{"type": [], "id": {}}])
        self.assertTrue(any("evidence requires type" in e for e in validate_project(self.root)))

    def test_supported_claim_needs_evidence_and_known_refs(self):
        self.claim(evidence=[])
        self.assertTrue(any("requires evidence" in e for e in validate_project(self.root)))
        self.claim()
        self.assertTrue(any("missing experiment" in e for e in validate_project(self.root)))

    def test_completed_execution_is_not_validated_evidence(self):
        self.result_file()
        self.experiment()
        self.claim()
        self.assertTrue(any("completed alone is insufficient" in e for e in validate_project(self.root)))

    def test_completed_execution_requires_declared_artifacts_to_exist(self):
        self.experiment()
        self.assertTrue(any("referenced file is missing" in e for e in validate_project(self.root)))
        self.result_file()
        self.assertEqual(validate_project(self.root), [])
        (self.root / "outputs" / "result.json").write_text("", encoding="utf-8")
        self.assertTrue(any("referenced file is missing, empty" in e for e in validate_project(self.root)))
        self.experiment(execution_status="planned")
        self.assertEqual(validate_project(self.root), [])

    def test_validated_experiment_requires_real_artifacts_and_protocol(self):
        self.experiment(evidence_status="validated", protocol=" ")
        self.claim()
        errors = validate_project(self.root)
        self.assertTrue(any("protocol" in e for e in errors))
        self.assertTrue(any("referenced file is missing" in e for e in errors))
        self.result_file()
        self.experiment(evidence_status="validated")
        self.assertEqual(validate_project(self.root), [])
        self.experiment(execution_status="running", evidence_status="validated")
        self.assertTrue(any("requires execution_status completed" in e for e in validate_project(self.root)))

    def test_full_text_requires_card_and_anchors(self):
        self.paper(reading_depth="full_text", source_anchors=[])
        errors = validate_project(self.root)
        self.assertTrue(any("requires source_anchors" in e for e in errors))
        self.assertTrue(any("card_ref" in e for e in errors))
        (self.root / "card.md").write_text("Source-grounded fixture card", encoding="utf-8")
        self.paper(reading_depth="full_text", card_ref="card.md")
        self.assertEqual(validate_project(self.root), [])

    def test_literature_support_and_empirical_distinction(self):
        self.paper()
        refs = [{"type": "paper", "id": "P1", "locator": "Section 4, Table 2"}]
        self.claim(kind="literature", evidence=refs)
        self.assertEqual(validate_project(self.root), [])
        self.claim(kind="empirical", evidence=refs)
        self.assertTrue(any("requires a validated experiment" in e for e in validate_project(self.root)))
        self.paper(reading_depth="abstract")
        self.claim(kind="literature", evidence=refs)
        self.assertTrue(any("requires partial or full_text" in e for e in validate_project(self.root)))

    def test_locator_and_candidate_lesson(self):
        self.paper()
        self.claim(kind="literature", evidence=[{"type": "paper", "id": "P1", "locator": "invented location"}])
        self.assertTrue(any("locator is not registered" in e for e in validate_project(self.root)))
        self.ledger("claims", [])
        lesson = {"id": "L1", "lesson": "Candidate strategy", "conditions": "When models disagree", "evidence": []}
        self.ledger("lessons", [lesson])
        self.assertEqual(validate_project(self.root), [])
        lesson["evidence_strength"] = "observed"
        self.ledger("lessons", [lesson])
        self.assertTrue(any("requires evidence" in e for e in validate_project(self.root)))

    def test_external_artifact_paths_rejected(self):
        for artifact in ("../outside.json", "/tmp/outside.json", "C:\\outside.json", "outputs/../outside.json"):
            with self.subTest(artifact=artifact):
                self.experiment(evidence_status="validated", artifacts=[artifact])
                self.assertTrue(any("inside the workspace" in e for e in validate_project(self.root)))

    def test_explicit_parent_relative_project_target(self):
        result = subprocess.run(
            [sys.executable, str(SKILL_SCRIPTS / "init_project.py"), "--path", "../sibling-project", "--domain", "Domain", "--objective", "Objective"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(validate_project(Path(self.temp.name) / "sibling-project"), [])

    def test_symlinks_rejected_when_platform_allows(self):
        link = Path(self.temp.name) / "linked-project"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted on this platform")
        with self.assertRaises(ValueError):
            init_project(link, "Domain", "Objective")
        self.assertTrue(any("symlink" in e for e in validate_project(link)))
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text("Real external data", encoding="utf-8")
        (self.root / "outputs").mkdir()
        (self.root / "outputs" / "result.json").symlink_to(outside)
        self.experiment(evidence_status="validated")
        self.assertTrue(any("symlink" in e for e in validate_project(self.root)))

    def test_validator_cli(self):
        result = subprocess.run([sys.executable, str(SKILL_SCRIPTS / "validate_project.py"), "--path", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("does not certify scientific truth", result.stdout)


class InstallerTests(unittest.TestCase):
    def test_installer_copies_only_skill_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("Test skill", encoding="utf-8")
            (source / "scripts").mkdir()
            (source / "scripts" / "tool.py").write_text("pass\n", encoding="utf-8")
            target = installer.install(root / "skills", source)
            self.assertTrue((target / "scripts" / "tool.py").is_file())
            self.assertEqual(list((root / "skills").iterdir()), [target])
            with self.assertRaises(FileExistsError):
                installer.install(root / "skills", source)
            self.assertEqual((target / "SKILL.md").read_text(), "Test skill")

    def test_bad_source_never_creates_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "empty-source"
            source.mkdir()
            with self.assertRaises(ValueError):
                installer.install(root / "skills", source)
            self.assertFalse((root / "skills").exists())

    def test_explicit_parent_relative_install_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            child = root / "child"
            child.mkdir()
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install.py"), "--dest", "../skills"],
                cwd=child, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "skills" / "research-loop" / "SKILL.md").is_file())

    def test_installer_rejects_source_symlinks_when_platform_allows(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("Test skill", encoding="utf-8")
            outside = root / "outside.txt"
            outside.write_text("External data", encoding="utf-8")
            try:
                (source / "linked.txt").symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation not permitted on this platform")
            with self.assertRaises(ValueError):
                installer.install(root / "skills", source)
            self.assertFalse((root / "skills").exists())

    def test_installed_script_works_without_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = installer.install(root / "skills")
            project = root / "research"
            result = subprocess.run([sys.executable, str(target / "scripts" / "init_project.py"), "--path", str(project), "--domain", "Example", "--objective", "An explicit question"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(validate_project(project), [])


if __name__ == "__main__":
    unittest.main()
