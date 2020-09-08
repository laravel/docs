# Resetting Passwords

- [Introduction](#introduction)
- [Database Considerations](#resetting-database)
- [Routing](#resetting-routing)
- [Views](#resetting-views)
- [After Resetting Passwords](#after-resetting-passwords)
- [Customization](#password-customization)

<a name="introduction"></a>
## Introduction

> {tip} **Want to get started fast?** Install the `laravel/jetstream` Composer package and run `php artisan jetstream:install livewire/inertia` in a fresh Laravel application. After migrating your database, navigate your browser to `http://your-app.test/register` or any other URL that is assigned to your application. This single command will take care of scaffolding your entire authentication system, including resetting passwords!

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

> {note} Before using the password reset features of Laravel, your user must use the `Illuminate\Notifications\Notifiable` trait.

<a name="resetting-database"></a>
## Database Considerations

To get started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

#### Generating The Reset Token Table Migration

Next, a table must be created to store the password reset tokens. The migration for this table is included in the `laravel/jetstream` Composer package. After installing the `laravel/jetstream` package, you may use the `migrate` command to create the password reset token database table:

    composer require laravel/jetstream

    php artisan jetstream:install livewire/inertia

    php artisan migrate

<a name="resetting-routing"></a>
## Routing

All of the routes needed to perform password resets may be generated using the `laravel/jetstream` Composer package:

    composer require laravel/jetstream

    php artisan jetstream:install livewire/inertia

<a name="resetting-views"></a>
## Views

To generate all of the necessary view for resetting passwords, you may use the `laravel/jetstream` Composer package:

    composer require laravel/jetstream

    php artisan jetstream:install livewire/inertia

These views are placed in the `resources/views/auth` directory. You are free to customize them as needed for your application.

<a name="after-resetting-passwords"></a>
## After Resetting Passwords

Once you have defined the routes and views to reset your user's passwords, you may access the route in your browser at `/password/reset`. The controllers included in the Laravel Jetstream package already includes the logic to send the password reset link emails as well as the logic to reset user passwords.

> {note} By default, password reset tokens expire after one hour. You may change this via the password reset `expire` option in your `config/auth.php` file.

<a name="password-customization"></a>
## Customization

#### Reset Email Customization

You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `User` model. Within this method, you may send the notification using any notification class you choose. The password reset `$token` is the first argument received by the method:

    /**
     * Send the password reset notification.
     *
     * @param  string  $token
     * @return void
     */
    public function sendPasswordResetNotification($token)
    {
        $this->notify(new ResetPasswordNotification($token));
    }
