# Eloquent ORM

- [Giriş](#introduction)
- [Temel Kullanım](#basic-usage)
- [Toplu Atama](#mass-assignment)
- [Ekleme, Güncelleme, Silme](#insert-update-delete)
- [Belirsiz Silme](#soft-deleting)
- [Zaman Damgaları](#timestamps)
- [Sorgu Kapsamları](#query-scopes)
- [İlişkiler](#relationships)
- [İlişkilerin Sorgulanması](#querying-relations)
- [Ateşli Yükleme](#eager-loading)
- [İlişkili Modelleri Ekleme](#inserting-related-models)
- [Ebeveyn Zaman Damgalarına Dokunma](#touching-parent-timestamps)
- [Pivot Tablolarla Çalışmak](#working-with-pivot-tables)
- [Koleksiyonlar](#collections)
- [Erişimciler & Değiştiriciler (Accessors & Mutators)](#accessors-and-mutators)
- [Tarih Değiştiricileri](#date-mutators)
- [Model Olayları](#model-events)
- [Model Gözlemcileri](#model-observers)
- [Diziye / JSON'a Çevirme](#converting-to-arrays-or-json)

<a name="introduction"></a>
## Giriş

Laravelle gelen "Eloquent ORM", veritabanınızla çalışırken kullanacağınız güzel ve sade bir ActiveRecord uygulaması sağlamaktadır. Her veritabanı tablosu, bu tabloyla etkilişim için kullanıcak kendine has bir "Model" sahibidir.

Başlamadan önce, `app/config/database.php`'de bir veritabanı bağlantısı yapılandırmış olun.

<a name="basic-usage"></a>
## Temel Kullanım

Başlamadan önce, bir Eloquent modeli oluşturunuz. Modeller tipik olarak `app/models` klasöründe yer alır, fakat siz modellerinizi `composer.json` dosyanıza göre otomatik yükleme yapabileceğiniz başka bir yere de koyabilirsiniz.

**Bir Eloquent Modelinin Tanımlanması**

	class Uye extends Eloquent {}

Dikkat ederseniz Eloquent'e `Uye` modelimiz için hangi tabloyu kullanacağımızı söylemedik. Eğer açıkça başka bir isim belirtilmezse tablo isimi olarak sınıf adının ingilizde çoğulunun küçük harf hali kullanılacaktır. Dolayısıyla bizim örneğimizde Eloquent, `Uye` modelinin  `uyes` tablosundaki kayıtları tutacağını varsayacaktır. Tablo ismini açıkça belirtmek için modelinizde bir `table` özelliği tanımlayınız:

	class Uye extends Eloquent {

		protected $table = 'uyeler';

	}

> **Not:** Eloquent'in başka bir ön kabulü de her tablonun `id` adında bir primer key sütunu olduğudur. Bu kuralı aşmak için de bir `primaryKey` özelliği tanımlamanız gerekecek. Benzer şekilde, modeliniz kullanılacağı zaman kullanılacak veritabanı bağlantısının adını değiştirmek için bir `connection` özelliği tanımlayabilirsiniz.

Bir model tanımladıktan sonra artık tablonuzda kayıt oluşturmaya ve ondan kayıt getirmeye başlayabilirsiniz. Tablolarınıza ön tanımlı olarak `updated_at` ve `created_at` sütunları koymanız gerektiğine dikkat ediniz. Şayet bu sütunların otomatik olarak tutulmasını istemiyorsanız, modelinizdeki `$timestamps` özelliğini `false` olarak ayarlayınız.

**Tüm Modellerin Alınması**

	$uyeler = Uye::all();

**Birincil Alana Göre Bir Kaydın Alınması**

	$uye = Uye::find(1);

	var_dump($uye->isim);

> **Not:** [Sorgu Oluşturucusu](/docs/queries)'nda bulunan tüm metodlar Eloquent modellerini sorgularken de kullanılabilir.

**Birincil Alana Göre Bir Model Alınması ya da Ortaya Bir İstisna Çıkartılması**

Bazı durumlarda bir model bulunamadığında bir istisna çıkartmak, böylece bir `App::error` işleyicisi kullanarak istisnayı yakalayabilmek ve bir 404 sayfası göstermek isteyebilirsiniz.

	$model = Uye::findOrFail(1);

Bu hata işleyicinin kaydını yapmak için `ModelNotFoundException`'i dinlemek lazım.

	use Illuminate\Database\Eloquent\ModelNotFoundException;

	App::error(function(ModelNotFoundException $e)
	{
		return Response::make('Bulunamadı', 404);
	});

**Eloquent Modelleri Kullanarak Sorgu Yapma**

	$uyeler = Uye::where('puan', '>', 100)->take(10)->get();

	foreach ($uyeler as $uye)
	{
		var_dump($uye->isim);
	}

Tabi ki, sorgu oluşturucusunun kümeleme fonksiyonlarını da kullanabilirsiniz.

**Eloquent Küme Metodları**

	$adet = Uye::where('puan', '>', 100)->count();

<a name="mass-assignment"></a>
## Toplu Atama

Yeni bir model oluşturulurken model oluşturucuya niteliklerden oluşan bir dizi geçersiniz. Bu nitelikler bu durumda modele "toplu atama" aracılığıyla atanır. Bu gayet uygun bir yaklaşımdır, fakat bir kullanıcı girdisi bir modele körleme geçirildiği takdirde **ciddi (serious)** bir güvenlik sorunu olabilecektir. Kullanıcı girdisi bir modele körlemesine geçirilirse, bu kullanıcı modelin niteliklerinin **birisini (any)** ve **hepsini (all)** değiştirebilecektir. Bu sebepler yüzünden, tüm Eloquent modelleri ön tanımlı olarak toplu atamaya karşı koyar.

Başlamak için modelinizde `fillable` veya `guarded` özelliğini ayarlayınız.

Bunlardan `fillable` özelliği hangi niteliklerin toplu atanacaklarını belirler. Bu işlem sınıf ya da olgu düzeyinde ayarlanabilir.

**Bir Modelde Fillable Niteliklerin Tanımlanması**

	class Uye extends Eloquent {

		protected $fillable = array('ismi', 'soy_ismi', 'email');

	}

Bu örnekte, sadece belirttiğimiz üç nitelik toplu atanabilecektir.

`fillable`'in tersi `guarded`'dir ve bir "beyaz-liste" yerine bir "kara-liste" olarak iş görür:

**Bir Modelde Guarded Niteliklerin Tanımlanması**

	class Uye extends Eloquent {

		protected $guarded = array('id', 'parola');

	}

Yukardaki örneğe göre `id` ve `parola` nitelikleri toplu atana **mayacaktır**. Diğer tüm nitelikler toplu atanabilecektir. Toplu atamayı niteliklerin **hepsi (all)** için bloke etmeyi de seçebilirsiniz:

**Toplu Atamanın Tüm Nitelikler İçin Engellenmesi**

	protected $guarded = array('*');

<a name="insert-update-delete"></a>
## Ekleme, Güncelleme, Silme

Veritabanında bir modelden yeni bir kayıt oluşturmak için, yeni bir model olgusu oluşturun ve `save` metodunu çağırın.

**Yeni Bir Modelin Kaydedilmesi**

	$uye = new Uye;

	$uye->isim = 'Can';

	$uye->save();

> **Not:** Tipik olarak, Eloquent modellerinizde otomatik artan anahtarlar olacaktır. Ama siz kendi keylerinizi belirlemek isterseniz, modelinizdeeki `incrementing` özelliğini `false` olarak ayarlayın.

Yeni bir modeli tek satırda kaydetmek için `create` metodunu kullanabilirsiniz. Eklenen model olgusu bu metoddan döndürülecektir. Ancak, tüm Elequent modelleri toplu atamaya karşı korunumlu oldukları için, bunu yapmadan önce modelinizde bir `fillable` veya `guarded` özelliği belirlemeniz gerekecektir.

**Modeldeki Korunumlu Niteliklerin Ayarlanması**

	class Uye extends Eloquent {

		protected $guarded = array('id', 'hesap_no');

	}

**Model Create Metodunun Kullanımı**

	$uye = Uye::create(array('isim' => 'Can'));

Bir modeli güncellemek için onu getirir, bir niteliğini değiştirir, sonra da `save` metodunu kullanabilirsiniz:

**Getirilen Bir Modelin Güncellenmesi**

	$uye = Uye::find(1);

	$uye->email = 'can@filan.com';

	$uye->save();

Bazen sadece bir modeli değil, onun bütün ilişkilerini de kaydetmek isteyebilirsiniz. Bunu yapmak için `push` metodunu kullanın:

**Bir Model ve İlişkilerinin Kaydedilmesi**

	$uye->push();

Ayrıca, bir modeller kümesinde güncelleme sorguları da çalıştırabilirsiniz:

	$satirSayisi = Uye::where('puan', '>', 100)->update(array('durum' => 2));

Bir modeli silmek için olgu üzerinde `delete` metodunu çağırın:

**Mevcut Bir Modelin Silinmesi**

	$uye = Uye::find(1);

	$uye->delete();

**Mevcut Bir Modelin Key Aracılığıyla Silinmesi**

	Uye::destroy(1);

	Uye::destroy(1, 2, 3);

Gayet tabii, bir modeller kümesinde bir silme sorgusu da çalıştırabilirsiniz:

	$satirSayisi = Uye::where('puan', '>', 100)->delete();

Eğer bir modelde sadece zaman damgalarını güncellemek istiyorsanız, `touch` metodunu kullanabilirsiniz:

**Bir Modelin Sadece Zaman Damgalarının Güncellenmesi**

	$uye->touch();

<a name="timestamps"></a>
## Zaman Damgaları

Ön tanımlı olarak, veritabanı tablonuzdaki `created_at` ve `updated_at` sütunlarının idamesini otomatik olarak Eloquent yapacaktır. Size tek düşen `datetime` tipindeki bu iki alanı tablonuza eklemektir, geri kalan işleri Eloquent üstlenecektir. Şayet siz bu sütunların idamesini Eloquent'in yapmasını istemiyorsanız, modelinize şu özelliği eklemeniz gerekir:

**Otomatik Zaman Damgalarının Devre Dışı Bırakılması**

	class Uye extends Eloquent {

		protected $table = 'uyeler';

		public $timestamps = false;

	}

Zaman damgalarınızın biçimini özelleştirmek isterseniz, modelinizdeki `freshTimestamp` metodunu ezebilirsiniz(override):

**Özel Bir Zaman Damgası Biçiminin Şart Koşulması**

	class Uye extends Eloquent {

		public function freshTimestamp()
		{
			return time();
		}

	}

<a name="soft-deleting"></a>
## Belirsiz Silme

Bir model belirsiz silindiğinde, aslında veritabanınızdan çıkartılmaz. Onun yerinde kayıttaki bir `deleted_at` zaman damgası ayarlanır. Bir modeli için belirsiz silmeler yapılabilmesi için modelinizde `softDelete` özelliğine atama yapmanız gerekir:

	class Uye extends Eloquent {

		protected $softDelete = true;

	}

Tablonuza bir `deleted_at` sütunu eklemek için ise, bir migrasyondan `softDeletes` metodunu kullanabilirsiniz:

	$table->softDeletes();

Şimdi, artık modelinizde `delete` metodunu çağırdığınız zaman, bu `deleted_at` sütunu güncel zaman damgasına ayarlanacaktır. Belirsiz silme kullanılan bir model sorgulandığında, "silinmiş olan" modeller sorgu sonuçlarına dahil edilmeyecektir. Bir sonuç kümesinde belirsiz silinmiş modellerin gözükmesini zorlamak için sorgunuzda `withTrashed` metodunu kullanınız:

**Belirsiz Silinmiş Modelleri Sonuçlara Girmeye Zorlama**

	$uyeler = Uye::withTrashed()->where('hesap_no', 1)->get();

Sonuç kümenizde **sadece** belirsiz silinmiş modellerin olmasını istiyorsanız, `onlyTrashed` metodunu kullanabilirsiniz:

	$uyeler = Uye::onlyTrashed()->where('hesap_no', 1)->get();

Belirsiz silinmiş bir modeli tekrar etkin hale getirmek için, `restore` metodunu kullanın:

	$uye->restore();

`restore` metodunu bir sorguda da kullanabilirsiniz:

	Uye::withTrashed()->where('hesap_no', 1)->restore();

`restore` metodu ilişkilerde de kullanılabilir:

	$uye->postalar()->restore();

Bir modeli veritabanından gerçekten çıkartmak istediğinizde, `forceDelete` metodunu kullanabilirsiniz:

	$uye->forceDelete();

`forceDelete` metodu ilişkilerde de çalışır:

	$uye->postalar()->forceDelete();

Belli bir model olgusunun belirsiz silme özelliğine sahip olup olmadığını öğrenmek için, `trashed` metodunu kullanabilirsiniz:

	if ($uye->trashed())
	{
		//
	}

<a name="query-scopes"></a>
## Sorgu Kapsamları

Kapsamlar size sorgu mantığınızı modellerinizde tekrar tekrar kullanma imkanı verir. Bir kapsam tanımlamak için bir model metodunun başına `scope` getirmeniz yeterlidir:

**Bir Sorgu Kapsamının Tanımlanması**

	class Uye extends Eloquent {

		public function scopePopular($query)
		{
			return $query->where('puan', '>', 100);
		}

	}

**Bir Sorgu Kapsamının Kullanılması**

	$uyeler = Uye::popular()->orderBy('created_at')->get();

<a name="relationships"></a>
## İlişkiler

Pek tabii, veritabanı tablolarınız büyük ihtimalle bir diğeriyle ilişkilidir. Örneğin bir blog yazısında çok sayıda yorum olabilir veya bir sipariş onu ısmarlayan kullanıcı ile ilişkili olacaktır. Eloquent bu ilişkileri kolayca yönetmenizi ve rahat çalışmanızı sağlar. Laravel dört tip ilişkiyi desteklemektedir:

- [Birden Bire](#one-to-one)
- [Birden Birçoğa](#one-to-many)
- [Birçoktan Birçoğa](#many-to-many)
- [Çokbiçimli İlişkiler](#polymorphic-relations)

<a name="one-to-one"></a>
### Birden Bire

Birden bire şeklindeki bir ilişki çok basit bir ilişikidir. Örneğin, bir `Uye` modelinin bir `Telefon`'u olabilir. Eloquent'de bu ilişkiiyi şöyle tanımlayabiliriz:

**Birden Bire Tarzı İlişki Tanımlama**

	class Uye extends Eloquent {

		public function tel()
		{
			return $this->hasOne('Telefon');
		}

	}

`hasOne` metoduna geçirilen ilk parametre ilişkili modelin adıdır. İlişki tanımlandıktan sonra onu Eloquent'in [dinamik özellikler](#dynamic-properties)'ini kullanarak elde edebiliriz:

	$tel = Uye::find(1)->tel;

Bu cümlenin gerçekleştirdiği SQL şunlardır (tablo isimleri model tanımında özel olarak belirtilmedi ise tablo ismi olarak model isminin küçük harfli çoğul halinin kullanıldığını hatırlayınız):

	select * from uyes where id = 1

	select * from telefons where uye_id = 1

Eloquent'in ilişkideki yabancı key'in ne olduğuna model adına göre karar verdiğine dikkat ediniz. Şimdiki örnekte `Telefon` modelinin `uye_id` adlı bir yabancı key kullandığı varsayılmaktadır. Siz nu ön kuralı değiştirmek istiyorsanız `hasOne` metoduna ikinci bir parametre geçebilirsiniz:

	return $this->hasOne('Telefon', 'mahsus_key');

`Telefon` modeli üzerinde ilişkinin tersini tanımlamak için, `belongsTo` metodunu kullanınız:

**Bir İlişkinin Tersinin Tanımlanması**

	class Telefon extends Eloquent {

		public function uye()
		{
			return $this->belongsTo('Uye');
		}

	}

<a name="one-to-many"></a>
### Birden Birçoğa

Birde birçoğa ilişki örneği olarak birçok yorum yapılmış bir blog yazısı verilebilir. Bu ilişkiyi de şöyle modelleyebiliriz:

	class Makale extends Eloquent {

		public function yorumlar()
		{
			return $this->hasMany('Yorum');
		}

	}

Şimdi artık bir makalenin yorumlarına [dinamik özellik](#dynamic-properties) aracılığıyla ulaşabiliriz:

	$yorumlar = Makale::find(1)->yorumlar;

Hangi yorumların alınacağını daha da kısıtlamak için `yorumlar` metodunu çağırabilir ve şartlar koşmayı sürdürebilirsiniz:

	$yorumlar = Makale::find(1)->yorumlar()->where('baslik', '=', 'bu')->first();

Tıpkı hasOne'de olduğu gibi konvansiyonel yabancı key varsayımını `hasMany` metoduna ikinci bir parametre geçerek değiştirebilirsiniz:

	return $this->hasMany('Yorum', 'mahsus_key');

İlişkinin tersini `Yorum` modelinde tanımlamak için, `belongsTo` metodu kullanılmaktadır:

**Bir İlişkinin Tersinin Tanımlanması**

	class Yorum extends Eloquent {

		public function makale()
		{
			return $this->belongsTo('Makale');
		}

	}

<a name="many-to-many"></a>
### Birçoktan Birçoğa

Birçoktan birçoğa ilişkiler daha karmaşık bir ilişki tipidir. Bu tarz bir ilişki örneği bir üyenin birçok rolü olması, aynı zamanda bu rollerin başka kullanıcılar tarafından da paylaşılmasıdır. Örneğin birçok üye "Müdür" rolünde olabilir. Bu ilişki için üç veritabanı tablosu gereklidir: `uyeler`, `roller` ve `rol_uye`. Bu `rol_uye` tablosu ilişkili model isimlerinin alfabetik sıralamasına göre adlandırılır ve `uye_id` ve `rol_id` sütunlarına sahip olmalıdır (model isimlerine alttire ve id eklenmiş iki alan).

Birçoktan birçoğa ilişikileri `belongsToMany` metodunu kullanarak tanımlayabiliyoruz:

	class Uye extends Eloquent {

		public function roller()
		{
			return $this->belongsToMany('Rol');
		}

	}

Artık rolleri `Uye` modeli aracılığıyla getirebiliriz:

	$roller = Uye::find(1)->roller;

Pivot tablo ismi olarak ön kabullü tablo ismi yerine başka bir isim kullanmak isterseniz, bunu `belongsToMany` metoduna ikinci bir parametre geçerek gerçekleştirebilirsiniz:

	return $this->belongsToMany('Rol', 'uye_rollleri');

İlişkili key için konvansiyonel yaklaşımı da değiştirebilirsiniz:

        return $this->belongsToMany('Rol', 'uye_rollleri', 'user_id', 'foo_id');

Ve tabii ki ilişkinin tersini `Rol` modelinde de tanımlayabilirsiniz:

	class Rol extends Eloquent {

		public function uyeler()
		{
			return $this->belongsToMany('Uye');
		}

	}

<a name="polymorphic-relations"></a>
### Çokbiçimli İlişkiler

Çokbiçimli (Polimorfik) İlişkiler bir modelin tek bir ilişkilendirme ile birden çok modele ait olmasına imkan verir. Örneğin, kendisi ya bir personel modeline ya da bir siparis modeline ait olan bir foto modeliniz olduğunu düşünün. Bu ilişkiyi şu şekilde tanımlayacağız:

	class Foto extends Eloquent {

		public function resim()
		{
			return $this->morphTo();
		}

	}

	class Personel extends Eloquent {

		public function fotolar()
		{
			return $this->morphMany('Foto', 'resim');
		}

	}

	class Siparis extends Eloquent {

		public function fotolar()
		{
			return $this->morphMany('Foto', 'resim');
		}

	}

Artık bir personel ya da siparişe ait fotoları elde edebiliriz:

**Çokbiçimli Bir İlişkinin Getirilmesi**

	$personel = Personel::find(1);

	foreach ($personel->fotolar as $foto)
	{
		//
	}

Ancak, "çokbiçimli" ilişkinin gerçek farkını bir personel veya siparişe `Foto` modelinden erişebilmekle görürsünüz:

**Çokbiçimli Bir İlişkinin Sahibinin Getirilmesi**

	$foto = Foto::find(1);

	$resim = $foto->resim;

`Foto` modelindeki `resim` ilişkisi, fotonun sahibi olan modele bağlı olarak ya bir `Personel` ya da bir `Siparis` olgusu döndürecektir.

Bunun nasıl çalıştığını anlamanıza yardımcı olmak için veritabanı yapımızı polimorfik bir ilişkiye açalım:

**Polymorphic Relation Table Structure**

	personel
		id - integer
		isim - string

	siparisler
		id - integer
		fiyat - integer

	fotolar
		id - integer
		dosyayolu - string
		resim_id - integer
		resim_type - string

Buradaki anahtar alanların The key fields to notice here are the on the `fotolar` tablosundaki `resim_id` and `resim_type` olduğuna dikkat ediniz. Buradaki ID, fotonun sahibi olan personel veya siparişin ID'ini, TYPE ise sahip olan modelin sınıf adını tutacaktır. Böylece ORM, `resim` ilişkisiyle erişildiğinde döndürülecek sahip modelin hangisi olduğunu tespit edebilecektir.

<a name="querying-relations"></a>
## İlişkilerin Sorgulanması

Bir modelin kayıtlarına erişirken, sonuçları bir ilişki varlığına göre sınırlamak isteyebilirsiniz. Diyelim ki, en az bir yorum yapılmış tüm blog makalelerini çekmek istediniz. Bunu yapmak için `has` metodunu kullanabilirsiniz:

**Seçerken İlişkilerin Yoklanması**

	$makaleler = Makale::has('yorumlar')->get();

Ayrıca, bir işlemci ve bir sayı da belirleyebilirsiniz, örneğin üç ve daha çok yorum almış makaleleri getirmek için:

	$makaleler = Makale::has('yorumlar', '>=', 3)->get();

<a name="dynamic-properties"></a>
### Dinamik Özellikler

Eloquent, ilişkilerinize dinamik özellikle yoluyla erişme imkanı verir. Eloquent ilişkiyi sizin için otomatik olarak yükleyecektir. Hatta, `get` (birden birçoğa ilişkiler için) metodunun mu yoksa `first` (birden bire ilişkiler için) metodunun mu çağırılacağını bilecek kadar akılllıdır. İlişkiyle aynı isimli dinamik bir özellik aracılığı ile erişileblir olacaktır. Örneğin, şu `$telefon` modelinde:

	class Telefon extends Eloquent {

		public function uye()
		{
			return $this->belongsTo('Uye');
		}

	}

	$telefon= Telefon::find(1);
	
Bu kullanının email'ini şu şekilde göstermek yerine:

	echo $telefon->uye()->first()->email;

Buradaki gibi basit bir hale kısaltılabilir:

	echo $telefon->uye->email;

<a name="eager-loading"></a>
## Ateşli Yüklemeler

Ateşli yükleme N + 1 sorgu problemini gidermek içindir. Örnek olarak, `Yazar` ile ilişkilendirilmiş bir `Kitap` modelini düşünün. İlişki de şöyle tanımlanmış olsun:

	class Kitap extends Eloquent {

		public function yazar()
		{
			return $this->belongsTo('Yazar');
		}

	}

Şimdi, şu kodu ele alalım:

	foreach (Kitap::all() as $kitap)
	{
		echo $kitap->yazar->isim;
	}

Bu döngü tablodaki kitapların hepsini almak için 1 sorgu çalıştıracak, sonra da yazarını elde etmek için her bir kitabı sorgulayacaktır. Yani, eğer 25 kitabımız varsa bu döngü 26 sorgu çalıştıracaktır.

Neyseki, sorgu sayısını büyük ölçüde azaltan ateşli yükleme kullanabiliriz. Ateşli yüklenecek ilişkiler `with` metodu aracılığıyla belirlenebilmektedir:

	foreach (Kitap::with('yazar')->get() as $kitap)
	{
		echo $kitap->yazar->isim;
	}

Yukardaki döngüde sadece iki sorgu çalıştırılacaktır (model tanımında tablo isimleri açıkça belirtilmediyse ingilizce küçük harf çoğul kabulünü hatorlayınız):

	select * from kitaps

	select * from yazars where id in (1, 2, 3, 4, 5, ...)

Ateşli yüklemenin akıllıca kullanımı uygulamanızın performansını önemli ölçüde artırabilir.

Tabii ki, bir defada birden çok ilişkiyi ateşli yükleyebilirsiniz:

	$kitaplar = Kitap::with('yazar', 'kitabevi')->get();

Hatta içi içe ilişkileri de ateşleyebilirsiniz:

	$kitaplar = Kitap::with('yazar.kisiler')->get();

Yukarıdaki örnekte `yazar` ilişkisi ateşli yüklenecektir ve yazarın `kisiler` ilişkisi de ateşli yüklenecektir.

### Ateşli Yükleme Sınırlamaları

Bazen bir ilişkiyi ateşli yüklemek, ama ateşli yükleme için de bir şart belirlemek isteyebiliriz. İşte bir örnek:

	$uyeler = Uye::with(array('makaleler' => function($query)
	{
		$query->where('baslik', 'like', '%birinci%');
	}))->get();

Bu örnekte üyenin makalelerinden sadece baslik alaninda "birinci" kelimesi geçen makalelerini ateşli yüklüyoruz.

### Tembel Ateşli Yükleme

İlişkili modelleri, direkt olarak önceden mevcut model koleksiyonundan ateşli yüklemek de mümkündür. Bu özellikle ilişkili modeli önbellekleme ile birlikte yükleyip yüklememeye dinamik karar vereceğiniz zaman işe yarayabilir.

	$kitaplar= Kitap::all();

	$kitaplar->load('yazar', 'kitabevi');

<a name="inserting-related-models"></a>
## İlişkili Modelleri Ekleme

Yeni ilişkili model ekleme ihtiyacınız çok olacaktır. Örneğin, bir makale için yeni bir yorum eklemek isteyebilirsiniz. Model üzerinde `makale_id` yabancı key alanını elle ayarlamak yerine, doğrudan ebeveyn `Makale` modelinden yeni yorum ekleyebilirsiniz:

**İlişkili Bir Modelin Eklenmesi**

	$yorum = new Yorum(array('mesaj' => 'Yeni bir yorum.'));

	$makale = Makale::find(1);

	$yorum = $makale->yorumlar()->save($yorum);

Bu örnekte eklenen yorumdaki `makale_id` alanı otomatik olarak ayarlanmaktadır.

### İlişkili Model Ekleme (Birçoktan Birçoğa)

Birçoktan birçoğa ilişkilerle çalışırken de ilişkili model ekleyebilirsiniz. Daha önceki örneğimiz `Uye` ve `Rol` modellerini kullanamaya devam edelim. Bir uyeye yeni roller eklemeyi `attach` metodu ile yapabiliriz:

**Birçoktan Birçoğa Modellerinin Eklenmesi**

	$uye = Uye::find(1);

	$uye->roller()->attach(1);

İlişkiler için pivot tabloda tutulan nitelelikleri bir diz olarak da geçebilirsiniz:

	$uye->roller()->attach(1, array('sonaerme' => $sonaerme));

Tabii, `attach`'in ters işlemi `detach`'tir:

	$uye->roller()->detach(1);

İlişkili modelleri bağlamak için `sync` metodunu da kullanabilirsiniz. Bu `sync` metodu parametre olarak pivot tablodaki yerlerin id'lerinden oluşan bir dizi geçirilmesini ister. Bu işlem tamamlandıktan sonra, model için kullanıcak ara tabloda sadece bu id'ler olacaktır:

**Birçoktan Birçoğa Model Bağlamak İçin Sync Kullanımı**

	$uye->roller()->sync(array(1, 2, 3));

Belli id değerleri olan başka pivot tabloyu da ilişkilendirebilirsiniz:

**Sync Yaparken Pivot Veri Eklenmesi**

	$uye->roller()->sync(array(1 => array('sonaerme' => true)));

Bazen yeni bir ilişkili model oluşturmak ve tek bir komutla bunu eklemek isteyebilirsiniz. Bu işlem için, `save` metodunu kullanabilirsiniz:

	$rol = new Rol(array('isim' => 'Editor'));

	Uye::find(1)->roller()->save($rol);

Bu örnekte, yeni bir `Rol` modeli kaydedilecek ve uye modeline eklenecektir. Bu işlem için bağlı tablolardaki niteliklerden oluşan bir dizi de geçebilirsiniz:

	Uye::find(1)->roller()->save($rol, array('sonaerme' => $sonaerme));

<a name="touching-parent-timestamps"></a>
## Ebeveyn Zaman Damgalarına Dokunma

Bir `Yorum`'un bir `Makale`'ye ait olması örneğimizdeki gibi, bir model başka bir modele ait (`belongsTo`) olduğu takdirde, çocuk modeli güncellediğiniz zaman ebeveyn zaman damgasını da güncellemek iyidir. Örneğin, bir `Yorum` güncellendiğinde, bunun sahibi olan `Makale`'nin `updated_at` zaman damgasını otomatikman güncellemek isteyebilirsiniz. Bunu gerçekleştirmek için tek yapacağınız şey, çocuk modele ilişkilerin isimlerini içeren bir `touches` özelliği   eklemektir:

	class Yorum extends Eloquent {

		protected $touches = array('makale');

		public function makale()
		{
			return $this->belongsTo('Makale');
		}

	}

Bunu yaptıktan sonra artık bir `Yorum` güncellediğinizde, sahibi olan `Makale` de güncellenmiş bir `updated_at` sütununa sahip olacaktır:

	$yorum = Yorum::find(1);

	$yorum->text = 'Bu yorumu düzelt!';

	$yorum->save();

<a name="working-with-pivot-tables"></a>
## Pivot Tablolarla Çalışmak

Daha önce öğrendiğiniz gibi, birçoktan birçoğa ilişkilerle çalışmak bir ara tablonun olmasını gerektirir. Eloquent işte bu tablo ile etkileşim için çok yararlı bazı yollar sağlamaktadır. Örneğin bizim bir `Uye` nesnemiz, bir de onun bağlı olduğu birçok `Rol` nesnelerimiz olsun. Bu ilişkiye eriştikten sonra, `pivot` tabloya modellerimiz üzerinden erişebiliriz:

	$uye = Uye::find(1);

	foreach ($uye->roller as $rol)
	{
		echo $rol->pivot->created_at;
	}

Dikkat ederseniz, elde ettiğimiz her bir `Rol` modeline otomatikman bir `pivot` niteliği atanmıştır. Bu nitelik, ara tabloyu temsil eden bir modeli taşır ve herhangi bir Eloquent modeli gibi kullanılabilir.

Ön tanımlı olarak, `pivot` nesnesinde sadece keyler olacaktır. Şayet pivot tablonuzda bunlardan başka nitelikler varsa, bunları ilişki tanımlama sırasında belirtmelisiniz:

	return $this->belongsToMany('Rol')->withPivot('falan', 'filan');

Şimdi `Rol` modelinin `pivot` nesnesinde `falan` ve `filan` nitelikleri erişilebilir olacaktır.

Eğer pivot tablonuzun `created_at` ve `updated_at` zaman damgalarını otomatik olarak halletmesini istiyorsanız, ilişki tanımlamasında `withTimestamps` metodunu kullanın:

	return $this->belongsToMany('Rol')->withTimestamps();

Bir modelin pivot tablosundaki tüm kayıtları silmek için, `detach` metodunu kullanabilirsiniz:

**Bir Pivot Tablodaki Tüm Kayıtların Silinmesi**

	Uye::find(1)->roller()->detach();

Bu operasyonun `roller` tablosundan kayıt silmediğine, sadece pivot tablodan sildiğine dikkat ediniz.

<a name="collections"></a>
## Koleksiyonlar

Eloquent tarafından döndürülen tüm çoklu sonuç kümeleri ya `get` metodu aracılığıyla döndürülür veya bir ilişki bir Eloquent `Collection` nesnesi döndürür. Bu nesne PHP'nin `IteratorAggregate` arayüzünün bir uygulama biçimidir ve tıpkı bir dizide dolaşır gibi dolaşılabilinmektedir. Bunun yanında, bu nesne sonuç kümeleriyle çalışırken işe yarayan başka bir takım metodlara da sahiptir.

Örneğin biz `contains` metodunu kullanarak bir sonuç kümesinin belli bir primer key içerip içermediğini tespit edebiliriz:

**Bir Koleksiyonun Bir Key Taşıyıp Taşımadığının Yoklanması**

	$roller = Uye::find(1)->roller;

	if ($roller->contains(2))
	{
		//
	}

Koleksiyonlar aynı zamanda bir dizi ya da JSON'a dünüştürülebilmektedir:

	$roller = Uye::find(1)->roller->toArray();

	$roller = Uye::find(1)->roller->toJson();

Eğer bir koleksiyon bir string kalıbına çevrilirse JSON olarak döndürülecektir:

	$roller = (string) Uye::find(1)->roller;

Eloquent koleksiyonları içerdikleri elemanları dolaşmak ve filtre etmekle ilgili bazı metodlara da sahiptir:

**Koleksiyonlarda Tekrarlı İşlemler ve Süzmeler**

	$roller = $uye->roller->each(function($rol)
	{

	});

	$roller = $uye->roller->filter(function($rol)
	{

	});

**Her Bir Koleksiyon Nesnesine Bir Dönüş (Callback) Yapmak**

	$roller = Uye::find(1)->roller;
	
	$roller->each(function($rol)
	{
		//	
	});

**Bir Koleksiyonu Bir Değere Göre Sıralama**

	$roller = $roller->sortBy(function($rol)
	{
		return $rol->created_at;
	});

Bazen de, kendi eklediğiniz metodları olan özel bir koleksiyon nesnesi döndürmek isteyebilirsiniz. Bunu, Eloquent modeliniz üzerinde `newCollection` metodunu ezerek yapabilirsiniz:

**Özel Bir Koleksiyon Tipinin Döndürülmesi**

	class Uye extends Eloquent {

		public function newCollection(array $models = array())
		{
			return new CustomCollection($models);
		}

	}

<a name="accessors-and-mutators"></a>
## Erişimciler & Değiştiriciler (Accessors & Mutators)

Eloquent model niteliklerini alıp getirirken veya onları ayarlarken dönüşüm yapmak için uygun bir yol sağlar. Bir erişimci beyan etmek için modeliniz üzerinde sadece bir `getFilanAttribute` metodu tanımlamak yeterlidir. Yalnız unutmamanız gereken şey, veritabanı sütunlarınızın isimleri yılan tarzı (küçük harfli kelimelerin boşluk olmaksızın alt tire ile birbirine bağlanması) olsa dahi, metodlarınızın deve tarzı (birinci kelimenin tümü küçük harf olmak ve sonraki kelimelerin ilk harfi büyük diğer hafleri küçük olmak üzere boşluk olmaksızın kelimelerin yanyana dizilmesi) olması gerektiğidir:

**Bir Erişimci Tanımlanması**

	class Uye extends Eloquent {

		public function getSoyAdiAttribute($value)
		{
			return ucfirst($value);
		}

	}

Yukarıdaki örnekte `soy_adi` sütununun bir erişimcisi vardır. Niteliğin değerinin erişimciye geçildiğine dikkat ediniz.

Değiştiriciler de benzer şekilde deklare edilir:

**Bir Değiştirici Tanımlanması**

	class Uye extends Eloquent {

		public function setSoyAdiAttribute($value)
		{
			$this->attributes['soy_adi'] = strtolower($value);
		}

	}

<a name="date-mutators"></a>
## Tarih Değiştiricileri

Ön tanımlı olarak, Eloquent will convert the `created_at`, `updated_at`, and `deleted_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), olgularına çevirecektir. Carbon çeşitli yardımcı metodlar sağlar ve PHP'nin `DateTime` sınıfını genişletir.

Siz hangi alanların otomatik olarak değiştirileceğini isteğinize göre ayarlayabilirsiniz, hatta modeldeki `getDates` metodunu ezmek suretiyle bu motasyonu tamamen devre dışı bırakabilirsiniz:

	public function getDates()
	{
		return array('created_at');
	}

Bir sütun bir tarih olarak kabul edildiğinde, bunun değerini bir UNIX timetamp, date string (`Y-m-d`), date-time string ve tabii ki bir `DateTime` / `Carbon` olgusuna ayarlayabilirsiniz.

Tarih değiştiricilerini tümden devre dışı bırakmak için `getDates` metodunda boş bir dizi döndürünüz:

	public function getDates()
	{
		return array();
	}

<a name="model-events"></a>
## Model Olayları

Eloquent modelleri bazı olayları tetikleyerek, modelin yaşam döngüsündeki çeşitli noktalarda müdahale etmenize imkan verir. Bu amaçla şu metodlar kullanılmaktadır: `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`. Eğer `creating`, `updating` veya `saving` olaylarından `false` döndürülürse, eylem iptal edilecektir:

**Saklama Operasyonlarının Olaylar Aracığıyla İptal Edilmesi**

	Uye::creating(function($uye)
	{
		if ( ! $uye->isValid()) return false;
	});

Eloquent modelleri bunun dışında static bir `boot` metodu içermekte olup, olay bağlamanızı kayıt etmeniz için uygun bir yerdir.

**Bir Model Boot Metodunun Ayarlanması**

	class Uye extends Eloquent {

		public static function boot()
		{
			parent::boot();

			// Olay bağlamayı ayarla...
		}

	}

<a name="model-observers"></a>
## Model Gözlemcileri

Model olaylarının işlenmesini pekiştirmek için, bir model gözlemcisi kaydı yapabilirsiniz. Bir gözlemci sınıfında çeşitli model olaylarına tekabül eden metodlar bulunabilir. Örneğin bir gözlemcide, diğer model olay isimlerine ek olarak `creating`, `updating`, `saving` metodları olabilir.

Yani, bir model gözlemcisi şöyle olabilir:

	class UyeGozlemcisi {

		public function saving($model)
		{
			//
		}

		public function saved($model)
		{
			//
		}

	}

Modelinizde `observe` metodunu kullanarak bir gözlemci olgusu kaydı yapabilirsiniz:

	Uye::observe(new UyeGozlemcisi);

<a name="converting-to-arrays-or-json"></a>
## Diziye / JSON'a Çevirme

JSON APIler oluşturulurken, çoğu defa modellerinizi ve ilişkilerini dizilere veya JSON'a çevirmeniz gerekecektir. Bu yüzden Eloquent bunları yapacak metodlar içermektedir. Bir modeli ve onun yüklenen ilişkilerini bir diziye çevirmek için `toArray` metodunu kullanabilirsiniz:

**Bir Modelin Bir Diziye Çevrilmesi**

	$uye = Uye::with('roller')->first();

	return $uye->toArray();

Modellerin koleksiyonlarının da bütün olarak dizilere dönüştürülebildiğini unutmayın:

	return Uye::all()->toArray();

Bir Modeli JSON'a çevirmek için, `toJson` metodunu kullanabilirsiniz:

**Bir Modelin JSON'a Çevrilmesi**

	return Uye::find(1)->toJson();

Bir model veya koleksiyon bir string kalıbına sokulduğu takdirde, JSON'a çevrileceğine dikkat ediniz. Yani Elequent nesnelerini direkt olarak uygulamanızın rotalarından döndürebilirsiniz!

**Bir Modelin Bir Rotadan Döndürülmesi**

	Route::get('uyeler', function()
	{
		return Uye:all();
	});

Bazen bazı nitelikleri (örneğin şifreleri) modelinizin dizi veya JSON biçimlerinden hariç tutmak isteyebilirsiniz. Bunu yapmak için modelinize bir `hidden` özelliği ekleyiniz:

**Niteliklerin Dizi veya JSON'a Çevrilmekten Saklanması**

	class Uye extends Eloquent {

		protected $hidden = array('parola');

	}

Alternatif olarak, beyaz bir liste tanımlamak için `visible` özelliğini kullanabilirsiniz:

	protected $visible = array('adi', 'soy_adi');
