# Upgrade Guide

- [Upgrading To 5.7.0 From 5.6](#upgrade-5.7.0)

<a name="upgrade-5.7.0"></a>
## Upgrading To 5.7.0 From 5.6

#### Estimated Upgrade Time: 10 - 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.7.*` in your `composer.json` file.

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.7 support.

### Application

#### The `register` Method

**Likelihood Of Impact: Very Low**

The unused `options` argument of the `Illuminate\Foundation\Application` class' `register` method has been removed. If you are overriding this method, you should update your method's signature:

    /**
     * Register a service provider with the application.
     *
     * @param  \Illuminate\Support\ServiceProvider|string  $provider
     * @param  bool   $force
     * @return \Illuminate\Support\ServiceProvider
     */
    public function register($provider, $force = false);

### Authentication

#### The `Authenticate` Middleware

**Likelihood Of Impact: Low**

The `authenticate` method of the `Illuminate\Auth\Middleware\Authenticate` middleware has been updated to accept the incoming `$request` as its first argument. If you are overriding this method in your own `Authenticate` middleware, you should update your middleware's signature:

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

#### The `ResetsPasswords` Trait

**Likelihood Of Impact: Low**

The protected `sendResetResponse` method of the `ResetsPasswords` trait now accepts the incoming `Illuminate\Http\Request` as its first argument. If you are overriding this method, you should update your method's signature:

    /**
     * Get the response for a successful password reset.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $response
     * @return \Illuminate\Http\RedirectResponse|\Illuminate\Http\JsonResponse
     */
    protected function sendResetResponse(Request $request, $response)

#### The `SendsPasswordResetEmails` Trait

**Likelihood Of Impact: Low**

The protected `sendResetLinkResponse` method of the `SendsPasswordResetEmails` trait now accepts the incoming `Illuminate\Http\Request` as its first argument. If you are overriding this method, you should update your method's signature:

    /**
     * Get the response for a successful password reset link.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $response
     * @return \Illuminate\Http\RedirectResponse|\Illuminate\Http\JsonResponse
     */
    protected function sendResetLinkResponse(Request $request, $response)

### Blade

#### The `or` Operator

**Likelihood Of Impact: High**

The Blade "or" operator has been removed in favor of PHP's built-in `??` "null coalesce" operator, which has the same purpose and functionality:

    // Laravel 5.6...
    {{ $foo or 'default' }}

    // Laravel 5.7...
    {{ $foo ?? 'default' }}

### Carbon

**Likelihood Of Impact: Very Low**

Carbon "macros" are now handled by the Carbon library directly instead of Laravel's extension of the library. We do not expect this to break your code; however, [please make us aware of any problems you encounter related to this change](https://github.com/laravel/framework/pull/23938).

### Collections

#### The `split` Method

**Likelihood Of Impact: Low**

The `split` method [has been updated to always return the requested number of "groups"](https://github.com/laravel/framework/pull/24088), unless the total number of items in the original collection is less than the requested collection count. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution.

### Database

#### The `softDeletesTz` Migration Method

**Likelihood Of Impact: Low**

The schema table builder's `softDeletesTz` method now accepts the column name as its first argument, while the `$precision` has been moved to the second argument position:

    /**
     * Add a "deleted at" timestampTz for the table.
     *
     * @param  string  $column
     * @param  int  $precision
     * @return \Illuminate\Support\Fluent
     */
    public function softDeletesTz($column = 'deleted_at', $precision = 0)

### Eloquent

#### The `latest` / `oldest` Methods

**Likelihood Of Impact: Low**

The Eloquent query builder's `latest` and `oldest` methods have been updated to respect custom "created at" timestamp columns that may be specified on your Eloquent models. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution.

#### The `wasChanged` Method

**Likelihood Of Impact: Very Low**

An Eloquent model's changes are now available to the `wasChanged` method **before** firing the `updated` model event. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/25026).

### Filesystem

#### `Filesystem` Contract Methods

**Likelihood Of Impact: Low**

The `readStream` and `writeStream` methods [have been added to the `Illuminate\Contracts\Filesystem\Filesystem` contract](https://github.com/laravel/framework/pull/23755). If you are implementing this interface, you should add these methods to your implementation.

### Mail

#### Mailable Dynamic Variable Casing

**Likelihood Of Impact: Medium**

Variables that are dynamically passed to mailable views [are now automatically "camel cased"](https://github.com/laravel/framework/pull/24232), which makes mailable dynamic variable behavior consistent with dynamic view variables. Dynamic mailable variables are not a documented Laravel feature, so likelihood of impact to your application is low.

### Routing

#### The `Route::redirect` Method

The `Route::redirect` method now returns a `302` HTTP status code redirect. The `permanentRedirect` method has been added to allow `301` redirects.

    // Return a 302 redirect...
    Route::redirect('/foo', '/bar');

    // Return a 301 redirect...
    Route::permanentRedirect('/foo', '/bar');

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.6...master) and choose which updates are important to you.
