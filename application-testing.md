# Application Testing

- [Introduction](#introduction)
- [Interacting With Your Application](#interacting-with-your-application)
    - [Interacting With Links](#interacting-with-links)
    - [Interacting With Forms](#interacting-with-forms)
- [Testing JSON APIs](#testing-json-apis)
    - [Verifying Exact Match](#verifying-exact-match)
    - [Verifying Structural Match](#verifying-structural-match)
- [Sessions / Authentication](#sessions-and-authentication)
- [Disabling Middleware](#disabling-middleware)
- [Custom HTTP Requests](#custom-http-requests)
- [PHPUnit Assertions](#phpunit-assertions)

<a name="introduction"></a>
## Introduction

Laravel provides a very fluent API for making HTTP requests to your application, examining the output, and even filling out forms. For example, take a look at the test defined below:

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
                 ->see('Laravel 5')
                 ->dontSee('Rails');
        }
    }

The `visit` method makes a `GET` request into the application. The `see` method asserts that we should see the given text in the response returned by the application. The `dontSee` method asserts that the given text is not returned in the application response. This is the most basic application test available in Laravel.

You may also use the 'visitRoute' method to make a 'GET' request via a named route:

    $this->visitRoute('profile');

    $this->visitRoute('profile', ['user' => 1]);

<a name="interacting-with-your-application"></a>
## Interacting With Your Application

Of course, you can do much more than simply assert that text appears in a given response. Let's take a look at some examples of clicking links and filling out forms:

<a name="interacting-with-links"></a>
### Interacting With Links

In this test, we will make a request to the application, "click" a link in the returned response, and then assert that we landed on a given URI. For example, let's assume there is a link in our response that has a text value of "About Us":

    <a href="/about-us">About Us</a>

Now, let's write a test that clicks the link and asserts the user lands on the correct page:

    public function testBasicExample()
    {
        $this->visit('/')
             ->click('About Us')
             ->seePageIs('/about-us');
    }

You may also check that the user has arrived at the correct named route using the `seeRouteIs` method:

    ->seeRouteIs('profile', ['user' => 1]);

<a name="interacting-with-forms"></a>
### Interacting With Forms

Laravel also provides several methods for testing forms. The `type`, `select`, `check`, `attach`, and `press` methods allow you to interact with all of your form's inputs. For example, let's imagine this form exists on the application's registration page:

    <form action="/register" method="POST">
        {{ csrf_field() }}

        <div>
            Name: <input type="text" name="name">
        </div>

        <div>
            <input type="checkbox" value="yes" name="terms"> Accept Terms
        </div>

        <div>
            <input type="submit" value="Register">
        </div>
    </form>

We can write a test to complete this form and inspect the result:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

Of course, if your form contains other inputs such as radio buttons or drop-down boxes, you may easily fill out those types of fields as well. Here is a list of each form manipulation method:

Method  | Description
------------- | -------------
`$this->type($text, $elementName)`  |  "Type" text into a given field.
`$this->select($value, $elementName)`  |  "Select" a radio button or drop-down field.
`$this->check($elementName)`  |  "Check" a checkbox field.
`$this->uncheck($elementName)`  |  "Uncheck" a checkbox field.
`$this->attach($pathToFile, $elementName)`  |  "Attach" a file to the form.
`$this->press($buttonTextOrElementName)`  |  "Press" a button with the given text or name.

<a name="file-inputs"></a>
#### File Inputs

If your form contains `file` inputs, you may attach files to the form using the `attach` method:

    public function testPhotoCanBeUploaded()
    {
        $this->visit('/upload')
             ->attach($pathToFile, 'photo')
             ->press('Upload')
             ->see('Upload Successful!');
    }

<a name="testing-json-apis"></a>
### Testing JSON APIs

Laravel also provides several helpers for testing JSON APIs and their responses. For example, the `json`, `get`, `post`, `put`, `patch`, and `delete` methods may be used to issue requests with various HTTP verbs. You may also easily pass data and headers to these methods. To get started, let's write a test to make a `POST` request to `/user` and assert that the expected data was returned:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->json('POST', '/user', ['name' => 'Sally'])
                 ->seeJson([
                     'created' => true,
                 ]);
        }
    }

> {tip} The `seeJson` method converts the given array into JSON, and then verifies that the JSON fragment occurs **anywhere** within the entire JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present.

<a name="verifying-exact-match"></a>
### Verifying Exact Match

If you would like to verify that the given array is an **exact** match for the JSON returned by the application, you should use the `seeJsonEquals` method:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->json('POST', '/user', ['name' => 'Sally'])
                 ->seeJsonEquals([
                     'created' => true,
                 ]);
        }
    }

<a name="verifying-structural-match"></a>
### Verifying Structural Match

It is also possible to verify that a JSON response adheres to a specific structure. In this scenario, you should use the `seeJsonStructure` method and pass it your expected JSON structure:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->get('/user/1')
                 ->seeJsonStructure([
                     'name',
                     'pet' => [
                         'name', 'age'
                     ]
                 ]);
        }
    }

The above example illustrates an expectation of receiving a `name` attribute and a nested `pet` object with its own `name` and `age` attributes. `seeJsonStructure` will not fail if additional keys are present in the response. For example, the test would still pass if the `pet` had a `weight` attribute.

You may use the `*` to assert that the returned JSON structure has a list where each list item contains at least the attributes found in the set of values:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            // Assert that each user in the list has at least an id, name and email attribute.
            $this->get('/users')
                 ->seeJsonStructure([
                     '*' => [
                         'id', 'name', 'email'
                     ]
                 ]);
        }
    }

You may also nest the `*` notation. In this case, we will assert that each user in the JSON response contains a given set of attributes and that each pet on each user also contains a given set of attributes:

    $this->get('/users')
         ->seeJsonStructure([
             '*' => [
                 'id', 'name', 'email', 'pets' => [
                     '*' => [
                         'name', 'age'
                     ]
                 ]
             ]
         ]);

<a name="sessions-and-authentication"></a>
### Sessions / Authentication

Laravel provides several helpers for working with the session during testing. First, you may set the session data to a given array using the `withSession` method. This is useful for loading the session with data before issuing a request to your application:

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $this->withSession(['foo' => 'bar'])
                 ->visit('/');
        }
    }

Of course, one common use of the session is for maintaining state for the authenticated user. The `actingAs` helper method provides a simple way to authenticate a given user as the current user. For example, we may use a [model factory](/docs/{{version}}/database-testing#writing-factories) to generate and authenticate a user:

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $user = factory(App\User::class)->create();

            $this->actingAs($user)
                 ->withSession(['foo' => 'bar'])
                 ->visit('/')
                 ->see('Hello, '.$user->name);
        }
    }

You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method:

    $this->actingAs($user, 'api')

<a name="disabling-middleware"></a>
### Disabling Middleware

When testing your application, you may find it convenient to disable [middleware](/docs/{{version}}/middleware) for some of your tests. This will allow you to test your routes and controller in isolation from any middleware concerns. Laravel includes a simple `WithoutMiddleware` trait that you can use to automatically disable all middleware for the test class:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use WithoutMiddleware;

        //
    }

If you would like to only disable middleware for a few test methods, you may call the `withoutMiddleware` method from within the test methods:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->withoutMiddleware();

            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="custom-http-requests"></a>
### Custom HTTP Requests

If you would like to make a custom HTTP request into your application and get the full `Illuminate\Http\Response` object, you may use the `call` method:

    public function testApplication()
    {
        $response = $this->call('GET', '/');

        $this->assertEquals(200, $response->status());
    }

If you are making `POST`, `PUT`, or `PATCH` requests you may pass an array of input data with the request. Of course, this data will be available in your routes and controller via the [Request instance](/docs/{{version}}/requests):

       $response = $this->call('POST', '/user', ['name' => 'Taylor']);

<a name="phpunit-assertions"></a>
### PHPUnit Assertions

Laravel provides a variety of custom assertion methods for [PHPUnit](https://phpunit.de/) tests:

Method  | Description
------------- | -------------
`->assertResponseOk();`  |  Assert that the client response has an OK status code.
`->assertResponseStatus($code);`  |  Assert that the client response has a given code.
`->assertViewHas($key, $value = null);`  |  Assert that the response view has a given piece of bound data.
`->assertViewHasAll(array $bindings);`  |  Assert that the view has a given list of bound data.
`->assertViewMissing($key);`  |  Assert that the response view is missing a piece of bound data.
`->assertRedirectedTo($uri, $with = []);`  |  Assert whether the client was redirected to a given URI.
`->assertRedirectedToRoute($name, $parameters = [], $with = []);`  |  Assert whether the client was redirected to a given route.
`->assertRedirectedToAction($name, $parameters = [], $with = []);`  |  Assert whether the client was redirected to a given action.
`->assertSessionHas($key, $value = null);`  |  Assert that the session has a given value.
`->assertSessionHasAll(array $bindings);`  |  Assert that the session has a given list of values.
`->assertSessionHasErrors($bindings = [], $format = null);`  |  Assert that the session has errors bound.
`->assertHasOldInput();`  |  Assert that the session has old input.
`->assertSessionMissing($key);`  |  Assert that the session is missing a given key.
