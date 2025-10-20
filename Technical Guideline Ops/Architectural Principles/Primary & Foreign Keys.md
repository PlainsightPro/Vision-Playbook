# Primary & Foreign Keys

## Overview
Use **whole number** surrogate keys for relationships. Avoid text/GUID keys. Ensure uniqueness
on the one‑side and matching data types between related columns.
## Why It Matters
Integers are compressed exceptionally well in tools such as Power BI; clean star schemas reduce ambiguity
and speed up filters and joins at scale. GUID relationships are stored as strings and take-up a lot of memory in your mode. 
## Do’s & Don’ts
**Do**
- Use `CustomerID`, `ProductID` (INT) as PKs; use the same INTs as FKs in facts.
- Mark the Date table and use a consistent key (Date or `YYYYMMDD` INT).
- Remove unused or redundant key columns.

**Don’t**
- Don’t relate on high‑cardinality text or GUID columns when avoidable.
- Don’t leave duplicate keys on the one‑side (breaks one‑to‑many).
## Practical Examples

**Key approach**
- `FactSales[CustomerID]` (e.g., 12356) → `Inv. Customer[CustomerID]`


> [!NOTE] Dates as PK/FK?
> Within Power BI, dates are also stored as an integer and have the same level of compression. In addition, having this column as a date in your transactional/fact table does have some advantages (it can be treated as a degenerate dimension and shown directly on the table without importing another Date dimension). As such, dates are also allowed as keys. 