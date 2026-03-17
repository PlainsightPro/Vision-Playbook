---
description: "Power BI CI/CD and versioning guide: PBIP project format, Git integration, deployment pipelines, and OTAP promotion strategies for enterprise BI."
---

# CICD & Versioning

## Overview
Treat Power BI like software.  
Prefer **Power BI Desktop Projects (.pbip)**[^1] so semantic model and report definitions are **text-based, diffable, and Git-friendly**.  
This enables proper versioning, branching, and CI/CD.  

??? note "📝 What are .pbip and .pbir files?"
    A `.pbip` file is a **project manifest** that points to the actual definition files:  
    - **`.tmdl` (Tabular Model Definition Language):** semantic model definition (tables, relationships, measures).  
    - **`.pbir` (Power BI Report):** report layout, visuals, and metadata.  
    These text-based files replace binary `.pbix` files as the preferred format for collaborative, versioned development.

---

## Definitions

- **`.pbip`**: Manifest that ties everything together, referencing dataset (`.tmdl`) and report (`.pbir`).  
- **`.tmdl`**: Stores dataset/semantic model as text (tables, relationships, measures, metadata).  
- **`.pbir`**: Stores report visuals and layout in text form.  
- **`.gitignore`**: Ensures caches, logs, and local settings don’t pollute Git repositories.  
- **`.pbix`**: Legacy binary file format containing both semantic model and report. Not diffable or Git-friendly.  

### Difference between `.pbip` and `.pbix`
- **`.pbix`** is a single **binary** file that contains dataset + report. Easy to share, but hard to version (diffs not possible).  
- **`.pbip`** is a **project-based format**: a manifest pointing to `.tmdl` and `.pbir` text files. This makes it Git-friendly, diffable, and collaborative.  

---

## Versioning Options (Least → Most Mature)

### 1. No Version History (❌ Not done)
- **Description:** Files live only in the Power BI Service.  
- **Use when:** Never recommended.  
- **Risks:**  
  - No audit trail.  
  - High risk of overwrites.  
  - Difficult or impossible to roll back.  

---

### 2. SharePoint / OneDrive Library with Versioning (✔ Acceptable for small projects)
- **Description:** Store `.pbix` or `.pbip` files in SharePoint or OneDrive with version history enabled.  
  - OneDrive/SharePoint may back up workspace files automatically.  
  - Or: maintain a mirrored folder structure that reflects your Power BI Service workspaces.  
- **Pros:**  
  - Simple to set up.  
  - Built-in versioning & timestamps.  
  - “Who changed what and when” visibility.  
- **Cons:**  
  - Diffs are not meaningful for binary `.pbix`.  
  - Limited branching/review; merges are manual.  
- **Use when:**  
  - **Small teams/projects** or short-lived prototypes.  
  - Not suitable for production-grade enterprise BI.  

---

### 3. Fabric Deployment Pipelines (➡ Promotion, not true versioning)
- **Description:** Use Deployment Pipelines to promote artifacts across environments (Dev → Test → Prod).  
- **Pros:**  
  - Safe, repeatable promotions.  
  - Parameter/connection rules at stage level.  
  - Governance through controlled promotion.  
- **Cons:**  
  - Deployment Pipelines are **not a version control system**.  
  - Limited diffs and history.  
  - Does not replace Git.  
- **Use when:**  
  - You need structured **environment promotion** but no Git maturity.  
  - Combine with (2) or (4) for stronger governance.  

---

### 4. Linked Git Repository (✅ Preferred)
- **Description:** Connect your workspace or PBIP projects to a Git repository in **Azure DevOps** or **GitHub (Enterprise)**.  
- **Pros:**  
  - Proper version history (commits, branches, tags).  
  - Pull requests and code reviews.  
  - Text-based diffs for `.tmdl` and `.pbir`.  
  - Enables true collaborative development.  
- **Deployments:**  
  - Orchestrate OTAP (Dev/Test/Acc/Prod) with **Fabric Deployment Pipelines** and/or **Azure DevOps Pipelines** (`YAML/IaC`).  
  - Automate dataset/report promotion and parameter swaps.  
- **Use when:**  
  - **Default choice** for production-grade, multi-developer, and enterprise BI projects.  

??? note "🔍 Quality Assurance in Git Workflows"
    
When integrating Power BI with Git, you can also introduce **automated quality checks** for semantic models and reports:
> 
> - **[Tabular Editor Best Practice Analyzer (BPA)](https://github.com/TabularEditor/BestPracticeRules)**  
  Define and enforce best-practice rules for DAX, relationships, naming conventions, unused fields, etc.  
  Rules can be customized in JSON and run automatically in pipelines.  
> 
> - **[PBI Inspector v2](https://github.com/NatVanG/PBI-InspectorV2)**  
  Open-source tooling for inspecting Power BI projects, validating structure, and running automated checks.  
  Useful for compliance, technical debt reduction, and governance.  
> 
These tools can be integrated into CI/CD pipelines to enforce coding standards, naming conventions, and model optimization **before deployment**.  

---

## Comparison Table

| Approach | Description | Pros | Cons | Suitable for | Format Support |
|----------|-------------|------|------|--------------|----------------|
| **1. No version history ❌** | Files only in Power BI Service | None | No audit trail, overwrites, no rollback | Never | `.pbix` (implicit only) |
| **2. SharePoint/OneDrive ✔** | Store `.pbix` / `.pbip` in library with version history | Simple setup, auto versioning, timestamps | Binary diffs not meaningful, manual merges | Small projects, prototypes | `.pbix`, `.pbip` |
| **3. Fabric Deployment Pipelines ➡** | Promote across Dev → Test → Prod | Safe, repeatable promotion, governance | Not true version control, limited diffs/history | Teams needing promotion only | `.pbix`, `.pbip` (partial support) |
| **4. Linked Git repository ✅** | PBIP linked to Git | Full version history, PRs, diffs on `.tmdl`/`.pbir` | Requires Git/DevOps maturity | Enterprise BI, multi-developer projects | `.pbip` (with `.tmdl` + `.pbir`) |

---

## Folder Structure (PBIP Projects)

A PBIP project typically contains:

```text
MyProject/
│
├── MyModel.pbip                # Project manifest
│
├── dataset/
│   └── definition.tmdl         # Tabular model definition
│
├── report/
│   └── definition.pbir         # Report definition
│
└── .gitignore                  # Ignore build artifacts, cache files, etc.
```

---

## OTAP Deployment Approaches

- **Fabric Deployment Pipelines:** Use rules to swap connections/parameters; promote Dataset before Reports.  
- **Azure Pipelines (YAML/IaC):** Automate build & release from Git; manage Fabric assets/config via templates; gates and approvals per stage.  
- **Hybrid:** Git (source of truth) + Fabric Pipelines (promotion) for a lightweight but governed flow.  

---

## Best Practices
- Prefer **.pbip** over `.pbix` for version control.  
- Define a **branching strategy** (main/dev/feature).  
- Use **pull requests and code reviews** for semantic model changes.  
- Write clear **commit messages** documenting dataset/report changes.  
- Parameterize connections to keep environments aligned (Dev/Test/Prod).  
- Validate changes locally in Desktop before merging to Git.  
- Automate **unit checks**: schema validation, row counts, refresh tests.  

---

[^1]: **Power BI Projects (.pbip)** files are relatively new. Some features (such as pipeline integration) may still be evolving.  
