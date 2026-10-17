import { readdir, readFile, mkdir, writeFile, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const site = fileURLToPath(new URL('../', import.meta.url));
const root = path.resolve(site, '..');
// Only this generated locale is replaced; future translations stay untouched.
const output = path.join(site, 'src/content/docs/en');
const files = (await readdir(root)).filter(file => file.endsWith('.md') && !['documentation.md', 'readme.md'].includes(file.toLowerCase()));
const slugs = new Set(files.map(file => file.slice(0, -3)));
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

function localLinks(content) {
  return content.replace(/\/docs\/\{\{version\}\}\/([\w-]+)(#[\w-]+)?/g, (match, slug, hash = '') =>
    slugs.has(slug) ? `/en/${slug}/${hash}` : `https://laravel.com/docs/13.x/${slug}${hash}`);
}

for (const file of files) {
  let content = await readFile(path.join(root, file), 'utf8');
  const heading = content.match(/^# (.+)\r?\n/);
  const title = heading?.[1] || file.slice(0, -3);
  if (heading) content = content.slice(heading[0].length).trimStart();
  content = localLinks(content);
  // Laravel uses named HTML anchors, including names that differ from heading slugs.
  content = content.replace(/<a name="([^"]+)"><\/a>/g, '<a id="$1"></a>');
  content = content.replace(/^> \[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]/gm, (_, kind) => `> **${kind[0]}${kind.slice(1).toLowerCase()}:**`);
  await writeFile(path.join(output, file), `---\ntitle: ${JSON.stringify(title)}\n---\n\n${content}`);
}

const sidebar = [];
const listed = new Set();
for (const line of (await readFile(path.join(root, 'documentation.md'), 'utf8')).split('\n')) {
  const group = line.match(/^- ## (.+)/);
  if (group) sidebar.push({ label: group[1].trim(), collapsed: true, items: [] });
  const item = line.match(/\[([^\]]+)\]\(\/docs\/\{\{version\}\}\/([\w-]+)\)/);
  if (item && slugs.has(item[2]) && sidebar.length) {
    sidebar.at(-1).items.push({ label: item[1], slug: item[2] });
    listed.add(item[2]);
  }
}
const unlisted = [...slugs].filter(slug => !listed.has(slug)).sort();
if (unlisted.length) sidebar.push({ label: 'More documentation', collapsed: true, items: unlisted.map(slug => ({ slug })) });
await writeFile(path.join(site, 'src/sidebar.generated.json'), JSON.stringify(sidebar.filter(group => group.items.length), null, 2) + '\n');
await writeFile(path.join(output, 'index.md'), `---
title: Laravel Translations
description: Community documentation and future translations for Laravel.
template: splash
hero:
  title: Laravel Translations
  tagline: Explore the Laravel documentation. Community translations are coming next.
  actions:
    - text: Read the documentation
      link: /en/installation/
      icon: right-arrow
    - text: View on GitHub
      link: https://github.com/MathHRM/docs
      icon: external
---

This community project hosts Laravel documentation and will receive translations in the future. The documentation is currently available in English.

This is an independent community project. For the official documentation, visit [laravel.com](https://laravel.com/docs).
`);
console.log(`Imported ${files.length} English documentation pages.`);
