# Redis

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Clusters](#clusters)
    - [Predis](#predis)
    - [phpredis](#phpredis)
- [Interacting With Redis](#interacting-with-redis)
    - [Transactions](#transactions)
    - [Pipelining Commands](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## Introduction

[Redis](https://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](https://redis.io/topics/data-types#strings), [hashes](https://redis.io/topics/data-types#hashes), [lists](https://redis.io/topics/data-types#lists), [sets](https://redis.io/topics/data-types#sets), and [sorted sets](https://redis.io/topics/data-types#sorted-sets).

Before using Redis with Laravel, we encourage you to install and use the [phpredis](https://github.com/phpredis/phpredis) PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using [Laravel Sail](/docs/{{version}}/sail), this extension is already installed in your application's Docker container.

If you are unable to install the phpredis extension, you may install the `predis/predis` package via Composer. Predis is a Redis client written entirely in PHP and does not require any additional extensions:

```bash
composer require predis/predis
```

<a name="configuration"></a>
## Configuration

You may configure your application's Redis settings via the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers utilized by your application:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

        'cache' => [
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_CACHE_DB', 1),
        ],

    ],

Each Redis server defined in your configuration file is required to have a name, host, and a port unless you define a single URL to represent the Redis connection:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'url' => 'tcp://127.0.0.1:6379?database=0',
        ],

        'cache' => [
            'url' => 'tls://user:password@127.0.0.1:6380?database=1',
        ],

    ],

<a name="configuring-the-connection-scheme"></a>
#### Configuring The Connection Scheme

By default, Redis clients will use the `tcp` scheme when connecting to your Redis servers; however, you may use TLS / SSL encryption by specifying a `scheme` configuration option in your Redis server's configuration array:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'default' => [
            'scheme' => 'tls',
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'password' => env('REDIS_PASSWORD', null),
            'port' => env('REDIS_PORT', 6379),
            'database' => env('REDIS_DB', 0),
        ],

    ],

<a name="clusters"></a>
### Clusters

If your application is utilizing a cluster of Redis servers, you should define these clusters within a `clusters` key of your Redis configuration. This configuration key does not exist by default so you will need to create it within your application's `config/database.php` configuration file:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'clusters' => [
            'default' => [
                [
                    'host' => env('REDIS_HOST', 'localhost'),
                    'password' => env('REDIS_PASSWORD', null),
                    'port' => env('REDIS_PORT', 6379),
                    'database' => 0,
                ],
            ],
        ],

    ],

By default, clusters will perform client-side sharding across your nodes, allowing you to pool nodes and create a large amount of available RAM. However, client-side sharding does not handle failover; therefore, it is primarily suited for transient cached data that is available from another primary data store.

If you would like to use native Redis clustering instead of client-side sharding, you may specify this by setting the `options.cluster` configuration value to `redis` within your application's `config/database.php` configuration file:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
        ],

        'clusters' => [
            // ...
        ],

    ],

<a name="predis"></a>
### Predis

If you would like your application to interact with Redis via the Predis package, you should ensure the `REDIS_CLIENT` environment variable's value is `predis`:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'predis'),

        // ...
    ],

In addition to the default `host`, `port`, `database`, and `password` server configuration options, Predis supports additional [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) that may be defined for each of your Redis servers. To utilize these additional configuration options, add them to your Redis server configuration in your application's `config/database.php` configuration file:

    'default' => [
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'read_write_timeout' => 60,
    ],

<a name="the-redis-facade-alias"></a>
#### The Redis Facade Alias

Laravel's `config/app.php` configuration file contains an `aliases` array which defines all of the class aliases that will be registered by the framework. For convenience, an alias entry is included for each [facade](/docs/{{version}}/facades) offered by Laravel; however, the `Redis` alias is disabled because it conflicts with the `Redis` class name provided by the phpredis extension. If you are using the Predis client and would like to enable this alias, you may un-comment the alias in your application's `config/app.php` configuration file.

<a name="phpredis"></a>
### phpredis

By default, Laravel will use the phpredis extension to communicate with Redis. The client that Laravel will use to communicate with Redis is dictated by the value of the `redis.client` configuration option, which typically reflects the value of the `REDIS_CLIENT` environment variable:

    'redis' => [

        'client' => env('REDIS_CLIENT', 'phpredis'),

        // Rest of Redis configuration...
    ],

In addition to the default `scheme`, `host`, `port`, `database`, and `password` connection configurations, phpredis supports the following additional parameters: 

- `persistent` whether to use persistent connections, boolean
- `persistent_id` optional string by which to distinguish persistent connections, string
- `timeout` connection timeout in seconds, float
- `read_timeout` read timeout in seconds, float
- `retry_interval` retry interval in milliseconds, int
- `context` assoc array
- `options` assoc array

`context` is an array that contains additional connection related config like tls/ssl settings and `options` is an array that lets you configure additional phpredis features like:

- `name` internal connection name, may be useful for debugging purposes or when multiple connections are used
- `prefix` all keys will be prefixed with this string before sending to the redis server
- `scan` scan behaviour, one of: `Redis::SCAN_NORETRY` (default), `Redis::SCAN_RETRY`, `Redis::SCAN_PREFIX`, `Redis::SCAN_NOPREFIX`
- `serializer` serializer to use, depending on the phpredis version and compilation one of: `Redis::SERIALIZER_NONE` (default), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`
- `compression` compression algorithm to use, depending on the phpredis version and compilation one of: `Redis::COMPRESSION_NONE` (default), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`
- `compression_level` only used for ZSTD (`Redis::COMPRESSION_ZSTD_MIN`: 1, `Redis::COMPRESSION_ZSTD_DEFAULT`: 3, `Redis::COMPRESSION_ZSTD_MAX`: 22) and LZ4 (`<= 0` for default or `1 - 12` for high compression variant)

Refer to https://github.com/phpredis/phpredis for an in depth documentation of all available parameters.

Example phpredis server configuration in the `config/database.php` configuration file:

    'default' => [
        'scheme' => 'tlsv1.2',
        'host' => env('REDIS_HOST', 'localhost'),
        'password' => env('REDIS_PASSWORD', null),
        'port' => env('REDIS_PORT', 6379),
        'database' => 0,
        'timeout' => 0.25,
        'read_timeout' => 0.5,
        'retruy_interval' => 250,
        'context' => [
            // 'auth' => ['username', 'secret'],
            // 'stream' => ['verify_peer' => false],
        ],
        'options' => [
            'name' => 'demo_connection',
            'prefix' => 'service_name:',
            'scan' => Redis::SCAN_RETRY,
            'serializer' => Redis::SERIALIZER_MSGPACK,
            'compression' => Redis::COMPRESSION_LZ4,
            'compression_level' => 7,
        ],
    ],


<a name="interacting-with-redis"></a>
## Interacting With Redis

You may interact with Redis by calling various methods on the `Redis` [facade](/docs/{{version}}/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](https://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the Redis `GET` command by calling the `get` method on the `Redis` facade:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\Redis;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return \Illuminate\Http\Response
         */
        public function show($id)
        {
            return view('user.profile', [
                'user' => Redis::get('user:profile:'.$id)
            ]);
        }
    }

As mentioned above, you may call any of Redis' commands on the `Redis` facade. Laravel uses magic methods to pass the commands to the Redis server. If a Redis command expects arguments, you should pass those to the facade's corresponding method:

    use Illuminate\Support\Facades\Redis;

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

Alternatively, you may pass commands to the server using the `Redis` facade's `command` method, which accepts the name of the command as its first argument and an array of values as its second argument:

    $values = Redis::command('lrange', ['name', 5, 10]);

<a name="using-multiple-redis-connections"></a>
#### Using Multiple Redis Connections

Your application's `config/database.php` configuration file allows you to define multiple Redis connections / servers. You may obtain a connection to a specific Redis connection using the `Redis` facade's `connection` method:

    $redis = Redis::connection('connection-name');

To obtain an instance of the default Redis connection, you may call the `connection` method without any additional arguments:

    $redis = Redis::connection();

<a name="transactions"></a>
### Transactions

The `Redis` facade's `transaction` method provides a convenient wrapper around Redis' native `MULTI` and `EXEC` commands. The `transaction` method accepts a closure as its only argument. This closure will receive a Redis connection instance and may issue any commands it would like to this instance. All of the Redis commands issued within the closure will be executed in a single, atomic transaction:

    use Illuminate\Support\Facades\Redis;

    Redis::transaction(function ($redis) {
        $redis->incr('user_visits', 1);
        $redis->incr('total_visits', 1);
    });

> {note} When defining a Redis transaction, you may not retrieve any values from the Redis connection. Remember, your transaction is executed as a single, atomic operation and that operation is not executed until your entire closure has finished executing its commands.

#### Lua Scripts

The `eval` method provides another method of executing multiple Redis commands in a single, atomic operation. However, the `eval` method has the benefit of being able to interact with and inspect Redis key values during that operation. Redis scripts are written in the [Lua programming language](https://www.lua.org).

The `eval` method can be a bit scary at first, but we'll explore a basic example to break the ice. The `eval` method expects several arguments. First, you should pass the Lua script (as a string) to the method. Secondly, you should pass the number of keys (as an integer) that the script interacts with. Thirdly, you should pass the names of those keys. Finally, you may pass any other additional arguments that you need to access within your script.

In this example, we will increment a counter, inspect its new value, and increment a second counter if the first counter's value is greater than five. Finally, we will return the value of the first counter:

    $value = Redis::eval(<<<'LUA'
        local counter = redis.call("incr", KEYS[1])

        if counter > 5 then
            redis.call("incr", KEYS[2])
        end

        return counter
    LUA, 2, 'first-counter', 'second-counter');

> {note} Please consult the [Redis documentation](https://redis.io/commands/eval) for more information on Redis scripting.

<a name="pipelining-commands"></a>
### Pipelining Commands

Sometimes you may need to execute dozens of Redis commands. Instead of making a network trip to your Redis server for each command, you may use the `pipeline` method. The `pipeline` method accepts one argument: a closure that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be sent to the Redis server at the same time to reduce network trips to the server. The commands will still be executed in the order they were issued:

    use Illuminate\Support\Facades\Redis;

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel provides a convenient interface to the Redis `publish` and `subscribe` commands. These Redis commands allow you to listen for messages on a given "channel". You may publish messages to the channel from another application, or even using another programming language, allowing easy communication between applications and processes.

First, let's setup a channel listener using the `subscribe` method. We'll place this method call within an [Artisan command](/docs/{{version}}/artisan) since calling the `subscribe` method begins a long-running process:

    <?php

    namespace App\Console\Commands;

    use Illuminate\Console\Command;
    use Illuminate\Support\Facades\Redis;

    class RedisSubscribe extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Subscribe to a Redis channel';

        /**
         * Execute the console command.
         *
         * @return mixed
         */
        public function handle()
        {
            Redis::subscribe(['test-channel'], function ($message) {
                echo $message;
            });
        }
    }

Now we may publish messages to the channel using the `publish` method:

    use Illuminate\Support\Facades\Redis;

    Route::get('/publish', function () {
        // ...

        Redis::publish('test-channel', json_encode([
            'name' => 'Adam Wathan'
        ]));
    });

<a name="wildcard-subscriptions"></a>
#### Wildcard Subscriptions

Using the `psubscribe` method, you may subscribe to a wildcard channel, which may be useful for catching all messages on all channels. The channel name will be passed as the second argument to the provided closure:

    Redis::psubscribe(['*'], function ($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function ($message, $channel) {
        echo $message;
    });
