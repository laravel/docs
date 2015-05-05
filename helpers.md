# Helper Functions

- [Arrays](#arrays)
- [Paths](#paths)
- [Routing](#routing)
- [Strings](#strings)
- [URLs](#urls)
- [Miscellaneous](#miscellaneous)

<a name="arrays"></a>
## Arrays

### array_add

The `array_add` function adds a given key / value pair to the array if the given key doesn't already exist in the array.

	$array = ['foo' => 'bar'];

	$array = array_add($array, 'key', 'value');

### array_divide

The `array_divide` function returns two arrays, one containing the keys, and the other containing the values of the original array.

	$array = ['foo' => 'bar'];

	list($keys, $values) = array_divide($array);

### array_dot

The `array_dot` function flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth.

	$array = ['foo' => ['bar' => 'baz']];

	$array = array_dot($array);

	// ['foo.bar' => 'baz'];

### array_except

The `array_except` method removes the given key / value pairs from the array.

	$array = array_except($array, ['keys', 'to', 'remove']);

### array_fetch

The `array_fetch` method returns a flattened array containing the selected nested element.

	$array = [
		['developer' => ['name' => 'Taylor']],
		['developer' => ['name' => 'Dayle']]
	];

	$array = array_fetch($array, 'developer.name');

	// ['Taylor', 'Dayle'];

### array_first

The `array_first` method returns the first element of an array passing a given truth test.

	$array = [100, 200, 300];

	$value = array_first($array, function($key, $value)
	{
		return $value >= 150;
	});

A default value may also be passed as the third parameter:

	$value = array_first($array, $callback, $default);

### array_last

The `array_last` method returns the last element of an array passing a given truth test.

	$array = [350, 400, 500, 300, 200, 100];

	$value = array_last($array, function($key, $value)
	{
		return $value > 350;
	});

	// 500

A default value may also be passed as the third parameter:

	$value = array_last($array, $callback, $default);

### array_flatten

The `array_flatten` method will flatten a multi-dimensional array into a single level.

	$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

	$array = array_flatten($array);

	// ['Joe', 'PHP', 'Ruby'];

### array_forget

The `array_forget` method will remove a given key / value pair from a deeply nested array using "dot" notation.

	$array = ['names' => ['joe' => ['programmer']]];

	array_forget($array, 'names.joe');

### array_get

The `array_get` method will retrieve a given value from a deeply nested array using "dot" notation.

	$array = ['names' => ['joe' => ['programmer']]];

	$value = array_get($array, 'names.joe');

	$value = array_get($array, 'names.john', 'default');

> **Note:** Want something like `array_get` but for objects instead? Use `object_get`.

### array_only

The `array_only` method will return only the specified key / value pairs from the array.

	$array = ['name' => 'Joe', 'age' => 27, 'votes' => 1];

	$array = array_only($array, ['name', 'votes']);

### array_pluck

The `array_pluck` method will pluck a list of the given key / value pairs from the array.

	$array = [['name' => 'Taylor'], ['name' => 'Dayle']];

	$array = array_pluck($array, 'name');

	// ['Taylor', 'Dayle'];

### array_pull

The `array_pull` method will return a given key / value pair from the array, as well as remove it.

	$array = ['name' => 'Taylor', 'age' => 27];

	$name = array_pull($array, 'name');

### array_set

The `array_set` method will set a value within a deeply nested array using "dot" notation.

	$array = ['names' => ['programmer' => 'Joe']];

	array_set($array, 'names.editor', 'Taylor');

### array_sort

The `array_sort` method sorts the array by the results of the given Closure.

	$array = [
		['name' => 'Jill'],
		['name' => 'Barry']
	];

	$array = array_values(array_sort($array, function($value)
	{
		return $value['name'];
	}));

### array_where

Filter the array using the given Closure.

	$array = [100, '200', 300, '400', 500];

	$array = array_where($array, function($key, $value)
	{
		return is_string($value);
	});

	// Array ( [1] => 200 [3] => 400 )

### head

Return the first element in the array.

	$first = head($this->returnsArray('foo'));

### last

Return the last element in the array. Useful for method chaining.

	$last = last($this->returnsArray('foo'));

<a name="paths"></a>
## Paths

### app_path

Get the fully qualified path to the `app` directory.

	$path = app_path();

### base_path

Get the fully qualified path to the root of the application install.

### config_path

Get the fully qualified path to the `config` directory.

### public_path

Get the fully qualified path to the `public` directory.

### storage_path

Get the fully qualified path to the `storage` directory.

<a name="routing"></a>
## Routing

### get

Register a new GET route with the router.

	get('/', function() { return 'Hello World'; });

### post

Register a new POST route with the router.

	post('foo/bar', 'FooController@action');

### put

Register a new PUT route with the router.

	put('foo/bar', 'FooController@action');

### patch

Register a new PATCH route with the router.

	patch('foo/bar', 'FooController@action');

### delete

Register a new DELETE route with the router.

	delete('foo/bar', 'FooController@action');
	
### resource

Register a new RESTful resource route with the router.

	resource('foo', 'FooController');

<a name="strings"></a>
## Strings

### camel_case

Convert the given string to `camelCase`.

	$camel = camel_case('foo_bar');

	// fooBar

### class_basename

Get the class name of the given class, without any namespace names.

	$class = class_basename('Foo\Bar\Baz');

	// Baz

### e

Run `htmlentities` over the given string, with UTF-8 support.

	$entities = e('<html>foo</html>');

### ends_with

Determine if the given haystack ends with a given needle.

	$value = ends_with('This is my name', 'name');

### snake_case

Convert the given string to `snake_case`.

	$snake = snake_case('fooBar');

	// foo_bar

### str_limit

Limit the number of characters in a string.

	str_limit($value, $limit = 100, $end = '...')

Example:

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

### starts_with

Determine if the given haystack begins with the given needle.

	$value = starts_with('This is my name', 'This');

### str_contains

Determine if the given haystack contains the given needle.

	$value = str_contains('This is my name', 'my');

### str_finish

Add a single instance of the given needle to the haystack. Remove any extra instances.

	$string = str_finish('this/string', '/');

	// this/string/

### str_is

Determine if a given string matches a given pattern. Asterisks may be used to indicate wildcards.

	$value = str_is('foo*', 'foobar');

### str_plural

Convert a string to its plural form (English only).

	$plural = str_plural('car');

### str_random

Generate a random string of the given length.

	$string = str_random(40);

### str_singular

Convert a string to its singular form (English only).

	$singular = str_singular('cars');

### str_slug

Generate a URL friendly "slug" from a given string.

	str_slug($title, $separator);

Example:

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

### studly_case

Convert the given string to `StudlyCase`.

	$value = studly_case('foo_bar');

	// FooBar

### trans

Translate a given language line. Alias of `Lang::get`.

	$value = trans('validation.required'):

### trans_choice

Translate a given language line with inflection. Alias of `Lang::choice`.

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## URLs

### action

Generate a URL for a given controller action.

	$url = action('HomeController@getIndex', $params);

### route

Generate a URL for a given named route.

	$url = route('routeName', $params);

### asset

Generate a URL for an asset.

	$url = asset('img/photo.jpg');

### secure_asset

Generate a URL for an asset using HTTPS.

	echo secure_asset('foo/bar.zip', $title, $attributes = []);

### secure_url

Generate a fully qualified URL to a given path using HTTPS.

	echo secure_url('foo/bar', $parameters = []);

### url

Generate a fully qualified URL to the given path.

	echo url('foo/bar', $parameters = [], $secure = null);

<a name="miscellaneous"></a>
## Miscellaneous

### csrf_token

Get the value of the current CSRF token.

	$token = csrf_token();

### dd

Dump the given variable and end execution of the script.

	dd($value);

### elixir

Get the path to a versioned Elixir file.

	elixir($file);

### env

Gets the value of an environment variable or return a default value.

	env('APP_ENV', 'production')

### event

Fire an event.

	event('my.event');

### value

If the given value is a `Closure`, return the value returned by the `Closure`. Otherwise, return the value.

	$value = value(function() { return 'bar'; });

### view

Get a View instance for the given view path.

	return view('auth.login');

### with

Return the given object.

	$value = with(new Foo)->doWork();
