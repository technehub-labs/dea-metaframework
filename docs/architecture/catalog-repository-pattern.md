# Catalog Repository Pattern

**Status**: Adopted (CR-CATALOG-STRUCT-01)
**Layer**: L0 (Metaframework; cross-repo contract)
**Audience**: Catalog authors; downstream consumers; tooling authors

This document describes the **catalog repository pattern** that every TechNeHub Labs catalog repo (L1 layer) follows. The pattern is structural; it does not prescribe what any catalog decides, only how a catalog organizes, surfaces, and evolves its decisions.

## The one-paragraph summary

A catalog repo hosts governed entities of one metamodel type. Each entity lives in its own subtree at `entities/v1-alpha/<entity-id>/`. The subtree contains the entity's canonical YAML at the root and four state folders: `research/`, `candidates/`, the canonical file itself, and `retired/`. The repo root carries a single machine-generated `CATALOG.yaml` index that enumerates every entity, its state, its path, and cross-cutting content. Consumers read the catalog by fetching `CATALOG.yaml` and following each entity's `path` field. The pattern is enforced by a CI gate that fails any PR whose `CATALOG.yaml` is stale.

## The four-state lifecycle

Every entity has one of four lifecycle states, each with a named directory under the entity's subtree:

| State | Path | Production? |
|---|---|---|
| research | `entities/v1-alpha/<entity-id>/research/` | No |
| candidate | `entities/v1-alpha/<entity-id>/candidates/` | No |
| canonical | `entities/v1-alpha/<entity-id>/<entity-id>.yaml` | Yes |
| retired | `entities/v1-alpha/<entity-id>/retired/` | No |

State transitions are recorded in the entity's `metadata.change_history[]`. A retirement manifest in `retired/README.md` names who retired the entity, when, why, and what supersedes it. Retired files are preserved byte-for-byte; only `lifecycle_status` is updated.

## Per-entity subtree

```
entities/v1-alpha/<entity-id>/
├── <entity-id>.yaml        # canonical
├── research/                # evidence, candidate universes, sweeps
│   ├── README.md            # research history index
│   └── <files>
├── candidates/              # candidate entries awaiting admission
│   ├── README.md
│   └── <candidate>.yaml
└── retired/                 # superseded canonical entries
    ├── README.md            # retirement manifest
    └── <entity-id>-<version>.yaml
```

Directory names preserve the entity ID exactly, including colons: `dea:process-manage-customer-relationship/` is a valid POSIX directory name. This matches the entity ID everywhere, so a consumer can resolve `<id>` ; `<path>` with a single substitution rule.

## CATALOG.yaml

The repo root carries exactly one `CATALOG.yaml`. It is **machine-generated** by `scripts/regenerate_catalog.py` (CR-CATALOG-STRUCT-06) and is regenerated on every PR. Hand-edits are forbidden; the CI gate fails any PR whose `CATALOG.yaml` is out of date with the filesystem.

The file has five sections:

1. **catalog metadata**: id, name, abbreviation, version, status, metamodel_version, description, repository, owner.
2. **entities[]**: one entry per entity subtree, declaring `id`, `type`, `state`, `path`, file counts (`research_count`, `candidate_count`, `canonical_count`, `retired_count`), `last_modified`, `version`, `lifecycle_status`.
3. **cross_cutting**: paths to classifications, schemas, validators, contribution queue, change-requests.
4. **counts**: cheap aggregate updated on every regeneration.
5. **research_registers[]**: convenience listing of which entity owns which research files.

## Read path

A consumer (dea-metamodel viewer, dea-architecture-framework, dea-cli, third-party tools) reads a catalog by:

1. Fetching `https://raw.githubusercontent.com/technehub-labs/<repo>/main/CATALOG.yaml`.
2. Parsing the YAML.
3. Iterating the `entities[]` array; following each `path` to fetch the canonical file.
4. Optionally iterating `research_registers[]` to render research summaries.

The consumer never scans the catalog's filesystem. The consumer never trusts filenames; only entity IDs declared in the canonical YAML.

## CI gate

Every catalog repo carries a CI gate:

```bash
python scripts/regenerate_catalog.py --check   # exit 0 only if CATALOG.yaml matches filesystem
python scripts/check_catalog_index.py          # JSON-Schema validation + sanity checks
```

A PR fails if either step fails. The gate is required, not advisory, and is the same shape across all catalog repos.

## Migration three-step

Existing catalogs adopt the pattern in three reversible steps. Each step is a separate commit and a separate per-catalog CR.

1. **Adopt the layout, no content moves**: create `entities/v1-alpha/<id>/` subtrees for every existing entity; move canonical files into subtrees; update `metamodel-pointer.yaml` paths; add the regenerator script and CI gate; generate `CATALOG.yaml` for the first time; verify all validators pass.
2. **Distribute research into per-entity subfolders**: classify each file in `docs/research/` by which entity it studies; move it under that entity's `research/` subfolder; write a `research/README.md` per entity subtree showing provenance.
3. **Codify the contribution flow**: convert `contributions/<entity-type>/` into a single `contributions/` intake queue; add per-entity-type contribution templates; the contribution-report workflow validates per-type using the schemas declared in the catalog.

The migration lands one repo at a time. The pattern stabilizes after the second repo lands.

## What this pattern is not

- **Not a metamodel change.** The pattern is structural; entity semantics are unchanged.
- **Not a contribution workflow change.** The contribution intake still lives at `contributions/`; per-entity-type templates land in step 3 of the migration.
- **Not a replacement for `metamodel-pointer.yaml`.** That file maps a catalog repo to the metamodel entities it hosts; the pattern adds a per-entity inventory on top.
- **Not an entity content decision.** The pattern organizes how a catalog decides, not what it decides.

## Adoption CRs

| CR | Repo | Purpose |
|---|---|---|
| CR-CATALOG-STRUCT-01 | `dea-metaframework` | Pattern definition (this doc + change-request) |
| CR-CATALOG-STRUCT-02 | `dea-catalog-processes` | Process catalog adoption (step 1 + 2 + 3) |
| CR-CATALOG-STRUCT-03 | `dea-catalog-business-capabilities` | Business Capability catalog adoption |
| CR-CATALOG-STRUCT-04 | `dea-catalog-digital-business-service-factory` | DBSF adoption (convert existing `CATALOG/v1-alpha/` to per-entity subtrees) |
| CR-CATALOG-STRUCT-05 | `dea-catalog-stakeholders` | Stakeholders adoption (scaffold from day one) |
| CR-CATALOG-STRUCT-06 | `dea-metaframework/tools/` | `CATALOG.yaml` regenerator + CI gate tool |
| CR-CATALOG-STRUCT-07 | `dea-metaframework/viewer/`, `dea-architecture-framework/` | Cross-repo consumer of `CATALOG.yaml` |
