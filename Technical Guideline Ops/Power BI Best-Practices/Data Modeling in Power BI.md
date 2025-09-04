# Data Modeling Best Practices for Power BI

## Overview
Design star schemas around a central **fact** table with surrounding **dimension** tables.
Use robust relationships (single-direction where possible), prefer whole-number surrogate keys,
and plan for scale with incremental refresh/partitioning in enterprise models.

## Do’s & Don’ts

**Do**
- Model as a star schema for clarity and performance.
- Ensure one-to-many relationships with unique dimension keys. 
- Use integer surrogate keys (Primary Keys, Foreign Keys); avoid text/GUID keys for relationships. Read more here: [[Primary & Foreign Keys]]
- Use Date dimension(s); mark it as a Date table.

**Don’t**
- Don’t build one giant “flat” table for everything. 
- Don’t snowflake dimensions unless there’s a compelling reason.
- Don’t enable bi‑directional relationships by default. Bi-directional relationship could lead to ambiguous relationships. If bi-directional relationships are required, override the filtering behaviour **in your measure** by using CROSSFILTER[^1]. 


[^1]: Do note that CROSSFILTER and USERELATIONSHIP are not supported in models using Row-Level Security (RLS). 