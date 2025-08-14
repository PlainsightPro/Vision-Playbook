# Data Modeling Best Practices (Power BI + Fabric)

## Overview
Design star schemas around a central **fact** table with surrounding **dimension** tables.
Use robust relationships (single-direction where possible), prefer whole-number surrogate keys,
and plan for scale with incremental refresh/partitioning in enterprise models.

## Do’s & Don’ts
**Do**
- Model as a star schema for clarity and performance.
- Ensure one-to-many relationships with unique dimension keys.
- Use integer surrogate keys; avoid text/GUID keys for relationships. GUID relationships are stored as strings and take-up a lot of memory in your mode. 
- Use Date dimension(s); mark it as a Date table.

**Don’t**
- Don’t build one giant “flat” table for everything. 
- Don’t snowflake dimensions unless there’s a compelling reason.
- Don’t enable bi‑directional relationships by default. Bi-directional relationship could lead to ambiguous relationships. If bi-directional relationships are required, override the filtering behaviour in your measure by using CROSSFILTER[^1]. 

## Why It Matters
Integers are compressed exceptionally well; clean star schemas reduce ambiguity
and speed up filters and joins at scale.

[^1]: Do note that CROSSFILTER and USERELATIONSHIP are not supported in models using Row-Level Security (RLS). 