# 用户请求 与 用户提交的信息

- [操作用户提交信息基础](#basic-input)
- [Cookies](#cookies)
- [用户提交信息持久化](#old-input)
- [文件上传](#files)
- [用户请求的详细信息](#request-information)

<a name="basic-input"></a>
## 操作用户提交信息基础

Laravel使用一种简单的方式来访问用户提交的信息。 你可以用统一的方式来访问用户提交的信息，而不用为用户提交信息的方式操心。

**获取一个用户提交的值**

  $name = Input::get('name');

**为用户提交信息指定一个的默认返回值(如果用户未提交)**

	$name = Input::get('name', 'Sally');

**判断指定的提交信息是否存在**

	if (Input::has('name'))
	{
		//
	}

**获取所有用户提交的信息**

	$input = Input::all();

**Getting Only Some Of The Request Input**

	$input = Input::only('username', 'password');

	$input = Input::except('credit_card');

Some JavaScript libraries such as Backbone may send input to the application as JSON. You may access this data via `Input::get` like normal.

<a name="cookies"></a>
## Cookies

All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client.

**Retrieving A Cookie Value**

	$value = Cookie::get('name');

**Attaching A New Cookie To A Response**

	$response = Response::make('Hello World');

	$response->withCookie(Cookie::make('name', 'value', $minutes));

**Creating A Cookie That Lasts Forever**

	$cookie = Cookie::forever('name', 'value');

<a name="old-input"></a>
## Old Input

You may need to keep input from one request until the next request. For example, you may need to re-populate a form after checking it for validation errors.

**Flashing Input To The Session**

	Input::flash();

**Flashing Only Some Input To The Session**

	Input::flashOnly('username', 'email');

	Input::flashExcept('password');

Since you often will want to flash input in association with a redirect to the previous page, you may easily chain input flashing onto a redirect.

	return Redirect::to('form')->withInput();

	return Redirect::to('form')->withInput(Input::except('password'));

> **Note:** You may flash other data across requests using the [Session](/docs/session) class.

**Retrieving Old Data**

	Input::old('username');

<a name="files"></a>
## Files

**Retrieving An Uploaded File**

	$file = Input::file('photo');

**Determining If A File Was Uploaded**

	if (Input::hasFile('photo'))
	{
		//
	}

The object returned by the `file` method is an instance of the `Symfony\Component\HttpFoundation\File\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file.

**Moving An Uploaded File**

	Input::file('photo')->move($destinationPath);

	Input::file('photo')->move($destinationPath, $fileName);

**Retrieving The Path To An Uploaded File**

	$path = Input::file('photo')->getRealPath();

**Retrieving The Size Of An Uploaded File**

	$size = Input::file('photo')->getSize();

**Retrieving The MIME Type Of An Uploaded File**

	$mime = Input::file('photo')->getMimeType();

<a name="request-information"></a>
## 用户请求的详细信息

The `Request` class provides many methods for examining the HTTP request for your application and extends the `Symfony\Component\HttpFoundation\Request` class. Here are some of the highlights.

**获取请求URI**

	$uri = Request::path();

**判断请求路径是否符合指定模式**

	if (Request::is('admin/*'))
	{
		//
	}

**获取请求URL**

	$url = Request::url();

**获取请求URI信息**

	$segment = Request::segment(1);

**获取请求头里的Content-Type信息**

	$value = Request::header('Content-Type');

**获取 $_SERVER 数组里指定的值**

	$value = Request::server('PATH_INFO');

**判断是否是使用ajax请求**

	if (Request::ajax())
	{
		//
	}

**判断请求是否使用https连接**

	if (Request::secure())
	{
		//
	}
