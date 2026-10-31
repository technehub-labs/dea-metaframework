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
| [CR-ECF-007](./CR-ECF-007.md) | Rename Domain 3: People & Organization -> Agency & Organization (v2.4.0) | Merged (PR #28) | One of seven Domains renamed; Domain 3 only. Driven by the Substrate Independence Stress Test (ADR-ECF-002 §5): the domain must remain semantically valid whether the enterprise's internal agents are biological (humans), artificial (AI systems, autonomous software agents), or hybrid. `People` is biologically loaded and fails the Technology Independence test; `Agency` is the substrate-independent term. No content redistribution required (CR-ECF-007 §6.3): all content that previously belonged to `People & Organization` remains in `Agency & Organization`. Backed by ADR-ECF-002 (Domain Semantic Integrity Contract; MECE re-audit; AI-Agent Stress Test; OTCHERE Inc. scenario test). Non-breaking for matrix topology (v2.4.0, not v3.0.0): the seven-Domain cardinality is unchanged. Breaking for downstream consumers that hard-code `PeopleAndOrganization` / `peopleAndOrganization` / `people-organization`; backward-compat aliases preserved in `tools/ecf_coordinates.py:DOMAIN_ALIASES` for at least 2 release cycles. Downstream migration carriers: CR-MM-ECF-02 (dea-metamodel), CR-BC-17-...-v2.4.0 (dea-catalog-business-capabilities), CR-BP-18 (dea-catalog-processes). |
| [CR-ECF-008](./CR-ECF-008.md) | Rename Domain 6: Operations & Enablement -> Enablement & Operations (v2.5.0) | Merged (PR #30) | One of seven Domains renamed; Domain 6 only. Driven by the Domain/Stage Orthogonality Stress Test (ADR-ECF-003 §5): the word `Operations` in the Domain 6 name shared a lexical root with Stage 5 `Operate`, obscuring the orthogonality that the ECF requires between the Domain axis and the Stage axis. The rename swaps the two nouns: `Enablement` now leads (lexically distinct from any Stage name) and `Operations` trails (the sustained day-to-day concern, not the lifecycle Stage). Backed by ADR-ECF-003 (lexical collision analysis, alternative-name evaluation, backward-compat policy). Unchanged: Domain number (6), matrix position (row 6), semantic anchor (`Execution`), axiomatic grounding ("persists" + "exchanging value"), domain scope, lifecycle applicability, seven-Domain partition, seven lifecycle Stages, Stage 5 name (`Operate`), and the `ECF = Domain × Stage = 49 coordinates` construction. Breaking for downstream consumers that hard-code `OperationsAndEnablement` / `operationsAndEnablement` / `operations-enablement`; backward-compat aliases preserved in `tools/ecf_coordinates.py:DOMAIN_ALIASES` for at least 2 release cycles. Downstream migration carriers: CR-MM-ECF-03 (dea-metamodel), CR-BC-ECF-03 (dea-catalog-business-capabilities), CR-BP-23 (dea-catalog-processes), CR-AR-FMWK-ECF-03 (dea-architecture-framework). |
| [CR-ECF-009](./CR-ECF-009-authorship-cardinal-rule.md) | Authorship Cardinal Rule (R1, R2) - Org-Wide Propagation Slice (dea-metaframework) | Merged (PR #35) | Org-wide propagation slice of the CR-BP-118 authorship cardinal rules. Blocking gate `scripts/check_authorship.py` (AUT-001..003), data-driven from `reconciliation/authorship-fields.yaml` (allowlist `{Emmanuel A. Otchere, TechNeHub Labs}`; denylist `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`). Retroactive sweep rewrites 4 files / 5 textual replacements; new CI workflow `.github/workflows/validate-authorship.yml` runs the gate in `--strict` on every push and PR. 21/21 `test_check_authorship` pass. Landed as authored. |
| [CR-ECF-010](./CR-ECF-010-entity-system-cross-reference.md) | Entity System Cross-Reference (Metaframework) | Merged (PR #36) | Metaframework cross-reference slice of the General Entity System institutionalisation (cross-repo cascade T7). The Metaframework repo is a metaframework (ECF + ADRs) repo; it does not contain entity records and does NOT adopt the entity-system gate. This PR records the cross-reference to `dea-governance` (DEA-ID-000 + CR-012) and enumerates the Metaframework repo's commitments to the General Entity System standard. D-004 clean. 118a/b/c authorship gates remain CONFORMANT. Follow-on: T8 legacy ID reconciliation. |
| [CR-ECF-011](./CR-ECF-011-regenerator-open-cr-counter.md) | Regenerator Open-CR Counter Fix (status tokens, both metadata shapes, org-consistent closed set) | **Proposed (this PR)** | `tools/regenerate_catalog.py` `count_open_change_requests` fixed at the source: status-token parser for both house metadata shapes (bold-line and table), closed set `{Merged, Landed, Applied, Accepted, Rejected, Superseded, Withdrawn}` (as landed downstream in CR-DEA-BC-38 / capabilities PR #91; superset of the CR-BP-114 set), duplicated `"Status**: Merged"` condition removed, first-status-line-wins so a carrier quoting a status line is classified by its metadata (observed on stakeholders CR-CATALOG-STRUCT-08). Conservative-open semantics preserved. 7 new machinery tests (20/20 dual-runner; full suite 90/90). Downstream: fixes already vendored per-repo in processes/capabilities/stakeholders; next release tag should carry this so re-vendor replaces divergence; services' data-side fix becomes belt-and-braces. |
| [CR-ECF-012](./CR-ECF-012-ecf-identifier-finalization.md) | ECF Coordinate Identifier Finalization (And-Stripped Convention) | **Proposed (this PR)** | Executes the CR-ECF-005 finalization deferral: DOMAIN_ID table (And-stripped six + enablementAndOperations exception) is normative; coordinate_identifier() builds from it; spec section 4 restated; 49 identifiers pinned in test_005; metamodel CR-MET-018 mirror test closes the dual-source-of-truth defect. Census: zero downstream consumers of the retired form. |

## Conformance Gate series

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-ECF-CG-001](./CR-ECF-CG-001.md) | ECF Conformance Gate Definition | Merged (PR #9) | The umbrella: five conformance layers, four states, gate conditions, evidence, governance principle (the gate tests consumers; it does not modify the contract). |

## Catalog Structure series

Cross-repo **mandatory standard** applied by every TechNeHub Labs catalog repo (L1 layer). Established by CR-CATALOG-STRUCT-01 and enforced by CI gates + conformance tests + the new-repo template.

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-CATALOG-STRUCT-01](./CR-CATALOG-STRUCT-01.md) | Catalog Repository Standard (Four-State Per-Entity Subtrees + CATALOG.yaml Index) | Merged (PR #10) | Establishes the standard: four-state per-entity lifecycle, per-entity subtree shape, machine-generated CATALOG.yaml index, CI gate, conformance tests (CST-001..CST-015), new-repo template, retroactive adoption schedule. Lands `docs/standards/catalog-repository-pattern.md` + `docs/standards/catalog-repository-pattern-adoption.md`. |
| [CR-CATALOG-STRUCT-06a](./CR-CATALOG-STRUCT-06a.md) | CATALOG.yaml Regenerator + Gate + Schema | Merged (PR #11) | The engine: JSON Schema (`tools/catalog-index-schema.json`), regenerator (`tools/regenerate_catalog.py`), gate (`tools/check_catalog_index.py`), and pytest self-test suite. Implements the standard's §6 contract. Adoption CRs (STRUCT-02..05) wire it into each catalog's CI; cross-repo conformance tests CST-001..CST-015 land in STRUCT-06b. |
| [CR-CATALOG-STRUCT-06b](./CR-CATALOG-STRUCT-06b.md) | Conformance Tests + New-Repo Template + Bootstrap Script | Merged (PR #12) | The enforcement layer: CST-001..CST-016 (`tools/conformance_test_catalog_structure.py`), new-repo template (`tools/catalog-repo-template/`), bootstrap script (`tools/bootstrap_catalog_repo.py`), and worked example. Implements the standard's §8, §11, §12. Adoption CRs (STRUCT-02..05) now unblocked. |
| [CR-CATALOG-STRUCT-07a](./CR-CATALOG-STRUCT-07a.md) | Cross-Repo Consumer Module | Merged (PR #19) | First PR of the STRUCT-07 stack. `tools/cross_repo_consumer/` exposes `Catalog`, `CatalogEntity`, `CatalogCounts`, `CatalogMetadata` dataclasses + `fetch_catalog_yaml()` (stdlib urllib, no new deps) + `parse_catalog_yaml()` + a CLI. Stdlib-only; one ~29-test pytest module. 07b + 07c land separately against the viewer and AF. |
| [CR-CATALOG-STRUCT-10](./CR-CATALOG-STRUCT-10-catalog-kit-generator.md) | Catalog Kit Generator | **Proposed (this PR)** | `tools/generate_catalog_kit.py`: machine-generates the full S1-S3 standup kit from the canonical metamodel (hybrid pointer for layer/dimension/shared-repo shapes, dependency manifest, schema projection copied-and-narrowed or derived-from-definition with flagging, fixtures, gates 1-6, three workflows, FOUNDATIONS/RECORD-STANDARD/README/CONTRIBUTING, CR register + drafted foundation CR). Population intentionally not generated (evidence-gated CR-02 per repo). 13-test suite with fixture metamodel; full suite 103 passed. Unblocks the org-wide catalog advancement programme. |

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
| [ADR-ECF-002](../docs/adr/ADR-ECF-002.md) | ECF Domain Semantic Integrity & Substrate Independence | Merged (PR #28) | The design decision behind CR-ECF-007. Records the Normative Principle for domain naming, the Domain Semantic Integrity Contract (10 requirements: single semantic anchor, stable subject, noun-based, departmentalization-independent, technology-substrate-independent, lifecycle-complete, boundary-explicit, cross-domain relationships, internal MECE partition, no generic outcome ownership), the AI-Agent Stress Test that proves the rename holds for a workforce consisting entirely of AI agents, and the OTCHERE Inc. scenario test that validates the new domain set remains MECE. Three candidates evaluated for Domain 3 (`People & Organization`, `Workforce & Organization`, `Agency & Organization`); `Agency & Organization` selected. Landed as authored. |
| [ADR-ECF-003](../docs/adr/ADR-ECF-003.md) | ECF Domain 6 Rename — Operations & Enablement → Enablement & Operations | Merged (PR #30) | The design decision behind CR-ECF-008. Records the lexical collision analysis (Domain 6 `Operations` vs Stage 5 `Operate` sharing a Latin root, obscuring the Domain/Stage orthogonality), the alternative-name evaluation (`Execution & Enablement`, `Delivery & Enablement`, `Means & Execution`, `Service Operations & Enablement`, `Operations & Infrastructure` — all rejected; minimum-change rename selected), the normative Domain/Stage distinction rule, the backward-compat alias policy (5 deprecated aliases mapped to the canonical value; catalog IDs unchanged), and the Domain Semantic Integrity Contract re-validation. |

## Conventions

- Sequential: one CR (or CR milestone) per PR; the next CR is parked until the
  current one merges.
- Land as authored: landed CR files are byte-identical to the source document
  section.
- Docs style: no en/em dashes in authored text (colons/semicolons instead);
  Design Specification tone.
