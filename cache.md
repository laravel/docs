# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
    - [Obtaining A Cache Instance](#obtaining-a-cache-instance)
    - [Retrieving Items From The Cache](#retrieving-items-from-the-cache)
    - [Storing Items In The Cache](#storing-items-in-the-cache)
    - [Removing Items From The Cache](#removing-items-from-the-cache)
    - [The Cache Helper](#the-cache-helper)
- [Cache Tags](#cache-tags)
    - [Storing Tagged Cache Items](#storing-tagged-cache-items)
    - [Accessing Tagged Cache Items](#accessing-tagged-cache-items)
    - [Removing Tagged Cache Items](#removing-tagged-cache-items)
- [Atomic Locks](#atomic-locks)
    - [Driver Prerequisites](#lock-driver-prerequisites)
    - [Managing Locks](#managing-locks)
    - [Managing Locks Across Processes](#managing-locks-across-processes)
- [Adding Custom Cache Drivers](#adding-custom-cache-drivers)
    - [Writing The Driver](#writing-the-driver)
    - [Registering The Driver](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as [Memcached](https://memcached.org) or [Redis](https://redis.io).

Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application.

<a name="configuration"></a>
## Configuration

Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache driver you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects on the server's filesystem. For larger applications, it is recommended that you use a more robust driver such as Memcached or Redis. You may even configure multiple cache configurations for the same driver.

<a name="driver-prerequisites"></a>
### Driver Prerequisites

<a name="prerequisites-database"></a>
#### Database

When using the `database` cache driver, you will need to setup a table to contain the cache items. You'll find an example `Schema` declaration for the table below:

    Schema::create('cache', function ($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> {tip} You may also use the `php artisan cache:table` Artisan command to generate a migration with the proper schema.

<a name="memcached"></a>
#### Memcached

Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started:

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

If needed, you may set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`:

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### Redis

Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. [Laravel Sail](/docs/{{version}}/sail) already includes this extension. In addition, official Laravel deployment platforms such as [Laravel Forge](https://forge.laravel.com) and [Laravel Vapor](https://vapor.laravel.com) have the PhpRedis extension installed by default.

For more information on configuring Redis, consult its [Laravel documentation page](/docs/{{version}}/redis#configuration).

<a name="dynamodb"></a>
#### DynamoDB

The DynamoDB driver requires you to set up a table to store all of the cached data. Luckily there's an easy way with Laravel to set up one. Simply run the following command to create the cache table in DynamoDB:

    php artisan cache:dynamodb

This command will use your settings for the `dynamodb` store in your `cache.php` config file to make the connection and create the table for you. After it's set up you can use your DynamoDB driver for caching.

If you don't want to use a command to set this up but rather something like AWS CloudFormation you should create the table with the following configuration:

```json
{
    TableName : "cache",
    KeySchema: [
        {
            AttributeName: "key",
            KeyType: "HASH",
        }
    ],
    AttributeDefinitions: [
        {
            AttributeName: "key",
            AttributeType: "S"
        }
    ],
    ProvisionedThroughput: { // Only specified if using provisioned mode
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1
    }
}
```

The `TableName` and `AttributeName` values should match the `table` and `key` config values from `cache.stores.dynamodb` respectively.

<a name="cache-usage"></a>
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
### Obtaining A Cache Instance

To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * Show a list of all users of the application.
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

<a name="accessing-multiple-cache-stores"></a>
#### Accessing Multiple Cache Stores

Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file:

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes

<a name="retrieving-items-from-the-cache"></a>
### Retrieving Items From The Cache

The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist:

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service:

    $value = Cache::get('key', function () {
        return DB::table(...)->get();
    });

<a name="checking-for-item-existence"></a>
#### Checking For Item Existence

The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`:

    if (Cache::has('key')) {
        //
    }

<a name="incrementing-decrementing-values"></a>
#### Incrementing / Decrementing Values

The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value:

    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### Retrieve & Store

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. For example, you may wish to retrieve all users from the cache or, if they don't exist, retrieve them from the database and add them to the cache. You may do this using the `Cache::remember` method:

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache.

You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist:

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### Retrieve & Delete

If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache:

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### Storing Items In The Cache

You may use the `put` method on the `Cache` facade to store items in the cache:

    Cache::put('key', 'value', $seconds = 10);

If the storage time is not passed to the `put` method, the item will be stored indefinitely:

    Cache::put('key', 'value');

Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item:

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### Store If Not Present

The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation:

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### Storing Items Forever

The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method:

    Cache::forever('key', 'value');

> {tip} If you are using the Memcached driver, items that are stored "forever" may be removed when the cache reaches its size limit.

<a name="removing-items-from-the-cache"></a>
### Removing Items From The Cache

You may remove items from the cache using the `forget` method:

    Cache::forget('key');

You may also remove items by providing a zero or negative number of expiration seconds:

    Cache::put('key', 'value', 0);

    Cache::put('key', 'value', -5);

You may clear the entire cache using the `flush` method:

    Cache::flush();

> {note} Flushing the cache does not respect your configured cache "prefix" and will remove all entries from the cache. Consider this carefully when clearing a cache which is shared by other applications.

<a name="the-cache-helper"></a>
### The Cache Helper

In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key:

    $value = cache('key');

If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration:

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods:

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> {tip} When testing call to the global `cache` function, you may use the `Cache::shouldReceive` method just as if you were [testing the facade](/docs/{{version}}/mocking#mocking-facades).

<a name="cache-tags"></a>
## Cache Tags

> {note} Cache tags are not supported when using the `file`, `dynamodb`, or `database` cache drivers. Furthermore, when using multiple tags with caches that are stored "forever", performance will be best with a driver such as `memcached`, which automatically purges stale records.

<a name="storing-tagged-cache-items"></a>
### Storing Tagged Cache Items

Cache tags allow you to tag related items in the cache and then flush all cached values that have been assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` a value into the cache:

    Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

    Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);

<a name="accessing-tagged-cache-items"></a>
### Accessing Tagged Cache Items

To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method and then call the `get` method with the key you wish to retrieve:

    $john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

<a name="removing-tagged-cache-items"></a>
### Removing Tagged Cache Items

You may flush all items that are assigned a tag or list of tags. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache:

    Cache::tags(['people', 'authors'])->flush();

In contrast, this statement would remove only cached values tagged with `authors`, so `Anne` would be removed, but not `John`:

    Cache::tags('authors')->flush();

<a name="atomic-locks"></a>
## Atomic Locks

> {note} To utilize this feature, your application must be using the `memcached`, `redis`, `dynamodb`, `database`, `file`, or `array` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

<a name="lock-driver-prerequisites"></a>
### Driver Prerequisites

<a name="atomic-locks-prerequisites-database"></a>
#### Database

When using the `database` cache driver, you will need to setup a table to contain your application's cache locks. You'll find an example `Schema` declaration for the table below:

    Schema::create('cache_locks', function ($table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

<a name="managing-locks"></a>
### Managing Locks

Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Forge](https://forge.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method:

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // Lock acquired for 10 seconds...

        $lock->release();
    }

The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock:

    Cache::lock('foo')->get(function () {
        // Lock acquired indefinitely and automatically released...
    });

If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock can not be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown:

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // Lock acquired after waiting a maximum of 5 seconds...
    } catch (LockTimeoutException $e) {
        // Unable to acquire lock...
    } finally {
        optional($lock)->release();
    }

The example above may be simplified by passing a closure to the `block` method. When a closure is passed to this method, Laravel will attempt to acquire the lock for the specified number of seconds and will automatically release the lock once the closure has been executed:

    Cache::lock('foo', 10)->block(5, function () {
        // Lock acquired after waiting a maximum of 5 seconds...
    });

<a name="managing-locks-across-processes"></a>
### Managing Locks Across Processes

Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token.

In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method:

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($result = $lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token:

    Cache::restoreLock('processing', $this->owner)->release();

If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method:

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
### Writing The Driver

To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts). So, a MongoDB cache implementation might look something like this:

    <?php

    namespace App\Extensions;

    use Illuminate\Contracts\Cache\Store;

    class MongoStore implements Store
    {
        public function get($key) {}
        public function many(array $keys) {}
        public function put($key, $value, $seconds) {}
        public function putMany(array $values, $seconds) {}
        public function increment($key, $value = 1) {}
        public function decrement($key, $value = 1) {}
        public function forever($key, $value) {}
        public function forget($key) {}
        public function flush() {}
        public function getPrefix() {}
    }

We just need to implement each of these methods using a MongoDB connection. For an example of how to implement each of these methods, take a look at the `Illuminate\Cache\MemcachedStore` in the [Laravel framework source code](https://github.com/laravel/framework). Once our implementation is complete, we can finish our custom driver registration by calling the `Cache` facade's `extend` method:

    Cache::extend('mongo', function ($app) {
        return Cache::repository(new MongoStore);
    });

> {tip} If you're wondering where to put your custom cache driver code, you could create an `Extensions` namespace within your `app` directory. However, keep in mind that Laravel does not have a rigid application structure and you are free to organize your application according to your preferences.

<a name="registering-the-driver"></a>
### Registering The Driver

To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class:

    <?php

    namespace App\Providers;

    use App\Extensions\MongoStore;
    use Illuminate\Support\Facades\Cache;
    use Illuminate\Support\ServiceProvider;

    class CacheServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            $this->app->booting(function () {
                 Cache::extend('mongo', function ($app) {
                     return Cache::repository(new MongoStore);
                 });
             });
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            //
        }
    }

The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/{{version}}/container).

Once your extension is registered, update your `config/cache.php` configuration file's `driver` option to the name of your extension.

<a name="events"></a>
## Events

To execute code on every cache operation, you may listen for the [events](/docs/{{version}}/events) fired by the cache. Typically, you should place these event listeners within your application's `App\Providers\EventServiceProvider` class:

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Cache\Events\CacheHit' => [
            'App\Listeners\LogCacheHit',
        ],

        'Illuminate\Cache\Events\CacheMissed' => [
            'App\Listeners\LogCacheMissed',
        ],

        'Illuminate\Cache\Events\KeyForgotten' => [
            'App\Listeners\LogKeyForgotten',
        ],

        'Illuminate\Cache\Events\KeyWritten' => [
            'App\Listeners\LogKeyWritten',
        ],
    ];
