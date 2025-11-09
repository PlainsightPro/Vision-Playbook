# dbt SQL Style & Configuration

## SQL File Structure & Style
- **Config first:** Always open with `{{ config(...) }}` (or a concise comment) so overrides are obvious. Add a blank line before the first CTE.
- **CTE runway:** Chain CTEs in logical order - sources ➜ transformations ➜ final projection—and document major blocks with short comments.
- **Alias discipline:** Use lowercase snake_case aliases, select explicit columns (no `select *`), and alias each `ref()`/`source()` once.
- **Deterministic ordering:** End with a single `final` CTE (or last `select`) to make diffs predictable and enforce “one exit point”.
- **Macro + var hygiene:** Centralize reusable expressions in macros and read runtime toggles from `var()`/`env_var()` instead of hardcoding constants.
- **Open-source employment**: Don't reinvent the wheel. There are open-source packages online vetted by dbt-labs that contain helpful macros.
- **Whitespace conventions:** Uppercase SQL keywords, place joins on new lines, and aim for ≤120 characters per line for Git-friendly diffs.

---

## Configuration Inheritance
- Define defaults high in `dbt_project.yml` (materializations, tags, quoting) and override only when necessary.
- Example: enforce quoting + incremental strategy for Conformed and Front Room folders.

```yaml
models:
  my_project:
    conformed:
      +materialized: table
      +on_schema_change: append_new_columns
    front_room/logistics:
      +incremental_strategy: merge
      +unique_key: order_id
```

> [!warning] ⚠️ Avoid Ad-Hoc Overrides  
> Scattered `{{ config(...) }}` blocks make maintenance difficult. Prefer path-level settings so reviewers can reason about behavior from the tree alone.


---

## Example Model (Putting It Together)

```sql
{{ config(
    materialized = 'incremental',
    unique_key = 'order_id',
    on_schema_change = 'append_new_columns'
) }}

with
-- Pull only the columns we need from the source system
source_orders as (
    select
        order_id,
        customer_id,
        order_status,
        order_total_cents,
        order_date,
        updated_at
    from {{ source('commerce', 'orders') }}
    {% if is_incremental() %}
        where updated_at >= (select coalesce(max(updated_at), '1900-01-01') from {{ this }})
    {% endif %}
),

-- Apply business-friendly renames and units
staged_orders as (
    select
        order_id,
        customer_id,
        {{ normalize_status('order_status') }} as order_status,
        order_total_cents / 100.0 as order_total_usd,
        order_date::date as order_date,
        updated_at
    from source_orders
),

-- Join to the conformed customer dimension for attributes
orders_with_customer as (
    select
        o.order_id,
        o.customer_id,
        c.customer_type,
        c.region,
        o.order_status,
        o.order_total_usd,
        o.order_date,
        o.updated_at
    from staged_orders as o
    left join {{ ref('conf_customer') }} as c
        on o.customer_id = c.customer_id
),

-- Final CTE prepares the fact rows
final as (
    select
        order_id,
        customer_id,
        customer_type,
        region,
        order_status,
        order_total_usd,
        order_date,
        updated_at,
        current_timestamp as loaded_at
    from orders_with_customer
)

select * from final
```
