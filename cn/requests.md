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

**获取指定的信息，或者获取排除指定几个提交项之外的所有提交信息**

	$input = Input::only('username', 'password');

	$input = Input::except('credit_card');

有一些javascript库，比如 Backbone 会以json格式提交信息。 通过 `Input::get` 来获取信息，使用上无差别。

<a name="cookies"></a>
## Cookies

Laravel会加密所有已创建的cookie信息，并附加上授权码，当客户端擅自修改cookie信息时，该cookie将被废弃，从而保证安全性。

**获取一个指定的cookie值**

	$value = Cookie::get('name');

**添加一个新的cookie键值对**

	$response = Response::make('Hello World');

	$response->withCookie(Cookie::make('name', 'value', $minutes));

**创建一个永不过期的cookie键值对**

	$cookie = Cookie::forever('name', 'value');

<a name="old-input"></a>
## 用户提交信息持久化

有时可能需要在多个用户请求之间持久化用户提交的信息。 比如，当用户提交的信息验证失败重新返回提交信息页面时还原用户的输入。

**将用户提交的信息存入Session**

	Input::flash();

**把指定的用户提交的信息存入Session**

	Input::flashOnly('username', 'email');

	Input::flashExcept('password');

如果你需要关联持久用户提交的信息的操作和重定向操作，可以使用如下的链式调用的方法：

	return Redirect::to('form')->withInput();

	return Redirect::to('form')->withInput(Input::except('password'));

> **注意：** 如果你想持久化其它的信息，请参考 [Session](/docs/session) 类.

**获取已持久化的用户提交的信息**

	Input::old('username');

<a name="files"></a>
## 文件上传

**获取用户上传的文件**

	$file = Input::file('photo');

**判断指定文件是否已经被上传**

	if (Input::hasFile('photo'))
	{
		//
	}

`file` 方法返回了一个 `Symfony\Component\HttpFoundation\File\UploadedFile` 类的实例, 该类继承自PHP的 `SplFileInfo` 类，并提供了大量操作该用户上传的文件的方法。

**移动一个已上传的文件**

	Input::file('photo')->move($destinationPath);

	Input::file('photo')->move($destinationPath, $fileName);

**获取一个已上传的文件在服务器的真实路径**

	$path = Input::file('photo')->getRealPath();

**获取一个已上传的文件的大小**

	$size = Input::file('photo')->getSize();

**获取一个已上传的文件的 MIME 类型**

	$mime = Input::file('photo')->getMimeType();

<a name="request-information"></a>
## 用户请求的详细信息

`Request` 类提供了许多 方法 用于获取关于请求的详细信息，该类继承自 `Symfony\Component\HttpFoundation\Request` 类。 下面提供了几个具有代表性的方法：

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
