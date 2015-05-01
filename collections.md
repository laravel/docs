# Collections

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)

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

As mentioned above, the `collect` helper will return a new `Illuminate\Support\Collection` instance for the given array. You may also use the `make` command on the `Collection` class:

	$collection = collect([1, 2, 3]);

	$collection = Collection::make([1, 2, 3]);

Of course, collections of [Eloquent](/docs/{{version}}/eloquent) objects are always returned as `Collection` instances; however, you should feel free to use the `Collection` class wherever it is convenient for your application.

#### Explore The Collection

Instead of listing all of the methods (there are a lot) the Collection makes available, check out the [API documentation for the class](http://laravel.com/api/master/Illuminate/Support/Collection.html)!
