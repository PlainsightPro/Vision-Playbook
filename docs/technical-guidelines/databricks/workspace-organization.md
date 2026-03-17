---
description: "Databricks workspace organization: folder structure for landing, staging, ADS, and gold layers, naming conventions, and repo vs workspace folders."
---

# Databricks Best Practices: Workspace & Folder Organization

??? info "info"
    **Audience:** Data engineers, analytics engineers, and platform administrators working with Databricks on Plainsight projects.

A well-organized Databricks workspace accelerates collaboration, code quality, and data governance. Use a clear folder structure aligned with our semantic layers (`landing`, `staging`, `ads`, `gold` / `star`, see [Data Layers and Modeling](../architectural-principles/data-layers-and-modeling.md) and [Analytical Data Store (ADS)](../architectural-principles/analytical-data-store-ads.md)) and mirror them to the Medallion zones (bronze/silver/gold, see [Medallion Architecture](../architectural-principles/medallion-bronze-silver-gold.md)) so teams can navigate using either naming set. Integrating unit tests into your workspace further strengthens code reliability.

## A general folder structure for Databricks workspaces

We recommend two top-level folders: `/src` and `/test`. The `/src` folder contains all production code, organized by our semantic data layers (`landing`, `staging`, `ads`, `gold` / `star`) and shared utilities (`shared`). Treat bronze/silver/gold as direct aliases: `landing` and `staging` = bronze, `ads` = silver, `gold`/`star` = gold. The `/test` folder mirrors this structure to enable automated testing with pytest.

Notebooks can be named using the following convention:
- Landing (raw ingestion): `<data_source>_<table_name>.py` (for example `sap_sales_order_items_landing.py`) - Bronze equivalent
- ADS (cleansed and integrated): `<data_source>_<table_name>.py` (for example `sap_sales_ads.py`) - Silver equivalent
- Gold / Star dimensional model and products: `<data_product>_<table_or_view>.py` (for example `dwh_f_sales.py`) - Gold equivalent

??? tip "tip"
    In the Gold / star layer, one of the main applications is the data warehouse (`dwh`). Prefix fact notebooks with `f_` and dimension notebooks with `d_` (for example `dwh_f_sales.py`, `dwh_d_customer.py`).

To trigger an automated testing framework, test notebooks can be named using the `test_` prefix, for example `test_<data_source>_<table_name>.py`.

```
/Workspace Root
  /src
    /landing        # raw ingestion (Bronze-equivalent)
      <ingest_notebooks>
    /staging        # optional per-source staging
      <staging_notebooks>
    /ads            # cleansed and integrated (Silver-equivalent)
      <transform_notebooks>
/gold           # star / products (Gold-equivalent)
      <analytics_notebooks>
    /shared
      <utils>
  /test
    /landing
      <test_ingest_notebooks>
    /staging
      <test_staging_notebooks>
    /ads
      <test_transform_notebooks>
    /gold
      <test_analytics_notebooks>
    /shared
      <test_utils>
```

??? tip "tip"
    Optional: add a subfolder per data source (Landing/ADS) and per data product (Gold/Star) for further organization. When bronze/silver/gold must be shown explicitly (for example, in shared platform folders), treat them as aliases for `landing` / `ads` / `gold`.

## Workspace Folders vs Repo Folders

??? info "info"
    **Workspace folders** are Databricks-native directories for organizing notebooks, libraries, and other artifacts directly in the Databricks UI. **Repo folders** are linked to Git repositories, enabling version control and collaborative development.

Our recommendation is to use repo folders. This simplifies production deploys (pull from Git) and allows you to import files and build Python packages, which is not possible with workspace folders.

Workspace folders still exist and can be useful for ad hoc analysis and prototyping, but for production code and shared logic, repo folders are preferred.

| Use Case                | Recommended Location |
|-------------------------|----------------------|
| Prototyping/Ad hoc      | Workspace folder     |
| Production code         | Repo folder          |
| Shared utilities        | Repo folder          |
| Unit tests              | Repo folder          |
