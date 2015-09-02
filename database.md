# Database: Getting Started

- [簡介](#introduction)
- [執行原始SQL查詢](#running-queries)
    - [監聽 Query 事件](#listening-for-query-events)
- [資料庫交易](#database-transactions)
- [使用多資料庫連接](#accessing-connections)

<a name="introduction"></a>
## 簡介

Laravel使資料庫連接與執行查詢變得非常簡單，無論是使用原始SQL[fluent query builder](/docs/{{version}}/queries)，或是目前的[Eloquent ORM](/docs/{{version}}/eloquent)，
Laravel支援以下的資料庫系統:

- MySQL
- Postgres
- SQLite
- SQL Server

<a name="configuration"></a>
### 設定

Laravel使資料庫連線與執行查詢變得非常簡單。資料庫的設定檔存放在`config/database.php`。在這個設定檔內你可以定義所有關於你的資料庫連線，以及可以指定哪個連線成爲預設值。在這個檔案內提供了所有資料庫系統的設定檔範例。

Laravel預設環境[environment configuration](/docs/{{version}}/installation#environment-configuration)是使用[Laravel Homestead](/docs/{{version}}/homestead)作為預設，在開發Laravel時，這是相當便利的本地虛擬機。當然，你可以因應需求隨時修改你本地端的資料庫設定。

<a name="read-write-connections"></a>
#### 讀 / 寫 連線

有時候也許你會希望使用一個資料庫作為查詢，而另一個作為寫入、更新以及刪除。Laravel使他變得輕而一舉，，無論你使用原始查詢、Query Builder或是Eloquent ORM都是可以使用的。

如何去設定讀 / 寫連接，看看這個例子:

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

注意有兩個鍵加入了這個設定檔陣列內:`read` and `write`。並且這兩個鍵內包含了陣列，裡面也包含了一個單獨的鍵:`host`。其他的資料庫設定選項將會合併在主要的`mysql`陣列內。

所以，如果需要在主要陣列內覆寫值，只需要在`read` and `write`陣列內放置設定參數。在這個例子中，`192.168.1.1`將被使用在"讀"連接，而`192.168.1.2`將被使用在"寫"連接。資料庫的憑證，前綴，編碼設定，以及所有額外的選項都存放在`mysql`陣列內，他會把設定分享給所有的連接使用。

<a name="running-queries"></a>
## 執行原始SQL查詢

一旦你配置好了資料庫連線，你可以使用`DB` facade進行查詢。`DB` facade 提供每個類型的查詢方法:`select`, `update`, `insert`, `delete`, and `statement`。

#### 執行一個 Select 查詢

執行一個基本查詢，我們可以在`DB` facade使用`select`:

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show a list of all of the application's users.
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::select('select * from users where active = ?', [1]);

            return view('user.index', ['users' => $users]);
        }
    }

傳遞給`select`方法的第一個參數是原始SQL查詢，而第二個參數是任何參數綁定需要的查詢。通常，這些`where`是條件限定值。參數綁定提供了保護，防止SQL注入。

`select`方法總是返回結果的`array`。陣列中的每個結果將是一個PHP`StdClass`物件，允許您存取結果的值：

    foreach ($users as $user) {
        echo $user->name;
    }

#### 使用命名綁定

代替使用`?`去表示你的參數綁定，你可以使用命名綁定執行查詢:

    $results = DB::select('select * from users where id = :id', ['id' => 1]);

#### 執行 Insert

你可以在`DB` facade使用`insert`方法執行`insert`。像`select`，這個方法第一個參數是使用原始SQL查詢，並且綁定第二個參數:

    DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### 執行 Update

`update`方法用於更新已經存在於資料庫的記錄。影響的行將被這個方法返回。

    $affected = DB::update('update users set votes = 100 where name = ?', ['John']);

#### 執行 Delete

`delete`方法用於刪除已經存在於資料庫的記錄。像是`update`，影響的行將被這個方法返回。

The `delete` method should be used to delete records from the database. Like `update`, the number of rows deleted will be returned:

    $deleted = DB::delete('delete from users');

#### 執行一般性操作

有時候一些資料庫操作不應該返回任何參數。對於這種類型的操作，你可以在`DB` facade使用`statement`方法。

    DB::statement('drop table users');

<a name="listening-for-query-events"></a>
### 監聽查詢事件

如果你希望能夠收到來自於你的應用程式每一筆SQL查詢，你可以使用`listen`方法。這個方法對於紀錄查詢跟除錯非常有用。你可以在[service provider](/docs/{{version}}/providers)註冊你的查詢監聽:

    <?php

    namespace App\Providers;

    use DB;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
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
         * Register the service provider.
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

要在資料庫中運行的一組操作，你可以在`DB` facade使用`transaction`方法。如果交易發生異常將會拋出`Closure`，交易將自動返回。如果`Closure`執行成功，交易將自動提交，你不需要擔心使用`transaction`方法手動返回或提交，:

    DB::transaction(function () {
        DB::table('users')->update(['votes' => 1]);

        DB::table('posts')->delete();
    });

#### 手動操作交易

如果你想手動處理交易並且完全控制返回或提交，你可以在`DB` facade使用`beginTransaction`:

    DB::beginTransaction();

你可以返回交易，透過`rollBack`方法:

    DB::rollBack();

最後，你可以提交這個交易，透過`commit`方法:

    DB::commit();

> **Note:** 使用 `DB` facade'的交易方法，也可以控制 [query builder](/docs/{{version}}/queries) and [Eloquent ORM](/docs/{{version}}/eloquent)的交易.

<a name="accessing-connections"></a>
## 使用多資料庫連接

當你使用多個連接，你可以使用`DB` facade的`connection`方法存取每個連線。在`config/database.php`這個設定檔中，`name`傳遞`connection`方法應該去對應列表其中的一項連線。:

    $users = DB::connection('foo')->select(...);

你可以使用基於PDO原始查詢的方法，在連接例當中使用`getPdo`方法。

    $pdo = DB::connection()->getPdo();
