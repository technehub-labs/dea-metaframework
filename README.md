# Enterprise Concept Framework

**The 7×7 axiom-derived matrix for describing any enterprise.**

This repo holds the **Meta Framework** of the TechNeHub Labs DEA ecosystem, 
the conceptual skeleton beneath the
[DEA Metamodel](../dea-metamodel) and every catalog in the
DEA catalog orgs (`dea-catalog-*`).

The framework is axiom-derived: in a single sentence, *an enterprise is any
bounded entity that persists by exchanging value with its environment*,
generates seven domains. 
A universal lifecycle of seven stages partitions the work of any object over time. 
The matrix **M = D × S** is 49 cells, and every object, capability, event, actor, 
and resource in the enterprise lives in one of them.

Together with the [DEA Metamodel](../dea-metamodel), this repo is the
**Digital Ecosystem & Enterprise Metamoat**, the foundation above the
catalogs, the conceptual layer above the tooling.

---

## What's in this repo

| Path | What it is |
|------|-----------|
| [`REPORT.md`](./REPORT.md) | Full walkthrough of the framework — intent, axiom, axes, rules, matrix, case studies, notation, metrics, adoption playbook. The single source of truth. |
| [`framework/`](./framework) | Modular artifacts extracted from the report — axiom, matrix, case studies, formal notation, metrics. |
| [`metamodel/`](./metamodel) | The Enterprise Concepts Metamodel (Section 16 + Appendix A) — the 19-entity ER model that formalizes the framework's constructs. |
| [`schemas/`](./schemas) | JSON Schemas for the framework's derived artifacts — entity catalog, capability map, lifecycle traceability matrix. |
| [`docs/terminology/`](./docs/terminology) | Terminology alignment with the OpenDEA Concepts Model — `Domain`/`Stage` are reserved ECF terms (CR-CM-000 / CR-CM-000A). |
| [`change-requests/`](./change-requests) | Cross-references to change requests in the canonical CR repository (`dea-metamodel`). |
| [`pages/`](./pages) | GitHub Pages source — interactive 7×7 matrix viewer + metamodel explorer. |

---

## Quick start

### Read the framework
Start with [`REPORT.md`](./REPORT.md) — Sections 1–3 (intent, axiom, principles)
and Section 9 (the foundation matrix) cover the essentials in 15 minutes.

### Apply the framework
- **Step 1 (Days 1–4)** — Map: place your top-50 business objects in cells.
- **Step 2 (Days 5–7)** — Validate: walk each row and column with owners.
- **Step 3 (Days 8–10)** — Metrics: compute coverage, coupling, lifecycle completeness.
- **Step 4 (Days 11–13)** — Operate: wire into the planning cycle; snapshot each sprint.
- **Step 5 (Day 14)** — Govern: charter the matrix owner and versioning cadence.

### Use the schemas
- [`schemas/entity.schema.json`](./schemas/entity.schema.json) — canonical business object entry (id, domain, stage, attributes, owners, relatedObjects, complianceTags, version).
- [`schemas/capability.schema.json`](./schemas/capability.schema.json) — capability map entry (id, cell, actor, resources, events).
- [`schemas/traceability.schema.json`](./schemas/traceability.schema.json) — object → stage → event → actor end-to-end trace.

### Build on it
- **DEA Metamodel** — [`technehub-labs/dea-metamodel`](../dea-metamodel) — entity
  types and relationships formalize the framework's constructs. The
  `Business Capability` entity carries `ecfCoordinates: (Domain, Stage)`.
- **DEA Taxonomies** — the 7 domains × 7 stages are the top two levels of
  `dea-catalog-taxonomy`.
- **DEA Reference Architecture** — DERA's 4 phases group the 7 stages:
  *Discover & Define* = Conceive + Design, *Design & Build* = Build + Activate,
  *Deploy & Operate* = Operate + Improve, *Evolve & Retire* = Retire.

---

## Where it fits

```
                        ┌──────────────────────────────────────┐
                        │ Digital Ecosystem & Enterprise      │
                        │ Metamoat                             │
                        │                                      │
                        │  ┌────────────┐    ┌─────────────┐  │
                        │  │   Meta     │    │             │  │
                        │  │ Framework  │    │  Metamodel  │  │
                        │  │ (this repo)│    │  (dea-      │  │
                        │  │            │    │  metamodel) │  │
                        │  └─────┬──────┘    └──────┬──────┘  │
                        │        │                  │         │
                        │        ▼                  ▼         │
                        │  ┌────────────────────────────────┐ │
                        │  │ DEA Catalogs & Tools           │ │
                        │  │ dea-catalog-concepts           │ │
                        │  │ dea-catalog-patterns           │ │
                        │  │ dea-catalog-guardrails         │ │
                        │  │ dea-catalog-metrics            │ │
                        │  │ dea-catalog-…                  │ │
                        │  └────────────────────────────────┘ │
                        └──────────────────────────────────────┘
```

---

## Live sites

- **Meta Framework Explorer** —
  [technehub-labs.github.io/dea-metaframework/](https://technehub-labs.github.io/dea-metaframework/)
  Interactive 7×7 matrix viewer with foundation / telecom / digital scenarios.
- **DEA Metamodel Explorer** —
  [technehub-labs.github.io/metamodel/](https://technehub-labs.github.io/metamodel/)
  19-entity metamodel with layer filter, detail panel, and click-through to
  catalog repos.
- **TechNeHub Labs root** —
  [technehub-labs.github.io](https://technehub-labs.github.io)

---

## Contributing

Open an issue or pull request. The framework is versioned; semantic-version
bump for any change to the axiom, axes, or matrix construction rules.

## License

Apache 2.0 — see [LICENSE](./LICENSE).## Citation

See [`CITATION.cff`](./CITATION.cff) for cite-as metadata.
