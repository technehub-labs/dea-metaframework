# ADR-ECF-003: ECF Domain 6 Rename — Operations & Enablement → Enablement & Operations

| Field | Value |
| :--- | :--- |
| **Status** | Accepted |
| **Date** | 2026-09-08 |
| **Deciders** | TechNeHub Labs Architecture Board |
| **Technical Story** | CR-ECF-008: Domain 6 rename for Domain/Stage orthogonality |
| **Tags** | `ecf`, `domains`, `metaframework`, `lexical-collision`, `orthogonality`, `naming` |
| **Version** | v2.4.0 → v2.5.0 |

---

## 1. Research Question

> **Given that the Enterprise Concept Framework is constructed as `ECF = Domain × Stage` and requires the two axes to remain orthogonal, how should Domain 6 be named such that its lexical identity does not collide with Stage 5 (`Operate`), while preserving the axiomatic grounding, semantic anchor (`Execution`), and 7×7 matrix topology?**

---

## 2. Context and Problem Statement

### 2.1 The Current State

The ECF carries:

- **Domain 6**: `Operations & Enablement` (canonical PascalCase: `OperationsAndEnablement`)
- **Stage 5**: `Operate`

### 2.2 The Lexical Collision

The word *Operations* appears in the Domain 6 name, and the word *Operate* appears in the Stage 5 name. Both terms share the same Latin root (`operari`, "to work"), and the surface similarity causes readers — both human and machine — to conflate the two axes:

1. A downstream consumer reading "Operations & Enablement × Operate" cannot tell at a glance whether "Operate" is redundant with "Operations" (a tautology) or orthogonal to it (a Domain × Stage intersection).
2. Process Catalog L1 Process Group records use `process_context: dea:pc-oe-operate` (Domain 6 abbreviation `oe` + Stage 5). The `oe` abbreviation reads as "operations-enablement," which is not self-evidently distinct from "operate."
3. Cross-domain findings in the research register (CR-BP-11 §9) use "operations-enablement x operate" as a single token in narrative text; a reader cannot tell whether the domain or the stage is being referenced without parsing the id form.

The current name is **semantically defensible** (the Domain is grounded in the axiom and the scope is correct) but **lexically ambiguous** (the name collides with the Stage vocabulary).

### 2.3 The Architectural Invariant

The ECF architecture requires:

```
ECF
│
├── Domain Axis  (persistent enterprise concern; e.g., Domain 6)
│
└── Stage Axis   (lifecycle position; e.g., Stage 5 = Operate)

Relationship: Domain × Stage = 49 coordinates
NOT:          Domain → Stage  (directional)
NOT:          Domain = Stage  (collapsed)
```

When Domain 6's name shares its lexical root with Stage 5's name, the two axes are not obviously orthogonal. This is a **discoverability hazard** for consumers of the ECF (the metamodel, the catalogs, the architecture framework, downstream UI surfaces) and a **cognitive hazard** for human readers of the matrix.

---

## 3. The Decision

### 3.1 Rename Domain 6

```
Operations & Enablement  →  Enablement & Operations
```

The swap of the two nouns preserves both concepts (`Enablement` — the means that make execution possible; `Operations` — the sustained day-to-day activities) while putting `Enablement` first. The word `Operations` remains in the Domain name but is no longer the leading noun, which reduces the visual collision with the Stage 5 `Operate` cell.

### 3.2 What does NOT change

| Property | Value before | Value after |
|---|---|---|
| Domain number | 6 | 6 |
| Matrix position | Row 6 | Row 6 |
| Semantic anchor | Execution | Execution |
| Axiomatic grounding | "persists" + "exchanging value" | "persists" + "exchanging value" |
| Domain scope | Operational processes, technology enablement, physical/virtual infrastructure, service mechanisms, operational controls | **same** |
| Lifecycle applicability | All 7 stages | All 7 stages |
| Seven-Domain partition | MECE | MECE (unchanged) |
| Seven lifecycle Stages | Conceive/Design/Build/Activate/Operate/Improve/Retire | **same** |
| Stage 5 name | Operate | Operate |
| ECF construction | Domain × Stage = 49 coordinates | **same** |

### 3.3 What changes

| Surface | Before | After |
|---|---|---|
| Display form | Operations & Enablement | Enablement & Operations |
| PascalCase | OperationsAndEnablement | EnablementAndOperations |
| lowerCamelCase | operationsAndEnablement | enablementAndOperations |
| kebab-case | operations-enablement | enablement-operations |
| Canonical identifier (machine) | `operations_and_enablement` | `enablement_and_operations` |
| Domain abbreviation (catalog IDs) | `oe` (unchanged) | `oe` (unchanged) |

**Note on the abbreviation**: The catalog ID form `dea:pc-oe-*` uses the lowercase abbreviation `oe`. The abbreviation's two letters come from the first letters of the two nouns in the Domain name. After the rename, the letters are the same (`E` and `O`), so the abbreviation is preserved without change. This is deliberate: the abbreviation is a stable identifier, not a display label, and existing `dea:pc-oe-*` and `dea:group-*` records must NOT be re-keyed. CR-ECF-008 §17: "existing stable machine identifiers should not be changed merely because the display name changes."

### 3.4 Normative rule

This ADR establishes the following normative rule:

> **Domain 6, Enablement & Operations, is a persistent semantic domain concerned with enabling and sustaining enterprise execution. Stage 5, Operate, is a lifecycle stage describing the context in which a particular enterprise concept is actively run, delivered, monitored, maintained, or otherwise operated. The two constructs are orthogonal and must never be treated as synonyms, aliases, or parent/child representations of one another.**

---

## 4. Axiomatic Grounding

The grounding axiom is unchanged:

> *An enterprise is any bounded entity that persists by exchanging value with its environment.*

Domain 6 is derived from two complementary elements:

| Axiom fragment | Interpretation | Domain 6 reading |
|---|---|---|
| "persists" | Persistence requires a mechanism through which the enterprise can continue to function | Enablement: the substrate-as-enabler; the means that make sustained execution possible |
| "exchanging value" | Value exchange requires mechanisms through which propositions are transformed into and delivered as outcomes | Operations: the sustained operation; the transformation of offerings into delivered outcomes |

The rename preserves this dual grounding exactly. The two nouns in the Domain name map 1:1 to the two axiom fragments; only the order is changed.

---

## 5. The Lexical Collision Analysis

### 5.1 Before the rename

```
Domain 6: Operations & Enablement
             ↑         ↑
             │         │
             │         └─ the enabler noun
             └─────────── the executor noun (shares root with Stage 5 "Operate")

Stage 5: Operate
             ↑
             └─ the same root, used as a verb-form for a lifecycle position

Reader's mental model: "Operations & Enablement × Operate" reads as
"operations × operate" — a near-tautology that obscures the orthogonality.
```

### 5.2 After the rename

```
Domain 6: Enablement & Operations
             ↑         ↑
             │         │
             │         └─ the executor noun (still shares root, but no longer leads)
             └─────────── the enabler noun (now leads; distinct from any Stage name)

Stage 5: Operate
             ↑
             └─ unchanged

Reader's mental model: "Enablement & Operations × Operate" reads as
"enablement+operations × operate" — the leading noun (Enablement) is
lexically distinct from Operate; the trailing noun (Operations) reads as
"the sustained day-to-day thing that the Domain is about," not "the Stage."
```

The rename does not eliminate the shared Latin root between *Operations* and *Operate*; that root is intrinsic to the vocabulary. It reduces the visual prominence of the collision by moving `Operations` from the leading position to the trailing position, and it pairs the rename with an explicit normative rule (§3.4) that the two constructs are orthogonal.

### 5.3 Why not a stronger rename?

Several alternative names were considered and rejected:

| Alternative | Why rejected |
|---|---|
| `Execution & Enablement` | `Execution` is the Domain's semantic anchor, not a noun; using the anchor as the name would invert the pattern used by the other six Domains (whose names are subjects, not anchors). |
| `Delivery & Enablement` | `Delivery` is narrower than `Operations`; it does not cover monitoring, maintenance, resilience, or operational controls. |
| `Means & Execution` | Too abstract; not a recognizable enterprise-architecture term. |
| `Service Operations & Enablement` | `Service` is a subtype of the Domain's scope (services are one kind of deliverable); not all Domain 6 concerns are service-shaped. |
| `Operations & Infrastructure` | `Infrastructure` is narrower than `Enablement`; it does not cover digital platforms or operational processes. |

The rename `Operations & Enablement → Enablement & Operations` is the **minimum change** that reduces the lexical collision while preserving both nouns, both axiom fragments, the semantic anchor, and the 1:1 mapping with downstream artifacts that already use the abbreviation `oe`.

---

## 6. The Domain/Stage Distinction in Detail

### 6.1 The two axes answer different questions

| Axis | Question | Example |
|---|---|---|
| **Domain 6 (Enablement & Operations)** | *What enables and sustains enterprise execution?* | "Run the production line"; "Operate the data platform"; "Maintain the fleet." |
| **Stage 5 (Operate)** | *Where is the concept in its lifecycle?* | "The strategy is in the Operate stage"; "The product is in the Operate stage"; "The governance framework is in the Operate stage." |

### 6.2 The intersection

The coordinate `Enablement & Operations × Operate` is the cell where:

- The Domain is Enablement & Operations (the persistent concern)
- The Stage is Operate (the lifecycle position)

This is the cell that carries: "the sustained, day-to-day running of the means and mechanisms through which the enterprise executes." It is one of seven cells in the Domain 6 row. The other six cells are:

| Coordinate | Reading |
|---|---|
| Enablement & Operations × Conceive | Conceive the operational demand, constraints, and required enabling mechanisms |
| Enablement & Operations × Design | Design the processes, service mechanisms, technology, and infrastructure |
| Enablement & Operations × Build | Provision, configure, and construct the operational means |
| Enablement & Operations × Activate | Integrate, cut over, and verify operational readiness |
| **Enablement & Operations × Operate** | **Run, deliver, monitor, and maintain** (the Operate cell) |
| Enablement & Operations × Improve | Analyze performance, resolve incidents, and optimize |
| Enablement & Operations × Retire | Decommission, recover, migrate, and close operational means |

The Domain exists across the lifecycle. The Stage 5 Operate cell is one intersection among seven.

### 6.3 The "Domain ≠ Stage" invariant

The ECF architecture states (in `framework/architecture.md` and `specification/ecf-coordinates.md`):

```
ECF = Domain × Stage
```

This means:

- A Domain is a persistent semantic concern that exists at every lifecycle stage.
- A Stage is a lifecycle position that applies to every Domain.
- A Coordinate is the ordered pair `(Domain, Stage)`.
- No Domain is a Stage. No Stage is a Domain. The two axes are orthogonal by construction.

CR-ECF-008 §6 codifies this invariant as a normative rule specific to Domain 6 because the lexical collision was concentrated there. The rule generalizes to all seven Domains and all seven Stages.

---

## 7. The Migration Policy

### 7.1 Backward compatibility

The former name is retained as a **deprecated alias** in the canonical schema:

```yaml
deprecated_aliases:
  - "Operations & Enablement"
  - "OperationsAndEnablement"
  - "operationsAndEnablement"
  - "operations-enablement"
  - "operations_and_enablement"
```

The alias resolution function `resolve_domain_alias()` in `tools/ecf_coordinates.py` is extended to map each alias to `EnablementAndOperations`. The alias map is maintained for at least 2 release cycles (per the CR-ECF-007 precedent).

### 7.2 Machine identifier stability

The lowercase abbreviation `oe` used in catalog IDs (`dea:pc-oe-*`) is **unchanged**. The letters come from the two nouns' first letters, which are the same before and after the rename.

Existing catalog IDs (`dea:pc-oe-operate`, `dea:group-*` with `process_context: dea:pc-oe-operate`) are **not re-keyed**. The change is to the Domain's *display name* and *canonical PascalCase enum value*, not to the abbreviation or to existing IDs.

### 7.3 Coordinate identifier stability

The ECF coordinate identifier form is `ecf:<domain>.<stage>`, where `<domain>` is the lowerCamelCase form. Before the rename: `ecf:operationsAndEnablement.operate`. After the rename: `ecf:enablementAndOperations.operate`.

The identifier **does change** because the domain field carries the canonical PascalCase value. This is the same breaking-change pattern as CR-ECF-007 (Domain 3 identifier changed from `ecf:peopleAndOrganization.*` to `ecf:agencyAndOrganization.*`). The alias resolution function handles the migration for consumers that have not yet re-keyed.

---

## 8. Downstream Impact

### 8.1 Repositories that consume the ECF Domain enum

| Repository | Artifact | Change required |
|---|---|---|
| `dea-metamodel` | Domain profile label and definition in Core | Update to `EnablementAndOperations` |
| `dea-concepts-model` | Terminology registry | Update Domain 6 entry; add alias mapping |
| `dea-catalog-business-capabilities` | Capability records with `ecfConformance.canonicalReferences[].domain` | Update to `EnablementAndOperations`; no capability identity change |
| `dea-catalog-processes` | Process records with `ecfConformance.canonicalReferences[].domain`; Process Context records with `domain` field | Update to `EnablementAndOperations`; no process identity change |
| `dea-architecture-framework` | ECF Domain references and matrix documentation | Update references; add ADR-ECF-003 pointer |
| `technehub-labs.github.io` | Pages display | Update matrix-data.json, site.js, site.css |

### 8.2 What does NOT change downstream

- **Capability identities**: `dea:capability-*` ids are domain-agnostic; the rename does not change them.
- **Process identities**: `dea:process-*` and `dea:group-*` ids are domain-agnostic; the rename does not change them.
- **Process Context ids**: `dea:pc-oe-*` ids use the stable abbreviation; the rename does not change them.
- **Coordinate counts**: 49 coordinates remain 49 coordinates; the matrix topology is unchanged.
- **MECE partition**: Domain 6's scope, included/excluded lists, and internal subdivision are unchanged.

---

## 9. Compliance and Validation

### 9.1 The Semantic Integrity Contract (ADR-ECF-002 §6.4)

Domain 6 after the rename:

| Contract element | Value | Pass/Fail |
|---|---|---|
| Exactly one declared semantic anchor | `Execution` | ✅ |
| A stable enterprise subject (not a department, technology, or activity) | `Enablement & Operations` (the means and mechanisms of execution) | ✅ |
| Noun-based, semantically durable naming | Two nouns (`Enablement`, `Operations`) joined by `&` | ✅ |
| Independence from organizational departmentalization | No "Operations Department" implication | ✅ |
| Independence from technology substrate | `Enablement` covers technology, digital platforms, physical infrastructure | ✅ |
| Lifecycle completeness | Domain exists at all 7 stages (Conceive through Retire) | ✅ |
| Explicit inclusion/exclusion boundary rules | §8 of CR-ECF-008 (included: operational process execution, fulfillment/delivery, technology enablement, physical enablement, operational planning/capacity, operational assurance/resilience; excluded: governance, strategy, agency, party, product, finance, lifecycle) | ✅ |
| Cross-domain relationship declarations | Adjacent domains: ProductAndValue (value-bearing propositions become deliverables), FinanceAndAccounting (monetary reality of operations), AgencyAndOrganization (agents staff operations), PartyAndRelationship (suppliers and partners feed operations) | ✅ |
| Internal MECE partition into sub-concerns | Six sub-concerns (§9 of CR-ECF-008) | ✅ |
| No ownership of generic enterprise outcomes | Domain 6 owns *execution* (the means and mechanisms); *value* is owned by ProductAndValue and measured by FinanceAndAccounting | ✅ |

### 9.2 The Lexical Collision Test

| Test | Before | After |
|---|---|---|
| Domain name leads with a noun distinct from any Stage name | ❌ (`Operations` collides with `Operate`) | ✅ (`Enablement` is distinct from `Operate`) |
| Domain name contains a noun that shares a root with a Stage name | ⚠️ (`Operations` shares root with `Operate`) | ⚠️ (`Operations` still shares root with `Operate`, but no longer leads) |
| The Domain/Stage orthogonality is documented as a normative rule | ❌ (implicit) | ✅ (CR-ECF-008 §6; ADR-ECF-003 §6.3) |

### 9.3 The 49-cell matrix validation

All 49 coordinates remain valid after the rename. The coordinate identifiers change from `ecf:operationsAndEnablement.<stage>` to `ecf:enablementAndOperations.<stage>` for the 7 coordinates in the Domain 6 row. The alias resolution function maps the old identifiers to the new ones.

---

## 10. Consequences

### 10.1 Positive

| Consequence | Impact |
|---|---|
| Domain/Stage orthogonality is explicit | The normative rule (§6.3) is machine-testable and human-readable |
| Lexical collision reduced | `Enablement & Operations × Operate` reads as a Domain × Stage intersection, not a tautology |
| Backward compatibility preserved | Deprecated aliases map to the canonical value for at least 2 release cycles |
| No downstream re-keying | Catalog IDs (`dea:pc-oe-*`, `dea:group-*`, `dea:process-*`) are unchanged |
| Matrix topology preserved | 7×7 = 49 coordinates; no cells added, removed, or re-ordered |

### 10.2 Negative / Trade-offs

| Consequence | Impact | Mitigation |
|---|---|---|
| Coordinate identifiers change for Domain 6 row | `ecf:operationsAndEnablement.*` → `ecf:enablementAndOperations.*` | Alias resolution function maps old to new; consumers have 2 release cycles to re-key |
| PascalCase enum value changes | `OperationsAndEnablement` → `EnablementAndOperations` | Same as above; enum is the machine-readable form |
| Display name changes | `Operations & Enablement` → `Enablement & Operations` | Deprecated alias retained in schema and tools |
| Documentation must be updated across 5 repos | 19+ files in dea-metaframework alone | Phased cascade: metaframework first, then downstream |

### 10.3 Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Consumers continue to use the old name | Medium | Low | Alias resolution function; deprecated alias warning in CI |
| The word `Operations` still collides with `Operate` | Low | Low | The collision is reduced, not eliminated; the normative rule (§6.3) is the durable mitigation |
| The abbreviation `oe` is ambiguous | Low | Low | The abbreviation is stable; the letters are the same before and after |

---

## 11. Implementation Notes for the CR

The Change Request implementing this ADR should:

1. **Update the canonical schema** (`schemas/ecf-domain.schema.json`) to replace `OperationsAndEnablement` with `EnablementAndOperations` and add the deprecated aliases to the description.
2. **Update the tools** (`tools/ecf_coordinates.py`) to add the alias mapping and update the `DOMAINS` tuple and `DOMAIN_DISPLAY` dict.
3. **Update the framework documentation** (`framework/axiom.md`, `framework/domain-grounding.md`, `framework/matrix.md`, `framework/architecture.md`) to reflect the rename.
4. **Update the specification** (`specification/ecf-coordinates.md`) to update the Domain enumeration table.
5. **Update the README and REPORT** (`README.md`, `REPORT.md`) to reflect the rename.
6. **Update the pages** (`pages/assets/matrix-data.json`, `pages/assets/site.js`, `pages/assets/site.css`) to reflect the rename.
7. **Update the tests** (`tests/conformance/test_005_coordinate_spec.py`) to use the new canonical value.
8. **Update the CHANGELOG** (`CHANGELOG.md`) to record the v2.5.0 release.
9. **Add the CR and ADR** (`change-requests/CR-ECF-008.md`, `docs/adr/ADR-ECF-003.md`).
10. **Tag the release** as `v2.5.0`.
11. **Cascade to downstream repos** (dea-metamodel, dea-catalog-processes, dea-catalog-business-capabilities, dea-architecture-framework) in the same order as CR-ECF-006 and CR-ECF-007.

---

## 12. References

- **Axiom**: *"An enterprise is any bounded entity that persists by exchanging value with its environment."*
- **Repository**: `github.com/technehub-labs/dea-metaframework`
- **Related ADRs**: ADR-ECF-001 (ECF Initial Domain Definition); ADR-ECF-002 (Domain Semantic Integrity & Substrate Independence)
- **Related CRs**: CR-ECF-006 (Domain enum v2.3.0); CR-ECF-007 (Domain 3 rename to Agency & Organization)
- **Architectural Principles**: MECE, Semantic Anchoring, Technology Independence, Substrate Independence, Domain/Stage Orthogonality

---

*This ADR serves as the normative rationale for CR-ECF-008. All subsequent domain specifications, catalog mappings, and metamodel references MUST conform to the decisions recorded herein.*