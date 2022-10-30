# 控制器（Controller）

- [前言](#introduction)
- [撰寫控制器](#writing-controllers)
    - [基礎控制器](#basic-controllers)
    - [單一動作的控制器](#single-action-controllers)
- [控制器中介層](#controller-middleware)
- [資源控制器](#resource-controllers)
    - [部分的資源路由](#restful-partial-resource-routes)
    - [巢狀資源](#restful-nested-resources)
    - [命名資源路由](#restful-naming-resource-routes)
    - [命名資源路由的參數](#restful-naming-resource-route-parameters)
    - [限制資源路由的範圍](#restful-scoping-resource-routes)
    - [本地化資源 URI](#restful-localizing-resource-uris)
    - [補充資源控制器](#restful-supplementing-resource-controllers)
- [依賴注入（dependency injection）和控制器](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 前言

比起在路由檔案中使用閉包定義所有的請求處理邏輯，你可能會希望用「控制器」類別來組織這個行為。控制器可以將相關的請求處理邏輯群組化到單一類別內。舉例來說，`UserController` 類別可以處理有關使用者的所有連入請求，包含顯示、建立、更新和刪除使用者。預設情況下，控制器被儲存在 `app/Http/Controllers` 目錄中。

<a name="writing-controllers"></a>
## 撰寫控制器

<a name="basic-controllers"></a>
### 基礎控制器

來看看一個基礎控制器的例子。請注意，該控制器繼承了 Laravel 所包含的基礎控制器類別：`App\Http\Controllers\Controller`：

    <?php

    namespace App\Http\Controllers;
    
    use App\Models\User;

    class UserController extends Controller
    {
        /**
         * 顯示指定使用者的個人檔案。
         *
         * @param  int  $id
         * @return \Illuminate\View\View
         */
        public function show($id)
        {
            return view('user.profile', [
                'user' => User::findOrFail($id)
            ]);
        }
    }

你可以像這樣定義此控制器方法的路由：

    use App\Http\Controllers\UserController;

    Route::get('/user/{id}', [UserController::class, 'show']);

當連入請求符合指定的路由 URI，`App\Http\Controllers\UserController` 類別的 `show` 方法將會被調用，且路由參數也會被傳入此方法。

> **Note**  
> 控制器並 **不一定** 要繼承基礎類別。不過，你也會無法存取方便的功能，如 `middleware` 和 `authorize` 方法。

<a name="single-action-controllers"></a>
### 單一動作的控制器

如果某個控制器動作特別複雜，你會發現將整個控制器類別放到單一動作更顯得方便。為此，可以在控制器內定義一個 `__invoke` 方法：

    <?php

    namespace App\Http\Controllers;
    
    use App\Models\User;

    class ProvisionServer extends Controller
    {
        /**
         * 提供一個新的 web 伺服器。
         *
         * @return \Illuminate\Http\Response
         */
        public function __invoke()
        {
            // ...
        }
    }

使用單一動作控制器註冊路由時，你不需要指定控制器方法。只需要單純傳入控制器的名稱給路由：

    use App\Http\Controllers\ProvisionServer;

    Route::post('/server', ProvisionServer::class);

你可以使用 Artisan 指令 `make:controller` 的 `--invokable` 選項來產生一個可調用的控制器：

```shell
php artisan make:controller ProvisionServer --invokable
```

> **Note**  
> 控制器的 stub 可以使用 [發佈 stub](/docs/{{version}}/artisan#stub-customization) 自定義。

<a name="controller-middleware"></a>
## 控制器中介層

可以在路由檔案中指派 [中介層](/docs/{{version}}/middleware) 給控制器路由：

    Route::get('profile', [UserController::class, 'show'])->middleware('auth');

或者，你會發現在控制器的建構子（constructor）指定中介層會更方便。使用控制器建構子的`middleware` 方法，可以指派中介層給控制器動作：

    class UserController extends Controller
    {
        /**
         * 實體化一個新的控制器執行個體（controller instance）。
         *
         * @return void
         */
        public function __construct()
        {
            $this->middleware('auth');
            $this->middleware('log')->only('index');
            $this->middleware('subscribed')->except('store');
        }
    }

控制器也允許你使用閉包註冊中介層。這提供了方便的方法為單一控制器定義內嵌的中介層，而不需要定義整個中介層類別：

    $this->middleware(function ($request, $next) {
        return $next($request);
    });

<a name="resource-controllers"></a>
## 資源控制器

如果你將應用程式的每個 Eloquent 模型視作是「資源」，則對應用程式中的每個資源執行相同的動作是很平常的。舉例來說，想像應用程式中包含一個 `Photo` 模型和一個 `Movie` 模型。那使用者可能就可以建立、檢視、更新或刪除這些資源。

由於這些常見的使用情況，Laravel 資源路由可以使用一行程式碼指派常見的建立（create）、檢視（read）、更新（update）和刪除（delete）（CRUD）路由給控制器。我們可以使用 Artisan 指令 `make:controller` 的 `--resource` 選項快速建立一個控制器來處理這些動作：

```shell
php artisan make:controller PhotoController --resource
```

這個指令會在 `app/Http/Controllers/PhotoController.php` 中產生一個控制器。該控制器將會包含各種可用資源操作的方法。下一步，你可以註冊一個指向該控制器的資源路由：

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class);

這個單一路由宣告會建立多個路由去處理對資源的多種動作。產生的控制器也已經為這些動作保留了方法。請記得，你永遠可以透過執行 Artisan 指令 `route:list` 快速檢視應用程式的路由。

甚至可以透過 `resources` 方法傳入陣列來一次註冊多個資源控制器：

    Route::resources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

<a name="actions-handled-by-resource-controller"></a>
#### 資源控制器處理的動作

Verb      | URI                    | Action       | Route Name
----------|------------------------|--------------|---------------------
GET       | `/photos`              | index        | photos.index
GET       | `/photos/create`       | create       | photos.create
POST      | `/photos`              | store        | photos.store
GET       | `/photos/{photo}`      | show         | photos.show
GET       | `/photos/{photo}/edit` | edit         | photos.edit
PUT/PATCH | `/photos/{photo}`      | update       | photos.update
DELETE    | `/photos/{photo}`      | destroy      | photos.destroy

<a name="customizing-missing-model-behavior"></a>
#### 自訂找不到模型的行為

通常，如果沒找到隱式綁定的模型時會產生一個 404 HTTP 回應。不過你可以在定義路由時自訂呼叫 `missing` 方法的行為。`missing` 方法是接受一個閉包（closure）並可以在任何資源路由上找不到隱式綁定模型時做調用：

    use App\Http\Controllers\PhotoController;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Redirect;

    Route::resource('photos', PhotoController::class)
            ->missing(function (Request $request) {
                return Redirect::route('photos.index');
            });

<a name="soft-deleted-models"></a>
#### 軟刪除（soft delete）模型

一般而言，隱式模型綁定不會檢索已經被 [軟刪除](/docs/{{version}}/eloquent#soft-deleting) 的模型，而且會回傳一個 404 HTTP 回應作為替代。但你可以在定義資源路由時調用 `withTrashed` 方法指示框架允許檢索軟刪除模型：

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->withTrashed();

呼叫 `withTrashed` 不帶引數的話將會允許軟刪除 `show`、`edit`、和 `update` 資源路由的模型。你可以傳入一組陣列給 `withTrashed` 方法來指定這些路由的子集：

    Route::resource('photos', PhotoController::class)->withTrashed(['show']);

<a name="specifying-the-resource-model"></a>
#### 指定資源模型

如果你正在使用 [路由模型綁定](/docs/{{version}}/routing#route-model-binding) 且想要用資源控制器方法對模型執行個體做型別提示（type-hint），可以在產生控制器時使用 `--model` 選項：

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 產生表單請求

你可以在產生資源控制器時提供 `--requests` 選項去指示 Aritsan 要產生用於控制器儲存（storage）和更新（update）方法的 [表單請求類別](/docs/{{version}}/validation#form-request-validation)：

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 部分資源路由

宣告資源路由時，可以指示控制器處理部分動作而不是全套的預設動作：

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->only([
        'index', 'show'
    ]);

    Route::resource('photos', PhotoController::class)->except([
        'create', 'store', 'update', 'destroy'
    ]);

<a name="api-resource-routes"></a>
#### API 資源路由

宣告資源路由將會被 API 使用時，你通常會希望排除顯示 HTML 模板的路由，例如 `create` 和 `edit`。為了方便起見，可以使用 `apiResource` 方法去自動排除這兩個路由：

    use App\Http\Controllers\PhotoController;

    Route::apiResource('photos', PhotoController::class);

你可以傳入一組陣列給 `apiResource` 方法來一次註冊許多 API 資源控制器：

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\PostController;

    Route::apiResources([
        'photos' => PhotoController::class,
        'posts' => PostController::class,
    ]);

要快速產生不包含 `create` 或 `edit` 方法的 API 資源控制器，可以在執行 `make:controller` 指令時使用 `--api` 開關：

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 巢狀資源

有時候你會需要給巢狀資源定義路由。舉例來說，照片資源會在照片上附加多個評論。要巢狀嵌入資源控制器，可以在路由宣告上使用符號「.」：

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class);

這個路由會註冊一個巢狀資源使其可以存取像是下面的 URI：

    /photos/{photo}/comments/{comment}

<a name="scoping-nested-resources"></a>
#### 限定範圍的巢狀資源

Laravel 的 [限制範圍的隱式模型綁定](/docs/{{version}}/routing#implicit-model-binding-scoping) 功能可以自動限制巢狀綁定的範圍，並確認被解析的子模型是否屬於父模型。在定義巢狀資源時透過使用 `scoped` 方法，就可以自動開啟範圍限制，並指示 Laravel 應該檢索哪個子資源的欄位。更多關於如何完成此功能的資訊，請參閱文件 [限定資源路由的範圍](#restful-scoping-resource-routes)。

<a name="shallow-nesting"></a>
#### 淺層巢狀（shallow nesting）

通常 URI 中並不需要同時擁有父層與子層的 ID，因為子 ID 已經是唯一的識別碼。使用唯一的識別碼如自動遞增的主鍵（primary key）來辨識 URI 字段的模型時，可以選擇使用「淺層巢狀」：

    use App\Http\Controllers\CommentController;

    Route::resource('photos.comments', CommentController::class)->shallow();

該路由定義會定義以下的路由：

Verb      | URI                               | Action       | Route Name
----------|-----------------------------------|--------------|---------------------
GET       | `/photos/{photo}/comments`        | index        | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create       | photos.comments.create
POST      | `/photos/{photo}/comments`        | store        | photos.comments.store
GET       | `/comments/{comment}`             | show         | comments.show
GET       | `/comments/{comment}/edit`        | edit         | comments.edit
PUT/PATCH | `/comments/{comment}`             | update       | comments.update
DELETE    | `/comments/{comment}`             | destroy      | comments.destroy

<a name="restful-naming-resource-routes"></a>
### 命名資源路由

預設情況下，所有的資源控制器動作都會有個路由名稱；不過你可以通過傳入 `names` 陣列覆寫成你想要的路由名稱：

    use App\Http\Controllers\PhotoController;

    Route::resource('photos', PhotoController::class)->names([
        'create' => 'photos.build'
    ]);

<a name="restful-naming-resource-route-parameters"></a>
### 命名資源路由的參數

預設情況下，`Route::resource` 會基於「單數化」資源名稱，為資源路由建立路由參數。你可以使用 `parameters` 方法來輕鬆地覆寫各個資源基礎。傳入 `parameters` 方法的陣列應該要是包含資源名稱和參數名稱的關聯陣列：

    use App\Http\Controllers\AdminUserController;

    Route::resource('users', AdminUserController::class)->parameters([
        'users' => 'admin_user'
    ]);

以上範例為資源的 `show` 路由產生以下的 URI：

    /users/{admin_user}

<a name="restful-scoping-resource-routes"></a>
### 限制資源路由的範圍

Laravel 的 [限制範圍的隱式模型綁定](/docs/{{version}}/routing#implicit-model-binding-scoping) 功能可以自動限制巢狀綁定的範圍，並確認被解析的子模型是否屬於父模型。在定義巢狀資源時透過使用 `scoped` 方法，就可以自動開啟範圍限制，並指示 Laravel 應該檢索哪個子資源的欄位：

    use App\Http\Controllers\PhotoCommentController;

    Route::resource('photos.comments', PhotoCommentController::class)->scoped([
        'comment' => 'slug',
    ]);

這個路由會註冊一個巢狀資源使其可以存取像是下面的 URI：

    /photos/{photo}/comments/{comment:slug}

使用自訂鍵的隱式綁定作為巢狀路由參數時，Laravel 會透過猜測父層約定的關聯名稱去自動限制查詢範圍，並檢索巢狀模型。在這個例子中，假設 `Photo` 模型有一個關聯名稱 `comments`（路由參數名稱的複數形式），此關聯便會被用來檢索 `Comment` 模型。

<a name="restful-localizing-resource-uris"></a>
### 本地化資源 URI

預設情況下，`Route::resource` 會使用英文動詞和複數規則建立資源 URI。如果你需要本地化 `create` 和 `edit` 動作的動詞，可以使用 `Route::resourceVerbs` 方法。這可以在 `App\Providers\RouteServiceProvider` 的 `boot` 方法開頭完成：

    /**
     * 定義路由模型綁定，模式過濾器等。
     *
     * @return void
     */
    public function boot()
    {
        Route::resourceVerbs([
            'create' => 'crear',
            'edit' => 'editar',
        ]);

        // ...
    }

Laravel 的複數化支援 [依需求設定的多種不同語言](/docs/{{version}}/localization#pluralization-language)。一旦動詞和複數化語言已經自訂過，資源路由註冊例如 `Route::resource('publicacion', PublicacionController::class)` 會產生以下的 URI：

    /publicacion/crear

    /publicacion/{publicaciones}/editar

<a name="restful-supplementing-resource-controllers"></a>
### 補充資源控制器

如果你需要增加預設資源路由之外的額外路由給資源控制器，應該要在呼叫 `Route::resource` 之前先行定義這些路由；否則，由 `resource` 方法定義的路由可能會無意中優先於補充路由。

    use App\Http\Controller\PhotoController;

    Route::get('/photos/popular', [PhotoController::class, 'popular']);
    Route::resource('photos', PhotoController::class);

> **Note**  
> 請記得保持控制器的專一性。如果你發現常需要用到一般資源動作以外的方法，請考慮將控制器拆成兩個、更小的控制器。

<a name="dependency-injection-and-controllers"></a>
## 依賴注入和控制器

<a name="constructor-injection"></a>
#### 建構子注入（constructor injection）

Laravel 的 [服務容器](/docs/{{version}}/container) 被用於解析所有的 Laravel 控制器。因此，可以在建構子中，型別提式任何依賴的控制器。宣告的依賴會被自動解析且注入到控制器的執行個體：

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * 使用者的資料倉儲執行個體（repository instance）
         */
        protected $users;

        /**
         * 建立一個新的控制器執行個體。
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }
    }

<a name="method-injection"></a>
#### 方法注入（method injection）

除了建構子注入之外，也可以在控制器方法上對依賴項作型別提式。常見的方法注入的使用情況是注入 `Illuminate\Http\Request` 的執行個體到控制器方法中：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 儲存一個新的使用者。
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            $name = $request->name;

            //
        }
    }

若控制器方法有來自路由參數的預期輸入，請在其他依賴項之後列出路由引數。舉例來說，如果你的路由像這樣定義：

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

你依然可以像以下定義控制器方法作型別提式 `Illuminate\Http\Request` 並存取 `id` 參數

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * 更新指定使用者。
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  string  $id
         * @return \Illuminate\Http\Response
         */
        public function update(Request $request, $id)
        {
            //
        }
    }
