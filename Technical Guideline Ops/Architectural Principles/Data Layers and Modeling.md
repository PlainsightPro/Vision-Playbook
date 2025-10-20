
# Data Layers and Modeling - Overview

The graph underneath, shows the normal flow of a best-practice implementation of a Data Platform at projects of Plainsight. 

```mermaid
---
config:
  theme: forest
  layout: elk
---
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
graph LR
    %% Expanded DW/BI platform

    subgraph Source Systems
        A1[(Source System A)]
        A2[(Source System B)]
        A3[(Source System C)]
    end

    subgraph Ingestion
        I1[Batch ETL<br/>files, DB extracts]
        I2[Streaming / CDC]
    end

    subgraph Data Platform
        subgraph Back Room
            L[Landing<br/>Δ-only]:::delta
            B[Staging]:::all
            M[Intermediate<br/>Δ-only]:::delta
            C[ODS]:::all
            O[Intermediate<br/>Δ-only]:::delta
        end

        subgraph Front Room
            G[Master Data]
            D[Dimensional Model]:::all
            S[Semantic Layer]
            E[Reporting Tools<br/>Power BI, Excel, …]
            X[Advanced Analytics / ML]
            R[Reverse ETL / APIs]
        end
    end

%% Flows
A1 --> I1
A2 --> I1
A3 --> I1
A1 --> I2
A2 --> I2
A3 --> I2

I1 --> L
I2 --> L
L --> B
M --> C
O --> D
D --> S
S --> E
D --> X
D --> R
B --> M
C --> O

%% Cross-cutting (dotted = supporting)
M -.-> G
G -.-> C

%% Node styles
classDef delta fill:#F3F4F6,stroke:#6B7280,stroke-width:2px,stroke-dasharray:6 3,color:#374151;
classDef all fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
class A,C blueBox;

```

The flow of data is hence as follows: 

```mermaid
---
config:
  theme: forest
  layout: elk
---
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
            ODS[ODS<br/>All data]:::all
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
M1 --> ODS
ODS --> M2
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
4. The **Intermediate Layers** provide helpful steps to apply changes to the staging and ODS layers such as flattening, filtering, grouping, denormalizing/flattening and more. The intermediary layers can consist of volatile views, of small increments, persisted tables and more. These layer helps split-up the ETL for more modularity, re-use of logic and more. 
5. The **Operational Data Store (ODS)** provides cleaned data with data quality rules applied. This layer is used to more easily integrate different sources, for historical build-up (supporting SCD2 logic in later-on streams) and for increased querying capacity to address difficult business questions. This layer is not meant for querying by the business as data is organised in a somewhat normalized manner. This layer can be used by more experienced data engineers and data analysts. Read more about this layer in [[Operational Data Store]]. 
6. The **Dimensional Model** provides data in facts and dimensions. This layer is optimized for fast querying, easy to explore by business users and ideal for use in reporting tools. Read more about this layer in [[Dimensional Modeling]]. 

