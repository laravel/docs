# HTTP 中间层

- [简介](#introduction)
- [建立中间层](#defining-middleware)
- [注册中间层](#registering-middleware)
- [Terminable 中间层](#terminableness-middleware)

<a name="introduction"></a>
## 简介

HTTP 中间层提供一个方便的机制来过滤进入应用程序的 HTTP 请求，例如，Laravel 本身使用中间层来检验用户身份验证，如果用户经过身份验证，中间层会将用户导向登录页面，然而，如果用户通过身份验证，中间层将会允许这个请求进一步继续前进。

当然，除了身份验证之外，中间层也可以被用来执行各式各样的任务，CORS 中间层负责替所有即将离开程序的回应加入适当的标头，一个日志中间层可以记录所有传入应用程序的请求。
Laravel 框架已经内置一些中间层，包括维护、身份验证、CSRF 保护，等等。所有的中间层都位于 `app/Http/Middleware`  目录内。

<a name="defining-middleware"></a>
## 建立中间层

要建立一个新的中间层，可以使用 `make:middleware` 这个 Artisan 指令：

	php artisan make:middleware OldMiddleware

此指令将会 在 `app/Http/Middleware` 目录内置立一个名称为 `OldMiddleware` 的类别。在这个中间层内我们只允许 `年龄` 大于 200 的才能访问路由，否则，我们会将用户重新导向 "home" 的 URI 。

	<?php namespace App\Http\Middleware;

	class OldMiddleware {

		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') < 200)
			{
				return redirect('home');
			}

			return $next($request);
		}

	}

如你所见，若是 `年龄` 小于 `200` ，中间层将会回传 HTTP 重新导向给用户端，否则，请求将会进一步传递到应用程序。只需调用带有 `$request` 的 `$next` 方法，即可将请求传递到更深层的应用程序(允许跳过中间层)
HTTP 请求在实际碰触到应用程序之前，最好是可以层层通过许多中间层，每一层都可以对请求进行检查，甚至是完全拒绝请求。

<a name="registering-middleware"></a>
## 注册中间层

### 全域中间层

若是希望中间层被所有的 HTTP 请求给执行，只要将中间层的类别加入到 `app/Http/Kernel.php` 的 `$middleware` 属性清单列表中。

### 指派中间层给路由

如果你要指派中间层给特定的路由，你得先将中间层在 `app/Http/Kernel.php` 设置一个键值，默认情况下，这个文件内的 `$routeMiddleware` 属性已包含了 Laravel 目前设置的中间层，你只需要在清单列表中加上一组自订的键值即可。
中间层一旦在 HTTP kernel 文件内被定义，你即可在路由选项内使用 `middleware` 键值来指派：

	Route::get('admin/profile', ['middleware' => 'auth', function()
	{
		//
	}]);

<a name="terminable-middleware"></a>
## Terminable 中间层

有些时候中间层需要在 HTTP 回应已被发送到用户端之后才执行，例如，Laravel 内置的 "session" 中间层，保存 session 数据是在回应已被发送到用户端 _之后_ 才执行。为了做到这一点，你需要定义中间层为“terminable”。

	use Illuminate\Contracts\Routing\TerminableMiddleware;

	class StartSession implements TerminableMiddleware {

		public function handle($request, $next)
		{
			return $next($request);
		}

		public function terminate($request, $response)
		{
			// Store the session data...
		}

	}

如你所见，除了定义 `handle` 方法之外， `TerminableMiddleware` 定义一个 `terminate`  方法。这个方法接收请求和回应。一旦定义了 terminable 中间层，你需要将它增加到 HTTP kernel 文件的全域中间层清单列表中。
