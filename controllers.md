# HTTP 控制器

- [簡介](#introduction)
- [基礎控制器](#basic-controllers)
- [控制器中介層](#controller-middleware)
- [RESTful 資源控制器](#restful-resource-controllers)
    - [部分資源路由](#restful-partial-resource-routes)
    - [命名資源路由](#restful-naming-resource-routes)
    - [巢狀資源](#restful-nested-resources)
    - [附加資源控制器](#restful-supplementing-resource-controllers)
- [隱式控制器](#implicit-controllers)
- [依賴注入與控制器](#dependency-injection-and-controllers)
- [路由快取](#route-caching)

<a name="introduction"></a>
## 簡介

除了在單一的 `routes.php` 檔案中定義所有的請求處理邏輯，您可能希望使用控制器類別來組織此行為。控制器可將相關的 HTTP 請求處理邏輯組成一個類別。控制器一般存放在 `app/Http/Controllers` 目錄下。

<a name="basic-controllers"></a>
## 基礎控制器

這是一個基礎控制器類別的範例。所有 Laravel 控制器都應繼承基礎控制器類別，它包含在 Laravel 的預設安裝中：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的個人資料。
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            return view('user.profile', ['user' => User::findOrFail($id)]);
        }
    }

我們可以經由路由指定控制器行為，就像這樣：

    Route::get('user/{id}', 'UserController@showProfile');

現在，當請求和此特定的路由 URI 相匹配時，`UserController` 類別的 `showProfile` 方法就會被執行。當然，路由的參數也會被傳遞至該方法。

#### 控制器和命名空間

有一點非常重要，那就是我們在定義控制器路由時，不需要指定完整的控制器命名空間。我們只需要定義「根」命名空間 `App\Http\Controllers` 之後的部分類別名稱。預設 `RouteServiceProvider` 會將 `routes.php` 檔案裡的路由規則包在
根控制器命名空間的路由群組下。

若你選擇在 `App\Http\Controllers` 目錄內層，使用 PHP 命名空間巢狀或組織控制器，只要使用相對於 `App\Http\Controllers` 根命名空間的特定類別名稱即可。因此，若您的控制器類別全名為 `App\Http\Controllers\Photos\AdminController`，您可以像這樣註冊一個路由：

    Route::get('foo', 'Photos\AdminController@method');

#### 命名控制器路由

就像閉包路由，您可以指定控制器路由的名稱：

    Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

#### 控制器行為的 URLs

您也可以使用 `route` 輔助方法，產生命名控制器路由的 URL：

    $url = route('name');

一旦你指定了控制器路由的名稱，你可以很容易地產生能達成該行為的 URL。你也可以使用 `action` 輔助方法產生指向控制器行為的 URL。同樣地，我們只需指定基底命名空間 `App\Http\Controllers` 之後的部分控制器類別名稱就可以了：

    $url = action('FooController@method');

You may access the name of the controller action being run using the `currentRouteAction` method on the `Route` facade:

	$action = Route::currentRouteAction();

<a name="controller-middleware"></a>
## 控制器中介層

可將[中介層](/docs/{{version}}/middleware)指定給控制器路由，例如：

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'UserController@showProfile'
    ]);

不過，在控制器建構子中指定中介層會更為方便。在控制器建構子中使用 `middleware` 方法，你可以很容易地將中介層指定給控制器。你甚至可以對中介層作出限制，僅將它提供給控制器類別中的某些方法。

    class UserController extends Controller
    {
        /**
         * 新增一個 UserController 實例。
         *
         * @return void
         */
        public function __construct()
        {
            $this->middleware('auth');

            $this->middleware('log', ['only' => ['fooAction', 'barAction']]);

            $this->middleware('subscribed', ['except' => ['fooAction', 'barAction']]);
        }
    }

<a name="restful-resource-controllers"></a>
## RESTful 資源控制器

資源控制器讓您可以無痛地建立與資源有關的 RESTful 控制器。例如，你可能想要建立一個控制器，用來處理對你應用程式儲存「相片」發送的 HTTP 請求。使用 `make:controller` Artisan 指令，我們可以快速地建立像這樣的控制器：

    php artisan make:controller PhotoController

此 Artisan 指令會產生 `app/Http/Controllers/PhotoController.php` 控制器檔案。此控制器會包含用來操作可取得的各種資源的方法。

接下來，您可以在控制器中註冊資源化路由：

    Route::resource('photo', 'PhotoController');

這一條路由宣告會創建多個路由，用來處理各式各樣和相片資源相關的的 RESTful 行為。同樣地，產生的控制器已有各種和這些行為繫結的方法，並包含通知您它們所處理的 URI 及動詞的記錄。

#### 由資源控制器處理的行為

動詞      | 路徑                  | 行為         | 路由名稱
----------|-----------------------|--------------|---------------------
GET       | `/photo`              | index        | photo.index
GET       | `/photo/create`       | create       | photo.create
POST      | `/photo`              | store        | photo.store
GET       | `/photo/{photo}`      | show         | photo.show
GET       | `/photo/{photo}/edit` | edit         | photo.edit
PUT/PATCH | `/photo/{photo}`      | update       | photo.update
DELETE    | `/photo/{photo}`      | destroy      | photo.destroy

<a name="restful-partial-resource-routes"></a>
#### 部分資源路由

宣告資源路由時，您可以指定讓此路由僅處理一部分的行為：

    Route::resource('photo', 'PhotoController',
                    ['only' => ['index', 'show']]);

    Route::resource('photo', 'PhotoController',
                    ['except' => ['create', 'store', 'update', 'destroy']]);

<a name="restful-naming-resource-routes"></a>
#### 命名資源路由

所有的資源控制器行為預設都有一路由名稱；不過你可以在選項中傳遞一個 `names` 陣列來覆寫這些名稱：

    Route::resource('photo', 'PhotoController',
                    ['names' => ['create' => 'photo.build']]);

<a name="restful-nested-resources"></a>
#### 巢狀資源

有時您可能會需要對「巢狀」資源定義路由。例如，相片資源可能會附帶多個「註解」。要「巢狀化」此資源控制器，可在路由宣告中使用「點」記號：

    Route::resource('photos.comments', 'PhotoCommentController');

此路由會註冊一個「巢狀化」的資源，可透過下面這樣的 URL 來存取它：`photos/{photos}/comments/{comments}`。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;

    class PhotoCommentController extends Controller
    {
        /**
         * 顯示指定相片的註解。
         *
         * @param  int  $photoId
         * @param  int  $commentId
         * @return Response
         */
        public function show($photoId, $commentId)
        {
            //
        }
    }

<a name="restful-supplementing-resource-controllers"></a>
#### 附加資源控制器

若您必須在資源控制器中預設的資源路由之外，加入額外的路由，您應該在呼叫 `Route::resource` 之前定義這些路由。否則，由 `resource` 方法定義的路由可能會意外地覆蓋您附加的路由：

    Route::get('photos/popular', 'PhotoController@method');

    Route::resource('photos', 'PhotoController');

<a name="implicit-controllers"></a>
## 隱式控制器

Laravel 讓您能夠輕易地透過定義單一路由來處理控制器類別中的各種行為。首先，使用 `Route::controller` 方法來定義路由。`controller` 方法接受兩個參數。第一個參數是控制器所處理的基底 URI，第二個是控制器的類別名稱：

    Route::controller('users', 'UserController');

接下來，只要在控制器中加入方法。方法的名稱應由它們所回應的 HTTP 動詞作為開頭，緊跟著首字母大寫的 URI 所組成：

    <?php

    namespace App\Http\Controllers;

    class UserController extends Controller
    {
        /**
         * 回應對 GET /users 的請求
         */
        public function getIndex()
        {
            //
        }

        /**
         * 回應對 GET /users/show/1 的請求
         */
        public function getShow($id)
        {
            //
        }

        /**
         * 回應對 GET /users/admin-profile 的請求
         */
        public function getAdminProfile()
        {
            //
        }

        /**
         * 回應對 POST /users/profile 的請求
         */
        public function postProfile()
        {
            //
        }
    }

正如您在上述範例中所看到的，`index` 方法會回應控制器所處理的根 URI，在這個例子中是 `users`。

#### 分派路由名稱

如果你想要[命名](/docs/{{version}}/routing#named-routes)控制器中的某些路由，你可以在 `controller` 方法中傳入一個名稱陣列作為第三個參數：

    Route::controller('users', 'UserController', [
        'getShow' => 'user.show',
    ]);

<a name="dependency-injection-and-controllers"></a>
## 依賴注入與控制器

#### 建構子注入

Laravel [服務容器](/docs/{{version}}/container)用於解析所有的 Laravel 控制器。因此，在建構子中，你可以對控制器可能需要的任何依賴使用型別提示。依賴會自動被解析並注入控制器實例之中。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Routing\Controller;
    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * 使用者儲存庫實例。
         */
        protected $users;

        /**
         * 建立新的控制器實例。
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }
    }

當然，您也可以對任何的 [Laravel contract](/docs/{{version}}/contracts) 使用型別提示。若容器能夠解析它，你就可以使用型別提示。

#### 方法注入

除了建構子注入之外，你也可以對控制器行為方法的依賴使用型別提示。例如，讓我們對 `Illuminate\Http\Request` 實例的其中一個方法使用型別提示：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * 儲存一個新的使用者。
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $name = $request->input('name');

            //
        }
    }

若你的控制器方法也預期從路由參數獲得輸入值，只要在你其它的依賴之後列出路由參數即可。例如，如果你的路由被定義成這個樣子：

    Route::put('user/{id}', 'UserController@update');

你依然可以做 `Illuminate\Http\Request` 型別提示並透過定義你的控制器方法類似下面範例，來存取你的路由參數 `id`：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * 更新指定的使用者。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function update(Request $request, $id)
        {
            //
        }
    }

<a name="route-caching"></a>
## 路由快取

> **Note:** Route caching does not work with Closure based routes. To use route caching, you must convert any Closure routes to use controller classes.

若您的應用程式完全透過控制器使用路由，您可以利用 Laravel 的路由快取。使用路由快取可以大幅降低註冊您應用程式全部的路由所需的時間。在某些情況下，您的路由註冊甚至可以快上一百倍！要產生路由快取，只要執行 `route:cache` 此 Artisan 指令：

    php artisan route:cache

這就是全部了！現在你的快取路由檔案將被用來代替 `app/Http/routes.php` 此一檔案。請記得，若你新增了任何新的路由，就必須產生新的路由快取。因此你可能希望只在您的專案部署時才執行 `route:cache` 此一指令。

要移除快取路由檔案而不產生新的快取，請使用 `route:clear` 指令：

    php artisan route:clear
