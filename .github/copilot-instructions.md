# Copilot Instructions for Vision-Playbook

## Project Overview

This is **Plainsight's Vision Playbook** - an open-source company handbook built on transparency, documenting organizational purpose, values, technical guidelines, and operational processes. The content is standard **Markdown** with **MkDocs Material** extensions, deployed as a static site via Azure Static Web Apps.

**Core philosophy**: "Plain Sight" - transparency builds trust, trust generates speed and impact.

## Repository Structure

```
Vision-Playbook/
├── docs/                          # All content (standard Markdown)
│   ├── index.md                   # Site homepage
│   ├── about-plainsight/          # Company mission, values, organisation
│   ├── people-ops/               # HR: onboarding, compensation, holidays
│   │   ├── working/              # Day-to-day work practices
│   │   └── remuneration/         # Compensation and benefits
│   ├── service-delivery/         # Customer engagement
│   ├── technical-guidelines/     # Data platform & Power BI best practices
│   │   ├── architectural-principles/
│   │   ├── power-bi/
│   │   ├── databricks/
│   │   ├── fabric/
│   │   └── dbt/
│   ├── partners/                 # Communities and partnerships
│   ├── images/                   # All image assets
│   ├── stylesheets/extra.css     # Custom branding CSS
│   └── assets/                   # Logo SVGs
├── branding/                     # Internal branding reference (not published)
├── overrides/main.html           # MkDocs theme override
├── mkdocs.yml                    # Site configuration
├── requirements.txt              # Python dependencies
└── .github/workflows/deploy.yml  # CI/CD: build, link-check, deploy
```

## Key Conventions

### Linking & Navigation
Use standard Markdown links: `[Link Text](relative/path.md)`. For images: `![alt text](../images/filename.png)` with relative paths. Use kebab-case for filenames (e.g., `evolution-process.md`).

### Visual Communication First
**Prioritize diagrams over text.** Use Mermaid extensively for processes, architectures, and workflows. Always include proper config:

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
```

Keep diagrams clean and professional - use minimal colors to maintain clarity.

**Color legend (Medallion + semantic layers)**  
- Bronze (Landing/Staging): `#CD7F32` fill, `#8B4513` stroke, light text  
- Silver (ADS/intermediate): `#C0C0C0` fill, `#808080` stroke, dark text  
- Gold (Business products: dims/facts/OBT/feature store): `#FFD700` fill, `#DAA520` stroke, dark text  
Use dashed strokes for optional components and keep the `%%{init...}%%` block intact.

> Avoid Mermaid parsing pitfalls: keep node labels simple (no parentheses/comma-heavy text); prefer separators like `Semantic / Reports / ML` instead of `Semantic, Reports (ML)`.

### MkDocs Material Features
Use MkDocs Material formatting capabilities:

- **Admonitions**: `!!! info "Title"`, `!!! warning "Title"`, `!!! tip "Title"`
- **Collapsible blocks**: `??? info "Title"` (collapsed) / `???+ info "Title"` (open)
- **Code blocks**: Use syntax highlighting (` ```python`, ` ```sql`, ` ```yaml`)
- **Footnotes**: `[^1]` for references without cluttering main text
- **Tables**: Structure data clearly instead of long bullet lists
- **Highlights**: `==highlighted text==`

### Content Philosophy
Write for **consultants in action**, not academic completeness. Professional yet warm tone reflecting Plainsight's transparency values. Mix audience of employees, partners, customers, and public. ==Concrete examples beat abstract principles.==

### Workflow Patterns
**Adding playbook content**: Choose the right `docs/` subfolder → Use kebab-case filenames → **Create a Mermaid diagram first** → Link related pages with standard Markdown links → Update `mkdocs.yml` nav if adding new pages

**Technical guidelines**: Check `docs/technical-guidelines/` → Follow structure: Overview → Practical Examples → Do's & Don'ts → **Always include architecture diagrams** → Reference related pages

## Critical Rules
~~Don't use excessive bullet points~~ → Use tables, diagrams, or prose instead. Use standard Markdown links `[text](path.md)`, not wiki-links. Document actual practiced patterns, not aspirational theory. When adding new pages, update `mkdocs.yml` nav section.

## When Making Changes

Preserve mermaid config blocks, admonition syntax, and table formatting. Update link references when renaming files. Include practical examples or diagrams - match Plainsight's warm, transparent voice.

**Before editing, verify:**
- Standard Markdown links `[text](path.md)` used correctly?
- Content follows structure with visuals?
- Tone matches company values?
- `mkdocs.yml` nav updated if new pages added?
- **Have I created a diagram instead of listing bullet points?**
