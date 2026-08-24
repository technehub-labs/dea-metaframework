# Concepts Model Terminology Alignment

> **The Enterprise Concept Framework owns `Domain` and `Stage`. The
> OpenDEA Concepts Model speaks in Concept Area, Concept Profile, Concept
> Classification, and ECF Context. The two vocabularies are related by
> association, never by identity.**
>
> Source: [CR-CM-000 + CR-CM-000A](https://github.com/technehub-labs/dea-metamodel/blob/main/change-requests/CR-CM-000.md)
> (canonical CR copies live in `technehub-labs/dea-metamodel/change-requests/`).
> Machine-readable registry (interim canonical home):
> [`dea-metamodel/vocabulary/terminology-registry.yaml`](https://github.com/technehub-labs/dea-metamodel/blob/main/vocabulary/terminology-registry.yaml).

## Why this document exists

The OpenDEA body of work spans complementary semantic layers:

```
Enterprise Concept Framework          ← this repository
          │
          ▼
OpenDEA Concepts Model                ← dea-concepts-model (CR-CM-001)
          │
          ▼
Foundational Metamodel                ← dea-metamodel
          │
          ▼
Catalogs / Domain Models / Implementations
```

These layers must not use the same terms with different meanings. The
collision that forced the decision: the ECF gives **Domain** a precise
structural meaning (one axis of the Domain × Stage coordinate system),
while early Concepts Model sketches used "domain" as a generic thematic
grouping. CR-CM-000 / CR-CM-000A resolve that collision *before* the
Concepts Model repository exists.

## The reservation (ECF side)

| Term | Meaning | Owner |
|------|---------|-------|
| **Domain** | Enterprise structural dimension — one of the seven axiom-derived rows of the foundation matrix (see [`framework/matrix.md`](../../framework/matrix.md)) | `dea-metaframework` (this repo) |
| **Stage** | Enterprise lifecycle dimension — one of the seven lifecycle columns | `dea-metaframework` (this repo) |

Every use of *Domain* or *Stage* anywhere in OpenDEA must be either
explicitly **ECF Domain** / **ECF Stage** or namespace-qualified
(e.g. `ecf:Domain`). No Concepts Model artifact may introduce an
independent construct called Domain to mean "collection of related
concepts."

## The Concepts Model vocabulary (referenced, not redefined)

| Term | Meaning |
|------|---------|
| **Concept** | A defined unit of meaning. |
| **Concept Area** | Thematic organization of concepts (many-to-many; concepts may belong to multiple areas). |
| **Concept Profile** | Purposeful, *compositional* composition of concepts and relationships for a particular perspective — never hierarchical, never a Domain. |
| **Concept Classification** | The mechanism for categorizing concepts. |
| **ECF Context** | The association of a concept with an ECF Domain + ECF Stage pair (zero or more per concept). |

## The canonical semantic shape

```
                    ECF  (this repository)
                     │
             ┌───────┴───────┐
             │               │
          Domain           Stage
             │               │
             └───────┬───────┘
                     │
                     ▼
                ECF Context          ← Domain × Stage pair
                     │
                has-ecf-context
                     │
                     ▼
                  Concept
                     │
          ┌──────────┴──────────┐
     belongs-to             included-in
          │                     │
          ▼                     ▼
   Concept Area          Concept Profile
```

Relationship verbs are governed: `has-ecf-context`, `uses-domain`,
`uses-stage`, `belongs-to`, `includes`, and `maps-to` (Concept → metamodel
EntitySpec — deliberately **not** `is-a` / `specializes` / `inherits-from`;
conceptual classification never implies metamodel inheritance).

## Prohibited patterns

- A bare `domain:` attribute on a concept (unless the value is a canonical
  ECF Domain).
- Treating a Concept Area as equivalent to an ECF Domain.
- Naming a conceptual perspective a "Domain" (it is a Concept Profile).
- Automatically promoting a concept to a metamodel entity type without a
  separate `maps-to` mapping decision.

## What the ECF does NOT do

This repository's semantics are **referenced, not redefined**: the ECF
matrix, its seven domains, and its seven stages remain defined solely by
[`REPORT.md`](../../REPORT.md) and [`framework/`](../../framework). The
Concepts Model does not fork, rename, or re-derive them — it
contextualizes against them via ECF Context.

## Forward pointer

CR-CM-001 (OpenDEA Concepts Model Foundation) will create the
`dea-concepts-model` repository with the mandated layout —
`concept-areas/`, `profiles/`, `concepts/`, `relationships/`,
`mappings/ecf/`, `governance/terminology-registry.yaml` — at which point
the registry's canonical home migrates there from `dea-metamodel`.
