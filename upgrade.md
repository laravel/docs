# Upgrade Guide

- [Upgrading To 11.0 From 10.x](#upgrade-11.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating Minimum Stability](#updating-minimum-stability)
- [SQLite Minimum Version](#sqlite-minimum-version)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Modifying Columns](#modifying-columns)
- [Floating-Point Types](#floating-point-types)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [The `Enumerable` Contract](#the-enumerable-contract)
- [Spatial Types](#spatial-types)
- [Doctrine DBAL Removal](#doctrine-dbal-removal)

</div>

<a name="upgrade-11.0"></a>
## Upgrading To 11.0 From 10.x

<a name="estimated-upgrade-time-??-minutes"></a>
#### Estimated Upgrade Time: ?? Minutes

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

<a name="modifying-columns"></a>
#### Modifying Columns

**Likelihood Of Impact: Medium**

When modifying a column, you must now explicitly include all the modifiers you want to keep on the column definition after it is changed. Any missing attributes will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column, even if those attributes have been assigned to the column by a previous migration:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="floating-point-types"></a>
#### Floating-Point Types

**Likelihood Of Impact: Medium**

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

