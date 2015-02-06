# 資料庫使用基礎

- [設定](#configuration)
- [讀取/寫入連線](#read-write-connections)
- [執行查詢](#running-queries)
- [資料庫交易](#database-transactions)
- [取用連線](#accessing-connections)
- [查詢日誌紀錄](#query-logging)

<a name="configuration"></a>
## 設定

Laravel 讓連結資料庫和執行查詢變得相當容易。資料庫相關設定檔案都在 `config/database.php`。 在這個檔案你可以定義所有的資料庫連線，以及指定預設的資料庫連線。預設檔案中已經有所有支援的資料庫系統範例了。

目前 Laravel 支援四種資料庫系統： MySQL、Postgres、SQLite、以及 SQL Server。

<a name="read-write-connections"></a>
## 讀取/寫入連線

有時候你可能希望使用特定資料庫連線進行 SELECT 操作，同時使用另外的連線作 INSERT 、 UPDATE 、以及 DELETE 。 Laravel 讓這些變得輕鬆簡單，並確保你不論在使用原始查詢、查詢建立器、或者是 Eloquent ORM 使用的都是正確的連線。

來看看如何設定讀取/寫入連線，讓我們來看以下的範例：

	'mysql' => [
		'read' => [
			'host' => '192.168.1.1',
		],
		'write' => [
			'host' => '196.168.1.2'
		],
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	],

注意我們加了兩個鍵值到設定檔陣列中： `read` 及 `write`。 兩個鍵值都包含了單一鍵值的陣列：`host`。`read` 及 `write` 的其餘資料庫設定會從`mysql` 陣列中合併。 所以，如果我們想要覆寫設定值，只要將選項放入 `read` 和 `write` 陣列即可。 所以在上面的例子裡， `192.168.1.1` 將被用作「讀取」連線，而 `192.168.1.2` 將被用作「寫入」連線。資料庫憑證、 前綴、字元編碼設定、以及其他所有的設定會共用 `mysql` 陣列裡的設定。

<a name="running-queries"></a>
## 執行查詢

如果設定好資料庫連線，就可以透過 `DB` facade 執行查詢。

#### 執行 Select 查詢

	$results = DB::select('select * from users where id = ?', [1]);

`select` 方法會回傳一個 `array` 結果。

#### 執行 Insert 語法

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### 執行 Update 語法

	DB::update('update users set votes = 100 where name = ?', ['John']);

#### 執行 Delete 語法

	DB::delete('delete from users');

> **注意：** `update` 和 `delete` 語法會回傳在操作中所影響的資料筆數。

#### 執行一般語法

	DB::statement('drop table users');

#### 監聽查詢事件

你可以使用 `DB::listen` 方法，去監聽查詢的事件：

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## 資料庫交易

你可以使用 `transaction` 方法，去執行一組資料庫交易的操作：

	DB::transaction(function()
	{
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

> **注意：** 在 `transaction` 閉包若拋出任何例外會導致交易自動還原 。

有時候你可能需要自己開始一個交易：

	DB::beginTransaction();

你可以透過 `rollback` 的方法還原交易：

	DB::rollback();

最後，你可以透過 `commit` 的方法提交交易：

	DB::commit();

<a name="accessing-connections"></a>
## 取用連線

若要使用多個連線，可以透過 `DB::connection` 方法取用：

	$users = DB::connection('foo')->select(...);

你也可以取用原始底層的 PDO 實例：

	$pdo = DB::connection()->getPdo();

有時候你可能需要重新連線到特定的資料庫：

	DB::reconnect('foo');

如果你因為超過了底層 PDO 實例的 `max_connections` 的限制，需要關閉特定的資料庫連線，可以透過 `disconnect` 方法:

	DB::disconnect('foo');

<a name="query-logging"></a>
## 查詢日誌記錄

預設情況下，Laravel 會在記憶體裡存取這次請求中所有的查詢語句。然而，在有些例子下，比如一次新增 大量的資料，可能會導致應用程式耗損過多記憶體。 如果要禁用日誌，可以使用 `disableQueryLog` 方法：

	DB::connection()->disableQueryLog();

要得到執行過的查詢紀錄陣列，你可以使用 `getQueryLog` 方法：

       $queries = DB::getQueryLog();
