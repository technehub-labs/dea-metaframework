# Formal Constructs

The framework's center of gravity is the ECF coordinate, not the cell. An ECF
coordinate is a classification context; an enterprise concept is contextualized
by one or more coordinates according to the semantics of the consuming model.
This file defines the formal notation for the coordinate system and the
named things the matrix contextualizes.

## Definitions

- **Domain.** One of the seven canonical enterprise concern dimensions of
  ECF: Governance & Existence; Supply & Resources; People & Organization;
  Customer & Demand; Product & Offering; Operations & Delivery;
  Finance & Value.
- **Stage.** One of the seven canonical lifecycle dimensions of ECF:
  Conceive; Design; Build; Activate; Operate; Improve; Retire.
- **Coordinate.** The ordered pair `(Domain, Stage)`. The ECF matrix
  `M = D x S` is the cartesian product of the seven Domains and the seven
  Stages; `|M| = 7 x 7 = 49`. A coordinate is identified by its ordered pair;
  display labels are not semantic identity.
- **Context.** The semantic interpretation of an ECF coordinate for a
  particular modeling concern (Process Context, Capability Context,
  Architecture Context, Assessment Context, and so on). The consuming model
  defines the context.
- **Business object.** A thing the enterprise cares about: a customer, a
  circuit, a feature flag, a grant.
- **Entity.** A business object with a unique identity and a persistent
  state.
- **Capability.** The ability to do something with an object: provision,
  bill, monitor, retire.
- **Value stream.** The end-to-end flow that carries an object across the
  seven stages.
- **State.** A named phase in an object's lifecycle: proposed, designed,
  provisioned, active, retired. State is a property of an object; it is
  distinct from ECF Stage, which is a lifecycle context for consideration.
- **Event.** A state transition: signup, cut-over, incident, sunset.
- **Actor.** The owner or performer of a capability: a person, team, or
  system.
- **Resource.** The asset consumed by a capability: spectrum, compute,
  budget, hours.

## How Constructs Relate

An enterprise concept may be contextualized by one or more ECF coordinates.
The matrix is not a container of objects; a coordinate is the context in
which a concept is considered.

```
type Domain = 1..7;   // rows
type Stage  = 1..7;   // columns

// the matrix is the cartesian product of the seven Domains and seven Stages
M = D x S = { (d, s) | d in D, s in S }

// |M| = 49 coordinates; each is identified by its ordered pair
type Coordinate = (Domain, Stage)

// a coordinate carries context, not identity
contextualizes : Entity x Coordinate -> Context

// an entity may participate in multiple coordinates where governed
// by the consuming catalog (multi-coordinate contextualization)
coordinates : Entity -> 2^Coordinate

// a process may traverse multiple Stages
stages       : Process -> 2^Stage

// an object's lifecycle is a path
lifecycle(o) = < s_1 -> s_2 -> ... -> s_7 >
```

A coordinate establishes a context. Whether zero, one, or many modeled
elements are appropriate within that context is determined by the consuming
catalog, not by the ECF.

## Traceability Functions

```
// who owns an object
owner : Entity -> Actor

// what state it's in (object state, not ECF Stage)
state : Entity -> State

// what it depends on (other entities)
deps  : Entity -> 2^Entity

// impact closure: change ripples
impact(e) = deps*(e) = UNION deps^n(e), n >= 0
```

### Impact Propagation: Worked Example with Formal Closure

A change traced through entity dependencies:

- **Change:** a tariff plan is retired (Product and Offering).
- **-> deps:** every subscriber on that plan is affected.
- **-> deps:** every billing account linked to those subscribers must re-rate.

```
closure(c_1) = deps(c_1) U deps(deps(c_1)) U {}
           = {c_2, c_3} U {c_4} U {}
           = {c_2, c_3, c_4}

impact(c_4) = {c_1, c_2, c_3}  // reverse closure
```

The `impact` function computes the transitive closure of dependencies,
revealing the full blast radius of a single change. ECF coordinates are not
inputs to this function: dependencies live on the entity graph, not on the
coordinate graph.

## Mapping to DEA Metamodel

| ECF Construct | DEA Metamodel Entity |
|---------------|---------------------|
| Domain | `TaxonomyNode` (Domain layer) |
| Stage | `TaxonomyNode` (Stage layer) |
| Coordinate | `ECFCoordinate` (profile binding) |
| Business object | `BusinessService` |
| Capability | `BusinessCapability` |
| Pattern / Standard | `ArchitecturePattern` / `Standard` |
| Actor | `SolutionComponent` owner |
| Metric | `MeasurementMetric` |
| Relationship | `Relationship` (typed, governed) |

ECF Domain and Stage are reserved classification terms. Capability,
Process, and their coordinate usages are formalized in the OpenDEA ECF
profile within `dea-metamodel`. See
[`technehub-labs/dea-metamodel`](../dea-metamodel) for the canonical
entity-relationship model.

## Mapping to DERA

| DERA Phase | ECF Stages |
|-----------|------------|
| Phase 1: Discover & Define | Conceive + Design |
| Phase 2: Design & Build | Build + Activate |
| Phase 3: Deploy & Operate | Operate + Improve |
| Phase 4: Evolve & Retire | Retire |

This is a mapping, not an identity relationship. DERA is the coarser delivery
wrapper; ECF's seven stages are the finer-grained lifecycle context.
