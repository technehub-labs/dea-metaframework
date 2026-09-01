CR-ECF-005 — ECF Coordinate Specification

This becomes the implementation gate.

CR-ECF-005 — ECF Coordinate Specification

Status: Proposed
Type: Normative Specification
Implements: CR-ECF-001 through CR-ECF-004
Depends On: CR-ECF-002, CR-ECF-003, CR-ECF-004

1. Change Request

Establish the canonical machine-readable and normative specification for ECF Coordinates.

2. Formal Definition

Let:

D = set of seven ECF Domains
S = set of seven ECF Stages

Then:

ECF Coordinate = D × S

and:

|ECF Coordinates| = 7 × 7 = 49

Each coordinate shall have a stable identifier.

3. Canonical Representation

The logical representation shall be:

ecfCoordinate:
  domain: <ECF Domain>
  stage: <ECF Stage>

A canonical identifier may be represented as:

ecf:<domain>.<stage>

The precise identifier syntax shall be finalized against the OpenDEA semantic-ID conventions.

4. Coordinate Identity

A coordinate is identified by its ordered pair:

(Domain, Stage)

The display label shall not itself constitute semantic identity.

This aligns with the OpenDEA metamodel’s established principle that normative entities and relationships carry stable identifiers rather than relying on display labels. (GitHub⁠)

5. Coordinate Metadata

Each coordinate shall be capable of carrying:

Identifier
Domain
Stage
Label
Definition
Scope
Included Concerns
Excluded Concerns
Adjacent Coordinates
Rationale
Version
Lifecycle Status

6. Contextual Use

An ECF Coordinate may be referenced by:

Capability
Process Context
Architecture Context
Catalog Entry
Assessment Context
Scenario
Other governed OpenDEA constructs

The consuming model determines the semantics of the reference.

7. Multiple Coordinates

A modeled construct may reference:

ecf:
  coordinates:
    - domain: ...
      stage: ...

where multiple contextual relationships are semantically legitimate.

The existence of multiple coordinates shall not imply multiple identities.

8. Validation

The ECF specification shall validate:

Domain ∈ Canonical Domains
Stage ∈ Canonical Stages
Coordinate = Domain × Stage

Invalid combinations shall fail validation.

9. No Cell Filling Rule

The specification shall explicitly prohibit the interpretation:

49 Coordinates
    ↓
49 required catalog entries

A coordinate establishes a context.

A consuming catalog determines whether zero, one or many modeled elements are appropriate within that context.

10. Conformance

An ECF-aware repository shall conform by:

1. using canonical Domain values;
2. using canonical Stage values;
3. using canonical coordinate identity;
4. preserving coordinate semantics;
5. not redefining ECF Domains or Stages locally;
6. not treating coordinates as entity identities;
7. declaring extensions through governed OpenDEA mechanisms.

11. Acceptance Criteria

* [ ]	Canonical Domain enumeration exists.
* [ ]	Canonical Stage enumeration exists.
* [ ]	All 49 coordinates are derivable.
* [ ]	Stable coordinate identifiers exist.
* [ ]	Machine-readable representation exists.
* [ ]	Validation exists.
* [ ]	Multiple contextual coordinates are supported.
* [ ]	Coordinate semantics are independent of consuming catalog semantics.
* [ ]	No 49-cell population requirement exists.
* [ ]	OpenDEA semantic-ID conventions are respected.
* [ ]	Conformance requirements are documented.
