# Collections

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
- [Available Methods](#available-methods)

<a name="introduction"></a>
## Introduction

The `Illuminate\Support\Collection` class provides a fluent, convenient wrapper for working with arrays of data. For example, check out the following code. We'll use the `collect` helper to create a new collection instance from the array:

	$collection = collect(['taylor', 'abigail', null])->map(function($name)
	{
		return strtoupper($name);
	})
	->reject(function($name)
	{
		return empty($name);
	});


As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, every `Collection` method returns an entirely new `Collection` instance. To dig in further, keep reading!

<a name="basic-usage"></a>
## Basic Usage

#### Creating Collections

As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. You may also use the `make` command on the `Collection` class:

	$collection = collect([1, 2, 3]);

	$collection = Collection::make([1, 2, 3]);

Of course, collections of [Eloquent](/docs/{{version}}/eloquent) objects are always returned as `Collection` instances; however, you should feel free to use the `Collection` class wherever it is convenient for your application.

<a name="available-methods"></a>
## Available Methods

Here is a list of all the methods the `Collection` makes available:

- [`all`](#method-all)
- [`chunk`](#method-chunk)
- [`collapse`](#method-collapse)
- [`contains`](#method-contains)
- [`count`](#method-count)
- [`diff`](#method-diff)
- [`each`](#method-each)
- [`filter`](#method-filter)
- [`first`](#method-first)
- [`flatten`](#method-flatten)
- [`flip`](#method-flip)
- [`forget`](#method-forget)
- [`forPage`](#method-forpage)
- [`get`](#method-get)
- [`groupBy`](#method-groupby)
- [`has`](#method-has)
- [`implode`](#method-implode)
- [`intersect`](#method-intersect)
- [`isEmpty`](#method-isempty)
- [`keyBy`](#method-keyby)
- [`keys`](#method-keys)
- [`last`](#method-last)
- [`map`](#method-map)
- [`merge`](#method-merge)
- [`pluck`](#method-pluck)
- [`pop`](#method-pop)
- [`prepend`](#method-prepend)
- [`pull`](#method-pull)
- [`push`](#method-push)
- [`put`](#method-put)
- [`random`](#method-random)
- [`reduce`](#method-reduce)
- [`reject`](#method-reject)
- [`reverse`](#method-reverse)
- [`search`](#method-search)
- [`shift`](#method-shift)
- [`shuffle`](#method-shuffle)
- [`slice`](#method-slice)
- [`sort`](#method-sort)
- [`sortBy`](#method-sortby)
- [`sortByDesc`](#method-sortbydesc)
- [`splice`](#method-splice)
- [`sum`](#method-sum)
- [`take`](#method-take)
- [`toArray`](#method-toarray)
- [`toJson`](#method-tojson)
- [`transform`](#method-transform)
- [`unique`](#method-unique)
- [`values`](#method-values)
- [`where`](#method-where)
- [`whereLoose`](#method-whereloose)
- [`zip`](#method-zip)

<a name="method-all"></a>
#### `all`

Returns the underlying plain array:

	collect([1, 2, 3])->all();

	// [1, 2, 3]

> **Note:** This returns the underlying array as is. To convert all of the array's values to an array as well, use the [`toArray`](#method-toarray) method.

<a name="method-chunk"></a>
#### `chunk`

Chunks up the collection into smaller-chunked collections:

	$collection = collect([1, 2, 3, 4, 5, 6, 7])->chunk(4);

	$collection->toArray();

	// [[1, 2, 3, 4], [5, 6, 7]]

This is especially useful in your [views](/docs/{{version}}/views), when working with a grid system such as [bootstrap](http://getbootstrap.com/css/#grid). Imagine you have an [Eloquent](/docs/{{version}}/eloquent) collection of products which you want to display in a grid:

	@foreach ($products->chunk(3) as $chunk)
		<div class="row">
			@foreach ($chunk as $product)
				<div class="col-xs-4">{{ $product->name }}</div>
			@endforeach
		</div>
	@endforeach

That was easy!

<a name="method-collapse"></a>
#### `collapse`

Collapses a collection of arrays into a flat collection:

	$collection = collect([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

	$collapsed = $collection->collapse();

	$collapsed->all();

	// [1, 2, 3, 4, 5, 6, 7, 8, 9]

You can think of it as the inverse of the `chunk` method.

<a name="method-contains"></a>
#### `contains`

Checks whether the collection contains a given item:

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$collection->contains('laravel'); // true

	$collection->contains('codeigniter'); // false

You may optionally pass a value as well, and it'll check if the given key value pair exists:

	$collection = collect([
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'jeffrey', 'last' => 'way'],
	]);

	$collection->contains('first', 'otwell'); // false

Alternatively, you may pass a callback to `contains` to run your own checks:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->contains(function($key, $value)
	{
		return $value > 5;
	});

	// false

<a name="method-count"></a>
#### `count`

Returns the total amount of items in the collection:

	$collection = collect(['taylor', 'abigail', 'dayle', 'jeffrey']);

	$collection->count();

	// 4

<a name="method-diff"></a>
#### `diff`

Compares the collection against a different collection or plain array:

	$collection = collect([1, 2, 3, 4, 5]);

	$diff = $collection->diff([2, 4, 6, 8]);

	$diff->all();

	// [1, 3, 5]

<a name="method-each"></a>
#### `each`

Iterate over the items in the collection, calling the given callback for each item in the collection:

	$collection->each(function($item, $key)
	{
		// return false to stop
	});

To break out of the loop at any time, return `false` from your callback.

<a name="method-filter"></a>
#### `filter`

Filters the collection by the given callback, keeping only those items for which the callback returns `true`:

	$collection = collect([1, 2, 3, 4]);

	$filtered = $collection->filter(function($item)
	{
		return $item > 2;
	});

	$filtered->all();

	// [3, 4]

For the inverse of `filter`, see [`reject`](#method-reject).

<a name="method-first"></a>
#### `first`

Returns the first element in the collection. If the collection is empty, `null` is returned. You may optionally pass a callback to determine which item is actually returned:

	collect([1, 2, 3, 4])->first(function($item)
	{
		return $item > 2;
	});

	// 3

You may optionally pass a second argument, which is returned if no matching items are found.

<a name="method-flatten"></a>
#### `flatten`

Flattens a multi-dimensional collection into a single level:

	$collection = collect(['name' => 'taylor', 'languages' => ['php', 'javascript']]);

	$flattened = $collection->flatten();

	$flattened->all();

	// ['taylor', 'php', 'javascript'];

<a name="method-flip"></a>
#### `flip`

Swaps the collection's keys with their respective values:

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$flipped = $collection->flip();

	$flipped->all();

	// ['taylor' => 'name', 'laravel' => 'framework']

<a name="method-forget"></a>
#### `forget`

Removes an item from the collection by its key:

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$collection->forget('name');

	$collection->all();

	// ['laravel' => 'framework']

> **Note:** Unlike most other collection methods, `forget` does not return a new modified collection; it changes the actual collection it is called on.

<a name="method-forpage"></a>
#### `forPage`

A convenient way to extract part of a collection for a given chunk:

	$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9])->forPage(2, 3);

	$collection->all();

	// [4, 5, 6]

Think of this as `$collection->chunk(3)[1]`, just more elegant (and more efficient).

<a name="method-get"></a>
#### `get`

Returns the item at the given key. If the key does not exist, `null` is returned. You may optionally pass a second argument, to be used as the default when the key does not exist:

	$collection = collect(['name' => 'taylor', 'framework' => 'otwell']);

	$collection->get('email', 'placeholder@email.com');

	// placeholder@email.com

You may even pass a callback as the default value. The result of the callback will be returned if the specified key does not exist:

	$collection->get('email', function()
	{
		return 'placeholder@email.com';
	});

	// placeholder@email.com

<a name="method-groupby"></a>
#### `groupBy`

Groups the items by the specified key:

	$collection = collect([
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'abigail', 'last' => 'otwell'],
		['first' => 'jeffery', 'last' => 'way'],
		['first' => 'allie', 'last' => 'way'],
	]);

	$grouped = $collection->groupBy('last');

	$grouped->toArray();

	/*
		[
			'otwell' => [
				['first' => 'taylor', 'last' => 'otwell'],
				['first' => 'abigail', 'last' => 'otwell'],
			],
			'way' => [
				['first' => 'jeffery', 'last' => 'way'],
				['first' => 'allie', 'last' => 'way'],
			],
		]
	*/

Of course, you may pass a callback instead, which is used to determine the grouping:

	$grouped = $collection->groupBy(function($item, $key)
	{
		return substr($item['first'], 0, 1);
	});

	$grouped->toArray();

	/*
		[
			'a' => [
				['first' => 'abigail', 'last' => 'otwell'],
				['first' => 'allie', 'last' => 'way'],
			],
			't' => [
				['first' => 'taylor', 'last' => 'otwell'],
			],
			'j' => [
				['first' => 'jeffery', 'last' => 'way'],
			],
		]
	*/

<a name="method-has"></a>
#### `has`

Determines if an item exists in the collection at the given key:

	$collection = collect(['first' => 'taylor', 'last' => 'otwell']);

	$collection->has('email');

	// false

<a name="method-implode"></a>
#### `implode`

Joins the items in the collection. The arguments it takes depends on the type of items in the collection. If it's a collection of arrays or objects, pass the key for the attribute you want extracted:

	$collection = collect([
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'abigail', 'last' => 'otwell'],
	]);

	$collection->implode('first');

	// 'taylorabigail'

You may optionally pass a second argument, which is used as the "glue" to connect the individual pieces:

	$collection->implode('first', ', ');

	// 'taylor, abigail'

If the collection contains simple strings or numbers, just pass it the "glue" as the first argument directly:

	collect([1, 2, 3, 4, 5])->implode('-');

	// '1-2-3-4-5'

<a name="method-intersect"></a>
#### `intersect`

Filters the items in the collection, excluding any values not present in the given array/collection:

	$collection = collect(['taylor', 'abigail', 'jeffrey']);

	$intersect = $collection->intersect(['jeffrey', 'dayle', 'taylor']);

	$intersect->all();

	// [0 => 'taylor', 2 => 'jeffrey']

As you can see, the result will keep the original keys in place.

<a name="method-isempty"></a>
#### `isEmpty`

Checks whether there are no items in the collection:

	collect([])->isEmpty() // true

<a name="method-keyby"></a>
#### `keyBy`

Keys the collection by the given key:

	$collection = collect([
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'abigail', 'last' => 'otwell'],
	]);

	$keyed = $collection->keyBy('first');

	$keyed->all();

	/*
		[
			'taylor' => ['first' => 'taylor', 'last' => 'otwell'],
			'abigail' => ['first' => 'abigail', 'last' => 'otwell'],
		]
	*/

Of course, you may pass in your own callback to determine the key to be used:

	$keyed = $collection->keyBy(function($item)
	{
		return $item['first'].'-'.$item['last'];
	});

	$keyed->all();

	/*
		[
			'taylor-otwell' => ['first' => 'taylor', 'last' => 'otwell'],
			'abigail-otwell' => ['first' => 'abigail', 'last' => 'otwell'],
		]
	*/


<a name="method-keys"></a>
#### `keys`

Returns the collection's keys:

	$collection = collect([
		'taylor' => ['first' => 'taylor', 'last' => 'otwell'],
		'abigail' => ['first' => 'abigail', 'last' => 'otwell'],
	]);

	$keys = $collection->keys();

	$keys->all();

	// ['taylor', 'abigail']

<a name="method-last"></a>
#### `last`

Returns the last item in the collection:

	collect([1, 2, 3, 4, 5])->last();

	// 5

<a name="method-map"></a>
#### `map`

Calls the given callback on every item in the collection, and returns a new collection with those items:

	$collection = collect([1, 2, 3, 4, 5]);

	$multiplied = $collection->map(function($item, $key)
	{
		return $item * 2;
	});

	$multiplied->all();

	// [2, 4, 6, 8, 10]

> **Note:** Like most other collection methods, `map` returns a new modified collection; it does not change the actual collection it is called on. If you want to transform the actual collection itself, use the [`transform`](#method-transform) method.

<a name="method-merge"></a>
#### `merge`

Merges the given array into the collection. Any string key in the given array matching a string key in the collection will overwrite the value in the collection:

	$collection = collect(['first' => 'taylor', 'state' => 'arkansas']);

	$merged = $collection->merge(['first' => 'abigail', 'last' => 'otwell']);

	$merged->all();

	// ['first' => 'abigail', 'state' => 'arkansas', 'last' => 'otwell']

If the given array's keys are numeric, only the values will be added:

	$collection = collect(['taylor', 'otwell']);

	$merged = $collection->merge(['abigail', 'otwell']);

	$merged->all();

	// ['taylor', 'otwell', 'abigail', 'otwell']

<a name="method-pluck"></a>
#### `pluck`

Uses the given key to get a value from each item in the collection:

	$collection = collect([
		['name' => 'taylor', 'project' => 'laravel'],
		['name' => 'jeffrey', 'project' => 'laracasts'],
	]);

	$plucked = $collection->pluck('project');

	$plucked->all();

	// ['laravel', 'laracasts']

You may optionally pass a second argument, to be used to pluck the key from the items in the collection:

	$plucked = $collection->pluck('project', 'name');

	$plucked->all();

	// ['taylor' => 'laravel', 'jeffrey' => 'laracasts']

<a name="method-pop"></a>
#### `pop`

Removes the last item in the collection, and returns it:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->pop();

	// 5

	$collection->all();

	// [1, 2, 3, 4]

<a name="method-prepend"></a>
#### `prepend`

Adds an item to the beginning of the collection:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->prepend(0);

	$collection->all();

	// [0, 1, 2, 3, 4, 5]

<a name="method-pull"></a>
#### `pull`

Removes an item from the collection by its key, and returns it:

	$collection = collect(['first' => 'taylor', 'last' => 'otwell']);

	$collection->pull('first');

	// 'taylor'

	$collection->all();

	// ['last' => 'otwell']

<a name="method-push"></a>
#### `push`

Pushes an item onto the end of the collection:

	$collection = collect([1, 2, 3, 4]);

	$collection->push(5);

	$collection->all();

	// [1, 2, 3, 4, 5]

<a name="method-put"></a>
#### `put`

Sets the value at the given key:

	$collection = collect(['first' => 'taylor', 'last' => 'otwell']);

	$collection->put('state', 'arkansas');

	$collection->all();

	// ['first' => 'taylor', 'last' => 'otwell', 'state' => 'arkansas']

<a name="method-random"></a>
#### `random`

Returns a random item in the collection:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->random();

	// 4 - or any other random item

You may optionally pass a number to `random`. If that number is more than 1, a collection of items is returned:

	$random = $collection->random(3);

	$random->all();

	// [2, 4, 5] - or 3 other random items

If you request more items than are in the collection, an `InvalidArgumentException` is thrown.

<a name="method-reduce"></a>
#### `reduce`

Reduces the collection to a single value, passing the result of each iteration into the next one:

	$collection = collect([1, 2, 3]);

	$total = $collection->reduce(function($carry, $item)
	{
		return $carry + $item;
	});

	// 6

The value for `$carry` is always the result of the previous iteration. The last result is the one that is actually returned by `reduce`.

The value for `$carry` on the first iteration is `null`, but you can specify its initial value instead by passing it as the second argument to `reduce`:

	$collection->reduce(function($carry, $item)
	{
		return $carry + $item;
	}, 4);

	// 10

<a name="method-reject"></a>
#### `reject`

Filters the collection by the given callback, rejecting any items for which the callback returns `true`:

	$collection = collect([1, 2, 3, 4]);

	$filtered = $collection->reject(function($item)
	{
		return $item > 2;
	});

	$filtered->all();

	// [1, 2]

For the inverse of `reject`, see [`filter`](#method-filter).

<a name="method-reverse"></a>
#### `reverse`

reverses the order of the items in the collection:

	$collection = collect([1, 2, 3, 4, 5]);

	$reversed = $collection->reverse();

	$reversed->all();

	// [5, 4, 3, 2, 1]

<a name="method-search"></a>
#### `search`

Searches the collection for a given value and returns the corresponding key if successful. If the item is not found, `false` is returned.

	$collection = collect([2, 4, 6, 8]);

	$collection->search(4);

	// 1

The search is done using loose comparison. To use strict comparison instead, pass `true` as the second argument:

	$collection->search('4', true);

	// false

Alternatively, pass in your own callback:

	$collection->search(function($item, $key)
	{
		return $item > 5;
	});

	// 2

<a name="method-shift"></a>
#### `shift`

Removes the first item in the collection, and returns it:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->shift();

	// 1

	$collection->all();

	// [2, 3, 4, 5]

All numerical keys will be modified to start counting from zero.

<a name="method-shuffle"></a>
#### `shuffle`

Shuffles the items in the collection:

	$collection = collect([1, 2, 3, 4, 5]);

	$shuffled = $collection->shuffle();

	$shuffled->all();

	// [3, 2, 5, 1, 4] // or any other random order

<a name="method-slice"></a>
#### `slice`

Returns a slice of the collection, starting at the given index:

	$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

	$slice = $collection->slice(4);

	$slice->all();

	// [5, 6, 7, 8, 9, 10]

You may optionally pass the size of the slice you want as the second argument:

	$slice = $collection->slice(4, 2);

	$slice->all();

	// [5, 6]

As you can see, the new slice returned will have new numerically indexed keys. If you want to preserve the keys from the original collection, pass `true` as the third argument.

<a name="method-sort"></a>
#### `sort`

Sorts the collection:

	$collection = collect([5, 3, 1, 2, 4]);

	$sorted = $collection->sort();

	$sorted->values()->all();

	// [1, 2, 3, 4, 5]

The sorted collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

For sorting a collection of nested arrays or objects, see the [`sortBy`](#method-sortby) and [`sortByDesc`](#method-sortbydesc) methods.

If your sorting needs are more advanced, you can pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [`usort`](http://php.net/manual/en/function.usort.php#refsect1-function.usort-parameters), which is what the collection class calls under the hood.


<a name="method-sortby"></a>
#### `sortBy`

Sorts the collection by the specified key:

	$collection = collect([
		['name' => 'jill', 'age' => 23],
		['name' => 'sandy', 'age' => 12],
		['name' => 'john', 'age' => 45],
	]);

	$sorted = $collection->sortBy('age');

	$sorted->->values()->all();

	/*
		[
			['name' => 'sandy', 'age' => 12],
			['name' => 'jill', 'age' => 23],
			['name' => 'john', 'age' => 45],
		]
	*/

The sorted collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

Of course, you can pass your own callback to determine what should be used for comparing the items:

	$collection = collect([
		['name' => 'jill', 'children' => ['miriam', 'abigail', 'josh']],
		['name' => 'sandy', 'children' => ['allen']],
		['name' => 'john', 'children' => ['kay', 'daren']],
	]);

	$sorted = $collection->sort(function($person, $key)
	{
		return count($person['children']);
	});

	$sorted->values()->all();

	/*
		[
			['name' => 'sandy', 'children' => ['allen']],
			['name' => 'john', 'children' => ['kay', 'daren']],
			['name' => 'jill', 'children' => ['miriam', 'abigail', 'josh']],
		]
	*/

<a name="method-sortbydesc"></a>
#### `sortByDesc`

This method works the same as [`sortBy`](#method-sortby), but will sort the collection in reverse order.

<a name="method-splice"></a>
#### `splice`

Removes a slice of items starting at the specified index, and returns them:

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2);

	$chunk->all();

	// [3, 4, 5]

	$collection->all();

	// [1, 2]

You can also add a second argument specifying the amount of items in the chunk:

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2, 1);

	$chunk->all();

	// [3]

	$collection->all();

	// [1, 2, 4, 5]

In addition, you can pass a third argument with new items to replace the ones removed:

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2, 1, [10, 11]);

	$chunk->all();

	// [3]

	$collection->all();

	// [, 2, 10, 11, 4, 5]

<a name="method-sum"></a>
#### `sum`

Returns the sum of all items in the collection:

	collect([1, 2, 3, 4, 5])->sum();

	// 15

If the collection contains nested arrays or objects, pass in a key to use for calculating the values:

	$collection = collect([
		['name' => 'JavaScript: The Good Parts', 'pages' => 176],
		['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
	]);

	$collection->sum('pages');

	// 1272

Of course, you can pass your own callback as well:

	$collection = collect([
		['name' => 'jill', 'children' => ['miriam', 'abigail', 'josh']],
		['name' => 'sandy', 'children' => ['allen']],
		['name' => 'john', 'children' => ['kay', 'daren']],
	]);

	$collection->sum(function($person)
	{
		return count($person['children']);
	});

	// 6

<a name="method-take"></a>
#### `take`

Returns a new collection with the specified amount of items:

	$collection = collect([0, 1, 2, 3, 4, 5]);

	$chunk = $collection->take(3);

	$chunk->all();

	// [0, 1, 2]

You can also pass in a negative number to take the given amount of items from the end of the collection instead:

	$collection = collect([0, 1, 2, 3, 4, 5]);

	$chunk = $collection->take(-2);

	$chunk->all();

	// [4, 5]

<a name="method-toarray"></a>
#### `toArray`

Converts the collection into a plain array:

	$taylor = collect(['name' => 'taylor', 'project' => 'laravel']);

	$jeffrey = collect(['name' => 'jeffrey', 'project' => 'laracasts']);

	$collection = collect([$taylor, $jeffrey]);

	$collection->toArray();

	/*
		[
			['name' => 'taylor', 'project' => 'laravel'],
			['name' => 'jeffrey', 'project' => 'laracasts']
		]
	*/

> **Note:** `toArray` also converts all of its nested objects to an array. If you want to get the underlying array as is, use the [`all`](#method-all) method instead.

<a name="method-tojson"></a>
#### `toJson`

Converts the collection into JSON:

	$taylor = collect(['name' => 'taylor', 'project' => 'laravel']);

	$jeffrey = collect(['name' => 'jeffrey', 'project' => 'laracasts']);

	$collection = collect([$taylor, $jeffrey]);

	$collection->toJson();

	// '[{"name":"taylor","project":"laravel"},{"name":"jeffrey","project":"laracasts"}]'

<a name="method-transform"></a>
#### `transform`

Calls the given callback on every item in the collection, and replaces the items in the collection with those returned from the callback:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->transform(function($item, $key)
	{
		return $item * 2;
	});

	$collection->all();

	// [2, 4, 6, 8, 10]

> **Note:** Unlike most other collection methods, `transform` modified the collection itself. If you want to create a new collection instead, use the [`map`](#method-map) method.

<a name="method-unique"></a>
#### `unique`

Returns only unique items in the collection:

	$collection = collect([1, 1, 2, 2, 3, 4, 2]);

	$unique = $collection->unique();

	$unique->values()->all();

	// [1, 2, 3, 4]

The returned collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

When dealing with nested arrays or objects, specify the key used to determine uniqueness:

	$collection = collect([
		['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
		['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],
		['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
		['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
		['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
	]);

	$unique = $collection->unique('brand');

	$unique->values()->all();

	/*
		[
			['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
			['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
		]
	*/

Of course, you may pass your own callback to determine uniqueness:

	$unique = $collection->unique(function($item)
	{
		return $item['brand'].$item['type'];
	});

	$unique->values()->all();

	/*
		[
			['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
			['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
			['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
			['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
		]
	*/

<a name="method-values"></a>
#### `values`

Returns a new collection with the keys reset to consecutive numbers:

	$collection = collect(['name' => 'taylor', 'state' => 'arkansas']);

	$values = $collection->values();

	$values->all();

	// ['taylor', 'arkansas']

<a name="method-where"></a>
#### `where`

Filters the collection by the given key-value pair:

	$collection = collect([
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'abigail', 'last' => 'otwell'],
		['first' => 'jeffery', 'last' => 'way'],
		['first' => 'allie', 'last' => 'way'],
	]);

	$filtered = $collection->where('last', 'otwell');

	$filtered->all();

	/*
	[
		['first' => 'taylor', 'last' => 'otwell'],
		['first' => 'abigail', 'last' => 'otwell'],
	]
	*/

The filtering is done by running a strict comparison between the provided value and the value in each item. To filter using a loose comparison, use the [`whereLoose`](#where-loose) method.

<a name="method-whereloose"></a>
#### `whereLoose`

This method works the same as [`where`](#method-where), but will only compare the values loosely.

<a name="method-zip"></a>
#### `zip`

Merges together the values of the given array with the values in the collection at the corresponding position:

	$collection = collect(['taylor', 'jeffrey']);

	$zipped = $collection->zip(['laravel', 'laracasts']);

	$zipped->all();

	// [['taylor', 'laravel'], ['jeffrey', 'laracasts']]
