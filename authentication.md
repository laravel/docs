# 認證

- [介紹](#introduction)
- [使用者認證](#authenticating-users)
- [擷取經過認證的使用者](#retrieving-the-authenticated-user)
- [保護路由](#protecting-routes)
- [HTTP 簡易認證](#http-basic-authentication)
- [忘記密碼與密碼重設](#password-reminders-and-reset)
- [社群認證](#social-authentication)

<a name="introduction"></a>
## 介紹

Laravel 的目標就是要讓實作認證機制變得簡單。事實上，幾乎所有的設定預設就已經完成了。有關認證的設定檔都放在 `config/auth.php` 裡，而在這些檔案裡也都包含了良好的註解說明每一個選項的所對應的認證服務的方法。

Laravel 預設在 `app` 資料夾內就包含了一個使用 Eloquent 認證驅動的 `App\User` 模型。 

請記得！在建立模型結構時，密碼欄位至少要有 60 個字元長度。此外，在開始之前，請確認你的 `users` (或其他同義)資料表包含一個名為 `remember_token` 的欄位，欄寬 100 字元、字串型態、可接受 null。這個欄位將會被用來儲存「記住我」的 session token。這可以透過 `$table->rememberToken();` 在遷移中。當然，可以使用預設 Laravel 5 所有遷移欄位！

假設你的應用程式不是使用 Eloquent，你可以使用 Laravel 搜尋架構器 `database` 認證驅動。

<a name="authenticating-users"></a>
## 使用者認證

Laravel 可以使用預設兩個相關驗證控制器。`AuthController` 處理新的使用者註冊和「登入」，而 `PasswordController` 可以幫助已經註冊的使用者卻忘記密碼，重新設定密碼。

每個控制器包含必要的方法並且使用他們的特點。對於許多應用程式，你不需要去修改這些控制器。這些控制器呈現視圖在 `resources/views/auth` 的資料夾。你可以自由的自訂這些視圖。

### 使用者記錄員

當一個新的使用者註冊你的應用程式需要修改表單，你可以修改 `App\Services\Registrar` 類別。這個應用程式類別負責驗證和建立新的使用者。

在 `Registrar` 的 `validator` 方法包含應用程式新的使用者的驗證規則，而 `Registrar` 的 `create` 方法負責建立新的 `User` 記錄在你的資料庫。你可以自由的修改這些方法。經由 `AuthenticatesAndRegistersUsers` 方法特點 `AuthController` 去呼叫 `Registrar`。

#### 手動登入使用者

如果你選擇不執行提供的 `AuthController`，可以直接使用 Laravel 身分驗證類別，你需要管理你的使用者身份驗證，別擔心！這是很簡單的！首先，讓我們確認 `attempt` 方法：

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

在 `attempt` 的方法可以接受陣列或是 key/value 當作第一個參數。 則 `password` 的值會是 [雜湊的](/docs/5.0/hashing)。其他陣列中的值可以用來查詢使用者在資料庫內的資料表。所以，在上面的範例中，使用者會擷取到 `email` 的值。如果找到該使用者，資料庫中儲存的雜湊的密碼會和通過陣列傳遞方式的雜湊 `password` 做比較。假設兩個雜湊密碼相同，將為使用者啟動新的身份認證 session。

假設認證成功，`attempt` 將會回傳 `true`。否則，會回傳 `false`。

> **注意：** 在這個範例，`email` 不是必需的選項，他只是一個範例。你應該使用任何欄位名稱對應到資料庫中的「username」。

通過認證篩選器，在嘗試存取之前，`intended` 重導功能會將使用者重導到指定的 URL。在返回 URL 時可以使用這個方法，以防預定的目標無法使用。

#### 條件認證使用者

在認證過程中，你可能會想要增加額外的認證條件：

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1]))
    {
        // The user is active, not suspended, and exists.
    }

#### 判定使用者是否已登入

判定一個使用者是否已經登入您的應用程式，你可以使用 `check` 這個方法：

	if (Auth::check())
	{
		// The user is logged in...
	}

#### 認證一個使用者並且「記住」他

假如你想要在你的應用程式內提供「記住我」的選項，你可以在 `attempt` 方法的第二個參數給布林值，這樣就可以保留使用者的認證身份 (或直到他手動登出為止)。當然，你的 `users` 資料表必需包括一個字串型態的 `remember_token` 欄位來儲存「記住我」的標記。

	if (Auth::attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

假如你讓使用者透過「記住我」的方式來登入，則你可以使用 `viaRemember` 方法來判定使用者是否擁有「記住我」cookie 來認證使用者登入：

	if (Auth::viaRemember())
	{
		//
	}

#### 認證使用者的 ID

使用者登入應用程式透過 ID，可以使用 `loginUsingId` 的方法：

	Auth::loginUsingId(1);

#### 驗證使用者資訊而不要登入

`validate` 方法可以讓你驗證使用者資訊而不真的登入應用程式：

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

假如你需要將一個已存在的使用者實體登入您的應用程式，你可以用該實體很簡單的呼叫 `login` 方法：

	Auth::login($user);

這個方式和用使用者帳號密碼來 `attempt` 的功能是一樣的。

#### 登出使用者

	Auth::logout();

當然，假設你使用 Laravel 內建的認證控制器，可以透過控制器處理使用者在應用程式的日誌記錄。

#### 認證事件

當 `attempt` 方法被呼叫時，`auth.attempt` [事件](/docs/5.0/events) 會被啟動。假設嘗試認證是成功的以及使用者成功登入，`auth.login` 事件會被啟動。

<a name="retrieving-the-authenticated-user"></a>
## 擷取經過認證的使用者

一旦通過身分認證的使用者，有幾種方式來得到使用者的實例。

首先，你可以從 `Auth` facade 存取使用者：

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

再來，你可以存取認證使用者透過 `Illuminate\Http\Request` 範例：

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

最後，你可以用類型提示 `Illuminate\Contracts\Auth\Authenticatable` contract。這個類型提示可以增加到控制器的建構函式，控制器的方法或是其他的建構函式類別可以透過 [服務容器](/docs/5.0/container) 解決：

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

[路由中介層](/docs/5.0/middleware) 只允許通過認證的使用者存取指定的路由。Laravel 預設提供 `auth` 中介層，而被定義在 `app\Http\Middleware\Authenticate.php`。所以你需要做的是將連接定義到一個路由：

	// With A Route Closure...

	Route::get('profile', ['middleware' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// With A Controller...

	Route::get('profile', ['middleware' => 'auth', 'uses' => 'ProfileController@show']);

<a name="http-basic-authentication"></a>
## HTTP 簡易認證

HTTP 簡易認證提供了一個快速的方式來認證使用者而不用特定設置一個「登入」頁。若要開始，請將 `auth.basic` 中介增加到你的路由：

#### Protecting A Route With HTTP Basic

	Route::get('profile', ['middleware' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

在預設下 `basic` 中介會使用 `email` 使用者記錄欄位當作「username」。

#### 設定無狀態的 HTTP 簡易過濾器

一般在實作 API 認證時，往往會想要使用 HTTP 簡易認證而不要產生任何 session 或 cookie。如果要這這樣做 [定義一個中介層](/docs/5.0/middleware) 並回傳 `onceBasic` 方法來達成：

	public function handle($request, Closure $next)
	{
		return Auth::onceBasic() ?: $next($request);
	}

如果你使用 PHP FastCGI，HTTP 簡易認證預設是無法正常運作的。請在你的 `.htaccess` 檔案內新增以下程式碼來啟動這個功能：

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## 忘記密碼與重設

### 模型與資料表

大多數的網路應用程式都會提供使用者忘記密碼的功能。為了不讓開發者重複實作這個功能，Laravel 提供了方便的方法來寄送忘記密碼通知及密碼重設的功能。

在開始之前，請先確認你的 `User` 模型有實作 `Illuminate\Contracts\Auth\Remindable` contract。當然，預設 Laravel 的 `User` 模型本身就已實作，並且使用 `Illuminate\Auth\Reminders\Remindable` 來包括所有需要實作的介面方法。

#### 產生 Reminder 資料表遷移

接下來，我們需要產生一個資料表來儲存重設密碼標記。Laravel 預設是包含遷移此資料表，以及放在 `database/migrations` 的目錄。所以你需要做這個遷移：

	php artisan migrate

### 密碼重設控制器

Laravel 還包含了 `Auth\PasswordController` 其中包含重設使用者的密碼的功能。我們甚至提供一些視圖，讓你可以開始使用，而視圖被放在 `resources/views/auth` 目錄。你可以按照你的應用程式設計，自由的修改這些視圖。

你的使用者會收到一封 e-mail 連結，並且指向 `PasswordController` 中的 `getReset` 方法。這個方法可以呈現密碼重設的表單以及允許使用者重新設定他們的密碼。在密碼重新設定完後，使用者將會自動登入到應用程式中，然後被導向到 `/home`。你可以透過 `PasswordController` 中的 `redirectTo` 來定義重設後要被導向的位置：

	protected $redirectTo = '/dashboard';

> **注意：** 在預設下，密碼必須在一個小時內重設完成。你可以透過修改 `config/auth.php` 檔案裡的 `reminder.expire` 這個選項。

<a name="social-authentication"></a>
## 社群認證

除了典型的表單基本認證，Laravel 還提供了簡單、方便的方式 [Laravel Socialite](https://github.com/laravel/socialite)，使用 OAuth 進行認證。**Socialite 目前支援認證有 Facebook、 Twitter、Google、以及GitHub。** 

如果要開始使用社群認證，請將下面的程式碼加入到你的 `composer.json` 檔案內：

	"laravel/socialite": "~2.0"

接下來，在你的 `config/app.php` 設定檔裡註冊 `Laravel\Socialite\SocialiteServiceProvider`。也可以註冊 [facade](/docs/5.0/facades)：

	'Socialize' => 'Laravel\Socialite\Facades\Socialite',

你需要透過 OAuth 服務，增加憑證到你的應用程式。這些憑證都放在 `config/services.php` 設定檔裡，以及應該使用這些金鑰 `facebook`、`twitter`、`google` 或 `github`，根據你的供應商應用程式的要求。例如：

	'github' => [
		'client_id' => 'your-github-app-id',
		'client_secret' => 'your-github-app-secret',
		'redirect' => 'http://your-callback-url',
	],

接下來，你準備好要要進行認證使用者！你會需要兩個路由：一個用於重新定向使用者的 OAuth 供應商，另一個用於認證之後，從供應商接收回傳認證。這裡是一個範例使用 `Socialize` facade：

	public function redirectToProvider()
	{
		return Socialize::with('github')->redirect();
	}

	public function handleProviderCallback()
	{
		$user = Socialize::with('github')->user();

		// $user->token;
	}

`redirect` 方法將使用者發送到 OAuth 供應商，雖然 `user` 方法會讀取傳入的要求，以及從供應商擷取使用者的資訊。再重新導向使用者之前，你也可以設定「範圍」的要求：

	return Socialize::with('github')->scopes(['scope1', 'scope2'])->redirect();

一旦你有一個使用者實例，你能獲取更多的使用者詳細資訊：

#### 擷取使用者的細項

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
