# 單元測試

- [介紹](#introduction)
- [定義並執行測試](#defining-and-running-tests)
- [測試環境](#test-environment)
- [從測試呼叫 Routes](#calling-routes-from-tests)
- [模擬 Facades](#mocking-facades)
- [框架 Assertions](#framework-assertions)
- [輔助方法](#helper-methods)
- [重置應用程式](#refreshing-the-application)

<a name="introduction"></a>
## 介紹

Laravel 在建立時就有考慮到單元測試。事實上，它支援立即使用被引入的 PHPUnit 做測試，而且已經為你的應用程式建立了 `phpunit.xml` 檔案。 除了 PHPUnit 以外，Laravel 也利用 Symfony HttpKernel、 DomCrawler 和 BrowserKit 元件讓你在測試的時候，檢查和操作你的 views、模擬網頁瀏覽器。

在 `app/tests` 資料夾有提供一個測試範例。 在安裝新 Laravel 應用程式之後，簡單地在 command line 上執行 `phpunit` 執行你的測試。

<a name="defining-and-running-tests"></a>
## 定義並執行測試

要建立一個測試案例，只要簡單地建立新的測試檔案在 `app/tests` 資料夾。 測試類別必須繼承 `TestCase`，接著你可以像你通常使用 PHPUnit 一般去定義測試方法。

#### 測試類別範例

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

你可以從終端機執行 `phpunit` 命令來執行應用程式的所有測試。

> **Note:** 如果你定義自己的 `setUp` 方法， 請確定呼叫了 `parent::setUp`.

<a name="test-environment"></a>
## 測試環境

當執行單元測試的時候，Laravel 會自動地設定 configuration 環境 為 `testing`。另外, Laravel 會在測試環境匯入 `session` 和 `cache` 的 configuration 檔案。當在測試環境裡這兩個 drivers 會被設定為 `array` (空陣列)，意思是當測試的時候沒有 session 或 cache 資料將會被保留。 有需要你可以自由的建立其他測試環境 configurations。

<a name="calling-routes-from-tests"></a>
## 從測試呼叫 Routes

#### 從測試呼叫 Route

你可以使用 `call` 方法，簡單地呼叫你的其中一個 route 來測試 :

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

接著你可以檢查 `Illuminate\Http\Response` 物件 :

	$this->assertEquals('Hello World', $response->getContent());

#### 從測試呼叫 Controller

你也可以從測試呼叫 controller :

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', array('user' => 1));

`getContent` 方法會回傳求值後的字串內容回應. 如果你的 route 回傳一個 `View`, 你可以使用 `original` 屬性獲取它 :

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

你可以使用 `callSecure` 方法去呼叫 HTTPS route:

	$response = $this->callSecure('GET', 'foo/bar');

> **Note:** 在測試環境中， Route filters 是被禁用的。 如果要啟用它們，必須加 `Route::enableFilters()` 到你的測試.

### DOM Crawler

你也可以呼叫 route 並接受 DOM Crawler 物件實體來檢查內容  :

	$crawler = $this->client->request('GET', '/');

	$this->assertTrue($this->client->getResponse()->isOk());

	$this->assertCount(1, $crawler->filter('h1:contains("Hello World!")'));

如果需要更多如何使用 crawler 的資訊，請參考它的 [官方文件](http://symfony.com/doc/master/components/dom_crawler.html).

<a name="mocking-facades"></a>
## 模擬 Facades

當測試的時候，你或許會時常想要模擬呼叫 Laravel 靜態 facade。 舉個例子，思考下面的 controller action :

	public function getIndex()
	{
		Event::fire('foo', array('name' => 'Dayle'));

		return 'All done!';
	}

我們可以在 facade 上使用 `shouldReceive` 方法，模擬呼叫 `Event` 類別， 它將會回傳一個 [Mockery](https://github.com/padraic/mockery) mock 物件實體.

#### 模擬 Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', array('name' => 'Dayle'));

		$this->call('GET', '/');
	}

> **Note:** 你不應該模擬 `Request` facade。 取而代之，當執行你的測試，傳想要的輸入進去 `call` 方法 .

<a name="framework-assertions"></a>
## 框架 Assertions

Laravel 附帶幾個 `assert` 方法，讓測試更簡單一點:

#### Assert 回應為 OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### Assert 回應狀態碼

	$this->assertResponseStatus(403);

#### Assert 回應為重新導向

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### Assert 回應 View 有一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### Assert 回應 Session 有一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### Assert 回應 Session 有錯誤

    public function testMethod()
    {
        $this->call('GET', '/');

        $this->assertSessionHasErrors();

        // Asserting the session has errors for a given key...
        $this->assertSessionHasErrors('name');

        // Asserting the session has errors for several keys...
        $this->assertSessionHasErrors(array('name', 'age'));
    }

#### Assert 舊輸入有一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertHasOldInput();
	}

<a name="helper-methods"></a>
## 輔助方法

`TestCase` 類別包含幾個輔助方法讓你的應用程式更簡單測試。

#### 從測試設定和刷新 Sessions

	$this->session(['foo' => 'bar']);

	$this->flushSession();

#### 設定目前經過驗證的使用者

你可以使用 `be` 方法設定目前經過驗證的使用者:

	$user = new User(array('name' => 'John'));

	$this->be($user);

你可以從測試使用 `seed` 方法 re-seed 你的資料庫:

#### 從測試 Re-Seeding 資料庫

	$this->seed();

	$this->seed($connection);

更多建立 seeds 的資訊可以在文件的 [migrations and seeding](/docs/migrations#database-seeding) 部分找到.

<a name="refreshing-the-application"></a>
## 重置應用程式

你可能已經知道，你可以借由 `$this->app` 從任何測試方法獲取你的 Laravel `Application` / IoC 容器. 這個應用程式物件實體會在每個測試類別被重置。 如果你希望在給定的方法手動強制應用程式重置，你可以從你的測試方法使用 `refreshApplication` 方法。 這將會重置任何額外的綁定， 例如那些從測試案例執行開始被放倒 IoC 容器的 mocks。
