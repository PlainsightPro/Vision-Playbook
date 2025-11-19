# Databricks Best Practices: Workspace & Folder Organization

> [!info]
> **Audience:** Data engineers, analytics engineers, and platform administrators working with Databricks on Plainsight projects.

A well-organized Databricks workspace accelerates collaboration, code quality, and data governance. Adopting a clear folder structure—aligned with the bronze, silver, gold data architecture—ensures clarity, reusability, and maintainability. Integrating unit tests into your workspace further strengthens code reliability.

## A general folder structure for Databricks workspaces

In general we recommend a folder structure with two top-level folders: `/src` and `/test`. The `/src` folder contains all production code, organized by data layer (`bronze`, `silver`, `gold`) and shared utilities (`shared`). The `/test` folder mirrors this structure in order to allow for automated testing using pytest.

Notebooks can be named using the following convention:
- Bronze: `<data_source>_<table_name>.py` (e.g. `sap_sales_order_items.py`)
- Silver: `<data_source>_<table_name>.py` (e.g. `sap_sales.py`)
- Gold: `<data_product>_<table/view>.py` (e.g. `dwh_f_sales.py`)

> [!tip] 
> In the gold layer, one of the (main) applications is the data warehouse (`dwh`). Therefore, we suggest to prefix gold notebooks with `dwh_` to indicate their purpose. Here we have a dimensional model with fact and dimension tables/views. To indicate these, we suggest to prefix fact tables/views with `f_` and dimension tables/views with `d_`. An example of a fact table notebook would be `dwh_f_sales.py` and for a dimension table `dwh_d_customer.py`.

In order to trigger an automated testing framework, test notebooks can be named using the `test_` prefix, e.g. for bronze/silver, `test_<data_source>_<table_name>.py`.

```
/Workspace Root
  /src
    /bronze
      <ingest_notebooks>
    /silver
      <transform_notebooks>
    /gold
      <analytics_notebooks>
    /shared
      <utils>
  /test
    /bronze
      <test_ingest_notebooks>
    /silver
      <test_transform_notebooks>
    /gold
      <test_analytics_notebooks>
    /shared
      <test_utils>
```

> [!tip] 
> Optional: You can add a subfolder per datasource (bronze, silver) and data product (gold) if needed for further organization.

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
