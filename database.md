# 資料庫： 快速入門

- [簡介](#introduction)
    - [設定](#configuration)
    - [分離讀寫的連接](#read-and-write-connections)
- [執行 SQL 語句](#running-queries)
    - [使用多個 SQL 連接](#using-multiple-database-connections)
    - [監聽查詢事件](#listening-for-query-events)
- [資料庫交易](#database-transactions)
- [連接到資料庫的 CLI](#connecting-to-the-database-cli)

<a name="introduction"></a>
## 簡介

幾乎所有的現代 Web 應用程式都需要和資料庫互動。 Laravel 用 [fluent query builder](/docs/{{version}}/queries) 和 [Eloquent ORM](/docs/{{version}}/eloquent) 來與受支援的資料庫進行互動，並使其變得異常簡單。現今，Laravel 提供五種資料庫的第一手支援：

<div class="content-list" markdown="1">

- MariaDB 10.2+ ([版本原則](https://mariadb.org/about/#maintenance-policy))
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

SQLite 資料庫被包含在你的檔案系統上的一個檔案中。你可以在終端機用 `touch` 指令建立一個全新的 SQLite 資料庫
： `touch database/database.sqlite`。資料庫被建立後，你可以輕鬆的在 `DB_DATABASE` 設定放置資料庫的絕對路徑：

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
## Running SQL Queries

Once you have configured your database connection, you may run queries using the `DB` facade. The `DB` facade provides methods for each type of query: `select`, `update`, `insert`, `delete`, and `statement`.

<a name="running-a-select-query"></a>
#### Running A Select Query

To run a basic SELECT query, you may use the `select` method on the `DB` facade:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * Show a list of all of the application's users.
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

The first argument passed to the `select` method is the SQL query, while the second argument is any parameter bindings that need to be bound to the query. Typically, these are the values of the `where` clause constraints. Parameter binding provides protection against SQL injection.

The `select` method will always return an `array` of results. Each result within the array will be a PHP `stdClass` object representing a record from the database:

    use Illuminate\Support\Facades\DB;

    $users = DB::select('select * from users');

    foreach ($users as $user) {
        echo $user->name;
    }

<a name="selecting-scalar-values"></a>
#### Selecting Scalar Values

Sometimes your database query may result in a single, scalar value. Instead of being required to retrieve the query's scalar result from a record object, Laravel allows you to retrieve this value directly using the `scalar` method:

    $burgers = DB::scalar(
        "select count(case when food = 'burger' then 1 end) as burgers from menu"
    );

<a name="using-named-bindings"></a>
#### Using Named Bindings

Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

<a name="running-an-insert-statement"></a>
#### Running An Insert Statement

To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method accepts the SQL query as its first argument and bindings as its second argument:

    use Illuminate\Support\Facades\DB;

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);

<a name="running-an-update-statement"></a>
#### Running An Update Statement

The `update` method should be used to update existing records in the database. The number of rows affected by the statement is returned by the method:

    use Illuminate\Support\Facades\DB;

    $affected = DB::update(
        'update users set votes = 100 where name = ?',
        ['Anita']
    );

<a name="running-a-delete-statement"></a>
#### Running A Delete Statement

The `delete` method should be used to delete records from the database. Like `update`, the number of rows affected will be returned by the method:

    use Illuminate\Support\Facades\DB;

    $deleted = DB::delete('delete from users');

<a name="running-a-general-statement"></a>
#### Running A General Statement

Some database statements do not return any value. For these types of operations, you may use the `statement` method on the `DB` facade:

    DB::statement('drop table users');

<a name="running-an-unprepared-statement"></a>
#### Running An Unprepared Statement

Sometimes you may want to execute an SQL statement without binding any values. You may use the `DB` facade's `unprepared` method to accomplish this:

    DB::unprepared('update users set votes = 100 where name = "Dries"');

> {note} Since unprepared statements do not bind parameters, they may be vulnerable to SQL injection. You should never allow user controlled values within an unprepared statement.

<a name="implicit-commits-in-transactions"></a>
#### Implicit Commits

When using the `DB` facade's `statement` and `unprepared` methods within transactions you must be careful to avoid statements that cause [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). These statements will cause the database engine to indirectly commit the entire transaction, leaving Laravel unaware of the database's transaction level. An example of such a statement is creating a database table:

    DB::unprepared('create table a (col varchar(1) null)');

Please refer to the MySQL manual for [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) that trigger implicit commits.

<a name="using-multiple-database-connections"></a>
### Using Multiple Database Connections

If your application defines multiple connections in your `config/database.php` configuration file, you may access each connection via the `connection` method provided by the `DB` facade. The connection name passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file or configured at runtime using the `config` helper:

    use Illuminate\Support\Facades\DB;

    $users = DB::connection('sqlite')->select(...);

You may access the raw, underlying PDO instance of a connection using the `getPdo` method on a connection instance:

    $pdo = DB::connection()->getPdo();

<a name="listening-for-query-events"></a>
### Listening For Query Events

If you would like to specify a closure that is invoked for each SQL query executed by your application, you may use the `DB` facade's `listen` method. This method can be useful for logging queries or debugging. You may register your query listener closure in the `boot` method of a [service provider](/docs/{{version}}/providers):

    <?php

    namespace App\Providers;

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
            DB::listen(function ($query) {
                // $query->sql;
                // $query->bindings;
                // $query->time;
            });
        }
    }

<a name="database-transactions"></a>
## Database Transactions

You may use the `transaction` method provided by the `DB` facade to run a set of operations within a database transaction. If an exception is thrown within the transaction closure, the transaction will automatically be rolled back and the exception is re-thrown. If the closure executes successfully, the transaction will automatically be committed. You don't need to worry about manually rolling back or committing while using the `transaction` method:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    });

<a name="handling-deadlocks"></a>
#### Handling Deadlocks

The `transaction` method accepts an optional second argument which defines the number of times a transaction should be retried when a deadlock occurs. Once these attempts have been exhausted, an exception will be thrown:

    use Illuminate\Support\Facades\DB;

    DB::transaction(function () {
        DB::update('update users set votes = 1');

        DB::delete('delete from posts');
    }, 5);

<a name="manually-using-transactions"></a>
#### Manually Using Transactions

If you would like to begin a transaction manually and have complete control over rollbacks and commits, you may use the `beginTransaction` method provided by the `DB` facade:

    use Illuminate\Support\Facades\DB;

    DB::beginTransaction();

You can rollback the transaction via the `rollBack` method:

    DB::rollBack();

Lastly, you can commit a transaction via the `commit` method:

    DB::commit();

> {tip} The `DB` facade's transaction methods control the transactions for both the [query builder](/docs/{{version}}/queries) and [Eloquent ORM](/docs/{{version}}/eloquent).

<a name="connecting-to-the-database-cli"></a>
## Connecting To The Database CLI

If you would like to connect to your database's CLI, you may use the `db` Artisan command:

```shell
php artisan db
```

If needed, you may specify a database connection name to connect to a database connection that is not the default connection:

```shell
php artisan db mysql
```

