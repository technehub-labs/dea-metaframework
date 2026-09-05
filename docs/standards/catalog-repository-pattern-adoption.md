# Adoption Tracker: Catalog Repository Standard

**Standard**: [catalog-repository-pattern.md](./catalog-repository-pattern.md)
**Owner**: TechNeHub Labs
**Last updated**: 2026-09-05

This document tracks adoption of the catalog repository standard (CR-CATALOG-STRUCT-01) across every TechNeHub Labs catalog repo.

## Status values

| Status | Meaning |
|---|---|
| `not-started` | No adoption PR opened. |
| `in-progress` | PR opened but not merged. |
| `partial` | Layout adopted (step 1); research distribution (step 2) or contribution flow (step 3) pending. |
| `conforming` | All three migration steps complete; conformance tests CST-001..CST-015 pass; CI gate green. |
| `exempted` | Explicit waiver granted by the metaframework; rationale and sunset date recorded. |

## Adoption register

| Repo | Adoption CR | Status | Conformance tests | PR | Notes |
|---|---|---|---|---|---|
| `dea-catalog-processes` | CR-CATALOG-STRUCT-02 | conforming | passing | #21 | First adoption CR; lands the standard end-to-end. 2 canonical entities; 3 research files moved into `dea:group-customer-lifecycle-management/research/`. CI runs regenerator + gate + 6 existing validators + conformance suite (16/16 CSTs pass under `--strict`). STRUCT-07 (cross-repo consumer) now unblocked. |
| `dea-catalog-business-capabilities` | CR-CATALOG-STRUCT-03a+03b | conforming | passing | #44 + #45 | Largest adoption slice: 26 canonical entities in per-entity subtrees; CAND-018 boundary decision lives with `dea:capability-analytics-and-intelligence/research/`; 31 catalog-wide CR-DEA-BC-02 execution artifacts in new `catalog-research/`; 9 SVG visuals + manifest in new `visuals/` (separate from `docs/`); `docs/research/` removed. CI runs regenerator + gate + 3 existing validators + conformance suite (16/16 CSTs pass under `--strict`). All five pre-existing workflows still run; `validate-entries.yml` was updated to filter state-directory files (research/, candidates/, retired/) from entry validation. STRUCT-07 (cross-repo consumer) now has two conformant adopters. |
| `dea-catalog-digital-business-service-factory` | CR-CATALOG-STRUCT-04 | conforming | passing | #6 | First adoption CR for DBSF. 18 `BusinessService` entries split from 6 domain-grouped YAMLs into per-entity subtrees (`entities/v1-alpha/dea:service-*`); 2 capability maps moved to `mappings/capability-maps/`; `CATALOG/index.yaml` and `CATALOG/v1-alpha/index.yaml` deleted (superseded by `CATALOG.yaml`); governance contract kept at `CATALOG/v1-alpha/governance-contracts/`. Vendored regenerator + gate + schema + one-shot extractor. CI: `catalog-conformance.yml` (new) + `validate-allocation.yml` (existing, pinned to `dea-architecture-framework@v0.2.1`). 16/16 CSTs pass under `--strict`. STRUCT-07 now has three conformant adopters. |
| `dea-catalog-stakeholders` | CR-CATALOG-STRUCT-05 | conforming | passing | #3 | Scaffold adoption: pre-wire the standard before any entity is added. Vendored regenerator + gate + schema; `catalog-conformance.yml` workflow; `CATALOG.yaml` (0 entities) + `TEMPLATE_VERSION` (0.1.0); `change-requests/`, `classifications/`, `contributions/` with `.gitkeep`. Existing `ci.yml` (entry validator) and `validate-allocation.yml` (OpenDEAM pin) preserved. 16/16 CSTs pass under `--strict`. Phase 2 readiness items (dsanders11 multiline-glob limitation, early-exit on empty entities/) noted in CR for the contributor who adds the first entity. STRUCT-07 now has four conformant adopters (all L1 catalogs). |
| (any new catalog repo, future) | n/a (scaffolded from template) | n/a | n/a | n/a | New repos MUST be bootstrapped from `dea-metaframework/tools/catalog-repo-template/`. |

## Cross-repo consumer

The cross-repo consumer (CR-CATALOG-STRUCT-07) is implemented as a three-PR stack:

- **STRUCT-07a** lands the consumer module in `dea-metaframework/tools/cross_repo_consumer/` (dataclasses + parser + urllib fetcher + CLI; stdlib-only; 29 pytest tests).
- **STRUCT-07b** integrates the module into the metamodel viewer (`dea-metamodel/viewer/`).
- **STRUCT-07c** adds an `dea-architecture-framework/` smoke test that uses the module to verify cataloged entities match the OpenDEAM model.

| Consumer | CR | Status | PR | Notes |
|---|---|---|---|---|
| `dea-metaframework/tools/cross_repo_consumer/` | CR-CATALOG-STRUCT-07a | merged | #19 | Reference consumer module + 29 pytest tests. Stdlib-only. Live CLI rollup confirms all four adopters' CATALOG.yaml parse cleanly. The follow-up PR adds the `pytest tools/cross_repo_consumer/tests/` step to the metaframework CI workflow. |
| `dea-metamodel/viewer/` | CR-CATALOG-STRUCT-07b | not-started | n/a | Integrate the consumer into the viewer; rebuild entity-graph.json so each card surfaces catalog content (count, last_modified, lifecycle_status histogram). Lands after STRUCT-07a. |
| `dea-architecture-framework/` | CR-CATALOG-STRUCT-07c | not-started | n/a | Smoke test using the consumer module to verify cataloged entities match the OpenDEAM model. Lands with viewer PR or after. |

## Sequencing rule

1. **STRUCT-01** (this standard) + **STRUCT-06** (regenerator + conformance tests + template) MUST merge before any adoption CR.
2. **STRUCT-02** + **STRUCT-06** MUST merge before **STRUCT-07** (cross-repo consumer). The consumer needs at least one conforming catalog to be useful.
3. Adoption CRs (STRUCT-02..05) are independent of each other and may land in any order.
4. New catalog repos are pre-wired from the template; no adoption CR needed.

## Updates

Update this document whenever an adoption CR is opened, merged, or its status changes. Update is a CR or a docs-only PR; the latter requires maintainer review.
