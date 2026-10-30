# CR-CATALOG-STRUCT-10: Catalog Kit Generator

| Field | Value |
|---|---|
| **CR** | CR-CATALOG-STRUCT-10 |
| **Title** | Catalog kit generator: machine-generate the full standup kit from the metamodel |
| **Status** | Merged (this PR) |
| **Layer** | Tooling (catalog repository pattern, §12 new-repo gate extension) |
| **Repository** | `technehub-labs/dea-metaframework` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-02 |
| **Depends on** | CR-CATALOG-STRUCT-01 (standard), CR-CATALOG-STRUCT-06a/06b (regenerator, template, bootstrap), CR-ECF-011 (regenerator counter fix) |
| **Trigger** | Org-wide catalog advancement programme (owner directive 2026-10-30): advance every initial-state catalog repo to the reputable-foundation standard with initial entities. The standard's kit (proven manually as CR-IA-CAT-01..03 on dea-catalog-information-assets) must become a generated artifact so ~38 repositories advance by parameterization and curation, not hand-crafting. |

## 1. Executive summary

`tools/generate_catalog_kit.py` emits the complete S1-S3 standup kit for a catalog repository, derived from the canonical metamodel: hybrid metamodel pointer (identity keys for the regenerator + `metamodel:` allocation block for validate-against-model, layer- and dimension-allocated shapes, multi-entity shared repos), `dependencies.yaml`, schema projection with the catalogue-instance layer, vendored relationship-instance contract, valid/invalid fixtures, gates 1-6, three CI workflows, FOUNDATIONS with a D-1..D-6 decision register, RECORD-STANDARD, README contract, CONTRIBUTING, CR register, and a drafted foundation CR. Population (S4) is intentionally not generated: admissions are evidence-driven and land as the repo's own CR-02.

## 2. Projection strategy

1. **Copied-and-narrowed** (metamodel schema present; 138 entities): the normative schema is copied; the id pattern narrows to `dea:<slug>-[a-z0-9-]+` (information-classes id precedent), `type` const and `lifecycle_status` enum are pinned, `additionalProperties: false`, required becomes the standard five plus metamodel extras, base props (external_references, tags, metadata) and the instance layer (evidence, provenance ladder, governance) are injected where absent.
2. **Derived-from-entity-definition** (null-artifact entities; 25): a minimal normative projection is derived from the entity record; the generator flags every such entity for a metamodel schema-backfill CR.

Slug derivation uses `legacy_ids[0]` (`dea:entity-X` -> `X`), the stable allocation identifier.

## 3. Guards

- Shared-repo mismatch guard: every entity in `--entity` must declare the same `catalog_repo` (exit otherwise).
- Re-run safety: without `--force`, existing files are kept and reported (curation is never clobbered); `--force` overwrites.
- `.gitignore` repair: the template's ignore of `CATALOG.yaml` (which breaks the §6 freshness gate) is replaced by the committed-index form; the standard cross-cutting dirs are scaffolded with `.gitkeep`.

## 4. Tests

`tests/test_generate_catalog_kit.py` (13 tests) with a fixture metamodel covering all three projection shapes: emission inventory, pointer block assertions (including the dimension shape), copy-and-narrow assertions (id pattern, enum carry-through, instance layer, required merge), derived-projection flagging, the self-validation loop (every generated gate runs green against its own generated kit), re-run-without-force preservation, and the shared-repo mismatch guard. Full metaframework suite: 103 passed.

## 5. Scope

In scope: `tools/generate_catalog_kit.py`, `tests/test_generate_catalog_kit.py`, `tests/fixtures/kit-metamodel.yaml`, `tests/fixtures/kit-schemas/*`, this CR, register row, CHANGELOG entry.

Out of scope: no change to the standard docs; no template change (the generator overlays bootstrapped or existing repos); no population content; no changes to regenerator/index machinery.

## 6. NOT-list

1. The generator never admits records and never invents evidence.
2. No normative vocabulary is widened: the projection copies or derives, never extends.
3. No network access at generation time beyond none at all: the generator is fully offline (metamodel + metaframework paths are inputs).
