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
- ...
</div>

<a name="upgrade-7.0"></a>
## Upgrading To 7.0 From 6.0

#### Estimated Upgrade Time: ?

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Symfony 5 Required

**Likelihood Of Impact: Medium**

Laravel 7 adds support for Symfony 5 which is now also the new minimum compatible version.

### PHP 7.2.5 Required

**Likelihood Of Impact: Low**

The new minimum PHP version (which mimics Symfony 5.0) is now 7.2.5.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `^7.0` in your `composer.json` file.

Next, examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 7 support.

### Eloquent

<a name="date-serialization"></a>
#### Date Serialization

**Likelihood Of Impact: High**

Laravel 7 comes with a new default for serializing dates when using the `toArray` or `toJson` method on Eloquent models. It makes use of the default Carbon `toJSON` behavior and will provide a datetime string with fractions and timezone info.

The previous behavior would serialize a date, for example, to `2019-12-02 20:01:00`. The new behavior will serialize a date to something like `2019-12-02T20:01:00.283041Z`. This will provide more info if you're, for example, building API's.

If you want to keep using the previous behavior you can override the `serializeDate` method on your model:

    /**
     * Prepare a date for array / JSON serialization.
     */
    protected function serializeDate(DateTimeInterface $date) : string
    {
        return $date->format('Y-m-d H:i:s');
    }

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.0...master) and choose which updates are important to you.
