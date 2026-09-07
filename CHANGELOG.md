# Changelog

All notable changes to this repository are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository is
governed by change requests (`change-requests/`).

## [Unreleased]

No changes.

## [2.4.0] - 2026-09-07

The **Agency & Organization** rename: ECF Domain 3 is renamed from `PeopleAndOrganization` to `AgencyAndOrganization` (kebab-case `people-organization` → `agency-organization`; display form `People & Organization` → `Agency & Organization`). The change is driven by the **Substrate Independence Stress Test** (ADR-ECF-002 §5): the domain must remain semantically valid whether the enterprise's internal agents are biological (humans), artificial (AI systems, autonomous software agents), or hybrid. The term `People` is biologically loaded and fails the Technology Independence test; `Agency` is the architecturally precise, substrate-independent term for the capacity to act on behalf of the enterprise. No content redistribution is required (the underlying capability taxonomy is unchanged; only the domain name and its surrounding language shift). The other six Domains are unchanged.

### Domain set (canonical v2.4.0)

| # | PascalCase | lowerCamelCase | kebab-case | Display |
|--:|---|---|---|---|
| 1 | `GovernanceAndExistence` | `governanceAndExistence` | `governance-existence` | Governance & Existence |
| 2 | `StrategyAndDirection` | `strategyAndDirection` | `strategy-direction` | Strategy & Direction |
| 3 | `AgencyAndOrganization` | `agencyAndOrganization` | `agency-organization` | Agency & Organization **(renamed)** |
| 4 | `PartyAndRelationship` | `partyAndRelationship` | `party-relationship` | Party & Relationship |
| 5 | `ProductAndValue` | `productAndValue` | `product-value` | Product & Value |
| 6 | `OperationsAndEnablement` | `operationsAndEnablement` | `operations-enablement` | Operations & Enablement |
| 7 | `FinanceAndAccounting` | `financeAndAccounting` | `finance-accounting` | Finance & Accounting |

### Why v2.4.0 (not v3.0.0, not v2.3.1)

Per ADR-ECF-001 §6 (Renaming Rule), whenever a canonical identifier is renamed the version is incremented. The cardinality of the seven Domains is unchanged (7), the seven Stages are unchanged (7), the matrix M = D × S still defines 49 coordinates, and the no-cell-filling rule still applies. The change is semantically meaningful (the Domain now survives the AI-agent workforce transition without requiring redefinition) but does not break the matrix topology, so a minor bump is appropriate. `v2.4.0` matches the existing `v2.2.0` / `v2.3.0` minor-bump pattern.

### Why the Domain needs the rename

The ECF grounding axiom states: *An enterprise is any bounded entity that **persists** by exchanging value with its environment.* The derivation for Domain 3 says: *"persists" → persistence requires agents.* The axiom requires **agency**, not **biology**. The semantic quality that makes an entity a constituent of the enterprise is agency — the capacity to act. `People` is the current biological implementation of agency; `Agency` is the substrate-independent subject.

The Domain Semantic Integrity Contract (ADR-ECF-002 §6.4) requires that every domain specification identify a stable enterprise subject, declare exactly one semantic anchor, and survive paradigm shifts (Test 4: Technology Independence). `People & Organization` fails Test 4 by requiring a definitional caveat; `Agency & Organization` passes Test 4 by default.

### What changed

- **Schema** (`schemas/ecf-domain.schema.json`): `AgencyAndOrganization` replaces `PeopleAndOrganization` in the enum; description documents the deprecation aliases.
- **Tool** (`tools/ecf_coordinates.py`): `AgencyAndOrganization` added to `DOMAINS` and `DOMAIN_DISPLAY`; new `DOMAIN_ALIASES` map and `resolve_domain_alias()` function preserve backward compatibility for the 5 deprecated aliases (`PeopleAndOrganization`, `peopleAndOrganization`, `people-organization`, `People & Organization`, `people`).
- **Framework docs** (`framework/`):
  - `domain-grounding.md`: §3.3 Agency & Organization rewritten with substrate-independent language, the **Fundamental Enterprise Question** added, the Internal MECE Partition re-keyed (`Workforce Planning` → `Agent Capacity Planning`; `Culture & Collaboration` → `Coordination & Collaboration`), the **Lifecycle Applicability** section added.
  - `axiom.md`: derivation table row for "persists" (agents) reworded to remove biological language and cite ADR-ECF-002 §5 / CR-ECF-007.
  - `matrix.md`: §11 Domain table row 3 entry uses the substrate-independent definition; the canonical matrix row re-keyed (`Workforce plan` → `Capacity plan`; `Hire / train` → `Acquire / onboard`; `Engagement` → `Coordination`); subdomain table `Culture` → `Coordination`.
  - `case-studies/telecom.md` + `case-studies/digital-services.md`: Agency & Organization row re-keyed for substrate neutrality.
- **REPORT.md**: §2.1 derivation table, §5.1 domain table, all three matrix snapshots (canonical + 2 case studies), and the subdomain table updated.
- **README.md**: §3 domain table already used substrate-neutral language; verified consistent.
- **Page assets** (`pages/assets/`):
  - `site.js`: DOMAINS row 3 `key: 'people'` → `'agency'`, `shortName: 'People'` → `'Agency'`; all 21 cell keys (3 scenarios × 7 stages) `'people.<stage>'` → `'agency.<stage>'`; `people-ops` actor → `agent-ops`.
  - `site.css`: color-variable comment for `--l3` re-worded (no functional change).
- **CITATION.cff**: version `2.3.0` → `2.4.0`.

### Migration mapping (CR-ECF-007 §6.1)

| Old form | New form |
|---|---|
| `PeopleAndOrganization` | `AgencyAndOrganization` |
| `peopleAndOrganization` | `agencyAndOrganization` |
| `people-organization` | `agency-organization` |
| `People & Organization` | `Agency & Organization` |
| `people` (cell-key prefix) | `agency` |
| `Workforce Planning` | `Agent Capacity Planning` |
| `Workforce plan` (matrix label) | `Capacity plan` |
| `Hire / train` (matrix label) | `Acquire / onboard` |
| `Culture & Collaboration` | `Coordination & Collaboration` |
| `Engagement` (matrix label) | `Coordination` |
| `people-ops` (actor identifier) | `agent-ops` |

### Backward compatibility

For a transition period of at least 2 release cycles, `tools/ecf_coordinates.py` exposes the `DOMAIN_ALIASES` map and the `resolve_domain_alias()` function. Consumers that have not yet migrated to the canonical identifier MAY resolve the alias and use the canonical value. The deprecation policy is recorded in ADR-ECF-002 §6.3 and CR-ECF-007 §6.2.

### What did NOT change

- The cardinality of the seven Domains (7), the seven Stages (7), and the matrix M = D × S (49 coordinates) is unchanged.
- The no-cell-filling rule (ADR-ECF-001 §11) still applies.
- No content redistribution is required (CR-ECF-007 §6.3): all content that previously belonged to `People & Organization` remains in `Agency & Organization`. The change is a rename and redefinition, not a restructuring of scope.
- No capability matrix entry is invalidated.
- The five other Domain renames from v2.3.0 (CR-ECF-006) are unchanged.

### Implementation

This release is the implementation of **CR-ECF-007** (governed by **ADR-ECF-002**). Both documents are filed verbatim in `change-requests/CR-ECF-007.md` and `docs/adr/ADR-ECF-002.md` per the byte-identical-rule convention.

## [2.3.0] - 2026-09-07

The ECF domain restructure: five of the seven canonical Domains are renamed, one is replaced, and the change is backed by the first ADR in this repository. This is a content-narrowing, scope-grounding, axiomatic-concreteness release; it is NOT a SemVer-major breaking change (v2.3.0, not v3.0.0) because the seven-Domain cardinality and the seven-Stage cardinality are unchanged, the matrix M = D x S still defines 49 coordinates, and the no-cell-filling rule still applies. What changes is the rigor and precision of the Domain names and their boundaries, so the framework can ground downstream mapping work more rigorously and correctly.

### Added

- `change-requests/ADR-ECF-001.md`: the first Architecture Decision Record in
  this repository. Records the five-tests rubric (Semantic Anchor, Lifecycle
  Completeness, Boundary Integrity, Technology Independence, Collective
  Exhaustiveness) used to assess each Domain, and the design decisions
  behind each rename. (ADR-ECF-001)
- `change-requests/CR-ECF-006.md`: the change request that records the
  before/after for each of the seven Domains, the rename rationale, and
  the redistribution of the prior Supply & Resources content. (CR-ECF-006)
- `docs/adr/`: directory for Architecture Decision Records (first entry:
  ADR-ECF-001). The ADR series is the design-decision record; the CR series
  is the implementation record.

### Changed

- **Domain enumeration (CR-ECF-006, normative change):**

  | # | Before (v2.2.0) | After (v2.3.0) | Change |
  |---|------------------|------------------|--------|
  | 1 | Governance & Existence | Governance & Existence | Retained, enhanced definition |
  | 2 | Supply & Resources | Strategy & Direction | Replaced; substance redistributed |
  | 3 | Agency & Organization | Agency & Organization | Retained, enhanced definition |
  | 4 | Customer & Demand | Party & Relationship | Renamed and expanded |
  | 5 | Product & Offering | Product & Value | Renamed and sharpened |
  | 6 | Operations & Delivery | Operations & Enablement | Renamed and expanded |
  | 7 | Finance & Value | Finance & Accounting | Renamed and sharpened |

- `framework/domain-grounding.md`: full rewrite of the compound-name audit
  and all seven Domain grounding records, adding semantic anchors,
  internal MECE partitions per Domain, and the redistribution rationale
  for Supply & Resources (assets moved to Operations & Enablement as
  enablers; financial resources moved to Finance & Accounting; human
  resources remain in Agency & Organization). (CR-ECF-003, CR-ECF-006)
- `framework/constructs.md`: Domain list updated to the v2.3.0 set. (CR-ECF-006)
- `framework/axiom.md`: derivation table now resolves "persists" into three
  facets (directed, agents, substrate as enabler) and "exchanging value"
  into three facets (counterparty, bearer of value, mechanism), one per
  Domain. (CR-ECF-006)
- `framework/matrix.md`: domain enumeration, the 7x7 cell content table,
  and the MECE subdomain table rewritten against the v2.3.0 Domain set.
  (CR-ECF-006)
- `framework/case-studies/telecom.md`,
  `framework/case-studies/digital-services.md`: cell content and worked
  examples updated to the v2.3.0 Domain names. (CR-ECF-006)
- `specification/ecf-coordinates.md`: Section 4 Domain Enumeration and
  Section 9 Multiple Coordinates example updated; a paragraph added
  noting that the v2.2.0->v2.3.0 transition is a deliberate domain
  restructure (no backward-compatibility aliases are defined). (CR-ECF-006)
- `schemas/ecf-domain.schema.json`: canonical PascalCase enum updated to
  the v2.3.0 Domain set. (CR-ECF-006)
- `tools/ecf_coordinates.py`: `DOMAINS` and `DOMAIN_DISPLAY` updated to
  the v2.3.0 Domain set. (CR-ECF-006)
- `tests/conformance/test_005_coordinate_spec.py`: validator
  acceptance/rejection test fixtures updated from
  `OperationsAndDelivery` to `OperationsAndEnablement`. (CR-ECF-006)
- `pages/assets/site.js`: `DOMAINS` array, cell keys, cell content, and
  row comments updated. The strategy row content is rewritten to match
  the new Domain's anchor (purpose, strategic choices, initiative
  portfolio, course correction) rather than the old supply-and-resources
  content. (CR-ECF-006)
- `pages/assets/site.css`: domain palette row labels updated. (CR-ECF-006)
- `REPORT.md`: the derivation table, domain enumeration, MECE subdomain
  table, three cell-content tables (foundation, telecom, digital
  services), the metamodel layer mapping, the domain-to-catalog mapping,
  and three JSON examples all updated to the v2.3.0 Domain set.
  (CR-ECF-006)

### Breaking changes for downstream consumers

The five renames and the Supply & Resources replacement are breaking for
any downstream consumer that hard-codes the v2.2.0 Domain names in
kebab-case, camelCase, PascalCase, or display form. The
`dea-metamodel`, `dea-catalog-processes`,
`dea-catalog-business-capabilities`, `dea-catalog-stakeholders`,
`dea-catalog-actors`, and `dea-catalog-digital-business-service-factory`
repositories all require coordinated migration PRs against the
post-v2.3.0 enum. The following are the canonical kebab-case
identifiers for the v2.3.0 Domain set (the same identifiers used in
the v0.2 ECF Overlay and downstream catalog entity files):

- `governance-existence` (unchanged)
- `strategy-direction` (was `supply-resources`)
- `agency-organization` (unchanged)
- `party-relationship` (was `customer-demand`)
- `product-value` (was `product-offering`)
- `operations-enablement` (was `operations-delivery`)
- `finance-accounting` (was `finance-value`)

The downstream reconciliation CRs (CR-MM-ECF-01, CR-BC-ECF-01,
CR-BP-ECF-01; all parked under the post-gate downstream reconciliation
programme) are the carriers of those migration PRs. Each will be
unblocked against this v2.3.0 release.

### Verification

- `tests/`: **39/39 pass** (conformance + machinery + structure)
- 0 en/em dashes introduced in any new authored content
- en/em dashes in `change-requests/ADR-ECF-001.md` and
  `change-requests/CR-ECF-006.md` are byte-identical to the source
  documents as supplied (landing rule: landed CR files are
  byte-identical to the source section)

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
