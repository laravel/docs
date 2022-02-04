# Compiling Assets (Mix)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
- [Running Mix](#running-mix)
- [Working With Stylesheets](#working-with-stylesheets)
    - [Tailwind CSS](#tailwindcss)
    - [PostCSS](#postcss)
    - [Sass](#sass)
    - [URL Processing](#url-processing)
    - [Source Maps](#css-source-maps)
- [Working With JavaScript](#working-with-scripts)
    - [Vue](#vue)
    - [React](#react)
    - [Vendor Extraction](#vendor-extraction)
    - [Custom Webpack Configuration](#custom-webpack-configuration)
- [Versioning / Cache Busting](#versioning-and-cache-busting)
- [Browsersync Reloading](#browsersync-reloading)
- [Environment Variables](#environment-variables)
- [Notifications](#notifications)

<a name="introduction"></a>
## Introduction

[Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors.

In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example:

    mix.js('resources/js/app.js', 'public/js')
        .postCss('resources/css/app.css', 'public/css');

If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all.

> {tip} If you need a head start building your application with Laravel and [Tailwind CSS](https://tailwindcss.com), check out one of our [application starter kits](/docs/{{version}}/starter-kits).

<a name="installation"></a>
## Installation & Setup

<a name="installing-node"></a>
#### Installing Node

Before running Mix, you must first ensure that Node.js and NPM are installed on your machine:

    node -v
    npm -v

You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](/docs/{{version}}/sail), you may invoke Node and NPM through Sail:

    ./sail node -v
    ./sail npm -v

<a name="installing-laravel-mix"></a>
#### Installing Laravel Mix

The only remaining step is to install Laravel Mix. Within a fresh installation of Laravel, you'll find a `package.json` file in the root of your directory structure. The default `package.json` file already includes everything you need to get started using Laravel Mix. Think of this file like your `composer.json` file, except it defines Node dependencies instead of PHP dependencies. You may install the dependencies it references by running:

    npm install

<a name="running-mix"></a>
## Running Mix

Mix is a configuration layer on top of [webpack](https://webpack.js.org), so to run your Mix tasks you only need to execute one of the NPM scripts that are included in the default Laravel `package.json` file. When you run the `dev` or `production` scripts, all of your application's CSS and JavaScript assets will be compiled and placed in your application's `public` directory:

    // Run all Mix tasks...
    npm run dev

    // Run all Mix tasks and minify output...
    npm run prod

<a name="watching-assets-for-changes"></a>
#### Watching Assets For Changes

The `npm run watch` command will continue running in your terminal and watch all relevant CSS and JavaScript files for changes. Webpack will automatically recompile your assets when it detects a change to one of these files:

    npm run watch

Webpack may not be able to detect your file changes in certain local development environments. If this is the case on your system, consider using the `watch-poll` command:

    npm run watch-poll

<a name="working-with-stylesheets"></a>
## Working With Stylesheets

Your application's `webpack.mix.js` file is your entry point for all asset compilation. Think of it as a light configuration wrapper around [webpack](https://webpack.js.org). Mix tasks can be chained together to define exactly how your assets should be compiled.

<a name="tailwindcss"></a>
### Tailwind CSS

[Tailwind CSS](https://tailwindcss.com) is a modern, utility-first framework for building amazing sites without ever leaving your HTML. Let's dig into how to start using it in a Laravel project with Laravel Mix. First, we should install Tailwind using NPM and generate our Tailwind configuration file:

    npm install

    npm install -D tailwindcss

    npx tailwindcss init

The `init` command will generate a `tailwind.config.js` file. The `content` section of this file allows you to configure the paths to all of your HTML templates, JavaScript components, and any other source files that contain Tailwind class names so that any CSS classes that are not used within these files will be purged from your production CSS build:

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

Next, you should add each of Tailwind's "layers" to your application's `resources/css/app.css` file:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Once you have configured Tailwind's layers, you are ready to update your application's `webpack.mix.js` file to compile your Tailwind powered CSS:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

Finally, you should reference your stylesheet in your application's primary layout template. Many applications choose to store this template at `resources/views/layouts/app.blade.php`. In addition, ensure you add the responsive viewport `meta` tag if it's not already present:

```html
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="/css/app.css" rel="stylesheet">
</head>
```

<a name="postcss"></a>
### PostCSS

[PostCSS](https://postcss.org/), a powerful tool for transforming your CSS, is included with Laravel Mix out of the box. By default, Mix leverages the popular [Autoprefixer](https://github.com/postcss/autoprefixer) plugin to automatically apply all necessary CSS3 vendor prefixes. However, you're free to add any additional plugins that are appropriate for your application.

First, install the desired plugin through NPM and include it in your array of plugins when calling Mix's `postCss` method. The `postCss` method accepts the path to your CSS file as its first argument and the directory where the compiled file should be placed as its second argument:

    mix.postCss('resources/css/app.css', 'public/css', [
        require('postcss-custom-properties')
    ]);

Or, you may execute `postCss` with no additional plugins in order to achieve simple CSS compilation and minification:

    mix.postCss('resources/css/app.css', 'public/css');

<a name="sass"></a>
### Sass

The `sass` method allows you to compile [Sass](https://sass-lang.com/) into CSS that can be understood by web browsers. The `sass` method accepts the path to your Sass file as its first argument and the directory where the compiled file should be placed as its second argument:

    mix.sass('resources/sass/app.scss', 'public/css');

You may compile multiple Sass files into their own respective CSS files and even customize the output directory of the resulting CSS by calling the `sass` method multiple times:

    mix.sass('resources/sass/app.sass', 'public/css')
        .sass('resources/sass/admin.sass', 'public/css/admin');

<a name="url-processing"></a>
### URL Processing

Because Laravel Mix is built on top of webpack, it's important to understand a few webpack concepts. For CSS compilation, webpack will rewrite and optimize any `url()` calls within your stylesheets. While this might initially sound strange, it's an incredibly powerful piece of functionality. Imagine that we want to compile Sass that includes a relative URL to an image:

    .example {
        background: url('../images/example.png');
    }

> {note} Absolute paths for any given `url()` will be excluded from URL-rewriting. For example, `url('/images/thing.png')` or `url('http://example.com/images/thing.png')` won't be modified.

By default, Laravel Mix and webpack will find `example.png`, copy it to your `public/images` folder, and then rewrite the `url()` within your generated stylesheet. As such, your compiled CSS will be:

    .example {
        background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
    }

As useful as this feature may be, your existing folder structure may already be configured in a way you like. If this is the case, you may disable `url()` rewriting like so:

    mix.sass('resources/sass/app.scss', 'public/css').options({
        processCssUrls: false
    });

With this addition to your `webpack.mix.js` file, Mix will no longer match any `url()` or copy assets to your public directory. In other words, the compiled CSS will look just like how you originally typed it:

    .example {
        background: url("../images/thing.png");
    }

<a name="css-source-maps"></a>
### Source Maps

Though disabled by default, source maps may be activated by calling the `mix.sourceMaps()` method in your `webpack.mix.js` file. Though it comes with a compile/performance cost, this will provide extra debugging information to your browser's developer tools when using compiled assets:

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps();

<a name="style-of-source-mapping"></a>
#### Style Of Source Mapping

Webpack offers a variety of [source mapping styles](https://webpack.js.org/configuration/devtool/#devtool). By default, Mix's source mapping style is set to `eval-source-map`, which provides a fast rebuild time. If you want to change the mapping style, you may do so using the `sourceMaps` method:

    let productionSourceMaps = false;

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps(productionSourceMaps, 'source-map');

<a name="working-with-scripts"></a>
## Working With JavaScript

Mix provides several features to help you work with your JavaScript files, such as compiling modern ECMAScript, module bundling, minification, and concatenating plain JavaScript files. Even better, this all works seamlessly, without requiring an ounce of custom configuration:

    mix.js('resources/js/app.js', 'public/js');

With this single line of code, you may now take advantage of:

<div class="content-list" markdown="1">

- The latest EcmaScript syntax.
- Modules
- Minification for production environments.

</div>

<a name="vue"></a>
### Vue

Mix will automatically install the Babel plugins necessary for Vue single-file component compilation support when using the `vue` method. No further configuration is required:

    mix.js('resources/js/app.js', 'public/js')
       .vue();

Once your JavaScript has been compiled, you can reference it in your application:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="react"></a>
### React

Mix can automatically install the Babel plugins necessary for React support. To get started, add a call to the `react` method:

    mix.js('resources/js/app.jsx', 'public/js')
       .react();

Behind the scenes, Mix will download and include the appropriate `babel-preset-react` Babel plugin. Once your JavaScript has been compiled, you can reference it in your application:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="vendor-extraction"></a>
### Vendor Extraction

One potential downside to bundling all of your application-specific JavaScript with your vendor libraries such as React and Vue is that it makes long-term caching more difficult. For example, a single update to your application code will force the browser to re-download all of your vendor libraries even if they haven't changed.

If you intend to make frequent updates to your application's JavaScript, you should consider extracting all of your vendor libraries into their own file. This way, a change to your application code will not affect the caching of your large `vendor.js` file. Mix's `extract` method makes this a breeze:

    mix.js('resources/js/app.js', 'public/js')
        .extract(['vue'])

The `extract` method accepts an array of all libraries or modules that you wish to extract into a `vendor.js` file. Using the snippet above as an example, Mix will generate the following files:

<div class="content-list" markdown="1">

- `public/js/manifest.js`: *The Webpack manifest runtime*
- `public/js/vendor.js`: *Your vendor libraries*
- `public/js/app.js`: *Your application code*

</div>

To avoid JavaScript errors, be sure to load these files in the proper order:

    <script src="/js/manifest.js"></script>
    <script src="/js/vendor.js"></script>
    <script src="/js/app.js"></script>

<a name="custom-webpack-configuration"></a>
### Custom Webpack Configuration

Occasionally, you may need to manually modify the underlying Webpack configuration. For example, you might have a special loader or plugin that needs to be referenced.

Mix provides a useful `webpackConfig` method that allows you to merge any short Webpack configuration overrides. This is particularly appealing, as it doesn't require you to copy and maintain your own copy of the `webpack.config.js` file. The `webpackConfig` method accepts an object, which should contain any [Webpack-specific configuration](https://webpack.js.org/configuration/) that you wish to apply.

    mix.webpackConfig({
        resolve: {
            modules: [
                path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
            ]
        }
    });

<a name="versioning-and-cache-busting"></a>
## Versioning / Cache Busting

Many developers suffix their compiled assets with a timestamp or unique token to force browsers to load the fresh assets instead of serving stale copies of the code. Mix can automatically handle this for you using the `version` method.

The `version` method will append a unique hash to the filenames of all compiled files, allowing for more convenient cache busting:

    mix.js('resources/js/app.js', 'public/js')
        .version();

After generating the versioned file, you won't know the exact filename. So, you should use Laravel's global `mix` function within your [views](/docs/{{version}}/views) to load the appropriately hashed asset. The `mix` function will automatically determine the current name of the hashed file:

    <script src="{{ mix('/js/app.js') }}"></script>

Because versioned files are usually unnecessary in development, you may instruct the versioning process to only run during `npm run prod`:

    mix.js('resources/js/app.js', 'public/js');

    if (mix.inProduction()) {
        mix.version();
    }

<a name="custom-mix-base-urls"></a>
#### Custom Mix Base URLs

If your Mix compiled assets are deployed to a CDN separate from your application, you will need to change the base URL generated by the `mix` function. You may do so by adding a `mix_url` configuration option to your application's `config/app.php` configuration file:

    'mix_url' => env('MIX_ASSET_URL', null)

After configuring the Mix URL, The `mix` function will prefix the configured URL when generating URLs to assets:

```shell
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
## Browsersync Reloading

[BrowserSync](https://browsersync.io/) can automatically monitor your files for changes, and inject your changes into the browser without requiring a manual refresh. You may enable support for this by calling the `mix.browserSync()` method:

```js
mix.browserSync('laravel.test');
```

[BrowserSync options](https://browsersync.io/docs/options) may be specified by passing a JavaScript object to the `browserSync` method:

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

Next, start webpack's development server using the `npm run watch` command. Now, when you modify a script or PHP file you can watch as the browser instantly refreshes the page to reflect your changes.

<a name="environment-variables"></a>
## Environment Variables

You may inject environment variables into your `webpack.mix.js` script by prefixing one of the environment variables in your `.env` file with `MIX_`:

    MIX_SENTRY_DSN_PUBLIC=http://example.com

After the variable has been defined in your `.env` file, you may access it via the `process.env` object. However, you will need to restart the task if the environment variable's value changes while the task is running:

    process.env.MIX_SENTRY_DSN_PUBLIC

<a name="notifications"></a>
## Notifications

When available, Mix will automatically display OS notifications when compiling, giving you instant feedback as to whether the compilation was successful or not. However, there may be instances when you would prefer to disable these notifications. One such example might be triggering Mix on your production server. Notifications may be deactivated using the `disableNotifications` method:

    mix.disableNotifications();
