# Enterprise Concept Framework

**The 7×7 axiom-derived matrix for describing any enterprise.**

This repo holds the **Enterprise Concept Framework (ECF)**: the enterprise
organizing framework of the TechNeHub Labs DEA ecosystem. ECF is an OpenDEA
profile: it supplies the Domain x Stage coordinate system that contextualizes
the concepts the [DEA Metamodel](../dea-metamodel) formally represents and the
DEA catalogs (`dea-catalog-*`) instantiate.

The framework is axiom-derived: in a single sentence, *an enterprise is any
bounded entity that persists by exchanging value with its environment*,
generates seven domains.
A universal lifecycle of seven stages partitions the work of any object over time.

The matrix **M = D × S** defines 49 ECF coordinates. Enterprise concepts are
contextualized by one or more coordinates according to the semantics of the
consuming model; a coordinate is a classification context, not an entity
container.

ECF sits within the OpenDEA semantic architecture: the World Semantic
Foundation (WSF) provides foundational semantics, OpenDEA specializes them for
enterprise architecture, ECF organizes the enterprise domain/lifecycle space,
and the metamodel plus catalogs carry formal representation and governed
content. See
[Position in the Semantic and OpenDEA Architecture](#position-in-the-semantic-and-opendea-architecture).

---

## What's in this repo

| Path | What it is |
|------|-----------|
| [`REPORT.md`](./REPORT.md) | Full walkthrough of the framework: intent, axiom, axes, rules, matrix, case studies, notation, metrics, adoption playbook. The authoritative explanatory synthesis; normative authority lives in [`framework/`](./framework) and the CR-governed change requests. |
| [`framework/`](./framework) | Modular artifacts extracted from the report: axiom, matrix, case studies, formal notation, metrics; plus [`framework/architecture.md`](./framework/architecture.md), the normative architectural position (CR-ECF-001); [`framework/domain-grounding.md`](./framework/domain-grounding.md), the per-Domain grounding records and compound-name audit (CR-ECF-003). |
| [`metamodel/`](./metamodel) | The Enterprise Concepts Metamodel (Section 16 + Appendix A) — the 19-entity ER model that formalizes the framework's constructs. |
| [`schemas/`](./schemas) | JSON Schemas for the framework's derived artifacts — entity catalog, capability map, lifecycle traceability matrix. |
| [`docs/terminology/`](./docs/terminology) | Terminology alignment with the OpenDEA Concepts Model — `Domain`/`Stage` are reserved ECF terms (CR-CM-000 / CR-CM-000A). |
| [`change-requests/`](./change-requests) | Change requests governing this framework (CR-ECF series), plus cross-references to change requests in the canonical CR repository (`dea-metamodel`). |
| [`pages/`](./pages) | GitHub Pages source — interactive 7×7 matrix viewer + metamodel explorer. |

---

## Position in the Semantic and OpenDEA Architecture

ECF is an enterprise organizing framework within OpenDEA, grounded in the
World Semantic Foundation (WSF). The normative statement of this position is
[`framework/architecture.md`](./framework/architecture.md) (CR-ECF-001).

```
World Semantic Foundation (WSF)
        foundational semantics
                |
                v
OpenDEA Core Semantics
        WSF specialized for enterprise architecture
                |
    +-----------+------------+-----------+
    |           |            |           |
ECF Profile   Business     Data       Technology
(this repo)   Profile      Profile    Profile
    |
    v
ECF Coordinates (Domain x Stage; 7 x 7 = 49)
    |
    |           +----------- other OpenDEA Profiles
    v           v
OpenDEA Metamodel
        formal semantic representation
                |
                v
Reference Catalogs
        governed concept instances
```

Normative boundaries: `WSF != OpenDEA != ECF != DEA Metamodel != Catalog`.
ECF organizes and contextualizes; the metamodel formally represents; catalogs
instantiate governed concepts. Downstream consumers of the ECF contract:
[`dea-metamodel`](https://github.com/technehub-labs/dea-metamodel) (ECF
profile),
[`dea-catalog-business-capabilities`](https://github.com/technehub-labs/dea-catalog-business-capabilities)
(classification context, not capability identity), and
[`dea-catalog-processes`](https://github.com/technehub-labs/dea-catalog-processes)
(Process Context, not process identity).

---

## Quick start

### Read the framework
Start with [`REPORT.md`](./REPORT.md) — Sections 1–3 (intent, axiom, principles)
and Section 9 (the foundation matrix) cover the essentials in 15 minutes.

### Apply the framework in 5 Steps and 14 days
- **Step 1 (Days 1–4)**: Contextualize: for each top-50 business concept, identify the ECF coordinate(s) that contextualize it; record the consuming catalog that owns the coordinate usage.
- **Step 2 (Days 5–7)**: Validate: walk each row and column with owners.
- **Step 3 (Days 8–10)**: Metrics: compute coverage, coupling, lifecycle completeness.
- **Step 4 (Days 11–13)**: Operate: wire into the planning cycle; snapshot each sprint.
- **Step 5 (Day 14)**: Govern: charter the matrix owner and versioning cadence.

### Use the schemas
- [`schemas/entity.schema.json`](./schemas/entity.schema.json) — canonical business object entry (id, domain, stage, attributes, owners, relatedObjects, complianceTags, version).
- [`schemas/capability.schema.json`](./schemas/capability.schema.json) — capability map entry (id, cell, actor, resources, events).
- [`schemas/traceability.schema.json`](./schemas/traceability.schema.json) — object → stage → event → actor end-to-end trace.

### Build on it
- **DEA Metamodel**: [`technehub-labs/dea-metamodel`](../dea-metamodel); the
  canonical semantic model. ECF is consumed there as an OpenDEA profile.
- **Business Capability catalog**:
  [`technehub-labs/dea-catalog-business-capabilities`](../dea-catalog-business-capabilities);
  ECF coordinates are classification context, not capability identity.
- **Business Process catalog**:
  [`technehub-labs/dea-catalog-processes`](../dea-catalog-processes);
  an ECF intersection establishes Process Context, not a Business Process.
- **DEA Reference Architecture**: DERA's 4 phases map to the 7 stages:
  *Discover & Define* = Conceive + Design, *Design & Build* = Build + Activate,
  *Deploy & Operate* = Operate + Improve, *Evolve & Retire* = Retire. This is a
  mapping, not an identity relationship.

---

## Where it fits

The ECF, the DEA Metamodel, and the DEA catalogs together form the **Digital
Ecosystem & Enterprise Metamoat**. Their relationship is governed by the
architectural position above: ECF is the OpenDEA profile that supplies the
coordinate system; the metamodel is the canonical semantic model that formally
represents OpenDEA concepts; the catalogs instantiate governed concepts and
consume ECF coordinates as context. See
[`framework/architecture.md`](./framework/architecture.md).

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
