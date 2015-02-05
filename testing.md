# 測試

- [介紹](#introduction)
- [定義並執行測試](#defining-and-running-tests)
- [測試環境](#test-environment)
- [從測試呼叫路由](#calling-routes-from-tests)
- [模擬 Facades](#mocking-facades)
- [框架 Assertions](#framework-assertions)
- [輔助方法](#helper-methods)
- [重置應用程式](#refreshing-the-application)

<a name="introduction"></a>
## 介紹

Laravel 在建立時就有考慮到單元測試。事實上，它支援立即使用被引入的 PHPUnit 做測試，而且已經為你的應用程式建立了 `phpunit.xml` 檔案。

在 `tests` 資料夾有提供一個測試範例。在安裝新 Laravel 應用程式之後，只要在命令列上執行 `phpunit` 來進行測試流程。

<a name="defining-and-running-tests"></a>
## 定義並執行測試

要建立一個測試案例，只要在 `tests` 資料夾建立新的測試檔案。測試類別必須繼承自 `TestCase`，接著你可以如你平常使用 PHPUnit 一般去定義測試方法。

#### 測試類別範例

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

你可以從終端機執行 `phpunit` 命令來執行應用程式的所有測試。

> **注意:** 如果你定義自己的 `setUp` 方法， 請記得呼叫 `parent::setUp`。

<a name="test-environment"></a>
## 測試環境

當執行單元測試的時候，Laravel 會自動將環境設置成 `testing`。另外 Laravel 會在測試環境匯入 `session` 和 `cache` 的設定檔案。當在測試環境裡這兩個驅動會被設定為 `array` (空陣列)，代表在測試的時候沒有 session 或 cache 資料將會被保留。視情況你可以任意的建立你需要的測試環境設定。

`testing` 環境的變數可以在 `phpunit.xml` 檔案中設定。

<a name="calling-routes-from-tests"></a>
## 從測試呼叫路由

#### 從單一測試中呼叫路由

你可以使用 `call` 方法，輕易地呼叫你的任何一個路由來測試：

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

接著你可以檢查 `Illuminate\Http\Response` 物件：

	$this->assertEquals('Hello World', $response->getContent());

#### 從測試呼叫控制器

你也可以從測試呼叫控制器：

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', array('user' => 1));

> **注意:** 當使用 `action` 方法的時候，你不需要指定完整的控制器命名空間。只需要指定 `App\Http\Controllers` 命名空間後面的類別名稱部分。

`getContent` 方法會回傳求值後的字串內容回應。如果你的路由回傳一個 `View`，你可以透過 `original` 屬性存取它：

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

你可以使用 `callSecure` 方法去呼叫 HTTPS 路由：

	$response = $this->callSecure('GET', 'foo/bar');

<a name="mocking-facades"></a>
## 模擬 Facades

當測試的時候，你或許常會想要模擬呼叫 Laravel 靜態 facade。舉個例子，思考下面的控制器行為：

	public function getIndex()
	{
		Event::fire('foo', ['name' => 'Dayle']);

		return 'All done!';
	}

我們可以在 facade 上使用 `shouldReceive` 方法，來模擬呼叫 `Event` 類別，它將會回傳一個 [Mockery](https://github.com/padraic/mockery) mock 物件實例。

#### 模擬 Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', ['name' => 'Dayle']);

		$this->call('GET', '/');
	}

> **注意:** 你不應該模擬 `Request` facade。取而代之，當執行你的測試，傳遞想要的輸入資料進去 `call` 方法。

<a name="framework-assertions"></a>
## 框架 Assertions

Laravel 附帶幾個 `assert` 方法，讓測試更簡單一點：

#### Assert 回應為 OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### Assert 回應的狀態碼

	$this->assertResponseStatus(403);

#### Assert 回應為重導向

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### Assert 回應的視圖包含一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### Assert Session 包含一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### Assert Session 有錯誤資訊

    public function testMethod()
    {
        $this->call('GET', '/');

        $this->assertSessionHasErrors();

        // Asserting the session has errors for a given key...
        $this->assertSessionHasErrors('name');

        // Asserting the session has errors for several keys...
        $this->assertSessionHasErrors(array('name', 'age'));
    }

#### Assert 舊輸入內容有一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertHasOldInput();
	}

<a name="helper-methods"></a>
## 輔助方法

`TestCase` 類別包含幾個輔助方法讓應用程式的測試更為簡單。

#### 從測試裡設定和刷新 Sessions

	$this->session(['foo' => 'bar']);

	$this->flushSession();

#### 設定目前為通過身份驗證的使用者

你可以使用 `be` 方法設定目前為通過身份驗證的使用者：

	$user = new User(array('name' => 'John'));

	$this->be($user);

你可以從測試中使用 `seed` 方法重新填充你的資料庫：

#### 在測試中重新填充資料庫

	$this->seed();

	$this->seed($connection);

更多建立填充資料的資訊可以在文件的 [遷移與資料填充](/docs/migrations#database-seeding) 部分找到。

<a name="refreshing-the-application"></a>
## 重置應用程式

你可能已經知道，你可以透過 `$this->app` 在任何測試方法中存取你的 Laravel `應用程式本體` / IoC 容器。這個應用程式物件實例會在每個測試類別被重置。如果你希望在給定的方法手動強制重置應用程式，你可以從你的測試方法使用 `refreshApplication` 方法。這將會重置任何額外的綁定，例如那些從測試案例執行開始被放到 IoC 容器的 mocks。
