# Redis

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipelining](#pipelining)

<a name="introduction"></a>
## Introduction

[Redis](http://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](http://redis.io/topics/data-types#strings), [hashes](http://redis.io/topics/data-types#hashes), [lists](http://redis.io/topics/data-types#lists), [sets](http://redis.io/topics/data-types#sets), and [sorted sets](http://redis.io/topics/data-types#sorted-sets).

Before using Redis with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

> **Note:** If you have the Redis PHP extension installed via PECL, you will need to rename the alias for Redis in your `config/app.php` file.

<a name="configuration"></a>
## Configuration

The Redis configuration for your application is stored in the `config/database.php` file. Within this file, you will see a `redis` array containing the Redis servers used by your application:

	'redis' => [

		'cluster' => true,

		'default' => ['host' => '127.0.0.1', 'port' => 6379],

	],

The default server configuration should suffice for development. However, you are free to modify this array based on your environment. Simply give each Redis server a name, and specify the host and port used by the server.

The `cluster` option will tell the Laravel Redis client to perform client-side sharding across your Redis nodes, allowing you to pool nodes and create a large amount of available RAM. However, note that client-side sharding does not handle failover; therefore, is primarily suited for cached data that is available from another primary data store.

If your Redis server requires authentication, you may supply a password by adding a `password` key / value pair to your Redis server configuration array.

<a name="usage"></a>
## Usage

You may get a Redis instance by calling the `Redis::connection` method:

	$redis = Redis::connection();

This will give you an instance of the default Redis server. If you are not using server clustering, you may pass the server name to the `connection` method to get a specific server as defined in your Redis configuration:

	$redis = Redis::connection('other');

Once you have an instance of the Redis client, we may issue any of the [Redis commands](http://redis.io/commands) to the instance. Laravel uses magic methods to pass the commands to the Redis server:

	$redis->set('name', 'Taylor');

	$name = $redis->get('name');

	$values = $redis->lrange('names', 5, 10);

Notice the arguments to the command are simply passed into the magic method. Of course, you are not required to use the magic methods, you may also pass commands to the server using the `command` method:

	$values = $redis->command('lrange', [5, 10]);

When you are simply executing commands against the default connection, just use static magic methods on the `Redis` class:

	Redis::set('name', 'Taylor');

	$name = Redis::get('name');

	$values = Redis::lrange('names', 5, 10);

> **Note:** Redis [cache](/docs/{{version}}/cache) and [session](/docs/{{version}}/session) drivers are included with Laravel.

<a name="pipelining"></a>
## Pipelining

Pipelining should be used when you need to send many commands to the server in one operation. To get started, use the `pipeline` command:

#### Piping Many Commands To Your Servers

	Redis::pipeline(function($pipe)
	{
		for ($i = 0; $i < 1000; $i++)
		{
			$pipe->set("key:$i", $i);
		}
	});
