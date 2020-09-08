# Email Verification

- [Introduction](#introduction)
- [Model Preparation](#model-preparation)
- [Database Considerations](#verification-database)
- [Routing](#verification-routing)
    - [Protecting Routes](#protecting-routes)
- [Views](#verification-views)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending and verifying email verification requests.

<a name="model-preparation"></a>
## Model Preparation

To get started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

Once this interface has been added to your model, newly registered users will automatically be sent an email containing an email verification link. As you can see by examining your `EventServiceProvider`, Laravel already contains a `SendEmailVerificationNotification` listener that is attached to the `Illuminate\Auth\Events\Registered` event.

<a name="verification-database"></a>
### Database Considerations

#### The Email Verification Column

Next, your `user` table must contain an `email_verified_at` column to store the date and time that the email address was verified. By default, the `users` table migration included with the Laravel framework already includes this column. So, all you need to do is run your database migrations:

    php artisan migrate

<a name="verification-routing"></a>
## Routing

The [Laravel Jetstream](https://github.com/laravel/jetstream) package contains the necessary logic to send verification links and verify emails. The routes needed for this functionality are automatically registered by Jetstream, which may be installed via Composer:

    composer require laravel/jetstream

    php artisan jetstream:install livewire/inertia

<a name="protecting-routes"></a>
### Protecting Routes

[Route middleware](/docs/{{version}}/middleware) can be used to only allow verified users to access a given route. Laravel ships with a `verified` middleware, which is defined at `Illuminate\Auth\Middleware\EnsureEmailIsVerified`. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition:

    Route::get('profile', function () {
        // Only verified users may enter...
    })->middleware('verified');

<a name="verification-views"></a>
## Views

To generate all of the necessary view for email verification, you may use the `laravel/jetstream` Composer package:

    composer require laravel/jetstream

    php artisan jetstream:install livewire/inertia

The email verification view is placed in the `resources/views/auth/` directory. You are free to customize this view as needed for your application.

<a name="events"></a>
## Events

Laravel dispatches [events](/docs/{{version}}/events) during the email verification process. You may attach listeners to these events in your `EventServiceProvider`:

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerifiedUser',
        ],
    ];
