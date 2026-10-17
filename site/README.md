# Laravel Translations website

Astro + Starlight site for community Laravel documentation and future translations.
The original English Markdown stays in the repository root. No documentation has
been translated.

## Local development

Use Node.js 22.12 or newer. From the repository root:

```sh
npm ci --prefix site
npm run dev --prefix site
```

Open the displayed URL. The homepage redirects to `/en/`.

```sh
npm run build --prefix site
npm run preview --prefix site
```

Every dev/build run imports the root Markdown into `site/src/content/docs/en/`
and derives the sidebar from `documentation.md`. Generated files are ignored.
Edit the original Markdown, not the generated copies. The importer adjusts
Laravel links, named anchors, and alert labels for this standalone site.

## Deploy to Vercel

1. Import the GitHub repository `MathHRM/docs` at https://vercel.com/new.
2. Keep **Root Directory** at the repository root (`./`), not `site`.
   The importer needs access to the original Markdown in the repository root.
3. Use **Framework Preset: Other** and **Node.js: 22.x** (or newer supported LTS).
4. The root `vercel.json` defines installation, build, output and homepage redirect.
5. Deploy the `13.x` branch and select it as the Production Branch if necessary.

No application secrets or database are required. Vercel supplies the production
hostname for sitemap generation. Set `SITE_URL` to the full canonical origin
(e.g. `https://docs.example.com`) when adding a custom domain.

## Future translations

English routes use `/en/`. Add future locale entries to `astro.config.mjs` and
place translated Markdown in `src/content/docs/<locale>/`. The importer only
replaces the generated `en` folder, preserving other languages. Update sidebar
labels/translations when enabling a locale. No untranslated locale is advertised.
