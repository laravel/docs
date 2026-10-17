# Laravel Translations website

Astro + Starlight documentation. All maintained languages and Laravel major
versions live on `main`; feature and translation branches are temporary.

## Development

Use Node.js 22.12 or newer, from the repository root:

```sh
npm ci --prefix site
npm run dev --prefix site
npm run build --prefix site
npm run preview --prefix site
```

Edit tracked Markdown directly in `src/content/docs/<locale>/<version>/`.
The `sync` script validates content and generates the sidebar and page manifest;
it never replaces documentation or translations. Generated JSON is ignored.
`src/navigation/<version>.json` defines the sidebar groups and order; additional
pages are included under “More documentation”. Only the current version's
navigation and pagination are shown.

## URLs and selectors

Canonical URLs are `/<locale>/<version>/<page>/`, for example:

```text
/en/13.x/installation/
/pt-br/13.x/installation/
```

The language selector keeps the version and page. The version selector keeps
the language and page if the destination has it, otherwise it opens that
version's homepage. The site title opens the current language/version homepage.
Missing translations use Starlight's English fallback and translation notice.
Relative links such as `../configuration/` keep both language and version.

`/` and `/<locale>/` redirect to the configured current version. Old unversioned
article URLs redirect to their original Laravel 13.x page. Static builds emit
HTML redirects, which work on Vercel and the local preview server.

## Add a Laravel version

1. Import that version's actual English documentation into
   `src/content/docs/en/12.x/`, including `index.md`. Do not copy 13.x content
   and label it 12.x. Add Starlight `title` frontmatter and adjust links/anchors
   when importing upstream Markdown.
2. Add `src/navigation/12.x.json`, using `13.x.json` as a format reference.
   Slugs are relative to the version, e.g. `installation`.
3. Register the published version in `src/versions.json`:

   ```json
   {
     "current": "13.x",
     "versions": [
       { "label": "13.x", "version": "13.x" },
       { "label": "12.x", "version": "12.x" }
     ]
   }
   ```

4. Run the build. It rejects registered versions without an English homepage,
   unregistered content versions, and translations without an English source.

`current` chooses the landing version; the selector reads the URL to identify
the version being viewed. It is not inferred from GitHub releases. Git tags such
as `site-v1.0.0` may mark a website release containing multiple Laravel versions.

## Add translations and languages

For Portuguese, add Markdown to `src/content/docs/pt-br/13.x/` with the same
filename as the English source and a `title` frontmatter. For another language,
register it in `src/locales.json`, then add its translated files. Untranslated
pages fall back to English within the same Laravel version.

Optionally record the English source's last-changing commit in each translation:

```yaml
---
title: Instalação
translationSourceCommit: <full English source commit SHA>
---
```

Find that commit with `git log -1 --format=%H --
site/src/content/docs/en/13.x/installation.md`. Compare the English file against
that commit when reviewing translation updates. This metadata is a manual
tracking convention; it does not automatically flag stale translations.

## Deploy to Vercel

Import `MathHRM/docs`, Root Directory `./`, Framework Preset Other, Node.js 22.x
or newer supported LTS. Set the Production Branch to `main` in Vercel's project
Git settings. The root `vercel.json` defines install, build, and output paths.

No database or application secrets are required. Vercel supplies the production
hostname for sitemap generation. Set `SITE_URL` when adding a custom domain.
Changing the GitHub default branch does not configure an existing Vercel project;
its Production Branch must also be updated.
