# 資料庫基本用法

- [設定](#configuration)
- [讀取 / 寫入 連線](#read-write-connections)
- [Running Queries](#running-queries)
- [Database Transactions](#database-transactions)
- [Accessing Connections](#accessing-connections)
- [Query Logging](#query-logging)

<a name="configuration"></a>
## 設定

Laravel 讓資料庫連線與執行查詢語句變得相當簡單。資料庫設定檔位在 `app/config/database.php`。 您可以在此定義所需的資料庫連線，也可以指定哪一個連線是預設的。所有支援的資料庫類型與範例皆在檔案內說明。

目前為止 Laravel 支援 4 種資料庫系統: MySQL, Postgres, SQLite 和 SQL Server。

<a name="read-write-connections"></a>
## 讀取 / 寫入 連線

有時候您會需要使用一個資料庫進行 SELECT 操作，另一個資料庫負責 INSERT, UPDATE 和 DELETE 操作。Laravel 使這件事變得輕而易舉,且會自行使用適當的連線，不論您是使用 raw 查詢、query builder 或是 Eloquent ORM。

要了解如何設定 讀取 / 寫入 連線, 請看以下範例:

	'mysql' => array(
		'read' => array(
			'host' => '192.168.1.1',
		),
		'write' => array(
			'host' => '196.168.1.2'
		),
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	),

注意到有兩個鍵值 `read` 和 `write` 已經被加到設定陣列中。這兩個鍵值都包含一個關鍵數值組 `host`。 而資料庫 `read` 和 `write`的其他選項將會併入 `mysql` 的主要陣列值內。所以,我們只需要取代 `read` 和 `write` 陣列，如果我們想要複寫主要陣列的值。因此，以這個範例來看 `192.168.1.1` 將會被當作 `讀取` 連線，`192.168.1.2` 將會被當作 `寫入` 連線。該資料庫的憑證、前綴詞、字元集和所有其他在 `mysql` 陣列內的選項將會被兩個連線內共享。

<a name="running-queries"></a>
## Running Queries

Once you have configured your database connection, you may run queries using the `DB` class.

#### Running A Select Query

	$results = DB::select('select * from users where id = ?', array(1));

The `select` method will always return an `array` of results.

#### Running An Insert Statement

	DB::insert('insert into users (id, name) values (?, ?)', array(1, 'Dayle'));

#### Running An Update Statement

	DB::update('update users set votes = 100 where name = ?', array('John'));

#### Running A Delete Statement

	DB::delete('delete from users');

> **Note:** The `update` and `delete` statements return the number of rows affected by the operation.

#### Running A General Statement

	DB::statement('drop table users');

#### Listening For Query Events

You may listen for query events using the `DB::listen` method:

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## Database Transactions

To run a set of operations within a database transaction, you may use the `transaction` method:

	DB::transaction(function()
	{
		DB::table('users')->update(array('votes' => 1));

		DB::table('posts')->delete();
	});

> **Note:** Any exception thrown within the `transaction` closure will cause the transaction to be rolled back automatically.

Sometimes you may need to begin a transaction yourself:

	DB::beginTransaction();

You can rollback a transaction via the `rollback` method:

	DB::rollback();

Lastly, you can commit a transaction via the `commit` method:

	DB::commit();

<a name="accessing-connections"></a>
## Accessing Connections

When using multiple connections, you may access them via the `DB::connection` method:

	$users = DB::connection('foo')->select(...);

You may also access the raw, underlying PDO instance:

	$pdo = DB::connection()->getPdo();

Sometimes you may need to reconnect to a given database:

	DB::reconnect('foo');

If you need to disconnect from the given database due to exceeding the underlying PDO instance's `max_connections` limit, use the `disconnect` method:

	DB::disconnect('foo');

<a name="query-logging"></a>
## Query Logging

By default, Laravel keeps a log in memory of all queries that have been run for the current request. However, in some cases, such as when inserting a large number of rows, this can cause the application to use excess memory. To disable the log, you may use the `disableQueryLog` method:

	DB::connection()->disableQueryLog();

To get an array of the executed queries, you may use the `getQueryLog` method:

       $queries = DB::getQueryLog();
