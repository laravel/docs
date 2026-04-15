# Upgrade Guide

- [Upgrading To 13.0 From 12.x](#upgrade-13.0)
    - [Upgrading Using AI](#upgrading-using-ai)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)
- [Request Forgery Protection](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Cache `serializable_classes` Configuration](#cache-serializable_classes-configuration)
- [Database `upsert` With MySQL or MariaDB](#database-upsert-mariadb-mysql)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [Cache Prefixes and Session Cookie Names](#cache-prefixes-and-session-cookie-names)
- [Collection Model Serialization Restores Eager-Loaded Relations](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` and Nullable Class Defaults](#containercall-and-nullable-class-defaults)
- [Domain Route Registration Precedence](#domain-route-registration-precedence)
- [`JobAttempted` Event Exception Payload](#jobattempted-event-exception-payload)
- [Manager `extend` Callback Binding](#manager-extend-callback-binding)
- [MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [Pagination Bootstrap View Names](#pagination-bootstrap-view-names)
- [Polymorphic Pivot Table Name Generation](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` Event Property Rename](#queuebusy-event-property-rename)
- [`Str` Factories Reset Between Tests](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
## Upgrading To 13.0 From 12.x

#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. To save time, you may use [Shift](https://laravelshift.com). Shift is a community-maintained service that automates Laravel upgrades.

<a name="upgrading-using-ai"></a>
### Upgrading Using AI

You can automate your upgrade using [Laravel Boost](https://github.com/laravel/boost). Boost is a first-party MCP server that provides your AI assistant with guided upgrade prompts — once installed in any Laravel 12 application, use the `/upgrade-laravel-v13` slash command in Claude Code, Cursor, OpenCode, Gemini, or VS Code to begin the upgrade to Laravel 13. This command requires Laravel Boost `^2.0`.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^13.0`
- `laravel/boost` to `^2.0`
- `laravel/tinker` to `^3.0`
- `phpunit/phpunit` to `^12.0`
- `pestphp/pest` to `^4.0`

</div>

<a name="updating-the-laravel-installer"></a>
### Updating the Laravel Installer

If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation for Laravel 13.x compatibility.

If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`:

```shell
composer global update laravel/installer
```

Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release.

<a name="cache"></a>
### Cache

<a name="cache-prefixes-and-session-cookie-names"></a>
#### Cache Prefixes and Session Cookie Names

**Likelihood Of Impact: Low**

Laravel's default cache and Redis key prefixes now use hyphenated suffixes.

In most applications, this change will not apply because application-level configuration files already define these values. This primarily affects applications that rely on framework-level fallback configuration when corresponding application config values are not present.

If your application relies on these generated defaults, cache keys and session cookie names may change after upgrading:

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';
```

To retain previous behavior, explicitly configure `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` in your environment.

<a name="store-and-repository-contracts-touch"></a>
#### `Store` and `Repository` Contracts: `touch`

**Likelihood Of Impact: Very Low**

The cache contracts now include a `touch` method for extending item TTLs. If you maintain custom cache store implementations, you should add this method:

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
#### Cache `serializable_classes` Configuration

**Likelihood Of Impact: Medium**

The default application `cache` configuration now includes a `serializable_classes` option set to `false`. This hardens cache unserialization behavior to help prevent PHP deserialization gadget chain attacks if your application's `APP_KEY` is leaked. If your application intentionally stores PHP objects in cache, you should explicitly list the classes that may be unserialized:

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

If your application previously relied on unserializing arbitrary cached objects, you will need to migrate that usage to explicit class allow-lists or to non-object cache payloads (such as arrays).

<a name="container"></a>
### Container

<a name="containercall-and-nullable-class-defaults"></a>
#### `Container::call` and Nullable Class Defaults

**Likelihood Of Impact: Low**

`Container::call` now respects nullable class parameter defaults when no binding exists, matching constructor injection behavior introduced in Laravel 12:

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

If your method-call injection logic depended on the previous behavior, you may need to update it.

<a name="contracts"></a>
### Contracts

<a name="dispatcher-contract-dispatchafterresponse"></a>
#### `Dispatcher` Contract: `dispatchAfterResponse`

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Bus\Dispatcher` contract now includes the `dispatchAfterResponse($command, $handler = null)` method.

If you maintain a custom dispatcher implementation, add this method to your class.

<a name="responsefactory-contract-eventstream"></a>
#### `ResponseFactory` Contract: `eventStream`

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Routing\ResponseFactory` contract now includes an `eventStream` signature.

If you maintain a custom implementation of this contract, you should add this method.

<a name="mustverifyemail-contract-markemailasunverified"></a>
#### `MustVerifyEmail` Contract: `markEmailAsUnverified`

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Auth\MustVerifyEmail` contract now includes `markEmailAsUnverified()`.

If you provide a custom implementation of this contract, add this method to remain compatible.

<a name="database"></a>
### Database

<a name="database-upsert-mariadb-mysql"></a>
#### Database `upsert` With MySQL or MariaDB

**Likelihood Of Impact: Medium**

Laravel now validates that the caller provides a non-empty value for `uniqueBy`, and will throw an `InvalidArgumentException` instead of generating invalid SQL.

Although the MariaDB and MySQL database drivers ignore the `uniqueBy` value and always use the table's primary and unique indexes to detect existing records, the validation still applies. An `InvalidArgumentException` will be thrown if `uniqueBy` is empty.

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`

**Likelihood Of Impact: Low**

Laravel now compiles full `DELETE ... JOIN` queries including `ORDER BY` and `LIMIT` for MySQL grammar.

In previous versions, `ORDER BY` / `LIMIT` clauses could be silently ignored on joined deletes. In Laravel 13, these clauses are included in the generated SQL. As a result, database engines that do not support this syntax (such as standard MySQL / MariaDB variants) may now throw a `QueryException` instead of executing an unbounded delete.

<a name="eloquent"></a>
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
#### Model Booting and Nested Instantiation

**Likelihood Of Impact: Very Low**

Creating a new model instance while that model is still booting is now disallowed and throws a `LogicException`.

This affects code that instantiates models from inside model `boot` methods or trait `boot*` methods:

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

Move this logic outside the boot cycle to avoid nested booting.

<a name="polymorphic-pivot-table-name-generation"></a>
#### Polymorphic Pivot Table Name Generation

**Likelihood Of Impact: Low**

When table names are inferred for polymorphic pivot models using custom pivot model classes, Laravel now generates pluralized names.

If your application depended on the previous singular inferred names for morph pivot tables and used custom pivot classes, you should explicitly define the table name on your pivot model.

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
#### Collection Model Serialization Restores Eager-Loaded Relations

**Likelihood Of Impact: Low**

When Eloquent model collections are serialized and restored (such as in queued jobs), eager-loaded relations are now restored for the collection's models.

If your code depended on relations not being present after deserialization, you may need to adjust that logic.

<a name="http-client"></a>
### HTTP Client

<a name="http-client-response-throw-and-throwif-signatures"></a>
#### HTTP Client `Response::throw` and `throwIf` Signatures

**Likelihood Of Impact: Very Low**

The HTTP client response methods now declare their callback parameters in the method signatures:

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

If you override these methods in custom response classes, ensure your method signatures are compatible.

<a name="notifications"></a>
### Notifications

<a name="default-password-reset-subject"></a>
#### Default Password Reset Subject

**Likelihood Of Impact: Very Low**

Laravel's default password reset mail subject has changed:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

If your tests, assertions, or translation overrides depend on the previous default string, update them accordingly.

<a name="queued-notifications-and-missing-models"></a>
#### Queued Notifications and Missing Models

**Likelihood Of Impact: Very Low**

Queued notifications now respect the `#[DeleteWhenMissingModels]` attribute and `$deleteWhenMissingModels` property defined on the notification class.

In previous versions, missing models could still cause queued notification jobs to fail in cases where you expected them to be deleted.

<a name="queue"></a>
### Queue

<a name="jobattempted-event-exception-payload"></a>
#### `JobAttempted` Event Exception Payload

**Likelihood Of Impact: Low**

The `Illuminate\Queue\Events\JobAttempted` event now exposes the exception object (or `null`) via `$exception`, replacing the previous boolean `$exceptionOccurred` property:

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

If you listen for this event, update your listener code accordingly.

<a name="queuebusy-event-property-rename"></a>
#### `QueueBusy` Event Property Rename

**Likelihood Of Impact: Low**

The `Illuminate\Queue\Events\QueueBusy` event property `$connection` has been renamed to `$connectionName` for consistency with other queue events.

If your listeners reference `$connection`, update them to `$connectionName`.

<a name="queue-contract-method-additions"></a>
#### `Queue` Contract Method Additions

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Queue\Queue` contract now includes queue size inspection methods that were previously only declared in docblocks.

If you maintain custom queue driver implementations of this contract, add implementations for:

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
### Routing

<a name="domain-route-registration-precedence"></a>
#### Domain Route Registration Precedence

**Likelihood Of Impact: Low**

Routes with an explicit domain are now prioritized before non-domain routes in route matching.

This allows catch-all subdomain routes to behave consistently even when non-domain routes are registered earlier. If your application relied on previous registration precedence between domain and non-domain routes, review route matching behavior.

<a name="scheduling"></a>
### Scheduling

<a name="withscheduling-registration-timing"></a>
#### `withScheduling` Registration Timing

**Likelihood Of Impact: Very Low**

Schedules registered via `ApplicationBuilder::withScheduling()` are now deferred until `Schedule` is resolved.

If your application relied on immediate schedule registration timing during bootstrap, you may need to adjust that logic.

<a name="security"></a>
### Security

<a name="request-forgery-protection"></a>
#### Request Forgery Protection

**Likelihood Of Impact: High**

Laravel's CSRF middleware has been renamed from `VerifyCsrfToken` to `PreventRequestForgery`, and now includes request-origin verification using the `Sec-Fetch-Site` header.

`VerifyCsrfToken` and `ValidateCsrfToken` remain as deprecated aliases, but direct references should be updated to `PreventRequestForgery`, especially when excluding middleware in tests or route definitions:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

The middleware configuration API now also provides `preventRequestForgery(...)`.

<a name="support"></a>
### Support

<a name="manager-extend-callback-binding"></a>
#### Manager `extend` Callback Binding

**Likelihood Of Impact: Low**

Custom driver closures registered via manager `extend` methods are now bound to the manager instance.

If you previously relied on another bound object (such as a service provider instance) as `$this` inside these callbacks, you should move those values into closure captures using `use (...)`.

<a name="str-factories-reset-between-tests"></a>
#### `Str` Factories Reset Between Tests

**Likelihood Of Impact: Low**

Laravel now resets custom `Str` factories during test teardown.

If your tests depended on custom UUID / ULID / random string factories persisting between test methods, you should set them in each relevant test or setup hook.

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from` Uses Unescaped Unicode By Default

**Likelihood Of Impact: Very Low**

`Illuminate\Support\Js::from` now uses `JSON_UNESCAPED_UNICODE` by default.

If your tests or frontend output comparisons depended on escaped Unicode sequences (for example `\u00e8`), update your expectations.

<a name="utilities"></a>
### Utilities

<a name="symfony-polyfill"></a>
#### Symfony PHP 8.5 Polyfill and Global Function Conflicts

**Likelihood Of Impact: Low**

Laravel 13 introduces a dependency on `symfony/polyfill-php85`. On PHP versions below 8.5, this polyfill defines global functions such as `array_first()` and `array_last()` unless they have already been defined earlier during bootstrap.

These functions may conflict with legacy helper packages like `laravel/helpers` or custom global helpers using the same names. For example, the historical `array_first()` helper accepted a callback to return the first matching element, while the polyfilled version only returns the first element of the array.

To avoid conflicts and ensure consistent behavior across PHP versions, you should prefer the `Illuminate\Support\Arr` methods:

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a name="views"></a>
### Views

<a name="pagination-bootstrap-view-names"></a>
#### Pagination Bootstrap View Names

**Likelihood Of Impact: Low**

The internal pagination view names for Bootstrap 3 defaults are now explicit:

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

If your application references the old pagination view names directly, update those references.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x) and choose which updates are important to you.
