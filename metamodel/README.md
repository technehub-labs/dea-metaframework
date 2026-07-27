# Enterprise Concepts Metamodel

The Enterprise Concepts Metamodel formalizes the framework's constructs as a
typed entity-relationship model. It is organized into five layers, each
answering a different question about the enterprise. The metamodel is the
bridge between the conceptual matrix (Section 9 of `REPORT.md`) and the
concrete artifacts (entity catalog, capability map, traceability matrix) —
it specifies the entity types, their attributes, and the relationships
between them.

This is the **19-entity model** shared with
[`technehub-labs/dea-metamodel`](../dea-metamodel). Source of truth for
entity definitions lives in that repo; this directory holds the canonical
PlantUML source and a rendered SVG.

## Files

| File | What it is |
|------|-----------|
| [`enterprise-concepts.puml`](./enterprise-concepts.puml) | PlantUML source (Appendix A of `REPORT.md`) |
| `enterprise-concepts.svg` | Rendered SVG (generated from the PlantUML source; rendered here for convenience) |
| `README.md` | This file |

## The Five Layers

1. **Strategic & Investment** — the 'Why' & 'When'
2. **Business Operating Model** — the 'What' & 'Who'
3. **Digital Ecosystem & Intelligence** — the 'Digital Era'
4. **Technology & Execution** — the 'How'
5. **Measurement & Governance** — cross-cutting

Layer 3 (Digital Ecosystem & Intelligence) is the distinguishing layer of
this version of the metamodel. It captures the digital-era constructs that
have become first-class citizens of enterprise architecture: digital
identities, event streams, AI/ML models, and data products. These entities
sit between the business operating model and the technology execution
layer, reflecting the reality that digital concerns are neither purely
business nor purely technology — they are a distinct stratum.

## Entity Inventory

| Layer | Entity | Attributes |
|-------|--------|-----------|
| 1 | Strategic Objective | `id: string`, `name: string` |
| 1 | Investment Initiative | `id: string`, `budget: decimal` |
| 2 | Value Stream | `id: string`, `name: string` |
| 2 | Business Capability | `id: string`, `ecfCoordinates: (Domain, Stage)` |
| 2 | Business Process | `id: string`, `name: string` |
| 2 | Business Object | `id: string`, `name: string` |
| 2 | Journey Touchpoint | `id: string`, `channel: string` |
| 2 | Organizational Unit | `id: string`, `name: string` |
| 3 | Digital Identity | `id: string`, `type: (Customer, Partner, Bot)` |
| 3 | Event / Event Stream | `id: string`, `topic: string`, `schema: string` |
| 3 | AI / ML Model | `id: string`, `modelType: string`, `version: string` |
| 3 | Data Product | `id: string`, `SLA: string`, `domainOwner: string` |
| 4 | System Function | `id: string`, `name: string` |
| 4 | Application Component | `id: string`, `name: string` |
| 4 | API / Service Contract | `id: string`, `version: string` |
| 4 | Data Entity | `id: string`, `name: string` |
| 4 | Information Class | `id: string`, `securityLevel: string` |
| 4 | Platform Service | `id: string`, `type: (Compute, DB, Network)` |
| 5 | Performance Metric | `id: string`, `targetValue: string` |

## Relationship Summary

| From | Cardinality | To | Verb |
|------|-----------|----|------|
| Strategic Objective | 1 — 0..* | Investment Initiative | drives |
| Investment Initiative | 0..* — 1..* | Business Capability | funds |
| Value Stream | 0..* — 1..* | Business Capability | traverses |
| Value Stream | 1 — 0..* | Journey Touchpoint | experienced via |
| Business Capability | 1 — 0..* | Business Process | implemented by |
| Business Capability | 1 — 1..* | Organizational Unit | owned by |
| Business Capability | 1 — 0..* | Business Object | produces/consumes |
| Journey Touchpoint | 1 — 0..* | Digital Identity | authenticates |
| Digital Identity | 0..* — 1..* | Data Entity | represented by |
| Business Process | 1 — 0..* | System Function | automated by |
| Business Object | 1 — 1 | Data Entity | digitized as |
| Data Entity | 0..* — 1..* | Information Class | classified by |
| Data Entity | 0..* — 0..* | Data Product | curated into |
| System Function | 1 — 0..* | Event / Event Stream | publishes / subscribes to |
| Event / Event Stream | 0..* — 0..* | Data Entity | carries payload of |
| Data Product | 1 — 0..* | API / Service Contract | exposed via |
| AI / ML Model | 1 — 0..* | Data Product | trained on |
| AI / ML Model | 1 — 0..* | System Function | enhances / automates |
| System Function | 1 — 0..* | Application Component | hosted by |
| Application Component | 0..* — 0..* | Platform Service | deployed on |
| System Function | 1 — 0..* | API / Service Contract | exposed via |
| API / Service Contract | 0..* — 0..* | Data Entity | serves/exchanges |
| Strategic Objective | 1 — 0..* | Performance Metric | measured by |
| Business Capability | 1 — 0..* | Performance Metric | evaluated by |
| System Function | 1 — 0..* | Performance Metric | evaluated by |

## How the Metamodel Links to ECF

Every entity in the metamodel lives in a cell of the 7×7 matrix. The
**Business Capability** entity carries an explicit `ecfCoordinates: (Domain,
Stage)` attribute — the metamodel knows which cell it is in.

The five layers map onto ECF as follows:

| Metamodel Layer | ECF Domain | ECF Stage |
|-----------------|-----------|-----------|
| Layer 1 — Strategic & Investment | Finance & Value | Conceive |
| Layer 2 — Business Operating Model | All seven domains | All seven stages |
| Layer 3 — Digital Ecosystem & Intelligence | Customer & Supply domains | Build → Operate |
| Layer 4 — Technology & Execution | Supply & Resources | Build → Operate |
| Layer 5 — Measurement & Governance | Governance & Existence | Cross-cutting (all stages) |

## Rendering

To render the PlantUML to SVG locally:

```bash
# Option 1 — PlantUML CLI (requires Java + plantuml.jar)
java -jar plantuml.jar enterprise-concepts.puml

# Option 2 — PlantUML Docker image
docker run --rm -v "$PWD:/work" plantuml/plantuml:latest \
  -tsvg enterprise-concepts.puml

# Option 3 — VS Code PlantUML extension
# Open enterprise-concepts.puml → Alt+D to preview
```

Or use the live DEA Metamodel Explorer:
[technehub-labs.github.io/metamodel/](https://technehub-labs.github.io/metamodel/)

## See Also

- [`technehub-labs/dea-metamodel`](../dea-metamodel) — entity definitions,
  JSON Schema, interactive viewer
- [`REPORT.md`](../REPORT.md) § 16 — full prose description of the metamodel
- [`/framework/matrix.md`](../framework/matrix.md) — the 7×7 ECF matrix this
  metamodel instantiates