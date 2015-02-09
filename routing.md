# HTTP 路由

- [基本路由](#basic-routing)
- [CSRF 保護](#csrf-protection)
- [方法欺騙](#method-spoofing)
- [路由參數](#route-parameters)
- [指名路由](#named-routes)
- [路由群組](#route-groups)
- [路由模型綁定](#route-model-binding)
- [拋出 404 錯誤](#throwing-404-errors)

<a name="basic-routing"></a>
## 基本路由

您將在您應用中的 `app/Http/routes.php` 的檔案載入了 `App\Providers\RouteServiceProvider` 類別來定義大多數的路由。大多數基本的 Laravel 路由都只透過 URI 和 `閉包(Closure)`：

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

通常情況下，您將會需要為您的路由產生 URL，您可以使用 `url` 輔助函數來操作：

	$url = url('foo');

<a name="csrf-protection"></a>
## CSRF 保護

Laravel 提供簡易的方法，讓您可以保護您的應用程式不受到 [CSRF (跨網站請求偽造)]((http://en.wikipedia.org/wiki/Cross-site_request_forgery) 攻擊。跨網站請求偽造是一種惡意的攻擊，藉以代表經過身份驗證的使用者執行未經授權的命令。

Laravel 會自動在每一位使用者的 session 中放置隨機的 `token`，這個 token 將被用來確保經過驗證的使用者是實際發出請求至應用程式的使用者：

#### 插入 CSRF Token 到表單

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

當然也可以在 Blade [模板引擎](/docs/5.0/templates)使用：

	<input type="hidden" name="_token" value="{{ csrf_token() }}">

您不需要手動驗證在 POST, PUT, DELETE 請求的 CSRF token。`VerifyCsrfToken`  [HTTP 中介層](/docs/5.0/middleware)將儲存在 session 中的請求輸入的 token 配對來驗證 token。

除了尋找 CSRF token 作為 「POST」參數，中介層也檢查 `X-XSRF-TOKEN` 請求標頭，這在多數 Javascript framework 常被拿來使用。

<a name="method-spoofing"></a>
## 方法欺騙

HTML 表單沒有支援 `PUT` 或 `DELETE` 動作。所以當定義 `PUT` 或 `DELETE` 路由並在 HTML 表單中被呼叫的時候，您將需要添加隱藏 `_method` 欄位在表單中。

將數值同 `_method` 欄位發送使用 HTTP 請求方法。舉例來說：

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
    	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">
    </form>

<a name="route-parameters"></a>
## 路由參數

當然，您可以再您的路由獲取請求的 URI 區段。

#### 基礎路由參數

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

#### 選項路由參數

	Route::get('user/{name?}', function($name = null)
	{
		return $name;
	});

#### 帶預設值的路由參數

	Route::get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

#### 正規表達式參數約束

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

#### 傳替陣列約束

	Route::get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+'])

#### 定義全域模式

如果妳喜歡路由參數總是被約束一個給定的正規表達式下，您可以使用 `pattern` 方法。您應該在 `before` 方法的 `RouteServiceProvider` 定義模式：

	$router->pattern('id', '[0-9]+');

一個模式被定義，這使用的參數被應用在所有的路由上：

	Route::get('user/{id}', function($id)
	{
		// 只有 {id} 是數字才被呼叫。
	});

#### 允許路由參數

如果您需要允許外部路由參數，請使用 `input` 方法：

	if ($route->input('id') == 1)
	{
		//
	}

您也可以允許當前路由參數訪問 `Illuminate\Http\Request` 實體。當前請求的請求實體可以透過 `Request` facade 訪問，或透過類型提示 `Illuminate\Http\Request` 依賴注入：

	use Illuminate\Http\Request;

	Route::get('user/{id}', function(Request $request, $id)
	{
		if ($request->route('id'))
		{
			//
		}
	});

<a name="named-routes"></a>
## 指名路由

指名路由在產生 URL 與重導至特定路由時更為方便。您可以用 `as` 的陣列鍵指定名稱給指定的路由：

	Route::get('user/profile', ['as' => 'profile', function()
	{
		//
	}]);

您一樣可以為控制器動作指定的路由名稱：

	Route::get('user/profile', [
        'as' => 'profile', 'uses' => 'UserController@showProfile'
	]);

現在您可以在產生 URL 或重導時使用該路由名稱：

	$url = route('profile');

	$redirect = redirect()->route('profile');

`currentRouteName` 方法會返回目前請求的路由名稱：

	$name = Route::currentRouteName();

<a name="route-groups"></a>
## 路由群組

有時候您需要套用篩選器到群組的路由上。不需要為每個路由去套用篩選器，您只需使用路由群組：

	Route::group(['before' => 'auth'], function()
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

您一樣可以在 `group` 陣列中使用 `namespace` 參數，指定在這 group 中的控制器都有共同的命名空間：

	Route::group(['namespace' => 'Admin'], function()
	{
		//
	});

> **注意：** 在預設情況下，`RouteServiceProvider` 包含內建您命名空間群組的 `routes.php` 檔案，允許您不須指定完整的命名空間來註冊控制器路由。

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

Laravel 模型綁定提供方便的方式將模型實體注入到您的路由中。例如，要注入使用者 ID 您可以注入符合給定 ID 的整個使用者模型實體。

首先，使用 `model` 方法來給參數指令的類別，您應該在 `RouteServiceProvider::boot` 方法定義您的模型綁定：

#### 綁定參數至模型

	public function boot(Router $router)
	{
		parent::boot($router);

		$router->model('user', 'App\User');
	}

再來定義路由包涵 `{user}` 參數：

	Route::get('profile/{user}', function(App\User $user)
	{
		//
	});

從我們有 `{user}` 綁定參數到 `App\User` 模型，`User` 實體將注入路由。所以舉例來說，請求至 `profile/1` 將注入有 ID 為 1 的 `User` 實體。

> **注意：** 如果在資料庫中找不到匹配的模型實體，將引發 404 錯誤。

如果您想要指定您自己的「沒有找到」的行為，將閉包作為第三個參數傳入 `model` 方法：

	Route::model('user', 'User', function()
	{
		throw new NotFoundHttpException;
	});

如果您想要使用您自己決定的邏輯，您應該使用 `Router::bind`方法。閉包透過 `bind` 方法將傳遞 URI 區段數值，並應該返回您想要被注入路由的類別實體：

	Route::bind('user', function($value)
	{
		return User::where('name', $value)->first();
	});

<a name="throwing-404-errors"></a>
## 拋出 404 錯誤

這裡有兩種方法從路由手動切換 404 錯誤。首先，您可以使用 `abort` 輔助函數：

	abort(404);

`abort` 輔助函數只拋出 `Symfony\Component\HttpFoundation\Exception\HttpException` 帶有特定狀態代碼。

第二，您可以手動拋出實體 `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`。

有關如何處理 404 例外狀況和自定回應的更多資訊，可以參考 [錯誤](/docs/5.0/errors#http-exceptions) 章節內的文件。
