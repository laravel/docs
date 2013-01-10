# Cache

- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Database Cache](#database-cache)

<a name="configuration"></a>
## Configuration

Laravel provides a unified API for various caching systems. The cache configuration is located at `app/config/cache.php`. In this file you may specify which cache driver you would like used by default throughout your application. Laravel supports popular caching backends like [Memcached](http://memcached.org) and [Redis](http://redis.io) out of the box.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects in the filesystem. For larger applications, it is recommended that you use an in-memory cache such as Memcached or APC.

<a name="cache-usage"></a>
## Cache Usage

**Storing An Item In The Cache**

	Cache::put('key', 'value', $minutes);

**Retrieving An Item From The Cache**

	$value = Cache::get('key');

**Retrieving An Item Or Returning A Default Value**

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

**Storing An Item In The Cache Permanently**

	Cache::forever('key', 'value');

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doens't exist. You may do this using the `Cache::remember` method:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

You may also combine the `remember` and `forever` methods:

	$value = Cache::rememberForever('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

Note that all items stored in the cache are serialized, so you are free to store any type of data.

**Removing An Item From The Cache**

	Cache::forget('key');

<a name="database-cache"></a>
## Database Cache

When using the `database` cache driver, you will need to setup a table to contain the cache items. Below is an example `Schema` declaration for the table:

	Schema::create('cache', function($t)
	{
		$t->string('key')->unique();
		$t->text('value');
		$t->integer('expiration');
	});