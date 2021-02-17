# Starter Kits

- [Introduction](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## Introduction

To give you a head start building your new Laravel application, we are happy to offer authentication and application starter kits. These kits automatically scaffold your application with the routes, controllers, and views you need to register and authenticate your application's users.

While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great!

<a name="laravel-breeze"></a>
## Laravel Breeze

Laravel Breeze is a minimal, simple implementation of all of Laravel's [authentication features](/docs/{{version}}/authentication), including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's default view layer is made up of simple [Blade templates](/docs/{{version}}/blade) styled with [Tailwind CSS](https://tailwindcss.com). Breeze provides a wonderful starting point for beginning a fresh Laravel application.

<a name="laravel-breeze-installation"></a>
### Installation

First, you should [create a new Laravel application](/docs/{{version}}/installation), configure your database, and run your [database migrations](/docs/{{version}}/migrations):

```bash
curl -s https://laravel.build/example-app | bash

cd example-app

php artisan migrate
```

Once you have created a new Laravel application, you may install Laravel Breeze using Composer:

```bash
composer require laravel/breeze --dev
```

After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. After Breeze is installed, you should also compile your assets so that your application's CSS file is available:

```bash
php artisan breeze:install

npm install

npm run dev
```

Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file.

> {tip} To learn more about compiling your application's CSS and JavaScript, check out the [Laravel Mix documentation](/docs/{{version}}/mix#running-mix).

<a name="breeze-and-inertia"></a>
#### Breeze & Inertia

Laravel Breeze also offers an [Inertia.js](https://inertiajs.com) frontend implementation powered by Vue. To use the Inertia stack, pass the `--inertia` option when executing the `breeze:install` Artisan command:

```bash
php artisan breeze:install --inertia

npm install

npm run dev
```

<a name="laravel-jetstream"></a>
## Laravel Jetstream

While Laravel Breeze provides a simple and minimal starting point for building a Laravel application, Jetstream augments that functionality with more robust features and additional frontend technology stacks. **For those brand new to Laravel, we recommend learning the ropes with Laravel Breeze before graduating to Laravel Jetstream.**

Jetstream provides a beautifully designed application scaffolding for Laravel and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia.js](https://inertiajs.com) driven frontend scaffolding.

Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/2.x/introduction.html).
