# 目錄結構

- [簡介](#introduction)
- [根目錄](#the-root-directory)
    - [`app` 目錄](#the-root-app-directory)
    - [`bootstrap` 目錄](#the-bootstrap-directory)
    - [`config` 目錄](#the-config-directory)
    - [`database` 目錄](#the-database-directory)
    - [`public` 目錄](#the-public-directory)
    - [`resources` 目錄](#the-resources-directory)
    - [`routes` 目錄](#the-routes-directory)
    - [`storage` 目錄](#the-storage-directory)
    - [`tests` 目錄](#the-tests-directory)
    - [`vendor` 目錄](#the-vendor-directory)
- [App 目錄](#the-app-directory)
    - [`Console` 目錄](#the-console-directory)
    - [`Events` 目錄](#the-events-directory)
    - [`Exceptions` 目錄](#the-exceptions-directory)
    - [`Http` 目錄](#the-http-directory)
    - [`Jobs` 目錄](#the-jobs-directory)
    - [`Listeners` 目錄](#the-listeners-directory)
    - [`Mail` 目錄](#the-mail-directory)
    - [`Notifications` 目錄](#the-notifications-directory)
    - [`Policies` 目錄](#the-policies-directory)
    - [`Providers` 目錄](#the-providers-directory)

<a name="introduction"></a>
## 簡介

預設的 Laravel 應用程式結構旨在提供一個好的起始點給不同大小的應用程式。當然，你可以依照喜好自由地組織應用程式。Laravel 幾乎沒有強加限制任何類別的放置位置 - 只要 Composer 可以自動載入這些類別即可。

#### 為何沒有 Models 目錄？

許多初學者都會困惑 Laravel 為什麼沒有 `models` 目錄，這是有意而為之的。因為「models」這個詞對不同人而言有不同的含義，容易造成歧義，有些開發者認為應用的模型指的是業務邏輯，另外一些人則認為模型指的是與資料庫的互動。

正是因為如此，我們預設將 Eloquent 的模型放置到 `app` 目錄下，從而允許開發者自行選擇放置的位置。

<a name="the-root-directory"></a>
## 根目錄

<a name="the-root-app-directory"></a>
#### App 目錄

如你所料，目錄 `app` 包含應用程式的核心程式碼，我們很快地深入探討這個目錄的細節；然而，你的應用程式的大部分類別將會放置在這個目錄之中。

<a name="the-bootstrap-directory"></a>
#### Bootstrap 目錄

`bootstrap` 目錄包含的檔案用來啟動框架和設定自動載入；以及包含一個 `cache` 資料夾，其中內有框架對效能最佳化所產生的檔案，例如 route 和 services 的快取檔案。

<a name="the-config-directory"></a>
#### Config 目錄

顧名思義，config 目錄包含所有應用程式的配置檔案。熟悉並且熟讀所有這些設定檔案中的選項，對你而言會是個好主意。

<a name="the-database-directory"></a>
#### Database 目錄

`database` 目錄包含資料庫遷移與資料填充檔案。如果你願意的話，你也可以在此資料夾存放 SQLite 資料庫。

<a name="the-public-directory"></a>
#### Public 目錄

`public` 目錄存放著 `index.php` 檔案，此檔案為應用程式的 HTTP 請求入口點。此目錄還包含了前端資源檔，如圖片、JavaScript 和 CSS。

<a name="the-resources-directory"></a>
#### Resources 目錄

resources 目錄包含你的視圖、原始的資源檔 (LESS、SASS、CoffeeScript) ，以及語言檔。

<a name="the-routes-directory"></a>
#### Routes 目錄

`routes` 目錄包含了應用的所有路由定義。Laravel 預設提供了三個路由檔案：`web.php`、`api.php` 和 `console.php`。

`web.php` 檔案裡定義的路由都會在 `RouteServiceProvider` 中被指配到 web 中介層群組，具備 Session、CSRF 防護以及 Cookie 加密功能，如果應用程式無需提供無狀態的、RESTful 風格的 API，則所有的路由都會定義在 `web.php` 檔案中。

`api.php` 檔案裡定義的路由都會在 `RouteServiceProvider` 中被指配到 api 中介層群組，具備頻率限制功能，這些路由是無狀態的，所以經由這些路由進入應用程式需要 token 進行認證，並且不能訪問 Session 狀態。

`console.php` 檔案用於定義所有基於閉包的控制台指令，每個閉包都被繫結到一個控制台指令並且允許與指令列 IO 方法進行互動，儘管這個檔案並不定義 HTTP 路由，但是它定義了基於指令列的應用程式入口（路由）。

<a name="the-storage-directory"></a>
#### Storage 目錄

`storage` 目錄包含編譯後的 Blade 模板、基於檔案的 session、檔案快取和其它框架生成的檔案。底下資料夾分隔成 `app`、`framework`，及 `logs` 目錄。`app` 目錄可用於儲存應用程式使用的任何檔案。`framework` 目錄被用於儲存框架生成的檔案及快取。最後，`logs` 目錄包含了應用程式的日誌檔案。

`storage/app/public` 可以用來存放使用者上傳檔案（例如個人大頭照）。為了能公開訪問，需要建立 `public/storage` 連結（symbolic link），然後指到 storage/app/public 這個資料夾，你可以使用 `php artisan storage:link` 來建立連結。

<a name="the-tests-directory"></a>
#### Tests 目錄

`tests` 目錄包含自動化測試。並提供一個現成的 [PHPUnit](https://phpunit.de/) 範例。每一個測試類都需要新增 `Test` 字首，你可以使用 `phpunit` 或者 `php vendor/bin/phpunit` 指令來執行測試。

<a name="the-vendor-directory"></a>
#### Vendor 目錄

`vendor` 目錄包含你的 [Composer](https://getcomposer.org) 依賴模組。

<a name="the-app-directory"></a>
## App 目錄

大部分你撰寫的應用程式會存放於 `app` 目錄中。預設情況下，這個目錄使用命名空間 `App` 並藉由 Composer 自動載入（採用 [PSR-4 自動載入標準](http://www.php-fig.org/psr/psr-4/)）。

`app` 目錄附帶許多個額外的目錄，例如：`Console`、`Http` 和 `Providers`。可以將 `Console` 和 `Http` 目錄試想為提供 API 進入應用程式的核心。HTTP 協定和 CLI 都是跟應用程式進行互動的機制，但實際上並不包含應用程式邏輯。換句話說，它們是兩種簡單地釋出指令給應用程式的方法。`Console` 目錄包含你全部的 Artisan 指令，而 `Http` 目錄包含你的控制器、中介層和請求。

當你使用 Artisan 指令 `make` 產生類別的時候，其他的目錄才會被建立到 `app` 目錄下。例如執行 `make:job` 指令產生任務類別時，`app/Jobs` 目錄才會出現在目錄中。

> {tip} 在 `app` 目錄中的很多類別都可以透過 Artisan 指令產生，要檢視所有有效的指令，可以在終端機中執行 `php artisan list make` 指令。

<a name="the-console-directory"></a>
#### Console 目錄

`Console` 目錄包含應用程式所有自定義的 Artisan 指令，這些指令類別可以使用 `make:command` 指令產生。該目錄中有你的控制台核心（註冊自定義的 Artisan 指令）和已定義的[排程任務](/docs/{{version}}/scheduling)。

<a name="the-events-directory"></a>
#### Events 目錄

Events 目錄預設不存在，會在你使用 `event:generate` 或 `make:event` 指令以後才會被建立。如你所料，此 `Events` 目錄是用來放置[事件類別](/docs/{{version}}/events)的。事件可以被用於當指定動作發生時，通知你應用程式的其它部分，提供了很棒的靈活性及解耦。

<a name="the-exceptions-directory"></a>
#### Exceptions 目錄

`Exceptions` 目錄包含應用程式的異常處理程序，同時也是個處置應用程式丟擲異常的好位置。如果你想自定義異常的記錄和渲染，你應該修改此目錄下的 `Handler` 類別。

<a name="the-http-directory"></a>
#### Http 目錄

`Http` 目錄包含了控制器、中介層以及表單請求等，幾乎所有進入應用程式的請求處理都放在這裡。

<a name="the-jobs-directory"></a>
#### Jobs 目錄

該目錄預設不存在，可以通過執行 `make:job` 指令建立，`Jobs` 目錄用於存放[佇列任務](/docs/{{version}}/queues)，應用程式中的任務可以被佇列化，也可以在當前請求生命週期內同步執行。同步執行的任務有時也被看作指令，因為它們實現了[命令模式](https://en.wikipedia.org/wiki/Command_pattern)。

<a name="the-listeners-directory"></a>
#### Listeners 目錄

這個目錄預設不存在，可以通過執行 `event:generate` 和 `make:listener` 指令建立。`Listeners` 目錄包含處理[事件](/docs/{{version}}/events)的類別（事件監聽器），事件監聽器接收一個事件並提供對該事件發生後的響應邏輯，例如，`UserRegistered` 事件可以被 `SendWelcomeEmail` 監聽器處理。

<a name="the-mail-directory"></a>
#### Mail 目錄

這個目錄預設不存在，但是可以通過執行 `make:mail` 指令產生，`Mail` 目錄包含郵件傳送類別，郵件物件允許你在一個地方封裝構建郵件所需的所有業務邏輯，然後使用 `Mail::send` 方法傳送郵件。

<a name="the-notifications-directory"></a>
#### Notifications 目錄

這個目錄預設不存在，你可以通過執行 `make:notification` 指令建立， `Notifications` 目錄包含應用程式傳送的所有通知，比如事件發生通知。Laravel 的通知功能將傳送和驅動方式解耦，你可以透過郵件，也可以透過 Slack、簡訊或者資料庫傳送通知。

<a name="the-policies-directory"></a>
#### Policies 目錄

這個目錄預設不存在，你可以通過執行 `make:policy` 指令來建立， `Policies` 目錄包含了所有的授權策略類別，策略用於判斷某個使用者是否有許可權去訪問指定資源。更多詳情，請檢視[授權文件](/docs/{{version}}/authorization)。

<a name="the-providers-directory"></a>
#### Providers 目錄

`Providers` 目錄包含應用的[服務提供者](/docs/{{version}}/providers)。服務提供者在啟動應用過程中繫結服務到容器、註冊事件，以及執行其他任務，為即將到來的請求處理做準備。

在新安裝的 Laravel 應用中，該目錄已經包含了一些服務提供者，你可以按需新增自己的服務提供者到該目錄。
