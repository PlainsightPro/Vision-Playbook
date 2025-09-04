#!/usr/bin/env python3
import argparse
import os
import re
import zipfile
from datetime import datetime
from pathlib import Path

# ---- Rules distilled from your .gitignore + your earlier "Publish*" ask ----
EXCLUDED_DIR_NAMES = {
    ".obsidian", "images"
    ".vs", ".vscode", "bin", "obj", "build", "x64", "x86",
    "testresults", "generated files", "publish", ".git"
}
EXCLUDED_DIR_PREFIXES = ("publish",)

def dir_matches_pattern(dname_lower: str) -> bool:
    return (
        dname_lower.startswith("_resharper")
        or dname_lower.startswith("_ncrunch_")
    )

EXCLUDED_FILE_EXTS = {
    ".suo", ".user", ".userosscache", ".sln.docstates",
    ".ilk", ".meta", ".obj", ".iobj", ".pch", ".pdb", ".ipdb", ".pgc", ".pgd", ".rsp",
    ".mdf", ".ldf",
    ".coverage", ".coveragexml",
    ".cr.user",
    ".tlog", ".log",
    ".dbmdl", ".jfm", ".jfl", ".pfx",
    ".visualstate.xml",
    ".zip"
}
EXCLUDED_FILE_NAMES = {
    "thumbs.db", "ehthumbs.db", "desktop.ini",
    "testresult.xml", "QuickZip.py"
}
EXCLUDED_FILE_PATTERNS = [
    r"^nunit-.*\.xml$",
    r"^\..*crunch.*\.local\.xml$"
]

PACKAGES_RE = re.compile(r"/packages/", re.IGNORECASE)
PACKAGES_BUILD_RE = re.compile(r"/packages/.*/build/", re.IGNORECASE)

def is_in_packages(path_rel_fwd: str) -> bool:
    return PACKAGES_RE.search(path_rel_fwd) is not None

def is_in_packages_build(path_rel_fwd: str) -> bool:
    return PACKAGES_BUILD_RE.search(path_rel_fwd) is not None

def should_prune_dir(dir_name: str, rel_dir_fwd: str) -> bool:
    dlow = dir_name.lower()
    if dlow in EXCLUDED_DIR_NAMES:
        return True
    if any(dlow.startswith(pfx) for pfx in EXCLUDED_DIR_PREFIXES):
        return True
    if dir_matches_pattern(dlow):
        return True
    # allow walking through to find packages/**/build/**
    if "packages" in rel_dir_fwd.lower() and "build/" not in rel_dir_fwd.lower():
        return False
    return False

def file_is_excluded(root: Path, fpath: Path, out_zip: Path) -> bool:
    try:
        if fpath.resolve() == out_zip.resolve():
            return True
    except Exception:
        pass

    name_lower = fpath.name.lower()
    ext_lower = fpath.suffix.lower()

    if ext_lower in EXCLUDED_FILE_EXTS:
        return True
    if name_lower in EXCLUDED_FILE_NAMES:
        return True
    for pat in EXCLUDED_FILE_PATTERNS:
        if re.match(pat, name_lower, flags=re.IGNORECASE):
            return True

    try:
        rel_fwd = fpath.resolve().relative_to(root.resolve()).as_posix().lower()
    except Exception:
        return True

    if is_in_packages(rel_fwd) and not is_in_packages_build(rel_fwd):
        return True

    return False

def main():
    ap = argparse.ArgumentParser(description="Zip a folder while honoring a Visual Studio-style .gitignore.")
    ap.add_argument("root", nargs="?", default=".", help="Root folder to archive (default: current folder)")
    ap.add_argument("-o", "--out", default=None, help="Destination .zip path (default: inside the root folder)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Root folder does not exist or is not a directory: {root}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # CHANGED: write the ZIP one folder deeper (inside the root)
    out = Path(args.out).resolve() if args.out else root / f"{root.name}_{ts}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            rel_dir = Path(dirpath).resolve().relative_to(root).as_posix()
            if rel_dir == ".":
                rel_dir = ""

            pruned = []
            kept = []
            for d in list(dirnames):
                rel_child_fwd = f"{rel_dir}/{d}".strip("/")
                if should_prune_dir(d, rel_child_fwd):
                    pruned.append(d)
                else:
                    kept.append(d)

            rel_dir_lower = rel_dir.lower()
            if "packages" in rel_dir_lower and "build/" not in rel_dir_lower:
                kept = [d for d in kept if d.lower() == "build"]
                pruned = list(set(dirnames) - set(kept))

            dirnames[:] = kept

            for fname in filenames:
                fpath = Path(dirpath) / fname
                if file_is_excluded(root, fpath, out):
                    continue
                parts_lower = [p.lower() for p in fpath.resolve().relative_to(root).parts]
                if any(p in EXCLUDED_DIR_NAMES for p in parts_lower):
                    continue
                if any(p.startswith(EXCLUDED_DIR_PREFIXES) for p in parts_lower):
                    continue
                if any(dir_matches_pattern(p) for p in parts_lower):
                    continue

                arcname = fpath.resolve().relative_to(root).as_posix()
                zf.write(fpath, arcname)

    print(f"Created: {out}")

if __name__ == "__main__":
    main()
