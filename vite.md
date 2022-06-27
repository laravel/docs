# Bundling Assets (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
  - [Installing Node](#installing-node)
  - [Installing Vite And The Laravel Plugin](#installing-vite-and-laravel-plugin)
  - [Configuring Vite](#configuring-vite)
  - [Loading Your Scripts And Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Server-Side Rendering (SSR)](#ssr)

<a name="introduction"></a>
## Introduction

[Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. For example, you will typically use Vite to bundle your application's Tailwind CSS and JavaScript files into production ready assets.

Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production.

> {tip} Are you running Laravel Mix? Vite has replaced Laravel Mix in new Laravel installations. For Mix documentation, please visit the [Laravel Mix](https://laravel-mix.com/) website. If you would like to switch to Vite, please see our [migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite).

<a name="vite-or-mix"></a>
#### Choosing Between Vite And Laravel Mix

Before transitioning to Vite, new Laravel applications utilized [Mix](https://laravel-mix.com/), which is powered by [webpack](https://webpack.js.org/), when bundling assets. Vite focuses on providing a faster and more productive experience when building rich JavaScript applications. If you are developing a Single Page Application (SPA), including those developed with tools like [Inertia](https://inertiajs.com), Vite will be the perfect fit.

Vite also works well with traditional server-side rendered applications with JavaScript "sprinkles", including those using [Livewire](https://laravel-livewire.com). However, it lacks some features that Laravel Mix supports, such as the ability to copy arbitrary assets into the build that are not referenced directly in your JavaScript application.

<a name="installation"></a>
## Installation & Setup

> {tip} The following documentation discusses how to manually install and configure the Laravel Vite plugin. However, Laravel's [starter kits](/docs/{{version}}/starter-kits) already include all of this scaffolding! Laravel's starter kits are the fastest way to get started with Laravel and Vite.

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
### Installing Vite And The Laravel Plugin

Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies by running:

```sh
npm install
```

<a name="configuring-vite"></a>
### Configuring Vite

Vite is configured in a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs and you may also install any other plugins your application requires, such as `@vitejs/plugin-vue` or `@vitejs/plugin-react`.

The Laravel Vite plugin requires you to specify any entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```

If you are building an SPA, including applications built using Inertia, Vite works best without CSS entry points:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

Instead, you should import your CSS via JavaScript. Typically, this would be done in your application's `resources/js/app.js` file:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

The Laravel plugin also supports multiple entry points and advanced configuration such as [SSR entry points](#ssr).

<a name="loading-your-scripts-and-styles"></a>
### Loading Your Scripts And Styles

With your Vite entry points configured, you only need reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

If you're importing your CSS via JavaScript then you only need to include the JavaScript entry point:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, it will load your compiled and versioned assets, including any imported CSS.

<a name="running-vite"></a>
## Running Vite

There are two ways you can run Vite. You may run the development server via the `dev` command, which is useful while developing locally. The development server will automatically detect changes to your files and instantly reflect them in any open browser windows.

Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production.

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```

<a name="working-with-scripts"></a>
## Working With JavaScript

<a name="aliases"></a>
### Aliases

The Laravel plugin provides a common alias to help you hit the ground running:

```js
{
    '@' => 'resources/js'
}
```

You may overwrite the `'@'` alias by adding your own to the `vite.config.js`:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': 'resources/ts',
        },
    },
});
```

<a name="vue"></a>
### Vue

There are a few additional options you will need to include when using the Vue plugin with the Laravel plugin:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
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
});
```

> {tip} Laravel's [starter kits](/docs/{{version}}/starter-kits) already include the proper Laravel, Vite, and Vue configuration. Check out [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia) for the fastest way to get started with Laravel, Vite, and Vue.

<a name="react"></a>
### React

When using Vite with React, you will need to ensure that any files containing JSX have the `.jsx` or `.tsx` extension, remembering to update your entry point, if required, as [shown above](#configuring-vite). You will also need to include the additional `@viteReactRefresh` directive alongside your existing `@vite` directive.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

The `@viteReactRefresh` directive must be called **before** the `@vite` directive.

> {tip} Laravel's [starter kits](/docs/{{version}}/starter-kits) already include the proper Laravel, Vite, and React configuration. Check out [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia) for the fastest way to get started with Laravel, Vite, and React.

<a name="inertia"></a>
### Inertia

The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React.

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/inertia-vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

> {tip} Laravel's [starter kits](/docs/{{version}}/starter-kits) already include the proper Laravel, Vite, and Inertia configuration. Check out [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia) for the fastest way to get started with Laravel, Vite, and Inertia.

<a name="url-processing"></a>
### URL Processing

When referencing assets in your application's HTML, CSS, or JS, there are a couple of things to consider. If you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory.

When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite.

Consider the following project structure:

```nothing
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

You can learn more about Vite's CSS support within the [Vite documentation](https://vitejs.dev/guide/features.html#css). If you are using PostCSS plugins, such as [Tailwind](https://tailwindcss.com), you may create a `postcss.config.js` file in the root of your project and Vite will automatically apply it:

```js
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

<a name="custom-base-urls"></a>
## Custom Base URLs

If your Vite compiled assets are deployed to a domain separate from your application such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file:

```env
ASSET_URL=https://cdn.example.com
```

After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value:

```nothing
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

The Laravel Vite plugin makes it painless to set up server-side rending with Vite. Create your SSR entry point, for example at `resources/js/ssr.js`, and specify the entry point by passing a configuration option to the Laravel plugin:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```

To ensure you don't forget to rebuild the SSR entry point, we recommend augmenting the "build" script in your application's `package.json` to create your SSR build:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

Then, to build and start the SSR server, you may run the following commands:

```sh
npm run build
node storage/ssr/ssr.js
```
