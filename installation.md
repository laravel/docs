# 安裝

- [安裝 Composer](#install-composer)
- [安裝 Laravel](#install-laravel)
- [伺服器環境需求](#server-requirements)
- [設定](#configuration)
- [優雅鏈結](#pretty-urls)

<a name="install-composer"></a>
## 安裝 Composer

Laravel 框架使用 [Composer](http://getcomposer.org)來管理其相依性。首先，下載一份 `composer.phar` 下來。之後，你可以把它放在本地端的專案目錄，或者是搬移至 `/usr/local/bin` 讓全站皆可使用。在 Windows 下，你可以使用 Composer [Windows 安裝工具](https://getcomposer.org/Composer-Setup.exe)。

<a name="install-laravel"></a>
## 安裝 Laravel

### 透過 Laravel 安裝工具

首先，下載 [Laravel PHAR 安裝包](http://laravel.com/laravel.phar)。為了方便，將安裝包改名為 `laravel` 並搬移到 `/usr/local/bin`。一旦安裝完成，只要簡單的 `laravel new` 命令，一個全新的 laravel 就會安裝在你指定的目錄中。例如，`laravel new blog` 將會創建一個目錄為 `blog`，並在此目錄中安裝 laravel 及其相依套件。這方法安裝將會比透過 Composer 安裝要來得快許多。

### 透過 Composer Create-Project

你一樣可以透過 Composer 在命令列執行 `create-project` 來安裝 laravel: 

	composer create-project laravel/laravel --prefer-dist

### 透過下載

Composer 安裝完成後，下載[最新版](https://github.com/laravel/laravel/archive/master.zip)的Laravel 框架並且解壓縮到伺服器上的一個目錄中。接著，在 Laravel 應用程式的根目錄下，執行 `php composer.phar install`（或者是 `composer install`）來將所有框架所需的相依套件安裝完成。為了能夠成功完成安裝，您必須在伺服器上安裝好 Git。

如果你想要更新 Laravel 框架，你需要在命令列執行 `php composer.phar update` 來更新。

<a name="server-requirements"></a>
## 伺服器環境需求

Laravel 框架有一些系統需求：

- PHP >= 5.4
- MCrypt PHP 套件

PHP 5.5 之後，一些作業系統需要手動安裝 PHP JSON 套件。如果你使用的是 Ubuntu，可以透過 `apt-get install php5-json` 來直接安裝。

<a name="configuration"></a>
## 設定

Laravel 幾乎無需設定即可馬上使用。你可以自由的開始開發。然而，你可以查看 `app/config/app.php` 檔案和他的文件。它包含了數個你的應用程式所想要更動的選項如 `時區（timezone）` 和 `語系（locale）` 。

一旦 Laravel 安裝完成，你應該同時[設定本地環境](/docs/configuration#environment-configuration)。當你在你的本機上部署時，可以讓你得到更詳細的錯誤訊息。預設在你的正式環境裡詳細的錯誤訊息是被關掉的。

> **附註:** 你不應該在正式環境中將 `app.debug` 設為 `true`。絕對！千萬不要！

<a name="permissions"></a>
### 權限

Laravel 框架有一個目錄需要額外設置權限：app/storage 需要讓網頁伺服器有寫入的權限。

<a name="paths"></a>
### 路徑

一些框架的目錄路徑是可以被設定配置的。如果要更改這些目錄的位置，請查看 `bootstrap/paths.php` 檔案。

<a name="pretty-urls"></a>
## 優雅鏈結

### Apache

Laravel 框架透過 `public/.htaccess` 檔案來讓網址中不需要 `index.php`。如果你網頁伺服器是使用 Apache 的話，請確認你有開啟 'mod_rewrite` 模組。

如果框架附帶的 `.htaccess` 檔在 Apache 中無法作用，請嘗試下面的版本：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]


### Nginx

在 Nginx, 在你的網站設定中增加下面的設定將可以開啟"優雅連結"：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
