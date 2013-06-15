# 查询生成器

- [简介](#introduction)
- [获取数据](#selects)
- [连接](#joins)
- [高级查询条件](#advanced-wheres)
- [聚合查询结果](#aggregates)
- [原始查询表达式](#raw-expressions)
- [创建数据](#inserts)
- [更新数据](#updates)
- [删除数据](#deletes)
- [union合并查询结果](#unions)
- [缓存查询结果](#caching-queries)

<a name="introduction"></a>
## 简介

查询生成器 为操作数据库提供了一个方便，顺畅的的接口，它支持所有Laravel支持的数据库系统，并能够完成绝大部分查询任务。

> **注意:** 查询生成器 使用了PDO参数绑定传递的方式，从而避免sql注入攻击，也就是在使用参数时不需要进行保证安全性的过滤操作。

<a name="selects"></a>
## 获取数据

**获取一张表里的所有数据**

  $users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

**获取一张表里的一条数据**

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

**获取一张表里的满足where条件的第一行数据的指定字段的值**

	$name = DB::table('users')->where('name', 'John')->pluck('name');

**以列表形势获取一张表里一个字段的值**

	$roles = DB::table('roles')->lists('title');

lists方法返回一个包含所有roles表的title字段的值的数组. 可以通过lists的第二个参数为返回的数组自定义键名：

	$roles = DB::table('roles')->lists('title', 'name');

**筛选查询结果**

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

**为已经建立的查询添加筛选**

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

**使用where条件语句**

	$users = DB::table('users')->where('votes', '>', 100)->get();

**使用or语句**

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

**在Where语句中使用Between子句**

	$users = DB::table('users')
	                    ->whereBetween('votes', array(1, 100))->get();

**在Where语句中使用In子句，In的内容通过数组传递**

	$users = DB::table('users')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

**使用whereNull方法获取未被清除或未被初始化的记录(字段如果没有指定默认值将会是null)**

	$users = DB::table('users')
	                    ->whereNull('updated_at')->get();

**Order By语句, Group By语句, 和 Having 语句筛选**

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

**Offset 和 Limit语句**

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="joins"></a>
## 连接

查询生成器 也可以用来建立数据连接操作，我们看看下面的例子:

**简单连接语句**

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price');

指定更多的连接条件:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## 高级查询条件

有时你可能需要创建更高级的where查询，比如 "where exists"筛选 或者给where条件分组. 查询生成器 都能够很好的处理：

**where条件分组**

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

上面的查询将产生如下的 SQL：

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

**where中的Exists语句**

	DB::table('users')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

上面的查询将产生如下的 SQL：

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregates"></a>
## 聚合查询结果

查询生成器 提供了多个聚合方法, 比如 `count`, `max`, `min`, `avg`,和 `sum`.

**使用聚合方法**

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## 原始查询表达式

有时，你可能需要使用原始的查询表达式， 这种表达式需要直接插入最终的sql语句中, 所以，请特别注意防范sql注入! 使用 `DB::raw` 方法实现原始查询表达式：

**使用原始查询表达式**

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

**将数据表中的某个字段+1或-1**

	DB::table('users')->increment('votes');

	DB::table('users')->decrement('votes');

<a name="inserts"></a>
## 创建数据

**插入一条数据**

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

如果数据表已经有主键了, 使用 `insertGetId` 方法插入数据，不需要主键字段信息:

**同时插入多条数据，同时让主键自增**

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **注意:** 当使用 PostgreSQL 数据库系统时， insertGetId 方法要求主键字段名为 id

**一次插入多条数据**

	DB::table('users')->insert(array(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	));

<a name="updates"></a>
## 更新数据

**更新数据**

	DB::table('users')
	            ->where('id', 1)
	            ->update(array('votes' => 1));

<a name="deletes"></a>
## 删除数据

**普通删除方式**

	DB::table('users')->where('votes', '<', 100)->delete();

**删除一张表的所有数据**

	DB::table('users')->delete();

**清空一张表**

	DB::table('users')->truncate();

<a name="unions"></a>
## union合并查询结果

查询生成器提供了一个快速的方式来 "union" 两个查询:

**使用Union合并两次查询**

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

`unionAll` 也是可用的, 它和 `union` 方法一样.

<a name="caching-queries"></a>
## 缓存查询结果

使用 `remember` 方法可以很容易的缓存查询结果:

**缓存一次查询的查询结果**

	$users = DB::table('users')->remember(10)->get();

在上面的例子中， 查询结果将被缓存10分钟， 当某个查询的结果正在被缓存时， 该查询实际不会执行， 查询结果将直接从缓存系统中读取。
