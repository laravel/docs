# Configuration

- [ 前言 ](#introduction)
- [ 環境設定 ](#environment-configuration)
    - [ 環境變數型態 ](#environment-variable-types)
    - [ 檢索環境設定 ](#retrieving-environment-configuration)
    - [ 判斷目前環境 ](#determining-the-current-environment)
    - [加密環境檔](#encrypting-environment-files)
- [ 存取設定值 ](#accessing-configuration-values)
- [ 快取設定 ](#configuration-caching)
- [ 除錯模式 ](#debug-mode)
- [ 維護模式 ](#maintenance-mode)

<a name="introduction"></a>
## 前言

Laravel 框架所有的設定檔都儲存在 `config` 目錄中。每個選項都會被記錄，所以請隨意瀏覽並去熟悉你可用的選項。

這些組態設定允許你設定資料庫的連接資訊、郵件伺服器資訊及各種核心設定值，例如應用程式的時區和加密金鑰。

<a name="application-overview"></a>
#### 應用程式概述

趕時間嗎？你可以透過 Artisan 指令 `about` 快速了解應用程式的組態設定、驅動程式和環境。 

```shell
php artisan about
```

如果你只對應用程式的概覽輸出部分感興趣，可以使用 `--only` 選項過濾該部分：

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
## 環境設定

根據應用程式執行的環境，不同的設定值通常很有幫助。例如，你可能希望在本地（local）使用與產品伺服器（production server）不同的快取驅動程式。

為了讓這件事變輕鬆，Laravel 使用 [ DotEnv ](https://github.com/vlucas/phpdotenv) PHP 函式庫（library）。在一個全新 Laravel 安裝過程中，應用程式的根目錄會包含一個定義了許多常見環境變數的 `.env.example` 檔。在 Laravel 安裝過程中，這個檔案將會自動複製到 `.env`。

Laravel 預設的 `env` 檔包含一些常見的設定值，這些值可能會根據應用程式執行的環境（本機、產品 web 伺服器）有所不同。可以從  `config` 中的 `env` 函式的各種 Laravel 設定檔檢索這些設定值。

如果是正在進行團隊開發，你可能希望繼續在應用程式包含 `.env.example` 檔。透過範例設定檔的佔位符（placeholder）值，隊伍中的其他開發者可以清楚明白，執行應用程式需要那些環境變數。

> **Note**  
> `.env` 檔中所有的變數都可以被外部環境變數覆蓋，例如伺服器級（server-level）或系統級（system-level）的環境變數。

<a name="environment-file-security"></a>
#### 環境檔案安全

你的 `.env` 檔不應該提交給你的應用程式版控。因為每個使用應用程式的開發者或伺服器可能需要不同的環境設定。而且，如果入侵者取得你專案原始碼的控制權限將會是個隱憂，因為全部的敏感數據都會暴露出來。

However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely.

<a name="additional-environment-files"></a>
#### 附加環境檔案

在載入應用程式的環境變數之前，Laravel 會判斷外部是否已提供 `APP_ENV` 環境變數或 `--env` 的指令列介面引數（CLI argument）是否已被指定。如果有的話，Laravel 會嘗試載入 `.env.[APP_ENV]` 檔。如果檔案不存在，則會載入預設的 `.env` 檔。

<a name="environment-variable-types"></a>
### 環境變數型態

`.env` 檔內所有的變數型態通常被解析為字串（string），因此建立了一些保留值以允許你用 `env()` 函式輸入更廣泛的變數型態：

| `.env` 值 | `env()` 值 |
|--------------|---------------|
| true         | (bool) true   |
| (true)       | (bool) true   |
| false        | (bool) false  |
| (false)      | (bool) false  |
| empty        | (string) ''   |
| (empty)      | (string) ''   |
| null         | (null) null   |
| (null)       | (null) null   |

如果你需要定義包含空白（space）的環境變數值，可以把值括在雙引號中：

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 檢索環境設定

當應用程式收到請求時，`.env` 檔內列出所有的變數會被載入到超全域（super-global）`$_ENV` 中。你可以使用 `env` 函式檢索這些設定檔的值。事實上，如果你查看 Laravel 設定檔，你會發現許多選項已經使用了這個函式：

    'debug' => env('APP_DEBUG', false),

`env` 函式的第二個參數是「預設值」。當環境變數沒有給定參數時則會回傳預設值。

<a name="determining-the-current-environment"></a>
### 判斷目前環境

目前應用程式環境是由 `.env` 檔內的 `APP_ENV` 變數決定的。你可以透過 `APP` [facade](/docs/{{version}}/facades) 的 `environment` 方法（method）存取這些值：

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

你也可以使用 `environment` 方法（method）傳送引數（arguments）去判斷目前環境是否與給定值相符。當相符時會回傳 `true`：

    if (App::environment('local')) {
        // 目前環境是 local
    }

    if (App::environment(['local', 'staging'])) {
        // 目前環境是 local 或 staging……
    }

> **Note**  
> 目前應用程式環境檢測可以由定義伺服器級（server-level）`APP_ENV` 環境變數去做覆蓋。

<a name="encrypting-environment-files"></a>
### 加密環境檔

未加密環境檔不應該被存取到原始碼控制中。不過Laravel 可以加密你的環境檔，因此這些加密過的環境檔可以更安全地加進你的部分應用的原始碼控制中。

<a name="encryption"></a>
#### 加密

你可以使用 `env:encrypt` 指令來加密環境檔：

```shell
php artisan env:encrypt
```

執行 `env:encrypt` 指令會加密你的 `.env` 檔然後將加密的內容放進 `.env.encrypted` 檔。解密金鑰會顯示在指令的輸出，我們應該要將金鑰儲存在安全的密碼管理器中。如果你想提供自己的加密金鑰你可以在調用指令時使用 `--key` 選項：

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> **Note**  
> 被提供的金鑰長度應該和所使用的加密密碼所需的金鑰長度相符。正常情況下，Laravel 會使用需要32個英文字符組成的 `AES-256-CBC` 密碼。在調用指令時通過 `--cipher` 選項，你可以自由的使用任何Laravel [加密器](/docs/{{version}}/encryption)支援的密碼。

如果你的應用有多個環境檔，例如 `.env` 和 `.env.staging` ，你可以藉由通過 `--env` 選項提供環境名字來指定需要被加密的環境檔：

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 解密

你可以使用 `env:decrypt` 指令來解密環境檔。這個指令需要解密金鑰，Laravel會從 `LARAVEL_ENV_ENCRYPTION_KEY` 這個環境變數中找出金鑰。

```shell
php artisan env:decrypt
```
或者可以直接通過 `--key` 選項來提供解密金鑰：

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

當 `env:decrypt` 指令被調用時，Laravel會解密 `.env.encrypted` 這個檔案，然後把解密後的內容放進 `.env` 檔中。

在 `env:decrypt` 指令後面加上 `--cipher` 選項可以用來自定義加密密碼：
The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

如果你的應用有多個環境檔，例如 `.env` 和 `.env.staging` ，你可以藉由通過 `--env` 選項提供環境名字來指定需要被解密的環境檔：

```shell
php artisan env:decrypt --env=staging
```

為了覆蓋已經存在的環境檔，你可以在 `env:decrypt` 指令後面加上 `--force` 選項。

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 存取設定值

你可以在應用程式的任何位置使用全域 `config` 函式輕易存取設定值。此設定值使用「dot」語法，其中包含你想要存取的檔名和選項。若設定選項不存在時也能指定回傳預設值：

    $value = config('app.timezone');

    // 若設定值不存在則檢索預設值……
    $value = config('app.timezone', 'Asia/Seoul');

要在執行時改動設定值，請傳送陣列（array）給 `config` 函式：

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## 快取設定

為了增加應用程式的速度，你應該使用 Artisan 指令 `config:cache` 將全部的設定檔到一個檔案內做快取。這將會結合所有的設定選項到一個檔案並加速框架的載入。

你通常會產品部署過程（deployment process）執行 `php artisan config:cache` 指令。這個指令不應該在本地部署（local development）時執行，因為在應用程式的開發過程中需要經常更改設定選項。

> **Warning**  
> 如果你在部署過程中執行 `config:cache` 指令，則必須確定你在設定檔中只有呼叫 `env` 函式。一旦設定檔進入快取，`.env` 檔將不會被載入；因此，`env` 函式只會回傳外部的系統等級（external system level）的環境變數。

<a name="debug-mode"></a>
## Debug 模式

`config/app.php` 設定檔內的 `debug` 選項會判斷要顯示給使用者的錯誤發生的訊息量。預設情況下，該選項被設定為尊重 `APP_DEBUG` 的環境變數值且儲存在 `.env` 檔內。

在本地開發時，你必須設定 `APP_DEBUG` 的環境變數值為 `true`。**在你的產品環境中，這個值必須永遠為 `false`。如果在產品環境將變數設定為 `true`，你可能會暴露敏感的設定值給應用程式的最終使用者。**

<a name="maintenance-mode"></a>
## 維護模式

當應用程式在維護模式時，傳送到應用程式的所有請求（request）都會被顯示在一個自定義的視圖（view）。這可以在升級或執行維護時讓「關閉」應用程式變得容易。維護模式的檢查包含了應用程式的預設中介層堆疊（middleware stack）。如果應用程式處於維護模式，會拋出（throw）一個狀態碼為 503 的 `Symfony\Component\HttpKernel\Exception\HttpException` 執行個體（instance）。

想要啟動維護模式，請執行 Artisan 指令 `down`：

```shell
php artisan down
```
如果你想要 `Refresh` 的 HTTP 標頭（header）跟所有維護模式的回應（response）一起送出，你可以在使用 `down` 指令時附加 `refresh` 選項。`Refresh` 標頭將指示瀏覽器在指定秒數後自動刷新頁面：

```shell
php artisan down --refresh=15
```

你也可以在執行 `down` 指令時附加 `retry` 選項，該選項被設定為 `Retry-After` 的 HTTP 標頭值，雖然瀏覽器一般會忽視此標頭：

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 繞過維護模式

在維護模式可以使用 `secret` 選項附加隱藏標記（secret token）繞過維護模式：

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

將應用程式設置在維護模式之後，你可以導航到應用程式 URL 指定的標記（token）且 Laravel 會向瀏覽器發佈一個繞過維護模式的 cookie。

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

存取這個隱藏路由時，你會被重新導向到應用程式的 `/` 路由。一旦這個 cookie 被發布到你的瀏覽器，你將可以正常瀏覽應用程式，而不像是在維護模式。

> **Note**  
> 維護模式的隱藏標記通常應該用字母、數字字元和連接號「-」組成。你必須避免在 URL 使用類似 `?` 的特殊含義字元。

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 預先渲染維護模式視圖

如果你在部署時使用 `php artisan down` 指令，你的使用者可能會在存取你的 Composer 依賴項或其他正在升級的基架套件時遇到程式錯誤。這是因為 Laravel 框架必須啟動這重要部分，才能判斷應用程式是否為維護模式並渲染維護模式視圖所使用的模板引擎。

因為這個原因，Laravel 允許你預先渲染維護模式視圖，該視圖會在請求周期（request cycle）的一開始便回傳。這個視圖在應用程式的任何依賴項載入之前就可以呈現。你可以使用 `down` 指令附加 `render` 選項來預先渲染你選好的模板：

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 重新導向維護模式的請求

在維護模式下，Laravel 會展示使用者意圖存取的所有應用程式 URL 的維護模式視圖。如果你想要，你可以指示 Laravel 把所有請求重新導向特定的 URL。這可以使用 `redirect` 選項來完成。例如，你可能希望把所有請求重新導向至 `/` URI：

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 關閉維護模式

要關閉維護模式，請使用 `up` 指令：

```shell
php artisan up
```

> **Note**  
> 你可以在 `resources/views/errors/503.blade.php` 自定義預設的維護模式模板。

<a name="maintenance-mode-queues"></a>
#### 維護模式與佇列

當應用程式在維護模式時，不會處理任何 [ 佇列任務（queued jobs） ](/docs/{{version}}/queues)。這些任務要在離開維護模式後才會繼續正常處理。

<a name="alternatives-to-maintenance-mode"></a>
#### 維護模式的替代方案

維護模式會要求應用程式數秒的停機時間，斟酌使用替代方案像是 [ Laravel Vapor ](https://vapor.laravel.com) 和 [ Envoyer ](https://envoyer.io) 來實現 Laravel 的零停機（zero-downtime）部署。
