# The Canonical Foundation Matrix

The 7×7 matrix **M = D × S** is the framework's center of gravity. Every
business object lives in one cell — the intersection of its domain (row) and
its current lifecycle stage (column). Capabilities, events, actors, and
resources attach to cells.

## The Two Axes

### Domains (Rows) — Scope of Operations

The **domains** answer the question *what does the enterprise do?*

| # | Domain | One-line definition |
|---|--------|---------------------|
| 1 | Governance & Existence | The precondition of boundedness — what defines the entity, what rules apply, and the assurance that the other domains behave. |
| 2 | Supply & Resources | The substrate the enterprise persists on — physical or virtual, owned or rented — and its capacity, health, and disposal. |
| 3 | People & Organization | The humans who perform every capability — their structure, skills, performance, and movement. |
| 4 | Customer & Demand | The enterprise's reason to exchange: identifying, acquiring, serving, and retaining the people whose need it meets. |
| 5 | Product & Offering | The catalog of what the enterprise offers — its design, packaging, release, and retirement. |
| 6 | Operations & Delivery | The engine that turns an offering into a delivered outcome — planning, fulfilling, running, resolving. |
| 7 | Finance & Value | The accounting for the environment — the flow of money and the measurement of value created, consumed, and retained. |

### Stages (Columns) — Value Stream Stages

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

## The Foundation Matrix

The cell content at each (domain, stage) intersection:

| Domain \ Stage | Conceive | Design | Build | Activate | Operate | Improve | Retire |
|----------------|----------|--------|-------|----------|---------|---------|--------|
| **Governance & Existence** | Policy intent | Controls design | Compliance build | Enforce | Assurance | Risk review | Policy retire |
| **Supply & Resources** | Capacity vision | Architecture | Build / procure | Integration | Monitoring | Utilization | Retire assets |
| **People & Organization** | Workforce plan | Org design | Hire / train | Mobilize | Perform & develop | Engagement | Offboard / reassign |
| **Customer & Demand** | Need identification | Journey mapping | Onboarding | Activation | Support & service | Satisfaction & churn | Offboarding |
| **Product & Offering** | Market sensing | Catalog & specs | Configuration | Launch | Catalog mgmt | Performance | Sunset |
| **Operations & Delivery** | Demand planning | Process design | Provisioning | Cut-over | Run & maintain | Quality & incident | Decommission |
| **Finance & Value** | Business case | Pricing model | Funding | Billing activation | Revenue & cost | Margin analysis | Write-off |

## Patterns the Foundation Reveals

1. **Diagonal flow.** Objects move left to right across rows; the matrix
   makes the lifecycle visible as motion.
2. **Column coupling.** Adjacent stages share events — a Build exit is an
   Activate entry — surfacing handoff risks.
3. **Row completeness.** A sparse row signals a neglected domain; a sparse
   column signals a skipped stage.

## Construction Rules

1. **Map domains to rows.** Place each of the seven domains on a row, in
   axiomatic order: governance first, finance last.
2. **Map stages to columns.** Place each of the seven stages on a column,
   left to right, in lifecycle order.
3. **Place objects in cells.** Each business object goes in the cell at the
   intersection of its domain and its current stage.
4. **One object, one primary cell.** If an object spans domains, model it as
   a linking object — never duplicate it across rows.
5. **Capabilities map to earliest stage.** A capability belongs to the stage
   where it is first initiated, not where it runs longest.
6. **Attach capabilities.** Within each cell, list the capabilities that act
   on those objects.
7. **Mark events and actors.** Annotate each cell with the events that
   trigger transitions and the actors who perform.
8. **Version the matrix.** Snapshot at each planning cycle; diff to see
   what moved.

## Value Stream Overlay Routes

Cross-cutting concerns are modeled as *directed graphs routing through
specific cells* — not as blanket layers draped over the whole grid. A route
names the handoffs; a layer does not.

**Commercialization route:**
```
Finance × Design     → pricing
Product × Activate   → channel launch
Operations × Operate  → perform
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
- **Overloading a cell:** stuffing a cell with objects from another domain
  to avoid creating a new row.
- **Skipping stages:** assuming an object is "born live." Every object has a
  Conceive and a Build stage.
- **Static matrix:** treating the matrix as a one-time diagram. It must
  version with the enterprise.

## MECE Sub-Decomposition

### Domain Subdomains

| Domain | Subdomains |
|--------|-----------|
| Governance & Existence | Policy, Controls, Compliance, Assurance, Retirement |
| Supply & Resources | Capacity, Build/procure, Integration, Monitoring, Disposal |
| People & Organization | Planning, Acquisition, Mobilization, Development, Exit |
| Customer & Demand | Acquisition, Onboarding, Care & support, Retention, Offboarding |
| Product & Offering | Catalog, Packaging, Pricing, Lifecycle, Sunset |
| Operations & Delivery | Planning, Fulfillment, Run, Incident, Decommission |
| Finance & Value | Business case, Funding, Billing, Revenue, Recovery |

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

## Recursive Self-Similarity

Any cell can be decomposed into its own 7×7 sub-matrix — the cell's objects
become the enterprise described by the sub-matrix. This gives infinite depth
without changing the top-level logic. The framework scales because it does
not grow; it recurses. A 50-person charity and a 500,000-person telco
occupy the same grid — only the depth of decomposition differs.