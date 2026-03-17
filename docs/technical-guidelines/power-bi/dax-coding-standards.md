---
description: "DAX coding standards for Power BI: VAR blocks, DIVIDE, CALCULATE best practices, formatting guidelines, and practical measure examples."
---

# DAX Coding Standards

## Overview
Prioritize readability and maintainability: use `VAR` blocks, format with line breaks/indentation,  
add comments, and prefer **measures** over calculated columns when possible.

## Do’s & Don’ts

**Do**
- Use `VAR` to compute sub-results once and `RETURN` a clear expression. Prefix your variables with an underscore.  
- Format DAX consistently (each argument on a new line, indent filters).  
- Add inline `// comments` for complex business rules.  
- Use `DIVIDE` instead of `/` as `DIVIDE` allows safe handling of divide-by-zero.  
- Use helper measures to avoid duplication and simplify maintenance.  
- Use `CALCULATE` only when you need to change filter context, otherwise keep logic in base measures.  
- Replace complex `IF` chains with `SWITCH(TRUE(), …)` for readability.  
- Keep business logic in measures, not in calculated columns (except when needed for relationships).  
- Test for blank values explicitly to avoid misleading 0s in reports.  
- Document assumptions in comments (e.g., “Assumes sales amount is net of tax”).  

**Don’t**
- Don’t cram everything into one giant measure; break it down into helper/base measures.  
- Don’t use `FILTER(ALL(Table), …)` when `REMOVEFILTERS` or `ALLSELECTED` is sufficient.  
- Don’t overuse iterators (`SUMX`, `AVERAGEX`) when a simple aggregator (`SUM`, `AVERAGE`) works.  
- Don’t create calculated columns for context-dependent logic (calculated columns are fixed at refresh).  
- Don’t use `ALL` blindly; it removes filters across the board and may introduce unexpected results.  

---

## Practical Examples

>[!Using VAR for clarity]-
>
>```DAX
>[YoY Sales %] =
>VAR _PrevYear =
>    CALCULATE (
>        [Total Sales],
>        DATEADD ( 'Date'[Date], -1, YEAR )
>    )
>RETURN
>    IF (
>        _PrevYear = 0,
>        BLANK(),
>        DIVIDE ( [Total Sales] - _PrevYear, _PrevYear )
>    )
>```

>[!Safe margin calculation]-
>
>```DAX
>[Margin %] =
>VAR _TotalSales = [Total Sales]
>VAR _TotalCost  = [Total Cost]
>RETURN
 >   IF (
 >       _TotalSales = 0,
 >       BLANK(),
 >       DIVIDE ( _TotalSales - _TotalCost, _TotalSales )
 >   )
>```

>[!Switch instead of nested IF]-
>```DAX
>[Customer Segment] =
>SWITCH (
 >   TRUE(),
 >   [Customer Spend] > 10000, "High Value",
 >   [Customer Spend] > 5000,  "Medium Value",
 >   [Customer Spend] > 0,     "Low Value",
 >   BLANK()
>)
>```

>[!Remove filters selectively]-
>```DAX
>[Total Sales (Ignore Product)] =
>CALCULATE (
>    [Total Sales],
>    REMOVEFILTERS ( 'Product' )
>)
>```

>[!Iterators vs aggregators]-
>
>❌ Less efficient
>```DAX
>[Total Sales X] =
>SUMX ( 'Sales', 'Sales'[Quantity] * 'Sales'[UnitPrice] )
>```
>
>✅ Better (when column already exists)
>```DAX
>[Total Sales] = SUM ( 'Sales'[SalesAmount] )
>```

>[!Explicit blank handling]-
>
>```DAX
>[Return Rate %] =
>VAR _Returns = [Total Returns]
>VAR _Sales   = [Total Sales]
>RETURN
  >  IF (
>    ISBLANK ( _Sales ),
>	BLANK(),
>	DIVIDE ( _Returns, _Sales )
>)
>```
