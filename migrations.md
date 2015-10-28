# 資料庫: 遷移

- [簡介](#introduction)
- [產生遷移](#generating-migrations)
- [遷移結構](#migration-structure)
- [執行遷移](#running-migrations)
    - [還原遷移](#rolling-back-migrations)
- [編寫遷移](#writing-migrations)
    - [建立資料表](#creating-tables)
    - [重新命名 / 刪除資料表](#renaming-and-dropping-tables)
    - [建立欄位](#creating-columns)
    - [修改欄位](#modifying-columns)
    - [刪除欄位](#dropping-columns)
    - [建立索引](#creating-indexes)
    - [刪除索引](#dropping-indexes)
    - [外鍵約束](#foreign-key-constraints)

<a name="introduction"></a>
## 簡介

遷移是一種資料庫的版本控制, 讓團隊能夠輕鬆的修改跟共享應用程式的資料庫模式。
遷移通常是 Laravel 搭配的結構生成器，讓您可以輕鬆的建立應用程式的資料庫架構。

Laravel 的結構生成器「Schema」，[facade](/docs/{{version}}/facades) 提供創建和操作表的資料庫相關支援，
它分享相同的表現，也是支援所有 Laravel 資料庫系統的 API。

<a name="generating-migrations"></a>
## 產生遷移

建立遷移, 使用 「make:migration」 [Artisan command](/docs/{{version}}/artisan):

    php artisan make:migration create_users_table

新的遷移檔將會放置在「database/migrations」資料夾內。
每個文件名都將包含 Laravel 自帶的時間戳記，用來確認遷移的順序。

「--table」和 「--create」選項可用來指定表內的操作或是用來創建新的表。
這些選項只要預先填入在生成表的遷移文件 :

    php artisan make:migration add_votes_to_users_table --table=users

    php artisan make:migration create_users_table --create=users

If you would like to specify a custom output path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The provided path should be relative to your application's base path.

<a name="migration-structure"></a>
## 遷移結構

遷移類包含兩個方法: 「up」和 「down」。
「up」方法是在資料庫內添加新的表、欄位、或索引，而「down」方法則是簡單的反向執行「up」方法。

在這兩個方法您必需使用 Laravel 建立出來的類別去創建跟修改表。
在此您可以使用這兩種方去讓 Laravel schema 結構生成器自動的創建或修改表。
例如 :  我們來產生一個 遷移 創建 `flights` 表 :
要瞭解所有的方法，可在結構生成器「Schema」內查看[check out its documentation](#creating-tables)

    <?php

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Database\Migrations\Migration;

    class CreateFlightsTable extends Migration
    {
        /**
         * Run the migrations.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->increments('id');
                $table->string('name');
                $table->string('airline');
                $table->timestamps();
            });
        }

        /**
         * Reverse the migrations.
         *
         * @return void
         */
        public function down()
        {
            Schema::drop('flights');
        }
    }


<a name="running-migrations"></a>
## 執行遷移

要運行所有未遷移過的應用程式，在 Artisan 的命令提示字元內使用 `migrate `指令。
如果您使用 [Homestead 虛擬主機](/docs/{{version}}/homestead)，只要執行下面的指令:

    php artisan migrate

如果您執行時出現 "class not found" 的錯誤，請試試運行完 `composer dump-autoload` 後再次執行一次。

#### 正式機上強制執行遷移

一些遷移的操作是有破壞性的，意思是它們可能會導致您失去資料。
為了保護您在資料庫內的資料，在正式機上執行這些命令之前將會提示您進行確認。
要執行命令而沒有任何的提示的狀況下運行，可在後面加入 `--force` :

    php artisan migrate --force

<a name="rolling-back-migrations"></a>
### 還原遷移

要還原遷移至上一個操作，使用 `rollback` 指令。
請注意，此還原是回復到上一次的"批次處理"，其中可能包括多筆的 遷移檔案:

    php artisan migrate:rollback

`migrate:reset` 指令將會還原到最初時的 遷移:

    php artisan migrate:reset

#### 在單個命令列內還原 / 執行遷移

`migrate:refresh` 命令將會還原至最初時的遷移後，再運行 `migrate` 指令。
此指令能有效的重新創建整個資料庫:

    php artisan migrate:refresh

    php artisan migrate:refresh --seed

<a name="writing-migrations"></a>
## 編寫遷移

<a name="creating-tables"></a>
### 創建資料表

創建一個新的資料表， 使用 `Schema` 結構生成器類別內 `create`方法。
`create`方法內需代入二個參數。
第一個參數代表資料表名稱，第二個參數代表一個 `Closure` 它接收一個 `Blueprint` 對象用來定義新的資料表:

    Schema::create('users', function ($table) {
        $table->increments('id');
    });

當創建新的表時，你可以使用任何的 schema 結構生成器[創建欄位](#creating-columns)去定義資料表欄位內容的屬性。

#### 表單 / 欄位存在檢查

您可以使用 `hasTable` 和 `hasColumn` 簡單的檢查表單或欄位存不存在:

    if (Schema::hasTable('users')) {
        //
    }

    if (Schema::hasColumn('users', 'email')) {
        //
    }

#### 連線 & 儲存引擎

如果您想要的一個資料庫連結，並不是默認的資料庫連結可使用 `connection` 方法指定連結方式:

    Schema::connection('foo')->create('users', function ($table) {
        $table->increments('id');
    });

設定資料表的儲存引擎，在schema 結構生成器上 設定 `engine`屬性:

    Schema::create('users', function ($table) {
        $table->engine = 'InnoDB';

        $table->increments('id');
    });

<a name="renaming-and-dropping-tables"></a>
### 重新命名 / 刪除資料表

重新命合資料表，使用 `rename` 方法:

    Schema::rename($from, $to);

刪除存在的資料表，您可使用 `drop` 或 `dropIfExists` 方法:

    Schema::drop('users');

    Schema::dropIfExists('users');

<a name="creating-columns"></a>
### 創建欄位

更新資料表，我們將使用 `Schema` 結構生成器內的 `table`方法。

像是 `create`方法，`table`方法接收二個參數， 第一個為資料表名稱和第二個為一個 `Closure` 它接收一個 `Blueprint` ，我們可以使用它新增表的欄位:

    Schema::table('users', function ($table) {
        $table->string('email');
    });

#### 可用的欄位狀態

schema 結構生成器包含許多欄位狀態，您能夠使用它們去創建您的資料表:

Command  | Description
------------- | -------------
`$table->bigIncrements('id');`  |  遞增的 ID（主鍵），使用相當於「UNSIGNED BIG INTEGER」的型態。
`$table->bigInteger('votes');`  |  相當於 BIGINT 型態。
`$table->binary('data');`  |  相當於 BLOB 型態。
`$table->boolean('confirmed');`  | 相當於 BOOLEAN 型態。
`$table->char('name', 4);`  | 相當於 CHAR 型態，並帶有長度。
`$table->date('created_at');`  |  相當於 DATE 型態。
`$table->dateTime('created_at');`  |  相當於 DATETIME 型態。
`$table->decimal('amount', 5, 2);`  |  相當於 DECIMAL 型態，並帶有精度與基數。
`$table->double('column', 15, 8);`  |  相當於 DOUBLE 型態，總共有 15 位數，在小數點後面有 8 位數。
`$table->enum('choices', ['foo', 'bar']);` | 相當於 ENUM 型態。
`$table->float('amount');`  |  相當於 FLOAT 型態。
`$table->increments('id');`  |  遞增的 ID (主鍵)，使用相當於「UNSIGNED INTEGER」的型態。
`$table->integer('votes');`  |  相當於 INTEGER 型態。
`$table->json('options');`  |  相當於 JSON 型態。
`$table->jsonb('options');`  |  相當於 JSONB 型態。
`$table->longText('description');`  |  相當於 LONGTEXT 型態。
`$table->mediumInteger('numbers');`  |  相當於 MEDIUMINT 型態。
`$table->mediumText('description');`  |  相當於 MEDIUMTEXT 型態。
`$table->morphs('taggable');`  |  加入整數 `taggable_id` 與字串 `taggable_type`。
`$table->nullableTimestamps();`  |  與 `timestamps()` 相同，但允許 NULL。
`$table->rememberToken();`  |  加入 `remember_token` 使用 VARCHAR(100) NULL。
`$table->smallInteger('votes');`  |  相當於 SMALLINT 型態。
`$table->softDeletes();`  |  加入 `deleted_at` 欄位於軟刪除使用。
`$table->string('email');`  |  相當於 VARCHAR 型態。
`$table->string('name', 100);`  |  相當於 VARCHAR 型態，並帶有長度。
`$table->text('description');`  |  相當於 TEXT 型態。
`$table->time('sunrise');`  |  相當於 TIME 型態。
`$table->tinyInteger('numbers');`  |  相當於 TINYINT 型態。
`$table->timestamp('added_on');`  |  相當於 TIMESTAMP 型態。
`$table->timestamps();`  |  加入 `created_at` 和 `pdated_at` 欄位。

#### 欄位修飾

除了上述的欄位類型，還有其它一些的欄位「修飾」，它們能增加至欄位。例如，若要在欄位增加「nullable」屬性，你可以使用 `nullable` 方法：

    Schema::table('users', function ($table) {
        $table->string('email')->nullable();
    });

以下清單為欄位內可用的修飾方法，此列表不包括[索引修飾](#creating-indexes)：

Modifier  | Description
------------- | -------------
`->first()`  |  將此欄位放置為第一個 (MySQL Only)
`->after('column')`  |  放置此欄位在某欄位名稱之後 (MySQL Only)
`->nullable()`  |  欄位允許NULL
`->default($value)`  |  設定欄位預設值為 $value
`->unsigned()`  |  設定欄位內容值為正整數

<a name="changing-columns"></a>
<a name="modifying-columns"></a>
### 修改欄位

#### 必要條件

在修正欄位之前, 在您的 `composer.json` 的檔案內必需先有 `doctrine/dbal` 套件。
此套件是用來產出要修正欄位指定的 SQL 語句。

#### 更新欄位屬性

有時候您需要修改一個存在的欄位，或修改欄位的屬性。例如：您可能想增加儲存文字欄位的長度。
藉由 change 方法讓這件事情變得非常容易，假設我們想要將欄位 name 的長度從 25 增加到 50 的時候：

    Schema::table('users', function ($table) {
        $table->string('name', 50)->change();
    });

另外也能將某個欄位修改為允許 NULL：

    Schema::table('users', function ($table) {
        $table->string('name', 50)->nullable()->change();
    });

<a name="renaming-columns"></a>
#### 修改欄位名稱

要修改欄位名稱，可在結構生成器內使用 renameColumn 方法，請確認在修改前 composer.json 檔案內已經加入 doctrine/dbal:

    Schema::table('users', function ($table) {
        $table->renameColumn('from', 'to');
    });

> **注意:** Renum 欄位型別現在不支援修改欄位名稱。

<a name="dropping-columns"></a>
### 移除欄位

要移除欄位，可在結構生成器內使用 dropColumn 方法:

    Schema::table('users', function ($table) {
        $table->dropColumn('votes');
    });

您可在方法內加入陣列，移除多筆資料欄位:

    Schema::table('users', function ($table) {
        $table->dropColumn(['votes', 'avatar', 'location']);
    });

> **注意:** 請確認在移除前 composer.json 檔案內已經加入 doctrine/dbal.

<a name="creating-indexes"></a>
### 加入索引

結構生成器支援多種索引類型，首先下面的例子為在欄位內的值應該是唯一值。
您可以在定義欄位時順便附加 `unique` 方法上去:

    $table->string('email')->unique();

您也可在創建完欄位後，另外加入。

例如:

    $table->unique('email');

你可在方法中加入一個陣列，創建一個複合索引:

    $table->index(['account_id', 'created_at']);

#### 支援的索引類型

Command  | Description
------------- | -------------
`$table->primary('id');`  |  加入主鍵 (primary key)。
`$table->primary(['first', 'last']);`  |  加入複合鍵 (composite keys)。
`$table->unique('email');`  |  加入唯一索引 (unique index)。
`$table->index('state');`  |  加入基本索引 (index)。

<a name="dropping-indexes"></a>
### 移除索引

若要移除索引，你必須指定索引名稱。預設中，Laravel 自動分配合理的名稱至索引。簡單地連結這些資料表名稱，索引的欄位名稱，及索引型別。舉例如下：

Command  | Description
------------- | -------------
`$table->dropPrimary('users_id_primary');`  |  從「users」資料表移除主鍵。
`$table->dropUnique('users_email_unique');`  |  從「users」資料表移除唯一索引。
`$table->dropIndex('geo_state_index');`  |  從「geo」資料表移除基本索引。

<a name="foreign-key-constraints"></a>
### 外鍵約束

Laravel 也支援資料表的外鍵約束, 這是用在資料庫型別的強制約束. 例如,
在 `posts` 表內有一個 `user_id` 欄位要強制約束到 `users` 表的 `id` 欄位 :

    Schema::table('posts', function ($table) {
        $table->integer('user_id')->unsigned();

        $table->foreign('user_id')->references('id')->on('users');
    });

您也可以指定選擇在「on delete」和「on update」進行約束動作：

    $table->foreign('user_id')
          ->references('id')->on('users')
          ->onDelete('cascade');

要移除外鍵，可使用 `dropForeign` 方法。外鍵的命名方式如同其他索引，所以我們可以使用 "_foreign" 將表名和欄位名做外鍵約束 :

    $table->dropForeign('posts_user_id_foreign');
