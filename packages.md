# Paket Geliştirme

- [Giriş](#introduction)
- [Bir Paket Oluşturma](#creating-a-package)
- [Paket Yapısı](#package-structure)
- [Hizmet Sağlayıcıları](#service-providers)
- [Paket Gelenekleri](#package-conventions)
- [Geliştirme İş Akışı](#development-workflow)
- [Paket Yönlendirme (Routing)](#package-routing)
- [Paket Yapılandırması](#package-configuration)
- [Paket Migrasyonları](#package-migrations)
- [Paket Varlıkları](#package-assets)
- [Paketlerin Yayımlanması](#publishing-packages)

<a name="introduction"></a>
## Giriş

Paketler Laravel'e işlevsellik eklemenin esas yollarıdır. Paketler tarihlerle çalışmanın harika bir yolu olan [Carbon](https://github.com/briannesbitt/Carbon) gibi bir şey ya da [Behat](https://github.com/Behat/Behat) gibi tam bir BDD test framework'ı olabilir.

Farklı paket türleri bulunmaktadır. Bazı paketler kendi başınadır, yani sadece Laravel değil herhangi bir framework ile çalışırlar: Carbon ve Behat her ikisi de bu tür stand-alone paket örnekleridir. Bu paketler sadece `composer.json` dosyasında istek yapılmak suretiyle Laravel'le kullanılabilmektedir.

Öte yandan, diğer bazı paketler özellikle Laravel ile kullanım için tasarlanmıştır. Önceki Laravel sürümlerinde, bu tip paketlere "bundle" deniyordu. Bu paketlerde özellikle bir Laravel uygulamasını güçlendirmeyi amaçlamış rotalar, denetçiler (controllers), görünümler, yapılandırmalar ve migrasyonlar olabilir. Kendi başına türde bir paket geliştirmek için gerekli özel bir süreç olmadığı için, bu kılavuz esas itibarıyla Laravel'e özgü olanların geliştirilmesini kapsamaktadır.

Tüm Laravel paketleri [Packagist](http://packagist.org) ve [Composer](http://getcomposer.org) aracılığıyla dağıtılır, bu yüzden bu harika PHP paket dağıtım araçlarını öğrenmek esastır.

<a name="creating-a-package"></a>
## Bir Paket Oluşturma

Laravel'le kullanmak üzere yeni bir paket oluşturmanın en kolay yolu `workbench` Artisan komutudur. Öncelikle, `app/config/workbench.php` dosyasında birkaç seçeneği ayarlamanız gerekiyor. Bu dosyada, bir `name` ve `email` seçeneği bulacaksınız. Bu değerler sizin yeni paketiniz için bir `composer.json` dosyası üretmekte kullanılacaktır. Bu değerleri girdikten sonra, bir tezgah (workbench) paketi oluşturmaya hazırsınız!

**Workbench Artisan Komutunun Verilmesi**

	php artisan workbench satıcıadı/paketadı --resources

Satıcıadı sizin paketinizi farklı yazarlardan gelen aynı isimli diğer paketlerden ayırt etmenin bir yoludur. Örneğin ben (Taylor Otwell) "Zapper" adında yeni bir paket oluşturacaksam, satıcıadı `Taylor`, paketadı ise `Zapper` olacaktır. Ön tanımlı olarak, bu workbench komutu framework bilinemez paketler oluşturur; ancak, `resources` komutu workbench'e `migrations`, `views`, `config` ve bunlar gibi Laravel'e özgü dizinleri olan paketler üretmesini söyler.

`workbench` komutu çalıştırıldıktan sonra sizin paketiniz Laravel kurulumunuzun `workbench` dizini içerisinde hazırlanmış olacaktır. Daha sonra, paketiniz için oluşturulmuş olan `ServiceProvider`'i kayda geçireceksiniz. Bu hizmet sağlayıcının adını `app/config/app.php` dosyasındaki `providers` dizisine ekleyerek kayda geçirebilirsiniz. Bu, Laravel'e uygulamanız başladığı zaman sizin paketinizi yüklemesi talimatı verecektir. Hizmet sağlayıcıları `[Paket]ServiceProvider` şeklinde bir isimlendirme geleneği kullanırlar. Öyleyse, yukarıdaki örnek için `providers` dizisine `Taylor\Zapper\ZapperServiceProvider` ekleyeceğiz.

Sağlayıcıyı kayda geçirdikten sonra artık paketinizi geliştirmeye başlayabilirsiniz! Bununla birlikte, bu konuya geçmeden önce, paket yapısı ve geliştirme iş akışını daha yakından tanımak için aşağıdaki kesimleri gözden geçirmenizde yarar var.

<a name="package-structure"></a>
## Paket Yapısı

`workbench` komutu kullanılırken, paketiniz, paketinizin Laravel frameworkün diğer kısımlarıyla iyi bütünleşmesine imkan veren geleneklerle kurulur:

**Temel Paket Dizin Yapısı**

	/src
		/Satici
			/Paket
				PaketServiceProvider.php
		/config
		/lang
		/migrations
		/views
	/tests
	/public

Bu yapıyı biraz daha açalım. Buradaki `src/Satici/Paket` dizini sizin paketinizin `ServiceProvider` de dahil olmak üzere tüm sınıflarının evidir. `config`, `lang`, `migrations` ve `views` dizinleri ise, tahmin edebileceğiniz gibi paketinizdeki kaynakların kendilerine tekabül edenlerini içermektedir. Paketlerde, tıpkı "normal" uygulamalarda olduğu gibi bu kaynaklardan birileri olabilir.

<a name="service-providers"></a>
## Hizmet Sağlayıcıları

Hizmet sağlayıcıları paketleriniz için tamamen önceden yükleme (bootstrap) sınıflarıdır. Ön tanımlı olarak bunlar iki metod taşırlar: `boot` ve `register`. Bu metodların içerisinde, istediğiniz her şeyi yapabilirsiniz: bir rota dosyası dahil etmek, IoC konteynerinde bağlayıcı kayda geçirmek, olaylara tutturmak veya istediğiniz daha başka bir şey.

Bunlardan `register` metodu, hizmet sağlayıcı kayıt edilir edilmez çağrılır, `boot` komutu ise sadece bir istek yönlendirilmeden önce çağrılır. Bu nedenle, eğer sizin hizmet sağlayıcınızdaki eylemler, zaten kaydı yapılmış başka bir hizmet sağlayıcısına dayanıyorsa veya başka bir sağlayıcı tarafından bağlanan hizmetleri geçersiz bırakıyorsanız, `boot` metodunu kullanmalısınız.

`workbench` kullanarak bir paket oluşturulurken, `boot` komutu zaten bir eylem içerir:

	$this->package('satici/paket');

Bu metod Laravel'in uygulamanız için görünüm, konfigürasyon ve diğer kaynakları nasıl düzgünce yükleyeceğini bilmesine imkan verir. Genelde, paket kurulumunu workbench gelenekleri kullanarak yapacağı için bu kod satırını değiştirmenin bir gereği yoktur.

<a name="package-conventions"></a>
## Paket Gelenekleri

Bir paketten gelen kaynaklar kullanılırken, örneğin yapılandırma öğeleri veya görünümler için genelde çift iki nokta üst üste söz dizimi kullanılır:

**Bir Paketteki Bir Görünümü Yükleme**

	return View::make('package::gorunum.isim');

**Bir Paket Yapılandırma Öğesinin Öğrenilmesi**

	return Config::get('package::grup.secenek');

> **Not:** Eğer paketinizde migrasyonlar varsa, sınıf adının başka paketlerle olası sınıf adı çatışmalarını önlemek amacıyla migrasyon isimlerine paketinizin adını ön ek vermeyi düşünün.

<a name="development-workflow"></a>
## Geliştirme İş Akışı

Bir paket geliştirirken bir uygulama kapsamı içerisinde geliştiriyor olabilmek yararlı olur ve size kolaylıkla görmek ve şablonlarınızla denemek ve benzeri imkanlar verir. Bu nedenle, bu işe başlarken Laravel'in yeni bir kopyasını yükleyin, sonra da paket yapınızı oluşturmak için `workbench` komutunu kullanın.

`workbench` komutunun paketinizi oluşturmasından sonra, `workbench/[satici]/[paket]` dizininden `git init` yapabilir ve paketinizi doğrudan workbench'tan `git push` yapabilirsiniz! Bu size sürekli `composer update` komutlarıyla batağa saplanmaksızın bir uygulama bağlamında uygun bir şekilde paket geliştirmenize imkan verecektir.

Sizin paketleriniz `workbench` dizininde olduğundan, Composer'in sizin paketinizin dosyalarını otomatik yüklemeyi nereden bileceğini merak ediyor olabilirsiniz. Bu `workbench` dizini mevcut olduğu zaman, Laravel akıllı bir şekilde paket var mı diye bu dizini tarayacak, uygulama başladığında bunların Composer autoload dosyalarını yükleyecektir!

Eğer paketinizin autoload dosyalarını tekrar üretmeniz gerekirse, `php artisan dump-autoload` komutunu kullanabilirsiniz. Bu komut, sizin kök projenizdekiler yanında, oluşturmuş olduğunuz workbench'lerdeki autoload dosyalarını da tekrardan üretecektir.

**Artisan Autoload Komutunun Çalıştırılması**

	php artisan dump-autoload

<a name="package-routing"></a>
## Paket Yönlendirme (Routing)

Laravel'in önceki sürümlerinde, bir paketin hangi URI'lere cevap vereceğini belirtmek için `handles` cümleciği kullanılırdı. Ancak, Laravel 4'te, bir paket her URI'ye cevap verebilir. Paketiniz için bir rota dosyasını yüklemek için, hizmet sağlayıcınızın `boot` metodu içerisinde onu `include` etmeniz yeterlidir.

**Bir Hizmet Sağlayıcısından Bir Rota Dosyasının Dahil Edilmesi**

	public function boot()
	{
		$this->package('satici/paket');

		include __DIR__.'/../../routes.php';
	}

> **Not:** Şayet paketiniz denetçiler (controllers) kullanıyorsa, bunların sizin `composer.json` dosyanızın auto-load kesiminde düzgün bir şekilde yapılandırılmış olduğundan emin olun.

<a name="package-configuration"></a>
## Paket Yapılandırması

Bazı paketler yapılandırma dosyaları gerektirebilir. Bu dosyalar tipik uygulama yapılandırma dosyalarıyla aynı şekilde tanımlanmalıdır. Ve, hizmet sağlayıcınızda kaynakları kayda geçirmede ön tanımlı `$this->package` metodunu kullanıyorken, olağan "çift iki nokta üst üste" söz dizimini kullanarak erişebilirsiniz:

**Paket Yapılandırma Dosyalarına Erişme**

	Config::get('paket::dosya.secenek');

Ancak eğer paketiniz tek bir yapılandırma dosyası içeriyorsa, adına sadece `config.php` diyebilirsiniz. Böyle yapmışsanız, dosya adını belirtmenize gerek kalmadan seçeneklere doğrudan erişebilirsiniz:

**Tek Dosyalı Paket Yapılandırmasına Erişme**

	Config::get('paket::secenek');

Bazen, görünümler gibi paket kaynaklarınızı tipik `$this->package` metodundan başka türlü kayda geçirmek isteyebilirsiniz. Tipik olarak bu sadece kaynaklar konvansiyonel bir yerleşimde olmadıkları takdirde yapılacaktır. Bu kaynakları elle kayda geçirmek için `View`, `Lang` ve `Config` sınıflarının `addNamespace` metodunu kullanabilirsiniz:

**Bir Kaynak Aduzayının Elle Kayda Geçirilmesi**

	View::addNamespace('paket', __DIR__.'/path/to/views');

Aduzayı kayda geçirildikten sonra, kaynağa erişmek için aduzayının adını ve "çift iki nokta üst üste" söz dizimini kullanabilirsiniz:

	return View::make('paket::view.isim');

`View`, `Lang` ve `Config` sınıflarında `addNamespace` için metod biçimi aynıdır.

### Basamaklı Yapılandırma Dosyaları

Diğer geliştiriciler sizin paketlerinizi yükledikleri zaman yapılandırma seçeneklerinden bir kısmını geçersiz kılmak ve değiştirmek isteyebilirler. Ancak, eğer sizin paket kaynak kodunuzdaki değerleri değiştirirlerse, Composer'in daha sonraki paket güncellemesinde bunun üzerine yazılacaktır, tekrar sizin yazdığınız hale gelecektir. O yüzden, bunun yerine `config:publish` artisan komutu kullanılmalıdır:

**Config Publish Komutunun Çalıştırılması**

	php artisan config:publish satici/paket

Bu komut çalıştırıldığında, sizin uygulamanız için olan konfigürasyon dosyaları `app/config/packages/satici/paket` dizinine kopyalanacak, burada geliştiriciler tarafından güvenle değiştirilebilecektir!

> **Not:** Geliştiriciler ayrıca onları `app/config/packages/satici/paket/environment`'e koyarak sizin paketiniz için ortama özgü yapılandırma dosyaları da oluşturabilirler.

<a name="package-migrations"></a>
## Paket Migrasyonları

Paketleriniz için kolayca migrasyon oluşturabilir ve çalıştırabilirsiniz. workbench'de bir paket için bir migrasyon oluşturmak için `--bench` seçeneğini kullanın:

**Workbench Paketleri İçin Migrasyon Oluşturulması**

	php artisan migrate:make create_users_table --bench="satici/paket"

**Workbench Paketleri İçin Migrasyonların Çalıştırılması**

	php artisan migrate --bench="satici/paket"

`vendor` dizinine Composer tarafından yüklenmiş bitmiş bir paket için migrasyonlar çalıştırmak için `--package` yönergesini kullanabilirsiniz:

**Yüklenmiş Bir Paket İçin Migrasyonların Çalıştırılması**

	php artisan migrate --package="satici/paket"

<a name="package-assets"></a>
## Paket Varlıkları

Bazı paketlerde JavaScript, CSS ve resimler gibi varlıklar olabilir. Ancak biz `satici` veya `workbench` dizinlerinde varlıklara bağlanamayız, öyleyse bu varlıkları uygulamamızın `public` dizinine taşıyacak bir yola ihtiyacımız var. Sizin için bununla `asset:publish` komutu ilgilenecektir:

**Paket Varlıklarının Public Dizinine Taşınması**

	php artisan asset:publish

	php artisan asset:publish satici/paket

Eğer paket hala `workbench`'de ise, `--bench` yönergesini kullanın:

	php artisan asset:publish --bench="satici/paket"

Bu komut varlıkları satıcı ve paket ismine göre `public/packages` dizinine taşıyacaktır. Yani, `userscape/kudos` adındaki bir paket kendi varlıklarını `public/packages/userscape/kudos` dizinine taşıyacaktır. Bu varlık yayımlama geleneğinin kullanılması, kendi paketlerinizin görünümlerinde varlık path'lerini güvenle kodlamanıza imkan verir.

<a name="publishing-packages"></a>
## Paketlerin Yayımlanması

Paketiniz yayımlanmaya hazır olduğunda, paketi [Packagist](http://packagist.org) ambarına yollayacaksınız. Eğer paketiniz Laravel'e özgü ise, paketinizin `composer.json` dosyasına bir `laravel` etiketi eklemeyi düşünün.

Ayrıca, geliştiriciler kendi `composer.json` dosyalarında sizin paketinize istek yaptıklarında stabil sürümlere bağlı olabilmeleri için sürümlerinizi de etiketlemeniz hoş ve yardımcı olacaktır. Şayet stabil bir sürüm hazır değilse, `branch-alias` Composer direktifini kullanmayı düşünün.

Paketinizi yayımladıktan sonra, `workbench` tarafından oluşturulan uygulama bağlamı içinde onu geliştirmeye devam etmekte özgürsünüz. Bu, paketinizi yayımladıktan sonra bile rahat bir şekilde geliştirmek için muazzam bir yoldur.

Bazı kuruluşlar kendi geliştiricileri için paketlerini kendi özel ambarlarında barındırmayı tercih ediyorlar. Siz de böyle yapmayı düşünürseniz, Composer ekibi tarafından sağlanan [Satis](http://github.com/composer/satis) belgelerini inceleyin.
