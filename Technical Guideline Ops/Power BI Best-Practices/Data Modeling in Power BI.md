# Data Modeling Best Practices for Power BI

## Overview
Design star schemas around a central **fact** table with surrounding **dimension** tables.  
Use robust relationships (single-direction where possible), prefer whole-number surrogate keys, and plan for scale with incremental refresh/partitioning in enterprise models.

## Do’s & Don’ts

**Do**
- Model as a star schema for clarity and performance.  
- Ensure one-to-many relationships with unique dimension keys.  
- Use integer surrogate keys (Primary Keys, Foreign Keys); avoid text/GUID keys for relationships. Read more here: [[Surrogate, Primary & Foreign Keys]]  
- Use Date dimension(s); mark it as a Date table.  
- Declare the grain of each fact table (e.g., “one row per order line”) to avoid confusion.  
- Add an Unknown / Not Applicabl key (e.g., `-1`) in dimensions to handle orphaned fact rows.  
- Build dimensions wide enough with relevant attributes, but avoid unnecessary snowflaking.  
- Use bridge tables for many-to-many instead of direct relationships.  
- Enable `Incremental Refresh` on large tables with stable “last modified” columns for efficiency.  
- Optimize column storage:  
  - Remove unused columns.  
  - Use whole numbers where possible.  
  - Avoid high-cardinality text fields in facts.  
- Periodically review models with VertiPaq Analyzer / Performance Analyzer to identify bottlenecks.  
- Apply Row-Level Security (RLS) on dimensions (not facts) for better performance.  
- Enforce schema/type checks in Power Query or upstream to ensure data quality.  
- Surface a last refresh timestamp and data dictionary page to improve trust.  
- Keep reports thin: heavy logic belongs in the dataset, not in visuals.  


>[!Example: Grain declaration]-
>
>```text
F_Sales: One row per order line
>- OrderID
>- OrderLineID
>- ProductKey
>- CustomerKey
>- SalesAmount
>```
>
>This makes it clear that “OrderID” alone is not unique in the fact table.

>[!Example: Incremental Refresh policy]-
>
>```text
>Policy:
>- Keep data for last 5 years
>- Refresh last 7 days
>- Detect changes on [ModifiedDate]
>```
>
>This balances query performance with manageable refresh times.

**Don’t**
- Don’t build one giant “flat” table for everything.  
- Don’t snowflake dimensions unless reuse or maintenance clearly requires it.  
- Don’t enable bi-directional relationships by default. Bi-directional relationships can lead to ambiguity. If bi-directional relationships are required, override the filtering behaviour **in your measure** by using CROSSFILTER[^1].  
- Don’t apply RLS with complex filters directly on large fact tables.  
- Don’t leave large descriptive text or high-cardinality columns in facts—split them into separate detail tables if needed.  
- Don’t hard-code data sources; use parameters for environment portability.  
- Don’t deploy straight to production; always validate in test first.  

[^1]: CROSSFILTER and USERELATIONSHIP are not supported in models using Row-Level Security (RLS).
