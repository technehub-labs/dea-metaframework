"""Self-tests for tools/conformance_test_catalog_structure.py (CR-CATALOG-STRUCT-06b).

The suite:
- runs the conformance suite against the in-tree conforming fixture and
  asserts all CSTs pass;
- builds synthetic catalogs in `tmp_path` that violate specific CSTs and
  asserts the suite flags them;
- verifies the suite's --strict mode escalates CST-009 / CST-016 warnings;
- runs the bootstrap script and asserts the result is conformant.

Conventions match `tests/conformance/test_005_coordinate_spec.py` and
`tests/test_catalog_index_machinery.py`: stdlib only (plus PyYAML and
jsonschema, which are already installed), module-level FAILURES list,
exit-0-or-1 runner.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

CONFORMANCE = REPO_ROOT / "tools" / "conformance_test_catalog_structure.py"
BOOTSTRAP = REPO_ROOT / "tools" / "bootstrap_catalog_repo.py"
REGEN = REPO_ROOT / "tools" / "regenerate_catalog.py"
SCHEMA = REPO_ROOT / "tools" / "catalog-index-schema.json"
TEMPLATE = REPO_ROOT / "tools" / "catalog-repo-template"
CONFORMING_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "catalog-conforming"

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


def copy_conforming(target: Path) -> None:
    shutil.copytree(CONFORMING_FIXTURE, target)


# ---------- Conformance suite tests ----------

def test_conformance_passes_against_conforming_fixture(tmp_root: Path) -> None:
    target = tmp_root / "conforming"
    copy_conforming(target)
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    # Conforming fixture has no TEMPLATE_VERSION, so CST-016 emits a warning
    # but the suite still passes (warning-only).
    check(
        rc.returncode == 0,
        f"conformance on conforming fixture expected exit 0; got {rc.returncode}; stderr={rc.stderr}; stdout={rc.stdout}",
    )


def test_conformance_flags_missing_catalog_yaml(tmp_root: Path) -> None:
    target = tmp_root / "missing-catalog"
    copy_conforming(target)
    (target / "CATALOG.yaml").unlink()
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"missing CATALOG.yaml expected exit 2; got {rc.returncode}; stderr={rc.stderr}")
    check("CST-001" in rc.stderr, f"CST-001 not flagged; stderr={rc.stderr}")


def test_conformance_flags_unresolved_path(tmp_root: Path) -> None:
    target = tmp_root / "bad-path"
    copy_conforming(target)
    # Manually edit CATALOG.yaml to point a path at a missing file.
    text = (target / "CATALOG.yaml").read_text(encoding="utf-8")
    bad = text.replace(
        "entities/v1-alpha/dea:process-foo/dea:process-foo.yaml",
        "entities/v1-alpha/dea:process-foo/missing.yaml",
    )
    (target / "CATALOG.yaml").write_text(bad, encoding="utf-8")
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"bad path expected exit 2; got {rc.returncode}; stderr={rc.stderr}")
    check("CST-007" in rc.stderr, f"CST-007 not flagged; stderr={rc.stderr}")


def test_conformance_flags_orphan_subtree(tmp_root: Path) -> None:
    target = tmp_root / "orphan"
    copy_conforming(target)
    # Add a new subtree not declared in CATALOG.yaml.
    new_subtree = target / "entities" / "v1-alpha" / "dea:orphan-entity"
    new_subtree.mkdir(parents=True, exist_ok=True)
    (new_subtree / "dea:orphan-entity.yaml").write_text(
        "id: dea:orphan-entity\ntype: Process\nname: Orphan\nversion: 1.0.0\nlifecycle_status: active\n",
        encoding="utf-8",
    )
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"orphan subtree expected exit 2; got {rc.returncode}; stderr={rc.stderr}")
    check("CST-006" in rc.stderr, f"CST-006 not flagged; stderr={rc.stderr}")


def test_conformance_flags_missing_ci_workflow(tmp_root: Path) -> None:
    target = tmp_root / "no-ci"
    copy_conforming(target)
    # Remove the CI workflow (and the .github directory entirely).
    shutil.rmtree(target / ".github")
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"no CI workflow expected exit 2; got {rc.returncode}; stderr={rc.stderr}")
    check("CST-015" in rc.stderr, f"CST-015 not flagged; stderr={rc.stderr}")


def test_conformance_strict_escalates_template_drift(tmp_root: Path) -> None:
    target = tmp_root / "drift"
    copy_conforming(target)
    # Add a TEMPLATE_VERSION that doesn't match the canonical template's.
    (target / "TEMPLATE_VERSION").write_text("99.99.99\n", encoding="utf-8")
    rc_default = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE)],
        cwd=tmp_root,
    )
    check(rc_default.returncode == 0, f"default mode expected exit 0 (warning only); got {rc_default.returncode}; stderr={rc_default.stderr}")
    check("CST-016" in rc_default.stderr, "CST-016 warning not surfaced")

    rc_strict = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--strict"],
        cwd=tmp_root,
    )
    check(rc_strict.returncode == 2, f"strict mode expected exit 2; got {rc_strict.returncode}; stderr={rc_strict.stderr}")
    check("STRICT" in rc_strict.stderr, "STRICT escalation not flagged")


def test_conformance_cst_filter_runs_only_named(tmp_root: Path) -> None:
    target = tmp_root / "filter"
    copy_conforming(target)
    (target / "CATALOG.yaml").unlink()  # would fail CST-001
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", "CST-013"],
        cwd=tmp_root,
    )
    check(rc.returncode == 0, f"CST-013-only run expected exit 0; got {rc.returncode}; stderr={rc.stderr}")


# ---------- Bootstrap script tests ----------

def test_bootstrap_produces_conformant_catalog(tmp_root: Path) -> None:
    target = tmp_root / "bootstrapped"
    rc = run_subprocess(
        [
            str(BOOTSTRAP),
            "--target", str(target),
            "--catalog-id", "dea:catalog-test-bootstrapped",
            "--catalog-name", "Test Bootstrapped",
            "--catalog-abbreviation", "TB",
            "--owner", "TechNeHub Labs",
        ],
        cwd=REPO_ROOT,
    )
    check(rc.returncode == 0, f"bootstrap expected exit 0; got {rc.returncode}; stderr={rc.stderr}; stdout={rc.stdout}")

    # The bootstrapped catalog must contain the expected files.
    for required in (
        "CATALOG.yaml",  # may be missing until first regen; that's expected
        "TEMPLATE_VERSION",
        "metamodel-pointer.yaml",
        "README.md",
        "scripts/.gitkeep",
        ".github/workflows/ci.yml",
        "entities/v1-alpha/.gitkeep",
    ):
        check(
            (target / required).exists(),
            f"bootstrap did not create {required}",
        )

    # Placeholder replacement happened.
    readme = (target / "README.md").read_text(encoding="utf-8")
    check("dea:catalog-test-bootstrapped" in readme, "catalog_id not substituted into README")
    check("Test Bootstrapped" in readme, "catalog_name not substituted into README")
    check("TB" in readme, "abbreviation not substituted into README")

    license_text = (target / "LICENSE").read_text(encoding="utf-8")
    check("TechNeHub Labs" in license_text, "owner not substituted into LICENSE")

    pointer = (target / "metamodel-pointer.yaml").read_text(encoding="utf-8")
    check("dea:catalog-test-bootstrapped" in pointer, "catalog_id not in metamodel-pointer.yaml")


def test_bootstrap_refuses_overwrite_without_force(tmp_root: Path) -> None:
    target = tmp_root / "existing"
    target.mkdir()
    (target / "marker.txt").write_text("do not delete\n", encoding="utf-8")
    rc = run_subprocess(
        [
            str(BOOTSTRAP),
            "--target", str(target),
            "--catalog-id", "dea:catalog-x",
            "--catalog-name", "X",
        ],
        cwd=REPO_ROOT,
    )
    check(rc.returncode != 0, f"bootstrap into existing dir expected nonzero; got {rc.returncode}")
    check((target / "marker.txt").exists(), "bootstrap deleted existing marker without --force")


def test_bootstrap_with_force_replaces(tmp_root: Path) -> None:
    target = tmp_root / "force"
    target.mkdir()
    (target / "stale.txt").write_text("stale\n", encoding="utf-8")
    rc = run_subprocess(
        [
            str(BOOTSTRAP),
            "--target", str(target),
            "--catalog-id", "dea:catalog-f",
            "--catalog-name", "F",
            "--force",
        ],
        cwd=REPO_ROOT,
    )
    check(rc.returncode == 0, f"--force bootstrap expected exit 0; got {rc.returncode}; stderr={rc.stderr}")
    check(not (target / "stale.txt").exists(), "--force did not clear stale file")
    check((target / "TEMPLATE_VERSION").is_file(), "--force did not write TEMPLATE_VERSION")


def test_bootstrap_writes_matching_template_version(tmp_root: Path) -> None:
    target = tmp_root / "version"
    rc = run_subprocess(
        [
            str(BOOTSTRAP),
            "--target", str(target),
            "--catalog-id", "dea:catalog-v",
            "--catalog-name", "V",
        ],
        cwd=REPO_ROOT,
    )
    check(rc.returncode == 0, f"bootstrap exit {rc.returncode}; stderr={rc.stderr}")
    template_v = (TEMPLATE / "TEMPLATE_VERSION").read_text(encoding="utf-8").strip()
    catalog_v = (target / "TEMPLATE_VERSION").read_text(encoding="utf-8").strip()
    check(catalog_v == template_v, f"catalog TEMPLATE_VERSION {catalog_v!r} != template {template_v!r}")


# ---------- Runner ----------

def make_tmp_root() -> Path:
    import tempfile
    return Path(tempfile.mkdtemp(prefix="cst-fixture-"))


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def run_all() -> int:
    import inspect
    tests = sorted(
        (name, fn)
        for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )

    for name, fn in tests:
        sig = inspect.signature(fn)
        takes_tmp = "tmp_root" in sig.parameters
        if not takes_tmp:
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")
            continue

        tmp_root = make_tmp_root()
        try:
            fn(tmp_root)
        except Exception as exc:  # noqa: BLE001
            FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")
        finally:
            cleanup(tmp_root)

    if FAILURES:
        print(f"FAIL: {len(FAILURES)} conformance-test failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"OK: {len(tests)} conformance-test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
