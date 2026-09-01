"""Conformance suite for the ECF coordinate specification.

Authority: specification/ecf-coordinates.md (CR-ECF-005).

The suite enforces:
- the canonical Domain and Stage enumerations,
- the 49-derivable count,
- the coordinate identifier pattern,
- the no-cell-filling rule (no requirement that every coordinate have a
  catalog entry),
- validator acceptance/rejection behaviour.

It runs against the in-repo enumeration tool (`tools/ecf_coordinates.py`)
and validates every JSON payload under `schemas/` and `framework/`. The
intentional absence of a `conftest.py` keeps the suite dependency-free
(stardard library only); the CI workflow installs pytest if a richer
runner is desired.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import ecf_coordinates as ecf  # noqa: E402

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def test_canonical_domain_count() -> None:
    check(len(ecf.DOMAINS) == 7, f"expected 7 canonical domains, got {len(ecf.DOMAINS)}")


def test_canonical_stage_count() -> None:
    check(len(ecf.STAGES) == 7, f"expected 7 canonical stages, got {len(ecf.STAGES)}")


def test_domain_values_are_unique() -> None:
    check(
        len(set(ecf.DOMAINS)) == len(ecf.DOMAINS),
        f"domain set is not unique: {ecf.DOMAINS}",
    )


def test_stage_values_are_unique() -> None:
    check(
        len(set(ecf.STAGES)) == len(ecf.STAGES),
        f"stage set is not unique: {ecf.STAGES}",
    )


def test_full_coordinate_count_is_49() -> None:
    coords = ecf.enumerate_coordinates()
    check(
        len(coords) == 49,
        f"expected 49 derivable coordinates, got {len(coords)}",
    )


def test_coordinate_identifier_pattern() -> None:
    coords = ecf.enumerate_coordinates()
    bad = [c["identifier"] for c in coords if not ecf.IDENTIFIER_PATTERN.match(c["identifier"])]
    check(
        not bad,
        f"identifiers not matching the canonical pattern: {bad}",
    )


def test_coordinate_identifier_matches_domain_and_stage() -> None:
    coords = ecf.enumerate_coordinates()
    for c in coords:
        expected = ecf.coordinate_identifier(c["domain"], c["stage"])
        check(
            c["identifier"] == expected,
            f"coordinate {c!r} identifier {c['identifier']!r} != expected {expected!r}",
        )
        check(
            c["label"] == ecf.coordinate_label(c["domain"], c["stage"]),
            f"coordinate {c!r} label {c['label']!r} != expected",
        )


def test_no_cell_filling_rule() -> None:
    """The specification must NOT impose a population requirement.

    A coordinate establishes a context. The conformance suite does not
    require any catalog to map every coordinate to an entry.
    """
    check(
        ecf.COORDINATE_COUNT == 49,
        "coordinate count is not 49; cell-filling rule would be ambiguous",
    )
    # No `required_population` knob is allowed on the enumeration.
    check(
        not hasattr(ecf, "required_population"),
        "ecf_coordinates exposes required_population; this contradicts the no-cell-filling rule",
    )


def test_validator_accepts_canonical_coordinate() -> None:
    payload = {"domain": "OperationsAndDelivery", "stage": "Operate"}
    ok, msg = ecf.validate_coordinate(payload)
    check(ok, f"validator rejected canonical coordinate: {msg}")


def test_validator_accepts_coordinate_with_identifier() -> None:
    payload = {
        "domain": "OperationsAndDelivery",
        "stage": "Operate",
        "identifier": "ecf:operationsAndDelivery.operate",
    }
    ok, msg = ecf.validate_coordinate(payload)
    check(ok, f"validator rejected coordinate with identifier: {msg}")


def test_validator_rejects_unknown_domain() -> None:
    payload = {"domain": "StrategyAndGovernance", "stage": "Operate"}
    ok, msg = ecf.validate_coordinate(payload)
    check(not ok, "validator accepted unknown domain")
    check(
        "domain" in msg.lower(),
        f"validator error should mention 'domain'; got: {msg!r}",
    )


def test_validator_rejects_unknown_stage() -> None:
    payload = {"domain": "OperationsAndDelivery", "stage": "Maintain"}
    ok, msg = ecf.validate_coordinate(payload)
    check(not ok, "validator accepted unknown stage")
    check(
        "stage" in msg.lower(),
        f"validator error should mention 'stage'; got: {msg!r}",
    )


def test_validator_rejects_identifier_mismatch() -> None:
    payload = {
        "domain": "OperationsAndDelivery",
        "stage": "Operate",
        "identifier": "ecf:operationsAndDelivery.build",
    }
    ok, msg = ecf.validate_coordinate(payload)
    check(not ok, "validator accepted mismatched identifier")


def test_validator_rejects_malformed_identifier() -> None:
    payload = {
        "domain": "OperationsAndDelivery",
        "stage": "Operate",
        "identifier": "OPERATIONS-DELIVERY/operate",
    }
    ok, msg = ecf.validate_coordinate(payload)
    check(not ok, "validator accepted malformed identifier")


def test_repository_coordinate_payloads_validate() -> None:
    """Any JSON object in the repo carrying `domain`+`stage` must validate.

    The enumeration tool enumerates the canonical set; this check covers
    the rest of the repository. It is intentionally broad so that future
    authored artefacts are caught by the conformance suite.
    """
    schemas_dir = REPO_ROOT / "schemas"
    framework_dir = REPO_ROOT / "framework"
    bad: list[str] = []
    for candidate in (schemas_dir, framework_dir):
        if not candidate.exists():
            continue
        for path, payload in ecf.find_coordinate_payloads(candidate):
            ok, msg = ecf.validate_coordinate(payload)
            if not ok:
                bad.append(f"{path}: {msg}")
    check(not bad, f"repository coordinate payloads failed validation: {bad}")


def run() -> int:
    """Run all `test_*` functions in this module. Return 0 on success, 1 on failure."""
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    for name, fn in tests:
        fn()
    if FAILURES:
        print(f"FAIL: {len(FAILURES)} conformance failure(s):")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print(f"OK: {len(tests)} conformance test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
