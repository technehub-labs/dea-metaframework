# CR-CATALOG-STRUCT-12: State-Grouped Subtrees (top-level retired/, candidates/, research/)

| Field | Value |
|---|---|
| **CR** | CR-CATALOG-STRUCT-12 |
| **Title** | State-grouped subtrees: whole-entity grouping under a top-level state directory, enumerated as ordinary subtrees |
| **Status** | Proposed (this PR) |
| **Layer** | Tooling (catalog repository pattern; entity-storage-layout §3 + §5) |
| **Repository** | `technehub-labs/dea-metaframework` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-10 |
| **Depends on** | CR-CATALOG-STRUCT-01 (standard: per-entity subtree shape), CR-CATALOG-STRUCT-06a (regenerator + gate), CR-CATALOG-STRUCT-06b (conformance suite + state-dir semantics), CR-CATALOG-STRUCT-11 (entity-storage-layout v1.1.0 codification) |
| **Trigger** | Owner directive 2026-11-10 (CR-CATALOG-STRUCT-16 in `dea-catalog-stakeholders`, follow-on review): fully-retired records that retire in place sit mixed with canonical records under `entities/v1-alpha/`, defeating the tree's readability for its primary audience (the owner reviewing what is canonical). The in-place shape was forced by this toolchain: `list_subtrees` (regenerator + gate) and `list_entity_subtrees` (CST) enumerate only direct children of `entities/v1-alpha/`, and every emitted path was hardcoded to the flat prefix, so a subtree under a top-level state directory was invisible to the index and unaddressable by the gates. |

---

## 1. Purpose

Make the tree tell the truth. This CR adds the **state grouping**: a state directory (`research/`, `candidates/`, `retired/`) that sits *directly* under `entities/v1-alpha/` groups whole entity subtrees by state; its direct children enumerate as ordinary entity subtrees everywhere (regenerator, index gate, conformance suite), and the emitted `CATALOG.yaml` paths carry the grouping segment. A catalog can then separate its canonical set from its history on disk without leaving the standard.

The design keeps the two invariants that forced the in-place shape:

- **Id stability**: directory names and record files keep their id-derived form; a move into the grouping recomputes nothing (§5, assign-once).
- **Layout-agnostic tooling**: the grouped shape is an extension of the existing state-dir vocabulary, not a parallel concept; the per-subtree `retired/` shape (a live subtree holding superseded versions) is untouched, so every existing catalog regenerates byte-identically.

## 2. Scope

**In scope**:

- `tools/regenerate_catalog.py`: `list_subtrees` enumerates direct children of top-level state groupings; `_subtree_rel_dir` derives the entity dir from the subtree's actual position; `infer_state`, `entity_path_for`, and the empty-subtree placeholder emit position-true paths.
- `tools/check_catalog_index.py`: `list_subtrees` mirrors the regenerator (the gate's disk-side enumeration and the regenerator's emission agree by construction).
- `tools/conformance_test_catalog_structure.py`: `list_entity_subtrees` enumerates grouped children by the same CST-003 shape rule; `cst_010_retired_lifecycle` gains the grouped mirror (records under the top-level `retired/` grouping must carry `lifecycle_status` retired/deprecated).
- `docs/entity-storage-layout.md`: §3.2 (grouped form + rules), §5 (two-location path probe); version 1.1.0 to 1.2.0.
- Six self-tests: grouped emission with grouping-segment paths (record + research register), gate `--strict` pass on a grouped catalog, orphan detection under the grouping, full-suite conformance on a catalog with a grouping, CST-010 contradiction flag.

**Out of scope**:

- Any catalog repo's actual adoption (each lands its own move CR and its own pin bump; the motivating consumer is `dea-catalog-stakeholders` CR-CATALOG-STRUCT-17).
- ECF-coordinated (containment-tree) repos adopting the grouping: the enumeration rule is depth-agnostic and would work, but no such repo needs it today; adoption stays per-repo.
- The kit generator emitting grouped scaffolds: no kit bootstraps retired records on day one.
- Tagging the release that carries this CR: the pin-bump convention lands each catalog's pin in its own PR against the tag that contains this change.

## 3. Definitions

- **State grouping**: a directory named `research/`, `candidates/`, or `retired/` sitting directly under `entities/v1-alpha/`. The names are reserved at that level; deeper state dirs keep their per-subtree meaning and never group.
- **Grouped subtree**: a direct child of a state grouping; an ordinary entity subtree by the CST-003 shape rule (root `*.yaml` or non-empty state content).
- **Retired-in-place**: a fully-retired record whose subtree stays at the flat location (pre-CR shape; still valid, no longer the only option).

## 4. Design rules

- **R1 (recognition)**: a grouping is recognized by name AND position (direct child of the entities root). A deeper dir named `retired/` is per-subtree content, exactly as before; the CST `_is_state_dir` semantics are unchanged.
- **R2 (enumeration)**: direct children of a grouping enumerate once, never the grouping itself. Content deeper than a grouped subtree's own root does not enumerate (grouped subtrees are leaves of the entity tree).
- **R3 (paths)**: every emitted path is derived from the subtree's position on disk (`_subtree_rel_dir`), replacing the hardcoded `entities/v1-alpha/<dir>` prefix; flat subtrees emit exactly as before (byte-identical regeneration, verified on `dea-catalog-stakeholders` main).
- **R4 (lifecycle agreement)**: CST-010 mirrors its per-subtree rule at the grouping: a record under the top-level `retired/` grouping with an active lifecycle is a conformance failure.
- **R5 (path integrity)**: §5 probes two id-derived locations per record (flat, grouped); ids are never recomputed by a move.

## 5. Tests

- `tests/test_catalog_index_machinery.py`: `test_regenerator_emits_grouped_retired_entity_with_grouped_path`, `test_gate_passes_strict_on_catalog_with_grouped_retired`, `test_gate_flags_grouped_subtree_missing_from_catalog` (24/24 dual-runner).
- `tests/test_conformance_catalog_structure.py`: `test_cst_suite_passes_on_retired_grouping` (full suite on the conforming fixture + a grouped retired subtree, regenerated first), `test_cst_010_flags_active_record_under_retired_grouping`.
- Full suite: 144 passed locally (the two CST-017 git-work-tree self-tests require a git checkout and pass in CI).
- Backward compatibility: the modified regenerator's `--check` passes byte-identically against `dea-catalog-stakeholders` main (23 entities, in-place retired shape), and the v2.7.0+ suite passes 17/17 strict against the same tree.

## 6. Rollout

1. This CR merges; the next release tag carries it.
2. `dea-catalog-stakeholders` CR-CATALOG-STRUCT-17 moves its 11 retired party subtrees into `entities/v1-alpha/retired/` and bumps its CI pin to the release tag carrying this CR (re-vendoring its regenerator + gate copies in the same PR).
3. Other flat-layout repos adopt at their own cadence; no repo is required to group.

## 7. Follow-ons

- Kit-generator scaffold awareness if a kit ever needs a grouped shape from day one.
- The adoption tracker's `conforming` definition gains the grouping as an optional shape (no CST asserts it; CST-010 only guards lifecycle agreement when a catalog chooses to group).
