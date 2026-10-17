import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { docsPath, routeParts } from './utils/docs-routes';
import { versions } from './versions.json';

export const onRequest = defineRouteMiddleware(({ locals, url }) => {
  const route = locals.starlightRoute;
  const { locale, version } = routeParts(url.pathname);
  const label = versions.find(item => item.version === version)?.label;
  const selected = route.sidebar.find(item => item.type === 'group' && item.label === label);
  route.sidebar = selected?.type === 'group' ? selected.entries : [];
  route.siteTitleHref = docsPath(locale, version);
  // Starlight computes pagination before this filter; prevent links across versions.
  for (const direction of ['prev', 'next'] as const) {
    const link = route.pagination[direction];
    if (link && !link.href.startsWith(`/${locale}/${version}/`)) route.pagination[direction] = undefined;
  }
});
