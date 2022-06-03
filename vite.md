# Compiling Assets (Vite)

- [Introduction](#introduction)
  - [Choosing Between Vite and Laravel Mix](#vite-or-mix)
- [Installation & Setup](#installation)
  - [Installing Node](#installing-node)
  - [Installing Vite & The Laravel Plugin](#installing-vite-and-laravel-plugin)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  - [Entry Points](#entry-points)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Server-Side Rendering (SSR)](#ssr)

<a name="introduction"></a>
## Introduction

[Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production.

Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production.

<a name="vite-or-mix"></a>
### Choosing Between Vite and Laravel Mix

Vite focuses on building rich JavaScript applications. If you are developing a Single Page Application (SPA), including those developed with tools like InertiaJS, Vite will be the perfect fit.

Vite also works well with traditional Server-Side Rendered applications with JavaScript "sprinkles". It lacks some features that Laravel Mix supports, such as the ability to copy arbitrary assets into the build that are not referenced directly in your JavaScript application.

<a name="installation"></a>
## Installation & Setup

<a name="installing-node"></a>
### Installing Node

You must ensure that Node.js and NPM are installed before running Vite and the Laravel plugin:

```sh
node -v
npm -v
```

You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/{{version}}/sail), you may invoke Node and NPM through Sail:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Installing Vite & The Laravel Plugin

The only remaining step is to install your npm dependencies. Within a fresh installation of Laravel, you'll find a `package.json` file in the root of your directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install the dependencies by running:

```sh
npm install
```

<a name="running-vite"></a>
## Running Vite

There are two ways you can run Vite. You may run the development server, which is useful while developing locally. It will automatically detect changes to your files and instantly reflect them in any open browser windows.

On the other hand, running the build command will version and bundle your application's assets and get them ready for you to deploy to production.

```shell
# Run the Vite development server
npm run dev

# Build and version the assets for production
npm run build
```

<a name="working-with-scripts"></a>
## Working With JavaScript

<a name="entry-points"></a>
### Entry Points

Out of the box, the Laravel plugin will look for your entry point at `resources/js/app.js`, so with that file already in place with a fresh Laravel installation, the only thing you will need to do is add the `@vite` directive to the `<head>` of your application.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite
</head>
```

If you want to change the default entry point to your application, you should pass the path to the Laravel plugin in your `vite.config.js`. Entry points may be JavaScript, TypeScript, JSX, or TSX files.

```js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'

export default defineConfig({
    plugins: [
        laravel('resources/js/entry-point.js'),
    ],
})
```

The compiled entry point can then be loaded by specifying the same path in the `@vite` Blade directive...

```blade
@vite('resources/js/entry-point.js')
```

If you have multiple entry points, you can also pass an array of paths to the Laravel plugin:

```js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'

export default defineConfig({
    plugins: [
        laravel([
            'resources/js/app.js',
            'resources/js/admin.js',
        ]),
    ],
})
```

<a name="aliases"></a>
### Aliases

The Laravel plugin provides two common aliases to help you hit the ground running, with the Ziggy alias only being applied when installed.

```js
{
    '@' => 'resources/js',
    'ziggy' => 'vendor/tightenco/ziggy/dist/index.es.js',
}
```

You may overwrite the `'@'` alias by adding your own to the `vite.config.js`...

```js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'

export default defineConfig({
    plugins: [
        laravel('resources/ts/app.tsx'),
    ],
    resolve: {
        alias: {
            '@': 'resources/ts',
        },
    },
})
```

<a name="vue"></a>
### Vue

There are a few additional options you will need to include when using the Vue plugin with the Laravel plugin:

```js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        laravel(),
        vue({
            template: {
                transformAssetUrls: {
                    // The Vue plugin will re-write asset URLs, when referenced
                    // in Single File Components, to point to the Laravel web
                    // server. Setting this to `null` allows the Laravel plugin
                    // to instead re-write asset URLs to point to the Vite
                    // server instead.
                    base: null,

                    // The Vue plugin will parse absolute URLs and treat them
                    // as absolute paths to files on disk. Setting this to
                    // `false` will leave absolute URLs un-touched so they can
                    // reference assets in the public directly as expected.
                    includeAbsolute: false,
                },
            },
        }),
    ],
})
```

<a name="react"></a>
### React

When using Vite with React, you will need to ensure that any files containing JSX have the `.jsx` or `.tsx` extension, remembering to update your entry point, if required, as [shown above](#entry-points). You will also need to include the additional `@viteReactRefresh` directive alongside your existing `@vite` directive.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

The `@viteReactRefresh` directive must be called **before** the `@vite` directive.


<a name="url-processing"></a>
### URL Processing

When referencing assets in your application's HTML, CSS, or JS, there are a couple of things to consider. If you reference assets with an absolute path, Vite will not include the asset in the build. You should ensure that the image is available in your public directory.

When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite.

Consider the following project structure:

```
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

The following demonstrates how Vite will treat relative and absolute URLs:

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## Working With Stylesheets

When using Vite, it is recommended to import your stylesheets from within your JavaScript files:

```js
import '../css/app.css'
```

When you import the JavaScript using the `@vite` Blade directive, Laravel will automatically load any stylesheets referenced in those files for you.

Vite supports <a href="https://vitejs.dev/guide/features.html#postcss">PostCSS</a> without any additional plugins. You can learn more about Vite's CSS support on the [Vite docs](https://vitejs.dev/guide/features.html#css).

<a name="custom-base-urls"></a>
## Custom Base URLs

If your Vite compiled assets are deployed to a domain separate from your application, e.g. via a CDN, you must specify the `ASSET_URL` environment variable:

```env
ASSET_URL=https://cdn.example.com
```

After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value:

```
https://cdn.example.com/build/assets/app.9dce8d17.js
```

Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed.

<a name="environment-variables"></a>
## Environment Variables

You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your `.env` file:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

You may access injected environment variables via the `import.meta.env` object:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="ssr"></a>
## Server-Side Rendering (SSR)

The Laravel plugin makes it painless to set up Server-Side Rending with Vite. Create your SSR entry point at `resources/js/ssr.js`, and no additional configuration is required.

Then to build and start the SSR server, you may run the following commands:

```sh
npm run ssr:build
npm run ssr:serve
```

However, if you want to specify a different entry point, you may augment your `vite.config.js` to include the SSR and non-SSR entry points.

```js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
})
```
