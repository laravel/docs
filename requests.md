# Requests & Input

- [Basic Input](#basic-input)
- [Cookies](#cookies)
- [Old Input](#old-input)
- [Files](#files)
- [Request Information](#request-information)

<a name="basic-input"></a>
## Basic Input

You may access all user input with a few simple methods. You do not need to worry about the HTTP verb used for the request, as input is accessed in the same way for all verbs.

<a name="retrieving-an-input-value"></a>
**Retrieving An Input Value**

	$name = Input::get('name');

<a name="retrieving-a-default-value-if-the-input-value-is-absent"></a>
**Retrieving A Default Value If The Input Value Is Absent**

	$name = Input::get('name', 'Sally');

<a name="determining-if-an-input-value-is-present"></a>
**Determining If An Input Value Is Present**

	if (Input::has('name'))
	{
		//
	}

<a name="getting-all-input-for-the-request"></a>
**Getting All Input For The Request**

	$input = Input::all();

<a name="getting-only-some-of-the-request-input"></a>
**Getting Only Some Of The Request Input**

	$input = Input::only('username', 'password');

	$input = Input::except('credit_card');

Some JavaScript libraries such as Backbone may send input to the application as JSON. You may access this data via `Input::get` like normal.

<a name="cookies"></a>
## Cookies

All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client.

<a name="retrieving-a-cookie-value"></a>
**Retrieving A Cookie Value**

	$value = Cookie::get('name');

<a name="attaching-a-new-cookie-to-a-response"></a>
**Attaching A New Cookie To A Response**

	$response = Response::make('Hello World');

	$response->withCookie(Cookie::make('name', 'value', $minutes));

<a name="creating-a-cookie-that-lasts-forever"></a>
**Creating A Cookie That Lasts Forever**

	$cookie = Cookie::forever('name', 'value');

<a name="old-input"></a>
## Old Input

You may need to keep input from one request until the next request. For example, you may need to re-populate a form after checking it for validation errors.

<a name="flashing-input-to-the-session"></a>
**Flashing Input To The Session**

	Input::flash();

<a name="flashing-only-some-input-to-the-session"></a>
**Flashing Only Some Input To The Session**

	Input::flashOnly('username', 'email');

	Input::flashExcept('password');

Since you often will want to flash input in association with a redirect to the previous page, you may easily chain input flashing onto a redirect.

	return Redirect::to('form')->withInput();

	return Redirect::to('form')->withInput(Input::except('password'));

> **Note:** You may flash other data across requests using the [Session](/docs/session) class.

<a name="retrieving-old-data"></a>
**Retrieving Old Data**

	Input::old('username');

<a name="files"></a>
## Files

<a name="retrieving-an-uploaded-file"></a>
**Retrieving An Uploaded File**

	$file = Input::file('photo');

<a name="determining-if-a-file-was-uploaded"></a>
**Determining If A File Was Uploaded**

	if (Input::hasFile('photo'))
	{
		//
	}

The object returned by the `file` method is an instance of the `Symfony\Component\HttpFoundation\File\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file.

<a name="moving-an-uploaded-file"></a>
**Moving An Uploaded File**

	Input::file('photo')->move($destinationPath);

	Input::file('photo')->move($destinationPath, $fileName);

<a name="retrieving-the-path-to-an-uploaded-file"></a>
**Retrieving The Path To An Uploaded File**

	$path = Input::file('photo')->getRealPath();

<a name="retrieving-the-size-of-an-uploaded-file"></a>
**Retrieving The Size Of An Uploaded File**

	$size = Input::file('photo')->getSize();

<a name="retrieving-the-mime-type-of-an-uploaded-file"></a>
**Retrieving The MIME Type Of An Uploaded File**

	$mime = Input::file('photo')->getMimeType();

<a name="request-information"></a>
## Request Information

The `Request` class provides many methods for examining the HTTP request for your application and extends the `Symfony\Component\HttpFoundation\Request` class. Here are some of the highlights.

<a name="retrieving-the-request-uri"></a>
**Retrieving The Request URI**

	$uri = Request::path();

<a name="determining-if-the-request-path-matches-a-pattern"></a>
**Determining If The Request Path Matches A Pattern**

	if (Request::is('admin/*'))
	{
		//
	}

<a name="get-the-request-url"></a>
**Get The Request URL**

	$url = Request::url();

<a name="retrieve-a-request-uri-segment"></a>
**Retrieve A Request URI Segment**

	$segment = Request::segment(1);

<a name="retrieving-a-request-header"></a>
**Retrieving A Request Header**

	$value = Request::header('Content-Type');

<a name="retrieving-values-from-$_server"></a>
**Retrieving Values From $_SERVER**

	$value = Request::server('PATH_INFO');

<a name="determine-if-the-request-is-using-ajax"></a>
**Determine If The Request Is Using AJAX**

	if (Request::ajax())
	{
		//
	}

<a name="determining-if-the-request-is-over-https"></a>
**Determining If The Request Is Over HTTPS**

	if (Request::secure())
	{
		//
	}
