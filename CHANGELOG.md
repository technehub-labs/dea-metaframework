# Changelog

All notable changes to this repository are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository is
governed by change requests (`change-requests/`).

## [Unreleased]

No changes.

## [2.2.0] - 2026-09-07

The Catalog Repository Standard (four-state per-entity subtrees + machine
`CATALOG.yaml` index) with its regenerator, gate, conformance tests, new-repo
template and cross-repo consumer module, plus the per-repo adoption marks
across the five DEA catalog repositories.

### Added

#### Catalog Repository Standard (CR-CATALOG-STRUCT-01, -06a, -06b, -07a)

- `docs/standards/catalog-repository-pattern.md`: the standard. Four-state
  per-entity lifecycle (proposed / accepted / deprecated / retired), per-entity
  subtree shape, machine-generated `CATALOG.yaml` index, CI gate, conformance
  tests (CST-001..CST-015), and new-repo template. (CR-CATALOG-STRUCT-01)
- `docs/standards/catalog-repository-pattern-adoption.md`: the mandatory
  per-repo adoption schedule. (CR-CATALOG-STRUCT-01)
- `tools/catalog-index-schema.json`: JSON Schema draft-07 describing the
  `CATALOG.yaml` index file (CR-CATALOG-STRUCT-01 §6 contract).
  (CR-CATALOG-STRUCT-06a)
- `tools/regenerate_catalog.py`: machine regenerator for `CATALOG.yaml`.
  Reads filesystem; emits the index atomically; supports `--check`,
  `--dry-run`, `--verbose`. Deterministic, byte-stable, stdlib-only.
  (CR-CATALOG-STRUCT-06a)
- `tools/check_catalog_index.py`: gate that validates the committed
  `CATALOG.yaml` against the schema and runs structural sanity checks.
  `--strict` upgrades warnings to errors. (CR-CATALOG-STRUCT-06a)
- `tools/conformance_test_catalog_structure.py`: cross-repo conformance
  suite implementing CST-001..CST-015 (standard §11) plus CST-016
  (template-version diff, advisory by default). (CR-CATALOG-STRUCT-06b)
- `tools/bootstrap_catalog_repo.py`: hand-rolled bootstrap script (no
  Jinja, no cookiecutter). Copies the template, substitutes placeholders,
  writes metamodel-pointer.yaml and TEMPLATE_VERSION, optionally runs
  `git init` and `gh repo create`. (CR-CATALOG-STRUCT-06b)
- `tools/catalog-repo-template/`: the new-repo bootstrap source per
  standard §12. Ships TEMPLATE_VERSION (0.1.0), README, LICENSE, NOTICE,
  CITATION.cff, .gitignore, .github/workflows/ci.yml, and directory
  placeholders for entities, classifications, schemas, scripts,
  contributions, change-requests. (CR-CATALOG-STRUCT-06b)
- `tools/cross_repo_consumer/`: stdlib-only consumer module exposing
  `Catalog`, `CatalogEntity`, `CatalogCounts`, `CatalogMetadata` dataclasses
  and `fetch_catalog_yaml()` (stdlib urllib, no new deps) plus
  `parse_catalog_yaml()` and a CLI. (CR-CATALOG-STRUCT-07a)
- `tests/fixtures/catalog-conforming/`: a real catalog the conformance
  suite passes against. Includes canonical, candidate-only, and
  fully-retired entities; the regenerator + gate + schema copies; a CI
  workflow; and a generated CATALOG.yaml. (CR-CATALOG-STRUCT-06b)
- `tests/test_catalog_index_machinery.py`, `tests/test_conformance_catalog_structure.py`,
  `tests/conftest.py`, `tests/__init__.py`: pytest self-test suites (23 tests
  total) exercising the regenerator, gate, schema, bootstrap, and consumer
  against in-memory fixture catalogs.
- `change-requests/CR-CATALOG-STRUCT-01.md`, `CR-CATALOG-STRUCT-06a.md`,
  `CR-CATALOG-STRUCT-06b.md`, `CR-CATALOG-STRUCT-07a.md`: design, decisions,
  usage, CST map, and worked examples.

### Fixed

- `tools/regenerate_catalog.py`: bug fix in `read_canonical_yaml` to fall
  back to `retired/<file>.yaml` when no root canonical exists; bug fix in
  `infer_state` precedence 3/4 to use the loaded canonical's lifecycle when
  `canonical_path` is None. (CR-CATALOG-STRUCT-06b)
- `tools/regenerate_catalog.py`: strip embedded credentials (PATs) from
  authenticated git URLs before persisting them in `CATALOG.yaml` entries.

### Housekeeping

- Per-repo adoption marks for the Catalog Repository Standard
  (CR-CATALOG-STRUCT-02..05): `dea-catalog-processes` and
  `dea-catalog-business-capabilities` (partial then full), then
  `dea-catalog-digital-business-service-factory` and `dea-catalog-stakeholders`.
- STRUCT-07 substack closure: viewer integration smoke test
  (STRUCT-07b) and the architecture-framework smoke test (STRUCT-07c) marked
  merged; STRUCT-07 closed.
- `change-requests/README.md`: CR-CATALOG-STRUCT-01, -06a, -06b, -07a added;
  STRUCT-07 status set to Closed.

## [2.1.0] - 2026-09-01

The architectural reconciliation, semantic boundary, domain and lifecycle
grounding, and the ECF Coordinate Specification (the ECF Conformance Gate).

### Added

#### Architectural reconciliation and semantic boundary (CR-ECF-001, CR-ECF-002)

- `framework/architecture.md`: normative statement of the ECF architectural
  position (WSF -> OpenDEA -> ECF -> Metamodel -> Catalogs), the architectural
  boundary, the OpenDEA profile architecture, the downstream contract, and the
  downstream consumer registry. (CR-ECF-001)
- `change-requests/README.md`: ECF change request index and conventions.
  (CR-ECF-001)
- `change-requests/CR-ECF-001.md`: ECF Architectural Reconciliation, landed as
  authored. (CR-ECF-001)
- README: "Position in the Semantic and OpenDEA Architecture" section with the
  normative stack and boundary statement. (CR-ECF-001)
- `change-requests/CR-ECF-002.md`: ECF Semantic Boundary, landed as authored.
  (CR-ECF-002)
- `framework/constructs.md`: rewrote Definitions and How Constructs Relate;
  introduced canonical Domain/Stage/Coordinate/Context definitions and
  `contextualizes : Entity x Coordinate -> Context` notation; removed the
  `Cell_{d,s} = { objects: Entity[], caps: Capability[] }` container type and
  `decompose : Cell -> M` rule; renamed `state : Entity -> Stage` to
  `state : Entity -> State`; added explicit `state`/`stage` distinction.
  (CR-ECF-002)
- `framework/matrix.md`: reframed header from "every business object lives in
  one cell" to "49 coordinates; a coordinate is classification context, not
  entity container"; rewrote Construction Rules to use contextualization
  semantics, multi-coordinate participation, and capability-identity
  independence; renamed "Recursive Self-Similarity" to "Recursive
  Applicability" and decoupled ECF recursion from Business Process
  decomposition. (CR-ECF-002)

#### Domain and lifecycle grounding (CR-ECF-003, CR-ECF-004)

- `change-requests/CR-ECF-003.md`: ECF Domain Grounding, landed as authored.
  (CR-ECF-003)
- `framework/domain-grounding.md`: per-Domain grounding records (axiom
  grounding, semantic definition, included concerns, excluded concerns,
  adjacent Domains, boundary rules, evidence); compound-name boundary
  audit (verdicts per compound); orthogonality statement; completeness
  check against the grounding axiom; renaming rule (no rename without
  explicit evidence and governance). (CR-ECF-003)
- `change-requests/CR-ECF-004.md`: ECF Lifecycle Grounding, landed as authored.
  (CR-ECF-004)
- `framework/lifecycle-grounding.md`: per-Stage grounding records; Stage
  vs object-State distinction; Stage vs process-level independence;
  Stage vs DERA-phase mapping (as a mapping, not an identity); multi-stage
  participation rule; recursive applicability section. (CR-ECF-004)

#### ECF Coordinate Specification and Conformance Gate (CR-ECF-005, CR-ECF-CG-001)

- `change-requests/CR-ECF-005.md`: ECF Coordinate Specification, landed as
  authored. (CR-ECF-005)
- `specification/ecf-coordinates.md`: normative coordinate specification
  (formal definition, canonical representation, coordinate identity,
  Domain and Stage enumerations, coordinate metadata, contextual use,
  multiple coordinates, validation, no-cell-filling rule, conformance
  requirements, authority, pre-existing-schema reconciliation note).
  (CR-ECF-005)
- `schemas/ecf-domain.schema.json`: canonical PascalCase Domain enum.
  (CR-ECF-005)
- `schemas/ecf-stage.schema.json`: canonical Stage enum. (CR-ECF-005)
- `schemas/ecf-coordinate.schema.json`: coordinate object schema with
  optional identifier and label fields; identifier must match
  `ecf:<domain>.<stage>` pattern. (CR-ECF-005)
- `tools/ecf_coordinates.py`: enumeration tool (49 derivable
  coordinates), identifier builder, validator. (CR-ECF-005)
- `tests/conformance/test_005_coordinate_spec.py`: conformance suite
  enforcing canonical enums, the 49-derivable count, the identifier
  pattern, the no-cell-filling rule, validator behaviour, and the
  repository-wide payload scan. (CR-ECF-005)
- `tests/__init__.py`, `tests/conformance/__init__.py`: test package
  layout. (CR-ECF-005)
- `.github/workflows/ci.yml`: CI runs the conformance suite on push and
  pull_request. (CR-ECF-005)
- `change-requests/CR-ECF-CG-001.md`: ECF Conformance Gate Definition
  (proposal); the umbrella for the five conformance layers, four states,
  gate conditions, evidence, and the governance principle that the gate
  tests consumers and does not modify the contract.

### Changed

- README: ECF reframed from "conceptual skeleton beneath the DEA Metamodel" to
  an OpenDEA organizing framework/profile; the 49 matrix positions are
  described as coordinates that contextualize enterprise concepts, not cells
  that contain them. (CR-ECF-001)
- README: `REPORT.md` demoted from "single source of truth" to authoritative
  explanatory synthesis; normative authority identified as `framework/` plus
  CR-governed change requests. (CR-ECF-001)
- README: "Build on it" now names the actual downstream consumers
  (dea-metamodel ECF profile, business capability catalog, business process
  catalog); the stale `dea-catalog-taxonomy` claim removed; the DERA phase
  grouping is labelled a mapping, not an identity. (CR-ECF-001)
- REPORT section 21: rewritten as "Position in the TechNeHub Labs Ecosystem";
  the embedded organization snapshot removed in favour of portfolio
  references; the core relationship restated as "WSF grounds; OpenDEA
  specializes; ECF organizes; the metamodel represents; catalogs instantiate";
  subsection numbering corrected (20.x -> 21.x); domain-to-catalog and
  construct-to-entity tables marked as illustrative snapshots. (CR-ECF-001)
- REPORT section 22: closing positioning aligned with the CR-ECF-001
  architectural statement. (CR-ECF-001)
- REPORT section 6: introduced Domain/Stage/Coordinate/Context as ECF
  primitives before the named constructs; replaced the cell-snapshot
  relation with `Enterprise Concept contextualized by ECF Coordinate(s)`;
  added explicit `Capability != Process != Function != Activity != Task` and
  the recursion/process-decomposition independence statement. (CR-ECF-002)
- REPORT section 7.3: rewrote the MECE rationale to use contextualization
  semantics and the state/stage distinction. (CR-ECF-002)
- REPORT section 8.1: rewrote Construction Rules to remove "place objects in
  cells" and "one object, one primary cell"; "earliest initiation" downgraded
  to a catalog placement heuristic. (CR-ECF-002)
- REPORT section 8.4 and 8.5: recursive self-similarity reframed as
  applicability governed by the consuming model; "overloading a cell"
  anti-pattern rewritten for coordinate semantics. (CR-ECF-002)
- REPORT section 15: formal notation block replaced; `Cell_{d,s}` and
  universal `decompose : Cell -> M` explicitly deprecated; `state : Entity
  -> Stage` renamed to `state : Entity -> State`. (CR-ECF-002)
- REPORT section 16.6: "every entity in the metamodel lives in a cell"
  replaced with coordinate-contextualization semantics. (CR-ECF-002)
- REPORT section 19 Step 1: "place every top-50 business object in a cell"
  replaced with "identify the ECF coordinate(s) that contextualize each
  business concept; record the consuming catalog that owns the coordinate
  usage". (CR-ECF-002)
- README Quick Start Step 1: "Map: place your top-50 business objects in
  cells" replaced with the contextualization instruction. (CR-ECF-002)
- REPORT section 5.1: pointer to `framework/domain-grounding.md` added; the
  seven Domain rows link to the formal grounding records. (CR-ECF-003)
- REPORT section 5.2: pointer to `framework/lifecycle-grounding.md` added.
  (CR-ECF-004)
- REPORT section 21.4: DERA mapping paragraph labelled explicitly as a
  mapping, not an identity relationship; pointer to lifecycle-grounding.md
  added. (CR-ECF-004)
- README "What's in this repo": `framework/`, `schemas/`, and `specification/`
  descriptions updated to distinguish pre-existing artefacts (display-label
  enums; reconciliation deferred to CR-MM-ECF-01) from the new canonical
  artefacts. (CR-ECF-001, CR-ECF-002, CR-ECF-003, CR-ECF-004, CR-ECF-005)
- `change-requests/README.md`: CR status flipped to Merged for CR-ECF-001
  (PR #4), CR-ECF-002 (PR #5), CR-ECF-003 (PR #6), CR-ECF-004 (PR #7), and
  CR-ECF-005 (PR #8); CR-ECF-CG-001 added.

## [2.0.0] - 2026-07-27

Initial public release of the Enterprise Concept Framework as the
axiom-derived 7x7 organizing matrix for the TechNeHub Labs DEA ecosystem.
See `CITATION.cff` for the canonical citation metadata.

[Unreleased]: https://github.com/technehub-labs/dea-metaframework/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/technehub-labs/dea-metaframework/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/technehub-labs/dea-metaframework/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/technehub-labs/dea-metaframework/releases/tag/v2.0.0
