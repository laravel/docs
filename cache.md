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

	Schema::create('cache', function($table) {
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

However, you may also use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts.

For example, let's import the `Cache` facade into a controller:

	<?php namespace App\Http\Controllers;

	use Cache;
	use Illuminate\Routing\Controller;

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

<a name="cache-usage"></a>
## Cache Usage

#### Storing An Item In The Cache

When you place an item in the cache, you will need to specify the number of minutes for which the value should be cached:

	Cache::put('key', 'value', $minutes);

#### Using DateTime Objects To Set Expire Time

You may also pass a PHP `DateTime` instance representing the expiration time of the cache item:

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### Storing An Item In The Cache If It Doesn't Exist

The `add` method will return `true` if the item is actually **added** to the cache. Otherwise, the method will return `false`.

	Cache::add('key', 'value', $minutes);

#### Checking For Item Existence

	if (Cache::has('key')) {
		//
	}

#### Retrieving An Item From The Cache

	$value = Cache::get('key');

#### Retrieving An Item Or Returning A Default Value

The second argument passed to the `get` method will be returned if the specified item does not exist in the cache:

	$value = Cache::get('key', 'default');

You may even pass a `Closure` as the default value. The result of the `Closure` will be returned if the specified item does not exist in the cache:

	$value = Cache::get('key', function() {
		return 'default';
	});

#### Incrementing / Decrementing Values

> **Note:** All cache drivers except the `database` driver support the increment and decrement operations:

	Cache::increment('key');

	Cache::increment('key', $amount);

	Cache::decrement('key');

	Cache::decrement('key', $amount);

#### Storing An Item In The Cache Permanently

	Cache::forever('key', 'value');

#### Retrieve An Item & Update Value If Missing

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. You may do this using the `Cache::remember` method:

	$value = Cache::remember('users', $minutes, function() {
		return DB::table('users')->get();
	});

You may also combine the `remember` and `forever` methods:

	$value = Cache::rememberForever('users', function() {
		return DB::table('users')->get();
	});

> **Note:** All items stored in the cache are serialized, so you are free to store any type of data.

#### Pulling An Item From The Cache

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method:

	$value = Cache::pull('key');

#### Removing An Item From The Cache

	Cache::forget('key');

<a name="accessing-multiple-cache-stores"></a>
## Accessing Multiple Cache Stores

Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file:

	$value = Cache::store('file')->get('foo');

	Cache::store('redis')->put('bar', 'baz', 10);
