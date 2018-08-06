# Upgrade Guide

- [Upgrading To 5.7.0 From 5.6](#upgrade-5.7.0)

<a name="upgrade-5.7.0"></a>
## Upgrading To 5.7.0 From 5.6

#### Estimated Upgrade Time: 10 - 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.7.*` in your `composer.json` file.

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.7 support.

### Authentication

#### The `Authenticate` Middleware

The `authenticate` method of the `Illuminate\Auth\Middleware\Authenticate` middleware has been updated to accept the incoming `$request` as its first argument:

    /**
     * Determine if the user is logged in to any of the given guards.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  array  $guards
     * @return void
     *
     * @throws \Illuminate\Auth\AuthenticationException
     */
    protected function authenticate($request, array $guards)

### Blade

#### The `or` Operator

The Blade "or" operator has been removed in favor of PHP's built-in `??` null coalesce operator, which has the same purpose:

    // Laravel 5.6...
    {{ $foo or 'default' }}

    // Laravel 5.7...
    {{ $foo ?? 'default' }}

### Database

#### The `softDeletesTz` Migration Method

The schema table builder's `softDeletesTz` method now accepts the column name as its first argument, while the `$precision` has been moved to the second argument position:

    /**
     * Add a "deleted at" timestampTz for the table.
     *
     * @param  string  $column
     * @param  int  $precision
     * @return \Illuminate\Support\Fluent
     */
    public function softDeletesTz($column = 'deleted_at', $precision = 0)

### Filesystem

#### `Filesystem` Contract Methods

The `readStream` and `writeStream` methods [have been added to the `Illuminate\Contracts\Filesystem\Filesystem` contract](https://github.com/laravel/framework/pull/23755). If you are implementing this interface, you should add these methods to your implementation.

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.5...master) and choose which updates are important to you.
