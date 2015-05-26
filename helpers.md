# Helper Functions

- [Introduction](#introduction)
- [Available Methods](#available-methods)

<a name="introduction"></a>
## Introduction

Laravel includes a variety of "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.

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
[array_divide](#method-array-divide)
[array_dot](#method-array-dot)
[array_except](#method-array-except)
[array_fetch](#method-array-fetch)
[array_first](#method-array-first)
[array_last](#method-array-last)
[array_flatten](#method-array-flatten)
[array_forget](#method-array-forget)
[array_get](#method-array-get)
[array_only](#method-array-only)
[array_pluck](#method-array-pluck)
[array_pull](#method-array-pull)
[array_set](#method-array-set)
[array_sort](#method-array-sort)
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
[public_path](#method-public-path)
[storage_path](#method-storage-path)
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
[trans](#method-trans)
[trans_choice](#method-trans-choice)
</div>

### URLs

<div class="collection-method-list" markdown="1">
[action](#method-action)
[route](#method-route)
[url](#method-url)
</div>

### Miscellaneous

<div class="collection-method-list" markdown="1">
[csrf_token](#method-csrf-token)
[dd](#method-dd)
[elixir](#method-elixir)
[env](#method-env)
[event](#method-event)
[response](#method-response)
[value](#method-value)
[view](#method-view)
[with](#method-with)
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

<a name="method-array-add"></a>
#### `array_add()` {#collection-method .first-collection-method}

The `array_add` function adds a given key / value pair to the array if the given key doesn't already exist in the array:

	$array = ['foo' => 'bar'];

	$array = array_add($array, 'key', 'value');

<a name="method-array-divide"></a>
#### `array_divide()` {#collection-method}

The `array_divide` function returns two arrays, one containing the keys, and the other containing the values of the original array:

	$array = ['foo' => 'bar'];

	list($keys, $values) = array_divide($array);

<a name="method-array-dot"></a>
#### `array_dot()` {#collection-method}

The `array_dot` function flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth:

	$array = ['foo' => ['bar' => 'baz']];

	$array = array_dot($array);

	// ['foo.bar' => 'baz'];

<a name="method-array-except"></a>
#### `array_except` {#collection-method}

The `array_except` method removes the given key / value pairs from the array:

	$array = array_except($array, ['keys', 'to', 'remove']);

<a name="method-array-fetch"></a>
#### `array_fetch()` {#collection-method}

The `array_fetch` method returns a flattened array containing the selected nested element:

	$array = [
		['developer' => ['name' => 'Taylor']],
		['developer' => ['name' => 'Dayle']]
	];

	$array = array_fetch($array, 'developer.name');

	// ['Taylor', 'Dayle'];

<a name="method-array-first"></a>
#### `array_first()` {#collection-method}

The `array_first` method returns the first element of an array passing a given truth test.

	$array = [100, 200, 300];

	$value = array_first($array, function ($key, $value) {
		return $value >= 150;
	});

A default value may also be passed as the third parameter:

	$value = array_first($array, $callback, $default);

<a name="method-array-last"></a>
#### `array_last()` {#collection-method}

The `array_last` method returns the last element of an array passing a given truth test.

	$array = [350, 400, 500, 300, 200, 100];

	$value = array_last($array, function ($key, $value) {
		return $value > 350;
	});

	// 500

A default value may also be passed as the third parameter:

	$value = array_last($array, $callback, $default);

<a name="method-array-flatten"></a>
#### `array_flatten()` {#collection-method}

The `array_flatten` method will flatten a multi-dimensional array into a single level.

	$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

	$array = array_flatten($array);

	// ['Joe', 'PHP', 'Ruby'];

<a name="method-array-forget"></a>
#### `array_forget()` {#collection-method}

The `array_forget` method will remove a given key / value pair from a deeply nested array using "dot" notation.

	$array = ['names' => ['joe' => ['programmer']]];

	array_forget($array, 'names.joe');

<a name="method-array-get"></a>
#### `array_get()` {#collection-method}

The `array_get` method will retrieve a given value from a deeply nested array using "dot" notation.

	$array = ['names' => ['joe' => ['programmer']]];

	$value = array_get($array, 'names.joe');

	$value = array_get($array, 'names.john', 'default');

<a name="method-array-only"></a>
#### `array_only()` {#collection-method}

The `array_only` method will return only the specified key / value pairs from the array.

	$array = ['name' => 'Joe', 'age' => 27, 'votes' => 1];

	$array = array_only($array, ['name', 'votes']);

<a name="method-array-pluck"></a>
#### `array_pluck()` {#collection-method}

The `array_pluck` method will pluck a list of the given key / value pairs from the array.

	$array = [['name' => 'Taylor'], ['name' => 'Dayle']];

	$array = array_pluck($array, 'name');

	// ['Taylor', 'Dayle'];

<a name="method-array-pull"></a>
#### `array_pull()` {#collection-method}

The `array_pull` method will return a given key / value pair from the array, as well as remove it.

	$array = ['name' => 'Taylor', 'age' => 27];

	$name = array_pull($array, 'name');

<a name="method-array-set"></a>
#### `array_set()` {#collection-method}

The `array_set` method will set a value within a deeply nested array using "dot" notation.

	$array = ['names' => ['programmer' => 'Joe']];

	array_set($array, 'names.editor', 'Taylor');

<a name="method-array-sort"></a>
#### `array_sort()` {#collection-method}

The `array_sort` method sorts the array by the results of the given Closure.

	$array = [
		['name' => 'Jill'],
		['name' => 'Barry']
	];

	$array = array_values(array_sort($array, function ($value) {
		return $value['name'];
	}));

<a name="method-array-where"></a>
#### `array_where()` {#collection-method}

Filter the array using the given Closure.

	$array = [100, '200', 300, '400', 500];

	$array = array_where($array, function ($key, $value) {
		return is_string($value);
	});

	// Array ( [1] => 200 [3] => 400 )

<a name="method-head"></a>
#### `head()` {#collection-method}

Return the first element in the array.

	$first = head($this->returnsArray('foo'));

<a name="method-last"></a>
#### `last()` {#collection-method}

Return the last element in the array. Useful for method chaining.

	$last = last($this->returnsArray('foo'));

<a name="paths"></a>
## Paths

<a name="method-app-path"></a>
#### `app_path()` {#collection-method}

Get the fully qualified path to the `app` directory.

	$path = app_path();

<a name="method-base-path"></a>
#### `base_path()` {#collection-method}

Get the fully qualified path to the root of the application install.

<a name="method-config-path"></a>
#### `config_path()` {#collection-method}

Get the fully qualified path to the `config` directory.

<a name="method-public-path"></a>
#### `public_path()` {#collection-method}

Get the fully qualified path to the `public` directory.

<a name="method-storage-path"></a>
#### `storage_path()` {#collection-method}

Get the fully qualified path to the `storage` directory.

<a name="strings"></a>
## Strings

<a name="method-camel-case"></a>
#### `camel_case()` {#collection-method}

Convert the given string to `camelCase`.

	$camel = camel_case('foo_bar');

	// fooBar

<a name="method-class-basename"></a>
#### `class_basename()` {#collection-method}

Get the class name of the given class, without any namespace names.

	$class = class_basename('Foo\Bar\Baz');

	// Baz

<a name="method-e"></a>
#### `e()` {#collection-method}

Run `htmlentities` over the given string, with UTF-8 support.

	$entities = e('<html>foo</html>');

<a name="method-ends-with"></a>
#### `ends_with()` {#collection-method}

Determine if the given haystack ends with a given needle.

	$value = ends_with('This is my name', 'name');

<a name="method-snake-case"></a>
#### `snake_case()` {#collection-method}

Convert the given string to `snake_case`.

	$snake = snake_case('fooBar');

	// foo_bar

<a name="method-str-limit"></a>
#### `str_limit()` {#collection-method}

Limit the number of characters in a string.

	str_limit($value, $limit = 100, $end = '...')

Example:

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

<a name="method-starts-with"></a>
#### `starts_with()` {#collection-method}

Determine if the given haystack begins with the given needle.

	$value = starts_with('This is my name', 'This');

<a name="method-str-contains"></a>
#### `str_contains()` {#collection-method}

Determine if the given haystack contains the given needle.

	$value = str_contains('This is my name', 'my');

<a name="method-str-finish"></a>
#### `str_finish()` {#collection-method}

Add a single instance of the given needle to the haystack. Remove any extra instances.

	$string = str_finish('this/string', '/');

	// this/string/

<a name="method-str-is"></a>
#### `str_is()` {#collection-method}

Determine if a given string matches a given pattern. Asterisks may be used to indicate wildcards.

	$value = str_is('foo*', 'foobar');

<a name="method-str-plural"></a>
#### `str_plural()` {#collection-method}

Convert a string to its plural form (English only).

	$plural = str_plural('car');

<a name="method-str-random"></a>
#### `str_random()` {#collection-method}

Generate a random string of the given length.

	$string = str_random(40);

<a name="method-str-singular"></a>
#### `str_singular()` {#collection-method}

Convert a string to its singular form (English only).

	$singular = str_singular('cars');

<a name="method-str-slug"></a>
#### `str_slug()` {#collection-method}

Generate a URL friendly "slug" from a given string.

	str_slug($title, $separator);

Example:

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

<a name="method-studly-case"></a>
#### `studly_case()` {#collection-method}

Convert the given string to `StudlyCase`.

	$value = studly_case('foo_bar');

	// FooBar

<a name="method-trans"></a>
#### `trans()` {#collection-method}

Translate a given language line. Alias of `Lang::get`.

	$value = trans('validation.required'):

<a name="method-trans-choice"></a>
#### `trans_choice()` {#collection-method}

Translate a given language line with inflection. Alias of `Lang::choice`.

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## URLs

<a name="method-action"></a>
#### `action()` {#collection-method}

Generate a URL for a given controller action.

	$url = action('HomeController@getIndex', $params);

<a name="method-route"></a>
#### `route()` {#collection-method}

Generate a URL for a given named route.

	$url = route('routeName', $params);

<a name="method-url"></a>
#### `url()` {#collection-method}

Generate a fully qualified URL to the given path.

	echo url('foo/bar', $parameters = [], $secure = null);

<a name="miscellaneous"></a>
## Miscellaneous

<a name="method-csrf-token"></a>
#### `csrf_token()` {#collection-method}

Get the value of the current CSRF token.

	$token = csrf_token();

<a name="method-dd"></a>
#### `dd()` {#collection-method}

Dump the given variable and end execution of the script.

	dd($value);

<a name="method-elixir"></a>
#### `elixir()` {#collection-method}

Get the path to a versioned Elixir file.

	elixir($file);

<a name="method-env"></a>
#### `env()` {#collection-method}

Get the value of an environment variable or return a default value.

	env('APP_ENV', 'production')

<a name="method-event"></a>
#### `event()` {#collection-method}

Fire an event.

	event('my.event');

<a name="method-response"></a>
#### `response()` {#collection-method}

Create a response instance or obtain an instance of the response factory.

	return response('Hello World', 200, $headers);

	return response()->json(['foo' => 'bar'], 200, $headers);

<a name="method-value"></a>
#### `value()` {#collection-method}

If the given value is a `Closure`, return the value returned by the `Closure`. Otherwise, return the value.

	$value = value(function() { return 'bar'; });

<a name="method-view"></a>
#### `view()` {#collection-method}

Get a View instance for the given view path.

	return view('auth.login');

<a name="method-with"></a>
#### `with()` {#collection-method}

Return the given object.

	$value = with(new Foo)->doWork();
