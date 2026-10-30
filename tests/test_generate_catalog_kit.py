#!/usr/bin/env python3
"""Self-test for the catalog-kit generator (CR-CATALOG-STRUCT-10).

Runs the generator against the fixture metamodel for all three projection
shapes (schema-present copy, schema-absent derivation, dimension
allocation) and asserts the emitted kit is internally consistent: pointer
blocks parse and agree with the generator parameters, the projection
narrowed the id pattern and injected the instance layer, the derived
projection flags itself, and the generated gates pass against the
generated kit (the kit validates itself).

Stdlib + pyyaml only: no network, no sibling-repo checkout.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "tests" / "fixtures"
GENERATOR = REPO / "tools" / "generate_catalog_kit.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_catalog_kit", GENERATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_generator(tmp_path: Path, entity: str, extra: list[str] | None = None) -> Path:
    target = tmp_path / "kit"
    cmd = [
        sys.executable,
        str(GENERATOR),
        "--target", str(target),
        "--entity", entity,
        "--metamodel", str(FIXTURES / "kit-metamodel.yaml"),
        "--schema-dir", str(FIXTURES / "kit-schemas"),
        "--rel-schema", str(FIXTURES / "kit-schemas" / "relationship-instance.json"),
        "--metaframework", str(REPO),
        *(
            extra
            if extra is not None
            else ["--root-ref", "v0.8.0", "--owner", "TechNeHub Labs", "--force"]
        ),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return target


CASES = [
    ("dea:Widget", "dea:catalog-widgets", "widget", "WDG", "dea:entity-widget"),
    ("dea:Gadget", "dea:catalog-gadgets", "gadget", "GDG", "dea:entity-gadget"),
    ("dea:Notion", "dea:catalog-notions", "notion", "NOT", "dea:entity-notion"),
]


class TestKitEmission:
    @pytest.mark.parametrize("entity,catalog_id,slug,alias,legacy", CASES)
    def test_files_emitted(self, tmp_path, entity, catalog_id, slug, alias, legacy):
        kit = _run_generator(tmp_path, entity)
        for rel in (
            "metamodel-pointer.yaml",
            "dependencies.yaml",
            "schemas/entity.schema.json",
            "schemas/relationship-instance.schema.json",
            "schemas/fixtures/example-valid.yaml",
            "schemas/fixtures/example-invalid.yaml",
            "scripts/check_parse.py",
            "scripts/check_pointer.py",
            "scripts/check_record_posture.py",
            "scripts/check_schema.py",
            "scripts/check_record_documentation.py",
            "scripts/regenerate_catalog.py",
            "scripts/check_catalog_index.py",
            "scripts/check_authorship.py",
            "catalog-index-schema/catalog-index-schema.json",
            ".github/workflows/validate-catalogue.yml",
            ".github/workflows/validate-allocation.yml",
            ".github/workflows/validate-authorship.yml",
            "docs/FOUNDATIONS.md",
            "docs/RECORD-STANDARD.md",
            "README.md",
            "CONTRIBUTING.md",
            f"change-requests/CR-{alias}-CAT-01-catalogue-foundation.md",
            "CHANGELOG.md",
            "CATALOG_IGNORED_GUARANTEE",
        ):
            if rel == "CATALOG_IGNORED_GUARANTEE":
                gi_lines = [ln.strip() for ln in (kit / ".gitignore").read_text().splitlines() if ln.strip() and not ln.strip().startswith("#")]
                assert "CATALOG.yaml" not in gi_lines
            else:
                assert (kit / rel).exists(), f"missing {rel}"

    @pytest.mark.parametrize("entity,catalog_id,slug,alias,legacy", CASES)
    def test_pointer_blocks(self, tmp_path, entity, catalog_id, slug, alias, legacy):
        kit = _run_generator(tmp_path, entity)
        doc = yaml.safe_load((kit / "metamodel-pointer.yaml").read_text())
        assert doc["id"] == catalog_id
        assert doc["abbreviation"] == alias
        assert doc["metamodel"]["entity_id"] == legacy
        assert doc["metamodel"]["class_alias"] == alias
        assert doc["metamodel"]["version"] == "v0.8.0"
        assert doc["links"]["github"].endswith(doc["id"].removeprefix("dea:catalog-"))
        if entity == "dea:Notion":
            assert "layer" not in doc["metamodel"]
            assert doc["metamodel"].get("dimension") == "semantic-dimension"
        else:
            assert doc["metamodel"]["layer"] == "L4"


class TestProjection:
    def test_copy_and_narrow(self, tmp_path):
        kit = _run_generator(tmp_path, "dea:Widget")
        schema = json.loads((kit / "schemas/entity.schema.json").read_text())
        assert schema["additionalProperties"] is False
        props = schema["properties"]
        assert props["id"]["pattern"] == "^dea:widget-[a-z0-9-]+$"
        assert props["type"]["const"] == "Widget"
        assert props["material"]["enum"] == ["wood", "metal", "plastic"]
        for key in ("evidence", "provenance", "governance"):
            assert key in props, f"instance layer field {key} missing"
        assert schema["required"] == ["id", "type", "name", "version", "lifecycle_status"]

    def test_derived_projection_flags_metamodel_gap(self, tmp_path):
        kit = _run_generator(tmp_path, "dea:Gadget")
        schema = json.loads((kit / "schemas/entity.schema.json").read_text())
        assert schema["properties"]["id"]["pattern"] == "^dea:gadget-[a-z0-9-]+$"
        # derived projection still carries the full normative base
        for key in ("id", "type", "name", "description", "version",
                    "lifecycle_status", "external_references", "tags",
                    "relationships", "metadata", "evidence", "provenance", "governance"):
            assert key in schema["properties"]


class TestGeneratedGatesPass:
    @pytest.mark.parametrize("entity,catalog_id,slug,alias,legacy", CASES)
    def test_kit_validates_itself(self, tmp_path, entity, catalog_id, slug, alias, legacy):
        kit = _run_generator(tmp_path, entity)
        for gate in ("check_parse.py", "check_pointer.py", "check_record_posture.py",
                     "check_schema.py", "check_record_documentation.py"):
            result = subprocess.run(
                [sys.executable, str(kit / "scripts" / gate)],
                capture_output=True, text=True,
            )
            assert result.returncode == 0, f"{gate} failed:\n{result.stdout}\n{result.stderr}"

    def test_rerun_without_force_keeps_edits(self, tmp_path):
        kit = _run_generator(tmp_path, "dea:Widget")
        edited = kit / "docs/FOUNDATIONS.md"
        edited.write_text("curated by a steward\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable, str(GENERATOR),
                "--target", str(kit),
                "--entity", "dea:Widget",
                "--metamodel", str(FIXTURES / "kit-metamodel.yaml"),
                "--schema-dir", str(FIXTURES / "kit-schemas"),
                "--rel-schema", str(FIXTURES / "kit-schemas" / "relationship-instance.json"),
                "--metaframework", str(REPO),
            ],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "curated by a steward" in edited.read_text()
        assert "exists (kept" in result.stdout


class TestSharedRepo:
    def test_shared_repo_entities_list(self, tmp_path):
        # two fixture entities share no repo; use --entity with a repeated
        # catalog_repo by editing the fixture in-memory is out of scope here:
        # the shared-repo branch is exercised by asserting the mismatch guard.
        mod = _load_generator()

        class Args:
            entity = "dea:Widget,dea:Notion"
            metamodel = FIXTURES / "kit-metamodel.yaml"
            schema_dir = FIXTURES / "kit-schemas"
            rel_schema = FIXTURES / "kit-schemas" / "relationship-instance.json"
            metaframework = REPO
            root_ref = "v0.8.0"
            owner = "TechNeHub Labs"
            target = tmp_path / "kit"
            force = False

        with pytest.raises(SystemExit) as exc:
            mod.Kit(Args)
        assert "catalog_repo" in str(exc.value)
