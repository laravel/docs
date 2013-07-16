# Şema Oluşturucusu

- [Giriş](#introduction)
- [Tabloların Oluşturulması ve Yok Edilmesi](#creating-and-dropping-tables)
- [Sütunların Eklenmesi](#adding-columns)
- [Sütün İsimlerinin Değiştirilmesi](#renaming-columns)
- [Sütunların Yok Edilmesi](#dropping-columns)
- [Mevcutluk Yoklanması](#checking-existence)
- [İndeks Eklenmesi](#adding-indexes)
- [Yabancı Key](#foreign-keys)
- [İndekslerin Yok Edilmesi](#dropping-indexes)
- [Depolama Motorları](#storage-engines)

<a name="introduction"></a>
## Giriş

Laravel'in `Schema` sınıfı tablolara müdahale etmekte veritabanı bilinmesine gerek kalmaz bir yol sağlar. Laravel'in desteklediği tüm veritabanlarıyla sağlıklı çalışır ve bu sistemlerin tümünde aynı olan bir API'ye sahiptir.

<a name="creating-and-dropping-tables"></a>
## Tabloların Oluşturulması ve Yok Edilmesi

Yeni bir veritabanı tablosu oluşturmak için `Schema::create` metodu kullanılır:

	Schema::create('uyeler', function($table)
	{
		$table->increments('id');
	});

Bu `create` metoduna geçilen ilk parametre tablonun adıdır ve ikincisi bu yeni tabloyu tanımlamakta kullanılabilecek bir proje (`Blueprint`) nesnesi alacak bir bitirme (`Closure`) fonksiyonudur.

Mevcut bir veritabanı tablosunun adını değiştirmek için `rename` metodu kullanılabilir:

	Schema::rename($eskisinden, $yeniye);

Şema operasyonunun gerçekleştirileceği bağlantıyı belirlemek için `Schema::connection` metodunu kullanınız:

	Schema::connection('falan')->create('uyeler', function($table)
	{
		$table->increments('id'):
	});

Bir tabloyu yok etmek için, `Schema::drop` metodunu kullanabilirsiniz:

	Schema::drop('uyeler');

	Schema::dropIfExists('uyeler');

<a name="adding-columns"></a>
## Sütunların Eklenmesi

Mevcut bir tabloda sütun ekleme için `Schema::table` metodunu kullanıyoruz:

	Schema::table('uyeler', function($table)
	{
		$table->string('email');
	});

Tablo oluşturma zamanında ise tablo oluşturucusunda bulunan çeşitli sütun tiplerini kullanabilirsiniz:

Komut  | Açıklama
------------- | -------------
`$table->increments('id');`  |  Giderek artan ID alanı ekler (esas key).
`$table->string('email');`  |  VARCHAR eşdeğeri sütun
`$table->string('isim', 100);`  |  belli uzunlukta VARCHAR eşdeğeri sütun
`$table->integer('puan');`  |  INTEGER eşdeğeri sütun
`$table->bigInteger('puan');`  |  BIGINT eşdeğeri sütun
`$table->smallInteger('puan');`  |  SMALLINT eşdeğeri sütun
`$table->float('miktar');`  |  FLOAT eşdeğeri sütun
`$table->decimal('miktar', 5, 2);`  |  basamak ve ondalık basamak sayısı belirlenmiş DECIMAL eşdeğeri sütun
`$table->boolean('teyit');`  |  BOOLEAN eşdeğeri sütun
`$table->date('created_at');`  |  DATE eşdeğeri sütun
`$table->dateTime('created_at');`  |  DATETIME eşdeğeri sütun
`$table->time('ikindi');`  |  TIME eşdeğeri sütun
`$table->timestamp('eklenme_vakti');`  |  TIMESTAMP eşdeğeri sütun
`$table->timestamps();`  |  **created\_at** ve **updated\_at** sütunlarını ekler
`$table->softDeletes();`  |  Belirsiz silmeler için **deleted\_at** sütunu ekler
`$table->text('izahat');`  |  TEXT eşdeğeri sütun
`$table->binary('veri');`  |  BLOB eşdeğeri sütun
`$table->enum('tercihler', array('falan', 'filan'));` | ENUM eşdeğeri sütun
`->nullable()`  |  İlgili sütunun NULL değerleri olabilir demektir
`->default($deger)`  |  Bir sütun için ön tanımlı bir değer tanımlar
`->unsigned()`  |  INTEGER'i UNSIGNED olarak ayarlar

Şayet MySQL veritabanı kullanıyorsanız, sütunların sıralamasını belirlemek için `after` metodunu kullanabilirsiniz:

**MySQL Veritabanında After Kullanımı**

	$table->string('isim')->after('email');

<a name="renaming-columns"></a>
## Sütün İsimlerinin Değiştirilmesi

Bir sütun ismini değiştirmek için Şema Oluşturucusunda `renameColumn` metodunu kullanabilirsiniz:

**Bir Sütun İsminin Değiştirilmesi**

	Schema::table('uyeler', function($table)
	{
		$table->renameColumn('eskiden', 'yeniye');
	});

> **Not:** `enum` sütun tipleri için isim değiştirme desteklenmemektedir.

<a name="dropping-columns"></a>
## Sütunların Yok Edilmesi

**Bir Veritabanı Tablosundan Bir Sütunun Yok Edilmesi**

	Schema::table('uyeler', function($table)
	{
		$table->dropColumn('puan');
	});

**Bir Veritabanı Tablosundan Birden Çok Sütunun Yok Edilmesi**

	Schema::table('uyeler', function($table)
	{
		$table->dropColumn('puan', 'avatar', 'ikametgah');
	});

<a name="checking-existence"></a>
## Mevcutluk Yoklanması

`hasTable` ve `hasColumn` metodlarını kullanarak bir tablo ya da sütunun var olup olmadığını kolayca yoklayabilirsiniz:

**Tablonun Var Olduğunun Yoklanması**

	if (Schema::hasTable('uyeler'))
	{
		//
	}

**Sütunların Var Olduğunun Yoklanması**

	if (Schema::hasColumn('uyeler', 'email'))
	{
		//
	}

<a name="adding-indexes"></a>
## İndeks Eklenmesi

Şema oluşturucusu çeşitli indeks tiplerini desteklemektedir. Bunları iki şekilde ekleyebilirsiniz. Birinci yol bir sütun tanımı sırasında tanımlamak, ikinci yol ise ayrıca eklemektir:

**Bir Sütun ve İndeksin Birlikte Oluşturulması**

	$table->string('email')->unique();

Ya da, ayrı satırlarda indeks ekleme yolunu seçebilirsiniz. Aşağıda, kullanılabilecek tüm indeks tiplerinin bir listesi verilmiştir:

Komut  | Açıklama
------------- | -------------
`$table->primary('id');`  |  Bir esas key eklenmesi
`$table->primary(array('ilk', 'son'));`  |  Bileşik keylerin eklenmesi
`$table->unique('email');`  |  Benzersiz bir indeks eklenmesi
`$table->index('il');`  |  Basit bir indeks eklenmesi

<a name="foreign-keys"></a>
## Yabancı Key

Laravel, tablolarınıza yabancı key sınırlaması eklemeniz için de destek verir:

**Bir Tabloya Bir Yabcancı Key Eklenmesi**

	$table->foreign('uye_id')->references('id')->on('uyeler');

Bu örnekte, `uye_id` sütununun `uyeler` tablosundaki `id` sütununu referans aldığını beyan ediyoruz.

Ayrıca, güncelleme ve silme ("on delete" ve "on update") eylemi sınırlamaları için seçenekler de belirleyebilirsiniz:

	$table->foreign('uye_id')
          ->references('id')->on('uyeler')
          ->onDelete('cascade');

Bir yabancı keyi yok etmek için, `dropForeign` metodunu kullanabilirsiniz. Yabancı key için de diğer indeksler için kullanılan isimlendirme geleneği kullanılır:

	$table->dropForeign('makaleler_uye_id_foreign');

> **Note:** When creating a foreign key that references an incrementing integer, remember to always make the foreign key column `unsigned`.

<a name="dropping-indexes"></a>
## İndekslerin Yok Edilmesi

Bir indeksi yok etmek için indeksin adını belirtmelisiniz. Laravel, ön tanımlı olarak indekslere makul bir isim tahsis eder. Tablo adını, indekslenen alan adlarını ve indeks tipini art arda ekler. İşte bazı örnekler:

Komut  | Açıklama
------------- | -------------
`$table->dropPrimary('uyeler_id_primary');`  |  "uyeler" tablosundan primer key'in yok edilmesi
`$table->dropUnique('uyeler_email_unique');`  |  "uyeler" tablosundan benzersiz bir indeksin yok edilmesi
`$table->dropIndex('geo_il_index');`  |  "geo" tablosundan basit bir indeksin yok edilmesi

<a name="storage-engines"></a>
## Depolama Motorları

Bir tablo için depolama motoru ayarlamak için, şema oluşturucusunda `engine` özelliğini ayarlayınız:

    Schema::create('uyeler', function($table)
    {
        $table->engine = 'InnoDB';

        $table->string('email');
    });
