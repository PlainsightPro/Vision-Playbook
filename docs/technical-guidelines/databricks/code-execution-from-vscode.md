---
description: "Run Databricks notebooks and code from VS Code with explicit cluster selection across dev, acc, and prod environments."
---

# Code Execution from VS Code

??? info "Purpose"
    This guide explains how to execute notebooks and Python code against Databricks clusters directly from VS Code, with explicit environment selection to prevent accidental runs against the wrong cluster.

## Databricks Extension for VS Code

The official Databricks extension lets you attach to a remote cluster and run notebooks interactively.

### Setup

1. Install the **Databricks** extension from the VS Code marketplace
2. Open the command palette (`Ctrl+Shift+P`) → `Databricks: Configure Workspace`
3. Select or create a Databricks CLI profile (stored in `~/.databrickscfg`)

### Cluster Selection

Once the extension is configured:

1. Open the **Databricks sidebar** in VS Code
2. Browse the list of available clusters — names should follow your project naming convention (e.g. `dev-analytics`, `acc-etl`, `prod-reporting`)
3. **Click to attach** to the cluster you want to use
4. The attached cluster name is always visible in the **VS Code status bar**

!!! warning "Always verify the status bar"
    Before running any cell, check the cluster name in the VS Code status bar. Switching environments requires deliberately selecting a different cluster — there is no accidental drift.

### Running Code

With a cluster attached you can:

- **Run `.py` files** as Databricks notebooks
- **Run Jupyter notebooks** (`.ipynb`) cell-by-cell against the remote cluster
- **Use the integrated terminal** with the Databricks CLI for ad-hoc commands

### Useful Extensions

Install these alongside the Databricks extension for a complete development experience:

| Extension | Purpose |
|-----------|---------|
| **Python** | Language support, linting, formatting |
| **Jupyter** | Notebook rendering and cell execution |
| **Pylance** | Type checking and IntelliSense |
| **GitLens** | Git history and blame annotations |

## Databricks MCP via Claude Code

The Databricks MCP server gives Claude Code direct access to SQL execution, Unity Catalog, jobs, and 50+ other Databricks tools. See [Connect Databricks MCP to Claude Code](connect-databricks-mcp-claude-code.md) for the full setup guide.

For safe multi-environment usage, configure **separate MCP entries per environment** in your `.mcp.json`:

```json
{
  "mcpServers": {
    "databricks-dev": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/ai-dev-kit", "python", "databricks-mcp-server/run_server.py"],
      "env": { "DATABRICKS_CONFIG_PROFILE": "dev-workspace" },
      "defer_loading": true
    },
    "databricks-acc": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/ai-dev-kit", "python", "databricks-mcp-server/run_server.py"],
      "env": { "DATABRICKS_CONFIG_PROFILE": "acc-workspace" },
      "defer_loading": true
    },
    "databricks-prod": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/ai-dev-kit", "python", "databricks-mcp-server/run_server.py"],
      "env": { "DATABRICKS_CONFIG_PROFILE": "prod-workspace" },
      "defer_loading": true
    }
  }
}
```

The environment name is part of the MCP server name (`databricks-dev`, `databricks-acc`, `databricks-prod`), making it immediately clear which workspace any tool call targets.

## How Cluster Selection Is Enforced

Every execution path requires an explicit environment choice — there is no default that silently targets production.

| Mechanism | How It Enforces Explicit Selection |
|---|---|
| **Databricks VS Code extension** | Cluster must be selected in sidebar; name shown in status bar; no default |
| **MCP `.mcp.json`** | Each entry is named per environment; profile determines workspace |
| **Databricks CLI profiles** | `~/.databrickscfg` has named profiles (`dev`, `acc`, `prod`); you choose which to use |
| **DAB bundles (CI/CD)** | Target is an explicit CLI argument: `databricks bundle deploy -t dev` |

!!! tip "Naming convention matters"
    Use consistent, environment-prefixed names for clusters (`dev-*`, `acc-*`, `prod-*`) and CLI profiles. This makes accidental environment mismatches immediately visible across all tools.
