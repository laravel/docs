# Authentication

- [Introduction](#introduction)
- [Authenticating Users](#authenticating-users)
- [Retrieving The Authenticated User](#retrieving-the-authenticated-user)
- [Protecting Routes](#protecting-routes)
- [HTTP Basic Authentication](#http-basic-authentication)
- [Password Reminders & Reset](#password-reminders-and-reset)
- [Authentication Drivers](#authentication-drivers)

<a name="introduction"></a>
## Introduction

Laravel makes implementing authentication very simple. In fact, almost everything is configured for you out of the box. The authentication configuration file is located at `config/auth.php`, which contains several well documented options for tweaking the behavior of the authentication services.

By default, Laravel includes an `App\User` model in your `app` directory. This model may be used with the default Eloquent authentication driver. Remember: when building the database schema for this model, make the password column at least 60 characters.

If your application is not using Eloquent, you may use the `database` authentication driver which uses the Laravel query builder.

> **Note:** Before getting started, make sure that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for "remember me" sessions being maintained by your application. This can be done by using `$table->rememberToken();` in a migration.

<a name="authenticating-users"></a>
## Authenticating Users

To authenticate users, you will need to obtain an implementation of the `Illuminate\Contracts\Auth\Guard` [contract](/docs/master/contracts). This contract provides methods for validating user credentials and managing authenticated user sessions.

Of course, you can use Laravel's automatic [dependency injection](/docs/master/container) to obtain an implementation of the contract. Once we have the `Guard` instance, we can use the `attempt` method to log users into the application:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\Guard;

	class AuthController extends Controller {

		/**
		 * The authenticator implementation.
		 */
		protected $auth;

		/**
		 * Create a new controller instance.
		 *
		 * @param  Guard  $auth
		 * @return void
		 */
		public function __construct(Guard $auth)
		{
			$this->auth = $auth;
		}

		/**
		 * Handle an authentication attempt.
		 *
		 * @return Response
		 */
		public function authenticate()
		{
			if ($this->auth->attempt(['email' => $email, 'password' => $password]))
			{
				return redirect()->intended('dashboard');
			}
		}

	}

The `attempt` method accepts an array of key / value pairs as its first argument. The `password` value will be [hashed](/docs/master/hashing). The other values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the hashed `password` value passed to the method via the array. If the two hashed passwords match, the `Guard` will begin an authenticated session for the user.

The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned.

> **Note:** In this example, `email` is not a required option, it is merely used as an example. You should use whatever column name corresponds to a "username" in your database.

The `intended` redirect function will redirect the user to the URL they were attempting to access before being caught by the authentication filter. A fallback URI may be given to this method in case the intended destination is not available.

#### Authenticating A User With Conditions

You also may add extra conditions to the authentication query:

    if ($this->auth->attempt(['email' => $email, 'password' => $password, 'active' => 1]))
    {
        // The user is active, not suspended, and exists.
    }

#### Determining If A User Is Authenticated

To determine if the user is already logged into your application, you may use the `check` method on the `Guard` implementation:

	if ($this->auth->check())
	{
		// The user is logged in...
	}

#### Authenticating A User And "Remembering" Them

If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method, which will keep the user authenticated indefinitely, or until they manually logout. Of course, your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token.

	if ($this->auth->attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

If you are "remembering" users, you may use the `viaRemember` method to determine if the user was authenticated using the "remember me" cookie:

	if ($this->auth->viaRemember())
	{
		//
	}

#### Authenticating Users By ID

To log a user into the application by their ID, use the `loginUsingId` method:

	$this->auth->loginUsingId(1);

#### Validating User Credentials Without Login

The `validate` method allows you to validate a user's credentials without actually logging them into the application:

	if ($this->auth->validate($credentials))
	{
		//
	}

#### Logging A User In For A Single Request

You may also use the `once` method to log a user into the application for a single request. No sessions or cookies will be utilized:

	if ($this->auth->once($credentials))
	{
		//
	}

#### Manually Logging In A User

If you need to log an existing user instance into your application, you may call the `login` method with the user instance:

	$this->auth->login($user);

This is equivalent to logging in a user via credentials using the `attempt` method.

#### Logging A User Out Of The Application

	$this->auth->logout();

#### Authentication Events

When the `attempt` method is called, the `auth.attempt` [event](/docs/master/events) will be fired. If the authentication attempt is successful and the user is logged in, the `auth.login` event will be fired as well.

<a name="retrieving-the-authenticated-user"></a>
## Retrieving The Authenticated User

Once a user is authenticated, there are several ways to obtain an instance of the User.

First, you may access the authenticated user via an `Illuminate\Http\Request` instance:

	<?php namespace App\Http\Controllers;

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

Secondly, you may type-hint the `Illuminate\Contracts\Auth\User` contract. This type-hint may be added to a controller constructor, controller method, or any other constructor of a class resolved by the [service container](/docs/master/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\User;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(User $user)
		{
			// $user is an instance of the authenticated user...
		}

	}

<a name="protecting-routes"></a>
## Protecting Routes

[Route filters](/docs/master/filters) can be used to allow only authenticated users to access a given route. Laravel provides the `auth` filter by default, and it is defined in `app\Http\Filters\AuthFilter.php`. All you need to do is attach it to a route definition:

	// With A Route Closure...

	$router->get('profile', ['before' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// With A Controller...

	$router->get('profile', ['before' => 'auth', 'uses' => 'ProfileController@show']);

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication

HTTP Basic Authentication provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` filter to your route:

#### Protecting A Route With HTTP Basic

	$router->get('profile', ['before' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

By default, the `basic` filter will use the `email` column on the user record as the "username". If you wish to use another column, you may pass the column name as the first parameter to the filter in your `App\Http\Filters\BasicAuthFilter` class:

	public function filter(Route $route, Request $request)
	{
		return $this->auth->basic('username');
	};

#### Setting Up A Stateless HTTP Basic Filter

You may also use HTTP Basic Authentication without setting a user identifier cookie in the session, which is particularly useful for API authentication. To do so, [define a filter](/docs/master/filters) that returns the `onceBasic` method:

	public function filter(Route $route, Request $request)
	{
		return $this->auth->onceBasic();
	}

If you are using PHP FastCGI, HTTP Basic authentication may not work correctly out of the box. The following lines should be added to your `.htaccess` file:

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## Password Reminders & Reset

### Model & Table

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

To get started, verify that your `User` model implements the `Illuminate\Contracts\Auth\Remindable` contract. Of course, the `User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Reminders\RemindableTrait` to include the methods needed to implement the interface.

#### Generating The Reminder Table Migration

Next, a table must be created to store the password reset tokens. To generate a migration for this table, simply execute the `auth:reminders-table` Artisan command:

	php artisan auth:reminders-table

	php artisan migrate

### Password Reminder Controller

Now we're ready to generate the password reminder controller. To automatically generate a controller, you may use the `auth:reminders-controller` Artisan command, which will create a `RemindersController.php` file in your `app/Http/Controllers` directory.

	php artisan auth:reminders-controller

The generated controller accepts an implementation of the `Illuminate\Contracts\Auth\PasswordBroker` [contract](/docs/master/contracts). This contract provides a few simple methods that allow you to reset passwords.

The generated controller will also already have a `getRemind` method that handles showing your password reminder form. All you need to do is create a `password.remind` [view](/docs/responses#views). This view should have a basic form with an `email` field. The form should POST to the `RemindersController@postRemind` action.

A simple form on the `password.remind` view might look like this:

	<form action="{{ action('RemindersController@postRemind') }}" method="POST">
		<input type="email" name="email">
		<input type="submit" value="Send Reminder">
	</form>

In addition to `getRemind`, the generated controller will already have a `postRemind` method that handles sending the password reminder e-mails to your users. This method expects the `email` field to be present in the `POST` variables. If the reminder e-mail is successfully sent to the user, a `status` message will be flashed to the session. If the reminder fails, an `error` message will be flashed instead.

Within the `postRemind` controller method, you may modify the message instance before it is sent to the user:

	$result = $this->password->remind($request->only('email'), function($message)
	{
		$message->subject('Password Reminder');
	});

Your user will receive an e-mail with a link that points to the `getReset` method of the controller. The password reminder token, which is used to identify a given password reminder attempt, will also be passed to the controller method.

The action is already configured to return a `password.reset` view which you should build. The `token` will be passed to the view, and you should place this token in a hidden form field named `token`. In addition to the `token`, your password reset form should contain `email`, `password`, and `password_confirmation` fields. The form should POST to the `RemindersController@postReset` method.

A simple form on the `password.reset` view might look like this:

	<form action="{{ action('RemindersController@postReset') }}" method="POST">
		<input type="hidden" name="token" value="{{ $token }}">
		<input type="email" name="email">
		<input type="password" name="password">
		<input type="password" name="password_confirmation">
		<input type="submit" value="Reset Password">
	</form>

Finally, the `postReset` method is responsible for actually changing the password in storage. In this controller action, the Closure passed to the `Password::reset` method sets the `password` attribute on the `User` and calls the `save` method. Of course, this Closure is assuming your `User` model is an [Eloquent model](/docs/eloquent); however, you are free to change this Closure as needed to be compatible with your application's database storage system.

If the password is successfully reset, the user will be redirected to the root of your application. Again, you are free to change this redirect URL. If the password reset fails, the user will be redirect back to the reset form, and an `error` message will be flashed to the session.

### Password Validation

By default, the `$password->reset` method of the `PasswordBroker` will verify that the passwords match and are >= six characters. You may customize these rules using the `$password->validator` method, which accepts a Closure. Within this Closure, you may do any password validation you wish. Note that you are not required to verify that the passwords match, as this will be done automatically by the framework.

	$this->password->validator(function($credentials)
	{
		return strlen($credentials['password']) >= 6;
	});

> **Note:** By default, password reset tokens expire after one hour. You may change this via the `reminder.expire` option of your `config/auth.php` file.

<a name="authentication-drivers"></a>
## Authentication Drivers

Laravel offers the `database` and `eloquent` authentication drivers out of the box. For more information about adding additional authentication drivers, check out the [Authentication extension documentation](/docs/extending#authentication).
