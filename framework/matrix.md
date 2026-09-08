# The Canonical Foundation Matrix

The 7x7 matrix **M = D x S** is the framework's center of gravity. It
provides 49 ECF coordinates: the cartesian product of seven Domains and
seven Stages. Each coordinate is a classification context in which
enterprise concepts (objects, capabilities, processes, events, actors,
resources) may be considered. A coordinate is not an entity container.

## The Two Axes

### Domains (Rows): Scope of Operations

The **domains** answer the question *what does the enterprise do?*

| # | Domain | One-line definition |
|---|--------|---------------------|
| 1 | Governance & Existence | The domain that constitutes the enterprise as a bounded, legitimate, persisting entity; the precondition of all other domains. |
| 2 | Strategy & Direction | The domain that determines the enterprise's intentional trajectory; positioning, ambition, and resource allocation priorities. |
| 3 | Agency & Organization | The domain that manages the enterprise's internal agentive fabric; the constitution, coordination, development, and lifecycle of all agents (biological, artificial, hybrid) that perform capabilities, and the organizational structures through which their agency is channeled. Substrate-independent: see ADR-ECF-002 §5 and CR-ECF-007. |
| 4 | Party & Relationship | The domain that manages the enterprise's external social fabric; the identification, establishment, development, and termination of bonds with all external entities. |
| 5 | Product & Value | The domain that manages the enterprise's value-bearing propositions; the complete lifecycle of whatever the enterprise creates and makes available for exchange. |
| 6 | Enablement & Operations | The domain that manages the enterprise's execution engine and the means that make execution possible; processes, delivery, technology, and physical infrastructure. |
| 7 | Finance & Accounting | The domain that manages the enterprise's monetary reality; the planning, allocation, movement, recording, and reporting of money in exchange with the environment. |

### Stages (Columns): Value Stream Stages

The **stages** answer the question *how does the work evolve?*

| # | Stage (short) | Stage (full) | One-line definition |
|---|---------------|-------------|---------------------|
| 1 | Conceive | Conceive | Naming the need, the opportunity, the policy. The enterprise decides what should exist. |
| 2 | Design | Design | Specifying the object, the process, the controls. The enterprise shapes what it will build. |
| 3 | Build | Build / Acquire | Constructing, provisioning, hiring, or buying. The object becomes real but is not yet live. |
| 4 | Activate | Deploy / Activate | Cutting over, launching, mobilizing. The object enters service and begins to deliver value. |
| 5 | Operate | Operate / Deliver | Running, serving, monitoring, maintaining. Where the object spends most of its life. |
| 6 | Improve | Measure / Learn | Measuring performance, learning from incidents, scoring satisfaction. The enterprise decides what to change. |
| 7 | Retire | Retire / Renew | Sunsetting, migrating, recovering, or renewing. The object exits its current form. |

## Foundation Matrix Content

The cell content at each (domain, stage) intersection names the typical
work performed when an enterprise concept is considered in that context.
Whether zero, one, or many modeled elements are appropriate within a
context is determined by the consuming catalog.

| Domain \ Stage | Conceive | Design | Build | Activate | Operate | Improve | Retire |
|----------------|----------|--------|-------|----------|---------|---------|--------|
| **Governance & Existence** | Policy intent | Controls design | Compliance build | Enforce | Assurance | Risk review | Policy retire |
| **Strategy & Direction** | Purpose & ambition | Strategic choices | Initiative portfolio | Launch direction | Course correction | Performance review | Strategic renewal |
| **Agency & Organization** | Capacity plan | Org design | Acquire / onboard | Mobilize | Perform & develop | Coordination | Offboard / reassign |
| **Party & Relationship** | Need identification | Journey mapping | Onboarding | Activation | Support & service | Satisfaction & churn | Offboarding |
| **Product & Value** | Market sensing | Catalog & specs | Configuration | Launch | Catalog mgmt | Performance | Sunset |
| **Enablement & Operations** | Demand planning | Process design | Provisioning | Cut-over | Run & maintain | Quality & incident | Decommission |
| **Finance & Accounting** | Business case | Pricing model | Funding | Billing activation | Revenue & cost | Margin analysis | Write-off |

## Patterns the Foundation Reveals

1. **Diagonal flow.** Concepts move left to right across rows as their
   lifecycle context shifts; the matrix makes the lifecycle visible as
   motion.
2. **Column coupling.** Adjacent stages share events; a Build exit is an
   Activate entry, surfacing handoff risks.
3. **Row completeness.** A sparse row signals a neglected domain; a sparse
   column signals a skipped stage.

## Construction Rules

1. **Map domains to rows.** Place each of the seven domains on a row, in
   axiomatic order: governance first, finance last.
2. **Map stages to columns.** Place each of the seven stages on a column,
   left to right, in lifecycle order.
3. **Contextualize concepts by coordinates.** Each enterprise concept is
   contextualized by one or more `(Domain, Stage)` coordinates according to
   the semantics of the consuming model.
4. **Multi-coordinate contextualization is supported where legitimate.** A
   single concept may participate in multiple coordinates (governed by the
   consuming catalog); the existence of multiple coordinates does not imply
   multiple identities.
5. **Capability identity is independent of coordinate.** A capability has
   its own semantic identity and business meaning; the ECF coordinate is
   classification context, not capability identity.
6. **Mark events and actors.** Annotate each context with the events that
   trigger transitions and the actors who perform.
7. **Version the matrix.** Snapshot at each planning cycle; diff to see
   what moved.

## Value Stream Overlay Routes

Cross-cutting concerns are modeled as *directed graphs routing through
specific cells*: not as blanket layers draped over the whole grid. A route
names the handoffs; a layer does not.

**Commercialization route:**
```
Finance × Design     → pricing
Product × Activate   → channel launch
Enablement & Operations × Operate → perform
Finance × Operate     → bill
Finance × Measure     → margin
```

**Statutory compliance route:**
```
Governance × Conceive → mandate
Governance × Design   → controls
Governance × Build    → evidence
Governance × Activate → enforce
Governance × Operate  → assure
```

## Anti-Patterns

- **Mixing axes:** putting a stage inside the domain column. The axes must
  stay orthogonal.
- **Overloading a coordinate:** treating a coordinate as a container for
  every object in a domain, irrespective of context.
- **Skipping stages:** assuming an object is "born live." Every object has a
  Conceive and a Build stage.
- **Static matrix:** treating the matrix as a one-time diagram. It must
  version with the enterprise.

## MECE Sub-Decomposition

### Domain Subdomains

| Domain | Subdomains |
|--------|-----------|
| Governance & Existence | Formation, Mandate, Policy, Compliance, Assurance, Succession |
| Strategy & Direction | Purpose, Sensing, Choices, Objectives, Planning, Adaptation |
| Agency & Organization | Design, Planning, Acquisition, Development, Coordination, Transition |
| Party & Relationship | Identification, Establishment, Engagement, Development, Governance, Termination |
| Product & Value | Proposition, Portfolio, Development, Packaging, Readiness, Evolution |
| Enablement & Operations | Process, Fulfillment, Technology, Physical, Planning, Assurance |
| Finance & Accounting | Planning, Capital, Transaction, Recording, Reporting, Control |

### Stage Substages

| Stage | Substages |
|-------|----------|
| Conceive | Sense, Frame, Decide |
| Design | Specify, Review, Baseline |
| Build / Acquire | Provision, Configure, Accept |
| Deploy / Activate | Integrate, Cut-over, Verify |
| Operate / Deliver | Run, Monitor, Resolve |
| Measure / Learn | Collect, Analyze, Decide |
| Retire / Renew | Migrate, Recover, Archive |

## Recursive Applicability

An ECF coordinate may be used as the organizing context for a further
specialized model. The specialization is not required and does not imply
that every coordinate must be recursively decomposed.

ECF recursion is independent of Business Process decomposition. The
Business Process Architecture defines its own process topology
(Process Context -> L0 Process Scope -> L1 Process Group -> L2 Business
Process -> L3 Activity -> L4 Task); the ECF provides the coordinate
context, not the process hierarchy.