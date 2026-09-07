# CR-ECF-007: Rename Domain 3 from "People & Organization" to "Agency & Organization"

---

## CR Metadata

| Field | Value |
| :--- | :--- |
| **CR ID** | CR-ECF-007 |
| **Title** | Rename ECF Domain 3: "People & Organization" → "Agency & Organization" |
| **Status** | Proposed |
| **Priority** | High |
| **Type** | Structural / Semantic |
| **Affected Layer** | ECF Metaframework (L0) |
| **Author** | TechNeHub Labs Architecture Board |
| **Reviewer** | — |
| **Approver** | — |
| **Created** | 2026-09-07 |
| **Target Completion** | — |
| **Governing ADR** | ADR-002: ECF Domain Semantic Integrity & Substrate Independence |
| **Related CRs** | CR-ECF-002 (Strategy & Direction introduction), CR-ECF-004 (Party & Relationship), CR-ECF-005 (Product & Value), CR-ECF-006 (Operations & Enablement), CR-ECF-008 (Finance & Accounting) |

---

## 1. Executive Summary

This Change Request implements the decision recorded in **ADR-002** to rename ECF Domain 3 from **"People & Organization"** to **"Agency & Organization"**. The change is driven by the requirement for **substrate independence**: the domain must remain semantically valid whether the enterprise's internal agents are biological (humans), artificial (AI agents), or hybrid. The term "People" is biologically loaded and fails the Technology Independence test; "Agency" is the architecturally precise, substrate-independent term for the capacity to act on behalf of the enterprise.

This CR covers:
- The updated domain specification (name, definition, anchor, scope, boundaries)
- All documentation changes across the `dea-metaframework`, `dea-metamodel`, and `dea-concepts-model` repositories
- Migration mapping for backward compatibility
- Impact analysis on downstream consumers
- Acceptance criteria

---

## 2. Rationale

### 2.1 The Problem

The current domain name **"People & Organization"** assumes that the agentive constituent of the enterprise is biological (human). This assumption:

1. **Fails the Technology Independence test** (ADR-002, Section 3.2, Test 4): The domain does not survive the substitution of human labor with AI agents without requiring a definitional caveat.
2. **Violates the Normative Principle** (ADR-002, Section 3.1): A domain name should identify a stable class of enterprise subject, not the current implementation. "People" is an implementation; "Agency" is the subject.
3. **Requires a definitional footnote** to accommodate AI agents, which signals an architectural deficiency. A metaframework should be substrate-independent *by default*, not *by exception*.

### 2.2 The Axiomatic Basis

The grounding axiom states:

> *"An enterprise is any bounded entity that **persists** by exchanging value with its environment."*

The derivation for Domain 3:

> *"persists" → Persistence requires **agents**: the entities that perform the work and the structure that organizes them.*

The axiom requires **agents**, not **humans**. The semantic quality that makes an entity a constituent of the enterprise is **agency** — the capacity to act. "People" is merely the current biological implementation of agency.

### 2.3 The Stress Test

ADR-002 (Section 5) stress-tested the domain against a **Digital Enterprise owned by an AI Agent, with a workforce consisting entirely of AI Agents**. The result:

| Aspect | "People & Organization" | "Agency & Organization" |
| :--- | :--- | :--- |
| Survives AI-only workforce? | ❌ Requires redefinition | ✅ Holds without modification |
| Axiomatically faithful? | ⚠️ Interpretation | ✅ Direct derivation |
| Requires definitional caveat? | Yes | No |
| Substrate-independent by default? | No | Yes |

### 2.4 The Naming Decision

Three candidates were evaluated in ADR-002 (Section 5.4):

| Candidate | Substrate-Independent? | Axiomatically Faithful? | Requires Caveat? | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| People & Organization | ❌ | ⚠️ | Yes | Rejected |
| Workforce & Organization | ✅ | ⚠️ Indirect | No | Viable but labor-focused |
| **Agency & Organization** | ✅ | ✅ Direct | No | **Selected** |

**"Agency & Organization"** was selected because:
- It directly names what the axiom requires (agents → agency)
- It is completely substrate-independent
- It captures both labor AND non-labor aspects of internal agents (authority, autonomy, initiative, coordination)
- It requires zero definitional caveats
- The pairing reads naturally: *the capacity to act (Agency) and the structure through which that capacity is coordinated (Organization)*

---

## 3. Scope of Change

### 3.1 What Changes

| Element | Before | After |
| :--- | :--- | :--- |
| Domain Name | People & Organization | **Agency & Organization** |
| Agentive Constituent | People (biological) | **Agency** (substrate-independent) |
| Semantic Anchor | Organization | Organization *(unchanged)* |
| One-line Definition | "The humans who perform every capability: their structure, skills, performance, and movement" | "The domain that manages the enterprise's internal agentive fabric: the constitution, coordination, development, and lifecycle of all agents that perform enterprise capabilities, and the organizational structures through which their agency is channeled" |
| Fundamental Question | "How is human agency and organizational structure constituted and coordinated?" | "How is agency constituted and coordinated?" |
| Sub-concern: "Culture & Collaboration" | Human-centric interpretation | Substrate-independent: "Coordination & Collaboration" |
| Sub-concern: "Workforce Planning" | Human headcount | Agent capacity planning (biological, artificial, hybrid) |

### 3.2 What Does NOT Change

| Element | Status |
| :--- | :--- |
| Domain Number (#3) | Unchanged |
| Semantic Anchor (Organization) | Unchanged |
| Axiomatic Grounding ("persists" → agents) | Unchanged |
| Boundary rules (internal vs. external) | Unchanged |
| Cross-domain relationships | Unchanged (terminology updated) |
| Lifecycle applicability | Unchanged |
| Position in the 7×7 matrix | Unchanged |

### 3.3 Affected Repositories

| Repository | Files Affected |
| :--- | :--- |
| `dea-metaframework` | `REPORT.md`, `README.md`, domain specification files |
| `dea-metamodel` | `docs/glossary.md`, domain entity definitions |
| `dea-concepts-model` | `governance/terminology-registry.yaml`, concept mappings |
| `dea-catalog-*` | Any catalog entries referencing Domain 3 |
| `dea-architecture-framework` | ECF matrix references, domain descriptions |

---

## 4. Updated Domain Specification

The following is the **complete, normative specification** for Domain 3 as it must appear in all documentation after this CR is implemented.

### 4.1 Canonical Tuple

```yaml
Domain: Agency & Organization
Semantic Anchor: Organization
Axiomatic Grounding: "persists" — persistence requires agents
Fundamental Question: How is agency constituted and coordinated?
```

### 4.2 Normative Definition

> **Agency & Organization** is the domain that manages the enterprise's internal agentive fabric. It owns the constitution, coordination, development, and lifecycle of all agents that perform enterprise capabilities, and the organizational structures through which their agency is channeled.
>
> The domain is **substrate-independent**: it encompasses biological agents (humans), artificial agents (AI), and hybrid human-AI configurations without requiring reclassification. The semantic anchor is **Organization** — the durable pattern of roles, authority, collaboration, and coordination through which agency is directed. **Agency** is the agentive constituent — the capacity to act on behalf of the enterprise.

### 4.3 Definitional Note

> Within this framework, **"Agency"** refers to the *capacity to act on behalf of the enterprise* — the quality that makes an entity a constituent of the enterprise's internal workforce. This definition is substrate-independent and encompasses biological agents (humans), artificial agents (AI systems, autonomous software agents), and hybrid configurations. The domain's semantic anchor remains **Organization**: the structure through which agency is coordinated. The term "People" is not used as a domain-level identifier because it is biologically loaded and fails the Technology Independence test (ADR-002, Section 3.2, Test 4).

### 4.4 Internal MECE Partition

| Sub-concern | Scope | Human Interpretation | AI-Agent Interpretation |
| :--- | :--- | :--- | :--- |
| **Organizational Design** | Structure, hierarchy, roles, authority delegation, span of control | Org charts, reporting lines, governance committees | Agent topology (hierarchical, swarm, federated), delegation chains, escalation paths |
| **Agent Capacity Planning** | Capability mapping, capacity forecasting, gap analysis | Headcount planning, skill gap analysis, talent pipeline | Agent provisioning plans, model diversity, capability coverage |
| **Acquisition & Onboarding** | Selection, provisioning, configuration, integration | Recruitment, hiring, orientation, onboarding | Agent selection, model deployment, API integration, access provisioning |
| **Development & Performance** | Capability enhancement, evaluation, progression | Training, coaching, performance reviews, career paths | Fine-tuning, RLHF, output evaluation, drift detection, benchmark scoring |
| **Coordination & Collaboration** | Communication, knowledge sharing, collective action | Teamwork, culture, engagement, inclusion | Multi-agent orchestration, shared knowledge bases, communication protocols |
| **Movement & Transition** | Redeployment, versioning, retirement | Promotion, transfer, offboarding, restructuring | Agent redeployment, version migration, decommissioning, graceful degradation |

### 4.5 Boundary Rules

| Included | Excluded (owned elsewhere) |
| :--- | :--- |
| Internal agents (biological, artificial, hybrid) | External parties (*Party & Relationship*) |
| Organizational structure, roles, authority | Governance authority and policy (*Governance & Existence*) |
| Agent capabilities, development, performance | Operational execution they perform (*Operations & Enablement*) |
| Coordination, collaboration, knowledge sharing | Strategic direction (*Strategy & Direction*) |
| Agent lifecycle (acquisition → retirement) | Monetary compensation and costs (*Finance & Accounting*) |
| Organizational design and development | Product work they produce (*Product & Value*) |

### 4.6 Cross-Domain Relationships

```
Agency & Organization staffs → Operations & Enablement (execution agents)
Agency & Organization builds → Product & Value (creators, designers, builders)
Agency & Organization manages → Party & Relationship (relationship managers)
Agency & Organization executes → Strategy & Direction (leaders, planners)
Agency & Organization is compensated via → Finance & Accounting (payroll, compute costs)
Agency & Organization is governed by → Governance & Existence (roles, authority, policy)
```

### 4.7 Lifecycle Applicability

| Lifecycle Stage | Agency & Organization Concern |
| :--- | :--- |
| **Conceive** | Define required agent capabilities, organizational structure, and coordination model |
| **Design** | Design organizational architecture, agent topology, role definitions, authority chains |
| **Build** | Acquire/provision agents, onboard, configure, integrate into organizational structure |
| **Operate** | Monitor performance, coordinate collaboration, manage capacity, resolve conflicts |
| **Evolve** | Develop capabilities, retrain/fine-tune, reorganize, adapt to new requirements |
| **Retire** | Decommission agents, offboard, archive organizational knowledge, transition |
| **Dissolve** | Wind down organizational structure, release agents, archive records |

---

## 5. Documentation Changes

### 5.1 `dea-metaframework/REPORT.md`

#### Change 1: Axiomatic Derivation Table (Section 2.1)

**Before:**
```markdown
| "persists" | → People & Organization | Persistence requires agents: the humans who perform the work and the structure that organizes them. |
```

**After:**
```markdown
| "persists" | → Agency & Organization | Persistence requires agents: the entities that perform the work and the structure that organizes them. |
```

#### Change 2: Domain Table (Section 5.1)

**Before:**
```markdown
| 3 | People & Organization | The humans who perform every capability: their structure, skills, performance, and movement. |
```

**After:**
```markdown
| 3 | Agency & Organization | The domain that manages the enterprise's internal agentive fabric: the constitution, coordination, development, and lifecycle of all agents that perform enterprise capabilities, and the organizational structures through which their agency is channeled. Substrate-independent: encompasses biological, artificial, and hybrid agents. |
```

#### Change 3: All occurrences of "People & Organization"

**Action:** Global find-and-replace `"People & Organization"` → `"Agency & Organization"` throughout `REPORT.md`. Update surrounding text to use substrate-independent language:
- "humans who perform" → "agents that perform"
- "human agency" → "agency"
- "human resources" → "agentive resources" or "agency"

### 5.2 `dea-metaframework/README.md`

#### Change 1: Domain listing

**Before:**
```markdown
"that persists" → People & Organization (agents who persist)
```

**After:**
```markdown
"that persists" → Agency & Organization (agents who persist)
```

#### Change 2: Domain table

**Before:**
```markdown
| 6 | **People & Organization** | Organization | How is human agency and organizational structure constituted? |
```

**After:**
```markdown
| 6 | **Agency & Organization** | Organization | How is agency constituted and coordinated? |
```

#### Change 3: Semantic anchors list

**Before:**
```
Organization
```

**After:**
```
Organization
```
*(No change to the anchor itself, but update any surrounding text that references "People")*

### 5.3 `dea-metamodel/docs/glossary.md`

#### Change 1: Domain glossary entry

**Before:**
```markdown
**People & Organization** — One of the seven axiom-derived rows of the Enterprise Concept Framework foundation matrix. The humans who perform every capability: their structure, skills, performance, and movement.
```

**After:**
```markdown
**Agency & Organization** — One of the seven axiom-derived rows of the Enterprise Concept Framework foundation matrix. The domain that manages the enterprise's internal agentive fabric: the constitution, coordination, development, and lifecycle of all agents that perform enterprise capabilities, and the organizational structures through which their agency is channeled. Substrate-independent: encompasses biological agents (humans), artificial agents (AI), and hybrid configurations. Semantic anchor: Organization.
```

#### Change 2: All cross-references

**Action:** Update all references to "People & Organization" in the glossary to "Agency & Organization". Ensure the glossary entry for "Domain" reflects the updated name.

### 5.4 `dea-concepts-model/governance/terminology-registry.yaml`

#### Change 1: Domain enumeration

**Before:**
```yaml
ecf_domains:
  - name: "Governance & Existence"
  - name: "Supply & Resources"
  - name: "People & Organization"
  - name: "Customer & Demand"
  - name: "Product & Offering"
  - name: "Operations & Delivery"
  - name: "Finance & Value"
```

**After:**
```yaml
ecf_domains:
  - name: "Governance & Existence"
    semantic_anchor: "Enterprise Existence"
  - name: "Strategy & Direction"
    semantic_anchor: "Direction"
  - name: "Agency & Organization"
    semantic_anchor: "Organization"
    agentive_constituent: "Agency"
    substrate_independent: true
  - name: "Party & Relationship"
    semantic_anchor: "Relationship"
  - name: "Product & Value"
    semantic_anchor: "Product"
  - name: "Operations & Enablement"
    semantic_anchor: "Execution"
  - name: "Finance & Accounting"
    semantic_anchor: "Money"
```

#### Change 2: Concept mappings

**Action:** Update all concept mappings that reference `people_and_organization` to `agency_and_organization`. Add a deprecation alias:

```yaml
deprecated_aliases:
  - old: "People & Organization"
    new: "Agency & Organization"
    deprecated_date: "2026-09-07"
    adr: "ADR-002"
    cr: "CR-ECF-007"
```

### 5.5 `dea-architecture-framework`

**Action:** Update all references to "People & Organization" in the ECF matrix documentation, domain descriptions, and any architectural guidance documents. Ensure the 7×7 matrix grid uses "Agency & Organization" as the row label for Domain 3.

### 5.6 `dea-catalog-*` (All Catalog Repositories)

**Action:** Search all catalog repositories for references to "People & Organization" and update to "Agency & Organization". Catalog entries that classify concepts under Domain 3 must be reviewed for substrate-independent language.

---

## 6. Migration Mapping

### 6.1 Terminology Migration

| Old Term | New Term | Context |
| :--- | :--- | :--- |
| People & Organization | **Agency & Organization** | Domain name |
| People | **Agency** / **Agents** | Agentive constituent |
| Humans who perform | **Agents that perform** | Definition text |
| Human agency | **Agency** | Conceptual references |
| Human resources | **Agentive resources** / **Agency** | Resource references |
| Workforce | **Agent workforce** / **Agency** | Collective references |
| Human capital | **Agentive capital** / **Agency** | Economic references |
| Culture & Collaboration | **Coordination & Collaboration** | Sub-concern name |
| Workforce Planning | **Agent Capacity Planning** | Sub-concern name |

### 6.2 Backward Compatibility

For a transition period, the following aliases MUST be maintained in all machine-readable registries:

```yaml
backward_compatibility:
  aliases:
    - canonical: "Agency & Organization"
      aliases:
        - "People & Organization"
        - "people_and_organization"
        - "agency_and_organization"
      status: "deprecated"
      deprecation_notice: "Renamed per ADR-002 / CR-ECF-007. Use 'Agency & Organization'."
```

### 6.3 Content Redistribution

No content redistribution is required for this CR. All content that previously belonged to "People & Organization" remains in "Agency & Organization." The change is a **rename and redefinition**, not a restructuring of scope.

---

## 7. Impact Analysis

### 7.1 Upstream Impact

| Component | Impact | Action Required |
| :--- | :--- | :--- |
| ECF Axiom | None | Axiom text unchanged |
| ECF Domain Set | Domain 3 renamed | Update all domain listings |
| ECF 7×7 Matrix | Row 3 label changed | Update matrix visualizations |

### 7.2 Downstream Impact

| Component | Impact | Action Required |
| :--- | :--- | :--- |
| DEA Metamodel | Entity references to Domain 3 | Update glossary, entity definitions |
| DEA Concepts Model | Terminology registry, concept mappings | Update YAML, add deprecation aliases |
| DEA Catalogs | Catalog entries classified under Domain 3 | Review and update language |
| DEA Architecture Framework | Matrix references, guidance docs | Update all references |
| L0 Process Categories | Process categories mapped to Domain 3 | Verify mapping still valid |

### 7.3 External Impact

| Audience | Impact | Action Required |
| :--- | :--- | :--- |
| Framework consumers | Domain 3 name change | Publish migration guide |
| Tooling integrators | API references to domain names | Update API schemas, add aliases |
| Documentation readers | Updated terminology | Publish changelog |

---

## 8. Acceptance Criteria

This CR is considered **complete** when ALL of the following criteria are met:

### 8.1 Naming & Definition

- [ ] All occurrences of "People & Organization" in `dea-metaframework/REPORT.md` are replaced with "Agency & Organization"
- [ ] All occurrences of "People & Organization" in `dea-metaframework/README.md` are replaced with "Agency & Organization"
- [ ] The updated domain specification (Section 4 of this CR) is present in the domain documentation
- [ ] The definitional note explaining substrate independence is included
- [ ] The fundamental question is updated to "How is agency constituted and coordinated?"
- [ ] The one-line definition uses substrate-independent language ("agents" not "humans")

### 8.2 Semantic Integrity

- [ ] The semantic anchor is explicitly declared as "Organization"
- [ ] The agentive constituent is explicitly declared as "Agency"
- [ ] The internal MECE partition uses substrate-independent sub-concern names
- [ ] Boundary rules are updated to reference "agents" instead of "humans"
- [ ] Cross-domain relationships are updated with new terminology

### 8.3 Registry & Machine-Readability

- [ ] `dea-concepts-model/governance/terminology-registry.yaml` is updated with the new domain name
- [ ] Deprecation aliases are added for backward compatibility
- [ ] All machine-readable references use `agency_and_organization` as the canonical identifier
- [ ] The domain enumeration reflects all seven updated domains (including other CRs)

### 8.4 Cross-Repository Consistency

- [ ] `dea-metamodel/docs/glossary.md` is updated
- [ ] `dea-architecture-framework` references are updated
- [ ] All `dea-catalog-*` repositories are searched and updated
- [ ] No remaining references to "People & Organization" exist without a deprecation alias

### 8.5 Validation

- [ ] The 49-cell matrix (7 domains × 7 lifecycle stages) is validated: all cells in the Agency & Organization row remain meaningful
- [ ] The AI-agent stress test passes: the domain specification holds for a fully AI-agent workforce without modification
- [ ] The boundary test passes: the "OTCHERE Inc. AI service" scenario correctly maps organizational concerns to Agency & Organization
- [ ] No other domain's boundary is violated by the rename

---

## 9. Implementation Checklist

### Phase 1: Core Specification (Priority: Critical)

| # | Task | Repository | File(s) | Assignee | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1.1 | Write the full domain specification per Section 4 | `dea-metaframework` | `domains/agency-and-organization.md` | — | ⬜ |
| 1.2 | Update axiomatic derivation table | `dea-metaframework` | `REPORT.md` §2.1 | — | ⬜ |
| 1.3 | Update domain listing table | `dea-metaframework` | `REPORT.md` §5.1 | — | ⬜ |
| 1.4 | Global find-replace in REPORT.md | `dea-metaframework` | `REPORT.md` | — | ⬜ |
| 1.5 | Update README.md domain listing | `dea-metaframework` | `README.md` | — | ⬜ |

### Phase 2: Metamodel & Glossary (Priority: High)

| # | Task | Repository | File(s) | Assignee | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 2.1 | Update glossary entry | `dea-metamodel` | `docs/glossary.md` | — | ⬜ |
| 2.2 | Update all cross-references | `dea-metamodel` | `docs/glossary.md` | — | ⬜ |
| 2.3 | Update entity definitions referencing Domain 3 | `dea-metamodel` | Entity definition files | — | ⬜ |

### Phase 3: Concepts Model & Registry (Priority: High)

| # | Task | Repository | File(s) | Assignee | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 3.1 | Update terminology registry | `dea-concepts-model` | `governance/terminology-registry.yaml` | — | ⬜ |
| 3.2 | Add deprecation aliases | `dea-concepts-model` | `governance/terminology-registry.yaml` | — | ⬜ |
| 3.3 | Update concept mappings | `dea-concepts-model` | Concept mapping files | — | ⬜ |

### Phase 4: Architecture Framework & Catalogs (Priority: Medium)

| # | Task | Repository | File(s) | Assignee | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 4.1 | Update ECF matrix references | `dea-architecture-framework` | Matrix documentation | — | ⬜ |
| 4.2 | Search and update all catalog references | `dea-catalog-*` | All catalog files | — | ⬜ |
| 4.3 | Update L0 process category mappings | `dea-architecture-framework` | Process framework docs | — | ⬜ |

### Phase 5: Validation & Publication (Priority: Critical)

| # | Task | Repository | File(s) | Assignee | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 5.1 | Validate 49-cell matrix completeness | `dea-metaframework` | Matrix validation | — | ⬜ |
| 5.2 | Run AI-agent stress test | `dea-metaframework` | Validation report | — | ⬜ |
| 5.3 | Run boundary test (OTCHERE scenario) | `dea-metaframework` | Validation report | — | ⬜ |
| 5.4 | Cross-repository consistency check | All | Automated search | — | ⬜ |
| 5.5 | Publish migration guide | `dea-metaframework` | `docs/migration/CR-ECF-007.md` | — | ⬜ |
| 5.6 | Publish changelog entry | `dea-metaframework` | `CHANGELOG.md` | — | ⬜ |

---

## 10. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| "Agency" confused with "government agency" | Low | Low | The pairing "Agency & Organization" disambiguates. Include clarification in glossary. |
| Practitioner resistance to unfamiliar term | Medium | Medium | Publish rationale (ADR-002) alongside the change. Provide migration guide. Maintain deprecation aliases. |
| Incomplete cross-repository updates | Medium | High | Automated search across all `technehub-labs` repositories for "People & Organization" before closing CR. |
| Downstream tooling breaks on name change | Low | Medium | Maintain backward-compatible aliases in all machine-readable registries for minimum 2 release cycles. |

---

## 11. References

| Reference | Location |
| :--- | :--- |
| ADR-002: ECF Domain Semantic Integrity & Substrate Independence | `dea-metaframework/docs/adr/ADR-002.md` |
| ECF Axiomatic Derivation | `dea-metaframework/REPORT.md` §2 |
| Domain Semantic Integrity Contract | ADR-002 §6.4 |
| AI-Agent Stress Test Results | ADR-002 §5 |
| Related CR: CR-ECF-002 (Strategy & Direction) | `dea-metaframework/docs/cr/CR-ECF-002.md` |
| Related CR: CR-ECF-004 (Party & Relationship) | `dea-metaframework/docs/cr/CR-ECF-004.md` |
| Related CR: CR-ECF-005 (Product & Value) | `dea-metaframework/docs/cr/CR-ECF-005.md` |
| Related CR: CR-ECF-006 (Operations & Enablement) | `dea-metaframework/docs/cr/CR-ECF-006.md` |
| Related CR: CR-ECF-008 (Finance & Accounting) | `dea-metaframework/docs/cr/CR-ECF-008.md` |

---

## 12. Approval

| Role | Name | Decision | Date |
| :--- | :--- | :--- | :--- |
| Author | — | Proposed | 2026-09-07 |
| Technical Reviewer | — | ⬜ Pending | — |
| Architecture Board | — | ⬜ Pending | — |
| Repository Maintainer | — | ⬜ Pending | — |

---

*This Change Request is governed by ADR-002. Implementation MUST NOT begin until all approval signatures are obtained. Upon approval, implementation follows the phased checklist in Section 9.*