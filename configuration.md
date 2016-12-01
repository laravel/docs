# 設定

- [簡介](#introduction)
- [存取設定值](#accessing-configuration-values)
- [環境設定](#environment-configuration)
    - [判斷當前環境](#determining-the-current-environment)
- [設定快取](#configuration-caching)
- [維護模式](#maintenance-mode)

<a name="introduction"></a>
## 簡介

Laravel 框架的所有設定都存放於 `config` 目錄中。每個選項都有文件，你可以隨意瀏覽這些檔案，並熟悉這些可用的選項。

<a name="accessing-configuration-values"></a>
## 存取設定值

你可以在應用程式的任何位置輕鬆的使用全域的 `config` 輔助函式來存取你的設定值。設定值可以透過「點」語法來取得，其中包含了你想存取的檔案與選項的名稱。也可以指定預設值，當該設定選項不存在時就會回傳預設值：

    $value = config('app.timezone');

若要在執行期間修改設定值，請傳遞一個陣列至 `config` 輔助方法：

    config(['app.timezone' => 'Asia/Taipei']);

<a name="environment-configuration"></a>
## 環境設定

基於應用程式的執行環境，採用不同的設定值，通常是很有幫助的。例如你可能會希望在本機開發環境上使用與正式環境不同的快取驅動。

為了做到這件事，Laravel 透過 Vance Lucas 的 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 函式庫來達到這項需求。在全新安裝好的 Laravel 裡，應用程式的根目錄下會包含一個 `.env.example` 檔案，你應該手動更改它的檔名為 `.env`。如果透過 Composer 安裝 Laravel，則這個檔案將自動被更名為 `.env`。

> {tip} 你也可以建立一個設定檔 `.env.testing`。當執行 PHPUnit 測試的時候，或是當執行 Artisan 指令的時候加上參數 `--env=testing`，這個檔案就會被用來取代 `.env` 設定檔。

#### 取得當前環境

當你的應用程式收到請求時，這個程式中所有的變數都會被載入到 PHP 超級全域變數 `$_ENV` 裡。然而，你可以使用 `env` 輔助方法來從設定檔中取得這些變數的值。事實上，如果你檢閱過 Laravel 的設定檔案，你會注意到有幾個選項已經在使用這個輔助方法：

    'debug' => env('APP_DEBUG', false),

傳遞至 `env` 函式的第二個參數為「預設值」。當給定的鍵沒有環境變數存在時就會使用該值。

你的 `.env` 檔案不應該被提交到應用程式的版本控制系統，因為使用此應用程式的每個開發人員或伺服器可能需要不同的環境設定。

如果你與團隊協同開發，不妨將`.env.example` 檔案放進你的應用程式。透過範例設定檔裡的預留值，其他的團隊開發者可以清楚地看到，執行應用程式時，有哪些環境變數是必須的。

<a name="determining-the-current-environment"></a>
### 判斷當前環境

應用程式的當前環境是由 `.env` 檔案中的 `APP_ENV` 變數所決定。你可以透過 `App` [facade](/docs/{{version}}/facades) 的 `environment` 方法取得該值：

    $environment = App::environment();

你也可以傳遞參數至 `environment` 方法中，來確認目前的環境是否與給定參數相符合。如果環境符合任何一個給定的值，該方法就會回傳 `true`：

    if (App::environment('local')) {
        // 應用程式的當前環境為 local
    }

    if (App::environment('local', 'staging')) {
        // 應用程式的當前環境為 local 或 staging...
    }

<a name="configuration-caching"></a>
## 設定快取

為了讓應用程式提升一些速度，你可以使用 `config:cache` Artisan 指令將所有的設定檔存到單一檔案。它會將所有的設定選項合併成一個檔案，讓框架能夠快速載入。

你通常應該將執行 `php artisan config:cache` 指令作為上線部署的例行公事。在你開發應用程式時，此指令則不應該執行，因為設定選項會因開發需要而經常地變動。

<a name="maintenance-mode"></a>
## 維護模式

當你的應用程式處於維護模式時，所有傳遞至應用程式的請求都會變成顯示自定視圖。在你要更新或進行維護作業時，這麼做可以很輕鬆的「關閉」整個應用程式。應用程式的預設中介層堆疊會核對是否處於維護模式。如果應用程式處於維護模式，會拋出 `MaintenanceModeException` 並附帶 503 的狀態碼。

若要啟用維護模式，只需要執行 `down` Artisan 指令：

    php artisan down

可以提供 `message` 和 `retry` 選項給 `down` 指令。 `message` 選項的值用來顯示或紀錄客製化訊息，`retry` 選項的值用來當作 HTTP 標頭 `Retry-After` 的值：

    php artisan down --message="Upgrading Database" --retry=60

若要關閉維護模式，請使用 `up` 指令：

    php artisan up

#### 維護模式的回應模板

維護模式回應的預設模板放置在 `resources/views/errors/503.blade.php`。你可以自由的根據應用程式需求修改該視圖。

#### 維護模式與隊列

當應用程式處於維護模式中，將不會處理任何 [隊列任務](/docs/{{version}}/queues) 。所有的任務將會在應用程式離開維護模式後繼續被進行。

#### 維護模式以外的選擇

因為維護模式需要讓你的應用程式有幾秒鐘的停機時間，你可以考慮像是 [Envoyer](https://envoyer.io) 的替代方案，以做到 Laravel 的零停機時間部署。
