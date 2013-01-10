# Unit Testing

- [Introduction](#introduction)
- [Defining & Running Tests](#defining-and-running-tests)
- [Test Environment](#test-environment)
- [Calling Routes From Tests](#calling-routes-from-tests)
- [Helper Methods](#helper-methods)

<a name="introduction"></a>
## Introduction

Laravel is built with unit testing in mind. In fact, support for testing with PHPUnit is included out of the box, and a `phpunit.xml` file is already setup for your application. In addition to PHPUnit, Laravel also utilizes the Symfony HttpKernel, DomCrawler, and BrowserKit components to allow you to inspect and manipulate your views while testing, allowing to simulate a web browser.

An example test file is provided in the `app/tests` directory. After installing a new Laravel application, simply run `phpunit` on the command line to run your tests.

<a name="defining-and-running-tests"></a>
## Defining & Running Tests

To create a test case, simply create a new test file in the `app/tests` directory. The test class should extend `TestCase`. You may then define test methods as you normally would when using PHPUnit.

**An Example Test Class**

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

<a name="calling-routes-from-tests"></a>
## Calling Routes From Tests

You may easily call one of your routes for a test using the `call` method:

**Calling A Route From A Test**

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

You may then inspect the `Illuminate\Http\Response` object:

	$this->assertEquals('Hello World', $response->getContent());

You may also call a controller from a test:

**Calling A Controller From A Test**

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', ['user' => 1]);

The `getContent` method will return the evaluated string contents of the response. If your route returns a `View`, you may access it using the `original` property:

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

### DOM Crawler

You may also call a route and receive a DOM Crawler instance that you may use to inspect the content:

	$crawler = $this->client->request('GET', '/');

	$this->assertTrue($this->client->getResponse()->isOk());

	$this->assertCount(1, $crawler->filter('h1:contains("Hello World!")'));

For more information on how to use the crawler, refer to its [official documentation](http://symfony.com/doc/master/components/dom_crawler.html).

<a name="helper-methods"></a>
## Helper Methods

The `TestCase` class contains several helper methods to make testing your application easier.

You may set the currently authenticated user using the `be` method:

**Setting The Currently Authenticated User**

	$user = new User(['name' => 'John']);

	$this->be($user);

You may re-seed your database from a test using the `seed` method:

**Re-Seeding Database From Tests**

	$this->seed();

	$this->seed($connection);

More information on creating seeds may be found in the [migrations and seeding](/docs/migrations#database-seeding) section of the documentation.