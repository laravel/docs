#!/usr/bin/env python3
"""Check a translated page against the English original it came from.

The translation has to match the upstream file structurally, line for line: the
site renders both from the same Markdown, the sidebar is built from the anchor
names, and the deep links in seeders and articles point at those anchors. A
model that drops an anchor or merges two code blocks produces a page that looks
fine in a diff and is broken on the site.

Exits non-zero on any mismatch, so a workflow can refuse to open the pull
request rather than asking a person to catch it in review.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ANCHOR = re.compile(r'<a\s+name="([^"]+)"\s*></a>')
FENCE = re.compile(r'^```', re.MULTILINE)
VERSION_LINK = re.compile(r'/docs/\{\{version\}\}/[a-z0-9-]+(?:#[a-z0-9-]+)?')
HEADER = re.compile(r'\A---\ngit: [0-9a-f]{40}\n---\n')

# Terms that stay in English. Checked only inside prose - a heading or a link
# target may legitimately differ.
KEEP_ENGLISH = ('middleware',)


def problems(original: str, translated: str) -> list[str]:
    found: list[str] = []

    if not HEADER.match(translated):
        found.append('missing or malformed `git:` header')

    # Line parity: the upstream file plus our three header lines. Anything else
    # means content was dropped or invented.
    expected = len(original.splitlines()) + 3
    actual = len(translated.splitlines())

    if actual != expected:
        found.append(f'line count {actual}, expected {expected} '
                     f'({actual - expected:+d})')

    src_anchors = ANCHOR.findall(original)
    out_anchors = ANCHOR.findall(translated)

    if src_anchors != out_anchors:
        missing = set(src_anchors) - set(out_anchors)
        added = set(out_anchors) - set(src_anchors)

        if missing:
            found.append(f'anchors dropped: {", ".join(sorted(missing))}')
        if added:
            found.append(f'anchors invented: {", ".join(sorted(added))}')
        if not missing and not added:
            found.append('anchors reordered')

    src_fences = len(FENCE.findall(original))
    out_fences = len(FENCE.findall(translated))

    if src_fences != out_fences:
        found.append(f'{out_fences} code fences, expected {src_fences}')

    # Every anchor referenced from the page's own contents list has to exist,
    # or the sidebar and the in-page table of contents link into nothing.
    targets = {t.split('#')[1] for t in VERSION_LINK.findall(translated) if '#' in t}
    dangling = {t for t in targets if t not in out_anchors}

    # Cross-page links point at other files; only same-page ones are checkable.
    same_page = {t for t in dangling if t in set(src_anchors)}

    if same_page:
        found.append(f'links to anchors it does not define: {", ".join(sorted(same_page))}')

    for term in KEEP_ENGLISH:
        if term in original.lower() and term not in translated.lower():
            found.append(f'`{term}` should stay untranslated but is absent')

    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('original', help='the English file from upstream')
    parser.add_argument('translated', help='the Ukrainian file to check')
    args = parser.parse_args()

    found = problems(
        Path(args.original).read_text(),
        Path(args.translated).read_text(),
    )

    if not found:
        print(f'{args.translated}: ok')
        return 0

    print(f'{args.translated}:', file=sys.stderr)

    for problem in found:
        print(f'  - {problem}', file=sys.stderr)

    return 1


if __name__ == '__main__':
    raise SystemExit(main())
