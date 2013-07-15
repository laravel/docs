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
- [Working With Pivot Tables](#working-with-pivot-tables)
- [Collections](#collections)
- [Accessors & Mutators](#accessors-and-mutators)
- [Date Mutators](#date-mutators)
- [Model Events](#model-events)
- [Model Observers](#model-observers)
- [Converting To Arrays / JSON](#converting-to-arrays-or-json)

<a name="introduction"></a>
## Giriş

Laravelle gelen "Eloquent ORM", veritabanınızla çalışırken kullanacağınız güzel ve sade bir ActiveRecord uygulaması sağlamaktadır. Her veritabanı tablosu, bu tabloyla etkilişim için kullanıcak kendine has bir  "Model" sahibidir.

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

When a model `belongsTo` another model, such as a `Comment` which belongs to a `Post`, it is often helpful to update the parent's timestamp when the child model is updated. For example, when a `Comment` model is updated, you may want to automatically touch the `updated_at` timestamp of the owning `Post`. Eloquent makes it easy. Just add a `touches` property containing the names of the relationships to the child model:

	class Comment extends Eloquent {

		protected $touches = array('post');

		public function post()
		{
			return $this->belongsTo('Post');
		}

	}

Now, when you update a `Comment`, the owning `Post` will have its `updated_at` column updated:

	$comment = Comment::find(1);

	$comment->text = 'Edit to this comment!';

	$comment->save();

<a name="working-with-pivot-tables"></a>
## Working With Pivot Tables

As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` object has many `Role` objects that it is related to. After accessing this relationship, we may access the `pivot` table on the models:

	$user = User::find(1);

	foreach ($user->roles as $role)
	{
		echo $role->pivot->created_at;
	}

Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table, and may be used as any other Eloquent model.

By default, only the keys will be present on the `pivot` object. If your pivot table contains extra attributes, you must specify them when defining the relationship:

	return $this->belongsToMany('Role')->withPivot('foo', 'bar');

Now the `foo` and `bar` attributes will be accessible on our `pivot` object for the `Role` model.

If you want your pivot table to have automatically maintained `created_at` and `updated_at` timestamps, use the `withTimestamps` method on the relationship definition:

	return $this->belongsToMany('Role')->withTimestamps();

To delete all records on the pivot table for a model, you may use the `detach` method:

**Deleting Records On A Pivot Table**

	User::find(1)->roles()->detach();

Note that this operation does not delete records from the `roles` table, but only from the pivot table.

<a name="collections"></a>
## Collections

All multi-result sets returned by Eloquent either via the `get` method or a relationship return an Eloquent `Collection` object. This object implements the `IteratorAggregate` PHP interface so it can be iterated over like an array. However, this object also has a variety of other helpful methods for working with result sets.

For example, we may determine if a result set contains a given primary key using the `contains` method:

**Checking If A Collection Contains A Key**

	$roles = User::find(1)->roles;

	if ($roles->contains(2))
	{
		//
	}

Collections may also be converted to an array or JSON:

	$roles = User::find(1)->roles->toArray();

	$roles = User::find(1)->roles->toJson();

If a collection is cast to a string, it will be returned as JSON:

	$roles = (string) User::find(1)->roles;

Eloquent collections also contain a few helpful methods for looping and filtering the items they contain:

**Iterating & Filtering Collections**

	$roles = $user->roles->each(function($role)
	{

	});

	$roles = $user->roles->filter(function($role)
	{

	});

**Applying A Callback To Each Collection Object**

	$roles = User::find(1)->roles;
	
	$roles->each(function($role)
	{
		//	
	});

**Sorting A Collection By A Value**

	$roles = $roles->sortBy(function($role)
	{
		return $role->created_at;
	});

Sometimes, you may wish to return a custom Collection object with your own added methods. You may specify this on your Eloquent model by overriding the `newCollection` method:

**Returning A Custom Collection Type**

	class User extends Eloquent {

		public function newCollection(array $models = array())
		{
			return new CustomCollection($models);
		}

	}

<a name="accessors-and-mutators"></a>
## Accessors & Mutators

Eloquent provides a convenient way to transform your model attributes when getting or setting them. Simply define a `getFooAttribute` method on your model to declare an accessor. Keep in mind that the methods should follow camel-casing, even though your database columns are snake-case:

**Defining An Accessor**

	class User extends Eloquent {

		public function getFirstNameAttribute($value)
		{
			return ucfirst($value);
		}

	}

In the example above, the `first_name` column has an accessor. Note that the value of the attribute is passed to the accessor.

Mutators are declared in a similar fashion:

**Defining A Mutator**

	class User extends Eloquent {

		public function setFirstNameAttribute($value)
		{
			$this->attributes['first_name'] = strtolower($value);
		}

	}

<a name="date-mutators"></a>
## Date Mutators

By default, Eloquent will convert the `created_at`, `updated_at`, and `deleted_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which provides an assortment of helpful methods, and extends the native PHP `DateTime` class.

You may customize which fields are automatically mutated, and even completely disable this mutation, by overriding the `getDates` method of the model:

	public function getDates()
	{
		return array('created_at');
	}

When a column is considered a date, you may set its value to a UNIX timetamp, date string (`Y-m-d`), date-time string, and of course a `DateTime` / `Carbon` instance.

<a name="model-events"></a>
## Model Events

Eloquent models fire several events, allowing you to hook into various points in the model's lifecycle using the following methods: `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`. If `false` is returned from the `creating`, `updating`, or `saving` events, the action will be cancelled:

**Cancelling Save Operations Via Events**

	User::creating(function($user)
	{
		if ( ! $user->isValid()) return false;
	});

Eloquent models also contain a static `boot` method, which may provide a convenient place to register your event bindings.

**Setting A Model Boot Method**

	class User extends Eloquent {

		public static function boot()
		{
			parent::boot();

			// Setup event bindings...
		}

	}

<a name="model-observers"></a>
## Model Observers

To consolidate the handling of model events, you may register a model observer. An observer class may have methods that correspond to the various model events. For example, `creating`, `updating`, `saving` methods may be on an observer, in addition to any other model event name.

So, for example, a model observer might look like this:

	class UserObserver {

		public function saving($model)
		{
			//
		}

		public function saved($model)
		{
			//
		}

	}

You may register an observer instance using the `observe` method:

	User::observe(new UserObserver);

<a name="converting-to-arrays-or-json"></a>
## Converting To Arrays / JSON

When building JSON APIs, you may often need to convert your models and relationships to arrays or JSON. So, Eloquent includes methods for doing so. To convert a model and its loaded relationship to an array, you may use the `toArray` method:

**Converting A Model To An Array**

	$user = User::with('roles')->first();

	return $user->toArray();

Note that entire collections of models may also be converted to arrays:

	return User::all()->toArray();

To convert a model to JSON, you may use the `toJson` method:

**Converting A Model To JSON**

	return User::find(1)->toJson();

Note that when a model or collection is cast to a string, it will be converted to JSON, meaning you can return Eloquent objects directly from your application's routes!

**Returning A Model From A Route**

	Route::get('users', function()
	{
		return User::all();
	});

Sometimes you may wish to limit the attributes that are included in your model's array or JSON form, such as passwords. To do so, add a `hidden` property definition to your model:

**Hiding Attributes From Array Or JSON Conversion**

	class User extends Eloquent {

		protected $hidden = array('password');

	}

Alternatively, you may use the `visible` property to define a white-list:

	protected $visible = array('first_name', 'last_name');
