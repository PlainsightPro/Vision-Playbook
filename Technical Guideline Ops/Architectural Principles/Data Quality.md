# Data Quality

## Overview
Data quality means “fit for purpose” for the defined use case. We make data trustworthy, explainable, and on time by setting clear expectations (contracts), preventing defects early, and monitoring continuously.

## Core principles
- **Business-fit**: define the intended decisions/metrics and the minimum acceptable quality per dataset.
- **Prevent > detect**: enforce schemas, keys, and valid domains at ingestion; don’t let bad data flow downstream.
- **Observable by default**: track freshness, volume, schema, distribution, and rule outcomes for every important dataset.
- **Fail loudly, degrade safely**: block loads on critical rule failures; otherwise quarantine bad rows and keep the rest flowing.
- **Single ownership**: one accountable owner per dataset with documented SLOs and a runbook.
- **Automate close to data**: codify rules as tests in pipelines/SQL and run on every build or load.

## Do's & Don'ts

**Do**
- Write a simple **data contract** per source/table: schema, keys, valid values, cadence, expected volume, and SLAs.
- Implement checks at three levels: **schema** (columns, types), **data** (nulls, ranges, uniqueness), **business** (aggregates reconcile, logical rules).
- Track **freshness** (max timestamp vs. now), **volume** (row deltas), and **distribution** (min/max/avg/top N categories).
- Maintain a **DQ results table** (per dataset, per run) with metrics and pass/fail; keep 30–90 days of history.
- Reconcile facts to source-of-truth totals (e.g., daily revenue within tolerance); document acceptable variance.
- Quarantine invalid rows with an `IsValid` flag and `InvalidReason` when safe; exclude them from semantic models.
- Centralize **reference data/code sets** with change control; validate against them.
- Document assumptions, edge cases, and known gaps in the model readme.

**Don't**
- Don’t accept silent schema drift; treat unexpected columns/types as a breaking change.
- Don’t relate on dirty or unstable natural keys; use surrogates and preserve naturals as attributes. See [[Primary & Foreign Keys]].
- Don’t spread the same rule logic across many tools; reuse macros/UDFs or package checks.
- Don’t hide defects; expose DQ status to consumers and annotate affected reports.
- Don’t hard-code magic values; codify as parameters or reference tables.

## Dimensions and example checks
- **Accuracy**: compare against a trusted source or control totals.
  - Example: `SUM(FactSales.Amount)` is within 0.5% of ERP for the same period.
- **Completeness**: required fields present; expected rows received.
  - Example: no nulls in `OrderID`; load row count within expected band.
- **Consistency**: same business rules across sources; conform units/codes.
  - Example: `CurrencyCode` always ISO-4217; one canonical product hierarchy.
- **Timeliness/Freshness**: data arrives within SLO; staleness monitored.
  - Example: last `LoadTimestamp` < 60 minutes for hourly datasets.
- **Validity**: values inside domains, formats, and ranges.
  - Example: `Email` matches regex; `Quantity >= 0`; dates within legal horizon.
- **Uniqueness**: no duplicates in keys or natural identifiers where required.
  - Example: `CustomerNaturalKey` unique in `DimCustomer` for current rows.
- **Integrity**: referential relationships hold or are flagged and handled.
  - Example: no orphan `CustomerID` values in facts; otherwise route to quarantine.

## Operating model & SLOs
- **Ownership**: each dataset has an owner and secondary; contact in metadata.
- **SLOs**: define freshness, availability, and quality thresholds (e.g., 99% loads on time, <0.1% invalid rows in facts).
- **Runbook**: triage steps, severities, rollback/patch approach, and communication templates.
- **Alerting**: on-call alerts for critical failures; daily digest for warnings.
- **Release gates**: block deployments when critical DQ tests fail; allow non-critical with clear annotation.

## Practical SQL checks (examples)
Schema present and types correct
```sql
-- Columns exist with expected types (illustrative; adapt to platform)
SELECT column_name, data_type
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'FactSales'
  AND (column_name, data_type) IN (
    ('OrderID','int'),
    ('CustomerID','int'),
    ('OrderDate','date'),
    ('Amount','decimal')
  );
```

Primary key uniqueness
```sql
SELECT COUNT(*) AS Duplicates
FROM (
  SELECT OrderID, COUNT(*) c
  FROM FactSales
  GROUP BY OrderID
  HAVING COUNT(*) > 1
) d;
```

Referential integrity (no orphan FKs)
```sql
SELECT COUNT(*) AS Orphans
FROM FactSales f
LEFT JOIN DimCustomer d ON d.CustomerID = f.CustomerID
WHERE d.CustomerID IS NULL;
```

Freshness
```sql
SELECT DATEDIFF(minute, MAX(LoadTimestamp), SYSDATETIME()) AS MinutesSinceLastLoad
FROM FactSales;
```

Distribution/validity
```sql
SELECT
  MIN(Amount) AS MinAmount,
  MAX(Amount) AS MaxAmount,
  AVG(Amount) AS AvgAmount,
  SUM(CASE WHEN Amount < 0 THEN 1 ELSE 0 END) AS NegativeCount
FROM FactSales;
```

## Quality telemetry table (example)
Maintain a small table for each dataset/run to store metrics and rule outcomes. Example shape:

- `DatasetName` (e.g., `FactSales`)
- `RunId` / `LoadTimestamp`
- `MetricName` (e.g., `row_count`, `freshness_minutes`, `pk_duplicates`, `fk_orphans`)
- `MetricValue`
- `Status` (`PASS`/`WARN`/`FAIL`)
- `Details` (optional JSON)

Expose this to stakeholders and dashboards; use it to spot trends and regressions.

## Power BI notes
- Keep DQ enforcement in the warehouse/ETL; surface status in the model.
- Add a small `QualitySummary` table to your semantic model with key metrics and a **banner** or **card** visual to warn on incidents.
- Use `IsValid` filters in report tables to exclude quarantined rows by default.

## Related
- [[Data Modeling]]
- [[Primary & Foreign Keys]]

## Notes & exceptions
- Some datasets are inherently “best-effort” (e.g., clickstreams). Set realistic thresholds and document known caveats.
- When upstream systems are inconsistent, add a **standardization** step and document the chosen canonical forms.
- For one-off data loads, annotate the run and relax rules intentionally with sign-off.
