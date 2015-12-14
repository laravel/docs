# 認證

- [介紹](#introduction)
    - [資料庫注意事項](#introduction-database-considerations)
- [認證快速入門](#authentication-quickstart)
    - [路由](#included-routing)
    - [視圖](#included-views)
    - [認證](#included-authenticating)
    - [取得已認證之使用者](#retrieving-the-authenticated-user)
    - [保護路由](#protecting-routes)
    - [認證限制](#authentication-throttling)
- [手動認證使用者](#authenticating-users)
    - [記住使用者](#remembering-users)
    - [其他認證方法](#other-authentication-methods)
- [HTTP 基礎認證](#http-basic-authentication)
     - [無狀態 HTTP 基礎認證](#stateless-http-basic-authentication)
- [重設密碼](#resetting-passwords)
    - [重設資料庫](#resetting-database)
    - [路由](#resetting-routing)
    - [視圖](#resetting-views)
    - [重設密碼後](#after-resetting-passwords)
- [社群認證](#social-authentication)
- [新增客製化認證驅動](#adding-custom-authentication-drivers)
- [事件](#events)

<a name="introduction"></a>
## 介紹

Laravel 讓實作認證變得非常簡單。事實上，幾乎所有東西都是可以藉由設定來直接使用。認證設定檔被放在 `config/auth.php`，其中包含了幾個有良好文件的選項，以此來調整認證服務的行為。

<a name="introduction-database-considerations"></a>
### 資料庫注意事項

預設的 Laravel 在你的 `app` 資料夾中含有 `App\User` [Eloquent 模型](/docs/{{version}}/eloquent)。這個模型使用預設的 Eloquent 認證來驅動。如果你的應用程式沒有使用 Eloquent，你可以使用 Laravel 查詢生成器的 `database` 認證驅動。

為 `App\User` 模型建立資料庫結構時，確認密碼欄位最少有 60 字元長。

同時，你需要確認你的 `users` (或是相同意義的) 資料表含有 nullable 、100 字元長的 `remember_token` 欄位，這個欄位將會被用來儲存「記住我」 session 的標記。只要在遷移時，使用 `$table->rememberToken()`，即可輕鬆加入這個欄位。

<a name="authentication-quickstart"></a>
## 認證快速入門

Laravel 帶有兩種認證控制器，它們被放置在 `App\Http\Controllers\Auth` 命名空間，`AuthController` 處理使用者註冊及認證，而 `PasswordController` 負責處理重置使用者的密碼。這些控制器使用了 trait 來包含所需要的方法，對於大多數的應用程式而言，你並不需要修改這些控制器。

<a name="included-routing"></a>
### 路由

預設中，沒有[路由](/docs/{{version}}/routing)指向這些認證控制器，你需要自己新增到 `app/Http/routes.php` 中。

    // 認證路由...
    Route::get('auth/login', 'Auth\AuthController@getLogin');
    Route::post('auth/login', 'Auth\AuthController@postLogin');
    Route::get('auth/logout', 'Auth\AuthController@getLogout');

    // 註冊路由...
    Route::get('auth/register', 'Auth\AuthController@getRegister');
    Route::post('auth/register', 'Auth\AuthController@postRegister');

<a name="included-views"></a>
### 視圖

雖然這些認證控制器被包含在框架中，你仍需提供[視圖](/docs/{{version}}/views)給控制器來算圖（render），而視圖需要被放置在 `resources/views/auth` 資料夾中，你可以任意的客製化此視圖。登入視圖應該被放在 `resources/views/auth/login.blade.php` 而註冊視圖則放在 `resources/views/auth/register.blade.php`。

#### 認證表單範例

    <!-- resources/views/auth/login.blade.php -->

    <form method="POST" action="/auth/login">
        {!! csrf_field() !!}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password" id="password">
        </div>

        <div>
            <input type="checkbox" name="remember"> Remember Me
        </div>

        <div>
            <button type="submit">Login</button>
        </div>
    </form>

#### 註冊表單範例

    <!-- resources/views/auth/register.blade.php -->

    <form method="POST" action="/auth/register">
        {!! csrf_field() !!}

        <div>
            Name
            <input type="text" name="name" value="{{ old('name') }}">
        </div>

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div>
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">Register</button>
        </div>
    </form>

<a name="included-authenticating"></a>
### 認證

現在你已經為認證控制器設定好了路由及視圖，你可以準備在你的應用程式註冊新使用者並認證他。你只要簡單地在瀏覽器存取你定義的路由，認證控制器早已包含了處理認證現有使用者，及儲存新使用者在資料庫的邏輯了（透過他們各自的 traits）。

當使用者成功的認證後，他們將被導向 `/home` URI，而你需要向路由註冊這個 URI 來處理這個請求，你可以客製化認證後，轉向的 URI，只需要修改 `AuthController` 的 `redirectPath` 屬性：

    protected $redirectPath = '/dashboard';

當使用者認證失敗，將會被重導到 `/auth/login` URI。你可以設定 `AuthController` 的 `loginPath` 屬性來自訂認證失敗後的重導位置：

    protected $loginPath = '/login';

`loginPath` 並不會改變當使用者存取受保護的路由時所重導的路徑。該路徑是由 `App\Http\Middleware\Authenticate` 中介層的 `handle` 方法所控制。

#### 客製化

如果想要修改註冊時的表單欄位，或是客製化如何將新使用者的記錄寫入資料庫，你可以修改 `AuthController` 類別，這個類別負責驗證和創造新的使用者。

`AuthController` 的 `validator` 方法包含了對於新使用者的驗證規則。你可以隨意的修改這個方法。

`AuthController` 的 `create` 方法負責使用 [Eloquent ORM](/docs/{{version}}/eloquent) 創造新的 `App\User` 紀錄到你的資料庫。你可以根據需求任意修改這個方法。

<a name="retrieving-the-authenticated-user"></a>
### 取得已認證之使用者

你可以透過 `Auth` facade 來存取認證的使用者。

    $user = Auth::user();

也有另外一種方法可以存取認證過的使用者，就是透過 `Illuminate\Http\Request` 實例：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class ProfileController extends Controller
    {
        /**
         * 更新使用者的資料
         *
         * @param  Request  $request
         * @return Response
         */
        public function updateProfile(Request $request)
        {
            if ($request->user()) {
                // $request->user() 回傳認證過的使用者的實例...
            }
        }
    }

#### 確認現在的使用者是否認證過

為了確認使用者是否已經登入，你可以使用 `Auth` facade 的 `check` 方法，如果認證過，將會回傳 `true`：

    if (Auth::check()) {
        // 這個使用者已經登入...
    }

不過，在允許該使用者存取特定的路由或控制器之前，你可以使用中介層來確認這個使用者是否認證過。想得到更多資訊，請閱讀[保護路由](/docs/{{version}}/authentication#protecting-routes)的文件。

<a name="protecting-routes"></a>
### 保護路由

[路由中介層](/docs/{{version}}/middleware)使用於限定認證過的使用者存取指定的路由，Laravel 提供了 `auth` 中介層來達到這個目的，而這個中介層被定義在 `app\Http\Middleware\Authenticate.php` 中，你只需要將它應用到路由定義中：

    // 使用路由閉包...

    Route::get('profile', ['middleware' => 'auth', function() {
        // 只有認證過的使用者能進來這裡...
    }]);

    // 使用控制器...

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'ProfileController@show'
    ]);

當然，如果你正在使用[控制器類別](/docs/{{version}}/controllers)，你可以在建構子中呼叫 `middleware` 方法，而不是在路由中直接定義它：

    public function __construct()
    {
        $this->middleware('auth');
    }

<a name="authentication-throttling"></a>
### 認證限制

如果你使用 Laravel's 內建的 `AuthController` 類別，可以透過 `Illuminate\Foundation\Auth\ThrottlesLogins` trait 在你的應用程式限制登入次數。預設情況下，如果使用者在幾次嘗試後仍不能提供正確的憑證，將在一分鐘內無法進行登入。這個限制會特別針對使用者的用戶名稱 / 郵件地址和他們的 IP 位址：

    <?php

    namespace App\Http\Controllers\Auth;

    use App\User;
    use Validator;
    use App\Http\Controllers\Controller;
    use Illuminate\Foundation\Auth\ThrottlesLogins;
    use Illuminate\Foundation\Auth\AuthenticatesAndRegistersUsers;

    class AuthController extends Controller
    {
        use AuthenticatesAndRegistersUsers, ThrottlesLogins;

        // Rest of AuthController class...
    }

<a name="authenticating-users"></a>
## 手動認證使用者

當然，你不一定要使用 Laravel 內建的認證控制器，如果你選擇刪除這些控制器，你將需要自己處理使用者認證，並使用 Laravel 的認證控制器。

我們將透過 `Auth` [facade](/docs/{{version}}/facades) 存取 Laravel 的認證服務，所以我們需要確認是否在類別的最上面引入 `Auth` facade，接下來讓我們看一下 `attempt` 方法：

    <?php

    namespace App\Http\Controllers;

    use Auth;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * 處理認證
         *
         * @return Response
         */
        public function authenticate()
        {
            if (Auth::attempt(['email' => $email, 'password' => $password])) {
                // 認證通過...
                return redirect()->intended('dashboard');
            }
        }
    }

`attempt` 方法的第一個參數接受陣列，在這個陣列的值用來找尋資料庫裡的使用者資料，所以在上面的範例中，使用者會藉由 `email` 欄位抽取，如果使用者被找到了，資料庫裡經過雜湊的密碼將會與陣列中雜湊的 `password` 值做比對，如果兩個一樣的話經會開啟一個通過認證的 session 給使用者。

如果認證成功，`attempt` 方法將會回傳 `true`，反之則為 `false`。

重導器上的 `intended` 方法將會重導使用者回原本想要進入的頁面，也可以傳入一個回退 URI 至這個方法，以避免要轉回的頁面不可使用。

如果你希望，你也可以加入除了使用者的電子信箱及密碼的額外條件至認證查詢。例如，我們要確認使用者是否被標記為 `active`：

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        //這個使用者是啟動的，沒有被停權，而且存在
    }

為了讓使用者登出，你可以使用 `Auth` facade 的 `logout` 方法。這個方法會清除所有認證後加入到使用者 session 的資料：

    Auth::logout();

> **注意：**在這些例子中，`email` 不是一個一定要有的選項，它僅僅是被用來當作範例，你可以用任何欄位，只要它在資料庫的意思等同於「使用者名稱」。

<a name="remembering-users"></a>
## 記住使用者

如果你想要提供「記住我」的功能，你需要傳入一個布林值到 `attempt` 方法的第二個參數，這會永久保持使用者的 session 直到登出。你的 `users` 資料表一定要包含一個 `remember_token` 欄位，這是用來儲存「記住我」的標記。

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // 這個使用者被記住了...
    }

如果你是被記住的使用者，你可以使用 `viaRemember` 方法來確認這個使用者是否使用「記住我」 cookie 來做認證：

    if (Auth::viaRemember()) {
        //
    }

<a name="other-authentication-methods"></a>
### 其他認證方法

#### 用使用者實例做認證

如果你需要使用存在的使用者實例來登入，你需要呼叫 `login` 方法，並傳入使用實例，這個物件必須是由 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/{{version}}/contracts) 所實現。當然，`App/User` 模型已經實現了這個介面：

    Auth::login($user);

#### 用使用者 ID 做認證

如果你需要使用使用者的 ID 來登入，你需要使用 `loginUsingId` 方法，這個方法接受要登入的使用者的主鍵：

    Auth::loginUsingId(1);

#### 只在這次認證使用者

你可以使用 `once` 方法來只針對一次的請求來認證使用者，沒有任何的 session 或 cookie 會被使用，這個對於建議無狀態的 API 非常的有用，`once` 方法跟 `attempt` 方法擁有同樣的傳入參數：

    if (Auth::once($credentials)) {
        //
    }

<a name="http-basic-authentication"></a>
## HTTP 基礎認證

[HTTP 基礎認證](http://en.wikipedia.org/wiki/Basic_access_authentication)提供一個快速的方法來認證使用者，不需要任何「登入」頁面。開始之前，先增加 `auth.basic` [中介層](/docs/{{version}}/middleware)到你的路由，`auth.basic` 中介層已經被包含在 Laravel 框架中，所以你不需要定義它：

    Route::get('profile', ['middleware' => 'auth.basic', function() {
        // 只有認證過的使用者可進入...
    }]);

一旦中介層被增加到路由上，當使用瀏覽器進入這個路由時，你將自動的被提示需要提供憑證。預設上，`auth.basic` 中介層將會使用使用者的 `email` 欄位當作「使用者名稱」。

#### FastCGI 的注意事項

如果是正在使用 FastCGI，HTTP 基礎認證可能無法正常運作，你需要將下面這幾行加入你 `.htaccess` 檔案中：

    RewriteCond %{HTTP:Authorization} ^(.+)$
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="stateless-http-basic-authentication"></a>
### 無狀態 HTTP 基礎認證

你可以使用 HTTP 基礎認證而不用在 session 中設定使用者認證用的 cookie，這個功能對 API 認證來說非常有用。為了達到這個目的，[定義一個中介層](/docs/{{version}}/middleware)並這個中介層會呼叫 `onceBasic` 方法。如果沒有任何回應從 `onceBasic` 方法返回的話，這個請求會直接傳進應用程式中：

    <?php

    namespace Illuminate\Auth\Middleware;

    use Auth;
    use Closure;

    class AuthenticateOnceWithBasicAuth
    {
        /**
         * 處理請求
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return Auth::onceBasic() ?: $next($request);
        }

    }

接著，[註冊這個路由中介層](/docs/{{version}}/middleware#registering-middleware)，然後將它增加在一個路由上：

    Route::get('api/user', ['middleware' => 'auth.basic.once', function() {
        // 只有認證過的使用者可以進入...
    }]);

<a name="resetting-passwords"></a>
## 重設密碼

<a name="resetting-database"></a>
### 重設資料庫

很多網路應用程式提供使用者一些方式來重設密碼，Laravel 提供便利的方法來傳送密碼提示和實現密碼重設，而不是強迫你重新實作這些功能一次。

開始之前，請先確認你的 `App\User` 模型實作了 `Illuminate\Contracts\Auth\CanResetPassword` contract。當然，原有的 `App\User` 早已實作了這個介面，並且使用 `Illuminate\Auth\Passwords\CanResetPassword` trait 引入實現這個介面所需要的方法。

#### 產生重置標記的資料表遷移檔

接下來，必須要創建一個資料表來儲存密碼的重置標記，而這個資料表的遷移已經包含在 Laravel 中了，就被放在 `database/migrations` 資料夾裡。所以，你要做的就是做一次遷移：

    php artisan migrate

<a name="resetting-routing"></a>
### 路由

Laravel 包含了 `Auth\PasswordController`，而它含有所有重置使用者密碼的邏輯。但是，你仍需要指定路由到這個控制器：

    // 密碼重置連結的路由...
    Route::get('password/email', 'Auth\PasswordController@getEmail');
    Route::post('password/email', 'Auth\PasswordController@postEmail');

    // 密碼重置的路由...
    Route::get('password/reset/{token}', 'Auth\PasswordController@getReset');
    Route::post('password/reset', 'Auth\PasswordController@postReset');

<a name="resetting-views"></a>
### 視圖

除了定義 `PasswordController` 的路由，你也需要提供視圖給這個控制器。不過不用擔心，我們已經提供了範例視圖來幫助你開始，當然你可以隨意的定義你的表單風格。

#### 重置密碼連結的請求表單範例

你將會需要提供 HTML 視圖給密碼重置的請求表單。這些視圖被放在 `resources/views/auth/password.blade.php`。這個表單提供了單一的欄位來給使用者輸入電子郵件，讓他們可以收到密碼重置連結：

    <!-- resources/views/auth/password.blade.php -->

    <form method="POST" action="/password/email">
        {!! csrf_field() !!}

        @if (count($errors) > 0)
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        @endif

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <button type="submit">
                傳送重置密碼連結
            </button>
        </div>
    </form>

當使用者送出重置密碼的請求，他們會收到一封有連結到 `PasswordController` 的 `getReset` 方法（通常是路由到 `/password/reset`）的電子郵件。你將需要為電子郵件創造一個 `resources/views/emails/password.blade.php` 視圖。這個視圖會接收一個帶有密碼重置標記的 `$token` 變數，這個變數含有了密碼重置標記來匹配使用者的密碼重置請求，以下是範例來讓你開始：

    <!-- resources/views/emails/password.blade.php -->

    點擊此處重置你的密碼：{{ url('password/reset/'.$token) }}

#### 密碼重置表單的範例

當使用者點擊了電子郵件的連結來重置密碼，將會顯示一個密碼重置表單，這個視圖被放在 `resources/views/auth/reset.blade.php`。

這裡有個密碼重置表單的範例：

    <!-- resources/views/auth/reset.blade.php -->

    <form method="POST" action="/password/reset">
        {!! csrf_field() !!}
        <input type="hidden" name="token" value="{{ $token }}">

        @if (count($errors) > 0)
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        @endif

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div>
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">
                Reset Password
            </button>
        </div>
    </form>

<a name="after-resetting-passwords"></a>
### 重設密碼後

一旦你定義了路由跟視圖來重置使用者的密碼，你只需要在瀏覽器存取這個路由。Laravel 中的 `PasswordController` 已經包含了傳送密碼重置連結的電子郵件，及更新密碼到資料庫的邏輯。

密碼重置以後，這個使用者會自動登入，並導向 `/home`。你可以自己客製化導向的目標，只要定義 `PasswordController` 的 `redirectTo` 屬性：

    protected $redirectTo = '/dashboard';

> **注意：**預設上，密碼重置標記會在一個小時後過期，你可以更改 `config/auth.php` 的 `reminder.expire` 選項，來修改這個設定。

<a name="social-authentication"></a>
## 社群認證

除了傳統的表單認證，Laravel 同樣提供了簡單方便的方法來認證 OAuth 提供者，這個方法使用了 [Laravel Socialite](https://github.com/laravel/socialite)。Socialite 目前支援 Facebook、Twitter、LinkedIn、Google、GitHub 跟 Bitbucket。

開始使用 Socialite 前，新增依賴包至你的 `composer.json`：

    composer require laravel/socialite

### 設定

安裝 Socialite 之後，到 `config/app.php` 設定檔中註冊 `Laravel\Socialite\SocialiteServiceProvider`：

    'providers' => [
        // 其他服務提供者...

        Laravel\Socialite\SocialiteServiceProvider::class,
    ],

同樣的，新增 `Socialite` facade 到 `app` 設定檔的 `aliases` 陣列中：

    'Socialite' => Laravel\Socialite\Facades\Socialite::class,

你將需要新增憑證來使用 OAuth 服務，這些憑證需要被放在 `config/services.php` 設定檔，並根據你應用程式的需求，增加 `facebook`、`twitter`、`linkedin`、`google`、`github` 或 `bitbucket` 的鍵，例如：

    'github' => [
        'client_id' => 'your-github-app-id',
        'client_secret' => 'your-github-app-secret',
        'redirect' => 'http://your-callback-url',
    ],

### 基礎應用

接下來，你已經準備好開始認證使用者了！你將需要兩個路由: 一個用來重導使用者到 OAuth 提供者，另一個在認證後接收提供者的回呼。我們將會藉由 `Socialite` [facade](/docs/{{version}}/facades) 存取 Socialite：

    <?php

    namespace App\Http\Controllers;

    use Socialite;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * 重導使用者到 GitHub 認證頁。
         *
         * @return Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * 從 Github 得到使用者資訊
         *
         * @return Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

`redirect` 方法會負責處理傳送使用者到 OAuth 提供者，而 `user` 方法會從提供者返回的請求來取得使用者資訊。在重導使用者之前，你也可以使用 `scopes` 方法來設定請求的 「作用域」。這個方法將覆寫所有已經存在的作用域：

    return Socialite::driver('github')
                ->scopes(['scope1', 'scope2'])->redirect();

當然，你需要定義路由到你的控制器方法：

    Route::get('auth/github', 'Auth\AuthController@redirectToProvider');
    Route::get('auth/github/callback', 'Auth\AuthController@handleProviderCallback');

一些 OAuth 提供者支援在重導的請求中自訂參數。若要在請求中加入任何自訂參數，只要呼叫 `with` 方法並帶上一個關聯陣列：

    return Socialite::driver('google')
                ->with(['hd' => 'example.com'])->redirect();

#### 取得使用者細節

一旦你有了使用者的實例，你可以獲取使用者更細節的資訊:

    $user = Socialite::driver('github')->user();

    // OAuth Two 提供者
    $token = $user->token;

    // OAuth One 提供者
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // 所有提供者
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

<a name="adding-custom-authentication-drivers"></a>
## 新增客製化的認證驅動

如果你不是使用傳統的關聯式資料庫來儲存使用者，你將需要擴充 Laravel 來新增你自己的認證驅動。我們將使用 `Auth` facade 的 `extend` 方法來定義客製化驅動。你應該將 `extend` 放置在[服務提供者](/docs/{{version}}/providers)中：

    <?php

    namespace App\Providers;

    use Auth;
    use App\Extensions\RiakUserProvider;
    use Illuminate\Support\ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Auth::extend('riak', function($app) {
                // 回傳 Illuminate\Contracts\Auth\UserProvider 的實例...
                return new RiakUserProvider($app['riak.connection']);
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

在你用 `extend` 方法註冊這個驅動後，你可以在 `config/auth.php` 轉換到新的驅動。

### 使用者提供者 Contract

`Illuminate\Contracts\Auth\UserProvider` 的實作只負責取得 `Illuminate\Contracts\Auth\Authenticatable` 的實作， 且不受限於永久儲存系統，例如 MySQL, Riak 等等。這兩個介面允許 Laravel 認證機制繼續作用，而不用管使用者如何儲存或是什麼類型的類別代表它。

讓我們來看看 `Illuminate\Contracts\Auth\UserProvider` contract：

    <?php

    namespace Illuminate\Contracts\Auth;

    interface UserProvider {

        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);

    }

`retrieveById` 函式通常取得一個代表使用者的值，例如 MySQL 中自動增加的 ID。`Authenticate` 的實作會匹配該 ID 能被取得並被這個方法回傳。

`retrieveByToken` 函式藉由使用者獨特的 `$identifier` 和「記住我」`$token` 取得使用者。如同之前的方法，`Authenticatable` 的實作應該被回傳。

`updateRememberToken` 方法使用新的 `$token` 更新了 `$user` 的 `remember_token` 欄位。這個新的標記可以是全新的標記（當使用「記住我」嘗試登入成功時），或是 null（當使用者登出時）。

`retrieveByCredentials` 方法取得了從 `Auth::attempt` 方法傳送過來的憑證陣列（當想要登入時）。這個方法應該要 「查詢」所使用的永久式儲存系統，來匹配這些憑證。通常，這個方法會執行一個帶著「where」`$credentials['username']` 條件的查詢。這個方法接著需要回傳一個 `UserInterface` 的實作。**這個方法不應該企圖做任何密碼的驗證或是認證。**

`validateCredentials` 方法應該要比較 `$user` 和 `$credentials` 來認證這個使用者。例如，這個方法可能會比較 `$user->getAuthPassword()` 字串及 `Hash::make` 後的 `$credentials['password']`。這個方法應該只驗證使用者的憑證並回傳一個布林值。

### 可驗證之 Contract

現在我們已經介紹了 `UserProvider` 的每個方法，讓我們看一下 `Authenticate` contract。記得，這個提供者需要 `retrieveById` 和 `retrieveByCredentials` 方法來回傳這個介面的實作：

    <?php

    namespace Illuminate\Contracts\Auth;

    interface Authenticatable {

        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();

    }

這個介面很簡單。`getAuthIdentifier` 方法需要回傳使用者的「主鍵」。在 MySQL，這個主鍵是指自動增加的主鍵。而 `getAuthPassword` 應該要回傳使用者雜湊後的密碼。這個介面允許認證系統和任何使用者類別運作，不用管你在使用何種 ORM 或是儲存抽象層。預設上，Laravel 的 `app` 資料夾中包含了 `User` 類別，它實作了這個介面，所以你可以觀察這個類別作為實作的範例。

<a name="events"></a>
## 事件

Laravel 提供了在認證過程中的各種[事件](/docs/{{version}}/events)。你可以在 `EventServiceProvider` 為這些事件連接監聽器：

    /**
     * 為你的應用程式註冊任何事件。
     *
     * @param  \Illuminate\Contracts\Events\Dispatcher  $events
     * @return void
     */
    public function boot(DispatcherContract $events)
    {
        parent::boot($events);

        // 在每次嘗試認證時觸發...
        $events->listen('auth.attempt', function ($credentials, $remember, $login) {
            //
        });

        // 登入成功時觸發...
        $events->listen('auth.login', function ($user, $remember) {
            //
        });

        // 登出時觸發...
        $events->listen('auth.logout', function ($user) {
            //
        });
    }
