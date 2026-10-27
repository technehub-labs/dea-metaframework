# CR-ECF-011: Regenerator Open-CR Counter Fix (Status Tokens, Both Metadata Shapes, Org-Consistent Closed Set)

| Field | Value |
|-------|-------|
| **CR** | CR-ECF-011 |
| **Title** | Regenerator Open-CR Counter Fix (status tokens, both metadata shapes, org-consistent closed set) |
| **Status** | Proposed (this PR) |
| **Layer** | Catalog index machinery (`tools/regenerate_catalog.py`, vendored by every catalog repo) |
| **Depends on** | None (ratified downstream: CR-BP-114 design in `dea-catalog-business-processes`; CR-DEA-BC-38 landed in `dea-catalog-business-capabilities` PR #91; CR-CATALOG-STRUCT-08 landed in `dea-catalog-stakeholders` PR #8) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Problem

`tools/regenerate_catalog.py` `count_open_change_requests` (`:499-529` at `main` @ `3ad9bdd`) computes `counts.open_change_requests` wrongly for every catalog repo that vendors it:

1. **Duplicated condition** (`:519`): `if "Status**: Merged" in head or "Status**: Merged" in head:` — the second operand was meant to be a different closed status. Copy-paste origin of the family (processes vendored copy carried the identical line at its `:466`).
2. **Closed set is `Merged`-only**, while the org's CR status vocabularies are Landed/Applied/Accepted/Superseded/Withdrawn/Merged — every CR in a repo that never writes the literal word `Merged` counts open forever.
3. **Substring matching over the whole head** — a CR that *quotes* a status line in its body (e.g. a carrier documenting this very bug) is misclassified by the quotation. Observed live: the stakeholders carrier CR-CATALOG-STRUCT-08 quotes the buggy `:519` line within its first 30 lines and the substring check counted that file as closed.
4. **Table-format CR metadata** (`| **Status** | Merged (PR #91) |`, the house shape used by capabilities and stakeholders CRs) is invisible; those files fall through to "conservative open" regardless of their real status.

Net effect: `open_change_requests` in every generated `CATALOG.yaml` is untrustworthy in both directions (over- and under-counting), which matters because catalog repos run `regenerate_catalog.py --check` as a blocking CI freshness gate.

The same defect has now been fixed independently in three vendored copies (processes by CR-BP-114's design, capabilities by CR-DEA-BC-38 / PR #91, stakeholders by CR-CATALOG-STRUCT-08 / PR #8). This CR fixes it once at the source so the vendored copies can re-vendor instead of diverging.

## 2. Design (ported from the landed downstream fixes)

Replace the substring probing with a status-token parser:

- `CLOSED_CR_STATUSES = {Merged, Landed, Applied, Accepted, Rejected, Superseded, Withdrawn}` — the org-consistent set as landed in capabilities PR #91 (superset of the CR-BP-114 set ratified in processes).
- `_cr_status_token(head)`: first Status line in the head (first 30 lines) parsed from **either** metadata shape — `**Status**: X` or `| **Status** | X |` — reduced to a bare token by cutting at the first `(`, `;`, or `,` (so `Merged (PR #91)` -> `Merged`).
- Classification: token in the closed set -> closed; otherwise (Proposed, Draft, unknown token, no status line) -> **conservative open**, preserving the existing semantics.

Documented conservatism: a terminal status word followed by unpunctuated prose (`Landed on main via PR #9`) does **not** close — the token is the full phrase. Houses that want closure write landing evidence inside separator-delimited context (`Landed (via PR #9)`), which is the shape the catalog repos already use.

## 3. Tests (`tests/test_catalog_index_machinery.py`)

Seven new tests in the module's house style (fixture catalog, subprocess CLI, `check()`, dual-runner):

1. Every terminal status in the closed set closes (line format).
2. Table format with trailing context closes (`Merged (PR #91)`, `Landed; see PR #42`).
3. Proposed/Draft count open in both formats.
4. Status-less CR counts open (conservative semantics preserved).
5. Mixed catalog exact count.
6. **First-status-line-wins**: a CR quoting a status line in its body is classified by its metadata line, not the quotation (the observed bypass of the substring approach).
7. Prose-continuation statuses count open (documents the conservatism).

Suite: 20/20 machinery tests under pytest and under the standalone `run_all()`; repo full suite 90/90.

## 4. Downstream impact and re-vendor path

- Catalog repos pin their CI toolchain checkout to `v2.6.0`, which does **not** contain this fix; they are unaffected until the next release tag. The next tag cut after this merges should carry it (the `v2.6.0` release note already established the pattern: cut a tag so template consumers can pin to fixed tooling).
- Vendored copies: `dea-catalog-business-capabilities` and `dea-catalog-stakeholders` already carry equivalent per-repo fixes (their CI runs the vendored copy, so they are correct today); re-vendoring after the next tag replaces the divergence with the upstream code. `dea-catalog-business-processes` fixed its copy via CR-BP-114's design. `dea-catalog-business-services` deliberately adopted a data-side fix (statuses written as `Merged`) because its CI runs the pinned upstream copy — this CR makes the eventual re-pin carry the full behavior.
- No interface change: exit codes, CLI flags, `CATALOG.yaml` shape all unchanged; only the value of `counts.open_change_requests` becomes truthful.

## 5. NOT-List

- No change to `tools/check_catalog_index.py` or the index schema.
- No change to the authorship gate or CST suite.
- No template (`tools/catalog-repo-template/`) change — the template vendors tooling at adoption time and each repo's vendored copy governs itself; a coordinated re-vendor sweep is a follow-on after the next release tag.
- No release-tag cut in this PR (release is the maintainer's call; §4 records the recommendation).

## 6. Acceptance criteria

- AC-01 `pytest -q tests/` passes (90+ tests) and `python tests/test_catalog_index_machinery.py` prints `OK: 20 machinery test(s) passed`.
- AC-02 The duplicated `"Status**: Merged"` condition no longer appears in `tools/regenerate_catalog.py`.
- AC-03 `_cr_status_token` parses both metadata shapes; covered by tests 1-2.
- AC-04 Conservative-open semantics preserved (status-less, unknown token, prose continuation) — covered by tests 4, 7.
- AC-05 CHANGELOG `[Unreleased]` entry added; `change-requests/README.md` gains the CR-ECF-011 row.
