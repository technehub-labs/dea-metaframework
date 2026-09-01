# Change Requests

Change requests governing the Enterprise Concept Framework
(`technehub-labs/dea-metaframework`). ECF-series CRs land in this repository;
cross-references point at the canonical CR repository (`dea-metamodel`).

## ECF series

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-ECF-001](./CR-ECF-001.md) | ECF Architectural Reconciliation | Merged (PR #4) | Positions ECF as an OpenDEA organizing framework/profile; establishes WSF -> OpenDEA -> ECF -> Metamodel -> Catalogs; lands `framework/architecture.md`. |
| [CR-ECF-002](./CR-ECF-002.md) | ECF Semantic Boundary | Merged (PR #5) | Canonical definitions for Domain, Stage, Coordinate, Context; replaces container semantics with contextualization; capability identity and process topology boundaries. |
| [CR-ECF-003](./CR-ECF-003.md) | ECF Domain Grounding | Proposed (PR open) | Formal grounding records for the seven Domains; compound-name boundary audit; orthogonality and completeness checks; renaming rule. |

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
