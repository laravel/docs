# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors & Mutators](#accessors-and-mutators)
    - [Defining An Accessor](#defining-an-accessor)
    - [Defining A Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array & JSON Casting](#array-and-json-casting)
    - [Date Casting](#date-casting)
    - [Query Time Casting](#query-time-casting)
- [Custom Casts](#custom-casts)
    - [Value Object Casting](#value-object-casting)
    - [Array / JSON Serialization](#array-json-serialization)
    - [Inbound Casting](#inbound-casting)
    - [Cast Parameters](#cast-parameters)
    - [Castables](#castables)

<a name="introduction"></a>
## Introduction

Accessors, mutators, and attribute casting allows you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/{{version}}/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model.

<a name="accessors-and-mutators"></a>
## Accessors & Mutators

<a name="defining-an-accessor"></a>
### Defining An Accessor

An accessor transform an Eloquent attribute value when it is accessed. To define an accessor, create a `get{Attribute}Attribute` method on your model where `{Attribute}` is the "studly" cased name of the column you wish to access.

In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute:

    <?php

    namespace App\Models;

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

As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance:

    use App\Models\User;

    $user = User::find(1);

    $firstName = $user->first_name;

You are not limited to interacting with a single attribute within your accessor. You may also use accessors to return new, computed values from existing attributes:

    /**
     * Get the user's full name.
     *
     * @return string
     */
    public function getFullNameAttribute()
    {
        return "{$this->first_name} {$this->last_name}";
    }

> {tip} If you would like these computed values to be added to the array / JSON representations of your model, [you will need to append them](https://laravel.com/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="defining-a-mutator"></a>
### Defining A Mutator

A mutator transforms an Eloquent attribute value when it is set. To define a mutator, define a `set{Attribute}Attribute` method on your model where `{Attribute}` is the "studly" cased name of the column you wish to access.

Let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Set the user's first name.
         *
         * @param  string  $value
         * @return void
         */
        public function setFirstNameAttribute($value)
        {
            $this->attributes['first_name'] = strtolower($value);
        }
    }

The mutator will receive the value that is being set on the attribute, allowing you to manipulate the value and set the manipulated value on the Eloquent model's internal `$attributes` property. To use our mutator, we only need to set the `first_name` attribute on an Eloquent model:

    use App\Models\User;

    $user = User::find(1);

    $user->first_name = 'Sally';

In this example, the `setFirstNameAttribute` function will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the internal `$attributes` array.

<a name="attribute-casting"></a>
## Attribute Casting

Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `$casts` property provides a convenient method of converting attributes to common data types.

The `$casts` property should be an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are:

<div class="content-list" markdown="1">
- `array`
- `boolean`
- `collection`
- `date`
- `datetime`
- `decimal:<digits>`
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`
</div>

To demonstrate attribute casting, let's cast the `is_admin` attribute, which is stored in our database as an integer (`0` or `1`) to a boolean value:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

After defining the cast, the `is_admin` attribute will always be cast to a boolean when you access it, even if the underlying value is stored in the database as an integer:

    $user = App\Models\User::find(1);

    if ($user->is_admin) {
        //
    }

> {note} Attributes that are `null` will not be cast. In addition, you should never define a cast (or an attribute) that has the same name as a relationship.

<a name="array-and-json-casting"></a>
### Array & JSON Casting

The `array` cast is particularly useful when working with columns that are stored as serialized JSON. For example, if your database has a `JSON` or `TEXT` field type that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

Once the cast is defined, you may access the `options` attribute and it will automatically be deserialized from JSON into a PHP array. When you set the value of the `options` attribute, the given array will automatically be serialized back into JSON for storage:

    use App\Models\User;

    $user = User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();

To update a single field of a JSON attribute with a more terse syntax, you may use the `->` operator when calling the `update` method:

    $user = User::find(1);

    $user->update(['options->key' => 'value']);

<a name="date-casting"></a>
### Date Casting

By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `$cast` property array. Typically, dates should be cast using the `datetime` cast.

When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/{{version}}/eloquent-serialization):

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'created_at' => 'datetime:Y-m-d',
    ];

When a column is cast as a date, you may set its value to a UNIX timestamp, date string (`Y-m-d`), date-time string, or a `DateTime` / `Carbon` instance. The date's value will be correctly converted and stored in your database:

You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database:

    /**
     * Prepare a date for array / JSON serialization.
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d');
    }

To specify the format that should be used when actually storing a model's dates within your database, you should define a `$dateFormat` property on your model:

    /**
     * The storage format of the model's date columns.
     *
     * @var string
     */
    protected $dateFormat = 'U';

<a name="query-time-casting"></a>
### Query Time Casting

Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query:

    use App\Models\Post;
    use App\Models\User;

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->get();

The `last_posted_at` attribute on the results of this query will be a simple string. It would be wonderful if we could apply a `datetime` cast to this attribute when executing the query. Thankfully, we may accomplish this using the `withCasts` method:

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->withCasts([
        'last_posted_at' => 'datetime'
    ])->get();

<a name="custom-casts"></a>
## Custom Casts

Laravel has a variety of built-in, helpful cast types; however, you may occasionally need to define your own cast types. You may accomplish this by defining a class that implements the `CastsAttributes` interface.

Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type:

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Json implements CastsAttributes
    {
        /**
         * Cast the given value.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  mixed  $value
         * @param  array  $attributes
         * @return array
         */
        public function get($model, $key, $value, $attributes)
        {
            return json_decode($value, true);
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  array  $value
         * @param  array  $attributes
         * @return string
         */
        public function set($model, $key, $value, $attributes)
        {
            return json_encode($value);
        }
    }

Once you have defined a custom cast type, you may attach it to a model attribute using its class name:

    <?php

    namespace App\Models;

    use App\Casts\Json;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'options' => Json::class,
        ];
    }

<a name="value-object-casting"></a>
### Value Object Casting

You are not limited to casting values to primitive types. You may also cast values to objects. Defining custom casts that cast values to objects is very similar to casting to primitive types; however, the `set` method should return an array of key / value pairs that will be used to set raw, storable values on the model.

As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`:

    <?php

    namespace App\Casts;

    use App\Models\Address as AddressModel;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
    use InvalidArgumentException;

    class Address implements CastsAttributes
    {
        /**
         * Cast the given value.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  mixed  $value
         * @param  array  $attributes
         * @return \App\Models\Address
         */
        public function get($model, $key, $value, $attributes)
        {
            return new AddressModel(
                $attributes['address_line_one'],
                $attributes['address_line_two']
            );
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  \App\Models\Address  $value
         * @param  array  $attributes
         * @return array
         */
        public function set($model, $key, $value, $attributes)
        {
            if (! $value instanceof AddressModel) {
                throw new InvalidArgumentException('The given value is not an Address instance.');
            }

            return [
                'address_line_one' => $value->lineOne,
                'address_line_two' => $value->lineTwo,
            ];
        }
    }

When casting to value objects, any changes made to the value object will automatically be synced back to the model before the model is saved:

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = 'Updated Address Value';

    $user->save();

> {tip} If you plan to serialize your Eloquent models containing value objects to JSON or arrays, you should implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces on the value object.

<a name="array-json-serialization"></a>
### Array / JSON Serialization

When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object.

Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom class cast should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object:

    /**
     * Get the serialized representation of the value.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return mixed
     */
    public function serialize($model, string $key, $value, array $attributes)
    {
        return (string) $value;
    }

<a name="inbound-casting"></a>
### Inbound Casting

Occasionally, you may need to write a custom cast that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. A classic example of an inbound only cast is a "hashing" cast. Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined.

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;

    class Hash implements CastsInboundAttributes
    {
        /**
         * The hashing algorithm.
         *
         * @var string
         */
        protected $algorithm;

        /**
         * Create a new cast class instance.
         *
         * @param  string|null  $algorithm
         * @return void
         */
        public function __construct($algorithm = null)
        {
            $this->algorithm = $algorithm;
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  array  $value
         * @param  array  $attributes
         * @return string
         */
        public function set($model, $key, $value, $attributes)
        {
            return is_null($this->algorithm)
                        ? bcrypt($value)
                        : hash($this->algorithm, $value);
        }
    }

<a name="cast-parameters"></a>
### Cast Parameters

When attaching a custom cast to a model, cast parameters may be specified by separating them from the class name using a `:` character and comma-delimiting multiple parameters. The parameters will be passed to the constructor of the cast class:

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'secret' => Hash::class.':sha256',
    ];

<a name="castables"></a>
### Castables

You may want to allow your application's value objects to define their own custom cast classes. Instead of attaching the custom cast class to your model, you may alternatively attach a value object class that implements the `Illuminate\Contracts\Database\Eloquent\Castable` interface:

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class,
    ];

Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use App\Casts\Address as AddressCast;

    class Address implements Castable
    {
        /**
         * Get the name of the caster class to use when casting from / to this cast target.
         *
         * @param  array  $arguments
         * @return string
         */
        public static function castUsing(array $arguments)
        {
            return AddressCast::class;
        }
    }

When using `Castable` classes, you may still provide arguments in the `$casts` definition. The arguments will be passed to the `castUsing` method:

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class.':argument',
    ];

<a name="anonymous-cast-classes"></a>
#### Castables & Anonymous Cast Classes

By combining "castables" with PHP's [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php), you may define a value object and its casting logic as a single castable object. To accomplish this, return an anonymous class from your value object's `castUsing` method. The anonymous class should implement the `CastsAttributes` interface:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Address implements Castable
    {
        // ...

        /**
         * Get the caster class to use when casting from / to this cast target.
         *
         * @param  array  $arguments
         * @return object|string
         */
        public static function castUsing(array $arguments)
        {
            return new class implements CastsAttributes
            {
                public function get($model, $key, $value, $attributes)
                {
                    return new Address(
                        $attributes['address_line_one'],
                        $attributes['address_line_two']
                    );
                }

                public function set($model, $key, $value, $attributes)
                {
                    return [
                        'address_line_one' => $value->lineOne,
                        'address_line_two' => $value->lineTwo,
                    ];
                }
            };
        }
    }
