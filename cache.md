# 缓存

- [设置](#configuration)
- [缓存用法](#cache-usage)
- [递增与递减](#increments-and-decrements)
- [缓存标签](#cache-tags)
- [数据库缓存](#database-cache)

<a name="configuration"></a>
## 设置

Laravel 为各种不同的缓存系统提供一致的 API 。缓存设置档位在 `config/cache.php` 。您可以在此为应用程序指定使用哪一种缓存系统， Laravel 支持各种常见的后端缓存系统，像是 [Memcached](http://memcached.org) 和 [Redis](http://redis.io) 。

缓存设置档也包含多个其他选项，在文件里都有说明，所以请务必先阅读过。 Laravel 缺省使用`文件` 缓存系统，该系统会保存串行化、缓存对象在文件系统中。在大型应用程序上，建议使用保存在内存内的缓存系统，像是 Memcached 或 APC 。你甚至可以以同一个缓存系统设置多个缓存设置。

在 Laravel 中使用 Redis 缓存系统前， 必须先使用 Composer 安装 `predis/predis` 套件 (~1.0) 。

<a name="cache-usage"></a>
## 缓存用法

#### 保存项目到缓存中

	Cache::put('key', 'value', $minutes);

#### 使用 Carbon 对象设置缓存过期时间

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### 若是项目不存在，则将其存入缓存中

	Cache::add('key', 'value', $minutes);

当项目确实被加入缓存时，使用 `add` 方法将会回传 `true` 否则会回传 `false` 。

#### 确认项目是否存在

	if (Cache::has('key'))
	{
		//
	}

#### 从缓存中取得项目

	$value = Cache::get('key');

#### 取得项目或是回传默认值

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

#### 永久保存项目到缓存中

	Cache::forever('key', 'value');

有时候您会希望从缓存中取得项目，而当此项目不存在时会保存一笔默认值，您可以使用 `Cache::remember` 方法：

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

您也可以结合 `remember` 和 `forever` 方法：

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

请注意所有保存在缓存中的项目皆会被串行化，所以您可以任意保存各种型别的数据。

#### 从缓存拉出项目

如果您需要从缓存中取得项目后将它删除，您可以使用 `pull` 方法：

	$value = Cache::pull('key');

#### 从缓存中删除项目

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## 递增与递减

除了`文件`与`数据库`以外的缓存系统都支持`递增`和`递减`操作：

#### 递增值

	Cache::increment('key');

	Cache::increment('key', $amount);

#### 递减值

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## 缓存标签

> **注意：** `文件`或`数据库`这类缓存系统均不支持缓存标签。此外，使用带有「forever」的缓存标签时，挑选 `memcached` 这类缓存系统将获得最好的性能，它会自动清除过期的纪录。

#### 访问缓存标签

缓存标签允许您标记缓存内的相关项目，然后使用特定名称更新所有缓存标签。要访问缓存标签可以使用 `tags` 方法。

您可以保存缓存标签，借由将有串行表当作参数传入，或者作为标签名称的有序数组：

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(array('people', 'artists'))->put('Anne', $anne, $minutes);

您可以结合使用各种缓存保存方法与标签，包含 `remember`, `forever`, 和 `rememberForever` 。您也可以从已标记的缓存中访问项目，以及使用其他缓存方法像是 `increment` 和 `decrement` 。

#### 从已标记的缓存中访问项目

要访问已标记的缓存，可传入相同的有序标签列表。

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(array('people', 'authors'))->get('John');

您可以更新所有已标记的项目，使用指定名称或名称列表。例如，以下范例将会移除带有 `people` 或 `authors` 或者两者皆有的所有缓存标签，所以「Anne」和「John」皆会从缓存中被移除:

	Cache::tags('people', 'authors')->flush();

对照来看，以下范例将只会移除带有 `authors` 的标签，所以「John」会被移除，但是「Anne」不会。

	Cache::tags('authors')->flush();

<a name="database-cache"></a>
## 数据库缓存

当使用`数据库`缓存系统时，您必须设置一张数据表来保存缓存项目。数据表的 `Schema` 宣告范例如下：

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
