# Upgrade Guide

- [Upgrading To 5.8.0 From 5.7](#upgrade-5.8.0)

<a name="upgrade-5.8.0"></a>
## Upgrading To 5.8.0 From 5.7

#### Estimated Upgrade Time: TBD

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.8.*` in your `composer.json` file.

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.8 support.

### Blade

#### Blade Custom Directives

**Likelihood Of Impact: Very Low**

Creating a custom Blade directive with an invalid name will now [throw an `/InvalidArgumentException`](https://github.com/laravel/framework/pull/25766). This change is unlikely to affect any projects, because if an invalid name was used previously, it would not have rendered at all when called.

### Facades

#### Facade Service Resolving

**Likelihood Of Impact: Low**

The `getFacadeAccessor` method may now [only return the string value representing the container identifier of the service](https://github.com/laravel/framework/pull/25525). Previously, this method may have returned an object instance.

### Routing

#### The `UrlGenerator` Contract

**Likelihood Of Impact: Very Low**

The `previous` method [has been added to the `Illuminate\Contracts\Routing\UrlGenerator` contract](https://github.com/laravel/framework/pull/25616). If you are implementing this interface, you should add this method to your implementation.

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.7...master) and choose which updates are important to you.
