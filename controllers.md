# Denetçiler (Controllers)

- [Temel Denetçiler](#basic-controllers)
- [Denetçi Filtreleri](#controller-filters)
- [TEDA-uyumlu (TEmsili Durum Aktarma Uyumlu, RESTful) Denetçiler](#restful-controllers)
- [Kaynak (Resource) Denetçileri](#resource-controllers)
- [Eksik Olan Eylemlerin Yönetilmesi](#handling-missing-methods)

<a name="basic-controllers"></a>
## Temel Denetçiler

Bütün rotalandırma mantığını, tüm rotaları tek tek `routes.php` dosyasında tanımlamak yerine, bu davranışlarını Denetçiler (Controllers) sınıflarını kullanarak organize edebilirsiniz. Denetçiler, ilişkin oldukları rotaların mantığını bir sınıfta gruplar. Aynı zamanda, daha ileri çerçeve (framework) özelliklerini kullanma avantajına sahiptirler, örneğin otomatik [dependency injection](/docs/ioc) (veri enjeksiyonu) gibi.

Denetçiler genelde `app/controllers` dizininde konumlandırılır ve `composer.json` dosyanızın sınıf haritası `classmap` seçeneğinde, varsayılan olarak bu dizin belirlenmiştir.

Basit bir denetçi (controller) sınıfı örneği şöyledir:

	class KullaniciController extends BaseController {

		/**
		 * Verilen kullanıcının profilini göster.
		 */
		public function showProfile($id)
		{
			$kullanici = Kullanici::find($id);

			return View::make('kullanici.profil', array('kullanici' => $kullanici));
		}

	}

Bütün denetçilerin `BaseController` sınıfından türetilmiş olması gerekir.  `BaseController` ın kendisi de `app/controllers` dizininde bulunur ve bütün denetçiler için geçerli olacak ortak mantığın içine yerleştirilmesinde kullanılabilir. `BaseController` sınıfı, çerçevenin `Controller` sınıfının uzantısıdır. Bu durumda, oluşturmuş olduğumuz denetçi fonksiyonuna rotalandırmayı şu şekilde yapabiliriz:

	Route::get('kullanici/{id}', 'KullaniciController@showProfile');

Eğer bir denetçinizi, dizin içerisinde yuvalandırarak (nest) veya PHP isim-alanları (namespaces) kullanarak organize etmek isterseniz, bu durumda rotayı tanımlarken, tam nitelendirilmiş (fully qualified) sınıf adını kullanınız:

	Route::get('falanca', 'Namespace\FalancaController@yontemAdi');

Denetçi rotalarına isimler de verebilirsiniz:

	Route::get('falanca', array('uses' => 'FalancaController@yontemAdi',
											'as' => 'rotaAdi'));

Herhangi bir denetçi eylemine ait bir URL üretmek için, `URL::action` yöntemini kullanabilirsiniz:

	$url = URL::action('FalancaController@yontemAdi');

Çalıştırılmakta olan bir denetçi eyleminin ismine `currentRouteAction` yöntemi ile erişebilirsiniz:

	$action = Route::currentRouteAction();

<a name="controller-filters"></a>
## Denetçi Filtreleri

Denetçi rotalarına, diğer rotalarda olduğuna benzer şekilde, filtreler [Filters](/docs/routing#route-filters) belirlenebilir:

	Route::get('profile', array('before' => 'auth',
				'uses' => 'KullaniciController@showProfile'));

Filtreleri, denetçinizin içerisinden de belirtebilirsiniz:

	class KullaniciController extends BaseController {

		/**
		 * Yeni bir KullaniciController sureti (instance) oluştur. (new KullaniciController)
		 */
		public function __construct()
		{
			$this->beforeFilter('auth');

			$this->beforeFilter('csrf', array('on' => 'post'));

			$this->afterFilter('log', array('only' =>
								array('falancaYontem', 'filancaYontem')));
		}

	}

Filtre fonksiyonun tanımlamasını denetçinin içerisinde ve bir bloklama {  } kullanarak yapabilirsiniz:

	class KullaniciController extends BaseController {

		/**
		 * Yeni bir KullaniciController sureti (instance) oluştur. (new KullaniciController)
		 */
		public function __construct()
		{
			$this->beforeFilter(function()
			{
				//
			});
		}

	}

<a name="restful-controllers"></a>
## TEDA-uyumlu (Temsili Durum Aktarma uyumlu, RESTful) Denetçiler

Laravel size, basit TEDA (REST) isimlendirme tüzüklerini (naming conventions) kullanarak, belirleyeceğiniz tek bir rota ile, denetçilerinizin içindeki her eylemi kullanabilme imkanını tanır. İlk olarak, (rota : denetçi) `Route::controller` yöntemi ile bu rotayı tanımlayınız:

**TEDA-uyumlu Bir Denetçi Oluşturulması**

	Route::controller('kullanicilar', 'KullaniciController');

`controller` (denetçi) yöntemi iki argüman alır. Birincisi denetçinin yöneteceği baz URI olup, ikincisi denetçinin sınıf ismidir. Akabinde sadece, isimlerine HTTP eyleminin ön ek olarak ekleneceği ve bunlara cevap verecek olan yöntemlerinizi denetçinize ilave ediniz:

	class KullaniciController extends BaseController {

		public function getIndex()
		{
			//
		}

		public function postProfile()
		{
			//
		}

	}

`index` (fihrist) yöntemleri, denetçi tarafından yönetilmekte olan kök URI 'a cevap verir. Örneğimizde bu, `kullanicilar` dır.

Denetçinizdeki bir eylem yönteminin ismi birden fazla kelimeden oluşuyorsa, bu eylem yöntemine, URI da kelime aralarına tire işareti "-" eklenmiş şekilde yazarak erişebilirsiniz. Örneğin, 'KullaniciController' denetçimizdeki aşağıdaki şekilde isimlendirilmiş olan yöntem, `kullanici/yonetici-profili` URI 'na cevap verecektir.

	public function getYoneticiProfili() {}

<a name="resource-controllers"></a>
## Kaynak (Resource) Denetçileri

Kaynak denetçileri, kaynaklar etrafında TEDA-uyumlu denetçiler oluşturulmasını kolaylaştırır. Artisan KSA'daki (Artisan Komut Satırı Arayüzü) `controller:make` komutunu ve de `Route::resource` yöntemini kullanmak sureti ile böyle bir denetçiyi çabucak oluşturabiliriz.

Denetçiyi komut satırını kullanarak oluşturmak için şu komutu kullanınız:

	php artisan controller:make FotoController

Bu denetçinin TEDA-uyumlu rotasını (routes.php) dosyasında kayıt ettiriniz:

	Route::resource('foto', 'FotoController');

Bu tek bir rota deklarasyonu, foto kaynağınız üzerinde çalıştıracağınız çeşitli TEDA-uyumlu eylem yöntemlerine erişeceğiniz rotalar oluşturur. Aynı zamanda, oluşturulmuş olan denetçide, bu eylemlerin her biri için yöntemleri hazır olarak oluşturulmuş ve hangi URI'ı ve eylemi yönettikleri yanlarına not olarak yazılmış olacaktır.

**Kaynak Denetçisinin Yöneteceği Eylemler**

HTTP Fiili | Patika                | Eylem            | Rota İsmi
-----------|-----------------------|------------------|---------------------
GET        | /kaynak               | index            | kaynak.index
GET        | /kaynak/create        | create (oluştur) | kaynak.create
POST       | /kaynak               | store (kaydet)   | kaynak.store
GET        | /kaynak/{id}          | show (göster)    | kaynak.show
GET        | /kaynak/{id}/edit     | edit (düzenle)   | kaynak.edit
PUT/PATCH  | /kaynak/{id}          | update (güncelle)| kaynak.update
DELETE     | /kaynak/{id}          | destroy (imha et)| kaynak.destroy

Bazen bu eylemlerin sadece bazılarına ihtiyaç duyabilirsiniz:

	php artisan controller:make FotoController --only=index,show   //sadece belirtilenleri

	php artisan controller:make FotoController --except=index     //belirtilenler hariç

Ve, rotasında da eylemlerin sadece bazılarını yönetmesini belirleyebilirsiniz:

	Route::resource('foto', 'FotoController',
					array('only' => array('index', 'show')));

<a name="handling-missing-methods"></a>
## Eksik Olan Yöntemlerin Yönetilmesi

Denetçide tanımlanmamış olan yöntemlere gelecek olan çağrıları yönetmek için bir "hepsini-yakala" yöntemi tanımlanabilir. Bu yöntemin isminin `missingMethod` (eksik yöntem) olması gerekir ve tek argümanı olarak gelen isteğin (request) parametrelerini  alır:

**Bir Hepsini-Yakala Yönteminin Tanımlanması**

	public function missingMethod($parameters)
	{
		//
	}
