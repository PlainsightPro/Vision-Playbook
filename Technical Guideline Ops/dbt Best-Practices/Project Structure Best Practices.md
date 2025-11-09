# dbt Project Structure Best Practices

## Overview
Design your dbt repo so the filesystem narrates how data travels from raw sources to curated front-room outputs. A tidy tree makes onboarding faster, testing easier, and CI/CD predictable. Use layers, conventions, and shared configuration to avoid model sprawl.

> [!tip] 💡 Golden Rule
> Each folder should describe *what problem the models solve*, not who authored them. Align structure to the business process or data contract.

> [!warning] ⚠️ Keep dbt’s Top-Level Skeleton
> Stick to dbt’s default root folders (`models/`, `snapshots/`, `tests/`, `macros/`, `analysis/`, etc.). Only organize within those directories—renaming or reshuffling the top-level structure breaks conventions, tooling, and contributor expectations.

---

## Canonical Layering

```text
models/
├─ staging/
│  ├─ sap/
│  │  ├─ _sources.yml          # Source definitions, freshness, owner metadata
│  │  ├─ stg_sap__charges.sql           # One-to-one with source() tables
│  │  └─ stg_sap__customers.sql
│  └─ salesforce/
│     └─ ...
├─ intermediate/
│  ├─ finance/
│  │  └─ int_finance_orders_enriched.sql
│  ├─ marketing/
│  └─ shared/
├─ conformed/
│  ├─ conf_customer.sql
│  ├─ conf_product.sql
│  └─ _models.yml              # Contracts, ownership, tests
└─ front_room/
   ├─ dimensional/
   │  ├─ dim_customer.sql
   │  └─ dim_product.sql
   │  └─ fact_orders.sql
   ├─ master/
   ├─ feature_store/
   └─ one_big_table/
```

### Staging (Source-Conformed)
- One dbt model per `source()` table, named `stg_<source>__<entity>`.
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
- Keep only the transformations needed to shape inputs for Conformed - avoid duplication of staging logic or presentation metrics.

### Conformed (Integrated Models)
- Integrate and cleanse data across domains so downstream teams inherit harmonized entities (customers, products, orders).
- Apply SCD rules, survivorship (choosing the “winning” version of a record when multiple sources disagree), and cross-source enrichment (merging attributes from different systems); document contracts, tests, and ownership in `_models.yml`.
- Name models `conf_<entity>` (e.g., `conf_customer`), materialize as `table`/`incremental`, and treat this layer as the reusable interface for front-room consumers.

### Front Room (Presentation & Experience)
- Deliver business-ready dimensional models, fact tables, master data, feature stores, and other consumer outputs that BI/ML teams query directly.
- Organize subfolders by consumption pattern (`front_room/dimensional`, `front_room/fact`, `front_room/feature_store`, `front_room/master`, `front_room/one_big_table`) and use business-friendly names (no prefixes) for models.
- Keep transformations light: the goal is to expose curated tables, not re-implement conformed logic. Default to `view` for agility, switching to `table`/`incremental` only when SLA or cost requires it.

---

## YAML + Metadata Strategy
- Keep `_sources.yml` beside the staging models it describes, include freshness, descriptions, and tests on source-data. 
- Store `_models.yml` per folder to apply tests and column docs. Keeping this metadata beside the code ensures business context and ownership stay synchronized with the transformations they depend on.
- Apply tags for lineage groups (`["stripe"]`, `["incremental"]`) to unlock targeted runs such as `dbt run --select tag:finance`.

---

## Naming & File Conventions

| Layer        | Naming Pattern              | Typical Materialization | Notes |
|--------------|-----------------------------|-------------------------|-------|
| Staging      | `<source>_<entity>`    | `view`                  | Mirrors upstream grain, grouped by source folders. |
| Intermediate | `<domain>_<action>`     | `ephemeral` or `view`   | Domain folders communicate owners - verbs explain intent (`int_finance_orders_enriched`). |
| Conformed    | `<domain>_<entity>`    | `table` / `incremental` | Harmonized, reusable entities that supply multiple experiences. |
| Front Room   | `<business_concept>`        | `view` | Consumer-facing names (e.g., `orders`, `customers_daily`, `dim_finance_account`). |


