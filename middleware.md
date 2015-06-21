# HTTP 中介層

- [簡介](#introduction)
- [建立中介層](#defining-middleware)
- [註冊中介層](#registering-middleware)
- [Middleware Parameters](#middleware-parameters)
- [Terminable 中介層](#terminable-middleware)

<a name="introduction"></a>
## 簡介

HTTP 中介層提供一個方便的機制來過濾進入應用程式的 HTTP 請求，例如，Laravel 本身使用中介層來檢驗使用者身份驗證，如果使用者未經過身份驗證，中介層會將用戶導向登入頁面，反之，當用戶通過身份驗證，中介層將會同意此請求繼續往前進。

當然，除了身份驗證之外，中介層也可以被用來執行各式各樣的任務，CORS 中介層負責替所有即將離開程式的回應加入適當的標頭。而日誌中介層可以記錄所有傳入應用程式的請求。

Laravel 框架已經內建一些中介層，包括維護、身份驗證、CSRF 保護，等等。所有的中介層都放在 `app/Http/Middleware` 目錄內。

<a name="defining-middleware"></a>
## 建立中介層

要建立一個新的中介層，可以使用 `make:middleware` 這個 Artisan 指令：

	php artisan make:middleware OldMiddleware

此指令將會在 `app/Http/Middleware` 目錄內建立一個名稱為 `OldMiddleware` 的類別。在這個中介層內我們只允許請求內的 `age` 變數大於 200 的才能存取路由，否則，我們會將用戶重新導向「home」這個 URI。

	<?php

	namespace App\Http\Middleware;

	use Closure;

	class OldMiddleware
	{
		/**
		 * 執行請求過濾器。
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') <= 200) {
				return redirect('home');
			}

			return $next($request);
		}

	}

如你所見，若是 age 小於 200，中介層將會回傳 HTTP 重新導向給用戶端，否則，請求將會進一步傳遞到應用程式。只需調用帶有 $request 的 $next 方法，即可將請求傳遞到更深層的應用程式(允許通過中介層)。

HTTP 請求在實際碰觸到應用程式之前，最好是可以層層通過許多中介層，每一層都可以對請求進行檢查，甚至是完全拒絕請求。

### *前* / *後* 中介層

一個中介層是在請求前還是請求後執行要看中介層自己。這個中介層會在應用程式處理請求**前**執行一些任務：

	<?php

	namespace App\Http\Middleware;

	use Closure;

	class BeforeMiddleware
	{
		public function handle($request, Closure $next)
		{
			// 執行動作

			return $next($request);
		}
	}

這個中介層則會在應用程式處理請求後執行它的任務：

	<?php

	namespace App\Http\Middleware;

	use Closure;

	class AfterMiddleware
	{
		public function handle($request, Closure $next)
		{
			$response = $next($request);

			// 執行動作

			return $response;
		}
	}

<a name="registering-middleware"></a>
## 註冊中介層

### Global Middleware

If you want a middleware to be run during every HTTP request to your application, simply list the middleware class in the `$middleware` property of your `app/Http/Kernel.php` class.

### Assigning Middleware To Routes

If you would like to assign middleware to specific routes, you should first assign the middleware a short-hand key in your `app/Http/Kernel.php` file. By default, the `$routeMiddleware` property of this class contains entries for the middleware included with Laravel. To add your own, simply append it to this list and assign it a key of your choosing. For example:

	// Within App\Http\Kernel Class...

    protected $routeMiddleware = [
        'auth' => 'App\Http\Middleware\Authenticate',
        'auth.basic' => 'Illuminate\Auth\Middleware\AuthenticateWithBasicAuth',
        'guest' => 'App\Http\Middleware\RedirectIfAuthenticated',
    ];

Once the middleware has been defined in the HTTP kernel, you may use the `middleware` key in the route options array:

	Route::get('admin/profile', ['middleware' => 'auth', function () {
		//
	}]);

<a name="middleware-parameters"></a>
## Middleware Parameters

Middleware can also receive additional custom parameters. For example, if your application needs to verify that the authenticated user has a given "role" before performing a given action, you could create a `RoleMiddleware` that receives a role name as an additional argument.

Additional middleware parameters will be passed to the middleware after the `$next` argument:

	<?php

	namespace App\Http\Middleware;

	use Closure;

	class RoleMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @param  string  $role
		 * @return mixed
		 */
		public function handle($request, Closure $next, $role)
		{
			if (! $request->user()->hasRole($role)) {
				// Redirect...
			}

			return $next($request);
		}

	}

Middleware parameters may be specified when defining the route by separating the middleware name and parameters with a `:`. Multiple parameters should be delimited by commas:

	Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
		//
	}]);

<a name="terminable-middleware"></a>
## Terminable 中介層

Sometimes a middleware may need to do some work after the HTTP response has already been sent to the browser. For example, the "session" middleware included with Laravel writes the session data to storage _after_ the response has been sent to the browser. To accomplish this, define the middleware as "terminable" by adding a `terminate` method to the middleware:

	<?php namespace Illuminate\Session\Middleware;

	use Closure;

	class StartSession
	{
		public function handle($request, Closure $next)
		{
			return $next($request);
		}

		public function terminate($request, $response)
		{
			// Store the session data...
		}
	}

The `terminate` method should receive both the request and the response. Once you have defined a terminable middleware, you should add it to the list of global middlewares in your HTTP kernel.
