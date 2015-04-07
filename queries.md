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
- [Pessimistic Locking](#pessimistic-locking)

<a name="introduction"></a>
## Introduction

The database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application, and works on all supported database systems.

> **Note:** The Laravel query builder uses PDO parameter binding throughout to protect your application against SQL injection attacks. There is no need to clean strings being passed as bindings.

<a name="selects"></a>
## Selects

#### Retrieving All Rows From A Table

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### Chunking Results From A Table

	DB::table('users')->chunk(100, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

You may stop further chunks from being processed by returning `false` from the `Closure`:

	DB::table('users')->chunk(100, function($users)
	{
		//

		return false;
	});

#### Retrieving A Single Row From A Table

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

#### Retrieving A Single Column From A Row

	$name = DB::table('users')->where('name', 'John')->pluck('name');

#### Retrieving A List Of Column Values

	$roles = DB::table('roles')->lists('title');

This method will return an array of role titles. You may also specify a custom key column for the returned array:

	$roles = DB::table('roles')->lists('title', 'name');

#### Specifying A Select Clause

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

#### Adding A Select Clause To An Existing Query

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### Using Where Operators

	$users = DB::table('users')->where('votes', '>', 100)->get();

#### Or Statements

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

#### Using Where Between

	$users = DB::table('users')
	                    ->whereBetween('votes', [1, 100])->get();

#### Using Where Not Between

	$users = DB::table('users')
	                    ->whereNotBetween('votes', [1, 100])->get();

#### Using Where In With An Array

	$users = DB::table('users')
	                    ->whereIn('id', [1, 2, 3])->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', [1, 2, 3])->get();

#### Using Where Null To Find Records With Unset Values

	$users = DB::table('users')
	                    ->whereNull('updated_at')->get();

#### Dynamic Where Clauses

You may even use "dynamic" where statements to fluently build where statements using magic methods:

	$admin = DB::table('users')->whereId(1)->first();

	$john = DB::table('users')
	                    ->whereIdAndEmail(2, 'john@doe.com')
	                    ->first();

	$jane = DB::table('users')
	                    ->whereNameOrAge('Jane', 22)
	                    ->first();

#### Order By, Group By, And Having

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

#### Offset & Limit

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="joins"></a>
## Joins

The query builder may also be used to write join statements. Take a look at the following examples:

#### Basic Join Statement

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price')
	            ->get();

#### Left Join Statement

	DB::table('users')
		    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    ->get();

You may also specify more advanced join clauses:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

If you would like to use a "where" style clause on your joins, you may use the `where` and `orWhere` methods on a join. Instead of comparing two columns, these methods will compare the column against a value:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')
	        	     ->where('contacts.user_id', '>', 5);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## Advanced Wheres

#### Parameter Grouping

Sometimes you may need to create more advanced where clauses such as "where exists" or nested parameter groupings. The Laravel query builder can handle these as well:

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

#### Exists Statements

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

#### Using Aggregate Methods

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

Sometimes you may need to use a raw expression in a query. These expressions will be injected into the query as strings, so be careful not to create any SQL injection points! To create a raw expression, you may use the `DB::raw` method:

#### Using A Raw Expression

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="inserts"></a>
## Inserts

#### Inserting Records Into A Table

	DB::table('users')->insert(
		['email' => 'john@example.com', 'votes' => 0]
	);

#### Inserting Records Into A Table With An Auto-Incrementing ID

If the table has an auto-incrementing id, use `insertGetId` to insert a record and retrieve the id:

	$id = DB::table('users')->insertGetId(
		['email' => 'john@example.com', 'votes' => 0]
	);

> **Note:** When using PostgreSQL the insertGetId method expects the auto-incrementing column to be named "id".

#### Inserting Multiple Records Into A Table

	DB::table('users')->insert([
		['email' => 'taylor@example.com', 'votes' => 0],
		['email' => 'dayle@example.com', 'votes' => 0]
	]);

<a name="updates"></a>
## Updates

#### Updating Records In A Table

	DB::table('users')
	            ->where('id', 1)
	            ->update(['votes' => 1]);

#### Incrementing or decrementing a value of a column

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

You may also specify additional columns to update:

	DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="deletes"></a>
## Deletes

#### Deleting Records In A Table

	DB::table('users')->where('votes', '<', 100)->delete();

#### Deleting All Records From A Table

	DB::table('users')->delete();

#### Truncating A Table

	DB::table('users')->truncate();

<a name="unions"></a>
## Unions

The query builder also provides a quick way to "union" two queries together:

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

The `unionAll` method is also available, and has the same method signature as `union`.

<a name="pessimistic-locking"></a>
## Pessimistic Locking

The query builder includes a few functions to help you do "pessimistic locking" on your SELECT statements.

To run the SELECT statement with a "shared lock", you may use the `sharedLock` method on a query:

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

To "lock for update" on a SELECT statement, you may use the `lockForUpdate` method on a query:

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
