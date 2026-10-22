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

import re
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
    """Record a failure AND fail the calling test immediately.

    This used to only append to the module-level FAILURES list, which
    made the module unfailable under pytest: `run_all()` (the only
    reporter) runs solely under `if __name__ == "__main__":`, so every
    test passed no matter what the suite found. The same fixture could
    report "11 passed" under pytest and "FAIL ... rc=1" standalone.

    Raising keeps both runners honest -- pytest fails the test, and
    `run_all()` catches the exception and records it -- while the append
    is retained so the standalone reporter still prints every message.
    No test depends on accumulating: each check() is an independent
    assertion.
    """
    if not condition:
        FAILURES.append(message)
        raise AssertionError(message)


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


# ---------- CST-013 / CST-014: pinned upstream resolution ----------

def test_cst_013_accepts_freshly_bootstrapped_catalog(tmp_root: Path) -> None:
    """A catalog bootstrapped from the template must PASS the standard.

    This is the regression CST-013 originally could not survive: the
    template ships only scripts/.gitkeep and stages the tools from a
    pinned upstream ref at CI time, so asserting a committed
    scripts/regenerate_catalog.py failed every correctly-bootstrapped
    catalog.
    """
    target = tmp_root / "bootstrapped-pin"
    rc = run_subprocess(
        [
            str(BOOTSTRAP),
            "--target", str(target),
            "--catalog-id", "dea:catalog-pin-test",
            "--catalog-name", "Pin Test",
            "--catalog-abbreviation", "PT",
            "--owner", "TechNeHub Labs",
        ],
        cwd=tmp_root,
    )
    check(rc.returncode == 0, f"bootstrap failed: rc={rc.returncode}; stderr={rc.stderr}")
    check(
        not (target / "scripts" / "regenerate_catalog.py").exists(),
        "fixture precondition broken: template now vendors the regenerator, so this "
        "test no longer covers the pinned-resolution path",
    )
    for cst in ("CST-013", "CST-014"):
        rc = run_subprocess(
            [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", cst],
            cwd=tmp_root,
        )
        check(rc.returncode == 0, f"{cst} should pass for a bootstrapped catalog; "
                                  f"got {rc.returncode}; stderr={rc.stderr}")


def test_cst_013_rejects_unpinned_upstream_branch(tmp_root: Path) -> None:
    """An upstream checkout pinned to a branch is not a pin.

    `ref: main` tracks a moving target, so every catalog repo would
    silently inherit whatever upstream shipped that day without review.
    """
    target = tmp_root / "unpinned"
    copy_conforming(target)
    wf = target / ".github" / "workflows" / "ci.yml"
    wf.write_text(
        wf.read_text(encoding="utf-8").replace("ref: v2.6.0", "ref: main"),
        encoding="utf-8",
    )
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", "CST-013"],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"unpinned branch should fail CST-013; got {rc.returncode}")
    check("release tag" in rc.stderr, f"CST-013 should name the pin requirement; stderr={rc.stderr}")


def test_cst_013_rejects_pin_without_sourcing_step(tmp_root: Path) -> None:
    """Pinning the upstream but never staging the tool from it is not enough.

    Guards against a workflow that declares a pin for appearance while
    still running something else.
    """
    target = tmp_root / "pin-not-sourced"
    copy_conforming(target)
    wf = target / ".github" / "workflows" / "ci.yml"
    text = wf.read_text(encoding="utf-8")
    # Keep the pinned checkout, drop the staging step that copies out of it.
    text = text.replace("cp .metaframework/tools/regenerate_catalog.py scripts/\n", "")
    text = text.replace("cp .metaframework/tools/check_catalog_index.py scripts/\n", "")
    text = text.replace("cp .metaframework/tools/catalog-index-schema.json scripts/\n", "")
    wf.write_text(text, encoding="utf-8")
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", "CST-013"],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"pin without a sourcing step should fail CST-013; got {rc.returncode}")
    check("never" in rc.stderr and "sources" in rc.stderr,
          f"CST-013 should say the tool is never sourced; stderr={rc.stderr}")


def test_cst_013_rejects_neither_pinned_nor_vendored(tmp_root: Path) -> None:
    """No pin and no vendored copy is non-conforming on both counts."""
    target = tmp_root / "neither"
    copy_conforming(target)
    wf = target / ".github" / "workflows" / "ci.yml"
    text = wf.read_text(encoding="utf-8")
    # Remove the upstream declaration entirely, and leave no vendored file.
    text = re.sub(r"      - name: Fetch regenerator.*?\n          path: \.metaframework\n", "", text, flags=re.S)
    text = text.replace("cp .metaframework/tools/regenerate_catalog.py scripts/\n", "")
    text = text.replace("cp .metaframework/tools/check_catalog_index.py scripts/\n", "")
    text = text.replace("cp .metaframework/tools/catalog-index-schema.json scripts/\n", "")
    wf.write_text(text, encoding="utf-8")
    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", "CST-013"],
        cwd=tmp_root,
    )
    check(rc.returncode == 2, f"unresolvable tool should fail CST-013; got {rc.returncode}")
    check("neither" in rc.stderr, f"CST-013 should say neither; stderr={rc.stderr}")


def test_cst_013_warns_when_vendored_without_pin(tmp_root: Path) -> None:
    """A vendored copy is accepted but warned about, not silently passed.

    This is the drift class F9 existed to hide: a committed copy that
    nothing ties to the upstream it claims to be. Accepting it silently is
    how the fixture's four copies diverged unnoticed.
    """
    target = tmp_root / "vendored-unpinned"
    copy_conforming(target)
    wf = target / ".github" / "workflows" / "ci.yml"
    wf.write_text(
        "name: CI\non:\n  pull_request:\n    branches: [main]\n"
        "jobs:\n  gate:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - run: python scripts/regenerate_catalog.py --check\n",
        encoding="utf-8",
    )
    (target / "scripts").mkdir(exist_ok=True)
    (target / "scripts" / "regenerate_catalog.py").write_text("# stand-in\n", encoding="utf-8")

    rc = run_subprocess(
        [str(CONFORMANCE), "--catalog-root", str(target), "--template-root", str(TEMPLATE), "--cst", "CST-013"],
        cwd=tmp_root,
    )
    check(rc.returncode == 0, f"vendored fallback should pass CST-013; got {rc.returncode}; stderr={rc.stderr}")
    check("vendored, not pinned" in rc.stderr,
          f"CST-013 should warn that a vendored tool can drift; stderr={rc.stderr}")


def test_fixture_carries_no_vendored_tool_copies() -> None:
    """The fixture must not carry copies of the shared tools (F9).

    Every one of the four copies it used to hold had drifted from tools/,
    and nothing tied them to the upstream they claimed to be. The fixture
    now models a real catalog: tools staged at CI time from a pinned tag.
    """
    fixture_scripts = CONFORMING_FIXTURE / "scripts"
    fixture_tools = CONFORMING_FIXTURE / "tools"
    for name in ("regenerate_catalog.py", "check_catalog_index.py", "catalog-index-schema.json"):
        check(
            not (fixture_scripts / name).exists(),
            f"fixture still vendors scripts/{name}; it must be resolved from the pinned upstream ref",
        )
        check(
            not (fixture_tools / name).exists(),
            f"fixture still vendors tools/{name}; the canonical copy is tools/{name} in this repo",
        )


def test_cst_filter_runs_only_named(tmp_root: Path) -> None:
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
    # CATALOG.yaml is deliberately absent: bootstrap scaffolds the catalog
    # but does not generate the index. The first `regenerate_catalog.py`
    # run produces it. Asserting its absence here is what pins that
    # contract, so a future change to bootstrap cannot silently start
    # emitting a stale or hand-built index.
    check(
        not (target / "CATALOG.yaml").exists(),
        "bootstrap unexpectedly created CATALOG.yaml; it must be generated "
        "by regenerate_catalog.py, not scaffolded",
    )
    for required in (
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
    # The abbreviation is NOT a README placeholder: no file under
    # tools/catalog-repo-template/ contains {{CATALOG_ABBREVIATION}}, so
    # asserting it appears in README was asserting something the template
    # never asked for. It is consumed by build_metamodel_pointer, which
    # writes metamodel-pointer.yaml, so that is where it must be checked.
    check(
        "TB" not in readme,
        "abbreviation leaked into README; it belongs only in "
        "metamodel-pointer.yaml",
    )

    pointer_text = (target / "metamodel-pointer.yaml").read_text(encoding="utf-8")
    check("TB" in pointer_text, "abbreviation not written to metamodel-pointer.yaml")

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
    """Build a tmp root for the standalone runner, mirroring pytest's fixture.

    `tests/conftest.py::tmp_root` seeds `<tmp_root>/tools/` with the
    canonical schema and the catalog repo template. The standalone runner
    needs the same layout, or a test relying on the default
    `--template-root` resolves it under the tmp root and bootstrap fails
    with "template root ... is not a directory".

    Keeping the two in step matters: they are the same suite run by two
    runners, and a test that passes under pytest must also pass standalone.
    """
    import tempfile
    root = Path(tempfile.mkdtemp(prefix="cst-fixture-"))
    tools_dst = root / "tools"
    tools_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCHEMA, tools_dst / "catalog-index-schema.json")
    shutil.copytree(TEMPLATE, tools_dst / "catalog-repo-template")
    return root


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
