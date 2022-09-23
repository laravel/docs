# Deployment

- [前言](#introduction)
- [伺服器需求](#server-requirements)
- [伺服器設定](#server-configuration)
    - [Nginx](#nginx)
- [優化](#optimization)
    - [優化自動載入](#autoloader-optimization)
    - [優化設定載入](#optimizing-configuration-loading)
    - [優化路由載入](#optimizing-route-loading)
    - [優化視圖載入](#optimizing-view-loading)
- [偵錯模式](#debug-mode)
- [使用 Forge / Vapor 部署](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 前言

當你準備好在產品環境上部署 Laravel 應用程式時，請注意幾點可以讓應用程式高效率執行的事情。在這個文件，我們會提供些很棒的起始點讓你確定你的 Laravel 應用程式已經部署妥當。

<a name="server-requirements"></a>
## 伺服器需求

Laravel 框架有一些系統需求。你必須確保 web 伺服器有滿足 PHP 版本和擴充功能（extension）需求：

<div class="content-list" markdown="1">

- PHP >= 8.0
- BCMath PHP 擴充功能
- Ctype PHP 擴充功能
- cURL PHP 擴充功能
- DOM PHP 擴充功能
- Fileinfo PHP 擴充功能
- JSON PHP 擴充功能
- Mbstring PHP 擴充功能
- OpenSSL PHP 擴充功能
- PCRE PHP 擴充功能
- PDO PHP 擴充功能
- Tokenizer PHP 擴充功能
- XML PHP 擴充功能

</div>

<a name="server-configuration"></a>
## 伺服器設定

<a name="nginx"></a>
### Nginx

如果你在執行 Nginx 的伺服器上部署應用程式，你可能要使用以下設定檔作為起始點來設定 web 伺服器。該檔案很有可能需要根據伺服器設定做一些自定義的修改。**如果你想要管理伺服器上的協助，考慮使用第一方 Laravel 伺服器管理和部署伺服器例如 [Laravel Forge](https://forge.laravel.com)。**

請確保像是下方的設定，web 伺服器會將所有請求導向應用程式的 `public/index.php` 檔。你不該把 `index.php` 檔移動到專案的根目錄，因為從專案根目錄提供服務的應用程式會在公用網路暴露許多敏感的設定檔：

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="optimization"></a>
## 優化

<a name="autoloader-optimization"></a>
### 優化自動載入

當部署至產品環境時，確定你有優化 Composer 的自動載入類別映射以便 Composer 可以快速找到對應的文件去載入給定的類別：

```shell
composer install --optimize-autoloader --no-dev
```

> **Note**  
> 除了優化自動載入器之外，你必須確定專案資源控制資料倉儲內包含一個 `composer.lock` 檔。當 `composer.lock` 檔存在時，可以更快速地安裝專案的相依性項目。

<a name="optimizing-configuration-loading"></a>
### 優化設定載入

當部署應用程式至產品環境時，你必須確定部屬過程中執行了 Artisan 指令 `config.cache`：

```shell
php artisan config:cache
```

這個指令會將所有的 Laravel 設定檔合併到單一個快取檔案，這大大減少了框架在載入設定值時讀取檔案系統的次數。

> **Warning**  
> 如果你在部屬過程中執行了指令 `config.cache`，必須確定設定檔中只有呼叫 `env` 函式。一旦設定檔被快取後，`.env` 檔就不會再被載入，且所有呼叫 `env` 函式的 `.env` 變數都會回傳 null。

<a name="optimizing-route-loading"></a>
### 優化路由載入

如果你正在建立一個有許多路由的大型應用程式，你必須確定在部署過程中已經執行了 Artisan 指令 `route:cache`：

```shell
php artisan route:cache
```

這個指令可以減少所有的路由註冊，使其成為快取檔案的單一方法呼叫，可以在註冊上百個路由時提高路由註冊性能。

<a name="optimizing-view-loading"></a>
### 優化視圖載入

當部署應用程式至產品環境時，你必須確定部屬過程中執行了 Artisan 指令 `view.cache`：

```shell
php artisan view:cache
```

這個指令會預先編譯所有的 Blade 視圖，不是被請求時才進行編譯，這可以提高每個有回傳視圖的請求效能。

<a name="debug-mode"></a>
## 偵錯模式

config/app.php 設定檔中的偵錯選項用於判斷該實際展示給使用者多少關於錯誤的資訊。預設情況下，該選項被設定為尊重 `APP_DEBUG` 的環境變數值，且儲存在應用程式的 `.env` 檔。

**在你的產品環境中，該值必須永遠為 `false`。如果 `APP_DEBUG` 的變數在產品環境中被設定為 `true`，會有將敏感設定值曝露給應用程式終端使用者的風險。

<a name="deploying-with-forge-or-vapor"></a>
## 使用 Forge / Vapor 部署

<a name="laravel-forge"></a>
#### Laravel Forge

如果你還沒準備好管理自身的伺服器設定或對於執行 大型 Laravel 應用程式所需的服務感到不適應，[Laravel Forge](https://forge.laravel.com) 是一款很棒的選擇。

Laravel Forge 可以在多個基礎設施提供者例如 DigitalOcean, Linode, AWS 等上建立伺服器。此外，Forge 可安裝並管理建立大型 Laravel 應用程式的全部所需工具，例如 Nginx, MySQL, Redis, Memcached, Beanstalk 等。

<a name="laravel-vapor"></a>
#### Laravel Vapor

如果你想要給 Laravel 一個完全無伺服器運算（serverless）、自動規模化（auto-scaling）的部署平台，參考看看 [Laravel Vapor](https://vapor.laravel.com)。Laravel Vapor 是一個由 AWS 驅動，為 Laravel 設計的無伺服器運算部署平台。在 Vapor 上啟動 Laravel 的基礎設施然後愛上可以簡單擴充的無伺服器運算。Laravel Vapor 已經經過 Laravel 作者們微調成可以完美地在框架上運作，讓你可以保持像往常一樣編寫 Laravel 應用程式。
