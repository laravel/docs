# Starter Kits

- [Laravel Breeze](#laravel-breeze)
    - [Installation](#laravel-breeze-installation)
- [Laravel Jetstream](#laravel-jetstream)

<a name="laravel-breeze"></a>
## Laravel Breeze

Laravel Breeze is a minimal, simple implementation of all of Laravel's [authentication features](/docs/{{version}}/authentication), including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/{{version}}/blade) styled with [Tailwind CSS](htts://tailwindcss.com).

<a name="laravel-breeze-installation"></a>
### Installation

First, you should [create a new Laravel application](/docs/{{version}}/installation), configure your database, and run your [database migrations](/docs/{{version}}/migrations):

```bash
curl -s https://laravel.build/my-app | bash

cd my-app

php artisan migrate
```

Once you have created a new Laravel application, you may install Laravel Breeze using Composer:

    composer require laravel/breeze --dev

After Composer has installed the Laravel Breeze package, you may run the `breeze:install` Artisan command. This command publishes the authentication views, routes, controllers, and other resources to your application. Laravel Breeze publishes all of its code to your application so that you have full control and visibility over its features and implementation. After Breeze is installed, you should also compile your assets so that your application's CSS file is available:

    php artisan breeze:install

    npm install && npm run dev

Next, you may navigate to your application's `/login` or `/register` URLs in your web browser. All of Breeze's routes are defined within the `routes/auth.php` file.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Jetstream is a beautifully designed application scaffolding for Laravel. Jetstream provides the perfect starting point for your next Laravel application and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia.js](https://inertiajs.com) scaffolding.

Complete documentation for installing Laravel Jetstream can be found within the [official Jetstream documentation](https://jetstream.laravel.com/1.x/introduction.html).
