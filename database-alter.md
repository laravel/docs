# Database Alter Statements

- [Introduction](#introduction)
    - [Expected Exception](#expected-exception)
- [Installation](#installation)
- [Timestamp Fields](#timestamp-fields)
- [Non-standard Field Types](#non-standard-field-types)
    - [enum columns](#enum-columns)

<a name="introduction"></a>
## Introduction

Laravel supports migrations that alter existing database structure, but it
does not do so out-of-the-box.  To support altering database structure Laraval
depends on a 3rd party package loaded through `composer` and suggested as
an optional dependency when installing with `composer`.

<a name="expected-exception"></a>
### Expected Exception

When you try to run a migration that alters a database field it is expected
you will get the following exception message:

> Changing columns for table "<table_name>" requires Doctrine DBAL. Please install
  the doctrine/dbal package.

<a name="installation"></a>
## Installation

Run `composer` from the root of your project as

```php
composer install doctrine/dbal
```

After installation most field types will be able to be altered.  However, if
you are altering a `datetime` field to a `timestamp`, or if you are altering a
`timestamp` field, there are additional steps to enable support.

<a name="timestamp-fields"></a>
## Timestamp Fields

Timestamps are a common field type in Laravel but in `doctrine/dbal` they are
not supported by a default installation.  So, in order to support timestamp
fields you must add some configuration to your `config/database.php` file:

Add this line to the top of the file:
```php
use Illuminate\Database\DBAL\TimestampType;
```

Then inside your database configuration array add:
```php
'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

This configuration change will allow all `timestamp` fields to be altered.

You may add your own custom types to this array using the same pattern
(see below).

<a name="non-standard-field-types"></a>
## Non-standard Field Types

After implementing the configuration changes in
[Timestamp Fields](#timestamp-fields) you may extend the configuration to
support other field types.  The documentation to build
custom field handlers for `doctrine/dbal` is at
[https://www.doctrine-project.org/projects/doctrine-orm/en/latest/cookbook/custom-mapping-types.html](https://www.doctrine-project.org/projects/doctrine-orm/en/latest/cookbook/custom-mapping-types.html)
and custom field handlers can be added to the `types` array shown above.

<a name="enum-columns"></a>
### enum Columns

In MySQL an `enum` column holds string values and allows for a distinct list
of possible values.  `enum` columns are not supported by Laravel migrations
but you can add custom configuration to enable them.

Follow this guide [https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/cookbook/mysql-enums.html](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/cookbook/mysql-enums.html) 
then add your custom class to the `types` array shown above.
