# Upgrade Guide

- [Upgrading To 10.0 From 9.x](#upgrade-10.0)

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
- [Redis Cache Tags](#redis-cache-tags)
- [Service Mocking](#service-mocking)
- [The Language Directory](#language-directory)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [Closure Validation Rule Messages](#closure-validation-rule-messages)
- [Monolog 3](#monolog-3)
- [Query Exception Constructor](#query-exception-constructor)
- [Rate Limiter Return Values](#rate-limiter-return-values)
- [Relation `getBaseQuery` Method](#relation-getbasequery-method)
- [The `Redirect::home` Method](#redirect-home)
- [The `Bus::dispatchNow` Method](#dispatch-now)
- [ULID Columns](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## Upgrading To 10.0 From 9.x

<a name="estimated-upgrade-time-??-minutes"></a>
#### Estimated Upgrade Time: 10 Minutes

> **Note**  
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

#### Composer 2.2 Required

Laravel now requires Composer 2.2 or greater.

#### PHP 8.1.0 Required

Laravel now requires PHP 8.1.0 or greater.

#### Composer Dependencies

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^10.0`
- `spatie/laravel-ignition` to `^2.0`

</div>

Optionally, if you wish to use [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html), you should delete the `processUncoveredFiles` attribute from the `<coverage>` section of your application's `phpunit.xml` configuration file. Then, update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `nunomaduro/collision` to `^7.0`
- `phpunit/phpunit` to `^10.0`

</div>

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 10 support.

<a name="updating-minimum-stability"></a>
#### Minimum Stability

You should update the `minimum-stability` setting in your application's `composer.json` file to `stable`:

```json
"minimum-stability": "stable",
```

### Cache

<a name="redis-cache-tags"></a>
#### Redis Cache Tags

**Likelihood Of Impact: Medium**

Redis [cache tag](/docs/{{version}}/cache#cache-tags) support has been rewritten for better performance and storage efficiency. In previously releases of Laravel, stale cache tags would accumulate in the cache when using Redis as your application's cache driver.

However, to properly prune stale cache tag entries, Laravel's new `cache:prune-stale-tags` Artisan command should be [scheduled](/docs/{{version}}/scheduling) in your application's `App\Console\Kernel` class:

    $schedule->command('cache:prune-stale-tags')->hourly();

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

<a name="query-exception-constructor"></a>
#### Query Exception Constructor

**Likelihood Of Impact: Very Low**

The `Illuminate\Database\QueryException` constructor now accepts a string connection name as its first argument. If your application is mainly throwing this exception, you should adjust your code accordingly.

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

<a name="relation-getbasequery-method"></a>
#### Relation `getBaseQuery` Method

**Likelihood Of Impact: Very Low**

The `getBaseQuery` method on the `Illuminate\Database\Eloquent\Relations\Relation` class has been renamed to `toBase`.

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

**Likelihood Of Impact: Low**

Laravel's Monolog dependency has been updated to Monolog 3.x. If you are directly interacting with Monolog within your application, you should review Monolog's [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md).

### Queues

<a name="dispatch-now"></a>
#### The `Bus::dispatchNow` Method

**Likelihood Of Impact: Low**

The deprecated `Bus::dispatchNow` and `dispatch_now` methods have been removed. Instead, your application should use the `Bus::dispatchSync` and `dispatch_sync` methods, respectively.

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

If your application uses these methods, we recommend you transition to `Event::fake`, `Bus::fake`, and `Notification::fake`, respectively. You can learn more about mocking via the complete [mocking documentation](/docs/{{version}}/mocking).

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

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be.

You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x) and choose which updates are important to you. However, many of the changes shown by the GitHub comparison tool are due to our organization's adoption of PHP native types. These changes are backwards compatible and the adoption of them during the migration to Laravel 10 is optional.
