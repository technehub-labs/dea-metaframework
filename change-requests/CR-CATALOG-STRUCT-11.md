# CR-CATALOG-STRUCT-11: Directory-Entry Cap (CST-017)

| Field | Value |
|---|---|
| **CR** | CR-CATALOG-STRUCT-11 |
| **Title** | Directory-entry cap: turn the entity-storage-layout §4 shard trigger into enforced conformance (CST-017) |
| **Status** | Merged (this PR) |
| **Layer** | Tooling (catalog repository pattern enforcement; entity-storage-layout §4) |
| **Repository** | `technehub-labs/dea-metaframework` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-10 |
| **Depends on** | CR-CATALOG-STRUCT-01 (standard, §11 conformance contract), CR-CATALOG-STRUCT-06b (conformance suite, CST registry), CR-MET-024 in `dea-catalog-metrics` (the sharding recipe this CST names as the remedy) |
| **Trigger** | Org-wide directory-size audit (owner directive 2026-11-09): the ratified storage contract already pinned the numbers (entity-storage-layout §1: GitHub truncates listings at 1,000 entries; §4: shard before any directory approaches 800) but nothing enforced them outside `dea-catalog-metrics` (whose `tests/test_layout.py` carries the same 800 constant). The audit census found tracked directories at 604 (metrics shard `c/`), 536 (business-services `entities/v1-alpha`, flat) and 518 (business-services `contributions/queue`, flat intake), with the services queue actively growing. A rule that exists only as prose is indistinguishable from a rule that does not exist. |

---

## 1. Purpose

Make §4 executable. This CR adds **CST-017** to the cross-repo conformance suite: no directory in a catalog repo may hold 800 or more tracked entries. It also codifies §4 of `docs/entity-storage-layout.md` (version 1.0.0 to 1.1.0) with the concrete thresholds and names the two enforcement layers, and updates the adoption tracker's definition of `conforming`.

The design follows the CR-MET-024 ruling set, lifted from the metrics corpus to every directory in every catalog repo:

- **R1 (threshold)**: fail at 800 tracked entries per directory; GitHub truncates listings at 1,000, so 800 leaves 200 entries of remediation headroom.
- **R2 (counting surface)**: count what a GitHub listing would show, i.e. **git-tracked** content only. When the catalog root is a git work tree, the census runs over `git ls-files` output; a fat untracked `.venv` or build directory can never fail the gate (the business-capabilities clone carries a 2,000-file untracked `.venv` that is not even gitignored). When the root is not a git repo (a bare checkout, a tmp fixture), the census falls back to a filesystem walk that skips the known untracked-noise directories (`.git`, `.venv`, `node_modules`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.idea`, `.vscode`, `.metaframework`).
- **R3 (semantics)**: an "entry" is exactly what a GitHub listing shows: a file or a subdirectory. Every tracked file adds one to its parent; every directory holding tracked content is itself one entry in its own parent. The census covers the **whole repo**, not just `entities/`: the live failure mode is an unsharded flat concern (a `change-requests/` directory, a contribution intake queue), not the containment tree (worst case ~15 entries per directory).
- **R4 (remedy pointer)**: the failure message names the remedy, because a gate that says only "800 entries" invites ad-hoc fixes that break the §5 path-integrity contract: introduce a shard level per the CR-MET-024 recipe (first character of the slug, `0-9` fallback, ids byte-identical, tooling moved to recursive walking in the same change).

## 2. Scope

**In scope**:

- CST-017 in `tools/conformance_test_catalog_structure.py` (registered in `CST_TESTS`; CST-016 stays invoked separately in `run()` because it needs the template root).
- Four self-tests in `tests/test_conformance_catalog_structure.py` (see §5).
- `docs/entity-storage-layout.md` §4 codification and version bump 1.0.0 to 1.1.0.
- `docs/standards/catalog-repository-pattern-adoption.md`: the `conforming` status definition now reads CST-001..CST-017, with the pin-bump caveat.
- Drive-by (separate defect, same PR for a green CI run): the consumer live-fetch test pinned `dea-catalog-stakeholders` at `counts.entities == 0`, stale since stakeholders was populated on 2026-11-08 (register v9: 11 canonical); replaced with a growth-tolerant `>= 1` assertion, leaving count truth to governance R3.

**Out of scope**:

- Wiring the conformance suite into the kit generator's emitted CI: a freshly bootstrapped kit legitimately has no `CATALOG.yaml` yet (the bootstrap contract pins its absence), so the full CST suite cannot run there from day one; the CST lifecycle for kits needs its own CR.
- Per-repo pin bumps to v2.7.0 (each repo lands its own, per the "bump `ref:` deliberately, in its own PR" convention).
- The org-wide weekly audit rule (R5 in `dea-governance/registers/reconcile_portfolio.py`, its own CR in that repo).
- Remediation of any current hot directory (business-services sharding lands in its own repo CR).

## 3. Definitions

- **Entry**: one line of a GitHub directory listing: a file or a subdirectory.
- **Hot directory**: a directory holding 800 or more tracked entries.
- **Shard level**: a directory level inserted under a hot parent, keyed on content that is stable per record (the CR-MET-024 R1 ruling: first character of the slug; `0-9` for digit-leading slugs), so §5 keeps holding.

## 4. Design

### 4.1 Counting

`_tracked_relpaths()` resolves the tracked file list via `git -C <root> ls-files -z` (60 s timeout; non-zero exit or absent git means "not a work tree" and the caller falls back). `_entry_counts_from_paths()` derives per-directory counts in one pass. `_entry_counts_from_walk()` mirrors the semantics for non-git roots. Threshold constants live at module level next to the section header, mirroring `dea-catalog-metrics/tests/test_layout.py` (`MAX_SHARD_ENTRIES = 800`).

### 4.2 Failure shape

Offenders are reported worst-first, one `check()` per directory, in the existing accumulator style, e.g.:

```
FAIL: CST-017: contributions/queue holds 812 entries (shard trigger 800; GitHub truncates listings at 1000); introduce a shard level (entity-storage-layout.md §4; CR-MET-024 recipe)
```

The repo root is reported as `<repo root>`. No warning tier: the CST exit-code contract stays 0/1/2 and warnings remain reserved for advisory CSTs (CST-009, CST-013/014 vendored, CST-016); the advisory watch tier (500+) belongs to the org-level weekly audit, where a finding would otherwise be a surprise to a repo that has not re-synced its pin yet.

### 4.3 Codified §4

`docs/entity-storage-layout.md` §4 now states the trigger (800), both enforcement layers (CST-017 PR-time; governance R5 weekly over every registered repo), and the remedy recipe with the metrics reference implementation, replacing the two stale prose bullets (which still said "currently 32 for capabilities, 18 for services").

## 5. Acceptance criteria

1. `pytest -q tests/ tools/cross_repo_consumer/tests/` passes (141 tests; standalone runner of the self-suite passes too).
2. The four new CST-017 tests pass and fail against the previous suite state for the right reason: conforming fixture exits 0; a non-git fixture directory with exactly 800 files exits 2 naming `contributions/queue` and the remedy; a git work tree with 850 **untracked** noise files exits 0; a git work tree with 805 **tracked** entries exits 2 naming the directory.
3. CST-017 run against the current org clones passes everywhere (worst tracked directories today: metrics `entities/v1-alpha/c` at 604, business-services `entities/v1-alpha` at 536, business-services `contributions/queue` at 518, all under the trigger), so the gate lands green and tightens from here.
4. The suite's stable exit-code contract is unchanged (0 success, 1 filesystem error, 2 conformance failures); `--cst CST-017` filtering works; the all-CST summary count reports 17.

## 6. NOT-List

- **No id system change**: CST-017 reads the filesystem; it does not touch ids, paths, or CATALOG.yaml.
- **No template or TEMPLATE_VERSION change**: the template's behavior is unaffected; TEMPLATE_VERSION stays 0.1.0 so CST-016 raises no new drift warnings on bootstrapped repos.
- **No threshold tunable**: 800 is the ratified §4 number, not a flag. Repos do not get to configure their way past the cap.
- **No entities-only scoping**: the census is repo-wide by design (see R3).
- **No new dependency**: the suite remains stdlib-only (plus PyYAML, already required).
- **No release cut in this CR**: the v2.7.0 tag is cut at merge time so consumer repos have a pin target; the pin bumps themselves are per-repo PRs (template `ci.yml` and the kit generator keep v2.6.0 until that follow-up, per the "bump `ref:` deliberately" convention).

## 7. Risks

| Risk | Mitigation |
|---|---|
| A catalog re-syncs its pin and goes red on a hot directory it did not know about | That is the gate working; the remedy is mechanical (CR-MET-024 recipe) and the weekly R5 watch tier (500+) gives early warning before any pin bump forces the issue |
| `git ls-files` counts the index, not HEAD, so staged-but-uncommitted files count | Intentional: CI checkouts never have a dirty index, and locally the staged tree is what the next push shows |
| Submodule paths count as one entry (the submodule dir), not their contents | Same as a GitHub listing; acceptable |

## 8. References

- `docs/entity-storage-layout.md` §1, §4, §5 (v1.1.0)
- `dea-catalog-metrics/change-requests/CR-MET-024.md` (sharding recipe; R4 bucket guard)
- `dea-catalog-metrics/tests/test_layout.py` (`MAX_SHARD_ENTRIES = 800`, the per-repo guard precedent)
- `dea-governance/registers/reconcile_portfolio.py` (R5 weekly audit; separate CR in that repo)
