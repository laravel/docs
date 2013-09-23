# Cache

- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Sections](#cache-sections)
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

<a name="cache-sections"></a>
## Cache Sections

> **Note:** Cache sections are not supported when using the `file` or `database` cache drivers.

Cache sections allow you to group related items in the cache, and then flush the entire section. To access a section, use the `section` method:

**Accessing A Cache Section**

	Cache::section('people')->put('John', $john, $minutes);

	Cache::section('people')->put('Anne', $anne, $minutes);

You may also access cached items from the section, as well as use the other cache methods such as `increment` and `decrement`:

**Accessing Items In A Cache Section**

	$anne = Cache::section('people')->get('Anne');

Then you may flush all items in the section:

	Cache::section('people')->flush();

<a name="database-cache"></a>
## Database Cache

When using the `database` cache driver, you will need to setup a table to contain the cache items. Below is an example `Schema` declaration for the table:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
