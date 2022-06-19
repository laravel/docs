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
#### Configuration Using URLs

Typically, database connections are configured using multiple configuration values such as `host`, `database`, `username`, `password`, etc. Each of these configuration values has its own corresponding environment variable. This means that when configuring your database connection information on a production server, you need to manage several environment variables.

Some managed database providers such as AWS and Heroku provide a single database "URL" that contains all of the connection information for the database in a single string. An example database URL may look something like the following:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

These URLs typically follow a standard schema convention:

```html
driver://username:password@host:port/database?options
```

For convenience, Laravel supports these URLs as an alternative to configuring your database with multiple configuration options. If the `url` (or corresponding `DATABASE_URL` environment variable) configuration option is present, it will be used to extract the database connection and credential information.

<a name="read-and-write-connections"></a>
### Read & Write Connections

Sometimes you may wish to use one database connection for SELECT statements, and another for INSERT, UPDATE, and DELETE statements. Laravel makes this a breeze, and the proper connections will always be used whether you are using raw queries, the query builder, or the Eloquent ORM.

To see how read / write connections should be configured, let's look at this example:

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

Note that three keys have been added to the configuration array: `read`, `write` and `sticky`. The `read` and `write` keys have array values containing a single key: `host`. The rest of the database options for the `read` and `write` connections will be merged from the main `mysql` configuration array.

You only need to place items in the `read` and `write` arrays if you wish to override the values from the main `mysql` array. So, in this case, `192.168.1.1` will be used as the host for the "read" connection, while `192.168.1.3` will be used for the "write" connection. The database credentials, prefix, character set, and all other options in the main `mysql` array will be shared across both connections. When multiple values exist in the `host` configuration array, a database host will be randomly chosen for each request.

<a name="the-sticky-option"></a>
#### The `sticky` Option

The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application.

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

