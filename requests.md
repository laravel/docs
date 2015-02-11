# Requests & Input

- [Basic Input](#basic-input)
- [Cookies](#cookies)
- [Old Input](#old-input)
- [Files](#files)
- [Request Information](#request-information)

<a name="basic-input"></a>
## Basic Input

You may access all user input with a few simple methods. You do not need to worry about the HTTP verb used for the request, as input is accessed in the same way for all verbs.

#### Retrieving An Input Value

	$name = Input::get('name');

#### Retrieving A Default Value If The Input Value Is Absent

	$name = Input::get('name', 'Sally');

#### Determining If An Input Value Is Present

	if (Input::has('name'))
	{
		//
	}

#### Getting All Input For The Request

	$input = Input::all();

#### Getting Only Some Of The Request Input

	$input = Input::only('username', 'password');

	$input = Input::except('credit_card');

When working on forms with "array" inputs, you may use dot notation to access the arrays:

	$input = Input::get('products.0.name');

> **Note:** Some JavaScript libraries such as Backbone may send input to the application as JSON. You may access this data via `Input::get` like normal.

<a name="cookies"></a>
## Cookies

All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client.

#### Retrieving A Cookie Value

	$value = Cookie::get('name');

#### Attaching A New Cookie To A Response

	$response = Response::make('Hello World');

	$response->withCookie(Cookie::make('name', 'value', $minutes));

#### Queueing A Cookie For The Next Response

If you would like to set a cookie before a response has been created, use the `Cookie::queue()` method. The cookie will automatically be attached to the final response from your application.

	Cookie::queue($name, $value, $minutes);

#### Creating A Cookie That Lasts Forever

	$cookie = Cookie::forever('name', 'value');

<a name="old-input"></a>
## Old Input

You may need to keep input from one request until the next request. For example, you may need to re-populate a form after checking it for validation errors.

#### Flashing Input To The Session

	Input::flash();

#### Flashing Only Some Input To The Session

	Input::flashOnly('username', 'email');

	Input::flashExcept('password');

Since you often will want to flash input in association with a redirect to the previous page, you may easily chain input flashing onto a redirect.

	return Redirect::to('form')->withInput();

	return Redirect::to('form')->withInput(Input::except('password'));

> **Note:** You may flash other data across requests using the [Session](/docs/4.2/session) class.

#### Retrieving Old Data

	Input::old('username');

<a name="files"></a>
## Files

#### Retrieving An Uploaded File

	$file = Input::file('photo');

#### Determining If A File Was Uploaded

	if (Input::hasFile('photo'))
	{
		//
	}

The object returned by the `file` method is an instance of the `Symfony\Component\HttpFoundation\File\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file.

#### Determining If An Uploaded File Is Valid

	if (Input::file('photo')->isValid())
	{
		//
	}

#### Moving An Uploaded File

	Input::file('photo')->move($destinationPath);

	Input::file('photo')->move($destinationPath, $fileName);

#### Retrieving The Path To An Uploaded File

	$path = Input::file('photo')->getRealPath();

#### Retrieving The Original Name Of An Uploaded File

	$name = Input::file('photo')->getClientOriginalName();

#### Retrieving The Extension Of An Uploaded File

	$extension = Input::file('photo')->getClientOriginalExtension();

#### Retrieving The Size Of An Uploaded File

	$size = Input::file('photo')->getSize();

#### Retrieving The MIME Type Of An Uploaded File

	$mime = Input::file('photo')->getMimeType();

<a name="request-information"></a>
## Request Information

The `Request` class provides many methods for examining the HTTP request for your application and extends the `Symfony\Component\HttpFoundation\Request` class. Here are some of the highlights.

#### Retrieving The Request URI

	$uri = Request::path();

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

#### Get The Request URL

	$url = Request::url();

#### Retrieve A Request URI Segment

	$segment = Request::segment(1);

#### Retrieving A Request Header

	$value = Request::header('Content-Type');

#### Retrieving Values From $_SERVER

	$value = Request::server('PATH_INFO');

#### Determining If The Request Is Over HTTPS

	if (Request::secure())
	{
		//
	}

#### Determine If The Request Is Using AJAX

	if (Request::ajax())
	{
		//
	}

#### Determine If The Request Has JSON Content Type

	if (Request::isJson())
	{
		//
	}

#### Determine If The Request Is Asking For JSON

	if (Request::wantsJson())
	{
		//
	}

#### Checking The Requested Response Format

The `Request::format` method will return the requested response format based on the HTTP Accept header:

	if (Request::format() == 'json')
	{
		//
	}
