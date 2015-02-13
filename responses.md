# HTTP 回应

- [基本回应](#basic-responses)
- [重导](#redirects)
- [其他回应](#other-responses)
- [回应巨集](#response-macros)

<a name="basic-responses"></a>
## 基本回应

#### 从路由回传字串

最基本的回应就是从 Laravel 的路由回传字串：

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### 建立自订回应

但是以大部分的路由及控制器所执行的动作来说，你需要回传完整的 `Illuminate\Http\Response` 实例或是一个[视图](/docs/5.0/views)。回传一个完整的 `Response` 实例时，你能够自订回应的 HTTP 状态码以及标头。`Response` 实例继承了 `Symfony\Component\HttpFoundation\Response` 类别，其提供了很多方法建立 HTTP 回应。

	use Illuminate\Http\Response;

	return (new Response($content, $status))
	              ->header('Content-Type', $value);

为了方便起见，你可以使用辅助方法 `response`：

	return response($content, $status)
	              ->header('Content-Type', $value);

> **提示：** 有关 `Response` 方法的完整列表可以参照 [API 文档](http://laravel.com/api/5.0/Illuminate/Http/Response.html) 以及 [Symfony API 文档](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/Response.html).

#### 在回应送出视图

如果想要使用 `Response` 类别的方法，但最终回传视图给用户，你可以使用简便的 `view` 方法：

	return response()->view('hello')->header('Content-Type', $type);

#### 附加 Cookies 到回应

	return response($content)->withCookie(cookie('name', 'value'));

#### 方法连接

切记，大多数的 `Response` 方法都是可连接的，用以建立流畅的回应：

	return response()->view('hello')->header('Content-Type', $type)
                     ->withCookie(cookie('name', 'value'));

<a name="redirects"></a>
## 重导

重导回应通常是类别 `Illuminate\Http\RedirectResponse` 的实例，并且包含用户要重导至另一个 URL 所需的标头。

#### 回传重导

有几种方法可以产生 `RedirectResponse` 的实例，最简单的方式就是透过辅助方法 `redirect`。当在测试时，建立一个仿真重导回应的测试并不常见，所以使用辅助方法通常是可行的：

	return redirect('user/login');

#### 回传重导并且加上快闪数据（ Flash Data ）

通常重导至新的 URL 时会一并将[数据存进一次性 Session](/docs/5.0/session)。所以为了方便，你可以利用方法连接的方式创建一个 `RedirectResponse` 的实例**并**将数据存进一次性 Session：

	return redirect('user/login')->with('message', 'Login Failed');

#### 回传根据前一个 URL 的重导

你可能希望将用户重导至前一个位置，例如当表单提交之后。你可以使用 `back` 方法来达成这个目的：

	return redirect()->back();

	return redirect()->back()->withInput();

#### 回传根据路由名称的重导

当你调用辅助方法 `redirect` 且不带任何参数时，将会回传 `Illuminate\Routing\Redirector` 的实例，你可以对该实例调用任何的方法。举个例子，要产生一个 `RedirectResponse` 到一个路由名称，你可以使用 `route` 方法：

	return redirect()->route('login');

#### 回传根据路由名称的重导，并给予路由参数赋值

如果你的路由有参数，你可以放进 `route` 方法的第二个参数。

	// 路由的 URI 为：profile/{id}

	return redirect()->route('profile', [1]);

如果你要重导至路由且路由的参数为 Eloquent 模型的「ID」，你可以直接将模型传入，ID 将会自动被提取：

	return redirect()->route('profile', [$user]);

#### 回传根据路由名称的重导，并给予特定名称路由参数赋值

	// 路由的 URI 为：profile/{user}

	return redirect()->route('profile', ['user' => 1]);

#### 回传根据控制器动作的重导

既然可以产生 `RedirectResponse` 的实例并重导至路由名称，同样的也可以重导至[控制器动作](/docs/5.0/controllers)：

	return redirect()->action('App\Http\Controllers\HomeController@index');

> **提示：** 如果你已经透过 `URL::setRootControllerNamespace` 注册了根控制器的命名空间，那么就不需要对 `action()` 方法内的控制器指定完整的命名空间。

#### 回传根据控制器动作的重导，并给予参数赋值

	return redirect()->action('App\Http\Controllers\UserController@profile', [1]);

#### 回传根据控制器动作的重导，并给予特定名称参数赋值

	return redirect()->action('App\Http\Controllers\UserController@profile', ['user' => 1]);

<a name="other-responses"></a>
## 其他回应

使用辅助方法 `response` 可以轻松的产生其他类型的回应实例。当你调用辅助方法 `response` 且不带任何参数时，将会回传 `Illuminate\Contracts\Routing\ResponseFactory` [Contract](/docs/5.0/contracts) 的实做。Contract 提供了一些有用的方法来产生回应。

#### 建立 JSON 回应

`json` 方法会自动将标头的 `Content-Type` 设置为 `application/json`：

	return response()->json(['name' => 'Abigail', 'state' => 'CA']);

#### 建立 JSONP 回应

	return response()->json(['name' => 'Abigail', 'state' => 'CA'])
	                 ->setCallback($request->input('callback'));

#### 建立文件下载的回应

	return response()->download($pathToFile);

	return response()->download($pathToFile, $name, $headers);

> **提醒：**管理文件下载的套件，Symfony HttpFoundation，要求下载文件名必须为 ASCII。

<a name="response-macros"></a>
## 回应巨集

如果你想要自订可以在很多路由和控制器重复使用的回应，你可以使用 `Illuminate\Contracts\Routing\ResponseFactory` 实做的方法 `macro`。

举个例子，来自[服务提供者的](/docs/5.0/providers) `boot` 方法:

	<?php namespace App\Providers;

	use Response;
	use Illuminate\Support\ServiceProvider;

	class ResponseMacroServiceProvider extends ServiceProvider {

		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Response::('caps', function($value) use ($response)
			{
				return $response->make(strtoupper($value));
			});
		}

	}

`macro` 函式第一个参数为巨集名称，第二个参数为闭包函式。闭包函式会在 `ResponseFactory`的实做或者辅助方法 `response` 调用巨集名称的时候被执行：

	return response()->caps('foo');
