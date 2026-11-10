# CR-CATALOG-STRUCT-13: Release-Pin Truth Check (CI `pins-resolve`)

| Field | Value |
|---|---|
| **CR** | CR-CATALOG-STRUCT-13 |
| **Title** | Release-pin truth check: every advertised metaframework pin must resolve to an existing release tag |
| **Status** | Merged (this PR) |
| **Layer** | Tooling (release discipline enforcement) |
| **Repository** | `technehub-labs/dea-metaframework` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |
| **Depends on** | CR-CATALOG-STRUCT-11 (the pin-bump discipline this gate enforces), CR-CATALOG-STRUCT-12 (the release whose consumer-facing 404 motivated this gate) |
| **Trigger** | 2026-11-11: a consumer (`dea-catalog-stakeholders` `catalog-conformance.yml`) pinned `ref: v2.8.0` while the release did not exist; every run 404'd at the checkout until the tag was cut. The ordering rule (land the change, cut the release, bump the pins in their own PR) existed only as convention; nothing enforced it. |

---

## 1. Purpose

Make the ordering rule executable. `tools/check_release_pins.py` scans every metaframework release-tag pin this repository advertises (the template's CI fetch, the kit generator's `metaframework_pin:` manifest note, its emitted workflow's upstream checkout, and the emitted README dependency-table row), and fails when a pinned tag does not exist on origin (`git ls-remote --tags`). The failure message carries the remedy and the order: cut the release at the intended merge commit first, then bump pins.

A pin merged ahead of its release is a distributed outage, not a cosmetic drift: every consumer that re-syncs onto it 404s at checkout. The gate runs at the only place the bump can be caught before consumers see it: this repository's own CI (`pins-resolve` job). Org-wide, the same defect class is watched weekly by the governance reconciler's pin-truth rule (dea-governance CR-021), which audits every registered repo's CI pins against this repository's tag set.

## 2. Scope decisions

- **Extraction is step-scoped**: a `ref:` counts only inside a step that names `technehub-labs/dea-metaframework`, so the emitted validate-allocation step's root-model pin (`dea-architecture-framework@{root_ref}`) is never mistaken for a metaframework pin.
- **Tag-form only**: `ref: main` is a floating pin, not a release-tag pin; it is out of scope here (org-wide floating-pin watching is the governance rule's watch tier).
- **Prose counts**: the vendored authorship-fields comments cite real tags historically; citing a nonexistent tag in prose is the same defect, so table/prose forms (`metaframework vX.Y.Z`) are checked too.
- **Transport honesty**: an `ls-remote` failure exits 2 without findings (a finding never fires on a flake, CR-014 convention).
- **Self-tests offline + one live test**: 5 offline extraction tests (step scoping, pin/table forms, prerelease suffix, branch-ignored) plus a live test mirroring the CI job; dual-runner.

## 3. Verification

1. Live positive: current tree advertises v2.6.0 (prose, vendored authorship-fields) and v2.7.0 (template CI + generator); both resolve; exit 0.
2. Negative (proved before landing): a scan root whose generator pins `v99.99.99` fails with exit 1 and the remedy message.
3. `tests/test_check_release_pins.py`: 6 tests, dual-runner green.
4. CI: new `pins-resolve` job runs the checker and its self-tests.

## 4. NOT-List

- **No release automation**: the gate fails the bad order; it does not cut tags. Tag cutting stays a deliberate human step (release notes carry the CR summary).
- **No consumer-repo enforcement here**: consumers are covered by CST-013/014 (pin format) and governance R6 (pin existence, weekly).
- **No root-model or other-upstream pins**: scoped to metaframework's own toolchain.
- **No toolchain pin change in this CR**: template/generator stay at v2.7.0; v2.8.0 bumps happen in consumers' own PRs when they adopt CR-CATALOG-STRUCT-12.

## 5. Acceptance criteria

1. `pins-resolve` green in CI on this PR.
2. Negative test reproducible: `python tools/check_release_pins.py --root <temp-root-with-fake-pin>` exits 1.
3. Full suite unchanged: 141 + 6 new tests.
