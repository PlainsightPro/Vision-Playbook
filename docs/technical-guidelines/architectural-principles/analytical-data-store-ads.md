# Analytical Data Store (ADS)

!!! info "Core Concept"
    The **Analytical Data Store (ADS)** is our Medallion **Silver** layer. It bridges Landing/Staging (Bronze) and the Gold layer (business products) by turning raw, source-aligned data into clean, integrated, and history-aware entities that dimensional models, feature stores, and downstream products can rely on.

## Why "Analytical Data Store"?

We keep the semantic name **ADS** to make responsibilities explicit while aligning it to the Medallion Silver layer.

### ADS vs Operational Data Store (ODS)

| Aspect | Operational Data Store (ODS) | Analytical Data Store (ADS) |
|--------|------------------------------|-----------------------------|
| Purpose | Near real-time operational reporting and monitoring | Integrated, cleansed data for analytics and history |
| Update frequency | High-frequency (near real-time) | Scheduled batch or micro-batch |
| Data structure | Often normalized, optimized for transactions | Denormalized, optimized for analysis and integration |
| Usage pattern | Operational queries (current state) | Analytical queries (trends, history, cross-source integration) |
| Historical tracking | Limited or none | Snapshot-friendly; SCD-ready |
| Primary consumers | Operational systems, dashboards | Dimensional models, feature stores, data scientists |

### ADS vs Dimensional Model (Dimensions & Facts)

| Aspect | Analytical Data Store (ADS) | Dimensional Model (Dims & Facts) |
|--------|----------------------------|----------------------------------|
| Focus | Integration and data quality | Business-optimized consumption |
| Structure | Denormalized entities | Star schema (Facts + Dimensions) |
| SCD approach | Snapshot tables can track all attributes (SCD2) | Dimensions selectively track attributes (Type 0/1/2 per need) |
| Granularity | Entity-level (one table per entity) | Business-process level (facts + supporting dimensions) |
| Consumers | Data engineers, analytics engineers | Business users, BI tools, ML models |

!!! note "Separation of concerns"
    ADS carries the heavy lifting for conformance, history, and integration. Gold-layer models focus on business meaning and performance rather than rebuilding history logic.

## Purpose and Core Transformations

ADS sits between the Staging/Intermediate steps and the Dimensional Model. It feeds Gold-layer outputs (Dims/Facts, OBTs, Feature Stores) and [Master Data](master-data.md).

- **Data quality validation**: Enforce rules, quarantine errors.
- **Denormalization**: Flatten normalized structures for usability.
- **Multi-source integration**: Merge overlapping entities from multiple systems.
- **History readiness**: Provide SCD-friendly snapshots so downstream models do not reimplement change tracking.

## Table Types: Base and Snapshot

| Table type | Purpose | Rows per entity | History approach | Naming convention |
|------------|---------|-----------------|------------------|-------------------|
| **Base tables** | Current, cleansed state | One current row | Overwrite changes (Type 1) | `ADS_<Entity>` (for example `ADS_Customer`) |
| **Snapshot tables** | Historical versions | Multiple rows per entity | Track all attribute changes (Type 2) | `ADS_<Entity>_Snapshot` (for example `ADS_Customer_Snapshot`) |

!!! warning "Snapshot vs Dimension"
    ADS snapshots capture every attribute change so downstream consumers can choose how to model history. Dimension tables in Gold selectively track only the attributes that matter to the business.

### Base Tables (current state)

**Characteristics**
- One row per entity (latest state)
- Denormalized structure with data quality enforced
- Multi-source integration applied

**Example**
```sql
CREATE TABLE ADS_Customer
(
    CustomerID INT NOT NULL PRIMARY KEY,
    CustomerNumber VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    AddressLine1 VARCHAR(100),
    City VARCHAR(50),
    StateProvince VARCHAR(50),
    Country VARCHAR(50),
    CustomerSegment VARCHAR(20),
    CreditRating VARCHAR(10),
    T_CreatedRunId UNIQUEIDENTIFIER NOT NULL,
    T_ModifiedRunId UNIQUEIDENTIFIER NOT NULL,
    T_CreatedDateTime DATETIME NOT NULL,
    T_ModifiedDateTime DATETIME NOT NULL
);
```

### Snapshot Tables (historical tracking)

**Characteristics**
- Multiple rows per entity (per version)
- `T_ValidFromDateTime`, `T_ValidToDateTime`, `T_IsCurrent` columns
- Default approach: track all attribute changes with SCD Type 2 (adjust if justified)

**Example**
```sql
CREATE TABLE ADS_Customer_Snapshot
(
    CustomerSnapshotID INT NOT NULL PRIMARY KEY,
    CustomerID INT NOT NULL,
    CustomerNumber VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    AddressLine1 VARCHAR(100),
    City VARCHAR(50),
    StateProvince VARCHAR(50),
    Country VARCHAR(50),
    CustomerSegment VARCHAR(20),
    CreditRating VARCHAR(10),
    T_ValidFromDateTime DATETIME NOT NULL,
    T_ValidToDateTime DATETIME NULL,
    T_IsCurrent BIT NOT NULL,
    T_CreatedRunId UNIQUEIDENTIFIER NOT NULL,
    T_ModifiedRunId UNIQUEIDENTIFIER NOT NULL,
    T_CreatedDateTime DATETIME NOT NULL,
    T_ModifiedDateTime DATETIME NOT NULL
);
```

!!! tip "When to create snapshots"
    Create a snapshot only when downstream analysis needs attribute change history, compliance requires it, or dimensions will consume the history. Transaction-style tables (for example invoices) are already point-in-time and rarely need snapshots.

## Key Transformations in Silver (ADS)

### Data quality validation
- Schema enforcement and required field checks
- Referential integrity where applicable
- Business rule validation (for example `OrderDate <= ShipDate`)

### Progressive denormalization

| Before (normalized) | After (denormalized) |
|---------------------|----------------------|
| Customer + Address tables | Customer with embedded address columns |
| Product + Category + Subcategory | Product with category/subcategory columns |
| Monthly columns (Jan, Feb, Mar...) | Month + Value rows (unpivoted) |

### Source system integration
- Deduplicate across systems.
- Standardize codes and naming.
- Resolve authority (which source wins on conflicts).
- Assign surrogate keys for downstream joins.

### History tracking with snapshots

| CustomerSnapshotID | CustomerID | Region | ValidFrom | ValidTo | IsCurrent |
|--------------------|------------|--------|-----------|---------|-----------|
| 1001 | 1 | East | 2024-01-01 00:00:00 | 2025-03-15 00:00:00 | 0 |
| 1002 | 1 | West | 2025-03-15 00:00:00 | NULL | 1 |

## Common Use Cases

- Multi-source customer, product, or supplier integration.
- Feeding [Master Data](master-data.md) with clean entities.
- Providing SCD-ready sources for dimension builds.
- Enabling point-in-time analysis for analysts and data scientists.

## Best Practices

| Practice | Why it matters |
|----------|----------------|
| Document transformation rules | Future maintainers need to understand ADS logic |
| Consistent naming | `ADS_<Entity>` for base, `ADS_<Entity>_Snapshot` for history |
| Quality gates before entry | Stop bad data before it pollutes Silver/Gold |
| Balance denormalization | Flatten for usability without losing modeling flexibility |
| Selective snapshotting | Only create snapshots when history is needed |
| Sync base and snapshot | Ensure base updates create matching snapshot versions |
| Rebuildable from Staging | Preserve reload paths from Landing/Staging for recovery |

---

## Related Topics

- [Data Layers and Modeling](data-layers-and-modeling.md) - Overall architecture context
- [Medallion - Bronze Silver Gold](Medallion%20-%20Bronze%20Silver%20Gold.md) - How ADS maps to Silver
- [Star - Dimension Tables](Star%20-%20Dimension%20Tables.md) - Downstream consumer for dimensional modeling
- [Star - Fact Tables](Star%20-%20Fact%20Tables.md) - Downstream consumer for dimensional modeling
- [Master Data](master-data.md) - Parallel consumer for reference data management
