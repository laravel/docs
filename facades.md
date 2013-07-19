# Cepheler (Facades)

- [Giriş](#introduction)
- [Açıklama](#explanation)
- [Pratik Kullanım](#practical-usage)
- [Cephe Oluşturma](#creating-facades)
- [Cepheleri Taklit Etme](#mocking-facades)

<a name="introduction"></a>
## Giriş

Cepheler uygulamanızın [IoC konteynerinde](/docs/ioc) bulunan sınıflar için "statik" bir arayüz sağlar. Laravel birçok cephe ile gelmektedir ve büyük bir ihtimalle daha ne olduklarını bilmeden onları kullanıyorsunuzdur!

Zaman zaman, uygulama ve paketleriniz için kendi cephelerinizi oluşturmak isteyebilirsiniz, bu itibarla bu sınıfların kavramlarını, geliştirilmesini ve kullanımını inceleyelim.

> **Not:** Cepheler konusunu incelemeden önce Laravel [IoC konteyneri](/docs/ioc) ile çok aşina olmanız kuvvetle önerilir.

<a name="explanation"></a>
## Açıklama

Bir Laravel uygulaması bağlamında bir cephe bir nesneye onun konteynerinden erişim sağlayan bir sınıf demektir. Bu işi yapan mekanizmalar `Facade` sınıfında tanımlıdır. Laravel'in cepheleri ve sizin oluşturduğunuz kendi cepheleriniz bu temel `Facade` sınıfından türeyecektir.

Sizin cephe sınıfınız sadece tek bir metoda tatbikat getirmesi gerekiyor: `getFacadeAccessor`. `getFacadeAccessor` methodunun tanımlayacağı iş konteynerden ne çözeceğidir. `Facade` temel sınıfı sizin cephelerinizden, çözülmüş nesneye yapılan çağrıları ertelemek için `__callStatic()` sihirli-metodunu kullanır.

<a name="practical-usage"></a>
## Pratik Kullanım

Aşağıdaki örnekte, Laravel önbellekleme sistemine bir çağrı yapılmış. Bu koda göz attığınızda, `Cache` sınıfında statik bir metod olan `get`'in çağrılıyor olduğunu düşünebilirsiniz.

	$deger = Cache::get('anahtar');

Ancak, eğer `Illuminate\Support\Facades\Cache` sınıfına bakacak olursak, orada `get` adında statik bir metod olmadığını görürüz:

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

Bu Cache sınıfı temel `Facade` sınıfından türetilmiş ve `getFacadeAccessor()` adında bir metod tanımlamış. Bu metodun işinin bir IoC bağlayıcısının adını döndürmek olduğunu hatırlayın.

Bir kullanıcı `Cache` cephesinde herhangi bir statik metoda başvurduğunda, Laravel, IoC konteynerinden `cache` bağlayıcısını çözecek ve istenen metodu (bu örnekte `get`) bu nesneye karşı çalıştıracaktır.

Yani bizim `Cache::get` çağrımız şu şekilde yeniden yazılabilir:

	$value = $app->make('cache')->get('anahtar');

<a name="creating-facades"></a>
## Cephe Oluşturma

Kendi uygulama veya paketiniz için bir cephe oluşturulması kolaydır. Sadece üç şeye ihtiyacınız vardır:

- Bir IoC bağlayıcısı
- Bir cephe sınıfı.
- Bir cephe takma adı yapılandırması.

Bir örnek bakalım. Burada, `OdemeGecidi\Odeme` olarak tanımlanmış bir sınıfımız var.

	namespace OdemeGecidi;

	class Odeme {

		public function process()
		{
			//
		}

	}

Bu sınıfı IoC konteynerinden çözebiliyor olmamız lazım. Öyleyse, bir bağlayıcı ekleyelim:

	App::bind('odeme', function()
	{
		return new \OdemeGecidi\Odeme;
	});

Bu bağlayıcıyı kayda geçirmek için harika bir yer `PaymentServiceProvider` adında yeni bir [hizmet sağlayıcı](/docs/ioc#service-providers) oluşturmak ve bu bağlayıcıyı `register` metoduna eklemek olacaktır. Daha sonra Laravel'i sizin hizmet sağlayıcınızı `app/config/app.php` yapılandırma dosyasından yükleyecek şekilde yapılandırın.

Daha sonra, kendi cephe sınıfımızı oluşturabiliriz:

	use Illuminate\Support\Facades\Facade;

	class Odeme extends Facade {

		protected static function getFacadeAccessor() { return 'odeme'; }

	}

Son olarak, eğer istiyorsak, `app/config/app.php` yapılandırma dosyasındaki `aliases` dizisine kendi cephe'miz için bir takma ad ekleyebiliriz. Artık, `process` metodunu `Odeme` sınıfının bir olgusunda çağırabiliriz.

	Odeme::process();

<a name="mocking-facades"></a>
## Cepheleri Taklit Etme

Ünite testi cephelerin nasıl çalıştıkları konusunda önemli bir husustur. Gerçekten, cephelerin varlıkları için bile primer neden test edilebilirliktir. Daha fazla bilgi için, belgelerdeki [Cepheleri Taklit Etme](/docs/testing#mocking-facades) kesimine bakın.
