"""ECF coordinate enumeration and validation.

Canonical authority: specification/ecf-coordinates.md (CR-ECF-005).
This module is the executable form of the specification. The conformance
suite imports `enumerate_coordinates()` and `validate_coordinate()`; the
CI workflow runs the suite.

Convention: zero third-party dependencies. The module imports only from
the standard library so it works in the bare CI image.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

DOMAINS: tuple[str, ...] = (
    "GovernanceAndExistence",
    "SupplyAndResources",
    "PeopleAndOrganization",
    "CustomerAndDemand",
    "ProductAndOffering",
    "OperationsAndDelivery",
    "FinanceAndValue",
)

STAGES: tuple[str, ...] = (
    "Conceive",
    "Design",
    "Build",
    "Activate",
    "Operate",
    "Improve",
    "Retire",
)

DOMAIN_DISPLAY: dict[str, str] = {
    "GovernanceAndExistence": "Governance & Existence",
    "SupplyAndResources": "Supply & Resources",
    "PeopleAndOrganization": "People & Organization",
    "CustomerAndDemand": "Customer & Demand",
    "ProductAndOffering": "Product & Offering",
    "OperationsAndDelivery": "Operations & Delivery",
    "FinanceAndValue": "Finance & Value",
}

STAGE_DISPLAY: dict[str, str] = {
    "Conceive": "Conceive",
    "Design": "Design",
    "Build": "Build",
    "Activate": "Activate",
    "Operate": "Operate",
    "Improve": "Improve",
    "Retire": "Retire",
}

COORDINATE_COUNT: int = 7 * 7
IDENTIFIER_PATTERN = re.compile(r"^ecf:[a-z][a-zA-Z0-9]*\.[a-z][a-zA-Z0-9]*$")


def camel_case(value: str) -> str:
    """Convert a PascalCase identifier to lowerCamelCase."""
    if not value:
        return value
    return value[0].lower() + value[1:]


def coordinate_identifier(domain: str, stage: str) -> str:
    """Build the canonical coordinate identifier `ecf:<domain>.<stage>`.

    Both `domain` and `stage` must be canonical PascalCase values.
    """
    if domain not in DOMAINS:
        raise ValueError(f"unknown domain: {domain!r}")
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    return f"ecf:{camel_case(domain)}.{camel_case(stage)}"


def coordinate_label(domain: str, stage: str) -> str:
    """Build the human-readable coordinate label."""
    if domain not in DOMAIN_DISPLAY:
        raise ValueError(f"unknown domain: {domain!r}")
    if stage not in STAGE_DISPLAY:
        raise ValueError(f"unknown stage: {stage!r}")
    return f"{DOMAIN_DISPLAY[domain]} x {STAGE_DISPLAY[stage]}"


def enumerate_coordinates() -> list[dict[str, str]]:
    """Return the canonical list of 49 coordinates.

    Each entry contains `domain`, `stage`, `identifier`, and `label`.
    The list is in domain-major, then stage-minor order.
    """
    coords: list[dict[str, str]] = []
    for domain in DOMAINS:
        for stage in STAGES:
            coords.append(
                {
                    "domain": domain,
                    "stage": stage,
                    "identifier": coordinate_identifier(domain, stage),
                    "label": coordinate_label(domain, stage),
                }
            )
    return coords


def validate_coordinate(payload: dict) -> tuple[bool, str]:
    """Validate a coordinate payload against the canonical contract.

    Returns `(ok, message)`. `message` is empty on success and a
    human-readable reason on failure.
    """
    if not isinstance(payload, dict):
        return False, "coordinate must be an object"
    domain = payload.get("domain")
    stage = payload.get("stage")
    if domain not in DOMAINS:
        return False, f"domain {domain!r} is not in the canonical Domain set"
    if stage not in STAGES:
        return False, f"stage {stage!r} is not in the canonical Stage set"
    identifier = payload.get("identifier")
    if identifier is not None:
        if not isinstance(identifier, str):
            return False, "identifier must be a string when present"
        if not IDENTIFIER_PATTERN.match(identifier):
            return False, f"identifier {identifier!r} does not match pattern"
        expected = coordinate_identifier(domain, stage)
        if identifier != expected:
            return (
                False,
                f"identifier {identifier!r} does not match canonical {expected!r}",
            )
    label = payload.get("label")
    if label is not None and not isinstance(label, str):
        return False, "label must be a string when present"
    return True, ""


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_coordinate_payloads(root: Path) -> Iterable[tuple[Path, object]]:
    """Yield `(path, payload)` tuples for candidate coordinate payloads.

    A candidate payload is a JSON object that contains both `domain` and
    `stage` keys whose values are strings. This is intentionally liberal;
    the validator rejects anything outside the canonical contract.
    """
    for path in sorted(root.rglob("*.json")):
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("domain"), str) and isinstance(
            data.get("stage"), str
        ):
            yield path, data
