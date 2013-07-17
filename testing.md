# Unit Testing

- [Giriş](#giris)
- [Testleri Tanımlamak ve Çalıştırmak](#testleri-tanimlamak-ve-calistirmak)
- [Test Ortamı](#test-ortami)
- [Testlerin İçerisinde Rotaları Çağırmak](#testlerin-icerisinde-rotalari-cagirmak)
- [Facade'ları Taklit Etmek](#mocking-facades)
- [Laravel'e Özel `Assert` Metodları](#laravele-ozel-assert-metodlari)
- [Yardımcı Metodlar](#yardimci-metodlar)

<a name="giris"></a>
## Giriş

Laravel hazırlanırken birim testler ile hazırlandı. Açıkçası, PHPUnit ile test desteği halihazırda var ve uygulamanız için hazırlanmış `phpunit.xml` dosyası da Laravel ile birlikte geliyor. PHPUnit'in haricinde, Laravel ayrıca Symfony HttpKernel, DomCrawler ve BrowserKit bileşenlerinden de yararlanıyor ki, kullanıcılar testler sırasında görünümleri inceleyebilsin ve müdahale edebilsin. Bu bileşenler ile temsili bir tarayıcıya sahip oluyorsunuz.

Örnek bir test dosyası `app/tests` dizininde bulunmaktadır. Yeni bir Laravel uygulaması kurulumundan sonra, komut satırında `phpunit` komutuyla testlerinizi çalıştırabilirsiniz.

<a name="testleri-tanimlamak-ve-calistirmak"></a>
## Testleri Tanımlamak ve Çalıştırmak

Yeni bir test durumu oluşturmak için, `app/test` dizini içerisinde yeni bir test dosyası oluşturmanız yeterli. Test sınıflarınız `TestCase` sınıfını extend ediyor olmalıdır. Bu şekilde normalde PHPUnit ile hazırladığınız test metodlarını aynı şekilde oluşturabilirsiniz.

**Örnek Bir Test Sınıfı**

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

Daha sonra komut satırında `phpunit` ile uygulamanızın tüm testlerini çalıştırabilirsiniz.

> **Not:** Eğer kendi `setUp` methodunuzu tanımlarsanız, `parent::setUp` kodunu çalıştırdığınızdan emin olun.

<a name="test-ortami"></a>
## Test Ortamı

Testleri çalıştırıken, Laravel otomatik olarak ortam yapılandırmasını `testing`'e alacaktır. Ayrıca, Laravel'de test ortamında `kaşe` ve `oturum` için özel ayar dosyaları bulunmaktadır. İki sürücü de bir `dizi` olacak şekilde ayarlanmış olup, test yaparkenki oturum ve kaşe verilerinin kalıcı olmaması sağlanmıştır. Test ortamı için gerektiğinde başka ayarlar yapmakta özgürsünüz.

<a name="testlerin-icerisinde-rotalari-cagirmak"></a>
## Testlerin İçerisinde Rotaları Çağırmak

Testleriniz içerisinde `call` metodu ile rahatlıkla rotaları çağırabilirsiniz:

**Test Dosyasından Bir Rota Çağırmak**

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

Daha sonra `Illuminate\Http\Response` nesnesini inceleyebilirsiniz:

	$this->assertEquals('Hello World', $response->getContent());

Ayrıca bir test dosyasından denetçileri de çağırabilirsiniz:

**Test Dosyasından Bir Denetçi Çağırmak**

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', array('user' => 1));

`getContent` metodu, hazırlanmış döngünün içeriğini döndürecektir. Eğer rotanız bir `Görünüm` döndürüyorsa, `original` özelliği ile buna ulaşabilirsiniz: 

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

Bir HTTPS rotayı çağırmak için, `callSecure` metodunu kullanabilirsiniz.

	$response = $this->callSecure('GET', 'foo/bar');

### DOM Böceği

Ayrıca bir rota çağırıp, bir DOM Böceği nesnesi alarak içeriği inceleyebilirsiniz:

	$crawler = $this->client->request('GET', '/');

	$this->assertTrue($this->client->getResponse()->isOk());

	$this->assertCount(1, $crawler->filter('h1:contains("Hello World!")'));

Böceği nasıl kullanacağınız hakkında detaylı bilgi için [kendi dökümantasyonunu](http://symfony.com/doc/master/components/dom_crawler.html) okuyabilirsiniz.

<a name="mocking-facades"></a>
## Facade'ları Taklit Etmek

Test yaparken, sabit Laravel facadelarını taklit etmeniz gerekecektir. Örneğin, şu denetçi aksiyonunu varsayalım:

	public function getIndex()
	{
		Event::fire('foo', array('name' => 'Dayle'));

		return 'All done!';
	}

`Event` sınıfına yapılan çağrıyı taklit edebilmek için Facade üzerinde `shouldReceive` metodunu kullanabilirsiniz, bu metod bir [Mockery](https://github.com/padraic/mockery) örneği döndürecek.

**Bir Facade'ı Taklit Etmek**

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with(array('name' => 'Dayle'));

		$this->call('GET', '/');
	}

> **Note:** `Request` metodunu taklit etmemelisiniz. Bunun yerine, testlerinizi çalıştırırken istediğiniz girdileri `call` metodunda belirtin.

<a name="laravele-ozel-assert-metodlari"></a>
## Laravel'e Özel `Assert` Metodları

Laravel test yapımını kolaylaştırmak için halihazırda bazı `assert` meodlarıyla gelir:

**Yanıtın Başarıyla Geldiği İspatlamak**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

**Yanıt Kodlarını İspatlamak**

	$this->assertResponseStatus(403);

**Yanıtın Bir Yönlendirme Olduğunu İspatlamak**

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

**Görünüme Bir Verinin Gitmediğini İspatlamak**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

**Oturumda Bir Verinin Kayıtlı Olduğunu İspatlamak**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

<a name="yardimci-metodlar"></a>
## Yardımcı Metodlar

Test yapımını kolaylaştırmak için `TestCase` sınıfı bazı yardımcı metodlarla birlikte gelir.

Mevcut oturum açmış kullanıcıyı `be` metodu ile belirleyebilirsiniz.

**Oturum Açmış Kullanıcıyı Belirleme**

	$user = new User(array('name' => 'John'));

	$this->be($user);

Bir test içerisinden `seed` metoduyla veritabanınızı yeniden filizlendirebilirsiniz:

**Test İçerisinden Veritabanını Yeniden Filizlendirmek**

	$this->seed();

	$this->seed($connection);

Filizlendirmeyle ilgili daha fazla bilgiyi dökümantasyonun [migrations and seeding](/docs/migrations#database-seeding) bölümünde bulabilirsiniz.