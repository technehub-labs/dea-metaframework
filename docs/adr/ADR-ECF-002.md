# ADR-ECF-002: ECF Domain Semantic Integrity & Substrate Independence

| Field | Value |
| :--- | :--- |
| **Status** | Proposed |
| **Date** | 2026-09-07 |
| **Deciders** | TechNeHub Labs Architecture Board |
| **Technical Story** | CR: ECF Domain Restructuring for Semantic Integrity, MECE Compliance, and Substrate Independence |
| **Tags** | `ecf`, `domains`, `metaframework`, `mece`, `ai-agents`, `naming` |

---

## 1. Research Question

> **Given the Enterprise Concept Framework's role as the normative organizing dimension for the DEA Metaframework's 7×7 matrix, how should the seven ECF domains be named, defined, and bounded such that they form a Mutually Exclusive, Collectively Exhaustive (MECE) partition of the enterprise that is:**
>
> 1. **Axiomatically faithful** — derived from and consistent with the grounding axiom;
> 2. **Semantically stable** — each domain identifies a primary, durable class of enterprise subject rather than a department, technology, process, or transient vocabulary;
> 3. **Lifecycle-complete** — each domain remains meaningful through every lifecycle stage;
> 4. **Technology-independent** — each domain survives radical technological paradigm shifts, including the substitution of human labor with AI agents;
> 5. **Collectively exhaustive** — the seven domains together cover the entire enterprise without requiring an eighth "miscellaneous" domain;
> 6. **Machine-testable** — domain boundaries can be formally specified through inclusion/exclusion rules suitable for automated validation?

---

## 2. Context and Problem Statement

### 2.1 The Original State

The ECF, as defined in the `dea-metaframework` repository, derives seven domains from the grounding axiom:

> *"An enterprise is any bounded entity that persists by exchanging value with its environment."*

The original seven domains were:

| # | Domain | Axiom Fragment |
| :-: | :--- | :--- |
| 1 | Governance & Existence | "bounded entity" |
| 2 | Supply & Resources | "persists" |
| 3 | People & Organization | "persists" |
| 4 | Customer & Demand | "exchanging value" |
| 5 | Product & Offering | "exchanging value" |
| 6 | Operations & Delivery | "exchanging value" |
| 7 | Finance & Value | "with its environment" |

### 2.2 The Problem

Multiple concerns were identified with the original domain set:

1. **"Supply & Resources"** fails MECE: physical assets overlap with Operations; financial resources overlap with Finance; human resources overlap with People. The domain becomes a catch-all for "things we use."
2. **"Customer & Demand"** is sell-side biased: it excludes suppliers, partners, regulators, and ecosystem participants. The axiom says "exchanging value with its environment," not merely "selling to customers."
3. **"People & Organization"** is biologically loaded: the term "People" assumes human agents. As AI agents become capable of constituting an enterprise's entire workforce, the domain fails the Technology Independence test.
4. **"Finance & Value"** violates Boundary Integrity: "Value" is a cross-cutting enterprise outcome created by Product, realized by Operations, measured by Finance, and directed by Strategy. No single domain can own "Value" without colliding with others.
5. **"Operations & Delivery"** does not explicitly accommodate technology as an enabler, creating ambiguity about where technology management resides.
6. **No Strategy domain exists**, despite Strategy being a mandatory L0 process category in all standard frameworks (APQC, TOGAF, BIZBOK).

### 2.3 The Trigger

A proposed change request (CR) was submitted to rename and restructure the domains. The initial proposal was evaluated, found partially suitable, and subjected to deeper architectural analysis. This ADR documents the full analytical journey and the resulting normative decision.

---

## 3. Analysis Methodology

### 3.1 The Normative Principle

The following principle was established as the governing rule for domain naming:

> **An ECF domain represents a primary, stable class of enterprise subject that the enterprise manages across its lifecycle. A domain name should identify that semantic subject, optionally paired with an inseparable complementary concern, rather than a department, technology, process, activity, outcome, or transient organizational vocabulary.**

### 3.2 The Five Tests

Every domain name and definition was evaluated against five rigorous tests:

| Test | Question |
| :--- | :--- |
| **1. Semantic Anchor** | What is the principal thing being managed? Is it a stable, durable subject? |
| **2. Lifecycle Completeness** | Does the domain remain meaningful through every lifecycle stage (conception → dissolution)? |
| **3. Boundary Integrity** | Can we state precisely what belongs and what does not belong? Are inclusion/exclusion rules unambiguous? |
| **4. Technology Independence** | Does the domain survive major technological change (e.g., human → AI workforce)? |
| **5. Collective Exhaustiveness** | Do all seven domains together cover the enterprise without requiring an eighth "miscellaneous" domain? |

### 3.3 The Domain Semantic Integrity Contract

A formal contract was established requiring that every domain specification includes:

```
Domain Name
Semantic Anchor
Axiomatic Grounding
Fundamental Enterprise Question
Scope
Included Concepts
Excluded Concepts
Cross-Domain Relationships
Lifecycle Applicability
Internal MECE Partition
```

### 3.4 The Stress Test

The final domain set was stress-tested against a radical edge case: **a Digital Enterprise owned by an AI Agent, with a workforce consisting entirely of AI Agents, actively exchanging value with its environment.** This test evaluated whether the axiom and domain definitions survive the complete substitution of human labor with artificial agents.

---

## 4. Domain-by-Domain Analysis

### 4.1 Governance & Existence → RETAIN (Enhanced)

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Enterprise Existence |
| **Test Results** | All 5 tests pass |
| **Decision** | Retain name. Enhance definition to explicitly cover formation, identity, legal standing, mandate, authority, policy, risk, compliance, assurance, and dissolution |
| **Rationale** | The axiom fragment "bounded entity" directly generates this domain. The name is already correct. The scope needed expansion from "rules and assurance" to the full ontological reality of the enterprise |

### 4.2 Supply & Resources → REPLACE with Strategy & Direction

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor (old)** | Substrate (assets) |
| **Semantic Anchor (new)** | Direction |
| **Test Results** | "Resources" fails MECE (cross-cutting asset class). "Strategy" passes all 5 tests |
| **Decision** | Remove "Supply & Resources." Introduce "Strategy & Direction" |
| **Rationale** | Under MECE analysis, "Resources" decomposes into: physical assets → Operations & Enablement; financial resources → Finance & Accounting; human resources → People/Agency. No coherent standalone domain remains. Strategy is a mandatory L0 process category in all standard frameworks and represents the deliberate steering required for directed persistence |
| **Redistribution** | Physical/virtual substrate → Operations & Enablement (as enablers). Financial resources → Finance & Accounting. Human resources → Agency & Organization |

### 4.3 People & Organization → EVOLVE to Agency & Organization

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Organization |
| **Agentive Constituent** | Agency (replacing "People") |
| **Test Results** | "People" fails Technology Independence. "Agency" passes all 5 tests |
| **Decision** | Rename to **Agency & Organization** |
| **Rationale** | See Section 5 (Stress Test) for full analysis |

### 4.4 Customer & Demand → EVOLVE to Party & Relationship

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Relationship |
| **Test Results** | "Customer" fails MECE (excludes suppliers, partners, regulators). "Party" passes all 5 tests |
| **Decision** | Rename to **Party & Relationship** |
| **Rationale** | "Customer" is a *role*; "Party" is the universal *entity*. A single party can simultaneously be a customer, supplier, and partner. "Demand" is a transient signal; "Relationship" is a lifecycle-complete subject. The axiom says "exchanging value with its environment" — the environment includes ALL external actors, not just buyers |

### 4.5 Product & Offering → EVOLVE to Product & Value

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Product |
| **Test Results** | All 5 tests pass with "Product & Value" |
| **Decision** | Rename to **Product & Value** |
| **Rationale** | "Offering" overlaps with "Product" and is vague. "Value" explicitly connects the product to the axiomatic purpose ("exchanging value") and establishes that this domain owns the *value-bearing proposition*. Critical boundary: Product & Value owns the value proposition, NOT every form of enterprise value |

### 4.6 Operations & Delivery → EVOLVE to Operations & Enablement

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Execution |
| **Test Results** | All 5 tests pass with "Operations & Enablement" |
| **Decision** | Rename to **Operations & Enablement** |
| **Rationale** | "Delivery" is an outcome/phase of execution. "Enablement" explicitly positions technology, platforms, and physical infrastructure as *means* of execution, ensuring Technology Independence. The domain absorbs the physical/virtual substrate concerns previously in "Supply & Resources" |

### 4.7 Finance & Value → EVOLVE to Finance & Accounting

| Aspect | Finding |
| :--- | :--- |
| **Semantic Anchor** | Money |
| **Test Results** | "Value" fails Boundary Integrity (cross-cutting outcome). "Accounting" passes all 5 tests |
| **Decision** | Rename to **Finance & Accounting** |
| **Rationale** | "Value" is created by Product, realized by Operations, measured by Finance, and directed by Strategy. No single domain can own it. "Accounting" correctly scopes the domain to monetary measurement. The domain covers both forward-looking finance (FP&A, treasury, investment) and backward-looking accounting (recording, reporting) |

---

## 5. Stress Test: The AI-Agent-Only Enterprise

### 5.1 Scenario Definition

> A Digital Enterprise is owned by a person or an AI Agent. Its workforce consists **entirely of AI Agents**. It actively exchanges value with its environment (customers, partners, regulators, other AI agents).

### 5.2 Axiom Evaluation

| Axiom Fragment | Human Enterprise | AI-Agent Enterprise | Holds? |
| :--- | :--- | :--- | :--- |
| "bounded entity" | Legal incorporation | Smart contract, DAO, registered entity | ✅ |
| "persists" | Human labor sustains operations | AI agents sustain operations autonomously | ✅ |
| "exchanging value" | Humans sell, buy, negotiate | AI agents execute transactions autonomously | ✅ |
| "with its environment" | Market, regulators, partners | Market, regulators, APIs, other AI agents | ✅ |

**Conclusion:** The axiom is **agent-agnostic**. It requires *agency*, not *biology*.

### 5.3 Domain Survival Analysis

| Domain | Survives AI-Only Workforce? | Notes |
| :--- | :--- | :--- |
| Governance & Existence | ✅ | Legal standing, mandate, authority still required |
| Strategy & Direction | ✅ | Strategic steering still required regardless of agent type |
| **Agency & Organization** | ✅ | **Critical: "Agency" is substrate-independent. "People" would fail** |
| Party & Relationship | ✅ | External parties remain external regardless of internal agent type |
| Product & Value | ✅ | Products/services still designed and delivered |
| Operations & Enablement | ✅ | Execution and enablement still required |
| Finance & Accounting | ✅ | Monetary measurement still required |

### 5.4 The Naming Decision for Domain 3

Three candidates were evaluated:

| Candidate | Substrate-Independent? | Axiomatically Faithful? | Requires Caveat? | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **People & Organization** | ❌ Biologically loaded | ⚠️ Interpretation | Yes | Rejected |
| **Workforce & Organization** | ✅ Function-based | ⚠️ Indirect | No | Viable |
| **Agency & Organization** | ✅ Absolute | ✅ Direct ("agents") | No | **Selected** |

**Decision:** Adopt **Agency & Organization**.

**Rationale:**
- The axiom derivation states: *"persistence requires agents."* The semantic quality is **agency** — the capacity to act. "People" is merely the current biological implementation.
- A metaframework should not require definitional footnotes to accommodate foreseeable technological realities.
- "Agency" captures both labor AND non-labor aspects of internal agents (authority, autonomy, initiative, coordination).
- The pairing "Agency & Organization" reads as: *the capacity to act (Agency) and the structure through which that capacity is coordinated (Organization).*

---

## 6. Decision

### 6.1 The Canonical Seven Domains

The following seven domains are hereby established as the normative ECF domain set:

| # | Domain | Semantic Anchor | Fundamental Question |
| :-: | :--- | :--- | :--- |
| 1 | **Governance & Existence** | Enterprise Existence | What makes the enterprise an entity, legitimate and governable? |
| 2 | **Strategy & Direction** | Direction | Where is the enterprise going and why? |
| 3 | **Agency & Organization** | Organization | How is agency constituted and coordinated? |
| 4 | **Party & Relationship** | Relationship | With whom does the enterprise relate and exchange value? |
| 5 | **Product & Value** | Product | What does the enterprise create and make valuable? |
| 6 | **Operations & Enablement** | Execution | How does the enterprise execute and what enables execution? |
| 7 | **Finance & Accounting** | Money | How are monetary resources and consequences planned and accounted for? |

### 6.2 The Semantic Anchors

```
Enterprise Existence
Direction
Organization
Relationship
Product
Execution
Money
```

### 6.3 The Axiomatic Mapping

| Axiom Fragment | Generated Domain(s) |
| :--- | :--- |
| "bounded entity" | Governance & Existence |
| "persists" (agents) | Agency & Organization |
| "persists" (directed) | Strategy & Direction |
| "persists" (substrate/mechanism) | Operations & Enablement |
| "exchanging value" (counterparty) | Party & Relationship |
| "exchanging value" (bearer) | Product & Value |
| "with its environment" (measurement) | Finance & Accounting |

### 6.4 The Domain Semantic Integrity Contract

Every domain specification MUST include:

1. Exactly one declared semantic anchor
2. A stable enterprise subject (not a department, technology, or activity)
3. Noun-based, semantically durable naming
4. Independence from organizational departmentalization
5. Independence from technology substrate
6. Lifecycle completeness
7. Explicit inclusion/exclusion boundary rules
8. Cross-domain relationship declarations
9. Internal MECE partition into sub-concerns
10. No ownership of generic enterprise outcomes (e.g., "value") unless that is the actual semantic subject

---

## 7. Consequences

### 7.1 Positive

| Consequence | Impact |
| :--- | :--- |
| MECE partition achieved | No enterprise concern is homeless or double-owned |
| Technology independence guaranteed | The framework survives human → AI workforce transition without modification |
| Standard L0 alignment | Domains map cleanly to APQC, TOGAF, and BIZBOK process categories |
| Machine-testability | Explicit inclusion/exclusion rules enable automated boundary validation |
| Axiomatic fidelity preserved | All seven domains remain derivable from the grounding axiom |
| Future-proofing | No domain name requires redefinition as technology evolves |

### 7.2 Negative / Trade-offs

| Consequence | Impact | Mitigation |
| :--- | :--- | :--- |
| "Agency" is less familiar than "People" | Adoption friction for practitioners accustomed to "People & Organization" | Provide clear definitional guidance and migration mapping |
| "Supply & Resources" removed | Existing content mapped to this domain must be redistributed | Provide explicit redistribution mapping (physical → Operations; financial → Finance; human → Agency) |
| "Strategy & Direction" added | Breaks strict 1:1 mapping with original 7-word axiom | Document that "persists" generates three domains (agents, direction, mechanism) |
| "Finance & Accounting" may feel narrower than "Finance & Value" | Perception of reduced strategic scope | Explicitly document that Finance includes FP&A, treasury, investment (forward-looking), not just bookkeeping |

### 7.3 Risks

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| "Agency" confused with "government agency" | Low | Low | The pairing "Agency & Organization" disambiguates |
| Practitioners resist "Party" instead of "Customer" | Medium | Medium | Document that "Customer" is a *role within* the Party domain, not a separate domain |
| Strategy domain seen as axiomatic stretch | Low | Medium | Document that "directed persistence" is a valid derivation of "persists" |

---

## 8. Compliance & Validation

### 8.1 The Boundary Test

The final domain set was validated using the following test:

> **OTCHERE Inc. decides to launch a new AI-enabled predictive maintenance service.**

| Domain | Question Asked | Concern Resolved? |
| :--- | :--- | :--- |
| Governance & Existence | Are we legally authorized and compliant? | ✅ |
| Strategy & Direction | Why are we doing this? What strategic objective does it serve? | ✅ |
| Agency & Organization | What agent capabilities, roles, and structures are needed? | ✅ |
| Party & Relationship | Who are the external actors (customers, data partners, regulators)? | ✅ |
| Product & Value | What is the AI service and what is the value proposition? | ✅ |
| Operations & Enablement | How do we build, host, deliver, and enable it? | ✅ |
| Finance & Accounting | How is it funded, priced, transacted, and accounted for? | ✅ |

**Result:** Nothing is missing. Nothing is double-owned. Nothing must be artificially forced into a domain.

### 8.2 The AI-Agent Stress Test

As documented in Section 5, the domain set survives complete substitution of human agents with AI agents without requiring any structural modification.

---

## 9. Implementation Notes for the CR

The Change Request implementing this ADR should:

1. **Update all domain names** in the `dea-metaframework` repository to the canonical seven
2. **Write full domain specifications** following the Domain Semantic Integrity Contract format
3. **Redistribute "Supply & Resources" content** to Operations & Enablement, Finance & Accounting, and Agency & Organization
4. **Update the REPORT.md** axiomatic derivation table to reflect the new 7-domain structure
5. **Update the terminology registry** in `dea-concepts-model` to reflect the new domain names and semantic anchors
6. **Update the glossary** in `dea-metamodel` to reference the new domain names
7. **Provide a migration mapping** from old domain names to new domain names for backward compatibility
8. **Validate the 49-cell matrix** (7 domains × 7 lifecycle stages) to ensure all cells remain meaningful with the new domain definitions

---

## 10. References

- **Axiom:** *"An enterprise is any bounded entity that persists by exchanging value with its environment."*
- **Repository:** `github.com/technehub-labs/dea-metaframework`
- **Related ADRs:** ADR-ECF-001 (ECF Initial Domain Definition)
- **Standards Referenced:** APQC Process Classification Framework, TOGAF Business Architecture, BIZBOK
- **Architectural Principles:** MECE, Semantic Anchoring, Technology Independence, Substrate Independence

---

*This ADR serves as the normative rationale for the ECF Domain Restructuring Change Request. All subsequent domain specifications, catalog mappings, and metamodel references MUST conform to the decisions recorded herein.*