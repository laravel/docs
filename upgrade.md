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

### Eloquent

<a name="model-factories"></a>
#### Model Factories

**Likelihood Of Impact: High**

Laravel's [model factories](/docs/{{version}}/database-testing#creating-factories) feature has been totally rewritten to support classes and is not compatible with Laravel 7.x style factories. However, to ease the upgrade process, a new `laravel/legacy-factories` package has been created to continue using your existing factories with Laravel 8.x. You may install this package via Composer:

    composer require laravel/legacy-factories

### Framework

<a name="maintenance-mode-updates"></a>
#### Maintenance Mode Updates

**Likelihood Of Impact: Optional**

The [maintenance mode](/docs/{{version}}/configuration#maintenance-mode) feature of Laravel has been improved in Laravel 8.x. Pre-rendering the maintenance mode template is now supported and eliminates the chances of end users encountering errors during maintenance mode. However, to support this, the following lines must be added to your `public/index.php` file. These lines should be placed directly under the existing `LARAVEL_START` constant definition:

    define('LARAVEL_START', microtime(true));

    if (file_exists(__DIR__.'/../storage/framework/maintenance.php')) {
        require __DIR__.'/../storage/framework/maintenance.php';
    }

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

#### Failed Jobs Table Batch Support

**Likelihood Of Impact: Optional**

If you plan to use the [job batching](/docs/{{version}}/queues#job-batching) features of Laravel 8.x, your `failed_jobs` database table will need to be updated. First, a new `uuid` column should be added to your table:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('{{table}}', function (Blueprint $table) {
        $table->string('uuid')->after('id')->unique();
    });

Next, the `failed.driver` configuration option within your `queue` configuration file should be updated to `database-uuids`.

### Testing

<a name="assert-exact-json-method"></a>
#### The `assertExactJson` Method

**Likelihood Of Impact: Medium**

The `assertExactJson` method now requires numeric keys of compared arrays to match and be in the same order. If you would like to compare JSON against an array without requiring numerically keyed arrays to have the same order, you may use the `assertSimilarJson` method instead.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.x...master) and choose which updates are important to you.
