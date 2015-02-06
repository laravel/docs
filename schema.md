# 結構生成器

- [介紹](#introduction)
- [建立與刪除資料表](#creating-and-dropping-tables)
- [加入欄位](#adding-columns)
- [修改欄位](#changing-columns)
- [修改欄位名稱](#renaming-columns)
- [移除欄位](#dropping-columns)
- [檢查是否存在](#checking-existence)
- [加入索引](#adding-indexes)
- [外鍵](#foreign-keys)
- [移除索引](#dropping-indexes)
- [移除時間戳記和軟刪除](#dropping-timestamps)
- [儲存引擎](#storage-engines)

<a name="introduction"></a>
## 介紹

Laravel 的結構生成器 (`Schema`) 提供一個與資料庫無關的資料表產生方法，它可以很好的處理 Laravel 支援的各種資料庫類型，並且在不同系統間提供一致性的 API 操作。

<a name="creating-and-dropping-tables"></a>
## 建立與刪除資料表

要建立一個新的資料表，可使用 `Schema::create` 方法：

	Schema::create('users', function($table)
	{
		$table->increments('id');
	});

傳入 `create` 方法的第一個參數是資料表名稱，第二個參數是 `Closure` 並接收 `Blueprint` 物件被用來定義新的資料表。

要修改資料表名稱，可使用 `rename` 方法：

	Schema::rename($from, $to);

要指定特定連線來操作，可使用 `Schema::connection` 方法：

	Schema::connection('foo')->create('users', function($table)
	{
		$table->increments('id');
	});

要移除資料表，可使用 `Schema::drop` 方法：

	Schema::drop('users');

	Schema::dropIfExists('users');

<a name="adding-columns"></a>
## 加入欄位

更新現有的資料表，可使用 `Schema::table` 方法：

	Schema::table('users', function($table)
	{
		$table->string('email');
	});

資料表產生器提供多種欄位型態可使用，在您建立資料表時也許會用到：

指令  | 功能描述
------------- | -------------
`$table->bigIncrements('id');`  |  ID 自動增量，使用相當於「big integer」型態
`$table->bigInteger('votes');`  |  相當於 BIGINT 型態
`$table->binary('data');`  |  相當於 BLOB 型態
`$table->boolean('confirmed');`  |  相當於 BOOLEAN 型態
`$table->char('name', 4);`  |  相當於 CHAR 型態，並帶有長度
`$table->date('created_at');`  |  相當於 DATE 型態
`$table->dateTime('created_at');`  |  相當於 DATETIME 型態
`$table->decimal('amount', 5, 2);`  |  相當於 DECIMAL 型態，並帶有精度與基數
`$table->double('column', 15, 8);`  |  相當於 DOUBLE 型態，總共有 15 位數，在小數點後面有 8 位數
`$table->enum('choices', array('foo', 'bar'));` | 相當於 ENUM 型態
`$table->float('amount');`  |  相當於 FLOAT 型態
`$table->increments('id');`  |  相當於 Incrementing 型態 (資料表主鍵)
`$table->integer('votes');`  |  相當於 INTEGER 型態
`$table->json('options');`  |  相當於 JSON 型態
`$table->longText('description');`  |  相當於 LONGTEXT 型態
`$table->mediumInteger('numbers');`  |  相當於 MEDIUMINT 型態
`$table->mediumText('description');`  |  相當於 MEDIUMTEXT 型態
`$table->morphs('taggable');`  |  加入整數 `taggable_id` 與字串 `taggable_type`
`$table->nullableTimestamps();`  |  與 `timestamps()` 相同，但允許 NULL
`$table->smallInteger('votes');`  |  相當於 SMALLINT 型態
`$table->tinyInteger('numbers');`  |  相當於 TINYINT 型態
`$table->softDeletes();`  |  加入 **deleted\_at** 欄位於軟刪除使用
`$table->string('email');`  |  相當於 VARCHAR 型態
`$table->string('name', 100);`  |  相當於 VARCHAR 型態，並指定長度
`$table->text('description');`  |  相當於 TEXT 型態
`$table->time('sunrise');`  |  相當於 TIME 型態
`$table->timestamp('added_on');`  |  相當於 TIMESTAMP 型態
`$table->timestamps();`  |  加入 **created\_at** 和 **updated\_at** 欄位
`$table->rememberToken();`  |  加入 `remember_token` 使用 VARCHAR(100) NULL
`->nullable()`  |  標示此欄位允許 NULL
`->default($value)`  |  宣告此欄位的預設值
`->unsigned()`  |  設定整數是無分正負

#### 在 MySQL 使用 After 方法

若您使用 MySQL 資料庫，您可以使用 `after` 方法來指定欄位的順序：

	$table->string('name')->after('email');

<a name="changing-columns"></a>
## 修改欄位

有時候您需要修改一個存在的欄位，例如：您可能想增加儲存文字欄位的長度。藉由 `change` 方法讓這件事情變得非常容易！假設我們想要將欄位 `name` 的長度從 25 增加到 50 的時候：

	Schema::table('users', function($table)
	{
		$table->string('name', 50)->change();
	});

另外也能將某個欄位修改為允許 NULL：

	Schema::table('users', function($table)
	{
		$table->string('name', 50)->nullable()->change();
	});

<a name="renaming-columns"></a>
## 修改欄位名稱

要修改欄位名稱，可在結構生成器內使用 `renameColumn` 方法，請確認在修改前 `composer.json` 檔案內已經加入 `doctrine/dbal`。

	Schema::table('users', function($table)
	{
		$table->renameColumn('from', 'to');
	});

> **注意:** `enum` 欄位型別不支援修改欄位名稱。

<a name="dropping-columns"></a>
## 移除欄位

要移除欄位，可在結構生成器內使用 `dropColumn` 方法，請確認在移除前 `composer.json` 檔案內已經加入 `doctrine/dbal`。

#### 移除資料表欄位

	Schema::table('users', function($table)
	{
		$table->dropColumn('votes');
	});

#### 移除資料表多筆欄位

	Schema::table('users', function($table)
	{
		$table->dropColumn(array('votes', 'avatar', 'location'));
	});

<a name="checking-existence"></a>
## 檢查是否存在

#### 檢查資料表是否存在

您可以輕鬆的檢查資料表或欄位是否存在，使用 `hasTable` 和 `hasColumn` 方法：

	if (Schema::hasTable('users'))
	{
		//
	}

#### 檢查欄位是否存在

	if (Schema::hasColumn('users', 'email'))
	{
		//
	}

<a name="adding-indexes"></a>
## 加入索引

結構生成器支援多種索引類型，有兩種方法可以加入，方法一，您可以在定義欄位時順便附加上去，或者是分開另外加入：

	$table->string('email')->unique();

或者，您可以獨立一行來加入索引，以下是支援的索引類型：

指令  | 功能描述
------------- | -------------
`$table->primary('id');`  |  加入主鍵 (primary key)
`$table->primary(array('first', 'last'));`  |  加入複合鍵 (composite keys)
`$table->unique('email');`  |  加入唯一索引 (unique index)
`$table->index('state');`  |  加入基本索引 (index)

<a name="foreign-keys"></a>
## 外鍵

Laravel 也支援資料表的外鍵約束：

	$table->integer('user_id')->unsigned();
	$table->foreign('user_id')->references('id')->on('users');

範例中，我們關注欄位 `user_id` 參照到 `users` 資料表的 `id` 欄位。請先確認已經建立外鍵！

您也可以指定選擇在「on delete」和「on update」進行約束動作：

	$table->foreign('user_id')
          ->references('id')->on('users')
          ->onDelete('cascade');

要移除外鍵，可使用 `dropForeign` 方法。外鍵的命名約定如同其他索引：

	$table->dropForeign('posts_user_id_foreign');

> **注意:** 當外鍵有參照到自動增量時，記得設定外鍵為 `unsigned` 型態。

<a name="dropping-indexes"></a>
## 移除索引

要移除索引您必須指定索引名稱，Laravel 預設有脈絡可循的索引名稱。簡單地連結這些資料表與索引的欄位名稱和型別。舉例如下：

指令  | 功能描述
------------- | -------------
`$table->dropPrimary('users_id_primary');`  |  從「users」資料表移除主鍵
`$table->dropUnique('users_email_unique');`  |  從「users」資料表移除唯一索引
`$table->dropIndex('geo_state_index');`  |  從「geo」資料表移除基本索引

<a name="dropping-timestamps"></a>
## 移除時間戳記和軟刪除

要移除 `timestamps`、`nullableTimestamps` 或 `softDeletes` 欄位型態，您可以使用以下方法：

指令  | 功能描述
------------- | -------------
`$table->dropTimestamps();`  |  移除 **created\_at** 和 **updated\_at** 欄位
`$table->dropSoftDeletes();`  |  移除 **deleted\_at** 欄位

<a name="storage-engines"></a>
## 儲存引擎

要設定資料表的儲存引擎，可在結構生成器設定 `engine` 屬性：

    Schema::create('users', function($table)
    {
        $table->engine = 'InnoDB';

        $table->string('email');
    });
