# Schema Builder

- [Introduction](#introduction)
- [Creating & Dropping Tables](#creating-and-dropping-tables)
- [Adding Columns](#adding-columns)
- [Dropping Columns](#dropping-columns)
- [Adding Indexes](#adding-indexes)
- [Dropping Indexes](#dropping-indexes)
- [Foreign Keys](#foreign-keys)

<a name="introduction"></a>
## Introduction

The Laravel `Schema` class provides a database agnostic way of manipulating tables. It works well with all of the databases supported by Laravel, and has a unified API across all of these systems.

<a name="creating-and-dropping-tables"></a>
## Creating & Dropping Tables

To create a new database table, the `Schema::create` method is used:

	Schema::create('users', function($table)
	{
		$table->increments('id');
	});

The first argument passed to the `create` method is the name of the table, and the second is a `Closure` which will receive a `Blueprint` object which may be used to define the new table.

To specify which connection the schema operation should take place on, use the `Schema::connection` method:

	Schema::connection('foo')->create('users', function($table)
	{
		$table->increments('id'):
	});

To drop a table, you may use the `Schema::drop` method:

	Schema::drop('users');

	Schema::dropIfExists('users');

<a name="adding-columns"></a>
## Adding Columns

To update an existing table, we will use the `Schema::table` method:

	Schema::table('users', function($table)
	{
		$table->string('email');
	});

The table builder contains a variety of column types that you may use when building your tables:

Command  | Description
------------- | -------------
`$table->increments('id');`  |  Incrementing ID to the table (primary key).
`$table->string('email');`  |  VARCHAR equivalent column
`$table->string('name', 100);`  |  VARCHAR equivalent with a length
`$table->integer('votes');`  |  INTEGER equivalent to the table
`$table->float('amount');`  |  FLOAT equivalent to the table
`$table->decimal('amount', 5, 2);`  |  DECIMAL equivalent with a precision and scale
`$table->boolean('confirmed');`  |  BOOLEAN equivalent to the table
`$table->date('created_at');`  |  DATE equivalent to the table
`$table->dateTime('created_at');`  |  DATETIME equivalent to the table
`$table->time('sunrise');`  |  TIME equivalent to the table
`$table->timestamp('added_on');`  |  TIMESTAMP equivalent to the table
`$table->timestamps();`  |  Adds **created\_at** and **updated\_at** columns
`$table->text('description');`  |  TEXT equivalent to the table
`$table->binary('data');`  |  BLOB equivalent to the table
`$table->enum('choices', array('foo', 'bar'));` | ENUM equivalent to the table
`->nullable()`  |  Designate that the column allows NULL values
`->default($value)`  |  Declare a default value for a column
`->unsigned()`  |  Set INTEGER to UNSIGNED

<a name="dropping-columns"></a>
## Dropping Columns

**Dropping A Column From A Database Table**

	Schema::table('users', function($table)
	{
		$table->dropColumn('votes');
	});

<a name="adding-indexes"></a>
## Adding Indexes

The schema builder supports several types of indexes. There are two ways to add them. First, you may fluently define them on a column definition, or you may add them separately:

**Fluently Creating A Column And Index**

	$table->string('email')->unique();

Or, you may choose to add the indexes on separate lines. Below is a list of all available index types:

Command  | Description
------------- | -------------
`$table->primary('id');`  |  Adding a primary key
`$table->primary(array('first', 'last'));`  |  Adding composite keys
`$table->unique('email');`  |  Adding a unique index
`$table->index('state');`  |  Adding a basic index

<a name="dropping-indexes"></a>
## Dropping Indexes

To drop index you must specify the index's name. Laravel assigns a reasonable name to the indexes by default. Simply concatenate the table name, the names of the column in the index, and the index type. Here are some examples:

Command  | Description
------------- | -------------
`$table->dropPrimary('users_id_primary');`  |  Dropping a primary key from the "users" table
`$table->dropUnique('users_email_unique');`  |  Dropping a unique index from the "users" table
`$table->dropIndex('geo_state_index');`  |  Dropping a basic index from the "geo" table

<a name="foreign-keys"></a>
## Adding Columns

When building your database you're very likely have columns in one table referencing primary keys of another table, for instance when you're using [Eloquent's Relationships](/docs/eloquent#relationships) features. If you let your database engine know this you can leverage it's capacity for keeping this data consistent and working smothly.


**Creating The Referencing Column**

	$table->integer("user_id")->unsigned()->index();;

Make sure the new column matches the data type of referenced column. The column needs to be able to store any data the referenced column can store, otherwise you will probably run into trouble at some point.

> **Note:** The referenced table must be created before the referencing table.

**Add A Foreign Key Constraint**

	$table->foreign("user_id")->references('id')->on('users');

But to really leverage the database engine you'll probably want to specify what you want it to do when the referenced column is updated or deleted

	$table->foreign("user_id")->references('id')->on('users')->onDelete('restrict');

	$table->foreign("user_id")->references('id')->on('users')->onUpdate('cascade')->onDelete('restrict');

Option  |  Description
------------- | -------------
`restrict`  |  Prevents deletion of the referenced row or updates of the foreign key
`cascade`  |  The action replicates - the new value is adopted, or the row is deleted along with the referenced row
`set null`  |  The value is set to null when the foreign key is updated or deleted
`no action`  |  Error is raised, but the action is performed **This is the default option**
`set default`  | The value is set to the default for the column when the foreign key is updated or deleted

> **Note:** `set default` is not supported by MySQL InnoDB!

**Dropping Foreign Key Constraints**

	$table->dropForeign("user_id");
