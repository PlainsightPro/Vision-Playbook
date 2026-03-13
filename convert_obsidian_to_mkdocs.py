"""
convert_obsidian_to_mkdocs.py

Reads every Markdown file from the Obsidian vault and writes a
MkDocs-compatible copy into docs/.  Original files are NEVER modified.

Conversions performed
---------------------
1. [[wikilinks]]              → [text](relative/path.md)
2. [[link|alias]]             → [alias](relative/path.md)
3. [[#heading|alias]]         → [alias](#heading-anchor)
4. [[page#heading|alias]]     → [alias](relative/path.md#heading-anchor)
5. ![[image.png]]             → ![image](../images/image.png)   (relative)
6. ![[image.png|300]]         → ![image](../images/image.png)   (size hint dropped; CSS handles it)
7. > [!type] Title  (callout) → !!! type "Title"  /  ??? type "Title" (collapsible)
8. ==highlight==              → <mark>highlight</mark>  (pymdownx.mark handles this natively via ==)
9. Obsidian frontmatter       → stripped (publish: false etc.)

Run:  python convert_obsidian_to_mkdocs.py
"""

from __future__ import annotations

import os
import re
import shutil
import textwrap
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent
DOCS_DIR = REPO_ROOT / "docs"
IMAGES_SRC = REPO_ROOT / "images"
IMAGES_DST = DOCS_DIR / "images"

# ── File mapping: Obsidian filename (without emoji prefix) → docs path ──
# Built dynamically at startup by scanning the vault.

# Maps a *lower-cased, emoji-stripped, extensionless* page name
# to its docs-relative path so we can resolve [[wikilinks]].
page_index: dict[str, str] = {}

# Maps original vault-relative path → docs-relative path
path_map: dict[str, str] = {}

# ── Source → destination folder mapping ──────────────────────────────────
FOLDER_MAP: dict[str, str] = {
    "About Plainsight": "about-plainsight",
    "People Ops - Employee Journey": "people-ops",
    "People Ops - Employee Journey/🔨Working @ Plainsight": "people-ops/working",
    "People Ops - Employee Journey/🔨Working @ Plainsight/Your Renumeration Package": "people-ops/remuneration",
    "Service Delivery Ops": "service-delivery",
    "Technical Guideline Ops": "technical-guidelines",
    "Technical Guideline Ops/Architectural Principles": "technical-guidelines/architectural-principles",
    "Technical Guideline Ops/Power BI Best-Practices": "technical-guidelines/power-bi",
    "Technical Guideline Ops/Databricks Best-Practices": "technical-guidelines/databricks",
    "Technical Guideline Ops/Fabric Best-Practices": "technical-guidelines/fabric",
    "Technical Guideline Ops/dbt Best-Practices": "technical-guidelines/dbt",
    "Partner Ops": "partners",
}

# ── Filename mapping (emoji → clean slug) ────────────────────────────────
FILENAME_MAP: dict[str, str] = {
    "🙋️ START HERE.md": "start-here.md",
    "🥇 The Foundation of Plainsight.md": "the-foundation-of-plainsight.md",
    "🏗️ How We're Organised.md": "how-were-organised.md",
    "🛹 Pre-boarding & Hiring.md": "pre-boarding-and-hiring.md",
    "🚀 Onboarding.md": "onboarding.md",
    "😢 Off-Boarding.md": "off-boarding.md",
    "🔨 Tools We Love.md": "tools-we-love.md",
    "🎯 Evolution Process.md": "evolution-process.md",
    "🚀 Impact by Ownership.md": "impact-by-ownership.md",
    "🌱 Learning And Experimentation.md": "learning-and-experimentation.md",
    "🏢 Our Offices and Locations.md": "our-offices-and-locations.md",
    "💪 Hosting a Teambuilding or Sports Event.md": "hosting-a-teambuilding-or-sports-event.md",
    "📄 CV - CurriculumVitae.md": "cv-curriculum-vitae.md",
    "🤑 Renumeration Package.md": "remuneration-package.md",
    "🌴 Holidays & Illness.md": "holidays-and-illness.md",
    "🚲 Mobility.md": "mobility.md",
    "⭐ Rewards - Stars And Clouds.md": "rewards-stars-and-clouds.md",
    "🎯 AI & Analytics Strategy.md": "ai-and-analytics-strategy.md",
    "🏗️ Execution.md": "execution.md",
    "🆘 Support.md": "support.md",
    "Why 'Technical Guideline Ops'.md": "why-technical-guidelines.md",
    "🤝 Partnerships.md": "partnerships.md",
    "🧑‍🤝‍🧑 Communities.md": "communities.md",
    "🚀 Impact by Ownership.md": "impact-by-ownership.md",
}


def slugify_filename(name: str) -> str:
    """Turn an Obsidian filename into a URL-friendly slug."""
    if name in FILENAME_MAP:
        return FILENAME_MAP[name]
    # Strip emojis (Unicode emoji blocks) and leading/trailing whitespace
    slug = re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\u200d]+', '', name)
    slug = slug.strip()
    # lowercase, replace spaces/special chars
    slug = slug.lower()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[&]", "and", slug)
    slug = re.sub(r"[()]+", "", slug)  # Remove parentheses before slugifying
    slug = re.sub(r"[^a-z0-9.]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)  # Collapse consecutive dashes
    slug = slug.strip("-")
    return slug


def dest_folder(vault_rel_dir: str) -> str:
    """Map a vault-relative directory to a docs-relative directory."""
    # Try longest prefix match
    best = ""
    for src, dst in sorted(FOLDER_MAP.items(), key=lambda x: -len(x[0])):
        if vault_rel_dir == src or vault_rel_dir.startswith(src + "/"):
            return dst + vault_rel_dir[len(src):]
    return vault_rel_dir.lower().replace(" ", "-")


def build_page_index() -> list[tuple[Path, Path]]:
    """Scan vault, build page_index and return (src, dst) pairs."""
    pairs: list[tuple[Path, Path]] = []

    # Folders to skip
    skip = {".git", ".github", ".obsidian", "docs", "__pycache__", "images", "node_modules"}

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in skip]
        root_path = Path(root)
        rel_dir = root_path.relative_to(REPO_ROOT).as_posix()
        if rel_dir == ".":
            rel_dir = ""

        for fname in files:
            if not fname.endswith(".md"):
                continue
            # Skip repo-level non-content files
            if rel_dir == "" and fname in ("README.md", "CONTRIBUTING.md"):
                continue

            src = root_path / fname
            slug = slugify_filename(fname)
            dst_dir = dest_folder(rel_dir) if rel_dir else ""
            dst_rel = f"{dst_dir}/{slug}" if dst_dir else slug
            dst = DOCS_DIR / dst_rel

            pairs.append((src, dst))

            # Index by multiple keys for wikilink resolution
            vault_rel = f"{rel_dir}/{fname}" if rel_dir else fname
            path_map[vault_rel] = dst_rel

            # Index by bare filename (no extension)
            bare = Path(fname).stem
            page_index[bare.lower()] = dst_rel
            # Also index the slug stem
            slug_stem = Path(slug).stem
            page_index[slug_stem.lower()] = dst_rel
            # Also index without emoji
            stripped = re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\u200d]+', '', bare).strip()
            if stripped:
                page_index[stripped.lower()] = dst_rel

    return pairs


def heading_anchor(heading: str) -> str:
    """Convert a heading text to an MkDocs anchor slug."""
    anchor = heading.lower().strip()
    anchor = re.sub(r"[^a-z0-9 _-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    return anchor


def resolve_wikilink(target: str, current_file_dst: str) -> str | None:
    """Resolve a wikilink target string to a docs-relative path."""
    # Handle heading-only links: [[#Heading]]
    if target.startswith("#"):
        return None  # handled separately

    # Strip leading/trailing whitespace
    target = target.strip()

    # Try exact vault-relative path match
    for vault_path, docs_path in path_map.items():
        # Match by vault-relative (without .md sometimes)
        if vault_path == target or vault_path == target + ".md":
            return docs_path
        # Match by tail (filename only)
        vp = Path(vault_path)
        if vp.stem == target or vp.name == target or vp.name == target + ".md":
            return docs_path

    # Try page_index by lowered name
    target_lower = target.lower()
    if target_lower in page_index:
        return page_index[target_lower]

    # Try stripping folder prefixes: "Technical Guideline Ops/Power BI Best-Practices/Third Party Tooling"
    base = target.rsplit("/", 1)[-1]
    base_lower = base.lower()
    if base_lower in page_index:
        return page_index[base_lower]

    # Try without emoji
    stripped = re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\u200d]+', '', base).strip()
    if stripped.lower() in page_index:
        return page_index[stripped.lower()]

    return None


def make_relative(target_docs_path: str, current_file_docs_path: str) -> str:
    """Compute a relative URL from current file to target file, both docs-relative."""
    target = Path(target_docs_path)
    current = Path(current_file_docs_path)
    try:
        rel = os.path.relpath(target, current.parent).replace("\\", "/")
    except ValueError:
        rel = target_docs_path
    return rel


def compute_images_relative(current_file_dst: str) -> str:
    """Compute relative path from current file to docs/images/."""
    current = Path(current_file_dst)
    images_dir = Path("images")
    try:
        rel = os.path.relpath(images_dir, current.parent).replace("\\", "/")
    except ValueError:
        rel = "images"
    return rel


# ── Regex patterns ───────────────────────────────────────────────────────

# Image embed: ![[filename.ext]] or ![[filename.ext|size]]
RE_IMG_EMBED = re.compile(r'!\[\[([^|\]\n]+?)(?:\|(\d+))?\]\]')

# Wikilink with alias: [[target|alias]]
RE_WIKILINK_ALIAS = re.compile(r'\[\[([^|\]\n]+?)\|([^\]\n]+?)\]\]')

# Wikilink simple: [[target]]
RE_WIKILINK_SIMPLE = re.compile(r'\[\[([^\]\n]+?)\]\]')

# Obsidian callout: > [!type] optional title  or  > [!type]-  (collapsible, closed)
# Also handles > [!type]+  (collapsible, open) though less common
RE_CALLOUT_START = re.compile(r'^(\s*)> \[!([^\]]+?)\]([+-])?\s*(.*)?$')

# Obsidian highlight ==text==
# Note: pymdownx.mark handles this natively, but we need it enabled in mkdocs.yml
# So actually we do NOT need to convert this — the mark extension supports == natively.
# We'll leave them as-is since we enabled pymdownx.mark.

# Frontmatter
RE_FRONTMATTER = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)


def convert_image_embeds(line: str, img_rel: str) -> str:
    """Replace ![[image.ext]] with ![image](relative/path/image.ext)."""
    def replacer(m: re.Match) -> str:
        filename = m.group(1).strip()
        alt = Path(filename).stem
        # URL-encode spaces
        encoded = filename.replace(" ", "%20")
        return f"![{alt}]({img_rel}/{encoded})"
    return RE_IMG_EMBED.sub(replacer, line)


def convert_wikilinks(line: str, current_dst: str) -> str:
    """Replace [[wikilinks]] with standard markdown links."""

    def replace_alias(m: re.Match) -> str:
        target = m.group(1).strip()
        alias = m.group(2).strip()

        # Heading-only: [[#Heading|Alias]]
        if target.startswith("#"):
            anchor = heading_anchor(target[1:])
            return f"[{alias}](#{anchor})"

        # Page#heading
        heading = ""
        if "#" in target:
            target, heading = target.rsplit("#", 1)
            heading = "#" + heading_anchor(heading)

        resolved = resolve_wikilink(target, current_dst)
        if resolved:
            rel = make_relative(resolved, current_dst)
            return f"[{alias}]({rel}{heading})"
        # Fallback: keep as text
        return f"[{alias}]({target.replace(' ', '%20')}.md{heading})"

    def replace_simple(m: re.Match) -> str:
        target = m.group(1).strip()

        # Heading-only: [[#Heading]]
        if target.startswith("#"):
            anchor = heading_anchor(target[1:])
            text = target[1:]
            return f"[{text}](#{anchor})"

        # Page#heading
        heading = ""
        display = target
        if "#" in target:
            target, heading_text = target.rsplit("#", 1)
            heading = "#" + heading_anchor(heading_text)
            display = target if target else heading_text

        # Clean display: strip path prefix, show just page name
        display_clean = display.rsplit("/", 1)[-1] if "/" in display else display

        resolved = resolve_wikilink(target, current_dst)
        if resolved:
            rel = make_relative(resolved, current_dst)
            return f"[{display_clean}]({rel}{heading})"
        return f"[{display_clean}]({target.replace(' ', '%20')}.md{heading})"

    line = RE_WIKILINK_ALIAS.sub(replace_alias, line)
    line = RE_WIKILINK_SIMPLE.sub(replace_simple, line)
    return line


CALLOUT_TYPE_MAP = {
    "info": "info",
    "note": "note",
    "tip": "tip",
    "warning": "warning",
    "danger": "danger",
    "example": "example",
    "question": "question",
    "quote": "quote",
    "abstract": "abstract",
    "success": "success",
    "failure": "failure",
    "bug": "bug",
}


def normalize_callout_type(raw_type: str) -> tuple[str, str]:
    """Return (admonition_type, title) from a raw Obsidian callout type string."""
    raw = raw_type.strip()
    # Check for known types (case-insensitive)
    lower = raw.lower()
    for key in CALLOUT_TYPE_MAP:
        if lower.startswith(key):
            return CALLOUT_TYPE_MAP[key], raw
    # Emoji or custom callouts → map to "note" with the raw as title
    if raw.startswith("📝") or raw.startswith("🔍"):
        return "note", raw
    if lower.startswith("example"):
        return "example", raw
    # Default
    return "note", raw


def convert_callouts(lines: list[str]) -> list[str]:
    """Convert Obsidian callouts into MkDocs Material admonitions."""
    result: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = RE_CALLOUT_START.match(line)
        if m:
            indent = m.group(1) or ""
            raw_type = m.group(2)
            collapse_marker = m.group(3)  # + or - or None
            title_extra = (m.group(4) or "").strip()

            adm_type, fallback_title = normalize_callout_type(raw_type)
            title = title_extra if title_extra else fallback_title

            # Determine admonition keyword
            if collapse_marker == "-":
                keyword = "???"  # collapsed by default
            elif collapse_marker == "+":
                keyword = "???+"  # open by default
            else:
                keyword = "!!!"

            result.append(f'{indent}{keyword} {adm_type} "{title}"\n')

            # Collect continuation lines (> indented or blank)
            i += 1
            while i < len(lines):
                cline = lines[i]
                # Check if it's a continuation of the blockquote
                stripped = cline.rstrip("\n")
                if stripped.startswith(f"{indent}> ") or stripped == f"{indent}>" or stripped == f"{indent}>":
                    # Remove the leading "> " and add 4-space indent
                    content = stripped
                    # Remove leading indent + "> "
                    if content.startswith(f"{indent}> "):
                        content = content[len(indent) + 2:]
                    elif content.startswith(f"{indent}>"):
                        content = content[len(indent) + 1:]
                    result.append(f"{indent}    {content}\n")
                    i += 1
                elif stripped.strip() == "":
                    # Blank line might end the callout or be part of it
                    # Check if next line continues the blockquote
                    if i + 1 < len(lines) and (lines[i + 1].startswith(f"{indent}> ") or lines[i + 1].startswith(f"{indent}>")):
                        result.append(f"{indent}    \n")
                        i += 1
                    else:
                        break
                else:
                    break
            continue

        result.append(line)
        i += 1

    return result


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter (--- blocks) from content."""
    return RE_FRONTMATTER.sub("", content, count=1)


def convert_file(src: Path, dst: Path, dst_rel: str) -> None:
    """Read src, apply all conversions, write to dst."""
    content = src.read_text(encoding="utf-8")

    # Strip Obsidian frontmatter
    content = strip_frontmatter(content)

    # Split into lines for callout processing
    lines = content.splitlines(keepends=True)

    # Convert callouts first (multi-line)
    lines = convert_callouts(lines)

    # Compute relative path to images dir
    img_rel = compute_images_relative(dst_rel)

    # Line-by-line conversions
    converted: list[str] = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        # Track fenced code blocks to avoid converting inside them
        if stripped.startswith("```"):
            in_code_block = not in_code_block

        if not in_code_block:
            line = convert_image_embeds(line, img_rel)
            line = convert_wikilinks(line, dst_rel)

        converted.append(line)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("".join(converted), encoding="utf-8")


def main() -> None:
    print("Building page index...")
    pairs = build_page_index()
    print(f"  Found {len(pairs)} content files to convert.")
    print(f"  Page index has {len(page_index)} entries.")

    # Ensure docs dir
    DOCS_DIR.mkdir(exist_ok=True)

    # Copy images
    if IMAGES_SRC.exists():
        if IMAGES_DST.exists():
            shutil.rmtree(IMAGES_DST)
        shutil.copytree(IMAGES_SRC, IMAGES_DST)
        print(f"  Copied images/ → docs/images/")

    # Convert each file
    for src, dst in pairs:
        dst_rel = dst.relative_to(DOCS_DIR).as_posix()
        convert_file(src, dst, dst_rel)
        print(f"  ✓ {src.name} → docs/{dst_rel}")

    # Create index.md from README
    readme_src = REPO_ROOT / "README.md"
    if readme_src.exists():
        index_dst = DOCS_DIR / "index.md"
        index_rel = "index.md"
        convert_file(readme_src, index_dst, index_rel)
        print(f"  ✓ README.md → docs/index.md")

    print(f"\nDone! Converted {len(pairs) + 1} files into docs/")


if __name__ == "__main__":
    main()
