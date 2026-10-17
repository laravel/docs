import { readdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const site = fileURLToPath(new URL('../', import.meta.url));
const readJSON = async file => JSON.parse(await readFile(path.join(site, file), 'utf8'));
const { current, versions } = await readJSON('src/versions.json');
const locales = await readJSON('src/locales.json');
if (!versions.some(item => item.version === current)) throw new Error('Current version must be published.');
const ids = versions.map(item => item.version);
if (new Set(ids).size !== ids.length || ids.some(id => !/^\d+\.x$/.test(id))) {
  throw new Error('Versions must be unique major versions, e.g. 13.x.');
}

async function pagesIn(directory, prefix = '') {
  const entries = await readdir(directory, { withFileTypes: true });
  const pages = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const relative = `${prefix}${entry.name}`;
    if (entry.isDirectory()) pages.push(...await pagesIn(path.join(directory, entry.name), `${relative}/`));
    else if (/\.mdx?$/.test(entry.name)) pages.push(relative.replace(/\.mdx?$/, '').replace(/(^|\/)index$/, ''));
  }
  return pages;
}

const pages = {};
const sidebar = [];
for (const { version, label } of versions) {
  const slugs = await pagesIn(path.join(site, 'src/content/docs/en', version));
  if (!slugs.includes('')) throw new Error(`${version} needs an English index.md.`);
  pages[version] = slugs.sort();
  const groups = await readJSON(`src/navigation/${version}.json`);
  const listed = new Set();
  const items = groups.map(group => ({
    ...group,
    items: group.items.filter(item => slugs.includes(item.slug)).map(item => {
      listed.add(item.slug);
      return { ...item, slug: `${version}/${item.slug}` };
    }),
  })).filter(group => group.items.length);
  const unlisted = slugs.filter(slug => slug && !listed.has(slug));
  if (unlisted.length) items.push({ label: 'More documentation', collapsed: true, items: unlisted.map(slug => ({ slug: `${version}/${slug}` })) });
  sidebar.push({ label, items });
}

// English is the source for fallback pages. Reject unregistered versions and orphan translations.
for (const locale of Object.keys(locales)) {
  const directory = path.join(site, 'src/content/docs', locale);
  let entries;
  try { entries = await readdir(directory, { withFileTypes: true }); }
  catch (error) { if (error.code === 'ENOENT') continue; throw error; }
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (!entry.isDirectory() || !pages[entry.name]) throw new Error(`Unregistered content: ${locale}/${entry.name}`);
    for (const slug of await pagesIn(path.join(directory, entry.name))) {
      if (!pages[entry.name].includes(slug)) throw new Error(`Translation has no English source: ${locale}/${entry.name}/${slug}`);
    }
  }
}
await writeFile(path.join(site, 'src/sidebar.generated.json'), JSON.stringify(sidebar, null, 2) + '\n');
await writeFile(path.join(site, 'src/pages.generated.json'), JSON.stringify(pages, null, 2) + '\n');
console.log(`Prepared ${versions.length} documentation version(s).`);
