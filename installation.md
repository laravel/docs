# 安裝

- [安裝](#installation)
    - [伺服器需求](#server-requirements)
    - [安裝 Laravel](#installing-laravel)
    - [設定](#configuration)

<a name="installation"></a>
## 安裝

<a name="server-requirements"></a>
### 伺服器需求

Laravel 框架有一些系統上的需求。當然，[Laravel Homestead](/docs/{{version}}/homestead) 虛擬機器都能滿足這些需求，所以強烈的建議你使用 Homestead 作為本機 Laravel 開發環境。

然而如果你不使用 Homestead，則需要確保你的伺服器符合下列要求：

<div class="content-list" markdown="1">
- PHP >= 5.6.4
- OpenSSL PHP Extension
- PDO PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension
</div>

<a name="installing-laravel"></a>
### 安裝 Laravel

Laravel 使用 [Composer](http://getcomposer.org) 來管理相依性。所以，在使用 Laravel 之前，你必須確認電腦上是否安裝了 Composer。

#### 方式一：透過 Laravel Installer

首先，使用 Composer 下載 Laravel installer：

    composer global require "laravel/installer"

請確定把 `$HOME/.composer/vendor/bin`路徑(實際路徑依據作業系統可能不同)放置於環境變數 $PATH 裡，這樣你的系統才能找到 `laravel` 執行檔。

一旦安裝完成後，就可以使用 `laravel new` 指令在指定的目錄建立一份全新安裝的 Laravel。例如：`laravel new blog` 將會建立一個名稱為 `blog` 的目錄，裡面存放著全新安裝的 Laravel 和相依程式碼：

    laravel new blog

#### 方式二：透過 Composer Create-Project

你也可以透過 Composer 在命令列執行 `create-project` 指令來安裝 Laravel：

    composer create-project --prefer-dist laravel/laravel blog

#### 本地開發環境伺服器

如果有在本地端安裝 PHP 且打算使用 PHP 內建的開發環境伺服器來啟用你的應用程式，可以使用 Artisan 指令 `serve`。這個指令會將開發伺服器啟動在 `http://localhost:8000` :

    php artisan serve

當然，更健全地開發環境選項還是透過 [Homestead](/docs/{{version}}/homestead) 和 [Valet](/docs/{{version}}/valet).

<a name="configuration"></a>
### 設定

#### Public 目錄

安裝完 Laravel 之後，需要將您的網站伺服器根目錄指向 `public` 目錄。該目錄下的 `index.php` 將作為前端控制器，所有的 HTTP 請求將會透過它進入你的應用程式。

#### 設定檔

所有 Laravel 框架的設定檔都放置在 `config` 目錄下。每個選項都有說明，因此你可以輕鬆地瀏覽這些文件，並且熟悉這些選項配置。

#### 目錄權限

安裝 Laravel 之後，你必須設定一些權限。`storage` 和 `bootstrap/cache` 目錄中的目錄必須讓你的伺服器有寫入權限，否則 Laravel 就無法執行。如果你使用 [Homestead](/docs/{{version}}/homestead) 虛擬機器，那麼這些權限應該已經被設定完成。

#### 應用程式金鑰

在你安裝完 Laravel 後，首先需要做的事情是設定一個隨機字串到應用程式金鑰。假設你是透過 Composer 或是 Laravel 安裝工具安裝 Laravel，那麼這個金鑰已經透過 `php artisan key:generate` 指令幫你設定完成。

通常這個金鑰應該有 32 字元長。這個金鑰可以被設定在 `.env` 環境檔案中。如果你還沒將  `.env.example` 檔案重新命名為 `.env`，那麼你應該現在開始。**如果應用程式金鑰沒有被設定的話，你的使用者 Sessions 和其他的加密資料都是不安全的！**

#### 其他設定

Laravel 幾乎不需設定就可以馬上使用，你可以自由的開始開發！當然，你可以瀏覽 `config/app.php` 檔案和對應的文件。它包含數個選項，如 `timezone(時區)` 和 `locale(語言環境)` ，你不仿根據你的應用程式來做修改。

你也可以設定 Laravel 的幾個附加元件，像是：

<div class="content-list" markdown="1">
- [快取](/docs/{{version}}/cache#configuration)
- [資料庫](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)
</div>

一旦 Laravel 安裝完成，你應該同時[設定本機環境](/docs/{{version}}/configuration#environment-configuration)。
