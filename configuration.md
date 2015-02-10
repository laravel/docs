# 設定

- [簡介](#introduction)
- [完成安裝後](#after-installation)
- [取得設定值](#accessing-configuration-values)
- [環境設定](#environment-configuration)
- [設定快取](#configuration-caching)
- [維護模式](#maintenance-mode)
- [優雅鏈結](#pretty-urls)

<a name="introduction"></a>
## 簡介

所有 Laravel 框架的設定檔案都放置在 `config` 目錄下。 每個選項都有說明，因此你可以輕鬆地瀏覽這些文件，並且熟悉這些選項配置。

<a name="after-installation"></a>
## 完成安裝後

### 命名你的應用程式

在安裝完成 Laravel 後，你可以「命名」你的應用程式。 預設情況下，`app` 的目錄是命名在 `App` 下，透過 Composer 使用 [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/) 自動載入。不過，你可以輕鬆地透過 Artisan 指令 `app:name` 來修改命名空間，以配合你的應用程式名稱。

舉例來說，假設你的應用程式叫做「 Horsefly 」，你可以從安裝的根目錄執行下面的指令：

	php artisan app:name Horsefly

重新命名你的應用程式是完全自由的，如果你希望的話也可以保持命名空間為 `App` 。

### 其他設定

Laravel 幾乎不需設定就可以馬上使用。你可以自由的開始開發！然而，你可以瀏覽 `config/app.php` 檔案和其他的文件。你可能希望依據你的本機而做更改，檔案包含數個選項如`時區`和`語言環境`。

一旦 Laravel 安裝完成，你應該同時 [設定本機環境](/docs/5.0/configuration#environment-configuration)。

> **注意：** 你不應該在正式環境中將 `app.debug` 設定為 `true` 。絕對！千萬不要！

<a name="permissions"></a>
### 權限

Laravel 框架有一個目錄需要額外設置權限：`storage` 目錄必須讓伺服器有寫入權限。

<a name="accessing-configuration-values"></a>
## 取得設定值

你可以很輕鬆的使用 `Config` facade 取得你的設定值：

	$value = Config::get('app.timezone');

	Config::set('app.timezone', 'America/Chicago');

你也可以使用 `config` 輔助方法：

	$value = config('app.timezone');

<a name="environment-configuration"></a>
## 環境設定

通常應用程式常常需要根據不同的執行環境而有不同的設定值。例如，你會希望在你的本機開發環境上會有與正式環境不同的暫存驅動（cache driver），透過設定檔案，就可以輕鬆完成。

Laravel 透過 [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas。 在全新安裝好的 Laravel 裡，你的應用程式的根目錄下會包含一個 `.env.example` 檔案。如果你透過 Composer 安裝 Laravel，這個檔案將自動被命名為 `.env`，不然你應該手動更改檔名。

當你的應用程式收到請求，這個檔案所有的變數會被載入到 `$_ENV` PHP 超級全域變數裡。你可以使用輔助方法 `env` 檢視這些變數。事實上，如果你檢閱過 Laravel 設定檔案，你會注意到幾個選項已經在使用這個輔助方法！

根據你的本機伺服器或者上線環境需求，你可以自由的修改你的環境變數。然而， 你的 `.env`  檔案不應該被提交到應用程式的版本控制系統，因為每個開發人員或伺服器使用你的應用程式可能需要不同的環境設定。

如果你是一個團隊的開發者，不妨將 `.env.example` 檔案包含到你的應用程式。透過範例設定檔裡的預留值，你的團隊中其他開發人員可以清楚地看到執行你的應用程式所需的哪些環境變數。

#### 取得目前應用程式的環境

你可以透過 `Application` 實例中的 `environment` 方法取得目前應用程式的環境：

	$environment = $app->environment();

你也可以傳遞參數至 `environment` 方法中，來確認目前的環境是否與參數相符合：

	if ($app->environment('local'))
	{
		// The environment is local
	}

	if ($app->environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

如果想取得應用程式的實例，可以透過[服務容器](/docs/5.0/container)的 `Illuminate\Contracts\Foundation\Application`  contract 來取得。當然，如果你想在[服務提供者](/docs/5.0/providers)中使用，應用程式實例可以透過實例變數 `$this->app` 取得。

也能透過 `App` facade 的輔助方法 `app` 取得應用程式實例：

	$environment = app()->environment();

	$environment = App::environment();

<a name="configuration-caching"></a>
## 設定快取

為了讓你的的應用程式提升一些速度，你可以使用 Artisan 指令 `config:cache`  將所有的設定檔暫存到單一檔案。透過指令會將所有的設定選項合併成一個檔案，讓框架能夠快速載入。

通常來說，你應該將執行 `config:cache` 指令作為部署工作的一部分。

<a name="maintenance-mode"></a>
## 維護模式

當你的應用程式處於維護模式時，所有的路由都會指向一個自定的視圖。當你要更新或進行維護作業時，「關閉」整個網站是很簡單的。維護模式會檢查包含在應用程式的預設中介層堆疊。如果應用程式處於維護模式，`HttpException` 會拋出 503 的狀態碼。

啟用維護模式，只需要執行 Artisan 指令 `down`：

	php artisan down

關閉維護模式，請使用 Artisan 指令 `up`：

	php artisan up

### 維護模式的回應模板

維護模式回應的預設模板放在 `resources/views/errors/503.blade.php`。

### 維護模式與隊列

當應用程式處於維護模式中，將不會處理任何[隊列工作](/docs/5.0/queues)。所有的隊列工作將會在應用程式離開維護模式後繼續被進行。

<a name="pretty-urls"></a>
## 優雅鏈結

### Apache

Laravel 框架透過 `public/.htaccess` 檔案來讓網址中不需要 `index.php`。如果你的伺服器是使用，請確認是否有開啟 `mod_rewrite` 模組。

假設 Laravel 附帶的 `.htaccess` 檔在 Apache 無法作用的話，請嘗試下面的方法：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

若使用 Nginx ，可以在你的網站設定中增加下面的設定，以開啟「優雅連結」：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

當然，如果你使用 [Homestead](/docs/5.0/homestead) 的話，優雅鏈結會自動的幫你設定完成。
