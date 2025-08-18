# Versioning & Folder Structure (Git + PBIP)

## Overview

Treat Power BI like software. Prefer **Power BI Desktop Projects (.pbip)**[^1] so semantic model/report definitions are text-based and diffable. Choose a versioning approach that fits project scale and governance needs; the options below are ordered from least to most mature.

## Versioning Options (least → most mature)

### 1) No version history (❌ Not done)

- **Description:** Files live only on a local machine or shared drive without versioning.
- **Use when:** Never recommended.
- **Risks:** No audit trail, high risk of overwrites, difficult rollbacks.

### 2) SharePoint / OneDrive library with versioning (✔ Acceptable for small projects)

- **Description:** Store `.pbix` / `.pbip` files in a SharePoint or OneDrive library with version history enabled.
- **Pros:** Simple to set up; automatic versioning & timestamps; familiar to business teams.
- **Cons:** Binary diffs are not meaningful; branching/review is limited; merges are manual.
- **Use when:** **Smaller projects** or short-lived prototypes where Git maturity is overkill.

### 3) Fabric Deployment Pipelines (➡ Promotion, not true versioning)

- **Description:** Use **Deployment Pipelines** to promote content across environments (e.g., Dev → Test → Prod).
- **Pros:** Safe, repeatable promotions; rules for parameters/connections; good governance step.
- **Cons:** Deployment Pipelines are actually **not a version control system** ; limited history/diffs; doesn’t replace Git.
- **Use when:** You need structured **environment promotion** but aren’t yet ready for full Git workflows. Can be combined with (2) or (4).

### 4) Linked Git repository (✅ Preferred)

- **Description:** Connect your workspace or PBIP projects to a Git repo in **Azure DevOps** or **GitHub (Enterprise)**.
- **Pros:** Proper version history, branches, pull requests, code reviews, CI/CD; text diffs on PBIP assets.
- **Deployments:** Orchestrate OTAP (Dev/Test/Acc/Prod) via **Fabric Deployment Pipelines** and/or **Azure (Build) Pipelines** using **YAML/IaC**.
- **Use when:** **Default choice** for all production-grade and multi-team projects.

# OTAP deployment approaches

- **Fabric Deployment Pipelines:** Use rules to swap connections/parameters; promote Dataset before Reports.
- **Azure Pipelines (YAML/IaC):** Automate build & release from Git; manage Fabric assets/config via templates; gates and approvals per stage.
- **Hybrid:** Git (source of truth) + Fabric Pipelines (promotion) for a lightweight but governed flow.

[^1]: **Power BI Projects (.pbip)** files are relatively new. Some features (such as using them in Fabric Deployment Pipelines) are not available at the time of writing. 
