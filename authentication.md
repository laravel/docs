# Authentication

- [Introduction](#introduction)
- [Authenticating Users](#authenticating-users)
- [Retrieving The Authenticated User](#retrieving-the-authenticated-user)
- [Protecting Routes](#protecting-routes)
- [HTTP Basic Authentication](#http-basic-authentication)
- [Password Reminders & Reset](#password-reminders-and-reset)
- [Social Authentication](#social-authentication)

<a name="introduction"></a>
## Introduction

Laravel makes implementing authentication very simple. In fact, almost everything is configured for you out of the box. The authentication configuration file is located at `config/auth.php`, which contains several well documented options for tweaking the behavior of the authentication services.

By default, Laravel includes an `App\User` model in your `app` directory. This model may be used with the default Eloquent authentication driver.

Remember: when building the database schema for this model, make the password column at least 60 characters. Also, before getting started, make sure that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for "remember me" sessions being maintained by your application. This can be done by using `$table->rememberToken();` in a migration. Of course, Laravel 5 ships migrations for these columns out of the box!

If your application is not using Eloquent, you may use the `database` authentication driver which uses the Laravel query builder.

<a name="authenticating-users"></a>
## Authenticating Users

Laravel ships with two authentication related controllers out of the box. The `AuthController` handles new user registration and "logging in", while the `PasswordController` contains the logic to help existing users reset their forgotten passwords.

Each of these controllers uses a trait to include their necessary methods. For many applications, you will not need to modify these controllers at all. The views that these controllers render are located in the `resources/views/auth` directory. You are free to customize these views however you wish.

### The User Registrar

To modify the form fields that are required when a new user registers with your application, you may modify the `App\Services\Registrar` class. This class is responsible for validating and creating new users of your application.

The `validator` method of the `Registrar` contains the validation rules for new users of the application, while the `create` method of the `Registrar` is responsible for creating new `User` records in your database. You are free to modify each of these methods as you wish. The `Registrar` is called by the `AuthController` via the methods contained in the `AuthenticatesAndRegistersUsers` trait.

#### Manual Authentication

If you choose not to use the provided `AuthController` implementation, you will need to manage the authentication of your users using the Laravel authentication classes directly. Don't worry, it's still a cinch! First, let's check out the `attempt` method:

	<?php namespace App\Http\Controllers;

	use Auth;
	use Illuminate\Routing\Controller;

	class AuthController extends Controller {

		/**
		 * Handle an authentication attempt.
		 *
		 * @return Response
		 */
		public function authenticate()
		{
			if (Auth::attempt(['email' => $email, 'password' => $password]))
			{
				return redirect()->intended('dashboard');
			}
		}

	}

The `attempt` method accepts an array of key / value pairs as its first argument. The `password` value will be [hashed](/docs/{{version}}/hashing). The other values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the hashed `password` value passed to the method via the array. If the two hashed passwords match, a new authenticated session will be started for the user.

The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned.

> **Note:** In this example, `email` is not a required option, it is merely used as an example. You should use whatever column name corresponds to a "username" in your database.

The `intended` redirect function will redirect the user to the URL they were attempting to access before being caught by the authentication filter. A fallback URI may be given to this method in case the intended destination is not available.

#### Authenticating A User With Conditions

You also may add extra conditions to the authentication query:

	if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1]))
	{
		// The user is active, not suspended, and exists.
	}

#### Determining If A User Is Authenticated

To determine if the user is already logged into your application, you may use the `check` method:

	if (Auth::check())
	{
		// The user is logged in...
	}

#### Authenticating A User And "Remembering" Them

If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method, which will keep the user authenticated indefinitely, or until they manually logout. Of course, your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token.

	if (Auth::attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

If you are "remembering" users, you may use the `viaRemember` method to determine if the user was authenticated using the "remember me" cookie:

	if (Auth::viaRemember())
	{
		//
	}

#### Authenticating Users By ID

To log a user into the application by their ID, use the `loginUsingId` method:

	Auth::loginUsingId(1);

#### Validating User Credentials Without Login

The `validate` method allows you to validate a user's credentials without actually logging them into the application:

	if (Auth::validate($credentials))
	{
		//
	}

#### Logging A User In For A Single Request

You may also use the `once` method to log a user into the application for a single request. No sessions or cookies will be utilized:

	if (Auth::once($credentials))
	{
		//
	}

#### Manually Logging In A User

If you need to log an existing user instance into your application, you may call the `login` method with the user instance:

	Auth::login($user);

This is equivalent to logging in a user via credentials using the `attempt` method.

#### Logging A User Out Of The Application

	Auth::logout();

Of course, if you are using the built-in Laravel authentication controllers, a controller method that handles logging users out of the application is provided out of the box.

#### Authentication Events

When the `attempt` method is called, the `auth.attempt` [event](/docs/{{version}}/events) will be fired. If the authentication attempt is successful and the user is logged in, the `auth.login` event will be fired as well.

<a name="retrieving-the-authenticated-user"></a>
## Retrieving The Authenticated User

Once a user is authenticated, there are several ways to obtain an instance of the User.

First, you may access the user from the `Auth` facade:

	<?php
	
	namespace App\Http\Controllers;
	
	use Auth;
	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile()
		{
			if (Auth::user())
			{
				// Auth::user() returns an instance of the authenticated user...
			}
		}

	}

Second, you may access the authenticated user via an `Illuminate\Http\Request` instance:

	<?php
	
	namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Request $request)
		{
			if ($request->user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

Thirdly, you may type-hint the `Illuminate\Contracts\Auth\Authenticatable` contract. This type-hint may be added to a controller constructor, controller method, or any other constructor of a class resolved by the [service container](/docs/{{version}}/container):

	<?php
	
	namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\Authenticatable;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Authenticatable $user)
		{
			// $user is an instance of the authenticated user...
		}

	}

<a name="protecting-routes"></a>
## Protecting Routes

[Route middleware](/docs/{{version}}/middleware) can be used to allow only authenticated users to access a given route. Laravel provides the `auth` middleware by default, and it is defined in `app\Http\Middleware\Authenticate.php`. All you need to do is attach it to a route definition:

	// With A Route Closure...

	Route::get('profile', ['middleware' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// With A Controller...

	Route::get('profile', ['middleware' => 'auth', 'uses' => 'ProfileController@show']);

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication

HTTP Basic Authentication provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` middleware to your route:

#### Protecting A Route With HTTP Basic

	Route::get('profile', ['middleware' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

By default, the `basic` middleware will use the `email` column on the user record as the "username".

#### Setting Up A Stateless HTTP Basic Filter

You may also use HTTP Basic Authentication without setting a user identifier cookie in the session, which is particularly useful for API authentication. To do so, [define a middleware](/docs/{{version}}/middleware) that calls the `onceBasic` method:

	public function handle($request, Closure $next)
	{
		return Auth::onceBasic() ?: $next($request);
	}

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

Laravel also includes an `Auth\PasswordController` that contains the logic necessary to reset user passwords. We've even provided views to get you started! The views are located in the `resources/views/auth` directory. You are free to modify these views as you wish to suit your own application's design.

Your user will receive an e-mail with a link that points to the `getReset` method of the `PasswordController`. This method will render the password reset form and allow users to reset their passwords. After the password is reset, the user will automatically be logged into the application and redirected to `/home`. You can customize the post-reset redirect location by defining a `redirectTo` property on the `PasswordController`:

	protected $redirectTo = '/dashboard';

> **Note:** By default, password reset tokens expire after one hour. You may change this via the `reminder.expire` option in your `config/auth.php` file.

<a name="social-authentication"></a>
## Social Authentication

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). **Socialite currently supports authentication with Facebook, Twitter, Google, GitHub and Bitbucket.**

To get started with Socialite, include the package in your `composer.json` file:

	"laravel/socialite": "~2.0"

Next, register the `Laravel\Socialite\SocialiteServiceProvider` in your `config/app.php` configuration file. You may also register a [facade](/docs/{{version}}/facades):

	'Socialize' => 'Laravel\Socialite\Facades\Socialite',

You will need to add credentials for the OAuth services your application utilizes. These credentials should be placed in your `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `google`, or `github`, depending on the providers your application requires. For example:

	'github' => [
		'client_id' => 'your-github-app-id',
		'client_secret' => 'your-github-app-secret',
		'redirect' => 'http://your-callback-url',
	],

Next, you are ready to authenticate users! You will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. Here's an example using the `Socialize` facade:

	public function redirectToProvider()
	{
		return Socialize::with('github')->redirect();
	}

	public function handleProviderCallback()
	{
		$user = Socialize::with('github')->user();

		// $user->token;
	}

The `redirect` method takes care of sending the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider. Before redirecting the user, you may also set "scopes" on the request:

	return Socialize::with('github')->scopes(['scope1', 'scope2'])->redirect();

Once you have a user instance, you can grab a few more details about the user:

#### Retrieving User Details

	$user = Socialize::with('github')->user();

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
