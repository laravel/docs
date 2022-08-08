# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
    - [Breeze & Blade](#breeze-and-blade)
    - [Breeze & React / Vue](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## Introduction

To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users.

While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze) is a minimal, simple implementation of all of Laravel's [authentication features](/docs/{{version}}/authentication), including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/{{version}}/blade) styled with [Tailwind CSS](https://tailwindcss.com). Or, Breeze can scaffold your application using Vue or React and [Inertia](https://inertiajs.com).

Breeze provides a wonderful starting point for beginning a fresh Laravel application and is also great choice for projects that plan to take their Blade templates to the next level with [Laravel Livewire](https://laravel-livewire.com).

<img src="https://laravel.com/img/docs/breeze-register.png">

<a name="laravel-breeze-installation"></a>
### Installation

First, you should [create a new Laravel application](/docs/{{version}}/installation), configure your database, and run your [database migrations](/docs/{{version}}/migrations). Once you have created a new Laravel application, you may install Laravel Breeze using Composer:

```shell
composer require laravel/breeze --dev
```

Once Breeze is installed, you may scaffold your application using one of the Breeze "stacks" discussed in the documentation below.

<a name="breeze-and-blade"></a>
### Breeze & Blade

After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation.

The default Breeze "stack" is the Blade stack, which utilizes simple [Blade templates](/docs/{{version}}/blade) to render your application's frontend. The Blade stack may be installed by invoking the `breeze:install` command with no other additional arguments. After Breeze's scaffolding is installed, you should also compile your application's frontend assets:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file.

> **Note**  
> To learn more about compiling your application's CSS and JavaScript, check out Laravel's [Vite documentation](/docs/{{version}}/vite#running-vite).

<a name="breeze-and-inertia"></a>
### Breeze & React / Vue

Laravel Breeze also offers React and Vue scaffolding via an [Inertia](https://inertiajs.com) frontend implementation. Inertia allows you to build modern, single-page React and Vue applications using classic server-side routing and controllers.

Inertia lets you enjoy the frontend power of React and Vue combined with the incredible backend productivity of Laravel and lightning-fast [Vite](https://vitejs.dev) compilation. To use an Inertia stack, specify `vue` or `react` as your desired stack when executing the `breeze:install` Artisan command. After Breeze's scaffolding is installed, you should also compile your application's frontend assets:

```shell
php artisan breeze:install vue

# Or...

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file.

<a name="server-side-rendering"></a>
#### Server-Side Rendering

If you would like Breeze to scaffold support for [Inertia SSR](https://inertiajs.com/server-side-rendering), you may provide the `ssr` option when invoking the `breeze:install` command:

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
### Breeze & Next.js / API

Laravel Breeze can also scaffold an authentication API that is ready to authenticate modern JavaScript applications such as those powered by [Next](https://nextjs.org), [Nuxt](https://nuxtjs.org), and others. To get started, specify the `api` stack as your desired stack when executing the `breeze:install` Artisan command:

```shell
php artisan breeze:install api

php artisan migrate
```

During installation, Breeze will add a `FRONTEND_URL` environment variable to your application's `.env` file. This URL should be the URL of your JavaScript application. This will typically be `http://localhost:3000` during local development. In addition, you should ensure that your `APP_URL` is set to `http://localhost:8000`, which is the default URL used by the `serve` Artisan command.

<a name="next-reference-implementation"></a>
#### Next.js Reference Implementation

Finally, you are ready to pair this backend with the frontend of your choice. A Next reference implementation of the Breeze frontend is [available on GitHub](https://github.com/laravel/breeze-next). This frontend is maintained by Laravel and contains the same user interface as the traditional Blade and Inertia stacks provided by Breeze.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.**

Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) driven frontend scaffolding.

Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/2.x/introduction.html).
