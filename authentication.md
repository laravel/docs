# Authentication

- [Introduction](#introduction)
- [Included Authentication Controllers](#included-authentication-controllers)
- [Manually Authenticating Users](#authenticating-users)
- [Retrieving The Authenticated User](#retrieving-the-authenticated-user)
- [Protecting Routes](#protecting-routes)
- [HTTP Basic Authentication](#http-basic-authentication)
- [Password Reminders & Reset](#password-reminders-and-reset)
- [Social Authentication](#social-authentication)
- [Adding Custom Authentication Drivers](#adding-custom-authentication-drivers)

<a name="introduction"></a>
## Introduction

Laravel makes implementing authentication very simple. In fact, almost everything is configured for you out of the box. The authentication configuration file is located at `config/auth.php`, which contains several well documented options for tweaking the behavior of the authentication services.

By default, Laravel includes an `App\User` [Eloquent model](/docs/{{version}}/eloquent) in your `app` directory. This model may be used with the default Eloquent authentication driver.

### Database Considerations

When building the database schema for this model, make the password column at least 60 characters.

Also, before getting started, make sure that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for "remember me" sessions being maintained by your application. This can be done by using `$table->rememberToken();` in a migration. The `scaffold:auth` command will generate these migrations for you.

> **Note:** If your application is not using Eloquent, you may use the `database` authentication driver which uses the Laravel query builder.

<a name="included-authentication-controllers"></a>
## Included Authentication Controllers

Laravel ships with two authentication controllers out of the box. These controllers are located in the `App\Http\Controllers\Auth` namespace. The `AuthController` handles new user registration and authentication, while the `PasswordController` contains the logic to help existing users reset their forgotten passwords.

Each of these controllers uses a trait to include their necessary methods. For many applications, you will not need to modify these controllers at all.

However, you will need to provide [views](/docs/{{version}}/views) that these controllers can render. The views should be placed in `resources/views/auth` directory. You are free to customize these views however you wish. The login view should be placed at `resources/auth/login.blade.php`, and the registration view should be placed at `resources/auth/register.blade.php`.

#### Sample Authentication Form

    <!-- resources/auth/login.blade.php -->

    <form method="POST" action="/auth/login">
        {{ csrf_field() }}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password" id="password">
        </div>

        <div>
            <input type="checkbox" name="remember"> Remember Me
        </div>

        <div>
            <button type="submit">Login</button>
        </div>
    </form>

#### Sample Registration Form

    <!-- resources/auth/register.blade.php -->

    <form method="POST" action="/auth/register">
        {{ csrf_field() }}

        <div class="col-md-6">
            Name
            <input type="text" name="name" value="{{ old('name') }}">
        </div>

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div class="col-md-6">
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">Register</button>
        </div>
    </form>

### After Authentication

If a user is successfully authenticated, they will be redirected to the `/home` URI. You will need to register a route to handle this URI.

You can customize the post-authentication redirect location by defining a `redirectTo` property on the `AuthController`:

    protected $redirectTo = '/dashboard';

### Customizing New User Validation

To modify the form fields that are required when a new user registers with your application, you may modify the `AuthController` class. This class is responsible for validating and creating new users of your application.

The `validator` method of the `AuthController` contains the validation rules for new users of the application. You are free to modify this method as you wish.

### Customizing New User Storage

The `create` method of the `AuthController` is responsible for creating new `User` records in your database. You are free to modify this method according to the needs of your database.

<a name="authenticating-users"></a>
## Manually Authenticating Users

Of course, you are not required to use the authentication controllers included with Laravel. If you choose to remove these controllers, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! First, let's check out the `attempt` method.

We will access Laravel's authentication services via the `Auth` [facade](/docs/{{version}}/facades), so we'll need to make sure to import the `Auth` facade at the top of the class.

    <?php namespace App\Http\Controllers;

    use Auth;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Handle an authentication attempt.
         *
         * @return Response
         */
        public function authenticate()
        {
            if (Auth::attempt(['email' => $email, 'password' => $password])) {
                // Authentication passed...
                return redirect()->intended('dashboard');
            }
        }
    }

The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the hashed `password` value passed to the method via the array. If the two hashed passwords match an authenticated session will be started for the user.

The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned.

> **Note:** In this example, `email` is not a required option, it is merely used as an example. You should use whatever column name corresponds to a "username" in your database.

The `intended` redirect function will redirect the user to the URL they were attempting to access before being caught by the authentication filter. A fallback URI may be given to this method in case the intended destination is not available.

#### Authenticating A User With Conditions

You also may add extra conditions to the authentication query:

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        // The user is active, not suspended, and exists.
    }

#### Determining If A User Is Authenticated

To determine if the user is already logged into your application, you may use the `check` method:

    if (Auth::check()) {
        // The user is logged in...
    }

However, you may use middleware to verify that the user is authenticated before allowing the user access to certain routes / controllers. To learn more about this, check out the documentation on [protecting routes](/docs/{{version}}/authentication#protecting-routes).

#### Authenticating A User And "Remembering" Them

If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method, which will keep the user authenticated indefinitely, or until they manually logout. Of course, your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token.

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // The user is being remembered...
    }

If you are "remembering" users, you may use the `viaRemember` method to determine if the user was authenticated using the "remember me" cookie:

    if (Auth::viaRemember()) {
        //
    }

#### Authenticating Users By ID

To log a user into the application by their ID, use the `loginUsingId` method:

    Auth::loginUsingId(1);

#### Validating User Credentials Without Login

The `validate` method allows you to validate a user's credentials without actually logging them into the application:

    if (Auth::validate($credentials)) {
        //
    }

#### Logging A User In For A Single Request

You may also use the `once` method to log a user into the application for a single request. No sessions or cookies will be utilized:

    if (Auth::once($credentials)) {
        //
    }

The `once` method is primarily useful for building stateless APIs.

#### Manually Logging In A User

If you need to log an existing user instance into your application, you may call the `login` method with the user instance:

    Auth::login($user);

This is equivalent to logging in a user via credentials using the `attempt` method.

#### Logging A User Out Of The Application

    Auth::logout();

<a name="retrieving-the-authenticated-user"></a>
## Retrieving The Authenticated User

You may access the authenticated user via the `Auth` facade:

    $user = Auth::user();

Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance:

    <?php namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class ProfileController extends Controller
    {
        /**
         * Update the user's profile.
         *
         * @return Response
         */
        public function updateProfile(Request $request)
        {
            if ($request->user()) {
                // $request->user() returns an instance of the authenticated user...
            }
        }
    }

<a name="protecting-routes"></a>
## Protecting Routes

[Route middleware](/docs/{{version}}/middleware) can be used to allow only authenticated users to access a given route. Laravel ships with the `auth` middleware, which is defined in `app\Http\Middleware\Authenticate.php`. All you need to do is attach it to a route definition:

    // Using A Route Closure...

    Route::get('profile', ['middleware' => 'auth', function() {
        // Only authenticated users may enter...
    }]);

    // Using A Controller...

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'ProfileController@show'
    ]);

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication

HTTP Basic Authentication provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` middleware to your route:

#### Protecting A Route With HTTP Basic

    Route::get('profile', ['middleware' => 'auth.basic', function() {
        // Only authenticated users may enter...
    }]);

By default, the `auth.basic` middleware will use the `email` column on the user record as the "username".

#### Setting Up A Stateless HTTP Basic Filter

You may also use HTTP Basic Authentication without setting a user identifier cookie in the session, which is particularly useful for API authentication. To do so, [define a middleware](/docs/{{version}}/middleware) that calls the `onceBasic` method:

    public function handle($request, Closure $next)
    {
        return Auth::onceBasic() ?: $next($request);
    }

Next, just [register the middleware](/docs/{{version}}/middleware#registering-middleware) and attach it to a route.

If you are using PHP FastCGI, HTTP Basic authentication may not work correctly out of the box. The following lines should be added to your `.htaccess` file:

    RewriteCond %{HTTP:Authorization} ^(.+)$
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## Password Reminders & Reset

### Model & Table

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

To get started, verify that your `User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. Of course, the `User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

#### Generating The Reminder Table Migration

Next, a table must be created to store the password reset tokens. The migration for this table is included with Laravel out of the box, and resides in the `database/migrations` directory. So all you need to do is migrate:

    php artisan migrate

### Password Reminder Controller

Laravel includes an `Auth\PasswordController` that contains the logic necessary to reset user passwords.

#### Sample Password Reset Request Form

You will simply need to provide an HTML view for the password reset request form. This view should be placed at `resources/views/auth/password.blade.php` Here is a sample form to get you started:

    <!-- resources/views/auth/password.blade.php -->

    <form method="POST" action="/password/email">
        {{ csrf_field() }}

        <div>
        	Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <button type="submit">
                Send Password Reset Link
            </button>
        </div>
    </form>

When a user submits a request to reset their password, they will receive an e-mail with a link that points to the `getReset` method of the `PasswordController`. You will need to create a view for this e-mail at `resources/views/emails/password.blade.php`. The view will receive the `$token` variable which contains the password reset token to match the user to the password reset request. Here is an example view to get you started:

    Click here to reset your password: {{ url('password/reset/'.$token) }}

#### Sample Password Reset Form

When the user clicks the e-mailed link to reset their password, they will be presented with a password reset form. This view should be placed at `resources/views/auth/reset.blade.php`.

Here is a sample password reset form to get you started:

    <!-- resources/views/auth/reset.blade.php -->

    <form method="POST" action="/password/reset">
        {{ csrf_field() }}
        <input type="hidden" name="token" value="{{ $token }}">

        <div>
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <input type="password" name="password">
        </div>

        <div>
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">
                Reset Password
            </button>
        </div>
    </form>

After the password is reset, the user will automatically be logged into the application and redirected to `/home`. You can customize the post-reset redirect location by defining a `redirectTo` property on the `PasswordController`:

    protected $redirectTo = '/dashboard';

> **Note:** By default, password reset tokens expire after one hour. You may change this via the `reminder.expire` option in your `config/auth.php` file.

<a name="social-authentication"></a>
## Social Authentication

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). **Socialite currently supports authentication with Facebook, Twitter, Google, GitHub and Bitbucket.**

### Installation

To get started with Socialite, include the package in your `composer.json` file:

    "laravel/socialite": "~2.0"

Next, register the `Laravel\Socialite\SocialiteServiceProvider` in your `config/app.php` configuration file. Also, add the `Socialite` facade to the `aliases` array in your `app` configuration file:

    'Socialite' => 'Laravel\Socialite\Facades\Socialite',

You will need to add credentials for the OAuth services your application utilizes. These credentials should be placed in your `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `google`, or `github`, depending on the providers your application requires. For example:

    'github' => [
        'client_id' => 'your-github-app-id',
        'client_secret' => 'your-github-app-secret',
        'redirect' => 'http://your-callback-url',
    ],

### Basic Usage

Next, you are ready to authenticate users! You will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. We will access Socialite using the `Socialite` [facade](/docs/{{version}}/facades):

    <?php namespace App\Http\Controllers;

    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Redirect the user to the GitHub authentication page.
         *
         * @return Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * Obtain the user information from GitHub.
         *
         * @return Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

The `redirect` method takes care of sending the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider. Before redirecting the user, you may also set "scopes" on the request:

    return Socialite::driver('github')
                ->scopes(['scope1', 'scope2'])->redirect();

> **Note:** Using `scopes` method will overwrite default scope `email`. If you want to get user's email, you should add it to scopes manually.

Once you have a user instance, you can grab a few more details about the user:

#### Retrieving User Details

    $user = $this->socialite->driver('github')->user();

    // OAuth Two Providers
    $token = $user->token;

    // OAuth One Providers
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All Providers
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

<a name="adding-custom-authentication-drivers"></a>
## Adding Custom Authentication Drivers

Authentication may be extended the same way as the cache and session facilities. Again, we will use the `extend` method used to extend other parts of the framework. You should place this call to `extend` within a [service provider](/docs/{{version}}/providers):

    <?php namespace App\Providers;

    use Auth;
    use App\Extensions\RiakUserProvider;
    use Illuminate\Support\ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Auth::extend('riak', function($app) {
                // Return an instance of Illuminate\Contracts\Auth\UserProvider...
                return new RiakUserProvider($app['riak.connection']);
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

The `UserProvider` implementations are only responsible for fetching a `Illuminate\Contracts\Auth\Authenticatable` implementation out of a persistent storage system, such as MySQL, Riak, etc. These two interfaces allow the Laravel authentication mechanisms to continue functioning regardless of how the user data is stored or what type of class is used to represent it.

Let's take a look at the `UserProvider` contract:

    interface UserProvider {

        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);

    }

The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method.

The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, stored in a field `remember_token`. As with the previous method, the `Authenticatable` implementation should be returned.

The `updateRememberToken` method updates the `$user` field `remember_token` with the new `$token`. The new token can be either a fresh token, assigned on successful "remember me" login attempt, or a null when user is logged out.

The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to sign into an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition on `$credentials['username']`. The method should then return an implementation of `UserInterface`. **This method should not attempt to do any password validation or authentication.**

The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method might compare the `$user->getAuthPassword()` string to a `Hash::make` of `$credentials['password']`. This method should only validate the user's credentials and return boolean.

Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable`. Remember, the provider should return implementations of this interface from the `retrieveById` and `retrieveByCredentials` methods:

    interface Authenticatable {

        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();

    }

This interface is simple. The `getAuthIdentifier` method should return the "primary key" of the user. In a MySQL back-end, again, this would be the auto-incrementing primary key. The `getAuthPassword` should return the user's hashed password. This interface allows the authentication system to work with any User class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes a `User` class in the `app` directory which implements this interface, so you may consult this class for an implementation example.

Finally, once we have implemented the `UserProvider`, we are ready to register our extension with the `Auth` facade:

    Auth::extend('riak', function($app) {
        return new RiakUserProvider($app['riak.connection']);
    });

After you have registered the driver with the `extend` method, you may switch to the new driver in your `config/auth.php` configuration file.
