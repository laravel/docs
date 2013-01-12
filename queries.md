## Query Builder

- [Introduction](#introduction)
- [Selects](#selects)
- [Joins](#joins)
- [Advanced Wheres](#advanced-wheres)
- [Aggregates](#aggregates)
- [Raw Expressions](#raw-expressions)
- [Inserts](#inserts)
- [Updates](#updates)
- [Deletes](#deletes)

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

**Specifying A Select Clause**

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

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
	            ->whereExist(function($query)
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
	                     ->select(DB:raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="inserts"></a>
## Inserts

**Inserting Records Into A Table**

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0),
	);

**Inserting Multiple Records Into A Table**

	DB::table('users')->insert(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	);

<a name="updates"></a>
## Updates

**Updating Records In A Table**

	DB::table('users')
	            ->where('id', 1)
	            ->update(['votes' => 1]);

<a name="deletes"></a>
## Deletes

**Deleting Records In A Table**

	DB::table('users')->where('votes', < 100)->delete();

**Deleting All Records From A Table**

	DB::table('users')->delete();
