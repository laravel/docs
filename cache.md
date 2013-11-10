# Cache

- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Tags](#cache-tags)
- [Database Cache](#database-cache)

<a name="configuration"></a>
## Configuration

Laravel provides a unified API for various caching systems. The cache configuration is located at `app/config/cache.php`. In this file you may specify which cache driver you would like used by default throughout your application. Laravel supports popular caching backends like [Memcached](http://memcached.org) and [Redis](http://redis.io) out of the box.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects in the filesystem. For larger applications, it is recommended that you use an in-memory cache such as Memcached or APC.

<a name="cache-usage"></a>
## Cache Usage

**Storing An Item In The Cache**

	Cache::put('key', 'value', $minutes);

**Storing An Item In The Cache If It Doesn't Exist**

	Cache::add('key', 'value', $minutes);

**Checking For Existence In Cache**

	if (Cache::has('key'))
	{
		//
	}

**Retrieving An Item From The Cache**

	$value = Cache::get('key');

**Retrieving An Item Or Returning A Default Value**

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

**Storing An Item In The Cache Permanently**

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

**Removing An Item From The Cache**

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## Increments & Decrements

All drivers except `file` and `database` support the `increment` and `decrement` operations:

**Incrementing A Value**

	Cache::increment('key');

	Cache::increment('key', $amount);

**Decrementing A Value**

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## Cache Tags

> **Note:** Cache tags are not supported when using the `file` or `database` cache drivers. When using multiple tags with caches stored forever, performance will be best with a driver such as `memcached`, which automatically purges least-recently-used records, vs a driver such as `redis`.

> **Note:** Cache sections have been superseded by Cache tags. The section() method has been deprecated, but will remain an alias for tags, and work as before.

Cache tags allow you to tag related items in the cache, and then flush all caches tagged with a given name. To access a tagged cache, use the `tags` method:

**Accessing A Tagged Cache**

You may store a tagged cache by passing in an ordered list of tag names as arguments, or as an ordered array of tag names.

	Cache::tags('people', 'authors')->put('John', $john, $minutes);
	Cache::tags(array('people', 'artists'))->put('Anne', $anne, $minutes);

You may use any cache storage method in combination with tags, including `remember`, `forever`, and `rememberForever`. You may also access cached items from the tagged cache, as well as use the other cache methods such as `increment` and `decrement`:

**Accessing Items In A Tagged Cache**

To access a tagged cache, pass the same ordered list of tags used to save it.

	$anne = Cache::tags('people', 'artists')->get('Anne');
	$john = $cache::tags(array('people', 'authors')->get('John);

You may flush all items tagged with a name or list of names. This

	Cache::tags('people', 'authors')->flush();

would remove all caches tagged with either 'people', 'authors', or both, so both Ann and John would be removed.

	Cache::tags('authors')->flush();

would remove only caches tagged with 'author', so John would be removed, but not Anne.

<a name="database-cache"></a>
## Database Cache

When using the `database` cache driver, you will need to setup a table to contain the cache items. Below is an example `Schema` declaration for the table:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
