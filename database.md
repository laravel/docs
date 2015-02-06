# 資料庫使用基礎

- [配置](#configuration)
- [讀取 / 寫入 連接](#read-write-connections)
- [執行查詢](#running-queries)
- [資料庫交易](#database-transactions)
- [存取連接](#accessing-connections)
- [查詢日誌紀錄](#query-logging)

<a name="configuration"></a>
## 設置

Laravel 讓連結資料庫和執行查尋變得相當容易。 資料庫相關設定檔案都在 `config/database.php`。 在這個檔案你可以定義你所有的資料庫連線， 以及指定資料庫在預設情況下應該使用哪個連線並提供所有支援的資料庫系統的範例。

目前 Laravel 支援四種資料庫系統： **MySQL**、**Postgres**、**SQLite**、以及 **SQL Server**。

<a name="read-write-connections"></a>
## 讀取 / 寫入 連接資料庫

有時候你可能希望連接資料庫並使用 **SELECT** 語法或者是其他 **INSERT**、**UPDATE**、以及 **DELETE** 語法。 **Laravel** 讓這些變得輕鬆簡單，並使用正確的連接，不論你使用原始查詢、查詢建立器、或者是 **Eloquent ORM**。

來看看如何 讀取 / 寫入 連結資料庫應該如何設置，讓我們來看以下的範例：

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

請注意兩個 key 值已經被加到配置陣列： `read` 及 `write`。 這兩個 key 值(read、write)都包含了一個 key 值陣列值：`host`。 其餘的資料庫選項 `read` 及 `write` 會在連接資料庫被 `mysql` 陣列合併。 所以，如果我們想要重寫主陣列中的值，只要將選項放入在 `read` 和 `write` 陣列。 所以在這個情況下， `192.168.1.1` 將被用作 "讀取" 連接，而 `192.168.1.2` 將被用作 "寫入" 連接。 資料庫憑證、 前綴、 字元編碼設定、 以及其他所有的設定在 `mysql` 陣列將會在連接之間共用。

<a name="running-queries"></a>
## 執行查詢

如果設置好你的資料庫連接，就可以執行查詢使用 `DB` **facade**。


#### 執行 Select 查詢

	$results = DB::select('select * from users where id = ?', [1]);

`select` 將會回傳一個 `array` 結果。

#### 執行 Insert 語法

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### 執行 Update 語法

	DB::update('update users set votes = 100 where name = ?', ['John']);

#### 執行 Delete 語法

	DB::delete('delete from users');

> **注意：** `update` 和 `delete` 語法會回傳在操作中所影響的資料筆數。

#### 執行一般語法

	DB::statement('drop table users');

#### 聆聽查詢事件

你可以使用 `DB::listen` 方法，去聆聽查詢的事件：

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

> **注意：** 在 `transaction` 閉包內發生的任何異常將會自動返回原本的交易。

有時候你可能需要自己開始一個交易：

	DB::beginTransaction();

你可以透過 `rollback` 方法去返回你的交易：

	DB::rollback();

最後，你可以透過 `commit` 方法去提交你的交易：

	DB::commit();

<a name="accessing-connections"></a>
## 存取連接

當你使用多個連接，可以透過 `DB::connection` 的方法，去存取他們：

	$users = DB::connection('foo')->select(...);

你也可以訪問原始，基本 **PDO** 的例子：

	$pdo = DB::connection()->getPdo();

有時後你可能需要重新連接到給定的資料庫：

	DB::reconnect('foo');

因為超過了 **PDO** 實例下 `max_connections` 的限制，需要斷開連線從給定的資料庫，你可以透過 `disconnect` 的方法:

	DB::disconnect('foo');

<a name="query-logging"></a>
## 查詢日誌記錄

預設情況下，**Laravel** 會保留日誌為目前要求執行的所有查詢的記憶體。 然而，在有些例子下，像 Insert 大量的語句，這會導致應用程式使用過多記憶體。 如果要禁用日誌，你可以使用 `disableQueryLog` 的方法：

	DB::connection()->disableQueryLog();

獲取陣列執行的查詢，你可以使用 `getQueryLog` 的方法：

       $queries = DB::getQueryLog();
