# Oturum

- [Yapılandırma](#yapilandirma)
- [Oturum Kullanımı](#oturum-kullanimi)
- [Flaş Verisi](#flas-verisi)
- [Veritabanı Oturumları](#veritabani-oturumlari)

<a name="yapilandirma"></a>
## Yapılandırma

HTTP odaklı uygulamalar izolasyonsuz olduğu için, oturumlar istekler arasında kullanıcı hakkında bilgi saklamak için bir yol sağlar. Laravel ships with a variety of session back-ends available for use through a clean, unified API. Support for popular back-ends such as [Memcached](http://memcached.org), [Redis](http://redis.io), and databases is included out of the box.

Oturum yapılandırma ayarları `app/config/session.php` dosyasında bulunmaktadır. Yapılandırma dosyası ayrıca dosyanın içinde açıklanmış çeşitli seçenekleri de içerir, bu yüzden o seçenekleri de okuduğunuzdan emin olun. Varsayılan olarak, Laravel `native` oturum sürücünü kullanmak üzere yapılandırılmıştır, bu yapılandırma uygulamaların çoğunda çalışacaktır.

<a name="oturum-kullanimi"></a>
## Oturum Kullanımı

**Bir Nesneyi Oturuma Koymak**

	Session::put('key', 'value');

**Oturumdan Bir Nesneyi Almak**

	$value = Session::get('key');

**Bir Oturum Değeri Almak Veya Varsayılan Bir Değer Döndürmek**

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

**Nesnenin Oturumda Var Olup Olmadığını Kontrol Etmek**

	if (Session::has('users'))
	{
		//
	}

**Oturumdan Bir Nesneyi Silmek**

	Session::forget('key');

**Oturumdanki Tüm Nesneleri Silmek**

	Session::flush();

**Oturum ID Numarasını Tekrar Oluşturmak**

	Session::regenerate();

<a name="flas-verisi"></a>
## Flaş Verisi

Sometimes you may wish to store items in the session only for the next request. You may do so using the `Session::flash` method:

	Session::flash('key', 'value');

**Reflashing The Current Flash Data For Another Request**

	Session::reflash();

**Reflashing Only A Subset Of Flash Data**

	Session::keep(array('username', 'email'));

<a name="veritabani-oturumlari"></a>
## Veritabanı Oturumları

When using the `database` session driver, you will need to setup a table to contain the session items. Below is an example `Schema` declaration for the table:

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

Of course, you may use the `session:table` Artisan command to generate this migration for you!

	php artisan session:table

	composer dump-autoload

	php artisan migrate