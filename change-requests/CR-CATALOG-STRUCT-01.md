# CR-CATALOG-STRUCT-01: Catalog Repository Standard (Four-State Per-Entity Subtrees + CATALOG.yaml Index)

**Status**: Proposed
**Layer**: L0 (Metaframework; cross-repo standard)
**Owner**: TechNeHub Labs
**Depends on**: none
**Supersedes**: none
**Related**: CR-CATALOG-STRUCT-02..07 (adoption CRs)
**Authority**: Mandatory; enforced by CI on every catalog repo

---

## 1. Purpose

Establish the canonical **catalog repository standard** applied by every TechNeHub Labs catalog repo (L1 layer). The standard establishes:

- A **four-state per-entity lifecycle** (research, candidate, canonical, retired) with one named directory per state.
- A **per-entity subtree** shape so that every artifact related to one entity lives under one folder and evolves as a unit.
- A **machine-generated `CATALOG.yaml` index** at the repo root that aggregates all entities, classifications, schemas, validators, and research registers into a single read path.
- A **migration three-step** that catalogs use to adopt the standard without losing historical content.
- A **CI gate** and **conformance test suite** that make adoption verifiable and non-bypassable.
- A **new-repo gate** so future catalog repos are pre-wired from the template.
- A **retroactive adoption schedule** so existing repos are brought into conformance on a tracked timeline.

The standard is intentionally **structural, not behavioral**: it does not change what any catalog decides; it changes how the catalog organizes, surfaces, and evolves its decisions.

## 2. Scope

**In scope**:

- The directory layout every catalog repo SHALL adopt.
- The `CATALOG.yaml` schema (machine-generated).
- The four-state lifecycle and the directory-per-state convention.
- The migration three-step (reversible) for existing catalogs.
- The cross-repo contract: how downstream consumers (dea-metamodel viewer, dea-architecture-framework, dea-cli) read a catalog.
- The CI gate contract: how a catalog proves its `CATALOG.yaml` is up to date.

**Out of scope**:

- Decisions about which entities belong in which catalog (handled by CR-ECF-001..005 and per-catalog CRs).
- The semantic content of any catalog entry (catalog CRs).
- The metamodel itself (handled by dea-metamodel CRs).

## 3. Glossary

- **Catalog**: a single TechNeHub Labs L1 reference repository that hosts governed entities of one metamodel type (e.g. `dea-catalog-processes` hosts `dea:Process` and `dea:ProcessGroup`).
- **Entity**: a single governed record in a catalog (e.g. `dea:process-manage-customer-relationship`).
- **Entity ID**: the canonical identifier (`dea:<family>-<kebab-name>`) declared inside the entity's YAML and referenced everywhere.
- **State**: the lifecycle state of an entity within a catalog (research, candidate, canonical, retired).
- **Subtree**: the per-entity directory `entities/v1-alpha/<entity-id>/` that contains every artifact related to one entity.
- **CATALOG.yaml**: the machine-generated index file at the repo root that lists every entity, its state, its path, and cross-cutting content.

## 4. The four-state per-entity lifecycle

| State | Path (under `entities/v1-alpha/<entity-id>/`) | Production? | Who reads it | Who writes it |
|---|---|---|---|---|
| **research** | `research/` | No | Catalog authors; downstream viewers may render research summaries | Catalog authors |
| **candidate** | `candidates/` | No | Catalog authors; admission pipelines | Contributors via `contributions/`; catalog authors |
| **canonical** | `<entity-id>.yaml` (single canonical file at subtree root) | **Yes** | Every consumer | Catalog authors after admission |
| **retired** | `retired/` | No (preserved) | Auditors; historical viewers | Catalog authors on deprecation |

State transitions:

```
research ──► candidate ──► canonical ──► retired
   ▲           │              │              │
   └───────────┴──────────────┴──────────────┘
              (backtrack possible; see §10)
```

- **research; candidate**: when a candidate entry is admitted to the queue.
- **candidate; canonical**: when an admission CR (per-catalog) lands.
- **canonical; retired**: when a deprecation CR (per-catalog) lands.
- **retired; canonical** (rare): when a deprecated entity is restored.
- **canonical; candidate** (rare): when an entity is suspended and re-admission is required.

## 5. Per-entity subtree shape

Every entity subtree follows this layout:

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

### 5.1 Naming rules

- `<entity-id>` is the canonical entity ID (e.g. `dea:process-manage-customer-relationship`). The colons in entity IDs are preserved as directory name separators: `<family>-<kebab-name>` (e.g. `dea:process-manage-customer-relationship`; directory name `dea:process-manage-customer-relationship`).
- The canonical file is named exactly `<entity-id>.yaml` (colons preserved).
- Research and candidate file names are free but SHOULD include a version suffix (`-v0.1`, `-v0.2`) when revisions exist.
- Retired files include the version they were retired at: `<entity-id>-<version>.yaml`.

### 5.2 What goes in research/

A file lives in `research/` if it satisfies ALL three:

1. It is **investigative output** about one entity (or about a coordinate the entity belongs to).
2. It is **not yet canonical** (i.e. it does not declare a governed entity record).
3. It has **provenance** (an author, a date, a source).

Examples: candidate universes, evidence registers, distinctness sweeps, boundary probes, ECF overlays, admission pre-checks.

A file that does NOT belong in `research/`: anything that declares a governed entity, anything that is a governance document (CR, ADR), anything that is documentation (architecture, classification, conformance).

### 5.3 What goes in candidates/

A file lives in `candidates/` if it satisfies:

1. It declares a candidate entity (i.e. it has `id`, `type`, `name`, and a `version` field with value `< 1.0.0` or a `lifecycle_status: candidate`).
2. It has not been admitted.
3. It has been registered for admission (a CR exists or is being authored).

### 5.4 What goes in retired/

A file lives in `retired/` if it:

1. Was once a canonical entry at the subtree root.
2. Has been superseded by another canonical entry, or deprecated outright, with a retirement manifest in `retired/README.md` that names who retired it, when, why, and what supersedes it.

The retired file's `lifecycle_status` is set to `deprecated` or `retired`. The file is otherwise unchanged from its last canonical form (auditable).

## 6. The CATALOG.yaml index

Every catalog repo carries exactly one `CATALOG.yaml` at its root. The file is **machine-generated** from the filesystem by `scripts/regenerate_catalog.py` (CR-CATALOG-STRUCT-06). Hand-edits to `CATALOG.yaml` are forbidden; a CI gate fails the PR if the file is stale.

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

### 6.2 Read path contract

Any consumer that needs to enumerate a catalog's content reads `CATALOG.yaml` and follows the `path` field. Consumers do not scan the filesystem. This makes the catalog **portable**: the same `CATALOG.yaml` works for local files, GitHub-API fetches, and future distributed mirrors.

### 6.3 Write path contract

`CATALOG.yaml` is regenerated whenever any entity subtree changes. CI runs the regenerator on every PR and fails if the committed `CATALOG.yaml` is out of date. Catalog authors do not hand-edit `CATALOG.yaml`.

## 7. Migration three-step (per repo, reversible)

Every existing catalog runs the same three-step migration. Each step is a separate commit; each is revertible.

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

The migration lands one repo at a time. The pattern stabilizes after the second repo lands. STRUCT-01 does not migrate any repo; it only defines the pattern.

## 8. CI gate contract

Every catalog repo carries a CI gate that runs:

```bash
python scripts/regenerate_catalog.py --check   # exits 0 only if CATALOG.yaml matches filesystem
python scripts/check_catalog_index.py          # JSON-Schema validation + sanity checks
```

A PR fails if either step fails. The gate is required (not advisory) and is the same shape across all catalog repos.

## 9. Cross-repo consumer contract

A consumer (e.g. `dea-metamodel/viewer/`, `dea-architecture-framework/`, `dea-cli`) reads a catalog by:

1. Fetching `https://raw.githubusercontent.com/technehub-labs/<repo>/main/CATALOG.yaml`.
2. Parsing the YAML.
3. Iterating the `entities[]` array; following each `path` to fetch the canonical file.
4. Optionally iterating `research_registers[]` to render research summaries.

The consumer never scans the catalog's filesystem. The consumer never trusts filenames; only entity IDs declared in the canonical YAML.

## 10. Reversibility rules

- Every state transition (research; candidate; canonical; retired) is reversible by the inverse operation. Backtracks are recorded in the entity's `metadata.change_history[]`.
- A retirement manifest (`retired/README.md`) names who, when, why, and what supersedes.
- A retired entity's canonical file is preserved byte-for-byte; only `lifecycle_status` is updated.
- A PR that moves an entity between states MUST include the state-transition CR (a per-catalog CR, not a metaframework CR).

## 11. Acceptance criteria

1. CR-CATALOG-STRUCT-01 lands in `dea-metaframework/change-requests/`.
2. `docs/standards/catalog-repository-pattern.md` (new doc; in dea-metaframework) describes the standard in plain prose.
3. `docs/standards/catalog-repository-pattern-adoption.md` (new doc) lists every catalog repo + adoption CR + status.
4. `tests/conformance/test_catalog_structure.py` (new test; in dea-metaframework) implements CST-001..CST-015.
5. `tools/catalog-repo-template/` (new template repo) pre-wires new catalog repos with the regenerator, the gate, and the conformance tests.
6. The standard is referenced from `README.md` and `docs/README.md` in dea-metaframework.
7. STRUCT-02..07 CRs reference this CR by ID in their `Depends on` field.
8. The four existing catalog repos (`dea-catalog-processes`, `dea-catalog-business-capabilities`, `dea-catalog-digital-business-service-factory`, `dea-catalog-stakeholders`) have adoption CRs filed with status tracked in the adoption tracker.

## 12. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Pattern is too rigid; catalog-specific needs can't be expressed | Medium | Medium | Per-catalog CRs extend the pattern; STRUCT-01 explicitly out-of-scope decisions about entity content |
| Per-entity subtree names collide with filesystem limits (entity IDs with colons on Windows) | Low | Low | Document the colon-preserved directory name convention; macOS/Linux work today; Windows requires WSL or a path-translation shim (deferred) |
| `CATALOG.yaml` regeneration is slow on large catalogs | Medium | Low | The regenerator is incremental; only changed subtrees are re-scanned. Benchmark on dea-catalog-business-capabilities (largest current catalog) |
| Existing `docs/research/` files can't be cleanly classified by entity | Medium | Medium | Step 2 uses a heuristic + manual review for ambiguous files; cross-entity research files land in a shared `research/_cross-cutting/` subfolder (allowed but discouraged) |
| Consumers don't migrate to the read-CATALOG.yaml contract | Medium | High | STRUCT-07 forces the migration; old read paths are deprecated with a one-release grace period |

## 13. Open questions

1. Should `dea:pc-*` (Process Context) and `dea:scope-*` (L0 Scope) get their own subtrees? **Recommendation: no, unless they are promoted to first-class entities.** Contexts live in `contexts/v1-alpha/`; Scopes live as `metadata` on canonical entries until promoted.
2. Should the `retired/` subfolder be required, or optional? **Recommendation: required.** Auditors and historical viewers benefit; the storage cost is small.
3. Should `CATALOG.yaml` include a `classifications` section enumerating controlled vocabularies? **Recommendation: yes**, with each classification's path + sha256 + last_modified.
4. Should `docs/research/` survive at the top level as a deprecated location? **Recommendation: no**, but the migration three-step leaves it in place for one release cycle then deletes it.
5. Should the per-entity subtree name use the entity ID with colons preserved (`dea:process-foo`) or with colons replaced (`dea-process-foo`)? **Recommendation: colons preserved**; matches the entity ID exactly; the colon is a path-safe character on POSIX systems.

---

## Files

- `change-requests/CR-CATALOG-STRUCT-01.md` (this file)
- `docs/standards/catalog-repository-pattern.md` (new; standard in plain prose)
- `docs/standards/catalog-repository-pattern-adoption.md` (new; adoption tracker)
- `README.md` (updated; one-paragraph summary in the Standards section)
- `docs/README.md` (updated; reference to the new standard)

No regenerator tool, conformance tests, or repo template in this CR; STRUCT-06 lands those.
