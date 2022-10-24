# 路由

- [基礎路由](#basic-routing)
    - [重新導向的路由](#redirect-routes)
    - [視圖路由](#view-routes)
    - [路由列表](#the-route-list)
- [路由參數](#route-parameters)
    - [必填參數](#required-parameters)
    - [選填參數](#parameters-optional-parameters)
    - [正規表達式限制](#parameters-regular-expression-constraints)
- [命名路由](#named-routes)
- [路由群組](#route-groups)
    - [中介層](#route-group-middleware)
    - [控制器](#route-group-controllers)
    - [子網域路由](#route-group-subdomain-routing)
    - [路由前置詞](#route-group-prefixes)
    - [路由名稱的前置詞](#route-group-name-prefixes)
- [路由模型綁定](#route-model-binding)
    - [隱式綁定](#implicit-binding)
    - [隱式列舉（enum）綁定](#implicit-enum-binding)
    - [顯式綁定](#explicit-binding)
- [遞補路由](#fallback-routes)
- [頻率限制](#rate-limiting)
    - [定義頻率限制器](#defining-rate-limiters)
    - [在路由上附加頻率限制器](#attaching-rate-limiters-to-routes)
- [表單方法（form method）偽造](#form-method-spoofing)
- [存取當下路由](#accessing-the-current-route)
- [跨來源資源共用（CORS）](#cors)
- [路由快取](#route-caching)

<a name="basic-routing"></a>
## 基礎路由

最基本的 Laravel 路由是接收一個 URI 和一個閉包（closure）提供一個非常簡單直觀的方法來定義路由和行為，而不用複雜的路由設定檔：

    use Illuminate\Support\Facades\Route;

    Route::get('/greeting', function () {
        return 'Hello World';
    });

<a name="the-default-route-files"></a>
#### 可用的路由器方法（router method）

所有的 Laravel 路由皆在路由檔案中定義，這些檔案在 `routes` 目錄中且由應用程式的 `App\Providers\RouteServiceProvider` 自動載入。`route/web.php` 檔會定義 web 介面的路由。這些路由被指派到 `web` 中介層群組內，且提供例如 session 狀態和 CSRF 保護等功能。`routes/api.php` 裡的路由是無狀態（stateless）且被指派給 `api` 中介層群組。

對大部分應用程式，你會在 `route/web.php` 檔內開始定義路由。這些定義在 `routes/web.php` 檔內的路由可以經由打開瀏覽器中定義的 URL 來存取。舉個例子，你可以在瀏覽器打開 `http://example.com/user` 來存取以下路由：

    use App\Http\Controllers\UserController;

    Route::get('/user', [UserController::class, 'index']);

`routes/api.php` 檔內定義的路由則嵌在 `RouteServiceProvider` 的路由群組中。在這個群組中， `/api` 會自動成為 URI 前置詞，所以你就不需要每次手動在路由加入 `/api`。你可以透過修改`RouteServiceProvider` 類別來更動前置詞和其他路由群組的選項。

<a name="available-router-methods"></a>
#### 可用的路由器方法（router method）

路由器允許你透過註冊路由來回應任何 HTTP 動詞：

    Route::get($uri, $callback);
    Route::post($uri, $callback);
    Route::put($uri, $callback);
    Route::patch($uri, $callback);
    Route::delete($uri, $callback);
    Route::options($uri, $callback);

有時候你會需要註冊一個路由來回應多個 HTTP 動詞。你可以使用 `match` 方法。甚至是使用 `any` 方法註冊一個路由來回應全部的 HTTP 動詞：

    Route::match(['get', 'post'], '/', function () {
        //
    });

    Route::any('/', function () {
        //
    });

> **Note**  
> 當定義多個路由共享 URI 時，使用 `get`, `post`, `put`, `patch`, `delete`, 和 `options` 方法的路由之前必須先定義 `any`, `match`, 和 `redirect` 方法的路由。這可以確保傳入的請求會被配對到正確的路由。

<a name="dependency-injection"></a>
#### 依賴注入（Dependency Injection）

你可以在路由的回呼簽章（callback signature）中對任何路由所需的依賴項目做型態提示（type-hint）。這些公佈的依賴項目會自動解析並被Laravel [服務容器](/docs/{{version}}/container) 注入到回呼。舉個例子，你可以對 `Illuminate\Http\Request` 類別做型態提示，使當前的 HTTP 請求自動注入至路由回呼：

    use Illuminate\Http\Request;

    Route::get('/users', function (Request $request) {
        // ...
    });

<a name="csrf-protection"></a>
#### CSRF 保護

請記得，任何在 `web` 路由檔內定義的 `POST`, `PUT`, `PATCH`, 或 `DELETE` 路由指向的 HTML 表單都必須包含一個 CSRF 標記（token），否則這個請求將會被拒絕。你可以在 [CSRF 文件](/docs/{{version}}/csrf) 參閱更多關於 CSRF 保護的資訊：

    <form method="POST" action="/profile">
        @csrf
        ...
    </form>

<a name="redirect-routes"></a>
### 重新導向的路由

如果你正在定義一個重新導向其他 URI 的路由，你可以使用 `Route::redirect` 方法。這個方法提供一個方便的捷徑讓你可以不用為了簡單的重新導向去定義完整的路由或控制器：

    Route::redirect('/here', '/there');

預設情況下，`Route::redirect` 會回傳一個 `302` 狀態碼。你可以選填第三個參數來自訂狀態碼：

    Route::redirect('/here', '/there', 301);

或者，你也可以用 `Route::permanentRedirect` 方法回傳一個 `301` 狀態碼：

    Route::permanentRedirect('/here', '/there');

> **Warning**  
> 在重新導向的路由使用路由參數時，以下參數會被 Laravel 保留且無法使用：`destination` and `status`。

<a name="view-routes"></a>
### 視圖路由

如果你的路由只需要回傳一個 [視圖](/docs/{{version}}/views)，你可以用 `Route::view` 方法。就像 `redirect` 方法，它提供簡單的捷徑讓你不需要定義一個完整個路由或控制器。`view` 方法接收一個 URI 作為第一個引數，而視圖名稱作為第二個引數。此外你還可以提供一個資料陣列給視圖，並作為第三個選填的引數：

    Route::view('/welcome', 'welcome');

    Route::view('/welcome', 'welcome', ['name' => 'Taylor']);

> **Warning**  
> 在視圖路由使用路由參數時，以下參數會被 Laravel 保留且無法使用：`view`, `data`, `status`, and `headers`。

<a name="the-route-list"></a>
### 路由列表

Artisan 指令 `route:list` 可以輕鬆地檢視所有應用程式內已定義的路由一覽：

```shell
php artisan route:list
```

預設情況下，指派給各個路由的中介層在 `route:list` 不會顯示；但你可以在指令中加上 `-v` 選項指示 Laravel 顯示中介層：

```shell
php artisan route:list -v
```

你也可以指示 Laravel 只顯示有給定 URI 的路由：

```shell
php artisan route:list --path=api
```

此外，你還可以在執行 `route:list` 指令時加上 `--except-vendor` 選項來指示 Laravel 隱藏由第三方套件定義的路由：

```shell
php artisan route:list --except-vendor
```

同樣地，也可以在執行 `route:list` 指令時加上 `--only-vendor` 選項指示 Laravel 只秀出由第三方套件定義的路由：

```shell
php artisan route:list --only-vendor
```

<a name="route-parameters"></a>
## 路由參數

<a name="required-parameters"></a>
### 必填參數

有時候你會需要抓取路由 URI 的部分字串。舉個例子，你可以透過定義路由參數從 URL 抓取使用者的 ID。

    Route::get('/user/{id}', function ($id) {
        return 'User '.$id;
    });

你可以根據自己路由所需，定義許多路由參數：

    Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
        //
    });

路由參數永遠是由 `{}` 包裝且由字母組成。底線（`_`）也是可接受的路由參數名稱。路由參數根據指令注入至路由回呼／控制器──路由的回呼／控制器中的名稱不會影響。

<a name="parameters-and-dependency-injection"></a>
#### 參數和依賴注入

如果路由有讓 Laravel 服務容器去自動注入至路由的回呼的依賴項，你必須在依賴項之後列出路由參數：

    use Illuminate\Http\Request;

    Route::get('/user/{id}', function (Request $request, $id) {
        return 'User '.$id;
    });

<a name="parameters-optional-parameters"></a>
### 選填參數

有時候你會需要指定一個不想要顯示在 URI 的路由參數。你可以在參數名稱之後放置一個 `?` 符號。請先確定這個路由對應的變數有預設值：

    Route::get('/user/{name?}', function ($name = null) {
        return $name;
    });

    Route::get('/user/{name?}', function ($name = 'John') {
        return $name;
    });

<a name="parameters-regular-expression-constraints"></a>
### 正規表達式限制

你會在路由實作上使用 `where` 方法限制路由參數的格式。`where` 方法接受一個參數名稱和一個正規表達式來定義參數如何被限制：

    Route::get('/user/{name}', function ($name) {
        //
    })->where('name', '[A-Za-z]+');

    Route::get('/user/{id}', function ($id) {
        //
    })->where('id', '[0-9]+');

    Route::get('/user/{id}/{name}', function ($id, $name) {
        //
    })->where(['id' => '[0-9]+', 'name' => '[a-z]+']);

為了方便起見，一些常用的正規表達式都有輔助方法讓你可以快速地將格式套用在路由上：

    Route::get('/user/{id}/{name}', function ($id, $name) {
        //
    })->whereNumber('id')->whereAlpha('name');

    Route::get('/user/{name}', function ($name) {
        //
    })->whereAlphaNumeric('name');

    Route::get('/user/{id}', function ($id) {
        //
    })->whereUuid('id');

    Route::get('/category/{category}', function ($category) {
        //
    })->whereIn('category', ['movie', 'song', 'painting']);

如果連入請求不符合路由的格式限制，則會回傳一個 404 HTTP 回應。

<a name="parameters-global-constraints"></a>
#### 全域條件限制

如果你想要用某個正規表達式永遠限制一個路由參數，你可以使永 `pattern` 方法。你必須定義這些在 `App\Providers\RouteServiceProvider` 類別中 `boot` 方法內的格式：

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @return void
     */
    public function boot()
    {
        Route::pattern('id', '[0-9]+');
    }

一旦格式被定義過，它會自動套用所有路由使用該參數名稱：

    Route::get('/user/{id}', function ($id) {
        // 只會在 {id} 為數字時執行……
    });

<a name="parameters-encoded-forward-slashes"></a>
#### 編碼斜線

Laravel 的路由元件允許除了 `/` 的所有字元出現在路由參數值內。你可以使用 `where` 正規表達式狀態明確允許 `/` 為預留位置的一部份：

    Route::get('/search/{search}', function ($search) {
        return $search;
    })->where('search', '.*');

> **Warning**  
> 編碼斜線只支援最後一個路由字段。

<a name="named-routes"></a>
## 命名路由

命名路由可以讓特定路由方便地產生 URL 或重新導向。你可以透過鏈式連接 `name` 方法到路由定義，以此給路由指定一個名稱：

    Route::get('/user/profile', function () {
        //
    })->name('profile');

你也可以給控制器動作指定路由名稱：

    Route::get(
        '/user/profile',
        [UserProfileController::class, 'show']
    )->name('profile');

> **Warning**  
> 路由名稱永遠是唯一性的，不可重複。

<a name="generating-urls-to-named-routes"></a>
#### 產生 URL 給命名路由

一旦給某個路由指定名稱，你可以透過 Laravel 的 `route` 和 `redirect` 輔助函式來產生 URL 或重新導向，來使用該路由名稱：

    // 產生 URLs…
    $url = route('profile');

    // 產生重新導向……
    return redirect()->route('profile');

    return to_route('profile');

如果命名路由有定義參數，參數會作為第二個引數傳給 `route` 函式。傳入的參數會自動插入到產生的 URL 的正確位置中：

    Route::get('/user/{id}/profile', function ($id) {
        //
    })->name('profile');

    $url = route('profile', ['id' => 1]);

如果你在陣列中傳入額外的參數，這些索引鍵／值（key/value）配對會自動插入到產生的 URL 的查詢字串（query string）：

    Route::get('/user/{id}/profile', function ($id) {
        //
    })->name('profile');

    $url = route('profile', ['id' => 1, 'photos' => 'yes']);

    // /user/1/profile?photos=yes

> **Note**  
> 有時候，你會想要給 URL 參數指定要求層級（request-wide）的預設值，像是當下的語言環境。你可以用 [`URL::defaults` 方法](/docs/{{version}}/urls#default-values) 做到。

<a name="inspecting-the-current-route"></a>
#### 檢查當下路由

如果你想要判斷當下的請求是否有被路由到給定的命名路由，可以在路由實作上使用 `named` 方法。舉個例子，你可以從路由中介層檢查當下的路由名稱：

    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if ($request->route()->named('profile')) {
            //
        }

        return $next($request);
    }

<a name="route-groups"></a>
## 路由群組

路由群組允許你共享路由的屬性，例如中介層，大數量的路由不需要再個別定義其路由的屬性。

巢狀群組會嘗試智慧「合併」屬性到他們的父層。在附加路由名稱和前置詞的同時，中介層和 `where` 條件也會被合併。URI 前置的命名空間（namespace）分隔符號和斜線會適時地自動加入。

<a name="route-group-middleware"></a>
### 中介層

欲分配 [中介層](/docs/{{version}}/middleware) 給群組內所有的路由，可以在定義群組前使用 `middleware` 方法。中介層會以陣列中列出的順序執行：

    Route::middleware(['first', 'second'])->group(function () {
        Route::get('/', function () {
            // 使用 first 和 second 中介層...
        });

        Route::get('/user/profile', function () {
            // 使用 first 和 second 中介層...
        });
    });

<a name="route-group-controllers"></a>
### 控制器

如果有個群組的路由全部都使用相同的 [控制器](/docs/{{version}}/controllers)，可以使用 `controller` 方法給群組內所有的路由定義通用控制器。之後定義路由時，你只需要提供要調用的控制器方法：

    use App\Http\Controllers\OrderController;

    Route::controller(OrderController::class)->group(function () {
        Route::get('/orders/{id}', 'show');
        Route::post('/orders', 'store');
    });

<a name="route-group-subdomain-routing"></a>
### 子網域路由

路由群組也可以用來處理子網域路由。子網域可以像路由 URI 一樣被分配路由參數，並允許抓取子網域的部分字段用在路由或控制器。子網域可以在定義群組前用 `domain` 方法指定：

    Route::domain('{account}.example.com')->group(function () {
        Route::get('user/{id}', function ($account, $id) {
            //
        });
    });

> **Warning**  
> 為了確保子網域路由是有效的，你必須在註冊根網域路由之前先註冊子網域路由。這可以防止根網域路由去覆蓋到相同 URI 路徑的子網域路由。

<a name="route-group-prefixes"></a>
### 路由前置詞

`prefix` 方法可以為群組內的每個路由加上指頂的 URI 前置詞。舉例來說，若想要把群組內的所有路由 URI 都加上 `admin` 前置詞：

    Route::prefix('admin')->group(function () {
        Route::get('/users', function () {
            // 配對到「/admin/users」URL
        });
    });

<a name="route-group-name-prefixes"></a>
### 命名路由的前置詞

`name` 方法可以給群組內的每個路由名稱加上給定字串的前置詞。舉例來說，你會想要給群組的路由名稱都加上 `admin` 前置詞。給定的字串會確切地被指定為路由名稱的前置詞，所以我們要確保有在前置詞後方加上 `.` 字元：

    Route::name('admin.')->group(function () {
        Route::get('/users', function () {
            // 路由被指派名稱為「admin.users」...
        })->name('users');
    });

<a name="route-model-binding"></a>
## 路由模型（model）綁定

當注入一個模型 ID 到路由或是控制器動作時，你通常會查詢資料庫來取得與該 ID 對應的模型。Laravel 的路由模型綁定提供了自動注入模型實體到路由的方便方法。舉個例子，你可以注入對應給定 ID 的整個 `User` 模型實體，而不是注入使用者的 ID。

<a name="implicit-binding"></a>
### 隱式綁定

Laravel 會自動解析定義在路由或控制器動作內的 Eloquent 模型，其型別提示（type-hint）的變數名稱對應到路由的部分名稱。舉例來說：

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        return $user->email;
    });

由於 `$user` 變數作為 `App/Models/User` Eloquent 模型的型別提示且變數名稱與 `{user}` URI 片段對應，Laravel 會自動注入符合 ID 請求內的 URI 對應值的模型實體。如果符合的模型實體不在資料庫內，將會自動產生一個 404 HTTP 回應。

當然，使用控制器方法時也能使用隱式綁定。注意 `{user}` URI 字段對應控制器內有 `App\Models\User` 型別提示的 `$user` 變數：

    use App\Http\Controllers\UserController;
    use App\Models\User;

    // Route 定義...
    Route::get('/users/{user}', [UserController::class, 'show']);

    // Controller 方法定義...
    public function show(User $user)
    {
        return view('user.profile', ['user' => $user]);
    }

<a name="implicit-soft-deleted-models"></a>
#### 軟刪除（soft delete）模型

一般而言，隱式模型綁定不會檢索已經被 [軟刪除](/docs/{{version}}/eloquent#soft-deleting) 的模型。但你可以在路由定義時串上 `withTrashed` 方法指示隱式綁定去檢索這些模型：

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        return $user->email;
    })->withTrashed();

<a name="customizing-the-key"></a>
<a name="customizing-the-default-key-name"></a>
#### 自訂索引鍵（key）

有時候你會希望使用 `id` 以外的欄位解析 Eloquent 模型。為此，你可以指定路由參數定義中的欄位：

    use App\Models\Post;

    Route::get('/posts/{post:slug}', function (Post $post) {
        return $post;
    });

如果你想要在檢索給定的模型類別時永遠使用 `id` 以外的資料庫欄位進行模型綁定，可以在 Eloquent 模型上複寫 `getRouteKeyName` 方法：

    /**
     * Get the route key for the model.
     *
     * @return string
     */
    public function getRouteKeyName()
    {
        return 'slug';
    }

<a name="implicit-model-binding-scoping"></a>
#### 自訂索引鍵和範圍界定

在一個路由定義中隱式綁定多個 Eloquent 模型時，你可以限定第二個 Eloquent 模型必須是前一個 Eloquent 模型的子模型。舉例來說，假設該路由定義是檢索一個指定使用者的客製化網址部落格（blog post by slug）貼文：

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    });

當使用自訂鍵的隱式綁定作為巢狀路由參數時，Laravel 會推測其父層級模型的關聯名稱來自動限制查詢範圍並用以檢索其巢狀模型。在此例中，假設 `User` 模型有一個關聯名稱 `posts`（路由參數名稱的複數形式），其關聯可用來檢索 `Post` 模型。

若希望，你可以指示 Laravel 即使沒有提供自訂鍵，也要限制「子層級」綁定。為此，可以在定義路由時調用 `scopeBindings` 方法：

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    })->scopeBindings();

或者，可以指示整個路由定義群組使用範圍綁定：

    Route::scopeBindings()->group(function () {
        Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
            return $post;
        });
    });

同樣地，你可以調用 `withoutScopedBindings` 方法來明確指示 Laravel 不要範圍綁定：

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    })->withoutScopedBindings();

<a name="customizing-missing-model-behavior"></a>
#### 自訂找不到模型時的行為

通常，如果沒找到隱式綁定的模型時會產生一個 404 HTTP 回應。不過你可以在定義路由時自訂呼叫 `missing` 方法的行為。`missing` 方法是接受一個閉包（closure）並可以在找不到隱式綁定模型時做調用：

    use App\Http\Controllers\LocationsController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
            ->name('locations.view')
            ->missing(function (Request $request) {
                return Redirect::route('locations.index');
            });

<a name="implicit-enum-binding"></a>
### 隱式列舉（Enum）綁定

PHP 8.1 介紹了對 [列舉](https://www.php.net/manual/en/language.enumerations.backed.php) 的支援。為了配合此功能，Laravel 允許在路由定義對 [回退列舉（backed Enum）](https://www.php.net/manual/en/language.enumerations.backed.php) 使用型別提示，Laravel 只會調用與路由字段對應且有效的列舉值的路由。否則會自動回傳一個 404 回應。舉例來說，若給定以下列舉：

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

你可以定義一個只有 `{category}` 路由字段有 `fruits` 或 `people` 才能調用的路由。否則，Laravel 將會回傳一個 404 回應：

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 顯式綁定

不一定要使用 Laravel 隱式的慣例模型來解析模型綁定。你也可以顯式定義路由參數要如何對應到模型。若要註冊一個顯式綁定，使用路由的 `model` 方法去給定好的參數指定類別。你必須在 `RouteServiceProvider` 類別的 `boot` 方法開頭就定義顯式模型綁定：

    use App\Models\User;
    use Illuminate\Support\Facades\Route;

    /**
     * 定義路由模型綁定、模式篩選器等
     *
     * @return void
     */
    public function boot()
    {
        Route::model('user', User::class);

        // ...
    }

接下來，定義一個包含 `{user}` 參數的路由：

    use App\Models\User;

    Route::get('/users/{user}', function (User $user) {
        //
    });

當我們已經綁定所有 `{user}` 參數到 `App\Model\User` 模型，該類別（user）的實體將會被注入到路由中。舉例來說，`users/1` 的請求將會 被注入到資料庫中 ID 為 `1` 的 `User` 實體。

如果資料庫中找不到符合的模型實體，會自動產生一個 404 HTTP 回應。

<a name="customizing-the-resolution-logic"></a>
#### 自訂解析邏輯

如果你希望定義自己的模型綁定解析邏輯，可以使用 `Route::bind` 方法。傳送一個閉包給 `bind` 方法將會取得 URI 字段的值，並回傳要注入到路由的類別實體。這個自訂邏輯必須放在 `RouteServiceProvider` 的 `boot` 方法內：

    use App\Models\User;
    use Illuminate\Support\Facades\Route;

    /**
     * 定義路由模型綁定、模式篩選器等
     *
     * @return void
     */
    public function boot()
    {
        Route::bind('user', function ($value) {
            return User::where('name', $value)->firstOrFail();
        });

        // ...
    }

或者，可以複寫 Eloquent 模型上的 `resolveRouteBinding` 方法。該方法會取得 URI 字段的值，並回傳要注入到路由的類別實體：

    /**
     * 檢索模型獲得綁定的值
     *
     * @param  mixed  $value
     * @param  string|null  $field
     * @return \Illuminate\Database\Eloquent\Model|null
     */
    public function resolveRouteBinding($value, $field = null)
    {
        return $this->where('name', $value)->firstOrFail();
    }

如果路由是使用 [限定範圍的隱式綁定](#implicit-model-binding-scoping)，則 `resolveChildRouteBinding` 方法會被用於解析父層模型的子層級綁定：

    /**
     * 檢索子層級模型的綁定值
     *
     * @param  string  $childType
     * @param  mixed  $value
     * @param  string|null  $field
     * @return \Illuminate\Database\Eloquent\Model|null
     */
    public function resolveChildRouteBinding($childType, $value, $field)
    {
        return parent::resolveChildRouteBinding($childType, $value, $field);
    }

<a name="fallback-routes"></a>
## 遞補路由

使用 `Route::fallback` 方法，可以定義當沒有符合連入請求的路由時要執行的路由。一般而言，未處理的請求會透過應用程式的例外處理器（exception handler）自動渲染一個「404」頁面。不過通常會在 `routes/web.php` 檔內定義 `fallback` 路由，所有在 `web` 中介層群組內的中介層都會套用 `fallback` 路由。若需要，你可以自由增加額外的中介層到此路由中：

    Route::fallback(function () {
        //
    });

> **Warning**  
> 遞補路由必須永遠是應用程式中最後一個註冊的路由。

<a name="rate-limiting"></a>
## 頻率限制

<a name="defining-rate-limiters"></a>
### 定義頻率限制器

Laravel 包含了強大和可自訂的頻率限制服務，可以用來給指定路由或路由群組限制流量。若要開始，必須依照應用程式需求去定義頻率限制器的設定。一般而言，這應該要在應用程式裡 `App\Providers\RouteServiceProvider` 類別的 `configureRateLimiting` 方法完成。

頻率限制器是用 `RateLimiter` facade 的 `for` 方法定義。`for` 方法接受一個頻率限制器名稱和一個閉包，並回傳套用到路由所指派的頻率限制器的組態設定。頻率組態設定是 `Illuminate\Cache\RateLimiting\Limit` 類別的實體。該類別包含實用的「建構器（builder）」方法讓你可以快速定義限制。頻率限制器的名稱可以是任何你希望的字串：

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\RateLimiter;

    /**
     * 為應用程式設定頻率限制器
     *
     * @return void
     */
    protected function configureRateLimiting()
    {
        RateLimiter::for('global', function (Request $request) {
            return Limit::perMinute(1000);
        });
    }

如果連入的請求超過指定的頻率限制，Laravel 會自動回傳一個 429 HTTP 狀態碼的回應。若你想要自訂頻率限制回傳的回應，可以使用 `response` 方法：

    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
            return response('自訂回應...', 429, $headers);
        });
    });

由於頻率限制器的回呼會檢索連入的 HTTP 請求實體，你可以基於連入請求或已認證使用者動態建立合適的頻率限制：

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100);
    });

<a name="segmenting-rate-limits"></a>
#### 分段頻率限制

有時候你會希望用某些值來分割頻率限制。舉例來說，你會希望允許使用者在每個 IP 位址每分鐘存取給定的路由 100 次。為此，可以在建立頻率限制時使用 `by` 方法：

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100)->by($request->ip());
    });

用其他例子說明此功能，我們可以限制每個認證使用者每分鐘 100 次存取路由，或限制每個 IP 位址的訪客每分鐘 10 次：

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()
                    ? Limit::perMinute(100)->by($request->user()->id)
                    : Limit::perMinute(10)->by($request->ip());
    });

<a name="multiple-rate-limits"></a>
#### 多個頻率限制

若需要，可以為給定的頻率限制器組態設定回傳一組頻率限制的陣列。每個頻率限制會依照陣列中的順序套用至路由：

    RateLimiter::for('login', function (Request $request) {
        return [
            Limit::perMinute(500),
            Limit::perMinute(3)->by($request->input('email')),
        ];
    });

<a name="attaching-rate-limiters-to-routes"></a>
### 在路由上附加頻率限制器

頻率限制器可以使用 `throttle` [中介層](/docs/{{version}}/middleware) 附加到路由或路由群組。throttle 中介層接受你希望指派給路由的限制器名稱：

    Route::middleware(['throttle:uploads'])->group(function () {
        Route::post('/audio', function () {
            //
        });

        Route::post('/video', function () {
            //
        });
    });

<a name="throttling-with-redis"></a>
#### 使用 Redis 做頻率限制

一般而言，`throttle` 中介層被映射到 `Illuminate\Routing\Middleware\ThrottleRequests` 類別。此映射定義在應用程式的 HTTP 核心（`App\Http\Kernel`）。不過，如果你使用 Redis 作為應用程式的快取驅動程式，你會希望將映射改為使用 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 類別。該類別能更有效率地使用 Redis 管理頻率限制：

    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,

<a name="form-method-spoofing"></a>
## 表單方法偽造

HTML 表單不支援 `PUT`、`PATCH`、或 `DELETE` 動作。所以，當定義從 HTML 表單呼叫的 `PUT`、`PATCH`、或 `DELETE` 路由時，你會需要新增一個隱藏的 `_method` 欄位進表單。包含 `_method` 欄位的值會被作為 HTTP 請求方法：

    <form action="/example" method="POST">
        <input type="hidden" name="_method" value="PUT">
        <input type="hidden" name="_token" value="{{ csrf_token() }}">
    </form>

為了方便，可以使用 `@method` [Blade 指示](/docs/{{version}}/blade) 來產生 `_method` 的輸入欄位：

    <form action="/example" method="POST">
        @method('PUT')
        @csrf
    </form>

<a name="accessing-the-current-route"></a>
## 存取當下路由

你可以使用 `Route` facade 上的 `current`、`currentRouteName`、和 `currentRouteAction` 方法存取關於處理傳入請求的資訊：

    use Illuminate\Support\Facades\Route;

    $route = Route::current(); // Illuminate\Routing\Route
    $name = Route::currentRouteName(); // string
    $action = Route::currentRouteAction(); // string

你可以參考 [路由 facade 的底層類別](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) 和 [路由實體](https://laravel.com/api/{{version}}/Illuminate/Routing/Route.html) 的 API 文件來複習所有可行的路由器方法和路由類別方法。

<a name="cors"></a>
## 跨來源資源共用（Cross-Origin Resource Sharing, CORS）

Laravel 會依照你設定的值自動回應 CORS 的 `OPTIONS` HTTP 請求。所有 CORS 設定都可以在應用程式中的 `config/cors.php` 設定檔中設定。`OPTIONS` 請求會自動被 `HandleCors` [中介層](/docs/{{version}}/middleware) 處理，預設就包含全域中介層堆疊（global middleware stack）。全域中介層堆疊存在應用程式的 HTTP 核心（`App\Http\Kernel`）。

> **Note**  
> 更多關於 CORS 和 CORS 標頭的資訊，請參照 [MDN 網路文件上的 CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)

<a name="route-caching"></a>
## 路由快取（route cache）

當部署應用程式到產品環境時，你應該利用 Laravel 的路由快取。使用路由快取可以大幅降低註冊所有應用程式路由的時間。要產生路由快取，請執行 Artisan 指令 `route:cache`：

```shell
php artisan route:cache
```

執行這個指令後，快取路由檔在每個請求都會被載入。請記得，如果你新增任何新路由，會需要產生一個新的路由快取。因此，你應該只在專案部屬期間執行指令 `route:cache`：

你可以使用 `route:clear` 指令清除路由快取：

```shell
php artisan route:clear
```
