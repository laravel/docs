# Testing

- [Introduction](#introduction)
- [Application Testing](#application-testing)
- [Working With Databases](#working-with-databases)
- [Mocking Facades](#mocking-facades)
- [Framework Assertions](#framework-assertions)
- [Helper Methods](#helper-methods)

<a name="introduction"></a>
## Introduction

Laravel is built with unit testing in mind. In fact, support for testing with PHPUnit is included out of the box, and a `phpunit.xml` file is already setup for your application. The framework also ships with convenient helper methods allowing you to expressively test your applications.

An `ExampleTest.php` file is provided in the `tests` directory. After installing a new Laravel application, simply run `phpunit` on the command line to run your tests.

### Test Environment

When running unit tests, Laravel will automatically set the configuration environment to `testing`. Also, Laravel includes configuration files for `session` and `cache` in the test environment. Both of these drivers are set to `array` while in the test environment, meaning no session or cache data will be persisted while testing. You are free to create other testing environment configurations as necessary.

The `testing` environment variables may be configured in the `phpunit.xml` file.

### Defining & Running Tests

To create a test case, simply create a new test file in the `tests` directory. The test class should extend `TestCase`. You may then define test methods as you normally would when using PHPUnit.

#### An Example Test Class

	<?php


	class FooTest extends TestCase
	{
		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}
	}

You may run all of the tests for your application by executing the `phpunit` command from your terminal.

> **Note:** If you define your own `setUp` method within a test class, be sure to call `parent::setUp`.

<a name="application-testing"></a>
## Application Testing

Laravel provides a very fluent API for making HTTP requests to your application, examining the output, and even filling out forms. For example, take a look at the `ExampleTest.php` file included in your `tests` directory:

	<?php

	use Illuminate\Foundation\Testing\WithoutMiddleware;
	use Illuminate\Foundation\Testing\DatabaseTransactions;

	class ExampleTest extends TestCase
	{
	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	        $this->visit('/')
	             ->see('Laravel 5');
	    }
	}

The `visit` method makes a `GET` request into the application. The `see` method asserts that we should see the given text should be contained in the response returned by the application. This is the most basic application test available in Laravel.

### Interacting With Your Application

Of course, you can do much more than simply assert that text appears in a given response. Let's take a look at some examples of clicking links and filling out forms:

#### Clicking A Link

In this test, we will make a request to the application, "click" a link in the returned response, and then assert that we landed on a given URI. In this example, let's assume there is a link in our response that has a text value of "About Us". For example:

	<a href="/about-us">About Us</a>

Now, let's write a test that clicks the link and asserts the user is on the correct page:

    public function testBasicExample()
    {
        $this->visit('/')
             ->click('About Us')
             ->seePageIs('/about-us');
    }

#### Working With Forms

Laravel also provides several methods for testing forms such as `type`, `select`, `check`, `attach`, and `press`. Let's take a look at each of these methods using an example. First, let's imagine this form exists on the application's registration page:

	<form action="/register" method="POST">
		{{ csrf_field() }}

		<div>
			Name: <input type="text" name="name">
		</div>

		<div>
			Plan:
			<input type="radio" value="basic_plan" name="plan"> Basic
			<input type="radio" value="pro_plan" name="plan"> Pro
		</div>

		<div>
			<input type="checkbox" value="yes" name="terms"> Accept Terms
		</div>

		<div>
			<input type="subnit" value="Register">
		</div>
	</form>

Now we can write a test to complete this form and inspect the result:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->select('basic_plan', 'plan')
             ->check('terms')
             ->press('Register');
             ->seePageIs('/dashboard');
    }

Alternatively, you may use the `submitForm` method to pass an array of all of the inputs in one method call:

    public function testNewUserRegistration()
    {
    	$formData = [
         	'name' => 'Taylor',
         	'plan' => 'basic_plan',
         	'terms' => true,
    	];

        $this->visit('/register')
             ->submitForm('Register', $formData)
             ->seePageIs('/dashboard');
    }

#### Working With Attachments

If your form contains `file` input types, you may attach files to the form using the `attach` method:

    public function testPhotoCanBeUploaded()
    {
        $this->visit('/upload')
             ->name('File Name', 'name')
             ->attach($absolutePathToFile, 'photo')
             ->press('Upload')
             ->see('Upload Successful!');
    }

### Making Custom HTTP Requsts

If you would like to make an HTTP request into your application and get the full `Illuminate\Http\Response` object, you may use the `call` method from your tests:

    public function testApplication()
    {
    	$response = $this->call('GET', '/');

    	$this->assertEquals(200, $response->status());
    }

If you are making `POST`, `PUT`, or `PATCH` requests you may pass an array of data with the request:

    public function testApplication()
    {
    	$response = $this->call('POST', '/user', ['name' => 'Taylor']);

    	$this->assertEquals(200, $response->status());
    }

<a name="working-with-databases"></a>
## Working With Databases

Laravel also provides a variety of helpful tools to make it easier to test your database driven applications. First, you may use the `seeInDatabase` helper to assert that data exists in the database matching a given set of criteria. For example, if we would like to verify that there is a record in the `users` table with the `email` value of `sally@example.com`, we can do the following:

    public function testDatabase()
    {
    	// Make call to application...

    	$this->seeInDatabase('users', ['email' => 'sally@foo.com']);
    }

Of course, the `seeInDatabase` method and other helpers like it are for convenience. You are free to use any of PHPUnit's built-in assertion methods to supplement your tests.

### Factories

When testing, it is common to need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a default set of attributes for each of your [Eloquent models](/docs/{{version}}/eloquent) using "factories". To get started, take a look at the `database/factories/ModelFactory.php` file in your application. Out of the box, this file contains one factory definition:

	$factory['App\User'] = function ($faker) {
	    return [
	        'name' => $faker->name,
	        'email' => $faker->email,
	        'password' => str_random(10),
	        'remember_token' => str_random(10),
	    ];
	};

Within the Closure, which serves as the factory definition, you may return the default test values of all attributes on the model. The Closure will receive an instance of the [Faker](https://github.com/fzaninotto/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing.

Of course, you are free to add your own additional factories to the `ModelFactory.php` file.

#### Multiple Factory Types

Sometimes you may wish to have multiple factories for the same Eloquent model class. For example, perhaps you would like to have a factory for "Administrator" users in addition to normal users. You may define these factories using the `defineAs` method:

	$factory->defineAs('App\User', 'admin', function ($faker) {
	    return [
	        'name' => $faker->name,
	        'email' => $faker->email,
	        'password' => str_random(10),
	        'remember_token' => str_random(10),
	        'admin' => true,
	    ];
	});

Instead of duplicating all of the attributes from your base user factory, you may use the `raw` method to retrieve the base attributes. Once you have the attributes, simply supplement them with any additional values you require:

	$factory->defineAs('App\User', 'admin', function ($faker) use ($factory) {
		$user = $factory->raw('App\User');

		$user['admin'] =  true;

		return $user;
	});

#### Using Factories In Tests

Once you have defined your factories, you may use them in your tests or database seed files to generate model instances. Within your test classes, you have access to the `$this->factory` property. So, let's take a look at a few examples of creating models. First, we'll use the `make` method, which creates models but does not save them to the database:

    public function testDatabase()
    {
    	$user = $this->factory->make('App\User');

    	// Use model in tests...
    }

Since the factory instance implements the PHP `ArrayAccess` interface, you may also make model instances by accessing the factory as an array:

	$user = $this->factory['App\User'];

If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified values will be replaced while the rest of the values remain set to their default values as specified by the factory:

    $user = $this->factory->make('App\User', [
    	'name' => 'Abigail',
   	]);

You may also create a Collection of many models:

   	$users = $this->factory->of('App\User')->times(3)->make();

#### Persisting Factory Models

The `create` method not only creates the model instances, but also saves them to the database using Eloquent's `save` method:

    public function testDatabase()
    {
    	$user = $this->factory->create('App\User');

    	// Use model in tests...
    }

Again, you may override attributes on the model by passing an array to the `create` method:

    $user = $this->factory->create('App\User', [
    	'name' => 'Abigail',
   	]);

#### Adding Relations To Models

You may even persist multiple models to the database. In this example, we'll even attach a relation to the created models. When using the `create` method to create multiple models, an Eloquent collection instance is returned, allowing you to use any of the convenient functions provided by the collection, such as `each`:

    $users = $this->factory->of('App\User')
               ->times(3)
               ->create()
               ->each(function($u) {
					$u->posts()->save($this->factory['App\Post']);
				});

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

You may re-seed your database from a test using the `seed` method:

#### Re-Seeding Database From Tests

	$this->seed();

	$this->seed('DatabaseSeeder');

More information on creating seeds may be found in the [migrations and seeding](/docs/migrations#database-seeding) section of the documentation.
