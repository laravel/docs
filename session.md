# Oturum

- [Yapılandırma](#yapilandirma)
- [Oturum Kullanımı](#oturum-kullanimi)
- [Flaş Verisi](#flas-verisi)
- [Veritabanı Oturumları](#veritabani-oturumlari)

<a name="yapilandirma"></a>
## Yapılandırma

HTTP odaklı uygulamalar durum bilgisi taşımadıkları için, oturumlar istekler arasında kullanıcı hakkında bilgi saklamak için bir yol sağlar. Laravel temiz, tek bir API aracılığıyla kullanılabilen çeşitli oturum back-endleri ile birlikte gelir. İçerisinde [Memcached](http://memcached.org), [Redis](http://redis.io) ve veritabanları gibi popüler back-end desteği yer almaktadır.

Oturum yapılandırma ayarları `app/config/session.php` dosyasında bulunmaktadır. Bu belgede size sunulan iyi belgelenmiş seçenekleri gözden geçirmeyi unutmayın. Ön tanımlı olarak, Laravel `native` oturum sürücüsünü kullanmak üzere yapılandırılmıştır ve bu yapılandırma uygulamaların çoğunda iyi çalışacaktır.

<a name="oturum-kullanimi"></a>
## Oturum Kullanımı

**Oturumda Bir Öğe Saklamak**

	Session::put('anahtar', 'deger');

**Oturumdaki Bir Öğeyi Öğrenmek**

	$deger = Session::get('anahtar');

**Bir Öğe Almak Veya Varsayılan Bir Değer Döndürmek**

	$deger = Session::get('anahtar', 'default');

	$deger = Session::get('anahtar', function() { return 'default'; });

**Oturumda Bir Öğenin Olup Olmadığını Tespit Etmek**

	if (Session::has('uyeler'))
	{
		//
	}

**Oturumdan Bir Öğeyi Çıkartmak**

	Session::forget('anahtar');

**Oturumdaki Tüm Öğeleri Çıkartmak**

	Session::flush();

**Tekrar Oturum ID Üretmek**

	Session::regenerate();

<a name="flas-verisi"></a>
## Flaş Verisi

Bazen oturumda sadece sonraki istek için öğeler saklamak isteyebilirsiniz. Bunu `Session::flash` metodunu kullanarak gerçekleştirebilirsiniz:

	Session::flash('anahtar', 'deger');

**Mevcut Flaş Verinin Bir Başka İstek İçin Yeniden Flaşlanması**

	Session::reflash();

**Flaş Verinin Sadece Bir Alt Kümesinin Yeniden Flaşlanması**

	Session::keep(array('uyeadi', 'email'));

<a name="veritabani-oturumlari"></a>
## Veritabanı Oturumları

`database` oturum sürücüsü kullanıyorken, oturum öğelerini taşıyan bir tablo kurulumu gerekecek. Aşağıda, bu tablo için örnek bir `Şema` deklarasyonu gösterilmektedir:

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('fayda');
		$table->integer('son_etkinlik');
	});

Tabii ki, bu migrasyonu üretmek için `session:table` Artisan komutunu kullanabilirsiniz!

	php artisan session:table

	composer dump-autoload

	php artisan migrate
