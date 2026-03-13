# Data Layers and Modeling - Overview

The graph underneath shows the normal flow of a best-practice implementation of a Data Platform at projects of Plainsight.

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
graph TD
    %% Expanded DW/BI platform with Medallion colors
    subgraph Source Systems
        A1[(Source System A)]
        A2[(Source System B)]
        A3[(Source System C)]
    end

    subgraph Data Platform 
        direction LR

        subgraph Bronze["Bronze (Landing & Staging)"]
            subgraph Source A
                L1[Landing A<br/>delta-only<br>optional]:::bronzeOptional
                B1[Staging A]:::bronze
            end
            subgraph Source B
                L2[Landing B<br/>delta-only<br>optional]:::bronzeOptional
                B2[Staging B]:::bronze
            end
            subgraph Source C
                L3[Landing C<br/>delta-only<br>optional]:::bronzeOptional
                B3[Staging C]:::bronze
            end
        end

        subgraph Silver["Silver (ADS + intermediate)"]
            M[Intermediate<br/>delta-only<br>optional]:::silverOptional
            C[ADS]:::silver
            O[Intermediate<br/>delta-only<br>optional]:::silverOptional
            G[Master Data]:::silverOptional
        end

        subgraph Gold["Gold (Business Products)"]
            FS[Feature Store<br/>optional]:::goldOptional
            D[Dimensional Model]:::gold
        end

        Semantic[Semantic Layer]
        Reports[Reporting Tools]
        ML[Advanced Analytics / ML]
    end

%% Flows
A1 --> L1
L1 --> B1
A2 --> L2
L2 --> B2
A3 --> L3
L3 --> B3

B1 --> M
B2 --> M
B3 --> M
M --> C
C --> O
O --> D
O -.-> FS
C <--> G
D --> Semantic
D --> Reports
D --> ML
FS --> ML
Semantic --> Reports

%% Node styles
classDef bronze fill:#CD7F32,stroke:#8B4513,stroke-width:1px,color:#FFFFFF;
classDef bronzeOptional fill:#CD7F32,stroke:#8B4513,stroke-width:2px,stroke-dasharray:5 5,color:#FFFFFF;
classDef silver fill:#C0C0C0,stroke:#808080,stroke-width:1px,color:#111827;
classDef silverOptional fill:#C0C0C0,stroke:#808080,stroke-width:2px,stroke-dasharray:5 5,color:#111827;
classDef gold fill:#FFD700,stroke:#DAA520,stroke-width:1px,color:#111827;
classDef goldOptional fill:#FFD700,stroke:#DAA520,stroke-width:2px,stroke-dasharray:5 5,color:#111827;
class A,C blueBox;
```

The typical flow of data is as follows:

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } }}%%
graph LR
	subgraph Source Systems
		S[(Source<br/>All data)]
	end

    subgraph Data Platform
        subgraph Bronze
            L[Landing<br/>delta-only<br/>Optional]:::bronzeOptional
            B[Staging<br/>All data]:::bronze
        end

        subgraph Silver
            M1[Intermediate<br/>delta-only<br>optional]:::silverOptional
            CONF[ADS<br/>All data]:::silver
            M2[Intermediate<br/>delta-only<br>optional]:::silverOptional
        end

        subgraph Gold
            D[Dimensional Model<br/>All data]:::gold
        end
    end
	
%% Flows
S -->|Optional| L
L --> B
S -.->|Direct| B
B --> |Optional|M1
M1 --> CONF
B -.-> |Direct|CONF
CONF --> |Optional|M2
M2 --> D
CONF -.-> |Direct|D

%% Node styles
classDef bronze fill:#CD7F32,stroke:#8B4513,stroke-width:1px,color:#FFFFFF;
classDef bronzeOptional fill:#CD7F32,stroke:#8B4513,stroke-width:2px,stroke-dasharray:5 5,color:#FFFFFF;
classDef silver fill:#C0C0C0,stroke:#808080,stroke-width:1px,color:#111827;
classDef silverOptional fill:#C0C0C0,stroke:#808080,stroke-width:2px,stroke-dasharray:5 5,color:#111827;
classDef gold fill:#FFD700,stroke:#DAA520,stroke-width:1px,color:#111827;
class A,C blueBox;
```

Here we see all data that the information is flowing through. 
1. The **Source** contains all information but is not part of our Data Platform. Read more about sources in [[Data Sources & Data Loading]]

2. **Landing (Optional, Bronze)** contains the increments extracted from the source or external tables populated by ingestion tools. This layer is useful when:
   - External tools (Fabric Pipelines, Databricks Lakeflow Connect, replication, ...) populate external tables
   - Incremental-only data needs preprocessing before merging into staging
   - Raw files (JSON, Parquet) require parsing before staging
   - Change data capture (CDC) streams need transformation
   
> [!tip] The 'Landing' layer can be skipped when no intermediary steps are required to fill 'Staging'
   
4. The **Staging layer (Bronze)** contains a replica of the source information. This layer contains a replica of the source after an ETL load. The data in this layer is as close to the source as possible (similar column names, similar table names) and nearly no data corrections are applied here. This layer is used for reloads of data to subsequent layers. Read more in [[Landing and Staging]].

5. The **Intermediate layers (Silver)** provide helpful steps to apply changes to the staging and ADS layers such as flattening, filtering, grouping, denormalizing/flattening and more. The intermediary layers can consist of volatile views, of small increments, persisted tables and more. These layers help split up the ETL for more modularity, re-use of logic and more. 
   
> [!tip] The 'Intermediate' layer can be skipped when no intermediary steps are required to fill 'ADS' or 'Gold' layers
   
5. The **ADS layer (Silver)** provides cleaned data with data quality rules applied and initial denormalization. Tables are unpivoted, making the data more accessible while still allowing for further business-friendly modeling. This layer is used to integrate different sources, for historical build-up (supporting SCD2 logic in later-on streams), and for increased querying capacity to address business questions. This is the ideal phase to feed Master Data Services (MDS). This layer can be used by experienced data engineers and data analysts. Read more about this layer in [[Analytical Data Store (ADS)]]. 

6. The **Gold layer** provides business-optimized data structures for reporting, analytics, and machine learning:
   - **Star - Dimensional Model** (Facts & Dimensions): Star schema optimized for fast querying and business user exploration. Read more in [[Star - Dimension Tables]] and [[Star - Fact Tables]].
   - **Feature Store**: Curated, reusable feature tables (often wide / denormalized) for machine learning model training, inference, and advanced analytics.


# Architecture Philosophy

Our layered architecture approach balances flexibility with performance, inspired by industry best practices while adapted to modern cloud data platforms.

## Why Multiple Layers?

This multi-layered approach is preferred over a 'Dimensional Model Only' architecture for several key reasons:

* **Flexibility for integration**: Bronze and Silver layers (Landing, Staging, ADS) provide multiple integration points for diverse source systems and historical data build-up.
* **Easier dimensional modeling**: Having clean, ADS data makes it significantly easier to build and maintain dimensional models.
* **Cost efficiency**: Modern data platforms separate storage and compute, making additional data layers low-cost while providing significant value.
* **Advanced analytics support**: For AI, Data Science, and ML use cases, the Bronze/Silver structure is often preferred over the Gold-optimized dimensional model.
* **AI-assisted development**: Leveraging AI-supported ETL development tools works efficiently with both Silver and Gold layers, accelerating delivery.
* **Source system isolation**: Keeping Landing and Staging per source system maintains clear data lineage and simplifies troubleshooting.
* **Progressive transformation**: The Intermediate layers enable modular, reusable transformations that can be tested and maintained independently.



## Layer-by-Layer Transformation Example

To illustrate how data transforms across layers, let's follow a typical e-commerce scenario from Source/Staging through ADS to Dimensional Model.

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
graph LR
    subgraph Bronze["Bronze (Source/Staging)"]
        ADDR[Address]:::bronze
        CUST[Customer]:::bronze
        INV_H[Invoice Header]:::bronze
        INV_L[Invoice Line]:::bronze
        PROD[Product]:::bronze
        COLOR[Product Color]:::bronze
        CAT[Product Category]:::bronze
        BUD[Sales Budget]:::bronze
    end
    
    subgraph Silver["Silver (ADS)"]
        ADS_CUST[ADS_Customer]:::silver
        ADS_CUST_SNAP[ADS_Customer_Snapshot]:::silver
        ADS_PROD[ADS_Product]:::silver
        ADS_PRODCAT[ADS_ProductCategory]:::silver
        ADS_INV[ADS_Invoice]:::silver
        ADS_BUDGET[ADS_SalesBudget]:::silver
    end
    
    subgraph Gold["Gold (Dimensional Model)"]
        D_CUST[D_Customer <br/>SCD2]:::gold
        D_PROD[D_Product]:::gold
        F_SALES[F_Sales]:::gold
        F_BUDGET[F_SalesBudget]:::gold
    end
    
    CUST --> ADS_CUST
    ADDR --> ADS_CUST
    CUST --> ADS_CUST_SNAP
    PROD --> ADS_PROD
    COLOR --> ADS_PROD
    CAT --> ADS_PROD
    CAT --> ADS_BUDGET
    BUD --> ADS_BUDGET
    BUD --> ADS_PRODCAT
    CAT --> ADS_PRODCAT
    INV_H --> ADS_INV
    INV_L --> ADS_INV
    
    ADS_CUST --> D_CUST
    ADS_CUST_SNAP --> D_CUST
    ADS_PROD --> D_PROD
    ADS_PRODCAT --> D_PROD
    ADS_INV --> F_SALES
    ADS_BUDGET --> F_BUDGET
    
    D_CUST --> F_SALES
    D_PROD --> F_SALES
    D_PROD --> F_BUDGET

    %% Node styles
    classDef bronze fill:#CD7F32,stroke:#8B4513,stroke-width:1px,color:#FFFFFF;
    classDef silver fill:#C0C0C0,stroke:#808080,stroke-width:1px,color:#111827;
    classDef gold fill:#FFD700,stroke:#DAA520,stroke-width:1px,color:#111827;
```

**Transformation flow:**
- **Bronze (Source/Staging) — 8 tables**: Normalized structure with `Customer`, `Address`, `Invoice Header`, `Invoice Line`, `Product`, `Product Color`, `Product Category`, `Sales Budget`.
- **Silver (ADS) — 6 tables**: Denormalized into `ADS_Customer` (Customer + Address), `ADS_Customer_Snapshot` (history tracking from Customer), `ADS_Product` (Product + Color + Category), `ADS_ProductCategory` (aggregated product categories from Sales Budget), `ADS_Invoice` (Invoice Header + Lines), `ADS_SalesBudget` (budget targets from Sales Budget and Product Category).
- **Gold (Dimensional Model) — 4 tables**: Star schema with 2 facts (`F_Sales`, `F_SalesBudget`) and 2 dimensions (`D_Customer`, `D_Product` merging both detail and category levels).

> [!tip] Progressive Denormalization
> Notice the progressive reduction in table count as data moves through layers:
> - **Staging**: 8 tables with complex relationships
> - **ADS**: 6 tables with denormalization, history tracking (`ADS_Customer_Snapshot`), business categorization (`ADS_ProductCategory`), and budgets (`ADS_SalesBudget`)
> - **Dimensional**: 2 fact tables + 2 dimension tables in star schema
> 
> Key insight: `D_Product` merges both `ADS_Product` (detail level with individual products) and `ADS_ProductCategory` (aggregate category level) into a single dimensional hierarchy. This allows both `F_Sales` (detailed transactions at product level) and `F_SalesBudget` (aggregated budgets at category level) to share the same dimension, enabling actual vs. budget comparisons across the product hierarchy.
---

## Related Topics

- [[Data Sources & Data Loading]] - How data enters the platform
- [[Analytical Data Store (ADS)]] - Silver layer between Bronze and Gold
- [[Star - Dimension Tables]] - Star schema dimension design patterns
- [[Star - Fact Tables]] - Star schema fact table design patterns  
- [[Master Data]] - Operational database for business-maintained reference data
