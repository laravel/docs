# 数据库使用基础

- [设置](#configuration)
- [读取/写入连接](#read-write-connections)
- [执行查找](#running-queries)
- [数据库交易](#database-transactions)
- [取用连接](#accessing-connections)
- [查找日志纪录](#query-logging)

<a name="configuration"></a>
## 设置

Laravel 让链接数据库和执行查找变得相当容易。数据库相关设置文件都在 `config/database.php`。 在这个文件你可以定义所有的数据库连接，以及指定默认的数据库连接。默认文件中已经有所有支持的数据库系统范例了。

目前 Laravel 支持四种数据库系统： MySQL、Postgres、SQLite、以及 SQL Server。

<a name="read-write-connections"></a>
## 读取/写入连接

有时候你可能希望使用特定数据库连接进行 SELECT 操作，同时使用另外的连接作 INSERT 、 UPDATE 、以及 DELETE 。 Laravel 让这些变得轻松简单，并确保你不论在使用原始查找、查找建立器、或者是 Eloquent ORM 使用的都是正确的连接。

来看看如何设置读取/写入连接，让我们来看以下的范例：

	'mysql' => [
		'read' => [
			'host' => '192.168.1.1',
		],
		'write' => [
			'host' => '196.168.1.2'
		],
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	],

注意我们加了两个键值到设置档数组中： `read` 及 `write`。 两个键值都包含了单一键值的数组：`host`。`read` 及 `write` 的其余数据库设置会从`mysql` 数组中合并。 所以，如果我们想要覆写设置值，只要将选项放入 `read` 和 `write` 数组即可。 所以在上面的例子里， `192.168.1.1` 将被用作「读取」连接，而 `192.168.1.2` 将被用作「写入」连接。数据库凭证、 前缀、字符编码设置、以及其他所有的设置会共用 `mysql` 数组里的设置。

<a name="running-queries"></a>
## 执行查找

如果设置好数据库连接，就可以透过 `DB` facade 执行查找。

#### 执行 Select 查找

	$results = DB::select('select * from users where id = ?', [1]);

`select` 方法会返回一个 `array` 结果。

#### 执行 Insert 语法

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### 执行 Update 语法

	DB::update('update users set votes = 100 where name = ?', ['John']);

#### 执行 Delete 语法

	DB::delete('delete from users');

> **注意：** `update` 和 `delete` 语法会返回在操作中所影响的数据笔数。

#### 执行一般语法

	DB::statement('drop table users');

#### 监听查找事件

你可以使用 `DB::listen` 方法，去监听查找的事件：

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## 数据库交易

你可以使用 `transaction` 方法，去执行一组数据库交易的操作：

	DB::transaction(function()
	{
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

> **注意：** 在 `transaction` 闭包若抛出任何例外会导致交易自动还原 。

有时候你可能需要自己开始一个交易：

	DB::beginTransaction();

你可以透过 `rollback` 的方法还原交易：

	DB::rollback();

最后，你可以透过 `commit` 的方法提交交易：

	DB::commit();

<a name="accessing-connections"></a>
## 取用连接

若要使用多个连接，可以透过 `DB::connection` 方法取用：

	$users = DB::connection('foo')->select(...);

你也可以取用原始底层的 PDO 实例：

	$pdo = DB::connection()->getPdo();

有时候你可能需要重新连接到特定的数据库：

	DB::reconnect('foo');

如果你因为超过了底层 PDO 实例的 `max_connections` 的限制，需要关闭特定的数据库连接，可以透过 `disconnect` 方法:

	DB::disconnect('foo');

<a name="query-logging"></a>
## 查找日志记录

默认情况下，Laravel 会在内存里访问这次请求中所有的查找语句。然而，在有些例子下，比如一次添加 大量的数据，可能会导致应用程序耗损过多内存。 如果要禁用日志，可以使用 `disableQueryLog` 方法：

	DB::connection()->disableQueryLog();

要得到执行过的查找纪录数组，你可以使用 `getQueryLog` 方法：

       $queries = DB::getQueryLog();
