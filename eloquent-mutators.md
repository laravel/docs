# Eloquent: Mutators

- [Introduction](#introduction)
- [Accessors & Mutators](#accessors-and-mutators)
- [Date Mutators](#date-mutators)
- [Attribute Casting](#attribute-casting)

<a name="introduction"></a>
## Introduction

Accessors and mutators allow you to format Eloquent attributes when retrieving them from a model or setting their value. For example, you may want to use the [Laravel encrypter](/docs/{{version}}/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model.

In addition to custom accessors and mutators, Eloquent can also automatically cast date fields to [Carbon](https://github.com/briannesbitt/Carbon) instances or even [cast text fields to JSON](#attribute-casting).

<a name="accessors-and-mutators"></a>
## Accessors & Mutators

#### Defining An Accessor

To define an accessor, create a `getFooAttribute` method on your model where `Foo` is the "camel" cased name of the column you wish to access. In this example, we'll defined an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of `first_name`:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get the user's first name.
		 *
		 * @param  string  $value
		 * @return string
		 */
		public function getFirstNameAttribute($value)
		{
			return ucfirst($value);
		}
	}

As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the mutator, you may simply access the `first_name` attribute:

	$user = App\User::find(1);

	$firstName = $user->first_name;

#### Defining A Mutator

To define a mutator, define a `setFooAttribute` method on your model where `Foo` is the "camel" cased name of the column you wish to access. So, again, let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Set the user's first name.
		 *
		 * @param  string  $value
		 * @return string
		 */
		public function setFirstNameAttribute($value)
		{
			$this->attributes['first_name'] = strtolower($value);
		}
	}

The mutator will receive the value that is being set on the attribute, allowing you to manipulate the value and set the manipulated value on the Eloquent model's internal `$attributes` property. So, for example, if we attempt to set the `first_name` attribute to `Sally`:

	$user = App\Find::user(1);

	$user->first_name = 'Sally';

In this example, the `setFirstNameAttribute` function will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its value in the internal `$attributes` array.

<a name="date-mutators"></a>
## Date Mutators

By default, Eloquent will convert the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which provides an assortment of helpful methods, and extends the native PHP `DateTime` class.

You may customize which fields are automatically mutated, and even completely disable this mutation, by overriding the `getDates` method of the model:

	public function getDates()
	{
		return ['created_at'];
	}

When a column is considered a date, you may set its value to a UNIX timestamp, date string (`Y-m-d`), date-time string, and of course a `DateTime` / `Carbon` instance.

To totally disable date mutations, simply return an empty array from the `getDates` method:

	public function getDates()
	{
		return [];
	}

<a name="attribute-casting"></a>
## Attribute Casting

If you have some attributes that you want to always convert to another data-type, you may add the attribute to the `casts` property of your model. Otherwise, you will have to define a mutator for each of the attributes, which can be time consuming. Here is an example of using the `casts` property:

	/**
	 * The attributes that should be casted to native types.
	 *
	 * @var array
	 */
	protected $casts = [
		'is_admin' => 'boolean',
	];

Now the `is_admin` attribute will always be cast to a boolean when you access it, even if the underlying value is stored in the database as an integer. Other supported cast types are: `integer`, `real`, `float`, `double`, `string`, `boolean`, `object` and `array`.

The `array` cast is particularly useful for working with columns that are stored as serialized JSON. For example, if your database has a TEXT type field that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model:

	/**
	 * The attributes that should be casted to native types.
	 *
	 * @var array
	 */
	protected $casts = [
		'options' => 'array',
	];

Now, when you utilize the Eloquent model:

	$user = User::find(1);

	// $options is an array...
	$options = $user->options;

	// options is automatically serialized back to JSON...
	$user->options = ['foo' => 'bar'];
