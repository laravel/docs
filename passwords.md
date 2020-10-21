# Resetting Passwords

- [Introduction](#introduction)
    - [Model Preparation](#model-preparation)
    - [Database Preparation](#database-preparation)
- [Routing](#routing)
    - [Requesting The Password Reset Link](#requesting-the-password-reset-link)
    - [Resetting The Password](#resetting-the-password)
- [Customization](#password-customization)

<a name="introduction"></a>
## Introduction

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

> {tip} Want to get started fast? Install [Laravel Jetstream](https://jetstream.laravel.com) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. Jetstream will take care of scaffolding your entire authentication system, including resetting passwords!

<a name="model-preparation"></a>
### Model Preparation

Before using the password reset features of Laravel, your `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is automatically included on the default `App\Models\User` model that is included with Laravel.

Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

<a name="database-preparation"></a>
### Database Preparation

A table must be created to store your application's password reset tokens. The migration for this table is included in the default Laravel installation, so you only need to migrate your database to create this table:

    php artisan migrate

<a name="routing"></a>
## Routing

To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them.

<a name="requesting-the-password-reset-link"></a>
### Requesting The Password Reset Link

<a name="the-password-reset-link-request-form"></a>
#### The Password Reset Link Request Form

First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form:

    Route::get('/forgot-password', function () {
        return view('auth.forgot-password');
    })->middleware(['guest'])->name('password.request');

The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address.

<a name="password-reset-link-handling-the-form-submission"></a>
#### Handling The Form Submission

Next, we will define a route will handle the form request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user:

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Password;

    Route::post('/forgot-password', function (Request $request) {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        return $status === Password::RESET_LINK_SENT
                    ? back()->with(['status' => __($status)])
                    : back()->withErrors(['email' => __($status)]);
    })->middleware(['guest'])->name('password.email');

Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/{{version}}/notifications).

The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/{{version}}/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `resources/lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file.

> {tip} When manually implementing password resets, you are required to define the contents of the views and routes yourself. If you would like scaffolding that includes all necessary authentication and verification logic, check out [Laravel Jetstream](https://jetstream.laravel.com).

<a name="resetting-the-password"></a>
### Resetting The Password

<a name="the-password-reset-form"></a>
#### The Password Reset Form

Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request:

    Route::get('/reset-password/{token}', function ($token) {
        return view('auth.reset-password', ['token' => $token]);
    })->middleware(['guest'])->name('password.reset');

The view that is returned by this route should have a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret token received by our route.

<a name="password-reset-handling-the-form-submission"></a>
#### Handling The Form Submission

Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database:

    use Illuminate\Auth\Events\PasswordReset;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Support\Facades\Password;
    use Illuminate\Support\Str;

    Route::post('/reset-password', function (Request $request) {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|min:8|confirmed',
        ]);

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function ($user, $password) use ($request) {
                $user->forceFill([
                    'password' => Hash::make($password)
                ])->save();

                $user->setRememberToken(Str::random(60));

                event(new PasswordReset($user));
            }
        );

        return $status == Password::PASSWORD_RESET
                    ? redirect()->route('login')->with('status', __($status))
                    : back()->withErrors(['email' => __($status)]);
    })->middleware(['guest'])->name('password.update');

Before moving on, let's examine this route in more detail. First, the request's `token`, `email`, and `password` attributes are validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to validate the password reset request credentials.

If the token, email address, and password given to the password broker are valid, the Closure passed to the `reset` method will be invoked. Within this Closure, which receives the user instance and the plain-text password, we may update the user's password in the database.

The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/{{version}}/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `resources/lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file.

<a name="password-customization"></a>
## Customization

<a name="reset-link-customization"></a>
#### Reset Link Customization

You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a Closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from a service provider's `boot` method:

    use Illuminate\Auth\Notifications\ResetPassword;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        ResetPassword::createUrlUsing(function ($notifiable, string $token) {
            return 'https://example.com/auth/reset-password?token='.$token;
        });
    }

<a name="reset-email-customization"></a>
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
