# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## What This Is

This is **not a software project** — it is **Plainsight's Vision Playbook**, an open-source company handbook published as a static site at [playbook.plainsight.pro](https://playbook.plainsight.pro). All content is Markdown in `docs/`, built with **MkDocs Material** and deployed to Azure Static Web Apps. There is no application code, test suite, or build artifacts to maintain — the "code" is documentation.

Core philosophy: **"Plain Sight"** — transparency builds trust; trust generates speed and impact.

## Commands

```bash
pip install -r requirements.txt   # one-time setup (mkdocs-material 9.x)
mkdocs serve                      # local preview at http://127.0.0.1:8000, auto-reloads on save
mkdocs build --strict            # the authoritative check — CI runs this and FAILS on any warning
```

`mkdocs build --strict` is the closest thing to a "test." It treats broken internal links, missing nav targets, and other warnings as errors. **Run it before considering any content change done** — it catches the most common breakages (a renamed file not updated in `mkdocs.yml` nav, a relative link pointing nowhere). CI additionally runs the [lychee](https://github.com/lycheeverse/lychee-action) link checker against the built `site/` to validate external URLs.

The generated `site/` folder is git-ignored — never commit it.

## How Content Is Wired Together

Three files must stay in sync when you add, rename, move, or delete a page:

1. **The Markdown file** in the correct `docs/` subfolder (kebab-case filename, e.g. `evolution-process.md`).
2. **`mkdocs.yml` `nav:` section** — pages are NOT auto-discovered into navigation; every page needs an explicit `nav` entry (often with an emoji prefix in its title) or it won't appear in the site menu. A page missing from `nav` triggers a `--strict` warning.
3. **Inbound relative links** from other pages — renaming a file breaks every `[text](path.md)` link pointing at it. `--strict` surfaces these.

Content sections (see `mkdocs.yml` nav for the canonical structure): `about-plainsight/`, `people-ops/` (HR), `service-delivery/`, `technical-guidelines/` (the largest area — `architectural-principles/`, `power-bi/`, `databricks/`, `fabric/`, `dbt/`, `migrations/`), and `partners/`.

`branding/VISUAL-GUIDELINES.md` is an **internal reference, not published** — it defines the brand color system, triangle decoration geometry, and typography that drive `docs/stylesheets/extra.css` and `overrides/main.html`.

## Authoring Conventions

These are house rules, not generic Markdown advice — follow them:

- **Visual-first.** Prioritize Mermaid diagrams and tables over bullet lists and prose — avoid excessive bullet points; reach for a table, diagram, or short prose instead. For processes, architectures, and workflows, create a diagram *first*. Keep diagrams clean and professional with minimal colors. Every Mermaid block should open with the config line so diagrams size correctly:
  ```
  %%{init: { "flowchart": { "useMaxWidth": true } } }%%
  ```
  Avoid Mermaid parsing pitfalls: keep node labels simple — no parentheses or comma-heavy text. Prefer `Semantic / Reports / ML` over `Semantic, Reports (ML)`.
- **Medallion color legend** (use consistently in architecture diagrams, also in `VISUAL-GUIDELINES.md`):
  - Bronze (Landing/Staging): fill `#CD7F32`, stroke `#8B4513`, light text
  - Silver (ADS/Intermediate): fill `#C0C0C0`, stroke `#808080`, dark text
  - Gold (Business products — dims/facts/OBT/feature store): fill `#FFD700`, stroke `#DAA520`, dark text
  - Dashed strokes (`stroke-dasharray: 5 5`) for optional components.
- **Standard Markdown links only** — `[text](relative/path.md)`, never wiki-links. Images: `![alt](../images/filename.png)`.
- **Use MkDocs Material extensions** that are already enabled (see `markdown_extensions` in `mkdocs.yml`): admonitions (`!!! info "Title"`), collapsible blocks (`??? info` / `???+ info`), highlights (`==text==`), footnotes (`[^1]`), task lists, fenced code with language hints.
- **Tone & audience.** Write for **consultants in action**, not academic completeness. Professional but warm, reflecting Plainsight's transparency. Audience is mixed: employees, partners, customers, and the public. Concrete examples beat abstract principles. Document patterns actually in practice, not aspirational theory.
- **Technical-guideline page structure:** Overview → Practical Examples → Do's & Don'ts → architecture diagram → links to related pages.

## Workflow

**One change = one branch**, PR targeting `main`. Each PR auto-deploys a staging preview via Azure Static Web Apps; merge to `main` deploys to production. Keep PRs focused and reviewable.

Before submitting a change, verify:

- Internal links use standard Markdown `[text](path.md)` (no wiki-links) and resolve.
- `mkdocs.yml` `nav` is updated if pages were added, renamed, moved, or deleted.
- Content leads with a diagram or table where it would beat a bullet list, and Mermaid config blocks / admonition syntax / table formatting are intact.
- Tone matches Plainsight's warm, transparent voice.
- `mkdocs build --strict` runs clean.
