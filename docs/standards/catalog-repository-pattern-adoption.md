# Adoption Tracker: Catalog Repository Standard

**Standard**: [catalog-repository-pattern.md](./catalog-repository-pattern.md)
**Owner**: TechNeHub Labs
**Last updated**: 2026-09-04

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
| `dea-catalog-processes` | CR-CATALOG-STRUCT-02 | not-started | pending | n/a | 2 canonical entities; 3 research files in `docs/research/`. Step 1: create subtrees for both entities. Step 2: distribute `docs/research/l1-*.yaml` into `dea:process-manage-customer-relationship/research/` and `dea:group-customer-lifecycle-management/research/`. |
| `dea-catalog-business-capabilities` | CR-CATALOG-STRUCT-03 | not-started | pending | n/a | Largest current catalog (~30 capabilities + ~30 research files). Step 1: create subtrees for every capability. Step 2: distribute `docs/research/*` into per-entity subtrees by YAML-field classification. |
| `dea-catalog-digital-business-service-factory` | CR-CATALOG-STRUCT-04 | not-started | pending | n/a | Has flat `CATALOG/v1-alpha/*.yaml` files. Step 1: convert each to a per-entity subtree. No top-level research dir to distribute. |
| `dea-catalog-stakeholders` | CR-CATALOG-STRUCT-05 | not-started | pending | n/a | Scaffold repo (no entities yet). Adoption = pre-wire the standard before any entity is added. Step 1: copy regenerator + gate from template; CI workflow; conformance tests. |
| (any new catalog repo, future) | n/a (scaffolded from template) | n/a | n/a | n/a | New repos MUST be bootstrapped from `dea-metaframework/tools/catalog-repo-template/`. |

## Cross-repo consumer

| Consumer | CR | Status | PR | Notes |
|---|---|---|---|---|
| `dea-metamodel/viewer/` | CR-CATALOG-STRUCT-07 | not-started | n/a | Migrates viewer to read `CATALOG.yaml` from each catalog. Lands after STRUCT-02 + STRUCT-06 merge. |
| `dea-architecture-framework/` | CR-CATALOG-STRUCT-07 | not-started | n/a | Same migration as viewer; lands with viewer PR. |

## Sequencing rule

1. **STRUCT-01** (this standard) + **STRUCT-06** (regenerator + conformance tests + template) MUST merge before any adoption CR.
2. **STRUCT-02** + **STRUCT-06** MUST merge before **STRUCT-07** (cross-repo consumer). The consumer needs at least one conforming catalog to be useful.
3. Adoption CRs (STRUCT-02..05) are independent of each other and may land in any order.
4. New catalog repos are pre-wired from the template; no adoption CR needed.

## Updates

Update this document whenever an adoption CR is opened, merged, or its status changes. Update is a CR or a docs-only PR; the latter requires maintainer review.
