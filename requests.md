# HTTP Requests

- [Obtaining A Request Instance](#obtaining-a-request-instance)
- [Retrieving Input](#retrieving-input)
- [Old Input](#old-input)
- [Cookies](#cookies)
- [Files](#files)
- [Other Request Information](#other-request-information)

<a name="obtaining-a-request-instance"></a>
## Obtaining A Request Instance

### Via Facade

The `Request` facade will grant you access to the current request that is bound in the container. For example:

	$name = Request::input('name');

Remember, if you are in a namespace, you will have to import the `Request` facade using a `use Request;` statement at the top of your class file.

### Via Dependency Injection

To obtain an instance of the current HTTP request via dependency injection, you should type-hint the class on your controller constructor or method. The current request instance will automatically be injected by the [service container](/docs/{{version}}/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

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

If your controller method is also expecting input from a route parameter, simply list your route arguments after your other dependencies:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Update the specified user.
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

	$name = Request::input('name');

#### Retrieving A Default Value If The Input Value Is Absent

	$name = Request::input('name', 'Sally');

#### Determining If An Input Value Is Present

	if (Request::has('name'))
	{
		//
	}

#### Getting All Input For The Request

	$input = Request::all();

#### Getting Only Some Of The Request Input

	$input = Request::only('username', 'password');

	$input = Request::except('credit_card');

When working on forms with "array" inputs, you may use dot notation to access the arrays:

	$input = Request::input('products.0.name');

<a name="old-input"></a>
## Old Input

Laravel also allows you to keep input from one request during the next request. For example, you may need to re-populate a form after checking it for validation errors.

#### Flashing Input To The Session

The `flash` method will flash the current input to the [session](/docs/{{version}}/session) so that it is available during the user's next request to the application:

	Request::flash();

#### Flashing Only Some Input To The Session

	Request::flashOnly('username', 'email');

	Request::flashExcept('password');

#### Flash & Redirect

Since you often will want to flash input in association with a redirect to the previous page, you may easily chain input flashing onto a redirect.

	return redirect('form')->withInput();

	return redirect('form')->withInput(Request::except('password'));

#### Retrieving Old Data

To retrieve flashed input from the previous request, use the `old` method on the `Request` instance.

	$username = Request::old('username');

If you are displaying old input within a Blade template, it is more convenient to use the `old` helper:

	{{ old('username') }}

<a name="cookies"></a>
## Cookies

All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client.

#### Retrieving A Cookie Value

	$value = Request::cookie('name');

#### Attaching A New Cookie To A Response

The `cookie` helper serves as a simple factory for generating new `Symfony\Component\HttpFoundation\Cookie` instances. The cookies may be attached to a `Response` instance using the `withCookie` method:

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

#### Creating A Cookie That Lasts Forever*

_By "forever", we really mean five years._

	$response->withCookie(cookie()->forever('name', 'value'));

#### Queueing Cookies

You may also "queue" a cookie to be added to the outgoing response, even before that response has been created:

	<?php namespace App\Http\Controllers;

	use Cookie;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Update a resource
		 *
		 * @return Response
		 */
		 public function update()
		 {
		 	Cookie::queue('name', 'value');

		 	return response('Hello World');
		 }
	}

<a name="files"></a>
## Files

#### Retrieving An Uploaded File

	$file = Request::file('photo');

#### Determining If A File Was Uploaded

	if (Request::hasFile('photo'))
	{
		//
	}

The object returned by the `file` method is an instance of the `Symfony\Component\HttpFoundation\File\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file.

#### Determining If An Uploaded File Is Valid

	if (Request::file('photo')->isValid())
	{
		//
	}

#### Moving An Uploaded File

	Request::file('photo')->move($destinationPath);

	Request::file('photo')->move($destinationPath, $fileName);

### Other File Methods

There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/File/UploadedFile.html) for more information regarding these methods.

<a name="other-request-information"></a>
## Other Request Information

The `Request` class provides many methods for examining the HTTP request for your application and extends the `Symfony\Component\HttpFoundation\Request` class. Here are some of the highlights.

#### Retrieving The Request URI

	$uri = Request::path();
	
#### Determine If The Request Is Using AJAX

	if (Request::ajax())
	{
		//
	}

#### Retrieving The Request Method

	$method = Request::method();

	if (Request::isMethod('post'))
	{
		//
	}

#### Determining If The Request Path Matches A Pattern

	if (Request::is('admin/*'))
	{
		//
	}

#### Get The Current Request URL

	$url = Request::url();
