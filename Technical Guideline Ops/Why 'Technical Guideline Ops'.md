These Technical Guidelines guide you towards a better implementation within a Data Project at Plainsight. These guidelines result from years of experience, countless projects and experiences. Projects at Plainsight should, as closely as possible, adhere to these best-practices. 

While these Technical Guidelines provide our way of working, there are always reasons one prefers to use another way/manner. The flowchart below shows what to do when. 

```mermaid
---
config:
  theme: forest
  layout: elk
---
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
graph TD;
    A[Q? Can I adhere to the technical Guidelines?]
    B[Yes, it's a greenfield.]
    C[Implement the Technical Guidelines.]
    D[No, the technical guidelines are not sufficient.]
    E[Alter the 'Git' Page of the Technical Guidelines and add your new experiences.]
    F[No, I'm working on a project that differs from it.]
    G[Document why you differ from these Technical Guidelines on the as-is scenario. For future scope...]
    

    A --> B --> C
    A --> D --> E --> C
    A --> F --> G --> C
    

    classDef pinkBox fill:#FDCAD2,stroke:#031B89,stroke-width:1px;
    class B,D,E,F,G pinkBox;

    classDef blueBox fill:#031B89,stroke:#031B89,stroke-width:1px,color:#FFFFFF;
    class A,C blueBox;
```

## Why do we have these Technical Guidelines? 

* We want to provide best-practices to our customers. 
* Our projects should easily be transferrable between consultants.