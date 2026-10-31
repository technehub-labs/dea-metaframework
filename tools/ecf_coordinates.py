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
    "StrategyAndDirection",
    "AgencyAndOrganization",
    "PartyAndRelationship",
    "ProductAndValue",
    "EnablementAndOperations",
    "FinanceAndAccounting",
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
    "StrategyAndDirection": "Strategy & Direction",
    "AgencyAndOrganization": "Agency & Organization",
    "PartyAndRelationship": "Party & Relationship",
    "ProductAndValue": "Product & Value",
    "EnablementAndOperations": "Enablement & Operations",
    "FinanceAndAccounting": "Finance & Accounting",
}

# Deprecated domain aliases (CR-ECF-007 §6.2; ADR-ECF-002 §6.3;
# CR-ECF-008 §17; ADR-ECF-003 §7).
# Domain 3 was renamed from "People & Organization" to
# "Agency & Organization" by CR-ECF-007. Domain 6 was renamed from
# "Operations & Enablement" to "Enablement & Operations" by CR-ECF-008.
# Consumers that have not yet migrated to the canonical identifier SHOULD
# resolve the alias and use the canonical value. Maintained for at least
# 2 release cycles.
DOMAIN_ALIASES: dict[str, str] = {
    "PeopleAndOrganization": "AgencyAndOrganization",
    "peopleAndOrganization": "AgencyAndOrganization",
    "people-organization": "AgencyAndOrganization",
    "People & Organization": "AgencyAndOrganization",
    "people": "AgencyAndOrganization",
    "OperationsAndEnablement": "EnablementAndOperations",
    "operationsAndEnablement": "EnablementAndOperations",
    "operations-enablement": "EnablementAndOperations",
    "Operations & Enablement": "EnablementAndOperations",
    "operations_and_enablement": "EnablementAndOperations",
}


def resolve_domain_alias(value: str) -> str:
    """Resolve a deprecated domain alias to the canonical PascalCase value.

    Returns the value unchanged if it is already canonical or unknown.
    """
    if value in DOMAINS:
        return value
    return DOMAIN_ALIASES.get(value, value)

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


# Canonical coordinate-identifier map (CR-ECF-012): the And-stripped
# lowerCamel serialization, with EnablementAndOperations the one domain
# whose identifier keeps its connective (the historical reading
# "enablement operations" would be lost otherwise). This table IS the
# identifier convention; the generic camel_case() lowercasing it replaces
# produced And-kept forms (e.g. financeAndAccounting) that no catalog,
# gate, or metamodel script uses and that the metamodel's drift detector
# rejects. The dea-metamodel mirror test (test_035_ecf_identifier_mirror)
# asserts map equality for all 49 coordinates, so the two repos cannot
# drift apart silently again.
DOMAIN_ID: dict[str, str] = {
    "GovernanceAndExistence": "governanceExistence",
    "StrategyAndDirection": "strategyDirection",
    "AgencyAndOrganization": "agencyOrganization",
    "PartyAndRelationship": "partyRelationship",
    "ProductAndValue": "productValue",
    "EnablementAndOperations": "enablementAndOperations",
    "FinanceAndAccounting": "financeAccounting",
}

# Deprecated identifier forms resolve through resolve_domain_alias first;
# the deprecated PascalCase domains' identifier forms are carried here so
# an identifier built from a resolved-alias path still lands canonically.
DEPRECATED_DOMAIN_ID_ALIASES: dict[str, str] = {
    "operationsEnablement": "enablementAndOperations",
    "peopleAndOrganization": "agencyOrganization",
}

def coordinate_identifier(domain: str, stage: str) -> str:
    """Build the canonical coordinate identifier `ecf:<domain>.<stage>`.

    Both `domain` and `stage` must be canonical PascalCase values; the
    identifier comes from the DOMAIN_ID convention table (CR-ECF-012),
    not from generic camelization.
    """
    if domain not in DOMAINS:
        raise ValueError(f"unknown domain: {domain!r}")
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage!r}")
    # Stages are single-word: the identifier form is the lowercased stage.
    return f"ecf:{DOMAIN_ID[domain]}.{stage.lower()}"


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
