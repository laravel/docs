# 中介層（Middleware）

- [前言](#introduction)
- [定義中介層](#defining-middleware)
- [註冊中介層](#registering-middleware)
    - [全域中介層](#global-middleware)
    - [指派中介層給路由](#assigning-middleware-to-routes)
    - [中介層群組](#middleware-groups)
    - [中介層排序](#sorting-middleware)
- [中介層參數](#middleware-parameters)
- [可終止的中介層](#terminable-middleware)

<a name="introduction"></a>
## 前言

中介層為進入應用程式提供了方便的機制，檢查和過濾 HTTP 請求。舉例來說，Laravel 包含一個驗證使用者是否已登入的中介層。如果使用者未登入，中介層會將使用者重新導向至應用程式的登入畫面。不過，若使用者已經登入，中介層將會允許請求進一步進入應用程式。

除了身份驗證之外，也能撰寫追加的中介層來進行各種任務（task）。舉例來說，日誌中介層可以記錄應用程式的所有連入請求。Laravel 框架中許多中介層，包含登入認證的中介層和 CSRF 保護的中介層。這些中介層全部都存在 `app/Http/Middleware` 目錄中。

<a name="defining-middleware"></a>
## 定義中介層

要建立一個新的中介層，請使用 Artisan 指令 `make:middleware`：

```shell
php artisan make:middleware EnsureTokenIsValid
```

該指令會在 `app/Http/Middleware` 目錄內放置一個新的 `EnsureTokenIsValid` 類別。在這個中介層中，我們只會允許提供符合指定值的 `token` 才能存取路由。否則會將使用者重新導向 `home` URI：

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureTokenIsValid
    {
        /**
         * 處理一個傳入請求。
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            if ($request->input('token') !== 'my-secret-token') {
                return redirect('home');
            }

            return $next($request);
        }
    }

如你所見，如果一個給定的 `token` 沒有符合我們的secret token，中介層會回傳一個 HTTP 重新導向給client；若符合，該請求就會進一步進入應用程式。要將請求進一步傳到應用程式（讓中介層「通過」），你應該要用 `$request` 呼叫 `$next` 的回呼。

最佳的預想是把中介層當成 HTTP 請求在進入應用程式前必須通過的各種「層級」。每個層級可以檢查請求內容，甚至能完全拒絕請求。

> **Note**  
> 所有的中介層皆透過 [服務容器（service container）](/docs/{{version}}/container) 解析，所以你可以在中介層的建構子（constructor）上給予任何依賴項目做型別提示（type-hint）。

<a name="before-after-middleware"></a>
<a name="middleware-and-responses"></a>
#### 中介層和回應

當然，中介層可以在請求更深入應用程式之前或之後執行任務。舉例來說，以下的中介層會在請求被應用程式處理 **之前** 執行一些任務：

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

不過，這個中介層會在請求被應用程式處理 **之後** 才執行任務：

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

<a name="global-middleware"></a>
### 全域中介層

如果你想要中介層在每個 HTTP 請求都執行的話，請將中介層列在 `app/Http/Kernel.php` 類別的 `$middleware` 屬性內。

<a name="assigning-middleware-to-routes"></a>
### Assigning Middleware To Routes

如果你想要指派中介層到指定的路由，你應該先在 `app/Http/Kernel.php` 檔內給該中介層指派一個索引鍵（key）。預設情況下，這個類別的 `$routeMiddleware` 屬性包含了 Laravel 附帶的中介層。你可以加入自己的中介層到此列表並指派自訂的索引鍵：

    // 在 App\Http\Kernel 類別中...

    protected $routeMiddleware = [
        'auth' => \App\Http\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];

一旦中介層已經在 HTTP 核心定義過，你可以使用 `middleware` 方法指派中介層給路由：

    Route::get('/profile', function () {
        //
    })->middleware('auth');

你可以傳入一組中介層名稱的陣列給 `middleware` 方法來指派多個中介層給路由：

    Route::get('/', function () {
        //
    })->middleware(['first', 'second']);

當指派中介層時，你也可以傳入完整的類別名稱（fully qualified class name）：

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::get('/profile', function () {
        //
    })->middleware(EnsureTokenIsValid::class);

<a name="excluding-middleware"></a>
#### 排除中介層

指派中介層給路由群組時，偶爾會需要阻止中介層套用在路由群組的某個路由。你可以使用 `withoutMiddleware` 方法來達成：

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::middleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/', function () {
            //
        });

        Route::get('/profile', function () {
            //
        })->withoutMiddleware([EnsureTokenIsValid::class]);
    });

也可以從整個 [路由群組](/docs/{{version}}/routing#route-groups) 定義中排除一組指定的中介層：

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/profile', function () {
            //
        });
    });

`withoutMiddleware` 方法只能移除路由中介層而不適用於 [全域中介層](#global-middleware)。

<a name="middleware-groups"></a>
### 中介層群組

有時候你會想把多個中介層分在單一個索引鍵（key）使其可以更輕鬆地指派給路由。可以在 HTTP 核心中使用 `$middlewareGroups` 屬性來達成。

Laravel 有著可即用的 `web` 和 `api` 這些含有你想套用在 web 和 API 路由的常見中介層群組。請記得，這些中介層群組會被應用程式的 `App\Providers\RouteServiceProvider` 服務提供者給自動套用到對應的 `web` 和 `api` 路由檔案：

    /**
     * 應用程式的路由中介層群組。
     *
     * @var array
     */
    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            \App\Http\Middleware\VerifyCsrfToken::class,
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],

        'api' => [
            'throttle:api',
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

中介層群組可以使用與單一中介層相同的語法來指派給路由和控制器動作（controller action）。使用中介層群組比起一次指派多個中介層給路由來說更加方便：

    Route::get('/', function () {
        //
    })->middleware('web');

    Route::middleware(['web'])->group(function () {
        //
    });

> **Note**  
> `web` 和 `api` 這些可即用的中介層群組會由 `App\Providers\RouteServiceProvider` 自動套用對應到 `routes/web.php` 和 `routes/api.php` 檔案。

<a name="sorting-middleware"></a>
### 中介層排序

你偶爾會需要中介層用指定的順序執行，但無法控制他們指派給路由的順序。這時，你可以使用 `app/Http/Kernel.php` 檔案中的 `$middlewarePriority` 屬性來指定中介層的優先權。該屬性預設是不存在 HTTP 核心的。若不存在，你可以複製以下的預設定義：

    /**
     * 中介層的優先權排序列表。
     *
     * 這表示非全域的中介層群組會永遠套用此順序
     *
     * @var string[]
     */
    protected $middlewarePriority = [
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Contracts\Session\Middleware\AuthenticatesSessions::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ];

<a name="middleware-parameters"></a>
## 中介層參數

中介層也能檢索額外的參數。舉例來說，如果應用程式需要辨識認證的使用者在執行特定動作前是否有給定的「權限（role）」，可以建立一個 `EnsureUserHasRole` 中介層並檢索一個權限名稱作為額外的引數。

額外的中介層參數會在 `$next` 引數後傳給中介層：

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureUserHasRole
    {
        /**
         * 處理傳入請求。
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

中介層參數可以在定義路由時在中介層名稱和參數間使用 `:` 來指定。多個參數則使用 `,` 分隔：

    Route::put('/post/{id}', function ($id) {
        //
    })->middleware('role:editor');

<a name="terminable-middleware"></a>
## 可終止的中介層

有時候中介層會需要在 HTTP 回應已經送給瀏覽器後才做些其他工作。如果你在中介層上定義了 `terminate` 方法且 web 伺服器正在使用 FastCGI，`terminate` 方法會在回應被送給瀏覽器後被自動呼叫：

    <?php

    namespace Illuminate\Session\Middleware;

    use Closure;

    class TerminatingMiddleware
    {
        /**
         * 處理傳入請求。
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return $next($request);
        }

        /**
         * 回應已經送給瀏覽器後，處理任務
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Illuminate\Http\Response  $response
         * @return void
         */
        public function terminate($request, $response)
        {
            // ...
        }
    }

`terminate` 方法應該接收請求和回應。一旦已經定義了某個可終止的中介層，你應該將其增加到路由列表或 `app/Http/Kernel.php` 檔內的全域中介層中。

在中介層呼叫 `terminate` 方法時，Laravel 會從 [服務容器](/docs/{{version}}/container) 中解析出一個新的中介層實體。如果你想要讓 `handle` 和 `terminate` 方法在使用同一個的中介層實體上呼叫，使用容器的 `singleton` 方法註冊容器的中介層。通常這應該會在 `AppServiceProvider` 的 `register` 方法達成：

    use App\Http\Middleware\TerminatingMiddleware;

    /**
     * 註冊任何應用程式服務。
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(TerminatingMiddleware::class);
    }
