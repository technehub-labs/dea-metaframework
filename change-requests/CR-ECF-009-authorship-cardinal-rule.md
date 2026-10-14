# CR-ECF-009: Authorship Cardinal Rule (Org-Wide Propagation Slice)

| Field | Value |
|-------|-------|
| **CR** | CR-ECF-009 |
| **Title** | Authorship Cardinal Rule (R1, R2) - Org-Wide Propagation Slice (dea-metaframework) |
| **Status** | Accepted (per user directive 2026-10-13) |
| **Layer** | Org-wide (dea-metaframework) |
| **Depends on** | CR-BP-118 (org-wide authorship cardinal rule, main authority) |
| **Companion to** | CR-DEA-BC-34 (BC slice), CR-BO-03 (BO slice), CR-OU-03 (OU slice) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-13 |

## 1. The cardinal rule (pinned)

Two cardinal rules from CR-BP-118 (org-wide authority) are propagated to this
repo (dea-metaframework):

- **R1 (Authorship-field cardinal rule)**: every authorship-bearing field must
  carry a value from the allowlist `{Emmanuel A. Otchere, TechNeHub Labs}`.
  Substring matches against the denylist
  `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}` are
  blocking (AUT-001).
- **R2 (Named-role file cardinal rule)**: any file or field whose purpose is
  to name a person playing a named role must carry the canonical identity.

The rules are CR-level (immutable by a gate change) and governance-doc-level
(immutable by a code change).

## 2. The retro sweep (MF-repo scope)

5 hits across 4 files, all swept:

| File | Field | Replaced |
|---|---|---|
| change-requests/CR-ECF-008.md | `**Owner**` | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |
| change-requests/CR-ECF-CG-001.md | `**Author**` | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |
| docs/entity-storage-layout.md | `**Owner**` | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |
| docs/id-system.md | `**Owner**` | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |
| change-requests/CR-ECF-008.md | prose `Editorial note (Coder, 2026-09-08)` | `(Coder, ...)` -> `(Emmanuel A. Otchere, ...)` |

Total: 4 files, 5 textual replacements. 0 entity content changes; 0 id
changes; 0 cross-reference changes. The MF repo has 0 entity YAMLs, 0
CITATION.cff, and 0 catalog-research YAML; the field set is CR-doc +
status-doc metadata, both bold-key form.

The `Editorial note (Coder, YYYY-MM-DD)` prose byline is the first prose
mention swept under the 118b rule. The same shape is rare in MF; if it
recurs in other repos it gets a per-field registry entry.

## 3. The gate (MF-repo, blocking)

- **AUT-001 (blocking)**: substring denylist against
  `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`.
- **AUT-002 (blocking)**: parent-block present but field empty.
- **AUT-003 (advisory, blocking under --strict)**: value not in allowlist.

Data-driven from `reconciliation/authorship-fields.yaml`. Fields registered
for the MF repo (per the field shape this repo uses):

| Path | file_glob | prefix_match |
|---|---|---|
| `**Owner**` | `change-requests/CR-*.md` | (default: exact) |
| `**Author**` | `change-requests/CR-*.md` | (default: exact) |
| `**Owner**` | `docs/*.md` | (default: exact) |

The `docs/*.md` glob is MF-specific: ratified status documents in MF
carry `**Owner**` at the top of the file. The 118a (dea-catalog-business-
processes) baseline doesn't have this shape; the BC slice has
catalog-research YAML extensions but not docs extensions.

## 4. CI wiring

A new workflow `.github/workflows/validate-authorship.yml` runs the gate
in `--strict` mode on every push and PR. The gate has its own per-repo
test module `tests/test_check_authorship.py` (21 tests, 21/21 pass on
the MF repo's tree).

## 5. Out of scope (CR-118c, deferred)

Prose-content occurrences of `Agent` / `Coder` / etc. in record `name` /
`definition` / `description` fields (not the authorship-metadata fields)
are inventoried for the 118c follow-on but not rewritten in this slice.

## 6. Test posture

- 21/21 `test_check_authorship` pass.
- Gate `--strict` exit 0 against the live MF tree.
- 0 D-004 violations across 4 new/modified files.

## 7. Carrier

This document. Plus the CHANGELOG `[Unreleased]` entry and the new
`.github/workflows/validate-authorship.yml` workflow.
