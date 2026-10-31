# CR-ECF-012: ECF Coordinate Identifier Finalization (And-Stripped Convention)

| Field | Value |
|---|---|
| **CR** | CR-ECF-012 |
| **Title** | ECF coordinate identifier finalization: adopt the And-stripped DOMAIN_ID convention as normative |
| **Status** | Merged (this PR) |
| **Layer** | ECF contract (coordinate specification §4 execution) |
| **Repository** | `technehub-labs/dea-metaframework` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-31 |
| **Depends on** | CR-ECF-005 (identifier deferral), CR-ECF-006/007/008 (domain renames that produced the deprecated alias set) |
| **Trigger** | A capability-admission PR failed the consumer ECF drift gate with identifier-form errors, exposing a dual source of truth: `tools/ecf_coordinates.py` built And-kept identifiers by generic camelization (`financeAndAccounting`) while the metamodel's `detect_drift.py` `DOMAIN_ID` map — the convention every catalog, gate, and script actually implements — carries the And-stripped form (`financeAccounting`). |

## 1. Executive summary

This CR executes the identifier finalization deferred by CR-ECF-005 §3 and specification §2 ("checked against the OpenDEA semantic-ID conventions in dea-metamodel before this representation is finalised"): the metamodel convention is adopted as normative. `tools/ecf_coordinates.py` gains the explicit `DOMAIN_ID` table and `coordinate_identifier()` builds from it; `specification/ecf-coordinates.md` §4 is restated; the conformance suite pins the convention literally. Zero downstream consumers of the And-kept form existed (census: only `test_005_coordinate_spec.py` called the builder), so nothing else needed migration; catalogs were already conformant.

## 2. The convention

And-stripped lowerCamel for six domains; `enablementAndOperations` keeps its connective (the "enablement operations" reading would be lost — the same historical reasoning the metamodel map records). Deprecated identifier forms (`operationsEnablement`, `peopleAndOrganization`) resolve through the existing `DOMAIN_ALIASES` chain upstream of the builder; `DEPRECATED_DOMAIN_ID_ALIASES` documents the identifier-level forms.

## 3. Changes

1. `tools/ecf_coordinates.py`: `DOMAIN_ID` table + rewritten `coordinate_identifier()` (stages lowercased; generic `camel_case` retired); `DEPRECATED_DOMAIN_ID_ALIASES` documented.
2. `specification/ecf-coordinates.md` §4 restated with the finalization note (and §2's deferral discharged).
3. `tests/conformance/test_005_coordinate_spec.py`: new `test_domain_identifier_convention_table` pinning all 49 identifiers against the literal convention (self-consistency alone cannot catch a convention regression).
4. Cross-repo mirror guarantee: the metamodel's mirror test (its CR-MET-018) asserts `coordinate_identifier == DOMAIN_ID` equality for all 49 pairs in its CI, so the two repos cannot drift apart silently again.

## 4. Census (evidence for the zero-migration claim)

Wrong And-kept forms exist in committed artifacts only in `dea-catalog-business-processes` (11 entity files + reconciliation/scripts) and one capabilities script — repaired by the respective repos' own CRs (metamodel CR-MET-018 reconciliation programme; capabilities CR-DEA-BC-67 §scope). No metaframework artifact carries a wrong form except the superseded spec table and the retired builder behavior.

## 5. Acceptance criteria

1. Full metaframework suite green (106 tests).
2. All 49 identifiers match the convention table literally.
3. Spec §4/§2 agree with the code.

## 6. NOT-list

1. No domain or stage rename; no enum change.
2. No catalog data migration in this repo.
3. `DOMAIN_ALIASES` (PascalCase display resolution) unchanged.
