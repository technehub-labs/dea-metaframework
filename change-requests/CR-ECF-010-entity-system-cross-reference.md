# CR-ECF-010: Entity System Cross-Reference (Metaframework Slice)

| Field | Value |
|-------|-------|
| **CR** | CR-ECF-010 |
| **Title** | Entity System Cross-Reference (Metaframework) |
| **Status** | Proposed (this PR) |
| **Layer** | Meta (cross-reference to `dea-governance`) |
| **Depends on** | CR-BP-121 through CR-BP-125 (the 6-stage institutionalisation in dea-catalog-processes); CR-012 (org-wide entity governance in dea-governance); DEA-ID-000 (foundation paper) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-15 |

## 1. Purpose

This is the **Metaframework cross-reference slice** of the General Entity System institutionalisation programme (CR-BP-121 through CR-BP-125 in dea-catalog-processes). Unlike the single-type catalog slices (BC, BO, OU, ACT, BL, CON, STAKE, TEN), this repo is a **metaframework (ECF + ADRs)** repo and does not contain entity records. The entity system applies differently here:

- The repo's role is to metaframework (ECF + ADRs).
- The entity-system standard itself lives in `dea-governance` (per DEA-ID-000 + CR-012).
- This PR records the cross-reference: the Metaframework repo's commitment to conform its metaframework (ECF + ADRs) output to the General Entity System standard.

## 2. The Metaframework repo's role in the entity-system architecture

The authority model (per DEA-ID-000 section 2):

```
OpenDEAM Architecture Framework  (dea-architecture-framework)
  +- Architectural authority: ADRs that resolve architecture-level conflicts

ECF + Canonical Metamodel        (dea-metaframework + dea-metamodel)
  +- Entity-type definitions, properties, relationships

General Entity System            (dea-governance; THIS REPO's domain)
  +- Identity, lifecycle, references, governance, conformance

Catalog Repositories             (dea-catalog-*; instantiate the metamodel)
  +- Catalog-specific profiles and instances
```

The Metaframework repo is a **metaframework (ECF + ADRs)** repo in this hierarchy. Its output is consumed by the catalog repositories; the catalog repositories' entity-system conformance depends on the Metaframework repo's conformance.

## 3. What this repo commits to

- The metaframework's ECF matrix and ADRs conform to the General Entity System standard's authority model (per DEA-ID-000 section 2).
- The metaframework's ECF Domain + Stage definitions are the canonical reference for entity-type classifications; every catalog's ECF conformance gate consults the metaframework.
- The metaframework's ADRs (ADR-0001, ADR-0004, ADR-0006, ADR-ECF-001 through ADR-ECF-003) codify the architectural decisions that ground the entity-system standard.
- The metaframework's `docs/entity-storage-layout.md` is the canonical reference for the entity-storage layout that the catalog repositories follow.

## 4. The cross-reference

The entity-system standard is documented in:

- **DEA-ID-000**: `dea-governance/docs/design/entity-system-foundation.md` (the foundation paper)
- **CR-012**: `dea-governance/change-requests/CR-012-org-wide-entity-governance.md` (the org-wide governance CR; 12 EGV-001 through EGV-012)
- **CR-BP-121 through CR-BP-125**: `dea-catalog-processes/change-requests/CR-BP-121-*.md` etc. (the 6-stage institutionalisation in the pilot)

The General Entity System comprises 5 concerns (per DEA-ID-000 section 1):

1. Entity identity (Identity Standard IS-001 through IS-006)
2. Entity semantics (Entity Contract Standard EC-001 through EC-004)
3. Entity relationships (Relationship Standard RS-001 through RS-005)
4. Entity lifecycle (Lifecycle Standard LS-001 through LS-007)
5. Entity conformance (Conformance Standard CS-001 through CS-011)

The Metaframework repo's metaframework (ECF + ADRs) output is the foundation for concerns 1, 2, 3, and 5 across all catalog repositories; concern 4 (lifecycle) is per-catalog.

## 5. What this PR is NOT

- **NOT a gate adoption.** No `scripts/check_entity_system.py` is added. The Metaframework repo's output is validated by the catalog repositories' gates; no umbrella gate runs in this repo.
- **NOT a registry addition.** No `reconciliation/entity-system-registry.yaml` is added. The Metaframework repo's metaframework (ECF + ADRs) output does not declare entity records; the entity-system registry is per-catalog.
- **NOT a CI workflow addition.** No `.github/workflows/validate-entity-system.yml` is added. The catalog repositories' CI workflows cover the Metaframework repo's output (via the `conformance` tests).
- **NOT a schema, vocabulary, or ADR change.** This PR is a cross-reference only.
- **NOT a bulk rename.** No existing records renumbered.
- **NOT a metamodel change.** Out of scope (different repo).
- **NOT a cross-catalog URI resolution.** U-01 is deferred to T8.

## 6. Repository changes

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-ECF-010-entity-system-cross-reference.md` | NEW | This file (the cross-reference CR) |
| `change-requests/README.md` | MOD | New row |
| `CHANGELOG.md` | MOD | [Unreleased] entry |

## 7. Acceptance criteria

- AC-01 The cross-reference CR is filed at `change-requests/CR-ECF-010-entity-system-cross-reference.md`.
- AC-02 The Metaframework repo's role in the entity-system architecture is documented (per DEA-ID-000 section 2).
- AC-03 The cross-reference to `dea-governance` (DEA-ID-000 + CR-012) is documented.
- AC-04 The Metaframework repo's commitments are enumerated.
- AC-05 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-06 The 118a/b/c authorship gates remain CONFORMANT (no overlap with this slice).
- AC-07 No entity-system gate, registry, or CI workflow is added to the Metaframework repo (per the cross-reference pattern).

## 8. Out-of-scope follow-ons

- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog URI form (U-01 resolution) + IDM-001 pattern fix. The Metaframework repo's metaframework (ECF + ADRs) output is the foundation for the per-repo ID-pattern fixes.
- **Future catalog adoption**: when any new catalog repository is created, it MUST conform to the General Entity System standard; the cross-reference pattern in this PR is the template.

## 9. Cross-references

- **CR-BP-121 through CR-BP-125**: the 6-stage institutionalisation in `dea-catalog-processes`.
- **CR-DEA-BC-35**: the BC slice of the cross-repo cascade (the single-type slice that established the pattern; this PR adapts the pattern for a metaframework (ECF + ADRs) repo).
- **DEA-ID-000**: the foundation paper in `dea-governance/docs/design/entity-system-foundation.md`.
- **CR-012**: the org-wide governance CR in `dea-governance/change-requests/CR-012-org-wide-entity-governance.md`.
- **T7 of umbrella programme**: the cross-repo cascade (this PR is the Metaframework cross-reference slice).
