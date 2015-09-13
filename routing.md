# HTTP 路由

- [基本路由](#basic-routing)
- [路由參數](#route-parameters)
    - [基礎路由參數](#required-parameters)
    - [選擇性路由參數](#parameters-optional-parameters)
    - [正規表達式限制參數](#parameters-regular-expression-constraints)
- [命名路由](#named-routes)
- [路由群組](#route-groups)
    - [中介層](#route-group-middleware)
    - [命名空間](#route-group-namespaces)
    - [子網域路由](#route-group-sub-domain-routing)
    - [路由前綴](#route-group-prefixes)
- [CSRF 保護](#csrf-protection)
    - [介紹](#csrf-introduction)
    - [例外 URIs](#csrf-excluding-uris)
    - [X-CSRF-Token](#csrf-x-csrf-token)
    - [X-XSRF-Token](#csrf-x-xsrf-token)
- [表單方法欺騙](#form-method-spoofing)
- [拋出 404 錯誤](#throwing-404-errors)

<a name="basic-routing"></a>
## 基本路由

你會在 `app/Http/routes.php` 中定義應用程式大多數的路由，該檔案將會被 `App\Providers\RouteServiceProvider` 類別載入。而最基本的 Laravel 路由僅接受 URI 加上一個 `閉包 (Closure)`：

    Route::get('/', function () {
        return 'Hello World';
    });

    Route::post('foo/bar', function () {
        return 'Hello World';
    });

    Route::put('foo/bar', function () {
        //
    });

    Route::delete('foo/bar', function () {
        //
    });

#### 為多重的動作註冊路由

有時候你可能需要註冊一個路由來回應多個 HTTP 的動作。你可以透過 `Route` [facade](/docs/{{version}}/facades) 的 `match` 方法來使用：

    Route::match(['get', 'post'], '/', function () {
        return 'Hello World';
    });

或者，你甚至可以透過 `any` 方法來使用註冊路由並回應所有的 HTTP 動作：

    Route::any('foo', function () {
        return 'Hello World';
    });

#### 產生 URLs 路由

你可以透過 `url` 輔助函式產生應用程式路由：

    $url = url('foo');

<a name="route-parameters"></a>
## 路由參數

<a name="required-parameters"></a>
### 基礎路由參數

有時候你可能需要在你的 URI 路由中，取得一些參數。例如，你可能需要從 URL 取得使用者的 ID。你可以透過定義路由參數來取得：

    Route::get('user/{id}', function ($id) {
        return 'User '.$id;
    });

你可以依照路由需要，定義任何數量的路由參數：

    Route::get('posts/{post}/comments/{comment}', function ($postId, $commentId) {
        //
    });

路由的參數都會被放在「大括號」內。當執行路由時，參數會透過路由 `閉包 (Closure)` 來傳遞。

> **注意：** 路由參數不能包含 `-` 字元。用下劃線 (`_`) 來取代。

<a name="parameters-optional-parameters"></a>
### 選擇性路由參數

有時候你可能需要指定路由參數，但是讓路由參數的存在是可選的。你可以藉由在參數名稱後面加上 `?` 達成：

    Route::get('user/{name?}', function ($name = null) {
        return $name;
    });

    Route::get('user/{name?}', function ($name = 'John') {
        return $name;
    });

<a name="parameters-regular-expression-constraints"></a>
### 正規表達式限制參數

你可以在路由實例上使用 `where` 方法限制你的路由參數格式。`where` 方法接受參數的名稱和定義參數應該如何被限制的正規表達式：

    Route::get('user/{name}', function ($name) {
        //
    })
    ->where('name', '[A-Za-z]+');

    Route::get('user/{id}', function ($id) {
        //
    })
    ->where('id', '[0-9]+');

    Route::get('user/{id}/{name}', function ($id, $name) {
        //
    })
    ->where(['id' => '[0-9]+', 'name' => '[a-z]+']);

<a name="parameters-global-constraints"></a>
#### 全域限制

如果你希望路由參數可以總是遵循正規表達式，你可以使用 `pattern` 方法。你應該在 `RouteServiceProvider` 的 `boot` 方法裡定義這些模式：

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @param  \Illuminate\Routing\Router  $router
     * @return void
     */
    public function boot(Router $router)
    {
        $router->pattern('id', '[0-9]+');

        parent::boot($router);
    }

一旦定義了模式，會自動的應用到所有使用該參數名稱的路由：

    Route::get('user/{id}', function ($id) {
        // Only called if {id} is numeric.
    });

<a name="named-routes"></a>
## 命名路由

命名路由讓你更方便為特定路由產生 URL 或進行重導。你可以使用 `as`  陣列鍵指定名稱到你的路由：

    Route::get('user/profile', ['as' => 'profile', function () {
        //
    }]);

你還可以指定路由名稱到你的控制器操作：

    Route::get('user/profile', [
        'as' => 'profile', 'uses' => 'UserController@showProfile'
    ]);

#### 路由群組和命名路由

假設你使用 [路由群組](#route-groups)，你可以指定一個 `as` 關鍵字在你的路由群組的屬性陣列，也允許你設定所有路由群組中共同的路由名稱前綴：

    Route::group(['as' => 'admin::'], function () {
        Route::get('dashboard', ['as' => 'dashboard', function () {
            // Route named "admin::dashboard"
        }]);
    });

#### 對命名路由產生 URLs

一旦你在給定的路由中分配了名稱，你可以透過 `route` 函式，使用路由名稱產生 URLs 或是重新導向：

    $url = route('profile');

    $redirect = redirect()->route('profile');

如果在路由定義參數，你可以把參數作為第二個參數傳遞給 `route` 方法。給定的參數將自動加入到 URL：

    Route::get('user/{id}/profile', ['as' => 'profile', function ($id) {
        //
    }]);

    $url = route('profile', ['id' => 1]);

<a name="route-groups"></a>
## 路由群組

路由群組允許你共用路由屬性，例如：中介層、命名空間，你可以利用路由群組套用這些屬性到多個路由，而不需在每個路由都設定一次。共用屬性被指定為陣列格式，當作 `Route::group` 方法的第一個參數：

為了了解更多路由群組相關內容，我們會看過去幾個常見的使用範例和功能。

<a name="route-group-middleware"></a>
### 中介層

要指定中介層到所有群組內的路由，你可以在群組屬性陣列裡使用 `middleware` 參數。中介層將會依照你在列表內指定的順序執行：

    Route::group(['middleware' => 'auth'], function () {
        Route::get('/', function ()    {
            // Uses Auth Middleware
        });

        Route::get('user/profile', function () {
            // Uses Auth Middleware
        });
    });

<a name="route-group-namespaces"></a>
### 命名空間

另一個常見的範例是，指派相同的 PHP 命名空間中給控制器群組。你可以使用 `namespace` 參數指定群組內所有控制器的命名空間：


    Route::group(['namespace' => 'Admin'], function()
    {
        // Controllers Within The "App\Http\Controllers\Admin" Namespace

        Route::group(['namespace' => 'User'], function()
        {
            // Controllers Within The "App\Http\Controllers\Admin\User" Namespace
        });
    });

記得，預設 `RouteServiceProvider` 會在命名空間群組內導入你的 `routes.php` 檔案，讓你不用指定完整的 `App\Http\Controllers` 命名空間前綴就能註冊控制器路由。所以，我們只需要指定在基底 `App\Http\Controllers` 根命名空間之後的命名空間部分。

<a name="route-group-sub-domain-routing"></a>
### 子網域路由

路由群組也可以用來處理萬用字元的子網域。子網域可以像路由 URIs 分配路由參數，讓你在你的路由或控制器取得子網域參數。可以使用路由群組屬性陣列上的 `domain` 指定子網域變數名稱：

    Route::group(['domain' => '{account}.myapp.com'], function () {
        Route::get('user/{id}', function ($account, $id) {
            //
        });
    });

<a name="route-group-prefixes"></a>
### 路由前綴

透過路由群組陣列屬性中的 `prefix`，在路由群組內為每個路由給定的 URI 加上前綴。例如，你可能想要在路由群組中將所有的路由 URIs 加上前綴 `admin`：

    Route::group(['prefix' => 'admin'], function () {
        Route::get('users', function ()    {
            // Matches The "/admin/users" URL
        });
    });

你也可以使用 `prefix` 參數去指定你的路由群組中共用的參數：

    Route::group(['prefix' => 'accounts/{account_id}'], function () {
        Route::get('detail', function ($account_id)    {
            // Matches The accounts/{account_id}/detail URL
        });
    });

<a name="csrf-protection"></a>
## CSRF 保護

<a name="csrf-introduction"></a>
### 介紹

Laravel 提供簡單的方法保護你的應用程式不受到 [跨網站請求偽造](http://en.wikipedia.org/wiki/Cross-site_request_forgery) 攻擊。跨網站請求偽造是一種惡意的攻擊，藉以透過經過身份驗證的使用者身份執行未經授權的命令。

Laravel 會自動產生了一個 CSRF token 給每個活動使用者受應用程式管理的 Session。該 token 用來驗證使用者為實際發出請求至應用程式的使用者。要產生一個隱藏的輸入欄位 `_token` 包含 CSRF token，你可以使用 `csrf_field` 輔助函式：

    <?php echo csrf_field(); ?>

`csrf_field` 輔助函式產生以下的 HTML：

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

當然，也可以在 Blade [模板引擎](/docs/{{version}}/blade) 中使用：

    {!! csrf_field() !!}

你不需要手動驗證 POST、PUT 或 DELETE 請求的 CSRF token。在 `VerifyCsrfToken` [HTTP 中介層](/docs/{{version}}/middleware) 將自動驗證請求與 session 中的 token 是否相符。

<a name="csrf-excluding-uris"></a>
### 不受 CSRF 保護的 URIs

有時候你可能會希望一組 URIs 不要被 CSRF 保護。例如，你如果使用 [Stripe](https://stripe.com) 處理付款，並且利用他們的 webhook 系統，你需要從 Laravel CSRF 保護中，排除 webhook 的處理路由。

你可以在 `VerifyCsrfToken` 中介層中增加 `$execpt` 屬性來排除 URIs：

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as BaseVerifier;

    class VerifyCsrfToken extends BaseVerifier
    {
        /**
         * The URIs that should be excluded from CSRF verification.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
        ];
    }

<a name="csrf-x-csrf-token"></a>
### X-CSRF-TOKEN

除了檢查 CSRF token 當作 POST 參數之外，在 Laravel `VerifyCsrfToken` 中介層也會確認請求標頭中的 `X-CSRF-TOKEN`。例如，你可以將其儲存在 meta 標籤中：

    <meta name="csrf-token" content="{{ csrf_token() }}">

一旦你建立了 `meta` 標籤，你可以使用 jQuery 之類的函式庫將 token 加入到所有的請求標頭。基於 AJAX 的應用，提供了簡單、方便的 CSRF 保護：

    $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
    });

<a name="csrf-x-xsrf-token"></a>
### X-XSRF-TOKEN

Laravel 也會在 `XSRF-TOKEN` cookie 中儲存 CSRF token。你也可以使用 cookie 的值來設定 `X-XSRF-TOKEN` 請求標頭。一些 JavaScript 框架會自動幫你處理，例如：Angular。你不太可能會需要手動去設定這個值。

<a name="form-method-spoofing"></a>
## 表單方法欺騙

HTML 表單沒有支援 `PUT`、`PATCH` 或 `DELETE` 動作。所以在定義 `PUT`、`PATCH` 或 `DELETE` 路由，並在 HTML 表單中被呼叫的時候，你將需要在表單中增加隱藏的 `_method` 欄位。隨著 `_method` 欄位送出的值將被視為 HTTP 請求方法使用：

    <form action="/foo/bar" method="POST">
        <input type="hidden" name="_method" value="PUT">
        <input type="hidden" name="_token" value="{{ csrf_token() }}">
    </form>

<a name="throwing-404-errors"></a>
## 拋出 404 錯誤

這裡有兩種方法從路由手動觸發 404 錯誤。首先，你可以使用 `abort` 輔助函式。`abort` 輔助函式只是簡單的拋出一個帶有指定狀態代碼的 `Symfony\Component\HttpFoundation\Exception\HttpException`：

    abort(404);

第二，你可以手動拋出 `Symfony\Component\HttpKernel\Exception\NotFoundHttpException` 的實例。

更多有關如何操作 404 例外和自訂的回應，可以到 [錯誤](/docs/{{version}}/errors#http-exceptions) 章節內參考文件。
