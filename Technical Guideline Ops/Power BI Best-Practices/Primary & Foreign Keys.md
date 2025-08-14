# Primary & Foreign Keys

## Overview
Use **whole number** surrogate keys for relationships. Avoid text/GUID keys. Ensure uniqueness
on the one‑side and matching data types between related columns.

## Do’s & Don’ts
**Do**
- Use `CustomerID`, `ProductID` (INT) as PKs; use the same INTs as FKs in facts.
- Mark the Date table and use a consistent key (Date or `YYYYMMDD` INT).
- Remove unused or redundant key columns.

**Don’t**
- Don’t relate on high‑cardinality text or GUID columns when avoidable.
- Don’t leave duplicate keys on the one‑side (breaks one‑to‑many).

## Practical Examples

**Date key approach**
- `FactSales[DateKey]` (e.g., 20250101) → `DimDate[DateKey]`
