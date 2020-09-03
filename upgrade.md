# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- ...
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- ...
</div>

<a name="upgrade-9.0"></a>
## Upgrading To 9.0 From 8.x

#### Estimated Upgrade Time: ?? Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update the following dependencies in your `composer.json` file:

<div class="content-list" markdown="1">
- ...
</div>

The following first-party packages have new major releases to support Laravel 9. If applicable, you should read their individual upgrade guides before upgrading:

<div class="content-list" markdown="1">
- ...
</div>

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 9 support.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...master) and choose which updates are important to you.
