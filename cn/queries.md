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
## Joins

The query builder may also be used to write join statements. Take a look at the following examples:

**Basic Join Statement**

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price');

You may also specify more advanced join clauses:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## Advanced Wheres

Sometimes you may need to create more advanced where clauses such as "where exists" or nested parameter groupings. The Laravel query builder can handle these as well:

**Parameter Grouping**

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

The query above will produce the following SQL:

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

**Exists Statements**

	DB::table('users')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

The query above will produce the following SQL:

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregates"></a>
## Aggregates

The query builder also provides a variety of aggregate methods, such as `count`, `max`, `min`, `avg`, and `sum`.

**Using Aggregate Methods**

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

Sometimes you may need to use a raw expression in a query. These expressions will be injected into the query as strings, so be careful not to create any SQL injection points! To create a raw expression, you may use the `DB::raw` method:

**Using A Raw Expression**

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

**Incrementing or decrementing a value of a column**

	DB::table('users')->increment('votes');

	DB::table('users')->decrement('votes');

<a name="inserts"></a>
## Inserts

**Inserting Records Into A Table**

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

If the table has an auto-incrementing id, use `insertGetId` to insert a record and retrieve the id:

**Inserting Records Into A Table With An Auto-Incrementing ID**

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **Note:** When using PostgreSQL the insertGetId method expects the auto-incrementing column to be named "id".

**Inserting Multiple Records Into A Table**

	DB::table('users')->insert(array(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	));

<a name="updates"></a>
## Updates

**Updating Records In A Table**

	DB::table('users')
	            ->where('id', 1)
	            ->update(array('votes' => 1));

<a name="deletes"></a>
## Deletes

**Deleting Records In A Table**

	DB::table('users')->where('votes', '<', 100)->delete();

**Deleting All Records From A Table**

	DB::table('users')->delete();

**Truncating A Table**

	DB::table('users')->truncate();

<a name="unions"></a>
## Unions

The query builder also provides a quick way to "union" two queries together:

**Performing A Query Union**

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

The `unionAll` method is also available, and has the same method signature as `union`.

<a name="caching-queries"></a>
## Caching Queries

You may easily cache the results of a query using the `remember` method:

**Caching A Query Result**

	$users = DB::table('users')->remember(10)->get();

In this example, the results of the query will be cached for ten minutes. While the results are cached, the query will not be run against the database, and the results will be loaded from the default cache driver specified for your application.
