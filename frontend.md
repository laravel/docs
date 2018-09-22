# JavaScript & CSS Scaffolding

- [Introduction](#introduction)
- [Writing CSS](#writing-css)
- [Writing JavaScript](#writing-javascript)
    - [Writing Vue Components](#writing-vue-components)
    - [Using React](#using-react)

<a name="introduction"></a>
## Introduction

While Laravel does not dictate which JavaScript or CSS pre-processors you use, it does provide a basic starting point using [Bootstrap](https://getbootstrap.com/) and [Vue](https://vuejs.org) that will be helpful for many applications. By default, Laravel uses [NPM](https://www.npmjs.org) to install both of these frontend packages.

#### CSS

[Laravel Mix](/docs/{{version}}/mix) provides a clean, expressive API over compiling SASS or Less, which are extensions of plain CSS that add variables, mixins, and other powerful features that make working with CSS much more enjoyable. In this document, we will briefly discuss CSS compilation in general; however, you should consult the full [Laravel Mix documentation](/docs/{{version}}/mix) for more information on compiling SASS or Less.

#### JavaScript

Laravel does not require you to use a specific JavaScript framework or library to build your applications. In fact, you don't have to use JavaScript at all. However, Laravel does include some basic scaffolding to make it easier to get started writing modern JavaScript using the [Vue](https://vuejs.org) library. Vue provides an expressive API for building robust JavaScript applications using components. As with CSS, we may use Laravel Mix to easily compile JavaScript components into a single, browser-ready JavaScript file.

#### Removing The Frontend Scaffolding

If you would like to remove the frontend scaffolding from your application, you may use the `preset` Artisan command. This command, when combined with the `none` option, will remove the Bootstrap and Vue scaffolding from your application, leaving only a blank SASS file and a few common JavaScript utility libraries:

    php artisan preset none

<a name="writing-css"></a>
## Writing CSS

Laravel's `package.json` file includes the `bootstrap` package to help you get started prototyping your application's frontend using Bootstrap. However, feel free to add or remove packages from the `package.json` file as needed for your own application. You are not required to use the Bootstrap framework to build your Laravel application - it is provided as a good starting point for those who choose to use it.

Before compiling your CSS, install your project's frontend dependencies using the [Node package manager (NPM)](https://www.npmjs.org):

    npm install

Once the dependencies have been installed using `npm install`, you can compile your SASS files to plain CSS using [Laravel Mix](/docs/{{version}}/mix#working-with-stylesheets). The `npm run dev` command will process the instructions in your `webpack.mix.js` file. Typically, your compiled CSS will be placed in the `public/css` directory:

    npm run dev

The default `webpack.mix.js` included with Laravel will compile the `resources/sass/app.scss` SASS file. This `app.scss` file imports a file of SASS variables and loads Bootstrap, which provides a good starting point for most applications. Feel free to customize the `app.scss` file however you wish or even use an entirely different pre-processor by [configuring Laravel Mix](/docs/{{version}}/mix).

<a name="writing-javascript"></a>
## Writing JavaScript

All of the JavaScript dependencies required by your application can be found in the `package.json` file in the project's root directory. This file is similar to a `composer.json` file except it specifies JavaScript dependencies instead of PHP dependencies. You can install these dependencies using the [Node package manager (NPM)](https://www.npmjs.org):

    npm install

> {tip} By default, the Laravel `package.json` file includes a few packages such as `vue` and `axios` to help you get started building your JavaScript application. Feel free to add or remove from the `package.json` file as needed for your own application.

Once the packages are installed, you can use the `npm run dev` command to [compile your assets](/docs/{{version}}/mix). Webpack is a module bundler for modern JavaScript applications. When you run the `npm run dev` command, Webpack will execute the instructions in your `webpack.mix.js` file:

    npm run dev

By default, the Laravel `webpack.mix.js` file compiles your SASS and the `resources/js/app.js` file. Within the `app.js` file you may register your Vue components or, if you prefer a different framework, configure your own JavaScript application. Your compiled JavaScript will typically be placed in the `public/js` directory.

> {tip} The `app.js` file will load the `resources/js/bootstrap.js` file which bootstraps and configures Vue, Axios, jQuery, and all other JavaScript dependencies. If you have additional JavaScript dependencies to configure, you may do so in this file.

<a name="writing-vue-components"></a>
### Writing Vue Components

By default, fresh Laravel applications contain an `ExampleComponent.vue` Vue component located in the `resources/js/components` directory. The `ExampleComponent.vue` file is an example of a [single file Vue component](https://vuejs.org/guide/single-file-components) which defines its JavaScript and HTML template in the same file. Single file components provide a very convenient approach to building JavaScript driven applications. The example component is registered in your `app.js` file:

    Vue.component(
        'example-component',
        require('./components/ExampleComponent.vue')
    );

To use the component in your application, you may drop it into one of your HTML templates. For example, after running the `make:auth` Artisan command to scaffold your application's authentication and registration screens, you could drop the component into the `home.blade.php` Blade template:

    @extends('layouts.app')

    @section('content')
        <example-component></example-component>
    @endsection

> {tip} Remember, you should run the `npm run dev` command each time you change a Vue component. Or, you may run the `npm run watch` command to monitor and automatically recompile your components each time they are modified.

Of course, if you are interested in learning more about writing Vue components, you should read the [Vue documentation](https://vuejs.org/guide/), which provides a thorough, easy-to-read overview of the entire Vue framework.

<a name="using-react"></a>
### Using React

If you prefer to use React to build your JavaScript application, Laravel makes it a cinch to swap the Vue scaffolding with React scaffolding. On any fresh Laravel application, you may use the `preset` command with the `react` option:

    php artisan preset react

This single command will remove the Vue scaffolding and replace it with React scaffolding, including an example component.
