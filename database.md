# 資料庫： 快速入門

- [簡介](#introduction)
    - [設定](#configuration)
    - [分離讀寫的連接](#read-and-write-connections)
- [執行 SQL 語句](#running-queries)
    - [使用多個 SQL 連接](#using-multiple-database-connections)
    - [監聽查詢事件](#listening-for-query-events)
- [資料庫交易](#database-transactions)
- [連接到資料庫的 CLI](#connecting-to-the-database-cli)
- [Inspecting Your Databases](#inspecting-your-databases)
- [Monitoring Your Databases](#monitoring-your-databases)

<a name="introduction"></a>
## 簡介

幾乎所有的現代 Web 應用程式都需要和資料庫互動。 Laravel 用 [fluent query builder](/docs/{{version}}/queries) 和 [Eloquent ORM](/docs/{{version}}/eloquent) 來與受支援的資料庫進行互動，並使其變得異常簡單。現今，Laravel 提供五種資料庫的第一手支援：

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([版本原則](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([版本原則](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([版本原則](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([版本原則](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

<a name="configuration"></a>
### 設定

Laravel 的資料庫服務設定檔位於應用程式的 `config/database.php`。在這個檔案中，你可以定義所有的資料庫連接，並指定哪個連線應該要被當成預設值。此檔案的多數設定值取決於你應用程式的環境變數設定。同時，此檔案也提供了 Laravel 支援的大多資料庫的設定檔範例。

在預設情況下，Laravel簡易[環境變數](/docs/{{version}}/configuration#environment-configuration)已經可以和 [Laravel Sail](/docs/{{version}}/sail) 搭配使用，Laravel Sail 是一個可以直接架起本機開發狀態應用程式的 Docker 設定。 不過你也可以自由修改資料庫的設定檔以符合你本機的資料庫。

<a name="sqlite-configuration"></a>
#### SQLite 設定

SQLite 資料庫被包含在你的檔案系統上的一個檔案中。你可以在終端機用 `touch` 指令建立一個全新的 SQLite 資料庫： `touch database/database.sqlite`。資料庫被建立後，你可以輕鬆的在 `DB_DATABASE` 設定放置資料庫的絕對路徑：

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

要啟用 SQLite 的外鍵約束，你需要設定 `DB_FOREIGN_KEYS` 的環境變數為 `true`：

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 設定

要使用 Microsoft SQL Server 資料庫, 你需要確保 `sqlsrv` 和 `pdo_sqlsrv` 的 PHP 擴充功能和其他依賴已經安裝完成（例如 Microsoft SQL ODBC 驅動）。

<a name="configuration-using-urls"></a>
#### 用 URL 來進行設定

在傳統作法中，資料庫連接都是用 `host`、`database`、`username`、`password` 等設定值來設定。每個設定值都有它自己對應的環境變數。這表示當你要設定你生產環境伺服器的資料庫連線資訊時，你需要管理數個環境變數。

有些託管資料庫的提供商（如 AWS 和 Heroku）用單個字串提供一個資料庫 "URL"，並包含了所有資料庫的連接資訊。舉例來說資料庫 URL 可能看起來像下面這樣：

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

這些 URL 基本上遵照一個標準的結構慣例：

```html
driver://username:password@host:port/database?options
```

為了方便起見，Laravel 支援直接使用這些 URL 來替代數個設定。如果 `url`（或對應的 `DATABASE_URL` 環境變數） 的設定存在，它就會被用來解析資料庫連接和憑證資訊。

<a name="read-and-write-connections"></a>
### 分離讀寫的連接

有時你可能希望用一個資料庫連接來執行 SELECT 語句，另一個用來執行 INSERT、UPDATE 和 DELETE 語句。Laravel 讓它變得異常簡單，無論你使用的是原生查詢、 query builder 或是 Eloquent ORM 都將始終使用適當的連接。

來看看下面分離讀寫連接是怎麼設定的：

    'mysql' => [
        'read' => [
            'host' => [
                '192.168.1.1',
                '196.168.1.2',
            ],
        ],
        'write' => [
            'host' => [
                '196.168.1.3',
            ],
        ],
        'sticky' => true,
        'driver' => 'mysql',
        'database' => 'database',
        'username' => 'root',
        'password' => '',
        'charset' => 'utf8mb4',
        'collation' => 'utf8mb4_unicode_ci',
        'prefix' => '',
    ],

注意到 `read`、`write` 和 `sticky` 這三個索引鍵被加到設定的陣列中。`read` 和 `write` 這兩個索引鍵的陣列值裡面有單個 `host` 的索引鍵。`read` 和 `write` 的其他資料庫設定將會從主要的 `mysql` 設定陣列中合併進來。

如果你想要覆寫掉 `mysql` 設定陣列中的內容，你只需要把項目放置在 `read` 和 `write` 陣列中。所以在這個例子中，`192.168.1.1` 將會被用做 "讀取" 連接的 host，而 `192.168.1.3` 將會被用作 "寫入" 連接的 host。資料庫的憑證、前綴、字符集和其他在 `mysql` 設定陣列的設定將會在兩個連接中共享。當 `host` 的設定陣列中有複數個數值時，每個請求會在其中隨機選取一個來使用。

<a name="the-sticky-option"></a>
#### `sticky` 設定

`sticky` 是一個 *選用* 的數值，可用於允許立即讀取在當前請求週期中已寫入資料庫的記錄。如果 `sticky` 已啟用且 "寫入" 操作對資料庫來說在當前請求週期中已經執行，任何進一步的 "讀取" 操作都會用 "write" 連接執行。這確保在當前請求週期中已寫入的資料可以在同一個請求中立刻從資料庫中被讀回來。你可以自己決定這是否是你應用程式的預期行為。

<a name="running-queries"></a>
## 執行 SQL 語句

當你設定好你的資料庫連接後，你可以用 `DB` facade 來執行語句。`DB` facade 為每個類型的語句都提供了方法：`select`、`update`、`insert`、`delete` 和 `statement`。

<a name="running-a-select-query"></a>
#### 執行一個 Select 語句

要執行基本的 SELECT 語句，你可以用 `DB` facade 中的 `select` 方法：

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * 顯示一個有所有應用程式使用者的清單。
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

第一個傳遞給 `select` 方法的參數是 SQL 語句，而第二個參數是任何需要被綁定在語句中的參數綁定。一般來說，這些數值是 `where` 子句的約束。參數綁定提供了對 SQL 注入的保護措施。

`select` 方法總是回傳一個結果的 `array`。每個在這個陣列中的結果都會是一個用來表示來自資料庫的紀錄的 PHP `stdClass` 物件：

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### 搜尋標量數值

有時你的資料庫查詢可能拿到一個標量數值。Laravel 讓你用 `scalar` 方法直接取得數值，而不必從記錄物件中把標量的結果取出：

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="using-named-bindings"></a>
#### 使用名稱綁定

你可以用名稱綁定來執行查詢，而不用使用 `?` 來表示參數綁定：

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### 執行插入的語句

你可以用 `DB` facade 中的 `insert` 方法來執行 `insert` 語句。像 `select` 一樣，這個方法接受 SQL 查詢與參數綁定作為它的第一和第二個參數：

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### 執行更新的語句

`update` 方法應該用於更新資料庫中已存在的紀錄。此方法會回傳總共影響的列數：

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### 執行刪除的語句

`delete` 方法應該用在刪除資料庫中的紀錄。就像 `update` 一樣，它會回傳總影響的列數：

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### 執行一般的語句

有些資料庫語句不回傳任何數值。對這種類型的操作，你可以用 `DB` facade 中的 `statement` 方法：

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### 執行不需準備的語句

有時候你可能想執行一個沒有綁定任何述職的 SQL 語句。你可以用 `DB` 中的 `unprepared` 方法來達成：

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> **Warning**
> 因為不需準備的語句沒有綁定任何參數，它們可能會受到 SQL 注入的攻擊。你永遠不應該讓使用者可以自己控制此種語句其中的數值。

<a name="implicit-commits-in-transactions"></a>
#### 隱式提交

當在交易（transaction）中使用 `DB` facade 中的 `statement` 和 `unprepared` 方法時，你一定要小心避免語句造成[隱式提交](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。這些語句會導致資料庫引擎間接提交整個交易，讓 Laravel 不知道資料庫的交易階段。一個此類型語句的範例就是建立一個資料庫表：

    DB::unprepared('create table a (col varchar(1) null)');

請參考 MySQL 說明書中的 [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) 來了解哪些語句會觸發隱式提交。

<a name="using-multiple-database-connections"></a>
### 使用多個 SQL 連接

如果你的應用程式在 `config/database.php` 中定義了複數個資料庫連接，你可以用 `DB` facade 中的 `connection` 方法來存取每個連接。要傳遞給 `connection` 方法的連接名稱應該要對應到 `config/database.php` 或執行時其用 `config` helper 設定的其中一個連接：

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(/* ... */);

你可以用連接實體上的 `getPdo` 方法來存取連接底層的 PDO 實例：

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### 監聽查詢事件

如果你想要指定一個閉包在你應用程式 SQL 查詢執行時觸發，你可以用 `DB` facade 中的 `listen` 方法。這個方法在紀錄查詢或除錯時特別有用。你可以在 [service provider](/docs/{{version}}/providers) 的 `boot` 方法中註冊你的查詢監聽監聽器：

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 註冊任何應用程式的服務
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 任何服務的啟動程序
         *
         * @return void
         */
        public function boot()
        {
            DB::listen(function ($query) {
                // $query->sql;
                // $query->bindings;
                // $query->time;
            });
        }
    }

<a name="monitoring-cumulative-query-time"></a>
### Monitoring Cumulative Query Time

A common performance bottleneck of modern web applications is the amount of time they spend querying databases. Thankfully, Laravel can invoke a closure or callback of your choice when it spends too much time querying the database during a single request. To get started, provide a query time threshold (in milliseconds) and closure to the `whenQueryingForLongerThan` method. You may invoke this method in the `boot` method of a [service provider](/docs/{{version}}/providers):

    <?php

    namespace App\Providers;

    use Illuminate\Database\Connection;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            DB::whenQueryingForLongerThan(500, function (Connection $connection) {
                // Notify development team...
            });
        }
    }

<a name="database-transactions"></a>
## 資料庫交易

你可以在資料庫交易中用 `DB` facade 中的 `transaction`方法來執行一系列的操作。如果在交易的閉包中拋出了任何例外，交易會自動被退回且例外會被再次丟出。如果閉包執行成功，這個交易會被自動提交。當你使用 `transaction` 時你不需要擔心手動退回或提交：

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### 處理死結

`transaction` 方法接受一個選用的第二參數，它定義了交易在死結發生時應該嘗試的次數。當這些嘗試次數都用盡時，會拋出一個例外：

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### 手動使用交易

如果你想要手動開始一個交易且完全控制退回和提交，你可以使用 `DB` facade 中的 `beginTransaction` 方法：

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

你可以用 `rollBack` 方法來退回交易：

    DB::rollBack();

最後用 `commit` 方法來提交交易：

    DB::commit();

> **Note**  
> `DB` facade 中的 transaction 方法控制 [query builder](/docs/{{version}}/queries) 和 [Eloquent ORM](/docs/{{version}}/eloquent) 兩者的交易。

<a name="connecting-to-the-database-cli"></a>
## 連接到資料庫的 CLI

如果你想要連接到你的資料庫 CLI，你可以用 `db` Artisan 指令:

```shell
php artisan db
```

如果有需要，你也可以指定一個資料庫連接名稱連接到一個非預設的資料庫連接：

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## Inspecting Your Databases

Using the `db:show` and `db:table` Artisan commands, you can get valuable insight into your database and its associated tables. To see an overview of your database, including its size, type, number of open connections, and a summary of its tables, you may use the `db:show` command:

```shell
php artisan db:show
```

You may specify which database connection should be inspected by providing the database connection name to the command via the `--database` option:

```shell
php artisan db:show --database=pgsql
```

If you would like to include table row counts and database view details within the output of the command, you may provide the `--counts` and `--views` options, respectively. On large databases, retrieving row counts and view details can be slow:

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
#### Table Overview

If you would like to get an overview of an individual table within your database, you may execute the `db:table` Artisan command. This command provides a general overview of a database table, including its columns, types, attributes, keys, and indexes:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## Monitoring Your Databases

Using the `db:monitor` Artisan command, you can instruct Laravel to dispatch an `Illuminate\Database\Events\DatabaseBusy` event if your database is managing more than a specified number of open connections.

To get started, you should schedule the `db:monitor` command to [run every minute](/docs/{{version}}/scheduling). The command accepts the names of the database connection configurations that you wish to monitor as well as the maximum number of open connections that should be tolerated before dispatching an event:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

Scheduling this command alone is not enough to trigger a notification alerting you of the number of open connections. When the command encounters a database that has an open connection count that exceeds your threshold, a `DatabaseBusy` event will be dispatched. You should listen for this event within your application's `EventServiceProvider` in order to send a notification to you or your development team:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
                ->notify(new DatabaseApproachingMaxConnections(
                    $event->connectionName,
                    $event->connections
                ));
    });
}
```
