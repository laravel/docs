# Unit Testing

- [Giriş](#introduction)
- [Testleri Tanımlamak ve Çalıştırmak](#defining-and-running-tests)
- [Test Ortamı](#test-environment)
- [Testlerin İçerisinde Rotaları Çağırmak](#calling-routes-from-tests)
- [Facade'ları Taklit Etmek](#mocking-facades)
- [Laravel'e Özel `Assert` Metodları](#framework-assertions)
- [Yardımcı Metodlar](#helper-methods)

<a name="introduction"></a>
## Giriş

Laravel hazırlanırken birim testler ile hazırlandı. Açıkçası, PHPUnit ile test desteği halihazırda var ve uygulamanız için hazırlanmış `phpunit.xml` dosyası da Laravel ile birlikte geliyor. PHPUnit'in haricinde, Laravel ayrıca Symfony HttpKernel, DomCrawler ve BrowserKit bileşenlerinden de yararlanıyor ki, kullanıcılar testler sırasında görünümleri inceleyebilsin ve müdahale edebilsin. Bu bileşenler ile temsili bir tarayıcıya sahip oluyorsunuz.

Örnek bir test dosyası `app/tests` dizininde bulunmaktadır. Yeni bir Laravel uygulaması kurulumundan sonra, komut satırında `phpunit` komutuyla testlerinizi çalıştırabilirsiniz.

<a name="defining-and-running-tests"></a>
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

<a name="test-environment"></a>
## Test Ortamı

Testleri çalıştırıken, Laravel otomatik olarak ortam yapılandırmasını `testint`'a alacaktır. Ayrıca, Laravel'de test ortamında `kaşe` ve `oturum` için özel ayar dosyaları bulunmaktadır. İki sürücü de bir `dizi` olacak şekilde ayarlanmış olup, test yaparkenki oturum ve kaşe verilerinin kalıcı olmaması sağlanmıştır. Test ortamı için gerektiğinde başka ayarlar yapmakta özgürsünüz.

<a name="calling-routes-from-tests"></a>
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

We can mock the call to the `Event` class by using the `shouldReceive` method on the facade, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock.

**Mocking A Facade**

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with(array('name' => 'Dayle'));

		$this->call('GET', '/');
	}

> **Note:** You should not mock the `Request` facade. Instead, pass the input you desire into the `call` method when running your test.

<a name="framework-assertions"></a>
## Laravel'e Özel `Assert` Metodları

Laravel ships with several `assert` methods to make testing a little easier:

**Asserting Responses Are OK**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

**Asserting Response Statuses**

	$this->assertResponseStatus(403);

**Asserting Responses Are Redirects**

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

**Asserting A View Has Some Data**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

**Asserting The Session Has Some Data**

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

<a name="helper-methods"></a>
## Yardımcı Metodlar

The `TestCase` class contains several helper methods to make testing your application easier.

You may set the currently authenticated user using the `be` method:

**Setting The Currently Authenticated User**

	$user = new User(array('name' => 'John'));

	$this->be($user);

You may re-seed your database from a test using the `seed` method:

**Re-Seeding Database From Tests**

	$this->seed();

	$this->seed($connection);

More information on creating seeds may be found in the [migrations and seeding](/docs/migrations#database-seeding) section of the documentation.
