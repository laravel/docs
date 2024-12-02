# Upgrade Guide

- [Upgrading to 10.0 from 9.x](#upgrade-10.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating Minimum Stability](#updating-minimum-stability)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Database Expressions](#database-expressions)
- [Model "Dates" Property](#model-dates-property)
- [Monolog 3](#monolog-3)
- [Redis Cache Tags](#redis-cache-tags)
- [Service Mocking](#service-mocking)
- [The Language Directory](#language-directory)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [Closure Validation Rule Messages](#closure-validation-rule-messages)
- [Form Request `after` Method](#form-request-after-method)
- [Public Path Binding](#public-path-binding)
- [Query Exception Constructor](#query-exception-constructor)
- [Rate Limiter Return Values](#rate-limiter-return-values)
- [The `Redirect::home` Method](#redirect-home)
- [The `Bus::dispatchNow` Method](#dispatch-now)
- [The `registerPolicies` Method](#register-policies)
- [ULID Columns](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## Upgrading to 10.0 from 9.x

<a name="estimated-upgrade-time-??-minutes"></a>
#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]  
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

#### PHP 8.1.0 Required

Laravel now requires PHP 8.1.0 or greater.

#### Composer 2.2.0 Required

Laravel now requires [Composer](https://getcomposer.org) 2.2.0 or greater.

#### Composer Dependencies

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^10.0`
- `laravel/sanctum` to `^3.2`
- `doctrine/dbal` to `^3.0`
- `spatie/laravel-ignition` to `^2.0`
- `laravel/passport` to `^11.0` ([Upgrade Guide](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` to `^4.0`

</div>

If you are upgrading to Sanctum 3.x from the 2.x release series, please consult the [Sanctum upgrade guide](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md).

Furthermore, if you wish to use [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html), you should delete the `processUncoveredFiles` attribute from the `<coverage>` section of your application's `phpunit.xml` configuration file. Then, update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `nunomaduro/collision` to `^7.0`
- `phpunit/phpunit` to `^10.0`

</div>

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 10 support.

<a name="updating-minimum-stability"></a>
#### Minimum Stability

You should update the `minimum-stability` setting in your application's `composer.json` file to `stable`. Or, since the default value of `minimum-stability` is `stable`, you may delete this setting from your application's `composer.json` file:

```json
"minimum-stability": "stable",
```

### Application

<a name="public-path-binding"></a>
#### Public Path Binding

**Likelihood Of Impact: Low**

If your application is customizing its "public path" by binding `path.public` into the container, you should instead update your code to invoke the `usePublicPath` method offered by the `Illuminate\Foundation\Application` object:

```php
app()->usePublicPath(__DIR__.'/public');
```

### Authorization

<a name="register-policies"></a>
### The `registerPolicies` Method

**Likelihood Of Impact: Low**

The `registerPolicies` method of the `AuthServiceProvider` is now invoked automatically by the framework. Therefore, you may remove the call to this method from the `boot` method of your application's `AuthServiceProvider`.

### Cache

<a name="redis-cache-tags"></a>
#### Redis Cache Tags

**Likelihood Of Impact: Medium**

Usage of `Cache::tags()` is only recommended for applications using Memcached. If you are using Redis as your application's cache driver, you should consider moving to Memcached or using an alternative solution.

### Database

<a name="database-expressions"></a>
#### Database Expressions

**Likelihood Of Impact: Medium**

Database "expressions" (typically generated via `DB::raw`) have been rewritten in Laravel 10.x to offer additional functionality in the future. Notably, the grammar's raw string value must now be retrieved via the expression's `getValue(Grammar $grammar)` method. Casting an expression to a string using `(string)` is no longer supported.

**Typically, this does not affect end-user applications**; however, if your application is manually casting database expressions to strings using `(string)` or invoking the `__toString` method on the expression directly, you should update your code to invoke the `getValue` method instead:

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

This also means that methods like `orderByRaw` or `groupByRaw` can no longer accept expressions returned by `DB::raw(...)` and only accept strings.

<a name="query-exception-constructor"></a>
#### Query Exception Constructor

**Likelihood Of Impact: Very Low**

The `Illuminate\Database\QueryException` constructor now accepts a string connection name as its first argument. If your application is manually throwing this exception, you should adjust your code accordingly.

<a name="ulid-columns"></a>
#### ULID Columns

**Likelihood Of Impact: Low**

When migrations invoke the `ulid` method without any arguments, the column will now be named `ulid`. In previous releases of Laravel, invoking this method without any arguments created a column erroneously named `uuid`:

    $table->ulid();

To explicitly specify a column name when invoking the `ulid` method, you may pass the column name to the method:

    $table->ulid('ulid');

### Eloquent

<a name="model-dates-property"></a>
#### Model "Dates" Property

**Likelihood Of Impact: Medium**

The Eloquent model's deprecated `$dates` property has been removed. Your application should now use the `$casts` property:

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

### Localization

<a name="language-directory"></a>
#### The Language Directory

**Likelihood Of Impact: None**

Though not relevant to existing applications, the Laravel application skeleton no longer contains the `lang` directory by default. Instead, when writing new Laravel applications, it may be published using the `lang:publish` Artisan command:

```shell
php artisan lang:publish
```

### Logging

<a name="monolog-3"></a>
#### Monolog 3

**Likelihood Of Impact: Medium**

Laravel's Monolog dependency has been updated to Monolog 3.x. If you are directly interacting with Monolog within your application, you should review Monolog's [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md).

If you are using third-party logging services such as BugSnag or Rollbar, you may need to upgrade those third-party packages to a version that supports Monolog 3.x and Laravel 10.x.

### Queues

<a name="dispatch-now"></a>
#### The `Bus::dispatchNow` Method

**Likelihood Of Impact: Low**

The deprecated `Bus::dispatchNow` and `dispatch_now` methods have been removed. Instead, your application should use the `Bus::dispatchSync` and `dispatch_sync` methods, respectively.

<a name="dispatch-return"></a>
#### The `dispatch()` Helper Return Value

**Likelihood Of Impact: Low**

Invoking `dispatch` with a class that does not implement `Illuminate\Contracts\Queue` would previously return the result of the class's `handle` method. However, this will now return an `Illuminate\Foundation\Bus\PendingBatch` instance. You may use `dispatch_sync()` to replicate the previous behavior.

### Routing

<a name="middleware-aliases"></a>
#### Middleware Aliases

**Likelihood Of Impact: Optional**

In new Laravel applications, the `$routeMiddleware` property of the `App\Http\Kernel` class has been renamed to `$middlewareAliases` to better reflect its purpose. You are welcome to rename this property in your existing applications; however, it is not required.

<a name="rate-limiter-return-values"></a>
#### Rate Limiter Return Values

**Likelihood Of Impact: Low**

When invoking the `RateLimiter::attempt` method, the value returned by the provided closure will now be returned by the method. If nothing or `null` is returned, the `attempt` method will return `true`:

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
#### The `Redirect::home` Method

**Likelihood Of Impact: Very Low**

The deprecated `Redirect::home` method has been removed. Instead, your application should redirect to an explicitly named route:

```php
return Redirect::route('home');
```

### Testing

<a name="service-mocking"></a>
#### Service Mocking

**Likelihood Of Impact: Medium**

The deprecated `MocksApplicationServices` trait has been removed from the framework. This trait provided testing methods such as `expectsEvents`, `expectsJobs`, and `expectsNotifications`.

If your application uses these methods, we recommend you transition to `Event::fake`, `Bus::fake`, and `Notification::fake`, respectively. You can learn more about mocking via fakes in the corresponding documentation for the component you are attempting to fake.

### Validation

<a name="closure-validation-rule-messages"></a>
#### Closure Validation Rule Messages

**Likelihood Of Impact: Very Low**

When writing closure based custom validation rules, invoking the `$fail` callback more than once will now append the messages to an array instead of overwriting the previous message. Typically, this will not affect your application.

In addition, the `$fail` callback now returns an object. If you were previously type-hinting the return type of your validation closure, this may require you to update your type-hint:

```php
public function rules()
{
    'name' => [
        function ($attribute, $value, $fail) {
            $fail('validation.translation.key')->translate();
        },
    ],
}
```

<a name="validation-messages-and-closure-rules"></a>
#### Validation Messages and Closure Rules

**Likelihood Of Impact: Very Low**

Previously, you could assign a failure message to a different key by providing an array to the `$fail` callback injected into Closure based validation rules. However, you should now provide the key as the first argument and the failure message as the second argument:

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
#### Form Request After Method

**Likelihood Of Impact: Very Low**

Within form requests, the `after` method is now [reserved by Laravel](https://github.com/laravel/framework/pull/46757). If your form requests define an `after` method, the method should be renamed or modified to utilize the new "after validation" feature of Laravel's form requests.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be.

You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x) and choose which updates are important to you. However, many of the changes shown by the GitHub comparison tool are due to our organization's adoption of PHP native types. These changes are backwards compatible and the adoption of them during the migration to Laravel 10 is optional.
