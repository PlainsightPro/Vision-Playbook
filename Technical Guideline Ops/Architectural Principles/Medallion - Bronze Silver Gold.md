# Medallion Architecture - Bronze, Silver, Gold

> [!info] Overview
> Medallion architecture (Bronze → Silver → Gold) is a popular pattern for organizing data by quality tier. At Plainsight, we prefer the more explicit layering approach described in [[Data Layers and Modeling]] because Medallion's boundaries are often ambiguous and lead to layer proliferation (Diamond, Platinum, etc.).

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true, "curve": "basis" }, "theme": "base" } }%%
flowchart LR
    Sources[(Sources)] --> Bronze[Bronze<br/>Raw]
    Bronze --> Silver[Silver<br/>Clean]
    Silver --> Gold[Gold<br/>Business-Ready]
    Gold --> Consumers[Consumers]
    
    style Bronze fill:#CD7F32,stroke:#8B4513,color:#FFFFFF
    style Silver fill:#C0C0C0,stroke:#808080,color:#000000
    style Gold fill:#FFD700,stroke:#DAA520,color:#000000
```

## Why We Prefer Explicit Layering

**Problems with Medallion:**

1. **Ambiguous boundaries**: Where does deduplication belong; Bronze or Silver? What about type conversions?
2. **Layer proliferation**: Teams add Diamond, Platinum, Titanium layers when three tiers don't fit. 
3. **Endless debates**: "Is this Silver or Gold work?" wastes time. 
4. **Metaphorical names**: Bronze/Silver/Gold lack semantic meaning.

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true, "curve": "basis" }, "theme": "base" } }%%
flowchart LR
    Bronze --> Silver --> Gold --> Diamond[Diamond 🤔] --> Platinum[Platinum 🤷]
    
    style Diamond fill:#B9F2FF,stroke:#4A90E2,color:#000000
    style Platinum fill:#E5E4E2,stroke:#9C9C9C,color:#000000
```

**Our approach uses semantic names** (Landing, Staging, Conformed, Front Room) with clear responsibilities per layer.  

## Detailed Mapping

Following maps our [[Data Layers and Modeling]] to the different layers. Stick to 'Bronze, Silver, Gold' and map the 'Gold' to the `Front Room` layers

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true, "curve": "basis" }, "theme": "base" } }%%
flowchart TB
    subgraph Bronze["Bronze"]
        Staging[Staging]
    end
    
    subgraph Silver["Silver"]
        Conformed[Conformed]
    end
    
    subgraph Gold["Gold = Front Room"]
        Dims[Star - Dimens & Facts] & Facts[One Big Table] & Feat[Feature Stores]
    end
    
    Staging --> Conformed
    Conformed --> Dims & Facts & Feat
    
    style Bronze fill:#CD7F32,stroke:#8B4513,color:#FFFFFF
    style Silver fill:#C0C0C0,stroke:#808080,color:#000000
    style Gold fill:#FFD700,stroke:#DAA520,color:#000000
```

---
## Related Pages

- [[Data Layers and Modeling]]: Our preferred approach
- [[Landing and Staging]]: Bronze equivalent
- [[Conformed Layer]]: Silver equivalent
- [[Star - Dimension Tables]] & [[Star - Fact Tables]]: Gold equivalent

> [!tip] Bottom Line
> Medallion works for simple cases, but semantic layer names (Landing/Staging/Conformed/Front Room) prevent ambiguity and layer proliferation in complex implementations.
