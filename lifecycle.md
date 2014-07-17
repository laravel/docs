# Request 生命週期

- [概覽](#overview)
- [Request 生命週期](#request-lifecycle)
- [啟動文件](#start-files)
- [應用程式事件](#application-events)

<a name="overview"></a>
## 概覽

在“真實世界”裡使用任何工具，只要你了解該工具的運作原理，你將會很順手。應用程式開發上也是相同的。當你了解開發工具的功能，你使用上會更得心應手。而這份文件的目的就是要給予你一個優良、高層次的Laravel 框架運作概覽。隨著了解整個框架越多，你就不會覺得很"奇妙"且更容易去建構你的應用程式。除了關於 request 生命週期的高層次概覽外，我們也會介紹”啟動“檔案和應用程式事件。

如果你對許多東西不明白，不用擔心。只要了解個基本的原理，隨著探索其他文件，你將會得到更多的知識。

<a name="request-lifecycle"></a>
## 請求的生命週期

對你的應用程式的所有請求，都會被導到 `public/index.php` 程式去。如果使用 Apache，Laravel 的 `.htaccess` 會將所有的請求都讓 `index.php` 來做處理。從這裡開始，Laravel 就會進行處理請求跟回應給客戶端的流程。了解 Laravel 引導過程的總體思路是有幫助的。

至此，了解 Laravel 的引導過程一個要把握的最重要概念就是**服務提供商**。你可以在你的 `app/config/app.php` 設定中找到 `providers` 的陣列，條列出所有的服務提供商。這些提供商作為 Laravel 的主要引導機制。但在深入探討服務提供商之前，我們先回到 `index.php`。在一個請求進入到你的 `index.php` 後，`bootstrap/start.php` 檔案將接著被載入。這檔案創建一個新的 Laravel `Application` 物件，並也作為一個[IoC 容器](/docs/ioc)。

在創建 `Application` 物件之後，少部分的物件路徑將被設定且進行[偵測運行環境](/docs/configuration#environment-configuration)。然後，一個內部的 Laravel 引導腳本將會被呼叫。這個檔案深藏在 Laravel 的程式碼中，並且依據你的設定檔做一些相關設定，如：時區、錯誤回報等等。但除了這些設定與瑣碎的配置選項外，他也做一些比較重要的事情：註冊所有你應用程式中設定的服務提供商。

比較簡單的服務提供商僅含有一個方法：`register`。此方法用於應用程式物件註冊服務提供商時，應用程式會透過所屬的 `register` 方法來呼叫服務提供商的 `register` 方法。此方法中，服務提供商註冊[IoC 容器](/docs/ioc)。本質上來說，每個服務提供商會綁定一個以上容器中的[封包](http://us3.php.net/manual/en/functions.anonymous.php)，讓你可以在應用程式中存取這些綁定服務。所以例如，`QueueServiceProvider` 註冊封包來處理多個[對列](/docs/queues)相關類別。當然，服務提供商註冊可以被使用在任何引導任務上，不只是註冊在容器中的事情。服務提供商亦可以註冊事件監聽器，view composers, artisan 命令等等。

在所有的事件提供者都被註冊後，你的 `app/start` 檔案將會被載入。最後，你的 `app/routes.php` 檔案才會被載入。一旦你的 `routes.php` 檔案被載入後，請求物件將會被送至應用程式中，如此他才能被指派至其中一個路由。

好，讓我們來總結一下：

1. 請求進入 `public/index.php` 檔案中。
2. `bootstrap/start.php` 檔案創建應用程式和偵測運行環境。
3. 內部 `framework/start.php` 檔案配置設定和載入服務提供商。
4. 應用程式 `app/start` 檔案被載入。
5. 應用程式 `app/routes.php` 檔案被載入。
6. 請求物件傳入應用程式中，回傳回應物件。
7. 回應物件回傳客戶端。

現在你對於 Laravel 如何處理一個請求有個比較好的了解，讓我們更近些了解 "起始檔案"！

<a name="start-files"></a>
## 起始檔案

你的應用程式的起始檔案被儲存在 `app/start` 目錄下。預設下，三個檔案被包含在你的應用程式中：`global.php`, `local.php` 和 `artisan.php`。關於 `artisan.php` 更多的資訊可以參考 [Artisan 命令列](/docs/commands#registering-commands)文件。

`global.php` 起始檔預設包含了一些基本項目，如 [日誌](/docs/errors)的註冊和包含你的 `app/filters.php` 檔案。然而，你可以自由添加任何你想添加的東西至此。不管何種運行環境，他都會自動被包含進去在每個_請求_裡。另一方面，`local.php` 檔僅會在 `local` 環境下才會被執行。更多關於運行環境的資訊，請參照 [設定](/docs/configuration)文件。

當然，除了 `local` 外你還有其他的運行環境，你一樣可以為這些運行環境創建起始檔案。當應用程式運行在該運行環境時將會自動載入對應檔案。所以例如，如果你在 `bootstrap/environment.php` 中設定了一個 `development` 運行環境，你可以創建 `app/start/development.php` 檔案，當應用程式在該運行環境中接收請求時會自動載入該檔案。

### 起始檔案中要放什麼

起始檔案作為一個簡單的地方來放置任何“引導程序”。例如，你可以註冊一個 View composer，配置你的日誌喜好或是一些 PHP 設置等等。完全取決與你。當然，把你的所有的引導程式碼都丟在起始檔中也會造成混亂，建議將一些引導程式碼放置到[服務提供商](/docs/ioc#service-providers)中。

<a name="application-events"></a>
## 應用程式事件

#### 註冊應用程式事件

你可以註冊 `before`, `after`, `finish` 和 `shutdown` 應用程式事件，來對請求前或請求後做處理：

	App::before(function($request)
	{
		//
	});

	App::after(function($request, $response)
	{
		//
	});

監聽器將會對你的應用程式在每次請求執行 `before` 和 `after` 函式。這些事件對於全域篩選或是全域修改回應上很有幫助。你可以將他們註冊在你的其中一個“起始檔”中或者是[服務提供商](/docs/ioc#service-providers)中。

你也可以註冊一個監聽器在"匹配"的事件上，當傳入的請求以備匹配到一個路由，但該路由尚未被執行的情況下，該事件將會被觸發：

	Route::matched(function($route, $request)
	{
		//
	});

`finish` 事件在你的應用程式回應給客戶端之後會被呼叫。這是非常好的一個地方去放置你應用程最後要做的事項。`shutdown` 是在所有 `finish` 事件處理器都結束之後立即被呼叫，他也是最後一個在程式終結前最後可以做些什麼的機會。最有可能狀況下，你可以能不需要用到任何一個事件。