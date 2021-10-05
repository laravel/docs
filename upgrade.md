# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="upgrade-9.0"></a>
## Upgrading To 9.0 From 8.x

<a name="queue"></a>
### Queue

<a name="the-opis-closure-library"></a>
#### The `opis/closure` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated classes `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you.
