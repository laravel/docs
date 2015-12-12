# 應用程式結構

- [簡介](#introduction)
- [根目錄](#the-root-directory)
- [App 目錄](#the-app-directory)
- [為應用程式設定命名空間](#namespacing-your-application)

<a name="introduction"></a>
## 簡介

預設的 Laravel 應用程式結構意在提供一個好的起始點給不同大小的應用程式。當然，你可以依照喜好自由地組織應用程式。Laravel 幾乎沒有強加限制任何類別的放置位置 - 只要 Composer 可以自動載入這些類別即可。

<a name="the-root-directory"></a>
## 根目錄

一個新安裝的 Laravel 根目錄包含許多個資料夾：

`app` 目錄，如你所料，包含應用程式的核心程式碼。我們之後將會很快深入探討這個目錄的細節。

`bootstrap` 目錄包含幾個框架啟動跟自動載入設定的檔案。以及 `cache` 資料夾，包含一些框架對啟動效能最佳化所產生的檔案。

`config` 目錄，顧名思義，包含所有應用程式的設定檔。

`database` 目錄包含你的資料庫遷移與資料填充檔案。如果你希望，你也可以在此資料夾存放 SQLite 資料庫。

`public` 目錄包含前面的控制器和你的資源檔（圖片、JavaScript、CSS，等等）。

`resources` 目錄包含你的視圖、原始的資源檔 (LESS、SASS、CoffeeScript) ，以及語言檔。

storage 目錄包含編譯後的 Blade 模板、基於檔案的 session、檔案快取和其他框架產生的檔案。此資料夾分格成 `app`、`framework`，及 `logs` 目錄。`app` 目錄可用於存儲應用程式使用的任何檔案。`framework` 目錄被用於儲存框架產生的檔案及快取。最後，`logs` 目錄包含了應用程式的日誌檔案。

tests 目錄包含你的自動化測試。包含一個現成的[PHPUnit](https://phpunit.de/)範例。

vendor 目錄包含你的 [Composer](https://getcomposer.org) 依賴模組。

<a name="the-app-directory"></a>
## App 目錄

應用程式的「內容」存在於 `app` 目錄中。預設情況下，這個目錄在 `App` 命名空間下並藉由 Composer 使用 [PSR-4 自動載入標準](http://www.php-fig.org/psr/psr-4/)自動載入。**你可以使用 `app:name` Artisan 指令變更這個命名空間**。

`app` 目錄附帶許多個額外的目錄，例如：`Console`、`Http` 和 `Providers`。試想 `Console` 和 `Http` 目錄作為提供 API 進入應用程式的「核心」。HTTP 協定和 CLI 都是跟應用程式互動的機制，但實際上並不包含應用程式邏輯。換句話說，它們是兩種簡單地發布命令給應用程式的方法。`Console` 目錄包含你全部的 Artisan 指令，而 `Http` 目錄包含你的控制器、中介層和請求。

`Jobs` 目錄，當然，用於放置應用程式[可隊列的任務](/docs/{{version}}/queues)。任務可能被應用程式放到隊列中，以及可以在當前請求生命週期內同步執行。

`Events` 目錄，如你所料，是用來放置[事件類別](/docs/{{version}}/events)。事件可以被用於當指定的動作發生時，通知你應用程式的其他部分，提供很大的靈活性及減少耦合。

`Listeners` 目錄包含事件的處理類別。處理程序接收一個事件，並針對該事件執行邏輯。例如，`UserRegistered` 事件可能由 `SendWelcomeEmail` 監聽器處理。

`Exceptions` 目錄包含應用程式的例外處理程序，也是個處置應用程式拋出的任何例外的好位置。

> **注意：**在 `app` 目錄中的許多類別可以透過 Artisan 指令產生。若要查看可以使用的指令，只要在終端機執行 `php artisan list make` 命令。

<a name="namespacing-your-application"></a>
## 為應用程式設定命名空間

如前面所提到的，預設的應用程式命名空間為 `App`；然而，你可以簡單地藉由 `app:name` Artisan 指令，將此命名空間變更成應用程式的名稱。例如：如果你的應用程式叫做「SocialNet」，你將會執行下方的指令：

    php artisan app:name SocialNet

當然，你可以自由且簡單的使用 `App` 命名空間。
