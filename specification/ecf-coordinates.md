# ECF Coordinate Specification

Status: Normative (CR-ECF-005, the ECF Conformance Gate)
Scope: the canonical machine-readable and normative specification for ECF Coordinates
Implementation lives alongside this specification: `schemas/ecf-domain.schema.json`,
`schemas/ecf-stage.schema.json`, `schemas/ecf-coordinate.schema.json`,
`tools/ecf_coordinates.py`, `.github/workflows/ci.yml`.

This is the conformance gate: no substantive ECF-dependent catalog
population proceeds until repositories conform to this specification
(per the tranche directive).

## 1. Formal Definition

Let

```
D = the set of seven ECF Domains
S = the set of seven ECF Stages
```

Then an ECF Coordinate is the ordered pair of one Domain and one Stage:

```
ECF Coordinate = D x S
```

and

```
|ECF Coordinates| = |D| x |S| = 7 x 7 = 49
```

Each coordinate carries a stable identifier. The identifier is defined by
the ordered pair `(domain, stage)`, not by any display label.

## 2. Canonical Representation

The logical representation is:

```
ecfCoordinate:
  domain: <ECF Domain>
  stage:  <ECF Stage>
```

A canonical identifier may be represented as:

```
ecf:<domain-identifier>.<stage-identifier>
```

where `<domain-identifier>` and `<stage-identifier>` use the
`lowerCamelCase` short labels defined below. The identifier is checked
against the OpenDEA semantic-ID conventions in `dea-metamodel` before this
representation is finalised; the present form is the working contract and
will be updated if the metamodel convention differs (the conformance suite
documents the check).

## 3. Coordinate Identity

A coordinate is identified by its ordered pair `(Domain, Stage)`. The
display label is presentation; it is not the semantic identity. Two
representations that resolve to the same ordered pair refer to the same
coordinate.

## 4. Domain Enumeration

| # | Domain (canonical) | Identifier (camelCase) | Display label |
|---|--------------------|-------------------------|---------------|
| 1 | GovernanceAndExistence | governanceAndExistence | Governance & Existence |
| 2 | SupplyAndResources | supplyAndResources | Supply & Resources |
| 3 | PeopleAndOrganization | peopleAndOrganization | People & Organization |
| 4 | CustomerAndDemand | customerAndDemand | Customer & Demand |
| 5 | ProductAndOffering | productAndOffering | Product & Offering |
| 6 | OperationsAndDelivery | operationsAndDelivery | Operations & Delivery |
| 7 | FinanceAndValue | financeAndValue | Finance & Value |

The `canonical` value is the value carried in the `domain` field of a
Coordinate. The `identifier` is the camelCase form used in the
`ecf:<domain>.<stage>` coordinate identifier. The `display` label is the
human-readable form.

## 5. Stage Enumeration

| # | Stage (canonical) | Identifier (camelCase) | Display label |
|---|-------------------|-------------------------|---------------|
| 1 | Conceive | conceive | Conceive |
| 2 | Design | design | Design |
| 3 | Build | build | Build |
| 4 | Activate | activate | Activate |
| 5 | Operate | operate | Operate |
| 6 | Improve | improve | Improve |
| 7 | Retire | retire | Retire |

## 6. Coordinate Metadata

Every coordinate carries the following metadata. The minimum required set
is in §6.1; the extended set is in §6.2.

### 6.1 Required metadata

| Field | Type | Meaning |
|-------|------|---------|
| `identifier` | string | Stable coordinate identifier of the form `ecf:<domain>.<stage>` |
| `domain` | string | Domain canonical value (one of §4) |
| `stage` | string | Stage canonical value (one of §5) |
| `label` | string | Human-readable label of the form `<Domain Display> x <Stage Display>` |
| `version` | string | ECF specification version that defines the coordinate |

### 6.2 Recommended metadata

| Field | Type | Meaning |
|-------|------|---------|
| `definition` | string | Short definition of the work performed in this coordinate |
| `scope` | string | Scope note (typically empty; included for future expansion) |
| `includedConcerns` | array of string | Concerns within scope of the coordinate |
| `excludedConcerns` | array of string | Concerns explicitly out of scope |
| `adjacentCoordinates` | array of string | Identifiers of related coordinates and the nature of adjacency |
| `rationale` | string | Why this coordinate is distinct; grounding evidence |
| `lifecycleStatus` | string | One of `proposed`, `accepted`, `deprecated` |

## 7. Coordinate Set

All 49 coordinates are derivable from §4 and §5. The full set is enumerated
in `tools/ecf_coordinates.py::enumerate_coordinates()` and is generated
by the conformance suite. Every coordinate has a stable identifier; no
two coordinates share an identifier.

## 8. Contextual Use

An ECF Coordinate may be referenced by any governed OpenDEA construct:

- Capability
- Process Context
- Architecture Context
- Catalog Entry
- Assessment Context
- Scenario
- Other governed OpenDEA constructs

The consuming model defines the semantics of the reference. A coordinate
is a context; the consuming model determines whether zero, one, or many
modeled elements are appropriate within that context.

## 9. Multiple Coordinates

A modeled construct may reference more than one coordinate:

```
ecf:
  coordinates:
    - domain: customerAndDemand
      stage:  activate
    - domain: operationsAndDelivery
      stage:  operate
```

The existence of multiple coordinates does not imply multiple identities
of the modeled construct. Multi-coordinate participation is supported where
governed by the consuming catalog.

## 10. Validation

The ECF specification validates:

- `domain` is one of the seven canonical Domain values
- `stage` is one of the seven canonical Stage values
- `Coordinate = Domain x Stage` is the only valid form of a coordinate
- the canonical `identifier` matches `ecf:<domain-identifier>.<stage-identifier>`
- all 49 coordinates are derivable from §4 and §5

Invalid combinations fail validation. The conformance suite in
`tests/conformance/` enforces these rules.

## 11. No Cell-Filling Rule

This specification explicitly prohibits the interpretation:

```
49 Coordinates
        |
        v
49 required catalog entries
```

A coordinate establishes a context. A consuming catalog determines whether
zero, one, or many modeled elements are appropriate within that context.
The ECF does not impose a population requirement.

## 12. Conformance

An ECF-aware repository conforms to this specification by:

1. Using canonical Domain values (§4)
2. Using canonical Stage values (§5)
3. Using canonical coordinate identity (the ordered pair; the
   `ecf:<domain>.<stage>` form when an identifier is required)
4. Preserving coordinate semantics (a coordinate is a context, not an
   identity)
5. Not redefining ECF Domains or Stages locally
6. Not treating coordinates as entity identities
7. Declaring extensions through governed OpenDEA mechanisms

The conformance suite in `tests/conformance/test_005_coordinate_spec.py`
enforces conformance for the `dea-metaframework` repository. Downstream
repositories declare conformance via their own suites; CR-MM-ECF-01,
CR-BC-ECF-01, and CR-BP-ECF-01 (the post-gate downstream reconciliation
CRs) are the carriers of that declaration.

## 13. Authority

This specification is the normative authority for the ECF Coordinate
contract within `technehub-labs/dea-metaframework`. The
`dea-metamodel` repository owns the formal semantic representation
(ECF profile); this repository owns the coordinate contract.

## 14. Pre-existing schema artefacts

`schemas/entity.schema.json`, `schemas/capability.schema.json`, and
`schemas/traceability.schema.json` predate this specification and use
display-label enum values (for example `"Customer & Demand"`,
`"Deploy / Activate"`). They are retained for backward compatibility and
are explicitly out of scope for this CR; their reconciliation with the
canonical PascalCase enums of §4 and §5 is the responsibility of the
post-gate downstream CR-MM-ECF-01 in `technehub-labs/dea-metamodel`. The
new `schemas/ecf-domain.schema.json`, `schemas/ecf-stage.schema.json`,
and `schemas/ecf-coordinate.schema.json` are the canonical artefacts
under this specification.
