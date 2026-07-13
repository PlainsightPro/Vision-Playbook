---
description: "High-level security habits for Plainsight's Azure work: Azure Key Vault as the single home for secrets."
---

# Security Fundamentals

??? info "Purpose"
    You don't need to be a security engineer to build securely on Azure: one habit covers most of it. Every secret lives in Key Vault. This page keeps it deliberately high-level.

## Azure Key Vault

Key Vault is the **only** acceptable home for secrets, keys, and certificates. If a credential exists, it lives in a vault, full stop.

| Store in Key Vault | Never store in |
|---|---|
| Connection strings, API keys, storage keys | Code or notebooks |
| Certificates | Pipeline variable text fields |
| Encryption keys | Config files in Git |
| Service credentials that can't be managed identities | Chat messages or wikis |

How we use it:

| Practice | Detail |
|---|---|
| One vault per product per environment | `kv-<product>-prd-...` and `kv-<product>-dev-...`: PRD secrets are never readable from non-PRD |
| RBAC authorization mode | Use Azure RBAC (e.g. *Key Vault Secrets User*), not legacy access policies |
| Consumers use managed identities | Databricks secret scopes, ADF linked services, and Fabric connections all read from Key Vault without any bootstrap secret |
| Soft delete + purge protection | Enabled: an accidental (or malicious) delete is recoverable |
| Rotation | Prefer managed identities so there is nothing to rotate; where keys must exist, rotate them and let consumers resolve the vault reference |

!!! tip "The litmus test"
    If revoking a credential requires editing code or redeploying a pipeline, it's stored in the wrong place.

## Quick Reference: Do's and Don'ts

| Do ✅ | Don't ❌ |
|---|---|
| Put every secret in Key Vault | Paste keys into notebooks, code, or chat |
| Enable soft delete and purge protection on vaults | Leave vaults deletable in one click |
| Separate PRD and non-PRD vaults | Share one vault across environments |
| Disable public network access where the service allows it | Expose storage and SQL publicly by default |

## Related pages

- [Identity & Access](identity-and-access.md): the identity layer in practice
- [Regions & Storage](regions-and-storage.md): storage network settings
- [Resource Organization](resource-organization.md): enforcing security settings via Azure Policy
