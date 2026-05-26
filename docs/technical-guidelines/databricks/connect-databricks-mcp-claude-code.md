---
description: "Connect the Databricks MCP server to your local Claude Code session. Gives Claude direct access to SQL execution, job management, vector search, and 50+ Databricks tools."
---

# Connect Databricks MCP to Claude Code

??? info "Purpose"
    This guide explains how to connect the Databricks MCP server to Claude Code running on your local machine. Once connected, Claude can execute SQL, manage jobs, query vector search indexes, browse Unity Catalog, and use 50+ Databricks tools directly from your terminal.

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Claude Code** | CLI (`npm install -g @anthropic-ai/claude-code`) or Desktop app |
| **uv** | Python package manager (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| **ai-dev-kit repo** | Clone `PlainsightPro/ai-dev-kit` locally |
| **Databricks CLI** | Installed and authenticated with at least one profile |

## Step 1: Clone the ai-dev-kit repo

If you haven't already:

```bash
git clone https://github.com/PlainsightPro/ai-dev-kit.git
```

This repo contains the Databricks MCP server under `databricks-mcp-server/`.

## Step 2: Configure a Databricks CLI profile

The MCP server authenticates to Databricks using a CLI profile. If you don't have one yet:

```bash
databricks configure --profile <your-profile-name>
```

You'll be prompted for your workspace URL and access token. You can verify your profile works:

```bash
databricks auth env --profile <your-profile-name>
```

Your profiles are stored in `~/.databrickscfg` (on Windows: `C:\Users\<you>\.databrickscfg`).

## Step 3: Add to .mcp.json

Create or edit `.mcp.json` in your project root (per-project) or `~/.claude/.mcp.json` (global):

=== "Windows"

    ```json
    {
      "mcpServers": {
        "databricks": {
          "command": "uv",
          "args": [
            "run",
            "--directory",
            "C:\\Users\\<you>\\path\\to\\ai-dev-kit",
            "python",
            "databricks-mcp-server/run_server.py"
          ],
          "env": {
            "DATABRICKS_CONFIG_PROFILE": "<your-profile-name>"
          },
          "defer_loading": true
        }
      }
    }
    ```

=== "macOS / Linux"

    ```json
    {
      "mcpServers": {
        "databricks": {
          "command": "uv",
          "args": [
            "run",
            "--directory",
            "/Users/<you>/path/to/ai-dev-kit",
            "python",
            "databricks-mcp-server/run_server.py"
          ],
          "env": {
            "DATABRICKS_CONFIG_PROFILE": "<your-profile-name>"
          },
          "defer_loading": true
        }
      }
    }
    ```

Replace:

- `<you>` with your OS username
- `path/to/ai-dev-kit` with the actual path to your cloned ai-dev-kit repo
- `<your-profile-name>` with your Databricks CLI profile name

??? tip "`defer_loading` keeps startup fast"
    The `defer_loading: true` setting means Claude Code won't load the Databricks tools until you actually need them. This keeps session startup snappy — the 50+ Databricks tools are loaded on first use.

## Step 4: Verify the connection

Start Claude Code in your project and type `/mcp`. You should see `databricks` listed as a connected server.

Quick test — ask Claude:

> Execute a SQL query on Databricks: SELECT current_user()

If it returns your Databricks username, the connection is working.

## Available tools

Once connected, Claude has access to 50+ Databricks tools including:

| Category | Examples |
|----------|---------|
| **SQL execution** | `execute_sql`, `execute_sql_multi` |
| **Unity Catalog** | `manage_uc_objects`, `manage_uc_grants`, `get_table_stats_and_schema` |
| **Jobs & pipelines** | `manage_jobs`, `manage_job_runs`, `manage_pipeline` |
| **Compute** | `list_compute`, `manage_cluster`, `manage_sql_warehouse` |
| **Vector search** | `manage_vs_index`, `query_vs_index`, `manage_vs_endpoint` |
| **Model serving** | `manage_serving_endpoint` |
| **Genie** | `ask_genie`, `manage_genie` |
| **Workspace** | `manage_workspace_files`, `execute_code` |

## Switching workspaces

To connect to a different Databricks workspace, change the `DATABRICKS_CONFIG_PROFILE` value in your `.mcp.json` to a different CLI profile. Each profile points to a specific workspace.

You can also have multiple Databricks MCP entries for different workspaces:

```json
{
  "mcpServers": {
    "databricks-dev": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/ai-dev-kit", "python", "databricks-mcp-server/run_server.py"],
      "env": { "DATABRICKS_CONFIG_PROFILE": "dev-workspace" },
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

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `databricks` shows as disconnected in `/mcp` | Check that the `--directory` path in your `.mcp.json` points to the correct ai-dev-kit location. Run `uv run --directory /path/to/ai-dev-kit python databricks-mcp-server/run_server.py` manually to see errors. |
| Authentication error / 401 | Your Databricks CLI profile may be expired. Re-run `databricks configure --profile <name>` or refresh your token. |
| `uv` not found | Install uv: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Tools load but SQL fails | Verify your profile has access to a SQL warehouse. Check with `databricks sql warehouses list --profile <name>`. |
| Slow startup | Ensure `defer_loading` is set to `true` so tools are loaded on demand, not at session start. |
