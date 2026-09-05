# CR-CATALOG-STRUCT-06a: CATALOG.yaml Regenerator + Gate + Schema

**Status**: Proposed
**Layer**: L0 (Metaframework; cross-repo machinery)
**Owner**: TechNeHub Labs
**Depends on**: CR-CATALOG-STRUCT-01 (merged; PR #10)
**Supersedes**: none
**Related**: CR-CATALOG-STRUCT-06b (conformance tests + template), CR-CATALOG-STRUCT-02..05 (adoption CRs)
**Authority**: Mandatory; runs in every catalog repo CI after STRUCT-02 lands

---

## 1. Purpose

Ship the **engine** that makes the catalog repository standard (CR-CATALOG-STRUCT-01) executable. After this CR merges, any catalog can manually run the regenerator and ship a `CATALOG.yaml` that conforms to the standard. STRUCT-06b adds the cross-repo conformance tests CST-001..CST-015 and the new-repo template; STRUCT-02..05 land adoption CRs that wire the gate into each existing catalog's CI.

The CR ships three artifacts:

- A **JSON Schema** (`tools/catalog-index-schema.json`) that defines the shape of `CATALOG.yaml`. Lives next to its consumer scripts (sibling-of-entity-schemas pick); not in `schemas/entities/` because it describes a cross-entity index, not a single entity.
- A **regenerator** (`tools/regenerate_catalog.py`) that walks the filesystem and emits `CATALOG.yaml` deterministically. The standard requires the index to be machine-generated (no hand edits); the regenerator is the only legitimate writer.
- A **gate** (`tools/check_catalog_index.py`) that validates `CATALOG.yaml` against the schema and runs sanity checks. Wired into CI in STRUCT-02..05; callable today by catalog maintainers on demand.

The CR also lands a **pytest self-test suite** (`tests/test_catalog_index_machinery.py`) that exercises the machinery against an in-tree fixture catalog. Conformance tests CST-001..CST-015 (cross-repo, against any catalog URL) land in STRUCT-06b.

## 2. Scope

**In scope**:

- The JSON Schema for `CATALOG.yaml`: required/optional fields, types, enums, patterns.
- The regenerator's filesystem walk, entity-state inference, and atomic write semantics.
- The gate's schema validation + structural sanity checks.
- CLI surface (`--check`, `--dry-run`, `--verbose`, `--strict`, `--catalog-root`, `--output`, `--schema`).
- Self-tests covering: regenerator round-trip, gate clean state, gate schema violation, gate filesystem drift, determinism across two runs, and the four-state precedence rule.

**Out of scope**:

- Cross-repo conformance tests CST-001..CST-015 (STRUCT-06b).
- The new-repo template at `tools/catalog-repo-template/` (STRUCT-06b).
- CI wiring on each catalog repo (per-catalog adoption CRs).
- The cross-repo consumer (STRUCT-07).

## 3. Definitions

- **CATALOG.yaml**: the machine-generated YAML file at the repo root that indexes every entity subtree, classification, schema, validator, contribution queue, and research register. The standard's §6 is the authoritative description; this CR implements it.
- **Entity subtree**: `entities/v1-alpha/<entity-id>/` per the standard's §5.
- **State (per-entity)**: one of `research`, `candidate`, `canonical`, `retired`. Inferred from the subtree's directory contents; canonical wins if multiple states are present.
- **Regenerator**: `tools/regenerate_catalog.py`. The sole legitimate writer of `CATALOG.yaml`. Hand-edits are forbidden (standard §6.3); CI fails any PR where the committed file is stale.
- **Gate**: `tools/check_catalog_index.py`. The companion read-path validator. Schema validation + structural sanity (paths resolve, IDs match subtree names, no orphans in either direction).

## 4. Design

### 4.1 Entity-state inference (regenerator's precedence rule)

The regenerator derives each entity's `state` from the subtree's directory contents. The rule is deterministic and total; every subtree maps to exactly one state.

| Precedence | Observed subtree contents | Inferred state |
|---|---|---|
| 1 (lowest) | `research/` contains files only; no canonical file at subtree root | `research` |
| 2 | `candidates/` contains files only; no canonical file | `candidate` |
| 3 | Canonical file `<entity-id>.yaml` exists at subtree root AND `lifecycle_status` in `deprecated`, `retired` | `retired` |
| 4 | Canonical file exists; `lifecycle_status` not in `{deprecated, retired}`; OR `lifecycle_status` absent | `canonical` |
| 5 (highest) | Subtree is empty or contains only `.gitkeep`/`.DS_Store` | `candidate` (placeholder) |

Precedence rationale: a retired entity's canonical file MUST be preserved byte-for-byte (standard §10), so its directory shape mirrors an active canonical entry; the only signal is `lifecycle_status`. A canonical entity supersedes any research or candidate residue from its earlier lifecycle; residue is allowed to remain (e.g. post-admission `research/` files describing the now-canonical entity) but does not move the state. A subtree without any of the four state directories is treated as a candidate placeholder; the gate emits a warning (not error) so empty subtrees can exist during early scaffolding.

The four states are mutually exclusive in `CATALOG.yaml`; precedence 5 means the regenerator still emits an entry rather than dropping the subtree, so consumers see it as a known-empty placeholder.

### 4.2 Field provenance (regenerator reads)

Every field emitted into `CATALOG.yaml` has a single, deterministic source. The regenerator does NOT call any external service or read git history.

| Field | Source |
|---|---|
| `catalog.id` | `metamodel-pointer.yaml` `catalog.id` if present; else `<repo-name>` derived |
| `catalog.name`, `abbreviation`, `version`, `description` | `metamodel-pointer.yaml` block if present; else empty string + warning |
| `catalog.status` | `metamodel-pointer.yaml` if present; else `active` |
| `catalog.metamodel_version` | `metamodel-pointer.yaml` if present; else `unknown` |
| `catalog.repository` | `git config --get remote.origin.url` (read once at start, cached); else empty |
| `catalog.owner` | `metamodel-pointer.yaml` if present; else `TechNeHub Labs` (default) |
| `entities[].id` | Subtree directory name (POSIX-safe; colons preserved) |
| `entities[].type` | Canonical YAML `type` field if present; else `unknown` |
| `entities[].state` | Per §4.1 precedence rule |
| `entities[].path` | `entities/v1-alpha/<entity-id>/<entity-id>.yaml` if canonical file exists; else first YAML under the subtree (e.g. `candidates/<id>.yaml`) with the relative path; else the subtree root with trailing slash |
| `entities[].research_count` | Number of files (not directories) under `research/` |
| `entities[].candidate_count` | Number of files under `candidates/` |
| `entities[].canonical_count` | 1 if canonical file exists; 0 otherwise |
| `entities[].retired_count` | Number of files under `retired/` |
| `entities[].last_modified` | Max `st_mtime` across the subtree's regular files, formatted `YYYY-MM-DD` |
| `entities[].version` | Canonical YAML `version` field; `0.0.0` for subtrees without a canonical file |
| `entities[].lifecycle_status` | Canonical YAML `lifecycle_status` field; `candidate` for subtrees without a canonical file |
| `cross_cutting.*` | Hard-coded relative paths per the standard's §6.1 schema; counted from the catalog root |
| `counts.*` | Aggregate over `entities[]`; recomputed deterministically |
| `research_registers[].files` | Lexicographically sorted file list under the subtree's `research/` (regular files only) |

### 4.3 Atomic write

The regenerator builds the full `CATALOG.yaml` payload in memory, validates it against the schema, and writes atomically: write to `CATALOG.yaml.tmp`, `os.replace()` onto `CATALOG.yaml`. A crash mid-write leaves the previous `CATALOG.yaml` intact.

### 4.4 Determinism

The regenerator is byte-stable across runs on the same filesystem state. The implementation guarantees:

- All `entities[]` entries are sorted by `id` (lexicographic, case-sensitive, Unicode-codepoint order).
- All `research_registers[].files` are lexicographically sorted.
- `cross_cutting` keys are emitted in the schema's declared order.
- Timestamps are formatted `YYYY-MM-DD` (UTC), not locale-dependent.
- The YAML emitter sorts keys deterministically (`sort_keys=True`); the emitter also uses `default_flow_style=False` and `allow_unicode=True`.
- No wall-clock fields appear in the output (timestamps come from mtime only).

Two consecutive runs on the same subtree produce identical bytes (verified by self-test `test_regenerator_is_deterministic`).

### 4.5 Gate semantics

The gate (`tools/check_catalog_index.py`) runs in two modes:

- **Default**: schema validation + structural sanity checks. Exits 0 on clean, 1 on schema invalid, 2 on sanity failure (e.g. a `path` field that does not resolve to a real file).
- **`--strict`**: also upgrades warnings to errors. Warnings include: missing `research/README.md` for non-empty `research/`, subtrees without a canonical file (warning-only by design; the standard allows empty subtrees during scaffolding), missing `metamodel-pointer.yaml` at the catalog root.

The gate does NOT regenerate `CATALOG.yaml`; that is the regenerator's job. If the regenerator's output is stale, the gate emits a clear message: "CATALOG.yaml is stale; run `python tools/regenerate_catalog.py` to refresh." This separation means the gate is fast (read-only) and the regenerator can be heavy (full filesystem walk).

### 4.6 CLI surface

`tools/regenerate_catalog.py`:

```
python tools/regenerate_catalog.py [--catalog-root PATH] [--output PATH] [--check] [--dry-run] [--verbose] [--schema PATH]
```

- `--catalog-root PATH`: catalog repo root (default: current working directory).
- `--output PATH`: output path (default: `<catalog-root>/CATALOG.yaml`).
- `--check`: exit 0 if committed `CATALOG.yaml` matches regenerator output, 3 otherwise; do NOT write.
- `--dry-run`: build the payload, print to stdout, do NOT write.
- `--verbose`: print per-entity detection diagnostics to stderr.
- `--schema PATH`: schema path (default: `tools/catalog-index-schema.json`).

`tools/check_catalog_index.py`:

```
python tools/check_catalog_index.py [--catalog-root PATH] [--strict] [--schema PATH]
```

- `--catalog-root PATH`: catalog repo root (default: current working directory).
- `--strict`: warnings become errors.
- `--schema PATH`: schema path (default: `tools/catalog-index-schema.json`).

### 4.7 Error codes

Both tools use a stable exit-code contract:

| Code | Regenerator | Gate |
|---|---|---|
| 0 | Success | Success |
| 1 | Filesystem error (cannot read subtree, permission denied) | Schema validation failed |
| 2 | Schema validation failed (regenerated payload fails schema) | Structural sanity failure |
| 3 | `--check` mode: committed file is stale | (unused) |

Stable exit codes mean CI scripts and CR-style per-catalog adoption docs can rely on them.

## 5. Files

**New** (6 files):

- `tools/catalog-index-schema.json`: JSON Schema draft-07 describing `CATALOG.yaml`. ~110 lines.
- `tools/regenerate_catalog.py`: regenerator script. Pure stdlib (`yaml`, `json`, `argparse`, `pathlib`, `os`, `sys`). ~220 lines.
- `tools/check_catalog_index.py`: gate script. Pure stdlib (`yaml`, `json`, `argparse`, `pathlib`, `sys`). ~180 lines.
- `tests/test_catalog_index_machinery.py`: pytest self-test suite. ~150 lines. Uses `tmp_path` fixture; no network; no git; runs in <2s.
- `change-requests/CR-CATALOG-STRUCT-06a.md`: this document.
- `tests/__init__.py`: empty marker (matches the existing `tests/conformance/__init__.py` pattern); only added if missing.

**Modified** (1 file):

- `CHANGELOG.md`: `[Unreleased]` entry for the STRUCT-06a tranche.
- `change-requests/README.md`: row for CR-CATALOG-STRUCT-06a in the Catalog Structure series.

**Not modified**:

- `tools/ecf_coordinates.py`: unrelated; the regenerator does not consume the ECF enumeration directly. ECF coordinates are surfaced by individual catalog entries, not the catalog index.
- `tests/conformance/test_005_coordinate_spec.py`: existing conformance suite; the regenerator must not break it (verified by self-test).
- `docs/standards/catalog-repository-pattern.md` and the adoption tracker: no changes; STRUCT-06a implements the contract they describe.

## 6. Conformance contract

The machinery is conformant iff:

1. `python tools/regenerate_catalog.py` exits 0 on a well-formed catalog and writes a `CATALOG.yaml` that validates against `tools/catalog-index-schema.json`.
2. `python tools/check_catalog_index.py` exits 0 immediately after the regenerator.
3. `python tools/regenerate_catalog.py --check` exits 0 immediately after the regenerator.
4. A second `python tools/regenerate_catalog.py` run produces byte-identical output.
5. `pytest -q tests/test_catalog_index_machinery.py` passes (all self-tests).
6. `pytest -q tests/conformance/` still passes (no regression to the ECF coordinate suite).

Self-tests in `tests/test_catalog_index_machinery.py` cover these contracts plus failure modes:

- `test_regenerator_emits_canonical_entity`: subtree with one canonical YAML plus research, candidates, and retired directories; emits a `state: canonical` entry with the right counts.
- `test_regenerator_emits_research_only_subtree`: subtree with `research/` only; emits `state: research`.
- `test_regenerator_emits_candidate_only_subtree`: subtree with `candidates/` only; emits `state: candidate`.
- `test_regenerator_emits_retired_when_lifecycle_status_retired`: subtree with canonical file whose `lifecycle_status: retired`; emits `state: retired`.
- `test_regenerator_infers_state_for_empty_subtree`: empty subtree; emits `state: candidate` with a warning.
- `test_regenerator_is_deterministic`: two runs produce byte-identical bytes.
- `test_regenerator_atomic_write_no_partial_file`: simulate a crash mid-write by patching `os.replace` to raise; assert `CATALOG.yaml` retains its previous contents.
- `test_check_passes_after_regenerate`: regenerate then gate; both exit 0.
- `test_check_fails_on_schema_violation`: manually corrupt `CATALOG.yaml`; gate exits 1.
- `test_check_fails_on_unresolved_path`: replace `entities[0].path` with a non-existent file; gate exits 2.
- `test_check_fails_on_stale_catalog`: regenerate to a temp file, then move a file under the subtree, then `--check`; exits 3.
- `test_check_strict_upgrades_missing_readme_to_error`: missing `research/README.md`; default mode warns; `--strict` errors.
- `test_no_regression_on_ecf_conformance_suite`: invokes the existing conformance suite's `run()` and asserts exit 0.

## 7. Decisions log

### D-STRUCT-06a-001: regenerate full file, not partial

Partial regeneration (only re-emitting changed entities) was considered and rejected. The file is small (<10 KB for any current catalog), the canonical contract is "CATALOG.yaml is the catalog's view of itself", and partial regeneration complicates the gate's job. The full-file approach makes the byte-identical determinism property easy to verify.

### D-STRUCT-06a-002: warn not error on missing `research/README.md`

Per user micro-decision during planning: the standard requires `research/README.md` when `research/` is non-empty (CST-009), but adoption CRs may not have completed step 2 of the migration yet. Default mode warns; `--strict` errors. Adoption CRs can opt into `--strict` once their research distribution is complete.

### D-STRUCT-06a-003: regenerator reads `metamodel-pointer.yaml` if present

Catalog repos already carry `metamodel-pointer.yaml` (the entity-to-metamodel map). The regenerator reuses it for `catalog.{id,name,version,description,metamodel_version,status}` to avoid duplicating catalog-level metadata. If absent, sensible defaults are emitted and a warning is logged.

### D-STRUCT-06a-004: no git dependency

The regenerator reads filesystem state only. mtime is the source of `last_modified`; no `git log` calls. This keeps the tool usable in CI containers without git history and in tests with `tmp_path` fixtures.

### D-STRUCT-06a-005: gate and regenerator are separate scripts

Two scripts, not one. Reasons: the gate is read-only and fast; the regenerator does filesystem walks and writes. Keeping them separate means the gate can be invoked freely on hot paths (PR check) without the cost of a regeneration. The standard's §8 lists both as required CI steps, and the standard treats them as distinct concepts.

### D-STRUCT-06a-006: schema lives at `tools/catalog-index-schema.json`

Sibling of entity schemas (per the planning pick). Rationale: the schema describes the cross-entity index, not any one entity. Putting it in `schemas/entities/` would conflate two distinct concerns; putting it in `schemas/` (the existing dir) would lose the locality with its consumer scripts. `tools/catalog-index-schema.json` keeps it next to the regenerator and gate, which are its only consumers.

### D-STRUCT-06a-007: subprocess-based self-tests

The self-tests invoke the regenerator and gate as subprocesses (not as imports). Reason: the tools use `sys.argv` and `sys.exit` directly; importing them would pollute the test process. Subprocess invocation also exercises the CLI surface, which is the actual contract CI uses.

## 8. Usage

After STRUCT-06a merges and a catalog has the two scripts:

```bash
# First-time generation
python tools/regenerate_catalog.py

# Verify the committed CATALOG.yaml is current
python tools/regenerate_catalog.py --check

# Validate the committed CATALOG.yaml against the schema
python tools/check_catalog_index.py

# Strict mode (warnings become errors)
python tools/check_catalog_index.py --strict

# Preview the regenerator output without writing
python tools/regenerate_catalog.py --dry-run

# Run the self-test suite
pytest -q tests/test_catalog_index_machinery.py
```

Per-catalog CI wiring lands in STRUCT-02..05 (adoption CRs). Until those merge, the standard's §8 CI gate contract is unenforceable; STRUCT-06a ships the engine but the engines only run when a catalog wires it up.

## 9. Out of scope (deferred)

- **STRUCT-06b**: conformance tests CST-001..CST-015 (cross-repo), the new-repo template at `tools/catalog-repo-template/`, and the template-version conformance test CST-016. STRUCT-06a does not gate on STRUCT-06b; STRUCT-02..05 do.
- **STRUCT-02..05**: adoption CRs that wire the regenerator + gate into each existing catalog's CI.
- **STRUCT-07**: cross-repo consumer in `dea-metamodel/viewer/` and `dea-architecture-framework/`.

## 10. Acceptance criteria

1. All six new files exist on the branch and parse / type-check.
2. `pytest -q tests/test_catalog_index_machinery.py` passes with at least 10 tests.
3. `pytest -q tests/conformance/test_005_coordinate_spec.py` still passes (no regression).
4. `python tools/regenerate_catalog.py` on a synthetic fixture catalog exits 0.
5. `python tools/check_catalog_index.py` on the synthetic fixture catalog exits 0.
6. `python tools/regenerate_catalog.py --check` exits 0 immediately after a successful regeneration.
7. The CR document is dash-clean (no en/em dashes, no right-arrow glyphs) per the repo's documentation conventions.
8. No secrets, tokens, or credentials are introduced (verified by the org-wide secret scan).
9. CHANGELOG and CR README updates reflect the new CR.

## 11. Risks

- **R-STRUCT-06a-001**: A catalog with a malformed `metamodel-pointer.yaml` produces a `CATALOG.yaml` with empty catalog-level fields. Mitigation: regenerator logs a warning; gate does not error on absent `metamodel-pointer.yaml` (default mode).
- **R-STRUCT-06a-002**: A future catalog uses a non-YAML format for entities. Mitigation: the regenerator currently only handles YAML; CR can be opened to add JSON support if needed. Out of scope for STRUCT-06a.
- **R-STRUCT-06a-003**: The schema evolves; the regenerator must be updated in lockstep. Mitigation: schema is referenced by both scripts via the same default path; both fail clearly if the schema is missing or malformed.
- **R-STRUCT-06a-004**: Adopted catalogs do not run the gate in CI until STRUCT-02..05 land. Mitigation: STRUCT-06a explicitly defers CI wiring to the adoption CRs; the standard's §13 schedule names the target milestones.

## 12. Open questions

None at authoring time. Resolved during planning:

- Schema location: `tools/catalog-index-schema.json` (D-006).
- Template engine: hand-rolled; deferred to STRUCT-06b.
- Gate strictness: default warns; `--strict` errors (D-002).

## 13. Related

- CR-CATALOG-STRUCT-01 (merged; PR #10): the standard this CR implements.
- CR-CATALOG-STRUCT-06b (next): conformance tests CST-001..CST-015 + new-repo template.
- CR-CATALOG-STRUCT-02..05 (downstream): per-catalog adoption CRs.
- CR-CATALOG-STRUCT-07 (downstream): cross-repo consumer.

---

## Appendix A: Example output

A minimal `CATALOG.yaml` for a catalog with one canonical entity and one research-only subtree:

```yaml
catalog:
  id: dea:catalog-processes
  name: Business Process
  abbreviation: BP
  version: "1.0.0"
  status: active
  metamodel_version: "1.0.0"
  description: Reference catalog for Business Process and Process Group entities.
  repository: https://github.com/technehub-labs/dea-catalog-processes
  owner: TechNeHub Labs

  entities:
    - id: dea:process-manage-customer-relationship
      type: Process
      state: canonical
      path: entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml
      research_count: 3
      candidate_count: 0
      canonical_count: 1
      retired_count: 0
      last_modified: "2026-09-04"
      version: "1.0.0"
      lifecycle_status: candidate
    - id: dea:group-customer-lifecycle-management
      type: ProcessGroup
      state: canonical
      path: entities/v1-alpha/dea:group-customer-lifecycle-management/dea:group-customer-lifecycle-management.yaml
      research_count: 1
      candidate_count: 0
      canonical_count: 1
      retired_count: 0
      last_modified: "2026-09-04"
      version: "1.0.0"
      lifecycle_status: candidate

  cross_cutting:
    classifications: classifications/
    schemas: schemas/
    validators: scripts/
    contributions_queue: contributions/
    change_requests: change-requests/

  counts:
    entities: 2
    research_files: 4
    candidates: 0
    canonical: 2
    retired: 0
    open_change_requests: 0

  research_registers:
    - entity_id: dea:process-manage-customer-relationship
      path: entities/v1-alpha/dea:process-manage-customer-relationship/research/
      files:
        - L1-REGISTER-v0.1.md
        - l1-candidate-universe.yaml
        - l1-register.yaml
    - entity_id: dea:group-customer-lifecycle-management
      path: entities/v1-alpha/dea:group-customer-lifecycle-management/research/
      files:
        - group-promotion-rationale.md
```

This is the shape consumers (`dea-metamodel/viewer/`, `dea-architecture-framework/`, future CLIs) MUST read. The schema guarantees the keys and types; the regenerator guarantees the values match the filesystem.
