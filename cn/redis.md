# Redis

- [简介](#introduction)
- [配置](#configuration)
- [用法](#usage)
- [批量输送](#pipelining)

<a name="introduction"></a>
## 简介

[Redis](http://redis.io) 是一个开源、先进的键值对（key-value）存储容器。由于它允许使用[strings](http://redis.io/topics/data-types#strings)、[hashes](http://redis.io/topics/data-types#hashes)、[lists](http://redis.io/topics/data-types#lists)、[sets](http://redis.io/topics/data-types#sets)和[sorted sets](http://redis.io/topics/data-types#sorted-sets)作为键（key），因此它经常被称为数据结构服务器。

> **注意：** 如果你是通过PECL为PHP安装的Redis扩展模块，那么，你必须在 `app/config/app.php` 文件中对其别名进行重新命名。

<a name="configuration"></a>
## 配置

当前应用的Redis配置信息存储在 **app/config/database.php** 文件中。在此文件中，你可以看到一个 **redis** 数组，次数组中存储了当前使用Redis服务器信息。

	'redis' => array(

		'cluster' => true,

		'default' => array('host' => '127.0.0.1', 'port' => 6379),

	),

默认的服务器配置应该可以满足开发过程中的需求了。当然，你可以根据你的开发环境任意修改此配置数组。只需简单的为每个Redis服务器命名并制定此服务器所占用的host和port。

`cluster` 参数是告诉Laravel中的Redis客户端对所有的Redis节点执行客户端侧的分片（sharding），这就赋予你将创建一个节点池，并使用大量的RAM的能力。然而，客户端的分片机制不能够处理失效切换，因此，这种方式主要用来访问其它主数据容器中存放的缓存数据。

<a name="usage"></a>
## 用法

调用 `Redis::connection` 方法可以获取一个Redis类的实例：

	$redis = Redis::connection();

上面的代码可以获取一个到默认Redis服务器的连接。如果你没有使用服务器集群的话，你可以将服务器名称作为参数传递给 `connection` 方法，这样就可以获取Redis配置信息中的某个指定的服务器连接了：

	$redis = Redis::connection('other');

一旦获取到Redis类的实例，我们就可以向其发送任何[Redis命令](http://redis.io/commands) 了。Laravel使用一些魔术方法向Redis服务器传送命令：

	$redis->set('name', 'Taylor');

	$name = $redis->get('name');

	$values = $redis->lrange('names', 5, 10);

注意，向Redis命令传递的参数以同样类似的方式传递给这些魔术方法。当然，如果你不用这些魔术方法，还可以使用 `command` 方法向服务器传送Redis命令：

	$values = $redis->command('lrange', array(5, 10));

当命令只是在默认连接上执行时，仅需使用 `Redis` 类中定义的静态方法即可：

	Redis::set('name', 'Taylor');

	$name = Redis::get('name');

	$values = Redis::lrange('names', 5, 10);

> **注意：** Redis [cache](/docs/cache) 和 [session](/docs/session) 驱动都已经包含在Laravel中了。

<a name="pipelining"></a>
## 批量输送

批量输送（Pipelining）应当用于需要在一个操作中发送许多命令的场景。立即使用 `pipeline` 命令动手试试吧：

**批量输送命令到服务器**

	Redis::pipeline(function($pipe)
	{
		for ($i = 0; $i < 1000; $i++)
		{
			$pipe->set("key:$i", $i);
		}
	});


译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)