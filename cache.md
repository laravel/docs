# Kaşe (Cache)

- [Ayarlamalar](#ayarlamalar)
- [Kaşe Kullanımı](#kase-kullanimi)
- [Arttırma & Azaltma](#arttirma-ve-azaltma)
- [Kaşe Bölümleri](#kase-bolumleri)
- [Veritabanı Kaşesi](#veritabani-kasesi)

<a name="ayarlamalar"></a>
## Ayarlamalar

Laravel, çeşitli kaşeleme sistemleri için tümleşik bir API sağlar. Kaşe konfigürasyonu `app/config/cache.php`'de bulunmaktadır. Bu dosyada uygulamanızda varsayılan olarak hangi kaşe sürücüsünü kullanmak istediğinizi belirtebilirsiniz. Laravel, [Memcached](http://memcached.org) ve [Redis](http://redis.io) gibi popüler kaşeleme paketlerini barındırır.

Kaşe konfigürasyon dosyası ayrıca dosyanın içinde açıklanmış çeşitli seçenekleri de içerir, bu yüzden o seçenekleri de okuduğunuzdan emin olun. Varsayılan olarak, Laravel, sıralanarak kaşelenmiş nesneleri dosya sisteminde depolayan `file` (dosya) kaşe sürücüsünü kullanmak üzere konfigüre edilmiştir. Daha büyük uygulamalar için, Memcached ve APC gibi bir kaşe kullanmanız önerilir.

<a name="kase-kullanimi"></a>
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

Kaşede bütün nesnelerin sıralanmış şekilde saklandığını unutmayın, yani her türlü veriyi saklayabilirsiniz.

**Kaşeden Bir Nesneyi Kaldırmak**

	Cache::forget('key');

<a name="arttirma-ve-azaltma"></a>
## Arttırma & Azaltma

`file` ve `database` hariç tüm sürücüler `increment` (artma) ve `decrement` (azalma) işlemlerini destekler:

**Bir Değeri Arttırmak**

	Cache::increment('key');

	Cache::increment('key', $amount);

**Bir Değeri Azaltmak**

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="kase-bolumleri"></a>
## Kaşe Bölümleri

> **Not:** Kaşe bölümleri `dosya` ve `veritabanı` kaşe sürücüleri kullanılırken desteklenmemektedir.

Kaşe bölümleri, kaşedeki ilişkili nesneleri gruplamanıza ve tüm bölümü temizlemenize olanak sağlar.
Bölüme erişim için `section` metodu kullanılır:

**Bir kaşe Bölümününe Erişim**

	Cache::section('people')->put('John', $john);

	Cache::section('people')->put('Anne', $anne);

Ayrıca bölümlerde kaşelenmiş nesnelere, diğer kaşe metodlarında olduğu gibi `increment` ve `decrement` ile de erişebilirsiniz.

**Kaşe Bölümündeki Nesnelere Erişmek**

	$anne = Cache::section('people')->get('Anne');

Kaşe bölümünü bu şekilde temizleyebilirsiniz:

	Cache::section('people')->flush();

<a name="veritabani-kasesi"></a>
## Veritabanı Kaşesi

Veritabanı kaşesi kullanabilmek için, kaşe nesnelerini içerecek `database` kaşesi kurulmalıdır. Aşağıda, gerekli tablonun tanımlanması için kullanabileceğiniz Şema (`Schema`) mevcuttur:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
