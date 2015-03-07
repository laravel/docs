# HTTP 路由

- [基本路由](#basic-routing)
- [CSRF 保護](#csrf-protection)
- [方法欺騙](#method-spoofing)
- [路由參數](#route-parameters)
- [命名路由](#named-routes)
- [路由群組](#route-groups)
- [路由模型綁定](#route-model-binding)
- [拋出 404 錯誤](#throwing-404-errors)

<a name="basic-routing"></a>
## 基本路由

你將在 `app/Http/routes.php` 中定義應用中大多數的路由，該檔案將會被 `App\Providers\RouteServiceProvider` 類別載入。而多數的基本路由接受使用 URI 或是 `閉包 (Closure)`:

#### 基本 GET 路由

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### 其他基礎路由

	Route::post('foo/bar', function()
	{
		return 'Hello World';
	});

	Route::put('foo/bar', function()
	{
		//
	});

	Route::delete('foo/bar', function()
	{
		//
	});

#### 為複數動作註冊路由

	Route::match(['get', 'post'], '/', function()
	{
		return 'Hello World';
	});

#### 註冊路由回應所有 HTTP 動作

	Route::any('foo', function()
	{
		return 'Hello World';
	});

通常情況下，您將會需要為您的路由產生 URL，您可以使用 `url` 輔助函式來產生：

	$url = url('foo');

<a name="csrf-protection"></a>
## CSRF 保護

Laravel 提供簡易的方法，讓您可以保護您的應用程式不受到 [CSRF (跨網站請求偽造)](http://en.wikipedia.org/wiki/Cross-site_request_forgery) 攻擊。跨網站請求偽造是一種惡意的攻擊，藉以透過經過身份驗證的使用者身份執行未經授權的命令。

Laravel 為所有上線使用者的 Session 產生一個 CSRF “token”。該 token 用來驗證使用者為實際發出請求至應用程式的使用者。

#### 插入 CSRF Token 到表單

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

當然也可以在 Blade [模板引擎](/docs/5.0/templates)使用：

	<input type="hidden" name="_token" value="{{ csrf_token() }}">


除了 “POST” 參數中的 CSRF token 外，中介層也會驗證請求標頭中的 `X-CSRF-TOKEN`。

您不需要手動驗證 POST、PUT 或 DELETE 請求的 CSRF token。`VerifyCsrfToken` [HTTP  中介層](/docs/5.0/middleware)將自動驗證請求與 Session 中的 token 是否相符合。

#### X-CSRF-TOKEN

除了「POST」參數中的 CSRF token 外，中介層也會驗證請求標頭中的 `X-CSRF-TOKEN`。例如，你可以將其儲存在 meta 標籤中，並使用 jQuery 加進你的標頭：

	<meta name="csrf-token" content="{{ csrf_token() }}" />

	$.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });

Now all AJAX requests will automatically include the CSRF token:

	$.ajax({
	   url: "/foo/bar",
	})

#### X-XSRF-TOKEN

Laravel 也會在 `XSRF-TOKEN` cookie 中儲存 CSRF token。你也可以使用 cookie 的值來設定 `X-XSRF-TOKEN` 請求標頭。一些像是 Angular 的 Javascript 框架會自動幫你做到。

> 注意: `X-CSRF-TOKEN` 與 `X-XSRF-TOKEN` 的差別在於前者無加密，而後者為加密過的值，因為在 Laravel 中的 cookies 預設是加密過的。如果你使用 `csrf_token()` 函式來取得 token 值，你就得使用 `X-CSRF-TOKEN` 標頭。

<a name="method-spoofing"></a>
## 方法欺騙

HTML 表單沒有支援 `PUT` 或 `DELETE` 動作。所以當定義 `PUT` 或 `DELETE` 路由，並在 HTML 表單中被呼叫的時候，您將需要在表單中添加隱藏 的`_method` 欄位。

隨著 `_method` 欄位送出的值將被視為 HTTP 請求方法使用。舉例來說：

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
    	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">
    </form>

<a name="route-parameters"></a>
## 路由參數

當然，您可以獲取請求路由的 URI 區段。

#### 基礎路由參數

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

#### 選擇性路由參數

	Route::get('user/{name?}', function($name = null)
	{
		return $name;
	});

#### 帶預設值的選擇性路由參數

	Route::get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

#### 使用正規表達式限制參數

	Route::get('user/{name}', function($name)
	{
		//
	})
	->where('name', '[A-Za-z]+');

	Route::get('user/{id}', function($id)
	{
		//
	})
	->where('id', '[0-9]+');

#### 使用條件限制陣列

	Route::get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+'])

#### 定義全域模式

如果你想讓特定路由參數總是遵詢特定的正規表達式，可以使用 `pattern` 方法。你應該在 `RouteServiceProvider` 的 `boot` 方法裡定義模式：

	$router->pattern('id', '[0-9]+');

定義模式之後，會作用在所有使用這個特定參數的路由上：

	Route::get('user/{id}', function($id)
	{
		// 只有 {id} 是數字才被呼叫。
	});

#### 取得路由參數

如果需要在路由外部取得其參數，使用 `input` 方法：

	if ($route->input('id') == 1)
	{
		//
	}

你也可以使用 `Illuminate\Http\Request` 實體取得目前路由參數。當前請求的實體可以透過 `Request` facade  取得，或透過型別提示 `Illuminate\Http\Request` 注入依賴：

	use Illuminate\Http\Request;

	Route::get('user/{id}', function(Request $request, $id)
	{
		if ($request->route('id'))
		{
			//
		}
	});

<a name="named-routes"></a>
## 命名路由

命名路由讓你更方便為特定路由產生 URL 或進行重導。你可以使用 `as` 的陣列鍵為路由指定名稱。

	Route::get('user/profile', ['as' => 'profile', function()
	{
		//
	}]);

也可以為控制器動作指定路由名稱：

	Route::get('user/profile', [
        'as' => 'profile', 'uses' => 'UserController@showProfile'
	]);

現在你可以使用路由名稱產生 URL 或進行重導：

	$url = route('profile');

	$redirect = redirect()->route('profile');

`currentRouteName` 方法會返回目前請求的路由名稱：

	$name = Route::currentRouteName();

<a name="route-groups"></a>
## 路由群組

有時候您需要套用篩選器到群組的路由上。不需要為每個路由去套用篩選器，您只需使用路由群組：

	Route::group(['middleware' => 'auth'], function()
	{
		Route::get('/', function()
		{
			// Has Auth Filter
		});

		Route::get('user/profile', function()
		{
			// Has Auth Filter
		});
	});

您一樣可以在 `group` 陣列中使用 `namespace` 參數，指定這群組中控制器的命名空間：

	Route::group(['namespace' => 'Admin'], function()
	{
		//
	});

> **注意：** 在預設情況下，`RouteServiceProvider` 包含內建您命名空間群組的 `routes.php` 檔案，讓您不須使用完整的命名空間就可以註冊控制器路由。

<a name="sub-domain-routing"></a>
### 子網域路由

Laravel 路由一樣可以處理萬用字元的子網域，並且從網域中傳遞您的萬用字元參數：

#### 註冊子網域路由

	Route::group(['domain' => '{account}.myapp.com'], function()
	{

		Route::get('user/{id}', function($account, $id)
		{
			//
		});

	});

<a name="route-prefixing"></a>
### 路由前綴

群組路由可以透過群組的描述陣列中使用 `prefix` 選項，將群組內的路由加上前綴：

	Route::group(['prefix' => 'admin'], function()
	{

		Route::get('user', function()
		{
			//
		});

	});

<a name="route-model-binding"></a>
## 路由模型綁定

Laravel 模型綁定提供方便的方式將模型實體注入到您的路由中。例如，比起注入 User ID ，你可以選擇注入符合給定 ID 的 User 類別實體。

首先，使用路由的 `model` 方法指定特定參數要對應的類別，您應該在 `RouteServiceProvider::boot` 方法定義您的模型綁定：

#### 綁定參數至模型

	public function boot(Router $router)
	{
		parent::boot($router);

		$router->model('user', 'App\User');
	}

再來定義一個有 `{user}` 參數的路由：

	Route::get('profile/{user}', function(App\User $user)
	{
		//
	});

因為我們已經將 `{user}` 參數綁定到 `App\User` 模型，所以 `User` 實體將被注入到路由。所以舉例來說，請求至 `profile/1` 將注入 ID 為 1 的 `User` 實體。

> **注意：** 如果在資料庫中找不到匹配的模型實體，將引發 404 錯誤。

如果您想要自定「沒有找到」的行為，將閉包作為第三個參數傳入 `model` 方法：

	Route::model('user', 'User', function()
	{
		throw new NotFoundHttpException;
	});

如果您想要使用您自定的處理邏輯，您應該使用 `Router::bind` 方法。閉包透過 `bind` 方法將傳遞 URI 區段數值，並返回您想要被注入路由的類別實體：

	Route::bind('user', function($value)
	{
		return User::where('name', $value)->first();
	});

<a name="throwing-404-errors"></a>
## 拋出 404 錯誤

這裡有兩種方法從路由手動觸發 404 錯誤。首先，您可以使用 `abort` 輔助函式：

	abort(404);

`abort` 輔助函式只是簡單拋出帶有指定狀態代碼的 `Symfony\Component\HttpFoundation\Exception\HttpException`。

第二，您可以手動拋出 `Symfony\Component\HttpKernel\Exception\NotFoundHttpException` 的實體。

有關如何處理 404 例外狀況和自定回應的更多資訊，可以參考[錯誤](/docs/5.0/errors#http-exceptions)章節內的文件。
