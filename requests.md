# HTTP 请求

- [取得请求实例](#obtaining-a-request-instance)
- [取得输入数据](#retrieving-input)
- [旧输入数据](#old-input)
- [Cookies](#cookies)
- [上传文件](#files)
- [其他的请求信息](#other-request-information)

<a name="obtaining-a-request-instance"></a>
## 取得请求实例

### 透过 Facade

`Request` facade 允许你访问当前绑定容器的请求。例如：

	$name = Request::input('name');

切记，如果你在一个命名空间中，你必须导入 `Request` facade，接着在类别的上方宣告 `use Request;`。

### 透过依赖注入

要透过依赖注入的方式取得 HTTP 请求的实例，你必须在控制器中的构造函数或方法对该类别使用型别提示。当前请求的实例将会自动由[服务容器](/docs/5.0/master/container)注入：

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

如果你的控制器也有从路由参数传入的输入数据，只需要将路由参数置于其他依赖之后：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

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
## 取得输入数据

#### 取得特定输入数据

你可以透过 `Illuminate\Http\Request` 的实例，经由几个简洁的方法取得所有的用户输入数据。不需要担心发出请求时使用的 HTTP 动词，取得输入数据的方式都是相同的。

	$name = Request::input('name');

#### 取得特定输入数据，若没有则取得默认值

	$name = Request::input('name', 'Sally');

#### 确认是否有输入数据

	if (Request::has('name'))
	{
		//
	}

#### 取得所有发出请求时传入的输入数据

	$input = Request::all();

#### 取得部分发出请求时传入的输入数据

	$input = Request::only('username', 'password');

	$input = Request::except('credit_card');

如果是「数组」形式的输入数据，可以使用「点」语法取得数组：

	$input = Request::input('products.0.name');

<a name="old-input"></a>
## 旧输入数据

Laravel 可以让你保留这次的输入数据，直到下一次请求发送前。例如，你可能需要在表单验证失败后重新填入表单值。

#### 将输入数据存成一次性 Session

`flash` 方法会将当前的输入数据存进 [session](/docs/5.0/session)中，所以下次用户发出请求时可以使用保存的数据：

	Request::flash();

#### 将部分输入数据存成一次性 Session

	Request::flashOnly('username', 'email');

	Request::flashExcept('password');

#### 快闪及重导

你很可能常常需要在重导至前一页，并将输入数据存成一次性 Session。只要在重导方法串接的方法中传入输入数据，就能简单地完成。

	return redirect('form')->withInput();

	return redirect('form')->withInput(Request::except('password'));

#### 取得旧输入数据

若想要取得前一次请求所保存的一次性 Session，你可以使用 `Request` 实例中的 `old` 方法。

	$username = Request::old('username');

如果你想在 Blade 模板显示旧输入数据，可以使用更加方便的辅助方法 `old` ：

	{{ old('username') }}

<a name="cookies"></a>
## Cookies

Laravel 所建立的 cookie 会加密并且加上认证记号，这代表着被用户擅自更改的 cookie 会失效。

#### 取得 Cookie 值

	$value = Request::cookie('name');

#### 加上新的 Cookie 到回应

辅助方法 `cookie` 提供一个简易的工厂方法来产生新的 `Symfony\Component\HttpFoundation\Cookie` 实例。可以在 `Response` 实例之后连接 `withCookie` 方法带入 cookie 至回应：

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

#### 建立永久有效的 Cookie*

_虽然说是「永远」，但真正的意思是五年。_

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="files"></a>
## 上传文件

#### 取得上传文件

	$file = Request::file('photo');

#### 确认文件是否有上传

	if (Request::hasFile('photo'))
	{
		//
	}

`file` 方法回传的对象是 `Symfony\Component\HttpFoundation\File\UploadedFile` 的实例，`UploadedFile` 继承了 PHP 的 `SplFileInfo` 类别并且提供了很多和文件交互的方法。

#### 确认上传的文件是否有效

	if (Request::file('photo')->isValid())
	{
		//
	}

#### 移动上传的文件

	Request::file('photo')->move($destinationPath);

	Request::file('photo')->move($destinationPath, $fileName);

### 其他上传文件的方法

`UploadedFile` 的实例还有许多可用的方法，可以至[该对象的 API 文档](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/File/UploadedFile.html)了解有关这些方法的详细信息。

<a name="other-request-information"></a>
## 其他的请求信息

`Request` 类别提供很多方法检查 HTTP 请求，它继承了 `Symfony\Component\HttpFoundation\Request` 类别，下面是一些使用方式。

#### 取得请求 URI

	$uri = Request::path();

#### 取得请求方法

	$method = Request::method();

	if (Request::isMethod('post'))
	{
		//
	}

#### 确认请求路径是否符合特定格式

	if (Request::is('admin/*'))
	{
		//
	}

#### 取得请求 URL

	$url = Request::url();
