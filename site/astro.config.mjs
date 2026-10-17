import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sidebar from './src/sidebar.generated.json' with { type: 'json' };
import pages from './src/pages.generated.json' with { type: 'json' };
import locales from './src/locales.json' with { type: 'json' };
import { current } from './src/versions.json' with { type: 'json' };

const redirects = {};
for (const locale of Object.keys(locales)) {
  redirects[`/${locale}/`] = `/${locale}/${current}/`;
  // These routes predate versioned documentation and always refer to Laravel 13.x.
  for (const page of pages['13.x'] || []) {
    if (page) redirects[`/${locale}/${page}/`] = `/${locale}/13.x/${page}/`;
  }
}

export default defineConfig({
  trailingSlash: 'always',
  redirects,
  site: process.env.SITE_URL || (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : undefined),
  integrations: [starlight({
    title: 'Laravel Translations',
    description: 'Community documentation and translations for Laravel.',
    locales,
    defaultLocale: 'en',
    components: { LanguageSelect: './src/components/LanguageSelect.astro' },
    routeMiddleware: './src/routeData.ts',
    sidebar,
    expressiveCode: { shiki: { langAlias: { env: 'dotenv' } } },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/MathHRM/docs' }],
    customCss: ['./src/styles/custom.css'],
  })],
});
