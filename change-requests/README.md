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
| [CR-ECF-006](./CR-ECF-006.md) | ECF Domain Transformation (v2.3.0 restructure) | Merged (PR #24) | Five of seven Domains renamed; one Domain replaced (Supply & Resources -> Strategy & Direction). Backed by ADR-ECF-001 (five-tests rubric: Semantic Anchor, Lifecycle Completeness, Boundary Integrity, Technology Independence, Collective Exhaustiveness). Non-breaking SemVer-wise (v2.3.0, not v3.0.0): the seven-Domain cardinality is unchanged, the matrix M = D x S still defines 49 coordinates, and the no-cell-filling rule still applies. Breaking for downstream consumers that hard-code the v2.2.0 Domain names; downstream reconciliation CRs (CR-MM-ECF-01, CR-BC-ECF-01, CR-BP-ECF-01) are the migration carriers. |
| [CR-ECF-007](./CR-ECF-007.md) | Rename Domain 3: People & Organization -> Agency & Organization (v2.4.0) | Proposed (this PR) | One of seven Domains renamed; Domain 3 only. Driven by the Substrate Independence Stress Test (ADR-ECF-002 §5): the domain must remain semantically valid whether the enterprise's internal agents are biological (humans), artificial (AI systems, autonomous software agents), or hybrid. `People` is biologically loaded and fails the Technology Independence test; `Agency` is the substrate-independent term. No content redistribution required (CR-ECF-007 §6.3): all content that previously belonged to `People & Organization` remains in `Agency & Organization`. Backed by ADR-ECF-002 (Domain Semantic Integrity Contract; MECE re-audit; AI-Agent Stress Test; OTCHERE Inc. scenario test). Non-breaking for matrix topology (v2.4.0, not v3.0.0): the seven-Domain cardinality is unchanged. Breaking for downstream consumers that hard-code `PeopleAndOrganization` / `peopleAndOrganization` / `people-organization`; backward-compat aliases preserved in `tools/ecf_coordinates.py:DOMAIN_ALIASES` for at least 2 release cycles. Downstream migration carriers: CR-MM-ECF-02 (dea-metamodel), CR-BC-17-...-v2.4.0 (dea-catalog-business-capabilities), CR-BP-18 (dea-catalog-processes). |

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
| [CR-CATALOG-STRUCT-07a](./CR-CATALOG-STRUCT-07a.md) | Cross-Repo Consumer Module | Proposed | First PR of the STRUCT-07 stack. `tools/cross_repo_consumer/` exposes `Catalog`, `CatalogEntity`, `CatalogCounts`, `CatalogMetadata` dataclasses + `fetch_catalog_yaml()` (stdlib urllib, no new deps) + `parse_catalog_yaml()` + a CLI. Stdlib-only; one ~29-test pytest module. 07b + 07c land separately against the viewer and AF. |

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

## ADR series

Architecture Decision Records (ADRs) record the design decisions behind
this framework. ADRs are immutable once landed; they are cited by CRs
when those decisions are implemented.

| ADR | Title | Status | Notes |
|-----|-------|--------|-------|
| [ADR-ECF-001](./ADR-ECF-001.md) | ECF Domain Specifications: Normative Descriptions Update | Merged (PR #24) | The design decision behind CR-ECF-006. Introduces the five-tests rubric (Semantic Anchor, Lifecycle Completeness, Boundary Integrity, Technology Independence, Collective Exhaustiveness) used to assess each Domain, and records the rationale for each rename. Landed as authored. |
| [ADR-ECF-002](../docs/adr/ADR-ECF-002.md) | ECF Domain Semantic Integrity & Substrate Independence | Proposed (this PR) | The design decision behind CR-ECF-007. Records the Normative Principle for domain naming, the Domain Semantic Integrity Contract (10 requirements: single semantic anchor, stable subject, noun-based, departmentalization-independent, technology-substrate-independent, lifecycle-complete, boundary-explicit, cross-domain relationships, internal MECE partition, no generic outcome ownership), the AI-Agent Stress Test that proves the rename holds for a workforce consisting entirely of AI agents, and the OTCHERE Inc. scenario test that validates the new domain set remains MECE. Three candidates evaluated for Domain 3 (`People & Organization`, `Workforce & Organization`, `Agency & Organization`); `Agency & Organization` selected. Landed as authored. |

## Conventions

- Sequential: one CR (or CR milestone) per PR; the next CR is parked until the
  current one merges.
- Land as authored: landed CR files are byte-identical to the source document
  section.
- Docs style: no en/em dashes in authored text (colons/semicolons instead);
  Design Specification tone.
