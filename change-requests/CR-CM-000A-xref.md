# CR-CM-000A — Terminology Alignment (extension) — cross-reference

The full CR text lives in the canonical CR repository:

- **Primary copy:**
  [`technehub-labs/dea-metamodel/change-requests/CR-CM-000A.md`](https://github.com/technehub-labs/dea-metamodel/blob/main/change-requests/CR-CM-000A.md)
  (extension of [CR-CM-000](https://github.com/technehub-labs/dea-metamodel/blob/main/change-requests/CR-CM-000.md))
- **Interim terminology registry:**
  [`dea-metamodel/vocabulary/terminology-registry.yaml`](https://github.com/technehub-labs/dea-metamodel/blob/main/vocabulary/terminology-registry.yaml)

## Sections affecting this repository

| CR-CM-000A section | Consequence for dea-metaframework |
|---|---|
| §3.1 Reserve Domain | This repository is the **owner** of the reserved terms Domain and Stage; its semantics are referenced, never redefined, by the Concepts Model. |
| §6 ECF Context | The Concepts Model contextualizes concepts against this repo's Domain × Stage coordinate system. |
| §7 Canonical vocabulary | Domain/Stage rows name this repo as owner (`dea-metaframework`). |
| §16 Deliverables | `docs/terminology/concepts-model-alignment.md` (this PR) is the ECF-side companion document. |

## What this PR does NOT do

- No changes to the framework itself (`framework/`, `REPORT.md`,
  `metamodel/`, `schemas/` are untouched — the ECF is *referenced*, not
  modified).
- No copy of the full CR text (canonical copy lives in dea-metamodel —
  single authoritative source, no byte-drift).
- The `dea-concepts-model` repository is created by CR-CM-001, not here.
