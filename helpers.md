# Helpers

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Other Utilities](#other-utilities)
    - [Benchmarking](#benchmarking)
    - [Dates](#dates)
    - [Lottery](#lottery)
    - [Pipeline](#pipeline)
    - [Sleep](#sleep)

<a name="introduction"></a>
## Introduction

Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.

<a name="available-methods"></a>
## Available Methods

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<a name="arrays-and-objects-method-list"></a>
### Arrays & Objects

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAny](#method-array-hasany)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::sortRecursiveDesc](#method-array-sort-recursive-desc)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
[head](#method-head)
[last](#method-last)
</div>

<a name="paths-method-list"></a>
### Paths

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="urls-method-list"></a>
### URLs

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_route](#method-to-route)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### Miscellaneous

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)

</div>

<a name="arrays"></a>
## Arrays & Objects

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

The `Arr::accessible` method determines if the given value is array accessible:

    use Illuminate\Support\Arr;
    use Illuminate\Support\Collection;

    $isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

    // true

    $isAccessible = Arr::accessible(new Collection);

    // true

    $isAccessible = Arr::accessible('abc');

    // false

    $isAccessible = Arr::accessible(new stdClass);

    // false

<a name="method-array-add"></a>
#### `Arr::add()` {.collection-method}

The `Arr::add` method adds a given key / value pair to an array if the given key doesn't already exist in the array or is set to `null`:

    use Illuminate\Support\Arr;

    $array = Arr::add(['name' => 'Desk'], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]

    $array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]


<a name="method-array-collapse"></a>
#### `Arr::collapse()` {.collection-method}

The `Arr::collapse` method collapses an array of arrays into a single array:

    use Illuminate\Support\Arr;

    $array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

The `Arr::crossJoin` method cross joins the given arrays, returning a Cartesian product with all possible permutations:

    use Illuminate\Support\Arr;

    $matrix = Arr::crossJoin([1, 2], ['a', 'b']);

    /*
        [
            [1, 'a'],
            [1, 'b'],
            [2, 'a'],
            [2, 'b'],
        ]
    */

    $matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

    /*
        [
            [1, 'a', 'I'],
            [1, 'a', 'II'],
            [1, 'b', 'I'],
            [1, 'b', 'II'],
            [2, 'a', 'I'],
            [2, 'a', 'II'],
            [2, 'b', 'I'],
            [2, 'b', 'II'],
        ]
    */

<a name="method-array-divide"></a>
#### `Arr::divide()` {.collection-method}

The `Arr::divide` method returns two arrays: one containing the keys and the other containing the values of the given array:

    use Illuminate\Support\Arr;

    [$keys, $values] = Arr::divide(['name' => 'Desk']);

    // $keys: ['name']

    // $values: ['Desk']

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

The `Arr::dot` method flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth:

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    $flattened = Arr::dot($array);

    // ['products.desk.price' => 100]

<a name="method-array-except"></a>
#### `Arr::except()` {.collection-method}

The `Arr::except` method removes the given key / value pairs from an array:

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100];

    $filtered = Arr::except($array, ['price']);

    // ['name' => 'Desk']

<a name="method-array-exists"></a>
#### `Arr::exists()` {.collection-method}

The `Arr::exists` method checks that the given key exists in the provided array:

    use Illuminate\Support\Arr;

    $array = ['name' => 'John Doe', 'age' => 17];

    $exists = Arr::exists($array, 'name');

    // true

    $exists = Arr::exists($array, 'salary');

    // false

<a name="method-array-first"></a>
#### `Arr::first()` {.collection-method}

The `Arr::first` method returns the first element of an array passing a given truth test:

    use Illuminate\Support\Arr;

    $array = [100, 200, 300];

    $first = Arr::first($array, function (int $value, int $key) {
        return $value >= 150;
    });

    // 200

A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test:

    use Illuminate\Support\Arr;

    $first = Arr::first($array, $callback, $default);

<a name="method-array-flatten"></a>
#### `Arr::flatten()` {.collection-method}

The `Arr::flatten` method flattens a multi-dimensional array into a single level array:

    use Illuminate\Support\Arr;

    $array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

    $flattened = Arr::flatten($array);

    // ['Joe', 'PHP', 'Ruby']

<a name="method-array-forget"></a>
#### `Arr::forget()` {.collection-method}

The `Arr::forget` method removes a given key / value pair from a deeply nested array using "dot" notation:

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    Arr::forget($array, 'products.desk');

    // ['products' => []]

<a name="method-array-get"></a>
#### `Arr::get()` {.collection-method}

The `Arr::get` method retrieves a value from a deeply nested array using "dot" notation:

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    $price = Arr::get($array, 'products.desk.price');

    // 100

The `Arr::get` method also accepts a default value, which will be returned if the specified key is not present in the array:

    use Illuminate\Support\Arr;

    $discount = Arr::get($array, 'products.desk.discount', 0);

    // 0

<a name="method-array-has"></a>
#### `Arr::has()` {.collection-method}

The `Arr::has` method checks whether a given item or items exists in an array using "dot" notation:

    use Illuminate\Support\Arr;

    $array = ['product' => ['name' => 'Desk', 'price' => 100]];

    $contains = Arr::has($array, 'product.name');

    // true

    $contains = Arr::has($array, ['product.price', 'product.discount']);

    // false

<a name="method-array-hasany"></a>
#### `Arr::hasAny()` {.collection-method}

The `Arr::hasAny` method checks whether any item in a given set exists in an array using "dot" notation:

    use Illuminate\Support\Arr;

    $array = ['product' => ['name' => 'Desk', 'price' => 100]];

    $contains = Arr::hasAny($array, 'product.name');

    // true

    $contains = Arr::hasAny($array, ['product.name', 'product.discount']);

    // true

    $contains = Arr::hasAny($array, ['category', 'product.discount']);

    // false

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()` {.collection-method}

The `Arr::isAssoc` method returns `true` if the given array is an associative array. An array is considered "associative" if it doesn't have sequential numerical keys beginning with zero:

    use Illuminate\Support\Arr;

    $isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

    // true

    $isAssoc = Arr::isAssoc([1, 2, 3]);

    // false

<a name="method-array-islist"></a>
#### `Arr::isList()` {.collection-method}

The `Arr::isList` method returns `true` if the given array's keys are sequential integers beginning from zero:

    use Illuminate\Support\Arr;

    $isList = Arr::isList(['foo', 'bar', 'baz']);

    // true

    $isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

    // false

<a name="method-array-join"></a>
#### `Arr::join()` {.collection-method}

The `Arr::join` method joins array elements with a string. Using this method's second argument, you may also specify the joining string for the final element of the array:

    use Illuminate\Support\Arr;

    $array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

    $joined = Arr::join($array, ', ');

    // Tailwind, Alpine, Laravel, Livewire

    $joined = Arr::join($array, ', ', ' and ');

    // Tailwind, Alpine, Laravel and Livewire

<a name="method-array-keyby"></a>
#### `Arr::keyBy()` {.collection-method}

The `Arr::keyBy` method keys the array by the given key. If multiple items have the same key, only the last one will appear in the new array:

    use Illuminate\Support\Arr;

    $array = [
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ];

    $keyed = Arr::keyBy($array, 'product_id');

    /*
        [
            'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
            'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
        ]
    */

<a name="method-array-last"></a>
#### `Arr::last()` {.collection-method}

The `Arr::last` method returns the last element of an array passing a given truth test:

    use Illuminate\Support\Arr;

    $array = [100, 200, 300, 110];

    $last = Arr::last($array, function (int $value, int $key) {
        return $value >= 150;
    });

    // 300

A default value may be passed as the third argument to the method. This value will be returned if no value passes the truth test:

    use Illuminate\Support\Arr;

    $last = Arr::last($array, $callback, $default);

<a name="method-array-map"></a>
#### `Arr::map()` {.collection-method}

The `Arr::map` method iterates through the array and passes each value and key to the given callback. The array value is replaced by the value returned by the callback:

    use Illuminate\Support\Arr;

    $array = ['first' => 'james', 'last' => 'kirk'];

    $mapped = Arr::map($array, function (string $value, string $key) {
        return ucfirst($value);
    });

    // ['first' => 'James', 'last' => 'Kirk']

<a name="method-array-map-with-keys"></a>
#### `Arr::mapWithKeys()` {.collection-method}

The `Arr::mapWithKeys` method iterates through the array and passes each value to the given callback. The callback should return an associative array containing a single key / value pair:

    use Illuminate\Support\Arr;

    $array = [
        [
            'name' => 'John',
            'department' => 'Sales',
            'email' => 'john@example.com',
        ],
        [
            'name' => 'Jane',
            'department' => 'Marketing',
            'email' => 'jane@example.com',
        ]
    ];

    $mapped = Arr::mapWithKeys($array, function (array $item, int $key) {
        return [$item['email'] => $item['name']];
    });

    /*
        [
            'john@example.com' => 'John',
            'jane@example.com' => 'Jane',
        ]
    */

<a name="method-array-only"></a>
#### `Arr::only()` {.collection-method}

The `Arr::only` method returns only the specified key / value pairs from the given array:

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

    $slice = Arr::only($array, ['name', 'price']);

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-pluck"></a>
#### `Arr::pluck()` {.collection-method}

The `Arr::pluck` method retrieves all of the values for a given key from an array:

    use Illuminate\Support\Arr;

    $array = [
        ['developer' => ['id' => 1, 'name' => 'Taylor']],
        ['developer' => ['id' => 2, 'name' => 'Abigail']],
    ];

    $names = Arr::pluck($array, 'developer.name');

    // ['Taylor', 'Abigail']

You may also specify how you wish the resulting list to be keyed:

    use Illuminate\Support\Arr;

    $names = Arr::pluck($array, 'developer.name', 'developer.id');

    // [1 => 'Taylor', 2 => 'Abigail']

<a name="method-array-prepend"></a>
#### `Arr::prepend()` {.collection-method}

The `Arr::prepend` method will push an item onto the beginning of an array:

    use Illuminate\Support\Arr;

    $array = ['one', 'two', 'three', 'four'];

    $array = Arr::prepend($array, 'zero');

    // ['zero', 'one', 'two', 'three', 'four']

If needed, you may specify the key that should be used for the value:

    use Illuminate\Support\Arr;

    $array = ['price' => 100];

    $array = Arr::prepend($array, 'Desk', 'name');

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()` {.collection-method}

The `Arr::prependKeysWith` prepends all key names of an associative array with the given prefix:

    use Illuminate\Support\Arr;

    $array = [
        'name' => 'Desk',
        'price' => 100,
    ];

    $keyed = Arr::prependKeysWith($array, 'product.');

    /*
        [
            'product.name' => 'Desk',
            'product.price' => 100,
        ]
    */

<a name="method-array-pull"></a>
#### `Arr::pull()` {.collection-method}

The `Arr::pull` method returns and removes a key / value pair from an array:

    use Illuminate\Support\Arr;

    $array = ['name' => 'Desk', 'price' => 100];

    $name = Arr::pull($array, 'name');

    // $name: Desk

    // $array: ['price' => 100]

A default value may be passed as the third argument to the method. This value will be returned if the key doesn't exist:

    use Illuminate\Support\Arr;

    $value = Arr::pull($array, $key, $default);

<a name="method-array-query"></a>
#### `Arr::query()` {.collection-method}

The `Arr::query` method converts the array into a query string:

    use Illuminate\Support\Arr;

    $array = [
        'name' => 'Taylor',
        'order' => [
            'column' => 'created_at',
            'direction' => 'desc'
        ]
    ];

    Arr::query($array);

    // name=Taylor&order[column]=created_at&order[direction]=desc

<a name="method-array-random"></a>
#### `Arr::random()` {.collection-method}

The `Arr::random` method returns a random value from an array:

    use Illuminate\Support\Arr;

    $array = [1, 2, 3, 4, 5];

    $random = Arr::random($array);

    // 4 - (retrieved randomly)

You may also specify the number of items to return as an optional second argument. Note that providing this argument will return an array even if only one item is desired:

    use Illuminate\Support\Arr;

    $items = Arr::random($array, 2);

    // [2, 5] - (retrieved randomly)

<a name="method-array-set"></a>
#### `Arr::set()` {.collection-method}

The `Arr::set` method sets a value within a deeply nested array using "dot" notation:

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    Arr::set($array, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 200]]]

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()` {.collection-method}

The `Arr::shuffle` method randomly shuffles the items in the array:

    use Illuminate\Support\Arr;

    $array = Arr::shuffle([1, 2, 3, 4, 5]);

    // [3, 2, 5, 1, 4] - (generated randomly)

<a name="method-array-sort"></a>
#### `Arr::sort()` {.collection-method}

The `Arr::sort` method sorts an array by its values:

    use Illuminate\Support\Arr;

    $array = ['Desk', 'Table', 'Chair'];

    $sorted = Arr::sort($array);

    // ['Chair', 'Desk', 'Table']

You may also sort the array by the results of a given closure:

    use Illuminate\Support\Arr;

    $array = [
        ['name' => 'Desk'],
        ['name' => 'Table'],
        ['name' => 'Chair'],
    ];

    $sorted = array_values(Arr::sort($array, function (array $value) {
        return $value['name'];
    }));

    /*
        [
            ['name' => 'Chair'],
            ['name' => 'Desk'],
            ['name' => 'Table'],
        ]
    */

<a name="method-array-sort-desc"></a>
#### `Arr::sortDesc()` {.collection-method}

The `Arr::sortDesc` method sorts an array in descending order by its values:

    use Illuminate\Support\Arr;

    $array = ['Desk', 'Table', 'Chair'];

    $sorted = Arr::sortDesc($array);

    // ['Table', 'Desk', 'Chair']

You may also sort the array by the results of a given closure:

    use Illuminate\Support\Arr;

    $array = [
        ['name' => 'Desk'],
        ['name' => 'Table'],
        ['name' => 'Chair'],
    ];

    $sorted = array_values(Arr::sortDesc($array, function (array $value) {
        return $value['name'];
    }));

    /*
        [
            ['name' => 'Table'],
            ['name' => 'Desk'],
            ['name' => 'Chair'],
        ]
    */

<a name="method-array-sort-recursive"></a>
#### `Arr::sortRecursive()` {.collection-method}

The `Arr::sortRecursive` method recursively sorts an array using the `sort` function for numerically indexed sub-arrays and the `ksort` function for associative sub-arrays:

    use Illuminate\Support\Arr;

    $array = [
        ['Roman', 'Taylor', 'Li'],
        ['PHP', 'Ruby', 'JavaScript'],
        ['one' => 1, 'two' => 2, 'three' => 3],
    ];

    $sorted = Arr::sortRecursive($array);

    /*
        [
            ['JavaScript', 'PHP', 'Ruby'],
            ['one' => 1, 'three' => 3, 'two' => 2],
            ['Li', 'Roman', 'Taylor'],
        ]
    */

If you would like the results sorted in descending order, you may use the `Arr::sortRecursiveDesc` method.

    $sorted = Arr::sortRecursiveDesc($array);

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()` {.collection-method}

The `Arr::toCssClasses` conditionally compiles a CSS class string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

    use Illuminate\Support\Arr;

    $isActive = false;
    $hasError = true;

    $array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

    $classes = Arr::toCssClasses($array);

    /*
        'p-4 bg-red'
    */

<a name="method-array-to-css-styles"></a>
#### `Arr::toCssStyles()` {.collection-method}

The `Arr::toCssStyles` conditionally compiles a CSS style string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

```php
$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

This method powers Laravel's functionality allowing [merging classes with a Blade component's attribute bag](/docs/{{version}}/blade#conditionally-merge-classes) as well as the `@class` [Blade directive](/docs/{{version}}/blade#conditional-classes).

<a name="method-array-undot"></a>
#### `Arr::undot()` {.collection-method}

The `Arr::undot` method expands a single-dimensional array that uses "dot" notation into a multi-dimensional array:

    use Illuminate\Support\Arr;

    $array = [
        'user.name' => 'Kevin Malone',
        'user.occupation' => 'Accountant',
    ];

    $array = Arr::undot($array);

    // ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]

<a name="method-array-where"></a>
#### `Arr::where()` {.collection-method}

The `Arr::where` method filters an array using the given closure:

    use Illuminate\Support\Arr;

    $array = [100, '200', 300, '400', 500];

    $filtered = Arr::where($array, function (string|int $value, int $key) {
        return is_string($value);
    });

    // [1 => '200', 3 => '400']

<a name="method-array-where-not-null"></a>
#### `Arr::whereNotNull()` {.collection-method}

The `Arr::whereNotNull` method removes all `null` values from the given array:

    use Illuminate\Support\Arr;

    $array = [0, null];

    $filtered = Arr::whereNotNull($array);

    // [0 => 0]

<a name="method-array-wrap"></a>
#### `Arr::wrap()` {.collection-method}

The `Arr::wrap` method wraps the given value in an array. If the given value is already an array it will be returned without modification:

    use Illuminate\Support\Arr;

    $string = 'Laravel';

    $array = Arr::wrap($string);

    // ['Laravel']

If the given value is `null`, an empty array will be returned:

    use Illuminate\Support\Arr;

    $array = Arr::wrap(null);

    // []

<a name="method-data-fill"></a>
#### `data_fill()` {.collection-method}

The `data_fill` function sets a missing value within a nested array or object using "dot" notation:

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_fill($data, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 100]]]

    data_fill($data, 'products.desk.discount', 10);

    // ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]

This function also accepts asterisks as wildcards and will fill the target accordingly:

    $data = [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2'],
        ],
    ];

    data_fill($data, 'products.*.price', 200);

    /*
        [
            'products' => [
                ['name' => 'Desk 1', 'price' => 100],
                ['name' => 'Desk 2', 'price' => 200],
            ],
        ]
    */

<a name="method-data-get"></a>
#### `data_get()` {.collection-method}

The `data_get` function retrieves a value from a nested array or object using "dot" notation:

    $data = ['products' => ['desk' => ['price' => 100]]];

    $price = data_get($data, 'products.desk.price');

    // 100

The `data_get` function also accepts a default value, which will be returned if the specified key is not found:

    $discount = data_get($data, 'products.desk.discount', 0);

    // 0

The function also accepts wildcards using asterisks, which may target any key of the array or object:

    $data = [
        'product-one' => ['name' => 'Desk 1', 'price' => 100],
        'product-two' => ['name' => 'Desk 2', 'price' => 150],
    ];

    data_get($data, '*.name');

    // ['Desk 1', 'Desk 2'];

<a name="method-data-set"></a>
#### `data_set()` {.collection-method}

The `data_set` function sets a value within a nested array or object using "dot" notation:

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_set($data, 'products.desk.price', 200);

    // ['products' => ['desk' => ['price' => 200]]]

This function also accepts wildcards using asterisks and will set values on the target accordingly:

    $data = [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2', 'price' => 150],
        ],
    ];

    data_set($data, 'products.*.price', 200);

    /*
        [
            'products' => [
                ['name' => 'Desk 1', 'price' => 200],
                ['name' => 'Desk 2', 'price' => 200],
            ],
        ]
    */

By default, any existing values are overwritten. If you wish to only set a value if it doesn't exist, you may pass `false` as the fourth argument to the function:

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_set($data, 'products.desk.price', 200, overwrite: false);

    // ['products' => ['desk' => ['price' => 100]]]

<a name="method-data-forget"></a>
#### `data_forget()` {.collection-method}

The `data_forget` function removes a value within a nested array or object using "dot" notation:

    $data = ['products' => ['desk' => ['price' => 100]]];

    data_forget($data, 'products.desk.price');

    // ['products' => ['desk' => []]]

This function also accepts wildcards using asterisks and will remove values on the target accordingly:

    $data = [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2', 'price' => 150],
        ],
    ];

    data_forget($data, 'products.*.price');

    /*
        [
            'products' => [
                ['name' => 'Desk 1'],
                ['name' => 'Desk 2'],
            ],
        ]
    */

<a name="method-head"></a>
#### `head()` {.collection-method}

The `head` function returns the first element in the given array:

    $array = [100, 200, 300];

    $first = head($array);

    // 100

<a name="method-last"></a>
#### `last()` {.collection-method}

The `last` function returns the last element in the given array:

    $array = [100, 200, 300];

    $last = last($array);

    // 300

<a name="paths"></a>
## Paths

<a name="method-app-path"></a>
#### `app_path()` {.collection-method}

The `app_path` function returns the fully qualified path to your application's `app` directory. You may also use the `app_path` function to generate a fully qualified path to a file relative to the application directory:

    $path = app_path();

    $path = app_path('Http/Controllers/Controller.php');

<a name="method-base-path"></a>
#### `base_path()` {.collection-method}

The `base_path` function returns the fully qualified path to your application's root directory. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory:

    $path = base_path();

    $path = base_path('vendor/bin');

<a name="method-config-path"></a>
#### `config_path()` {.collection-method}

The `config_path` function returns the fully qualified path to your application's `config` directory. You may also use the `config_path` function to generate a fully qualified path to a given file within the application's configuration directory:

    $path = config_path();

    $path = config_path('app.php');

<a name="method-database-path"></a>
#### `database_path()` {.collection-method}

The `database_path` function returns the fully qualified path to your application's `database` directory. You may also use the `database_path` function to generate a fully qualified path to a given file within the database directory:

    $path = database_path();

    $path = database_path('factories/UserFactory.php');

<a name="method-lang-path"></a>
#### `lang_path()` {.collection-method}

The `lang_path` function returns the fully qualified path to your application's `lang` directory. You may also use the `lang_path` function to generate a fully qualified path to a given file within the directory:

    $path = lang_path();

    $path = lang_path('en/messages.php');

> **Note**
> By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

<a name="method-mix"></a>
#### `mix()` {.collection-method}

The `mix` function returns the path to a [versioned Mix file](/docs/{{version}}/mix):

    $path = mix('css/app.css');

<a name="method-public-path"></a>
#### `public_path()` {.collection-method}

The `public_path` function returns the fully qualified path to your application's `public` directory. You may also use the `public_path` function to generate a fully qualified path to a given file within the public directory:

    $path = public_path();

    $path = public_path('css/app.css');

<a name="method-resource-path"></a>
#### `resource_path()` {.collection-method}

The `resource_path` function returns the fully qualified path to your application's `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file within the resources directory:

    $path = resource_path();

    $path = resource_path('sass/app.scss');

<a name="method-storage-path"></a>
#### `storage_path()` {.collection-method}

The `storage_path` function returns the fully qualified path to your application's `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file within the storage directory:

    $path = storage_path();

    $path = storage_path('app/file.txt');

<a name="urls"></a>
## URLs

<a name="method-action"></a>
#### `action()` {.collection-method}

The `action` function generates a URL for the given controller action:

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

If the method accepts route parameters, you may pass them as the second argument to the method:

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="method-asset"></a>
#### `asset()` {.collection-method}

The `asset` function generates a URL for an asset using the current scheme of the request (HTTP or HTTPS):

    $url = asset('img/photo.jpg');

You can configure the asset URL host by setting the `ASSET_URL` variable in your `.env` file. This can be useful if you host your assets on an external service like Amazon S3 or another CDN:

    // ASSET_URL=http://example.com/assets

    $url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg

<a name="method-route"></a>
#### `route()` {.collection-method}

The `route` function generates a URL for a given [named route](/docs/{{version}}/routing#named-routes):

    $url = route('route.name');

If the route accepts parameters, you may pass them as the second argument to the function:

    $url = route('route.name', ['id' => 1]);

By default, the `route` function generates an absolute URL. If you wish to generate a relative URL, you may pass `false` as the third argument to the function:

    $url = route('route.name', ['id' => 1], false);

<a name="method-secure-asset"></a>
#### `secure_asset()` {.collection-method}

The `secure_asset` function generates a URL for an asset using HTTPS:

    $url = secure_asset('img/photo.jpg');

<a name="method-secure-url"></a>
#### `secure_url()` {.collection-method}

The `secure_url` function generates a fully qualified HTTPS URL to the given path. Additional URL segments may be passed in the function's second argument:

    $url = secure_url('user/profile');

    $url = secure_url('user/profile', [1]);

<a name="method-to-route"></a>
#### `to_route()` {.collection-method}

The `to_route` function generates a [redirect HTTP response](/docs/{{version}}/responses#redirects) for a given [named route](/docs/{{version}}/routing#named-routes):

    return to_route('users.show', ['user' => 1]);

If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_route` method:

    return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);

<a name="method-url"></a>
#### `url()` {.collection-method}

The `url` function generates a fully qualified URL to the given path:

    $url = url('user/profile');

    $url = url('user/profile', [1]);

If no path is provided, an `Illuminate\Routing\UrlGenerator` instance is returned:

    $current = url()->current();

    $full = url()->full();

    $previous = url()->previous();

<a name="miscellaneous"></a>
## Miscellaneous

<a name="method-abort"></a>
#### `abort()` {.collection-method}

The `abort` function throws [an HTTP exception](/docs/{{version}}/errors#http-exceptions) which will be rendered by the [exception handler](/docs/{{version}}/errors#the-exception-handler):

    abort(403);

You may also provide the exception's message and custom HTTP response headers that should be sent to the browser:

    abort(403, 'Unauthorized.', $headers);

<a name="method-abort-if"></a>
#### `abort_if()` {.collection-method}

The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`:

    abort_if(! Auth::user()->isAdmin(), 403);

Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function.

<a name="method-abort-unless"></a>
#### `abort_unless()` {.collection-method}

The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`:

    abort_unless(Auth::user()->isAdmin(), 403);

Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function.

<a name="method-app"></a>
#### `app()` {.collection-method}

The `app` function returns the [service container](/docs/{{version}}/container) instance:

    $container = app();

You may pass a class or interface name to resolve it from the container:

    $api = app('HelpSpot\API');

<a name="method-auth"></a>
#### `auth()` {.collection-method}

The `auth` function returns an [authenticator](/docs/{{version}}/authentication) instance. You may use it as an alternative to the `Auth` facade:

    $user = auth()->user();

If needed, you may specify which guard instance you would like to access:

    $user = auth('admin')->user();

<a name="method-back"></a>
#### `back()` {.collection-method}

The `back` function generates a [redirect HTTP response](/docs/{{version}}/responses#redirects) to the user's previous location:

    return back($status = 302, $headers = [], $fallback = '/');

    return back();

<a name="method-bcrypt"></a>
#### `bcrypt()` {.collection-method}

The `bcrypt` function [hashes](/docs/{{version}}/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade:

    $password = bcrypt('my-secret-password');

<a name="method-blank"></a>
#### `blank()` {.collection-method}

The `blank` function determines whether the given value is "blank":

    blank('');
    blank('   ');
    blank(null);
    blank(collect());

    // true

    blank(0);
    blank(true);
    blank(false);

    // false

For the inverse of `blank`, see the [`filled`](#method-filled) method.

<a name="method-broadcast"></a>
#### `broadcast()` {.collection-method}

The `broadcast` function [broadcasts](/docs/{{version}}/broadcasting) the given [event](/docs/{{version}}/events) to its listeners:

    broadcast(new UserRegistered($user));

    broadcast(new UserRegistered($user))->toOthers();

<a name="method-cache"></a>
#### `cache()` {.collection-method}

The `cache` function may be used to get values from the [cache](/docs/{{version}}/cache). If the given key does not exist in the cache, an optional default value will be returned:

    $value = cache('key');

    $value = cache('key', 'default');

You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of seconds or duration the cached value should be considered valid:

    cache(['key' => 'value'], 300);

    cache(['key' => 'value'], now()->addSeconds(10));

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()` {.collection-method}

The `class_uses_recursive` function returns all traits used by a class, including traits used by all of its parent classes:

    $traits = class_uses_recursive(App\Models\User::class);

<a name="method-collect"></a>
#### `collect()` {.collection-method}

The `collect` function creates a [collection](/docs/{{version}}/collections) instance from the given value:

    $collection = collect(['taylor', 'abigail']);

<a name="method-config"></a>
#### `config()` {.collection-method}

The `config` function gets the value of a [configuration](/docs/{{version}}/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. A default value may be specified and is returned if the configuration option does not exist:

    $value = config('app.timezone');

    $value = config('app.timezone', $default);

You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values:

    config(['app.debug' => true]);

<a name="method-cookie"></a>
#### `cookie()` {.collection-method}

The `cookie` function creates a new [cookie](/docs/{{version}}/requests#cookies) instance:

    $cookie = cookie('name', 'value', $minutes);

<a name="method-csrf-field"></a>
#### `csrf_field()` {.collection-method}

The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/{{version}}/blade):

    {{ csrf_field() }}

<a name="method-csrf-token"></a>
#### `csrf_token()` {.collection-method}

The `csrf_token` function retrieves the value of the current CSRF token:

    $token = csrf_token();

<a name="method-decrypt"></a>
#### `decrypt()` {.collection-method}

The `decrypt` function [decrypts](/docs/{{version}}/encryption) the given value. You may use this function as an alternative to the `Crypt` facade:

    $password = decrypt($value);

<a name="method-dd"></a>
#### `dd()` {.collection-method}

The `dd` function dumps the given variables and ends the execution of the script:

    dd($value);

    dd($value1, $value2, $value3, ...);

If you do not want to halt the execution of your script, use the [`dump`](#method-dump) function instead.

<a name="method-dispatch"></a>
#### `dispatch()` {.collection-method}

The `dispatch` function pushes the given [job](/docs/{{version}}/queues#creating-jobs) onto the Laravel [job queue](/docs/{{version}}/queues):

    dispatch(new App\Jobs\SendEmails);

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()` {.collection-method}

The `dispatch_sync` function pushes the given job to the [sync](/docs/{{version}}/queues#synchronous-dispatching) queue so that it is processed immediately:

    dispatch_sync(new App\Jobs\SendEmails);

<a name="method-dump"></a>
#### `dump()` {.collection-method}

The `dump` function dumps the given variables:

    dump($value);

    dump($value1, $value2, $value3, ...);

If you want to stop executing the script after dumping the variables, use the [`dd`](#method-dd) function instead.

<a name="method-encrypt"></a>
#### `encrypt()` {.collection-method}

The `encrypt` function [encrypts](/docs/{{version}}/encryption) the given value. You may use this function as an alternative to the `Crypt` facade:

    $secret = encrypt('my-secret-value');

<a name="method-env"></a>
#### `env()` {.collection-method}

The `env` function retrieves the value of an [environment variable](/docs/{{version}}/configuration#environment-configuration) or returns a default value:

    $env = env('APP_ENV');

    $env = env('APP_ENV', 'production');

> **Warning**  
> If you execute the `config:cache` command during your deployment process, you should be sure that you are only calling the `env` function from within your configuration files. Once the configuration has been cached, the `.env` file will not be loaded and all calls to the `env` function will return `null`.

<a name="method-event"></a>
#### `event()` {.collection-method}

The `event` function dispatches the given [event](/docs/{{version}}/events) to its listeners:

    event(new UserRegistered($user));

<a name="method-fake"></a>
#### `fake()` {.collection-method}

The `fake` function resolves a [Faker](https://github.com/FakerPHP/Faker) singleton from the container, which can be useful when creating fake data in model factories, database seeding, tests, and prototyping views:

```blade
@for($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

By default, the `fake` function will utilize the `app.faker_locale` configuration option in your `config/app.php` configuration file; however, you may also specify the locale by passing it to the `fake` function. Each locale will resolve an individual singleton:

    fake('nl_NL')->name()

<a name="method-filled"></a>
#### `filled()` {.collection-method}

The `filled` function determines whether the given value is not "blank":

    filled(0);
    filled(true);
    filled(false);

    // true

    filled('');
    filled('   ');
    filled(null);
    filled(collect());

    // false

For the inverse of `filled`, see the [`blank`](#method-blank) method.

<a name="method-info"></a>
#### `info()` {.collection-method}

The `info` function will write information to your application's [log](/docs/{{version}}/logging):

    info('Some helpful information!');

An array of contextual data may also be passed to the function:

    info('User login attempt failed.', ['id' => $user->id]);

<a name="method-logger"></a>
#### `logger()` {.collection-method}

The `logger` function can be used to write a `debug` level message to the [log](/docs/{{version}}/logging):

    logger('Debug message');

An array of contextual data may also be passed to the function:

    logger('User has logged in.', ['id' => $user->id]);

A [logger](/docs/{{version}}/errors#logging) instance will be returned if no value is passed to the function:

    logger()->error('You are not allowed here.');

<a name="method-method-field"></a>
#### `method_field()` {.collection-method}

The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/{{version}}/blade):

    <form method="POST">
        {{ method_field('DELETE') }}
    </form>

<a name="method-now"></a>
#### `now()` {.collection-method}

The `now` function creates a new `Illuminate\Support\Carbon` instance for the current time:

    $now = now();

<a name="method-old"></a>
#### `old()` {.collection-method}

The `old` function [retrieves](/docs/{{version}}/requests#retrieving-input) an [old input](/docs/{{version}}/requests#old-input) value flashed into the session:

    $value = old('value');

    $value = old('value', 'default');

Since the "default value" provided as the second argument to the `old` function is often an attribute of an Eloquent model, Laravel allows you to simply pass the entire Eloquent model as the second argument to the `old` function. When doing so, Laravel will assume the first argument provided to the `old` function is the name of the Eloquent attribute that should be considered the "default value":

    {{ old('name', $user->name) }}

    // Is equivalent to...

    {{ old('name', $user) }}

<a name="method-optional"></a>
#### `optional()` {.collection-method}

The `optional` function accepts any argument and allows you to access properties or call methods on that object. If the given object is `null`, properties and methods will return `null` instead of causing an error:

    return optional($user->address)->street;

    {!! old('name', optional($user)->name) !!}

The `optional` function also accepts a closure as its second argument. The closure will be invoked if the value provided as the first argument is not null:

    return optional(User::find($id), function (User $user) {
        return $user->name;
    });

<a name="method-policy"></a>
#### `policy()` {.collection-method}

The `policy` method retrieves a [policy](/docs/{{version}}/authorization#creating-policies) instance for a given class:

    $policy = policy(App\Models\User::class);

<a name="method-redirect"></a>
#### `redirect()` {.collection-method}

The `redirect` function returns a [redirect HTTP response](/docs/{{version}}/responses#redirects), or returns the redirector instance if called with no arguments:

    return redirect($to = null, $status = 302, $headers = [], $https = null);

    return redirect('/home');

    return redirect()->route('route.name');

<a name="method-report"></a>
#### `report()` {.collection-method}

The `report` function will report an exception using your [exception handler](/docs/{{version}}/errors#the-exception-handler):

    report($e);

The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message:

    report('Something went wrong.');

<a name="method-report-if"></a>
#### `report_if()` {.collection-method}

The `report_if` function will report an exception using your [exception handler](/docs/{{version}}/errors#the-exception-handler) if the given condition is `true`:

    report_if($shouldReport, $e);

    report_if($shouldReport, 'Something went wrong.');

<a name="method-report-unless"></a>
#### `report_unless()` {.collection-method}

The `report_unless` function will report an exception using your [exception handler](/docs/{{version}}/errors#the-exception-handler) if the given condition is `false`:

    report_unless($reportingDisabled, $e);

    report_unless($reportingDisabled, 'Something went wrong.');

<a name="method-request"></a>
#### `request()` {.collection-method}

The `request` function returns the current [request](/docs/{{version}}/requests) instance or obtains an input field's value from the current request:

    $request = request();

    $value = request('key', $default);

<a name="method-rescue"></a>
#### `rescue()` {.collection-method}

The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/{{version}}/errors#the-exception-handler); however, the request will continue processing:

    return rescue(function () {
        return $this->method();
    });

You may also pass a second argument to the `rescue` function. This argument will be the "default" value that should be returned if an exception occurs while executing the closure:

    return rescue(function () {
        return $this->method();
    }, false);

    return rescue(function () {
        return $this->method();
    }, function () {
        return $this->failure();
    });

A `report` argument may be provided to the `rescue` function to determine if the exception should be reported via the `report` function:

    return rescue(function () {
        return $this->method();
    }, report: function (Throwable $throwable) {
        return $throwable instanceof InvalidArgumentException;
    });

<a name="method-resolve"></a>
#### `resolve()` {.collection-method}

The `resolve` function resolves a given class or interface name to an instance using the [service container](/docs/{{version}}/container):

    $api = resolve('HelpSpot\API');

<a name="method-response"></a>
#### `response()` {.collection-method}

The `response` function creates a [response](/docs/{{version}}/responses) instance or obtains an instance of the response factory:

    return response('Hello World', 200, $headers);

    return response()->json(['foo' => 'bar'], 200, $headers);

<a name="method-retry"></a>
#### `retry()` {.collection-method}

The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, its return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown:

    return retry(5, function () {
        // Attempt 5 times while resting 100ms between attempts...
    }, 100);

If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the third argument to the `retry` function:

    use Exception;

    return retry(5, function () {
        // ...
    }, function (int $attempt, Exception $exception) {
        return $attempt * 100;
    });

For convenience, you may provide an array as the first argument to the `retry` function. This array will be used to determine how many milliseconds to sleep between subsequent attempts:

    return retry([100, 200], function () {
        // Sleep for 100ms on first retry, 200ms on second retry...
    });

To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function:

    use Exception;

    return retry(5, function () {
        // ...
    }, 100, function (Exception $exception) {
        return $exception instanceof RetryException;
    });

<a name="method-session"></a>
#### `session()` {.collection-method}

The `session` function may be used to get or set [session](/docs/{{version}}/session) values:

    $value = session('key');

You may set values by passing an array of key / value pairs to the function:

    session(['chairs' => 7, 'instruments' => 3]);

The session store will be returned if no value is passed to the function:

    $value = session()->get('key');

    session()->put('key', $value);

<a name="method-tap"></a>
#### `tap()` {.collection-method}

The `tap` function accepts two arguments: an arbitrary `$value` and a closure. The `$value` will be passed to the closure and then be returned by the `tap` function. The return value of the closure is irrelevant:

    $user = tap(User::first(), function (User $user) {
        $user->name = 'taylor';

        $user->save();
    });

If no closure is passed to the `tap` function, you may call any method on the given `$value`. The return value of the method you call will always be `$value`, regardless of what the method actually returns in its definition. For example, the Eloquent `update` method typically returns an integer. However, we can force the method to return the model itself by chaining the `update` method call through the `tap` function:

    $user = tap($user)->update([
        'name' => $name,
        'email' => $email,
    ]);

To add a `tap` method to a class, you may add the `Illuminate\Support\Traits\Tappable` trait to the class. The `tap` method of this trait accepts a Closure as its only argument. The object instance itself will be passed to the Closure and then be returned by the `tap` method:

    return $user->tap(function (User $user) {
        // ...
    });

<a name="method-throw-if"></a>
#### `throw_if()` {.collection-method}

The `throw_if` function throws the given exception if a given boolean expression evaluates to `true`:

    throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

    throw_if(
        ! Auth::user()->isAdmin(),
        AuthorizationException::class,
        'You are not allowed to access this page.'
    );

<a name="method-throw-unless"></a>
#### `throw_unless()` {.collection-method}

The `throw_unless` function throws the given exception if a given boolean expression evaluates to `false`:

    throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

    throw_unless(
        Auth::user()->isAdmin(),
        AuthorizationException::class,
        'You are not allowed to access this page.'
    );

<a name="method-today"></a>
#### `today()` {.collection-method}

The `today` function creates a new `Illuminate\Support\Carbon` instance for the current date:

    $today = today();

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()` {.collection-method}

The `trait_uses_recursive` function returns all traits used by a trait:

    $traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);

<a name="method-transform"></a>
#### `transform()` {.collection-method}

The `transform` function executes a closure on a given value if the value is not [blank](#method-blank) and then returns the return value of the closure:

    $callback = function (int $value) {
        return $value * 2;
    };

    $result = transform(5, $callback);

    // 10

A default value or closure may be passed as the third argument to the function. This value will be returned if the given value is blank:

    $result = transform(null, $callback, 'The value is blank');

    // The value is blank

<a name="method-validator"></a>
#### `validator()` {.collection-method}

The `validator` function creates a new [validator](/docs/{{version}}/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade:

    $validator = validator($data, $rules, $messages);

<a name="method-value"></a>
#### `value()` {.collection-method}

The `value` function returns the value it is given. However, if you pass a closure to the function, the closure will be executed and its returned value will be returned:

    $result = value(true);

    // true

    $result = value(function () {
        return false;
    });

    // false
    
Additional arguments may be passed to the `value` function. If the first argument is a closure then the additional parameters will be passed to the closure as arguments, otherwise they will be ignored:

    $result = value(function (string $name) {
        return $name;
    }, 'Taylor');
    
    // 'Taylor'

<a name="method-view"></a>
#### `view()` {.collection-method}

The `view` function retrieves a [view](/docs/{{version}}/views) instance:

    return view('auth.login');

<a name="method-with"></a>
#### `with()` {.collection-method}

The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned:

    $callback = function (mixed $value) {
        return is_numeric($value) ? $value * 2 : 0;
    };

    $result = with(5, $callback);

    // 10

    $result = with(null, $callback);

    // 0

    $result = with(5, null);

    // 5

<a name="other-utilities"></a>
## Other Utilities

<a name="benchmarking"></a>
### Benchmarking

Sometimes you may wish to quickly test the performance of certain parts of your application. On those occasions, you may utilize the `Benchmark` support class to measure the number of milliseconds it takes for the given callbacks to complete:

    <?php

    use App\Models\User;
    use Illuminate\Support\Benchmark;

    Benchmark::dd(fn () => User::find(1)); // 0.1 ms

    Benchmark::dd([
        'Scenario 1' => fn () => User::count(), // 0.5 ms
        'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
    ]);

By default, the given callbacks will be executed once (one iteration), and their duration will be displayed in the browser / console.

To invoke a callback more than once, you may specify the number of iterations that the callback should be invoked as the second argument to the method. When executing a callback more than once, the `Benchmark` class will return the average amount of milliseconds it took to execute the callback across all iterations:

    Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms

Sometimes, you may want to benchmark the execution of a callback while still obtaining the value returned by the callback. The `value` method will return a tuple containing the value returned by the callback and the amount of milliseconds it took to execute the callback:

    [$count, $duration] = Benchmark::value(fn () => User::count());

<a name="dates"></a>
### Dates

Laravel includes [Carbon](https://carbon.nesbot.com/docs/), a powerful date and time manipulation library. To create a new `Carbon` instance, you may invoke the `now` function. This function is globally available within your Laravel application:

```php
$now = now();
```

Or, you may create a new `Carbon` instance using the `Illuminate\Support\Carbon` class:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

For a thorough discussion of Carbon and its features, please consult the [official Carbon documentation](https://carbon.nesbot.com/docs/).

<a name="lottery"></a>
### Lottery

Laravel's lottery class may be used to execute callbacks based on a set of given odds. This can be particularly useful when you only want to execute code for a percentage of your incoming requests:

    use Illuminate\Support\Lottery;

    Lottery::odds(1, 20)
        ->winner(fn () => $user->won())
        ->loser(fn () => $user->lost())
        ->choose();

You may combine Laravel's lottery class with other Laravel features. For example, you may wish to only report a small percentage of slow queries to your exception handler. And, since the lottery class is callable, we may pass an instance of the class into any method that accepts callables:

    use Carbon\CarbonInterval;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Lottery;

    DB::whenQueryingForLongerThan(
        CarbonInterval::seconds(2),
        Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
    );

<a name="testing-lotteries"></a>
#### Testing Lotteries

Laravel provides some simple methods to allow you to easily test your application's lottery invocations:

    // Lottery will always win...
    Lottery::alwaysWin();

    // Lottery will always lose...
    Lottery::alwaysLose();

    // Lottery will win then lose, and finally return to normal behavior...
    Lottery::fix([true, false]);

    // Lottery will return to normal behavior...
    Lottery::determineResultsNormally();

<a name="pipeline"></a>
### Pipeline

Laravel's `Pipeline` facade provides a convenient way to "pipe" a given input through a series of invokable classes, closures, or callables, giving each class the opportunity to inspect or modify the input and invoke the next callable in the pipeline:

```php
use Closure;
use App\Models\User;
use Illuminate\Support\Facades\Pipeline;

$user = Pipeline::send($user)
            ->through([
                function (User $user, Closure $next) {
                    // ...

                    return $next($user);
                },
                function (User $user, Closure $next) {
                    // ...

                    return $next($user);
                },
            ])
            ->then(fn (User $user) => $user);
```

As you can see, each invokable class or closure in the pipeline is provided the input and a `$next` closure. Invoking the `$next` closure will invoke the next callable in the pipeline. As you may have noticed, this is very similar to [middleware](/docs/{{version}}/middleware).

When the last callable in the pipeline invokes the `$next` closure, the callable provided to the `then` method will be invoked. Typically, this callable will simply return the given input.

Of course, as discussed previously, you are not limited to providing closures to your pipeline. You may also provide invokable classes. If a class name is provided, the class will be instantiated via Laravel's [service container](/docs/{{version}}/container), allowing dependencies to be injected into the invokable class:

```php
$user = Pipeline::send($user)
            ->through([
                GenerateProfilePhoto::class,
                ActivateSubscription::class,
                SendWelcomeEmail::class,
            ])
            ->then(fn (User $user) => $user);
```

<a name="sleep"></a>
### Sleep

Laravel's `Sleep` class is a light-weight wrapper around PHP's native `sleep` and `usleep` functions, offering greater testability while also exposing a developer friendly API for working with time:

    use Illuminate\Support\Sleep;

    $waiting = true;

    while ($waiting) {
        Sleep::for(1)->second();

        $waiting = /* ... */;
    }

The `Sleep` class offers a variety of methods that allow you to work with different units of time:

    // Pause execution for 90 seconds...
    Sleep::for(1.5)->minutes();

    // Pause execution for 2 seconds...
    Sleep::for(2)->seconds();

    // Pause execution for 500 milliseconds...
    Sleep::for(500)->milliseconds();

    // Pause execution for 5,000 microseconds...
    Sleep::for(5000)->microseconds();

    // Pause execution until a given time...
    Sleep::until(now()->addMinute());

    // Alias of PHP's native "sleep" function...
    Sleep::sleep(2);

    // Alias of PHP's native "usleep" function...
    Sleep::usleep(5000);

To easily combine units of time, you may use the `and` method:

    Sleep::for(1)->second()->and(10)->milliseconds();

<a name="testing-sleep"></a>
#### Testing Sleep

When testing code that utilizes the `Sleep` class or PHP's native sleep functions, your test will pause execution. As you might expect, this makes your test suite significantly slower. For example, imagine you are testing the following code:

    $waiting = /* ... */;

    $seconds = 1;

    while ($waiting) {
        Sleep::for($seconds++)->seconds();

        $waiting = /* ... */;
    }

Typically, testing this code would take _at least_ one second. Luckily, the `Sleep` class allows us to "fake" sleeping so that our test suite stays fast:

    public function test_it_waits_until_ready()
    {
        Sleep::fake();

        // ...
    }

When faking the `Sleep` class, the actual execution pause is by-passed, leading to a substantially faster test.

Once the `Sleep` class has been faked, it is possible to make assertions against the expected "sleeps" that should have occurred. To illustrate this, let's imagine we are testing code that pauses execution three times, with each pause increasing by a single second. Using the `assertSequence` method, we can assert that our code "slept" for the proper amount of time while keeping our test fast:

    public function test_it_checks_if_ready_four_times()
    {
        Sleep::fake();

        // ...

        Sleep::assertSequence([
            Sleep::for(1)->second(),
            Sleep::for(2)->seconds(),
            Sleep::for(3)->seconds(),
        ]);
    }

Of course, the `Sleep` class offers a variety of other assertions you may use when testing:

    use Carbon\CarbonInterval as Duration;
    use Illuminate\Support\Sleep;

    // Assert that sleep was called 3 times...
    Sleep::assertSleptTimes(3);

    // Assert against the duration of sleep...
    Sleep::assertSlept(function (Duration $duration): bool {
        return /* ... */;
    }, times: 1);

    // Assert that the Sleep class was never invoked...
    Sleep::assertNeverSlept();

    // Assert that, even if Sleep was called, no execution paused occurred...
    Sleep::assertInsomniac();

Sometimes it may be useful to perform an action whenever a fake sleep occurs in your application code. To achieve this, you may provide a callback to the `whenFakingSleep` method. In the following example, we use Laravel's [time manipulation helpers](/docs/{{version}}/mocking#interacting-with-time) to instantly progress time by the duration of each sleep:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Progress time when faking sleep...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

Laravel uses the `Sleep` class internally whenever it is pausing execution. For example, the [`retry`](#method-retry) helper uses the `Sleep` class when sleeping, allowing for improved testability when using that helper.
