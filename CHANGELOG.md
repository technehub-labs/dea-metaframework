# Changelog

All notable changes to this repository are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository is
governed by change requests (`change-requests/`).

## [Unreleased]

### Added

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

### Added

- `change-requests/CR-ECF-002.md`: ECF Semantic Boundary, landed as authored.
  (CR-ECF-002)

### Changed

- `framework/constructs.md`: rewrote Definitions and How Constructs Relate;
  introduced canonical Domain/Stage/Coordinate/Context definitions and
  `contextualizes : Entity x Coordinate -> Context` notation; removed the
  `Cell_{d,s} = { objects: Entity[], caps: Capability[] }` container type and
  `decompose : Cell -> M` rule; renamed `state : Entity -> Stage` to
  `state : Entity -> State`; added explicit `state`/`stage` distinction.
  (CR-ECF-002)
- `framework/matrix.md`: reframed header from "every business object lives
  in one cell" to "49 coordinates; a coordinate is classification context,
  not entity container"; rewrote Construction Rules to use contextualization
  semantics, multi-coordinate participation, and capability-identity
  independence; renamed "Recursive Self-Similarity" to "Recursive
  Applicability" and decoupled ECF recursion from Business Process
  decomposition. (CR-ECF-002)
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
- `change-requests/README.md`: CR-ECF-001 status flipped to Merged (PR #4);
  CR-ECF-002 added. (CR-ECF-002)

### Added

- `change-requests/CR-ECF-003.md`: ECF Domain Grounding, landed as authored.
  (CR-ECF-003)
- `framework/domain-grounding.md`: per-Domain grounding records (axiom
  grounding, semantic definition, included concerns, excluded concerns,
  adjacent Domains, boundary rules, evidence); compound-name boundary
  audit (verdicts per compound); orthogonality statement; completeness
  check against the grounding axiom; renaming rule (no rename without
  explicit evidence and governance). (CR-ECF-003)

### Changed

- REPORT section 5.1: pointer to `framework/domain-grounding.md` added; the
  seven Domain rows link to the formal grounding records. (CR-ECF-003)
- README "What's in this repo": `framework/` description now mentions
  `framework/domain-grounding.md`. (CR-ECF-003)
- `change-requests/README.md`: CR-ECF-002 status flipped to Merged (PR #5);
  CR-ECF-003 added. (CR-ECF-003)
