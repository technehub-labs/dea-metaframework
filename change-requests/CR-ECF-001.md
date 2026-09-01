CR-ECF-001 — ECF Architectural Reconciliation

CR-ECF-001 — ECF Architectural Reconciliation

Status: Proposed
Type: Architecture Reconciliation
Scope: technehub-labs/dea-metaframework and downstream ECF consumers
Predecessor: None
Depends On: WSF foundational semantic architecture

1. Change Request

Reconcile the Enterprise Concept Framework (ECF) with the current OpenDEA semantic architecture and its downstream implementations.

The ECF shall be positioned as an enterprise organizing framework within OpenDEA, rather than as the foundational ontology of the enterprise or world.

The resulting architecture shall distinguish:

World Semantic Foundation
        │
        ▼
OpenDEA Core Semantics
        │
        ├── ECF Profile
        │       │
        │       ▼
        │   ECF Coordinates
        │
        ├── Business Profile
        ├── Data Profile
        ├── Technology Profile
        └── other OpenDEA Profiles
                │
                ▼
        OpenDEA Metamodel
                │
                ▼
        Reference Catalogs

WSF provides foundational semantic grounding; OpenDEA specializes that grounding for enterprise architecture; ECF provides the enterprise-domain/lifecycle organizing framework.

The WSF architecture explicitly establishes that OpenDEA consumes and specializes WSF semantics while remaining independently governed.

2. Architectural Boundary

The following distinctions shall be normative:

WSF
≠ OpenDEA
≠ ECF
≠ DEA Metamodel
≠ Catalog

and:

ECF
    organizes and contextualizes
        ↓
OpenDEA Metamodel
    formally represents
        ↓
Catalogs
    instantiate governed concepts

3. Current-State Reconciliation

The live dea-metamodel already implements a core/profile architecture in which Core contains stable semantic anchors and profiles extend Core without redefining it. The ECF is already represented as one such profile. (GitHub⁠)

Therefore this CR shall document and reconcile the existing architecture rather than create a competing ECF ontology.

4. Downstream Contract

The following downstream interpretation is already present and shall be adopted as the ECF contract:

Business Capability

The ECF coordinates capabilities but does not generate them. Capability identity remains independent of ECF coordinate. (GitHub⁠)

Business Process

The ECF intersection establishes Process Context; it does not itself constitute a Business Process. (GitHub⁠)

Metamodel

The metamodel remains the canonical semantic model. Its normative specification is the source from which schemas and other representations are derived. (GitHub⁠)

5. Required Changes

dea-metaframework shall:

* replace any implication that ECF is the world or OpenDEA ontological foundation;
* identify ECF as an OpenDEA organizing framework/profile;
* establish the WSF → OpenDEA → ECF relationship;
* establish the ECF → Metamodel → Catalog relationship;
* remove contradictory claims from README, REPORT, framework artifacts and schemas;
* explicitly identify downstream repositories as consumers of the ECF contract.

6. Acceptance Criteria

* [ ]	ECF architectural position is explicitly documented.
* [ ]	WSF/OpenDEA/ECF boundaries are documented.
* [ ]	ECF/metamodel/catalog boundaries are documented.
* [ ]	Current OpenDEA profile architecture is reflected.
* [ ]	No ECF artifact claims authority over WSF semantics.
* [ ]	No catalog is described as being generated merely by enumerating ECF cells.
* [ ]	README and REPORT agree with downstream implementations.
