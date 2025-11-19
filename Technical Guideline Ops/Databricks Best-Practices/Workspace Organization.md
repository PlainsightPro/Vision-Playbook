# Databricks Best Practices: Workspace & Folder Organization

> [!info]
> **Audience:** Data engineers, analytics engineers, and platform administrators working with Databricks on Plainsight projects.

A well-organized Databricks workspace accelerates collaboration, code quality, and data governance. Adopting a clear folder structure - aligned first and foremost with our semantic data layers (`landing`, `staging`, `ads`, `front_room` / `star`, see [[Data Layers and Modeling]] and [[Analytical Data Store (ADS)]]) and, only where you must align with existing conventions, optionally mapped to bronze/silver/gold Medallion zones (see [[Technical Guideline Ops/Architectural Principles/Medallion - Bronze Silver Gold|Medallion Architecture]]) - ensures clarity, reusability, and maintainability. Integrating unit tests into your workspace further strengthens code reliability.

## A general folder structure for Databricks workspaces

In general we recommend a folder structure with two top-level folders: `/src` and `/test`. The `/src` folder contains all production code, organized by our semantic data layers (`landing`, `staging`, `ads`, `front_room` / `star`) and shared utilities (`shared`). If the team or platform is already using bronze/silver/gold, you can map them directly: `landing` ≈ bronze, `ads` ≈ silver, `front_room`/`star` ≈ gold. The `/test` folder mirrors this structure in order to allow for automated testing using pytest.

Notebooks can be named using the following convention:
- Landing (raw ingestion): `<data_source>_<table_name>.py` (e.g. `sap_sales_order_items_landing.py`) - equivalent to Bronze
- ADS (cleansed & integrated): `<data_source>_<table_name>.py` (e.g. `sap_sales_ads.py`) - equivalent to Silver
- Front Room / Star (dimensional model & products): `<data_product>_<table/view>.py` (e.g. `dwh_f_sales.py`) - equivalent to Gold

> [!tip] 
> In the Front Room / star layer (Gold-equivalent), one of the (main) applications is the data warehouse (`dwh`). Therefore, we suggest to prefix star-model notebooks with `dwh_` to indicate their purpose. Here we have a dimensional model with fact and dimension tables/views. To indicate these, we suggest to prefix fact tables/views with `f_` and dimension tables/views with `d_`. An example of a fact table notebook would be `dwh_f_sales.py` and for a dimension table `dwh_d_customer.py`.

In order to trigger an automated testing framework, test notebooks can be named using the `test_` prefix, e.g. for Landing/ADS, `test_<data_source>_<table_name>.py`.

```
/Workspace Root
  /src
    /landing        # raw ingestion (Bronze-equivalent)
      <ingest_notebooks>
    /staging        # optional per-source staging
      <staging_notebooks>
    /ads            # cleansed & integrated (Silver-equivalent)
      <transform_notebooks>
    /front_room     # star / products (Gold-equivalent)
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
    /front_room
      <test_analytics_notebooks>
    /shared
      <test_utils>
```

> [!tip] 
> Optional: You can add a subfolder per datasource (Landing/ADS) and data product (Front Room/Star) if needed for further organization. When you must expose bronze/silver/gold explicitly (for example, in shared platform folders), treat them as aliases for `landing` / `ads` / `front_room`.

## Workspace Folders vs Repo Folders

> [!info]
> **Workspace folders** are Databricks-native directories for organizing notebooks, libraries, and other artifacts directly in the Databricks UI. **Repo folders** are linked to Git repositories, enabling version control and collaborative development.

Our recommendation is to use repo folders. First of all this will simplify production deploys as you only need to do a `git pull` to get the code in production. Secondly, the Repos allow you to import files and build python packages in your Databricks environment, which is not possible with workspace folders.

Workspace folders still exist and can be useful for ad hoc analysis and prototyping, but for production code and shared logic, repo folders are preferred.

| Use Case                | Recommended Location |
|-------------------------|---------------------|
| Prototyping/Ad hoc      | Workspace folder    |
| Production code         | Repo folder         |
| Shared utilities        | Repo folder         |
| Unit tests              | Repo folder         |
