# Email Verification

- [Introduction](#introduction)
- [Database Considerations](#verification-database)
- [Routing](#verification-routing)
    - [Protecting Routes](#protecting-routes)
- [Views](#verification-views)
- [After Verifying Emails](#after-verifying-emails)

<a name="introduction"></a>
## Introduction

Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending and verifying email verification requests.

### Model Preparation

To get started, verify that your `App\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract:

    <?php

    namespace App;

    use Illuminate\Notifications\Notifiable;
    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

### Email verification notification process

During the registration process an event `Illuminate\Auth\Events\Registered` is emit. Laravel come whith a listener `Illuminate\Auth\Listeners\SendEmailVerificationNotification` which is already registered in the `App\Providers\EventServiceProvider`.

After implementing the `MustVerifyEmail` interface when the `Registered` event is emit the `SendEmailVerificationNotification` listener will check if the `App\User` have already use the `Illuminate\Contracts\Auth\MustVerifyEmail` trait by checking if the user create is an instance of `MustVerifyEmail` if that is the case it will call the `sendEmailVerificationNotification` method on the `user` which get the implementation of this method when it use the `Illuminate\Auth\MustVerify`  trait.

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

Laravel will generate all of the necessary email verification views when the `make:auth` command is executed. This view is placed in `resources/views/auth/verify.blade.php`. You are free to customize this view as needed for your application.

<a name="after-verifying-emails"></a>
## After Verifying Emails

After an email address is verified, the user will automatically be redirected to `/home`. You can customize the post verification redirect location by defining a `redirectTo` method or property on the `VerificationController`:

    protected $redirectTo = '/dashboard';
