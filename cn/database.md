# 数据库使用基础

- [配置](#configuration)
- [执行查询语句](#running-queries)
- [事务](#database-transactions)
- [使用多个数据库](#accessing-connections)
- [查询日志](#query-logging)

<a name="configuration"></a>
## 配置

在Laravel中连接和使用数据库非常简单。 数据库配置在 `app/config/database.php` 文件中. 所有受支持的数据库系统都列在了配置文件中，在配置文件中可以同时配置多个数据库系统的连接信息, 并指定默认使用哪个数据库连接。

Laravel 目前支持四种数据库系统,分别是: MySQL， Postgres， SQLite， 和 SQL Server。

<a name="running-queries"></a>
## 执行crud语句

完成数据库配置后， 就可以直接使用DB类执行sql语句了.

**执行 select 语句**

  $results = DB::select('select * from users where id = ?', array(1));

`select` 方法总是返回一个包含查询结果的 `array`。

**执行 Insert 语句**

	DB::insert('insert into users (id, name) values (?, ?)', array(1, 'Dayle'));

**执行 Update 语句**

	DB::update('update users set votes = 100 where name = ?', array('John'));

**执行 Delete 语句**

	DB::delete('delete from users');

> **注意:** `update` 和 `delete` 语句返回操作所影响的数据的行数(int)。

**执行非crud语句**also

	DB::statement('drop table users');

可以使用 `DB::listen` 方法监听数据库操作:

**监听数据库操作事件**

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## 事务

将需要在事务模式下执行的查询放入 `transaction` 方法即可:

	DB::transaction(function()
	{
		DB::table('users')->update(array('votes' => 1));

		DB::table('posts')->delete();
	});

<a name="accessing-connections"></a>
## 使用多个数据库

有时可能需要使用多个数据库, 通过DB类的 `DB::connection` 方法来切换:

	$users = DB::connection('foo')->select(...);

你可能需要在数据库系统的层面上操作数据库，使用PDO实例即可:

	$pdo = DB::connection()->getPdo();

Sometimes you may need to reconnect to a given database:

	DB::reconnect('foo');

<a name="query-logging"></a>
## Query Logging

By default, Laravel keeps a log in memory of all queries that have been run for the current request. However, in some cases, such as when inserting a large number of rows, this can cause the application to use excess memory. To disable the log, you may use the `disableQueryLog` method:

	DB::connection()->disableQueryLog();
