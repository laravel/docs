# Redis

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
    - [Pipelining Commands](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## Introduction

[Redis](http://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](http://redis.io/topics/data-types#strings), [hashes](http://redis.io/topics/data-types#hashes), [lists](http://redis.io/topics/data-types#lists), [sets](http://redis.io/topics/data-types#sets), and [sorted sets](http://redis.io/topics/data-types#sorted-sets). Before using Redis with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

<a name="configuration"></a>
### Configuration

The Redis configuration for your application is located in the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers used by your application:

    'redis' => [

        'cluster' => false,

        'default' => [
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'database' => 0,
        ],

    ],

The default server configuration should suffice for development. However, you are free to modify this array based on your environment. Simply give each Redis server a name, and specify the host and port used by the server.

The `cluster` option will tell the Laravel Redis client to perform client-side sharding across your Redis nodes, allowing you to pool nodes and create a large amount of available RAM. However, note that client-side sharding does not handle failover; therefore, is primarily suited for cached data that is available from another primary data store.

Additionally, you may define an `options` array value in your Redis connection definition, allowing you to specify a set of Predis [client options](https://github.com/nrk/predis/wiki/Client-Options).

If your Redis server requires authentication, you may supply a password by adding a `password` configuration item to your Redis server configuration array.

> **Note:** If you have the Redis PHP extension installed via PECL, you will need to rename the alias for Redis in your `config/app.php` file.

<a name="basic-usage"></a>
## Basic Usage

You may interact with Redis by calling various methods on the `Redis` [facade](/docs/{{version}}/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](http://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the `GET` command on Redis by calling the `get` method on the `Redis` facade:

    <?php

    namespace App\Http\Controllers;

    use Redis;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            $user = Redis::get('user:profile:'.$id);

            return view('user.profile', ['user' => $user]);
        }
    }

Of course, as mentioned above, you may call any of the Redis commands on the `Redis` facade. Laravel uses magic methods to pass the commands to the Redis server, so simply pass the arguments the Redis command expects:

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

Alternatively, you may also pass commands to the server using the `command` method, which accepts the name of the command as its first argument, and an array of values as its second argument:

    $values = Redis::command('lrange', ['name', 5, 10]);

#### Using Multiple Redis Connections

You may get a Redis instance by calling the `Redis::connection` method:

    $redis = Redis::connection();

This will give you an instance of the default Redis server. If you are not using server clustering, you may pass the server name to the `connection` method to get a specific server as defined in your Redis configuration:

    $redis = Redis::connection('other');

<a name="pipelining-commands"></a>
### Pipelining Commands

Pipelining should be used when you need to send many commands to the server in one operation. The `pipeline` method accepts one argument: a `Closure` that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be executed within a single operation:

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

Laravel also provides a convenient interface to the Redis `publish` and `subscribe` commands. These Redis commands allow you to listen for messages on a given "channel". You may publish messages to the channel from another application, or even using another programming language, allowing easy communication between applications / processes.

First, let's setup a listener on a channel via Redis using the `subscribe` method. We will place this method call within an [Artisan command](/docs/{{version}}/artisan) since calling the `subscribe` method begins a long-running process:

    <?php

    namespace App\Console\Commands;

    use Redis;
    use Illuminate\Console\Command;

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
            Redis::subscribe(['test-channel'], function($message) {
                echo $message;
            });
        }
    }

Now, we may publish messages to the channel using the `publish` method:

    Route::get('publish', function () {
        // Route logic...

        Redis::publish('test-channel', json_encode(['foo' => 'bar']));
    });

#### Wildcard Subscriptions

Using the `psubscribe` method, you may subscribe to a wildcard channel, which is useful for catching all messages on all channels. The `$channel` name will be passed as the second argument to the provided callback `Closure`:

    Redis::psubscribe(['*'], function($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function($message, $channel) {
        echo $message;
    });
