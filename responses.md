# HTTP 回應

- [基本回應](#basic-responses)
- [重導](#redirects)
- [其他回應](#other-responses)
- [回應巨集](#response-macros)

<a name="basic-responses"></a>
## 基本回應

#### 從路由回傳字串

最基本的回應就是從 Laravel 的路由回傳字串：

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### 建立自訂回應

但是以大部分的路由及控制器所執行的動作來說，你需要回傳完整的 `Illuminate\Http\Response` 實例或是一個[視圖](/docs/5.0/views)。回傳一個完整的 `Response` 實例時，你能夠自訂回應的 HTTP 狀態碼以及標頭。`Response` 實例繼承了 `Symfony\Component\HttpFoundation\Response` 類別，其提供了很多方法建立 HTTP 回應。

	use Illuminate\Http\Response;

	return (new Response($content, $status))
	              ->header('Content-Type', $value);

為了方便起見，你可以使用輔助方法 `response`：

	return response($content, $status)
	              ->header('Content-Type', $value);

> **提示：** 有關 `Response` 方法的完整列表可以參照 [API 文件](http://laravel.com/api/5.0/Illuminate/Http/Response.html) 以及 [Symfony API 文件](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/Response.html).

#### 在回應送出視圖

如果想要使用 `Response` 類別的方法，但最終回傳視圖給使用者，你可以使用簡便的 `view` 方法：

	return response()->view('hello')->header('Content-Type', $type);

#### 附加 Cookies 到回應

	return response($content)->withCookie(cookie('name', 'value'));

#### 方法連接

切記，大多數的 `Response` 方法都是可連接的，用以建立流暢的回應：

	return response()->view('hello')->header('Content-Type', $type)
                     ->withCookie(cookie('name', 'value'));

<a name="redirects"></a>
## 重導

重導回應通常是類別 `Illuminate\Http\RedirectResponse` 的實例，並且包含使用者要重導至另一個 URL 所需的標頭。

#### 回傳重導

有幾種方法可以產生 `RedirectResponse` 的實例，最簡單的方式就是透過輔助方法 `redirect`。當在測試時，建立一個模擬重導回應的測試並不常見，所以使用輔助方法通常是可行的：

	return redirect('user/login');

#### 回傳重導並且加上快閃資料（ Flash Data ）

通常重導至新的 URL 時會一併將[資料存進一次性 Session](/docs/5.0/session)。所以為了方便，你可以利用方法連接的方式創建一個 `RedirectResponse` 的實例**並**將資料存進一次性 Session：

	return redirect('user/login')->with('message', 'Login Failed');

#### 回傳根據前一個 URL 的重導

你可能希望將使用者重導至前一個位置，例如當表單提交之後。你可以使用 `back` 方法來達成這個目的：

	return redirect()->back();

	return redirect()->back()->withInput();

#### 回傳根據路由名稱的重導

當你呼叫輔助方法 `redirect` 且不帶任何參數時，將會回傳 `Illuminate\Routing\Redirector` 的實例，你可以對該實例呼叫任何的方法。舉個例子，要產生一個 `RedirectResponse` 到一個路由名稱，你可以使用 `route` 方法：

	return redirect()->route('login');

#### 回傳根據路由名稱的重導，並給予路由參數賦值

如果你的路由有參數，你可以放進 `route` 方法的第二個參數。

	// 路由的 URI 為：profile/{id}

	return redirect()->route('profile', [1]);

如果你要重導至路由且路由的參數為 Eloquent 模型的「ID」，你可以直接將模型傳入，ID 將會自動被提取：

	return redirect()->route('profile', [$user]);

#### 回傳根據路由名稱的重導，並給予特定名稱路由參數賦值

	// 路由的 URI 為：profile/{user}

	return redirect()->route('profile', ['user' => 1]);

#### 回傳根據控制器動作的重導

既然可以產生 `RedirectResponse` 的實例並重導至路由名稱，同樣的也可以重導至[控制器動作](/docs/5.0/controllers)：

	return redirect()->action('App\Http\Controllers\HomeController@index');

> **提示：** 如果你已經透過 `URL::setRootControllerNamespace` 註冊了根控制器的命名空間，那麼就不需要對 `action()` 方法內的控制器指定完整的命名空間。

#### 回傳根據控制器動作的重導，並給予參數賦值

	return redirect()->action('App\Http\Controllers\UserController@profile', [1]);

#### 回傳根據控制器動作的重導，並給予特定名稱參數賦值

	return redirect()->action('App\Http\Controllers\UserController@profile', ['user' => 1]);

<a name="other-responses"></a>
## 其他回應

使用輔助方法 `response` 可以輕鬆的產生其他類型的回應實例。當你呼叫輔助方法 `response` 且不帶任何參數時，將會回傳 `Illuminate\Contracts\Routing\ResponseFactory` [Contract](/docs/5.0/contracts) 的實做。Contract 提供了一些有用的方法來產生回應。

#### 建立 JSON 回應

`json` 方法會自動將標頭的 `Content-Type` 設定為 `application/json`：

	return response()->json(['name' => 'Abigail', 'state' => 'CA']);

#### 建立 JSONP 回應

	return response()->json(['name' => 'Abigail', 'state' => 'CA'])
	                 ->setCallback($request->input('callback'));

#### 建立檔案下載的回應

	return response()->download($pathToFile);

	return response()->download($pathToFile, $name, $headers);

> **提醒：**管理檔案下載的套件，Symfony HttpFoundation，要求下載檔名必須為 ASCII。

<a name="response-macros"></a>
## 回應巨集

如果你想要自訂可以在很多路由和控制器重複使用的回應，你可以使用 `Illuminate\Contracts\Routing\ResponseFactory` 實做的方法 `macro`。

舉個例子，來自[服務提供者的](/docs/5.0/providers) `boot` 方法:

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

`macro` 函式第一個參數為巨集名稱，第二個參數為閉包函式。閉包函式會在 `ResponseFactory`的實做或者輔助方法 `response` 呼叫巨集名稱的時候被執行：

	return response()->caps('foo');
