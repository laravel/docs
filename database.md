# 資料庫：入門

- [簡介](#introduction)
- [執行原始 SQL 查詢](#running-queries)
    - [監聽查詢事件](#listening-for-query-events)
- [資料庫交易](#database-transactions)
- [使用多資料庫連接](#accessing-connections)

<a name="introduction"></a>
## 簡介

Laravel 使得在各種資料庫後端系統進行連接與執行查詢變得非常簡單，無論是使用原始的 SQL、[流暢的查詢產生器](/docs/{{version}}/queries)，或是目前的 [Eloquent ORM](/docs/{{version}}/eloquent)。目前，Laravel 支援以下四種資料庫系統：

- MySQL
- Postgres
- SQLite
- SQL Server

<a name="configuration"></a>
### 設定

Laravel 使資料庫連線與執行查詢變得非常簡單。應用程式的資料庫的設定檔放置在 `config/database.php`。在這個設定檔內你可以定義所有的資料庫連接，以及指定預設使用哪個連接。在這個檔案內提供了所有支援的資料庫系統範例。

預設來說，Laravel 的[環境設定](/docs/{{version}}/installation#environment-configuration)範例是使用 [Laravel Homestead](/docs/{{version}}/homestead)，在開發 Laravel 時，這是相當便利的本機虛擬機器。當然，你可以因應需求隨時修改你本機端的資料庫設定。

<a name="read-write-connections"></a>
#### 讀取與寫入連接

有時候也許你會希望使用一個資料庫作為查詢，而另一個作為寫入、更新以及刪除。Laravel 使他變得輕而一舉，無論你使用原始查詢、查詢產生器或是 Eloquent ORM 都是可以使用的。

如何設定讀取與寫入的連接，讓我們看看這個例子：

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

注意，有兩個鍵加入了這個設定檔陣列內：`read` 及 `write`。這兩個鍵內包含了陣列，裡面也包含了一個單獨的鍵：`host`。`read` 及 `write` 連接的其他的資料庫設定選項將會合併在主要的 `mysql` 陣列內。

所以，如果需要在主要陣列內覆寫值，只需要在 `read` 及 `write` 陣列內放置設定參數。在這個例子中，`192.168.1.1`將被使用在「讀取」連接，而 `192.168.1.2` 將被使用在「寫入」連接。資料庫的憑證、前綴、編碼設定，以及所有其它的選項都存放在 `mysql` 陣列內，兩個連接將會共用這些選項。

<a name="running-queries"></a>
## 執行原始 SQL 查詢

一旦你設定好了資料庫連線，你可以使用 `DB` facade 進行查詢。`DB` facade 提供每個類型的查詢方法：`select`、`update`、`insert`、`delete`、`statement`。

#### 執行一個 Select 查詢

執行一個基本查詢，我們可以在 `DB` facade 使用 `select`：

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示應用程式中所有使用者的列表。
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

傳遞給 `select` 方法的第一個參數是原始 SQL 查詢，而第二個參數是任何查詢需要的參數綁定。通常，這些是 `where` 子句的限定值。參數綁定提供了保護，為防止 SQL 注入。

`select` 方法總是回傳結果的`陣列`。陣列中的每個結果將是一個 PHP `StdClass` 物件，讓你能夠存取結果的值：

    foreach ($users as $user) {
        echo $user->name;
    }

#### 使用命名綁定

除了使用 `?` 表示你的參數綁定外，你也可以使用命名綁定執行查詢：

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

#### 執行 Insert

若要執行 `insert` 語法，你可以在 `DB` facade 使用 `insert` 方法。如同 `select`，這個方法第一個參數是使用原始 SQL 查詢，第二個參數則是綁定：

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### 執行 Update

`update` 方法用於更新已經存在於資料庫的記錄。這個方法會回傳該語法影響的行數：

    $affected = DB::update('update users set votes = 100 where name = ?', ['John']);

#### 執行 Delete

`delete` 方法用於刪除已經存在於資料庫的記錄。如同 `update`，刪除的行數將會被回傳：

    $deleted = DB::delete('delete from users');

#### 執行一般語法

有時候一些資料庫操作不應該返回任何參數。對於這種類型的操作，你可以在 `DB` facade 使用 `statement` 方法：

    DB::statement('drop table users');

<a name="listening-for-query-events"></a>
### 監聽查詢事件

如果你希望能夠收到來自於你的應用程式每一筆 SQL 查詢，你可以使用 `listen` 方法。這個方法對於紀錄查詢跟除錯非常有用。你可以在[服務容器](/docs/{{version}}/providers)註冊你的查詢監聽器：

    <?php

    namespace App\Providers;

    use DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 啟動任何應用程式的服務。
         *
         * @return void
         */
        public function boot()
        {
            DB::listen(function($sql, $bindings, $time) {
                //
            });
        }

        /**
         * 註冊一個服務提供者。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

<a name="database-transactions"></a>
## 資料庫交易

要在資料庫交易中執行一組操作，你可以在 `DB` facade 使用 `transaction` 方法。如果在交易的`閉包`內拋出例外，交易會自動的被還原。如果`閉包`執行成功，交易將自動提交。你不需要擔心在使用 `transaction` 方法時手動還原或提交：

    DB::transaction(function () {
        DB::table('users')->update(['votes' => 1]);

        DB::table('posts')->delete();
    });

#### 手動操作交易

如果你想手動處理交易並且完全控制還原或提交，你可以在 `DB` facade 使用 `beginTransaction`：

    DB::beginTransaction();

你可以還原交易，透過 `rollBack` 方法：

    DB::rollBack();

最後，你可以提交這個交易，透過 `commit` 方法：

    DB::commit();

> **注意：**使用 `DB` facade 的交易方法也可以控制[查詢產生器](/docs/{{version}}/queries)及 [Eloquent ORM](/docs/{{version}}/eloquent) 的交易。

<a name="accessing-connections"></a>
## 使用多資料庫連接

當你使用多個連接，你可以使用 `DB` facade 的 `connection` 方法存取每個連線。傳遞給 `connection` 方法的 `name` 必須對應至 `config/database.php` 設定檔裡連接列表的其中一個：

    $users = DB::connection('foo')->select(...);

你也可以在連接的實例使用 `getPdo` 方法存取原始的底層 PDO 實例：

    $pdo = DB::connection()->getPdo();
