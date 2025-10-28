# Data Sources

- **Databases**: SQL Server Databases, PostgreSQL, MySQL, ...
- **Applications**: SaaS platforms, CRM systems (Hubspot, Salesforce), ERP systems, ... 
- **Files**: CSV, JSON, XML, Parquet files from SFTP/FTP servers or cloud storage
- **APIs**: REST APIs, GraphQL endpoints, webhooks
- **Message Queues**: Kafka, RabbitMQ, ... 
- **Streaming Sources**: IoT devices, clickstreams, social media feeds
- **Cloud Services**: Azure Storage Accounts, AWS S3, Google Cloud Storage, ...

# Data Loading
## ETL or ETL? 

| Property         | ETL                                                                                                                                                     | ELT                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Abbreviation** | Extract > Transform > Load                                                                                                                              | Extract > Load > Transform                                                                                                                           |
| **Explanation**  | The data is first extracted by an extraction tool, then transformed (typically in-memory of this extraction tool) and then loaded into a data platform. | The data is first extracted from the source system and directly loaded into a data platform. Transformations are applied within this data platform.  |

> [!NOTE] ETL or ELT? Frankly, we don't care 💁‍♂️
>  While our frameworks implement the 'ELT' principle, we often mix and match the older more used term 'ETL'. The term 'ETL' is more used by business and the difference between ETL and ELT is not always worth explaining (or an explanation could even lead to more confusion).
>   Our main goal is to provide insightful data layers meant for analytics, as long as this is achieved in a best-practice manner we don't care if you use the term 'ETL' or 'ELT'. 
## Data Ingestion Strategies

### Full Load

When applying a 'Full' loading strategy, all data from the source system is extracted during an ETL run. This means that the `Landing` and `Staging` layer have the same data. As such, subsequent layers can both use the `Landing` and `Staging` layer to fill the Conformed and Dimensional model. 

While the Staging layer can be filled using a 'Truncate and Insert' manner, this cannot be done in the `Conformed` or the `Dimensional Model` layer as history is being captured there (snapshot and SCD2). Hence, an upsert manner is used. 

Full load simplifies ETL but results in long loading times when the source data contains large amounts of data. 

```mermaid
---
config:
  theme: forest
  layout: elk
---
%%{init: { "flowchart": { "useMaxWidth": true } }}%%
graph LR
  subgraph Source Systems
    S[(Source<br/>All data)]:::full
  end

  subgraph Data Platform
    subgraph Back Room
      L[Landing]:::delta
      B[Staging]:::all
      M1[Intermediate]:::delta
      CONF[Conformed]:::all
      M2[Intermediate]:::delta
    end
    subgraph Front Room
      D[Dimensional Mode]:::all
    end
  end

%% Flows
S -->|full| L 
L -.->|truncate + insert| B 
B --> M1 
L -.->|optional| M1
M1 -->|upsert|CONF 
CONF -->M2 
M2 -->|upsert| D


%% Styles
classDef delta fill:#F3F4F6,stroke:#6B7280,stroke-width:2px,stroke-dasharray:6 3,color:#374151;
classDef all fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
classDef full fill:#FDE68A,stroke:#B45309,stroke-width:2px,color:#7C2D12;


```

### Incremental Loading

When applying an 'Incremental' loading strategy, only the changed records form the source system are extracted since the last run (newly inserted, updated or deleted records). 
The `Landing` stores the change set only, while these records are then upserted into `Staging`. These delta's are then used to efficiently fill the `Conformed` and `Dimensional Model` layers.  

Incremental loading mechanisms reduce ETL duration but improve complexity of maintaining copies of the source system. Whenever possible, an incremental loading mechanism is preferred. 

```mermaid
---
config:
  theme: forest
  layout: elk
---
%%{init: { "flowchart": { "useMaxWidth": true } }}%%
graph LR
  subgraph Source Systems
    S[(Source<br/>Changes since watermark)]:::all
  end

  subgraph Data Platform
    subgraph Back Room
      L[Landing<br/>Δ-only]:::delta
      W[Timestamp/Watermark]:::delta
      B[Staging<br/>All data]:::all
      M1[Intermediary<br/>Δ-only]:::delta
      CONF[Conformed<br/>All data]:::all
      M2[Intermediary<br/>Δ-only]:::delta
    end
    subgraph Front Room
      D[Dimensional Model<br/>All data]:::all
    end
  end

%% Flows
W <-.->|fetch watermark| L
S -->|cdc or delta| L
L -->|merge upsert| B
B -->|derive delta| M1
M1 -->|merge upsert| CONF
CONF -->|derive delta| M2
M2 -->|merge upsert| D


%% Styles
classDef delta fill:#F3F4F6,stroke:#6B7280,stroke-width:2px,stroke-dasharray:6 3,color:#374151;
classDef all fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
```

---

## Related Topics

- [[Data Layers and Modeling]] - Overall architecture showing how data sources fit into the platform
- [[Conformed Layer]] - Where source data is cleaned and integrated
