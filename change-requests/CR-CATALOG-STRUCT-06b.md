# CR-CATALOG-STRUCT-06b: Conformance Tests + New-Repo Template + Bootstrap Script

**Status**: Proposed
**Layer**: L0 (Metaframework; cross-repo enforcement)
**Owner**: TechNeHub Labs
**Depends on**: CR-CATALOG-STRUCT-01 (merged; PR #10), CR-CATALOG-STRUCT-06a (merged; PR #11)
**Supersedes**: none
**Related**: CR-CATALOG-STRUCT-02..05 (adoption CRs); CR-CATALOG-STRUCT-07 (consumer)
**Authority**: Mandatory; runs in every catalog repo CI after STRUCT-02..05 land

---

## 1. Purpose

Close the standard's enforcement loop. CR-CATALOG-STRUCT-06a shipped the engine (regenerator + gate + schema). This CR ships:

- **Cross-repo conformance suite** (`tools/conformance_test_catalog_structure.py`) implementing CST-001..CST-015 from the standard's §11, plus CST-016 (template-version diff) introduced by this CR.
- **New-repo template** (`tools/catalog-repo-template/`): the bootstrap source every future catalog repo MUST be created from per the standard's §12.
- **Bootstrap script** (`tools/bootstrap_catalog_repo.py`): the hand-rolled template engine per the pick-3 decision in STRUCT-06a planning (no Jinja, no cookiecutter, no new pip dep).
- **Conformance self-tests** (`tests/test_conformance_catalog_structure.py`) exercising the suite against synthetic catalogs that violate each CST in isolation.
- **Conforming fixture** (`tests/fixtures/catalog-conforming/`): a real catalog the conformance suite passes against. Doubles as the worked-example target.

The standard is now **executable and enforceable**: any catalog can run `python tools/conformance_test_catalog_structure.py --catalog-root .` and verify conformance to every invariant; any new catalog can be created with `python tools/bootstrap_catalog_repo.py --target ...` and ship conformant from day one.

## 2. Scope

**In scope**:

- CST-001..CST-015 implementation per the standard's §11.
- CST-016 (template-version diff): advisory by default, error under `--strict`.
- The new-repo template's directory shape, file content, and CI workflow.
- The bootstrap script's CLI, placeholder substitution, optional git init, optional `gh` create.
- Worked example in Appendix B demonstrating the end-to-end loop on the in-tree fixture.

**Out of scope**:

- Adoption CRs STRUCT-02..05 (per-catalog wiring of the gate into CI).
- Cross-repo consumer STRUCT-07.
- Migration of existing catalogs into the standard (per-catalog adoption CRs).

## 3. Definitions

- **CST**: Conformance Structure Test. A single invariant from the standard's §11. CST-001..CST-015 in the standard; CST-016 added by this CR.
- **Template**: `tools/catalog-repo-template/`. The bootstrap source for new catalog repos. Pre-wires the directory structure, CI workflow, regenerator + gate copies, README, LICENSE, NOTICE, CITATION.cff, metamodel-pointer, and `TEMPLATE_VERSION`.
- **TEMPLATE_VERSION**: A semver file (e.g. `0.1.0`) at the template root and at every catalog root. The conformance test CST-016 compares the catalog's version to the template's; mismatch emits a warning (or error under `--strict`).
- **Bootstrap**: The act of copying the template into a target directory, substituting catalog-specific placeholders, and writing a `TEMPLATE_VERSION` that matches the template at bootstrap time.

## 4. Design

### 4.1 Conformance suite architecture

`tools/conformance_test_catalog_structure.py` is a standalone Python script with an importable `run()` function. It takes a catalog root (filesystem path) and a template root (default: `tools/catalog-repo-template`), runs every CST against the catalog, accumulates failures and warnings, and exits non-zero if any CST fails.

Each CST is its own function (`cst_001_has_catalog_yaml`, `cst_002_catalog_yaml_validates_against_schema`, ...). The CST list is registered in module-level `CST_TESTS` so new CSTs can be added without touching the runner. CST-016 (template-version) is invoked separately because it needs both roots.

The script is also callable as `python -m tools.conformance_test_catalog_structure` and importable as `from tools.conformance_test_catalog_structure import run` for `dea-metaframework` CI's cross-repo checks.

### 4.2 CST-016: template-version diff

The new test compares `TEMPLATE_VERSION` at the catalog root to `TEMPLATE_VERSION` at the template root. Three outcomes:

| Catalog state | Default mode | `--strict` mode |
|---|---|---|
| `TEMPLATE_VERSION` matches | OK | OK |
| `TEMPLATE_VERSION` differs | WARN | FAIL |
| `TEMPLATE_VERSION` missing (hand-rolled catalog) | WARN | FAIL |

Default advisory mode mirrors the standard's gate contract: catalog maintainers re-sync opportunistically. `--strict` upgrades to errors so STRUCT-02..05 adoption CRs can opt into hard enforcement after the first re-sync.

### 4.3 Template shape

The template ships with:

```
tools/catalog-repo-template/
├── TEMPLATE_VERSION                    # 0.1.0 (initial)
├── README.md                           # placeholder-substituted
├── CHANGELOG.md
├── LICENSE                             # Apache 2.0; year + owner substituted
├── NOTICE
├── CITATION.cff                        # placeholder-substituted
├── .gitignore
├── .github/workflows/ci.yml            # runs regenerator + gate + installs deps
├── entities/v1-alpha/.gitkeep
├── classifications/.gitkeep
├── schemas/.gitkeep
├── scripts/.gitkeep                    # bootstrap populates from dea-metaframework
├── contributions/.gitkeep
└── change-requests/.gitkeep
```

The CI workflow references `scripts/regenerate_catalog.py` and `scripts/check_catalog_index.py`. The bootstrap copies the current versions of both scripts from `dea-metaframework/tools/` into the catalog's `scripts/` directory at bootstrap time.

### 4.4 Bootstrap script

`tools/bootstrap_catalog_repo.py` performs five steps:

1. **Copy template**: walk `tools/catalog-repo-template/`, copy every file to the target. Templated files (`.yaml`, `.yml`, `.md`, `.json`, `.txt`, plus `LICENSE`, `NOTICE`, `CITATION.cff`) get placeholder substitution; others copy verbatim.
2. **Rewrite metamodel-pointer.yaml**: the script writes an authoritative version derived from the CLI args (catalog id, name, abbreviation, owner, version 0.1.0, status active, metamodel_version 1.0.0).
3. **Write TEMPLATE_VERSION**: copies the template's version into the catalog so CST-016 reports "in sync" until the template next bumps.
4. **Optional git init**: runs `git init` + `git add -A` if `--git-init` is passed.
5. **Optional gh create**: runs `gh repo create --source ... --{public|private}` if `--gh-create public|private` is passed.

Placeholder substitution is intentionally simple: one `str.replace()` per placeholder per file. No Jinja2, no cookiecutter. The pick-3 decision from STRUCT-06a planning explained why: YAML stays YAML-clean; CI linters don't choke on Jinja syntax; no new pip dep; update story is "bump `TEMPLATE_VERSION` and cherry-pick diff" rather than "rerun cookiecutter and pray".

### 4.5 Exit code contract

Both new scripts use the same exit-code contract as STRUCT-06a:

| Code | Conformance suite | Bootstrap |
|---|---|---|
| 0 | All CSTs passed | Success |
| 1 | Filesystem error (cannot read catalog) | n/a |
| 2 | One or more CSTs failed | Bootstrap failed (target exists without --force, etc.) |
| 3 | (unused) | (unused) |

## 5. Files

**New** (10 files):

- `tools/conformance_test_catalog_structure.py`: cross-repo conformance suite. Stdlib-only; ~430 lines.
- `tools/bootstrap_catalog_repo.py`: bootstrap script. Stdlib-only (plus PyYAML, already a dep); ~280 lines.
- `tools/catalog-repo-template/TEMPLATE_VERSION`: `0.1.0`.
- `tools/catalog-repo-template/README.md`: catalog-specific placeholder template.
- `tools/catalog-repo-template/CHANGELOG.md`: boilerplate.
- `tools/catalog-repo-template/LICENSE`: Apache 2.0 with year + owner placeholders.
- `tools/catalog-repo-template/NOTICE`: TechNeHub Labs attribution.
- `tools/catalog-repo-template/CITATION.cff`: citation metadata template.
- `tools/catalog-repo-template/.gitignore`: standard Python + editor ignores.
- `tools/catalog-repo-template/.github/workflows/ci.yml`: CI workflow referencing scripts.
- `tools/catalog-repo-template/{entities/v1-alpha,classifications,schemas,scripts,contributions,change-requests}/.gitkeep`: directory placeholders.
- `tests/fixtures/catalog-conforming/`: real catalog the conformance suite passes against. Includes a canonical entity, a candidate-only entity, a fully-retired entity, the regenerator + gate copies in `scripts/`, the schema in `tools/`, a CI workflow, and a generated `CATALOG.yaml`.
- `tests/test_conformance_catalog_structure.py`: 11 self-tests covering all CSTs plus bootstrap behavior.

**Modified** (3 files):

- `tests/conftest.py`: extended the `tmp_root` fixture to seed both the schema AND the template root (needed by the conformance self-tests).
- `tools/regenerate_catalog.py`: bug fix in `read_canonical_yaml` to fall back to `retired/<file>.yaml` when no root canonical exists; bug fix in `infer_state` precedence 3/4 to use the loaded canonical's lifecycle when `canonical_path` is None.
- `CHANGELOG.md` (+12): tranche entry.
- `change-requests/README.md` (+1): row for STRUCT-06b.
- `docs/standards/catalog-repository-pattern.md` (+8): reference to STRUCT-06b as the implementation of §11; no behavior change.

## 6. Conformance contract

This CR is conformant iff:

1. `pytest -q tests/` exits 0 (38 tests: 12 machinery + 11 conformance + 15 ECF coordinate suite).
2. `python tools/conformance_test_catalog_structure.py --catalog-root tests/fixtures/catalog-conforming --template-root tools/catalog-repo-template` exits 0.
3. `python tools/bootstrap_catalog_repo.py --target /tmp/x --catalog-id dea:catalog-x --catalog-name X` exits 0; the resulting directory contains `TEMPLATE_VERSION`, `metamodel-pointer.yaml`, `README.md`, `.github/workflows/ci.yml`, and `TEMPLATE_VERSION` matches the template's.
4. The conformance suite correctly flags every negative case in `tests/test_conformance_catalog_structure.py`: missing `CATALOG.yaml`, unresolved paths, orphan subtrees, missing CI workflows, and template-version drift.
5. The bootstrap script correctly refuses to overwrite an existing directory unless `--force` is passed.
6. The CR document is dash-clean.
7. No secrets, tokens, or credentials introduced.

## 7. Decisions log

### D-STRUCT-06b-001: standalone script, not pytest module

The conformance suite ships as `python tools/conformance_test_catalog_structure.py` rather than a pytest module. Reasons: (a) the standard's §11 contract is "test runner exits non-zero"; (b) catalog adoption CRs (STRUCT-02..05) shell out to it from CI without adding a pytest dependency; (c) `dea-metaframework` CI on a schedule can `import run` for cross-repo checks.

### D-STRUCT-06b-002: CST-016 advisory by default, strict on demand

Per planning conversation: catalog maintainers re-sync templates opportunistically; STRUCT-02..05 adoption CRs opt into `--strict` after their first re-sync. Mirrors the gate's `--strict` upgrade pattern.

### D-STRUCT-06b-003: hand-rolled template, no Jinja

Per pick-3 decision in STRUCT-06a planning. The template is plain YAML + Markdown + JSON; placeholders are `{{NAME}}` strings substituted by one `str.replace()` per file per placeholder. Update story: bump `TEMPLATE_VERSION`, cherry-pick diff into outdated catalogs. No destructive re-render.

### D-STRUCT-06b-004: regenerator retired-fallback

A fully-retired entity may have moved its canonical file out of the subtree root into `retired/<file>-<version>.yaml` per standard §5.4. The regenerator's `read_canonical_yaml` falls back to the most recent file under `retired/` when no root canonical exists. `infer_state` precedence 3 uses the loaded canonical's `lifecycle_status` regardless of whether the file is at root or under `retired/`.

### D-STRUCT-06b-005: CST-003 relaxed to allow state-only subtrees

Standard §5 allows a subtree to be canonical-only OR fully-retired OR candidate-only. CST-003 originally required a YAML at the root; this CR relaxes it to "YAML at root OR files under research/, candidates/, or retired/". The error message is more descriptive. Aligns with the standard's existing language.

### D-STRUCT-06b-006: bootstrap script does NOT publish

`--gh-create` creates the GitHub repo via `gh` but does not push. Push is the user's choice after review. `--git-init` + `git add -A` is also optional; many users prefer to inspect the bootstrapped files first.

## 8. Usage

After STRUCT-06b merges:

```bash
# Verify any catalog repo's conformance to the standard
python tools/conformance_test_catalog_structure.py --catalog-root /path/to/catalog

# Same with strict mode (warnings become errors)
python tools/conformance_test_catalog_structure.py --catalog-root /path/to/catalog --strict

# Bootstrap a new catalog repo
python tools/bootstrap_catalog_repo.py \
    --target ../dea-catalog-foo \
    --catalog-id dea:catalog-foo \
    --catalog-name "Foo Catalog" \
    --catalog-abbreviation FC \
    --owner "TechNeHub Labs" \
    --git-init
    # Optional: --gh-create public | --gh-create private

# Verify the bootstrap result
cd ../dea-catalog-foo
python /path/to/dea-metaframework/tools/conformance_test_catalog_structure.py --catalog-root .

# Run the full self-test suite (this repo's CI does this)
pytest -q tests/
```

Adoption CRs (STRUCT-02..05) wire the conformance suite into each existing catalog's CI via shell-out from their workflow files. The template's CI workflow (`.github/workflows/ci.yml`) demonstrates the pattern for new repos.

## 9. Out of scope (deferred)

- **STRUCT-02..05**: adoption CRs that wire the gate and conformance suite into each existing catalog's CI.
- **STRUCT-07**: cross-repo consumer in `dea-metamodel/viewer/` + `dea-architecture-framework/`.

## 10. Acceptance criteria

1. All new files exist on the branch.
2. `pytest -q tests/` passes (38 tests).
3. `python tools/conformance_test_catalog_structure.py --catalog-root tests/fixtures/catalog-conforming` exits 0.
4. `python tools/bootstrap_catalog_repo.py --target /tmp/x --catalog-id dea:catalog-x --catalog-name X` exits 0 and produces a conformant directory.
5. The CR document is dash-clean.
6. No secrets introduced.
7. CHANGELOG, CR README, and standards doc updated.
8. CI on the branch is green (the `conformance` workflow).

## 11. Risks

- **R-STRUCT-06b-001**: An adopted catalog with an old `CATALOG.yaml` schema (pre-STRUCT-06a) may fail CST-002 schema validation. Mitigation: adoption CRs run the regenerator once before enabling `--strict`.
- **R-STRUCT-06b-002**: A template bump that changes file paths (rather than adding files) breaks outdated catalogs. Mitigation: `TEMPLATE_VERSION` bumps force a re-sync; conformance suite flags outdated catalogs.
- **R-STRUCT-06b-003**: The bootstrap script's `gh repo create` requires `gh` authenticated. Mitigation: `--gh-create no` is the default; users run it explicitly when ready.
- **R-STRUCT-06b-004**: CST-016's "no TEMPLATE_VERSION" warning may surprise existing catalogs that pre-date the template. Mitigation: warning is advisory; STRUCT-02..05 explicitly opt into strict.

## 12. Open questions

None at authoring time. Resolved during planning:

- Standalone vs pytest module: standalone (D-001).
- CST-016 default mode: advisory (D-002).
- Template engine: hand-rolled (D-003).

## 13. Related

- CR-CATALOG-STRUCT-01 (merged): the standard this CR implements.
- CR-CATALOG-STRUCT-06a (merged): the engine (regenerator + gate + schema).
- CR-CATALOG-STRUCT-02..05 (downstream): per-catalog adoption CRs.
- CR-CATALOG-STRUCT-07 (downstream): cross-repo consumer.

---

## Appendix A: CST map (current implementation)

| CST | Source standard § | Implementation |
|---|---|---|
| CST-001 | §6 (CATALOG.yaml required) | `cst_001_has_catalog_yaml` |
| CST-002 | §6 (schema validation) | `cst_002_catalog_yaml_validates_against_schema` |
| CST-003 | §5 (subtree shape) | `cst_003_subtree_shape` |
| CST-004 | §5 (canonical YAML required fields) | `cst_004_canonical_yaml_required_fields` |
| CST-005 | §6 (entities correspond to subtrees) | `cst_005_entities_match_subtrees` |
| CST-006 | §6 (no orphan subtrees) | `cst_006_no_orphan_subtrees` |
| CST-007 | §6 (paths resolve) | `cst_007_paths_resolve` |
| CST-008 | §6 (state matches subtree) | `cst_008_state_matches_subtree` |
| CST-009 | §5 (research README) | `cst_009_research_readme` (warning) |
| CST-010 | §5 (retired lifecycle) | `cst_010_retired_lifecycle` |
| CST-011 | §5 (candidate version) | `cst_011_candidate_version` |
| CST-012 | §6 (metamodel-pointer paths) | `cst_012_metamodel_pointer_paths` |
| CST-013 | §8 (regenerator present) | `cst_013_regenerator_present` |
| CST-014 | §8 (gate present) | `cst_014_gate_present` |
| CST-015 | §8 (CI workflow references) | `cst_015_ci_workflow_references_scripts` |
| CST-016 | This CR (template-version diff) | `cst_016_template_version` (warning) |

## Appendix B: Worked example

End-to-end demonstration of the standard on the in-tree conforming fixture:

```bash
# 1. Bootstrap a fresh catalog
cd /tmp
python /path/to/dea-metaframework/tools/bootstrap_catalog_repo.py \
    --target /tmp/demo-catalog \
    --catalog-id dea:catalog-demo \
    --catalog-name "Demo Catalog" \
    --catalog-abbreviation DC
# -> OK: bootstrapped dea:catalog-demo at /tmp/demo-catalog (template version 0.1.0)

# 2. Add a canonical entity
mkdir -p /tmp/demo-catalog/entities/v1-alpha/dea:demo-entity
cat > /tmp/demo-catalog/entities/v1-alpha/dea:demo-entity/dea:demo-entity.yaml <<'YAML'
id: dea:demo-entity
type: Demo
name: Demo Entity
version: 1.0.0
lifecycle_status: active
definition: |
  A canonical entity for the demo catalog.
YAML

# 3. Regenerate CATALOG.yaml
python /path/to/dea-metaframework/tools/regenerate_catalog.py \
    --catalog-root /tmp/demo-catalog
# -> writes CATALOG.yaml

# 4. Validate
python /path/to/dea-metaframework/tools/check_catalog_index.py \
    --catalog-root /tmp/demo-catalog
# -> OK: CATALOG.yaml validates (1 entities)

# 5. Run the cross-repo conformance suite
python /path/to/dea-metaframework/tools/conformance_test_catalog_structure.py \
    --catalog-root /tmp/demo-catalog \
    --template-root /path/to/dea-metaframework/tools/catalog-repo-template
# -> OK: 16 CST(s) passed (1 warning(s))
#    WARN: CST-016: catalog has no TEMPLATE_VERSION...
#    (warning is expected; the bootstrap script writes it, but the user
#     must commit and push it for downstream tools to see)

# 6. Watch the suite catch a deliberate drift
rm /tmp/demo-catalog/CATALOG.yaml
python /path/to/dea-metaframework/tools/conformance_test_catalog_structure.py \
    --catalog-root /tmp/demo-catalog
# -> FAIL: CST-001: CATALOG.yaml missing at repo root
#    exit 2
```

The example uses no external services, no network, no `gh` authentication. Reviewers can replay it locally with one Python invocation.
