# 快取

- [設定](#configuration)
- [快取用法](#cache-usage)
- [遞增與遞減](#increments-and-decrements)
- [快取標籤](#cache-tags)
- [資料庫快取](#database-cache)

<a name="configuration"></a>
## 設定

Laravel 為各種不同的快取系統提供一致的 API。 快取設定檔位在 `app/config/cache.php`。 您可以在此為應用程式指定使用哪一種快取系統，Laravel 支援各種常見的後端快取系統，像是 [Memcached](http://memcached.org) 和 [Redis](http://redis.io)。

快取設定檔也包含多個其他選項，在檔案裡都有說明，所以請務必先閱讀過。Laravel 預設使用 `檔案` 快取系統，該系統會儲存序列化、快取物件在檔案系統中。在大型應用程式上，建議使用儲存在記憶體內的快取系統，像是 Memcached 或 APC。

<a name="cache-usage"></a>
## 快取用法

#### 儲存項目到快取中

	Cache::put('key', 'value', $minutes);

#### 使用 Carbon 物件設定快取過期時間

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### 若是項目不存在，則將其存入快取中

	Cache::add('key', 'value', $minutes);

當項目確實被**加入**快取時，使用 `add` 方法將會回傳 `true` 否則會回傳 `false`。

#### 項目確實被  檢查快取是否存在

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

有時候您會希望從快取中取得項目，而當此項目不存在時會儲存一筆預設值，您可以使用 `Cache::remember` 方法:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

您也可以結合 `remember` 和 `forever` 方法:

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

請注意所有儲存在快取中的項目皆會被序列化，所以您可以任意儲存各種型別的資料。

#### 從快取拉出項目

如果您需要從快取中取得項目後將它刪除，您可以使用 `pull` 方法:

	$value = Cache::pull('key');

#### 從快取中刪除項目

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## 遞增與遞減

除了 `檔案` 與 `資料庫` 以外的快取系統都支援 `遞增` 和 `遞減` 操作:

#### 遞增值

	Cache::increment('key');

	Cache::increment('key', $amount);

#### 遞減值

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## 快取標籤

> **注意:** `檔案` 或 `資料庫` 這類快取系統均不支援快取標籤. 此外, 使用帶有 "forever" 的快取標籤時, 挑選 `memcached` 這類快取系統將獲得最好的效能, 它會自動清除過期的紀錄。

#### 存取快取標籤

快取標籤允許您標記快取內的相關項目，然後使用特定名稱刷新所有快取標籤。要存取快取標籤可以使用 `tags` 方法。

您可以儲存快取標籤，藉由將有序列表當作參數傳入，或者作為標籤名稱的有序陣列:

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(array('people', 'artists'))->put('Anne', $anne, $minutes);

您可以結合使用各種快取儲存方法與標籤，包含 `remember`, `forever` 和 `rememberForever`。您也可以從已標記的快取中存取項目 ，以及使用其他快取方法像是 `increment` 和 `decrement`。

#### 從已標記的快取中存取項目

要存取已標記的快取，可傳入相同的有序標籤列表。

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(array('people', 'authors'))->get('John');

您可以刷新所有已標記的項目，使用指定名稱或名稱列表。例如，以下演示將會移除帶有 `people` 或 `authors` 或者兩者皆有的所有快取標籤，所以 "Anne" 和 "John" 皆會從快取中被移除:

	Cache::tags('people', 'authors')->flush();

對照來看，以下演示將只會移除帶有 `authors` 的標籤，所以 "John" 會被移除，但是 "Anne" 不會。

	Cache::tags('authors')->flush();

<a name="database-cache"></a>
## 資料庫快取

當使用 `資料庫` 快取系統時，您必須設定一張資料表來儲存快取項目。資料表的 `Schema` 宣告範例如下:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
