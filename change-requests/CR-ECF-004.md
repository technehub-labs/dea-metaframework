CR-ECF-004 — ECF Lifecycle Grounding

CR-ECF-004 — ECF Lifecycle Grounding

Status: Proposed
Type: Lifecycle Semantics
Implements: CR-ECF-001
Depends On: CR-ECF-002

1. Change Request

Formalize the seven ECF Lifecycle Stages and establish their boundaries relative to other lifecycle constructs used within OpenDEA.

2. Canonical Stages

The current stages shall be retained:

Conceive
Design
Build
Activate
Operate
Improve
Retire

The existing REPORT provides their current definitions and expanded labels. (GitHub⁠)

3. Stage Semantics

A Stage represents a lifecycle context in which enterprise work concerning an object, concern or capability is considered.

It does not automatically represent:

Object State
Process Level
Process Phase
DERA Phase
Project Phase
Assessment Phase

4. Distinction from DERA

The existing mapping:

DERA Discover & Define
    → Conceive + Design
DERA Design & Build
    → Build + Activate
DERA Deploy & Operate
    → Operate + Improve
DERA Evolve & Retire
    → Retire

may remain as a mapping, but it shall explicitly be described as a mapping, not an identity relationship.

5. Stage and State

The ECF Stage shall not be equated with an object’s state.

For example:

Stage = Operate

does not necessarily mean:

Entity State = Operational

A lifecycle context and an object state are distinct semantic constructs.

6. Stage and Process

A Process may traverse multiple ECF Stages.

The ECF Stage identifies the contextual lifecycle position in which the process is considered, not necessarily its entire execution duration.

7. Stage and Capability

A capability may participate in multiple lifecycle contexts.

The ECF Stage therefore provides contextual classification rather than defining the capability itself.

8. Acceptance Criteria

* [ ]	Seven stages are formally defined.
* [ ]	Stage boundaries are documented.
* [ ]	Stage is distinct from object state.
* [ ]	Stage is distinct from process level.
* [ ]	Stage is distinct from DERA phase.
* [ ]	Existing DERA mapping is retained as a mapping.
* [ ]	Multi-stage participation is supported where legitimate.
