# HTTP Tests

- [Introduction](#introduction)
    - [Customizing Request Headers](#customizing-request-headers)
- [Session / Authentication](#session-and-authentication)
- [Testing JSON APIs](#testing-json-apis)
- [Testing File Uploads](#testing-file-uploads)
- [Available Assertions](#available-assertions)
    - [Response Assertions](#response-assertions)
    - [Authentication Assertions](#authentication-assertions)

<a name="introduction"></a>
## Introduction

Laravel provides a very fluent API for making HTTP requests to your application and examining the output. For example, take a look at the test defined below:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;

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

<a name="customizing-request-headers"></a>
### Customizing Request Headers

You may use the `withHeaders` method to customize the request's headers before it is sent to the application. This allows you to add any custom headers you would like to the request:

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
            $response = $this->withHeaders([
                'X-Header' => 'Value',
            ])->json('POST', '/user', ['name' => 'Sally']);

            $response
                ->assertStatus(201)
                ->assertJson([
                    'created' => true,
                ]);
        }
    }

> {tip} The CSRF middleware is automatically disabled when running tests.

<a name="session-and-authentication"></a>
## Session / Authentication

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

    use App\User;

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $user = factory(User::class)->create();

            $response = $this->actingAs($user)
                             ->withSession(['foo' => 'bar'])
                             ->get('/');
        }
    }

You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method:

    $this->actingAs($user, 'api')

<a name="testing-json-apis"></a>
## Testing JSON APIs

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
                ->assertStatus(201)
                ->assertJson([
                    'created' => true,
                ]);
        }
    }

> {tip} The `assertJson` method converts the response to an array and utilizes `PHPUnit::assertArraySubset` to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present.

<a name="verifying-exact-match"></a>
### Verifying An Exact JSON Match

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
                ->assertStatus(201)
                ->assertExactJson([
                    'created' => true,
                ]);
        }
    }

<a name="testing-file-uploads"></a>
## Testing File Uploads

The `Illuminate\Http\UploadedFile` class provides a `fake` method which may be used to generate dummy files or images for testing. This, combined with the `Storage` facade's `fake` method greatly simplifies the testing of file uploads. For example, you may combine these two features to easily test an avatar upload form:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;
    use Illuminate\Http\UploadedFile;
    use Illuminate\Support\Facades\Storage;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;

    class ExampleTest extends TestCase
    {
        public function testAvatarUpload()
        {
            Storage::fake('avatars');

            $file = UploadedFile::fake()->image('avatar.jpg');

            $response = $this->json('POST', '/avatar', [
                'avatar' => $file,
            ]);

            // Assert the file was stored...
            Storage::disk('avatars')->assertExists($file->hashName());

            // Assert a file does not exist...
            Storage::disk('avatars')->assertMissing('missing.jpg');
        }
    }

#### Fake File Customization

When creating files using the `fake` method, you may specify the width, height, and size of the image in order to better test your validation rules:

    UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);

In addition to creating images, you may create files of any other type using the `create` method:

    UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);

<a name="available-assertions"></a>
## Available Assertions

<a name="response-assertions"></a>
### Response Assertions

Laravel provides a variety of custom assertion methods for your [PHPUnit](https://phpunit.de/) tests. These assertions may be accessed on the response that is returned from the `json`, `get`, `post`, `put`, and `delete` test methods:

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">

[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertExactJson](#assert-exact-json)
[assertForbidden](#assert-forbidden)
[assertHeader](#assert-header)
[assertHeaderMissing](#assert-header-missing)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertLocation](#assert-location)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertSessionHas](#assert-session-has)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionMissing](#assert-session-missing)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-cookie"></a>
#### assertCookie

Assert that the response contains the given cookie:

    $response->assertCookie($cookieName, $value = null);

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

Assert that the response contains the given cookie and it is expired:

    $response->assertCookieExpired($cookieName);

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

Assert that the response contains the given cookie and it is not expired:

    $response->assertCookieNotExpired($cookieName);

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

Assert that the response does not contains the given cookie:

    $response->assertCookieMissing($cookieName);

<a name="assert-dont-see"></a>
#### assertDontSee

Assert that the given string is not contained within the response:

    $response->assertDontSee($value);

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

Assert that the given string is not contained within the response text:

    $response->assertDontSeeText($value);

<a name="assert-exact-json"></a>
#### assertExactJson

Assert that the response contains an exact match of the given JSON data:

    $response->assertExactJson(array $data);

<a name="assert-forbidden"></a>
#### assertForbidden

Assert that the response has a forbidden status code:

    $response->assertForbidden();

<a name="assert-header"></a>
#### assertHeader

Assert that the given header is present on the response:

    $response->assertHeader($headerName, $value = null);

<a name="assert-header-missing"></a>
#### assertHeaderMissing

Assert that the given header is not present on the response:

    $response->assertHeaderMissing($headerName);

<a name="assert-json"></a>
#### assertJson

Assert that the response contains the given JSON data:

    $response->assertJson(array $data);

<a name="assert-json-count"></a>
#### assertJsonCount

Assert that the response JSON has an array with the expected number of items at the given key:

    $response->assertJsonCount($count, $key = null);

<a name="assert-json-fragment"></a>
#### assertJsonFragment

Assert that the response contains the given JSON fragment:

    $response->assertJsonFragment(array $data);

<a name="assert-json-missing"></a>
#### assertJsonMissing

Assert that the response does not contain the given JSON fragment:

    $response->assertJsonMissing(array $data);

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

Assert that the response does not contain the exact JSON fragment:

    $response->assertJsonMissingExact(array $data);

<a name="assert-json-structure"></a>
#### assertJsonStructure

Assert that the response has a given JSON structure:

    $response->assertJsonStructure(array $structure);

<a name="assert-json-validation-errors"></a>
#### assertJsonValidationErrors

Assert that the response has the given JSON validation errors for the given keys:

    $response->assertJsonValidationErrors($keys);

<a name="assert-location"></a>
#### assertLocation

Assert that the response has the given URI value in the `Location` header:

    $response->assertLocation($uri);

<a name="assert-not-found"></a>
#### assertNotFound

Assert that the response has a not found status code:

    $response->assertNotFound();

<a name="assert-ok"></a>
#### assertOk

Assert that the response has a 200 status code:

    $response->assertOk();

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

Assert that the response contains the given cookie (unencrypted):

    $response->assertPlainCookie($cookieName, $value = null);

<a name="assert-redirect"></a>
#### assertRedirect

Assert that the response is a redirect to a given URI:

    $response->assertRedirect($uri);

<a name="assert-see"></a>
#### assertSee

Assert that the given string is contained within the response:

    $response->assertSee($value);

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

Assert that the given strings are contained in order within the response:

    $response->assertSeeInOrder(array $values);

<a name="assert-see-text"></a>
#### assertSeeText

Assert that the given string is contained within the response text:

    $response->assertSeeText($value);

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

Assert that the given strings are contained in order within the response text:

    $response->assertSeeTextInOrder(array $values);

<a name="assert-session-has"></a>
#### assertSessionHas

Assert that the session contains the given piece of data:

    $response->assertSessionHas($key, $value = null);

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

Assert that the session has a given list of values:

    $response->assertSessionHasAll(array $data);

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

Assert that the session contains an error for the given field:

    $response->assertSessionHasErrors(array $keys, $format = null, $errorBag = 'default');

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

Assert that the session has the given errors:

    $response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

Assert that the session has no errors:

    $response->assertSessionHasNoErrors();

<a name="assert-session-missing"></a>
#### assertSessionMissing

Assert that the session does not contain the given key:

    $response->assertSessionMissing($key);

<a name="assert-status"></a>
#### assertStatus

Assert that the response has a given code:

    $response->assertStatus($code);

<a name="assert-successful"></a>
#### assertSuccessful

Assert that the response has a successful status code:

    $response->assertSuccessful();

<a name="assert-view-has"></a>
#### assertViewHas

Assert that the response view was given a piece of data:

    $response->assertViewHas($key, $value = null);

<a name="assert-view-has-all"></a>
#### assertViewHasAll

Assert that the response view has a given list of data:

    $response->assertViewHasAll(array $data);

<a name="assert-view-is"></a>
#### assertViewIs

Assert that the given view was returned by the route:

    $response->assertViewIs($value);

<a name="assert-view-missing"></a>
#### assertViewMissing

Assert that the response view is missing a piece of bound data:

    $response->assertViewMissing($key);

<a name="authentication-assertions"></a>
### Authentication Assertions

Laravel also provides a variety of authentication related assertions for your [PHPUnit](https://phpunit.de/) tests:

Method  | Description
------------- | -------------
`$this->assertAuthenticated($guard = null);`  |  Assert that the user is authenticated.
`$this->assertGuest($guard = null);`  |  Assert that the user is not authenticated.
`$this->assertAuthenticatedAs($user, $guard = null);`  |  Assert that the given user is authenticated.
`$this->assertCredentials(array $credentials, $guard = null);`  |  Assert that the given credentials are valid.
`$this->assertInvalidCredentials(array $credentials, $guard = null);`  |  Assert that the given credentials are invalid.
