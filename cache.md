# Önbellekleme (Cache)

- [Yapılandırma](#yapilandirma)
- [Önbellekleme Kullanımı](#onbellekleme-kullanimi)
- [Arttırma & Azaltma](#arttirma-ve-azaltma)
- [Önbellek Bölümleri](#onbellek-bolumleri)
- [Veritabanı Önbelleği](#veritabani-onbellegi)

<a name="yapilandirma"></a>
## Yapılandırma

Laravel, çeşitli önbellekleme sistemleri için tümleşik bir API sağlar. Önbellekleme yapılandırma ayarları `app/config/cache.php` dosyasında bulunmaktadır. Bu dosyada uygulamanızda varsayılan olarak hangi önbellekleme sürücüsünü kullanmak istediğinizi belirtebilirsiniz. Laravel, [Memcached](http://memcached.org) ve [Redis](http://redis.io) gibi popüler önbellekleme sürücülerini barındırır.

Önbellekleme yapılandırma dosyası ayrıca dosyanın içinde açıklanmış çeşitli seçenekleri de içerir, bu yüzden o seçenekleri de okuduğunuzdan emin olun. Varsayılan olarak, Laravel, sıralanarak önbelleklenmiş nesneleri dosya sisteminde depolayan `file` (dosya) önbellekleme sürücüsünü kullanmak üzere ayarlanmıştır. Daha büyük uygulamalar için, Memcached ve APC gibi bir önbellekleme uygulaması kullanmanız önerilir.

<a name="onbellekleme-kullanimi"></a>
## Önbellekleme Kullanımı

**Bir Nesneyi Önbelleğe Koymak**

	Cache::put('key', 'value', $minutes);

**Eğer Nesne Önbellekte Yoksa, Nesneyi Önbelleğe Koymak**

	Cache::add('key', 'value', $minutes);

**Nesnenin Önbellekte Var Olup Olmadığını Kontrol Etmek**

	if (Cache::has('key'))
	{
		//
	}

**Önbellekten Bir Nesneyi Almak**

	$value = Cache::get('key');

**Bir Önbellek Değeri Almak Veya Varsayılan Bir Değer Döndürmek**

	$value = Cache::get('key', 'varsayılanDeğer');

	$value = Cache::get('key', function() { return 'varsayılanDeğer'; });

**Bir Nesneyi Kalıcı Olarak Önbelleğe Koymak**

	Cache::forever('key', 'value');

Bazen, önbellekten bir nesneyi almak isteyebilir ve ayrıca talep edilen nesne yoksa önbellekte varsayılan bir değer saklayabilirsiniz. Bunu, `Cache::remember` metodunu kullanarak yapabilirsiniz:

	$value = Cache::remember('kullanicilar', $minutes, function()
	{
		return DB::table('kullanicilar')->get();
	});

Ayrıca, `remember` ve `forever` methodlarını birlikte kullanabilirsiniz.

	$value = Cache::rememberForever('kullanicilar', function()
	{
		return DB::table('kullanicilar')->get();
	});

Önbellekte bütün nesnelerin sıralanmış şekilde saklandığını unutmayın, yani her türlü veriyi saklayabilirsiniz.

**Önbellekten Bir Nesneyi Silmek**

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

Önbellek bölümleri, önbellekteki ilişkili nesneleri gruplamanıza ve tüm bölümü temizlemenize olanak sağlar.
Bölüme erişim için `section` metodu kullanılır:

**Bir Önbellek Bölümününe Erişim**

	Cache::section('insanlar')->put('Mehmet', $mehmet);

	Cache::section('insanlar')->put('Ayşe', $ayse);

Ayrıca bölümlerde önbelleklenmiş nesnelere, diğer önbellek metodlarında olduğu gibi `increment` ve `decrement` ile de erişebilirsiniz.

**Önbellek Bölümündeki Nesnelere Erişmek**

	$anne = Cache::section('insanlar')->get('Mehmet');

Önbellek bölümünü bu şekilde temizleyebilirsiniz:

	Cache::section('insanlar')->flush();

<a name="veritabani-onbellegi"></a>
## Veritabanı Önbelleği

Veritabanı önbelleği kullanabilmek için, önbellek nesnelerini içerecek `database` önbelleği kurulmalıdır. Aşağıda, gerekli tablonun tanımlanması için kullanabileceğiniz Şema (`Schema`) mevcuttur:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
