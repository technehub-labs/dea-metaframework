# ECF Domain Grounding

Status: Normative (CR-ECF-003, extended by CR-ECF-006)
Scope: the seven ECF Domains, their compound-name boundaries, and the formal
grounding record for each Domain.

The seven Domains are derived from the grounding axiom recorded in
[`axiom.md`](./axiom.md):

> An enterprise is any bounded entity that persists by exchanging value with
> its environment.

Each Domain is a logical consequence of a word in the axiom. No Domain is
asserted; each is grounded. This file records the formal grounding record for
each Domain and the compound-name boundary audit.

Each Domain satisfies five tests (per ADR-ECF-001):

1. **Semantic Anchor**; a single, stable, manageable subject
2. **Lifecycle Completeness**; meaningful from conception through dissolution
3. **Boundary Integrity**; precise inclusion/exclusion rules
4. **Technology Independence**; survives any technological paradigm shift
5. **Collective Exhaustiveness**; seven Domains partition the enterprise without remainder

## 1. Grounding Record Template

Every Domain carries:

| Field | Meaning |
|-------|---------|
| Axiom grounding | which word(s) in the axiom generate the Domain |
| Semantic definition | what the Domain means |
| Semantic anchor | the stable subject the Domain name identifies |
| Included concerns | concerns within scope |
| Excluded concerns | concerns explicitly out of scope |
| Adjacent Domains | Domains that share concerns and require boundary rules |
| Boundary rules | how overlap with adjacent Domains is resolved |
| Internal MECE partition | the sub-concerns that partition the Domain without remainder |
| Evidence / rationale | case-study and derivation evidence |

## 2. Compound-Domain Boundary Audit

The seven Domain names are compounds. Each compound is audited and a verdict
recorded.

| Compound | Verdict |
|----------|---------|
| Governance + Existence | semantically necessary: the precondition of boundedness spans the rules and the entity that owns them |
| Strategy + Direction | semantically necessary: the intentional vector and the steering that maintains it; replaces the prior Supply + Resources, which was a non-substrate (assets, not direction) and failed MECE |
| People + Organization | semantically necessary: agents require structure; the anchor is organization (the stable subject), with people as the agentive constituent |
| Party + Relationship | semantically necessary: the entity (Party) and the bond (Relationship) are inseparable complements; replaces the prior Customer + Demand, which was sell-side biased and treated demand (a signal) as a subject |
| Product + Value | semantically necessary: the bearer of value (Product) and the proposition it carries (Value) are inseparable complements; replaces the prior Product + Offering, where "Offering" overlapped with "Product" without distinguishing the value proposition |
| Operations + Enablement | semantically necessary: the execution (Operations) and the means that make it possible (Enablement: technology, physical infrastructure) are inseparable complements; replaces the prior Operations + Delivery, which treated delivery as an outcome of execution rather than naming the enablement concern |
| Finance + Accounting | semantically necessary: planning (Finance) and recording (Accounting) are inseparable complements; replaces the prior Finance + Value, where "Value" was overloaded and created boundary collision with Product + Value |

No decomposition is introduced at this stage. Compounds are retained as a
single Domain identifier; the audit record is the artefact, not a renaming.
A future CR may revisit any compound if evidence accumulates.

**Note (CR-ECF-008; 2026-09-08)**: the `Operations + Enablement` compound
was renamed to `Enablement + Operations` by CR-ECF-008 (see §3.6 below
for the updated grounding record and the Domain/Stage orthogonality
rationale). The two nouns are unchanged; only their order in the Domain
name changed. The rationale for the rename is recorded in
[`ADR-ECF-003`](../docs/adr/ADR-ECF-003.md): the leading noun
`Operations` shared a lexical root with Stage 5 `Operate`, obscuring
the Domain/Stage orthogonality that the ECF requires. The renamed
compound puts `Enablement` first (lexically distinct from any Stage
name) and retains `Operations` as the trailing noun (the sustained
day-to-day concern, not the lifecycle Stage).

## 3. Domain Grounding Records

### 3.1 Governance & Existence

- **Axiom grounding**: "bounded entity": boundedness requires a boundary,
  authority, and the assurance that the entity persists as itself.
- **Semantic definition**: the domain that constitutes the enterprise as a
  bounded, legitimate, persisting entity. It owns the enterprise's
  ontological reality (what it is, why it is legitimate, under what authority
  it operates) and its constitutional machinery (how decisions are
  authorized, constrained, and assured). It is the precondition of all other
  domains.
- **Semantic anchor**: Enterprise Existence.
- **Included concerns**: entity charter; legal constitution; policy and
  standards; risk frameworks; controls; compliance; assurance; policy
  retirement; mandate and authority; dissolution and succession.
- **Excluded concerns**: people performing governance work (People &
  Organization); tooling that enforces controls (Enablement & Operations);
  monetary accounting of compliance cost (Finance & Accounting); strategic
  choices about direction (Strategy & Direction).
- **Adjacent Domains**: Agency & Organization (governance vs management);
  Enablement & Operations (controls vs run-time enforcement); Finance &
  Accounting (assurance vs audit); Strategy & Direction (constitutional
  authority vs deliberate choice of trajectory).
- **Boundary rules**: Governance & Existence owns the rules and the assurance
  that the rules hold; the run-time enforcement and the people performing
  governance work live in adjacent Domains and reference Governance &
  Existence coordinates. Governance & Existence authorizes but does not
  direct; Strategy & Direction directs within the authorized frame.
- **Internal MECE partition**: Formation & Identity; Mandate & Authority;
  Policy & Control; Risk & Compliance; Assurance & Accountability;
  Dissolution & Succession.
- **Evidence / rationale**: REPORT §5.1; the axiom-derivation table in
  [`axiom.md`](./axiom.md); the Telecom and Digital Services case studies
  place assurance, risk, and policy concerns in this Domain. The compound
  (governance + existence) is justified because boundedness is constituted
  by the rules and the entity that owns them; one without the other is not
  governance.

### 3.2 Strategy & Direction

- **Axiom grounding**: "persists": persistence is not mere survival; it
  requires deliberate, adaptive steering toward a future state.
- **Semantic definition**: the domain that determines the enterprise's
  intentional trajectory. It translates the enterprise's reason for existing
  (owned by Governance & Existence) into concrete choices about positioning,
  ambition, and resource allocation priorities. The domain manages direction
  as a stable subject: not the strategy document, not the planning ritual,
  but the enterprise's deliberate determination of where it will go, what
  it will become, and what it will prioritize.
- **Semantic anchor**: Direction.
- **Included concerns**: purpose and ambition; environmental sensing;
  strategic choices; objectives and targets; strategic planning; strategic
  adaptation.
- **Excluded concerns**: legal mandate and constitutional authority
  (Governance & Existence); operational execution of strategy (Operations &
  Enablement); monetary budgets and financial plans (Finance & Accounting);
  product design and portfolio decisions (Product & Value); relationships
  with market participants (Party & Relationship); organizational redesign
  execution (Agency & Organization).
- **Adjacent Domains**: Governance & Existence (authorized frame vs chosen
  trajectory); Enablement & Operations (strategy vs execution); Finance &
  Accounting (strategic investment choices vs monetary plans); Product &
  Value (portfolio evolution direction vs product design); Party &
  Relationship (target segments vs relationships); Agency & Organization
  (capability requirements vs organization design).
- **Boundary rules**: Strategy & Direction provides the intentional vector
  that all execution Domains follow. It decides where and why; it does not
  decide how (Operations), what (Product), with whom (Party), with what
  money (Finance), or with what people (People).
- **Internal MECE partition**: Purpose & Ambition; Environmental Sensing;
  Strategic Choices; Objectives & Targets; Strategic Planning; Strategic
  Adaptation.
- **Evidence / rationale**: REPORT §5.1; the axiom-derivation table;
  standard frameworks (APQC, TOGAF) treat strategy as a mandatory L0
  process category. The prior Domain "Supply & Resources" was removed
  because "Resources" is a cross-cutting asset class, not a stable
  subject: physical resources moved to Enablement & Operations (as
  enablers); financial resources moved to Finance & Accounting; human
  resources stay in Agency & Organization. The vacated axiom slot
  ("persists" as deliberate steering) maps cleanly to this new Domain.

### 3.3 Agency & Organization

- **Axiom grounding**: "persists" — persistence requires agents; the
  enterprise cannot act without agents organized for purpose. The axiom
  requires *agency*, not *biology*: the substrate-independent capacity to
  act on behalf of the enterprise.
- **Semantic definition**: the domain that manages the enterprise's
  internal agentive fabric. It owns the constitution, coordination,
  development, and lifecycle of all agents that perform enterprise
  capabilities, and the organizational structures through which their
  agency is channeled. The domain is **substrate-independent**: it
  encompasses biological agents (humans), artificial agents (AI systems,
  autonomous software agents), and hybrid human-AI configurations
  without requiring reclassification. The domain manages organization
  as a stable subject: the durable pattern of roles, authority,
  collaboration, and coordination through which agency is directed.
  Agency is the agentive constituent (the capacity to act); organization
  is the structure that channels that capacity.
- **Semantic anchor**: Organization.
- **Fundamental enterprise question**: how is agency constituted and
  coordinated?
- **Definitional note**: "Agency" refers to the *capacity to act on
  behalf of the enterprise* — the quality that makes an entity a
  constituent of the enterprise's internal workforce. The term is
  substrate-independent and encompasses biological agents (humans),
  artificial agents (AI systems, autonomous software agents), and hybrid
  configurations. The semantic anchor remains **Organization**: the
  structure through which agency is coordinated. The term "People" is
  not used as a domain-level identifier because it is biologically
  loaded and fails the Technology Independence test (ADR-ECF-002 §3.2
  Test 4).
- **Included concerns**: organizational design; agent capacity planning;
  acquisition and onboarding; development and performance; coordination
  and collaboration; movement and transition.
- **Excluded concerns**: external parties (Party & Relationship);
  strategic direction (Strategy & Direction); governance authority and
  policy (Governance & Existence); operational execution they perform
  (Enablement & Operations); monetary compensation decisions (Finance &
  Accounting); product work they produce (Product & Value).
- **Adjacent Domains**: Governance & Existence (rules that govern
  organizational behaviour); Strategy & Direction (capability
  requirements vs direction); Enablement & Operations (agents vs the
  engine they staff); Party & Relationship (internal agents vs external
  parties); Finance & Accounting (compensation accounting vs
  compensation decisions).
- **Boundary rules**: Agency & Organization owns agents and the
  structure that organizes them. Agents-as-counterparties are not
  modelled here; they live in Party & Relationship.
- **Internal MECE partition** (substrate-independent sub-concerns):
  Organizational Design; Agent Capacity Planning; Acquisition &
  Onboarding; Development & Performance; Coordination & Collaboration;
  Movement & Transition. Each sub-concern is interpretable for both
  biological and artificial agents (e.g., "Acquisition & Onboarding"
  covers recruitment *and* model deployment / API integration).
- **Lifecycle applicability**: Conception (define required agent
  capabilities and organizational structure); Design (design
  organizational architecture, agent topology, role definitions,
  authority chains); Build (acquire/provision agents, onboard,
  configure, integrate); Operate (monitor performance, coordinate
  collaboration, manage capacity); Improvement (develop capabilities,
  retrain or fine-tune, reorganize); Retirement (decommission agents,
  offboard, archive organizational knowledge); Dissolution (wind down
  organizational structure, release agents, archive records).
- **Evidence / rationale**: REPORT §5.1; `dea-catalog-actors` patterns;
  the anchor (organization, not agents) prevents the domain from being
  reduced to "HR management." The compound (agency + organization) is
  justified because the agents require the structure and the structure
  exists to channel the agents. The rename from "People & Organization"
  (v2.3.0) is governed by ADR-ECF-002 §5 (Substrate Independence
  Stress Test) and CR-ECF-007.

### 3.4 Party & Relationship

- **Axiom grounding**: "exchanging value": exchange requires a counterparty;
  the enterprise cannot exchange with itself.
- **Semantic definition**: the domain that manages the enterprise's external
  social fabric. It owns the identification, establishment, development, and
  termination of bonds between the enterprise and all external entities with
  whom it interacts. The domain manages relationships as stable subjects with
  full lifecycle integrity, not merely the transactional events that occur
  within them. It encompasses all external parties regardless of their role
  (customer, supplier, partner, regulator, community).
- **Semantic anchor**: Relationship.
- **Included concerns**: party identification; relationship establishment;
  engagement and interaction; relationship development; relationship
  governance; relationship termination.
- **Excluded concerns**: internal agents (Agency & Organization); the
  product or service exchanged (Product & Value); monetary transactions and
  records (Finance & Accounting); operational fulfillment of exchanges
  (Enablement & Operations); strategic targeting decisions (Strategy &
  Direction); legal entity constitution (Governance & Existence).
- **Adjacent Domains**: Product & Value (demand for the offering vs the
  offering itself); Agency & Organization (internal-agent agents vs
  counterparty parties); Finance & Accounting (relationship accounting vs
  monetary measurement); Strategy & Direction (targeting vs market
  intelligence); Enablement & Operations (engagement management vs
  fulfillment execution).
- **Boundary rules**: Party & Relationship owns the counterparty
  relationship and the bond. The offering that meets the need lives in
  Product & Value; the financial accounting of relationship value lives in
  Finance & Accounting. A single party may simultaneously be a customer, a
  supplier, and a partner; the party is one entity with multiple roles, and
  the relationship is a single bond with multiple facets, not three separate
  domains.
- **Internal MECE partition**: Party Identification; Relationship
  Establishment; Engagement & Interaction; Relationship Development;
  Relationship Governance; Relationship Termination.
- **Evidence / rationale**: REPORT §5.1; the prior Domain "Customer &
  Demand" was renamed and broadened because "Customer" is a role a party
  plays (a single party can be customer, supplier, and partner
  simultaneously), and "Demand" is a transient signal rather than a
  manageable subject. Party + Relationship is MECE-complete for the
  external environment.

### 3.5 Product & Value

- **Axiom grounding**: "exchanging value": exchange requires something to
  offer; a bearer of value must exist to be exchanged.
- **Semantic definition**: the domain that manages the enterprise's
  value-bearing propositions. It owns the complete lifecycle of whatever the
  enterprise creates, shapes, packages, and makes available for exchange
  with external parties. The domain manages products as stable subjects: not
  merely physical goods, but any value-bearing entity (services, solutions,
  experiences, platforms, intellectual property) that the enterprise designs,
  builds, evolves, and eventually retires. The critical boundary: Product &
  Value owns the value-bearing proposition, not every form of value in the
  enterprise.
- **Semantic anchor**: Product.
- **Included concerns**: proposition design; portfolio management; product
  development; packaging and configuration; market readiness; product
  evolution.
- **Excluded concerns**: relationships with buyers (Party & Relationship);
  monetary pricing decisions (Finance & Accounting); operational delivery
  of the product (Enablement & Operations); strategic portfolio investment
  decisions (Strategy & Direction); technology platforms that enable
  products (Enablement & Operations); legal governance of IP (Governance &
  Existence).
- **Adjacent Domains**: Party & Relationship (offering vs demand);
  Enablement & Operations (offering vs the engine that delivers it);
  Finance & Accounting (offering vs the financial model around it);
  Strategy & Direction (product direction vs strategic direction).
- **Boundary rules**: Product & Value owns the value-bearing proposition
  itself. Delivery of the offering is Enablement & Operations; pricing of
  the offering is Finance & Accounting. "Value" in this Domain's name
  refers to the value proposition carried by the product, not to
  enterprise-wide value (which is a cross-cutting outcome).
- **Internal MECE partition**: Proposition Design; Portfolio Management;
  Product Development; Packaging & Configuration; Market Readiness; Product
  Evolution.
- **Evidence / rationale**: REPORT §5.1; `dea-catalog-digital-business-service-factory`
  and `dea-catalog-solution-hub` patterns. The compound (product + value) is
  justified because the bearer of value (Product) and the value proposition
  (Value) it carries are inseparable complements; "Offering" in the prior
  compound was vague and overlapped with "Product" without distinguishing
  the value proposition.

### 3.6 Enablement & Operations

- **Axiom grounding**: "exchanging value": exchange requires a mechanism;
  value must be produced, delivered, and sustained.
- **Semantic definition**: the domain that establishes, sustains, and governs
  the means and mechanisms through which the enterprise executes, delivers,
  and maintains its capabilities and value exchanges. It encompasses the
  operational processes, enabling technology, physical and virtual
  infrastructure, service mechanisms, and operational controls required to
  make enterprise execution possible and sustainable. The domain manages
  execution as a stable subject: the repeatable, manageable, measurable
  engine that produces outcomes. Technology, platforms, and physical assets
  are positioned as enablers of execution, not as ends in themselves.
- **Semantic anchor**: Execution.
- **Fundamental question**: *How does the enterprise enable and sustain
  execution?*
- **Normative Domain/Stage distinction (CR-ECF-008 §6)**:
  Domain 6, Enablement & Operations, is a persistent semantic domain
  concerned with enabling and sustaining enterprise execution. Stage 5,
  Operate, is a lifecycle stage describing the context in which a
  particular enterprise concept is actively run, delivered, monitored,
  maintained, or otherwise operated. The term "Operations" in the Domain
  name denotes sustained enterprise day-to-day and ongoing activities as
  a persistent capability concern; it does not identify or absorb the
  ECF Operate lifecycle Stage.
- **Included concerns**: process design and management; execution and
  fulfillment; technology enablement; physical enablement; operational
  planning; operational assurance.
- **Excluded concerns**: strategic direction for operations (Strategy &
  Direction); product design and portfolio decisions (Product & Value);
  monetary capital expenditure decisions (Finance & Accounting);
  relationships with counterparties (Party & Relationship); organizational
  structure of operations teams (Agency & Organization); governance policies
  that constrain operations (Governance & Existence).
- **Adjacent Domains**: Strategy & Direction (engine vs direction);
  Product & Value (engine vs offering); Finance & Accounting (delivered
  outcome vs financial recognition); Party & Relationship (fulfillment vs
  relationship); Agency & Organization (execution agents vs organizational
  design); Governance & Existence (operational enforcement vs policy).
- **Boundary rules**: Enablement & Operations owns the execution mechanism
  and the means that enable it. Technology, platforms, and physical
  infrastructure are positioned as enablers of execution (not as a separate
  Domain) so that the Domain survives any technological paradigm shift
  (Technology Independence test, ADR-ECF-001 §4). Physical and virtual
  resources that previously sat in "Supply & Resources" now live here as
  enablers.
- **Internal MECE partition**: Process Design & Management; Execution &
  Fulfillment; Technology Enablement; Physical Enablement; Operational
  Planning; Operational Assurance.
- **Evidence / rationale**: REPORT §5.1; the Business Process Catalog's
  L0..L4 topology and the telecom run/assure patterns. The compound
  (enablement + operations) is justified because execution requires the
  means; the prior "Delivery" named only an outcome of execution and
  omitted the enablement concern that the absorption of "Supply & Resources"
  brings in. The compound order was swapped from `Operations + Enablement`
  to `Enablement + Operations` by CR-ECF-008 (2026-09-08) to reduce the
  lexical collision with Stage 5 `Operate` and to make the Domain/Stage
  orthogonality explicit (see [`ADR-ECF-003`](../docs/adr/ADR-ECF-003.md)
  §5 for the analysis).

### 3.7 Finance & Accounting

- **Axiom grounding**: "with its environment": the environment requires
  measurement; value exchanged must be quantified in monetary terms.
- **Semantic definition**: the domain that manages the enterprise's monetary
  reality. It owns the planning, allocation, movement, recording, and
  reporting of money as it flows through the enterprise in exchange with its
  environment. The domain manages money as a stable subject: the universal
  medium through which all enterprise activity is measured, compared, and
  controlled in monetary terms. It is explicitly not the domain of "value"
  in the abstract; it is the domain of monetary consequence.
- **Semantic anchor**: Money.
- **Included concerns**: financial planning; funding and capital;
  transaction and exchange; accounting and recording; reporting and
  disclosure; financial control.
- **Excluded concerns**: general enterprise value (a cross-cutting outcome);
  strategic investment choices (Strategy & Direction); product value
  proposition (Product & Value); operational cost drivers (Operations &
  Enablement); governance authority for financial controls (Governance &
  Existence); people decisions about who to pay (Agency & Organization).
- **Adjacent Domains**: all other Domains; Finance & Accounting
  intersects every Domain because every Domain produces and consumes
  monetary consequence. Product & Value (revenue/cost recognition);
  Enablement & Operations (capex/opex accounting); Strategy & Direction
  (investment appraisal); Party & Relationship (receivables/payables);
  Agency & Organization (payroll/benefits accounting); Governance &
  Existence (audit/compliance accounting).
- **Boundary rules**: Finance & Accounting owns the monetary model and the
  measurement of monetary consequence. The sources of monetary consequence
  live in their owning Domains; Finance & Accounting provides the
  accounting lens. "Value" in the prior compound was overloaded; "Accounting"
  correctly scopes the Domain to monetary measurement.
- **Internal MECE partition**: Financial Planning; Funding & Capital;
  Transaction & Exchange; Accounting & Recording; Reporting & Disclosure;
  Financial Control.
- **Evidence / rationale**: REPORT §5.1; the Commercialization route in
  REPORT §8.2; `dea-catalog-metrics` patterns. The compound (finance +
  accounting) is justified because the planning (Finance) and the recording
  (Accounting) are inseparable complements; one without the other is not
  a complete monetary Domain.

## 4. Domain Orthogonality

Knowledge of a Domain does not determine a Stage; knowledge of a Stage
does not determine a Domain. A capability contextualized by
`(Party & Relationship, Conceive)` is meaningfully different from one
contextualized by `(Party & Relationship, Operate)`; a capability
contextualized by `(Finance & Accounting, Conceive)` is meaningfully
different from one contextualized by `(Party & Relationship, Conceive)`.
The seven Domains and the seven Stages remain independent partitions.

## 5. Domain Completeness

The seven Domains collectively cover the grounding axiom (per CR-ECF-006
axiomatic mapping):

- "bounded entity" -> Governance & Existence
- "persists" (substrate as enabler) -> Enablement & Operations
- "persists" (agents) -> Agency & Organization
- "persists" (directed) -> Strategy & Direction
- "exchanging value" (counterparty) -> Party & Relationship
- "exchanging value" (bearer of value) -> Product & Value
- "exchanging value" (mechanism) -> Enablement & Operations
- "with its environment" -> Finance & Accounting

No gap: each word is grounded. No hidden assumption: the derivation is the
axiom. No imported framework category: the Domain set is axiom-derived, not
reverse-engineered from a specific industry. Controlled overlap: the
boundary rules above resolve the apparent overlap between Finance &
Accounting and the other Domains.

## 6. Renaming Rule

No Domain is renamed or restructured without explicit evidence and
governance. A future CR (or an extension of CR-ECF-003 / CR-ECF-006) may
revisit any Domain if evidence accumulates; the change must cite the
evidence and the governance decision. CR-ECF-006 + ADR-ECF-001 are the
exemplar of this rule: the five renames and the Supply & Resources removal
are backed by the ADR's five-tests rubric and the CR's before/after audit.
