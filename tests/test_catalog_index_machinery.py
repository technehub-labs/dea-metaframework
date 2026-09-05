"""Self-tests for tools/regenerate_catalog.py and tools/check_catalog_index.py.

Authority: CR-CATALOG-STRUCT-06a §6.

The suite builds a fixture catalog under `tmp_path`, invokes the
regenerator and gate as subprocesses (CLI surface is the actual contract),
and asserts the contract properties listed in the CR.

Conventions match `tests/conformance/test_005_coordinate_spec.py`:
stdlib only, module-level FAILURES list, exit-0-or-1 runner.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

REGEN = REPO_ROOT / "tools" / "regenerate_catalog.py"
GATE = REPO_ROOT / "tools" / "check_catalog_index.py"
SCHEMA = REPO_ROOT / "tools" / "catalog-index-schema.json"

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def run_subprocess(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *cmd],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
    )


def write_yaml(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_fixture(
    root: Path,
    *,
    canonical_entities: list[tuple[str, dict]] | None = None,
    research_entities: list[str] | None = None,
    candidate_entities: list[str] | None = None,
    retired_entities: list[tuple[str, str]] | None = None,
) -> None:
    """Construct a minimal conforming catalog fixture under `root`."""
    if canonical_entities is None:
        canonical_entities = []
    if research_entities is None:
        research_entities = []
    if candidate_entities is None:
        candidate_entities = []
    if retired_entities is None:
        retired_entities = []
    root.mkdir(parents=True, exist_ok=True)
    # metamodel-pointer.yaml
    write_yaml(
        root / "metamodel-pointer.yaml",
        "id: dea:catalog-fixture\n"
        "name: Fixture Catalog\n"
        "abbreviation: FX\n"
        "version: 1.0.0\n"
        "status: active\n"
        "metamodel_version: 1.0.0\n"
        "description: Self-test fixture.\n"
        "owner: TechNeHub Labs\n",
    )
    # directory scaffolding the gate's cross_cutting check expects to exist
    for sub in ("classifications", "schemas", "scripts", "contributions", "change-requests"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    for entity_id, payload in canonical_entities:
        subtree = root / "entities" / "v1-alpha" / entity_id
        subtree.mkdir(parents=True, exist_ok=True)
        (subtree / "research").mkdir(exist_ok=True)
        (subtree / "candidates").mkdir(exist_ok=True)
        (subtree / "retired").mkdir(exist_ok=True)
        body = "\n".join(f"{k}: {v!r}" if not isinstance(v, str) else f"{k}: {v}" for k, v in payload.items())
        write_yaml(subtree / f"{entity_id}.yaml", body + "\n")

    for entity_id in research_entities:
        subtree = root / "entities" / "v1-alpha" / entity_id
        subtree.mkdir(parents=True, exist_ok=True)
        (subtree / "research").mkdir(exist_ok=True)
        write_yaml(subtree / "research" / "evidence.yaml", "claim: research only\n")

    for entity_id in candidate_entities:
        subtree = root / "entities" / "v1-alpha" / entity_id
        subtree.mkdir(parents=True, exist_ok=True)
        (subtree / "candidates").mkdir(exist_ok=True)
        write_yaml(subtree / "candidates" / f"{entity_id}.yaml", "id: placeholder\n")

    for entity_id, lifecycle in retired_entities:
        subtree = root / "entities" / "v1-alpha" / entity_id
        subtree.mkdir(parents=True, exist_ok=True)
        (subtree / "research").mkdir(exist_ok=True)
        (subtree / "candidates").mkdir(exist_ok=True)
        (subtree / "retired").mkdir(exist_ok=True)
        write_yaml(
            subtree / f"{entity_id}.yaml",
            f"id: {entity_id}\ntype: Process\nversion: 1.0.0\nlifecycle_status: {lifecycle}\n",
        )


# ---------- Regenerator tests ----------

def test_regenerator_emits_canonical_entity(tmp_root: Path) -> None:
    build_fixture(
        tmp_root,
        canonical_entities=[
            ("dea:process-foo", {"id": "dea:process-foo", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"}),
        ],
    )
    res = run_subprocess(
        [str(REGEN), "--catalog-root", str(tmp_root)],
        cwd=tmp_root,
    )
    check(res.returncode == 0, f"regenerator exit code {res.returncode}; stderr={res.stderr}")
    out = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    check("dea:process-foo" in out, "canonical entity not in CATALOG.yaml")
    check("state: canonical" in out, "canonical state not emitted")
    check("canonical_count: 1" in out, "canonical_count not 1")


def test_regenerator_emits_research_only_state(tmp_root: Path) -> None:
    build_fixture(tmp_root, research_entities=["dea:research-bar"])
    res = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(res.returncode == 0, f"regen exit {res.returncode}; stderr={res.stderr}")
    out = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    check("dea:research-bar" in out, "research entity missing from CATALOG.yaml")
    check("state: research" in out, "research state not emitted")


def test_regenerator_emits_candidate_only_state(tmp_root: Path) -> None:
    build_fixture(tmp_root, candidate_entities=["dea:pc-od-co"])
    res = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(res.returncode == 0, f"regen exit {res.returncode}; stderr={res.stderr}")
    out = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    check("state: candidate" in out, "candidate state not emitted")


def test_regenerator_emits_retired_via_lifecycle_status(tmp_root: Path) -> None:
    build_fixture(tmp_root, retired_entities=[("dea:process-old", "retired")])
    res = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(res.returncode == 0, f"regen exit {res.returncode}; stderr={res.stderr}")
    out = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    check("dea:process-old" in out, "retired entity missing")
    check("state: retired" in out, "retired state not emitted")


def test_regenerator_is_deterministic(tmp_root: Path) -> None:
    build_fixture(
        tmp_root,
        canonical_entities=[
            ("dea:process-aaa", {"id": "dea:process-aaa", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"}),
            ("dea:process-zzz", {"id": "dea:process-zzz", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"}),
        ],
        research_entities=["dea:research-1"],
        candidate_entities=["dea:candidate-2"],
    )
    r1 = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(r1.returncode == 0, f"first regen exit {r1.returncode}")
    out1 = (tmp_root / "CATALOG.yaml").read_bytes()
    r2 = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(r2.returncode == 0, f"second regen exit {r2.returncode}")
    out2 = (tmp_root / "CATALOG.yaml").read_bytes()
    check(out1 == out2, f"non-deterministic output:\nfirst={out1!r}\nsecond={out2!r}")


def test_regenerator_check_exits_3_on_stale(tmp_root: Path) -> None:
    build_fixture(tmp_root, canonical_entities=[("dea:process-x", {"id": "dea:process-x", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"})])
    r1 = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(r1.returncode == 0, f"initial regen exit {r1.returncode}")
    # Add a new entity subtree; CATALOG.yaml is now stale.
    new_subtree = tmp_root / "entities" / "v1-alpha" / "dea:process-new"
    new_subtree.mkdir(parents=True, exist_ok=True)
    write_yaml(new_subtree / "research" / "new.md", "# new\n")
    rc = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root), "--check"], cwd=tmp_root)
    check(rc.returncode == 3, f"--check on stale expected exit 3; got {rc.returncode}; stderr={rc.stderr}")


def test_regenerator_dry_run_does_not_write(tmp_root: Path) -> None:
    build_fixture(tmp_root, canonical_entities=[("dea:process-dry", {"id": "dea:process-dry", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"})])
    rc = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root), "--dry-run"], cwd=tmp_root)
    check(rc.returncode == 0, f"dry-run exit {rc.returncode}; stderr={rc.stderr}")
    check("dea:process-dry" in rc.stdout, "dry-run stdout missing entity")
    check(not (tmp_root / "CATALOG.yaml").exists(), "dry-run wrote CATALOG.yaml unexpectedly")


# ---------- Gate tests ----------

def test_check_passes_after_regenerate(tmp_root: Path) -> None:
    build_fixture(
        tmp_root,
        canonical_entities=[("dea:process-good", {"id": "dea:process-good", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"})],
    )
    r1 = run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(r1.returncode == 0, f"regen exit {r1.returncode}")
    r2 = run_subprocess([str(GATE), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(r2.returncode == 0, f"gate exit {r2.returncode}; stderr={r2.stderr}; stdout={r2.stdout}")


def test_check_fails_on_schema_violation(tmp_root: Path) -> None:
    build_fixture(tmp_root, canonical_entities=[("dea:process-bad", {"id": "dea:process-bad", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"})])
    run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    # Tamper: invalid state value.
    text = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    (tmp_root / "CATALOG.yaml").write_text(text.replace("state: canonical", "state: bogus"), encoding="utf-8")
    rc = run_subprocess([str(GATE), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(rc.returncode == 1, f"gate on invalid state expected exit 1; got {rc.returncode}; stderr={rc.stderr}")


def test_check_fails_on_unresolved_path(tmp_root: Path) -> None:
    build_fixture(tmp_root, canonical_entities=[("dea:process-path", {"id": "dea:process-path", "type": "Process", "version": "1.0.0", "lifecycle_status": "active"})])
    run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    text = (tmp_root / "CATALOG.yaml").read_text(encoding="utf-8")
    bad = text.replace("entities/v1-alpha/dea:process-path/dea:process-path.yaml", "entities/v1-alpha/dea:process-path/missing.yaml")
    (tmp_root / "CATALOG.yaml").write_text(bad, encoding="utf-8")
    rc = run_subprocess([str(GATE), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(rc.returncode == 2, f"gate on unresolved path expected exit 2; got {rc.returncode}; stderr={rc.stderr}")


def test_check_strict_upgrades_missing_readme_to_error(tmp_root: Path) -> None:
    build_fixture(tmp_root, research_entities=["dea:research-no-readme"])
    run_subprocess([str(REGEN), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    rc_default = run_subprocess([str(GATE), "--catalog-root", str(tmp_root)], cwd=tmp_root)
    check(rc_default.returncode == 0, f"default gate exit {rc_default.returncode} (expected 0 with warning); stderr={rc_default.stderr}")
    rc_strict = run_subprocess([str(GATE), "--catalog-root", str(tmp_root), "--strict"], cwd=tmp_root)
    check(rc_strict.returncode == 2, f"strict gate exit {rc_strict.returncode} (expected 2 for missing README); stderr={rc_strict.stderr}")


# ---------- Conformance non-regression ----------

def test_no_regression_on_ecf_conformance_suite() -> None:
    conformance_test = REPO_ROOT / "tests" / "conformance" / "test_005_coordinate_spec.py"
    rc = run_subprocess([str(conformance_test)], cwd=REPO_ROOT)
    check(rc.returncode == 0, f"ECF conformance suite regression: exit {rc.returncode}; stdout={rc.stdout}; stderr={rc.stderr}")


# ---------- Runner ----------

def make_tmp_root() -> Path:
    import tempfile
    return Path(tempfile.mkdtemp(prefix="catalog-fixture-"))


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def run_all() -> int:
    """Run each test_* in its own tmp_root and aggregate failures."""
    import inspect

    tests = sorted(
        (name, fn)
        for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )

    for name, fn in tests:
        sig = inspect.signature(fn)
        takes_tmp = "tmp_root" in sig.parameters or any(
            p.kind is inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values()
        )
        if not takes_tmp:
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")
            continue

        tmp_root = make_tmp_root()
        # Always copy the schema into the fixture so the regenerator's
        # --schema tools/catalog-index-schema.json resolution finds it.
        schema_dst = tmp_root / "tools" / "catalog-index-schema.json"
        schema_dst.parent.mkdir(parents=True, exist_ok=True)
        schema_dst.write_bytes(SCHEMA.read_bytes())
        try:
            fn(tmp_root)
        except Exception as exc:  # noqa: BLE001
            FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")
        finally:
            cleanup(tmp_root)

    if FAILURES:
        print(f"FAIL: {len(FAILURES)} machinery failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"OK: {len(tests)} machinery test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
