---
description: "How Plainsight is organised — a flat, hierarchy-free structure with career coaches, knowledge hubs, and self-managed teams of data and AI experts."
---

??? tip "TL;DR"
    No hierarchy. No ivory towers. A team of experts, each with a different role, all playing for the same goal.

## The Plainsight Flywheel

Think of Plainsight as a **football team**, not a corporate ladder. Every player has a different role: goalkeeper, midfielder, striker. But no role is more important than another. The team wins or loses *together*. That's exactly how we operate.

We don't have "managers" in the traditional sense. We have people who take ownership of what needs to happen, and everyone's contribution carries equal weight.

Our organisation is built around two sides of the same machine, linked together like cogs in a wheel:

![Organisation structure](../images/Organisation%20structure.png)

On  the **right** sit our three offerings. This is where our experts do what they do best:

| Offering | What we do |
|---|---|
| **Data/AI Strategy & Governance** | Helping organisations define their data and AI roadmap and set up the right governance to make it stick. |
| **AI & GenAI Implementation** | Building and deploying AI and generative AI solutions that deliver real business value. |
| **Data & Analytics** | Engineering data platforms, analytics solutions, and everything in between. |

On the **left** sit the supporting services that keep the machine running: backoffice, marketing, sales, and recruitment. Without them, the offerings don't reach the people who need them.

Both sides are equally important. The cogs only turn when they work together. An expert building a customer's data platform is just as vital as the person making sure the right people find their way to Plainsight.

## Offer Leads: Bridge Between Capability and Customer

Offer Leads focus on translating Plainsight's capabilities into strong offers for (potential) customers. You can also think of this as our sales-facing offer function.

Their main purpose is to:

- turn our expertise, tools, and technologies into clear offers
- show customers what Plainsight is capable of
- guide (potential) customers toward the right approach

Offer Leads are expected to have broad, high-level knowledge across what we do as Plainsight. They are not expected to know every technical detail or the nitty-gritty of each implementation.

Consultants are not split into fixed "one consultant per offer" boxes. A consultant can work on a Data Engineering trajectory today and move to another project that is closer to a different offer tomorrow.

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%

flowchart TB
  subgraph TOP[Offer Leads]
    direction LR
    O1[Data/AI Strategy & Governance]
    O2[AI & GenAI Implementation]
    O3[Data & Analytics]
  end

  subgraph BOTTOM[Projects & Experts]
    direction LR
    C[Shared Consultant Pool<br/>Experts assigned based on project need]
  end

  subgraph SUPPORT[Growth & Partnerships]
    direction LR
    GL[Growth Lead & Partnership<br/>New business · Accounts · Technology partnerships]
  end

  O1 <---> C
  O2 <---> C
  O3 <---> C

  GL -.->|supports| O1
  GL -.->|supports| O2
  GL -.->|supports| O3
