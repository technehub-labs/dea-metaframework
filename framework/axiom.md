# The Grounding Axiom

> **An enterprise is any bounded entity that persists by exchanging value with its environment.**

Every word in that sentence generates a domain. The framework is not asserted
— it is *derived* from the definition of an enterprise.

## Axiomatic Derivation

| Word in the axiom | Generated domain | Why |
|-------------------|-----------------|-----|
| "bounded entity" | → Governance & Existence | Boundedness requires a boundary — who is inside, what rules apply, what constitutes the entity itself. |
| "persists" | → Supply & Resources | Persistence requires a substrate — the physical or virtual assets that keep the entity alive over time. |
| "persists" | → People & Organization | Persistence requires agents — the humans who perform the work and the structure that organizes them. |
| "exchanging value" | → Customer & Demand | Exchange requires a counterparty — the people whose need the entity meets, and the demand they generate. |
| "exchanging value" | → Product & Offering | Exchange requires something to offer — the catalog of what the entity provides to meet demand. |
| "exchanging value" | → Operations & Delivery | Exchange requires a mechanism — the engine that turns the offering into a delivered outcome. |
| "with its environment" | → Finance & Value | The environment requires accounting — the measurement of value created, consumed, and retained. |

Each domain is a logical consequence of a word in the axiom, not an
assertion. This is what makes the framework bottom-up: it is derived from
the definition of an enterprise, not reverse-engineered from a specific
industry's practices.

## Why Bottom-Up

Named frameworks — eTOM (telecom), ITIL (IT service management), COBIT
(governance), Zachman (architecture) — were each reverse-engineered from a
specific context. Adopting them wholesale imports that context's blind spots.

An axiom-derived matrix carries no foreign assumptions. It fits the
enterprise because it was derived from the definition of an enterprise. The
cost is the work of derivation; the benefit is a description that does not
need to be bent to fit.

## Defensibility

### "This just duplicates existing frameworks."
It doesn't. eTOM and ITIL describe *how* a telco or an IT shop works. This
framework describes *what any enterprise is* — the skeleton the others hang
on. eTOM is a projection of this matrix onto the telecom industry; ITIL is a
projection onto IT service management.

### "It's too abstract."
It's exactly as abstract as a skeleton needs to be. The cells are where the
concrete work lives. The framework specifies *where* a capability lives and
*what* it relates to; it does not pretend to specify what a telco's HLR/HSS
does.

### "It won't scale."
The matrix is 7×7 regardless of enterprise size. Any cell decomposes into a
7×7 sub-matrix, giving infinite depth without changing the top-level logic.
The framework scales because it does not grow; it recurses.

### "It's industry-specific."
The Telecom and Digital Services case studies prove otherwise. A telco's
HLR/HSS cut-over and a SaaS company's feature flag rollout live in the same
cell — Customer × Activate. Identical structure, different content, no
bending.