# 安裝

- [安裝 Composer](#install-composer)
- [安裝 Laravel](#install-laravel)
- [伺服器需求](#server-requirements)

<a name="install-composer"></a>
## 安裝 Composer

Laravel 使用 [Composer](http://getcomposer.org) 來管理相依性。所以，在使用 Laravel 之前，你必須確認電腦上是否安裝了 Composer。

<a name="install-laravel"></a>
## 安裝 Laravel

### 透過 Laravel 安裝工具

首先，使用 Composer 下載 Laravel 安裝包：

	composer global require "laravel/installer=~1.1"

請確定把 `~/.composer/vendor/bin` 路徑放置於你的 `PATH` 裡，這樣 `laravel` 執行檔就會存在於你的系統之中。

一旦安裝完成後，就可以使用 `laravel new` 指令在指定的目錄建立一份新安裝的 `Laravel` 專案，例如：`laravel new blog` 將會在當前目錄下建立一個叫 `blog` 的目錄，此目錄裡面存放著新安裝的 Laravel 和相依程式碼。這個安裝方法比透過 Composer 安裝速度快許多：

	laravel new blog

### 透過 Composer Create-Project

你也可以透過 Composer 在命令列執行 `create-project` 來安裝 Laravel：

	composer create-project laravel/laravel --prefer-dist

### Scaffolding

Laravel 附帶使用者註冊和認證的 scaffolding。如果你想要移除這些 scaffolding，使用 `fresh` Artisan 命令：

	php artisan fresh

<a name="server-requirements"></a>
## 伺服器需求

Laravel 框架有一些系統上的需求：

- PHP >= 5.4
- Mcrypt PHP Extension
- OpenSSL PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension

在 PHP 5.5 之後，有些作業系統需要手動安裝 PHP JSON 套件。如果你是使用 Ubuntu，可以透過 `apt-get install php5-json` 來進行安裝。

<a name="configuration"></a>
## 設定

在你安裝完 Laravel 後，首先需要做的事情是設定一個隨機字串到應用程式金鑰。假設你是透過 Composer 安裝 Laravel，這個金鑰有可能已經透過 `key:generate` 指令幫你設定完成。

通常這個金鑰應該有 32 字元長。這個金鑰可以被設定在 `.env` 環境檔案中。**如果這金鑰沒有被設定的話，你的使用者 sessions 和其他的加密資料都是不安全的！**

Laravel 幾乎不需要其他設定就可以馬上使用。你可以自由的開始開發！然而，你可以查看 `config/app.php` 檔案和它的文件。你可能會希望依據你的應用程式而做更改，它包含許多選項例如 `timezone` 和 `locale`。

一旦 Laravel 安裝完成，你也應該 [設定本地環境](/docs/5.0/configuration#environment-configuration)。

> **注意：** 你不應該在正式環境中將 `app.debug` 設定為 `true`。

<a name="permissions"></a>
### 權限

Laravel 框架有一個目錄需要額外設置權限：`storage` 要讓伺服器有寫入的權限。

<a name="pretty-urls"></a>
## 美化路徑

### Apache

Laravel 框架透過 `public/.htaccess` 檔案使網址中不需要 `index.php`。如果你的網頁伺服器是使用 Apache 的話，請確認是否有開啟 `mod_rewrite` 模組。

假設 Laravel 附帶的 `.htaccess` 檔在 Apache 無法作用的話，請嘗試下面的方法：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

使用 Nginx 時，在你的網站設定增加下面的設定，可以「美化」路徑：

	location / {
		try_files $uri $uri/ /index.php?$query_string;
	}

當然，如果你使用 [Homestead](/docs/5.0/homestead) 的話，會自動幫你設定美化路徑。
