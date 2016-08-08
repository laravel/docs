# Testing

- [Introduction](#introduction)
- [Defining & Running Tests](#defining-and-running-tests)
- [Test Environment](#test-environment)
- [Calling Routes From Tests](#calling-routes-from-tests)
- [Mocking Facades](#mocking-facades)
- [Framework Assertions](#framework-assertions)
- [Helper Methods](#helper-methods)
- [Refreshing The Application](#refreshing-the-application)

<a name="introduction"></a>
## Introduction

Laravel is built with unit testing in mind. In fact, support for testing with PHPUnit is included out of the box, and a `phpunit.xml` file is already setup for your application.

An example test file is provided in the `tests` directory. After installing a new Laravel application, simply run `phpunit` on the command line to run your tests.

<a name="defining-and-running-tests"></a>
## Defining & Running Tests

To create a test case, simply create a new test file in the `tests` directory. The test class should extend `TestCase`. You may then define test methods as you normally would when using PHPUnit.

#### An Example Test Class

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

You may run all of the tests for your application by executing the `phpunit` command from your terminal.

> **Note:** If you define your own `setUp` method, be sure to call `parent::setUp`.

<a name="test-environment"></a>
## Test Environment

When running unit tests, Laravel will automatically set the configuration environment to `testing`. Also, Laravel includes configuration files for `session` and `cache` in the test environment. Both of these drivers are set to `array` while in the test environment, meaning no session or cache data will be persisted while testing. You are free to create other testing environment configurations as necessary.

The `testing` environment variables may be configured in the `phpunit.xml` file.

<a name="calling-routes-from-tests"></a>
## Calling Routes From Tests

#### Calling A Route From A Test

You may easily call one of your routes for a test using the `call` method:

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $cookies, $files, $server, $content);

You may then inspect the `Illuminate\Http\Response` object:

	$this->assertEquals('Hello World', $response->getContent());

#### Calling A Controller From A Test

You may also call a controller from a test:

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', ['user' => 1]);

> **Note:** You do not need to specify the full controller namespace when using the `action` method. Only specify the portion of the class name that follows the `App\Http\Controllers` namespace.

The `getContent` method will return the evaluated string contents of the response. If your route returns a `View`, you may access it using the `original` property:

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

To call a HTTPS route, you may use the `callSecure` method:

	$response = $this->callSecure('GET', 'foo/bar');

<a name="mocking-facades"></a>
## Mocking Facades

When testing, you may often want to mock a call to a Laravel static facade. For example, consider the following controller action:

	public function getIndex()
	{
		Event::fire('foo', ['name' => 'Dayle']);

		return 'All done!';
	}

We can mock the call to the `Event` class by using the `shouldReceive` method on the facade, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock.

#### Mocking A Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', ['name' => 'Dayle']);

		$this->call('GET', '/');
	}

> **Note:** You should not mock the `Request` facade. Instead, pass the input you desire into the `call` method when running your test.

<a name="framework-assertions"></a>
## Framework Assertions

Laravel ships with several `assert` methods to make testing a little easier:

#### Asserting Responses Are OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### Asserting Response Statuses

	$this->assertResponseStatus(403);

#### Asserting Responses Are Redirects

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### Asserting A View Has Some Data

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### Asserting The Session Has Some Data

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### Asserting The Session Has Errors

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHasErrors();

		// Asserting the session has errors for a given key...
		$this->assertSessionHasErrors('name');

		// Asserting the session has errors for several keys...
 		$this->assertSessionHasErrors(['name', 'age']);
	}

#### Asserting Old Input Has Some Data

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertHasOldInput();
	}

<a name="helper-methods"></a>
## Helper Methods

The `TestCase` class contains several helper methods to make testing your application easier.

#### Setting And Flushing Sessions From Tests

	$this->session(['foo' => 'bar']);

	$this->flushSession();

#### Setting The Currently Authenticated User

You may set the currently authenticated user using the `be` method:

	$user = new User(['name' => 'John']);

	$this->be($user);

#### Re-Seeding Database From Tests

You may re-seed your database from a test using the `seed` method:

	$this->seed();

	$this->seed('DatabaseSeeder');

More information on creating seeds may be found in the [migrations and seeding](/docs/migrations#database-seeding) section of the documentation.

<a name="refreshing-the-application"></a>
## Refreshing The Application

As you may already know, you can access your Application ([service container](/docs/{{version}}/container)) via `$this->app` from any test method. This service container instance is refreshed for each test class. If you wish to manually force the Application to be refreshed for a given method, you may use the `refreshApplication` method from your test method. This will reset any extra bindings, such as mocks, that have been placed in the IoC container since the test case started running.
