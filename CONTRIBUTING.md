# Contributing to the Vision Playbook

Thank you for contributing to Plainsight's Vision Playbook! This guide explains how to set up your local environment, preview changes, and submit them for review.

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PlainsightPro/Vision-Playbook.git
cd Vision-Playbook
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the conversion script

The playbook source lives in the Obsidian vault (root-level markdown files). To generate the MkDocs `docs/` folder from the current Obsidian content, run:

```bash
python convert_obsidian_to_mkdocs.py
```

### 4. Preview locally

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. The site auto-reloads when you edit files in `docs/`.

## Editing Content

You have two workflows:

### Workflow A: Edit Obsidian files, then convert

1. Edit the **original** Markdown files (root folders like `About Plainsight/`, `Technical Guideline Ops/`, etc.) using Obsidian or any editor.
2. Re-run `python convert_obsidian_to_mkdocs.py` to regenerate `docs/`.
3. Preview with `mkdocs serve`.

### Workflow B: Edit docs/ directly

1. Edit files inside `docs/` (uses standard Markdown, no Obsidian syntax).
2. Preview with `mkdocs serve`.

> **Note:** If you edit `docs/` directly, those changes will be overwritten next time someone runs the conversion script. For permanent changes, update the original Obsidian files.

## Submitting Changes

1. Create a new branch from `main`:
   ```bash
   git checkout -b your-branch-name
   ```
2. Make your changes and commit with clear messages.
3. Push your branch:
   ```bash
   git push origin your-branch-name
   ```
4. Open a **Pull Request** targeting `main` on GitHub.
5. Request review — the PR will automatically build a staging preview via Azure Static Web Apps.

Once approved and merged, the site deploys automatically to [playbook.plainsight.pro](https://playbook.plainsight.pro).

## Project Structure

| Path | Purpose |
|---|---|
| `About Plainsight/`, `Technical Guideline Ops/`, etc. | Original Obsidian vault content |
| `docs/` | MkDocs-ready converted content (generated) |
| `images/` | Source images (copied into `docs/images/` during conversion) |
| `mkdocs.yml` | MkDocs configuration |
| `convert_obsidian_to_mkdocs.py` | Conversion script (Obsidian → MkDocs) |
| `requirements.txt` | Python dependencies |
| `.github/workflows/deploy.yml` | CI/CD pipeline |

## Questions?

Reach out to [sander.allert@plainsight.pro](mailto:sander.allert@plainsight.pro) for guidance.
