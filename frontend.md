# JavaScript & CSS Scaffolding

- [Introduction](#introduction)
- [Writing CSS](#writing-css)
- [Writing JavaScript](#writing-javascript)

<a name="introduction"></a>
## Introduction

While Laravel does not dictate which JavaScript or CSS pre-processors you use, [Laravel Jetstream](https://jetstream.laravel.com) provides a basic starting point using [Tailwind CSS](https://tailwindcss.com/), [Inertia](https://inertiajs.com/), and / or [Livewire](https://laravel-livewire.com/) that will be helpful for many applications. By default, Laravel uses [NPM](https://www.npmjs.com/) to install frontend packages.

The Tailwind CSS and Livewire / Inertia scaffolding provided by Laravel is located in the `laravel/jetstream` Composer package, which may be installed using Composer:

    composer require laravel/jetstream

Once the `laravel/jetstream` package has been installed, you may install the frontend scaffolding using the `jetstream:install` Artisan command:

    // Install Jetstream with the Livewire stack...
    php artisan jetstream:install livewire

    // Install Jetstream with the Inertia stack...
    php artisan jetstream:install inertia

    // Generate team support scaffolding...
    php artisan jetstream:install livewire --teams

> {tip} To learn more about Laravel Jetstream, please consult the official [Jetstream documentation](https://jetstream.laravel.com).

#### CSS

[Laravel Mix](/docs/{{version}}/mix) provides a clean, expressive API over compiling SASS or Less, which are extensions of plain CSS that add variables, mixins, and other powerful features that make working with CSS much more enjoyable. In this document, we will briefly discuss CSS compilation in general; however, you should consult the full [Laravel Mix documentation](/docs/{{version}}/mix) for more information on compiling SASS or Less.

#### JavaScript

Laravel does not require you to use a specific JavaScript framework or library to build your applications. In fact, you don't have to use JavaScript at all. However, [Laravel Jetstream](https://jetstream.laravel.com) includes scaffolding for writing modern JavaScript using [Inertia](https://inertiajs.com) and [Vue](https://vuejs.org). Vue provides an expressive API for building robust JavaScript applications using components. As with CSS, we may use Laravel Mix to easily compile JavaScript components into a single, browser-ready JavaScript file.

<a name="writing-css"></a>
## Writing CSS

Out of the box, Laravel contains a single `resources/css/app.css` file. Your application's `webpack.mix.js` file has already been configured to use PostCSS to compile this file to plain CSS. Before compiling your CSS, install your project's frontend dependencies using the [Node package manager (NPM)](https://www.npmjs.org):

    npm install

Once the dependencies have been installed using `npm install`, you can compile your CSS files using [Laravel Mix](/docs/{{version}}/mix#working-with-stylesheets). The `npm run dev` command will process the instructions in your `webpack.mix.js` file. Typically, your compiled CSS will be placed in the `public/css` directory:

    npm run dev

#### Laravel Jetstream

If you are using the [Laravel Jetstream](https://jetstream.laravel.com) scaffolding, your application's `package.json` file will include [Tailwind CSS](https://tailwindcss.com) packages to help you get started prototyping your application's frontend using Tailwind.

The `webpack.mix.js` file included with Laravel Jetstream's frontend scaffolding will compile the `resources/css/app.css` file. This `app.css` file contains the proper starting configuration for Tailwind CSS. Feel free to customize the `app.css` file however you wish.

<a name="writing-javascript"></a>
## Writing JavaScript

After creating a new Laravel project, your application's `resources/js` directory will contain an `app.js` and `bootstrap.js` file. You may place your application's JavaScript within these files. The `bootstrap.js` file already initializes a few helpful libraries such as Lodash and Axios.

Before compiling your JavaScript, install your project's frontend dependencies using the [Node package manager (NPM)](https://www.npmjs.org):

    npm install

Once the dependencies have been installed using `npm install`, you can compile your JavaScript files using [Laravel Mix](/docs/{{version}}/mix#working-with-stylesheets). The `npm run dev` command will process the instructions in your `webpack.mix.js` file. Typically, your compiled JavaScript will be placed in the `public/js` directory:

    npm run dev

#### Laravel Jetstream

When using Laravel Jetstream's Inertia scaffolding, all of the JavaScript dependencies required by your application can be found in the `package.json` file in the project's root directory. Laravel Jetstream's installation process will automatically add the necessary Vue and Inertia libraries to your `package.json` file. This file is similar to a `composer.json` file except it specifies JavaScript dependencies instead of PHP dependencies. You can install these dependencies using the [Node package manager (NPM)](https://www.npmjs.org):

    npm install

Once the packages are installed, you can use the `npm run dev` command to [compile your assets](/docs/{{version}}/mix). Webpack is a module bundler for modern JavaScript applications. When you run the `npm run dev` command, Webpack will execute the instructions in your `webpack.mix.js` file:

    npm run dev
