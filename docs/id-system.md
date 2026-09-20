# DEA Org-Wide ID System

**Version**: 1.0.0
**Date**: 2026-09-20
**Status**: Ratified
**Owner**: Coder (for eaojnr)
**Scope**: Org-wide. All `dea-catalog-*` repos, all `dea-metaframework` consumers, all CI gates.

---

## 1. Purpose

Every canonical record in every DEA catalog repo carries an `id:` field that is globally unique, self-describing, and stable across renames. This document defines the id structure, the namespace registry, and the cross-repo reference contract. It is the single source of truth for the org-wide id system.

## 2. ID structure

```
<repo-namespace>:<level>-<domain>-<stage>[-<cell>] [-<kind>] [<hash-suffix>]
```

Every field is optional except `<repo-namespace>` and `<level>`. The `<domain>` and `<stage>` fields are required only in ECF-coordinated repos (business-processes, business-capabilities). The `<hash-suffix>` is required on all records.

### 2.1 Repo namespace tokens

Stable logical names. Never renamed. Bound to repos via the registry in section 4.

| Token | Repo | Notes |
|---|---|---|
| `processes` | `dea-catalog-business-processes` | Business process architecture (L0-L4) |
| `capabilities` | `dea-catalog-business-capabilities` | Business capability decomposition |
| `actors` | `dea-catalog-actors` | Actor / agent registry |
| `orgunits` | `dea-catalog-organizational-units` | Organizational unit registry |
| `objects` | `dea-catalog-business-objects` | Business object / information model |
| `services` | `dea-catalog-business-services` | Business service definitions |
| `stakeholders` | `dea-catalog-stakeholders` | Stakeholder registry |

### 2.2 Level tokens

| Token | Level | Used in |
|---|---|---|
| `pc` | L0 Process Context | ECF-coordinated repos |
| `group` | L1 Process Group | ECF-coordinated repos |
| `process` | L2 Business Process | ECF-coordinated repos |
| `activity` | L3 Activity | ECF-coordinated repos |
| `task` | L4 Task | ECF-coordinated repos |
| `capability` | Capability | business-capabilities |
| `actor` | Actor | actors |
| `orgunit` | Organizational Unit | organizational-units |
| `object` | Business Object | business-objects |
| `service` | Business Service | business-services |
| `stakeholder` | Stakeholder | stakeholders |

Auxiliary kind tokens (reserved, not level tokens): `scope`, `workflow`, `instance`, `execution`, `candidate`, `discovery`.

### 2.3 ECF domain codes

| Code | Domain |
|---|---|
| `pr` | PartyAndRelationship |
| `ge` | GovernanceAndExistence |
| `pv` | ProductAndValue |
| `ao` | AgencyAndOrganization |
| `sd` | StrategyAndDirection |
| `fa` | FinanceAndAccounting |
| `eo` | EnablementAndOperations |

### 2.4 ECF stage codes

Full words, kebab-cased: `conceive`, `design`, `build`, `activate`, `operate`, `improve`, `retire`.

### 2.5 Hash suffix

- 6 characters, base32 (`a-z` + `2-7`, no `0`, `1`, `8`, `9` to avoid visual confusion).
- Content-addressed: computed from the canonical YAML serialization of the record file at migration time.
- Stable across renames: renaming a record does not change its hash suffix unless the content changes.
- Verified at gate time: `check_id_system.py` recomputes the hash and compares.

### 2.6 Cell and kind fields

- `<cell>` is OPTIONAL and reserved for non-standard sub-cells (e.g. a future EO/Operate-Primary vs EO/Operate-Secondary split). Defaults to absent.
- `<kind>` is OPTIONAL and reserved for auxiliary types (`scope`, `workflow`, `candidate`, `discovery`). Defaults to absent.

## 3. Examples

```
processes:pc-ao-operate-fz2h3
processes:group-pr-build-3d2h9
processes:process-ge-retire-7a4kq
processes:activity-pr-activate-8m2np7
processes:task-fa-activate-confirm-2x9y4p
capabilities:capability-asset-management-7a4kqz
capabilities:candidate-epm-7a4kqz
services:service-customer-360-7a4kqz
actors:actor-chief-technology-officer-7a4kqz
orgunits:orgunit-engineering-7a4kqz
objects:object-invoice-7a4kqz
stakeholders:stakeholder-regulator-7a4kqz
```

## 4. Registry binding

The registry in this section binds namespace tokens to repo URLs. Routing is registry lookup, not string matching. Repo renames become registry edits, not id migrations.

| Token | Repo URL | Default branch |
|---|---|---|
| `processes` | `github.com/technehub-labs/dea-catalog-business-processes` | `main` |
| `capabilities` | `github.com/technehub-labs/dea-catalog-business-capabilities` | `main` |
| `actors` | `github.com/technehub-labs/dea-catalog-actors` | `main` |
| `orgunits` | `github.com/technehub-labs/dea-catalog-organizational-units` | `main` |
| `objects` | `github.com/technehub-labs/dea-catalog-business-objects` | `main` |
| `services` | `github.com/technehub-labs/dea-catalog-business-services` | `main` |
| `stakeholders` | `github.com/technehub-labs/dea-catalog-stakeholders` | `main` |

## 5. Cross-repo reference contract

Every cross-repo reference carries the full id (namespace token + structural fields + hash suffix). The namespace token is the routing key; the registry resolves it to a repo URL.

- A Capability that realizes a Business Process writes `processes:process-ge-retire-7a4kq` in its `realizes[]` field.
- A Service that binds to a Capability writes `capabilities:capability-asset-management-7a4kqz` in its `capability_bindings[]` field.
- A Task that decomposes an Activity writes `processes:activity-pr-activate-8m2np7` in its `belongs_to_activity` field (in-repo reference; namespace token still present for uniformity).

## 6. ID vs path separation

- The `id:` field is the logical identifier. It contains colons (`processes:pc-ao-operate-fz2h3`).
- The filesystem path is derived from the id by normalizing colons to hyphens and lowercasing: `processes:pc-ao-operate-fz2h3` -> `processes-pc-ao-operate-fz2h3`.
- The path is NOT the id. Tools must resolve records by id, not by path. The path is a storage convention, not a semantic identifier.

## 7. Migration contract

- Every existing `dea:*` id is rewritten to the new form by the migration script.
- Every cross-reference (`belongs_to_*`, `composes[]`, evidence `source:`, `process_scope.*`, change_history `cr:` fields that name record ids) is rewritten to carry the full new id.
- The migration script emits `reconciliation/migration-id-map.yaml`: every old id -> new id, across all repos. This map is the audit trail for the migration.

## 8. Non-goals

- NOT a URI scheme. The `processes:` prefix is a namespace token, not a URI scheme. IDs are not resolvable URLs.
- NOT a global registry. The registry in section 4 is a static doc, not a live service. Tools must not depend on runtime resolution.
- NOT a renaming of existing records. The hash suffix is stable; the structural prefix is deterministic. Only the `id:` field changes; `name:`, `definition:`, and all other fields are preserved verbatim.

## 9. See also

- `docs/entity-storage-layout.md`: the filesystem layout convention (L0-rooted containment tree).
- `docs/decomposition-semantic-contract.md`: the decomposition chain (L0-L4) and the decomposition-vs-execution split.
- `scripts/check_id_system.py`: the CI gate that enforces this spec in every repo.
