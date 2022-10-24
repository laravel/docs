# HTTP Responses

- [Creating Responses](#creating-responses)
    - [Attaching Headers To Responses](#attaching-headers-to-responses)
    - [Attaching Cookies To Responses](#attaching-cookies-to-responses)
    - [Cookies & Encryption](#cookies-and-encryption)
- [Redirects](#redirects)
    - [Redirecting To Named Routes](#redirecting-named-routes)
    - [Redirecting To Controller Actions](#redirecting-controller-actions)
    - [Redirecting To External Domains](#redirecting-external-domains)
    - [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)
- [Other Response Types](#other-response-types)
    - [View Responses](#view-responses)
    - [JSON Responses](#json-responses)
    - [File Downloads](#file-downloads)
    - [File Responses](#file-responses)
- [Response Macros](#response-macros)

<a name="creating-responses"></a>
## Creating Responses

<a name="strings-arrays"></a>
#### Strings & Arrays

All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response:

    Route::get('/', function () {
        return 'Hello World';
    });

In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response:

    Route::get('/', function () {
        return [1, 2, 3];
    });

> **Note**  
> Did you know you can also return [Eloquent collections](/docs/{{version}}/eloquent-collections) from your routes or controllers? They will automatically be converted to JSON. Give it a shot!

<a name="response-objects"></a>
#### Response Objects

Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/{{version}}/views).

Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses:

    Route::get('/home', function () {
        return response('Hello World', 200)
                      ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent Models & Collections

You may also return [Eloquent ORM](/docs/{{version}}/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### Attaching Headers To Responses

Keep in mind that most response methods are chainable, allowing for the fluent construction of response instances. For example, you may use the `header` method to add a series of headers to the response before sending it back to the user:

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');

Or, you may use the `withHeaders` method to specify an array of headers to be added to the response:

    return response($content)
                ->withHeaders([
                    'Content-Type' => $type,
                    'X-Header-One' => 'Header Value',
                    'X-Header-Two' => 'Header Value',
                ]);

> **Warning**  
> In middleware you should instead set the response headers using the methods on its `ResponseHeaderBag`, e.g. `$response->headers->set(...);`.
> The framework returns other types of Symfony Responses on which the chainable header methods are undefined, e.g. `BinaryFileResponse` and `StreamedResponse`.

<a name="cache-control-middleware"></a>
#### Cache Control Middleware

Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier:

    Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
        Route::get('/privacy', function () {
            // ...
        });

        Route::get('/terms', function () {
            // ...
        });
    });

<a name="attaching-cookies-to-responses"></a>
### Attaching Cookies To Responses

You may attach a cookie to an outgoing `Illuminate\Http\Response` instance using the `cookie` method. You should pass the name, value, and the number of minutes the cookie should be considered valid to this method:

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method:

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser:

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### Generating Cookie Instances

If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance:

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### Expiring Cookies Early

You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response:

    return response('Hello World')->withoutCookie('name');

If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie:

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### Cookies & Encryption

By default, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `$except` property of the `App\Http\Middleware\EncryptCookies` middleware, which is located in the `app/Http/Middleware` directory:

    /**
     * The names of the cookies that should not be encrypted.
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="redirects"></a>
## Redirects

Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper:

    Route::get('/dashboard', function () {
        return redirect('home/dashboard');
    });

Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/{{version}}/session), make sure the route calling the `back` function is using the `web` middleware group:

    Route::post('/user/profile', function () {
        // Validate the request...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### Redirecting To Named Routes

When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method:

    return redirect()->route('login');

If your route has parameters, you may pass them as the second argument to the `route` method:

    // For a route with the following URI: /profile/{id}

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Populating Parameters Via Eloquent Models

If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically:

    // For a route with the following URI: /profile/{id}

    return redirect()->route('profile', [$user]);

If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model:

    /**
     * Get the value of the model's route key.
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### Redirecting To Controller Actions

You may also generate redirects to [controller actions](/docs/{{version}}/controllers). To do so, pass the controller and action name to the `action` method:

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

If your controller route requires parameters, you may pass them as the second argument to the `action` method:

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### Redirecting To External Domains

Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification:

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### Redirecting With Flashed Session Data

Redirecting to a new URL and [flashing data to the session](/docs/{{version}}/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain:

    Route::post('/user/profile', function () {
        // ...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

After the user is redirected, you may display the flashed message from the [session](/docs/{{version}}/session). For example, using [Blade syntax](/docs/{{version}}/blade):

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### Redirecting With Input

You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/{{version}}/requests#retrieving-old-input) during the next request to repopulate the form:

    return back()->withInput();

<a name="other-response-types"></a>
## Other Response Types

The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/{{version}}/contracts) is returned. This contract provides several helpful methods for generating responses.

<a name="view-responses"></a>
### View Responses

If you need control over the response's status and headers but also need to return a [view](/docs/{{version}}/views) as the response's content, you should use the `view` method:

    return response()
                ->view('hello', $data, 200)
                ->header('Content-Type', $type);

Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function.

<a name="json-responses"></a>
### JSON Responses

The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function:

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method:

    return response()
                ->json(['name' => 'Abigail', 'state' => 'CA'])
                ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### File Downloads

The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method:

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> **Warning**  
> Symfony HttpFoundation, which manages file downloads, requires the file being downloaded to have an ASCII filename.

<a name="streamed-downloads"></a>
#### Streamed Downloads

Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments:

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
                    ->contents()
                    ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="file-responses"></a>
### File Responses

The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the path to the file as its first argument and an array of headers as its second argument:

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="response-macros"></a>
## Response Macros

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/{{version}}/providers), such as the `App\Providers\AppServiceProvider` service provider:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Response::macro('caps', function ($value) {
                return Response::make(strtoupper($value));
            });
        }
    }

The `macro` function accepts a name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper:

    return response()->caps('foo');
