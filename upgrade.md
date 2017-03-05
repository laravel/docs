# Upgrade Guide

- [Upgrading To 5.5 From 5.4](#upgrade-5.5)

<a name="upgrade-5.5"></a>
## Upgrading To 5.5 From 5.4

#### Estimated Upgrade Time: Less than 1 Hour

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Eloquent

#### Model Events

The property `$events` on the Eloquent model has been renamed to `$dispatchesEvents`.

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [Github comparison tool](https://github.com/laravel/laravel/compare/5.4...master) and choose which updates are important to you.
