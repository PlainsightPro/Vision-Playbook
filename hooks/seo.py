"""Search and answer-engine helpers for the playbook (MkDocs hook).

1. Page titles. The nav labels carry emoji and repeat across sections ("Naming Conventions"
   exists for Fabric, Power BI and Azure), and MkDocs uses them for <title>. This hook sets
   page.meta.title from the page's own H1 without emoji ("Fabric Naming Conventions"), which
   Material uses for <title> and overrides/main.html uses for Open Graph and JSON-LD.
   A page can still set its own `title:` in front matter.
2. llms.txt and llms-full.txt. After the build, writes an index of every page in the nav
   (title, URL, description) and one file with the full text of those pages, so AI assistants
   can read the playbook without crawling it page by page. See https://llmstxt.org.
"""
import posixpath
import re
from pathlib import Path

# Emoji and pictographs, plus the joiners and variation selectors that glue them together.
EMOJI_RANGES = [(0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2B00, 0x2BFF), (0x2300, 0x23FF)]
EMOJI = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in EMOJI_RANGES)
                   + chr(0xFE0F) + chr(0x200D) + chr(0x20E3) + "]+")
H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
MD_LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)\s]+?\.md)(#[^)\s]*)?\)")
ASSET_LINK = re.compile(r"\]\((?!https?://)([^)\s]+?\.(?:png|svg|jpe?g|gif|webp))\)", re.I)
# Technical guideline titles name their platform, so "Naming Conventions" for Power BI
# and for Fabric don't share a search result title.
PLATFORMS = {"fabric": "Microsoft Fabric", "databricks": "Databricks", "power-bi": "Power BI",
             "dbt": "dbt", "azure": "Azure"}

_pages = {}
_nav = None


def clean(text):
    return re.sub(r"\s+", " ", EMOJI.sub("", text)).strip()


def on_nav(nav, config, files):
    global _nav
    _nav = nav
    _pages.clear()


def on_page_markdown(markdown, page, config, files):
    # Use the H1 only when the page has exactly one; pages with several H1s (sections in
    # capitals, say) keep their nav label, without emoji.
    h1s = H1.findall(FENCE.sub("", COMMENT.sub("", markdown)))
    title = clean(h1s[0]) if len(h1s) == 1 else clean(page.title or "")
    parts = page.file.src_uri.split("/")
    platform = PLATFORMS.get(parts[1]) if len(parts) > 2 and parts[0] == "technical-guidelines" else None
    if title and platform and platform.split()[-1].lower() not in title.lower():
        title = f"{title} ({platform})"
    if title and "title" not in page.meta and not page.is_homepage:
        page.meta["title"] = title
    site = config["site_url"].rstrip("/") + "/"
    base = posixpath.dirname(page.file.src_uri)

    def abs_page(m):
        target = files.get_file_from_path(posixpath.normpath(posixpath.join(base, m.group(1))))
        if target is None:
            return m.group(0)
        return f"]({site}{target.url}{m.group(2) or ''})"

    def abs_asset(m):
        return f"]({site}{posixpath.normpath(posixpath.join(base, m.group(1)))})"

    text = COMMENT.sub("", markdown)
    text = MD_LINK.sub(abs_page, text)
    text = ASSET_LINK.sub(abs_asset, text)
    _pages[page.file.src_uri] = {
        "title": page.meta.get("title", title) or config["site_name"],
        "description": page.meta.get("description", ""),
        "url": site + page.url,
        "text": re.sub(r"\n{3,}", "\n\n", text).strip(),
    }
    return markdown


def _walk(items, depth, index, full):
    for item in items:
        if item.is_section:
            index.append(f"\n{'#' * min(depth + 2, 4)} {clean(item.title)}\n")
            _walk(item.children, depth + 1, index, full)
        elif item.is_page and item.file.src_uri in _pages:
            p = _pages[item.file.src_uri]
            line = f"- [{p['title']}]({p['url']})"
            index.append(line + (f": {p['description']}" if p["description"] else ""))
            full.append(f"Source: {p['url']}\n\n{p['text']}\n")


def on_post_build(config):
    if _nav is None:
        return
    site = config["site_url"].rstrip("/") + "/"
    index = [
        f"# {config['site_name']}",
        "",
        f"> {config['site_description'].strip()}",
        "",
        f"The full text of every page below is in {site}llms-full.txt. "
        "The company website is https://www.plainsight.pro.",
    ]
    full = []
    _walk(_nav.items, 0, index, full)
    out = Path(config["site_dir"])
    (out / "llms.txt").write_text("\n".join(index).replace("\n\n\n", "\n\n") + "\n", encoding="utf-8")
    header = f"# {config['site_name']}\n\n> {config['site_description'].strip()}\n\n"
    (out / "llms-full.txt").write_text(header + "\n---\n\n".join(full), encoding="utf-8")
