# 設定

- [簡介](#introduction)
- [完成安裝後](#after-installation)
- [存取設定值](#accessing-configuration-values)
- [環境配置](#environment-configuration)
- [設定快取](#configuration-caching)
- [維護模式](#maintenance-mode)
- [優雅鏈結](#pretty-urls)

<a name="introduction"></a>
## 簡介

所有 Laravel 框架的設定檔案都放置在 `config` 目錄下。 每個選項都有說明，因此你可以輕鬆地瀏覽這些文件，並且熟悉這些選項配置。

<a name="after-installation"></a>
## 完成安裝後

### 命名你的應用程式

在安裝完成 Laravel 後，你可以 "命名" 你的應用程式。 預設情況下，`app` 的目錄是命名在 `App` 下，透過 Composer 使用 [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/) 自動載入。然而，你可以修改命名空間來匹配你的應用程式的名稱，你可以輕鬆地透過 Artisan 指令 `app:name`。

舉例來說，假設你的應用程式叫做 "Horsefly"，你可以從你的安裝的目錄執行下面的指令：

	php artisan app:name Horsefly

重新命名你的應用程式是完全自由的，以及你可以自由保持 `App` 命名空間。

### 其他設定

Laravel 幾乎不需設定就可以馬上使用。你可以自由的開始開發！然而，你可以瀏覽 `config/app.php` 檔案和其他的文件。你可能希望依據你的本機而做更改，檔案包含數個選項如 `時區` 和 `語言環境`。

一旦 Laravel 安裝完成，你應該同時 [設定本地環境](/docs/5.0/configuration#environment-configuration)。

> **注意：** 你不應該在正式環境中將 `app.debug` 設定為 `true`。絕對！千萬不要！

<a name="permissions"></a>
### 權限

Laravel 框架有一個目錄需要額外設置權限：`storage` 要讓網頁伺服器有寫入的權限。

<a name="accessing-configuration-values"></a>
## 存取設定值

你可以很輕鬆的存取你的設定值使用 `Config` facade：

	$value = Config::get('app.timezone');

	Config::set('app.timezone', 'America/Chicago');

你也可以使用 `config` 函數的輔助方法：

	$value = config('app.timezone');

<a name="environment-configuration"></a>
## 環境配置

通常應用程式常常需要根據不同的運行環境而有不同的配置設定值。例如，你會希望在你的本地開發機器上會有與正式環境不同的暫存驅動（cache driver），透過設定檔案，就可以完成。

Laravel 透過 [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas。 在全新安裝好的 Laravel 裡，你的應用程式的根目錄下會包含一個 `.env.example` 檔案。如果你透過 Composer 安裝 Laravel，這個檔案將自動被命名為 `.env`，不然你應該手動更改檔名。

當你的應用程式收到要求，這個檔案所有的變數會被載入到 `$_ENV` PHP 全域裡。你可以使用 `env` 從這些變數中檢索值的輔助。事實上，如果你想要檢閱 Laravel 設定檔案，你會注意到幾個已經在使用輔助方法的選項！

根據你的本地伺服器需求，你可以自由的修改你的環境變數，以及你的作業環境。然而， 你的 `.env` 檔案不應該被提交到你的應用程式源碼控制，由於每個開發人員/伺服器使用你的應用程式可能需要不同的環境設定。

如果你正在開發一個團隊，你不妨可以把 `.env.example` 檔案包含到你的應用程式。透過將範例設定檔的預留值，你的團隊的其他開發人員可以清楚地看到執行你的應用程式所需的哪些環境變數。

#### 存取目前應用程式的環境

你可以存取目前的應用程式環境透過 `environment` 的方法在 `Application` 例如：

	$environment = $app->environment();

你也可以透過參數 `environment` 的方法去確認是否為環境匹配給定的值：

	if ($app->environment('local'))
	{
		// The environment is local
	}

	if ($app->environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

如果要得到應用程式的範例，可以解析 `Illuminate\Contracts\Foundation\Application` contract 透過 [服務容器](/docs/5.0/container)。當然，如果你是一個 [服務提供者](/docs/5.0/providers)，應用程式範例是可以透過 `$this->app` 執行個體變數。

也可以存取應用程式範例透過 `App` facade 的 `app` 輔助方法：

	$environment = app()->environment();

	$environment = App::environment();

<a name="configuration-caching"></a>
## 設定快取

為了讓你的的應用程式提升一些速度，你可能會暫存所有的設定文件到單一文件，使用 `config:cache` Artisan 指令。這可以結合所有單一檔案由框架快速載入到應用程式的設定選項。

你通常應該執行 `config:cache` 指令作為部署工作的一部分。

<a name="maintenance-mode"></a>
## 維護模式

當你的應用程式是在維護模式，自定義視圖將顯示所有要求到應用程式中。當你在更新，或者正在維護，你可以輕鬆的 "停用" 你的應用程式。維護模式檢查包含在應用程式的預設中介軟體堆疊。如果在應用程式處於維護模式，`HttpException` 會拋出 503 的 狀態碼。

啟用維護模式，只要執行 `down` Artisan 指令：

	php artisan down

關閉維護模式，只要執行 `up` Artisan 指令：

	php artisan up

### 維護模式的 Response 模板

維護模式的預設模板放在 `resources/views/errors/503.blade.php`。

### 維護模式 & 隊列

當應用程式處於維護模式中，將不會處理任何 [隊列工作](/docs/5.0/queues) 所有的隊列工作將會在應用程式離開維護模式後繼續被進行。

<a name="pretty-urls"></a>
## 優雅鏈結

### Apache

Laravel 框架透過 `public/.htaccess` 檔案來讓網址中不需要 `index.php`。如果你網頁伺服器是使用 Apache 的話，請確認是否有開啟 `mod_rewrite` 模組。

假設 Laravel 附帶的 `.htaccess` 檔在 Apache無法作用的話，請嘗試下面的方法：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

在 Nginx，在你的網站設定增加下面的設定，可以使用「優雅鏈結」：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

當然，如果你使用 [Homestead](/docs/5.0/homestead) 的話，優雅鏈結會自動的幫你設定完成。
