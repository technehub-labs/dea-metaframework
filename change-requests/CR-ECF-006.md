# ECF Domain Transformation: Before & After

## Summary Transformation Map

| # | Original (GitHub) | Final (Optimized) | Change Type |
| :--- | :--- | :--- | :--- |
| 1 | Governance & Existence | **Governance & Existence** | Retained & Enhanced |
| 2 | Supply & Resources | **Strategy & Direction** | Replaced |
| 3 | People & Organization | **People & Organization** | Retained & Enhanced |
| 4 | Customer & Demand | **Party & Relationship** | Renamed & Expanded |
| 5 | Product & Offering | **Product & Value** | Renamed & Sharpened |
| 6 | Operations & Delivery | **Operations & Enablement** | Renamed & Expanded |
| 7 | Finance & Value | **Finance & Accounting** | Renamed & Sharpened |

---

## Domain 1: Governance & Existence

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Governance & Existence |
| **Axiomatic Derivation** | *"bounded entity"* — Boundedness requires a boundary: who is inside, what rules apply, what constitutes the entity itself |
| **One-line Definition** | The precondition of boundedness: what defines the entity, what rules apply, and the assurance that the other domains behave |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Governance & Existence |
| **Semantic Anchor** | Enterprise Existence |
| **Axiomatic Grounding** | *"bounded entity"* — boundedness requires a boundary, authority, and the assurance that the entity persists as itself |
| **Enhanced Definition** | The domain that constitutes the enterprise as a bounded, legitimate, persisting entity. It owns the enterprise's ontological reality (what it is, why it is legitimate, under what authority it operates) and its constitutional machinery (how decisions are authorized, constrained, and assured). It is the precondition of all other domains. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Governance & Existence | Governance & Existence | Retained — the name was already correct |
| Scope | "What defines the entity, what rules apply" | Full ontological reality + constitutional machinery | Expanded to include formation, identity, legal standing, mandate, authority, dissolution |
| Boundary | Implicit | Explicit inclusion/exclusion rules | Added precise boundary with Strategy (choices), Operations (enforcement), People (implementers) |
| Lifecycle | Not specified | Formation → Identity → Mandate → Governance → Compliance → Dissolution | Made lifecycle-complete |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Formation & Identity | Legal constitution, registration, naming, brand identity, mission, ownership structure |
| Mandate & Authority | Constitutional documents, delegation frameworks, decision rights, jurisdiction |
| Policy & Control | Policy lifecycle, control design, rule frameworks, standards adoption |
| Risk & Compliance | Risk appetite, regulatory compliance, legal obligations, audit assurance |
| Assurance & Accountability | Internal audit, governance reporting, board oversight, fiduciary duty |
| Dissolution & Succession | Winding down, merger/acquisition governance, entity succession, continuity |

---

## Domain 2: Supply & Resources → Strategy & Direction

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Supply & Resources |
| **Axiomatic Derivation** | *"persists"* — Persistence requires a substrate: the physical or virtual assets that keep the entity alive over time |
| **One-line Definition** | The substrate the enterprise persists on: physical or virtual, owned or rented, and its capacity, health, and disposal |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Strategy & Direction |
| **Semantic Anchor** | Direction |
| **Axiomatic Grounding** | *"persists"* — persistence is not mere survival; it requires deliberate, adaptive steering toward a future state |
| **Enhanced Definition** | The domain that determines the enterprise's intentional trajectory. It translates the enterprise's reason for existing into concrete choices about positioning, ambition, and resource allocation priorities. It manages direction as a stable subject: not the strategy document, not the planning ritual, but the enterprise's deliberate determination of where it will go, what it will become, and what it will prioritize. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Supply & Resources | Strategy & Direction | "Resources" failed MECE: physical assets → Operations; financial resources → Finance; human resources → People |
| Anchor | Substrate (assets) | Direction (intent) | The enterprise needs a dedicated domain for intentional steering; "Resources" was a cross-cutting asset class, not a stable subject |
| Scope | Physical/virtual assets, capacity, health, disposal | Purpose, ambition, positioning, choices, objectives, adaptation | Strategy is a mandatory L0 process category in all standard frameworks (APQC, TOGAF) |
| Redistribution | N/A | Physical/virtual assets moved to **Operations & Enablement** as enablers; financial resources moved to **Finance & Accounting**; human resources moved to **People & Organization** | Achieves true MECE by eliminating the "Resources" catch-all |

### Why "Supply & Resources" Was Removed

Under the **Collective Exhaustiveness (MECE)** test, "Resources" is not a single manageable subject:
- **Physical resources** (equipment, facilities) → enablers of execution → **Operations & Enablement**
- **Virtual resources** (IT infrastructure, platforms) → enablers of execution → **Operations & Enablement**
- **Financial resources** (capital, budgets) → monetary management → **Finance & Accounting**
- **Human resources** (people, skills) → organizational agents → **People & Organization**

A standalone "Resources" domain created boundary collisions with all other domains and failed to form a clean partition.

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Purpose & Ambition | Mission articulation, vision definition, aspiration levels, strategic intent |
| Environmental Sensing | Market analysis, competitive intelligence, trend identification, scenario planning |
| Strategic Choices | Positioning decisions, scope boundaries, competitive advantage logic |
| Objectives & Targets | Goal decomposition, KPIs, strategic milestones, outcome definitions |
| Strategic Planning | Roadmap development, initiative portfolio selection, resource allocation priorities |
| Strategic Adaptation | Transformation triggers, strategic pivots, renewal decisions, learning loops |

---

## Domain 3: People & Organization

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | People & Organization |
| **Axiomatic Derivation** | *"persists"* — Persistence requires agents: the humans who perform the work and the structure that organizes them |
| **One-line Definition** | The humans who perform every capability: their structure, skills, performance, and movement |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | People & Organization |
| **Semantic Anchor** | Organization |
| **Axiomatic Grounding** | *"persists"* — persistence requires agents; the enterprise cannot act without humans organized for purpose |
| **Enhanced Definition** | The domain that manages the enterprise's internal human fabric. It owns the constitution, coordination, development, and movement of the agents who perform all enterprise capabilities, and the structures through which they are organized. The domain manages organization as a stable subject: the durable pattern of roles, authority, collaboration, and culture through which human agency is coordinated. People are the agents; organization is the structure that channels their agency. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | People & Organization | People & Organization | Retained — the name was already correct |
| Anchor | Implicit (People) | Explicit: **Organization** | Organization is the stable, durable subject; People are the agentive constituent. This prevents the domain from being reduced to "HR management" |
| Scope | "humans who perform every capability" | Full organizational fabric: structure, roles, authority, workforce, culture, collaboration, accountability | Expanded to include organizational design, authority delegation, culture, and organizational development |
| Boundary | Implicit | Explicit: excludes external parties, governance authority, operational execution, monetary compensation | Prevents collision with Party & Relationship, Governance, Operations, Finance |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Organizational Design | Structure, hierarchy, span of control, role architecture, authority delegation |
| Workforce Planning | Headcount, capability mapping, talent pipeline, succession planning |
| Acquisition & Onboarding | Recruitment, selection, contracting, integration |
| Development & Performance | Learning, skill building, performance management, career progression |
| Culture & Collaboration | Values, norms, engagement, teamwork, knowledge sharing, inclusion |
| Movement & Transition | Redeployment, offboarding, restructuring, organizational change management |

---

## Domain 4: Customer & Demand → Party & Relationship

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Customer & Demand |
| **Axiomatic Derivation** | *"exchanging value"* — Exchange requires a counterparty: the people whose need the entity meets, and the demand they generate |
| **One-line Definition** | The enterprise's reason to exchange: identifying, acquiring, serving, and retaining the people whose need it meets |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Party & Relationship |
| **Semantic Anchor** | Relationship |
| **Axiomatic Grounding** | *"exchanging value"* — exchange requires a counterparty; the enterprise cannot exchange with itself |
| **Enhanced Definition** | The domain that manages the enterprise's external social fabric. It owns the identification, establishment, development, and termination of bonds between the enterprise and all external entities with whom it interacts. The domain manages relationships as stable subjects with full lifecycle integrity, not merely the transactional events that occur within them. It encompasses all external parties regardless of their role (customer, supplier, partner, regulator, community). |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Customer & Demand | Party & Relationship | "Customer" is a *role*; "Party" is the universal *entity*. A single party can simultaneously be a customer, supplier, and partner. "Demand" is a transient signal; "Relationship" is a lifecycle-complete subject |
| Anchor | Customer (external buyer) | **Relationship** (the bond) | Relationship has a full lifecycle (Identify → Establish → Engage → Retain → Terminate); Demand is a momentary state |
| Scope | "identifying, acquiring, serving, retaining" (sell-side only) | All external parties and all relationship types (sell-side, buy-side, partner-side, regulatory) | "Customer" excluded suppliers, partners, regulators. "Party" is MECE-complete for the external environment |
| Boundary | Implicit | Explicit: excludes internal agents, products exchanged, monetary records, operational fulfillment | Prevents collision with People, Product, Finance, Operations |

### Why "Customer" Failed the MECE Test

| Problem | Explanation |
| :--- | :--- |
| Role vs. Entity | "Customer" is a role a party plays. A single entity can be a Customer, Supplier, and Partner simultaneously. Naming the domain after one role fractures the entity across domains |
| Sell-side bias | "Customer & Demand" only covers outbound exchange (selling). Inbound exchange (buying/sourcing) and lateral exchange (partnering) become homeless |
| Lifecycle incompleteness | "Demand" is a signal, not a manageable subject. You manage a *relationship*, not a *demand* |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Party Identification | Discovery, segmentation, profiling, qualification of external entities |
| Relationship Establishment | Onboarding, contracting, trust building, channel selection |
| Engagement & Interaction | Communication, collaboration, negotiation, conflict resolution |
| Relationship Development | Deepening, cross-role evolution, loyalty, retention |
| Relationship Governance | SLAs, relationship health monitoring, compliance with relationship terms |
| Relationship Termination | Offboarding, exit management, post-relationship obligations |

---

## Domain 5: Product & Offering → Product & Value

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Product & Offering |
| **Axiomatic Derivation** | *"exchanging value"* — Exchange requires something to offer: the catalog of what the entity provides to meet demand |
| **One-line Definition** | The catalog of what the enterprise offers: its design, packaging, release, and retirement |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Product & Value |
| **Semantic Anchor** | Product |
| **Axiomatic Grounding** | *"exchanging value"* — exchange requires something to offer; a bearer of value must exist to be exchanged |
| **Enhanced Definition** | The domain that manages the enterprise's value-bearing propositions. It owns the complete lifecycle of whatever the enterprise creates, shapes, packages, and makes available for exchange with external parties. The domain manages products as stable subjects: not merely physical goods, but any value-bearing entity (services, solutions, experiences, platforms, intellectual property) that the enterprise designs, builds, evolves, and eventually retires. The critical boundary: Product & Value owns the value-bearing proposition, not every form of value in the enterprise. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Product & Offering | Product & Value | "Offering" is vague and overlaps with "Product". "Value" explicitly connects the product to the axiomatic purpose ("exchanging value") and establishes that this domain owns the *value proposition* |
| Anchor | Catalog (collection) | **Product** (the fundamental unit) | Product is the stable, manageable subject. The catalog/portfolio is a sub-concern within the domain, not the anchor |
| Scope | "catalog of what the enterprise offers" | Full lifecycle of value-bearing propositions: conception → design → build → package → launch → evolve → retire | Expanded from catalog management to full product lifecycle |
| Boundary | Implicit | Explicit: owns the value-bearing proposition; does NOT own monetary accounting, relationships, or operational delivery | Prevents collision with Finance (monetary value), Party (relationships), Operations (delivery) |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Proposition Design | Value proposition definition, product concept, solution architecture, service design |
| Portfolio Management | Catalog curation, product mix decisions, lifecycle staging, retirement planning |
| Product Development | Research, prototyping, build, testing, iteration, release preparation |
| Packaging & Configuration | Bundling, pricing structure (not price itself), variant management, SKU management |
| Market Readiness | Launch orchestration, positioning, collateral, readiness validation |
| Product Evolution | Roadmap management, feature prioritization, continuous improvement, sunset |

---

## Domain 6: Operations & Delivery → Operations & Enablement

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Operations & Delivery |
| **Axiomatic Derivation** | *"exchanging value"* — Exchange requires a mechanism: the engine that turns the offering into a delivered outcome |
| **One-line Definition** | The engine that turns an offering into a delivered outcome: planning, fulfilling, running, resolving |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Operations & Enablement |
| **Semantic Anchor** | Execution |
| **Axiomatic Grounding** | *"exchanging value"* — exchange requires a mechanism; value must be produced, delivered, and sustained |
| **Enhanced Definition** | The domain that manages the enterprise's execution engine and the means that make execution possible. It owns the transformation of offerings into delivered outcomes, and the physical, virtual, and procedural infrastructure that enables that transformation. The domain manages execution as a stable subject: the repeatable, manageable, measurable engine that produces outcomes. Technology, platforms, and physical assets are positioned as enablers of execution, not as ends in themselves. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Operations & Delivery | Operations & Enablement | "Delivery" is an outcome/phase of execution. "Enablement" captures the critical architectural requirement of positioning technology, platforms, and physical infrastructure as *means* of execution |
| Anchor | Engine (mechanism) | **Execution** | Execution is the stable, lifecycle-complete subject. Delivery is one mode of execution; Enablement is the complementary concern (the means) |
| Scope | "planning, fulfilling, running, resolving" | Full execution scope: processes, delivery, technology platforms, physical infrastructure, operational planning, quality, resilience | Absorbed the physical/virtual resource concerns previously in "Supply & Resources" |
| Technology Treatment | Not explicitly addressed | Technology is an **enabler**, not the domain itself | Ensures Technology Independence: the domain survives any technological paradigm shift |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Process Design & Management | Workflow architecture, process orchestration, procedure definition, optimization |
| Execution & Fulfillment | Production, service delivery, order fulfillment, project execution, incident resolution |
| Technology Enablement | Platforms, applications, data infrastructure, integration, technical operations |
| Physical Enablement | Facilities, equipment, logistics infrastructure, physical security |
| Operational Planning | Demand planning, capacity scheduling, resource allocation (operational), SLA management |
| Operational Assurance | Quality management, monitoring, resilience, continuity, disaster recovery |

---

## Domain 7: Finance & Value → Finance & Accounting

### Before

| Attribute | Original |
| :--- | :--- |
| **Domain Name** | Finance & Value |
| **Axiomatic Derivation** | *"with its environment"* — The environment requires accounting: the measurement of value created, consumed, and retained |
| **One-line Definition** | The accounting for the environment: the flow of money and the measurement of value created, consumed, and retained |

### After

| Attribute | Final |
| :--- | :--- |
| **Domain Name** | Finance & Accounting |
| **Semantic Anchor** | Money |
| **Axiomatic Grounding** | *"with its environment"* — the environment requires measurement; value exchanged must be quantified in monetary terms |
| **Enhanced Definition** | The domain that manages the enterprise's monetary reality. It owns the planning, allocation, movement, recording, and reporting of money as it flows through the enterprise in exchange with its environment. The domain manages money as a stable subject: the universal medium through which all enterprise activity is measured, compared, and controlled in monetary terms. It is explicitly not the domain of "value" in the abstract; it is the domain of monetary consequence. |

### What Changed

| Aspect | Before | After | Rationale |
| :--- | :--- | :--- | :--- |
| Name | Finance & Value | Finance & Accounting | "Value" is a generic enterprise outcome created by Product, realized by Operations, measured by Finance, and directed by Strategy. No single domain can own "Value" without violating MECE. "Accounting" correctly scopes the domain to monetary measurement |
| Anchor | Flow of money + measurement of value | **Money** | Money is the stable, lifecycle-complete subject. "Value" is an outcome, not a manageable subject |
| Scope | "flow of money and measurement of value created, consumed, retained" | Full monetary lifecycle: planning → funding → allocation → commitment → transaction → recording → reconciliation → reporting → accounting | Expanded to include forward-looking finance (FP&A, treasury, investment) alongside backward-looking accounting |
| Boundary | Implicit, ambiguous ("value" is overloaded) | Explicit: owns monetary consequences; does NOT own general enterprise value, product value proposition, or operational cost drivers | Prevents collision with Product & Value (value proposition), Operations (cost drivers), Strategy (investment choices) |

### Why "Value" Failed the Boundary Integrity Test

| Problem | Explanation |
| :--- | :--- |
| Overloaded term | "Value" means different things in different contexts: customer value, product value, enterprise value, shareholder value, social value |
| Cross-cutting outcome | Value is created by Product, delivered by Operations, measured by Finance, directed by Strategy. It belongs to no single domain |
| Collision risk | If Finance owns "Value", then Product & Value cannot exist as a domain. The two domains would fight over the same semantic territory |

### Internal MECE Partition (New)

| Sub-concern | Scope |
| :--- | :--- |
| Financial Planning | Budgeting, forecasting, investment appraisal, capital allocation |
| Funding & Capital | Capital structure, equity, debt, grants, fundraising, treasury |
| Transaction & Exchange | Invoicing, billing, payments, receipts, foreign exchange, settlement |
| Accounting & Recording | General ledger, cost accounting, revenue recognition, reconciliation |
| Reporting & Disclosure | Financial statements, management reporting, regulatory disclosure, tax reporting |
| Financial Control | Internal controls, audit support, fraud prevention, financial risk management |

---

## Final Comparison Table

| # | Original Domain | Original Description | Final Domain | Final Description |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Governance & Existence | The precondition of boundedness: what defines the entity, what rules apply, and the assurance that the other domains behave | **Governance & Existence** | The domain that constitutes the enterprise as a bounded, legitimate, persisting entity. It owns the enterprise's ontological reality and its constitutional machinery |
| 2 | Supply & Resources | The substrate the enterprise persists on: physical or virtual, owned or rented, and its capacity, health, and disposal | **Strategy & Direction** | The domain that determines the enterprise's intentional trajectory. It translates purpose into concrete choices about positioning, ambition, and priorities |
| 3 | People & Organization | The humans who perform every capability: their structure, skills, performance, and movement | **People & Organization** | The domain that manages the enterprise's internal human fabric: the constitution, coordination, development, and movement of agents and the structures through which they are organized |
| 4 | Customer & Demand | The enterprise's reason to exchange: identifying, acquiring, serving, and retaining the people whose need it meets | **Party & Relationship** | The domain that manages the enterprise's external social fabric: the identification, establishment, development, and termination of bonds with all external entities |
| 5 | Product & Offering | The catalog of what the enterprise offers: its design, packaging, release, and retirement | **Product & Value** | The domain that manages the enterprise's value-bearing propositions: the complete lifecycle of whatever the enterprise creates, shapes, and makes available for exchange |
| 6 | Operations & Delivery | The engine that turns an offering into a delivered outcome: planning, fulfilling, running, resolving | **Operations & Enablement** | The domain that manages the enterprise's execution engine and the means that make execution possible: processes, delivery, technology, and physical infrastructure |
| 7 | Finance & Value | The accounting for the environment: the flow of money and the measurement of value created, consumed, and retained | **Finance & Accounting** | The domain that manages the enterprise's monetary reality: the planning, allocation, movement, recording, and reporting of money in exchange with the environment |

---

## Axiomatic Mapping: Before vs. After

| Axiom Word | Original Domain | Final Domain | Change |
| :--- | :--- | :--- | :--- |
| "bounded entity" | Governance & Existence | Governance & Existence | Retained |
| "persists" (substrate) | Supply & Resources | Operations & Enablement (as enablers) | Redistributed |
| "persists" (agents) | People & Organization | People & Organization | Retained |
| "persists" (directed) | *(implicit)* | Strategy & Direction | **Added** |
| "exchanging value" (counterparty) | Customer & Demand | Party & Relationship | Expanded |
| "exchanging value" (what) | Product & Offering | Product & Value | Sharpened |
| "exchanging value" (mechanism) | Operations & Delivery | Operations & Enablement | Expanded |
| "with its environment" | Finance & Value | Finance & Accounting | Sharpened |

The axiom is now fully and rigorously satisfied with no orphaned concerns and no overlapping claims.