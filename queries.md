# Sorgu Oluşturucusu

- [Giriş](#introduction)
- [Seçmeler](#selects)
- [Joinler](#joins)
- [İleri Where Cümleleri](#advanced-wheres)
- [Kümeleme (Aggregate) İşlemleri](#aggregates)
- [Ham İfadeler](#raw-expressions)
- [Eklemeler](#inserts)
- [Güncellemeler](#updates)
- [Silmeler](#deletes)
- [Birleştirmeler](#unions)
- [Sorguların Bellekte Saklanması](#caching-queries)

<a name="introduction"></a>
## Giriş

Veritabanı sorgu oluşturucusu veritabanı sorguları oluşturulması ve çalıştırılması için kullanışlı ve akıcı bir arayüz sağlar. Uygulamanızdaki pek çok veritabanı işlemini bununla gerçekleştirebilirsiniz ve desteklenen tüm veritabanı sistemlerinde çalışmaktadır.

> **Not:** Laravel sorgu oluşturucusu, uygulamanızı SQL enjeksiyon saldırılarına karşı korumak için PDO parametre bağlayıcı kullanmaktadır. Bağlayıcı olarak geçirilen yazıların temizlenmesine gerek yoktur.

<a name="selects"></a>
## Seçmeler

**Bir Tablonun Bütün Satırlarının Alınması**

	$uyeler = DB::table('uyeler')->get();

	foreach (uyeler as $uye)
	{
		var_dump($uye->isim);
	}

**Bir Tablonun Tek Bir Satırının Alınması**

	$uye = DB::table('uyeler')->where('isim', 'Can')->first();

	var_dump($uye->isim);

**Bir Satırın Tek Bir Sütununun Alınması**

	$isim = DB::table('uyeler')->where('isim', 'Can')->pluck('isim');

**Sütun Değerlerinden Oluşan Bir Liste Elde Edilmesi**

	$roller = DB::table('roller')->lists('unvan');

Bu metod rol ünvanlarından oluşan bir dizi döndürecektir. Döndürülen dizi için özel bir anahtar sütun da belirleyebilirsiniz:

	$roller = DB::table('roller')->lists('unvan', 'isim');

**Bir Select Bendinin Belirlenmesi**

	$uyeler = DB::table('uyeler')->select('isim', 'email')->get();

	$uyeler = DB::table('uyeler')->distinct()->get();

	$uyeler = DB::table('uyeler')->select('isim as uye_adi')->get();

**Mevcut Bir Sorguya Bir Select Bendinin Eklenmesi**

	$sorgu = DB::table('uyeler')->select('isim');

	$uyeler = $query->addSelect('yas')->get();

**Where Kullanımı**

	$uyeler = DB::table('uyeler')->where('puan', '>', 100)->get();

**Or Cümleleri**

	$uyeler = DB::table('uyeler')
	                    ->where('puan', '>', 100)
	                    ->orWhere('isim', 'Can')
	                    ->get();

**Where Between Kullanımı**

	$uyeler = DB::table('uyeler')
	                    ->whereBetween('puan', array(1, 100))->get();

**Bir Dizi Aracılığıyla Where In Kullanımı**

	$uyeler = DB::table('uyeler')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$uyeler = DB::table('uyeler')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

**Değer Girilmemiş Kayıtları Bulmak için Where Null Kullanımı**

	$uyeler = DB::table('uyeler')
	                    ->whereNull('guncelleme_vakti')->get();

**Order By, Group By ve Having**

	$uyeler = DB::table('uyeler')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

**Offset ve Limit**

	$uyeler = DB::table('uyeler')->skip(10)->take(5)->get();

<a name="joins"></a>
## Joinler

Sorgu oluşturucusu join cümleleri yazmak için de kullanılabilir. Şu örneklere bir bakın:

**Temel Join Cümleleri**

	DB::table('uyeler')
	            ->join('kisiler', 'uyeler.id', '=', 'kisiler.uye_id')
	            ->join('siparisler', 'uyeler.id', '=', 'siparisler.uye_id')
	            ->select('uyeler.id', 'kisiler.telefon', 'siparisler.fiyat');

Daha ileri join cümleleri de tanımlayabilirsiniz:

	DB::table('uyeler')
	        ->join('kisiler', function($join)
	        {
	        	$join->on('uyeler.id', '=', 'kisiler.uye_id')->orOn(...);
	        })
	        ->get();

<a name="advanced-wheres"></a>
## İleri Where Cümleleri

Kimi zaman "where exists" veya içi içe parametre gruplaması gibi daha ileri where cümleleri oluşturmanız gerekebilir. Laravel sorgu oluşturucusu bunu da halledecektir:

**Parametre Gruplaması**

	DB::table('uyeler')
	            ->where('isim', '=', 'Can')
	            ->orWhere(function($query)
	            {
	            	$query->where('puan', '>', 100)
	            	      ->where('unvan', '<>', 'Müdür');
	            })
	            ->get();

Yukardaki sorgu aşağıdaki SQL cümlesini oluşturacaktır:

	select * from uyeler where isim = 'Can' or (puan > 100 and unvan <> 'Müdür')

**Exists Cümleleri**

	DB::table('uyeler')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('siparisler')
	            	      ->whereRaw('siparisler.uye_id = uyeler.id');
	            })
	            ->get();

Yukardaki sorgu aşağıdaki SQL cümlesini oluşturacaktır:

	select * from uyeler
	where exists (
		select 1 from siparisler where siparisler.uye_id = uyeler.id
	)

<a name="aggregates"></a>
## Kümeleme (Aggregate) İşlemleri

Sorgu oluşturucusu; `count`, `max`, `min`, `avg` ve `sum` gibi çeşitli kümeleme metodları da sağlamaktadır.

**Aggregate Metodlarının Kullanımı**

	$uyeler = DB::table('uyeler')->count();

	$fiyat = DB::table('siparisler')->max('fiyat');

	$fiyat = DB::table('siparisler')->min('fiyat');

	$fiyat = DB::table('siparisler')->avg('fiyat');

	$toplam = DB::table('uyeler')->sum('puan');

<a name="raw-expressions"></a>
## Ham İfadeler

Bazen bir sorguda ham ifade kullanma ihtiyacı duyabilirsiniz. Bu ifadeler sorguya doğrudan yazı olarak enjekte edileceğinden, bir SQL enjeksiyon noktası oluşturmamaya özen gösteriniz. Ham ifade oluşturmak için `DB::raw` metodunu kullanabilirsiniz:

**Ham İfade Kullanımı**

	$users = DB::table('uyeler')
	                     ->select(DB::raw('count(*) as uye_adedi, durum'))
	                     ->where('durum', '<>', 1)
	                     ->groupBy('durum')
	                     ->get();

**Bir Sütun Değerinin Artırılması veya Azaltılması**

	DB::table('uyeler')->increment('puan');

	DB::table('uyeler')->decrement('puan');

<a name="inserts"></a>
## Eklemeler

**Bir Tabloya Kayıt Eklenmesi**

	DB::table('uyeler')->insert(
		array('email' => 'can@numune.com', 'puan' => 0)
	);

Şayet tabloda otomatik artan bir id alanı varsa, bir kayıt eklemek ve oluşan otomatik id'i öğrenmek için `insertGetId` metodu kullanılabilir:

**Otomatik Artan Bir Id Alanı Olan Tabloya Kayıt Eklenmesi**

	$id = DB::table('uyeler')->insertGetId(
		array('email' => 'can@numune.com', 'puan' => 0)
	);

> **Not:** PostgreSQL ile kullanıldığı zaman insertGetId metodu, otomatik artan alanın adının da "id" olmasını bekler.

**Bir Tabloya Birden Çok Kayıt Eklenmesi**

	DB::table('uyeler')->insert(array(
		array('email' => 'sinan@numune.com', 'puan' => 0),
		array('email' => 'ozan@numune.com', 'puan' => 0),
	));

<a name="updates"></a>
## Güncellemeler

**Bir Tablodaki Kayıtların Güncellenmesi**

	DB::table('uyeler')
	            ->where('id', 1)
	            ->update(array('puan' => 1));

<a name="deletes"></a>
## Silmeler

**Bir Tablodaki Kayıtların Silinmesi**

	DB::table('uyeler')->where('puan', '<', 100)->delete();

**Bir Tablodaki Tüm Kayıtların Silinmesi**

	DB::table('uyeler')->delete();

**Bir Tablonun Budanması**

	DB::table('uyeler')->truncate();

<a name="unions"></a>
## Birleştirmeler

Sorgu oluşturucusu, iki ayrı sorgunun tek bir "birlik" haline getirilmesi için de hızlı bir yol sağlamaktadır:

**Bir Birleştirme Sorgusu Yapılması**

	$ilksorgu = DB::table('uyeler')->whereNull('ismi');

	$users = DB::table('uyeler')->whereNull('soy_ismi')->union($ilksorgu)->get();

Ayrıca `unionAll` metodu da mevcut olup, aynı `union` gibi kullanılır.

<a name="caching-queries"></a>
## Sorguların Bellekte Saklanması

Bir sorgunun sonuçları `remember` metodu kullanılarak bellekte saklanabilir:

**Bir Sorgu Sonucunun Bellekte Saklanması**

	$uyeler = DB::table('uyeler')->remember(10)->get();

Bu örnekte, sorgunun sonuçları on dakika süreyle bellekte saklanacaktır. Sonuçlar bellekte tutulduğu süre boyunca bu sorgu artık veritabanında çalıştırılmayacak, onun yerine sonuçlar uygulamanız için belirlediğiniz ön tanımlı bellekleme sürücüsü tarafından yüklenecektir.
