# Upgrade Guide

- [Upgrading To 7.0 From 6.0](#upgrade-7.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- [Date Serialization](#date-serialization)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [Factory Types](#factory-types)
</div>

<a name="upgrade-7.0"></a>
## Upgrading To 7.0 From 6.0

#### Estimated Upgrade Time: ?

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Symfony 5 Required

**Likelihood Of Impact: Medium**

Laravel 7 upgrade its underlying Symfony components to the 5.x series, which is now also the new minimum compatible version.

### PHP 7.2.5 Required

**Likelihood Of Impact: Low**

The new minimum PHP version is now 7.2.5.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `^7.0` in your `composer.json` file. In addition, update your `nunomaduro/collision` dependency to `^4.0`.

Finally, examine any other 3rd party packages consumed by your application and verify you are using the proper version for Laravel 7 support.

### Eloquent

<a name="date-serialization"></a>
#### Date Serialization

**Likelihood Of Impact: High**

Laravel 7 uses a new date serialization format when using the `toArray` or `toJson` method on Eloquent models. To format dates for serialization, the framework now uses Carbon's `toJSON` method, which produces an ISO-8601 compatible date including timezone information and fractional seconds. In addition, this change provides better support and integration with client-side date parsing libraries.

Previously, dates would be serialized to a format like the following: `2019-12-02 20:01:00`. Dates serialized using the new format will appear like: `2019-12-02T20:01:00.283041Z`.

If you would like to keep using the previous behavior you can override the `serializeDate` method on your model:

    /**
     * Prepare a date for array / JSON serialization.
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d H:i:s');
    }

> {tip} This change only affects serialization of models and model collections to arrays and JSON. This change has no affect on how dates are stored in your database.

<a name="factory-types"></a>
#### Factory Types

**Likelihood Of Impact: Medium**

Laravel 7 removes the "factory types" feature. This feature has been undocumented since October 2016. If you are still using this feature, you should upgrade to [factory states](/docs/{{version}}/database-testing#factory-states), which provide more flexibility.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.0...master) and choose which updates are important to you.
