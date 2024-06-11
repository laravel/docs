# 服務容器

- [簡介](#introduction)
    - [零組態設定解析](#zero-configuration-resolution)
    - [何時使用容器](#when-to-use-the-container)
- [綁定](#binding)
    - [綁定基礎](#binding-basics)
    - [綁定介面到實作](#binding-interfaces-to-implementations)
    - [上下文綁定](#contextual-binding)
    - [綁定原始值](#binding-primitives)
    - [綁定 typed variadics](#binding-typed-variadics)
    - [標籤](#tagging)
    - [擴充綁定](#extending-bindings)
- [解析](#resolving)
    - [Make 方法](#the-make-method)
    - [自動注入](#automatic-injection)
- [方法引用與注入](#method-invocation-and-injection)
- [容器事件](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 簡介

Laravel 服務容器是一個強大的工具，用於管理類別的依賴性和執行依賴注入。依賴注入是一個專業術語，基本意思是：類別的依賴性通過建構子或（在某些情況下）“setter”方法“注入”到類別中。

讓我們看一個簡單的例子：

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Repositories\UserRepository;
    use App\Models\User;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * Create a new controller instance.
         */
        public function __construct(
            protected UserRepository $users,
        ) {}

        /**
         * Show the profile for the given user.
         */
        public function show(string $id): View
        {
            $user = $this->users->find($id);

            return view('user.profile', ['user' => $user]);
        }
    }

在這個例子中，`UserController` 需要從資料源中檢索用戶。因此，我們將**注入**一個能夠檢索用戶的服務。在這個上下文中，我們的 `UserRepository` 很可能使用 [Eloquent](/docs/{{version}}/eloquent) 從資料庫中檢索用戶資訊。然而，由於這個資料倉儲是被注入的，我們能夠輕鬆地將其替換為另一個實作。我們還可以在測試我們的應用程式時輕鬆地“模擬”或創建一個 `UserRepository` 的假實作。

對 Laravel 服務容器的深入理解對於構建強大的、大型應用程式以及為 Laravel 核心做貢獻是必不可少的。

<a name="zero-configuration-resolution"></a>
### 零組態設定解析

如果一個類別沒有依賴或者僅依賴於其他具體類別（而不是介面），容器不需要指示如何解析該類別。例如，你可以將以下程式碼放置在你的 `routes/web.php` 文件中：

    <?php

    class Service
    {
        // ...
    }

    Route::get('/', function (Service $service) {
        die($service::class);
    });

在這個例子中，訪問應用程式的 `/` 路由會自動解析 `Service` 類別並將其注入到路由的處理器中。這是一個改變遊戲規則的功能。這意味著你可以開發應用程式並利用依賴注入，而不用擔心冗長的組態設定文件。

值得慶幸的是，當你構建 Laravel 應用程式時，你編寫的許多類別會自動通過容器接收它們的依賴，包括 [控制器](/docs/{{version}}/controllers)、[事件監聽器](/docs/{{version}}/events)、[中介層](/docs/{{version}}/middleware) 等。此外，你可以在 [佇列任務](/docs/{{version}}/queues) 的 `handle` 方法中提示依賴。一旦你體驗了自動和零組態設定依賴注入的強大功能，就會覺得開發不能沒有它。

<a name="when-to-use-the-container"></a>
### 何時使用容器

由於零組態設定解析，你經常會在路由、控制器、事件監聽器等地方提示依賴，而不用手動與容器互動。例如，你可能會在路由定義上提示 `Illuminate\Http\Request` 物件，這樣你就可以輕鬆地存取當前請求。即使我們從未與容器互動以編寫此程式碼，它在幕後管理這些依賴的注入：

    use Illuminate\Http\Request;

    Route::get('/', function (Request $request) {
        // ...
    });

在許多情況下，得益於自動依賴注入和 [facades](/docs/{{version}}/facades)，你可以構建 Laravel 應用程式而**從不**手動綁定或解析來自容器的任何內容。**那麼，什麼時候你需要手動與容器互動呢？** 讓我們來看看兩種情況。

首先，如果你編寫了一個類別它實作了一個介面，並希望在路由或類別建構子中提示該介面，你必須 [告訴容器如何解析該介面](#binding-interfaces-to-implementations)。其次，如果你正在 [編寫一個 Laravel 套件](/docs/{{version}}/packages) 並計劃與其他 Laravel 開發者分享，你可能需要將你的套件的服務綁定到容器中。

<a name="binding"></a>
## 綁定

<a name="binding-basics"></a>
### 綁定基礎

<a name="simple-bindings"></a>
#### 簡單綁定

幾乎所有的服務容器綁定都會在 [服務提供者](/docs/{{version}}/providers) 中註冊，因此這些例子大多數會演示如何在這個上下文中使用容器。

在服務提供者中，你總是可以通過 `$this->app` 屬性存取容器。我們可以使用 `bind` 方法註冊一個綁定，傳遞我們希望註冊的類別或介面名稱，以及一個回傳類別實例的閉包：

    use App\Services\Transistor;
    use App\Services\PodcastParser;
    use Illuminate\Contracts\Foundation\Application;

    $this->app->bind(Transistor::class, function (Application $app) {
        return new Transistor($app->make(PodcastParser::class));
    });

請注意，我們將容器本身作為解析器的參數。我們可以使用容器來解析我們正在構建的物件的子依賴項。

如前所述，你通常會在服務提供者中與容器互動；然而，如果你希望在服務提供者之外與容器互動，你可以通過 `App` [facade](/docs/{{version}}/facades) 來完成：

    use App\Services\Transistor;
    use Illuminate\Contracts\Foundation\Application;
    use Illuminate\Support\Facades\App;

    App::bind(Transistor::class, function (Application $app) {
        // ...
    });

只有在尚未為給定類型註冊綁定的情況下，你可以使用 `bindIf` 方法註冊容器綁定：

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 如果類別不依賴於任何介面，則無需將其綁定到容器。容器不需要指示如何構建這些物件，因為它可以通過反射自動解析這些物件。

<a name="binding-a-singleton"></a>
#### 綁定單例

`singleton` 方法將一個類別或介面綁定到容器中，使其只解析一次。一旦單例綁定被解析，在後續引用容器時將回傳相同的物件實例：

    use App\Services\Transistor;
    use App\Services\PodcastParser;
    use Illuminate\Contracts\Foundation\Application;

    $this->app->singleton(Transistor::class, function (Application $app) {
        return new Transistor($app->make(PodcastParser::class));
    });

只有在尚未為給定類型註冊綁定的情況下，您可以使用 `singletonIf` 方法註冊單例容器綁定：

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
#### 綁定範圍單例

`scoped` 方法將一個類別或介面綁定到容器中，使其在給定的 Laravel 請求 / 任務生命週期內僅解析一次。雖然此方法與 `singleton` 方法相似，但使用 `scoped` 方法註冊的實例將在 Laravel 應用程序啟動新的「生命週期」時被清除，例如當 [Laravel Octane](/docs/{{version}}/octane) 工作者處理新請求或 Laravel [佇列工作者](/docs/{{version}}/queues) 處理新任務時：

    use App\Services\Transistor;
    use App\Services\PodcastParser;
    use Illuminate\Contracts\Foundation\Application;

    $this->app->scoped(Transistor::class, function (Application $app) {
        return new Transistor($app->make(PodcastParser::class));
    });

<a name="binding-instances"></a>
#### 綁定實例

您也可以使用 `instance` 方法將現有物件實例綁定到容器中。在後續引用容器時將總是回傳給定的實例：

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $service = new Transistor(new PodcastParser);

    $this->app->instance(Transistor::class, $service);

<a name="binding-interfaces-to-implementations"></a>
### 將介面綁定到實作

服務容器的一個非常強大的功能是它能夠將介面綁定到給定的實作。例如，假設我們有一個 `EventPusher` 介面和一個 `RedisEventPusher` 實作。一旦我們編寫了該介面的 `RedisEventPusher` 實作，就可以這樣註冊它：

    use App\Contracts\EventPusher;
    use App\Services\RedisEventPusher;

    $this->app->bind(EventPusher::class, RedisEventPusher::class);

這條敘述告訴容器，當類別需要 `EventPusher` 的實作時，它應該注入 `RedisEventPusher`。現在我們可以在由容器解析的類別的建構子中型別提示 `EventPusher` 介面。請記住，控制器、事件監聽器、中介層以及 Laravel 應用程序中的各種其他類型的類別總是使用容器解析：

use App\Contracts\EventPusher;

    /**
     * 創建一個新的類別實例。
     */
    public function __construct(
        protected EventPusher $pusher
    ) {}

<a name="contextual-binding"></a>
### 上下文綁定

有時您可能有兩個類別使用相同的介面，但希望將不同的實作注入到每個類別中。例如，兩個控制器可能依賴於 `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/{{version}}/contracts) 的不同實作。Laravel 提供了一個簡單、流暢的界面來定義這種行為：

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\UploadController;
    use App\Http\Controllers\VideoController;
    use Illuminate\Contracts\Filesystem\Filesystem;
    use Illuminate\Support\Facades\Storage;

    $this->app->when(PhotoController::class)
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('local');
              });

    $this->app->when([VideoController::class, UploadController::class])
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('s3');
              });

<a name="binding-primitives"></a>
### 綁定 Primitives

有時您可能有一個類別接收一些注入的類別，但也需要注入一個 primitive 的值，例如整數。您可以輕鬆地使用上下文綁定來注入類別所需的任何值：

    use App\Http\Controllers\UserController;
    
    $this->app->when(UserController::class)
              ->needs('$variableName')
              ->give($value);

有時一個類別可能依賴於一個 [標籤](#tagging) 的實例陣列。使用 `giveTagged` 方法，您可以輕鬆地注入具有該標籤的所有容器綁定：

    $this->app->when(ReportAggregator::class)
        ->needs('$reports')
        ->giveTagged('reports');

如果您需要注入來自應用程序組態設定文件之一的值，可以使用 `giveConfig` 方法：

    $this->app->when(ReportAggregator::class)
        ->needs('$timezone')
        ->giveConfig('app.timezone');

<a name="binding-typed-variadics"></a>
### 綁定 Typed Variadics

有時候，您可能有一個類別它接收一個已定義型別的物件陣列使用 variadic 建構子參數：

    <?php

    use App\Models\Filter;
    use App\Services\Logger;

    class Firewall
    {
        /**
         * 過濾器實例。
         *
         * @var array
         */
        protected $filters;

        /**
         * 創建一個新的類實例。
         */
        public function __construct(
            protected Logger $logger,
            Filter ...$filters,
        ) {
            $this->filters = $filters;
        }
    }

使用上下文綁定，您可以通過提供 `give` 方法一個回傳解析的 `Filter` 實例陣列的閉包來解決此依賴關係：

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give(function (Application $app) {
                    return [
                        $app->make(NullFilter::class),
                        $app->make(ProfanityFilter::class),
                        $app->make(TooLongFilter::class),
                    ];
              });

為了方便，您也可以僅提供一個類別名稱的陣列，當 `Firewall` 需要 `Filter` 實例時，這些類別名稱將由容器解析：

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give([
                  NullFilter::class,
                  ProfanityFilter::class,
                  TooLongFilter::class,
              ]);

<a name="variadic-tag-dependencies"></a>
#### Variadic 標籤依賴

有時候，一個類別可能有一個型別提示為給定類別的 variadic 依賴（`Report ...$reports`）。使用 `needs` 和 `giveTagged` 方法，您可以輕鬆地注入具有該 [標籤](#tagging) 的所有容器綁定：

    $this->app->when(ReportAggregator::class)
        ->needs(Report::class)
        ->giveTagged('reports');

<a name="tagging"></a>
### 標籤

有時候，您可能需要解析所有某一「種類」的綁定。例如，或許您正在構建一個報告分析器，它接收一個許多不同 `Report` 介面實作的陣列。在註冊 `Report` 實作之後，您可以使用 `tag` 方法為它們分配一個標籤：

    $this->app->bind(CpuReport::class, function () {
        // ...
    });

    $this->app->bind(MemoryReport::class, function () {
        // ...
    });

    $this->app->tag([CpuReport::class, MemoryReport::class], 'reports');

一旦服務被標籤，您可以通過容器的 `tagged` 方法輕鬆地解析它們：

    $this->app->bind(ReportAnalyzer::class, function (Application $app) {
        return new ReportAnalyzer($app->tagged('reports'));
    });

<a name="extending-bindings"></a>
### 擴充綁定

`extend` 方法允許修改解析的服務。例如，當服務被解析時，您可以運行額外的程式碼來裝飾或組態設定該服務。`extend` 方法接受兩個參數，即您正在擴充的服務類別以及應回傳修改後服務的閉包。該閉包接收被解析的服務和容器實例：

    $this->app->extend(Service::class, function (Service $service, Application $app) {
        return new DecoratedService($service);
    });

<a name="resolving"></a>
## 解析

<a name="the-make-method"></a>
### `make` 方法

您可以使用 `make` 方法從容器解析類實例。`make` 方法接受您希望解析的類別或介面的名稱：

    use App\Services\Transistor;

    $transistor = $this->app->make(Transistor::class);

如果您的某些類別依賴關係無法通過容器解析，您可以將它們作為關聯陣列傳遞給 `makeWith` 方法。例如，我們可以手動傳遞 `Transistor` 服務所需的 `$id` 建構子參數：

    use App\Services\Transistor;

    $transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);

`bound` 方法可以用來確定一個類別或介面是否已經明確地綁定在容器中：

    if ($this->app->bound(Transistor::class)) {
        // ...
    }

如果您在服務提供者之外的程式碼位置無法存取 `$app` 變數，您可以使用 `App` [facade](/docs/{{version}}/facades) 或 `app` [輔助函式](/docs/{{version}}/helpers#method-app) 從容器解析類別實例：

    use App\Services\Transistor;
    use Illuminate\Support\Facades\App;

    $transistor = App::make(Transistor::class);

    $transistor = app(Transistor::class);

如果您希望將 Laravel 容器實例本身注入到容器解析的類別中，您可以在類別的建構子中型別提示 `Illuminate\Container\Container` 類別：

    use Illuminate\Container\Container;

    /**
     * 創建一個新的類別實例。
     */
    public function __construct(
        protected Container $container
    ) {}

<a name="automatic-injection"></a>
### 自動注入

另外，也是最重要的，您可以在由容器解析的類別的建構子中型別提示依賴，包括 [控制器](/docs/{{version}}/controllers)、[事件監聽器](/docs/{{version}}/events)、[中介層](/docs/{{version}}/middleware) 等。此外，您可以在 [佇列任務](/docs/{{version}}/queues) 的 `handle` 方法中型別提示依賴。在實務中，這就是您的大多數物件應該如何由容器解析的方式。

例如，您可以在控制器的建構子中型別提示應用程序定義的資料倉儲。該資料倉儲將自動被解析並注入到類別中：

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;
    use App\Models\User;

    class UserController extends Controller
    {
        /**
         * 創建一個新的控制器實例。
         */
        public function __construct(
            protected UserRepository $users,
        ) {}

        /**
         * 顯示給定 ID 的用戶。
         */
        public function show(string $id): User
        {
            $user = $this->users->findOrFail($id);

            return $user;
        }
    }

<a name="method-invocation-and-injection"></a>
## 方法引用和注入

有時您可能希望引用物件實例上的方法，同時允許容器自動注入該方法的依賴關係。例如，給定以下類別：

    <?php

    namespace App;

    use App\Repositories\UserRepository;

    class UserReport
    {
        /**
         * 生成新的用戶報告。
         */
        public function generate(UserRepository $repository): array
        {
            return [
                // ...
            ];
        }
    }

您可以通過容器引用 `generate` 方法，如下所示：

    use App\UserReport;
    use Illuminate\Support\Facades\App;

    $report = App::call([new UserReport, 'generate']);

`call` 方法接受任何 PHP 可引用物件。容器的 `call` 方法甚至可以用來引用一個閉包，同時自動注入其依賴關係：

    use App\Repositories\UserRepository;
    use Illuminate\Support\Facades\App;

    $result = App::call(function (UserRepository $repository) {
        // ...
    });

<a name="container-events"></a>
## 容器事件

每次服務容器解析物件時都會觸發一個事件。您可以使用 `resolving` 方法監聽此事件：

    use App\Services\Transistor;
    use Illuminate\Contracts\Foundation\Application;

    $this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
        // 當容器解析 "Transistor" 類型的物件時引用...
    });

    $this->app->resolving(function (mixed $object, Application $app) {
        // 當容器解析任何類型的物件時引用...
    });

如您所見，正在解析的物件將傳遞給回呼，允許您在物件交給其消費者之前設置任何其他屬性。

<a name="psr-11"></a>
## PSR-11

Laravel 的服務容器實作了 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 介面。因此，您可以型別提示 PSR-11 容器介面以獲取 Laravel 容器的實例：

    use App\Services\Transistor;
    use Psr\Container\ContainerInterface;

    Route::get('/', function (ContainerInterface $container) {
        $service = $container->get(Transistor::class);

        // ...
    });

如果給定識別字無法解析，將拋出異常。如果識別字從未綁定，則異常將是 `Psr\Container\NotFoundExceptionInterface` 的實例。如果識別字已綁定但無法解析，則會拋出 `Psr\Container\ContainerExceptionInterface` 的實例。