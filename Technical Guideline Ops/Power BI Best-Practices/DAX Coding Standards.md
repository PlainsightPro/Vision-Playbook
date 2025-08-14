# DAX Coding Standards

## Overview
Prioritize readability and maintainability: use VAR blocks, format with line breaks/indentation,
add comments, and prefer measures over calculated columns when possible.

## Do’s & Don’ts
**Do**
- Use `VAR` to compute sub-results once and RETURN a clear expression. Prefix your variables with an underscore. 
- Format DAX consistently (each argument on a new line, indent filters).
- Add inline `// comments` for complex business rules.
- Use the DIVIDE function instead of the '/' as DIVIDE allows for dividing by 0. 

**Don’t**
- Don’t cram everything into one giant measure; compose helper measures.
- Don’t create calculated columns for context-dependent logic. Calculated columns are 'persisted' during model refresh (= visuals in your Power BI report do not impact the result of your calculated column). 

## Practical Examples
```DAX
// Calculate YoY Growth using a variable for prior year
[YoY Sales %] =
VAR _PrevYear = CALCULATE (
        [Total Sales],
        DATEADD ( 'Date'[Date], -1, YEAR )
	    )
RETURN
    IF (
        _PrevYear = 0,
        BLANK (),
        DIVIDE (
            [Total Sales] - _PrevYear,
            _PrevYear
        )
    )

```

```DAX
[Margin %] =
VAR _TotalSales = [Total Sales]
VAR _TotalCost  = [Total Cost]
RETURN
IF(
    _TotalSales = 0,
    BLANK(),
    DIVIDE(_TotalSales - _TotalCost, _TotalSales)
)

```
