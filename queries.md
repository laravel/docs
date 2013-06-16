# Query Builder

- [Introduction](#introduction)
- [Selects](#selects)
- [Joins](#joins)
- [Advanced Wheres](#advanced-wheres)
- [Aggregates](#aggregates)
- [Raw Expressions](#raw-expressions)
- [Inserts](#inserts)
- [Updates](#updates)
- [Deletes](#deletes)
- [Unions](#unions)
- [Caching Queries](#caching-queries)

<a name="introduction"></a>
## Introduction

The database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application, and works on all supported database systems.

> **Note:** The Laravel query builder uses PDO parameter binding throughout to protect your application against SQL injection attacks. There is no need to clean strings being passed as bindings.

<a name="selects"></a>
## Selects

**Retrieving All Rows From A Table**

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

**Retrieving A Single Row From A Table**

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

**Retrieving A Single Column From A Row**

	$name = DB::table('users')->where('name', 'John')->pluck('name');

**Retrieving A List Of Column Values**

	$roles = DB::table('roles')->lists('title');

This method will return an array of role titles. You may also specify a custom key column for the returned array:

	$roles = DB::table('roles')->lists('title', 'name');

**Specifying A Select Clause**

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

**Adding A Select Clause To An Existing Query**

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

**Using Where Operators**

	$users = DB::table('users')->where('votes', '>', 100)->get();

**Or Statements**

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

**Using Where Between**

	$users = DB::table('users')
	                    ->whereBetween('votes', array(1, 100))->get();

**Using Where In With An Array**

	$users = DB::table('users')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

**Using Where Null To Find Records With Unset Values**

	$users = DB::table('users')
	                    ->whereNull('updated_at')->get();

**Order By, Group By, And Having**

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

**Offset & Limit**

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

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

You may also specify additional columns to update:

	DB::table('users')->increment('votes', 1, array('name' => 'John'));

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