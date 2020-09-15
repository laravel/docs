# Resetting Passwords

- [Introduction](#introduction)
- [Database Considerations](#resetting-database)
- [Routing](#resetting-routing)
- [Views](#resetting-views)
- [Customization](#password-customization)

<a name="introduction"></a>
## Introduction

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

> {note} Before using the password reset features of Laravel, your user must use the `Illuminate\Notifications\Notifiable` trait.

#### Getting Started Fast

Want to get started fast? Install [Laravel Jetstream](https://jetstream.laravel.com) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. Jetstream will take care of scaffolding your entire authentication system, including resetting passwords!

<a name="resetting-database"></a>
## Database Considerations

To get started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

#### Generating The Reset Token Table Migration

Next, a table must be created to store the password reset tokens. The migration for this table is included in the default Laravel installation, so you only need to migrate your database to create this table:

    php artisan migrate

<a name="resetting-routing"></a>
## Routing

All of the routes needed to perform password resets are automatically included in [Laravel Jetstream](https://jetstream.laravel.com). To learn how to install Jetstream, please consult the official [Jetstream documentation](https://jetstream.laravel.com).

<a name="resetting-views"></a>
## Views

All of the views needed to perform password resets are automatically included in [Laravel Jetstream](https://jetstream.laravel.com). To learn how to install Jetstream, please consult the official [Jetstream documentation](https://jetstream.laravel.com).

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
