# Case Study — Digital Services

The foundation matrix populated for a digital services company. Same 49
cells, digital-era content.

| Domain \ Stage | Conceive | Design | Build | Activate | Operate | Improve | Retire |
|----------------|----------|--------|-------|----------|---------|---------|--------|
| **Governance & Existence** | Privacy policy | Controls design (SOC2) | Compliance build | Enforce (guardrails) | Audit log | Risk review (pentest) | Policy retire |
| **Strategy & Direction** | Market sensing | Strategic choice | Initiative portfolio | Launch direction | Course correct | Strategic review | Strategic renewal |
| **Agency & Organization** | Team topology | Org design (pods) | Acquire / onboard | Sprint mobilize | Perf review (360) | Coordination | Offboard |
| **Party & Relationship** | User need (JTBD) | Persona map | Signup flow | Activation event (aha) | In-product help | Retention cohort (DAU) | Account deletion (GDPR) |
| **Product & Value** | Discovery | Feature spec (PRD) | Build sprint | Feature flag launch | Roadmap mgmt | Feature adoption | Deprecation |
| **Enablement & Operations** | Demand forecast | Pipeline design (CI/CD) | Provision env (IaC) | Deploy to prod (canary) | SRE on-call (SLO) | Incident review (PSE) | Env teardown |
| **Finance & Accounting** | Unit econ (LTV) | Pricing tier (SaaS) | Funding round | Subscription start (stripe) | MRR / churn | Cohort margin (CAC) | Dunning / refund |

## Digital Services Patterns

- The **Product & Value × Activate** cell (feature flag rollout) is the
  digital company's equivalent of the telco cut-over: the moment of risk.
- The **Finance & Accounting × Operate** cell (FinOps) shows that in
  digital, cost is a runtime concern, not an annual one. The matrix makes
  this visible where an org chart would not.

## Worked Example — User Account Lifecycle (Digital)

| Stage | Cell | What happens |
|-------|------|-------------|
| Conceive | Party & Relationship × Conceive | User need identified (JTBD interviews, persona work) |
| Design | Party & Relationship × Design | Persona map, signup flow designed, friction points identified |
| Build | Party & Relationship × Build | Signup form, email verification, password hashing |
| Activate | Party & Relationship × Activate | First action, "aha moment"; value realized |
| Operate | Party & Relationship × Operate | In-product help, support tickets, DAU/MAU tracking |
| Improve | Party & Relationship × Improve | Retention cohort, NPS, churn prediction |
| Retire | Party & Relationship × Retire | GDPR account deletion, refund processing |

Same 7 stages as telco Subscriber; different industry, same skeleton.

## Cross-Industry Comparison

| Cell | Telecom | Digital Services |
|------|---------|------------------|
| Party & Relationship × Activate | Network attach (HLR/HSS) | Activation event (aha-moment) |
| Product & Value × Build | Bundle configuration | Build sprint (agile) |
| Enablement & Operations × Operate | NOC 24/7 | SRE on-call (SLO) |
| Finance & Accounting × Operate | Mediation & rating | MRR / churn |
| Governance & Existence × Conceive | Regulatory mandate (TRA) | Privacy policy intent |

The cell address is identical. Only the content changes. The framework did
not change to fit either industry; both fit the framework.
