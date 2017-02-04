# HTTP Tests

- [Introduction](#introduction)
- [Session / Authentication](#session-and-authentication)
- [Testing JSON APIs](#testing-json-apis)
- [Available Assertions](#available-assertions)

<a name="introduction"></a>
## Introduction

Laravel provides a very fluent API for making HTTP requests to your application and examining the output. For example, take a look at the test defined below:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function testBasicTest()
        {
            $response = $this->get('/');

            $response->assertStatus(200);
        }
    }

The `get` method makes a `GET` request into the application, while the `assertStatus` method asserts that the returned response should have the given HTTP status code. In addition to this simple assertion, Laravel also contains a variety of assertions for inspecting the response headers, content, JSON structure, and more.

<a name="session-and-authentication"></a>
### Session / Authentication

Laravel provides several helpers for working with the session during HTTP testing. First, you may set the session data to a given array using the `withSession` method. This is useful for loading the session with data before issuing a request to your application:

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $response = $this->withSession(['foo' => 'bar'])
                             ->get('/');
        }
    }

Of course, one common use of the session is for maintaining state for the authenticated user. The `actingAs` helper method provides a simple way to authenticate a given user as the current user. For example, we may use a [model factory](/docs/{{version}}/database-testing#writing-factories) to generate and authenticate a user:

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $user = factory(App\User::class)->create();

            $response = $this->actingAs($user)
                             ->withSession(['foo' => 'bar'])
                             ->get('/')
        }
    }

You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method:

    $this->actingAs($user, 'api')

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
            $response = $this->json('POST', '/user', ['name' => 'Sally']);

            $response
                ->assertStatus(200)
                ->assertJson([
                    'created' => true,
                ]);
        }
    }

> {tip} The `assertJson` method converts the response to an array and utilizes `PHPUnit::assertArraySubset` to verify that the given fragment exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present.

<a name="verifying-exact-match"></a>
### Verifying Exact Match

If you would like to verify that the given array is an **exact** match for the JSON returned by the application, you should use the `assertExactJson` method:

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
            $response = $this->json('POST', '/user', ['name' => 'Sally']);

            $response
                ->assertStatus(200)
                ->assertExactJson([
                    'created' => true,
                ]);
        }
    }

<a name="available-assertions"></a>
### Available Assertions

Laravel provides a variety of custom assertion methods for your [PHPUnit](https://phpunit.de/) tests. These assertions may be accessed on the response that is returned from the `json`, `get`, `post`, `put`, and `delete` test methods:

Method  | Description
------------- | -------------
`$response->assertStatus($code);`  |  Assert that the response has a given code.
`$response->assertRedirect($uri);`  |  Assert that the response is a redirect to a given URI.
`$response->assertHeader($headerName, $value = null);`  |  Assert that the given header is present on the response.
`$response->assertCookie($cookieName, $value = null);`  |  Assert that the response contains the given cookie.
`$response->assertPlainCookie($cookieName, $value = null);`  |  Assert that the response contains the given cookie (unencrypted).
`$response->assertSessionHas($key, $value = null);`  |  Assert that the session contains the given piece of data.
`$response->assertSessionMissing($key);`  |  Assert that the session does not contain the given key.
`$response->assertJson(array $data);`  |  Assert that the response contains the given JSON data.
`$response->assertExactJson(array $data);`  |  Assert that the response contains an exact match of the given JSON data.
`$response->assertViewHas($key, $value = null);`  |  Assert that the response view was given a piece of data.
