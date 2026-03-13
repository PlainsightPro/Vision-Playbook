# Third-Party Tools for dbt

## Overview
Several third-party tools complement dbt development, governance, and documentation.  
While not required, they significantly improve productivity, consistency, and the quality of published documentation.  

The most vital tool to know and use is **dbt Power User** in VS Code, paired with SQLFluff linting for dbt templating.  

---

## Key Tools

### dbt Power User
- **Purpose:** Primary VS Code extension for dbt navigation and documentation.  
- **Key Capabilities:**  
  - Graph and lineage browsing from manifest artifacts.  
  - `ref()`/`source()` auto-complete and quick open of dependent models.  
  - Inline editing of model/column descriptions to reduce undocumented items.  
  - Documentation stubs and shortcuts to keep `_models.yml` synchronized.  
- **Recommended Settings:**  
  - Point to `target/manifest.json` for accurate lineage.  
  - Enable “Generate Documentation Stub” command for new models.  

---

### SQLFluff
- **Purpose:** Enforce consistent SQL/Jinja style and catch templating errors.  
- **Key Capabilities:**  
  - dbt-aware linting (`templater = dbt`).  
  - CI-friendly outputs (GitHub annotations, JSON).  
  - Optional auto-fix with review.  
- **Config Example:**  

```ini
[sqlfluff]
dialect = ansi
templater = dbt
exclude_rules = L009

[tool:sqlfluff:templater:dbt]
project_dir = .
profiles_dir = .
```

```sh
sqlfluff lint models --format github-annotation
sqlfluff fix models --force
```

---

### dbt VS Code Extension (Fusion Engine Preview) ƒ?" Optional
- **Purpose:** Experimental Fusion Engine completion and semantic cues.  
- **When to Use:** Optional add-on alongside dbt Power User for teams that want graph-aware hints.  
- **Guardrails:** Keep lint/tests as the source of truth; disable conflicting shortcuts; validate features per adapter.  

---

## Common Community Packages (Reference)
Use a small, pinned set of packages; avoid floating versions. Evaluate maintenance, adapter support, and performance before adoption.

| Package                 | Why use it                                   | Notes / Guardrails                                                         |
| ----------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| `dbt-utils`             | Canonical macros and reusable tests          | Default include; keep versions pinned in `packages.yml`.                   |
| `dbt-codegen`           | Generate YAML/model stubs to accelerate docs | Review generated code; do not commit without edits.                        |
| `dbt_project_evaluator` | Governance checks for structure/tests        | Run in CI on schedule; validate findings before blocking.                  |
| `audit_helper`          | Lightweight reconciliation patterns          | Scope to critical flows; keep configs adapter-agnostic.                    |
| `dbt_expectations`      | Rich expectations-style tests                | Powerful but can be slow on large tables; sample/partition where possible. |
| `dbt-bounce`            | Validate refs/tests connectivity             | Optional; useful for dependency sanity checks.                             |
| `elementary`            | Monitoring/observability for dbt runs        | Adds overhead; justify for teams needing run-time telemetry.               |

!!! tip "Keep `packages.yml` pinned"
    Pin every package version and review upgrades alongside dbt-core minor releases.

---

## Onboarding Defaults
- Install VS Code and recommended extensions:  

```json
{
  "recommendations": [
    "innoverio.vscode-dbt-power-user",
    "ms-python.python",
    "ms-toolsai.jupyter",
    "ms-vscode.powershell"
  ]
}
```

- Set `DBT_PROFILES_DIR` (env or VS Code settings) and run `dbt deps` before first `dbt build`.  
- Install SQLFluff with dbt templater: `pip install "sqlfluff[dbt]"`.  
- Run `sqlfluff lint models/` locally; fix or baseline before opening PRs.  
- Use dbt Power User to generate docs stubs as you add models/sources.  

---

## Related Pages
- [Documentation](documentation.md)
