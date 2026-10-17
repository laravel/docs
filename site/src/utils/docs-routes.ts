import { current, versions } from '../versions.json';
import pages from '../pages.generated.json';
import locales from '../locales.json';

const available = pages as Record<string, string[]>;

export function routeParts(pathname: string) {
  const segments = pathname.split('/').filter(Boolean);
  const locale = segments[0] && segments[0] in locales ? segments.shift()! : 'en';
  const [candidate, ...rest] = segments;
  const version = versions.some(item => item.version === candidate) ? candidate! : current;
  return { locale, version, page: candidate === version ? rest.join('/') : '' };
}

export function docsPath(locale: string, version: string, page = '') {
  // Missing pages lead to the chosen version's homepage, never a different version's content.
  const target = available[version]?.includes(page) ? page : '';
  return `/${locale}/${version}/${target ? `${target}/` : ''}`;
}
