# Formal Constructs

The framework uses eight constructs — the named things the matrix operates on.

## Definitions

- **Business object.** A thing the enterprise cares about — a customer, a
  circuit, a feature flag, a grant. The atom of the matrix.
- **Entity.** A business object with a unique identity and a persistent
  state.
- **Capability.** The ability to do something with an object — provision,
  bill, monitor, retire.
- **Value stream.** The end-to-end flow that carries an object across all
  seven stages.
- **State.** A named phase in an object's lifecycle — proposed, designed,
  provisioned, active, retired.
- **Event.** A state transition — signup, cut-over, incident, sunset.
- **Actor.** The owner or performer of a capability — a person, team, or
  system.
- **Resource.** The asset consumed by a capability — spectrum, compute,
  budget, hours.

## How Constructs Relate

Each cell **C(d, s)** holds the objects in domain *d* currently in stage *s*,
the capabilities that act on them, the events that move them, the actors
who perform, and the resources consumed. A cell is a snapshot of one domain
at one stage — a bounded, inspectable unit of the enterprise.

```
type Domain = 1..7;   // rows
type Stage  = 1..7;   // columns

// the matrix is the cartesian product
M = D × S = { (d, s) | d ∈ D, s ∈ S }

// a cell holds objects + their capabilities
type Cell_{d,s} = {
  objects: Entity[],
  caps: Capability[]
}

// an object's lifecycle is a path
lifecycle(o) = ⟨ s₁ → s₂ → … → s₇ ⟩

// any cell recurses into a sub-matrix
decompose : Cell → M   // C(d,s) → 7×7 sub-grid
```

## Traceability Functions

```
// who owns an object
owner : Entity → Actor

// what state it's in (which column)
state : Entity → Stage

// what it depends on (other cells)
deps  : Entity → 2^Entity

// impact closure: change ripples
impact(e) = deps*(e) = ⋃ depsⁿ(e), n ≥ 0
```

### Impact Propagation — Worked Example with Formal Closure

A change in one cell, traced:

- **Change:** a tariff plan is retired (Product × Retire).
- **→ deps:** every subscriber on that plan (Customer × Operate) is affected.
- **→ deps:** every billing account linked to those subscribers (Finance ×
  Operate) must re-rate.

```
closure(c₁) = deps(c₁) ∪ deps(deps(c₁)) ∪ ∅
           = {c₂, c₃} ∪ {c₄} ∪ ∅
           = {c₂, c₃, c₄}

impact(c₄) = {c₁, c₂, c₃}  // reverse closure
```

The `impact` function computes the transitive closure of dependencies,
revealing the full blast radius of a single change.

## Mapping to DEA Metamodel

| ECF Construct | DEA Metamodel Entity |
|---------------|---------------------|
| Business object | `BusinessService` |
| Capability | `BusinessCapability` |
| Pattern / Standard | `ArchitecturePattern` / `Standard` |
| Domain / Stage | `TaxonomyNode` (the 7×7 grid = top two taxonomy levels) |
| Actor | `SolutionComponent` owner |
| Metric | `MeasurementMetric` |
| Relationship | `Relationship` (typed, governed) |

See [`technehub-labs/dea-metamodel`](../dea-metamodel) for the formal
entity-relationship model.

## Mapping to DERA

| DERA Phase | ECF Stages |
|-----------|------------|
| Phase 1 — Discover & Define | Conceive + Design |
| Phase 2 — Design & Build | Build + Activate |
| Phase 3 — Deploy & Operate | Operate + Improve |
| Phase 4 — Evolve & Retire | Retire |

ECF's finer granularity (7 vs 4) is the deeper lens; DERA is the coarser
delivery wrapper that groups adjacent stages.