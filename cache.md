# Cache

- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Sections](#cache-sections)
- [Database Cache](#database-cache)

<a name="configuration"></a>
## Configuration

Laravel, çeşitli kaşeleme sistemleri için tümleşik bir API sağlar. Kaşe konfigürasyonu `app/config/cache.php`'de bulunmaktadır. Bu dosyada uygulamanızda varsayılan olarak hangi kaşe sürücüsünü kullanmak istediğinizi belirtebilirsiniz. Laravel, [Memcached](http://memcached.org) ve [Redis](http://redis.io) gibi popüler kaşeleme paketlerini barındırır.

Kaşe konfigürasyon dosyası ayrıca dosyanın içinde açıklanmış çeşitli seçenekleri de içerir, bu yüzden o seçenekleri de okuduğunuzdan emin olun. Varsayılan olarak, Laravel, sıralanarak kaşelenmiş nesneleri dosya sisteminde depolayan `file` (dosya) kaşe sürücüsünü kullanmak üzere konfigüre edilmiştir. Daha büyük uygulamalar için, Memcached ve APC gibi bir kaşe kullanmanız önerilir.

<a name="cache-usage"></a>
## Kaşe Kullanımı

**Bir Nesneyi Kaşeye Koymak**

	Cache::put('key', 'value', $minutes);

**Bir Nesneyi Yoksa Kaşeye Koymak**

	Cache::add('key', 'value', $minutes);

**Nesnenin Kaşede Var Olup Olmadığını Kontrol Etmek**

	if (Cache::has('key'))
	{
		//
	}

**Kaşeden Bir Nesneyi Almak**

	$value = Cache::get('key');

**Bir Nesneyi Almak Veya Varsayılan Bir Değer Dönmek**

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

**Bir Nesneyi Kalıcı Olarak Kaşeye Koymak**

	Cache::forever('key', 'value');

Bazen, kaşeden bir nesneyi almak isteyebilir ve ayrıca talep edilen nesne yoksa kaşede varsayılan bir değer saklayabilirsiniz. Bunu, `Cache::remember` metodunu kullanarak yapabilirsiniz:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

Ayrıca, `remember` ve `forever` metotlarını birlikte kullanabilirsiniz.

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

Kaşede bütün nesnelerin sıralanmış şekilde saklandığını unutmayın, yani ger türlü veriyi saklayabilirsiniz.

*Kaşeden Bir Nesneyi Kaldırmak**

	Cache::forget('key');

<a name="increments-and-decrements"></a>
## Arttırma & Azaltma

`file` ve `database` hariç tüm sürücüler `increment` (artma) ve `decrement` (azalma) işlemlerini destekler:

**Bir Değeri Arttırmak**

	Cache::increment('key');

	Cache::increment('key', $amount);

**Bir Değeri Azaltmak**

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
