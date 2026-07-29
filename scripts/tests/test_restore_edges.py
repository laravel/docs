#!/usr/bin/env python3
"""Checks that section boundaries survive a round trip through the model.

A model strips the blank lines a section ends with - they read as formatting,
not content - which shortened every translated section by two lines and failed
the line-count check on twelve files at once.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from translate_diff import restore_edges, split_sections


def main() -> int:
    failures = 0

    for page in sorted(Path(__file__).resolve().parents[2].glob('*.md')):
        if page.name in {'GLOSSARY.md', 'readme.md', 'license.md'}:
            continue

        sections = split_sections(page.read_text())

        # Reassemble the page as if every section had come back from the model
        # with its blank edges stripped.
        rebuilt = sections[0] + ''.join(
            restore_edges(section, section.strip('\n')) for section in sections[1:]
        )

        if rebuilt != page.read_text():
            print(f'  {page.name}: does not round-trip', file=sys.stderr)
            failures += 1

    print('round-trip failures:', failures)

    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
