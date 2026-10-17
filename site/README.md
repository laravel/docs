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

The version dropdown beside the language dropdown is configured in
`src/versions.json`. Only Laravel 13.x is currently hosted. Set `current` to
the version served by this build and add entries with a `label`, `version`,
and `url` pointing to an existing version deployment or documentation site.
The current version uses `url: null` to keep the current page. Adding a menu
entry does not import or publish that version's documentation.

The header language selector switches between English (`/en/`) and Português
(Brasil) (`/pt-br/`), preserving the current page. English remains the default.
Until Portuguese pages are added, Starlight serves English fallback content with
a notice that the page has not been translated. No automatic translation runs.

Add Portuguese Markdown in `src/content/docs/pt-br/`, using the same filename as
the English page (for example, `installation.md`) and a `title` frontmatter.
The next build replaces the fallback for that page with the published translation.
The importer only replaces the generated `en` folder, preserving translations.
Add other locale entries to `astro.config.mjs` when supporting more languages.
