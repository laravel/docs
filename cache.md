# Cache

- [Configuration](#configuration)
- [Accessing The Cache](#accessing-the-cache)
- [Cache Usage](#cache-usage)
- [Accessing Multiple Cache Stores](#accessing-multiple-cache-stores)

<a name="configuration"></a>
## Configuration

Laravel provides a unified API for various caching systems. The cache configuration is located at `config/cache.php`. In this file you may specify which cache driver you would like used by default throughout your application. Laravel supports popular caching backends like [Memcached](http://memcached.org) and [Redis](http://redis.io) out of the box.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects in the filesystem. For larger applications, it is recommended that you use an in-memory cache such as Memcached or APC. You may even configure multiple cache configurations for the same driver.

### Cache Prerequisites

#### Database

When using the `database` cache driver, you will need to setup a table to contain the cache items. You'll find an example `Schema` declaration for the table below:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

#### Memcached

Using the Memcached cache requires the [Memcached PECL package](http://pecl.php.net/package/memcached) to be installed.

The default [configuration](#configuration) uses TCP/IP based on [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php):

	'memcached' => [
		[
			'host' => '127.0.0.1',
			'port' => 11211,
			'weight' => 100
		],
	],

You may also set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`:

	'memcached' => [
		[
			'host' => '/var/run/memcached/memcached.sock',
			'port' => 0,
			'weight' => 100
		],
	],

#### Redis

Before using a Redis cache with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

For more information on configuring Redis, consult its [Laravel documentation page](/docs/{{version}}/redis#configuration).

<a name="accessing-the-cache"></a>
## Accessing The Cache

The `Illuminate\Contracts\Cache\Factory` and `Illuminate\Contracts\Cache\Repository` [contracts](/docs/{{version}}/contracts) provide access to Laravel's cache services. The `Factory` contract provides access to all cache drivers defined for your application. The `Repository` contract is typically an implementation of the default cache driver for your application as specified by your `cache` configuration file.

To obtain an implementation of these contracts, simply type-hint them in a class that is resolved by the Laravel [service container](/docs/{{version}}/container), such as a controller, middleware, event listener, queued job, etc.

For example, to retrieve a cache implementation in a controller:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Cache\Repository as Cache;

	class UserController extends Controller
	{
		/**
		 * The cache implementation.
		 */
		protected $cache;

		/**
		 * Create a new controller instance.
		 *
		 * @param  \Illuminate\Contracts\Cache\Repository  $cache
		 * @return void
		 */
		public function __construct(Cache $cache)
		{
			$this->cache = $cache;
		}

		/**
		 * Show a list of all users of the application.
		 *
		 * @return Response
		 */
		public function index()
		{
			$value = $this->cache->get('key');

			//
		}
	}

Of course, service container dependencies are resolved recursively. So, if your controller receives a `UserRepository` instance, and that `UserRepository` type-hints a cache contract on its constructor, the cache implementation will be automatically injected into the `UserRepository`.

<a name="cache-usage"></a>
## Cache Usage

Once you have an instance of the cache, you may use it to retrieve and set values.

#### Storing An Item In The Cache

When you place an item in the cache, you will need to specify the number of minutes for which the value should be cached:

	$this->cache->put('key', 'value', $minutes);

#### Using DateTime Objects To Set Expire Time

You may also pass a PHP `DateTime` instance representing the expiration time of the cache item:

	$expiresAt = Carbon::now()->addMinutes(10);

	$this->cache->put('key', 'value', $expiresAt);

#### Storing An Item In The Cache If It Doesn't Exist

The `add` method will return `true` if the item is actually **added** to the cache. Otherwise, the method will return `false`.

	$this->cache->add('key', 'value', $minutes);

#### Checking For Item Existence

	if ($this->cache->has('key')) {
		//
	}

#### Retrieving An Item From The Cache

	$value = $this->cache->get('key');

#### Retrieving An Item Or Returning A Default Value

The second argument passed to the `get` method will be returned if the specified item does not exist in the cache:

	$value = $this->cache->get('key', 'default');

You may even pass a `Closure` as the default value. The result of the `Closure` will be returned if the specified item does not exist in the cache:

	$value = $this->cache->get('key', function() {
		return 'default';
	});

#### Incrementing / Decrementing Values

> **Note:** All cache drivers except the `database` driver support the increment and decrement operations:

	$this->cache->increment('key');

	$this->cache->increment('key', $amount);

	$this->cache->decrement('key');

	$this->cache->decrement('key', $amount);

#### Storing An Item In The Cache Permanently

	$this->cache->forever('key', 'value');

#### Retrieve An Item & Update Value If Missing

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. You may do this using the `Cache::remember` method:

	$value = $this->cache->remember('users', $minutes, function() {
		return DB::table('users')->get();
	});

You may also combine the `remember` and `forever` methods:

	$value = $this->cache->rememberForever('users', function() {
		return DB::table('users')->get();
	});

> **Note:** All items stored in the cache are serialized, so you are free to store any type of data.

#### Pulling An Item From The Cache

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method:

	$value = $this->cache->pull('key');

#### Removing An Item From The Cache

	$this->cache->forget('key');

<a name="accessing-multiple-cache-stores"></a>
## Accessing Multiple Cache Stores

When using multiple cache stores, you may access them via an implementation of the `Illuminate\Contracts\Cache\Factory` [contract](/docs/{{version}}/contracts). First, you will need to obtain an implementation of this contract from the Laravel [service container](/docs/{{version}}/container). You can do this by type-hinting the contract on a class that is resolved by the container. In this example, we'll type-hint it on a controller:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Cache\Factory as CacheFactory;

	class UserController extends Controller
	{
		/**
		 * The cache implementation.
		 */
		protected $cache;

		/**
		 * Create a new controller instance.
		 *
		 * @param  \Illuminate\Contracts\Cache\Factory  $cache
		 * @return void
		 */
		public function __construct(CacheFactory $cache)
		{
			$this->cache = $cache;
		}
	}

Once you have obstained an implementation of the contract, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file:

	$value = $this->cache->store('file')->get('foo');

	$this->cache->store('redis')->put('bar', 'baz', 10);
