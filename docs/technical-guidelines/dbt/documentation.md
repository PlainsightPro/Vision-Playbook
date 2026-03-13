# dbt Documentation Best Practices

!!! info "Purpose"
    Keep documentation current, enforceable, and tied to ownership so reviews can reject incomplete PRs before code is merged.

## Overview
Document every model, source, and column at the same time you build it. Treat docs as part of the definition of the contract for downstream consumers (BI, data apps, ML). Use `_models.yml` and `_sources.yml` colocated with models to keep context close to code and to unlock automated checks.

| Do ƒo.                                                | Don't ƒ?O                                          |
| ----------------------------------------------------- | -------------------------------------------------- |
| Co-locate docs with models/sources in the same folder | Write docs in a separate, rarely updated file      |
| Use `doc()` references to reuse canonical text        | Duplicate long descriptions across many YAML files |
| Declare owners and downstream exposures               | Publish assets without ownership or consumers      |
| Describe the business meaning, not just data type     | Write "String" or "ID" without context             |
| Regenerate docs as part of CI                         | Let docs drift from the manifest/catalog           |

---

## Minimum Documentation Standards
- **Models:** Each model has a description that states business purpose, grain, refresh expectation, and SLA notes where applicable.
- **Sources:** Each source table includes description, owner, freshness, and at least basic tests (not null, uniqueness for keys).
- **Columns:** Describe business meaning, units, and valid ranges; flag PII/SPI columns explicitly.
- **Ownership:** Every model/source carries an `owner` or `team` field so support paths are clear.
- **Contracts:** Use `constraints`/`tests` alongside docs so descriptions and enforcement stay aligned.

!!! tip "Folder-level YAML"
    Use `_models.yml` and `_sources.yml` in each folder (staging, intermediate, ADS, gold). This keeps metadata close to code and enables targeted `dbt build --select staging.*` runs with complete documentation.

---

## Docs Blocks and `doc()` Patterns
Use docs blocks for reusable concepts (definitions, KPIs, governance notes) and reference them via `doc()`. Keep each block short and business-facing.

```sql
{% docs customer_status %}
Customer status reflects the latest lifecycle state. Possible values: `prospect`, `active`, `churned`.  
Applied after survivorship rules in `ads_customer`.
{% enddocs %}
```

```yaml
models:
  - name: ads_customer
    description: "{{ doc('customer_status') }}"
    columns:
      - name: customer_id
        description: "Persistent surrogate key for the customer entity"
        tests: [not_null, unique]
      - name: status
        description: "{{ doc('customer_status') }}"
      - name: first_order_date
        description: "Date of first successful order (UTC)"
```

- Keep doc block names stable; avoid renaming without updating references.
- Use `doc()` for repeated business terms (definitions, SLAs, eligibility) rather than duplicating text.
- Avoid templating inside docs blocks that depends on adapter-specific functions; keep them portable.

---

## Exposures (Downstream Consumers)
- Declare Power BI reports, semantic models, notebooks, and scheduled jobs as exposures so lineage reflects true consumers.
- Include `url`, `owner`, and `maturity`. For Fabric/Power BI, link to the report or dataset URL; for other adapters, link to the consuming app or API.
- Capture critical dependencies (facts/dimensions) in `depends_on` to surface impact analysis.

```yaml
exposures:
  - name: sales_exec_dashboard
    type: dashboard
    maturity: high
    url: https://app.powerbi.com/groups/<workspace>/reports/<report_id>
    owner:
      name: Sales Analytics
      email: analytics@example.com
    depends_on:
      - ref('f_sales')
      - ref('d_customer')
    description: "Executive view of revenue, pipeline, and retention metrics."
```

!!! note "Adapter-specific considerations"
    URL formats and authentication vary by adapter; keep the exposure definition adapter-agnostic and store secrets in the consuming platform, not in dbt.

---

## Docs Generation Workflow
- **Local preview:** `dbt docs generate` then `dbt docs serve --port 8080 --no-browser` during development.
- **CI expectations:** Regenerate docs on every PR that touches models/sources; fail CI when undocumented models/columns are introduced.
- **Artifacts handling:** Publish `target/manifest.json` and `target/catalog.json` to your chosen wiki/storage location for reference; avoid committing the entire `target/` folder.
- **Shareable output:** If hosting HTML, keep it outside the repo (static storage or wiki attachment) and note the publish location in the README for the dbt project.

```sh
dbt docs generate --target prod
dbt docs serve --port 8080 --no-browser
```

---

## Documentation Definition of Done
- [ ] Every new/changed model and source has a description covering purpose, grain, and refresh expectations.
- [ ] All new columns carry business-meaningful descriptions; PII/SPI flagged.
- [ ] Ownership set (team/email) for models and sources.
- [ ] Applicable tests added (not null, unique, accepted values) and aligned with descriptions.
- [ ] Exposures updated/added for any new downstream consumer (reports, jobs, APIs).
- [ ] `dbt docs generate` runs cleanly with no undocumented items; artifacts published to the agreed location.


---

## Related Pages
- [Third Party Tooling](../power-bi/third-party-tooling.md)
- Free Packages (coming soon)
