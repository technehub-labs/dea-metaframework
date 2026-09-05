# Change Requests

Change requests governing the Enterprise Concept Framework
(`technehub-labs/dea-metaframework`). ECF-series CRs land in this repository;
cross-references point at the canonical CR repository (`dea-metamodel`).

## ECF series

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-ECF-001](./CR-ECF-001.md) | ECF Architectural Reconciliation | Merged (PR #4) | Positions ECF as an OpenDEA organizing framework/profile; establishes WSF -> OpenDEA -> ECF -> Metamodel -> Catalogs; lands `framework/architecture.md`. |
| [CR-ECF-002](./CR-ECF-002.md) | ECF Semantic Boundary | Merged (PR #5) | Canonical definitions for Domain, Stage, Coordinate, Context; replaces container semantics with contextualization; capability identity and process topology boundaries. |
| [CR-ECF-003](./CR-ECF-003.md) | ECF Domain Grounding | Merged (PR #6) | Formal grounding records for the seven Domains; compound-name boundary audit; orthogonality and completeness checks; renaming rule. |
| [CR-ECF-004](./CR-ECF-004.md) | ECF Lifecycle Grounding | Merged (PR #7) | Per-Stage grounding records; Stage distinct from object State, process level, and DERA phase; existing DERA mapping retained as a mapping; multi-stage participation rule. |
| [CR-ECF-005](./CR-ECF-005.md) | ECF Coordinate Specification | Merged (PR #8) | The ECF Conformance Gate: canonical normative + machine-readable coordinate specification; canonical PascalCase Domain/Stage enums; identifier pattern; no-cell-filling rule; conformance requirements. |

## Conformance Gate series

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-ECF-CG-001](./CR-ECF-CG-001.md) | ECF Conformance Gate Definition | Proposed (this PR) | The umbrella: five conformance layers, four states, gate conditions, evidence, governance principle (the gate tests consumers; it does not modify the contract). |

## Catalog Structure series

Cross-repo **mandatory standard** applied by every TechNeHub Labs catalog repo (L1 layer). Established by CR-CATALOG-STRUCT-01 and enforced by CI gates + conformance tests + the new-repo template.

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-CATALOG-STRUCT-01](./CR-CATALOG-STRUCT-01.md) | Catalog Repository Standard (Four-State Per-Entity Subtrees + CATALOG.yaml Index) | Proposed (this PR) | Establishes the standard: four-state per-entity lifecycle, per-entity subtree shape, machine-generated CATALOG.yaml index, CI gate, conformance tests (CST-001..CST-015), new-repo template, retroactive adoption schedule. Lands `docs/standards/catalog-repository-pattern.md` + `docs/standards/catalog-repository-pattern-adoption.md`. |
| [CR-CATALOG-STRUCT-06a](./CR-CATALOG-STRUCT-06a.md) | CATALOG.yaml Regenerator + Gate + Schema | Proposed | The engine: JSON Schema (`tools/catalog-index-schema.json`), regenerator (`tools/regenerate_catalog.py`), gate (`tools/check_catalog_index.py`), and pytest self-test suite. Implements the standard's §6 contract. Adoption CRs (STRUCT-02..05) wire it into each catalog's CI; cross-repo conformance tests CST-001..CST-015 land in STRUCT-06b. |
| [CR-CATALOG-STRUCT-06b](./CR-CATALOG-STRUCT-06b.md) | Conformance Tests + New-Repo Template + Bootstrap Script | Proposed | The enforcement layer: CST-001..CST-016 (`tools/conformance_test_catalog_structure.py`), new-repo template (`tools/catalog-repo-template/`), bootstrap script (`tools/bootstrap_catalog_repo.py`), and worked example. Implements the standard's §8, §11, §12. Adoption CRs (STRUCT-02..05) now unblocked. |

Downstream CRs (STRUCT-02..STRUCT-07) are per-repo adoptions, the regenerator tool, and the cross-repo consumer. STRUCT-06 (regenerator + tests + template) MUST land before any adoption CR. STRUCT-07 (consumer) lands after STRUCT-02 + STRUCT-06.

Downstream gate CRs (CG-002..CG-006) land in dependency order; each ships with its own PR once CG-001 is merged.

Parked (landed in dependency order; each lands with its own PR):

| CR | Title | Depends on |
|----|-------|-----------|
| CR-ECF-002 | ECF Semantic Boundary | CR-ECF-001 |
| CR-ECF-003 | ECF Domain Grounding | CR-ECF-001, CR-ECF-002 |
| CR-ECF-004 | ECF Lifecycle Grounding | CR-ECF-002 |
| CR-ECF-005 | ECF Coordinate Specification | CR-ECF-002, CR-ECF-003, CR-ECF-004 |

## Cross-references

| CR | Title | Primary copy |
|----|-------|--------------|
| [CR-CM-000A](./CR-CM-000A-xref.md) | Terminology Alignment (extension) | `technehub-labs/dea-metamodel` |

## Conventions

- Sequential: one CR (or CR milestone) per PR; the next CR is parked until the
  current one merges.
- Land as authored: landed CR files are byte-identical to the source document
  section.
- Docs style: no en/em dashes in authored text (colons/semicolons instead);
  Design Specification tone.
