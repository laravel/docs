# Helper Functions

- [Introduction](#introduction)
- [Available Methods](#available-methods)

<a name="introduction"></a>
## Introduction

Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.

<a name="available-methods"></a>
## Available Methods

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

### Arrays

<div class="collection-method-list" markdown="1">

[array_add](#method-array-add)
[array_collapse](#method-array-collapse)
[array_divide](#method-array-divide)
[array_dot](#method-array-dot)
[array_except](#method-array-except)
[array_first](#method-array-first)
[array_flatten](#method-array-flatten)
[array_forget](#method-array-forget)
[array_get](#method-array-get)
[array_has](#method-array-has)
[array_last](#method-array-last)
[array_only](#method-array-only)
[array_pluck](#method-array-pluck)
[array_prepend](#method-array-prepend)
[array_pull](#method-array-pull)
[array_set](#method-array-set)
[array_sort](#method-array-sort)
[array_sort_recursive](#method-array-sort-recursive)
[array_where](#method-array-where)
[head](#method-head)
[last](#method-last)
</div>

### Paths

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

### Strings

<div class="collection-method-list" markdown="1">

[camel_case](#method-camel-case)
[class_basename](#method-class-basename)
[e](#method-e)
[ends_with](#method-ends-with)
[snake_case](#method-snake-case)
[str_limit](#method-str-limit)
[starts_with](#method-starts-with)
[str_contains](#method-str-contains)
[str_finish](#method-str-finish)
[str_is](#method-str-is)
[str_plural](#method-str-plural)
[str_random](#method-str-random)
[str_singular](#method-str-singular)
[str_slug](#method-str-slug)
[studly_case](#method-studly-case)
[title_case](#method-title-case)
[trans](#method-trans)
[trans_choice](#method-trans-choice)

</div>

### URLs

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[secure_asset](#method-secure-asset)
[route](#method-route)
[secure_url](#method-secure-url)
[url](#method-url)

</div>

### Miscellaneous

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[cache](#method-cache)
[collect](#method-collect)
[config](#method-config)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[dd](#method-dd)
[dispatch](#method-dispatch)
[env](#method-env)
[event](#method-event)
[factory](#method-factory)
[info](#method-info)
[logger](#method-logger)
[method_field](#method-method-field)
[old](#method-old)
[redirect](#method-redirect)
[request](#method-request)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[value](#method-value)
[view](#method-view)

</div>

<a name="method-listing"></a>
## Method Listing

<style>
    #collection-method code {
        font-size: 14px;
    }

    #collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="arrays"></a>
## Arrays

<a name="method-array-add"></a>
#### `array_add()` {#collection-method .first-collection-method}

The `array_add` function adds a given key / value pair to the array if the given key doesn't already exist in the array:

    $array = array_add(['name' => 'Desk'], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-collapse"></a>
#### `array_collapse()` {#collection-method}

The `array_collapse` function collapses an array of arrays into a single array:

    $array = array_collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-array-divide"></a>
#### `array_divide()` {#collection-method}

The `array_divide` function returns two arrays, one containing the keys, and the other containing the values of the original array:

    list($keys, $values) = array_divide(['name' => 'Desk']);

    // $keys: ['name']

    // $values: ['Desk']

<a name="method-array-dot"></a>
#### `array_dot()` {#collection-method}

The `array_dot` function flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth:

    $array = array_dot(['foo' => ['bar' => 'baz']]);

    // ['foo.bar' => 'baz'];

<a name="method-array-except"></a>
#### `array_except()` {#collection-method}

The `array_except` function removes the given key / value pairs from the array:

    $array = ['name' => 'Desk', 'price' => 100];

    $array = array_except($array, ['price']);

    // ['name' => 'Desk']

<a name="method-array-first"></a>
#### `array_first()` {#collection-method}

The `array_first` function returns the first element of an array passing a given truth test:

    $array = [100, 200, 300];

    $value = array_first($array, function ($value, $key) {
        return $value >= 150;
    });

    // 200

A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test:

    $value = array_first($array, $callback, $default);

<a name="method-array-flatten"></a>
#### `array_flatten()` {#collection-method}

The `array_flatten` function will flatten a multi-dimensional array into a single level.

    $array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

    $array = array_flatten($array);

    // ['Joe', 'PHP', 'Ruby'];

<a name="method-array-forget"></a>
#### `array_forget()` {#collection-method}

The `array_forget` function removes a given key / value pair from a deeply nested array using "dot" notation:

    $array = ['products' => ['desk' => ['price' => 100]]];

    array_forget($array, 'products.desk');

    // ['products' => []]

<a name="method-array-get"></a>
#### `array_get()` {#collection-method}

The `array_get` function retrieves a value from a deeply nested array using "dot" notation:

    $array = ['products' => ['desk' => ['price' => 100]]];

    $value = array_get($array, 'products.desk');

    // ['price' => 100]

The `array_get` function also accepts a default value, which will be returned if the specific key is not found:

    $value = array_get($array, 'names.john', 'default');

<a name="method-array-has"></a>
#### `array_has()` {#collection-method}

The `array_has` function checks that a given item or items exists in an array using "dot" notation:

    $array = ['product' => ['name' => 'desk', 'price' => 100]];

    $hasItem = array_has($array, 'product.name');

    // true

    $hasItems = array_has($array, ['product.price', 'product.discount']);

    // false

<a name="method-array-last"></a>
#### `array_last()` {#collection-method}

The `array_last` function returns the last element of an array passing a given truth test:

    $array = [100, 200, 300, 110];

    $value = array_last($array, function ($value, $key) {
        return $value >= 150;
    });

    // 300

<a name="method-array-only"></a>
#### `array_only()` {#collection-method}

The `array_only` function will return only the specified key / value pairs from the given array:

    $array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

    $array = array_only($array, ['name', 'price']);

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-pluck"></a>
#### `array_pluck()` {#collection-method}

The `array_pluck` function will pluck a list of the given key / value pairs from the array:

    $array = [
        ['developer' => ['id' => 1, 'name' => 'Taylor']],
        ['developer' => ['id' => 2, 'name' => 'Abigail']],
    ];

    $array = array_pluck($array, 'developer.name');

    // ['Taylor', 'Abigail'];

You may also specify how you wish the resulting list to be keyed:

    $array = array_pluck($array, 'developer.name', 'developer.id');

    // [1 => 'Taylor', 2 => 'Abigail'];

<a name="method-array-prepend"></a>
#### `array_prepend()` {#collection-method}

The `array_prepend` function will push an item onto the beginning of an array:

    $array = ['one', 'two', 'three', 'four'];

    $array = array_prepend($array, 'zero');

    // $array: ['zero', 'one', 'two', 'three', 'four']

<a name="method-array-pull"></a>
#### `array_pull()` {#collection-method}

The `array_pull` function returns and removes a key / value pair from the array:

    $array = ['name' => 'Desk', 'price' => 100];

    $name = array_pull($array, 'name');

    // $name: Desk

    // $array: ['price' => 100]

<a name="method-array-set"></a>
#### `array_set()` {#collection-method}

The `array_set` function sets a value within a deeply nested array using "dot" notation:

    $array = ['products' => ['desk' => ['price' => 100]]];

    array_set($array, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 200]]]

<a name="method-array-sort"></a>
#### `array_sort()` {#collection-method}

The `array_sort` function sorts the array by the results of the given Closure:

    $array = [
        ['name' => 'Desk'],
        ['name' => 'Chair'],
    ];

    $array = array_values(array_sort($array, function ($value) {
        return $value['name'];
    }));

    /*
        [
            ['name' => 'Chair'],
            ['name' => 'Desk'],
        ]
    */

<a name="method-array-sort-recursive"></a>
#### `array_sort_recursive()` {#collection-method}

The `array_sort_recursive` function recursively sorts the array using the `sort` function:

    $array = [
        [
            'Roman',
            'Taylor',
            'Li',
        ],
        [
            'PHP',
            'Ruby',
            'JavaScript',
        ],
    ];

    $array = array_sort_recursive($array);

    /*
        [
            [
                'Li',
                'Roman',
                'Taylor',
            ],
            [
                'JavaScript',
                'PHP',
                'Ruby',
            ]
        ];
    */

<a name="method-array-where"></a>
#### `array_where()` {#collection-method}

The `array_where` function filters the array using the given Closure:

    $array = [100, '200', 300, '400', 500];

    $array = array_where($array, function ($value, $key) {
        return is_string($value);
    });

    // [1 => 200, 3 => 400]

<a name="method-head"></a>
#### `head()` {#collection-method}

The `head` function simply returns the first element in the given array:

    $array = [100, 200, 300];

    $first = head($array);

    // 100

<a name="method-last"></a>
#### `last()` {#collection-method}

The `last` function returns the last element in the given array:

    $array = [100, 200, 300];

    $last = last($array);

    // 300

<a name="paths"></a>
## Paths

<a name="method-app-path"></a>
#### `app_path()` {#collection-method}

The `app_path` function returns the fully qualified path to the `app` directory. You may also use the `app_path` function to generate a fully qualified path to a file relative to the application directory:

    $path = app_path();

    $path = app_path('Http/Controllers/Controller.php');

<a name="method-base-path"></a>
#### `base_path()` {#collection-method}

The `base_path` function returns the fully qualified path to the project root. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory:

    $path = base_path();

    $path = base_path('vendor/bin');

<a name="method-config-path"></a>
#### `config_path()` {#collection-method}

The `config_path` function returns the fully qualified path to the application configuration directory:

    $path = config_path();

<a name="method-database-path"></a>
#### `database_path()` {#collection-method}

The `database_path` function returns the fully qualified path to the application's database directory:

    $path = database_path();

<a name="method-mix"></a>
#### `mix()` {#collection-method}

The `mix` function gets the path to a [versioned Mix file](/docs/{{version}}/mix):

    mix($file);

<a name="method-public-path"></a>
#### `public_path()` {#collection-method}

The `public_path` function returns the fully qualified path to the `public` directory:

    $path = public_path();

<a name="method-resource-path"></a>
#### `resource_path()` {#collection-method}

The `resource_path` function returns the fully qualified path to the `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file relative to the storage directory:

    $path = resource_path();

    $path = resource_path('assets/sass/app.scss');

<a name="method-storage-path"></a>
#### `storage_path()` {#collection-method}

The `storage_path` function returns the fully qualified path to the `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file relative to the storage directory:

    $path = storage_path();

    $path = storage_path('app/file.txt');

<a name="strings"></a>
## Strings

<a name="method-camel-case"></a>
#### `camel_case()` {#collection-method}

The `camel_case` function converts the given string to `camelCase`:

    $camel = camel_case('foo_bar');

    // fooBar

<a name="method-class-basename"></a>
#### `class_basename()` {#collection-method}

The `class_basename` returns the class name of the given class with the class' namespace removed:

    $class = class_basename('Foo\Bar\Baz');

    // Baz

<a name="method-e"></a>
#### `e()` {#collection-method}

The `e` function runs `htmlspecialchars` over the given string:

    echo e('<html>foo</html>');

    // &lt;html&gt;foo&lt;/html&gt;

<a name="method-ends-with"></a>
#### `ends_with()` {#collection-method}

The `ends_with` function determines if the given string ends with the given value:

    $value = ends_with('This is my name', 'name');

    // true

<a name="method-snake-case"></a>
#### `snake_case()` {#collection-method}

The `snake_case` function converts the given string to `snake_case`:

    $snake = snake_case('fooBar');

    // foo_bar

<a name="method-str-limit"></a>
#### `str_limit()` {#collection-method}

The `str_limit` function limits the number of characters in a string. The function accepts a string as its first argument and the maximum number of resulting characters as its second argument:

    $value = str_limit('The PHP framework for web artisans.', 7);

    // The PHP...

<a name="method-starts-with"></a>
#### `starts_with()` {#collection-method}

The `starts_with` function determines if the given string begins with the given value:

    $value = starts_with('This is my name', 'This');

    // true

<a name="method-str-contains"></a>
#### `str_contains()` {#collection-method}

The `str_contains` function determines if the given string contains the given value:

    $value = str_contains('This is my name', 'my');

    // true

You may also pass an array of values to determine if the given string contains any of the values:

    $value = str_contains('This is my name', ['my', 'foo']);

    // true

<a name="method-str-finish"></a>
#### `str_finish()` {#collection-method}

The `str_finish` function adds a single instance of the given value to a string:

    $string = str_finish('this/string', '/');

    // this/string/

<a name="method-str-is"></a>
#### `str_is()` {#collection-method}

The `str_is` function determines if a given string matches a given pattern. Asterisks may be used to indicate wildcards:

    $value = str_is('foo*', 'foobar');

    // true

    $value = str_is('baz*', 'foobar');

    // false

<a name="method-str-plural"></a>
#### `str_plural()` {#collection-method}

The `str_plural` function converts a string to its plural form. This function currently only supports the English language:

    $plural = str_plural('car');

    // cars

    $plural = str_plural('child');

    // children

You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string:

    $plural = str_plural('child', 2);

    // children

    $plural = str_plural('child', 1);

    // child

<a name="method-str-random"></a>
#### `str_random()` {#collection-method}

The `str_random` function generates a random string of the specified length. This function uses PHP's `random_bytes` function:

    $string = str_random(40);

<a name="method-str-singular"></a>
#### `str_singular()` {#collection-method}

The `str_singular` function converts a string to its singular form. This function currently only supports the English language:

    $singular = str_singular('cars');

    // car

<a name="method-str-slug"></a>
#### `str_slug()` {#collection-method}

The `str_slug` function generates a URL friendly "slug" from the given string:

    $title = str_slug('Laravel 5 Framework', '-');

    // laravel-5-framework

<a name="method-studly-case"></a>
#### `studly_case()` {#collection-method}

The `studly_case` function converts the given string to `StudlyCase`:

    $value = studly_case('foo_bar');

    // FooBar

<a name="method-title-case"></a>
#### `title_case()` {#collection-method}

The `title_case` function converts the given string to `Title Case`:

    $title = title_case('a nice title uses the correct case');

    // A Nice Title Uses The Correct Case

<a name="method-trans"></a>
#### `trans()` {#collection-method}

The `trans` function translates the given language line using your [localization files](/docs/{{version}}/localization):

    echo trans('validation.required'):

<a name="method-trans-choice"></a>
#### `trans_choice()` {#collection-method}

The `trans_choice` function translates the given language line with inflection:

    $value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## URLs

<a name="method-action"></a>
#### `action()` {#collection-method}

The `action` function generates a URL for the given controller action. You do not need to pass the full namespace to the controller. Instead, pass the controller class name relative to the `App\Http\Controllers` namespace:

    $url = action('HomeController@getIndex');

If the method accepts route parameters, you may pass them as the second argument to the method:

    $url = action('UserController@profile', ['id' => 1]);

<a name="method-asset"></a>
#### `asset()` {#collection-method}

Generate a URL for an asset using the current scheme of the request (HTTP or HTTPS):

    $url = asset('img/photo.jpg');

<a name="method-secure-asset"></a>
#### `secure_asset()` {#collection-method}

Generate a URL for an asset using HTTPS:

    echo secure_asset('foo/bar.zip', $title, $attributes = []);

<a name="method-route"></a>
#### `route()` {#collection-method}

The `route` function generates a URL for the given named route:

    $url = route('routeName');

If the route accepts parameters, you may pass them as the second argument to the method:

    $url = route('routeName', ['id' => 1]);

<a name="method-secure-url"></a>
#### `secure_url()` {#collection-method}

The `secure_url` function generates a fully qualified HTTPS URL to the given path:

    echo secure_url('user/profile');

    echo secure_url('user/profile', [1]);

<a name="method-url"></a>
#### `url()` {#collection-method}

The `url` function generates a fully qualified URL to the given path:

    echo url('user/profile');

    echo url('user/profile', [1]);

If no path is provided, a `Illuminate\Routing\UrlGenerator` instance is returned:

    echo url()->current();
    echo url()->full();
    echo url()->previous();

<a name="miscellaneous"></a>
## Miscellaneous

<a name="method-abort"></a>
#### `abort()` {#collection-method}

The `abort` function throws a HTTP exception which will be rendered by the exception handler:

    abort(401);

You may also provide the exception's response text:

    abort(401, 'Unauthorized.');

<a name="method-abort-if"></a>
#### `abort_if()` {#collection-method}

The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`:

    abort_if(! Auth::user()->isAdmin(), 403);

<a name="method-abort-unless"></a>
#### `abort_unless()` {#collection-method}

The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`:

    abort_unless(Auth::user()->isAdmin(), 403);

<a name="method-auth"></a>
#### `auth()` {#collection-method}

The `auth` function returns an authenticator instance. You may use it instead of the `Auth` facade for convenience:

    $user = auth()->user();

<a name="method-back"></a>
#### `back()` {#collection-method}

The `back()` function generates a redirect response to the user's previous location:

    return back();

<a name="method-bcrypt"></a>
#### `bcrypt()` {#collection-method}

The `bcrypt` function hashes the given value using Bcrypt. You may use it as an alternative to the `Hash` facade:

    $password = bcrypt('my-secret-password');

<a name="method-cache"></a>
#### `cache()` {#collection-method}

The `cache` function may be used to get values from the cache. If the given key does not exist in the cache, an optional default value will be returned:

    $value = cache('key');

    $value = cache('key', 'default');

You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of minutes or duration the cached value should be considered valid:

    cache(['key' => 'value'], 5);

    cache(['key' => 'value'], Carbon::now()->addSeconds(10));

<a name="method-collect"></a>
#### `collect()` {#collection-method}

The `collect` function creates a [collection](/docs/{{version}}/collections) instance from the given array:

    $collection = collect(['taylor', 'abigail']);

<a name="method-config"></a>
#### `config()` {#collection-method}

The `config` function gets the value of a configuration variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist:

    $value = config('app.timezone');

    $value = config('app.timezone', $default);

The `config` helper may also be used to set configuration variables at runtime by passing an array of key / value pairs:

    config(['app.debug' => true]);

<a name="method-csrf-field"></a>
#### `csrf_field()` {#collection-method}

The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/{{version}}/blade):

    {{ csrf_field() }}

<a name="method-csrf-token"></a>
#### `csrf_token()` {#collection-method}

The `csrf_token` function retrieves the value of the current CSRF token:

    $token = csrf_token();

<a name="method-dd"></a>
#### `dd()` {#collection-method}

The `dd` function dumps the given variables and ends execution of the script:

    dd($value);

    dd($value1, $value2, $value3, ...);

If you do not want to halt the execution of your script, use the `dump` function instead:

    dump($value);

<a name="method-dispatch"></a>
#### `dispatch()` {#collection-method}

The `dispatch` function pushes a new job onto the Laravel [job queue](/docs/{{version}}/queues):

    dispatch(new App\Jobs\SendEmails);

<a name="method-env"></a>
#### `env()` {#collection-method}

The `env` function gets the value of an environment variable or returns a default value:

    $env = env('APP_ENV');

    // Return a default value if the variable doesn't exist...
    $env = env('APP_ENV', 'production');

<a name="method-event"></a>
#### `event()` {#collection-method}

The `event` function dispatches the given [event](/docs/{{version}}/events) to its listeners:

    event(new UserRegistered($user));

<a name="method-factory"></a>
#### `factory()` {#collection-method}

The `factory` function creates a model factory builder for a given class, name, and amount. It can be used while [testing](/docs/{{version}}/database-testing#writing-factories) or [seeding](/docs/{{version}}/seeding#using-model-factories):

    $user = factory(App\User::class)->make();

<a name="method-info"></a>
#### `info()` {#collection-method}

The `info` function will write information to the log:

    info('Some helpful information!');

An array of contextual data may also be passed to the function:

    info('User login attempt failed.', ['id' => $user->id]);

<a name="method-logger"></a>
#### `logger()` {#collection-method}

The `logger` function can be used to write a `debug` level message to the log:

    logger('Debug message');

An array of contextual data may also be passed to the function:

    logger('User has logged in.', ['id' => $user->id]);

A [logger](/docs/{{version}}/errors#logging) instance will be returned if no value is passed to the function:

    logger()->error('You are not allowed here.');

<a name="method-method-field"></a>
#### `method_field()` {#collection-method}

The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/{{version}}/blade):

    <form method="POST">
        {{ method_field('DELETE') }}
    </form>

<a name="method-old"></a>
#### `old()` {#collection-method}

The `old` function [retrieves](/docs/{{version}}/requests#retrieving-input) an old input value flashed into the session:

    $value = old('value');

    $value = old('value', 'default');

<a name="method-redirect"></a>
#### `redirect()` {#collection-method}

The `redirect` function returns a redirect HTTP response, or returns the redirector instance if called with no arguments:

    return redirect('/home');

    return redirect()->route('route.name');

<a name="method-request"></a>
#### `request()` {#collection-method}

The `request` function returns the current [request](/docs/{{version}}/requests) instance or obtains an input item:

    $request = request();

    $value = request('key', $default = null)

<a name="method-response"></a>
#### `response()` {#collection-method}

The `response` function creates a [response](/docs/{{version}}/responses) instance or obtains an instance of the response factory:

    return response('Hello World', 200, $headers);

    return response()->json(['foo' => 'bar'], 200, $headers);

<a name="method-retry"></a>
#### `retry()` {#collection-method}

The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, it's return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown:

    return retry(5, function () {
        // Attempt 5 times while resting 100ms in between attempts...
    }, 100);

<a name="method-session"></a>
#### `session()` {#collection-method}

The `session` function may be used to get or set session values:

    $value = session('key');

You may set values by passing an array of key / value pairs to the function:

    session(['chairs' => 7, 'instruments' => 3]);

The session store will be returned if no value is passed to the function:

    $value = session()->get('key');

    session()->put('key', $value);

<a name="method-value"></a>
#### `value()` {#collection-method}

The `value` function's behavior will simply return the value it is given. However, if you pass a `Closure` to the function, the `Closure` will be executed then its result will be returned:

    $value = value(function () {
        return 'bar';
    });

<a name="method-view"></a>
#### `view()` {#collection-method}

The `view` function retrieves a [view](/docs/{{version}}/views) instance:

    return view('auth.login');
