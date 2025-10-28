# Surrogate, Primary & Foreign Keys

## Overview
Use **whole number** surrogate keys for relationships. Avoid text/GUID keys. Ensure uniqueness
on the one‑side and matching data types between related columns.

## Why It Matters
Integers are compressed exceptionally well in modern analytics tools; clean star schemas reduce ambiguity
and speed up filters and joins at scale. GUID relationships are stored as strings and consume significant memory in your data model.

## Do's & Don'ts
**Do**
- Use `CustomerID`, `ProductID` (INT) as PKs; use the same INTs as FKs in facts.
- Mark the Date table and use a consistent key (Date or `YYYYMMDD` INT).
- Remove unused or redundant key columns.

**Don't**
- Don't relate on high‑cardinality text or GUID columns when avoidable.
- Don't leave duplicate keys on the one‑side (breaks one‑to‑many).

## Practical Examples

**Key approach**
- `FactSales[CustomerID]` (e.g., 12356) → `Dim_Customer[CustomerID]`


> [!NOTE] Dates as PK/FK?
> Within modern analytics platforms, dates are often stored as integers and benefit from excellent compression. Having date columns in your transactional/fact tables can provide advantages (they can be treated as degenerate dimensions and shown directly on the table without requiring a separate Date dimension). As such, dates are commonly allowed as keys. 

---

## Related Topics

- [[Dimension Tables]] - How surrogate keys are used in dimension design
- [[Fact Tables]] - How foreign keys reference dimension surrogate keys
- [[Data Layers and Modeling]] - Where keys fit in the overall architecture 