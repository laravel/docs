# 查找产生器

- [介绍](#introduction)
- [Selects](#selects)
- [Joins](#joins)
- [高端 Wheres](#advanced-wheres)
- [聚合](#aggregates)
- [Raw Expressions](#raw-expressions)
- [添加](#inserts)
- [更新](#updates)
- [删除](#deletes)
- [Unions](#unions)
- [悲观锁定](#pessimistic-locking)

<a name="introduction"></a>
## 介绍

数据库查找产生器 (query builder) 提供方便、流畅的接口，用来建立及执行数据库查找语法。在你的应用程序里面，它可以被使用在大部分的数据库操作，而且它在所有支持的数据库系统上都可以执行。

> **注意:** Laravel 查找产生器使用 PDO 参数绑定，以保护应用程序免于数据隐码攻击 (SQL injection)，因此传入的参数不需额外跳脱特殊字符。

<a name="selects"></a>
## Selects

#### 从数据表中取得所有的数据列

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### 从数据表中分块查找数据列

	DB::table('users')->chunk(100, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

借由在 `Closure` 中回传 `false` 来停止处理接下来的数据列：

	DB::table('users')->chunk(100, function($users)
	{
		//

		return false;
	});

#### 从数据表中取得单一数据列

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

#### 从数据表中取得单一数据列的单一字段

	$name = DB::table('users')->where('name', 'John')->pluck('name');

#### 取得单一字段值的列表

	$roles = DB::table('roles')->lists('title');

这个方法将会回传数据表 role 的 title 字段值的数组。你也可以透过下面的方法，为回传的数组指定自订键值。

	$roles = DB::table('roles')->lists('title', 'name');

#### 指定查找子句 (Select Clause)

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

#### 增加查找子句到既存的查找中

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### 使用 where 及运算子

	$users = DB::table('users')->where('votes', '>', 100)->get();

#### 「or」语法

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

#### 使用 Where In 与数组

	$users = DB::table('users')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

#### 使用 Where Null 找有未设置的值的数据

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

查找产生器也可以使用 join 语法，看看下面的范例：

#### 基本的 Join 语法

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price')
	            ->get();

#### Left Join 语法

	DB::table('users')
		    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    ->get();

你也可以指定更高端的 join 子句：

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

如果你想在你的 join 中使用 where 型式的子句，你可以在 join 子句里使用 `where` 或 `orWhere` 方法。下面的方法将会比较 contacts 数据表中的 user_id 的数值，而不是比较两个字段。

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')
	        	     ->where('contacts.user_id', '>', 5);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## 高端 Wheres

#### 群组化参数

有些时候你需要更高端的 where 子句，像是「where exists」或嵌套的群组化参数。Laravel 的查找产生器也可以处理这样的情况：

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

上面的查找语法会产生下方的 SQL：

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Exists 语法

	DB::table('users')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

上面的查找语法会产生下方的 SQL：

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregates"></a>
## 聚合

查找产生器也提供各式各样的聚合方法，像是 `count`、`max`、`min`、`avg` 及 `sum`。

#### 使用聚合方法

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

有些时候你需要使用 raw expression 在查找语句里，这样的表达式会成为字串插入至查找，因此要小心勿建立任何 SQL 隐码攻击点。要建立 raw expression，你可以使用 `DB::raw` 方法：

#### 使用 Raw Expression

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="inserts"></a>
## 添加

#### 添加一笔数据进数据表

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

#### 添加自动递增 (Auto-Incrementing) ID 的数据至数据表

如果数据表有自动递增的ID，可以使用 `insertGetId` 添加数据并回传该 ID：

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **注意:** 当使用 PostgreSQL 时，insertGetId 方法会预期自动增加的字段是以「id」为命名。

#### 添加多笔数据进数据表

	DB::table('users')->insert(array(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	));

<a name="updates"></a>
## 更新

#### 更新数据表中的数据

	DB::table('users')
	            ->where('id', 1)
	            ->update(array('votes' => 1));

#### 自增或自减一个字段的值

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

也能够同时指定其他要更新的字段：

	DB::table('users')->increment('votes', 1, array('name' => 'John'));

<a name="deletes"></a>
## 删除

#### 删除数据表中的数据

	DB::table('users')->where('votes', '<', 100)->delete();

#### 删除数据表中的所有数据

	DB::table('users')->delete();

#### 清空数据表

	DB::table('users')->truncate();

<a name="unions"></a>
## Unions

查找产生器也提供一个快速的方法去「合并 (union)」两个查找的结果：

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

`unionAll` 方法也可以使用，它与 `union` 方法的使用方式一样。

<a name="pessimistic-locking"></a>
## 悲观锁定 (Pessimistic Locking)

查找产生器提供了少数函式协助你在 SELECT 语句中做到「悲观锁定」。

想要在 SELECT 语句中加上「Shard lock」，只要在查找语句中使用 `sharedLock` 函式：

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

要在 select 语法中使用「锁住更新(lock for update)」时，你可以使用 `lockForUpdate` 方法：

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
