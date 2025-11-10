# dbt Operations & Testing Playbook

## Operating Principles
Keep dbt operations boring by standardizing how jobs run, how failures alert, and which tests guard each layer. Treat runs as production software pipelines—even if analysts write the SQL.

> [!📝 Run Vocabulary]- 
> - **Development:** local, iterative, `dbt build --select my_model+`
> - **Pre-Prod:** automated validation on feature branches or staging datasets
> - **Production:** scheduled jobs that own SLAs and downstream contracts

---

## Run Types & Commands

| Scenario               | Trigger             | dbt Command(s)                                              | Scope / Notes                                                      |
| ---------------------- | ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| Local development      | Developer CLI / IDE | `dbt build --select my_model+`                              | Fast feedback on a model plus dependencies.                        |
| Pull-request (Slim CI) | CI runner           | `dbt build --select state:modified+`                        | Touch only changed models + children, upload artifacts for review. |
| Scheduled production   | Orchestrator        | `dbt build --select tag:daily` or `dbt build`               | Full slices aligned to SLAs, rely on stored state for performance. |
| Backfill / replay      | Manual CLI / job    | `dbt run --select fact_orders --vars '{start_date: "..."}'` | Recompute historical windows or recover from upstream issues.      |

Document selectors, targets, threads, and variables for each scenario so operators rerun them consistently.

---

## Testing Ladder

> [!important] 🚨 Ship Nothing With Failing Tests
> CI pipelines and scheduled jobs must fail fast on any broken test. Production deployments without a green `dbt test` (or `dbt build`) are not allowed.

> [!tip] 💡 Testing Tactic
> - **Hit sources hard:** Saturate staging/source models with `not_null`, `unique`, freshness, and schema-conformance tests so bad data is blocked before it propagates.  
> - **Guard dimensions & facts:** In the conformed/front-room layers (dimensions & facts), prioritize relationship tests, contracts, and business constraints to ensure metrics stay trustworthy.

### 1. Built-In Data Quality
- Saturate staging and conformed/front-room models with `not_null` and `unique` on natural or surrogate keys; only add these tests to intermediate models when they are high-risk models.
- Use `relationships` to enforce referential integrity between front-room dimension & fact models.
- Attach `accepted_values` to enums and status fields to prevent silent drift.

### 2. Business Logic, Anomaly Tests & Freshness
- Store reusable custom tests in `tests/generic/` (e.g., `test_positive_amounts.sql`).
- Capture scenario-specific checks via singular tests (SQL queries that return zero rows).
- Parameterize tests so new models inherit the logic automatically by referencing macros.
- Configure `freshness` blocks per critical source with warn/error thresholds (e.g., warn after 18h, error after 26h).


---

## Test Coverage Matrix

| Layer        | Core Tests                               | 
|--------------|------------------------------------------|
| Staging      | `not_null`, `unique`, `accepted_values`, `source-freshness`  | 
| Intermediate (only if materialized) | Minimize tests in this layer. Only apply checks on high-risk models and during development | 
| Conformed    | Key uniqueness and relationship depth | 
| Front Room (Dims/Facts) | Contracts, metric-specific assertions, dimensional constraints (e.g., Type 2 checks) | 

> Intermediate models that remain ephemeral should not accumulate dedicated test suites—lean on staging coverage upstream and conformed/front-room constraints downstream.

---

## Lineage & Metadata Visibility
- Publish `dbt docs generate` (HTML or JSON artifacts) every production deployment so the documented DAG, schema catalog, and test results stay current.  
- Feed `manifest.json` and `run_results.json` into your data catalog or lineage tooling so business users can trace dependencies without reading SQL.  

## Performance & Cost Observability
- Prefer incremental models for large tables to avoid full reloads; ensure `is_incremental()` filters limit processing to new partitions.  
- Profile slow queries (warehouse query plan, execution stats) and refactor heavy constructs (e.g., `COUNT DISTINCT`) into pre-aggregations when needed.  
- Review materialization choices periodically—ephemeral chains are great for small datasets but promoting high-cost intermediates to tables can cut runtime and spend.

