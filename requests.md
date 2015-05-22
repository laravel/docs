# HTTP Requests

- [Accessing The Request](#accessing-the-request)
- [Retrieving Input](#retrieving-input)
	- [Old Input](#old-input)
	- [Cookies](#cookies)
	- [Files](#files)
- [Other Request Information](#other-request-information)

<a name="accessing-the-request"></a>
## Accessing The Request

To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your controller constructor or method. The current request instance will automatically be injected by the [service container](/docs/{{version}}/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}
	}

If your controller method is also expecting input from a route parameter, simply list your route arguments after your other dependencies. For example, if your route is defined like so:

	Route::put('user/{id}', 'UserController@update');

You may still type-hint the `Illuminate\Http\Request` and access your route parameter `id` by defining your controller method like the following:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}
	}

<a name="retrieving-input"></a>
## Retrieving Input

#### Retrieving An Input Value

Using a few simple methods, you may access all user input from your `Illuminate\Http\Request` instance. You do not need to worry about the HTTP verb used for the request, as input is accessed in the same way for all verbs.

	$name = $request->input('name');

You may pass a default value as the second argument to the `input` method. This value will be returned if the requested input value is not present on the request:

	$name = $request->input('name', 'Sally');

#### Determining If An Input Value Is Present

To determine if a value is present on the request, you may use the `has` method. The `has` method returns `true` if the value is present **and** is not an empty string:

	if ($request->has('name')) {
		//
	}

#### Retrieving All Input Data

You may also retrieve all of the input data as an `array` using the `all` method:

	$input = $request->all();

#### Retrieving A Portion Of The Input Data

If you need to retrieve a sub-set of the input data, you may use the `only` and `except` methods. Both of these methods accept a single `array` as their only argument:

	$input = $request->only('username', 'password');

	$input = $request->except('credit_card');

#### Retrieving Array Input

When working on forms with array inputs, you may use "dot" notation to access the arrays:

	$input = $request->input('products.0.name');

<a name="old-input"></a>
### Old Input

Laravel allows you to keep input from one request during the next request. This feature is particularly useful for re-populating forms after detecting validation errors.

#### Flashing Input To The Session

The `flash` method on the `Illuminate\Http\Request` instance will flash the current input to the [session](/docs/{{version}}/session) so that it is available during the user's next request to the application:

	$request->flash();

You may also use the `flashOnly` and `flashExcept` methods to flash a sub-set of the request data into the session:

	$request->flashOnly('username', 'email');

	$request->flashExcept('password');

#### Flash Input Into Session Then Redirect

Since you often will want to flash input in association with a redirect to the previous page, you may easily chain input flashing onto a redirect using the `withInput` method:

	return redirect('form')->withInput();

	return redirect('form')->withInput($request->except('password'));

#### Retrieving Old Data

To retrieve flashed input from the previous request, use the `old` method on the `Request` instance. The `old` method provides a convenient helper for pulling the flashed input data out of the [session](/docs/{{version}}/session):

	$username = $request->old('username');

Laravel also provides a global `old` helper function. If you are displaying old input within a [Blade template](/docs/{{version}}/views), it is more convenient to use the `old` helper:

	{{ old('username') }}

<a name="cookies"></a>
### Cookies

#### Retrieving Cookies From The Request

All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client. To retrieve a cookie value from the request, you may use the `cookie` method on the `Illuminate\Http\Request` instance:

	$value = $request->cookie('name');

#### Attaching A New Cookie To A Response

Laravel provides a global `cookie` helper function which serves as a simple factory for generating new `Symfony\Component\HttpFoundation\Cookie` instances. The cookies may be attached to a `Illuminate\Http\Response` instance using the `withCookie` method:

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

	return $response;

To create a long-lived cookie, which lasts for five years, you may use the `forever` method on the cookie factory by first calling the `cookie` helper with no arguments, and then chaining the `forever` method onto the returned cookie factory:

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="files"></a>
### Files

#### Retrieving An Uploaded File

	$file = $request->file('photo');

#### Determining If A File Was Uploaded

	if ($request->hasFile('photo'))
	{
		//
	}

The object returned by the `file` method is an instance of the `Symfony\Component\HttpFoundation\File\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file.

#### Determining If An Uploaded File Is Valid

	if ($request->file('photo')->isValid())
	{
		//
	}

#### Moving An Uploaded File

	$request->file('photo')->move($destinationPath);

	$request->file('photo')->move($destinationPath, $fileName);

#### Other File Methods

There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/File/UploadedFile.html) for more information regarding these methods.

<a name="other-request-information"></a>
## Other Request Information

The `Request` class provides many methods for examining the HTTP request for your application and extends the `Symfony\Component\HttpFoundation\Request` class. Here are some of the highlights.

#### Retrieving The Request URI

	$uri = $request->path();

#### Retrieving The Request Method

	$method = $request->method();

	if ($request->isMethod('post'))
	{
		//
	}

#### Determining If The Request Path Matches A Pattern

	if ($request->is('admin/*'))
	{
		//
	}

#### Get The Current Request URL

	$url = $request->url();
