CR-ECF-002 — ECF Semantic Boundary

This is the most important corrective CR.

CR-ECF-002 — ECF Semantic Boundary

Status: Proposed
Type: Semantic Model
Implements: CR-ECF-001
Depends On: CR-ECF-001

1. Change Request

Define the semantic distinction between an ECF Domain, Stage, Coordinate, Context, and the enterprise concepts that may be contextualized by them.

2. Canonical Definitions

Domain

An ECF Domain is one of the seven canonical enterprise concern dimensions.

Stage

An ECF Stage is one of the seven canonical lifecycle dimensions.

Coordinate

An ECF Coordinate is the ordered pair:

Coordinate = Domain × Stage

It identifies an enterprise context within the ECF.

Context

A Context is the semantic interpretation of an ECF Coordinate for a particular modeling concern.

Examples include:

Process Context
Capability Context
Architecture Context
Assessment Context

The context may be specialized by the consuming model.

3. Fundamental Rule

An ECF Coordinate is not an entity container.

The following formulation is deprecated:

Object ∈ Cell

The canonical formulation shall be:

Enterprise Concept
        │
        │ contextualized by
        ▼
ECF Coordinate

An enterprise concept may legitimately participate in multiple ECF contexts.

4. Consequences

The following shall not be inferred:

49 cells
   ≠
49 capabilities
49 cells
   ≠
49 processes
49 cells
   ≠
49 entities

Instead:

ECF Coordinate
       │
       ▼
Context
       │
       ▼
Applicable catalog/model elements

5. Capability Boundary

A Business Capability has its own semantic identity and business meaning.

Its ECF coordinate provides classification context.

The existing Business Capability catalog already implements this principle and explicitly rejects treating the catalog as a 49-cell filling exercise. (GitHub⁠)

The ECF shall therefore remove or revise the current “capability belongs to the earliest stage” rule where it is presented as an intrinsic property of capability identity.

Primary and secondary ECF coordinates may be used where governed by the consuming catalog.

6. Process Boundary

A Process Context is a specialization of an ECF Coordinate for Business Process Architecture.

The current Process Catalog already establishes:

ECF Coordinate
      ↓
Process Context
      ↓
L0 Process Scope
      ↓
L1 Process Group
      ↓
L2 Business Process
      ↓
L3 Activity
      ↓
L4 Task

(GitHub⁠)

The ECF shall adopt this interpretation.

7. Recursion Boundary

ECF recursion shall mean that an ECF coordinate may be used as the organizing context for a further specialized model.

It shall not imply that every ECF cell must recursively contain another 7×7 matrix.

Likewise, ECF recursion shall not determine Business Process decomposition.

8. Deprecated Assertions

The following statements in the current ECF documentation shall be removed or rewritten:

“every object … lives in one of them”

and:

Cell = {
    objects: Entity[],
    caps: Capability[]
}

The current formal notation in REPORT Section 15 is therefore subject to replacement. (GitHub⁠)

9. Acceptance Criteria

* [ ]	Domain is formally defined.
* [ ]	Stage is formally defined.
* [ ]	Coordinate is formally defined.
* [ ]	Context is formally defined.
* [ ]	Coordinate is not treated as an entity container.
* [ ]	Multi-coordinate contextualization is supported where legitimate.
* [ ]	Capability identity is separated from coordinate.
* [ ]	Process Context is explicitly established.
* [ ]	ECF recursion is separated from process decomposition.
