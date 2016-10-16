# Resetting Passwords

- [Introduction](#introduction)
- [Database Considerations](#resetting-database)
- [Routing](#resetting-routing)
- [Views](#resetting-views)
- [After Resetting Passwords](#after-resetting-passwords)
- [Customization](#password-customization)

<a name="introduction"></a>
## Introduction

> {tip} **Want to get started fast?** Just run `php artisan make:auth` in a fresh Laravel application and navigate your browser to `http://your-app.dev/register` or any other URL that is assigned to your application. This single command will take care of scaffolding your entire authentication system, including resetting passwords!

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

> {note} Before using the password reset features of Laravel, your user must use the `Illuminate\Notifications\Notifiable` trait.

<a name="resetting-database"></a>
## Database Considerations

To get started, verify that your `App\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. Of course, the `App\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

#### Generating The Reset Token Table Migration

Next, a table must be created to store the password reset tokens. The migration for this table is included with Laravel out of the box, and resides in the `database/migrations` directory. So, all you need to do is run your database migrations:

    php artisan migrate

<a name="resetting-routing"></a>
## Routing

Laravel includes `Auth\ForgotPasswordController` and `Auth\ResetPasswordController` classes that contains the logic necessary to e-mail password reset links and reset user passwords. All of the routes needed to perform password resets may be generated using the `make:auth` Artisan command:

    php artisan make:auth

<a name="resetting-views"></a>
## Views

Again, Laravel will generate all of the necessary views for password reset when the `make:auth` command is executed. These views are placed in `resources/views/auth/passwords`. You are free to customize them as needed for your application.

<a name="after-resetting-passwords"></a>
## After Resetting Passwords

Once you have defined the routes and views to reset your user's passwords, you may simply access the route in your browser at `/password/reset`. The `ForgotPasswordController` included with the framework already includes the logic to send the password reset link e-mails, while the `ResetPasswordController` includes the logic to reset user passwords.

After a password is reset, the user will automatically be logged into the application and redirected to `/home`. You can customize the post password reset redirect location by defining a `redirectTo` property on the `ResetPasswordController`:

    protected $redirectTo = '/dashboard';

> {note} By default, password reset tokens expire after one hour. You may change this via the password reset `expire` option in your `config/auth.php` file.

<a name="password-customization"></a>
## Customization

#### Authentication Guard Customization

In your `auth.php` configuration file, you may configure multiple "guards", which may be used to define authentication behavior for multiple user tables. You can customize the included `ResetPasswordController` to use the guard of your choice by overriding the `guard` method on the controller. This method should return a guard instance:

    use Illuminate\Support\Facades\Auth;

    protected function guard()
    {
        return Auth::guard('guard-name');
    }

#### Password Broker Customization

In your `auth.php` configuration file, you may configure multiple password "brokers", which may be used to reset passwords on multiple user tables. You can customize the included `ForgotPasswordController` and `ResetPasswordController` to use the broker of your choice by overriding the `broker` method:

    use Illuminate\Support\Facades\Password;

    /**
     * Get the broker to be used during password reset.
     *
     * @return PasswordBroker
     */
    protected function broker()
    {
        return Password::broker('name');
    }

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

