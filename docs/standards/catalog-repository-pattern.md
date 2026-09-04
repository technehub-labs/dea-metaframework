# Standard: Catalog Repository Pattern

**Status**: Adopted (CR-CATALOG-STRUCT-01)
**Layer**: L0 (Metaframework; cross-repo standard)
**Authority**: Mandatory; enforced by CI on every catalog repo
**Audience**: Catalog authors; downstream consumers; tooling authors; new-repo bootstrappers

This document is the **canonical standard** that every TechNeHub Labs catalog repo (L1 layer) MUST follow. The standard is structural; it does not prescribe what any catalog decides, only how a catalog organizes, surfaces, and evolves its decisions.

## 1. The one-paragraph summary

A catalog repo hosts governed entities of one metamodel type. Each entity MUST live in its own subtree at `entities/v1-alpha/<entity-id>/`. The subtree MUST contain the entity's canonical YAML at the root and four state folders: `research/`, `candidates/`, the canonical file itself, and `retired/`. The repo root MUST carry a single machine-generated `CATALOG.yaml` index that enumerates every entity, its state, its path, and cross-cutting content. Consumers MUST read the catalog by fetching `CATALOG.yaml` and following each entity's `path` field. The standard is enforced by a CI gate that fails any PR whose `CATALOG.yaml` is stale or whose repo structure deviates.

## 2. Scope and authority

**Mandatory for**:

- Every existing TechNeHub Labs catalog repo (`dea-catalog-processes`, `dea-catalog-business-capabilities`, `dea-catalog-digital-business-service-factory`, `dea-catalog-stakeholders`, and any sibling catalog that hosts a metamodel entity).
- Every new catalog repo created after the standard's adoption date.

**Enforcement**:

- The regenerator (`scripts/regenerate_catalog.py`) and the conformance gate (`scripts/check_catalog_index.py`) are required CI checks. A PR that breaks either check is non-mergeable.
- The cross-repo conformance test (`tests/conformance/test_catalog_structure.py` in `dea-metaframework`) is run by `dea-metaframework` CI on a schedule and against every catalog repo when its `dea-metaframework-pointer.yaml` is bumped.
- New catalog repos are bootstrapped from `dea-metaframework/tools/catalog-repo-template/`, which is pre-wired with the regenerator, the gate, and the conformance tests. A repo that does not start from the template MUST be brought into conformance before it can be referenced by `dea-metamodel` consumers.

**Exemptions**: None. If a catalog has a structural need not covered by this standard, that need MUST be addressed by amending the standard (a CR to this repo) before the catalog diverges.

## 3. Glossary

- **Catalog**: a single TechNeHub Labs L1 reference repository that hosts governed entities of one metamodel type (e.g. `dea-catalog-processes` hosts `dea:Process` and `dea:ProcessGroup`).
- **Entity**: a single governed record in a catalog (e.g. `dea:process-manage-customer-relationship`).
- **Entity ID**: the canonical identifier (`dea:<family>-<kebab-name>`) declared inside the entity's YAML and referenced everywhere.
- **State**: the lifecycle state of an entity within a catalog (research, candidate, canonical, retired).
- **Subtree**: the per-entity directory `entities/v1-alpha/<entity-id>/` that contains every artifact related to one entity.
- **CATALOG.yaml**: the machine-generated index file at the repo root that lists every entity, its state, its path, and cross-cutting content.

## 4. The four-state per-entity lifecycle (mandatory)

| State | Path (under `entities/v1-alpha/<entity-id>/`) | Production? | Who reads it | Who writes it |
|---|---|---|---|---|
| **research** | `research/` | No | Catalog authors; downstream viewers may render research summaries | Catalog authors |
| **candidate** | `candidates/` | No | Catalog authors; admission pipelines | Contributors via `contributions/`; catalog authors |
| **canonical** | `<entity-id>.yaml` (single canonical file at subtree root) | **Yes** | Every consumer | Catalog authors after admission |
| **retired** | `retired/` | No (preserved) | Auditors; historical viewers | Catalog authors on deprecation |

State transitions:

```
research -> candidate -> canonical -> retired
   ^          |             |             |
   +----------+-------------+-------------+
              (backtrack possible; see §10)
```

- **research -> candidate**: when a candidate entry is admitted to the queue.
- **candidate -> canonical**: when an admission CR (per-catalog) lands.
- **canonical -> retired**: when a deprecation CR (per-catalog) lands.
- **retired -> canonical** (rare): when a deprecated entity is restored.
- **canonical -> candidate** (rare): when an entity is suspended and re-admission is required.

Each state transition MUST be recorded in the entity's `metadata.change_history[]`. A retirement manifest in `retired/README.md` MUST name who retired the entity, when, why, and what supersedes it. Retired files MUST be preserved byte-for-byte; only `lifecycle_status` is updated.

## 5. Per-entity subtree shape (mandatory)

Every entity subtree MUST follow this layout:

```
entities/v1-alpha/<entity-id>/
├── <entity-id>.yaml             # canonical (one file; the entity's single source of truth)
├── research/                    # research state (may be empty)
│   ├── README.md                # research history index (provenance per file)
│   └── <files>                  # research output: evidence, candidate universes, sweeps
├── candidates/                  # candidate state (may be empty)
│   ├── README.md                # candidate queue index
│   └── <candidate>.yaml         # one or more candidate entries
└── retired/                     # retired state (may be empty)
    ├── README.md                # retirement manifest: who, when, why, what supersedes
    └── <entity-id>-<version>.yaml
```

### 5.1 Naming rules (mandatory)

- `<entity-id>` is the canonical entity ID (e.g. `dea:process-manage-customer-relationship`). The colons in entity IDs MUST be preserved as part of the directory name. POSIX-safe on macOS/Linux; Windows requires WSL or a path-translation shim (out of scope of this standard).
- The canonical file MUST be named exactly `<entity-id>.yaml` (colons preserved).
- Research and candidate file names SHOULD include a version suffix (`-v0.1`, `-v0.2`) when revisions exist.
- Retired files MUST include the version they were retired at: `<entity-id>-<version>.yaml`.

### 5.2 What goes in research/ (mandatory)

A file MUST live in `research/` if it satisfies ALL three:

1. It is **investigative output** about one entity (or about a coordinate the entity belongs to).
2. It is **not yet canonical** (i.e. it does not declare a governed entity record).
3. It has **provenance** (an author, a date, a source).

Examples: candidate universes, evidence registers, distinctness sweeps, boundary probes, ECF overlays, admission pre-checks.

A file MUST NOT be in `research/`: anything that declares a governed entity, governance documents (CR, ADR), or documentation (architecture, classification, conformance).

### 5.3 What goes in candidates/ (mandatory)

A file MUST live in `candidates/` if it satisfies:

1. It declares a candidate entity (i.e. it has `id`, `type`, `name`, and a `version` field with value `< 1.0.0` or a `lifecycle_status: candidate`).
2. It has not been admitted.
3. It has been registered for admission (a CR exists or is being authored).

### 5.4 What goes in retired/ (mandatory)

A file MUST live in `retired/` if it:

1. Was once a canonical entry at the subtree root.
2. Has been superseded by another canonical entry, or deprecated outright, with a retirement manifest in `retired/README.md` that names who retired it, when, why, and what supersedes it.

The retired file's `lifecycle_status` MUST be set to `deprecated` or `retired`. The file MUST be otherwise unchanged from its last canonical form (auditable).

## 6. The CATALOG.yaml index (mandatory)

Every catalog repo MUST carry exactly one `CATALOG.yaml` at its root. The file MUST be **machine-generated** from the filesystem by `scripts/regenerate_catalog.py` (CR-CATALOG-STRUCT-06). Hand-edits to `CATALOG.yaml` are forbidden; the CI gate fails any PR where the committed `CATALOG.yaml` is stale.

### 6.1 Schema (informal; full JSON Schema in STRUCT-06)

```yaml
catalog:
  id: dea:catalog-processes              # stable catalog id
  name: Business Process
  abbreviation: BP
  version: "1.0.0"                        # catalog version (not entity version)
  status: active
  metamodel_version: "1.0.0"
  description: ...
  repository: https://github.com/...
  owner: TechNeHub Labs

  entities:                               # one entry per entity subtree
    - id: dea:process-manage-customer-relationship
      type: Process
      state: canonical
      path: entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml
      research_count: 3
      candidate_count: 0
      canonical_count: 1
      retired_count: 0
      last_modified: 2026-09-04
      version: 1.0.0
      lifecycle_status: candidate

  cross_cutting:
    classifications: classifications/
    schemas: schemas/
    validators: scripts/
    contributions_queue: contributions/
    change_requests: change-requests/

  counts:                                 # cheap aggregate; updated on every regeneration
    entities: 2
    research_files: 4
    candidates: 0
    canonical: 2
    retired: 0
    open_change_requests: 1

  research_registers:                    # convenience: which entity owns which research
    - entity_id: dea:process-manage-customer-relationship
      path: entities/v1-alpha/dea:process-manage-customer-relationship/research/
      files: [l1-register.yaml, l1-candidate-universe.yaml, L1-REGISTER-v0.1.md]
```

### 6.2 Read path contract (mandatory)

Any consumer that needs to enumerate a catalog's content MUST read `CATALOG.yaml` and follow the `path` field. Consumers MUST NOT scan the filesystem. This makes the catalog **portable**: the same `CATALOG.yaml` works for local files, GitHub-API fetches, and future distributed mirrors.

### 6.3 Write path contract (mandatory)

`CATALOG.yaml` MUST be regenerated whenever any entity subtree changes. CI runs the regenerator on every PR and fails if the committed `CATALOG.yaml` is out of date. Catalog authors MUST NOT hand-edit `CATALOG.yaml`.

## 7. Migration three-step (mandatory for existing repos)

Every existing catalog MUST run the same three-step migration. Each step is a separate commit; each is revertible.

### Step 1: adopt the layout (no content moves)

- Create `entities/v1-alpha/<entity-id>/` subtrees for every existing entity.
- Move each entity's canonical file into its subtree.
- Update `metamodel-pointer.yaml` paths to the new locations.
- Add the regenerator script (from STRUCT-06) and the CI gate.
- Generate `CATALOG.yaml` for the first time.
- Verify all validators still pass against the new locations.

### Step 2: distribute research into per-entity subfolders

- For each file in `docs/research/` (or equivalent top-level research directory), classify which entity it studies (by YAML field parsing + filename hints).
- Move the file to the entity subtree's `research/` subfolder.
- Write a `research/README.md` per entity subtree showing provenance (where the file came from, when, why).
- Re-run the regenerator and validators.

### Step 3: codify the contribution flow

- Convert the existing `contributions/<entity-type>/` intake into `contributions/` (one intake queue per catalog repo).
- Add per-entity-type contribution templates under `contributions/<entity-type>/CONTRIBUTION-TEMPLATE.yaml`.
- The contribution-report workflow validates per-type using the schemas declared in the catalog.

The migration lands one repo at a time. The standard stabilizes after the second repo lands.

## 8. CI gate contract (mandatory)

Every catalog repo MUST carry a CI gate that runs:

```bash
python scripts/regenerate_catalog.py --check   # exits 0 only if CATALOG.yaml matches filesystem
python scripts/check_catalog_index.py          # JSON-Schema validation + sanity checks
```

A PR MUST fail if either step fails. The gate is required (not advisory) and is the same shape across all catalog repos.

## 9. Cross-repo consumer contract (mandatory for consumers)

A consumer (e.g. `dea-metamodel/viewer/`, `dea-architecture-framework/`, `dea-cli`) MUST read a catalog by:

1. Fetching `https://raw.githubusercontent.com/technehub-labs/<repo>/main/CATALOG.yaml`.
2. Parsing the YAML.
3. Iterating the `entities[]` array; following each `path` to fetch the canonical file.
4. Optionally iterating `research_registers[]` to render research summaries.

The consumer MUST NOT scan the catalog's filesystem. The consumer MUST NOT trust filenames; only entity IDs declared in the canonical YAML.

## 10. Reversibility rules (mandatory)

- Every state transition (research -> candidate -> canonical -> retired) MUST be reversible by the inverse operation. Backtracks MUST be recorded in the entity's `metadata.change_history[]`.
- A retirement manifest (`retired/README.md`) MUST name who, when, why, and what supersedes.
- A retired entity's canonical file MUST be preserved byte-for-byte; only `lifecycle_status` is updated.
- A PR that moves an entity between states MUST include the state-transition CR (a per-catalog CR, not a metaframework CR).

## 11. Conformance tests (mandatory)

`dea-metaframework/tests/conformance/test_catalog_structure.py` MUST verify, for any catalog repo passed as argument:

| Test ID | Invariant |
|---|---|
| CST-001 | Repo has `CATALOG.yaml` at root. |
| CST-002 | `CATALOG.yaml` parses as YAML and validates against `docs/standards/catalog-repository-pattern.schema.json`. |
| CST-003 | Every directory under `entities/v1-alpha/` matches the entity-subtree shape (has `<entity-id>.yaml`, `research/`, `candidates/`, `retired/`). |
| CST-004 | Every `<entity-id>.yaml` declares `id`, `type`, `name`, `version`, `lifecycle_status`. |
| CST-005 | Every entity in `CATALOG.yaml` `entities[]` corresponds to a real subtree on disk. |
| CST-006 | Every entity subtree on disk is enumerated in `CATALOG.yaml` `entities[]` (no orphans). |
| CST-007 | Every `path` field in `CATALOG.yaml` resolves to a real file on disk. |
| CST-008 | `state` in `CATALOG.yaml` matches the actual directory contents of the subtree. |
| CST-009 | `research/`, `candidates/`, `retired/` each contain a `README.md` if they contain any other file. |
| CST-010 | Every `retired/<file>.yaml` declares `lifecycle_status: deprecated` or `retired`. |
| CST-011 | Every `candidates/<file>.yaml` declares `version < 1.0.0` OR `lifecycle_status: candidate`. |
| CST-012 | `metamodel-pointer.yaml` paths (if present) resolve to real files on disk. |
| CST-013 | Repo has `scripts/regenerate_catalog.py` (executable). |
| CST-014 | Repo has `scripts/check_catalog_index.py` (executable). |
| CST-015 | CI workflow file references both scripts in its check job. |

A repo fails conformance if any test fails. The test runner exits non-zero and prints the failing test IDs.

## 12. New-repo gate (mandatory)

A new catalog repo MUST be bootstrapped from `dea-metaframework/tools/catalog-repo-template/`. The template pre-wires:

- The directory structure (`entities/v1-alpha/`, `contributions/`, `classifications/`, `schemas/`, `scripts/`, `change-requests/`).
- `scripts/regenerate_catalog.py` and `scripts/check_catalog_index.py` (copies of the canonical implementations).
- `.github/workflows/ci.yml` referencing both scripts as required checks.
- `metamodel-pointer.yaml` (empty; filled in once the entity is registered with `dea-metamodel`).
- `README.md`, `CHANGELOG.md`, `LICENSE`, `NOTICE`.

A repo that does not start from the template MUST be brought into conformance (run the conformance tests; fix every failure) before it is referenced by `dea-metamodel` consumers.

## 13. Retroactive adoption schedule (mandatory)

The four existing catalog repos MUST adopt this standard by landing adoption CRs. Adoption is tracked in `docs/standards/catalog-repository-pattern-adoption.md`.

| Repo | Adoption CR | Target milestone |
|---|---|---|
| `dea-catalog-processes` | CR-CATALOG-STRUCT-02 | Q3 2026 (next tranche after STRUCT-01 + STRUCT-06 merge) |
| `dea-catalog-business-capabilities` | CR-CATALOG-STRUCT-03 | Q3 2026 (next tranche after STRUCT-02 lands) |
| `dea-catalog-digital-business-service-factory` | CR-CATALOG-STRUCT-04 | Q4 2026 |
| `dea-catalog-stakeholders` | CR-CATALOG-STRUCT-05 | Q4 2026 (scaffold-from-day-one; no migration needed) |

The cross-repo consumer (CR-CATALOG-STRUCT-07) lands after STRUCT-02 + STRUCT-06 are merged. Consumer adoption is tracked separately.

## 14. Adoption tracker (mandatory)

`docs/standards/catalog-repository-pattern-adoption.md` MUST list every catalog repo + adoption CR + status. Status values are:

- `not-started`: no adoption PR opened.
- `in-progress`: PR opened but not merged.
- `partial`: layout adopted but research not yet distributed.
- `conforming`: layout adopted, research distributed, contribution flow codified, all conformance tests pass.
- `exempted`: explicit waiver granted by the metaframework (rare; recorded with rationale and sunset date).

## 15. What this standard is not

- **Not a metamodel change.** The standard is structural; entity semantics are unchanged.
- **Not a contribution workflow change.** The contribution intake still lives at `contributions/`; per-entity-type templates land in step 3 of the migration.
- **Not a replacement for `metamodel-pointer.yaml`.** That file maps a catalog repo to the metamodel entities it hosts; the standard adds a per-entity inventory on top.
- **Not an entity content decision.** The standard organizes how a catalog decides, not what it decides.

## 16. Adoption CRs

| CR | Repo | Purpose |
|---|---|---|
| CR-CATALOG-STRUCT-01 | `dea-metaframework` | Standard definition (this doc + change-request) |
| CR-CATALOG-STRUCT-02 | `dea-catalog-processes` | Process catalog adoption (step 1 + 2 + 3) |
| CR-CATALOG-STRUCT-03 | `dea-catalog-business-capabilities` | Business Capability catalog adoption |
| CR-CATALOG-STRUCT-04 | `dea-catalog-digital-business-service-factory` | DBSF adoption (convert existing `CATALOG/v1-alpha/` to per-entity subtrees) |
| CR-CATALOG-STRUCT-05 | `dea-catalog-stakeholders` | Stakeholders adoption (scaffold from day one) |
| CR-CATALOG-STRUCT-06 | `dea-metaframework/tools/` | `CATALOG.yaml` regenerator + CI gate tool + conformance tests + repo template |
| CR-CATALOG-STRUCT-07 | `dea-metamodel/viewer/`, `dea-architecture-framework/` | Cross-repo consumer of `CATALOG.yaml` |
