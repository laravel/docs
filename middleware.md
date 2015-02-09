# HTTP 中介層

- [簡介](#introduction)
- [建立中介層](#defining-middleware)
- [註冊中介層](#registering-middleware)
- [Terminable 中介層](#terminable-middleware)

<a name="introduction"></a>
## 簡介

HTTP 中介層提供一個方便的機制來過濾進入應用程式的 HTTP 請求，例如，Laravel 本身使用中介層來檢驗使用者身份驗證，如果使用者經過身份驗證，中介層會將用戶導向登入頁面，然而，如果用戶通過身份驗證，中介層將會允許這個請求進一步繼續前進。

當然，除了身份驗證之外，中介層也可以被用來執行各式各樣的任務，CORS 中介層負責替所有即將離開程式的回應加入適當的標頭，一個日誌中介層可以記錄所有傳入應用程式的請求。
Laravel 框架已經內建一些中介層，包括維護、身份驗證、CSRF 保護，等等。所有的中介層都位於 `app/Http/Middleware`  目錄內。

<a name="defining-middleware"></a>
## 建立中介層

要建立一個新的中介層，可以使用 `make:middleware` 這個 Artisan 指令：

	php artisan make:middleware OldMiddleware

此指令將會 在 `app/Http/Middleware` 目錄內建立一個名稱為 `OldMiddleware` 的類別。在這個中介層內我們只允許 `年齡` 大於 200 的才能存取路由，否則，我們會將用戶重新導向 "home" 的 URI 。

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

如你所見，若是 `年齡` 小於 `200` ，中介層將會回傳 HTTP 重新導向給用戶端，否則，請求將會進一步傳遞到應用程式。只需調用帶有 `$request` 的 `$next` 方法，即可將請求傳遞到更深層的應用程式(允許跳過中介層)
HTTP 請求在實際碰觸到應用程式之前，最好是可以層層通過許多中介層，每一層都可以對請求進行檢查，甚至是完全拒絕請求。

<a name="registering-middleware"></a>
## 註冊中介層

### 全域中介層

若是希望中介層被所有的 HTTP 請求給執行，只要將中介層的類別加入到 `app/Http/Kernel.php` 的 `$middleware` 屬性清單列表中。

### 指派中介層給路由

如果你要指派中介層給特定的路由，你得先將中介層在 `app/Http/Kernel.php` 設定一個鍵值，預設情況下，這個檔案內的 `$routeMiddleware` 屬性已包含了 Laravel 目前設定的中介層，你只需要在清單列表中加上一組自訂的鍵值即可。
中介層一旦在 HTTP kernel 檔案內被定義，你即可在路由選項內使用 `middleware` 鍵值來指派：

	Route::get('admin/profile', ['middleware' => 'auth', function()
	{
		//
	}]);

<a name="terminable-middleware"></a>
## Terminable 中介層

有些時候中介層需要在 HTTP 回應已被傳送到用戶端之後才執行，例如，Laravel 內建的 "session" 中介層，儲存 session 資料是在回應已被傳送到用戶端 _之後_ 才執行。為了做到這一點，你需要定義中介層為“terminable”。

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

如你所見，除了定義 `handle` 方法之外， `TerminableMiddleware` 定義一個 `terminate`  方法。這個方法接收請求和回應。一旦定義了 terminable 中介層，你需要將它增加到 HTTP kernel 檔案的全域中介層清單列表中。
