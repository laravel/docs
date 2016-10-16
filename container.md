# 服務容器（Container）

- [簡介](#introduction)
- [綁定](#binding)
    - [綁定基礎](#binding-basics)
    - [綁定介面至實作](#binding-interfaces-to-implementations)
    - [情境綁定](#contextual-binding)
    - [標記](#tagging)
- [解析](#resolving)
    - [Make 方法](#the-make-method)
    - [自動注入](#automatic-injection)
- [容器事件](#container-events)

<a name="introduction"></a>
## 簡介

Laravel 服務容器（Container）是管理類別依賴與執行依賴注入的強力工具。依賴注入是個花俏的名詞，事實上是指：類別的依賴透過建構子「注入」，或在某些情況下透過「setter」方法注入。

讓我們來看個簡單範例：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use App\Repositories\UserRepository;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 用戶儲存庫
         *
         * @var UserRepository
         */
        protected $users;

        /**
         * 建立一個新實例
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * 秀出用戶基本資料
         *
         * @param  int  $id
         * @return Response
         */
        public function show($id)
        {
            $user = $this->users->find($id);

            return view('user.profile', ['user' => $user]);
        }
    }

在這例子中，`UserController` 需要從資料來源中取得用戶。所以我們將會**注入**用戶儲存庫的服務來取得用戶。在此 `UserRepository` 的角色非常類似使用 [Eloquent](/docs/{{version}}/eloquent) 從資料庫中取得用戶資訊。由於儲存庫服務被注入，我們能容易地切換成其它實作。當測試應用程式時，我們一樣能輕易地「模擬(mock)」，或建立假的 `UserRepository` 實作來測試我們的程式。

深入地理解 Laravel 服務容器，對於構建功能強大的大型 Laravel 應用程式而言至關重要。甚至是貢獻 Laravel 核心的程式碼也是不可或缺的。

<a name="binding"></a>
## 綁定

<a name="binding-basics"></a>
### 綁定基礎

幾乎所有的服務容器綁定都會在[服務提供者](/docs/{{version}}/providers)中註冊，所以下方所有的例子將示範在該情境中使用容器。

> {tip} 如果類別沒有依賴任何的介面，那麼就沒有將類別綁定至容器中的必要。並不需要告訴容器如何建構這些物件，因為它會透過 PHP 的 reflection 自動解析出物件。

#### 簡單的綁定

在服務提供者中，隨時可以透過 `$this->app` 實例變數取得容器。我們可以使用 `bind` 方法註冊一個綁定，傳遞二個參數：希望註冊的類別或介面名稱，以及一個會回傳類別實例的`閉包`：

    $this->app->bind('HelpSpot\API', function ($app) {
        return new HelpSpot\API($app->make('HttpClient'));
    });

注意，我們將容器本身作為參數，傳入到解析器。然後我們可以使用該容器來解析我們正在構建的物件的子依賴。

#### 綁定一個單例（Singleton）

`singleton` 方法綁定一個類別或介面至容器中，只會被解析一次，且爾後的呼叫都會從容器中回傳相同的實例：

    $this->app->singleton('HelpSpot\API', function ($app) {
        return new HelpSpot\API($app->make('HttpClient'));
    });

#### 綁定實例（Instance）

你也可以使用 `instance` 方法，綁定一個已經存在的物件實例至容器中。爾後的呼叫都會從容器中回傳給定的實例：

    $api = new HelpSpot\API(new HttpClient);

    $this->app->instance('HelpSpot\Api', $api);

#### 綁定原始值（Primitive）

有時候，你的類別可能會接收注入的類別，同時還需注入原始值比如整數，這時你可以使用情境綁定輕鬆地注入此類別需要的任何值：

    $this->app->when('App\Http\Controllers\UserController')
              ->needs('$variableName')
              ->give($value);

<a name="binding-interfaces-to-implementations"></a>
### 綁定介面（Interface）至實作（Implementation）

服務容器有個非常強大的特色，就是能將給定的實作綁定至介面。舉個例子，假設我們有個 `EventPusher` 介面及一個 `RedisEventPusher` 實作。一旦我們撰寫完該介面的實作 `RedisEventPusher`，就可以如下將它註冊至服務容器：

    $this->app->bind(
        'App\Contracts\EventPusher',
        'App\Services\RedisEventPusher'
    );

這麼做會告知容器：當有個類別需要 `EventPusher` 的實作時，將會注入 `RedisEventPusher`。現在我們可以在建構子或任何其他透過服務容器注入依賴的地方進行 `EventPusher` 介面的依賴注入：

    use App\Contracts\EventPusher;

    /**
     * Create a new class instance.
     *
     * @param  EventPusher  $pusher
     * @return void
     */
    public function __construct(EventPusher $pusher)
    {
        $this->pusher = $pusher;
    }

<a name="contextual-binding"></a>
### 情境綁定

有時候，你可能有兩個類別使用到相同介面，但你希望每個類別能注入不同實作。例如，兩個控制器（譯註：PhotoController 和 VideoController）可能相依於 `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/{{version}}/contracts) 的不同實作。Laravel 提供一個簡單又流利介面來定義此行為：

    use Illuminate\Support\Facades\Storage;
    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\VideoController;
    use Illuminate\Contracts\Filesystem\Filesystem;

    $this->app->when(PhotoController::class)
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('local');
              });

    $this->app->when(VideoController::class)
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('s3');
              });

<a name="tagging"></a>
### 標記

少數情況下，可能需要解析特定「分類」下的所有綁定。例如，你正在建置一個報表匯整器，它能接收多個不同 `Report` 介面實作的陣列。註冊完 Report 實作後，可以使用 `tag` 方法為它們賦予一個標籤：

    $this->app->bind('SpeedReport', function () {
        //
    });

    $this->app->bind('MemoryReport', function () {
        //
    });

    $this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

一旦服務被標記之後，你可以簡單地透過 `tagged` 方法解析它們全部：

    $this->app->bind('ReportAggregator', function ($app) {
        return new ReportAggregator($app->tagged('reports'));
    });

<a name="resolving"></a>
## 解析

<a name="the-make-method"></a>
#### `make` 方法

你可以使用 `make` 方法從容器中解析出類別實例，`make` 方法接收你希望解析的類別或是介面的名稱：

    $api = $this->app->make('HelpSpot\API');

如果你的程式碼所在位置無法存取 `$app` 變數，可以使用此全域的輔助函數 `resolve`：

    $api = resolve('HelpSpot\API');

<a name="automatic-injection"></a>
#### 自動注入

此外，也是最常用的，你可以簡單地在類別的建構子中對依賴「型別提示」來解析出容器中物件，包含[控制器](/docs/{{version}}/controllers)、[事件監聽器](/docs/{{version}}/events)、[對列任務](/docs/{{version}}/queues)、[中介層](/docs/{{version}}/middleware)及其他等等。在實際情形中，這就是為何大部分的物件都是由容器中解析。

舉個例子，你可以在控制器的建構子中對應用程式中定義的儲存庫進行型別提示。儲存庫會自動被解析及注入至類別中：

    <?php

    namespace App\Http\Controllers;

    use App\Users\Repository as UserRepository;

    class UserController extends Controller
    {
        /**
         * 使用者儲存庫的實例
         */
        protected $users;

        /**
         * 建立一個新的控制器實例
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * 給定 ID 並回傳使用者
         *
         * @param  int  $id
         * @return Response
         */
        public function show($id)
        {
            //
        }
    }

<a name="container-events"></a>
## 容器事件

每當服務容器解析一個物件時就會觸發事件。你可以使用 `resolving` 方法監聽這個事件：The service container fires an event each time it resolves an object. You may listen to this event using the `resolving` method:

    $this->app->resolving(function ($object, $app) {
        // 當容器解析任何型別的物件時會被呼叫...
    });

    $this->app->resolving(HelpSpot\API::class, function ($api, $app) {
        // 當容器解析「HelpSpot\API」型別的物件時會被呼叫...
    });

如你所見，被解析的物件會被傳遞至回呼函式中，從而允許你在傳遞給消費者之前，設置任何額外的屬性至物件。
