# Naming Conventions

## Overview
Consistent, business‑friendly names improve discoverability and reduce errors.
Use **singular** names for dimensions (e.g., `Customer`) and **plural** for facts (e.g., `Sales`). 

## Do’s & Don’ts
**Do**
- Use business friendly names for tables and columns.
	- Let tables be singular (e.g. 'Customer' and not 'Customer**s**')
- Put your measures on the table they're linked to.[^1]
- Don't include 'Total' in your measures but use 'Revenue' or 'Transactions'
- (Try to) Prefix your column names with the (abbreviation of the) name of the table. 
	- If there are multiple tables that have a column (such as code), you know which table/role it is originating from. 


**Don’t**
- Don't prefix your tables with 'F_' (referencing Fact) or 'D_' (referencing Dimension). The semantic model should be used by business users and they don't know what Facts and Dimensions are. There will be tables in your semantic model that are not a F_ or D_ in the future anyway. 
## Practical Examples

**Tables & Columns** 
- `Sales Transaction (ST)`
	- `'Sales Transaction (ST)'[ST Order Number]`
	- `'Sales Transaction (ST)'[ST Line Number]`

*  `Product`
	* `Product[Product Code]`
	* `ProductProduct Name]`

- `Invoice Customer (Inv. Cust.)` (= Role Playing Dimension)
	- `'Invoice Customer (Inv. Cust.)'[Inv. Cust. First Name]`
	- `'Invoice Customer (Inv. Cust.)'[Inv. Cust. Last Name]`


**Measures**
```DAX
[Customer Count]
[Revenue Incl. VAT]
[Sales YoY Growth %]
```

[^1]: There was a time where we preferred measures on 'Ghost Tables/Unlinked Dummy Dimensions' to mimic Multidimensional Cubes. There are however more advantages to keeping your measures on the table they're linked to. 
