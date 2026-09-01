# ECF Lifecycle Grounding

Status: Normative (CR-ECF-004)
Scope: the seven ECF Lifecycle Stages and their boundaries relative to
object state, process level, and DERA phase

## 1. Canonical Stages

The seven ECF Lifecycle Stages are retained as recorded in REPORT §5.2:

| # | Stage (short) | Stage (full) | One-line definition |
|---|---------------|--------------|---------------------|
| 1 | Conceive | Conceive | Naming the need, the opportunity, the policy. The enterprise decides what should exist. |
| 2 | Design | Design | Specifying the object, the process, the controls. The enterprise shapes what it will build. |
| 3 | Build | Build / Acquire | Constructing, provisioning, hiring, or buying. The object becomes real but is not yet live. |
| 4 | Activate | Deploy / Activate | Cutting over, launching, mobilizing. The object enters service and begins to deliver value. |
| 5 | Operate | Operate / Deliver | Running, serving, monitoring, maintaining. Where the object spends most of its life. |
| 6 | Improve | Measure / Learn | Measuring performance, learning from incidents, scoring satisfaction. The enterprise decides what to change. |
| 7 | Retire | Retire / Renew | Sunsetting, migrating, recovering, or renewing. The object exits its current form. |

## 2. Stage Semantics

A Stage represents a lifecycle context in which enterprise work concerning
an object, concern, or capability is considered. An ECF Stage is not, by
itself, an assertion about any of the following:

- **Object State.** A named phase in an object's lifecycle (proposed,
  designed, provisioned, active, retired). Object State is a property of the
  object; ECF Stage is the context in which the object is being considered.
- **Process Level.** A step in a process decomposition hierarchy (L0
  Process Scope, L1 Process Group, L2 Business Process, L3 Activity, L4
  Task). The Business Process Architecture owns process decomposition; ECF
  provides the coordinate context, not the process hierarchy.
- **Process Phase.** A phase label used inside a process methodology.
- **DERA Phase.** A delivery-programme phase (Discover & Define, Design &
  Build, Deploy & Operate, Evolve & Retire). DERA Phase is a coarser
  delivery wrapper; ECF Stage is the finer-grained lifecycle context.
- **Project Phase.** A phase label from a project-management methodology.
- **Assessment Phase.** A phase label from an assessment methodology.

An ECF Stage and any of the above constructs can be coordinated through a
mapping, but none of them is identical to an ECF Stage.

## 3. Stage vs Object State

The ECF Stage shall not be equated with an object's State. For example:

```
Stage = Operate
```

does not necessarily mean:

```
Entity State = Operational
```

The Stage identifies the lifecycle context in which the object is being
considered; the State is the object's actual lifecycle position. The two
are independent semantic constructs and are owned by different models: Stage
by the ECF, State by the consuming model's entity semantics.

The notation in [`constructs.md`](./constructs.md) records the
distinction:

```
// what state it's in (object state, not ECF Stage)
state : Entity -> State
```

## 4. Stage vs Process Level

ECF Stages and Business Process decomposition are governed by separate
mechanisms. The Business Process Architecture owns the process topology
established by the Business Process Catalog:

```
ECF Coordinate
      |
      v
Process Context
      |
      v
L0 Process Scope
      |
      v
L1 Process Group
      |
      v
L2 Business Process
      |
      v
L3 Activity
      |
      v
L4 Task
```

ECF coordinates contextualize Process Context; the Business Process
Architecture defines the L0..L4 hierarchy. ECF recursion (a coordinate
contextualizing a further specialized model) is independent of process
decomposition. See [`matrix.md`](./matrix.md), section "Recursive
Applicability".

## 5. Stage vs DERA Phase

The existing DERA mapping is retained as a mapping, not as an identity
relationship:

| DERA Phase | ECF Stages |
|-----------|------------|
| Phase 1: Discover & Define | Conceive + Design |
| Phase 2: Design & Build | Build + Activate |
| Phase 3: Deploy & Operate | Operate + Improve |
| Phase 4: Evolve & Retire | Retire |

DERA is the coarser delivery wrapper; ECF's seven Stages are the
finer-grained lifecycle context. The mapping is governed by DERA. Any
change to either side of the mapping requires an explicit governance
decision; it is not a consequence of changing the other.

## 6. Multi-Stage Participation

A process may traverse multiple ECF Stages: the ECF Stage identifies the
contextual lifecycle position in which the process is considered, not
necessarily the entire execution duration of the process.

A capability may participate in multiple lifecycle contexts: the ECF Stage
provides contextual classification rather than defining the capability
itself.

Notation:

```
// a process may traverse multiple Stages
stages : Process -> 2^Stage
```

The consuming catalog determines whether zero, one, or many modeled
elements participate in a given Stage; the ECF does not impose a
population requirement.

## 7. Recursive Applicability

An ECF Stage may be used as the organizing context for a further
specialized model. The specialization is governed by the consuming model,
not mandated by the ECF. ECF recursion is separate from Business Process
decomposition (section 4) and from the DERA mapping (section 5).
