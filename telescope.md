# Laravel Telescope

- [簡介](#introduction)
- [安裝](#installation)
    - [設置](#configuration)
    - [資料修整](#data-pruning)
    - [客製化資料遷移](#migration-customization)
- [儀表板認證](#dashboard-authorization)
- [過濾](#filtering)
    - [條目](#filtering-entries)
    - [Batches](#filtering-batches)
- [標籤](#tagging)
- [可用的監視者](#available-watchers)
    - [快取監視者](#cache-watcher)
    - [Command 監視者](#command-watcher)
    - [Dump 監視者](#dump-watcher)
    - [事件監視者](#event-watcher)
    - [例外監視者](#exception-watcher)
    - [Gate 監視者](#gate-watcher)
    - [Job 監視者](#job-watcher)
    - [Log 監視者](#log-watcher)
    - [郵件監視者](#mail-watcher)
    - [模型監視者](#model-watcher)
    - [Notification 監視者](#notification-watcher)
    - [Query 監視者](#query-watcher)
    - [Redis 監視者](#redis-watcher)
    - [Request 監視者](#request-watcher)
    - [Schedule 監視者](#schedule-watcher)

<a name="introduction"></a>
## 簡介

Laravel Telescope 是 Laravel 框架一個優雅的除錯工具。Telescope 提供對應用的請求，例外，log 紀錄，資料庫存取，佇列工作，郵件，提示，快取操作，排程任務，變數操作等等的剖析。

Telescope 在本地環境進行開發 Laravel 專案時，會是你的完美搭檔。

<p align="center">
<img src="https://res.cloudinary.com/dtfbvvkyp/image/upload/v1539110860/Screen_Shot_2018-10-09_at_1.47.23_PM.png" width="600">
</p>

<a name="installation"></a>
## 安裝

你可以用 Composer 在你的 Laravel 專案內安裝 Telescope：

    composer require laravel/telescope

安裝 Telescope 之後，用 `telescope:install` Artisan 指令來安裝。安裝之後，你還應該運行一次 `migrate` 指令：

    php artisan telescope:install

    php artisan migrate

#### 更新 Telescope

要更新 Telescope 時，你需要重新發布 Telescope 相關的資產：

    php artisan telescope:publish

### 只安裝在特定環境內

如果你只希望在本地開發時使用 Telescope 協助，你應該在安裝時加上 `--dev` flag：

    composer require laravel/telescope --dev

跑完 `telescope:install` 之後，你還應該從 `app` 的設置檔裡面移除對 `TelescopeServiceProvider` 的註冊，然後手動註冊，並加上針對環境的檢查：

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        if ($this->app->isLocal()) {
            $this->app->register(TelescopeServiceProvider::class);
        }
    }

<a name="migration-customization"></a>
### 客製化資料庫遷移

如果你不希望使用 Telescope 預設的資料庫遷移內容，那麼在 `AppServiceProvider` 使用 `register` 函式註冊服務時，應該呼叫 `Telescope::ignoreMigrations` 函式。

你可以 `php artisan vendor:publish --tag=telescope-migrations` 指令來匯出預設的資料庫遷移

<a name="configuration"></a>
### 設置

發布 Telescope 資產之後，主要的設置檔案會在 `config/telescope.php` 裡面。

這個設置檔可以用來設置監視器選項，每個選項前面都有說明用途，所以請好好研究這個檔案。

如果需要的話，你可以修改 `enabled` 設置來將 Telescope 資料收集功能完全停用。

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### 資料修整

沒有進行資料修整的話，`telescope_entries` 資料表會很快的累積大量資料。

要減輕這個問題，你可以在排程內每日運行 `telescope:prune` 指令：

    $schedule->command('telescope:prune')->daily();

預設上，所有超過 24 小時的資料都會被清除。你可以使用 `hours` 選項來決定要清除多久之前的 Telescope 資料。

舉例來說，下面的指令會刪除 48 小時之前的資料：

    $schedule->command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
## 儀表板認證

Telescope 會在 `/telescope` 這個網址裡面顯示儀表板。

預設上，你只能從 `local` 環境存取儀表板。不過在 `app/Providers/TelescopeServiceProvider.php` 檔案裡面有一個 `gate` 方法，可以控制在**非 local 環境**內存取的規則。你可以依據需求調整此函式來控制存取的權限：

    /**
     * Register the Telescope gate.
     *
     * This gate determines who can access Telescope in non-local environments.
     *
     * @return void
     */
    protected function gate()
    {
        Gate::define('viewTelescope', function ($user) {
            return in_array($user->email, [
                'taylor@laravel.com',
            ]);
        });
    }

<a name="filtering"></a>
## 過濾

<a name="filtering-entries"></a>
### 條目

你可以透過改變 `TelescopeServiceProvider` 上面 `filter` 函式參數裡的回呼函式 ，來過濾紀錄在 Telescope 上面的資料。

預設上，這個回呼函式紀錄 `local` 環境的所有資料，包含例外，失敗工作，排程任務，還有其他環境裡面有監視標籤的資料：

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::filter(function (IncomingEntry $entry) {
            if ($this->app->isLocal()) {
                return true;
            }

            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->hasMonitoredTag();
        });
    }

<a name="filtering-batches"></a>
### Batches

While the `filter` callback filters data for individual entries, you may use the `filterBatch` method to register a callback that filters all data for a given request or console command. If the callback returns `true`, all of the entries are recorded by Telescope:

    use Illuminate\Support\Collection;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::filterBatch(function (Collection $entries) {
            if ($this->app->isLocal()) {
                return true;
            }

            return $entries->contains(function ($entry) {
                return $entry->isReportableException() ||
                    $entry->isFailedJob() ||
                    $entry->isScheduledTask() ||
                    $entry->hasMonitoredTag();
                });
        });
    }

<a name="tagging"></a>
## 標籤

Telescope 允許你根據標籤搜尋條目。

Telescope allows you to search entries by "tag". Often, tags are Eloquent model class names or authenticated user IDs which Telescope automatically adds to entries. Occasionally, you may want to attach your own custom tags to entries. To accomplish this, you may use the `Telescope::tag` method. The `tag` method accepts a callback which should return an array of tags. The tags returned by the callback will be merged with any tags Telescope would automatically attach to the entry. You should call the `tag` method within your `TelescopeServiceProvider`:

    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::tag(function (IncomingEntry $entry) {
            if ($entry->type === 'request') {
                return ['status:'.$entry->content['response_status']];
            }

            return [];
        });
     }

<a name="available-watchers"></a>
## 可用的監視者

Telescope 監視者 gather application data when a request or console command is executed. You may customize the list of watchers that you would like to enable within your `config/telescope.php` configuration file:

    'watchers' => [
        Watchers\CacheWatcher::class => true,
        Watchers\CommandWatcher::class => true,
        ...
    ],

Some watchers also allow you to provide additional customization options:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 100,
        ],
        ...
    ],

<a name="cache-watcher"></a>
### 快取監視者

快取監視者紀錄存取快取成功（hit），存取失敗（miss），更新以及遺忘的紀錄。

<a name="command-watcher"></a>
### 命令監視者

The command watcher records the arguments, options, exit code, and output whenever an Artisan command is executed. If you would like to exclude certain commands from being recorded by the watcher, you may specify the command in the `ignore` option in your `config/telescope.php` file:

    'watchers' => [
        Watchers\CommandWatcher::class => [
            'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
            'ignore' => ['key:generate'],
        ],
        ...
    ],

<a name="dump-watcher"></a>
### dump 監視者

Telescope 的 dump 監視者紀錄並顯示所有的變數 dump 內容。

在 Laravel 專案內，變數可能會透過 `dump` 函式做顯示。
When using Laravel, variables may be dumped using the global `dump` function. The dump watcher tab must be open in a browser for the recording to occur, otherwise the dumps will be ignored by the watcher.

<a name="event-watcher"></a>
### 事件監視者

The event watcher records the payload, listeners, and broadcast data for any events dispatched by your application. The Laravel framework's internal events are ignored by the Event watcher.

<a name="exception-watcher"></a>
### 例外監視者

例外監視者紀錄並 stack trace 所有被拋出的例外

<a name="gate-watcher"></a>
### Gate Watcher

The gate watcher records the data and result of gate and policy checks by your application. If you would like to exclude certain abilities from being recorded by the watcher, you may specify those in the `ignore_abilities` option in your `config/telescope.php` file:

    'watchers' => [
        Watchers\GateWatcher::class => [
            'enabled' => env('TELESCOPE_GATE_WATCHER', true),
            'ignore_abilities' => ['viewNova'],
        ],
        ...
    ],

<a name="job-watcher"></a>
### 工作監視者

工作監視者紀錄已委派工作的資料和狀態。

<a name="log-watcher"></a>
### log 檔監視者

log 檔監視者紀錄所有對 log 檔的所有資料。

<a name="mail-watcher"></a>
### 郵件監視者

The mail watcher allows you to view an in-browser preview of the emails along with their associated data. You may also download the email as an `.eml` file.

<a name="model-watcher"></a>
### 模型監視者

模型監視者紀錄所有 Eloquent 模型的改變，像是 `created`, `updated`, `restored` 或 `deleted` 等事件的委派。

你可以用下面的方式編輯 `events` 選項，修改監視器應該紀錄的事件：

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
        ],
        ...
    ],

<a name="notification-watcher"></a>
### 提示監視者

提示監視者紀錄所有的提示。如果提示會觸發寄送郵件，而且有打開郵件監視者，信件可以從郵件監視者上監控並預覽信件內容。

<a name="query-watcher"></a>
### 佇列監視者

佇列（query）監視者 records the raw SQL, bindings, and execution time for all queries that are executed by your application. The watcher also tags any queries slower than 100ms as `slow`. You may customize the slow query threshold using the watcher's `slow` option:

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 50,
        ],
        ...
    ],

<a name="redis-watcher"></a>
### Redis 監視者

> {note} Redis events must be enabled for the Redis watcher to function. You may enable Redis events by calling `Redis::enableEvents()` in the `boot` method of your `app/Providers/AppServiceProvider.php` file.

Redis 監視者紀錄所有執行的 Redis 指令。如果你使用 Redis 做快取的話，快取的指令也會被 Redis 監視者紀錄。

<a name="request-watcher"></a>
### 請求監視者

The request watcher records the request, headers, session, and response data associated with any requests handled by the application. You may limit your response data via the `size_limit` (in KB) option:

    'watchers' => [
        Watchers\RequestWatcher::class => [
            'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
            'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
        ],
        ...
    ],

<a name="schedule-watcher"></a>
### 排程監視者

排程監視者紀錄排程任務的所有指令以及輸出資料。
