# 資料庫基本用法

- [設定](#configuration)
- [讀取 / 寫入 連線](#read-write-connections)
- [資料庫操作](#running-queries)
- [資料庫交易](#database-transactions)
- [存取連線](#accessing-connections)
- [資料庫操作紀錄](#query-logging)

<a name="configuration"></a>
## 設定

Laravel 讓資料庫連線與執行查詢語句變得相當簡單。資料庫設定檔位在 `app/config/database.php`。 您可以在此定義所需的資料庫連線，也可以指定哪一個連線是預設的。所有支援的資料庫類型與範例皆在檔案內說明。

目前為止 Laravel 支援 4 種資料庫系統: MySQL, Postgres, SQLite 和 SQL Server。

<a name="read-write-connections"></a>
## 讀取 / 寫入 連線

有時候您會需要使用一個資料庫進行查詢操作，另一個資料庫負責新增、修改和刪除操作。Laravel 使這件事變得輕而易舉,且會自動使用適當的連線，不論您是使用原生查詢、query builder 或是 Eloquent ORM。

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
## 資料庫操作

一但完成資料庫連線設定後，即可使用 `DB` 類別進行資料庫操作。

#### 查詢操作

	$results = DB::select('select * from users where id = ?', array(1));

方法 `select` 總是回傳陣列值。

#### 新增操作

	DB::insert('insert into users (id, name) values (?, ?)', array(1, 'Dayle'));

#### 修改操作

	DB::update('update users set votes = 100 where name = ?', array('John'));

#### 刪除操作

	DB::delete('delete from users');

> **注意:**  `修改` 和 `刪除` 會回傳該次操作影響到的筆數。

#### 一般性操作

	DB::statement('drop table users');

#### 聆聽資料庫操作事件

您可以使用 `DB::listen` 方法來聆聽資料庫操作事件:

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## 資料庫交易

執行資料庫交易中的一組操作，您可以使用 `transaction` 方法:

	DB::transaction(function()
	{
		DB::table('users')->update(array('votes' => 1));

		DB::table('posts')->delete();
	});

> **注意:** 在 `交易` 閉包內拋出的任何錯誤皆會導致交易自動回復上一步。

有時候您需要自行初始化一筆交易:

	DB::beginTransaction();

您可以使用 `rollback` 方法來將交易回復到上一步:

	DB::rollback();

最後，您可以藉由 `commit` 方法來提交一筆交易:

	DB::commit();

<a name="accessing-connections"></a>
## 存取連線

當使用多筆連線時，您可以藉由 `DB::connection` 方法存取它們:

	$users = DB::connection('foo')->select(...);

您也可以在底層 PDO 實體化之下存取原生查詢，

	$pdo = DB::connection()->getPdo();

有時候您會需要重新連線至某個資料庫:

	DB::reconnect('foo');

由於執行底層 PDO 實體化的 `最大連線數` 限制，若需要從某個資料庫斷開時，您可以使用 `disconnect` 方法:

	DB::disconnect('foo');

<a name="query-logging"></a>
## 資料庫操作紀錄

預設之下，Laravel 將現有連線請求的所有操作紀錄存放在記憶體中，然而，在某些情況下，像是插入一組大量紀錄時，這可能會導致應用程式使用內存過量。要將紀錄關閉，您可以使用 `disableQueryLog` 方法:

	DB::connection()->disableQueryLog();

要得到執行過的操作紀錄陣列，您可以使用 `getQueryLog` 方法:

       $queries = DB::getQueryLog();
