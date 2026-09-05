# CR-CATALOG-STRUCT-07a: Cross-Repo Consumer Module

**Status**: Proposed
**Layer**: L0 (Metaframework; tooling)
**Owner**: TechNeHub Labs
**Depends on**: CR-CATALOG-STRUCT-01, CR-CATALOG-STRUCT-06a (regenerator), all four adoption CRs (STRUCT-02/03/04/05)
**Companion to**: CR-CATALOG-STRUCT-07 (the full STRUCT-07 slice; 07a is the infrastructure PR; 07b + 07c land separately against the viewer and `dea-architecture-framework`)

## What this CR is

Lands the first PR of the three-PR STRUCT-07 stack: a Python module in `dea-metaframework/tools/cross_repo_consumer/` that implements the §9 cross-repo consumer contract. The module exposes typed `Catalog`, `CatalogEntity`, `CatalogCounts`, `CatalogMetadata` dataclasses plus a `fetch_catalog_yaml()` HTTP layer (urllib, no extra deps). It does NOT change the viewer or `dea-architecture-framework`; those integrations are STRUCT-07b and 07c respectively.

After this lands, any consumer can:

```python
from tools.cross_repo_consumer import fetch_catalog_yaml, parse_catalog_yaml, summary

result = fetch_catalog_yaml("dea-catalog-processes")
catalog = parse_catalog_yaml(result.bytes)
print(summary(catalog))
# BP |   2 entities (2 canonical, 0 candidates, 0 retired) |    1.0.0 | Business Process
```

## Decisions locked during planning

- **Q1 (scope)**: metaframework module + tests only. The viewer (`dea-metamodel/viewer/`) and AF (`dea-architecture-framework/`) integrations land in 07b and 07c as separate PRs.
- **Q2 (HTTP layer)**: stdlib `urllib.request.urlopen` + `pyyaml.safe_load`. No `requests`, no `httpx`. Keeps the metaframework's zero-non-test-deps posture.
- **Q3 (caching)**: opt-in `--cache-dir` flag; the fetcher writes `<repo>@<ref>.yaml` per-call and returns the cache hit on subsequent calls.
- **Q4 (CI on the metaframework side)**: add a small unit-test step to the metaframework CI that exercises the parser + the offline fetcher. Live fetch is opt-in via `pytest -m network`.

## What changes

### Files added

- `tools/cross_repo_consumer/__init__.py` (~225 lines): dataclasses + `parse_catalog_yaml` + `summary` + `aggregate_summary`.
- `tools/cross_repo_consumer/fetch.py` (~125 lines): `fetch_catalog_yaml` + `fetch_many` + `FetchResult` dataclass.
- `tools/cross_repo_consumer/cli.py` (~100 lines): `python -m tools.cross_repo_consumer.cli` entry point with `--repos`, `--ref`, `--cache-dir`, `--offline`, `--timeout` flags.
- `tools/cross_repo_consumer/tests/__init__.py`: test package marker.
- `tools/cross_repo_consumer/tests/conftest.py`: registers the `network` marker.
- `tools/cross_repo_consumer/tests/test_catalog_parser.py` (~320 lines): 26 tests covering parsing, dataclasses, helpers, offline-fetch, and module surface.
- `tools/cross_repo_consumer/tests/test_cli.py` (~100 lines): 3 tests covering CLI parsing, run paths, and the live network smoke test.
- `01_plan/pr-struct-07a.md` (untracked PR body draft).

### Files changed

None. This CR is additive only; it does not modify the regenerator, the gate, the conformance suite, or the standard itself. STRUCT-07b and 07c land the consumer-side changes.

## Two-state semantics (important for future consumers)

The regenerator emits TWO distinct state fields per entity:

- `state` (structural): `research`/`candidate`/`canonical`/`retired`. Answers "where does the canonical YAML live in the subtree?"
- `lifecycle_status` (semantic): `active`/`candidate`/`retired`/etc. Answers "what does the entity say about itself?"

The dataclass exposes both. A canonical-state entity can have any `lifecycle_status`; the two are not redundant. The standard's §11 conformance suite does not constrain either; the regenerator emits both.

## CI on the metaframework side

The metaframework's existing CI workflow runs the conformance suite (`conformance_test_catalog_structure.py`). After this lands, add:

- A `python -m pytest tools/cross_repo_consumer/tests/` step in the metaframework workflow (excludes the `network` mark by default; a separate weekly cron with `-m network` verifies the live fetch path).

## Verification

Local run, all green:

- `python -m pytest tools/cross_repo_consumer/tests/` returns `29 passed, 1 skipped`.
- The skipped test is `test_live_fetch_against_real_catalog` (`network` mark), which makes a single live fetch against `dea-catalog-stakeholders` and asserts the live `CATALOG.yaml` parses cleanly. CI deselects it via `-m "not network"`.
- `python -m tools.cross_repo_consumer.cli --offline --cache-dir /tmp/cache` (with the four adopters' `CATALOG.yaml` copied into `/tmp/cache/<repo>@main.yaml`) prints the four-catalog rollup:
  ```
  abbrev |  entities | canon | cand | ret |     meta | name
  ---------------------------------------------------------
      BC |  26 entities (26 canonical, 0 candidates, 0 retired) |    1.0.0 | Business Capability
      BP |   2 entities (2 canonical, 0 candidates, 0 retired) |    1.0.0 | Business Process
    DBSF |  18 entities (18 canonical, 0 candidates, 0 retired) |   ^0.2.1 | Digital Business Service Factory
      SH |   0 entities (0 canonical, 0 candidates, 0 retired) |   ^0.2.1 | Stakeholders
  ```
- Dash sweep on new code: clean.
- Secret scan: 0.
- `git diff --check`: clean.

## Security

- The fetcher targets `https://raw.githubusercontent.com/`, the public read-only endpoint per the §9 contract. It does NOT carry or strip credentials.
- The dataclasses are `frozen=True`; the parser is read-only and never writes files outside the explicit `cache_dir` (passed by the caller).
- No PATs or tokens in any committed file.

## What STRUCT-07b + 07c add (out of scope here)

- **STRUCT-07b (`dea-metamodel/viewer/`)**: integrate the consumer into the metamodel viewer; rebuild `entity-graph.json` so each entity card surfaces catalog content (count + last_modified + lifecycle_status histogram). The viewer bundles the data at build time (Pages sites can't easily fetch cross-origin from `raw.githubusercontent.com`).
- **STRUCT-07c (`dea-architecture-framework/`)**: a `scripts/check_catalog_index_matches_model.py` smoke test that fetches every known catalog and verifies the entity IDs match the OpenDEAM model expectations.

## Sequencing

After this merges:

| Slice | Status |
|---|---|
| STRUCT-01 | Merged |
| STRUCT-06a | Merged |
| STRUCT-06b | Merged |
| STRUCT-02 | Merged (PR #21) |
| STRUCT-03 | Merged (PR #44 + #45) |
| STRUCT-04 | Merged (PR #6) |
| STRUCT-05 | Merged (PR #3) |
| STRUCT-07a | This PR |
| STRUCT-07b | next slice (viewer integration) |
| STRUCT-07c | third slice (AF smoke test) |