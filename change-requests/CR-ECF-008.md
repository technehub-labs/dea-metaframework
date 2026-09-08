# CR-ECF-008: Rename Domain 6 from "Operations & Enablement" to "Enablement & Operations"

**Status**: Accepted
**Layer**: ECF (Enterprise Concept Framework) — dea-metaframework
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-ECF-006 (Domain enum v2.3.0); CR-ECF-007 (Domain 3 rename to Agency & Organization)
**Related**: ADR-ECF-001 (domain restructure policy); ADR-ECF-002 (Domain 3 rename); ADR-ECF-003 (this CR's decision record)

## Editorial note (Coder, 2026-09-08)

Two typos in the original CR text are corrected for the implementation:
1. §3 Proposed Definition uses "Enablement & Operate" — this is a slip; the correct name is "Enablement & Operations" (`Operate` is reserved for Stage 5 and never used in the Domain name).
2. §20 Normative Domain Record's `canonical_identifier: "enablement_and_operate"` is inconsistent with §17's recommendation `enablement_and_operations`. The latter is correct; the canonical_identifier is `enablement_and_operations`. The PascalCase enum value is `EnablementAndOperations`. The kebab-case form is `enablement-operations`. The lowerCamelCase form is `enablementAndOperations`. The display form is `Enablement & Operations`. All four are the canonical identifier for Domain 6 across its surface forms.

## 1. Executive Decision

Change Domain 6:

`Operations & Enablement` → `Enablement & Operations`

This is a semantic and terminological refinement, not a change to the ECF structure.

The following remain unchanged:

- Domain number: 6
- Matrix position: Row 6
- Semantic anchor: Execution
- Axiomatic grounding
- Domain scope
- Lifecycle applicability
- Seven-Domain partition
- Seven lifecycle Stages
- Stage 5: Operate
- ECF construction: Domain × Stage = 49 coordinates

The purpose of the rename is to make the distinction between the Domain and the Operate lifecycle Stage explicit and durable.

## 2. Problem

The ECF currently contains:

- Domain 6: Operations & Enablement
- Stage 5: Operate

The existing name is semantically defensible, but creates an avoidable lexical collision between the Domain axis and Lifecycle axis.

Because the ECF is explicitly constructed as:

`ECF = Domain × Stage`

the two constructs must remain orthogonal.

The Domain describes a persistent enterprise concern/capability dimension.

The Stage describes a lifecycle position through which a concept progresses.

Therefore:

`Operations & Enablement ≠ Operate`

The current terminology makes this distinction less obvious than it should be.

## 3. Proposed Definition

### Canonical Definition

**Enablement & Operations** is the domain that establishes, sustains, and governs the means and mechanisms through which the enterprise executes, delivers, and maintains its capabilities and value exchanges. It encompasses the operational processes, enabling technology, physical and virtual infrastructure, service mechanisms, and operational controls required to make enterprise execution possible and sustainable.

### Short Definition

The domain that enables and sustains enterprise execution through the processes, mechanisms, technology, infrastructure, and operational means required to deliver and maintain outcomes.

### Fundamental Question

*How does the enterprise enable and sustain execution?*

## 4. Axiomatic Grounding

The grounding axiom is:

*An enterprise is any bounded entity that persists by exchanging value with its environment.*

Domain 6 is derived from two complementary elements:

- **"persists"** — Persistence requires a mechanism through which the enterprise can continue to function.
- **"exchanging value"** — Value exchange requires mechanisms through which propositions are transformed into and delivered as outcomes.

Therefore:

*Enablement & Operations represents the mechanisms and means through which enterprise execution is made possible and sustained.*

This preserves the existing axiomatic logic rather than introducing a new conceptual basis.

## 5. Semantic Anchor

The Domain's semantic anchor remains:

**Execution**

This is important.

The Domain is not anchored on:

- Operations as an organizational department;
- operational management as a discipline;
- the lifecycle Stage "Operate";
- technology;
- infrastructure;
- processes alone.

Those are manifestations or constituents of the broader semantic subject:

**Enterprise execution and the means that enable and sustain it.**

## 6. Normative Domain/Stage Distinction

This CR establishes the following normative rule:

> Domain 6, Enablement & Operations, is a persistent semantic domain concerned with enabling and sustaining enterprise execution. Stage 5, Operate, is a lifecycle stage describing the context in which a particular enterprise concept is actively run, delivered, monitored, maintained, or otherwise operated.

Consequently:

```
ENABLEMENT & OPERATIONS
        │
        │ Domain
        │
        ├── × Conceive
        ├── × Design
        ├── × Build
        ├── × Activate
        ├── × OPERATE
        ├── × Improve
        └── × Retire
```

The Domain therefore exists across the lifecycle.

The Operate Stage is merely one intersection:

`Enablement & Operations × Operate`

## 7. Boundary with the Operate Stage

The distinction must be expressed semantically rather than merely linguistically.

**Enablement & Operations** asks: *What enables and sustains enterprise execution?*

**Operate** asks: *Where is the concept in its lifecycle?*

Therefore:

| Construct | Axis | Meaning |
|---|---|---|
| Enablement & Operations | Domain | Persistent enterprise execution/enablement concern |
| Operate | Stage | Lifecycle context in which something is being run/delivered/maintained |
| Enablement & Operations × Operate | Coordinate | Operational execution of the relevant concept within its lifecycle |

This is the critical reconciliation.

## 8. Domain 6 Scope

### Included

- operational process execution;
- fulfillment and delivery mechanisms;
- service operation and management;
- technology enablement;
- digital platforms;
- physical infrastructure;
- operational capacity;
- readiness;
- monitoring;
- maintenance;
- reliability;
- resilience;
- continuity;
- operational controls;
- mechanisms transforming propositions into delivered outcomes.

### Excluded

| Concern | Domain |
|---|---|
| Constitutional authority | Governance & Existence |
| Strategic trajectory | Strategy & Direction |
| Agents and organizational structure | Agency & Organization |
| External parties and relationships | Party & Relationship |
| Value-bearing proposition | Product & Value |
| Monetary reality | Finance & Accounting |
| Lifecycle progression | Stage axis |

## 9. Internal MECE Partition

The existing Domain 6 decomposition should be retained but normalized under the new name:

| Sub-concern | Scope |
|---|---|
| Process & Execution | Operational processes and execution mechanisms |
| Fulfillment & Delivery | Transformation of propositions into delivered outcomes |
| Technology Enablement | Digital systems, platforms and technology mechanisms |
| Physical Enablement | Facilities, equipment and physical infrastructure |
| Operational Planning & Capacity | Demand, capacity, scheduling and readiness |
| Operational Assurance & Resilience | Monitoring, reliability, continuity, maintenance and assurance |

No new conceptual subdivision is introduced by this CR.

## 10. Lifecycle Applicability

Domain 6 remains lifecycle-complete:

| Stage | Domain 6 interpretation |
|---|---|
| Conceive | Identify operational demand, constraints and required enabling mechanisms |
| Design | Design processes, service mechanisms, technology and infrastructure |
| Build | Provision, configure and construct operational means |
| Activate | Integrate, cut over and verify operational readiness |
| Operate | Run, deliver, monitor and maintain |
| Improve | Analyze performance, resolve incidents and optimize |
| Retire | Decommission, recover, migrate and close operational means |

This is evidence that the Domain is not equivalent to Stage 5.

## 11. Canonical Matrix Changes

The current Domain 6 entry:

`Operations & Enablement`

becomes:

`Enablement & Operations`

The Domain 6 matrix row becomes:

| **Enablement & Operations** |
|---|
| Demand planning |
| Process design |
| Provisioning |
| Cut-over |
| Run & maintain |
| Quality & incident |
| Decommission |

The cell semantics themselves do not change.

Stage 5 remains:

`Operate`

## 12. Axiom Documentation

`framework/axiom.md` must change the Domain 6 derivations to:

| Axiom fragment | → | Domain | Rationale |
|---|---|---|---|
| "persists" (substrate as enabler) | → | Enablement & Operations | Persistence requires a mechanism; the means that make sustained execution possible. |
| "exchanging value" (mechanism) | → | Enablement & Operations | Exchange requires a mechanism; the transformation of offerings into delivered outcomes. |

This retains the existing dual grounding.

## 13. Domain Grounding Documentation

`framework/domain-grounding.md` must change the compound-domain audit from:

`Operations + Enablement`

to:

`Enablement + Operations`

with the following normative rationale:

> Enablement + Operations is semantically necessary because enterprise execution requires both the means that make execution possible and the sustained operation through which those means produce and maintain outcomes. The Domain is distinct from the ECF Operate lifecycle Stage, which represents temporal lifecycle context rather than a semantic domain.

The Domain 6 grounding record must explicitly include:

> The term "Operations" in the Domain name denotes sustained enterprise day-to-day and ongoing activities as a persistent capability concern; it does not identify or absorb the ECF Operate lifecycle Stage.

## 14. Architecture Rule

The architecture documentation should reinforce:

```
ECF
│
├── Domain Axis
│      └── Enablement & Operations
│
└── Stage Axis
       └── Operate
```

The relationship is:

`Domain × Stage`

not:

`Domain → Stage`

and not:

`Domain = Stage`

This is consistent with the existing ECF architectural position, which defines ECF coordinates explicitly as Domain × Stage and states that ECF organizes and contextualizes while the metamodel formally represents those constructs.

## 15. Repository-Wide Changes

The following artifacts require update.

### `README.md`

Replace Domain 6 references:

`Operations & Enablement`

with:

`Enablement & Operations`

Update the axiomatic narrative and Domain table.

### `REPORT.md`

Update all Domain 6 terminology and definitions.

Where the text refers to the lifecycle Stage, retain:

`Operate`

and do not replace those occurrences indiscriminately.

### `framework/axiom.md`

Update Domain 6 axiomatic derivation.

### `framework/domain-grounding.md`

Update:

- compound audit;
- Domain 6 grounding record;
- boundary rules;
- adjacent-domain references;
- rationale;
- terminology.

### `framework/matrix.md`

Update:

- Domain table;
- Domain 6 matrix row;
- Domain subdomain table;
- cross-domain relationships;
- Domain 6 examples.

### `specification/`

Update canonical Domain 6 definitions, enumerations, examples and coordinate specifications.

### `schemas/`

Update:

- Domain enumerations;
- examples;
- fixtures;
- descriptions;
- validation data.

The Stage 5 value `Operate` must remain unchanged.

### `pages/`

Update:

- matrix display;
- filters;
- tooltips;
- legends;
- search/index data;
- Domain descriptions.

### `docs/terminology/`

Add an explicit distinction:

```
Enablement & Operations = ECF Domain 6
Operate                 = ECF Stage 5
```

## 16. Downstream Impact

The downstream impact must be audited across:

| Consumer | Required action |
|---|---|
| `dea-metamodel` | Update ECF Domain 6 profile label, definition and mappings |
| `dea-concepts-model` | Update terminology registry and ECF Domain enumeration |
| `dea-catalog-business-capabilities` | Update Domain 6 coordinate references without changing capability identity |
| `dea-catalog-processes` | Update Process Context coordinate references without changing process identity |
| `dea-architecture-framework` | Update ECF Domain references and matrix documentation |
| Other `dea-catalog-*` repositories | Search and update governed coordinate references |

This is especially important because the ECF architecture defines coordinates as classification context, not entity identity.

## 17. Backward Compatibility

The former name should become a deprecated alias:

```yaml
deprecated_aliases:
  - "Operations & Enablement"
```

Recommended canonical identifier for new machine-readable artifacts:

```
enablement_and_operations
```

However, existing stable machine identifiers should not be changed merely because the display name changes.

Where backward compatibility requires it:

```
operations_and_enablement
        ↓
enablement_and_operations
```

must resolve to the same:

`Domain 6`

No second Domain may be created.

## 18. Non-Goals

This CR does not:

1. add a Domain;
2. remove a Domain;
3. change Domain ordering;
4. change the 7×7 construction;
5. change the semantic anchor;
6. change the axiom;
7. change the lifecycle;
8. rename Stage 5;
9. create an operational entity in the metamodel;
10. redefine ECF coordinates as capabilities or processes.

## 19. Acceptance Criteria

### Semantic

- [ ] Domain 6 is named Enablement & Operations.
- [ ] Domain 6 remains grounded in the axiom.
- [ ] Semantic anchor remains Execution.
- [ ] Domain 6 remains lifecycle-complete.
- [ ] Domain 6 remains technology-independent.
- [ ] Seven Domains remain collectively exhaustive.

### Orthogonality

- [ ] Enablement & Operations is explicitly defined as a Domain.
- [ ] Operate is explicitly defined as Stage 5.
- [ ] The two are never treated as synonyms.
- [ ] All 49 Domain × Stage coordinates remain valid.

### Documentation

- [ ] `framework/axiom.md`
- [ ] `framework/domain-grounding.md`
- [ ] `framework/matrix.md`
- [ ] `framework/architecture.md`
- [ ] `REPORT.md`
- [ ] `README.md`
- [ ] `specification/`
- [ ] `schemas/`
- [ ] `docs/terminology/`
- [ ] `pages/`

are updated.

### Downstream

- [ ] `dea-metamodel` impact identified and governed.
- [ ] `dea-concepts-model` aligned.
- [ ] ECF-consuming catalogs audited.
- [ ] Capability identities unchanged.
- [ ] Process identities unchanged.

### Compatibility

- [ ] Former name retained as deprecated alias where required.
- [ ] Existing stable machine identifiers preserved where appropriate.
- [ ] No duplicate Domain 6 introduced.

## 20. Normative Domain Record

```yaml
id: 6
name: "Enablement & Operations"
semantic_anchor: "Execution"
axiomatic_grounding:
  - "persists"
  - "exchanging value"
fundamental_question: "How does the enterprise enable and sustain execution?"
definition: >-
  Enablement & Operations is the domain that establishes, sustains, and governs
  the means and mechanisms through which the enterprise executes, delivers,
  and maintains its capabilities and value exchanges. It encompasses the
  operational processes, enabling technology, physical and virtual
  infrastructure, service mechanisms, and operational controls required to
  make enterprise execution possible and sustainable.
canonical_identifier: "enablement_and_operations"
pascal_case: "EnablementAndOperations"
lower_camel_case: "enablementAndOperations"
kebab_case: "enablement-operations"
deprecated_aliases:
  - "Operations & Enablement"
  - "OperationsAndEnablement"
  - "operationsAndEnablement"
  - "operations-enablement"
  - "operations_and_enablement"
```

**Normative distinction:**

`Enablement & Operations` is ECF Domain 6. `Operate` is ECF Stage 5. They are orthogonal constructs and must never be treated as synonyms, aliases, or parent/child representations of one another.

## 21. Expected Result

The resulting conceptual model should read:

```
                 ENTERPRISE AXIOM
                       │
                       ▼
              ┌─────────────────┐
              │      ECF        │
              │   Domain × Stage│
              └────────┬────────┘
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
      DOMAIN AXIS             STAGE AXIS
            │                     │
            ▼                     ▼
 Enablement & Operations        Operate
       Domain 6                 Stage 5
            │                     │
            └──────────┬──────────┘
                       ▼
        Enablement & Operations × Operate
                       │
                       ▼
          Sustained enterprise execution
```

---

*Status: Accepted. Decision requested and granted: Approve CR-ECF-008 as a Domain naming and semantic clarification, with no change to the ECF's underlying 7×7 metamodel. Implementation: metaframework v2.5.0 + downstream cascade (dea-metamodel, dea-catalog-processes, dea-catalog-business-capabilities, dea-architecture-framework).*