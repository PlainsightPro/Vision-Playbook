---
description: "dbt operations and testing playbook: run types, Slim CI, testing ladder with coverage matrix, freshness checks, and performance observability."
---

# dbt Operations & Testing Playbook

## Operating Principles
Keep dbt operations boring by standardizing how jobs run, how failures alert, and which tests guard each layer. Treat runs as production software pipelines - even if analysts write the SQL.

??? note "Run Vocabulary"
    - **Development:** local, iterative, `dbt build --select my_model+`
    - **Pre-Prod:** automated validation on feature branches or staging datasets
    - **Production:** scheduled jobs that own SLAs and downstream contracts

---

## Run Types & Commands

| Scenario               | Trigger             | dbt Command(s)                                              | Scope / Notes                                                      |
| ---------------------- | ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| Local development      | Developer CLI / IDE | `dbt build --select my_model+`                              | Fast feedback on a model plus dependencies.                        |
| Pull-request (Slim CI) | CI runner           | `dbt build --select state:modified+`                        | Touch only changed models + children, upload artifacts for review. |
| Scheduled production   | Orchestrator        | `dbt build --select tag:daily` or `dbt build`               | Full slices aligned to SLAs, rely on stored state for performance. |
| Backfill / replay      | Manual CLI / job    | `dbt run --select fact_orders --vars '{start_date: "..."}'` | Recompute historical windows or recover from upstream issues.      |
| Exposure-driven refresh | Downstream refresh dependency (e.g. Power BI dataset refresh) | `dbt build --select +exposure:sales_exec_dashboard` | Rebuild only what a specific report/job depends on, ahead of its own refresh schedule. |

Document selectors, targets, threads, and variables for each scenario so operators rerun them consistently.

---

## Orchestrating with Exposures & Selectors
Exposures (see [documentation](documentation.md)) aren't just documentation - the `exposure:` selector method lets an orchestrator target exactly the models a downstream consumer needs, instead of a full run or a best-guess tag.

- `dbt build --select +exposure:sales_exec_dashboard` - rebuild everything upstream of one exposure before its scheduled refresh.
- `dbt list --select +exposure:sales_exec_dashboard` - dry-run/preview the scope for impact analysis before changing a shared model.

### Reusable Named Selectors
Define selection criteria once in `selectors.yml` (union, intersection, exclude) and reference them by name (`dbt build --selector <name>`) so scheduled jobs and CI stay consistent instead of hardcoding long `--select` strings across environments.

!!! tip "💡 Combining Tags & Exposures for Cadence Separation"
    A single exposure can be fed by models that need different refresh cadences, and a single tag (e.g. `daily`) can span multiple unrelated exposures. Intersecting `exposure:` with `tag:` lets an orchestrator run "only the daily-cadence models that feed this dashboard" separately from its weekly slice, instead of over- or under-building.

`exclude` carves models back out of a selection - e.g. skip anything tagged `quarantined` (known-broken or under repair) so a single bad model doesn't block the whole daily build, without having to redefine the intersection above.

```yaml
selectors:
  - name: sales_dashboard_daily
    description: "Daily-cadence models feeding the sales exec dashboard"
    definition:
      method: intersection
      value:
        - method: exposure
          value: sales_exec_dashboard
          parents: true
        - method: tag
          value: daily
      exclude:
        - method: tag
          value: quarantined

  - name: sales_dashboard_weekly
    description: "Weekly-cadence models feeding the sales exec dashboard"
    definition:
      method: intersection
      value:
        - method: exposure
          value: sales_exec_dashboard
          parents: true
        - method: tag
          value: weekly
```

Two separate orchestrator jobs (daily schedule vs. weekly schedule) each call their own selector - `dbt build --selector sales_dashboard_daily` / `dbt build --selector sales_dashboard_weekly` - keeping cadence and downstream ownership consistent instead of one job over-building or the other missing dependencies.

> Keep exposure names and selector names stable once orchestrator/CI configs reference them; see [project structure](project-structure.md) for tag conventions.

---

## Testing Ladder

??? warning "Ship Nothing With Failing Tests"
    CI pipelines and scheduled jobs must fail fast on any broken test. Production deployments without a green `dbt test` (or `dbt build`) are not allowed.
    
    !!!tip "Testing Tactic"
        - **Hit sources hard:** Saturate staging/source models with `not_null`, `unique`, freshness, and schema-conformance tests so bad data is blocked before it propagates.  
        - **Guard dimensions & facts:** In the ADS/Gold layers (dimensions & facts), prioritize relationship tests, contracts, and business constraints to ensure metrics stay trustworthy.

### 1. Built-In Data Quality
- Saturate staging and ADS/Gold models with `not_null` and `unique` on natural or surrogate keys; only add these tests to intermediate models when they are high-risk models.
- Use `relationships` to enforce referential integrity between Gold-layer dimension & fact models.
- Attach `accepted_values` to enums and status fields to prevent silent drift.

### 2. Business Logic, Anomaly Tests & Freshness
- Store reusable custom tests in `tests/generic/` (e.g., `test_positive_amounts.sql`).
- Capture scenario-specific checks via singular tests (SQL queries that return zero rows).
- Parameterize tests so new models inherit the logic automatically by referencing macros (see [DRY - Don't Repeat Yourself](../architectural-principles/dry-dont-repeat-yourself.md) for patterns).
- Configure `freshness` blocks per critical source with warn/error thresholds (e.g., warn after 18h, error after 26h).


---

## Test Coverage Matrix

| Layer        | Core Tests                               |
|--------------|------------------------------------------|
| Staging      | `not_null`, `unique`, `accepted_values`, `source-freshness`  |
| Intermediate (only if materialized) | Minimize tests in this layer. Only apply checks on high-risk models and during development |
| ADS    | Key uniqueness and relationship depth |
| Gold (Dims/Facts) | Contracts, metric-specific assertions, dimensional constraints (e.g., Type 2 checks) |

> Intermediate models that remain ephemeral should not accumulate dedicated test suites - lean on staging coverage upstream and ADS/Gold constraints downstream.

---

## Lineage & Metadata Visibility
- Publish `dbt docs generate` (HTML or JSON artifacts) every production deployment so the documented DAG, schema catalog, and test results stay current.  
- Feed `manifest.json` and `run_results.json` into your data catalog or lineage tooling so business users can trace dependencies without reading SQL.  

## Performance & Cost Observability
- Prefer incremental models for large tables to avoid full reloads; ensure `is_incremental()` filters limit processing to new partitions.  
- Profile slow queries (warehouse query plan, execution stats) and refactor heavy constructs (e.g., `COUNT DISTINCT`) into pre-aggregations when needed.  
- Review materialization choices periodically - ephemeral chains are great for small datasets but promoting high-cost intermediates to tables can cut runtime and spend.
