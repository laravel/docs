# Directory Structure

- [ 前言 ](#introduction)
- [ 目錄 ](#the-root-directory)
    - [ `app` 目錄 ](#the-root-app-directory)
    - [ `bootstrap` 目錄 ](#the-bootstrap-directory)
    - [ `config` 目錄 ](#the-config-directory)
    - [ `database` 目錄 ](#the-database-directory)
    - [ `lang` 目錄 ](#the-lang-directory)
    - [ `public` 目錄 ](#the-public-directory)
    - [ `resources` 目錄 ](#the-resources-directory)
    - [ `routes` 目錄 ](#the-routes-directory)
    - [ `storage` 目錄 ](#the-storage-directory)
    - [ `tests` 目錄 ](#the-tests-directory)
    - [ `vendor` 目錄 ](#the-vendor-directory)
- [ App 目錄 ](#the-app-directory)
    - [ `Broadcasting` 目錄 ](#the-broadcasting-directory)
    - [ `Console` 目錄 ](#the-console-directory)
    - [ `Events` 目錄 ](#the-events-directory)
    - [ `Exceptions` 目錄 ](#the-exceptions-directory)
    - [ `Http` 目錄 ](#the-http-directory)
    - [ `Jobs` 目錄 ](#the-jobs-directory)
    - [ `Listeners` 目錄 ](#the-listeners-directory)
    - [ `Mail` 目錄 ](#the-mail-directory)
    - [ `Models` 目錄 ](#the-models-directory)
    - [ `Notifications` 目錄 ](#the-notifications-directory)
    - [ `Policies` 目錄 ](#the-policies-directory)
    - [ `Providers` 目錄 ](#the-providers-directory)
    - [ `Rules` 目錄 ](#the-rules-directory)

<a name="introduction"></a>
## 前言

預設的 Laravel 應用程式結構旨在提供一個好的起始點給不同大小的應用程式。但你也可以依照喜好自由地組織應用程式。Laravel 幾乎沒有強加限制任何類別的放置位置 - 只要 Composer 可以自動載入這些類別即可。

> **Note**
> New to Laravel? Check out the [Laravel Bootcamp](https://bootcamp.laravel.com) for a hands-on tour of the framework while we walk you through building your first Laravel application.

<a name="the-root-directory"></a>
## 根目錄

<a name="the-root-app-directory"></a>
#### App 目錄

目錄 `app` 包含應用程式的核心程式碼，我們很快會深入探討這個目錄的細節；然而，你應用程式的大部分類別將會放置在這個目錄之中。

<a name="the-bootstrap-directory"></a>
#### Bootstrap 目錄

目錄 `bootstrap` 包含用來啟動框架的 `app.php` 檔案。以及包含用來生成框架檔和設定路由及服務（service）快取檔的 `cache` 目錄。你通常不需要修改這個目錄中的任何檔案。

<a name="the-config-directory"></a>
#### Config 目錄

顧名思義，目錄 `config` 包含應用程式的所有設定檔。把這些檔案瀏覽一遍並熟悉對你有用的選項是個好主意。

<a name="the-database-directory"></a>
#### Database 目錄

目錄 `database` 包含你的資料庫遷移（database migration）、模型工廠（model factory）和資料填充（seed）。如果你希望，也可以在此目錄存放 SQLite 資料庫。

<a name="the-lang-directory"></a>
#### Lang 目錄

目錄 `lang` 存放著應用程式所有的語言檔案。

<a name="the-public-directory"></a>
#### Public 目錄

目錄 `public` 包含進入應用程式所有請求的入口和設定為自動載入的 `index.php` 檔。這個目錄也存放著你的資源，例如圖片、JavaScript 和 CSS。

<a name="the-resources-directory"></a>
#### Resources 目力

目錄 `resources` 包含你 [ 視圖（views）](/docs/{{version}}/views) 的原始碼和尚未編譯的 CSS 和 JavaScript 資源。

<a name="the-routes-directory"></a>
#### Routes 目錄

目錄 `routes`  包含所有應用程式的路由（route）定義。預設情況下，大部分的路由檔案都能在 Laravel 找到： `web.php`, `api.php`, `console.php` 和 `channels.php`。

`web.php` 檔案中定義的路由都會在 `RouteServiceProvider` 中且被指配到 `web` 中介層群組。具備 Session、CSRF 防護以及 Cookie 加密功能。如果你的應用程式不用提供無狀態的 RESTful API，那麼所有的路由都能在 `web.php` 檔案內找到。

`api.php` 檔案裡定義的路由都會在`RouteServiceProvider` 中且被指配到 `api` 中介層群組。 這些路由通常是無狀態的，所以透過這些路由進入應用程式的請求（request）通常是 [ 透過標記（tokens） ](/docs/{{version}}/sanctum) 進行驗證（authenticate）且不能存取 Session 狀態。

`console.php` 檔案是你定義所有基於閉包（closure）終端機指令（console command）的地方。每個閉包一定是一個允許跟指令的 IO 方法（method）進行簡易互動的指令執行個體（command instance）。儘管這個檔案沒有定義 HTTP 路由，它也會定義應用程式中基於入口點（路由）的終端（console）。

The `channels.php` 檔是你註冊所有應用程式支援的 [ 廣播事件 ](/docs/{{version}}/broadcasting) 頻道的地方。

<a name="the-storage-directory"></a>
#### Storage 目錄

目錄 `storage` 包含你的日誌、編譯後的 Blade 模板（template）、基於檔案的 Session、檔案快取（cache）和框架產生的其他檔案。這個目錄又被分為 `app`, `framework` 和 `logs` 資料夾。 `app` 目錄常用來儲存應用程式產生的任何檔案。 `framework` 目錄常用來儲存框架產生的檔案及快取。最後 `logs` 目錄包含應用程式的日誌檔。

目錄 `storage/app/public` 常用來儲存使用者上傳的檔案，例如個人資料的頭像這些可以公開存取的檔案。你應該在 `public/storage` 建立一個象徵性的連結並導向 `storage/app/public` 目錄。你可以使用 Artisan 指令 `php artisan storage:link` 來建立連結。

<a name="the-tests-directory"></a>
#### Tests 目錄

目錄 `tests` 包含了你的自動化測試。例如 [ PHPUnit ](https://phpunit.de/) 現成的單元測試（unit test）和功能測試（feature test）。每一個測試類別都需要新增 `Test` 字首。你可以使用 `phpunit` 和 `php vendor/bin/phpunit` 指令執行測試。又或者你想要更多詳細且漂亮地顯示測試結果，你可以使用 Artisan 指令 `php artisan test` 執行測試。

<a name="the-vendor-directory"></a>
#### Vendor 目錄

`vendor` 目錄包含了你的 [ Composer ](https://getcomposer.org) 依賴模組。

<a name="the-app-directory"></a>
## App 目錄

你的應用程式大部分都儲存在 `app` 目錄。預設情況下，這個目錄使用命名空間（namespace）`App` 且藉由 Composer 的 [PSR-4 自動載入標準](https://www.php-fig.org/psr/psr-4/) 被自動載入。

目錄 `app` 包含各種額外資料夾例如 `Console`, `Http` 和 `Providers`。將 `Console` 和 `Http` 目錄試想成作為進入應用程式核心所提供的 API。HTTP 協定和 CLI 都是跟應用程式互動的機制，但實際上沒有包含應用程式的邏輯。換句話說，它們是兩種對應用程式發出指令的方法。目錄 `Comsole` 包含了所有的 Artisan 指令，而目錄 `Http` 包含控制器（controller）、中介層（middleware）和請求（request）。

當你使用 Artisan 指令 `make` 產生類別（class）的時候，其他的目錄才會被建立到目錄 `app` 下。例如執行 Artisan 指令 `make:job` 產生任務類別（job class）時，`app/Jobs` 才會出現在目錄中。

> **Note**  
> 目錄 `app` 下的許多類別都可以透過 Artisan 指令產生。要檢視所有可用的指令可以在終端機（terminal）執行指令 `php artisan list make`。

<a name="the-broadcasting-directory"></a>
#### Broadcasting 目錄

目錄 `Broadcasting` 包含了所有的廣播頻道類別（ broadcast channel class）。這些類別可以使用指令 `make:channel` 產生。這個目錄預設並不存在，但會在你建立第一個頻道時出現。想了解更多關於頻道的資訊，可以查閱文件 [ 廣播事件（event broadcast） ](/docs/{{version}}/broadcasting)。

<a name="the-console-directory"></a>
#### Console 目錄

`Console` 目錄包含應用程式所有自定義的 Artisan 指令。這些指令透過 `make:command` 產生。這個目錄同時儲存已註冊的 Artisan 指令和已定義的 [ 任務排程（scheduled tasks） ](/docs/{{version}}/scheduling) 的終端（console）核心。

<a name="the-events-directory"></a>
#### Events 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令 `event:generate` 或 `make:event` 而被建立。目錄 `Events` 儲存著 [ 事件類別（event classes）](/docs/{{version}}/events)。事件常被用於當指定動作發生時，為提醒應用程式的其它部分提供了很棒的靈活性及解耦。

<a name="the-exceptions-directory"></a>
#### Exceptions 目錄

目錄 `Exceptions` 包含應用程式的異常處理程序且也是放置應用程式拋出例外（throw exception）的好地方。如果你想要自定義如何記錄或呈現異常的方法，你應該修改此目錄中的 `Handler` 類別（class）。

<a name="the-http-directory"></a>
#### Http 目錄

`Http` 目錄包含了你的控制器（controller）、中介層（middleware）和表單（form）請求（request）。幾乎所有進入應用程式的請求處理都會放置在這個目錄。

<a name="the-jobs-directory"></a>
#### Jobs 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令 `make:job` 而被建立。目錄 `Jobs` 儲存著應用程式的 [ 佇列任務（queueable job）](/docs/{{version}}/queues)。應用程式中的任務可以被佇列化，也可以在當前請求生命週期內同步執行。同步執行的任務有時也被看作「指令」，因為它們實現了 [ 指令模式 ](https://en.wikipedia.org/wiki/Command_pattern)。

<a name="the-listeners-directory"></a>
#### Listeners 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令 `event:generate` 或 `make:listener` 而被建立。目錄 `Listeners` 包含了處理 [ 事件（event） ](/docs/{{version}}/events) 的類別。事件監聽器（listener）接收了一個事件執行個體（instance）並回應（response）執行邏輯到被觸發的事件。舉個例子，一個 `UserRegistered` 事件可能會由 `SendWelcomeEmail` 監聽器處理。

<a name="the-mail-directory"></a>
#### Mail 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令（command）`make:mail` 而被建立。目錄 `Mail` 包含應用程式發送的 [ 代表電子郵件的類別 ](/docs/{{version}}/mail)，郵件對象允許你將建立郵件的所有邏輯封裝在一個簡單的類別中，該類別可能使用 `Mail::send` 方法寄信。

<a name="the-models-directory"></a>
#### Models 目錄

目錄 `Models` 包含了你所有的  [ Eloquent model classes ](/docs/{{version}}/eloquent)。Laravel 中包含的 Eloquent ORM 提供了一個漂亮、簡單的主動紀錄實作（ActiveRecord implementation）來處理你的資料庫。每個資料表（table）都有一個對應的「模型（model）」用來與資料表進行互動。模型允許你查詢表中的資料，也可以插入新的紀錄。

<a name="the-notifications-directory"></a>
#### Notifications 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令（command） `make:notification` 而被建立。目錄 `Notifications` 包含由應用程式發送的所有「業務性」 [ 通知 ](/docs/{{version}}/notifications)，例如應用程式發生事件的簡易通知。Laravel 的通知特性會將透過驅動程式發送的通知例如電子郵件、Slack、簡訊或資料儲存抽象化。 

<a name="the-policies-directory"></a>
#### Policies 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令（command）`make:policy` 而被建立。目錄 `Policies` 包含應用程式的 [ 授權原則類別（authorization policy class）](/docs/{{version}}/authorization)。這個類別用於判斷某個使用者是否可以對資源進行給定的操作行為。

<a name="the-providers-directory"></a>
#### Providers 目錄

目錄 `Providers` 包含了應用程式所有的 [ 服務提供者（service providers） ](/docs/{{version}}/providers)。服務提供者啟動應用程式時在服務容器綁定服務、註冊事件或準備執行應用程式的其他傳入請求。

在一個新的 Laravel 應用程式，該目錄已經包含數個提供者。你可以根據需要自行新增服務提供者到該目錄。

<a name="the-rules-directory"></a>
#### Rules 目錄

這個目錄預設並不存在，但會因為你執行 Artisan 指令（command）`make:rule` 而被建立。目錄 `Rules` 包含應用程式自定義的驗證規則（validation rule）。這些規則用於將複雜的驗證邏輯（validation logic）封裝在一個簡單的物件中。關於更多資訊，可以查看 [ 驗證文件 ](/docs/{{version}}/validation)。
