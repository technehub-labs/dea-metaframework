# Framework Design Principles

The framework obeys eight rules:

1. **Universality.** The framework must apply to any enterprise — a
   50-person charity, a 500,000-person telco, a hospital, a government
   agency — without modification.

2. **MECE.** The two partitions (domains and stages) are mutually exclusive
   and collectively exhaustive. A capability belongs to exactly one domain;
   an object is in exactly one stage at a time.

3. **Lifecycle continuity.** Every business object passes through every
   stage. Nothing is "born live."

4. **Orthogonality.** The two axes are independent. Knowing an object's
   domain does not determine its stage, and vice versa.

5. **Minimality.** The fewest constructs that fully describe the
   enterprise. Seven domains and seven stages are the minimum.

6. **Traceability.** Every cell traces to an owner (actor), a state
   (stage), and a set of dependencies (other cells).

7. **Evolvability.** The matrix is versioned. Each planning cycle produces a
   snapshot; diffing reveals what changed.

8. **Bottom-up.** Derived from the axiom, not imported from eTOM, ITIL,
   COBIT, Zachman, or any other named framework.

---

## Visual Representation

### The Matrix at a Glance

```
| Domain \ Stage  | Cnc | Des | Bld | Act | Opr | Imp | Ret |
|----------------|-----|-----|-----|-----|-----|-----|-----|
| Governance     |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |
| Supply         |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |
| People         |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |
| Customer       |  ●  |  ●  |  ●  |  ★  |  ●  |  ●  |  ●  |
| Product        |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |  ●  |
| Operations     |  ●  |  ●  |  ★  |  ●  |  ★  |  ●  |  ●  |
| Finance        |  ●  |  ●  |  ●  |  ●  |  ★  |  ●  |  ●  |

  ● = active   ★ = high-risk handoff
```

### Rendering Guidance

- **Color:** One accent per domain; stages share a neutral ramp. Never
  color both axes.
- **Grouping:** Group cells by domain (row) with a hairline. Do not group by
  stage.
- **Legend:** Mark high-risk handoffs (★) and steady-state (●). Keep the
  legend to two glyphs.
- **Emphasis:** When presenting, highlight one row or one column — never the
  whole grid at once.