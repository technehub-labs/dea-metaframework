# Metrics

Three primary metrics quantify matrix health.

```
// coverage: how full is the matrix?
coverage = |filled cells| / |D × S|

// coupling: how many deps cross cells?
coupling = |{ (a,b) ∈ deps | cell(a) ≠ cell(b) }| / |deps|

// lifecycle completeness: do objects traverse all 7 stages?
lifecycle(o) = |stages(o)| / 7
```

## Reading the metrics

- **Coverage < 0.5** → half-empty matrix: the enterprise is either unstudied
  or genuinely simple (small charity). Investigate which.
- **Coupling > 0.7** → spaghetti enterprise: objects depend on too many
  other cells. Re-cut the matrix or merge cells.
- **Lifecycle completeness < 1.0** → object skipping stages: either the
  object is born mature (legitimate, mark as exception) or work is being
  hidden (audit trigger).

## Worked Example — Telco Subscriber

```
Subscriber lifecycle:
  Customer × Conceive  → Customer × Design  → Customer × Build
  → Customer × Activate  → Customer × Operate  → Customer × Improve  → Customer × Retire

stages(Subscriber) = {Conceive, Design, Build, Activate, Operate, Improve, Retire}
                  = 7
lifecycle(Subscriber) = 7/7 = 1.0
```

## Worked Example — Feature Flag

```
Feature flag lifecycle:
  Product × Conceive  → Product × Design  → Product × Build
  → Product × Activate  → Product × Operate  → Product × Improve  → Product × Retire

stages(FeatureFlag) = 7
lifecycle(FeatureFlag) = 7/7 = 1.0
```

Same lifecycle. Different cell address. Same metric. This is what makes the
framework industry-agnostic.