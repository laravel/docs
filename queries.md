# 資料庫：查詢產生器

- [簡介](#introduction)
- [取得結果](#retrieving-results)
    - [聚合](#aggregates)
- [Selects（選出）](#selects)
- [Joins（連接）](#joins)
- [Unions（聯合）](#unions)
- [Where 子句](#where-clauses)
    - [進階 Where 子句](#advanced-where-clauses)
- [Ordering（排序）、Grouping（分組）、Limit（限制）及 Offset（偏移）](#ordering-grouping-limit-and-offset)
- [Inserts（插入）](#inserts)
- [Updates（更新）](#updates)
- [Deletes（刪除）](#deletes)
- [悲觀鎖定](#pessimistic-locking)

<a name="introduction"></a>
## 簡介

資料庫查詢產生器提供方便、流暢的介面，用來建立及執行資料庫查詢。它可用來執行你的應用程式中大部分的資料庫操作，且在所有支援的資料庫系統中都能作用。

> **注意：** Laravel 的查詢產生器使用 PDO 參數綁定，以保護你的應用程式不受資料隱碼（SQL injection）攻擊。傳入字串作為綁定前不需先清理它們。

<a name="retrieving-results"></a>
## 取得結果

#### 從資料表中取得所有的資料列

要開始進行流暢查詢，在 `DB` facade 上使用 `table` 方法。`table` 方法會針對給定的資料表傳回一個流暢查詢產生器實例，允許你在查詢上鏈結更多的約束，並於最後得到結果。在這個例子，讓我們從一個資料表中`取得`所有的記錄：

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示應用程式的所有使用者列表。
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::table('users')->get();

            return view('user.index', ['users' => $users]);
        }
    }

就像[原始查詢](/docs/{{version}}/database)，`get` 方法會回傳一個結果`陣列`，其中每一個結果都是 PHP `StdClass` 物件的實例。你可以將欄位作為物件的性質，來存取每個欄位的值：

    foreach ($users as $user) {
        echo $user->name;
    }

#### 從資料表中取得單一列／欄

若你只需從資料表中取出單一列，你可以使用 `first` 方法。這個方法會回傳單一的 `StdClass` 物件：

    $user = DB::table('users')->where('name', 'John')->first();

    echo $user->name;

若你甚至不需完整的一列，你可以使用 `value` 方法來從一筆記錄中取出單一值。這個方法會直接傳回欄位的值：

    $email = DB::table('users')->where('name', 'John')->value('email');

#### 從資料表中將結果切塊（chunking）

若你需要操作數千筆資料庫記錄，可考慮使用 `chunk` 方法。這個方法一次取出一小「塊」結果，並將每個區塊餵給一個`閉包`處理。這個方法對編寫要處理數千筆記錄的 [Artisan 指令](/docs/{{version}}/artisan)非常有用。例如，讓我們將整個 `user` 資料表切塊，一次處理 100 筆記錄：

    DB::table('users')->chunk(100, function($users) {
        foreach ($users as $user) {
            //
        }
    });

你可以從`閉包`中回傳 `false`，以停止對後續切塊的處理：

    DB::table('users')->chunk(100, function($users) {
        // 處理記錄…

        return false;
    });

#### 取得欄位值列表

若你想要取得一個包含單一欄位值的陣列，你可以使用 `lists` 方法。在這個例子中，我們將取出 role 資料表 title 欄位的陣列：

    $titles = DB::table('roles')->lists('title');

    foreach ($titles as $title) {
        echo $title;
    }

你也可以在傳回的陣列中指定自定的鍵值欄位：

    $roles = DB::table('roles')->lists('title', 'name');

    foreach ($roles as $name => $title) {
        echo $title;
    }

<a name="aggregates"></a>
### 聚合

查詢產生器也提供了各種聚合方法，例如 `count`、`max`、`min`、`avg`、以及 `sum`。你可以在建立你的查詢後呼叫其中任何一個方法：

    $users = DB::table('users')->count();

    $price = DB::table('orders')->max('price');

當然，你也可以將這些方法合併其他的子句來打造你的查詢：

    $price = DB::table('orders')
                    ->where('finalized', 1)
                    ->avg('price');

<a name="selects"></a>
## Selects（選出）

#### 指定一個 Select 子句

當然，你不會總是想要從資料表中選出所有的欄位。你可以使用 `select` 方法為查詢指定一個自訂的 `select` 子句：

    $users = DB::table('users')->select('name', 'email as user_email')->get();

`distinct` 方法允許你強制讓查詢傳回不重複的結果：

    $users = DB::table('users')->distinct()->get();

若你已有一個查詢產生器的實例，而你希望在其既存的 select 子句中加入一個欄位，你可使用 `addSelect` 方法：

    $query = DB::table('users')->select('name');

    $users = $query->addSelect('age')->get();

#### 原始表達式

有時你可能需要在查詢中使用原始表達式。這些表達式會被當作字串注入查詢中，因此小心不要造成資料隱碼攻擊！要建立一個原始表達式，你可以使用 `DB::raw` 方法：

    $users = DB::table('users')
                         ->select(DB::raw('count(*) as user_count, status'))
                         ->where('status', '<>', 1)
                         ->groupBy('status')
                         ->get();

<a name="joins"></a>
## Joins（連接）

#### Inner Join（內部連接）述句

查詢產生器也可用來編寫 join 述句。要操作基本的 SQL「inner join」，你可以在查詢產生器實例上使用 `join` 方法。傳入 `join` 方法的第一個參數是你需要連接的資料表名稱，其他參數則指定用以連接的欄位約束。當然，如你所見，你可以在單一查詢連接多個資料表：

    $users = DB::table('users')
                ->join('contacts', 'users.id', '=', 'contacts.user_id')
                ->join('orders', 'users.id', '=', 'orders.user_id')
                ->select('users.*', 'contacts.phone', 'orders.price')
                ->get();

#### Left Join（左連接）述句

如果你想以操作「left join」來代替「inner join」，使用 `leftJoin` 方法。`leftJoin` 方法和 `join` 方法有相同的署名：

    $users = DB::table('users')
                ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

#### 進階 Join 述句

你也可以指定更進階的 join 子句。以傳入一個`閉包`當作 `join` 方法的第二參數作為開始。此`閉包`會接收 `JoinClause` 物件，讓你可以在 `join` 子句上指定約束：

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')->orOn(...);
            })
            ->get();

若你想要在連接中使用「where」風格的子句，你可以在連接中使用 `where` 和 `orWhere` 方法。這些方法會比較欄位及一個值，來代替兩個欄位的比較：

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')
                     ->where('contacts.user_id', '>', 5);
            })
            ->get();

<a name="unions"></a>
## Unions（聯合）

查詢產生器也提供一個快速的方法來「聯合」兩個查詢。例如，你可以創建一個初始查詢，然後使用 `union` 方法將它與第二個查詢聯合：

    $first = DB::table('users')
                ->whereNull('first_name');

    $users = DB::table('users')
                ->whereNull('last_name')
                ->union($first)
                ->get();

也可使用 `unionAll` 方法，它和 `union` 有相同的方法署名。

<a name="where-clauses"></a>
## Where 子句

#### 簡易方法子句 Simple Where Clauses

要在查詢中加入 `where` 子句，在查詢建造者實例中使用 `where` 方法。最基本的 `where` 呼叫需要三個參數。第一個參數是欄位的名稱。第二個參數是一個運算子，它可以是資料庫所支援的任何運算子。第三個參數是要對欄位評估的值。

例如，這是一個要驗證「votes」欄位的值等於 100 的查詢：

    $users = DB::table('users')->where('votes', '=', 100)->get();

為了方便起見，若你單純只想驗證某欄位等於一個給定值，你可以直接將這個值作為第二個參數傳入 `where` 方法：

    $users = DB::table('users')->where('votes', 100)->get();

當然，在編寫 `where` 子句時，你可以使用各式其他的運算子：

    $users = DB::table('users')
                    ->where('votes', '>=', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('votes', '<>', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('name', 'like', 'T%')
                    ->get();

#### Or（或）述句

你也可以在查詢中加入 `or` 子句，將 where 約束鏈結在一起。`orWhere` 方法和 `where` 方法接受相同的參數：

    $users = DB::table('users')
                        ->where('votes', '>', 100)
                        ->orWhere('name', 'John')
                        ->get();

#### 其他的 Where 子句

**whereBetween**

`whereBetween` 方法驗證一個欄位的值介於兩個值之間：

    $users = DB::table('users')
                        ->whereBetween('votes', [1, 100])->get();

**whereNotBetween**

`whereNotBetween` 方法驗證一個欄位的值落在兩個值之外：

    $users = DB::table('users')
                        ->whereNotBetween('votes', [1, 100])
                        ->get();

**whereIn／whereNotIn**

`whereIn` 方法驗證給定欄位的值包含在給定的陣列之內：

    $users = DB::table('users')
                        ->whereIn('id', [1, 2, 3])
                        ->get();

`whereNotIn` 方法驗證給定欄位的值**不**包含在給定的陣列之內：

    $users = DB::table('users')
                        ->whereNotIn('id', [1, 2, 3])
                        ->get();

**whereNull／whereNotNull**

`whereNull` 方法驗證給定㯗位的值為 `NULL`：

    $users = DB::table('users')
                        ->whereNull('updated_at')
                        ->get();

`whereNotNull` 方法驗證一個欄位的值**不**為 `NULL`：

    $users = DB::table('users')
                        ->whereNotNull('updated_at')
                        ->get();

<a name="advanced-where-clauses"></a>
## 進階 Where 子句

#### 參數分組

有時你可能會需要建立更進階的 where 子句，例如「where exists」或者巢狀的參數分組。Laravel 的查詢產生器也可處理這些。讓我們看一個在括號中將約束分組的例子：

    DB::table('users')
                ->where('name', '=', 'John')
                ->orWhere(function ($query) {
                    $query->where('votes', '>', 100)
                          ->where('title', '<>', 'Admin');
                })
                ->get();

如同你看到的，將`閉包`傳入 `orWhere` 方法，告訴查詢產生器開始一個約束分組。此`閉包`接收查詢產生器的實例，你可以用它來設定應包含在括號分組中的約束。上面的例子會產生以下的 SQL：

    select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Exists（存在）述句

`whereExists` 方法允許你編寫 `where exists` SQL 子句。`whereExists` 方法接受一個`閉包`參數，它會接收查詢產生器實例，讓你可以定義應放在「exists」SQL 子句中的查詢：

    DB::table('users')
                ->whereExists(function ($query) {
                    $query->select(DB::raw(1))
                          ->from('orders')
                          ->whereRaw('orders.user_id = users.id');
                })
                ->get();

上述的查詢會產生以下的 SQL：

    select * from users
    where exists (
        select 1 from orders where orders.user_id = users.id
    )

<a name="ordering-grouping-limit-and-offset"></a>
## Ordering（排序）、Grouping（分組）、Limit（限制）及 Offset（偏移）

#### orderBy

`orderBy` 方法允許你針對給定的欄位，將查詢結果排序。`orderBy` 的第一個參數應為你要用來排序的欄位，第二個參數則控制排序的方向，可以是 `asc` 或 `desc`：

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

#### groupBy／having／havingRaw

`groupBy` 和 `having` 方法可以用來將查詢結果分組。`having` 方法的署名和 `where` 方法的類似：

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

`havingRaw` 方法可用來將原始字串設定為 `having` 子句的值。例如，我們可以找出所有銷售額大於 2,500 元的部門：

    $users = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > 2500')
                    ->get();

#### skip／take

要限制查詢所回傳的結果數量，或略過給定數量的查詢結果（`偏移`），你可使用 `skip` 和 `take` 方法：

    $users = DB::table('users')->skip(10)->take(5)->get();

<a name="inserts"></a>
## Inserts（插入）

查詢產生器也提供了 `insert` 方法，用來將記錄插入資料表。`insert` 方法接受一個陣列，包含要插入的欄位名稱及值：

    DB::table('users')->insert(
        ['email' => 'john@example.com', 'votes' => 0]
    );

你甚至可以在一次的 `insert` 呼叫中，傳入一個包含陣列的陣列，來插入數筆記錄到資料表裡。每個陣列代表要插入資料表中的一列記錄：

    DB::table('users')->insert([
        ['email' => 'taylor@example.com', 'votes' => 0],
        ['email' => 'dayle@example.com', 'votes' => 0]
    ]);

#### 自動遞增 ID

若資料表有一自動遞增的 id，使用 `insertGetId` 方法來插入記錄並取得其 ID：

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

>**注意：**當使用 PostgreSQL 時，insertGetId 方法預期自動遞增欄位的名稱為 `id`。若你要從不同的「次序」取得 ID，你可以將次序名稱作為第二個參數傳入 `insertGetId` 方法。

<a name="updates"></a>
## Updates（更新）

當然，除了在資料庫中插入記錄，也可使用 `update` 方法讓查詢產生器更新已存在的記錄。`update` 方法和 `insert` 方法一樣，接受含一對欄位及值的陣列，其中包含要被更新的欄位。你可以使用 `where` 子句來約束 `update` 查詢：

    DB::table('users')
                ->where('id', 1)
                ->update(['votes' => 1]);

#### 遞增／遞減

查詢產生器也提供便利的方法來遞增或遞減給定欄位的值。這只是個捷徑，提供了一個較手動編寫 `update` 述句更具表達力且精練的介面。

這兩個方法都接受至少一個參數：要修改的欄位。可選擇性地傳入第二個參數，用來控制欄位應遞增／遞減的量。

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

你也可以指定其餘要在操作中更新的欄位：

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="deletes"></a>
## Deletes（刪除）

當然，透過 `delete` 方法，查詢產生器也可用來將記錄從資料表中刪除：

    DB::table('users')->delete();

在呼叫 `delete` 方法之前，你可加上 `where` 子句用來約束 `delete` 述句：

    DB::table('users')->where('votes', '<', 100)->delete();

若你希望截去整個資料表來移除所有資料列，並將自動遞增 ID 重設為零，你可以使用 `truncate` 方法：

    DB::table('users')->truncate();

<a name="pessimistic-locking"></a>
## 悲觀鎖定

產詢產生器也包含一些函式，用以協助你在 `select` 述句上作「悲觀鎖定」。要以「共享鎖」來執行述句，你可以在查詢上使用 `sharedLock` 方法。共享鎖可避免選擇的資料列被更改，直到你的交易提交為止：

    DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

此外，你可以使用 `lockForUpdate` 方法。「用以更新」鎖可避免資料列被其他共享鎖修改或選取：

    DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
