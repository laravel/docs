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
    - [Custom Webpack Config](#custom-webpack-config)
- [Copying Files & Directories](#copying-files-and-directories)
- [Versioning / Cache Busting](#versioning-and-cache-busting)
- [Notifications](#notifications)

<a name="introduction"></a>
## Introduction

Laravel Mix provides a clean, fluent API for defining basic Webpack build steps for your Laravel application. Mix supports several common CSS and JavaScript pre-processors. Through simple method chaining, you can fluently define your asset pipeline. For example:

```javascript
mix.js('resources/assets/js/app.js', 'public/js')
   .sass('resources/assets/sass/app.scss', 'public/css');
```

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

Mix is a configuration layer on top of [Webpack](https://webpack.js.org), so to run your Mix tasks you only need to trigger the `webpack` command in your terminal. Adding the `NODE_ENV=production` flag to this command will additionally instruct Mix to minify your CSS and JavaScript files:

    // Run all tasks...
    node_modules/.bin/webpack

    // Run all tasks and minify all CSS and JavaScript...
    NODE_ENV=production node_modules/.bin/webpack

However, because it's a bit tedious to type these commands in the terminal over and over, Laravel provides a handful of NPM scripts to assist. You may review these within your `package.json` file. As such, you may freely use:

    // Run all tasks...
    npm run webpack

    // Run all tasks, and watch files for changes...
    npm run dev

    // Run all tasks and minify all CSS and JavaScript...
    npm run production

#### Watching Assets For Changes

The `npm run dev` command will continue running in your terminal and watch all relevant files for changes. Webpack will then automatically recompile your assets, if it detects a change.

    npm run dev

<a name="working-with-stylesheets"></a>
## Working With Stylesheets

The `webpack.mix.js` file is your entry point for all asset compilation. Think of it as a light configuration wrapper around Webpack. Mix tasks can be chained together to define exactly how your assets should be compiled.

<a name="less"></a>
### Less

The `less` method may be used to compile [Less](http://lesscss.org/) into CSS. Let's compile our primary `app.less` file to `public/css/app.less`.

```javascript
mix.less('resources/assets/less/app.less', 'public/css');
```

You may also compile multiple Less files into their own respective CSS files, like so:

```javascript
mix.less('resources/assets/less/app.less', 'public/css')
   .less('resources/assets/less/admin.less', 'public/css');
```

If you wish to customize the output file name of the compiled CSS, you may of course pass a full file path, as the second argument.

```javascript
mix.less('resouces/assets/less/app.less', 'public/stylesheets/styles.css');
```

<a name="sass"></a>
### Sass

The `sass` method allows you to compile [Sass](http://sass-lang.com/) into CSS. You may use the method like so:

```javascript
mix.sass('resources/assets/sass/app.scss', 'public/css');
```

Again, like the `sass` method, you may compile multiple Sass files into their own respective CSS files, and even customize the output directory of the resulting CSS:

```javascript
mix.sass('resources/assets/sass/app.sass', 'public/css');
   .sass('resources/assets/sass/admin.sass', 'public/css/admin');
```

<a name="plain-css"></a>
### Plain CSS

If you would just like to combine some plain CSS stylesheets into a single file, you may use the `combine` method. This will additionally work with any JavaScript files that require concatenation.

```javascript
mix.combine([
    'public/css/vendor/normalize.css',
    'public/css/vendor/videojs.css'
}, 'public/css/all.css');
```

<a name="css-source-maps"></a>
### Source Maps

Though disabled by default, source maps may be activated by calling the `mix.sourceMaps()` method in your `webpack.mix.js` file. Though it comes with a compile/performance cost, this will provide extra debugging information to your browser's developer tools when using compiled assets. 

```javascript
mix.js('resources/assets/js/app.js', 'public/js')
   .sourceMaps();
```

<a name="working-with-scripts"></a>
## Working With JavaScript

Mix provides several features to help you work with your JavaScript files, such as compiling ECMAScript 2015, module bundling, minification, and simply concatenating plain JavaScript files. Even better, this all works seamlessly, without requiring an ounce of configuration on your part.

```javascript
mix.js('resources/assets/js/app.js', 'public/js');
```

With this single line of code, you may now take advantage of:

1. ES2015 syntax
2. Automatic Babel transformation
3. JavaScript modules
4. Compiling `.vue` files 
5. Instant minification for production environments

<a name="code-splitting"></a>
### Code Splitting

One potential downside to bundling all application-specific JavaScript with your vendor libraries is that it makes long-term caching a bit more difficult. For example, a single update to your application code will force the browser to redownload your vendor libraries all over again - even if they haven't changed. 

If you intend to make frequent updates to your application's JavaScript, you might consider extracting all vendor libraries into their file. This way, a change to your application code will not affect the caching of your large `vendor.js` file. Mix makes this all a cinch, via the `extract` method.

```javascript
mix.js('resources/assets/js/app.js', 'public/js')
   .extract(['vue'])
```

Simply pass an array of all libraries or modules that you wish to extract into their own `vendor.js` file. Using the above snippet as an example, Mix will generate the following files:

- `public/js/manifest.js`: *The Webpack manifest runtime*
- `public/js/vendor.js`: *Your vendor libraries*
- `public/js/app.js`: *Your app code*

Within your HTML, be sure to reference them in the proper order, to avoid any nasty JavaScript errors:

```html
<script src="/js/manifest.js"></script>
<script src="/js/vendor.js"></script>
<script src="/js/app.js"></script>
```

While, yes, you will pay a small HTTP request penalty, now that we're importing three scripts instead of one, the long-term caching benefits should far out-weigh this cost.

<a name="custom-webpack-config"></a>
### Custom Webpack Config

Behind the scenes, Laravel Mix references a pre-configured `webpack.config.js` file to get you up and running as quickly as possible. In fact, you can ignore it entirely, if you wish! That being said, from time to time, you may find that you need to manually modify this file. Perhaps you have a special loader or plugin that needs to be referenced, or maybe you prefer to use Stylus instead of Sass. In such instances, you have two choices:

#### Merging

Mix provides a useful `webpackConfig` method that allows you to merge any short Webpack configuration overrides. This is a particularly appealing choice, as it doesn't require you to copy and maintain your own copy of the `webpack.config.js` file. The `webpackConfig` method accepts an object, which should contain any [Webpack-specific configuration](https://webpack.js.org/configuration/) that you wish to apply.

```javascript
mix.webpackConfig({
    resolve: {
        modules: [
            path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
        ]
    }
});
```

#### Reference Your Own

A second option is to copy Mix's `webpack.config.js` into your project root. 

```bash
cp node_modules/laravel-mix/setup/webpack.config.js ./
```

Next, you'll want to update the NPM scripts in your `package.json` to ensure that they no longer reference Mix's configuration file directly. Simply remove the `--config="node_modules/laravel-mix/setup/webpack.config.js"`, and you should be all set! You many now freely modify your configuration file, as needed.


<a name="copying-files-and-directories"></a>
## Copying Files & Directories

The `copy` method may be used to copy files and directories to new locations. This can be useful when a particular asset within, say, your `node_modules` directory needs to be relocated to your `public` folder.

```javascript
mix.copy('node_modules/foo/bar.css', 'public/css/bar.css');
```

<a name="versioning-and-cache-busting"></a>
## Versioning / Cache Busting

Many developers suffix their compiled assets with a timestamp or unique token to force browsers to load the fresh assets instead of serving stale copies of the code. Mix can handle this for you using the `version` method.

When executed in a production environment (`npm run production`), the `version` method will automatically append a unique hash to the filenames of all compiled files, allowing for cache-busting. For example, the generated file name will look something like: `app.16d570a7asdfa24usdf.css`:

```javascript
mix.js('resources/assets/js/app.js', 'public/js')
   .version();
```

After generating the versioned file, because you won't know the exact file name, you may use Laravel's global `mix` helper within your [views](/docs/{{version}}/views) to load the appropriately hashed asset. The `mix` function will automatically determine the current name of the hashed file:

```html
<link rel="stylesheet" href="{{ mix('/css/app.css') }}">
```

<a name="notifications"></a>
## Notifications

When available, Mix will automatically display OS notifications for each bundle. This will give you instant feedback, as to whether the compilation was successful or not. However, there may be instances when you'd prefer to disable these notifications. One such example might be triggering Mix on your production server. Notifications may be deactivated, via the `disableNotifications` method.

```javascript
mix.disableNotifications();
```
