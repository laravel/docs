# Email Verification

- [Introduction](#introduction)
- [Database Considerations](#verification-database)
- [Routing](#verification-routing)
    - [Protecting Routes](#protecting-routes)
- [Views](#verification-views)
- [After Verifying Emails](#after-verifying-emails)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending and verifying email verification requests.

### Model Preparation

To get started, verify that your `App\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract:

    <?php

    namespace App;

    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

<a name="verification-database"></a>
## Database Considerations

#### The Email Verification Column

Next, your `user` table must contain an `email_verified_at` column to store the date and time that the email address was verified. By default, the `users` table migration included with the Laravel framework already includes this column. So, all you need to do is run your database migrations:

    php artisan migrate

<a name="verification-routing"></a>
## Routing

Laravel includes the `Auth\VerificationController` class that contains the necessary logic to send verification links and verify emails. To register the necessary routes for this controller, pass the `verify` option to the `Auth::routes` method:

    Auth::routes(['verify' => true]);

<a name="protecting-routes"></a>
### Protecting Routes

[Route middleware](/docs/{{version}}/middleware) can be used to only allow verified users to access a given route. Laravel ships with a `verified` middleware, which is defined at `Illuminate\Auth\Middleware\EnsureEmailIsVerified`. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition:

    Route::get('profile', function () {
        // Only verified users may enter...
    })->middleware('verified');

<a name="verification-views"></a>
## Views

To generate all of the necessary view for email verification, you may use the `laravel/ui` Composer package:

    composer require laravel/ui --dev

    php artisan ui vue --auth

The email verification view is placed in `resources/views/auth/verify.blade.php`. You are free to customize this view as needed for your application.

<a name="after-verifying-emails"></a>
## After Verifying Emails

After an email address is verified, the user will automatically be redirected to `/home`. You can customize the post verification redirect location by defining a `redirectTo` method or property on the `VerificationController`:

    protected $redirectTo = '/dashboard';

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
