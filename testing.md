# 测试

- [介绍](#introduction)
- [定义并执行测试](#defining-and-running-tests)
- [测试环境](#test-environment)
- [从测试调用路由](#calling-routes-from-tests)
- [仿真 Facades](#mocking-facades)
- [框架 Assertions](#framework-assertions)
- [辅助方法](#helper-methods)
- [重置应用程序](#refreshing-the-application)

<a name="introduction"></a>
## 介绍

Laravel 在建立时就有考虑到单元测试。事实上，它支持立即使用被引入的 PHPUnit 做测试，而且已经为你的应用程序建立了 `phpunit.xml` 文件。

在 `tests` 文件夹有提供一个测试范例。在安装新 Laravel 应用程序之后，只要在命令行上执行 `phpunit` 来进行测试流程。

<a name="defining-and-running-tests"></a>
## 定义并执行测试

要建立一个测试案例，只要在 `tests` 文件夹建立新的测试文件。测试类别必须继承自 `TestCase`，接着你可以如你平常使用 PHPUnit 一般去定义测试方法。

#### 测试类别范例

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

你可以从终端机执行 `phpunit` 命令来执行应用程序的所有测试。

> **注意:** 如果你定义自己的 `setUp` 方法， 请记得调用 `parent::setUp`。

<a name="test-environment"></a>
## 测试环境

当执行单元测试的时候，Laravel 会自动将环境设置成 `testing`。另外 Laravel 会在测试环境导入 `session` 和 `cache` 的设置文件。当在测试环境里这两个驱动会被设置为 `array` (空数组)，代表在测试的时候没有 session 或 cache 数据将会被保留。视情况你可以任意的建立你需要的测试环境设置。

`testing` 环境的变量可以在 `phpunit.xml` 文件中设置。

<a name="calling-routes-from-tests"></a>
## 从测试调用路由

#### 从单一测试中调用路由

你可以使用 `call` 方法，轻易地调用你的任何一个路由来测试：

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

接着你可以检查 `Illuminate\Http\Response` 对象：

	$this->assertEquals('Hello World', $response->getContent());

#### 从测试调用控制器

你也可以从测试调用控制器：

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', array('user' => 1));

> **注意:** 当使用 `action` 方法的时候，你不需要指定完整的控制器命名空间。只需要指定 `App\Http\Controllers` 命名空间后面的类别名称部分。

`getContent` 方法会回传求值后的字串内容回应。如果你的路由回传一个 `View`，你可以透过 `original` 属性访问它：

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

你可以使用 `callSecure` 方法去调用 HTTPS 路由：

	$response = $this->callSecure('GET', 'foo/bar');

<a name="mocking-facades"></a>
## 仿真 Facades

当测试的时候，你或许常会想要仿真调用 Laravel 静态 facade。举个例子，思考下面的控制器行为：

	public function getIndex()
	{
		Event::fire('foo', ['name' => 'Dayle']);

		return 'All done!';
	}

我们可以在 facade 上使用 `shouldReceive` 方法，来仿真调用 `Event` 类别，它将会回传一个 [Mockery](https://github.com/padraic/mockery) mock 对象实例。

#### 仿真 Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', ['name' => 'Dayle']);

		$this->call('GET', '/');
	}

> **注意:** 你不应该仿真 `Request` facade。取而代之，当执行你的测试，传递想要的输入数据进去 `call` 方法。

<a name="framework-assertions"></a>
## 框架 Assertions

Laravel 附带几个 `assert` 方法，让测试更简单一点：

#### Assert 回应为 OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### Assert 回应的状态码

	$this->assertResponseStatus(403);

#### Assert 回应为重导向

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### Assert 回应的视图包含一些数据

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### Assert Session 包含一些数据

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### Assert Session 有错误信息

    public function testMethod()
    {
        $this->call('GET', '/');

        $this->assertSessionHasErrors();

        // Asserting the session has errors for a given key...
        $this->assertSessionHasErrors('name');

        // Asserting the session has errors for several keys...
        $this->assertSessionHasErrors(array('name', 'age'));
    }

#### Assert 旧输入内容有一些数据

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertHasOldInput();
	}

<a name="helper-methods"></a>
## 辅助方法

`TestCase` 类别包含几个辅助方法让应用程序的测试更为简单。

#### 从测试里设置和刷新 Sessions

	$this->session(['foo' => 'bar']);

	$this->flushSession();

#### 设置目前为通过身份验证的用户

你可以使用 `be` 方法设置目前为通过身份验证的用户：

	$user = new User(array('name' => 'John'));

	$this->be($user);

你可以从测试中使用 `seed` 方法重新填充你的数据库：

#### 在测试中重新填充数据库

	$this->seed();

	$this->seed($connection);

更多建立填充数据的信息可以在文档的 [迁移与数据填充](/docs/migrations#database-seeding) 部分找到。

<a name="refreshing-the-application"></a>
## 重置应用程序

你可能已经知道，你可以透过 `$this->app` 在任何测试方法中访问你的 Laravel `应用程序本体` / IoC 容器。这个应用程序对象实例会在每个测试类别被重置。如果你希望在给定的方法手动强制重置应用程序，你可以从你的测试方法使用 `refreshApplication` 方法。这将会重置任何额外的绑定，例如那些从测试案例执行开始被放到 IoC 容器的 mocks。
