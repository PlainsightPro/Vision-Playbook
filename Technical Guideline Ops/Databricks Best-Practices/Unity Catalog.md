# Working with the Unity Catalog

> [!info]
> **Audience:** Data engineers, analytics engineers, and platform administrators working with Databricks.  
> This guide shares quick tips to get productive with Unity Catalog in a scalable way.

## Overview

The Unity Catalog is Databricks' unified governance solution for all data assets. Advantages include fine-grained access control, centralized metadata management, and auditability across workspaces. Adopting Unity Catalog ensures data security, compliance, and operational efficiency.

## Unity Catalog components

The Unity Catalog uses a four-level structure: Metastore, Catalog (top level), Schema (mid level) and table/view (bottom level).

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
flowchart LR
    %% Schemas per layer
    MS[Metastore] --> UC[Catalog: prod]
    UC --> Landing[Schema: landing]
    UC --> Staging[Schema: staging]
    UC --> ADS[Schema: ads]
    UC --> Gold[Schema: gold]

    %% Example objects
    Landing --> L1[lnd_sap_sales]
    Landing --> L2[lnd_sf_accounts]
    Staging --> S1[stg_sap_sales]
    Staging --> S2[stg_sf_accounts]
    ADS --> A1[ads_customer]
    ADS --> A2[ads_product]
    ADS --> A3[ads_customer_snapshot]
    Gold --> G1[d_customer]
    Gold --> G2[f_sales]
    Gold --> G3[feature_customer_monthlysnapshot]
    Gold --> G4[feature_customer_kpi]

    %% Layer coloring aligned with Medallion mapping
    style Landing fill:#CD7F32,stroke:#8B4513,color:#FFFFFF
    style Staging fill:#CD7F32,stroke:#8B4513,color:#FFFFFF
    style ADS fill:#C0C0C0,stroke:#808080,color:#000000
    style Gold fill:#FFD700,stroke:#DAA520,color:#000000
```

The metastore is always present and fixed across the Databricks account. When creating or reading tables, reference the catalog, schema, and table/view/volume/model name using `catalog.schema.object`. When not specified, Spark assumes the `default` catalog and/or `default` schema.

The best way to read and write data is by using the `read_table` and `saveAsTable` functions in Python:

```python
# Read from the Landing/bronze schema
df = spark.read_table("prod.landing.sap_sales_order_items")
# Optionally read from staging/bronze if present
stg = spark.read_table("prod.staging.sap_sales_order_items")
# Write to ADS (Silver-equivalent)
df.write.saveAsTable("prod.ads.sales")
```

In SQL:

```sql
-- Read from Landing (Bronze-equivalent)
SELECT * FROM prod.landing.sap_sales_order_items;
-- Write into ADS (Silver-equivalent)
CREATE TABLE prod.ads.sales AS SELECT * FROM some_source_table;
```

## Managed vs external tables

Unity Catalog supports managed and external tables. **Prefer managed tables** so Unity Catalog manages storage locations, optimizations, and indexing. External tables are useful when you need fine-grained control or when another team enforces storage locations.

```python
# Adding a path parameter to saveAsTable results in an external table
(
    df.write
      .option("path", "abfss://container@storageaccount.dfs.core.windows.net/gold/sales_data")
      .saveAsTable("prod.gold.sales_data")
)
```

```sql
CREATE TABLE prod.ads.sales_data
USING DELTA
LOCATION 'abfss://container@storageaccount.dfs.core.windows.net/ads/sales_data'
AS SELECT * FROM source_table;
```

## Unity Catalog organization

Two organizational units matter: catalogs and schemas. Organize catalogs by environment (`dev`, `test`, `acc`, `prod`) to simplify promotion and isolation. Schemas can be organized by data domains or by **data layers**. Unity Catalog supports our semantic layers (`landing`, `staging`, `ads`, `gold` / `star`, see [[Data Layers and Modeling]] and [[Analytical Data Store (ADS)]]) and maps directly to Medallion zones: bronze = landing/staging, silver = ads, gold = gold/star (see [[Technical Guideline Ops/Architectural Principles/Medallion - Bronze Silver Gold|Medallion Architecture]]).

```python
# Set up the catalog to use for the current session
spark.catalog.setCurrentCatalog("catalog_name")
df = spark.read_table("schema.table_name")
```

```sql
USE CATALOG catalog_name;
SELECT * FROM schema.table_name;
```

Organizing by environment provides:
- Clear separation between environments, reducing risk of accidental exposure or modification.
- Simplified promotion and testing by isolating changes.
- Simplified access management (permissions per catalog).
- Environment-specific configuration and optimization.
- Clear cost allocation and resource management per environment.

## User and access management

Principals (users, groups, service principals) can be granted permissions on catalogs, schemas, and tables/views. Centralize identity in an external provider and synchronize to Unity Catalog (for example AIM on Azure or SCIM-based sync).

Follow least-privilege and role-based access control (RBAC). Use infrastructure-as-code (for example Terraform with the Databricks provider) to manage permissions reproducibly and keep an audit trail in Git.
