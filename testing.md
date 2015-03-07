# 測試

- [介紹](#introduction)
- [定義並執行測試](#defining-and-running-tests)
- [測試環境](#test-environment)
- [從測試呼叫路由](#calling-routes-from-tests)
- [模擬 Facades](#mocking-facades)
- [框架斷言](#framework-assertions)
- [輔助方法](#helper-methods)
- [重置應用程式](#refreshing-the-application)

<a name="introduction"></a>
## 介紹

Laravel 在建立時就已考慮到單元測試。事實上，預設上就支援以 PHPUnit 做測試，而且已經為你的應用程式建立了 `phpunit.xml` 檔案。

在 `tests` 資料夾有提供一個測試範例。在安裝新 Laravel 應用程式之後，只要在命令列上執行 `phpunit`，就可以進行測試。

<a name="defining-and-running-tests"></a>
## 定義並執行測試

要建立一個測試案例，只要在 `tests` 目錄下建立新的測試檔案。測試類別必須繼承 `TestCase`，接著就可以向平常使用 PHPUnit 一樣定義測試方法。

#### 測試類別範例

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

你可以從終端機執行 `phpunit` 命令來執行應用程式的所有測試。

> **注意:**如果你定義了自己的 `setUp` 方法，記得在裡面呼叫 `parent::setUp`。

<a name="test-environment"></a>
## 測試環境

當執行單元測試的時候，Laravel 會自動將環境設置成 `testing`。另外 Laravel 會匯入 `session` 和 `cache` 的測試設定。在測試環境裡，這兩個驅動會被設定為 `array`，代表測試時 session 或 cache 的資料不會被保留。你可以視情況建立需要的測試環境設定。

`testing` 環境的變數可以在 `phpunit.xml` 檔案中設定。

<a name="calling-routes-from-tests"></a>
## 從測試呼叫路由

#### 在測試中呼叫路由

你可以使用 `call` 方法，輕易地呼叫你的任何一個路由來測試：

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $cookies, $files, $server, $content);

接著你可以檢查 `Illuminate\Http\Response` 物件：

	$this->assertEquals('Hello World', $response->getContent());

#### 在測試中呼叫控制器

你也可以呼叫控制器進行測試：

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', ['user' => 1]);

> **注意:**使用 `action` 方法的時候，不需要指定完整的控制器命名空間。只需要指定 `App\Http\Controllers` 命名空間後面的類別名稱部分。

`getContent` 方法會回傳求值後的字串內容回應。如果你的路由回傳一個 `View`，你可以透過 `original` 屬性取得：

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

也可以使用 `callSecure` 方法呼叫 HTTPS 路由：

	$response = $this->callSecure('GET', 'foo/bar');

<a name="mocking-facades"></a>
## 模擬 Facades

測試的時候，你或許常會想要模擬 Laravel 靜態 facade 呼叫。舉個例子，思考下面的控制器動作：

	public function getIndex()
	{
		Event::fire('foo', ['name' => 'Dayle']);

		return 'All done!';
	}

我們可以在 facade 上使用 `shouldReceive` 方法，來模擬呼叫 `Event` 類別，它將會回傳一個 [Mockery](https://github.com/padraic/mockery) 實例。

#### 模擬 Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', ['name' => 'Dayle']);

		$this->call('GET', '/');
	}

> **注意:**你不應該模擬 `Request` facade，而是傳入想要的資料到 `call` 方法來執行測試時。

<a name="framework-assertions"></a>
## 框架斷言

Laravel 附帶幾個 `assert` 方法，讓測試更簡單一點：

#### 斷言回應 OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### 斷言回應狀態碼

	$this->assertResponseStatus(403);

#### 斷言回應為重導向

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### 斷言回應的視圖包含一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### 斷言 Session 包含一些資料

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### 斷言 Session 有錯誤資訊

    public function testMethod()
    {
        $this->call('GET', '/');

        $this->assertSessionHasErrors();

        // 斷言 session 有特定鍵值的錯誤資訊...
        $this->assertSessionHasErrors('name');

        // 斷言 session 有數個特定鍵值的錯誤資訊...
        $this->assertSessionHasErrors(['name', 'age']);
    }

#### 斷言舊輸入有一些資料

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

#### 設定一個通過身份驗證的使用者

你可以使用 `be` 方法設定一個通過身份驗證的使用者：

	$user = new User(['name' => 'John']);

	$this->be($user);

你可以在測試時使用 `seed` 方法重新填充資料庫：

#### 在測試時重新填充資料庫

	$this->seed();

	$this->seed($connection);

更多建立填充資料的資訊，可以在文件的[遷移與資料填充](/docs/5.0/migrations#database-seeding)部分找到。

<a name="refreshing-the-application"></a>
## 重置應用程式

你可能已經知道，你可以透過 `$this->app` 在任何測試方法中存取應用程式 ([服務容器](/docs/5.0/container))。這個應用程式物件實例會在每個測試類別被重置。如果你希望在某個方法中手動強制重置應用程式，可以在測試方法中使用 `refreshApplication` 方法。這將會重置任何額外的綁定，例如那些從測試案例執行開始被放到 IoC 容器的 mock。
