# Compiling Assets (Mix)

- [Introduction](#introduction)
- [Installation & Setup](#installation)

<a name="introduction"></a>
## Introduction

[Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors.

In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all.

<a name="installation"></a>
## Installation & Setup

Before running Mix, you must first ensure that Node.js and NPM are installed on your machine:

```shell
node -v
npm -v
```

You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](/docs/{{version}}/sail), you may invoke Node and NPM through Sail:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

You will now want to install and configure Laravel Mix for your project. For full instructions, head over to the [Laravel Mix website](https://laravel-mix.com/). If you are migrating a Laravel Vite based project to Mix, you may also wish to read the [Vite to Mix migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix).
