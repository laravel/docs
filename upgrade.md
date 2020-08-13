# 升級指南

- [從 5.6 升級到 5.7.0](#upgrade-5.7.0)

<a name="upgrade-5.7.0"></a>
## 從 5.6 升級到 5.7.0

#### 預估升級時間：10 - 15 分鐘

> {note} 我們嘗試記錄每個重大變更。由於有些重大的變更是在框架最隱密的地方，但實際上只有一小部分的變更會影響你的應用程式。

### 更新依賴項目

在 `composer.json` 檔案中更新 `laravel/framework` 到 `5.7.*`。

如果你正在使用 Laravel Passport，請到 `composer.json` 檔案中更新 `laravel/passport` 到 `^7.0`。

最後，請檢查你的應用程式所使用的第三方套件的版本是否能支援 Laravel 5.7。

### 應用程式

#### `register` 方法

**影響程度：非常低**

`Illuminate\Foundation\Application` 類別的 `register` 方法的 `options` 參數已正式棄用。如果你有覆寫過這個方法，請更新這個方法的參數：

    /**
     * 為應用程式註冊服務提供者。
     *
     * @param  \Illuminate\Support\ServiceProvider|string  $provider
     * @param  bool   $force
     * @return \Illuminate\Support\ServiceProvider
     */
    public function register($provider, $force = false);

### Artisan

#### 排程任務的連線與隊列

**影響程度：低**

如果現在沒有直接傳遞連線與任務到 `job` 方法，則 `$schedule->job` 方法會採用 Job 類別上的 `queue` 和 `connection` 屬性。

一般來說，這應該視為是錯誤修復。然而，經過審慎考量，還是把它列為重大變更。[如果遇到有關此變更的任何問題，請通知我們](https://github.com/laravel/framework/pull/25216)。

### Assets

#### Asset 目錄扁平化

**影響程度：沒有影響**

對於新的 Laravel 5.7 應用程式，具有 script 與 style 的 assert 目錄已正式壓平到 `resources` 目錄。這**並不會**影響到現有的應用程式，所以不需要修改現有的應用程式。

不過，如果你想要進行此變更，請將 `resources/assets/*` 上的所有檔案移動至上一層：

- 從 `resources/assets/js/*` 到 `resources/js/*`
- 從 `resources/assets/sass/*` 到 `resources/sass/*`

然後，更新 `webpack.mix.js` 檔案中任何舊目錄的引用路徑：

    mix.js('resources/js/app.js', 'public/js')
       .sass('resources/sass/app.scss', 'public/css');

#### 新增 `svg` 目錄

**影響程度：非常高**

新加入的目錄，`svg`，已加到 `public` 目錄中。它具有四個 svg 檔案：`403.svg`、`404.svg`、`500.svg` 和 `503.svg`，它們會顯示在各自的錯誤頁面上。

你可以從 [GitHub](https://github.com/laravel/laravel/tree/5.7/public/svg) 上取得檔案。

### 認證

#### `Authenticate` 中介層

**影響程度：低**

`Illuminate\Auth\Middleware\Authenticate` 中介層的 `authenticate` 方法現在可以傳入 `$request` 作為它的第一個參數。如果你正在自己的 `Authenticate` 中介層中覆寫這個方法，應該更新方法的參數。

    /**
     * 確認使用者是否有登入到任何給定的 Guard。
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  array  $guards
     * @return void
     *
     * @throws \Illuminate\Auth\AuthenticationException
     */
    protected function authenticate($request, array $guards)

#### `ResetsPasswords` Trait

**影響程度：低**

`ResetsPasswords` Trait 受保護的 `sendResetResponse` 方法現在可以傳入 `Illuminate\Http\Request` 作為它的第一個參數。如果你正在覆寫這個方法，應該更新方法的參數。

    /**
     * 取得成功的密碼重設的回應。
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $response
     * @return \Illuminate\Http\RedirectResponse|\Illuminate\Http\JsonResponse
     */
    protected function sendResetResponse(Request $request, $response)

#### `SendsPasswordResetEmails` Trait

**影響程度：低**

`SendsPasswordResetEmails` Trait 受保護的 `sendResetLinkResponse` 方法現在可以傳入 `Illuminate\Http\Request` 作為它的第一個參數。如果你正在覆寫這個方法，應該更新方法的參數。

    /**
     * 取得成功的密碼重設連結的回應。
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $response
     * @return \Illuminate\Http\RedirectResponse|\Illuminate\Http\JsonResponse
     */
    protected function sendResetLinkResponse(Request $request, $response)

### 授權

#### `Gate` Contract

**影響程度：非常低**

`raw` 方法能見度已從 `protected` 改為 `public`。還有，它[已加到 `Illuminate\Contracts\Auth\Access\Gate` Contract](https://github.com/laravel/framework/pull/25143)：

    /**
     * 從授權回呼上取得原生結果。
     *
     * @param  string  $ability
     * @param  array|mixed  $arguments
     * @return mixed
     */
    public function raw($ability, $arguments = []);

如果你正在實作這個介面，你應該將這個方法加到實作中。

#### `Login` 事件

**影響程度：非常低**

`Illuminate\Auth\Events\Login` 事件的 `__construct` 方法新增 `$guard` 參數：

    /**
     * 建立新事件實例。
     *
     * @param  string  $guard
     * @param  \Illuminate\Contracts\Auth\Authenticatable  $user
     * @param  bool  $remember
     * @return void
     */
    public function __construct($guard, $user, $remember)

如果要在應用程式中手動觸發這個事件，會需要傳遞這個參數到事件的建構子。下列會示範傳遞預設框架的 Guard 到登入事件：

    use Illuminate\Auth\Events\Login;

    event(new Login(config('auth.defaults.guard'), $user, $remember))

### Blade

#### `or` 運算子

**影響程度：高**

Blade 「or」 運算子已正式棄用，並使用 PHP 內建的 `??`「空合併」運算子來取代之，該運算子具有相同的作用與功能：

    // Laravel 5.6...
    {{ $foo or 'default' }}

    // Laravel 5.7...
    {{ $foo ?? 'default' }}

### 快取

**影響程度：非常高**

新的 `data` 目錄已加到 `storage/framework/cache`。你應該在應用程式中建立這個目錄。

    mkdir -p storage/framework/cache/data

然後，新增 [.gitignore](https://github.com/laravel/laravel/blob/76369205c8715a4a8d0d73061aa042a74fd402dc/storage/framework/cache/data/.gitignore) 檔案到剛建立的 `data` 目錄中：

    cp storage/framework/cache/.gitignore storage/framework/cache/data/.gitignore

最後，請確保 [storage/framework/cache/.gitignore](https://github.com/laravel/laravel/blob/76369205c8715a4a8d0d73061aa042a74fd402dc/storage/framework/cache/.gitignore) 檔案有更新底下內容：

    *
    !data/
    !.gitignore

### Carbon

**影響程度：非常低**

Carbon「macros」現在交由 Carbon 函式庫直接來處理，而不是 Laravel 的函式庫擴充。我們並不希望這會破壞你的程式碼。還有，[請讓我們知道你在這個變更發現的相關問題](https://github.com/laravel/framework/pull/23938)。

### 集合

#### `split` 方法

**影響程度：低**

`split` 方法[已更新成回傳要求的「群集」數量](https://github.com/laravel/framework/pull/24088)，不包括原本集合項目總數量小於要求的總數量。一般來說，這應該視為是錯誤修復。然而，經過審慎考量，還是把它列為重大變更。

### Cookie

#### `Factory` Contract 方法參數

**影響程度：非常低**

`Illuminate\Contracts\Cookie\Factory` 介面的 `make` 和 `forever` 方法的參數[有做修改](https://github.com/laravel/framework/pull/23200)。如果你正在實作這個介面，請更新這些方法到你的實作。

### 資料庫

#### `softDeletesTz` Migration 方法

**影響程度：低**

資料表結構建構氣的 `softDeletesTz` 方法現在可以將欄位名稱作為它的第一個參數，而 `$precision` 已移至第二參數位置：

    /**
     * 資料表新增「刪除時間」timestampTz。
     *
     * @param  string  $column
     * @param  int  $precision
     * @return \Illuminate\Support\Fluent
     */
    public function softDeletesTz($column = 'deleted_at', $precision = 0)

#### `ConnectionInterface` Contract

**影響程度：非常低**

`Illuminate\Database\ConnectionInterface` Contract 的 `select` 與 `selectOne` 方法參數新加入了 `$useReadPdo` 參數：

    /**
     * 執行 select 語法並回傳單一結果。
     *
     * @param  string  $query
     * @param  array   $bindings
     * @param  bool  $useReadPdo
     * @return mixed
     */
    public function selectOne($query, $bindings = [], $useReadPdo = true);

    /**
     * 對資料庫執行 select 語法。
     *
     * @param  string  $query
     * @param  array   $bindings
     * @param  bool  $useReadPdo
     * @return array
     */
    public function select($query, $bindings = [], $useReadPdo = true);

另外，`cursor` 方法已加到 Contract：

    /**
     * 對資料庫執行 select 語法並回傳一個產生器。
     *
     * @param  string  $query
     * @param  array  $bindings
     * @param  bool  $useReadPdo
     * @return \Generator
     */
    public function cursor($query, $bindings = [], $useReadPdo = true);

如果你正在實作這個介面，可以將這個方法加到你的實作。

#### `whereDate` 方法

**影響程度：低**

查詢建構器的 `whereDate` 方法現在可以將 `DateTime` 實體轉換為 `Y-m-d` 格式：

    // 之前的用法 - SELECT * FROM `table` WHERE `created_at` > '2018-08-01 13:00:00'
    $query->whereDate('created_at', '>', Carbon::parse('2018-08-01 13:00:00'));
    
    // 當前的用法 - SELECT * FROM `table` WHERE `created_at` > '2018-08-01'
    $query->whereDate('created_at', '>', Carbon::parse('2018-08-01 13:00:00'));
     

#### Migration 命令輸出

**影響程度：非常低**

Migration 核心命令已[更新成可以設定 Migration 類別上的輸出實體](https://github.com/laravel/framework/pull/24811)。如果你要覆寫或擴充 Migrateion 命令，可以使用 `$this->migrator->setOutput($this->output)` 來取代 `$this->migrator->getNotes()`。

#### SQL Server 驅動

**影響程度：低**

在 Laravel 5.7 之前，`PDO_DBLIB` 驅動被用來作為預設的 SQL Server PDO 驅動。Microsoft 認為要棄用這個驅動。從 Laravel 5.7 開始，`PDO_SQLSRV` 將會在可用的情況下被用來做為預設的驅動。還有，你可以選擇使用 `PDO_ODBC` 驅動：

    'sqlsrv' => [
        // ...
        'odbc' => true,
        'odbc_datasource_name' => 'your-odbc-dsn',
    ],

如果無法使用這些驅動，Laravel 會使用 `PDO_DBLIB` 驅動。

#### SQLite 的外鍵

**影響程度：中度**

SQLite 不支援刪除外鍵。因此，資料表上使用 `dropForeign` 方法現在會跳出異常。一般來說，這應該視為是錯誤修復。然而，經過審慎考量，還是把它列為重大變更。

如果你在多種資料庫上執行你的 Migration，請考慮在 Migration 中使用 `DB::getDriverName()` 來略過 SQLite 不支援的外鍵方法。

### 除錯

#### Dumper 類別

**影響程度：非常低**

刪除了 `Illuminate\Support\Debug\Dumper` 和 `Illuminate\Support\Debug\HtmlDumper` 類別，並改用 Symfony 的自身 Dumper：`Symfony\Component\VarDumper\VarDumper` and `Symfony\Component\VarDumper\Dumper\HtmlDumper`。

### Eloquent

#### `latest` 與 `oldest` 方法

**影響程度：低**

Eloquent 查詢建構器的 `latest` 和 `oldest` 方法已更新為採用 Eloquent 模型上指定自訂的「created_at」時間戳的欄位。 一般來說，這應該視為是錯誤修復。然而，經過審慎考量，還是把它列為重大變更。

#### `wasChanged` 方法

**影響程度：非常低**

Eloquent 模型的更改為現在可以在觸發 `updated` 模型事件**之前**可以使用 `wasChanged` 方法。一般來說，這應該視為是錯誤修復。然而，經過審慎考量，還是把它列為重大變更。 [如果你在這個變更上遇到的任何問題，請讓我們知道](https://github.com/laravel/framework/pull/25026).

#### PostgreSQL 特殊浮點數值

**影響程度：低**

PostgreSQL 支援浮點數值有 `Infinity`、`-Infinity` 和 `NaN`。在 Laravel 5.7 之前，當 Eloquent 為欄位轉換型別為 `float`、`double` 或 `real` 時，這些會被轉換成 `0`。

從 Laravel 5.7 開始，這些值會被轉換成對應的 PHP 常數 `INF`、`-INF` 和 `NAN`。

### Email 驗證

**影響程度：非必要**

如果你選擇使用 Laravel 新的[電子郵件驗證服務](/docs/{{version}}/verification)，就會需要加入額外的套件到你的應用程式。首先，將 `VerificationController` 加到你的應用程式：[App\Http\Controllers\Auth\VerificationController](https://github.com/laravel/laravel/blob/5.7/app/Http/Controllers/Auth/VerificationController.php)。

你還需要修改你的 `App\User` 模型來實作 `MustVerifyEmail` 介面：

    <?php

    namespace App;

    use Illuminate\Notifications\Notifiable;
    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

為了只讓驗證通過的使用者存取給定的路由而使用 `verified` 中介層，你需要更新 `app/Http/Kernel.php` 檔案，引入的 `verified` 與 `signed` 中介層到 `$routeMiddleware` 屬性：

    // 在 App\Http\Kernel Class 中...

    protected $routeMiddleware = [
        'auth' => \Illuminate\Auth\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];

你也會需要驗證視圖範本。這個視圖被放置在 `resources/views/auth/verify.blade.php`。你可以 [GitHub](https://github.com/laravel/framework/blob/5.7/src/Illuminate/Auth/Console/stubs/make/views/auth/verify.stub) 上取得這個視圖範本。

接著，你的使用者資料表必須包含 `email_verified_at` 欄位來儲存電子郵件被驗證的日期與時間：

    $table->timestamp('email_verified_at')->nullable();

為了要在使用者註冊之後寄送電子信件，你應該在 [App\Providers\EventServiceProvider](https://github.com/laravel/laravel/blob/5.7/app/Providers/EventServiceProvider.php) 類別註冊下列事件與監聽器：

    use Illuminate\Auth\Events\Registered;
    use Illuminate\Auth\Listeners\SendEmailVerificationNotification;

    /**
     * 應用程式的事件監聽器對照表。
     *
     * @var array
     */
    protected $listen = [
        Registered::class => [
            SendEmailVerificationNotification::class,
        ],
    ];

最後，在呼叫 `Auth::routes` 方法時，你應該傳遞 `verify` 選項到該方法。

    Auth::routes(['verify' => true]);

### 檔案系統

#### `Filesystem` Contract 方法

**影響程度：低**

[`Illuminate\Contracts\Filesystem\Filesystem` Contract](https://github.com/laravel/framework/pull/23755) 已加入 `readStream` 和 `writeStream` 方法。如果你正在實作這個介面，可以將這些方法加到你的實作中。

### 雜湊

#### `Hash::check` 方法

**影響程度：沒有影響**

現在 `check` 方法**可以選擇**檢查雜湊演算法是否與設定的演算法對應。

### 郵件

#### 轉換郵件動態變數

**影響程度：低**

動態傳遞郵件視圖的變數[會自動轉為「駝峰式命名」](https://github.com/laravel/framework/pull/24232)，這可使郵件動態變數的用法與動態視圖變數一致。動態郵件變數不是 Laravel 文件上的功能，所以對你的應用程式影響程度很小。

#### 模板主題

**影響程度：中度**

如果你有為 Markdown 自訂郵件模板的預設主題樣式，將會需要重新發布並再次客製化。按鈕顏色類別將「blue」、「green」和「red」依序改名為「primary」、「success」和「error」。

### 隊列

#### `QUEUE_DRIVER` 環境變數

**影響程度：非常低**

`QUEUE_DRIVER` 環境變數已重新命名為 `QUEUE_CONNECTION`。這不會影響既有的應用程式的升級，除非你刻意修改 `config/queue.php` 設定檔來對應 Laravel 5.7。

#### `WorkCommand` 選項

**影響程度：非常低**

`stop-when-empty` 選項已加到 `WorkCommand` 中。如果你有繼承過這個命令，則需要將 `stop-when-empty` 加到類別的 `$signature` 屬性

### 路由

#### `Route::redirect` 方法

**影響程度： High**

`Route::redirect` 方法現在會回傳 `302` HTTP 狀態碼的重導行為。加入了 `permanentRedirect` 方法來允許 `301` 重導。

    // 回傳 302 重導...
    Route::redirect('/foo', '/bar');

    // 回傳 301 重導...
    Route::redirect('/foo', '/bar', 301);

    // 回傳 301 重導...
    Route::permanentRedirect('/foo', '/bar');

#### `addRoute` 方法

**影響程度：低**

`Illuminate\Routing\Router` 類別的 `addRoute` 方法已從 `protected` 改為 `public`。

### 驗證

#### 巢狀驗證資料

**影響程度：中度**

在之前的 Laravel 版本，`validate` 方法沒有為巢狀驗證規則回傳正確的資料。Laravel 5.7 已修正了這個問題：

    $data = Validator::make([
        'person' => [
            'name' => 'Taylor',
            'job' => 'Developer'
        ]
    ], ['person.name' => 'required'])->validate();

    dump($data);

    // 之前的結果...
    ['person' => ['name' => 'Taylor', 'job' => 'Developer']]

    // 新的結果...
    ['person' => ['name' => 'Taylor']]

#### `Validator` Contract

**影響程度：非常低**

`validate` 方法[已加到 `Illuminate\Contracts\Validation\Validator` contract](https://github.com/laravel/framework/pull/25128):

    /**
     * 針對特定資料執行驗證器的規則。
     *
     * @return array
     */
    public function validate();

如果要實作這個介面，你可以將這個方法加到實例中。

### 測試

**影響程度：中度**

Laravel 5.7 採用了為 Artisan 命令所優化的測試工具。現在預設的 Artisan 命令輸出會被 Mock。如果在測試的過程中需要 `artisan` 方法來執行命令，你可以使用 `Artisan::call` 或在你的測試類別上定義 `public $mockConsoleOutput = false`。

### 其他

我們也鼓勵你查看 `laravel/laravel` [GitHub 儲存褲](https://github.com/laravel/laravel)中的任何異動。儘管許多更改並不是必要的，但你可能希望保持這些文件與你的應用程序同步。其中一些更改將在本升級指南中介紹，但其他更改（例如更改設定檔案或註釋）將不會被介紹。你可以使用 [GitHub 比較工具](https://github.com/laravel/laravel/compare/5.6...5.7)來輕易的檢查更動的內容，並選擇哪些更新對你比較重要。