# Upgrade Guide

- [Upgrading To 6.0 From 5.8](#upgrade-6.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- TODO
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- TODO
</div>

<a name="upgrade-6.0"></a>
## Upgrading To 6.0 From 5.8

#### Estimated Upgrade Time: TODO

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `^6.0` in your `composer.json` file.

Next, examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 6 support.

<a name="eloquent"></a>
### Eloquent

#### Declaration Of Primary Key Type

**Likelihood Of Impact: Medium**

Laravel 6.0 has received [performance optimizations](https://github.com/laravel/framework/pull/28153) for integer key types. If you are using a string as your model's primary key, you should declare the key type using the `$keyType` property on your model:

    /**
     * The "type" of the primary key ID.
     *
     * @var string
     */
    protected $keyType = 'string';

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.8...master) and choose which updates are important to you.
