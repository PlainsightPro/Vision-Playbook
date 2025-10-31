# Copilot Instructions for Vision-Playbook

## Project Overview

This is **Plainsight's Vision Playbook** — an open-source company handbook built on transparency, documenting organizational purpose, values, technical guidelines, and operational processes. The repository is written in **Markdown** with **Obsidian-style wiki links** (`[[Page Name]]`) and is managed as an Obsidian vault synced via Git.

**Core philosophy**: "Plain Sight" — transparency builds trust, trust generates speed and impact.

## Repository Structure

```
Vision-Playbook/
├── Playbook Usage/           # Company mission, values, getting started
├── People Ops - Employee Journey/  # HR processes: onboarding, compensation, holidays
├── Service Delivery Ops/     # Customer engagement: strategy, execution, support
├── Technical Guideline Ops/  # Data platform architecture & Power BI best practices
│   ├── Architectural Principles/
│   └── Power BI Best-Practices/
├── Partner Ops/              # Communities and partnerships
├── Customer Ops/             # (Customer-facing processes)
├── QuickZip.py               # Utility script for archiving workspace
└── .github/workflows/        # CI: link checker workflow
```

## Key Conventions

### Linking & Navigation
Use `[[Page Name]]` for internal wiki links (Obsidian convention). Embed images with `![[image.png]]`. Preserve emojis in filenames exactly as they appear (e.g., `🙋️ START HERE.md`). Maintain spaces in folder names like `People Ops - Employee Journey/`.

### Visual Communication First
**Prioritize diagrams over text.** Use Mermaid extensively for processes, architectures, and workflows. Always include proper config:

```mermaid
%%{init: { "flowchart": { "useMaxWidth": true } } }%%
```

Keep diagrams clean and professional—use minimal colors to maintain clarity. Readers need visual clarity for quick comprehension.

### Obsidian Power Features
Leverage Obsidian's full formatting capabilities:

- **Callouts**: `> [!info]`, `> [!warning]`, `> [!tip]` for highlighted information
- **Code blocks**: Use syntax highlighting (` ```python`, ` ```sql`, ` ```yaml`)
- **Footnotes**: `[^1]` for references without cluttering main text
- **Comments**: `%% internal note %%` for hidden documentation notes
- **Tables**: Structure data clearly instead of long bullet lists
- **Blockquotes**: `>` for quotes or extracted principles

### Content Philosophy
Write for **consultants in action**, not academic completeness. Professional yet warm tone reflecting Plainsight's transparency values. Mix audience of employees, partners, customers, and public. ==Concrete examples beat abstract principles.==

### Workflow Patterns
**Adding playbook content**: Choose the right folder → Use emoji-prefixed names where patterns exist → **Create a Mermaid diagram first** → Link related pages with `[[Page Name]]`

**Technical guidelines**: Check `Technical Guideline Ops/` → Follow structure: Overview → Practical Examples → Do's & Don'ts → **Always include architecture diagrams** → Reference related pages

## Critical Rules
~~Don't use excessive bullet points~~ → Use tables, diagrams, or prose instead. Preserve wiki link syntax `[[Page Name]]` and emoji filenames. This is Obsidian-flavored Markdown with custom plugins, not standard Markdown. Document actual practiced patterns, not aspirational theory.

## When Making Changes

Preserve mermaid config blocks, callout syntax, and table formatting. Update `[[Old Page Name]]` references when renaming. Include practical examples or diagrams—match Plainsight's warm, transparent voice. 

**Before editing, verify:**
- Obsidian compatibility maintained?
- Wiki links `[[Page Name]]` still valid?
- Content follows structure with visuals?
- Tone matches company values?
- **Have I created a diagram instead of listing bullet points?**