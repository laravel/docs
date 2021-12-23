# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods](#belongs-to-many-first-or-new)
- [Postgres "Schema" Configuration](#postgres-schema-configuration)
- [The `when` / `unless` Methods](#when-and-unless-methods)
- [Custom Casts & `null`](#custom-casts-and-null)
- [The `password` Rule](#the-password-rule)
- [The `lang` Directory](#the-lang-directory)
- [The `assertDeleted` Method](#the-assert-deleted-method)
</div>

<a name="upgrade-9.0"></a>
## Upgrading To 9.0 From 8.x

<a name="estimated-upgrade-time-10-minutes"></a>
#### Estimated Upgrade Time: 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="application"></a>
### Application

<a name="the-application-contract"></a>
#### The `Application` Contract

**Likelihood Of Impact: Low**

The `storagePath` method of the `Illuminate\Contracts\Foundation\Application` interface has been updated to accept a `$path` argument. If you are implementing this interface you should update your implementation accordingly:

    public function storagePath($path = '');

#### Exception Handler `ignore` Method

**Likelihood Of Impact: Low**

The exception handler's `ignore` method is now `public` instead of `protected`. This method is not included in the default application skeleton; however, if you have manually defined this method you should update its visibility to `public`:

```php
public function ignore(string $class);
```

### Blade

#### Lazy Collections & The `$loop` Variable

**Likelihood Of Impact: Low**

When iterating over a `LazyCollection` instance within a Blade template, the `$loop` variable is no longer available, as accessing this variable causes the entire `LazyCollection` to be loaded into memory, thus rendering the usage of lazy collections pointless in this scenario.

### Container

#### The `Container` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Container\Container` contract has received two method definitions: `scoped` and `scopedIf`. If you are manually implementing this contract, you should update your implementation to reflect these new methods.

#### The `ContextualBindingBuilder` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Container\ContextualBindingBuilder` contract now defines a `giveConfig` method. If you are manually implementing this interface, you should update your implementation to reflect this new method:

```php
public function giveConfig($key, $default = null);
```

### Database

<a name="postgres-schema-configuration"></a>
#### Postgres "Schema" Configuration

**Likelihood Of Impact: Medium**

The `schema` configuration option used to configure Postgres connection search paths in your application's `config/database.php` configuration file should be renamed to `search_path`.

### Eloquent

<a name="custom-casts-and-null"></a>
#### Custom Casts & `null`

**Likelihood Of Impact: Medium**

In previous releases of Laravel, the `set` method of custom cast classes was not invoked if the cast attribute was being set to `null`. However, this behavior was inconsistent with the Laravel documentation. In Laravel 9, the `set` method of the cast class will be invoked with `null` as the provided `$value` argument. Therefore, you should ensure your custom casts are able to sufficiently handle this scenario:

```php
/**
 * Prepare the given value for storage.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  AddressModel  $value
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
```

<a name="belongs-to-many-first-or-new"></a>
#### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods

**Likelihood Of Impact: Medium**

The `belongsToMany` relationship's `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods all accept an array of attributes as their first argument. In previous releases of Laravel, this array of attributes was compared against the "pivot" / intermediate table for existing records.

However, this behavior was unexpected and typically unwanted. Instead, these methods now compare the array of attributes against the table of the related model:

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

In addition, the `firstOrCreate` method now accepts a `$values` array as its second argument. This array will be merged with the first argument to the method (`$attributes`) when creating the related model if one does not already exist. This changes makes this method consistent with the `firstOrCreate` methods offered by other relationship types:

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

#### The `touch` Method

**Likelihood Of Impact: Low**

The `touch` method now accepts an attribute to touch. If you were previously overwriting this method, you should update your method signature to reflect this new argument:

```php
public function touch($attribute = null);
```

### Encryption

#### The Encrypter Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Encryption\Encrypter` contract now defines a `getKey` method. If you are manually implementing this interface, you should update your implementation accordingly:

```php
public function getKey();
```

### Facades

#### The `getFacadeAccessor` Method

**Likelihood Of Impact: Low**

The `getFacadeAccessor` method must always return a container binding key. In previous releases of Laravel, this method could return an object instance; however, this behavior is no longer supported. If you have written your own facades, you should ensure that this method returns a container binding string:

```php
/**
 * Get the registered name of the component.
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

### Filesystem

#### The `FILESYSTEM_DRIVER` Environment Variable

**Likelihood Of Impact: Low**

The `FILESYSTEM_DRIVER` environment variable has been renamed to `FILESYSTEM_DISK` to more accurately reflect its usage. This change only affects the application skeleton; however, you are welcome to update your own application's environment variables to reflect this change if you wish.

### Helpers

#### The `data_get` Helper & Iterable Objects

**Likelihood Of Impact: Very Low**

Previously, the `data_get` helper could be used to retrieve nested data on arrays and `Collection` instances; however, this helper can now retrieve nested data on all iterable objects.

<a name="when-and-unless-methods"></a>
#### The `when` / `unless` Methods

**Likelihood Of Impact: Medium**

As you may know, `when` and `unless` methods are offered by various classes throughout the framework. These methods can be used to conditionally perform an action if the boolean value of the first argument to the method evaluates to `true` or `false`:

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

Therefore, in previous releases of Laravel, passing a closure to the `when` or `unless` methods meant that the conditional operation would always execute, since a loose comparison against a closure object (or any other object) always evaluates to `true`. This often led to unexpected outcomes because developers expect the **result** of the closure to be used as the boolean value that determines if the conditional action executes.

So, in Laravel 9, any closures passed to the `when` or `unless` methods will be executed and the value returned by the closure will be considered the boolean value used by the `when` and `unless` methods:

```php
$collection->when(function ($collection) {
    // This closure is executed...
    return false;
}, function ($collection) {
    // Not executed since first closure returned "false"...
    $collection->merge([1, 2, 3]);
});
```

### Packages

<a name="the-lang-directory"></a>
#### The `lang` Directory

**Likelihood Of Impact: Medium**

In new Laravel applications, the `resources/lang` directory is now located in the root project directory (`lang`). If your package is publishing language files to this directory, you should ensure that your package is publishing to `app()->langPath()` instead of a hard-coded path.

<a name="queue"></a>
### Queue

<a name="the-opis-closure-library"></a>
#### The `opis/closure` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` classes have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead.

#### The Failed Job Provider `failed` Method

**Likelihood Of Impact: Low**

The `flush` method defined by the `Illuminate\Queue\Failed\FailedJobProviderInterface` interface now accepts an `$age` argument which determines how old a failed job must be (in days) before it is flushed by the `queue:flush` command. If you are manually implementing the `FailedJobProviderInterface` you should ensure that your implementation is updated to reflect this new argument:

```php
public function flush($age = null);
```

### Testing

<a name="the-assert-deleted-method"></a>
#### The `assertDeleted` Method

**Likelihood Of Impact: Medium**

All calls to the `assertDeleted` method should be updated to `assertModelMissing`.

### Validation

#### Form Request `validated` Method

**Likelihood Of Impact: Low**

The `validated` method offered by form requests now accepts `$key` and `$default` arguments. If you are manually overwriting the definition of this method, you should update your method's signature to reflect these new arguments:

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
#### The `password` Rule

**Likelihood Of Impact: Medium**

The `password` rule, which validates that the given input value matches the authenticated user's current password, has been renamed to `current_password`.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you.
