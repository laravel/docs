# IoC Konteyneri

- [Giriş](#introduction)
- [Basit Kullanım Şekli](#basic-usage)
- [Otomatik Çözümleme](#automatic-resolution)
- [Pratik Kullanım](#practical-usage)
- [Hizmet Sağlayıcılar](#service-providers)
- [Konteyner Olayları](#container-events)

<a name="introduction"></a>
## Giriş

Laravel inversion of control container sınıf bağımlılıklarının yönetiminde güçlü bir araçtır. Bağımlılık enjeksiyonu ağır kodlanmış sınıf bağımlılıklarının kaldırılması için bir yöntemdir. Bunun yerine, bağımlılıklar çalışma zamanında enjekte edilmekte, bağımlılık işlemleri kolayca takas edilebildiği için daha büyük esneklik sağlamaktadır.

Laravel IoC container'inin anlaşılması güçlü, büyük bir uygulama oluşturmak yanında Laravel'in kendi çekirdeğine katkıda bulunmak için de esastır.

<a name="basic-usage"></a>
## Basit Kullanım Şekli

IoC konteyneri bağımlılıkları iki yolla çözebilmektedir: ya Closure geri çağrıları yoluyla ya da otomatik çözülüm yoluyla. Önce Closure geri çağrılarını ele alalım. Birincisi, bir "tip" konteynere bağlanabilir:

**Bir Tipin Konteynere Bağlanması**

	App::bind('falan', function($app)
	{
		return new FalanFilan;
	});

**Bir Tipin Konteynerden Dönüştürülmesi**

	$deger = App::make('falan');

`App::make` metodu çağrıldığı zaman, ilgili Closure callback'i çalıştırılacak ve sonuç döndürülecektir.

Bazen, konteyner içine sadece bir kez çözümlenmesi ve aynı olgunun konteynere sonraki çağrılarda döndürülmesi gereken bir şeyler bağlamak isteyebilirsiniz:

**Konteynere "Paylaşılan" Bir Tip Bağlama**

	App::singleton('falan', function()
	{
		return new FalanFilan;
	});

`instance` metodunu kullanarak, konteynere mevcut bir nesne olgusunu da bağlayabilirsiniz:

**Mevcut Bir Olgunun Konteynere Bağlanması**

	$falan = new Falan;

	App::instance('falan', $falan);

<a name="automatic-resolution"></a>
## Otomatik Çözümleme

IoC konteyneri birçok durumda hiçbir yapılandırmaya gerek kalmadan sınıfları çözümleyecek kadar güçlüdür. Örneğin:

**Bir Sınıfın Çözümlenmesi**

	class FalanFilan {

		public function __construct(Baz $baz)
		{
			$this->baz = $baz;
		}

	}

	$falanFilan = App::make('FalanFilan');

Dikkat ederseniz, FalanFilan sınıfını konteynerde kayıt etmemiş olsak bile konteyner bu sınıfı hala çözümleyecek, hatta `Baz` bağımlılığını otomatik olarak enjekte edebilecektir!

Bir tip konteynerde bağlı olmadığı durumlarda, sınıfı görmek ve sınıf yapıcısının tip özelliklerini okumak için PHP'nin Reflection araçlarını kullanacaktır. Konteyner bu bilgiyi kullanmak suretiyle sınıfın bir olgusunu ototatik olarak inşa edecektir.

Buna karşın, bazı durumlarda, bir sınıf "somut tipte" olmayıp, arayüz tatbikatına (implementasyonuna) bağımlı olabilir. Böyle olduğu takdirde, hangi arayüz tatbikatının enjekte edileceği konusunda konteyneri bilgilendirmek için `App::bind` metodu kullanılmalıdır:

**Bir Implementasyona Bir Interface Bağlanması**

	App::bind('UyeRepositoryInterface', 'DbUyeRepository');

Şimdi şu denetçiyi ele alalım:

	class UyeController extends BaseController {

		public function __construct(UyeRepositoryInterface $uyeler)
		{
			$this->uyeler = $uyeler;
		}

	}

Biz `UyeRepositoryInterface`'i somut bir tipe bağladığımız için, `DbUserRepository` oluşturulduğu zaman otomatik olarak bu denetçiye enjekte edilecektir.

<a name="practical-usage"></a>
## Pratik Kullanım

Laravel uygulamanızın esneklik ve test edilebilirliğini artırmak amacıyla IoC konteyneri kullanmak için çeşitli fırsatlar sağlar. En başta gelen örnek denetçilerin çözümlenmesidir. Bütün denetçiler IoC kenteyneri aracılığı ile çözümlenir ve bir kontroller sınıf yapıcısındaki tip ipuçları bağımlılığı olabilir ve bunlar otomatik olarak enjekte edilecektir.

**Tip-Hinting Denetçi Bağımlılıkları**

	class SiparisController extends BaseController {

		public function __construct(SiparisRepository $siparisler)
		{
			$this->siparisler = $siparisler;
		}

		public function getIndex()
		{
			$all = $this->siparisler->all();

			return View::make('siparisler', compact('all'));
		}

	}

Bu örnekteki `SiparisRepository` sınıfı otomatik olarak kontrollere enjekte edilecektir. Bu şu anlama gelir: [unit testi](/docs/testing) sırasında "hayali" bir `SiparisRepository` konteynere bağlanabilir ve denetçiye enjekte edilebilir, böylece sorunsuz bir veritabanı katmanı etkileşimi mümkün olur.

[Filtreler](/docs/routing#route-filters), [kompozitörler](/docs/responses#view-composers) ve [olay işleyicileri](/docs/events#using-classes-as-listeners) de IoC konteynerinde çözülebilirler . Bunları kayda geçirdiğiniz zaman, sadece kullanılması gereken sınıfın adını vermeniz yeterlidir:

**Diğer IoC Kullanım Örnekleri**

	Route::filter('falan', 'FalanFilter');

	View::composer('falan', 'FalanComposer');

	Event::listen('falan', 'FalanHandler');

<a name="service-providers"></a>
## Hizmet Sağlayıcıları

Service providers are a great way to group related IoC registrations in a single location. Think of them as a way to bootstrap components in your application. Within a service provider, you might register a custom authentication driver, register your application's repository classes with the IoC container, or even setup a custom Artisan command.

In fact, most of the core Laravel components include service providers. All of the registered service providers for your application are listed in the `providers` array of the `app/config/app.php` configuration file.

To create a service provider, simply extend the `Illuminate\Support\ServiceProvider` class and define a `register` method:

**Defining A Service Provider**

	use Illuminate\Support\ServiceProvider;

	class FooServiceProvider extends ServiceProvider {

		public function register()
		{
			$this->app->bind('foo', function()
			{
				return new Foo;
			});
		}

	}

Note that in the `register` method, the application IoC container is available to you via the `$this->app` property. Once you have created a provider and are ready to register it with your application, simply add it to the `providers` array in your `app` configuration file.

You may also register a service provider at run-time using the `App::register` method:

**Registering A Service Provider At Run-Time**

	App::register('FooServiceProvider');

<a name="container-events"></a>
## Container Events

The container fires an event each time it resolves an object. You may listen to this event using the `resolving` method:

**Registering A Resolving Listener**

	App::resolving(function($object)
	{
		//
	});

Note that the object that was resolved will be passed to the callback.
