"""Self-tests for tools/check_release_pins.py (CR-CATALOG-STRUCT-13).

Offline: exercises the extraction and scoping rules only; the live
ls-remote existence check runs in the `pins-resolve` CI job and
locally. Dual-runner like the sibling suites: pytest discovers the
test_* functions; run_all() reports standalone under __main__.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from check_release_pins import extract_pins  # noqa: E402

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)
        raise AssertionError(message)


TEMPLATE_CI = """\
jobs:
  catalog-gate:
    steps:
      - uses: actions/checkout@v4
      - name: Fetch regenerator + gates from metaframework
        uses: actions/checkout@v4
        with:
          repository: technehub-labs/dea-metaframework
          ref: v2.7.0
          path: .metaframework
      - name: Allocation (root model, not our pin)
        uses: technehub-labs/dea-architecture-framework/.github/workflows/validate-against-model.yml@v0.9.0
"""

GENERATOR_SNIPPET = """\
metaframework_pin: v2.7.0

# README table row emitted per kit:
# | Dependency manifest | dependencies.yaml: metamodel 1.0.0, root model {root_ref}, metaframework v2.7.0 |
"""


def test_template_ref_scoped_to_upstream_step() -> None:
    """The template CI's metaframework ref is a pin; the validate-allocation
    step's root-model ref is NOT (different upstream, must never be
    checked against metaframework tags)."""
    pins = extract_pins(TEMPLATE_CI)
    check(pins == ["v2.7.0"], f"expected exactly ['v2.7.0'], got {pins}")


def test_generator_pin_and_table_forms() -> None:
    pins = extract_pins(GENERATOR_SNIPPET)
    check(pins == ["v2.7.0"], f"expected exactly ['v2.7.0'], got {pins}")


def test_prerelease_and_build_suffixes_admitted() -> None:
    text = (
        "repository: technehub-labs/dea-metaframework\n"
        "ref: v2.9.0-rc1\n"
    )
    check(extract_pins(text) == ["v2.9.0-rc1"], f"got {extract_pins(text)}")


def test_branch_ref_ignored() -> None:
    """A `ref: main` is a floating pin, not a release-tag pin: out of
    this gate's scope (org-wide floating-pin watching lives in the
    governance reconciler)."""
    text = (
        "repository: technehub-labs/dea-metaframework\n"
        "ref: main\n"
    )
    check(extract_pins(text) == [], f"got {extract_pins(text)}")


def test_scan_targets_cover_generator_and_template() -> None:
    from check_release_pins import _scan_targets
    targets = _scan_targets(REPO_ROOT)
    names = [str(p.relative_to(REPO_ROOT)) for p in targets]
    check("tools/generate_catalog_kit.py" in names, f"generator missing: {names}")
    check(
        any("catalog-repo-template" in n for n in names),
        f"template files missing: {names}",
    )


def test_pins_on_current_tree_resolve_live() -> None:
    """Live (network) sanity: every pin the tree currently advertises
    exists. Mirrors the CI job so a local run can catch the same
    defect before pushing."""
    import subprocess
    from check_release_pins import _existing_tags, _scan_targets
    pins: set[str] = set()
    for path in _scan_targets(REPO_ROOT):
        try:
            pins.update(extract_pins(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    check(bool(pins), "no pins found on the current tree; scan patterns stale")
    tags = _existing_tags()
    check(tags is not None, "ls-remote failed (transport)")
    missing = sorted(p for p in pins if p not in (tags or set()))
    check(not missing, f"pins on the current tree that do not exist: {missing}")


def run_all() -> int:
    import inspect
    tests = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    for name, fn in tests:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")
    if FAILURES:
        print(f"FAIL: {len(FAILURES)} release-pin-test failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"OK: {len(tests)} release-pin-test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
