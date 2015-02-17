# 認證

- [介紹](#introduction)
- [使用者認證](#authenticating-users)
- [取得經過認證的使用者](#retrieving-the-authenticated-user)
- [保護路由](#protecting-routes)
- [HTTP 基本認證](#http-basic-authentication)
- [忘記密碼與密碼重設](#password-reminders-and-reset)
- [社群認證](#social-authentication)

<a name="introduction"></a>
## 介紹

Laravel 的目標就是要讓實作認證機制變得簡單。事實上，幾乎所有的設定預設就已經完成了。有關認證的設定檔都放在 `config/auth.php` 裡，而在這些檔案裡也都包含了良好的註解，說明每一個選項的所對應的認證服務的方法。

Laravel 預設在 `app` 目錄內包含了一個使用 Eloquent 認證驅動的 `App\User` 模型。 

請記得！在建立模型結構時，密碼欄位至少要有 60 個字元長度。此外，在開始之前，請確認你的 `users` （或其他同義）資料表包含一個名為 `remember_token` 的欄位，欄寬 100 字元、字串型態、可接受 null。這個欄位將會被用來儲存「記住我」的 session token。可以在遷移檔裡透過 `$table->rememberToken();` 新增此欄位。當然，Laravel 5 預設已經建立好遷移欄位！

假設你的應用程式不是使用 Eloquent，你可以使用 Laravel 查詢產生器 `database` 認證驅動。

<a name="authenticating-users"></a>
## 使用者認證

Laravel 可以預設建立了兩個驗證相關的控制器。`AuthController` 處理新的使用者註冊和「登入」，而 `PasswordController` 可以幫助已經註冊的使用者重新設定忘記的密碼。

每個控制器使用 trait 引入需要的方法。在多數應用上，你不需要修改這些控制器。這些控制器用到的視圖放在 `resources/views/auth` 目錄下。你可以依照需求修改這些視圖。

### 使用者註冊

要修改應用程式註冊新使用者時所用到的表單欄位，可以修改 `App\Services\Registrar` 類別。這個類別負責驗證和建立應用程式的新使用者。

`Registrar` 的 `validator` 方法包含註冊新使用者的驗證規則，而 `Registrar` 的 `create` 方法負責建立一筆新的 `User` 在資料庫。你可以自由的修改這些方法。 `AuthController` 經由 `AuthenticatesAndRegistersUsers` trait 的方法呼叫 `Registrar`。

#### 手動認證

如果你不想使用預設的 `AuthController`，你需要直接 Laravel 的身分驗證類別管理使用者認證。別擔心，這也很簡單的！首先，讓我們看看 `attempt` 方法：

	<?php namespace App\Http\Controllers;

	use Auth;
	use Illuminate\Routing\Controller;

	class AuthController extends Controller {

		/**
		 * Handle an authentication attempt.
		 *
		 * @return Response
		 */
		public function authenticate()
		{
			if (Auth::attempt(['email' => $email, 'password' => $password]))
			{
				return redirect()->intended('dashboard');
			}
		}

	}

`attempt` 方法可以接受鍵值對組成的陣列作為第一個參數。`password` 的值先進行 [雜湊](/docs/5.0/hashing)。陣列中的其他值會被用來查詢資料表裡的使用者。所以，在上面的範例中，會依照 `email` 的值找出使用者。如果找到該使用者，會比對資料庫中的雜湊的密碼會和陣列裡的 `password` 值雜湊 。假設兩個雜湊密碼相同，會重新為使用者啟動認證通過的 session。

假設認證成功，`attempt` 將會回傳 `true`。否則，會回傳 `false`。

> **注意：**在上面的範例中，並不一定要使用 `email`，這只是作為範例。你應該使用對應到資料表中的「username」的任何鍵值。

`intended` 方法會重導到使用者嘗試要進入的 URL，其值會在進行認證過濾前被存起來。可以傳入預設的 URI，防止
重導的目的地無法使用。

#### 以特定條件驗證使用者

在認證過程中，你可能會想要增加額外的認證條件：

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1]))
    {
        // The user is active, not suspended, and exists.
    }

#### 判定使用者是否已驗證

判定一個使用者是否已經登入，你可以使用 `check` 方法：

	if (Auth::check())
	{
		// The user is logged in...
	}

#### 認證使用者並且「記住」他

假如你想要在應用程式內提供「記住我」的功能，你可以傳入布林值作爲 `attempt` 方法的第二個參數，這樣就可以保留使用者的認證身份（或直到他手動登出為止）。當然，你的 `users` 資料表必需包括一個字串型態的 `remember_token` 欄位來儲存「記住我」的標記。

	if (Auth::attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

假如有使用「記住我」功能，可以使用 `viaRemember` 方法判定使用者是否擁有「記住我」cookie 來判定使用者認證：

	if (Auth::viaRemember())
	{
		//
	}

#### 以 ID 認證使用者

要透過 ID 認證使用者，使用 `loginUsingId` 的方法：

	Auth::loginUsingId(1);

#### 驗證使用者資訊而不要登入

`validate` 方法可以讓你驗證使用者憑證資訊而不真的登入應用程式：

	if (Auth::validate($credentials))
	{
		//
	}

#### 在單一請求內登入使用者

你也可以使用 `once` 方法來讓使用者在單一請求內登入。不會有任何 session 或 cookie 被產生：

	if (Auth::once($credentials))
	{
		//
	}

#### 手動登入使用者

假如你需要將一個已存在的使用者實體登入應用程式，你可以呼叫 `login` 方法傳入實體：

	Auth::login($user);

這個方式和使用`attempt`方法驗證使用者的憑證資訊是一樣的。

#### 使用者登出

	Auth::logout();

當然，假設你使用 Laravel 內建的認證控制器，預設提供了讓使用者登出的方法。

#### 認證事件

當 `attempt` 方法被呼叫時，`auth.attempt` [事件](/docs/5.0/events) 會被觸發。假設嘗試認證成功而使用者登入了，`auth.login` 事件會被觸發。

<a name="retrieving-the-authenticated-user"></a>
## 取得經過認證的使用者

當使用者通過認證，有幾種方式取得使用者實例。

首先，你可以從 `Auth` facade 取得使用者：

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile()
		{
			if (Auth::user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

再來，你可以使用 `Illuminate\Http\Request` 實例取得認證過的使用者：

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Request $request)
		{
			if ($request->user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

第三，你可以使用 `Illuminate\Contracts\Auth\Authenticatable` contract 型別提示。這個型別提示可以用在控制器的建構子，控制器的方法，或是其他可以透過[服務容器](/docs/5.0/container) 解析的類別的建構子：

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\Authenticatable;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Authenticatable $user)
		{
			// $user is an instance of the authenticated user...
		}

	}

<a name="protecting-routes"></a>
## 保護路由

[路由中介層](/docs/5.0/middleware)只允許通過認證的使用者訪問指定的路由。Laravel 預設提供了 `auth` 中介層，放在 `app\Http\Middleware\Authenticate.php`。所以你需要做的是將其加到一個路由定義中：

	// With A Route Closure...

	Route::get('profile', ['middleware' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// With A Controller...

	Route::get('profile', ['middleware' => 'auth', 'uses' => 'ProfileController@show']);

<a name="http-basic-authentication"></a>
## HTTP 基本認證

HTTP 基本認證提供了一個快速的方式認證使用者，而不用特定設置一個「登入」頁。若要開始，請將 `auth.basic` 中介層增加到路由：

#### 使用 HTTP 基本認證保護路由

	Route::get('profile', ['middleware' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

在預設下 `basic` 中介層會使用使用者的 `email` 欄位當作「 username 」。

#### 設定無狀態的 HTTP 基本過濾器

你可能想要使用 HTTP 基本認證，但不會在 session 裡設置 使用者身份的設置 cookie，這在 API 認證時特別有用。如果要這樣做，[定義一個中介層](/docs/5.0/middleware)並呼叫 `onceBasic` 方法：

	public function handle($request, Closure $next)
	{
		return Auth::onceBasic() ?: $next($request);
	}

如果你使用 PHP FastCGI，HTTP 基本認證可能無法正常運作。在你的 `.htaccess` 檔案內新增以下程式碼：

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## 忘記密碼與重設

### 模型與資料表

大多數的網路應用程式都會提供使用者忘記密碼的功能。為了不讓開發者重複實作這個功能，Laravel 提供了方便的方法來寄送忘記密碼通知及密碼重設的功能。

在開始之前，請先確認你的 `User` 模型有實作 `Illuminate\Contracts\Auth\Remindable` contract。當然，預設 Laravel 的 `User` 模型已實作此介面，並且使用 `Illuminate\Auth\Reminders\Remindable` trait 引入所有需要實作的介面方法。

#### 產生 Reminder 資料表遷移

接下來，我們需要產生一個資料表來儲存重設密碼標記。Laravel 預設已有此資料表的遷移檔，放在 `database/migrations` 的目錄下。你所需要作的只有執行遷移：

	php artisan migrate

### 密碼重設控制器

Laravel 還包含了 `Auth\PasswordController` 其中包含重設使用者密碼的功能。預設甚至一些視圖，讓你可以開始使用！視圖在 `resources/views/auth` 目錄下。你可以按照你的應用程式設計，自由的修改這些視圖。

你的使用者會收到一封 e-mail，內含連結指向 `PasswordController` 中的 `getReset` 方法。這個方法會顯示密碼重設表單，允許使用者重新設定密碼。在密碼重新設定完後，使用者將會自動登入到應用程式中，然後被導向到 `/home`。你可以透過 `PasswordController` 中的 `redirectTo` 來定義重設密碼後要重導的位置：

	protected $redirectTo = '/dashboard';

> **注意：**預設，密碼重設 tokens 會在一小時後過期。你可以修改 `config/auth.php` 檔案裡的 `reminder.expire` 更改 這個設定。

<a name="social-authentication"></a>
## 社群認證

除了傳統已表單進行的認證，Laravel 還提供了簡單、方便的方式，使用 [Laravel Socialite](https://github.com/laravel/socialite) 進行 OAuth 認證。**Socialite 目前支援認證有 Facebook、 Twitter、Google、以及GitHub。** 

如果要開始使用社群認證，請將下面的程式碼加入到你的 `composer.json` 檔案內：

	"laravel/socialite": "~2.0"

接下來，在你的 `config/app.php` 設定檔裡註冊 `Laravel\Socialite\SocialiteServiceProvider`。也可以註冊 [facade](/docs/5.0/facades)：

	'Socialize' => 'Laravel\Socialite\Facades\Socialite',

你需要在應用程式加入 OAuth 服務所需的憑證到。這些憑證都放在 `config/services.php` 設定檔裡，並根據應用程式的需求使用 `facebook`、`twitter`、`google` 或 `github` 作為鍵值。例如：

	'github' => [
		'client_id' => 'your-github-app-id',
		'client_secret' => 'your-github-app-secret',
		'redirect' => 'http://your-callback-url',
	],

接下來就準備認證使用者了！你會需要兩個路由：一個用於將使用者重導到認證提供網站，另一個用於認證之後，從認證服務接收回饋。下面是一個使用 `Socialize` facade 的範例：

	public function redirectToProvider()
	{
		return Socialize::with('github')->redirect();
	}

	public function handleProviderCallback()
	{
		$user = Socialize::with('github')->user();

		// $user->token;
	}

`redirect` 方法將使用者重導到認證 OAuth 的網站，而 `user` 方法會讀取傳回的要求，以及從認證網站取得使用者的資訊。再重新導向使用者之前，你也可以設定請求的「 scopes 」：

	return Socialize::with('github')->scopes(['scope1', 'scope2'])->redirect();

一旦你取得使用者實例，你能獲取更多的使用者詳細資訊：

#### 取得使用者資料

	$user = Socialize::with('github')->user();

	// OAuth Two Providers
	$token = $user->token;

	// OAuth One Providers
	$token = $user->token;
	$tokenSecret = $user->tokenSecret;

	// All Providers
	$user->getNickname();
	$user->getName();
	$user->getEmail();
	$user->getAvatar();
