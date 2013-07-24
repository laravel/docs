# Önbellekleme (Cache)

- [Yapılandırma](#yapilandirma)
- [Önbellekleme Kullanımı](#onbellekleme-kullanimi)
- [Arttırma & Azaltma](#arttirma-ve-azaltma)
- [Önbellek Bölümleri](#onbellek-bolumleri)
- [Veritabanı Önbelleği](#veritabani-onbellegi)

<a name="yapilandirma"></a>
## Yapılandırma

Laravel, çeşitli önbellekleme sistemleri için tümleşik bir API sağlar. Önbellekleme yapılandırma ayarları `app/config/cache.php` dosyasında bulunmaktadır. Bu dosyada uygulamanızda varsayılan olarak hangi önbellekleme sürücüsünü kullanmak istediğinizi belirtebilirsiniz. Laravel, [Memcached](http://memcached.org) ve [Redis](http://redis.io) gibi popüler önbellekleme sürücülerini barındırır.

Önbellekleme yapılandırma dosyası ayrıca dosyanın içinde açıklanmış çeşitli seçenekleri de içerir, bu yüzden o seçenekleri de okuduğunuzdan emin olun. Varsayılan olarak, Laravel, sıralanarak önbelleklenmiş öğeleri dosya sisteminde depolayan `file` (dosya) önbellekleme sürücüsünü kullanmak üzere ayarlanmıştır. Daha büyük uygulamalar için, Memcached ve APC gibi bir önbellekleme uygulaması kullanmanız önerilir.

<a name="onbellekleme-kullanimi"></a>
## Önbellekleme Kullanımı

**Bir Öğeyi Önbelleğe Koymak**

	Cache::put('key', 'value', $minutes);

**Eğer Öğe Önbellekte Yoksa, Öğeyi Önbelleğe Koymak**

	Cache::add('key', 'value', $minutes);

**Öğenin Önbellekte Var Olup Olmadığını Kontrol Etmek**

	if (Cache::has('key'))
	{
		//
	}

**Önbellekten Bir Öğeyi Almak**

	$value = Cache::get('key');

**Bir Önbellek Değeri Almak Veya Varsayılan Bir Değer Döndürmek**

	$value = Cache::get('key', 'varsayılanDeğer');

	$value = Cache::get('key', function() { return 'varsayılanDeğer'; });

**Bir Öğeyi Kalıcı Olarak Önbelleğe Koymak**

	Cache::forever('key', 'value');

Bazen, önbellekten bir öğeyi almak isteyebilir ve ayrıca talep edilen öğe yoksa önbellekte varsayılan bir değer saklayabilirsiniz. Bunu, `Cache::remember` metodunu kullanarak yapabilirsiniz:

	$value = Cache::remember('kullanicilar', $minutes, function()
	{
		return DB::table('kullanicilar')->get();
	});

Ayrıca, `remember` ve `forever` methodlarını birlikte kullanabilirsiniz.

	$value = Cache::rememberForever('kullanicilar', function()
	{
		return DB::table('kullanicilar')->get();
	});

Önbellekte bütün öğelerin sıralanmış şekilde saklandığını unutmayın, yani her türlü veriyi saklayabilirsiniz.

**Önbellekten Bir Öğeyi Silmek**

	Cache::forget('key');

<a name="arttirma-ve-azaltma"></a>
## Arttırma & Azaltma

`file` ve `database` hariç tüm sürücüler `increment` (artma) ve `decrement` (azalma) işlemlerini destekler:

**Bir Değeri Arttırmak**

	Cache::increment('key');

	Cache::increment('key', $miktar);

**Bir Değeri Azaltmak**

	Cache::decrement('key');

	Cache::decrement('key', $miktar);

<a name="onbellek-bolumleri"></a>
## Önbellek Bölümleri

> **Not:** Önbellek bölümleri `dosya` ve `veritabanı` önbellekleme sürücüleri kullanılırken desteklenmemektedir.

Önbellek bölümleri, önbellekteki ilişkili öğeleri gruplamanıza ve tüm bölümü temizlemenize olanak sağlar.
Bölüme erişim için `section` metodu kullanılır:

**Bir Önbellek Bölümününe Erişim**

	Cache::section('insanlar')->put('Mehmet', $mehmet);

	Cache::section('insanlar')->put('Ayşe', $ayse);

Ayrıca bölümlerde önbelleklenmiş öğelere, diğer önbellek metodlarında olduğu gibi `increment` ve `decrement` ile de erişebilirsiniz.

**Önbellek Bölümündeki Öğelere Erişmek**

	$anne = Cache::section('insanlar')->get('Mehmet');

Önbellek bölümünü bu şekilde temizleyebilirsiniz:

	Cache::section('insanlar')->flush();

<a name="veritabani-onbellegi"></a>
## Veritabanı Önbelleği

Veritabanı önbellek sürücüsü kullanırken, önbellek öğelerini içeren bir tablo kurulumu gerekir. Bu tablo için örnek bir şema aşağıda gösterilmiştir:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
