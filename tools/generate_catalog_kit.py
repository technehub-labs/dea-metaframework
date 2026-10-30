#!/usr/bin/env python3
"""Catalog kit generator (org-wide catalog advancement programme, Wave 0).

Emits the standard S1-S3 standup kit for a DEA catalog repository, derived
from the canonical metamodel. The kit is the "IA standard" proven on
dea-catalog-information-assets (CR-IA-CAT-01..03): hybrid metamodel pointer,
dependency manifest, schema projection + vendored relationship-instance
contract, fixtures, gates 1-6, three CI workflows, FOUNDATIONS + RECORD-
STANDARD, README contract, CONTRIBUTING, CR register, and a drafted
foundation CR. Population (S4) is intentionally NOT generated: admissions
are evidence-driven and land as the repo's CR-02.

Projection strategy per entity:
  - the metamodel entity schema is copied and narrowed (id pattern,
    required set, additionalProperties false) with the catalogue-instance
    layer (evidence/provenance/governance) injected;
  - entities whose metamodel artifacts are null (no schema yet) get a
    derived minimal projection from the entity definition itself, and the
    generator flags them for a metamodel schema-backfill CR.

Dimension-allocated entities (no layer) emit the dimension pointer shape
(metamodel.dimension + scope_layers) validated by the same reusable
workflow (ADR-0002 D1).

Usage:
  python3 generate_catalog_kit.py \\
      --target PATH \\
      --entity dea:Primary[,dea:Shared...] \\
      --metamodel ../dea-metamodel/metamodel/dea-metamodel.yaml \\
      --schema-dir ../dea-metamodel/schemas/entities \\
      --rel-schema   ../dea-metamodel/schemas/relationships/relationship-instance.json \\
      --metaframework ../dea-metaframework \\
      [--root-ref v0.8.0] [--owner "TechNeHub Labs"] [--force]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

LIFECYCLE_ENUM = ["proposed", "planned", "active", "deprecated", "retired"]

PARSE_GATE = '''#!/usr/bin/env python3
"""Gate 1: every tracked YAML and JSON file must parse.

Runs the whole tree, not just entities: the catalogue's pointer, schema,
and documentation must parse even before records exist, and a record that
lands with malformed YAML should fail here rather than downstream.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent


def main() -> int:
    bad = 0
    checked = 0

    for pattern in ("**/*.yaml", "**/*.yml"):
        for f in glob.glob(str(REPO / pattern), recursive=True):
            if "/.git/" in f:
                continue
            checked += 1
            try:
                yaml.safe_load(open(f, encoding="utf-8"))
            except Exception as exc:
                print(f"FAIL: {Path(f).relative_to(REPO)} does not parse as YAML: {exc}")
                bad += 1

    for f in glob.glob(str(REPO / "**/*.json"), recursive=True):
        if "/.git/" in f:
            continue
        checked += 1
        try:
            json.load(open(f, encoding="utf-8"))
        except Exception as exc:
            print(f"FAIL: {Path(f).relative_to(REPO)} does not parse as JSON: {exc}")
            bad += 1

    print(f"Files checked: {checked}")
    print(f"Findings: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
'''
BASE_PROPS = {
    "external_references": {
        "type": "array",
        "description": "Identifiers in external systems. Never a substitute for the OpenDEAM id (E004).",
        "items": {
            "type": "object",
            "required": ["system", "identifier"],
            "properties": {"system": {"type": "string"}, "identifier": {"type": "string"}},
        },
    },
    "tags": {"type": "array", "items": {"type": "string"}},
    "metadata": {
        "type": "object",
        "description": "Metamodel base-entity metadata.",
        "properties": {
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "created_by": {"type": "string"},
            "status": {"type": "string"},
        },
    },
}

INSTANCE_LAYER = {
    "evidence": {
        "type": "object",
        "description": "Catalogue-instance layer. The source the record derives from; admission requires at least one source and a rationale.",
        "required": ["sources", "rationale"],
        "additionalProperties": False,
        "properties": {
            "sources": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["kind", "reference"],
                    "additionalProperties": False,
                    "properties": {
                        "kind": {
                            "type": "string",
                            "enum": ["repository-path", "system-of-record", "published-document"],
                            "description": "Kind of evidence: a path in a technehub-labs repository, an identified system of record, or a published document.",
                        },
                        "reference": {"type": "string", "minLength": 1},
                    },
                },
            },
            "rationale": {"type": "string", "minLength": 1},
        },
    },
    "provenance": {
        "type": "object",
        "description": "Catalogue-instance layer. Ladder passage from proposal to canonical admission (FOUNDATIONS admission ladder).",
        "required": ["ladder_passage"],
        "additionalProperties": False,
        "properties": {
            "ladder_passage": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["stage", "date", "actor"],
                    "additionalProperties": False,
                    "properties": {
                        "stage": {
                            "type": "string",
                            "enum": ["candidate", "corroborated", "reviewed", "canonical"],
                            "description": "Admission ladder stages (FOUNDATIONS D-4).",
                        },
                        "date": {"type": "string", "description": "ISO date (quoted in YAML so it stays a string)."},
                        "actor": {"type": "string", "description": "Authorship-bearing field (AUT rules)."},
                    },
                },
            }
        },
    },
    "governance": {
        "type": "object",
        "description": "Catalogue-instance layer. Ownership and review state.",
        "required": ["functional_owner", "steward", "approval_status"],
        "properties": {
            "functional_owner": {"type": "string"},
            "steward": {"type": "string"},
            "approval_status": {"type": "string", "enum": ["proposed", "under_review", "approved"]},
            "review_date": {"type": "string"},
            "source_and_evidence": {"type": "string"},
        },
    },
}


def kebab(name: str) -> str:
    s = re.sub(r"(?<!^)(?=[A-Z])", "-", name)
    return s.lower()


def load_entities(metamodel_path: Path) -> dict[str, dict]:
    data = yaml.safe_load(metamodel_path.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data["entities"] if isinstance(e, dict)}


class Kit:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.entities = load_entities(args.metamodel)
        self.ids = [e.strip() for e in args.entity.split(",")]
        self.records = [self.entities[i] for i in self.ids]
        self.primary = self.records[0]
        self.repo = self.primary["catalog_repo"]
        for r in self.records:
            if r["catalog_repo"] != self.repo:
                sys.exit(f"ERROR: {r['id']} catalog_repo {r['catalog_repo']} != {self.repo}")
        self.alias = self.primary["class_alias"]
        legacy = self.primary.get("legacy_ids") or []
        m = re.match(r"dea:entity-(.+)", legacy[0]) if legacy else None
        self.slug = m.group(1) if m else kebab(self.primary["name"])
        self.entity_name = self.primary["name"]
        self.catalog_id = "dea:catalog-" + self.repo.removeprefix("dea-catalog-")
        self.cr = f"CR-{self.alias}-CAT"
        self.target = Path(args.target)
        self.flagged: list[str] = []
        self.written: list[str] = []

    # ---------- helpers ----------

    def write(self, rel: str, content: str) -> None:
        path = self.target / rel
        if path.exists() and not self.args.force:
            self.flagged.append(f"exists (kept, --force to overwrite): {rel}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.written.append(rel)

    def copy(self, rel: str, src: Path) -> None:
        path = self.target / rel
        if path.exists() and not self.args.force:
            self.flagged.append(f"exists (kept, --force to overwrite): {rel}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, path)
        self.written.append(rel)

    # ---------- kit components ----------

    def pointer(self) -> None:
        p = self.primary
        dim = p.get("layer") is None
        mm: dict[str, Any] = {
            "version": self.args.root_ref,
            "entity_id": (p.get("legacy_ids") or [None])[0],
            "class_alias": self.alias,
            "viewer_url": f"https://technehub-labs.github.io/metamodel/?entity={self.alias}",
        }
        if dim:
            mm["dimension"] = p.get("dimension") or "measurement-dimension"
        else:
            mm["layer"] = p["layer"]
            if p.get("building_block"):
                mm["building_block"] = p["building_block"]
        extra = ""
        if len(self.records) > 1:
            entries = []
            for r in self.records[1:]:
                e = {"entity_id": (r.get("legacy_ids") or [None])[0], "class_alias": r["class_alias"]}
                if r.get("layer"):
                    e["layer"] = r["layer"]
                    if r.get("building_block"):
                        e["building_block"] = r["building_block"]
                entries.append(yaml.safe_dump(e, sort_keys=True, default_flow_style=False).strip())
            extra = "\nentities:\n" + "\n".join(f"  {yaml.safe_dump({'entity_id': (r.get('legacy_ids') or [''])[0], 'class_alias': r['class_alias'], **({'layer': r['layer']} if r.get('layer') else {}), **({'building_block': r['building_block']} if r.get('building_block') else {})}, sort_keys=True, default_flow_style=False).replace('\n', '\n  ')}" for r in self.records[1:])
        defn = " ".join((p.get("definition") or "").split())
        lines = [
            f"# Metamodel Pointer — {self.entity_name}",
            "#",
            "# Two consumers, two blocks (see FOUNDATIONS §5):",
            "#   - the top-level identity keys are consumed by the vendored",
            "#     regenerate_catalog.py to build CATALOG.yaml's catalog block;",
            "#   - the `metamodel:` allocation block is validated by",
            "#     dea-architecture-framework validate-against-model.yml",
            f"#     against the pinned root-model ref ({self.args.root_ref}), and asserted",
            "#     locally by scripts/check_pointer.py.",
            "#",
            "# Allocation changes go through the root model, not this file.",
            f"id: {self.catalog_id}",
            f"name: {self.entity_name}",
            f"abbreviation: {self.alias}",
            "version: 0.1.0",
            "status: active",
            "metamodel_version: 1.0.0",
            f"owner: {self.args.owner}",
            "description: |",
            f"  {defn}",
            "metamodel:",
        ]
        mm_dump = yaml.safe_dump(mm, sort_keys=True, default_flow_style=False).rstrip("\n")
        lines.extend("  " + ln if ln else ln for ln in mm_dump.splitlines())
        lines.append("links:")
        lines.append("  metamodel_repo: https://github.com/technehub-labs/dea-metamodel")
        lines.append("  root_model: https://github.com/technehub-labs/dea-architecture-framework")
        lines.append(f"  viewer: https://technehub-labs.github.io/metamodel/?entity={self.alias}")
        lines.append(f"  github: https://github.com/technehub-labs/{self.repo}")
        content = "\n".join(lines) + "\n" + (extra + "\n" if extra else "")
        self.write("metamodel-pointer.yaml", content)

    def dependencies(self) -> None:
        content = f"""# Catalog dependency manifest ({self.cr}-01).
#
# Schema follows the dea-catalog-business-capabilities precedent
# (CR-DEA-BC-05). Catalog pins move to tag pins at each target's first
# post-reset release cut.

metamodel_pin: 1.0.0

# The metamodel-pointer.yaml `metamodel:` block is validated against this
# OpenDEAM ref (validate-allocation.yml).
root_model_pin: {self.args.root_ref}

# Shared toolchain pin: regenerate_catalog.py, check_catalog_index.py,
# check_authorship.py and the index schema are vendored from this
# dea-metaframework release tag.
metaframework_pin: v2.6.0
"""
        self.write("dependencies.yaml", content)

    def projection_schema(self) -> None:
        src = None
        declared = (self.primary.get("artifacts") or {}).get("json_schema")
        if declared:
            candidate = Path(declared)
            src = candidate if candidate.exists() else (self.args.schema_dir / candidate.name)
        if src and src.exists():
            schema = json.loads(src.read_text(encoding="utf-8"))
            schema_source = "copied-and-narrowed"
        else:
            schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": f"{self.entity_name} (catalogue instance schema)",
                "type": "object",
                "required": ["id", "type", "name", "version", "lifecycle_status"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "name": {"type": "string", "minLength": 1, "maxLength": 200},
                    "description": {"type": "string", "maxLength": 2000},
                    "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                    "lifecycle_status": {"type": "string", "enum": LIFECYCLE_ENUM},
                    "external_references": {"type": "array", "items": {"type": "object", "required": ["system", "identifier"], "properties": {"system": {"type": "string"}, "identifier": {"type": "string"}}}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "relationships": {"type": "array", "items": {"$ref": "relationship-instance.schema.json"}},
                    "metadata": {"type": "object", "properties": {"created_at": {"type": "string"}, "updated_at": {"type": "string"}, "created_by": {"type": "string"}, "status": {"type": "string"}}},
                },
            }
            schema_source = "derived-from-entity-definition"
            self.flagged.append(
                f"metamodel schema absent for {self.primary['id']} ({self.slug}); projection derived from the "
                f"entity definition. A metamodel schema-backfill CR should add schemas/entities/{self.slug}.json."
            )
        schema["$id"] = f"https://technehub-labs.github.io/{self.repo}/schemas/entity.schema.json"
        schema["metamodel_source"] = f"https://github.com/technehub-labs/dea-metamodel/blob/main/schemas/entities/{self.slug}.json"
        schema["metamodel_version"] = "1.0.0"
        schema["title"] = f"{self.entity_name} (catalogue instance schema)"
        schema["description"] = (
            f"Catalogue-instance projection of the metamodel {self.entity_name} entity. The normative field set is "
            "defined by the metamodel schema; this file mirrors it and adds only the catalogue-instance layer "
            "(evidence, provenance ladder, governance). Do not widen a normative enum here to accept a value the "
            "metamodel does not define: fix the record instead. A catalogue that diverges from the metamodel is a "
            "second source of truth."
        )
        schema["additionalProperties"] = False
        props = schema.setdefault("properties", {})
        props["id"] = {
            "type": "string",
            "pattern": f"^dea:{self.slug}-[a-z0-9-]+$",
            "description": "OpenDEAM-local identifier, narrowed to this entity's namespace (information-classes id precedent).",
        }
        props["type"] = {"type": "string", "const": self.entity_name}
        props["lifecycle_status"] = {"type": "string", "enum": LIFECYCLE_ENUM, "description": "CR-3R: lifecycle state from metamodel/vocabularies/lifecycle.yaml."}
        rel = props.get("relationships")
        if not isinstance(rel, dict) or "$ref" not in (rel.get("items") or {}):
            props["relationships"] = {
                "type": "array",
                "description": "Typed relationship instances asserted by this record (metamodel relationship-instance contract).",
                "items": {"$ref": "relationship-instance.schema.json"},
            }
        for key, block in {**BASE_PROPS, **INSTANCE_LAYER}.items():
            props.setdefault(key, block)
        std5 = ["id", "type", "name", "version", "lifecycle_status"]
        extras = [r for r in schema.get("required", []) if r not in std5]
        schema["required"] = std5 + extras
        self.write("schemas/entity.schema.json", json.dumps(schema, indent=2, ensure_ascii=False) + "\n")
        self.projection_source = schema_source

    def fixtures(self) -> None:
        valid = f"""# Valid fixture: exercises the normative field set, the catalogue-instance
# layer, and one typed relationship instance. Illustrative ids only.
id: dea:{self.slug}-example-record
type: {self.entity_name}
name: Example {self.entity_name}
description: 'Fixture: an illustrative {self.entity_name.lower()} record demonstrating the canonical shape; not admitted.'
version: 1.0.0
lifecycle_status: active
tags:
  - fixture
evidence:
  sources:
    - kind: repository-path
      reference: schemas/fixtures/example-valid.yaml
  rationale: 'Fixture: demonstrates the record shape; not admitted.'
provenance:
  ladder_passage:
    - stage: candidate
      date: '2026-11-02'
      actor: Emmanuel A. Otchere
    - stage: canonical
      date: '2026-11-02'
      actor: Emmanuel A. Otchere
governance:
  functional_owner: Emmanuel A. Otchere
  steward: Emmanuel A. Otchere
  approval_status: approved
relationships:
  - id: dea:relationship-example-{self.slug}
    source_id: dea:{self.slug}-example-record
    target_id: dea:example-target-record
    relationship_type: references
    direction: source-to-target
    rationale: 'Fixture: illustrative typed assertion.'
    provenance:
      type: manual
      asserted_by: Emmanuel A. Otchere
      asserted_at: '2026-11-02'
      verification_status: verified
metadata:
  created_at: '2026-11-02'
  updated_at: '2026-11-02'
  created_by: Emmanuel A. Otchere
  status: active
"""
        self.write("schemas/fixtures/example-valid.yaml", valid)
        invalid = f"""# Invalid fixture: must FAIL validation (wrong namespace, wrong type
# const, widened lifecycle value, non-semver version, missing evidence,
# relationship instance without required fields).
id: dea:information-class-not-a-{self.slug.replace('-', '_')}
type: Not{self.entity_name.replace(' ', '')}
name: Example Invalid Record
version: not-semver
lifecycle_status: superseded
relationships:
  - source_id: dea:{self.slug}-example-record
"""
        self.write("schemas/fixtures/example-invalid.yaml", invalid)

    def gates(self) -> None:
        # Repo-agnostic parse gate (embedded template)
        self.write("scripts/check_parse.py", PARSE_GATE)

        pointer_gate = f'''#!/usr/bin/env python3
"""Gate 2: metamodel-pointer.yaml is present and internally consistent.

The pointer carries two blocks with two consumers (FOUNDATIONS §5): the
top-level identity keys (consumed by regenerate_catalog.py) and the
`metamodel:` allocation block (validated by validate-against-model.yml
against the pinned root-model ref and asserted here).

A finding here means the pointer drifted from its allocation. Fix the
allocation in dea-architecture-framework, not this file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent

REQUIRED_IDENTITY_FIELDS = (
    "id", "name", "abbreviation", "version", "status",
    "metamodel_version", "owner", "description",
)
REQUIRED_METAMODEL_FIELDS = (
    "version", "entity_id", "class_alias", "viewer_url",
)

EXPECTED_ID = "{self.catalog_id}"
EXPECTED_ABBREVIATION = "{self.alias}"
EXPECTED_METAMODEL_VERSION = "{self.args.root_ref}"
EXPECTED_ENTITY_ID = "{(self.primary.get('legacy_ids') or [''])[0]}"
EXPECTED_CLASS_ALIAS = "{self.alias}"
{f"EXPECTED_LAYER = {self.primary['layer']!r}" if self.primary.get("layer") else "# dimension-allocated entity: no layer expected"}


def main() -> int:
    findings: list[str] = []

    path = REPO / "metamodel-pointer.yaml"
    if not path.exists():
        print("FAIL: metamodel-pointer.yaml is missing")
        print("Findings: 1")
        return 1

    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {{}}

    for field in REQUIRED_IDENTITY_FIELDS:
        if field not in doc:
            findings.append(f"missing identity field: {{field}}")

    if doc.get("id") != EXPECTED_ID:
        findings.append(f"id is {{doc.get('id')!r}}, expected {{EXPECTED_ID!r}}")
    if doc.get("abbreviation") != EXPECTED_ABBREVIATION:
        findings.append(f"abbreviation is {{doc.get('abbreviation')!r}}, expected {{EXPECTED_ABBREVIATION!r}}")

    mm = doc.get("metamodel") or {{}}
    for field in REQUIRED_METAMODEL_FIELDS:
        if field not in mm:
            findings.append(f"missing metamodel field: {{field}}")

    if mm.get("entity_id") != EXPECTED_ENTITY_ID:
        findings.append(f"metamodel.entity_id is {{mm.get('entity_id')!r}}, expected {{EXPECTED_ENTITY_ID!r}}")
    if mm.get("class_alias") != EXPECTED_CLASS_ALIAS:
        findings.append(f"metamodel.class_alias is {{mm.get('class_alias')!r}}, expected {{EXPECTED_CLASS_ALIAS!r}}")
{"    if mm.get(\"layer\") != EXPECTED_LAYER:" + chr(10) + "        findings.append(f\"metamodel.layer is {mm.get(\'layer\')!r}, expected {EXPECTED_LAYER!r}\")" if self.primary.get("layer") else ""}
    version = str(mm.get("version", ""))
    if not re.fullmatch(r"v\\d+\\.\\d+\\.\\d+(-[a-z0-9.]+)?", version):
        findings.append(f"metamodel.version {{version!r}} is not a well-formed pin (vX.Y.Z[-tag])")

    links = doc.get("links") or {{}}
    for link in ("metamodel_repo", "root_model", "github"):
        if link not in links:
            findings.append(f"missing links.{{link}}")

    if findings:
        for f in findings:
            print(f"FAIL: {{f}}")
        print(f"Findings: {{len(findings)}}")
        return 1

    print("OK: pointer present and internally consistent")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        self.write("scripts/check_pointer.py", pointer_gate)

        posture = f'''#!/usr/bin/env python3
"""Gate 3: records-directory posture.

Records may not appear before the schema and documentation gates exist;
every record that lands carries the canonical identifier form and type.
Population is gated on the population CR ({self.cr}-02+).
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/*.yaml"

REQUIRED_POPULATION_GATES = (
    "scripts/check_schema.py",
    "scripts/check_record_documentation.py",
)

CANONICAL_ID = re.compile(r"dea:{self.slug}-[a-z0-9-]+")


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    records = [r for r in records if "/research/" not in r and "/retired/" not in r]
    print(f"Record count: {{len(records)}}")

    if not records:
        print("  OK: no records admitted; population is gated on the population CR")
        print("Findings: 0")
        return 0

    missing = [g for g in REQUIRED_POPULATION_GATES if not (REPO / g).exists()]
    if missing:
        print("Records are present but the population gates are incomplete:")
        for g in missing:
            print(f"  - FAIL: {{g}} is missing")
        print(f"Findings: {{len(missing)}}")
        return 1

    findings: list[str] = []
    for f in records:
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {{}}
        rid = doc.get("id") or ""
        if not CANONICAL_ID.fullmatch(rid):
            findings.append(f"{{Path(f).relative_to(REPO)}}: id {{rid!r}} is not a canonical {self.entity_name} id")
        rtype = doc.get("type") or ""
        if rtype != "{self.entity_name}":
            findings.append(f"{{Path(f).relative_to(REPO)}}: type {{rtype!r}} is not {self.entity_name!r}")

    if findings:
        print("Posture findings:")
        for f in findings:
            print(f"  - FAIL: {{f}}")
        print(f"Findings: {{len(findings)}}")
        return 1

    print(f"  OK: {{len(records)}} record(s) carry canonical identifiers and type")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        self.write("scripts/check_record_posture.py", posture)

        # schema gate: embed expectations from the projection we just emitted
        proj = json.loads((self.target / "schemas/entity.schema.json").read_text(encoding="utf-8"))
        enum_fields = {
            k: v.get("enum")
            for k, v in (proj.get("properties") or {}).items()
            if isinstance(v, dict) and isinstance(v.get("enum"), list) and k != "lifecycle_status"
        }
        enum_lines = "\n".join(
            f"EXPECTED_{k.upper()}_ENUM = {json.dumps(v)}"
            for k, v in enum_fields.items()
        )
        check_flag = "    if FIXTURE_INVALID.exists():" if True else ""
        schema_gate = f'''#!/usr/bin/env python3
"""Gate 4: the catalogue schema is a faithful projection of the metamodel
schema, and every record validates against it.

Expected values are embedded from dea-metamodel v1.0.0 by the kit
generator; bump them in the same CR that bumps metamodel_pin in
dependencies.yaml. Never widen a normative enum locally.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator
from referencing import Registry, Resource

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "entity.schema.json"
REL_SCHEMA_PATH = REPO / "schemas" / "relationship-instance.schema.json"
REL_SCHEMA_URI = f"https://technehub-labs.github.io/{self.repo}/schemas/relationship-instance.schema.json"
FIXTURE_VALID = REPO / "schemas" / "fixtures" / "example-valid.yaml"
FIXTURE_INVALID = REPO / "schemas" / "fixtures" / "example-invalid.yaml"
RECORD_GLOB = "entities/v1-alpha/**/*.yaml"

EXPECTED_TYPE_CONST = "{self.entity_name}"
EXPECTED_LIFECYCLE_ENUM = {json.dumps(LIFECYCLE_ENUM)}
EXPECTED_REQUIRED = {json.dumps(proj.get("required"))}
EXPECTED_ID_PATTERN = "^dea:{self.slug}-[a-z0-9-]+$"
{enum_lines}


def build_validator() -> Draft7Validator:
    schema = json.load(SCHEMA_PATH.open(encoding="utf-8"))
    rel_schema = json.load(REL_SCHEMA_PATH.open(encoding="utf-8"))
    registry = Registry().with_resource(REL_SCHEMA_URI, Resource.from_contents(rel_schema))
    return Draft7Validator(schema, registry=registry)


def check_projection() -> list[str]:
    if not SCHEMA_PATH.exists():
        return ["entity.schema.json is missing"]
    schema = json.load(SCHEMA_PATH.open(encoding="utf-8"))
    props = schema.get("properties") or {{}}
    findings: list[str] = []
    if schema.get("type") != "object":
        findings.append("type is not object")
    if schema.get("additionalProperties") is not False:
        findings.append("additionalProperties is not false")
    if schema.get("required") != EXPECTED_REQUIRED:
        findings.append(f"required is {{schema.get('required')!r}}")
    if props.get("type", {{}}).get("const") != EXPECTED_TYPE_CONST:
        findings.append("type const mismatch")
    if props.get("lifecycle_status", {{}}).get("enum") != EXPECTED_LIFECYCLE_ENUM:
        findings.append("lifecycle_status enum mismatch")
    if props.get("id", {{}}).get("pattern") != EXPECTED_ID_PATTERN:
        findings.append("id pattern mismatch")
    for field, expected in {json.dumps(enum_fields)}.items():
        got = (props.get(field) or {{}}).get("enum")
        if got != expected:
            findings.append(f"{{field}} enum drift")
    rel = props.get("relationships")
    if not rel or "$ref" not in (rel.get("items") or {{}}):
        findings.append("relationships items must $ref relationship-instance.schema.json")
    return findings


def main() -> int:
    findings = check_projection()
    if findings:
        for f in findings:
            print(f"FAIL: {{f}}")
        print(f"Findings: {{len(findings)}}")
        return 1

    validator = build_validator()

    if FIXTURE_VALID.exists():
        doc = yaml.safe_load(FIXTURE_VALID.read_text(encoding="utf-8"))
        errs = sorted(validator.iter_errors(doc), key=str)
        if errs:
            findings.append("valid fixture does not validate: " + "; ".join(e.message for e in errs[:3]))
    else:
        findings.append("valid fixture is missing")

{check_flag}
        doc = yaml.safe_load(FIXTURE_INVALID.read_text(encoding="utf-8"))
        errs = sorted(validator.iter_errors(doc), key=str)
        if not errs:
            findings.append("invalid fixture validates (it must not)")
    else:
        findings.append("invalid fixture is missing")

    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    records = [r for r in records if "/research/" not in r and "/retired/" not in r]
    for f in records:
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {{}}
        errs = sorted(validator.iter_errors(doc), key=str)
        if errs:
            findings.append(f"{{Path(f).relative_to(REPO)}}: " + "; ".join(e.message for e in errs[:3]))

    if findings:
        for f in findings:
            print(f"FAIL: {{f}}")
        print(f"Findings: {{len(findings)}}")
        return 1

    print(f"OK: projection faithful; {{len(records)}} record(s) validate; fixtures behave")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        self.write("scripts/check_schema.py", schema_gate)

        doc_gate = f'''#!/usr/bin/env python3
"""Gate 5: record documentation standard.

Validates every canonical record against the machine-checkable subset of
docs/RECORD-STANDARD.md. Until records exist, exits clean.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/*.yaml"

REQUIRED_SECTIONS = (
    "## Identity",
    "## Evidence",
    "## Classification-or-relationships",
    "## Provenance",
    "## Governance",
)
KNOWN_SOURCE_KINDS = {{"repository-path", "system-of-record", "published-document"}}


def check_record(path: Path) -> list[str]:
    findings: list[str] = []
    rel = path.relative_to(REPO)
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {{}}

    description = str(doc.get("description") or "").strip()
    if len(description) < 40:
        findings.append(f"{{rel}}: description is too thin to satisfy the standard (>= 40 chars)")

    evidence = doc.get("evidence") or {{}}
    rationale = str(evidence.get("rationale") or "").strip()
    if len(rationale) < 20:
        findings.append(f"{{rel}}: evidence.rationale is too thin (>= 20 chars)")
    sources = evidence.get("sources") or []
    if not sources:
        findings.append(f"{{rel}}: no evidence sources")
    for s in sources:
        if s.get("kind") not in KNOWN_SOURCE_KINDS:
            findings.append(f"{{rel}}: evidence source kind {{s.get('kind')!r}} is not known")

    rels = doc.get("relationships") or []

    readme = path.parent / "README.md"
    if not readme.exists():
        findings.append(f"{{rel}}: per-record README.md is missing")
        return findings

    text = readme.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            findings.append(f"{{readme.relative_to(REPO)}}: missing section {{section!r}}")

    blockquotes = [ln[2:].strip() for ln in text.splitlines() if ln.startswith("> ")]
    if not blockquotes:
        findings.append(f"{{readme.relative_to(REPO)}}: no definition blockquote")
    elif blockquotes[0] != description:
        findings.append(f"{{readme.relative_to(REPO)}}: definition blockquote does not match record description verbatim")

    if not rels:
        relsec = text.split("## Classification-or-relationships", 1)[-1]
        if "Deferred:" not in relsec:
            findings.append(f"{{rel}}: no relationship instances and no explicit deferral in README")

    return findings


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    records = [Path(r) for r in records if "/research/" not in r and "/retired/" not in r]
    print(f"Record count: {{len(records)}}")

    findings: list[str] = []
    for path in records:
        findings.extend(check_record(path))

    if findings:
        for f in findings:
            print(f"FAIL: {{f}}")
        print(f"Findings: {{len(findings)}}")
        return 1

    print("OK: documentation standard satisfied" + (f" ({{len(records)}} records)" if records else " (no records yet)"))
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        self.write("scripts/check_record_documentation.py", doc_gate)

        # vendor shared toolchain + index schema + authorship
        mf = Path(self.args.metaframework)
        self.copy("scripts/regenerate_catalog.py", mf / "tools/regenerate_catalog.py")
        self.copy("scripts/check_catalog_index.py", mf / "tools/check_catalog_index.py")
        self.copy("scripts/check_authorship.py", mf / "scripts/check_authorship.py")
        self.copy("catalog-index-schema/catalog-index-schema.json", mf / "tools/catalog-index-schema.json")
        if not (self.target / "reconciliation/authorship-fields.yaml").exists():
            self.copy("reconciliation/authorship-fields.yaml", mf / "reconciliation/authorship-fields.yaml")
        else:
            self.flagged.append("exists (kept): reconciliation/authorship-fields.yaml")

    def workflows(self) -> None:
        catalogue = f"""name: validate-catalogue

# The catalogue gates ({self.cr}-01): parse, pointer, posture, CATALOG
# freshness, schema projection + record validation, record documentation.

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    name: catalogue
    runs-on: ubuntu-latest
    steps:
      # Full history: the regenerator's last_modified field resolves from
      # git last-commit dates per record path; a shallow checkout collapses
      # them and the freshness gate drifts.
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Set canonical git origin URL (regenerator reads it)
        run: |
          git remote set-url origin "https://github.com/${{GITHUB_REPOSITORY}}.git"
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install pyyaml jsonschema referencing
      - name: "Step 1: YAML and JSON parsing"
        run: python3 scripts/check_parse.py
      - name: "Step 2: Pointer present and internally consistent"
        run: python3 scripts/check_pointer.py
      - name: "Step 3: Records directory posture"
        run: python3 scripts/check_record_posture.py
      - name: "Step 4: CATALOG.yaml freshness and validation"
        run: |
          python3 scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json
          python3 scripts/check_catalog_index.py --strict --schema catalog-index-schema/catalog-index-schema.json
      - name: "Step 5: Schema projection and record validation"
        run: python3 scripts/check_schema.py
      - name: "Step 6: Record documentation standard"
        run: python3 scripts/check_record_documentation.py
"""
        self.write(".github/workflows/validate-catalogue.yml", catalogue)

        allocation = f"""name: validate-allocation

# Pins this catalog's allocation declaration (metamodel-pointer.yaml)
# against the OpenDEAM root model. Drift fails CI.

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  allocation:
    uses: technehub-labs/dea-architecture-framework/.github/workflows/validate-against-model.yml@{self.args.root_ref}
    with:
      model_ref: {self.args.root_ref}
      pointer_file: metamodel-pointer.yaml
"""
        self.write(".github/workflows/validate-allocation.yml", allocation)

        authorship = """name: validate-authorship

# Authorship Cardinal Rule gate (CR-BP-118; AUT-001..003). Vendored copies
# preferred; pinned metaframework fetch as fallback.

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  authorship:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Fetch dea-metaframework (pinned; fallback for vendored copies)
        uses: actions/checkout@v4
        with:
          repository: technehub-labs/dea-metaframework
          ref: v2.6.0
          path: .metaframework
      - name: Prefer vendored gate copies
        run: |
          set -euo pipefail
          if [ ! -f scripts/check_authorship.py ]; then
            cp .metaframework/scripts/check_authorship.py scripts/
          fi
          if [ ! -f reconciliation/authorship-fields.yaml ]; then
            cp .metaframework/reconciliation/authorship-fields.yaml reconciliation/
          fi
      - name: Authorship Cardinal Rule gate (AUT-001..003)
        run: python3 scripts/check_authorship.py --strict
"""
        self.write(".github/workflows/validate-authorship.yml", authorship)

    def docs(self) -> None:
        defn = " ".join((self.primary.get("definition") or "").split())
        foundations = f"""# Foundations: {self.entity_name} Catalog

This document records the method the catalogue follows: cardinal scope,
exclusions, admission criteria, allocation, cross-catalogue policy, and the
decision register. The record documentation standard
([RECORD-STANDARD.md](RECORD-STANDARD.md)) and the schema projection carry
the operational contract.

## 1. Cardinal scope

**{self.entity_name}** — {defn}

## 2. What is deliberately excluded

Boundaries against sibling entity types are governed by the metamodel
definitions; anything that is not a {self.entity_name.lower()} record
belongs to its owning catalogue (see the metamodel's `catalog_repo`
allocations).

## 3. Admission criteria and evidence ladder

1. The record describes a {self.entity_name.lower()} per the metamodel definition.
2. At least one evidence source verifiably exists at admission time
   (`repository-path`, `system-of-record`, or `published-document`).
3. Relationship instances are asserted only against canonical target ids
   that exist; absence is honest (no local substitutes).

Evidence ladder (asserted in `provenance.ladder_passage`):
candidate → corroborated → reviewed → canonical.

## 4. Allocation

`{(self.primary.get('legacy_ids') or [''])[0]}` (alias `{self.alias}`), {"layer " + str(self.primary.get('layer')) + " / " + str(self.primary.get('building_block')) if self.primary.get('layer') else "dimension-allocated (no home layer)"}, pinned against
OpenDEAM {self.args.root_ref}. Validated remotely by `validate-allocation.yml`
and locally by Gate 2. Upstream pins live in `dependencies.yaml`.

## 5. Cross-catalogue reference policy

1. Crosswalks and references are recorded on the asserting record's side,
   as typed relationship instances (metamodel relationship-instance
   contract).
2. Assertions wait for canonical targets: no scheme invention where a
   sibling id scheme does not exist.
3. Gates never resolve remote repositories; vendored registry snapshots
   carry the offline contract where a specific target family is asserted.

## 6. Decision-points register

| # | Decision | Status |
|---|---|---|
| D-1 | Methodology-first bring-up: no records before the kit and population CR | Adopted ({self.cr}-01) |
| D-2 | Hybrid pointer: identity keys for the regenerator + `metamodel:` allocation block for the root-model validator | Adopted ({self.cr}-01) |
| D-3 | Record ids take the `dea:{self.slug}-<slug>` form (information-classes `dea:`-prefix precedent) | Adopted ({self.cr}-01) |
| D-4 | Admission ladder: candidate → corroborated → reviewed → canonical | Adopted ({self.cr}-01) |
| D-5 | Evidence-only admission: no record without a verifiable source; population plans document the wait | Adopted ({self.cr}-01) |
| D-6 | `CATALOG.yaml` is committed, not ignored (template deviation): the freshness gate diffs the committed index | Adopted ({self.cr}-01) |

## 7. Population plan

Initial population is evidence-gated. Candidate seed sources are named in
the population CR; where none are verifiable today, the catalogue stays at
zero canonical records with this section recording why and what would
unlock population.
"""
        self.write("docs/FOUNDATIONS.md", foundations)

        standard = f"""# Record Documentation Standard ({self.cr}-01)

Every canonical {self.entity_name} record must satisfy this standard. Gate 6
(`scripts/check_record_documentation.py`) enforces the machine-checkable
subset; steward review enforces the rest.

## 1. Record file

One record per subtree: `entities/v1-alpha/<id>/<id>.yaml`, where `<id>` is
the canonical id (`dea:{self.slug}-<slug>`). Obligations beyond the schema:

1. `name` is the real name as consumers know it.
2. `description` states what the record is and its consuming purpose — not
   a restatement of the name.
3. `evidence.sources` cites at least one verifiable source; `rationale`
   says why it justifies admission.
4. `provenance.ladder_passage` records passage to canonical with quoted
   dates and authorship-bearing actors (AUT rules).
5. Relationship instances are asserted only against canonical targets, or
   the README carries an explicit `Deferred:` note.

## 2. YAML conventions

- Dates single-quoted so they stay strings.
- Apostrophes escaped (`''`) in single-quoted prose; double quotes when the
  prose contains a colon.

## 3. Per-record README

Sections: `# <Name>` + verbatim definition blockquote, `## Identity`,
`## Evidence`, `## Classification-or-relationships`, `## Provenance`,
`## Governance`. The definition blockquote must equal the record's
`description` verbatim (Gate 6 checks).

## 4. Change discipline

Record changes land through CRs; a record edit regenerates `CATALOG.yaml`
in the same PR. Retired records move to `retired/`, never deleted.
"""
        self.write("docs/RECORD-STANDARD.md", standard)

        readme = f"""# {self.entity_name}

> {defn}

**Layer:** {self.primary.get('layer') or 'cross-cutting dimension'} : **Entity:** `{self.primary['id']}` (class alias `{self.alias}`) : **Root model:** [OpenDEAM {self.args.root_ref}](https://github.com/technehub-labs/dea-architecture-framework) : **Metamodel:** [v1.0.0](https://github.com/technehub-labs/dea-metamodel)

**Owner:** {self.args.owner}

[![View in Metamodel Explorer](https://img.shields.io/badge/Metamodel%20Explorer-View%20Entity-2C3E50?style=shield)](https://technehub-labs.github.io/metamodel/?entity={self.alias})

## Status

**Foundation.** Kit landed by `{self.cr}-01` (generated by
`dea-metaframework/tools/generate_catalog_kit.py`, the CR-IA-CAT-01..03
standard). Population is evidence-gated; see `docs/FOUNDATIONS.md` §7.

| Item | State |
|---|---|
| Metamodel pointer | hybrid (identity + allocation blocks), pinned to OpenDEAM {self.args.root_ref} |
| Dependency manifest | `dependencies.yaml`: metamodel 1.0.0, root model {self.args.root_ref}, metaframework v2.6.0 |
| Schema projection | metamodel v1.0.0 projection + catalogue-instance layer |
| Record documentation standard | `docs/RECORD-STANDARD.md`, Gate 6 |
| Population | gated on the population CR |
| Generated index | `CATALOG.yaml`, regenerator + strict gate in CI |

## What this catalogue is

The owning catalogue for {self.entity_name.lower()} records: {defn}

## What this catalogue is not

Boundaries are governed by the metamodel entity definitions and the
sibling `catalog_repo` allocations; anything outside this entity type
belongs to its owning catalogue.

## Catalogue structure

```
{self.repo}/
├── metamodel-pointer.yaml           ← entity allocation (identity + metamodel blocks)
├── dependencies.yaml                ← upstream pins
├── CATALOG.yaml                     ← machine-generated index (do not hand-edit)
├── docs/                            ← FOUNDATIONS.md, RECORD-STANDARD.md
├── schemas/                         ← entity.schema.json, relationship-instance.schema.json, fixtures/
├── scripts/                         ← gates 1-6 + vendored shared toolchain
├── entities/v1-alpha/               ← records (population gated)
├── reconciliation/                  ← authorship-fields.yaml (+ registries)
└── .github/workflows/               ← validate-catalogue, validate-allocation, validate-authorship
```

## Local validation

```bash
python3 scripts/check_parse.py
python3 scripts/check_pointer.py
python3 scripts/check_record_posture.py
python3 scripts/regenerate_catalog.py --schema catalog-index-schema/catalog-index-schema.json
python3 scripts/check_catalog_index.py --strict --schema catalog-index-schema/catalog-index-schema.json
python3 scripts/check_schema.py
python3 scripts/check_record_documentation.py
python3 scripts/check_authorship.py --strict
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Every change lands through a
change request; the authorship cardinal rule is gate-enforced.
"""
        self.write("README.md", readme)

        contributing = f"""# Contributing to {self.repo}

## Change control

Every change lands through a change request (CR) in `change-requests/`
carried by a pull request against `main`. CR format follows the house
pattern (metadata table, numbered sections, out-of-scope list, verifiable
acceptance criteria); every CR registers a row in `change-requests/README.md`.

## Workflow

1. Branch: `feat/{self.cr}-NN-short-title`.
2. Implement; regenerate the index when entity content changes.
3. Run the gates locally (README §Local validation). All must print `Findings: 0`.
4. Open a pull request; CI runs the same gates plus the allocation
   validator and the authorship gate.
5. Verify checks are green before merge.

## Authorship cardinal rule

Every authorship-bearing field carries `Emmanuel A. Otchere` or
`TechNeHub Labs` — never an agent or tool name (AUT-001..003 gate).

## Pointer and index discipline

`metamodel-pointer.yaml` allocation changes go through the root model.
`CATALOG.yaml` is machine-generated; regenerate, never hand-edit.
"""
        self.write("CONTRIBUTING.md", contributing)

    def cr_docs(self) -> None:
        cr_file = f"{self.cr}-01-catalogue-foundation.md"
        content = f"""# {self.cr}-01: {self.entity_name} Catalogue Foundation

| Field | Value |
|---|---|
| **CR** | {self.cr}-01 |
| **Title** | {self.entity_name} catalogue foundation (kit bring-up) |
| **Status** | Landed |
| **Layer** | Catalogue ({self.primary.get('layer') or 'cross-cutting'}) |
| **Programme** | Org-wide catalog advancement |
| **Repository** | `technehub-labs/{self.repo}` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-02 |
| **Depends on** | dea-metaframework catalog-kit generator CR |
| **Trigger** | Org-wide catalog advancement programme: advance this repository from initial state to the reputable-foundation standard with initial entities to follow under evidence-only admission. |

## 1. Executive summary

This CR lands the standard catalogue kit (the CR-IA-CAT-01..03 standard,
machine-generated): hybrid pointer pinned to OpenDEAM {self.args.root_ref},
dependency manifest, schema projection ({getattr(self, 'projection_source', 'metamodel')}) with the
catalogue-instance layer, vendored relationship-instance contract, fixtures,
gates 1-6, three CI workflows, FOUNDATIONS with the decision register, the
record documentation standard, README contract, and CONTRIBUTING. No
records are admitted; population is evidence-gated ({self.cr}-02).

## 2. Scope

In scope: everything under `metamodel-pointer.yaml`, `dependencies.yaml`,
`schemas/`, `scripts/`, `docs/`, `.github/workflows/`, `README.md`,
`CONTRIBUTING.md`, `CHANGELOG.md`, this CR and the register. The template
`ci.yml` is superseded by the three named workflows. `CATALOG.yaml` is
committed (template `.gitignore` deviation, D-6).

Out of scope: record population; metamodel changes; sibling catalogues.

## 3. Acceptance criteria

1. All six local gates print `Findings: 0`.
2. `validate-against-model` passes against OpenDEAM {self.args.root_ref}.
3. Authorship gate conformant.
4. `CATALOG.yaml` regenerated and committed (0 entities).

## 4. NOT-list

1. No records admitted.
2. No vocabulary widened beyond the metamodel.
3. No remote resolution in any gate.
"""
        self.write(f"change-requests/{cr_file}", content)

        register = f"""# Change Requests: {self.repo}

This index tracks every change request that lands on this repository.

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [{self.cr}-01]({cr_file}) | Catalogue foundation (kit bring-up) | Landed (this PR) | Standard kit: pointer, dependencies, schema projection, gates 1-6, workflows, FOUNDATIONS, record standard. No records admitted. |
| {self.cr}-02 | Initial population | Planned | Evidence-gated seed population per FOUNDATIONS §7. |

## Numbering

Series tag `{self.cr}-NN`, sequential. Cross-repo CRs that touch this
repository are recorded here with their home-repo identifier.
"""
        self.write("change-requests/README.md", register)

    def changelog(self) -> None:
        existing = self.target / "CHANGELOG.md"
        entry = f"""### `{self.cr}-01` — catalogue foundation (kit bring-up)

Standard kit generated from the metamodel (org-wide catalog advancement
programme): hybrid pointer pinned to OpenDEAM {self.args.root_ref};
`dependencies.yaml`; schema projection ({getattr(self, 'projection_source', 'metamodel')}) with the
catalogue-instance layer; vendored relationship-instance contract; fixtures;
gates 1-6 wired into `validate-catalogue.yml` plus allocation and authorship
workflows; FOUNDATIONS (D-1..D-6) and record documentation standard. No
records admitted (population gated on {self.cr}-02).
"""
        if existing.exists():
            text = existing.read_text(encoding="utf-8")
            if "## [Unreleased]" in text:
                text = text.replace("## [Unreleased]\n", "## [Unreleased]\n\n" + entry, 1)
            else:
                text = "# Changelog\n\n## [Unreleased]\n\n" + entry + "\n" + text
            if not self.args.force and "CHANGELOG.md" not in self.written:
                existing.write_text(text, encoding="utf-8")
                self.written.append("CHANGELOG.md")
        else:
            self.write("CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n\n" + entry)

    # ---------- orchestration ----------

    def scaffold_dirs(self) -> None:
        for d in ("classifications", "contributions", "entities/v1-alpha"):
            p = self.target / d
            if not p.exists():
                p.mkdir(parents=True, exist_ok=True)
                (p / ".gitkeep").write_text("", encoding="utf-8")
                self.written.append(f"{d}/.gitkeep")
        gi = self.target / ".gitignore"
        fixed = (
            "# Python\n__pycache__/\n*.pyc\n\n# Editor\n.vscode/\n.idea/\n*.swp\n.DS_Store\n\n"
            "# Test\n.pytest_cache/\n\n"
            "# Generated - CATALOG.yaml is COMMITTED, not ignored: the freshness gate\n"
            "# (regenerate_catalog.py --check) diffs the committed index (catalog\n"
            "# repository standard par. 6; IC/BC/IA precedent).\n"
        )
        if not gi.exists():
            gi.write_text(fixed, encoding="utf-8")
            self.written.append(".gitignore")
        elif "CATALOG.yaml" in gi.read_text(encoding="utf-8"):
            gi.write_text(fixed, encoding="utf-8")
            self.flagged.append(".gitignore: template ignore of CATALOG.yaml removed")

    def run(self) -> None:
        self.scaffold_dirs()
        self.pointer()
        self.dependencies()
        self.projection_schema()
        self.fixtures()
        self.copy("schemas/relationship-instance.schema.json", Path(self.args.rel_schema))
        self.gates()
        self.workflows()
        self.docs()
        self.cr_docs()
        self.changelog()
        print(f"Kit for {self.entity_name} ({self.repo}) written to {self.target}")
        print(f"  primary: {self.primary['id']} (alias {self.alias}, slug {self.slug})")
        if len(self.records) > 1:
            print(f"  shared with: {', '.join(r['id'] for r in self.records[1:])}")
        print(f"  files written: {len(self.written)}")
        for f in self.written:
            print(f"    + {f}")
        if self.flagged:
            print("  flags:")
            for f in self.flagged:
                print(f"    ! {f}")
        print("Next steps: review/curate FOUNDATIONS scope + CR-01 narrative, remove the")
        print("template ci.yml if present, fix .gitignore (un-ignore CATALOG.yaml),")
        print("regenerate CATALOG.yaml, run all gates, land CR-01; then CR-02 population.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", required=True, type=Path)
    ap.add_argument("--entity", required=True, help="primary entity id; comma-separate for shared repos")
    ap.add_argument("--metamodel", required=True, type=Path)
    ap.add_argument("--schema-dir", type=Path, help="defaults to <metamodel>/../schemas/entities")
    ap.add_argument("--rel-schema", type=Path, help="defaults to <metamodel>/../schemas/relationships/relationship-instance.json")
    ap.add_argument("--metaframework", required=True, type=Path)
    ap.add_argument("--root-ref", default="v0.8.0")
    ap.add_argument("--owner", default="TechNeHub Labs")
    ap.add_argument("--force", action="store_true", help="overwrite existing kit files")
    args = ap.parse_args()

    if not args.schema_dir:
        args.schema_dir = args.metamodel.parent.parent / "schemas" / "entities"
    if not args.rel_schema:
        args.rel_schema = args.metamodel.parent.parent / "schemas" / "relationships" / "relationship-instance.json"

    Kit(args).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
