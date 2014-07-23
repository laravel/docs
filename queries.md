# Query產生器

- [介紹](#introduction)
- [Selects](#selects)
- [Joins](#joins)
- [進階 Wheres](#advanced-wheres)
- [Aggregates](#aggregates)
- [Raw Expressions](#raw-expressions)
- [新增](#inserts)
- [更新](#updates)
- [刪除](#deletes)
- [Unions](#unions)
- [Pessimistic Locking](#pessimistic-locking)
- [Caching Queries](#caching-queries)

<a name="introduction"></a>
## 介紹

資料庫查詢產生器(query builder)提供方便流暢的介面，用來建立及執行資料庫查詢語法。在你的應用程式裡面，它可以被使用在大部分的資料
庫操作，而且它在所有支援的資料庫系統上都可以執行。

> **注意:** Laravel 查詢產生器使用 PDO 參數連結，以保護應用程式免於資料隱碼攻擊(SQL injection)，因此傳入的參數不需額外跳脫特殊字元。

<a name="selects"></a>
## Selects

#### 從users資料表中取得所有的資料列

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### 從users資料表中取得name column為John的第一列

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

#### 從users資料表中取得name為John的資料，並只回傳name欄位

	$name = DB::table('users')->where('name', 'John')->pluck('name');

#### 取得title欄位值的list

	$roles = DB::table('roles')->lists('title');

這個方法將會回傳role title的陣列。你也可以透過下面的方法，為回傳的陣列指定自訂的key欄位。

	$roles = DB::table('roles')->lists('title', 'name');

#### 指定查詢子句(Select Clause)

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

#### 增加查詢子句到已查詢的query

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### 使用where及運算子

	$users = DB::table('users')->where('votes', '>', 100)->get();

#### "Or" 語法

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

#### 使用 Where Between

	$users = DB::table('users')
	                    ->whereBetween('votes', array(1, 100))->get();

#### 使用 Where Not Between

	$users = DB::table('users')
	                    ->whereNotBetween('votes', array(1, 100))->get();

#### 使用 Where In 與陣列

	$users = DB::table('users')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

#### 使用 Where Null 找有未設定的值的資料

	$users = DB::table('users')
	                    ->whereNull('updated_at')->get();

#### 排序(Order By), 分群(Group By), 及 Having

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

#### 偏移(Offset) 及 限制(Limit)

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="joins"></a>
## Joins

Query產生器也可以寫join語法，看看下面的範例：

#### 基本的Join語法

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price')
	            ->get();

#### Left Join語法

	DB::table('users')
		    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    ->get();

你也可以指定更進階的join子句

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

如果你想用where型式的子句，你可以使用where或orWhere函數在join子句裡。下面的方法將會比較contacts資料表中的user_id的數值，而不是比較兩個欄位。

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')
	        	     ->where('contacts.user_id', '>', 5);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## 進階 Wheres

#### 群組化參數

有些時候你需要更進階的where子句，像是"where exists"或巢狀的群組化參數。Laravel的query產生器也可以處理這樣的情況；

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

上面的query語法會產生下方的SQL：

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Exists 語法

	DB::table('users')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

上面的query語法會產生下方的SQL：

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregates"></a>
## Aggregates

Query產生器也提供各式各樣的aggregate方法，像是count、max、min、avg、及sum
The query builder also provides a variety of aggregate methods, such as `count`, `max`, `min`, `avg`, and `sum`.

#### 使用 Aggregate 方法

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

有些時候你需要使用raw expression在query語句裡，這樣的表達式會成為字串插入至query，因此要小心勿建立任何SQL隱碼攻擊點。要建立raw expression，你可以使用"DB::raw"方法：

#### 使用 Raw Expression

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

#### 對欄位增加或減少數值值

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

你也可以指派其他欄位同時更新

	DB::table('users')->increment('votes', 1, array('name' => 'John'));

<a name="inserts"></a>
## 新增

#### 新增一筆資料進users資料表

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

#### Inserting Records Into A Table With An Auto-Incrementing ID

If the table has an auto-incrementing id, use `insertGetId` to insert a record and retrieve the id:

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **Note:** When using PostgreSQL the insertGetId method expects the auto-incrementing column to be named "id".

#### Inserting Multiple Records Into A Table

	DB::table('users')->insert(array(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	));

<a name="updates"></a>
## 更新

#### 更新資料表中的資料

	DB::table('users')
	            ->where('id', 1)
	            ->update(array('votes' => 1));

<a name="deletes"></a>
## 刪除

#### 刪除users資料表中votes大於100的資料

	DB::table('users')->where('votes', '<', 100)->delete();

#### 刪除資料表中的所有資料

	DB::table('users')->delete();

#### 清空資料表

	DB::table('users')->truncate();

<a name="unions"></a>
## Unions

Query產生器也提供一個快速的方法去"合併(union)"兩個query：

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

"unionAll"方法也可以使用，它與"union"方法的使用方式一樣。

<a name="pessimistic-locking"></a>
## 悲觀鎖定(Pessimistic Locking)

在你的執行select語法時，Query產生器包含了少數函數幫助你處理"悲觀鎖定(pessimistic locking)"。

要執行select語法搭配"shared lock"，你可以使用"sharedLock"方法在query語句上：

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

要"鎖住更新(lock for update)"在select語法時，你可以使用"lockForUpdate"方法：

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();

<a name="caching-queries"></a>
## 快取查詢(Caching Queries)

使用"remember"方法，你可以輕鬆得快取查詢結果：

	$users = DB::table('users')->remember(10)->get();

這個範例中，查詢結果將會有10分鐘的快取。當結果被快取時，query語句將不會被執行於資料庫，而且查詢結果會從應用程式指定的快取驅動器中載入。

如果你正在使用 [提供的快取驅動器](/docs/cache#cache-tags)，你也可以增加標籤(tags)到快取中：

	$users = DB::table('users')->cacheTags(array('people', 'authors'))->remember(10)->get();
