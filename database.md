# Basic Database Usage

- [Configuration](#configuration)
- [Multiple Databases](#multiple)
- [Running Queries](#running-queries)
- [Accessing Connections](#accessing-connections)

<a name="configuration"></a>
## Configuration

Laravel makes connecting with databases and running queries extremely simple. The database configuration file is `app/config/database.php`. In this file you may define all of your database connections, as well as specify which connection should be used by default. Examples for all of the supported database systems are provided in this file.

Currently Laravel supports four database systems: MySQL, Postgres, SQLite, and SQL Server.

<a name="multiple"></a>
## Multiple Databases

You can specify different connections in app/config/database.php.  The keys for the connections array can be anything, they do not need to be "sqlite", "mysql", etc.

	// application/config/database.php
	'default' => 'fred',
	'connections' => array(
	    'fred' => array(
	        'driver'   => 'mysql',
	        'host'     => 'localhost',
	        'database' => 'database1',
	        'username' => 'root',
	        'password' => '',
	        'charset'  => 'utf8',
	        'prefix'   => '',
	    ),
	
	    'wilma' => array(
	        'driver'   => 'mysql',
	        'host'     => 'localhost',
	        'database' => 'database2',
	        'username' => 'root',
	        'password' => '',
	        'charset'  => 'utf8',
	        'prefix'   => '',
	    ),
	
	    'barney' => array(
	        'driver'   => 'mysql',
	        'host'     => 'localhost',
	        'database' => 'database3',
	        'username' => 'root',
	        'password' => '',
	        'charset'  => 'utf8',
	        'prefix'   => '',
	    ),
	),

Now you can specify the connection on the model:

	class Dino extends Eloquent {
	    protected $connection = 'barney';
	}
 
<a name="running-queries"></a>
## Running Queries

Once you have configured your database connection, you may run queries using the `DB` class.

**Running A Select Query**

	$results = DB::select('select * from users where id = ?', array(1));

The `select` method will always return an `array` of results.

**Running An Insert Statement**

	DB::insert('insert into users (id, name) values (?, ?)', array(1, 'Dayle'));

**Running An Update Statement**

	DB::update('update users set votes = 100 where name = ?', array('John'));

**Running A Delete Statement**

	DB::delete('delete from users');

> **Note:** The `update` and `delete` statements return the number of rows affected by the operation.

**Running A General Statement**

	DB::statement('drop table users');

You may listen for query events using the `DB::listen` method:

**Listening For Query Events**

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="accessing-connections"></a>
## Accessing Connections

When using multiple connections, you may access them via the `DB::connection` method:

	$users = DB::connection('foo')->select(...);
