# Upgrade Guide

- [Upgrading To 8.0 From 7.x](#upgrade-8.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [PHP 7.3.0 Required](#php-7.3.0-required)
</div>

<a name="upgrade-8.0"></a>
## Upgrading To 8.0 From 7.x

#### Estimated Upgrade Time: ?? Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="php-7.3.0-required"></a>
### PHP 7.3.0 Required

**Likelihood Of Impact: Medium**

The new minimum PHP version is now 7.3.0.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `^8.0` in your `composer.json` file. In addition, update your `nunomaduro/collision` dependency to `^5.0`.

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 8 support.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.x...master) and choose which updates are important to you.
