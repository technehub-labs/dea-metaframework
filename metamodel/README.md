# Enterprise Concepts Metamodel

**Version 3.0** — Source of truth: [`technehub-labs/dea-metaframework`](https://github.com/technehub-labs/dea-metaframework) (this repo).

## What changed from v2 → v3

| Change | v2 | v3 |
|---|---|---|
| **Layers** | 5 (Strategic / Business / Digital / Technology / Measurement) | **6** (+ **Ecosystem & Value Network (External)** at the top) |
| **Entities** | 19 | **23** (+ Ecosystem Actor, Value Exchange, Collaboration Agreement; Business Function re-added; Journey Touchpoint moved to L1) |
| **Relationships** | 25 | **31** (+6 new external↔internal handoffs) |
| **Color scheme** | Site-dark, fixed | **Light + dark mode** via embedded CSS + `prefers-color-scheme` |
| **Theme control** | None | Auto (OS preference) + class override (`theme-light` / `theme-dark`) |

## Files

| File | What it is |
|------|-----------|
| [`enterprise-concepts.puml`](./enterprise-concepts.puml) | **Canonical source** — PlantUML source. Edit this, then run `python3 postprocess.py` to regenerate the SVG. |
| [`enterprise-concepts-v3.svg`](./enterprise-concepts-v3.svg) | **Rendered SVG** with embedded CSS for light/dark mode. Self-contained — drop it anywhere. |
| [`postprocess.py`](./postprocess.py) | Tool: takes PlantUML's raw SVG output + injects CSS for light/dark mode + site integration. |
| [`README.md`](./README.md) | This file. |

## Entity inventory (23 entities across 6 layers)

### Layer 1 — Ecosystem & Value Network (External) — *new*
- **Ecosystem Actor** — `id, type: (Supplier, Customer, Regulator)`
- **Value Exchange** — `flowType: (Information, Goods, Funds), direction: (Inbound, Outbound)`
- **Journey Touchpoint** — `id, channel` *(moved from Layer 2)*

### Layer 2 — Strategic & Governance (Intent & Rules)
- **Strategic Objective** — `description`
- **Investment Initiative** — `budget: decimal`
- **Collaboration Agreement** — `terms, type: (Cooperative, Mandated)` *new*

### Layer 3 — Business Operating Model (Internal)
- **Value Stream** — `name`
- **Business Capability** — `ecfCoordinates: (Domain, Stage)` *(the ECF anchor)*
- **Business Process** — `sequence: int`
- **Business Function** — `name` *(re-added from v1)*
- **Organizational Unit** — `name`
- **Business Object** — `name`

### Layer 4 — Digital & Intelligence (Data & Brain)
- **Digital Identity** — `type: (Customer, Partner, Bot)`
- **Data Entity** — `name`
- **Information Class** — `securityLevel`
- **Data Product** — `SLA`
- **Event / Event Stream** — `topic`
- **AI / ML Model** — `modelType`

### Layer 5 — Technology & Execution (Systems & Infra)
- **System Function** — `name`
- **API / Service Contract** — `version`
- **Application Component** — `name`
- **Platform Service** — `type: (Compute, DB, Network)`

### Layer 6 — Measurement (Cross-Cutting)
- **Performance Metric**

## Relationship summary (31 relationships)

### Internal — Layer 1
- EA → CA : "engages in"
- CA → VE : "governs"
- EA → SO : "influences"
- VE → JT : "crosses boundary at"
- VE → BO : "transports (payload)"

### Layer 1 → Layer 3/4 (External crosses boundary)
- EA → DI : "represented by"
- JT → DI : "authenticates"

### Internal — Layer 2
- SO → II : "drives"
- II → BC : "funds"

### Internal — Layer 3
- VS → BC : "traverses"
- VS → JT : "terminates at"
- BC → BF : "grouped by"
- BF → OU : "owned by"
- BC → BP : "implemented by"
- BC → BO : "produces/consumes"

### Layer 3 → Layer 4
- BO → DE : "digitized as"

### Layer 3 → Layer 5
- BP → SF : "automated by"

### Internal — Layer 4
- DE → IC : "classified by"
- DE → DP : "curated into"
- DP → API : "exposed via"
- AI → DP : "trained on"
- AI → SF : "enhances / automates"
- SF → EVT : "publishes / subscribes to"
- EVT → DE : "carries payload of"

### Layer 4 ↔ Layer 5
- SF → API : "exposed via"
- API → DE : "serves/exchanges"

### Internal — Layer 5
- SF → AC : "hosted by"
- AC → PS : "deployed on"

### Measurement (Cross-cutting — Layer 6)
- SO → PM : "measured by"
- BC → PM : "evaluated by"
- SF → PM : "evaluated by"

## Light/Dark theme support

The SVG (`enterprise-concepts-v3.svg`) has a `<style>` block embedded that:

1. **Auto-detects** the user's OS preference via `@media (prefers-color-scheme: dark)`
2. **Defaults to light** (PlantUML pastel palette) when no preference or `prefers-color-scheme: light`
3. **Allows explicit override** — add `theme-light` or `theme-dark` class to the `<svg>` element:
   ```html
   <svg class="theme-dark">…</svg>
   ```
4. **CSS variables** at the root enable site integration:
   - `--svg-bg`, `--svg-text`, `--svg-border`
   - `--layer-1-bg` through `--layer-6-bg`
   - `--entity-bg`

To restyle on a specific site, override the CSS variables in a wrapping stylesheet:

```css
.my-container svg {
  --svg-bg: #fafafa;
  --layer-1-bg: #e3f2fd;
  --layer-6-bg: #fce4ec;
}
```

## How the SVG is generated

```bash
# 1. Render the .puml with PlantUML (e.g. via kroki.io or local plantuml.jar)
plantuml -tsvg enterprise-concepts.puml -o raw.svg

# 2. Post-process to add light/dark CSS
python3 postprocess.py raw.svg enterprise-concepts-v3.svg

# 3. Publish enterprise-concepts-v3.svg
```

Cascade: this SVG is the **single source**. The dea-metamodel repo, the `technehub-labs.github.io/metamodel/` viewer, and the root-page Metamoat card all reference this same file. Edit here once → everywhere updates.

## Live sites

| Site | URL |
|------|-----|
| **Meta Framework repo** | https://github.com/technehub-labs/dea-metaframework |
| **Metamodel Explorer** | https://technehub-labs.github.io/metamodel/ |
| **Meta Framework Explorer** | https://technehub-labs.github.io/dea-metaframework/ |
| **TechNeHub Labs root** | https://technehub-labs.github.io |

## See also

- [`../REPORT.md`](../REPORT.md) — Enterprise Concept Framework v2.0 (this metamodel instantiates its constructs)
- [`../framework/matrix.md`](../framework/matrix.md) — The 7×7 ECF matrix that Business Capability's `ecfCoordinates` references
- [`../framework/constructs.md`](../framework/constructs.md) — The 8 formal constructs the metamodel formalizes
- [`technehub-labs/dea-metamodel`](https://github.com/technehub-labs/dea-metamodel) — the parallel repo for downstream catalog schema