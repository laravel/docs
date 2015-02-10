# 應用程式結構

- [介紹](#introduction)
- [根目錄](#the-root-directory)
- [App 目錄](#the-app-directory)
- [為應用程式設定命名空間](#namespacing-your-application)

<a name="introduction"></a>
## 介紹

預設的 Laravel 應用程式結構想要提供一個好的開始給任何大小的應用程式。當然，你可以依照喜好自由地組織應用程式。Laravel 幾乎沒有強加限制任何類別的放置位置 - 只要 Composer 可以自動載入這些類別即可。

<a name="the-root-directory"></a>
## 根目錄

一個新安裝的 Laravel 根目錄包含許多個目錄：

`app` 目錄，如你所料，包含應用程式的核心程式碼。我們之後將會很快深入探討這個目錄的細節。

`bootstrap` 目錄包含幾個框架啟動跟自動載入設定的檔案。

`config` 目錄，顧名思義，包含所有應用程式的設定檔。

`database` 目錄包含你的資料庫遷移與資料填充檔案。

`public` 目錄包含前面的控制器和你的資源檔 (圖片、JavaScript、CSS，等等)。

`resources` 目錄包含你的視圖、原始的資源檔 (LESS、SASS、CoffeeScript) 和「語言」檔。

`storage` 目錄包含編譯後的 Blade 模板、基於檔案的 session、檔案快取和其他框架產生的檔案。

`tests` 目錄包含你的自動化測試。

`vendor` 目錄包含你的 Composer 依賴模組。

<a name="the-app-directory"></a>
## App 目錄

 應用程式的「內容」存在於 `app` 目錄中。預設情況下，這個目錄在 `App` 命名空間下並藉由 Composer 使用 [PSR-4 自動載入標準](http://www.php-fig.org/psr/psr-4/) 自動載入。 **你可以使用 `app:name` Artisan 命令變更這個命名空間**.

`app` 目錄附帶許多個額外的目錄，例如：`Console`、`Http` 和 `Providers`。考慮 `Console` 和 `Http` 目錄用作提供 API 進入應用程式的「核心」。HTTP 協定和 CLI 都是跟應用程式互動的機制，但實際上並不包含應用程式邏輯。換句話說，它們是兩種簡單地發布命令給應用程式的方法。`Console` 目錄包含你全部的 Artisan 命令，而 `Http` 目錄包含你的控制器、過濾器和請求。

`Commands` 目錄當然是用來放置應用程式的命令。命令代表可以被應用程式放到隊列的任務，以及可以在當前請求生命週期內同步運行的任務。

`Events` 目錄，如你所料，是用來放置事件類別。當然，使用類別來代表事件不是必須的；然而，如果你選擇使用它們，這個目錄將會是藉由 Artisan 命令列創建它們時的預設位置。

`Handlers` 目錄包含命令和事件的處理類別。處理程序接收命令或事件，並針對該命令或事件執行邏輯。

`Services` 目錄包含各種「輔助」服務，囊括應用程式需要的功能。例如，Laravel 引入的 `Registrar` 服務負責驗證 並創建應用程式的新使用者。其他的例子可能是服務跟外部 API、評價系統或甚至是跟從你的應用程式匯集資料的服務互動。

`Exceptions` 目錄包含應用程式的例外處理程序，也是個處置應用程式拋出的任何例外的好地方。

> **注意：** 在 `app` 目錄中的許多類別可以用 Artisan 命令產生。要查看可以使用的命令，在終端機執行 `php artisan list make` 命令。

<a name="namespacing-your-application"></a>
## 為應用程式設定命名空間

如前面所提到的，預設的應用程式命名空間為 `App`；然而，你可以變更這個命名空間成跟應用程式的名稱一樣，這可以簡單地藉由 `app:name` Artisan 命令完成。例如：如果你的應用程式叫做「SocialNet」，你將會執行下面的命令：

	php artisan app:name SocialNet
