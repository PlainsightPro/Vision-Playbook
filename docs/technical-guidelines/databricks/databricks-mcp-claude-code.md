---
description: "Connect Databricks to AI tools: MCP server for Claude Code (local) and Genie Code via Plainsight Brain (cloud)."
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
    The `defer_loading: true` setting means Claude Code won't load the Databricks tools until you actually need them. This keeps session startup snappy - the 50+ Databricks tools are loaded on first use.

## Step 4: Verify the connection

Start Claude Code in your project and type `/mcp`. You should see `databricks` listed as a connected server.

Quick test - ask Claude:

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

---

# Databricks Genie Code ↔ Plainsight Brain

Connect Databricks Genie Code to Plainsight Brain via a Unity Catalog HTTP connection. No Agent Framework needed - Genie Code calls the MCP endpoint directly using OAuth2 delegated auth. Use the `/mcp/genie` endpoint to stay within Databricks' 15-tool limit.

## How It Works

```
Databricks Genie Code
  |
  |  Uses Unity Catalog HTTP Connection
  |  with OAuth2 delegated flow
  v
Plainsight Brain /mcp/genie Endpoint
  (Streamable HTTP, genie profile: 15 tools)
  |
  |  Token carries user identity
  |  scp: Brain.Access
  v
AuthMiddleware resolves Entra JWT → AuthContext
```

Genie Code connects to external MCP servers via Unity Catalog HTTP connections. The user logs in interactively through the OAuth2 flow, and the resulting token carries their Entra identity. Plainsight Brain validates the JWT and resolves the user to admin or team tier based on their roles and group memberships.

!!! warning "Genie Code 15-tool limit"
    Databricks Genie Code has a hard limit of 15 tools per MCP connection. Use the `/mcp/genie` base path instead of `/mcp`. This activates the genie tool profile, which exposes exactly 15 curated tools. The default `/mcp` endpoint advertises 26 tools and will exceed the limit.

## Prerequisites

| Requirement | Details |
|---|---|
| **Databricks workspace** | With Genie Code enabled |
| **Plainsight Entra ID account** | `your-name@plainsight.pro` |
| **Access to Brain app registration** | Ask an admin to grant you access to app `f090a744-fdef-4e40-aaa6-57811b4b6377` |
| **Unity Catalog permissions** | Permission to create HTTP connections in your Databricks workspace |

## Connection Details

| Setting | Value |
|---|---|
| **Connection type** | HTTP |
| **Host** | `https://ca-plainsight-brain.thankfulglacier-ff0d1152.swedencentral.azurecontainerapps.io` |
| **Base path** | `/mcp/genie` |
| **Auth type** | OAuth2 delegated (user signs in interactively) |
| **Client ID** | `28f0e9f1-2fb3-4512-a131-7fd01fe8c3dd` (MCP Client app registration) |
| **OAuth scope** | `api://f090a744-fdef-4e40-aaa6-57811b4b6377/Brain.Access offline_access` |

??? info "`offline_access` scope"
    The `offline_access` scope requests a refresh token so the connection persists across sessions without requiring re-authentication.

## Infrastructure: Allow Your Databricks Workspace

Before Genie Code can connect, the Plainsight Brain deployment must allow your Databricks workspace URL as a CORS origin and MCP client host. This is configured via the `databricksWorkspaceUrls` parameter in `infra/main.bicep`.

### How it works

The Bicep template merges the Databricks workspace URLs into the `MCP_ALLOWED_ORIGINS` and `MCP_ALLOWED_HOSTS` environment variables automatically. You only need to set the parameter - the merge logic handles the rest.

### Add your workspace URL

Find the `databricksWorkspaceUrls` parameter in `infra/main.bicep` and add your workspace URL. For multiple workspaces, use a comma-separated list:

```
// Single workspace (default)
param databricksWorkspaceUrls string = 'https://adb-7405619371624001.1.azuredatabricks.net'

// Multiple workspaces
param databricksWorkspaceUrls string = 'https://adb-7405619371624001.1.azuredatabricks.net,https://adb-9988776655443322.1.azuredatabricks.net'
```

### Deploy the change

```bash
az deployment group create -g rg-plainsight-brain -f infra/main.bicep
```

!!! warning "CORS allowlisting required"
    If your Databricks workspace URL is not allowlisted, MCP requests from Genie Code will be rejected by CORS policy. This is the most common cause of "connection works but tools fail" issues.

## Setup: Create the Unity Catalog HTTP Connection

Run the following in a Databricks notebook to create the HTTP connection:

```python
import json

connection_config = {
    "connection_name": "plainsight_brain_mcp",
    "connection_type": "HTTP",
    "host": "https://ca-plainsight-brain.thankfulglacier-ff0d1152.swedencentral.azurecontainerapps.io",
    "base_path": "/mcp/genie",
    "auth_type": "OAuth",
    "oauth_client_id": "28f0e9f1-2fb3-4512-a131-7fd01fe8c3dd",
    "oauth_scope": "api://f090a744-fdef-4e40-aaa6-57811b4b6377/Brain.Access offline_access"
}

# Create the connection via Unity Catalog
spark.sql(f"""
CREATE CONNECTION IF NOT EXISTS plainsight_brain_mcp
TYPE HTTP
OPTIONS (
    host '{connection_config["host"]}',
    base_path '/mcp/genie',
    auth_type 'OAuth',
    oauth_client_id '{connection_config["oauth_client_id"]}',
    oauth_scope '{connection_config["oauth_scope"]}'
)
""")
```

!!! warning "SQL syntax may vary"
    The exact SQL syntax for HTTP connections may vary by Databricks workspace version. Consult your workspace documentation if the above syntax does not work.

## Entra App Registrations

The integration uses two Entra app registrations by design - do not merge them.

| App | Client ID | Purpose |
|---|---|---|
| **API (Brain server)** | `f090a744-fdef-4e40-aaa6-57811b4b6377` | Exposes the `Brain.Access` scope, validates incoming tokens |
| **Client (MCP Client)** | `28f0e9f1-2fb3-4512-a131-7fd01fe8c3dd` | Used by Databricks (and other MCP clients) to request tokens on behalf of the user |

!!! warning "`accessTokenAcceptedVersion` must be `2`"
    `accessTokenAcceptedVersion` must be set to **2** on the API app registration manifest. If set to `null` or `1`, Entra issues v1 tokens with a different issuer format, causing JWT validation to fail with an issuer mismatch error.

## Genie Tool Profile (15 tools)

The `/mcp/genie` endpoint activates a curated profile of 15 tools designed for data exploration in Databricks. This stays within Genie Code's hard limit while covering the most valuable capabilities.

| Tool | Purpose |
|---|---|
| `brain_start` | Begin a session - loads project context and team intelligence |
| `brain_finish` | End session with durable learnings for the knowledge base |
| `recall` | Semantic search across personal memories |
| `remember` | Store a new memory |
| `sync_project` | Register or update project context |
| `get_project` | Get project details |
| `get_project_brief` | Get a project summary with recent activity |
| `get_company_intelligence` | Retrieve company-wide intelligence for a project |
| `team_search_findings` | Semantic search across team knowledge |
| `team_share_finding` | Share a discovery with the team |
| `playbook_search` | Search the team playbook |
| `playbook_get_section` | Read a specific playbook section |
| `sdlc_check_conformance` | Check SDLC governance conformance |
| `sdlc_search_guidance` | Search SDLC guidance and best practices |
| `review_scan` | Run an automated code review scan |

The full `/mcp` endpoint (26 tools) and the complete registry (`PLAINSIGHT_MCP_TOOL_PROFILE=full`, 87 tools) remain available for other MCP clients like Claude Code that don't have tool limits.

## Key Points

- **Use `/mcp/genie`**: Genie Code has a 15-tool limit. The genie profile exposes exactly 15 curated tools. The default `/mcp` (26 tools) will exceed the limit.
- **No Agent Framework needed**: Genie Code calls the MCP endpoint directly via the UC HTTP connection.
- **Streamable HTTP transport**: Plainsight Brain already supports this, which is what Genie Code requires.
- **User identity flows through**: the OAuth2 delegated flow means the token carries the user's Entra identity. Brain resolves them to admin or team tier based on their roles.
- **No separate service principal**: the existing MCP Client app registration is reused. No M2M client credentials flow.
- **Refresh tokens**: the `offline_access` scope ensures the connection gets a refresh token, so the user doesn't need to re-authenticate every session.
- **Same deployment**: the genie profile runs on the same container as the default endpoint. No additional infrastructure needed.

## Verify the Connection

After creating the connection, test it from a Databricks notebook:

```
# Test the connection by calling brain_start
# Genie Code should be able to invoke MCP tools through the connection

# Quick health check via the connection
# GET https://ca-plainsight-brain.thankfulglacier-ff0d1152.swedencentral.azurecontainerapps.io/healthz
# Should return 200 OK
```

If Genie Code can call `brain_start` and receives project context and intelligence sections, the connection is working.

## Troubleshooting

| Symptom | Fix |
|---|---|
| 401 Unauthorized | Check that your Entra account has been granted access to the Brain API app registration. Verify `accessTokenAcceptedVersion` is set to **2** on the API app manifest. |
| Issuer mismatch / invalid token | `accessTokenAcceptedVersion` is likely `null` or `1` on the API app registration. Set it to `2` in the Entra portal under App registrations → Manifest. |
| OAuth consent loop | Ensure the MCP Client app (`28f0e9f1`) has API permissions for `Brain.Access` on the API app (`f090a744`). An admin may need to grant tenant-wide consent. |
| CORS error / requests blocked | Your Databricks workspace URL is not in `databricksWorkspaceUrls` in `infra/main.bicep`. Add it and redeploy. See [Infrastructure](#infrastructure-allow-your-databricks-workspace) above. |
| Connection created but tools don't appear | Verify the base path is `/mcp/genie` and the host URL does not have a trailing slash. |
| Too many tools / tool limit exceeded | You are using `/mcp` instead of `/mcp/genie`. The default endpoint exposes 26 tools which exceeds Genie Code's 15-tool limit. Change the base path to `/mcp/genie`. |
| `/readyz` returns 503 | The server is still initializing its 17 Cosmos DB containers. Wait ~30 seconds and retry. |
| Token expires quickly / re-login required each session | Ensure `offline_access` is included in the OAuth scope so a refresh token is issued. |
