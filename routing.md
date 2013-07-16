# Rotalar

- [Temel Rotalandırma](#basic-routing)
- [Rota Parametreleri](#route-parameters)
- [Rota Filtreleri](#route-filters)
- [İsimli Rotalar](#named-routes)
- [Rota Grupları](#route-groups)
- [Alt Alanadı(Subdomain) Rotalandırması](#sub-domain-routing)
- [Rotalarda Ön-ek](#route-prefixing)
- [Rotalara Model Ataması](#route-model-binding)
- [404 Hatası Fırlatma](#throwing-404-errors)
- [Denetçilere Rotalandırma](#routing-to-controllers)

<a name="basic-routing"></a>
## Temel Rotalandırma

Uygulamanızdaki rotaların çoğu `app/routes.php` dosyasında tanımlanır. En basit Laravel rotası "URL deseni" ve "geriçağrım fonksiyonu"ndan oluşur.

**Temel GET Rotası**

	Route::get('/', function()
	{
		return 'Merhaba Laravel!';
	});

**Temel POST Rotası**

	Route::post('bir/sey', function()
	{
		return 'Merhaba Laravel!';
	});

**Tüm HTTP Metodları(GET, POST gibi) İçin Rota Yazımı**

	Route::any('birsey', function()
	{
		return 'Merhaba Laravel!';
	});

**Rotanın Zorunlu Olarak HTTPS Üzerinden Kullanılmasını Sağlamak**

	Route::get('birsey', array('https', function()
	{
		return 'HTTPS üzerinde olmalı!';
	}));

Sık sık, rotalara link oluşturmanız gerekecek. Bunu `URL::to` metoduyla yapabilirsiniz:

	$url = URL::to('birsey');

<a name="route-parameters"></a>
## Rota Parametreleri

	Route::get('kullanici/{id}', function($id)
	{
		return 'Kullanıcı NO: '.$id;
	});

**İsteğe Bağlı Rota Parametreleri**

	Route::get('kullanici/{isim?}', function($isim = null)
	{
		return $isim;
	});

**Öntanımlı Değerli İsteğe Bağlı Rota Parametreleri**

	Route::get('kullanici/{isim?}', function($isim = 'Ali')
	{
		return $isim;
	});

**Rotalarda Düzenli İfade Kontrolü**

	Route::get('kullanici/{isim}', function($isim)
	{
		//
	})
	->where('isim', '[A-Za-z]+');

	Route::get('kullanici/{id}', function($id)
	{
		//
	})
	->where('id', '[0-9]+');

Tabii ki kuralları bir dizi hâlinde tanımlayabilirsiniz:

	Route::get('kullanici/{id}/{isim}', function($id, $isim)
	{
		//
	})
	->where(array('id' => '[0-9]+', 'isim' => '[a-z]+'))

<a name="route-filters"></a>
## Rota Filtreleri

Rota filtreleri, sitenizin yetkilendirme gereken alanlarına erişimi kısıtlamak için uygun bir yoldur. Laravel'de `auth`, `auth.basic`, `guest`, `csrf` gibi `app/filters.php` dosyasında tanımlı filtreler vardır.
**Rota Filtresi Tanımlama**

	Route::filter('yas', function()
	{
		if (Input::get('yas') < 18)
		{
			return Redirect::to('anasayfa');
		}
	});

Eğer filtreden bir yanıt(`Redirect::to` gibi) döndürülürse, bu cevap olarak kabul edilecek. Bu yüzden rotadaki ve varsa `after` filtresindeki işlemler yapılmayacaktır.

**Rotaya Filtre Ekleme**

	Route::get('kullanici', array('before' => 'yas', function()
	{
		return '18 yaş üzerisin!';
	}));

**Rotaya Birden Çok Rota Ekleme**

	Route::get('user', array('before' => 'auth|yas', function()
	{
		return '18 yaşın üzerisin ve giriş yetkin var!';
	}));

**Filtre Parametrelerini Belirtme**

	Route::filter('yas', function($rota, $istek, $deger)
	{
		//
	});

	Route::get('kullanici', array('before' => 'yas:18', function()
	{
		return 'Merhaba Laravel!';
	}));

'After' filtreleri 3. parametre olarak `$yanit` değerini alırlar. 

	Route::filter('log', function($rota, $istek, $yanit, $deger)
	{
		//
	});

**Desenli Filtreler**

URL desenine göre de rotalara filtre ataması yapabilirsiniz.

	Route::filter('admin', function()
	{
		//
	});

	Route::when('admin/*', 'admin');


Yukarıdaki örnekte, `admin` filtresi `admin/` ile başlayan tüm rotalara uygulanacaktır. `*` karakteri tüm karakterleri yakalamak için kullanılır.

Filtreleri HTTP metodlarına(GET, POST gibi) göre uygulayabilirsiniz.

	Route::when('admin/*', 'admin', array('post'));

**Filtre Sınıfları**

Daha gelişmiş filtreler için geriçağrım fonksiyonları yerine sınıfları kullanmak isteyebilirsiniz. Since filter classes are resolved out of the application [IoC Container](/docs/ioc), you will be able to utilize dependency injection in these filters for greater testability.

**Filtre Sınıfı Oluşturma**

	class BirSeyFiltresi {

		public function filter()
		{
			// Filtre işlemleri...
		}

	}

**Filtre Sınıfını Tanımlamak**

	Route::filter('birsey', 'BirSeyFiltresi');

<a name="named-routes"></a>
## İsimli Rotalar

İsimli rotalar link veya yönlendirme oluştururken kolaylık sağlar. Bir rotayı şöyle isimlendirebilirsiniz:

	Route::get('kullanici/profil', array('as' => 'profil', function()
	{
		//
	}));

Denetçi yöntemleri için de rota isimleri belirleyebilirsiniz:

	Route::get('kullanici/profil', array('as' => 'profil', 'uses' => 'KullaniciController@profilGoster'));

Şimdi, rota isimlerini link veya yönlendirme oluştururken kullanabilirsiniz:

	$url = URL::route('profil');

	$yonlendirme = Redirect::route('profil');

Çalışan rotanın ismine `currentRouteName` metoduyla ulaşabilirsiniz:

	$isim = Route::currentRouteName();

<a name="route-groups"></a>
## Rota Grupları

Bazen bir grup rotaya filtre atamanız gerekebilir. Her birine ayrı filtre atamaktansa, rota gruplarını kullanabilirsiniz:

	Route::group(array('before' => 'auth'), function()
	{
		Route::get('/', function()
		{
			// Yetki gerekir. ("auth" filtresi)
		});

		Route::get('user/profile', function()
		{
			// Yetki gerekir. ("auth" filtresi)
		});
	});

<a name="sub-domain-routing"></a>
## Alt Alanadı(Subdomain) Rotalandırması

Laravel rotaları ile alt-alanadlarını yakalayabilir ve parametre olarak kullanabilirsiniz.

**Alt-alanadı Rotası Tanımlama**

	Route::group(array('domain' => '{hesapadi}.uygulamam.com'), function()
	{

		Route::get('kullanici/{id}', function($hesapadi, $id)
		{
			//
		});

	});
<a name="route-prefixing"></a>
## Rotalarda Ön-ek

`prefix` seçeneğini kullanarak gruptaki rotalara ön-ek ekleyebilirsiniz:

**Gruplanmış Rotalara Ön-ek Ekleme**

	Route::group(array('prefix' => 'admin'), function()
	{

		Route::get('kullanici', function()
		{
			//
		});

	});

<a name="route-model-binding"></a>
## Rotalara Model Ataması

Model ataması model sınıflarının rotalarda kullanılması için kolaylık sağlar. Mesela, bir kullanıcının ID'sinin aktarılması yerine, ID ile eşleşen Kullanici modelini aktarabilirsiniz. İlk olarak, girilen parametreler için kullanılacak modelleri `Route::model` metoduyla belirleyin:

**Parametrelere Model Atanması**

	Route::model('kullanici', 'Kullanici');

Daha sonra, `{kullanici}` parametresini içeren bir rota belirleyin:

	Route::get('profil/{kullanici}', function(Kullanici $kullanici)
	{
		//
	});

`{kullaniic}` parametresi ile `Kullanici` modelini eşleştirdiğimizden, bir `Kullanici` nesnesi rotaya aktarılacaktır. Yani, `profil/1` şeklindeki istek, ID'si 1 olan `Kullanici` nesnesini aktaracaktır. 

> **Not:** Eğer model için veritabanında eşleşme yapılamazsa, 404 hatası fırlatılır.

Eğer eşleşmeme durumunda yapılacak işlemi kendiniz belirlemek istiyorsanız, `model` metoduna 3. argüman olarak bir geriçağrım fonksiyonu ekleyebilirsiniz:
	Route::model('kullanici', 'Kullanici', function()
	{
		throw new NotFoundException;
	});

Modeller yerine kendi tanımlayıcınızı kullanmak isteyebilirsiniz. Bunun için `Route::bind` metodu kullanılır:
	Route::bind('kullanici', function($deger, $rota)
	{
		return Kullanici::where('isim', $deger)->first();
	});

<a name="throwing-404-errors"></a>
## 404 Hatalası Fırlatma

404 hatasını tetiklemenin iki yolu vardır. İlki, `App::abort` metodu.
	App::abort(404);

İkinci, `Symfony\Component\HttpKernel\Exception\NotFoundHttpException` nesnesi oluşturmaktır.
404 hatalarının yakalanması ve özel yanıtla oluşturulması hakkında daha fazla bilgiye dokümantasyonun [hatalar](/docs/errors#handling-404-errors) bölümünden ulaşabilirsiniz.
<a name="routing-to-controllers"></a>
## Denetçilere Rotalama

Laravel sadece geriçağrım fonksiyonlarına rotalama sağlamaz. Aynı zamanda denetçi sınıflarına hatta [kaynak denetçilerine](/docs/controllers#resource-controllers) rotalandırma yapılabilir.

Daha fazla bilgi için [Denetçiler](/docs/controllers) konusunu inceleyin.
