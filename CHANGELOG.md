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
