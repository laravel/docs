# Upgrade Guide

- [Upgrading To 8.0 From 7.x](#upgrade-8.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- [Model Factories](#model-factories)
- [Queue `retryAfter` Method](#queue-retry-after-method)
- [Pagination Defaults](#pagination-defaults)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [PHP 7.3.0 Required](#php-7.3.0-required)
- [Failed Jobs Table Batch Support](#failed-jobs-table-batch-support)
- [Maintenance Mode Updates](#maintenance-mode-updates)
- [The `assertExactJson` Method](#assert-exact-json-method)
</div>

<a name="upgrade-8.0"></a>
## Upgrading To 8.0 From 7.x

#### Estimated Upgrade Time: 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="php-7.3.0-required"></a>
### PHP 7.3.0 Required

**Likelihood Of Impact: Medium**

The new minimum PHP version is now 7.3.0.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `^8.0` in your `composer.json` file. In addition, update your `nunomaduro/collision` dependency to `^5.0`.

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 8 support.

### Collections

#### The `isset` Method

**Likelihood Of Impact: Low**

To be consistent with typical PHP behavior, the `offsetExists` method of `Illuminate\Support\Collection` has been updated to use `isset` instead of `array_key_exists`. This may present a change in behavior when dealing with collection items that have a value of `null`:

    $collection = collect([null]);

    // Laravel 7.x - true
    isset($collection[0]);

    // Laravel 8.x - false
    isset($collection[0]);

### Eloquent

<a name="model-factories"></a>
#### Model Factories

**Likelihood Of Impact: High**

Laravel's [model factories](/docs/{{version}}/database-testing#creating-factories) feature has been totally rewritten to support classes and is not compatible with Laravel 7.x style factories. However, to ease the upgrade process, a new `laravel/legacy-factories` package has been created to continue using your existing factories with Laravel 8.x. You may install this package via Composer:

    composer require laravel/legacy-factories

#### The `Castable` Interface

**Likelihood Of Impact: Low**

The `castUsing` method of the `Castable` interface has been updated to accept an array of arguments. If you are implementing this interface you should update your implementation accordingly:

    public static function castUsing(array $arguments);

#### Increment / Decrement Events

**Likelihood Of Impact: Low**

Proper "update" and "save" related model events will now be dispatched when executing the `increment` or `decrement` methods on Eloquent model instances.

### Events

#### The `Dispatcher` Contract

**Likelihood Of Impact: Low**

The `listen` method of the `Illuminate\Contracts\Events\Dispatcher` contract has been updated to make the `$listener` property optional. This change was made to support automatic detection of handled event types via reflection. If you are manually implementing this interface, you should update your implementation accordingly:

    public function listen($events, $listener = null);

### Framework

<a name="maintenance-mode-updates"></a>
#### Maintenance Mode Updates

**Likelihood Of Impact: Optional**

The [maintenance mode](/docs/{{version}}/configuration#maintenance-mode) feature of Laravel has been improved in Laravel 8.x. Pre-rendering the maintenance mode template is now supported and eliminates the chances of end users encountering errors during maintenance mode. However, to support this, the following lines must be added to your `public/index.php` file. These lines should be placed directly under the existing `LARAVEL_START` constant definition:

    define('LARAVEL_START', microtime(true));

    if (file_exists(__DIR__.'/../storage/framework/maintenance.php')) {
        require __DIR__.'/../storage/framework/maintenance.php';
    }

#### Manager `$app` Property

**Likelihood Of Impact: Low**

The previously deprecated `$app` property of the `Illuminate\Support\Manager` class has been removed. If you were relying on this property, you should use the `$container` property instead.

#### The `elixir` Helper

**Likelihood Of Impact: Low**

The previously deprecated `elixir` helper has been removed. Applications still using this method are encouraged to upgrade to [Laravel Mix](https://github.com/JeffreyWay/laravel-mix).

### Mail

#### The `sendNow` Method

**Likelihood Of Impact: Low**

The previously deprecated `sendNow` method has been removed. Instead, please use the `send` method.

### Pagination

<a name="pagination-defaults"></a>
#### Pagination Defaults

**Likelihood Of Impact: High**

The paginator now uses the [Tailwind CSS framework](https://tailwindcss.com) for its default styling. In order to keep using Bootstrap, you should add the following method call to the `boot` method of your application's `AppServiceProvider`:

    use Illuminate\Pagination\Paginator;

    Paginator::useBootstrap();

### Queue

<a name="queue-retry-after-method"></a>
#### The `retryAfter` Method

**Likelihood Of Impact: High**

For consistency with other features of Laravel, the `retryAfter` method and `retryAfter` property of queued jobs, mailers, notifications, and listeners has been renamed to `backoff`. You should update the name of this method / property in the relevant classes in your application.

<a name="failed-jobs-table-batch-support"></a>
#### Failed Jobs Table Batch Support

**Likelihood Of Impact: Optional**

If you plan to use the [job batching](/docs/{{version}}/queues#job-batching) features of Laravel 8.x, your `failed_jobs` database table will need to be updated. First, a new `uuid` column should be added to your table:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('failed_jobs', function (Blueprint $table) {
        $table->string('uuid')->after('id')->unique();
    });

Next, the `failed.driver` configuration option within your `queue` configuration file should be updated to `database-uuids`.

### Scheduling

#### The `cron-expression` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `dragonmantank/cron-expression` has been updated from `2.x` to `3.x`. This should not cause any breaking change in your application unless you are interacting with the `cron-expression` library directly. If you are interacting with this library directly, please review its [change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md).

### Session

#### The `Session` Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Session\Session` contract has received a new `pull` method. If you are implementing this contract manually, you should update your implementation accordingly:

    /**
      * Get the value of a given key and then forget it.
      *
      * @param  string  $key
      * @param  mixed  $default
      * @return mixed
      */
     public function pull($key, $default = null);

### Testing

<a name="assert-exact-json-method"></a>
#### The `assertExactJson` Method

**Likelihood Of Impact: Medium**

The `assertExactJson` method now requires numeric keys of compared arrays to match and be in the same order. If you would like to compare JSON against an array without requiring numerically keyed arrays to have the same order, you may use the `assertSimilarJson` method instead.

### Validation

### Database Rule Connections

**Likelihood Of Impact: Low**

The `unique` and `exists` rules will now respect the specified connection name (accessed via the model's `getConnectionName` method) of Eloquent models when performing queries.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.x...master) and choose which updates are important to you.
