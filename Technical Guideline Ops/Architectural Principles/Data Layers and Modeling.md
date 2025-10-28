
# Data Layers and Modeling - Overview

The graph underneath, shows the normal flow of a best-practice implementation of a Data Platform at projects of Plainsight. 

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
graph TD
    %% Expanded DW/BI platform
    subgraph Source Systems
        A1[(Source System A)]
        A2[(Source System B)]
        A3[(Source System C)]
    end

    subgraph Data Platform 
	    direction LR
        subgraph Back Room
            subgraph Source A
                L1[Landing A<br/>Δ-only]:::delta
                B1[Staging A]:::all
            end
            subgraph Source B
                L2[Landing B<br/>Δ-only]:::delta
                B2[Staging B]:::all
            end
            subgraph Source C
                L3[Landing C<br/>Δ-only]:::delta
                B3[Staging C]:::all
            end
            M[Intermediate<br/>Δ-only]:::delta
            C[Conformed]:::all
            O[Intermediate<br/>Δ-only]:::delta
        end

        subgraph Front Room
            G[Master Data]:::masterdata
            FS[Feature Store<br/>optional]:::optional
            OBT[One Big Table<br/>optional]:::optional
            D[Dimensional Model]:::all
            S[Semantic Layer]
            E[Reporting Tools]
            X[Advanced Analytics / ML]
        end
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
O -.-> OBT
D --> S
S --> E
D --> X
FS --> X
OBT --> X
C <--> G


%% Node styles
classDef delta fill:#F3F4F6,stroke:#6B7280,stroke-width:2px,stroke-dasharray:6 3,color:#374151;
classDef all fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
classDef optional fill:#E0E7FF,stroke:#6366F1,stroke-width:2px,stroke-dasharray:5 5,color:#4338CA;
classDef masterdata fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#FFFFFF;
class A,C blueBox;

```
The typical flow of data is hence as follows: 

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } }}%%
graph LR
	subgraph Source Systems
		S[(Source<br/>All data)]
	end

    subgraph Data Platform
        subgraph Back Room
            L[Landing<br/>Δ-only]:::delta
            B[Staging<br/>All data]:::all
            M1[Intermediate<br/>Δ-only]:::delta
            CONF[Conformed<br/>All data]:::all
            M2[Intermediate<br/>Δ-only]:::delta
        end

        subgraph Front Room
            D[Dimensional Model<br/>All data]:::all
        end
    end
	
%% Flows
S --> L
L --> B
B --> M1
M1 --> CONF
CONF --> M2
M2 --> D


%% Node styles
classDef delta fill:#F3F4F6,stroke:#6B7280,stroke-width:2px,stroke-dasharray:6 3,color:#374151;
classDef all fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
class A,C blueBox;
```

Here we see all data that the information is flowing through. 
1. The **Source** contains all information but is not part of our Data Platform. Read more about sources in [[Data Sources & Data Loading]]
2. **Landing** contains the increments extracted from the source. This includes the newly inserted, modified or deleted records compared to previous ETL run. The data going through landing is then merged into the Staging Layer. 
3. The **Staging** layer contains a replica of the source information. This layer contains a replica of the source after an ETL load. The data in this layer is as close to the source as possible (similar column names, similar table names) and nearly no data corrections are applied here. This layer is used for reloads of data to subsequent layers.
4. The **Intermediate Layers** provide helpful steps to apply changes to the staging and Conformed layers such as flattening, filtering, grouping, denormalizing/flattening and more. The intermediary layers can consist of volatile views, of small increments, persisted tables and more. These layer helps split-up the ETL for more modularity, re-use of logic and more. 
5. The **Conformed** layer provides cleaned data with data quality rules applied and initial denormalization. Tables are unpivoted, making the data more accessible while still allowing for further business-friendly modeling. This layer is used to integrate different sources, for historical build-up (supporting SCD2 logic in later-on streams), and for increased querying capacity to address business questions. This is the ideal phase to feed Master Data Services (MDS). This layer can be used by experienced data engineers and data analysts. Read more about this layer in [[Conformed Layer]]. 
6. The **Front Room** provides business-optimized data structures for reporting, analytics, and machine learning:
   - **Dimensional Model** (Facts & Dimensions): Star schema optimized for fast querying and business user exploration. Read more in [[Dimension Tables]] and [[Fact Tables]].
   - **Master Data**: Operational database for business-maintained reference data, budgets, and classifications that enriches the data platform. Read more in [[Master Data]].
   - **One Big Table (OBT)**: Fully denormalized wide table for simplified access and specific analytical use cases.
   - **Feature Store**: Curated features for machine learning model training and inference. 


# Architecture Philosophy

Our layered architecture approach balances flexibility with performance, inspired by industry best practices while adapted to modern cloud data platforms.

## Why Multiple Layers?

This multi-layered approach is preferred over a 'Dimensional Model Only' architecture for several key reasons:

* **Flexibility for integration**: The Back Room layers (Staging, Conformed) provide multiple integration points for diverse source systems and historical data build-up.
* **Easier dimensional modeling**: Having clean, conformed data makes it significantly easier to build and maintain dimensional models.
* **Cost efficiency**: Modern data platforms separate storage and compute, making additional data layers low-cost while providing significant value.
* **Advanced analytics support**: For AI, Data Science, and ML use cases, the Back Room's more granular and flexible structure is often preferred over the Front Room's optimized dimensional model.
* **AI-assisted development**: Leveraging AI-supported ETL development tools works efficiently with both Back Room and Front Room layers, accelerating delivery.
* **Source system isolation**: Keeping Landing and Staging per source system maintains clear data lineage and simplifies troubleshooting.
* **Progressive transformation**: The Intermediate layers enable modular, reusable transformations that can be tested and maintained independently.

---

## Related Topics

- [[Data Sources & Data Loading]] - How data enters the platform
- [[Conformed Layer]] - Critical transformation layer between Back Room and Front Room
- [[Dimension Tables]] - Star schema dimension design patterns
- [[Fact Tables]] - Star schema fact table design patterns  
- [[Master Data]] - Operational database for business-maintained reference data
