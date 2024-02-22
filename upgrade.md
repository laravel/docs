# Upgrade Guide

- [Upgrading To 11.0 From 10.x](#upgrade-11.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating Minimum Stability](#updating-minimum-stability)
- [Application Structure](#application-structure)
- [Modifying Columns](#modifying-columns)
- [Floating-Point Types](#floating-point-types)
- [SQLite Minimum Version](#sqlite-minimum-version)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Per-Second Rate Limiting](#per-second-rate-limiting)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [The `Enumerable` Contract](#the-enumerable-contract)
- [Eloquent Model `casts` Method](#eloquent-model-casts-method)
- [Spatial Types](#spatial-types)
- [Doctrine DBAL Removal](#doctrine-dbal-removal)

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

#### Composer Dependencies

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^11.0`

</div>

In addition, you may remove the `doctrine/dbal` Composer dependency if you have previously added it to your application, as Laravel is no longer dependent on this package.

<a name="application-structure"></a>
### Application Structure

Laravel 11 introduces a new default application structure with fewer default files. Namely, new Laravel applications contain fewer service providers, middleware, and configuration files.

However, we do **not recommend** that Laravel 10 applications upgrading to Laravel 11 attempt to migrate their application structure, as Laravel 11 has been carefully tuned to also support the Laravel 10 application structure.

Nevertheless, if you choose to attempt to migrate your application's structure and also choose to remove your application's configuration files, you should install the following compatibility package via Composer to ensure that Laravel continues to function correctly:

```shell
composer require laravel/previously-on-laravel-10
```

<a name="authentication"></a>
### Authentication

#### The `UserProvider` Contract

The `Illuminate\Contracts\Auth\UserProvider` contract has received a new `rehashPasswordIfRequired` method. This method is responsible for re-hashing and storing the user's password in storage when the application's hashing algorithm work factor has changed.

If your application or package defines a class that implements this interface, you should add the new `rehashPasswordIfRequired` method to your implementation. A reference implementation can be found within the `Illuminate\Auth\EloquentUserProvider` class:

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
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

Let's look at a concrete example. Previously you would maybe have a migration that created a `votes` column with `unsigned`, `default`, and `comment` attributes:


```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment');
});
```

Later on you might "change" that column to be `nullable` as well:


```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->nullable()->change();
});
```

This would retain the `unsigned`, `default`, and `comment` attributes. However, in Laravel v11 that second "change" migration needs to have all of the previous attributes as well:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->nullable()->change();
});
```

The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

The most easy way to deal with this change is to [squash and prune migrations](/docs/{{version}}/migrations#squashing-migrations) before migrating to Laravel v11:

```bash
php artisan schema:dump --prune
```

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

<a name="mail"></a>
### Mail

<a name="the-mailer-contract"></a>
#### The `Mailer` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Mail\Mailer` contract has received a new `sendNow` method. If your application or package is manually implementing this contract, you should add the new `sendNow` method to your implementation:

```php
public function sendNow($mailable, array $data = [], $callback = null);
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
