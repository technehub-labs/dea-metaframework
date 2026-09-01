# ECF Domain Grounding

Status: Normative (CR-ECF-003)
Scope: the seven ECF Domains and their compound-name boundaries

The seven Domains are derived from the grounding axiom recorded in
[`axiom.md`](./axiom.md):

> An enterprise is any bounded entity that persists by exchanging value with
> its environment.

Each Domain is a logical consequence of a word in the axiom. No Domain is
asserted; each is grounded. This file records the formal grounding record for
each Domain and the compound-name boundary audit.

## 1. Grounding Record Template

Every Domain carries:

| Field | Meaning |
|-------|---------|
| Axiom grounding | which word(s) in the axiom generate the Domain |
| Semantic definition | what the Domain means |
| Included concerns | concerns within scope |
| Excluded concerns | concerns explicitly out of scope |
| Adjacent Domains | Domains that share concerns and require boundary rules |
| Boundary rules | how overlap with adjacent Domains is resolved |
| Evidence / rationale | case-study and derivation evidence |

## 2. Compound-Domain Boundary Audit

The seven Domain names are compounds:

| Compound | Verdict |
|----------|---------|
| Governance + Existence | semantically necessary: the precondition of boundedness spans the rules and the entity that owns them |
| Supply + Resources | semantically necessary: substrate without capacity is not persistence |
| People + Organization | semantically necessary: agents require structure |
| Customer + Demand | semantically necessary: counterparty + the need that drives exchange |
| Product + Offering | semantically necessary: the offer must be packaged |
| Operations + Delivery | semantically necessary: offering + mechanism of delivery |
| Finance + Value | semantically necessary: exchange requires accounting and measurement |

No decomposition is introduced at this stage. Compounds are retained as a
single Domain identifier; the audit record is the artefact, not a renaming.
A future CR may revisit any compound if evidence accumulates.

## 3. Domain Grounding Records

### 3.1 Governance & Existence

- **Axiom grounding**: "bounded entity": boundedness requires a boundary,
  what defines the entity, what rules apply.
- **Semantic definition**: the precondition of boundedness; what defines the
  entity, what rules apply, and the assurance that the other domains behave.
- **Included concerns**: entity charter; policy and standards; risk; controls;
  compliance; assurance; policy retirement.
- **Excluded concerns**: people performing governance work (People & Organization);
  tooling that enforces controls (Supply & Resources; Operations & Delivery).
- **Adjacent Domains**: People & Organization (governance vs management);
  Operations & Delivery (controls vs run-time enforcement); Finance & Value
  (assurance vs audit).
- **Boundary rules**: Governance & Existence owns the rules and the assurance
  that the rules hold; the run-time enforcement and the people performing
  governance work live in adjacent Domains and reference Governance & Existence
  coordinates.
- **Evidence / rationale**: REPORT §5.1 and the derivation table in
  [`axiom.md`](./axiom.md); the Telecom and Digital Services case studies
  place assurance, risk, and policy concerns in this Domain.

### 3.2 Supply & Resources

- **Axiom grounding**: "persists": persistence requires a substrate.
- **Semantic definition**: the substrate the enterprise persists on;
  physical or virtual, owned or rented, and its capacity, health, and
  disposal.
- **Included concerns**: capacity planning; architecture; build and procure;
  integration; monitoring; utilization; retirement of assets.
- **Excluded concerns**: the people who run the substrate (People &
  Organization); the rules governing substrate use (Governance & Existence);
  the financial accounting for assets (Finance & Value).
- **Adjacent Domains**: Operations & Delivery (substrate vs the engine that
  runs on it); People & Organization (assets vs agents); Finance & Value
  (capacity vs accounting for capacity).
- **Boundary rules**: Supply & Resources owns the substrate and its capacity;
  Operations & Delivery owns the run-time usage of the substrate. A
  capability that provisions capacity lives in Supply & Resources; the
  capability that consumes capacity at run-time lives in Operations &
  Delivery.
- **Evidence / rationale**: REPORT §5.1 and the derivation table;
  `dea-catalog-digital-business-service-factory` and `dea-catalog-reference-models`
  patterns.

### 3.3 People & Organization

- **Axiom grounding**: "persists": persistence requires agents.
- **Semantic definition**: the humans who perform every capability; their
  structure, skills, performance, and movement.
- **Included concerns**: workforce planning; organizational design; hiring
  and training; mobilization; performance and development; engagement;
  offboarding and reassignment.
- **Excluded concerns**: governance of people (Governance & Existence);
  tooling that supports people (Supply & Resources); the demand side of
  customers (Customer & Demand).
- **Adjacent Domains**: Governance & Organization (rules that govern
  organizational behaviour); Supply & Resources (digital tools that
  people use); Customer & Demand (people-as-customers, distinct from
  people-as-agents).
- **Boundary rules**: People & Organization owns agents and the structure
  that organizes them. People-as-customers are not modelled here; they
  live in Customer & Demand.
- **Evidence / rationale**: REPORT §5.1; `dea-catalog-actors` patterns.

### 3.4 Customer & Demand

- **Axiom grounding**: "exchanging value": exchange requires a counterparty.
- **Semantic definition**: the enterprise's reason to exchange; identifying,
  acquiring, serving, and retaining the people whose need it meets.
- **Included concerns**: need identification; journey mapping; onboarding;
  activation; support and service; satisfaction and churn; offboarding.
- **Excluded concerns**: the people who perform customer-facing work
  (People & Organization); the offering itself (Product & Offering); the
  financial accounting of customer value (Finance & Value).
- **Adjacent Domains**: Product & Offering (demand for the offering);
  People & Organization (people-as-agents, not customers); Finance & Value
  (customer-lifetime-value accounting).
- **Boundary rules**: Customer & Demand owns the counterparty relationship
  and the demand signal. The offering that meets the demand lives in
  Product & Offering; the financial accounting of customer value lives in
  Finance & Value.
- **Evidence / rationale**: REPORT §5.1; Business Process Catalog topology
  for activation and support patterns.

### 3.5 Product & Offering

- **Axiom grounding**: "exchanging value": exchange requires something to
  offer.
- **Semantic definition**: the catalog of what the enterprise offers; its
  design, packaging, release, and retirement.
- **Included concerns**: market sensing; catalog and specs; configuration;
  launch; catalog management; performance; sunset.
- **Excluded concerns**: the demand for the offering (Customer & Demand);
  the delivery of the offering (Operations & Delivery); the financial
  pricing model (Finance & Value).
- **Adjacent Domains**: Customer & Demand (offering vs demand);
  Operations & Delivery (offering vs the engine that delivers it);
  Finance & Value (offering vs the financial model around it).
- **Boundary rules**: Product & Offering owns the offering itself. Delivery
  of the offering is Operations & Delivery; pricing of the offering is
  Finance & Value.
- **Evidence / rationale**: REPORT §5.1; `dea-catalog-digital-business-service-factory`
  and `dea-catalog-solution-hub` patterns.

### 3.6 Operations & Delivery

- **Axiom grounding**: "exchanging value": exchange requires a mechanism.
- **Semantic definition**: the engine that turns an offering into a
  delivered outcome; planning, fulfilling, running, resolving.
- **Included concerns**: demand planning; process design; provisioning;
  cut-over; run and maintain; quality and incident; decommission.
- **Excluded concerns**: the offering being delivered (Product & Offering);
  the substrate being run on (Supply & Resources); the financial accounting
  of delivered value (Finance & Value).
- **Adjacent Domains**: Supply & Resources (engine vs substrate);
  Product & Offering (engine vs offering); Finance & Value (delivered
  outcome vs financial recognition).
- **Boundary rules**: Operations & Delivery owns the delivery mechanism.
  The offering is Product & Offering; the substrate is Supply & Resources;
  the financial recognition of delivered outcome is Finance & Value.
- **Evidence / rationale**: REPORT §5.1; the Business Process Catalog's
  L0..L4 topology and the telecom run/assure patterns.

### 3.7 Finance & Value

- **Axiom grounding**: "with its environment": the environment requires
  accounting.
- **Semantic definition**: the accounting for the environment; the flow of
  money and the measurement of value created, consumed, and retained.
- **Included concerns**: business case; pricing model; funding; billing
  activation; revenue and cost; margin analysis; write-off.
- **Excluded concerns**: the offering priced (Product & Offering); the
  delivered outcome recognized (Operations & Delivery); the customer
  whose lifetime value is measured (Customer & Demand).
- **Adjacent Domains**: all other Domains: Finance & Value intersects
  every Domain because every Domain produces and consumes value.
- **Boundary rules**: Finance & Value owns the financial model and the
  measurement of value. The sources of value live in their owning Domains;
  Finance & Value provides the accounting lens.
- **Evidence / rationale**: REPORT §5.1; the Commercialization route in
  REPORT §8.2; `dea-catalog-metrics` patterns.

## 4. Domain Orthogonality

Knowledge of a Domain does not determine a Stage; knowledge of a Stage
does not determine a Domain. A capability contextualized by
`(Customer & Demand, Conceive)` is meaningfully different from one
contextualized by `(Customer & Demand, Operate)`; a capability
contextualized by `(Finance & Value, Conceive)` is meaningfully different
from one contextualized by `(Customer & Demand, Conceive)`. The seven
Domains and the seven Stages remain independent partitions.

## 5. Domain Completeness

The seven Domains collectively cover the grounding axiom:

- "bounded entity" -> Governance & Existence
- "persists" (substrate) -> Supply & Resources
- "persists" (agents) -> People & Organization
- "exchanging value" (counterparty) -> Customer & Demand
- "exchanging value" (offering) -> Product & Offering
- "exchanging value" (mechanism) -> Operations & Delivery
- "with its environment" -> Finance & Value

No gap: each word is grounded. No hidden assumption: the derivation is the
axiom. No imported framework category: the Domain set is axiom-derived, not
reverse-engineered from a specific industry. Controlled overlap: the
boundary rules above resolve the apparent overlap between Finance & Value
and the other Domains.

## 6. Renaming Rule

No Domain is renamed or restructured without explicit evidence and
governance. A future CR (or an extension of CR-ECF-003) may revisit any
Domain if evidence accumulates; the change must cite the evidence and the
governance decision.
