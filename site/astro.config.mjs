import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sidebar from './src/sidebar.generated.json' with { type: 'json' };

export default defineConfig({
  site: process.env.SITE_URL || (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : undefined),
  integrations: [starlight({
    title: 'Laravel Translations',
    description: 'Community documentation and translations for Laravel.',
    locales: {
      en: { label: 'English', lang: 'en' },
      'pt-br': { label: 'Português (Brasil)', lang: 'pt-BR' },
    },
    defaultLocale: 'en',
    components: { LanguageSelect: './src/components/LanguageSelect.astro' },
    sidebar,
    expressiveCode: { shiki: { langAlias: { env: 'dotenv' } } },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/MathHRM/docs' }],
    customCss: ['./src/styles/custom.css'],
  })],
});
