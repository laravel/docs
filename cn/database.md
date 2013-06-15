# 数据库使用基础

- [配置](#configuration)
- [执行查询语句](#running-queries)
- [事务](#database-transactions)
- [同时使用多个数据库系统](#accessing-connections)
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

**执行非crud语句**

	DB::statement('drop table users');

可以使用 `DB::listen` 方法监听数据库操作:

**监听数据库操作事件**

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## 事务

将需要在事务模式下执行的查询放入 `transaction` 方法内即可:

	DB::transaction(function()
	{
		DB::table('users')->update(array('votes' => 1));

		DB::table('posts')->delete();
	});

<a name="accessing-connections"></a>
## 同时使用多个数据库系统

有时可能需要同时使用多个数据库系统(MySQL，Postgres，SQLite，SQL Server), 通过DB类的 `DB::connection` 方法来切换:

	$users = DB::connection('foo')->select(...);

你可能需要在数据库系统的层面上操作数据库，使用PDO实例即可:

	$pdo = DB::connection()->getPdo();

使用reconnect方法重新连接一个指定的数据库系统：
	DB::reconnect('foo');

<a name="query-logging"></a>
## 查询日志

Laravel默认会为当前请求执行的的所有查询生成日志并保存在内存中。 因此， 在某些特殊的情况下， 比如一次性向数据库中插入大量数据， 就可能导致内存不足。 在这种情况下，你可以通过 `disableQueryLog` 方法来关闭查询日志：

	DB::connection()->disableQueryLog();
