# Yerleşimler (Migrations) ve Filizlendirme (Seeding)

- [Giriş](#introduction)
- [Yerleşimlerin Oluşturulması](#creating-migrations)
- [Yerleşimlerin Çalıştırılması](#running-migrations)
- [Yerleşimlerin Geriye Döndürülmesi](#rolling-back-migrations)
- [Veritabanı Filizlendirmesi](#database-seeding)

<a name="introduction"></a>
## Giriş

Yerleşimler, veritabanınız için bir çeşit sürüm yöneticisidir (Version Control). Beraber çalışan bir ekibe, veritabanı şemasında değişiklikler yapma ve en son şema durumunu güncelleme imkanı sağlar. Yerleşimler, uygulamanızın şemasını kolayca yönetmeniz için, genellikle Şema Kurucusu [Schema Builder](/docs/schema) ile birlikte kullanılır.

<a name="creating-migrations"></a>
## Yerleşimlerin Oluşturulması

Bir yerleşim oluşturmak için, Artisan KSA 'da (Artisan Komut Satırı Arayüzü) `migrate:make` komutunu kullanabilirsiniz:

**Bir Yerleşim Oluşturulması**

	php artisan migrate:make kullanicilar_tablosunu_olustur

Yerleşim `app/database/migrations` dizininize konumlandırılır ve bir 'zaman kayıtı' (timestamp) bulundurur. Zaman Kayıtı, uygulamanıza yerleşimlerinizin sırasını belirleme olanağını sağlar.

Yerleşimi oluştururken bir patika `--path` seçeneği de belirtebilirsiniz. Patika, kurulum kök dizinine ilişkin olmalıdır:

	php artisan migrate:make falancaYerlesim --path=app/migrations

Tablo ismini ve yeni bir tablonun oluşturulacagını da, tablo `--table` ve oluştur `--create` seçeneklerini kullanarak belirtebilirsiniz: 

	php artisan migrate:make kullanicilar_tablosunu_olustur --table=kullanicilar --create

<a name="running-migrations"></a>
## Yerleşimlerin Çalıştırılması

**Bekleyen Yerleşimlerin Hepsinin Birden Çalıştırılması**

	php artisan migrate

**Bir Patikadaki Yerleşimlerin Çalıştırılması**

	php artisan migrate --path=app/falancaDizin/migrations

**Bir Paketin Tüm Bekleyen Yerleşimlerinin Çalıştırılması**

	php artisan migrate --package=vendor/package

> **Not:** Yerleşimleri çalıştırırken, "class not found" (sınıf bulunamadı) hatası veririse, `composer update` (composer güncelle) komutunu çalıştırarak deneyiniz.

<a name="rolling-back-migrations"></a>
## Yerleşimlerin Geriye Döndürülmesi

**Son Yerleşim İşleminin Geriye Döndürülmesi**

	php artisan migrate:rollback

**Tüm Yerleşim İşlemlerinin Geriye Döndürülmesi**

	php artisan migrate:reset

**Tüm Yerleşim İşlemlerinin Geriye Döndürülmesi ve Hepsinin Tekrardan Çalıştırılması**

	php artisan migrate:refresh		//filizlendirmeler dahil edilmeden

	php artisan migrate:refresh --seed	//filizlendirmeler dahil edilerek

<a name="database-seeding"></a>
## Veritabanı Filizlendirmesi

Filizlendirme (seeding), yerleşim ile oluşturulacak veritabanı tablosunda gerekli olacak ilk veri kayıtlarının (seed data) oluşturulması işlemidir(:çevirenin notu). Laravel, veritabanınızın deneme verisi ile filizlendirilmesi için kolaylık sağlayacak olan filizlendirme (seed) sınıflarını bulundurur. Bütün filizlendirme sınıfları `app/database/seeds` dizininde konumlandırılır. Filizlendirme sınıflarına istediğiniz isimleri verebilirsiniz. Fakat isimlendirirken anlaşılacak belli bir düzene (convention) uyulması lehinizedir, örneğin `KullanicilarTablosuFilizlendiricisi`, vb. Başlangıçta, kullanacağınız sınıf olarak `DatabaseSeeder` (Veritabanı Filizlendiricisi) sınıfı belirlenmiştir. Filizlendirme sırasını denetlemenize imkan verecek olan, bu sınıfın 'çagır' `call` yöntemini kullanarak diğer filizlendirme sınıflarınızı çalıştırabilirsiniz. 

**Veritabanı Filizlendirme Sınıfı Örneği**

	class DatabaseSeeder extends Seeder {

		public function run()
		{
			$this->call('KullanicilarTablosuFilizlendiricisi');

			$this->command->info('Kullanıcı tablosu filizlendirildi!');
		}

	}

	class KullanicilarTablosuFilizlendiricisi extends Seeder {

		public function run()
		{
			DB::table('kullanicilar')->delete();

			User::create(array('email' => 'falanca@filanca.com'));
		}

	}

Veritabanınızı filizlendirmek için, Artisan KSA'da `db:seed` (filizlendir) komutunu kullanabilirsiniz:

	php artisan db:seed

Veritabanınızı `migrate:refresh` (yenile) komutunu kullanarak da filizlendirebilirsiniz, bu komut aynı zamanda bütün yerleşimleri geriye döndürüp, hepsini tekrardan çalıştıracaktır:

	php artisan migrate:refresh --seed
