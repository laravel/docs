# 缓存

- [配置](#configuration)
- [缓存用法](#cache-usage)
- [增加 & 减少](#increments-and-decrements)
- [缓存区](#cache-sections)
- [数据库缓存](#database-cache)

<a name="configuration"></a>
## 配置

Laravel 对不同的缓存机制提供了一套统一的API。缓存配置信息存放于`app/config/cache.php`文件。在该配置文件中，你可以指定整个应用程序所使用的缓存驱动器。Laravel自身支持大多数流行的缓存服务器，例如[Memcached](http://memcached.org)和[Redis](http://redis.io)。

缓存配置文件还包含了其他配置项，文件里都有详细说明，因此，请务必查看这些配置项和其描述信息。默认情况下，Laravel被配置为使用`file`缓存驱动，它将数据序列化，并存放于文件系统中。在大型应用中，强烈建议使用基于内存的缓存系统，例如Memcached或APC。

<a name="cache-usage"></a>
## 缓存用法

**将某一数据存入缓存**

	Cache::put('key', 'value', $minutes);

**当某一数据不在缓存中是才将其保存**

	Cache::add('key', 'value', $minutes);

**检查缓存中是否有某个key对应的数据**

	if (Cache::has('key'))
	{
		//
	}

**从缓存中取得数据**

	$value = Cache::get('key');

**从缓存中取得数据，如果数据不存，则返回指定的默认值**

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

**将数据永久地存于缓存中**

	Cache::forever('key', 'value');

有时你可能想从缓存中取得某项数据，但是还希望在数据不存在时存储一项默认值。那就可以通过 `Cache::remember`方法实现：

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

还可以将`remember`和`forever`方法结合使用：

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

注意：所有存在于缓存中的数据都是经过序列化的，因此，你可以存储任何类型的数据。

**从缓存中删除某项数据**

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## 增加 & 减少

除了`文件`和`数据库`驱动器，其他驱动器都支持`增加`和`减少`操作：

**让某个值增加**

	Cache::increment('key');

	Cache::increment('key', $amount);

**让某个值减少**

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-sections"></a>
## 缓存区

> **注意：** `文件`或`数据库`缓存驱动都不支持缓存区。

缓存区允许你将相关数据项分组存放，然后可以对整个区进行清空操作。要想访问缓存区，需要使用`section`方法：

**访问缓存区**

	Cache::section('people')->put('John', $john);

	Cache::section('people')->put('Anne', $anne);

你也可以从缓存区中取得缓存项，也可以使用其他的缓存方法，例如`increment`和`decrement`：

**从缓存区中取得数据项**

	$anne = Cache::section('people')->get('Anne');

你可以使用flush方法清空整个缓存区：

	Cache::section('people')->flush();

<a name="database-cache"></a>
## 数据库缓存

当使用`数据库`缓存驱动时，你需要设置一个数据表来缓存数据。以下是表`Schema`定义案例：

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)