# Deprecations

- [Introduction](#introduction)
    - [Route Middleware](#route-middleware)

<a name="introduction"></a>
## Introduction

Laravel will, when necessary, deprecate certain features or code within the framework. In an effort to help you track those changes, and update your applications prior to the deprecated code being removed, this page will highlight some of those deprecations. The best way to find **all** the deprecated code is to search `laravel/framework` for `@deprecated`.

<a name="route-middleware"></a>
### Route Middleware

In the `\Illuminate\Foundation\Http\Kernel` class, the `$routeMiddleware` property was renamed to `$middlewareAliases` to better reflect its purpose. The `$routeMiddleware` property and the `getRouteMiddleware()` method have been deprecated, and will be removed in Laravel 11.

https://github.com/laravel/framework/commit/78eb546e9c789ac84af87bb362535cc2883e4db4
