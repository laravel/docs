# 查詢產生器

- [介紹](#introduction)
- [Selects](#selects)
- [Joins](#joins)
- [進階 Wheres](#advanced-wheres)
- [聚合](#aggregates)
- [Raw Expressions](#raw-expressions)
- [新增](#inserts)
- [更新](#updates)
- [刪除](#deletes)
- [Unions](#unions)
- [悲觀鎖定](#pessimistic-locking)

<a name="introduction"></a>
## 介紹

資料庫查詢產生器 (query builder) 提供方便、流暢的介面，用來建立及執行資料庫查詢語法。在你的應用程式裡面，它可以被使用在大部分的資料庫操作，而且它在所有支援的資料庫系統上都可以執行。

> **注意:** Laravel 查詢產生器使用 PDO 參數綁定，以保護應用程式免於資料隱碼攻擊 (SQL injection)，因此傳入的參數不需額外跳脫特殊字元。

<a name="selects"></a>
## Selects

#### 從資料表中取得所有的資料列

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### 從資料表中分塊查詢資料列

	DB::table('users')->chunk(100, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

藉由在 `Closure` 中回傳 `false` 來停止處理接下來的資料列：

	DB::table('users')->chunk(100, function($users)
	{
		//

		return false;
	});

#### 從資料表中取得單一資料列

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

#### 從資料表中取得單一資料列的單一欄位

	$name = DB::table('users')->where('name', 'John')->pluck('name');

#### 取得單一欄位值的列表

	$roles = DB::table('roles')->lists('title');

這個方法將會回傳資料表 role 的 title 欄位值的陣列。你也可以透過下面的方法，為回傳的陣列指定自訂鍵值。

	$roles = DB::table('roles')->lists('title', 'name');

#### 指定查詢子句 (Select Clause)

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

#### 增加查詢子句到既存的查詢中

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### 使用 where 及運算子

	$users = DB::table('users')->where('votes', '>', 100)->get();

#### 「or」語法

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

#### 排序(Order By)、分群(Group By) 及 Having

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

#### 偏移(Offset) 及 限制(Limit)

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="joins"></a>
## Joins

查詢產生器也可以使用 join 語法，看看下面的範例：

#### 基本的 Join 語法

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price')
	            ->get();

#### Left Join 語法

	DB::table('users')
		    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    ->get();

你也可以指定更進階的 join 子句：

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

如果你想在你的 join 中使用 where 型式的子句，你可以在 join 子句裡使用 `where` 或 `orWhere` 方法。下面的方法將會比較 contacts 資料表中的 user_id 的數值，而不是比較兩個欄位。

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

有些時候你需要更進階的 where 子句，像是「where exists」或巢狀的群組化參數。Laravel 的查詢產生器也可以處理這樣的情況：

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

上面的查詢語法會產生下方的 SQL：

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

上面的查詢語法會產生下方的 SQL：

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregates"></a>
## 聚合

查詢產生器也提供各式各樣的聚合方法，像是 `count`、`max`、`min`、`avg` 及 `sum`。

#### 使用聚合方法

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

有些時候你需要使用 raw expression 在查詢語句裡，這樣的表達式會成為字串插入至查詢，因此要小心勿建立任何 SQL 隱碼攻擊點。要建立 raw expression，你可以使用 `DB::raw` 方法：

#### 使用 Raw Expression

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="inserts"></a>
## 新增

#### 新增一筆資料進資料表

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

#### 新增自動遞增 (Auto-Incrementing) ID 的資料至資料表

如果資料表有自動遞增的ID，可以使用 `insertGetId` 新增資料並回傳該 ID：

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **注意:** 當使用 PostgreSQL 時，insertGetId 方法會預期自動增加的欄位是以「id」為命名。

#### 新增多筆資料進資料表

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

#### 自增或自減一個欄位的值

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

也能夠同時指定其他要更新的欄位：

	DB::table('users')->increment('votes', 1, array('name' => 'John'));

<a name="deletes"></a>
## 刪除

#### 刪除資料表中的資料

	DB::table('users')->where('votes', '<', 100)->delete();

#### 刪除資料表中的所有資料

	DB::table('users')->delete();

#### 清空資料表

	DB::table('users')->truncate();

<a name="unions"></a>
## Unions

查詢產生器也提供一個快速的方法去「合併 (union)」兩個查詢的結果：

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

`unionAll` 方法也可以使用，它與 `union` 方法的使用方式一樣。

<a name="pessimistic-locking"></a>
## 悲觀鎖定 (Pessimistic Locking)

查詢產生器提供了少數函式協助你在 SELECT 語句中做到「悲觀鎖定」。

想要在 SELECT 語句中加上「Shard lock」，只要在查詢語句中使用 `sharedLock` 函式：

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

要在 select 語法中使用「鎖住更新(lock for update)」時，你可以使用 `lockForUpdate` 方法：

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
