# Temel Veritabanı Kullanımı

- [Yapılandırma](#yapilandirma)
- [Sorugları Çalıştırma](#sorgulari-calistirma)
- [Database Transactions](#veritabani-islemleri)
- [Bağlantılara Erişme](#baglantilara-erisme)
- [Sorgu Dökümü](#sorgu-dukumu)

<a name="yapilandirma"></a>
## Yapılandırma

Laravel, veritabanı bağlantısını ve sorguları çalıştırmayı fazlasıyla kolay kılar. Veritabanı yapılandırma ayarlarını `app/config/database.php` dosyasında bulabilirsiniz. Bı dosyada hem tüm veritabanı bağlantılarını tanımlayabilir, hem de hangi bağlantının varsayılan olarak kullanılacağını seçebilirsiniz. Örnek olarak desteklenen tüm veritabanı sistemleri bu dosya altında sunulmuştur.

Laravel tarafından desteklenen veritabanı sistemleri: MySQL, Postgres, SQLite, and SQL Server.

<a name="sorgulari-calistirma"></a>
## Sorguları Çalıştırma

Veritabanı bağlantılarını bir kere yapılandırdıktan sonra `DB` sınıfını kullanarak sorgularını çalıştırabilirsiniz.

**Kayıt Çekme (Select)**

	$sonuclar = DB::select('select * from uyeler where id = ?', array(1));

`select` metodu sonuçları her zaman `dizi` () tipinde döndürür.

**Yeni Kayıt Ekleme (Insert)**

	DB::insert('insert into uyeler (id, isim) values (?, ?)', array(1, 'Emre'));

**Kayıt Güncelleme (Update)**

	DB::update('update uyeler set oy = 100 where isim = ?', array('Hakan'));

**Kayıt Silme (Delete)**

	DB::delete('delete from uyeler');

> **Not:** `update` ve `delete` sorguları, bu işlemlerden etkilenen satır sayısını döndürür.

**Genel Bir Sorgu Çalıştırma**

	DB::statement('drop table uyeler');

`DB::listen` metodunu kullanarak sorgu olaylarını dinleyebilirsiniz:

**Sorgu Olaylarını Dinleme**

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="veritabani-islemleri"></a>
## Veritabanı İşlemleri

Bir veritabanı işleminde, birden fazla işlemi birden gerçekleştirmek için, 'transaction' metodunu kullanabilirsiniz:

	DB::transaction(function()
	{
		DB::table('uyeler')->update(array('votes' => 1));

		DB::table('posts')->delete();
	});

<a name="baglantilara-erisme"></a>
## Bağlantılara Erişme

Birden fazla bağlantı kullandığınız durumlarda, bu bağlantılara `DB::connection` metodu aracılığı ile ulabilirsiniz.

	$uyeler = DB::connection('foo')->select(...);

Ayrıca temel PDO örneğinede ulabilirsiniz:

	$pdo = DB::connection()->getPdo();

Bazen veritabanına tekrar bağlanmaya ihtiyacınız olabilir.

	DB::reconnect('foo');

<a name="sorgu-dukumu"></a>
## Sorgu Dökümü

Varsayılan olarak, Laravel çalıştırılan tüm surguların kayıdını hafızada tutar. Ama bazı durumlarda, -çok sayıda satır ekleme gibi- belleğin aşırı kullanılmasına yol açabilir. Sorgu dökümünü kapatmak için `disableQueryLog` metodunu kullanabilirsiniz.

	DB::connection()->disableQueryLog();
