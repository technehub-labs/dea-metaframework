# CR-ECF-CG-001 — ECF Conformance Gate Definition

| Field | Value |
|-------|-------|
| **CR** | CR-ECF-CG-001 |
| **Title** | ECF Conformance Gate Definition |
| **Status** | Proposed |
| **Type** | Governance / Conformance |
| **Scope** | OpenDEA repositories consuming the Enterprise Concept Framework |
| **Depends On** | CR-ECF-001, CR-ECF-002, CR-ECF-003, CR-ECF-004, CR-ECF-005 |
**Author**: Coder (for eaojnr)
| **Date** | 2026-09-01 |

## 1. Purpose

Establish the formal ECF Conformance Gate used to determine whether an OpenDEA repository correctly consumes and implements the established ECF contract.

The gate shall validate semantic, structural, terminological, identifier, schema and cross-repository conformance.

## 2. Governing Principle

CR-ECF-001 through CR-ECF-005 are established.

No downstream repository may reinterpret, weaken, extend, or locally redefine the ECF contract.

A downstream repository may specialize ECF semantics for its own domain, but such specialization shall remain explicitly distinguishable from the ECF itself.

## 3. Conformance Layers

Conformance shall be assessed at five levels:

L1: Semantic Conformance
L2: Structural Conformance
L3: Representation Conformance
L4: Referential Conformance
L5: Behavioral / Validation Conformance

### L1: Semantic Conformance

Verify that the repository correctly distinguishes:

Domain
Stage
Coordinate
Context
Concept
Identity

and does not treat an ECF Coordinate as an entity container or entity identity.

### L2: Structural Conformance

Verify that repository models preserve:

Domain × Stage = ECF Coordinate
7 × 7 = 49 coordinates

without imposing a requirement for 49 catalog entries.

### L3: Representation Conformance

Verify that ECF references use the canonical machine-readable representation and identifiers defined by CR-ECF-005.

### L4: Referential Conformance

Verify that references to ECF Domains, Stages and Coordinates resolve to canonical definitions rather than repository-local duplicates.

### L5: Behavioral / Validation Conformance

Verify that invalid ECF references are rejected and valid references are accepted consistently.

## 4. Conformance States

Each consuming repository shall have one of:

CONFORMANT
CONFORMANT-WITH-EXTENSION
NON-CONFORMANT
NOT-YET-ASSESSED

CONFORMANT-WITH-EXTENSION requires documented specialization that does not redefine ECF semantics.

## 5. Gate Conditions

A repository passes the ECF Conformance Gate only when:

- all mandatory ECF semantic rules pass;
- all canonical Domain values resolve;
- all canonical Stage values resolve;
- all ECF Coordinates resolve;
- no prohibited local ECF definitions remain;
- schemas validate;
- cross-repository identifiers resolve;
- repository-specific extensions are explicitly classified;
- documentation agrees with implementation.

## 6. Evidence

A conformance assessment shall produce machine-readable and human-readable evidence.

Minimum evidence:

conformance-report
validation-results
canonical-reference-results
schema-results
terminology-results
extension-register

## 7. Gate Principle

A repository that fails the gate shall not be represented as ECF-conformant merely because its conceptual intent is aligned.

Conformance requires implementation evidence.

## 8. Acceptance Criteria

- [ ] Gate dimensions are defined.
- [ ] Conformance states are defined.
- [ ] Mandatory versus extension behavior is defined.
- [ ] Evidence requirements are defined.
- [ ] Pass/fail criteria are defined.
- [ ] Gate is applicable to all ECF-consuming repositories.

## 9. Definition of Done (this proposal PR)

Two files: this CR (verbatim against the source attachment) and the change-requests index row. Implementation PRs (CG-002..006) follow on subsequent acceptance.

## 10. References

CR-ECF-001..005 (all in this repository); `dea-metamodel` (formal OpenDEA semantics); `dea-catalog-business-capabilities` (capability instances); `dea-catalog-processes` (process instances).