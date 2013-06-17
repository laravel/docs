# Cache

- [The Basics](#basics)
- [Configuration](#configuration)
- [Cache Drivers](#cache-drivers)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Sections](#cache-sections)
- [Database Cache](#database-cache)

<a name="basics"></a>
## The Basics

Imagine your application displays the ten most popular songs as voted on by your users. Do you really need to look up these ten songs every time someone visits your site? What if you could store them for 10 minutes, or even an hour, allowing you to dramatically speed up your application? Laravel's caching makes it simple.

Laravel provides a unified API for various caching systems:

* File System
* Database
* [Memcached](http://memcached.org)
* [Redis](http://redis.io)
* [APC](http://php.net/manual/en/book.apc.php)
* Arrays(memory).

<a name="configuration"></a>
## Configuration

The cache configuration is located at `app/config/cache.php`. In this file you may specify which cache driver you would like used by default throughout your application.

The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options.

By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects in the filesystem. For larger applications, it is recommended that you use an in-memory cache such as Memcached or APC. If you're satisfied with this driver, no other configuration is required. You're ready to start using it.

<a name="cache-drivers"></a>
## Cache Drivers

### File

Stores the serialized, cached objects in the filesystem.

### Database

The database cache driver uses a given [database table](#database-cache) as a simple key-value store.

### APC

Alternative PHP Cache (APC) is a free, open source (PHP license) framework that heavily optimizes and tunes the output of the PHP bytecode compiler and stores the final, compiled result in shared memory. It also provides the ability to store and retrieve keyed data in a global "data store", thereby allowing you to cache and significantly speed up access to very commonly used data without having to constantly go to disk or SQL backends.

### Memcached

Memcached is an ultra-fast, open-source distributed memory object caching system used by sites such as Wikipedia and Facebook. Before using Laravel's Memcached driver, you will need to install and configure Memcached and the PHP Memcache extension on your server. Before using the Memcached cache driver, you must set your servers in `memcached` at `app/config/cache.php`.

### Redis

Redis is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets, and sorted sets.

### Array (in-memory)

The "memory" cache driver does not actually cache anything to disk. It simply maintains an internal array of the cache data for the current request. This makes it perfect for unit testing your application in isolation from any storage mechanism. It should never be used as a "real" cache driver.

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

	Cache::section('people')->put('John', $john);

	Cache::section('people')->put('Anne', $anne);

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
