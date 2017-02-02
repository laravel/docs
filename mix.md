# Compiling Assets (Laravel Mix)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
- [Running Mix](#running-mix)
- [Working With Stylesheets](#working-with-stylesheets)
    - [Less](#less)
    - [Sass](#sass)
    - [Plain CSS](#plain-css)
    - [Source Maps](#css-source-maps)
- [Working With JavaScript](#working-with-scripts)
    - [Code Splitting](#code-splitting)
    - [Custom Webpack Configuration](#custom-webpack-configuration)
- [Copying Files & Directories](#copying-files-and-directories)
- [Versioning / Cache Busting](#versioning-and-cache-busting)
- [Notifications](#notifications)

<a name="introduction"></a>
## Introduction

Laravel Mix provides a fluent API for defining Webpack build steps for your Laravel application using several common CSS and JavaScript pre-processors. Through simple method chaining, you can fluently define your asset pipeline. For example:

    mix.js('resources/assets/js/app.js', 'public/js')
       .sass('resources/assets/sass/app.scss', 'public/css');

If you've ever been confused and overwhelmed about getting started with Webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application. Of course, you are free to use any asset pipeline tool you wish, or even none at all.

<a name="installation"></a>
## Installation & Setup

#### Installing Node

Before triggering Mix, you must first ensure that Node.js and NPM are installed on your machine.

    node -v
    npm -v

By default, Laravel Homestead includes everything you need; however, if you aren't using Vagrant, then you can easily install the latest version of Node and NPM using simple graphical installers from [their download page](https://nodejs.org/en/download/).

#### Laravel Mix

The only remaining step is to install Laravel Mix. Within a fresh installation of Laravel, you'll find a `package.json` file in the root of your directory structure. The default `package.json` file includes everything you need to get started. Think of this like your `composer.json` file, except it defines Node dependencies instead of PHP. You may install the dependencies it references by running:

    npm install

If you are developing on a Windows system or you are running your VM on a Windows host system, you may need to run the `npm install` command with the `--no-bin-links` switch enabled:

    npm install --no-bin-links

<a name="running-mix"></a>
## Running Mix

Mix is a configuration layer on top of [Webpack](https://webpack.js.org), so to run your Mix tasks you only need to execute one of the NPM scripts that is included with the default Laravel `package.json` file:

    // Run all Mix tasks...
    npm run dev

    // Run all Mix tasks and minify output...
    npm run production

#### Watching Assets For Changes

The `npm run watch` command will continue running in your terminal and watch all relevant files for changes. Webpack will then automatically recompile your assets when it detects a change:

    npm run watch

<a name="working-with-stylesheets"></a>
## Working With Stylesheets

The `webpack.mix.js` file is your entry point for all asset compilation. Think of it as a light configuration wrapper around Webpack. Mix tasks can be chained together to define exactly how your assets should be compiled.

<a name="less"></a>
### Less

The `less` method may be used to compile [Less](http://lesscss.org/) into CSS. Let's compile our primary `app.less` file to `public/css/app.css`.

    mix.less('resources/assets/less/app.less', 'public/css');

Multiple calls to the `less` method may be used to compile multiple files:

    mix.less('resources/assets/less/app.less', 'public/css')
       .less('resources/assets/less/admin.less', 'public/css');

If you wish to customize the file name of the compiled CSS, you may pass a full file path as the second argument to the `less` method:

    mix.less('resources/assets/less/app.less', 'public/stylesheets/styles.css');

<a name="sass"></a>
### Sass

The `sass` method allows you to compile [Sass](http://sass-lang.com/) into CSS. You may use the method like so:

    mix.sass('resources/assets/sass/app.scss', 'public/css');

Again, like the `less` method, you may compile multiple Sass files into their own respective CSS files and even customize the output directory of the resulting CSS:

    mix.sass('resources/assets/sass/app.sass', 'public/css')
       .sass('resources/assets/sass/admin.sass', 'public/css/admin');

<a name="plain-css"></a>
### Plain CSS

If you would just like to combine some plain CSS stylesheets into a single file, you may use the `combine` method. This method also supports concatenating JavaScript files:

    mix.combine([
        'public/css/vendor/normalize.css',
        'public/css/vendor/videojs.css'
    ], 'public/css/all.css');

<a name="css-source-maps"></a>
### Source Maps

Though disabled by default, source maps may be activated by calling the `mix.sourceMaps()` method in your `webpack.mix.js` file. Though it comes with a compile/performance cost, this will provide extra debugging information to your browser's developer tools when using compiled assets.

    mix.js('resources/assets/js/app.js', 'public/js')
       .sourceMaps();

<a name="working-with-scripts"></a>
## Working With JavaScript

Mix provides several features to help you work with your JavaScript files, such as compiling ECMAScript 2015, module bundling, minification, and simply concatenating plain JavaScript files. Even better, this all works seamlessly, without requiring an ounce of custom configuration:

    mix.js('resources/assets/js/app.js', 'public/js');

With this single line of code, you may now take advantage of:

<div class="content-list" markdown="1">
- ES2015 syntax.
- Compilation of `.vue` files.
- Minification for production environments.
</div>

<a name="code-splitting"></a>
### Code Splitting

One potential downside to bundling all application-specific JavaScript with your vendor libraries is that it makes long-term caching more difficult. For example, a single update to your application code will force the browser to re-download all of your vendor libraries even if they haven't changed.

If you intend to make frequent updates to your application's JavaScript, you should consider extracting all of your vendor libraries into their file. This way, a change to your application code will not affect the caching of your large `vendor.js` file. Mix's `extract` method makes this a breeze:

    mix.js('resources/assets/js/app.js', 'public/js')
       .extract(['vue'])

The `extract` method accepts an array of all libraries or modules that you wish to extract into a `vendor.js` file. Using the above snippet as an example, Mix will generate the following files:

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

Behind the scenes, Laravel Mix references a pre-configured `webpack.config.js` file to get you up and running as quickly as possible. Occasionally, you may need to manually modify this file. You might have a special loader or plugin that needs to be referenced, or maybe you prefer to use Stylus instead of Sass. In such instances, you have two choices:

#### Merging

Mix provides a useful `webpackConfig` method that allows you to merge any short Webpack configuration overrides. This is a particularly appealing choice, as it doesn't require you to copy and maintain your own copy of the `webpack.config.js` file. The `webpackConfig` method accepts an object, which should contain any [Webpack-specific configuration](https://webpack.js.org/configuration/) that you wish to apply.

    mix.webpackConfig({
        resolve: {
            modules: [
                path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
            ]
        }
    });

#### Reference Your Own Configuration

A second option is to copy Mix's `webpack.config.js` into your project root.

    cp node_modules/laravel-mix/setup/webpack.config.js ./

Next, you'll need to update the NPM scripts in your `package.json` to ensure that they no longer reference Mix's configuration file directly. Simply remove the `--config="node_modules/laravel-mix/setup/webpack.config.js"` entry from the commands. Once this has been done, you may freely modify your configuration file as needed.


<a name="copying-files-and-directories"></a>
## Copying Files & Directories

The `copy` method may be used to copy files and directories to new locations. This can be useful when a particular asset within your `node_modules` directory needs to be relocated to your `public` folder.

    mix.copy('node_modules/foo/bar.css', 'public/css/bar.css');

<a name="versioning-and-cache-busting"></a>
## Versioning / Cache Busting

Many developers suffix their compiled assets with a timestamp or unique token to force browsers to load the fresh assets instead of serving stale copies of the code. Mix can handle this for you using the `version` method.

When executed in a production environment (`npm run production`), the `version` method will automatically append a unique hash to the filenames of all compiled files, allowing for more convenient cache busting:

    mix.js('resources/assets/js/app.js', 'public/js')
       .version();

After generating the versioned file, you won't know the exact file name. So, you should use Laravel's global `mix` function within your [views](/docs/{{version}}/views) to load the appropriately hashed asset. The `mix` function will automatically determine the current name of the hashed file:

    <link rel="stylesheet" href="{{ mix('/css/app.css') }}">

<a name="notifications"></a>
## Notifications

When available, Mix will automatically display OS notifications for each bundle. This will give you instant feedback, as to whether the compilation was successful or not. However, there may be instances when you'd prefer to disable these notifications. One such example might be triggering Mix on your production server. Notifications may be deactivated, via the `disableNotifications` method.

    mix.disableNotifications();
