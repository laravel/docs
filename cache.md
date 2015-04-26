# Cache

- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Tags](#cache-tags)
- [Cache Events](#cache-events)
- [Database Cache](#database-cache)
- [Memcached Cache](#memcached-cache)
- [Redis Cache](#redis-cache)

<a name="configuration"></a>
## Configuration

Laravel provides a unified API for various caching systems. The cache configuration is located at `config/cache.php`. In this file you may specify which cache driver you would like used by default throughout your application. Laravel supports popular caching backends like [Memcached](http://memcached.org) and [Redis](http://redis.io) out of the box.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects in the filesystem. For larger applications, it is recommended that you use an in-memory cache such as Memcached or APC. You may even configure multiple cache configurations for the same driver.

Before using a Redis cache with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

<a name="cache-usage"></a>
## Cache Usage

#### Storing An Item In The Cache

	Cache::put('key', 'value', $minutes);

#### Using Carbon Objects To Set Expire Time

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### Storing An Item In The Cache If It Doesn't Exist

	Cache::add('key', 'value', $minutes);

The `add` method will return `true` if the item is actually **added** to the cache. Otherwise, the method will return `false`.

#### Checking For Existence In Cache

	if (Cache::has('key'))
	{
		//
	}

#### Retrieving An Item From The Cache

	$value = Cache::get('key');

#### Retrieving An Item Or Returning A Default Value

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

#### Storing An Item In The Cache Permanently

	Cache::forever('key', 'value');

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. You may do this using the `Cache::remember` method:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

You may also combine the `remember` and `forever` methods:

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

Note that all items stored in the cache are serialized, so you are free to store any type of data.

#### Pulling An Item From The Cache

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method:

	$value = Cache::pull('key');

#### Removing An Item From The Cache

	Cache::forget('key');

#### Access Specific Cache Stores

When using multiple cache stores, you may access them via the `store` method:

	$value = Cache::store('foo')->get('key');

<a name="increments-and-decrements"></a>
## Increments & Decrements

All drivers except `database` support the `increment` and `decrement` operations:

#### Incrementing A Value

	Cache::increment('key');

	Cache::increment('key', $amount);

#### Decrementing A Value

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## Cache Tags

> **Note:** Cache tags are not supported when using the `file` or `database` cache drivers. Furthermore, when using multiple tags with caches that are stored "forever", performance will be best with a driver such as `memcached`, which automatically purges stale records.

#### Accessing A Tagged Cache

Cache tags allow you to tag related items in the cache, and then flush all caches tagged with a given name. To access a tagged cache, use the `tags` method.

You may store a tagged cache by passing in an ordered list of tag names as arguments, or as an ordered array of tag names:

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(['people', 'artists'])->put('Anne', $anne, $minutes);

You may use any cache storage method in combination with tags, including `remember`, `forever`, and `rememberForever`. You may also access cached items from the tagged cache, as well as use the other cache methods such as `increment` and `decrement`.

#### Accessing Items In A Tagged Cache

To access a tagged cache, pass the same ordered list of tags used to save it.

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(['people', 'authors'])->get('John');

You may flush all items tagged with a name or list of names. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both "Anne" and "John" would be removed from the cache:

	Cache::tags('people', 'authors')->flush();

In contrast, this statement would remove only caches tagged with `authors`, so "John" would be removed, but not "Anne".

	Cache::tags('authors')->flush();

<a name="cache-events"></a>
## Cache Events

To execute code on every cache operation, you may listen for the events fired by the cache:

	Event::listen('cache.hit', function($key, $value) {
		//
	});

	Event::listen('cache.missed', function($key) {
		//
	});

	Event::listen('cache.write', function($key, $value, $minutes) {
		//
	});

	Event::listen('cache.delete', function($key) {
		//
	});

<a name="database-cache"></a>
## Database Cache

When using the `database` cache driver, you will need to setup a table to contain the cache items. You'll find an example `Schema` declaration for the table below:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

<a name="memcached-cache"></a>
#### Memcached Cache

Using the Memcached cache requires the [Memcached PECL package](http://pecl.php.net/package/memcached) to be installed.

The default [configuration](#configuration) uses TCP/IP based on [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php):

	'memcached' => array(
		array('host' => '127.0.0.1', 'port' => 11211, 'weight' => 100),
	),

You may also set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`:

	'memcached' => array(
		array('host' => '/var/run/memcached/memcached.sock', 'port' => 0, 'weight' => 100),
	),

<a name="redis-cache"></a>
#### Redis Cache

See [Redis Configuration](/docs/redis#configuration)
