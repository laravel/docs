# Laravel Translations

Community Laravel documentation and translations, published with Astro Starlight.

All maintained Laravel versions and languages live together on `main`:

```text
site/src/content/docs/
├── en/13.x/       # English source documentation
└── pt-br/13.x/    # Brazilian Portuguese translations
```

Pages use `/<language>/<version>/<page>/`, for example
`/pt-br/13.x/installation/`. English content is shown with a translation notice
when a translated page is missing.

Submit contributions to `main` using a short-lived branch. Edit the appropriate
language and Laravel major version folder. Do not submit changes to a separate
language or version branch.

See [the site guide](site/README.md) for development, deployment, adding languages
and versions, and tracking translation updates. This is an independent community
project; the official Laravel documentation is at https://laravel.com/docs.
