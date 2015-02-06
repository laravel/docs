# Cache

- [設定](#configuration)
- [快取用法](#cache-usage)
- [遞增與遞減](#increments-and-decrements)
- [快取標籤](#cache-tags)
- [資料庫快取](#database-cache)

<a name="configuration"></a>
## 設定

Laravel 為各種不同的快取系統提供一致的 API。快取設定檔位在 `config/cache.php` 。您可以在此為應用程式指定使用哪一種快取系統，Laravel 支援各種常見的後端快取系統，像是 [Memcached](http://memcached.org) 和 [Redis](http://redis.io) 。

快取設定檔也包含多個其他選項，在檔案裡都有說明，所以請務必先閱讀過。Laravel 預設使用 `檔案` 快取系統，該系統會儲存序列化、快取物件在檔案系統中。在大型應用程式上，建議使用儲存在記憶體內的快取系統，像是 Memcached 或 APC。你甚至可以以同一個快取系統設定多個快取設定。

在 Laravel 中使用 Redis 快取系統前， 必須先使用 Composer 安裝 `predis/predis` 套件 (~1.0) 。

<a name="cache-usage"></a>
## 快取用法

#### 儲存項目到快取中

	Cache::put('key', 'value', $minutes);

#### 使用 Carbon 物件設定快取過期時間

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### 若是項目不存在，則將其存入快取中

	Cache::add('key', 'value', $minutes);

當項目確實被加入快取時，使用 `add` 方法將會回傳 `true` 否則會回傳 `false` 。

#### 項目確實被 檢查快取是否存在

	if (Cache::has('key'))
	{
		//
	}

#### 從快取中取得項目

	$value = Cache::get('key');

#### 取得項目或是回傳預設值

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

#### 永久儲存項目到快取中

	Cache::forever('key', 'value');

有時候您會希望從快取中取得項目，而當此項目不存在時會儲存一筆預設值，您可以使用 `Cache::remember` 方法：

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

您也可以結合 `remember` 和  `forever` 方法：

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

請注意所有儲存在快取中的項目皆會被序列化，所以您可以任意儲存各種型別的資料。

#### 從快取拉出項目

如果您需要從快取中取得項目後將它刪除，您可以使用 `pull` 方法：

	$value = Cache::pull('key');

#### 從快取中刪除項目

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## 遞增與遞減

除了 `檔案` 與  `資料庫` 以外的快取系統都支援 `遞增` 和 `遞減` 操作：

#### 遞增值

	Cache::increment('key');

	Cache::increment('key', $amount);

#### 遞減值

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## 快取標籤

> **注意：** `檔案` 或  `資料庫` 這類快取系統均不支援快取標籤。此外，使用帶有「forever」的快取標籤時，挑選 `memcached` 這類快取系統將獲得最好的效能，它會自動清除過期的紀錄。

#### 存取快取標籤

Cache tags allow you to tag related items in the cache, and then flush all caches tagged with a given name. To access a tagged cache, use the `tags` method.

You may store a tagged cache by passing in an ordered list of tag names as arguments, or as an ordered array of tag names:

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(array('people', 'artists'))->put('Anne', $anne, $minutes);

You may use any cache storage method in combination with tags, including `remember`, `forever`, and `rememberForever`. You may also access cached items from the tagged cache, as well as use the other cache methods such as `increment` and `decrement`.

#### Accessing Items In A Tagged Cache

To access a tagged cache, pass the same ordered list of tags used to save it.

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(array('people', 'authors'))->get('John');

You may flush all items tagged with a name or list of names. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both "Anne" and "John" would be removed from the cache:

	Cache::tags('people', 'authors')->flush();

In contrast, this statement would remove only caches tagged with `authors`, so "John" would be removed, but not "Anne".

	Cache::tags('authors')->flush();

<a name="database-cache"></a>
## Database Cache

When using the `database` cache driver, you will need to setup a table to contain the cache items. You'll find an example `Schema` declaration for the table below:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
