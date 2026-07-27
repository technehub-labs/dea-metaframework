# Case Study — Digital Services

The foundation matrix populated for a digital services company. Same 49
cells, digital-era content.

| Domain \ Stage | Conceive | Design | Build | Activate | Operate | Improve | Retire |
|----------------|----------|--------|-------|----------|---------|---------|--------|
| **Governance & Existence** | Privacy policy | Controls design (SOC2) | Compliance build | Enforce (guardrails) | Audit log | Risk review (pentest) | Policy retire |
| **Supply & Resources** | Scale vision | Cloud arch. (AWS/GCP) | Infra build (Terraform) | Service mesh | Observability | Cost/usage (FinOps) | Infra retire |
| **People & Organization** | Team topology | Org design (pods) | Hire / onboard | Sprint mobilize | Perf review (360) | Engagement (eNPS) | Offboard |
| **Customer & Demand** | User need (JTBD) | Persona map | Signup flow | Activation event (aha) | In-product help | Retention cohort (DAU) | Account deletion (GDPR) |
| **Product & Offering** | Discovery | Feature spec (PRD) | Build sprint | Feature flag launch | Roadmap mgmt | Feature adoption | Deprecation |
| **Operations & Delivery** | Demand forecast | Pipeline design (CI/CD) | Provision env (IaC) | Deploy to prod (canary) | SRE on-call (SLO) | Incident review (PSE) | Env teardown |
| **Finance & Value** | Unit econ (LTV) | Pricing tier (SaaS) | Funding round | Subscription start (stripe) | MRR / churn | Cohort margin (CAC) | Dunning / refund |

## Digital Services Patterns

- The **Product × Activate** cell — feature flag rollout — is the digital
  company's equivalent of the telco cut-over: the moment of risk.
- The **Supply × Improve** cell — FinOps — shows that in digital, cost is a
  runtime concern, not an annual one. The matrix makes this visible where an
  org chart would not.

## Worked Example — User Account Lifecycle (Digital)

| Stage | Cell | What happens |
|-------|------|-------------|
| Conceive | Customer × Conceive | User need identified (JTBD interviews, persona work) |
| Design | Customer × Design | Persona map, signup flow designed, friction points identified |
| Build | Customer × Build | Signup form, email verification, password hashing |
| Activate | Customer × Activate | First action, "aha moment" — value realized |
| Operate | Customer × Operate | In-product help, support tickets, DAU/MAU tracking |
| Improve | Customer × Improve | Retention cohort, NPS, churn prediction |
| Retire | Customer × Retire | GDPR account deletion, refund processing |

Same 7 stages as telco Subscriber — different industry, same skeleton.

## Cross-Industry Comparison

| Cell | Telecom | Digital Services |
|------|---------|------------------|
| Customer × Activate | Network attach (HLR/HSS) | Activation event (aha-moment) |
| Product × Build | Bundle configuration | Build sprint (agile) |
| Operations × Operate | NOC 24/7 | SRE on-call (SLO) |
| Supply × Improve | Erlang utilization | FinOps cost/usage |
| Finance × Operate | Mediation & rating | MRR / churn |
| Governance × Conceive | Regulatory mandate (TRA) | Privacy policy intent |

The cell address is identical. Only the content changes. The framework did
not change to fit either industry; both fit the framework.