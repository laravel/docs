# 安裝

- [安裝](#installation)
- [設定](#configuration)
    - [基本設定](#basic-configuration)
    - [環境設定](#environment-configuration)
    - [設定快取](#configuration-caching)
    - [取得設定值](#accessing-configuration-values)
    - [命名你的應用程式](#naming-your-application)
- [維護模式](#maintenance-mode)

<a name="installation"></a>
## 安裝

### 伺服器需求

Laravel 框架有一些系統上的需求。當然，[Laravel Homestead](/docs/{{version}}/homestead) 虛擬機器都能滿足這些需求：

<div class="content-list" markdown="1">
- PHP >= 5.5.9
- OpenSSL PHP Extension
- PDO PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension
</div>

<a name="install-laravel"></a>
### 安裝 Laravel

Laravel 使用 [Composer](http://getcomposer.org) 來管理相依性。所以，在使用 Laravel 之前，你必須確認電腦上是否安裝了 Composer。

#### 透過 Laravel 安裝工具

首先，使用 Composer 下載 Laravel 安裝包：

    composer global require "laravel/installer=~1.1"

請確定把 `~/.composer/vendor/bin` 路徑放置於你的 PATH 裡，這樣你的系統才能找到 `laravel` 執行檔。

一旦安裝完成後，就可以使用 `laravel new` 指令在指定的目錄建立一份新安裝的 Laravel 專案，例如：`laravel new blog` 將會在當前目錄下建立一個叫 `blog` 的目錄，此目錄裡面存放著新安裝的 Laravel 和相依程式碼。這個安裝方法比透過 Composer 安裝速度快上許多：

    laravel new blog

#### 透過 Composer Create-Project

你也可以透過 Composer 在命令列執行 `create-project` 指令來安裝 Laravel：

    composer create-project laravel/laravel --prefer-dist

<a name="configuration"></a>
## 設定

<a name="basic-configuration"></a>
### 基本設定

所有 Laravel 框架的設定檔案都放置在 `config` 目錄下。每個選項都有說明，因此你可以輕鬆地瀏覽這些文件，並且熟悉這些選項配置。

#### 目錄權限

安裝 Laravel 之後，你必須設定一些權限。`storage` 和 `bootstrap/cache` 目錄必須讓伺服器有寫入權限。如果你使用 [Homestead](/docs/{{version}}/homestead) 虛擬機器，那麼這些權限應該已經被設定完成。

#### 應用程式金鑰

在你安裝完 Laravel 後，首先需要做的事情是設定一個隨機字串到應用程式金鑰。假設你是透過 Composer 或是 Laravel 安裝工具安裝 Laravel，那麼這個金鑰已經透過 `key:generate` 指令幫你設定完成。通常這個金鑰應該有 32 字元長。這個金鑰可以被設定在 `.env` 環境檔案中。如果你還沒將 `.env.example` 檔案重新命名為 `.env`，那麼你應該現在開始。**如果應用程式金鑰沒有被設定的話，你的使用者 Sessions 和其他的加密資料都是不安全的！**

#### 其他設定

Laravel 幾乎不需設定就可以馬上使用，你可以自由的開始開發！當然，你可以瀏覽 `config/app.php` 檔案和對應的文件。它包含數個選項，如`時區`和`語言環境`，你不仿根據你的應用程式來做修改。

你也可以設定 Laravel 的幾個附加元件，像是：

- [快取](/docs/{{version}}/cache#configuration)
- [資料庫](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)

一旦 Laravel 安裝完成，你應該同時[設定本機環境](/docs/{{version}}/installation#environment-configuration)。

<a name="pretty-urls"></a>
#### 優雅鏈結

**Apache**

Laravel 框架透過 `public/.htaccess` 檔案來讓網址中不需要 `index.php`。如果你的伺服器是使用 Apache，請確認是否有開啟 `mod_rewrite` 模組。

假設 Laravel 附帶的 `.htaccess` 檔在 Apache 無法作用的話，請嘗試下方的做法：

    Options +FollowSymLinks
    RewriteEngine On

    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^ index.php [L]

**Nginx**

若使用 Nginx ，可以在你的網站設定中增加下面的設定，以開啟「優雅連結」：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

當然，如果你使用 [Homestead](/docs/{{version}}/homestead) 的話，優雅鏈結會自動的幫你設定完成。

<a name="environment-configuration"></a>
### 環境設定

通常應用程式常常需要根據不同的執行環境而有不同的設定值。例如，你會希望在你的本機開發環境上會有與正式環境不同的暫存驅動。只要透過設定檔案，就可以輕鬆完成。

Laravel 透過 Vance Lucas 的 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 函式庫來達到這項需求。在全新安裝好的 Laravel 裡，你的應用程式的根目錄下會包含一個 `.env.example` 檔案。如果你透過 Composer 安裝 Laravel，這個檔案將自動被更名為 `.env`，不然你應該手動更改檔名。

當你的應用程式收到請求時，這個檔案所有的變數會被載入到 PHP 超級全域變數 `$_ENV` 裡。你可以使用輔助方法 `env` 來取得這些變數的值。事實上，如果你檢閱過 Laravel 的設定檔案，你會注意到有幾個選項已經在使用這個輔助方法！

根據你的本機伺服器或者正式環境需求，你可以自由的修改你的環境變數。但是，你的 `.env` 檔案不應該被提交到應用程式的版本控制系統，因為每個開發人員或伺服器在使用你的應用程式時，可能需要不同的環境設定。

如果你是一個團隊的開發者，不妨將 `.env.example` 檔案放進你的應用程式。透過範例設定檔裡的預留值，你的團隊中其他開發人員可以清楚地看到，在執行你的應用程式時，有哪些環境變數是必須的。

#### 取得目前應用程式的環境

應用程式的當前環境是由 `.env` 檔案中的 `APP_ENV` 變數所決定。你可以透過 `App` [facade](/docs/{{version}}/facades) 的 `environment` 方法取得該值：

    $environment = App::environment();

你也可以傳遞參數至 `environment` 方法中，來確認目前的環境是否與參數相符合：

    if (App::environment('local')) {
        // 環境是 local
    }

    if (App::environment('local', 'staging')) {
        // 環境是 local 或 staging...
    }

也能透過 `app` 輔助方法取得應用程式實例：

    $environment = app()->environment();

<a name="configuration-caching"></a>
### 設定快取

為了讓你的的應用程式提升一些速度，你可以使用 Artisan 指令 `config:cache` 將所有的設定檔暫存到單一檔案。透過指令會將所有的設定選項合併成一個檔案，讓框架能夠快速載入。

你應該將執行 `php artisan config:cache` 指令作為部署工作的一部分。此指令不應該在本機開發的時候執行，因為設定選項需要根據你應用程式的開發而經常變動。

<a name="accessing-configuration-values"></a>
### 取得設定值

你可以很輕鬆的使用 `config` 輔助方法取得你的設定值。設定值可以透過「點」語法來取得，其中包含了檔案與選項的名稱。也可以指定預設值，當該設定選項不存在時就會回傳預設值：

    $value = config('app.timezone');

若要在執行期間修改設定值，請傳遞一個陣列至 `config` 輔助方法：

    config(['app.timezone' => 'America/Chicago']);

<a name="naming-your-application"></a>
### 命名你的應用程式

在安裝完成 Laravel 後，你可以「命名」你的應用程式。預設情況下，`app` 的目錄的命名空間是 `App`，然後會透過 Composer 使用 [PSR-4 自動載入標準](http://www.php-fig.org/psr/psr-4/) 來自動載入。不過，你可以輕鬆地透過 Artisan 指令 `app:name` 來修改命名空間，以配合你的應用程式名稱。

舉例來說，假設你的應用程式叫做「Horsefly」，你可以在安裝完的根目錄執行下方的指令：

    php artisan app:name Horsefly

重新命名你的應用程式是完全自由的，如果你希望的話也可以保持命名空間為 `App`。

<a name="maintenance-mode"></a>
## 維護模式

當你的應用程式處於維護模式時，所有的傳遞至應用程式的請求都會顯示一個自定的視圖。在你要更新或進行維護作業時，這麼做可以很輕鬆的「關閉」整個應用程式。維護模式會檢查包含在應用程式的預設中介層堆疊。如果應用程式處於維護模式，`HttpException` 會拋出 503 的狀態碼。

啟用維護模式，只需要執行 Artisan 指令 `down`：

    php artisan down

關閉維護模式，請使用 Artisan 指令 `up`：

    php artisan up

### 維護模式的回應模板

維護模式回應的預設模板放在 `resources/views/errors/503.blade.php`。

### 維護模式與隊列

當應用程式處於維護模式中，將不會處理任何[隊列工作](/docs/{{version}}/queues)。所有的隊列工作將會在應用程式離開維護模式後繼續被進行。
