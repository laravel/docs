# Upgrade Guide

- [Upgrading To 11.0 From 10.x](#upgrade-11.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Application Structure](#application-structure)
- [Floating-Point Types](#floating-point-types)
- [Modifying Columns](#modifying-columns)
- [SQLite Minimum Version](#sqlite-minimum-version)
- [Updating Sanctum](#updating-sanctum)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Password Rehashing](#password-rehashing)
- [Per-Second Rate Limiting](#per-second-rate-limiting)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [Doctrine DBAL Removal](#doctrine-dbal-removal)
- [Eloquent Model `casts` Method](#eloquent-model-casts-method)
- [Spatial Types](#spatial-types)
- [Spatie Once Package](#spatie-once-package)
- [The `Enumerable` Contract](#the-enumerable-contract)
- [The `UserProvider` Contract](#the-user-provider-contract)
- [The `Authenticatable` Contract](#the-authenticatable-contract)

</div>

<a name="upgrade-11.0"></a>
## Upgrading To 11.0 From 10.x

<a name="estimated-upgrade-time-??-minutes"></a>
#### Estimated Upgrade Time: 15 Minutes

> [!NOTE]
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

#### PHP 8.2.0 Required

Laravel now requires PHP 8.2.0 or greater.

#### curl 7.34.0 Required

Laravel's HTTP client now requires curl 7.34.0 or greater.

#### Composer Dependencies

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^11.0`
- `nunomaduro/collision` to `^8.1`
- `laravel/breeze` to `^2.0` (If installed)
- `laravel/cashier` to `^15.0` (If installed)
- `laravel/dusk` to `^8.0` (If installed)
- `laravel/jetstream` to `^5.0` (If installed)
- `laravel/octane` to `^2.3` (If installed)
- `laravel/passport` to `^12.0` (If installed)
- `laravel/sanctum` to `^4.0` (If installed)
- `laravel/spark-stripe` to `^5.0` (If installed)
- `laravel/telescope` to `^5.0` (If installed)
- `inertiajs/inertia-laravel` to `^1.0` (If installed)

</div>

If your application is using Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe, or Telescope, you will need to publish their migrations to your application. Cashier Stripe, Passport, Sanctum, Spark Stripe, and Telescope **no longer automatically load migrations from their own migrations** directory. Therefore, you should run the following command to publish their migrations to your application:

```bash
php artisan vendor:publish --tag=cashier-migrations
php artisan vendor:publish --tag=passport-migrations
php artisan vendor:publish --tag=sanctum-migrations
php artisan vendor:publish --tag=spark-migrations
php artisan vendor:publish --tag=telescope-migrations
```

In addition, you should review the upgrade guides for each of these packages to ensure you are aware of any additional breaking changes:

- [Laravel Cashier Stripe](#cashier-stripe)
- [Laravel Passport](#passport)
- [Laravel Sanctum](#sanctum)
- [Laravel Spark Stripe](#spark-stripe)
- [Laravel Telescope](#telescope)

If you have manually installed the Laravel installer, you should update the installer via Composer:

```bash
composer global require laravel/installer:^5.6
```

Finally, you may remove the `doctrine/dbal` Composer dependency if you have previously added it to your application, as Laravel is no longer dependent on this package.

<a name="application-structure"></a>
### Application Structure

Laravel 11 introduces a new default application structure with fewer default files. Namely, new Laravel applications contain fewer service providers, middleware, and configuration files.

However, we do **not recommend** that Laravel 10 applications upgrading to Laravel 11 attempt to migrate their application structure, as Laravel 11 has been carefully tuned to also support the Laravel 10 application structure.

<a name="authentication"></a>
### Authentication

<a name="password-rehashing"></a>
#### Password Rehashing

Laravel 11 will automatically rehash your user's passwords during authentication if your hashing algorithm's "work factor" has been updated since the password was last hashed.

Typically, this should not disrupt your application; however, you may disable this behavior by adding the `rehash_on_login` option to your application's `config/hashing.php` configuration file:

    'rehash_on_login' => false,

<a name="the-user-provider-contract"></a>
#### The `UserProvider` Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Auth\UserProvider` contract has received a new `rehashPasswordIfRequired` method. This method is responsible for re-hashing and storing the user's password in storage when the application's hashing algorithm work factor has changed.

If your application or package defines a class that implements this interface, you should add the new `rehashPasswordIfRequired` method to your implementation. A reference implementation can be found within the `Illuminate\Auth\EloquentUserProvider` class:

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
```

<a name="the-authenticatable-contract"></a>
#### The `Authenticatable` Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Auth\Authenticatable` contract has received a new `getAuthPasswordName` method. This method is responsible for returning the name of your authenticatable entity's password column.

If your application or package defines a class that implements this interface, you should add the new `getAuthPasswordName` method to your implementation:

```php
public function getAuthPasswordName()
{
    return 'password';
}
```

The default `User` model included with Laravel receives this method automatically since the method is included within the `Illuminate\Auth\Authenticatable` trait.

<a name="the-authentication-exception-class"></a>

#### The `AuthenticationException` Class

**Likelihood Of Impact: Very Low**

The `redirectTo` method of the `Illuminate\Auth\AuthenticationException` class now requires an `Illuminate\Http\Request` instance as its first argument. If you are manually catching this exception and calling the `redirectTo` method, you should update your code accordingly:

```php
if ($e instanceof AuthenticationException) {
    $path = $e->redirectTo($request);
}
```

<a name="cache"></a>
### Cache

<a name="cache-key-prefixes"></a>
#### Cache Key Prefixes

**Likelihood Of Impact: Very Low**

Previously, if a cache key prefix was defined for the DynamoDB, Memcached, or Redis cache stores, Laravel would append a `:` to the prefix. In Laravel 11, the cache key prefix does not receive the `:` suffix. If you would like to maintain the previous prefixing behavior, you can manually add the `:` suffix to your cache key prefix.

<a name="collections"></a>
### Collections

<a name="the-enumerable-contract"></a>
#### The `Enumerable` Contract

**Likelihood Of Impact: Low**

The `dump` method of the `Illuminate\Support\Enumerable` contract has been updated to accept a variadic `...$args` argument. If you are implementing this interface you should update your implementation accordingly:

```php
public function dump(...$args);
```

<a name="database"></a>
### Database

<a name="sqlite-minimum-version"></a>
#### SQLite 3.35.0+

**Likelihood Of Impact: High**

If your application is utilizing an SQLite database, SQLite 3.35.0 or greater is required.

<a name="eloquent-model-casts-method"></a>
#### Eloquent Model `casts` Method

**Likelihood Of Impact: Low**

The base Eloquent model class now defines a `casts` method in order to support the definition of attribute casts. If one of your application's models is defining a `casts` relationship, it may conflict with the `casts` method now present on the base Eloquent model class.

<a name="modifying-columns"></a>
#### Modifying Columns

**Likelihood Of Impact: High**

When modifying a column, you must now explicitly include all the modifiers you want to keep on the column definition after it is changed. Any missing attributes will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column, even if those attributes have been assigned to the column by a previous migration.

For example, imagine you have a migration that creates a `votes` column with the `unsigned`, `default`, and `comment` attributes:

```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('The vote count');
});
```

Later, you write a migration that changes the column to be `nullable` as well:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->nullable()->change();
});
```

In Laravel 10, this migration would retain the `unsigned`, `default`, and `comment` attributes on the column. However, in Laravel 11, the migration must now also include all of the attributes that were previously defined on the column. Otherwise, they will be dropped:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')
        ->unsigned()
        ->default(1)
        ->comment('The vote count')
        ->nullable()
        ->change();
});
```

The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

If you do not want to update all of the existing "change" migrations in your application to retain the column's existing attributes, you may simply [squash your migrations](/docs/{{version}}/migrations#squashing-migrations):

```bash
php artisan schema:dump
```

Once your migrations have been squashed, Laravel will "migrate" the database using your application's schema file before running any pending migrations.

<a name="floating-point-types"></a>
#### Floating-Point Types

**Likelihood Of Impact: High**

The `double` and `float` migration column types have been rewritten to be consistent across all databases.

The `double` column type now creates a `DOUBLE` equivalent column without total digits and places (digits after decimal point), which is the standard SQL syntax. Therefore, you may remove the arguments for `$total` and `$places`:

```php
$table->double('amount');
```

The `float` column type now creates a `FLOAT` equivalent column without total digits and places (digits after decimal point), but with an optional `$precision` specification to determine storage size as a 4-byte single-precision column or an 8-byte double-precision column. Therefore, you may remove the arguments for `$total` and `$places` and specify the optional `$precision` to your desired value and according to your database's documentation:

```php
$table->float('amount', precision: 53);
```

The `unsignedDecimal`, `unsignedDouble`, and `unsignedFloat` methods have been removed, as the unsigned modifier for these column types has been deprecated by MySQL, and was never standardized on other database systems. However, if you wish to continue using the deprecated unsigned attribute for these column types, you may chain the `unsigned` method onto the column's definition:

```php
$table->decimal('amount', total: 8, places: 2)->unsigned();
$table->double('amount')->unsigned();
$table->float('amount', precision: 53)->unsigned();
```

<a name="dedicated-mariadb-driver"></a>
#### Dedicated MariaDB Driver

**Likelihood Of Impact: Very Low**

Instead of always utilizing the MySQL driver when connecting to MariaDB databases, Laravel 11 adds a dedicated database driver for MariaDB.

If your application connects to a MariaDB database, you may update the connection configuration to the new `mariadb` driver to benefit from MariaDB specific features in the future:

    'driver' => 'mariadb',
    'url' => env('DB_URL'),
    'host' => env('DB_HOST', '127.0.0.1'),
    'port' => env('DB_PORT', '3306'),
    // ...

Currently, the new MariaDB driver behaves like the current MySQL driver with one exception: the `uuid` schema builder method creates native UUID columns instead of `char(36)` columns.

If your existing migrations utilize the `uuid` schema builder method and you choose to use the new `mariadb` database driver, you should update your migration's invocations of the `uuid` method to `char` to avoid breaking changes or unexpected behavior:

```php
Schema::table('users', function (Blueprint $table) {
    $table->char('uuid', 36);

    // ...
});
```

<a name="spatial-types"></a>
#### Spatial Types

**Likelihood Of Impact: Low**

The spatial column types of database migrations have been rewritten to be consistent across all databases. Therefore, you may remove `point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, and `multiPolygonZ` methods from your migrations and use `geometry` or `geography` methods instead:

```php
$table->geometry('shapes');
$table->geography('coordinates');
```

To explicitly restrict the type or the spatial reference system identifier for values stored in the column on MySQL, MariaDB, and PostgreSQL, you may pass the `subtype` and `srid` to the method:

```php
$table->geometry('dimension', subtype: 'polygon', srid: 0);
$table->geography('latitude', subtype: 'point', srid: 4326);
```

The `isGeometry` and `projection` column modifiers of the PostgreSQL grammar have been removed accordingly.

<a name="doctrine-dbal-removal"></a>
#### Doctrine DBAL Removal

**Likelihood Of Impact: Low**

The following list of Doctrine DBAL related classes and methods have been removed. Laravel is no longer dependent on this package and registering custom Doctrines types is no longer necessary for the proper creation and alteration of various column types that previously required custom types:

<div class="content-list" markdown="1">

- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` class property
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` method
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` method
- `Illuminate\Database\Connection::isDoctrineAvailable()` method
- `Illuminate\Database\Connection::getDoctrineConnection()` method
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` method
- `Illuminate\Database\Connection::getDoctrineColumn()` method
- `Illuminate\Database\Connection::registerDoctrineType()` method
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` method
- `Illuminate\Database\PDO` directory
- `Illuminate\Database\DBAL\TimestampType` class
- `Illuminate\Database\Schema\Grammars\ChangeColumn` class
- `Illuminate\Database\Schema\Grammars\RenameColumn` class
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` method

</div>

In addition, registering custom Doctrine types via `dbal.types` in your application's `database` configuration file is no longer required.

If you were previously using Doctrine DBAL to inspect your database and its associated tables, you may use Laravel's new native schema methods (`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()`, etc.) instead.

<a name="deprecated-schema-methods"></a>
#### Deprecated Schema Methods

**Likelihood Of Impact: Very Low**

The deprecated, Doctrine based `Schema::getAllTables()`, `Schema::getAllViews()`, and `Schema::getAllTypes()` methods have been removed in favor of new Laravel native `Schema::getTables()`, `Schema::getViews()`, and `Schema::getTypes()` methods.

When using PostgreSQL and SQL Server, none of the new schema methods will accept a three-part reference (e.g. `database.schema.table`). Therefore, you should use `connection()` to declare the database instead:

```php
Schema::connection('database')->hasTable('schema.table');
```

<a name="get-column-types"></a>
#### Schema Builder `getColumnType()` Method

**Likelihood Of Impact: Very Low**

The `Schema::getColumnType()` method now always returns actual type of the given column, not the Doctrine DBAL equivalent type.

<a name="database-connection-interface"></a>
#### Database Connection Interface

**Likelihood Of Impact: Very Low**

The `Illuminate\Database\ConnectionInterface` interface has received a new `scalar` method. If you are defining your own implementation of this interface, you should add the `scalar` method to your implementation:

```php
public function scalar($query, $bindings = [], $useReadPdo = true);
```

<a name="dates"></a>
### Dates

<a name="carbon-3"></a>
#### Carbon 3

**Likelihood Of Impact: Medium**

Laravel 11 supports both Carbon 2 and Carbon 3. Carbon is a date manipulation library utilized extensively by Laravel and packages throughout the ecosystem. If you install Carbon 3, you should review Carbon's [change log](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0).

<a name="mail"></a>
### Mail

<a name="the-mailer-contract"></a>
#### The `Mailer` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Mail\Mailer` contract has received a new `sendNow` method. If your application or package is manually implementing this contract, you should add the new `sendNow` method to your implementation:

```php
public function sendNow($mailable, array $data = [], $callback = null);
```

<a name="packages"></a>
### Packages

<a name="publishing-service-providers"></a>
#### Publishing Service Providers to the Application

**Likelihood Of Impact: Very Low**

If you have written a Laravel package that manually publishes a service provider to the application's `app/Providers` directory and manually modifies the application's `config/app.php` configuration file to register the service provider, you should update your package to utilize the new `ServiceProvider::addProviderToBootstrapFile` method.

The `addProviderToBootstrapFile` method will automatically add the service provider you have published to the application's `bootstrap/providers.php` file, since the `providers` array does not exist within the `config/app.php` configuration file in new Laravel 11 applications.

```php
use Illuminate\Support\ServiceProvider;

ServiceProvider::addProviderToBootstrapFile(Provider::class);
```

<a name="queues"></a>
### Queues

<a name="the-batch-repository-interface"></a>
#### The `BatchRepository` Interface

**Likelihood Of Impact: Very Low**

The `Illuminate\Bus\BatchRepository` interface has received a new `rollBack` method. If you are implementing this interface within your own package or application, you should add this method to your implementation:

```php
public function rollBack();
```

<a name="synchronous-jobs-in-database-transactions"></a>
#### Synchronous Jobs in Database Transactions

**Likelihood Of Impact: Very Low**

Previously, synchronous jobs (jobs using the `sync` queue driver) would execute immediately, regardless of whether the `after_commit` configuration option of the queue connection was set to `true` or the `afterCommit` method was invoked on the job.

In Laravel 11, synchronous queue jobs will now respect the "after commit" configuration of the queue connection or job.

<a name="rate-limiting"></a>
### Rate Limiting

<a name="per-second-rate-limiting"></a>
#### Per-Second Rate Limiting

**Likelihood Of Impact: Medium**

Laravel 11 supports per-second rate limiting instead of being limited to per-minute granularity. There are a variety of potential breaking changes you should be aware of related to this change.

The `GlobalLimit` class constructor now accepts seconds instead of minutes. This class is not documented and would not typically be used by your application:

```php
new GlobalLimit($attempts, 2 * 60);
```

The `Limit` class constructor now accepts seconds instead of minutes. All documented usages of this class are limited to static constructors such as `Limit::perMinute` and `Limit::perSecond`. However, if you are instantiating this class manually, you should update your application to provide seconds to the class's constructor:

```php
new Limit($key, $attempts, 2 * 60);
```

The `Limit` class's `decayMinutes` property has been renamed to `decaySeconds` and now contains seconds instead of minutes.

The `Illuminate\Queue\Middleware\ThrottlesExceptions` and `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` class constructors now accept seconds instead of minutes:

```php
new ThrottlesExceptions($attempts, 2 * 60);
new ThrottlesExceptionsWithRedis($attempts, 2 * 60);
```

<a name="cashier-stripe"></a>
### Cashier Stripe

<a name="updating-cashier-stripe"></a>
#### Updating Cashier Stripe

**Likelihood Of Impact: High**

Laravel 11 no longer supports Cashier Stripe 14.x. Therefore, you should update your application's Laravel Cashier Stripe dependency to `^15.0` in your `composer.json` file.

Cashier Stripe 15.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Cashier Stripe's migrations to your application:

```shell
php artisan vendor:publish --tag=cashier-migrations
```

Please review the complete [Cashier Stripe upgrade guide](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md) for additional breaking changes.

<a name="spark-stripe"></a>
### Spark (Stripe)

<a name="updating-spark-stripe"></a>
#### Updating Spark Stripe

**Likelihood Of Impact: High**

Laravel 11 no longer supports Laravel Spark Stripe 4.x. Therefore, you should update your application's Laravel Spark Stripe dependency to `^5.0` in your `composer.json` file.

Spark Stripe 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Spark Stripe's migrations to your application:

```shell
php artisan vendor:publish --tag=spark-migrations
```

Please review the complete [Spark Stripe upgrade guide](https://spark.laravel.com/docs/spark-stripe/upgrade.html) for additional breaking changes.

<a name="passport"></a>
### Passport

<a name="updating-telescope"></a>
#### Updating Passport

**Likelihood Of Impact: High**

Laravel 11 no longer supports Laravel Passport 11.x. Therefore, you should update your application's Laravel Passport dependency to `^12.0` in your `composer.json` file.

Passport 12.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Passport's migrations to your application:

```shell
php artisan vendor:publish --tag=passport-migrations
```

In addition, the password grant type is disabled by default. You may enable it by invoking the `enablePasswordGrant` method in the `boot` method of your application's `AppServiceProvider`:

    public function boot(): void
    {
        Passport::enablePasswordGrant();
    }

<a name="sanctum"></a>
### Sanctum

<a name="updating-sanctum"></a>
#### Updating Sanctum

**Likelihood Of Impact: High**

Laravel 11 no longer supports Laravel Sanctum 3.x. Therefore, you should update your application's Laravel Sanctum dependency to `^4.0` in your `composer.json` file.

Sanctum 4.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Sanctum's migrations to your application:

```shell
php artisan vendor:publish --tag=sanctum-migrations
```

Then, in your application's `config/sanctum.php` configuration file, you should update the references to the `authenticate_session`, `encrypt_cookies`, and `validate_csrf_token` middleware to the following:

    'middleware' => [
        'authenticate_session' => Laravel\Sanctum\Http\Middleware\AuthenticateSession::class,
        'encrypt_cookies' => Illuminate\Cookie\Middleware\EncryptCookies::class,
        'validate_csrf_token' => Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
    ],

<a name="telescope"></a>
### Telescope

<a name="updating-telescope"></a>
#### Updating Telescope

**Likelihood Of Impact: High**

Laravel 11 no longer supports Laravel Telescope 4.x. Therefore, you should update your application's Laravel Telescope dependency to `^5.0` in your `composer.json` file.

Telescope 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Telescope's migrations to your application:

```shell
php artisan vendor:publish --tag=telescope-migrations
```

<a name="spatie-once-package"></a>
### Spatie Once Package

**Likelihood Of Impact: Medium**

Laravel 11 now provides its own [`once` function](/docs/{{version}}/helpers#method-once) to ensure that a given closure is only executed once. Therefore, if your application has a dependency on the `spatie/once` package, you should remove it from your application's `composer.json` file to avoid conflicts.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/10.x...11.x) and choose which updates are important to you.
