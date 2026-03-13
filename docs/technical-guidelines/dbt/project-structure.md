# dbt Project Structure Best Practices

## Overview
Design your dbt repo so the filesystem narrates how data travels from raw sources through Bronze (landing/staging) and Silver (ADS) into a grouped Gold presentation layer. A tidy tree makes onboarding faster, testing easier, and CI/CD predictable. Use layers, conventions, and shared configuration to avoid model sprawl.

> [!tip] Golden Rule
> Each folder should describe *what problem the models solve*, not who authored them. Align structure to the business process or data contract.

> [!warning] Keep dbt's Top-Level Skeleton
> Stick to dbt's default root folders (`models/`, `snapshots/`, `tests/`, `macros/`, `analysis/`, etc.). Only organize within those directories - renaming or reshuffling the top-level structure breaks conventions, tooling, and contributor expectations.

---

## Canonical Layering

```
models/
├─ bronze/                     # Landing + Staging (raw & source-aligned)
│  ├─ landing/                 # Optional - external tables or incremental ingestion
│  │  ├─ sap/
│  │  │  ├─ _sources.yml
│  │  │  ├─ lnd_sap_charges.sql
│  │  │  └─ lnd_sap_customers.sql
│  │  └─ salesforce/
│  └─ staging/
│     ├─ sap/
│     │  ├─ _sources.yml       # Source definitions, freshness, owner metadata
│     │  ├─ stg_sap_charges.sql # One-to-one with source() tables
│     │  └─ stg_sap_customers.sql
│     └─ salesforce/
├─ silver/                     # Intermediate + ADS (cleansed, integrated)
│  ├─ intermediate/
│  │  ├─ int_orders_enriched.sql
│  │  ├─ int_orders_flattened.sql
│  │  └─ ...
│  └─ ads/
│     ├─ ads_customer.sql
│     ├─ ads_product.sql
│     └─ _models.yml           # Contracts, ownership, tests
└─ gold/                       # Gold (presentation)
   ├─ star_dim_fact/
   │  ├─ d_customer.sql
   │  ├─ d_product.sql
   │  └─ f_orders.sql
   └─ feature_store/
```

### Landing (Optional Source-ADS)
- **Optional layer** for external tables, incremental-only ingestion, or raw file processing before staging.
- Name models `lnd_<source>_<entity>` if using this layer, otherwise skip directly to staging.
- Organize by source system (`landing/sap`, `landing/salesforce`) for consistency.
- Useful when:
  - Data arrives via external tools (Fivetran, Airbyte) that populate external tables
  - Incremental-only data needs preprocessing before merging into staging
  - Raw files need parsing (JSON, Parquet) before source definitions
  - Change data capture (CDC) streams require transformation
- **Can be skipped** when staging can directly reference `source()` tables without preprocessing.

> [!tip] When to Use Landing
> Use landing when external tools or incremental patterns require a preprocessing step before staging. If your sources are clean and directly queryable, skip this layer and start at staging.

### Staging (Source-ADS)
- One dbt model per `source()` table, named `stg_<source>_<entity>`.
- Keep logic atomic: rename, cast, and normalize fields - never join or aggregate.
- Organize folders by source system (`staging/sap`, `staging/salesforce`) so commands like `dbt build --select staging.sap+` work intuitively.
- Set default materialization to `view` via `dbt_project.yml`, e.g.

```yaml
models:
  my_project:
    staging:
      materialized: view
      tags: ["staging"]
```

### Intermediate (Business Logic)
- Organize by domain (`finance`, `marketing`, `platform`) to mirror how the business consumes data.
- Compose reusable joins/filters; prefer `ephemeral` materializations unless the model is reused broadly.
- Break heavy logic into `int_<noun>_<verb>` models (`int_finance_orders_enriched`).
- Keep only the transformations needed to shape inputs for ADS - avoid duplication of staging logic or presentation metrics.

### ADS (Integrated Models)
- Integrate and cleanse data across domains so downstream teams inherit harmonized entities (customers, products, orders).
- Apply SCD rules, survivorship (choosing the "winning" version of a record when multiple sources disagree), and cross-source enrichment (merging attributes from different systems); document contracts, tests, and ownership in `_models.yml`.
- Name models `ads_<entity>` (e.g., `ads_customer`), materialize as `table`/`incremental`, and treat this layer as the reusable interface for Gold consumers.
- The ADS layer stores your `dbt_snapshot` models.

### Gold (Presentation & Experience)
- Deliver business-ready dimensional models, fact tables, master data, feature stores, and other consumer outputs that BI/ML teams query directly.
- Organize subfolders by consumption pattern (`gold/star_dim_fact`,  `gold/feature_store`, ...) and use business-friendly names (no prefixes) for models.
- Keep transformations light: the goal is to expose curated tables, not re-implement ADS logic. Default to `view` for agility, switching to `table`/`incremental` only when SLA or cost requires it.

---

## YAML + Metadata Strategy
- Keep `_sources.yml` beside the staging models it describes; include freshness, descriptions, and tests on source data.
- Store `_models.yml` per folder to apply tests and column docs. Keeping this metadata beside the code ensures business context and ownership stay synchronized with the transformations they depend on.
- Apply tags for lineage groups (`["stripe"]`, `["incremental"]`) to unlock targeted runs such as `dbt run --select tag:finance`.

---

## Naming & File Conventions

| Layer        | Naming Pattern              | Typical Materialization | Medallion | Notes |
|--------------|-----------------------------|-------------------------|-----------|-------|
| Landing      | `lnd_<source>_<entity>`    | `external` or `view`    | Bronze    | Optional preprocessing step; use external tables or incremental patterns. Skip if staging can directly reference sources. |
| Staging      | `stg_<source>_<entity>`     | `view`                  | Bronze    | Mirrors upstream grain, grouped by source folders. |
| Intermediate | `int_<domain>_<action>`     | `ephemeral` or `view`   | Silver    | Domain folders communicate owners - verbs explain intent (`int_finance_orders_enriched`). |
| ADS          | `ads_<entity>`              | `table` / `incremental` | Silver    | Harmonized, reusable entities that supply multiple experiences. |
| Gold         | `<business_concept>`        | `view`                  | Gold      | Consumer-facing names (e.g., `orders`, `customers_daily`, `d_finance_account`). |
