#!/usr/bin/env python3
"""Bring translated pages up to date with an upstream diff.

Only the sections the diff touches are sent to the model, never whole files.
Documentation pages run to four thousand lines while a typical upstream commit
changes twenty, and output tokens cost five times what input does - sending
`strings.md` back in full to retitle one method would cost more than the entire
rest of the run. Untouched sections are copied through byte for byte, so the
model cannot damage what it never saw.

The result is checked by validate_translation.py before it is written.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import subprocess
import sys
from pathlib import Path

from validate_translation import problems

# Imported inside main(): the section-splitting logic below is the part worth
# testing, and it should not need the SDK installed to run.

MODEL = 'claude-sonnet-4-5'

# Sections start at an anchor; everything before the first one is the preamble
# (header, title, contents list) and travels as its own unit.
SECTION = re.compile(r'(?=^<a\s+name="[^"]+"></a>$)', re.MULTILINE)

SYSTEM = """\
Ти перекладаєш документацію Laravel англійською на українську для
laravelukraine.com.

Тобі дають фрагмент чинного українського перекладу і diff відповідного
фрагмента англійського оригіналу. Твоє завдання - оновити український текст
так, щоб він відповідав новому англійському, змінивши рівно те, що змінилось.

Правила:
- Не чіпай нічого, крім того, що змінює diff. Решту речень повертай дослівно.
- Зберігай розмітку точно: кількість рядків, порожні рядки, відступи,
  блоки коду, атрибути на кшталт {.collection-method}.
- Не перекладай код, назви класів, методів, змінних, ключі конфігурації.
- Якорі <a name="..."></a> лишаються англійською незмінними.
- Посилання виду /docs/{{version}}/... не змінюй.
- Дотримуйся глосарія, наведеного нижче.
- Тире - звичайний дефіс, не довге тире.

Повертай ТІЛЬКИ оновлений український текст фрагмента, без пояснень і без
огорнення у блок коду.\
"""


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True,
                          check=True).stdout


def split_sections(text: str) -> list[str]:
    return SECTION.split(text)


def anchor_of(section: str) -> str | None:
    match = re.match(r'^<a\s+name="([^"]+)"></a>', section)

    return match.group(1) if match else None


def changed_anchors(base: str, head: str, path: str) -> set[str]:
    """Which sections of a file the diff touches.

    Hunk headers carry the enclosing context, but not reliably enough to trust,
    so line numbers are mapped onto the section boundaries of the new file.
    """
    new_text = git('show', f'{head}:{path}')
    sections = split_sections(new_text)

    # Line number where each section starts, 1-based.
    bounds: list[tuple[int, int, str | None]] = []
    line = 1

    for section in sections:
        length = len(section.splitlines())
        bounds.append((line, line + length - 1, anchor_of(section)))
        line += length

    touched: set[str] = set()
    diff = git('diff', '-U0', base, head, '--', path)

    for header in re.finditer(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', diff, re.MULTILINE):
        start = int(header.group(1))
        count = int(header.group(2) or 1)
        end = start + max(count - 1, 0)

        for low, high, anchor in bounds:
            if start <= high and end >= low:
                # None marks the preamble, which has no anchor of its own.
                touched.add(anchor or '')

    return touched


def translate(client, glossary: str,
              current: str, diff: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=[
            {'type': 'text', 'text': SYSTEM},
            # Cached so a run that makes several calls pays for the glossary
            # once. Across runs the cache has expired, which is why nothing
            # else here is marked: writing a cache entry costs more than a
            # plain read when it is never read back.
            {'type': 'text', 'text': f'Глосарій:\n\n{glossary}',
             'cache_control': {'type': 'ephemeral'}},
        ],
        messages=[{
            'role': 'user',
            'content': (f'Чинний український переклад фрагмента:\n\n{current}\n\n'
                        f'Diff англійського оригіналу цього фрагмента:\n\n{diff}'),
        }],
    )

    return message.content[0].text


def section_diff(base: str, head: str, path: str, anchor: str) -> str:
    """The diff limited to one section, for context in the prompt."""
    def find(commit: str) -> str:
        for section in split_sections(git('show', f'{commit}:{path}')):
            if (anchor_of(section) or '') == anchor:
                return section

        return ''

    before, after = find(base), find(head)

    if before == after:
        return ''

    return ''.join(difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile='before', tofile='after', n=3,
    ))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--base', required=True, help='commit we translated from')
    parser.add_argument('--head', required=True, help='commit to catch up to')
    args = parser.parse_args()

    if not os.environ.get('ANTHROPIC_API_KEY'):
        print('ANTHROPIC_API_KEY is not set', file=sys.stderr)
        return 1

    import anthropic

    # The header stores the full hash, and callers pass whatever git gave them
    # - an abbreviated one would be written straight through and quietly fail
    # the header check on the next run.
    base = git('rev-parse', args.base).strip()
    head = git('rev-parse', args.head).strip()

    client = anthropic.Anthropic()
    glossary = Path('GLOSSARY.md').read_text()
    failed = False

    for name in args.files:
        path = Path(name)

        if not path.exists():
            print(f'{name}: not translated yet - skipping', file=sys.stderr)
            continue

        touched = changed_anchors(base, head, name)

        if not touched:
            continue

        sections = split_sections(path.read_text())
        rebuilt: list[str] = []

        for section in sections:
            anchor = anchor_of(section) or ''

            if anchor not in touched:
                rebuilt.append(section)
                continue

            diff = section_diff(base, head, name, anchor)

            if not diff:
                rebuilt.append(section)
                continue

            rebuilt.append(translate(client, glossary, section, diff))

        updated = ''.join(rebuilt)

        # The header records what the file is now in step with.
        updated = re.sub(r'^git: [0-9a-f]{40}$', f'git: {head}',
                         updated, count=1, flags=re.MULTILINE)

        # Checked before writing, against the upstream file it now claims to
        # match. A dropped anchor breaks the sidebar and every deep link into
        # the page, and reads as an ordinary wording change in review - the
        # kind of thing a person skims past, so it must not reach the branch.
        found = problems(git('show', f'{head}:{name}'), updated)

        if found:
            print(f'{name}: rejected', file=sys.stderr)

            for problem in found:
                print(f'  - {problem}', file=sys.stderr)

            failed = True
            continue

        path.write_text(updated)
        print(f'{name}: {len(touched)} sections')

    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
