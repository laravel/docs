# Upgrade Guide

- [Upgrading To 12.0 From 11.x](#upgrade-12.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)

</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Concurrency Result Index Mapping](#concurrency-result-index-mapping)
- [Multi-schema Database Inspecting](#multi-schema-database-inspecting)
- [Image Validation Now Excludes SVGs](#image-validation)
- [Nested Array Request Merging](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## Upgrading To 12.0 From 11.x

#### Estimated Upgrade Time: 5 Minutes

> [!NOTE]
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^12.0`

</div>

<a name="carbon-3"></a>
#### Carbon 3

**Likelihood Of Impact: Low**

Support for [Carbon 2.x](https://carbon.nesbot.com/docs/) has been removed. All Laravel 12 applications now require [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3).

<a name="updating-the-laravel-installer"></a>
### Updating the Laravel Installer

If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation to be compatible with Laravel 12.x and the [new Laravel starter kits](https://laravel.com/starter-kits). If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`:

```shell
composer global update laravel/installer
```

If you originally installed PHP and Laravel via `php.new`, you may simply re-run the `php.new` installation commands for your operating system to install the latest version of PHP and the Laravel installer:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release.

<a name="concurrency"></a>
### Concurrency

<a name="concurrency-result-index-mapping"></a>
#### Concurrency Result Index Mapping

**Likelihood Of Impact: Low**

When invoking the `Concurrency::run` method with an associative array, the results of the concurrent operations are now returned with their associated keys:

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="database"></a>
### Database

<a name="multi-schema-database-inspecting"></a>
#### Multi-schema Database Inspecting

**Likelihood Of Impact: Low**

The `Schema::getTables()`, `Schema::getViews()` and `Schema::getTypes()` methods now include the results from all schemas by default. You may pass the `schema` argument to retrieve the result for the given schema only:

```php
// All tables on all schemas...
$tables = Schema::getTables();

// All tables on the 'main' schema...
$table = Schema::getTables(schema: 'main');

// All tables on the 'main' and 'blog' schemas...
$table = Schema::getTables(schema: ['main', 'blog']);
```

The `Schema::getTableListing()` method now returns schema-qualified table names by default. You may pass the `schemaQualified` argument to change the behavior as desired:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$table = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$table = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

The `db:table` and `db:show` commands now output results of all schemas on MySQL, MariaDB and SQLite, just like PostgreSQL and SQL Server. Consistent usage across all DB drivers.

<a name="requests"></a>
### Requests

<a name="nested-array-request-merging"></a>
#### Nested Array Request Merging

**Likelihood Of Impact: Low**

The `$request->mergeIfMissing()` method now allows merging nested array data using "dot" notation. If you were previously relying on this method to create a top-level array key containing the "dot" notation version of the key, you may need to adjust your application to account for this new behavior:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="validation"></a>
### Validation

<a name="image-validation"></a>
#### Image Validation Now Excludes SVGs

The `image` validation rule no longer allows SVG images by default. If you would like to allow SVGs when using the `image` rule, you must explicitly allow them:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x) and choose which updates are important to you.
