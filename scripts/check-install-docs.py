#!/usr/bin/env python3
"""Check that README.md's install code matches apps/web/lib/install-snippets.ts.

The page and the agent prompt import those snippets, so they can't drift.
README is markdown and can't import, so it gets checked instead.

    python3 scripts/check-install-docs.py

Exits non-zero and prints a diff when they disagree.
"""

import difflib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPETS = os.path.join(REPO, "apps", "web", "lib", "install-snippets.ts")
README = os.path.join(REPO, "README.md")


def snippet(name):
    """Pull an exported template literal out of the TS module."""
    src = open(SNIPPETS).read()
    match = re.search(rf"export const {name} = `(.*?)`;\n", src, re.DOTALL)
    if not match:
        raise SystemExit(f"no export named {name} in {SNIPPETS}")
    body = match.group(1)
    # Undo the escaping the TS template literal needs.
    return body.replace("\\`", "`").replace("\\$", "$")


def fenced_blocks(lang):
    src = open(README).read()
    return [b.strip("\n") for b in re.findall(rf"```{lang}\n(.*?)```", src, re.DOTALL)]


def check(name, lang, must_contain):
    want = snippet(name)
    blocks = [b for b in fenced_blocks(lang) if must_contain in b]
    if not blocks:
        print(f"FAIL {name}: no ```{lang} block in README.md containing {must_contain!r}")
        return False
    if any(b == want for b in blocks):
        print(f"ok   {name}")
        return True
    print(f"FAIL {name}: README.md differs from install-snippets.ts")
    for line in difflib.unified_diff(
        blocks[0].splitlines(), want.splitlines(),
        fromfile="README.md", tofile=f"install-snippets.ts:{name}", lineterm="",
    ):
        print("  " + line)
    return False


ok = all([
    check("layoutSnippet", "tsx", "localFont"),
    check("themeSnippet", "css", "@theme inline"),
])

if not ok:
    print("\nREADME.md is out of sync. Copy the snippet above into it.")
sys.exit(0 if ok else 1)
