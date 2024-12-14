# Upgrade Guide

- [Upgrading To 5.6.30 From 5.6](#upgrade-5.6.30)
- [Upgrading To 5.6.0 From 5.5](#upgrade-5.6.0)

<a name="upgrade-5.6.30"></a>
## Upgrading To 5.6.30 From 5.6 (Security Release)

Laravel 5.6.30 is a security release of Laravel and is recommended as an immediate upgrade for all users. Laravel 5.6.30 also contains a breaking change to cookie encryption and serialization logic, so please read the following notes carefully when upgrading your application.

**This vulnerability may only be exploited if your application encryption key (`APP_KEY` environment variable) has been accessed by a malicious user.** Typically, it is not possible for users of your application to gain access to this value. However, ex-employees that had access to the encryption key may be able to use the key to attack your applications. If you have any reason to believe your encryption key is in the hands of a malicious party, you should **always** rotate the key to a new value.

### Cookie Serialization

Laravel 5.6.30 disables all serialization / unserialization of cookie values. Since all Laravel cookies are encrypted and signed, cookie values are typically considered safe from client tampering. **However, if your application's encryption key is in the hands of a malicious party, that party could craft cookie values using the encryption key and exploit vulnerabilities inherent to PHP object serialization / unserialization, such as calling arbitrary class methods within your application.**

Disabling serialization on all cookie values will invalidate all of your application's sessions and users will need to log into the application again (unless they have a `remember_token` set, in which case the user will be logged into a new session automatically). In addition, any other encrypted cookies your application is setting will have invalid values. For this reason, you may wish to add additional logic to your application to validate that your custom cookie values match an expected list of values; otherwise, you should discard them.

#### Configuring Cookie Serialization

Since this vulnerability is not able to be exploited without access to your application's encryption key, we have chosen to provide a way to re-enable encrypted cookie serialization while you make your application compatible with these changes. To enable / disable cookie serialization, you may change the static `serialize` property of the `App\Http\Middleware\EncryptCookies` [middleware](https://github.com/laravel/laravel/blob/5.6/app/Http/Middleware/EncryptCookies.php):

    /**
     * Indicates if cookies should be serialized.
     *
     * @var bool
     */
    protected static $serialize = true;

> **Note:** When encrypted cookie serialization is enabled, your application will be vulnerable to attack if its encryption key is accessed by a malicious party. If you believe your key may be in the hands of a malicious party, you should rotate the key to a new value before enabling encrypted cookie serialization.

### Dusk 4.0.0

Dusk 4.0.0 has been released and does not serialize cookies. If you choose to enable cookie serialization, you should continue to use Dusk 3.0.0. Otherwise, you should upgrade to Dusk 4.0.0.

### Passport 6.0.7

Passport 6.0.7 has been released with a new `Laravel\Passport\Passport::withoutCookieSerialization()` method. Once you have disabled cookie serialization, you should call this method within your application's `AppServiceProvider`.

<a name="upgrade-5.6.0"></a>
## Upgrading To 5.6.0 From 5.5

#### Estimated Upgrade Time: 10 - 30 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### PHP

Laravel 5.6 requires PHP 7.1.3 or higher.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.6.*` and your `fideloper/proxy` dependency to `^4.0` in your `composer.json` file.

If you are using the `laravel/browser-kit-testing` package, you should update the package to `4.*` in your composer.json file.

In addition, if you are using the following first-party Laravel packages, you should upgrade them to their latest release:

<div class="content-list" markdown="1">

- Dusk (Upgrade To `^3.0`)
- Passport (Upgrade To `^6.0`)
- Scout (Upgrade To `^4.0`)

</div>

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.6 support.

#### Symfony 4

All of the underlying Symfony components used by Laravel have been upgraded to the Symfony `^4.0` release series. If you are directly interacting with Symfony components within your application, you should review the [Symfony change log](https://github.com/symfony/symfony/blob/4.0/UPGRADE-4.0.md).

#### PHPUnit

You should update the `phpunit/phpunit` dependency of your application to `^7.0`.

### Arrays

#### The `Arr::wrap` Method

Passing `null` to the `Arr::wrap` method will now return an empty array.

### Artisan

#### The `optimize` Command

The previously deprecated `optimize` Artisan command has been removed. With recent improvements to PHP itself including the OPcache, the `optimize` command no longer provides any relevant performance benefit. Therefore, you may remove `php artisan optimize` from the `scripts` within your `composer.json` file.

### Blade

#### HTML Entity Encoding

In previous versions of Laravel, Blade (and the `e` helper) would not double encode HTML entities. This was not the default behavior of the underlying `htmlspecialchars` function and could lead to unexpected behavior when rendering content or passing in-line JSON content to JavaScript frameworks.

In Laravel 5.6, Blade and the `e` helper will double encode special characters by default. This brings these features into alignment with the default behavior of the underlying `htmlspecialchars` PHP function. If you would like to maintain the previous behavior of preventing double encoding, you may use the `Blade::withoutDoubleEncoding` method:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Blade::withoutDoubleEncoding();
        }
    }

### Cache

#### The Rate Limiter `tooManyAttempts` Method

The unused `$decayMinutes` parameter was removed from this method's signature. If you were overriding this method with your own implementation, you should also remove the argument from your method's signature.

### Database

#### Index Order Of Morph Columns

The indexing of the columns built by the `morphs` migration method has been reversed for better performance. If you are using the `morphs` method in one of your migrations, you may receive an error when attempting to run the migration's `down` method. If the application is still in development, you may use the `migrate:fresh` command to rebuild the database from scratch. If the application is in production, you should pass an explicit index name to the `morphs` method.

#### `MigrationRepositoryInterface` Method Addition

A new `getMigrationsBatches` method has been added to the `MigrationRepositoryInterface`. In the very unlikely event that you were defining your own implementation of this class, you should add this method to your implementation. You may view the default implementation in the framework as an example.

### Eloquent

#### The `getDateFormat` Method

This `getDateFormat` method is now `public` instead of `protected`.

### Hashing

#### New Configuration File

All hashing configuration is now housed in its own `config/hashing.php` configuration file. You should place a copy of the [default configuration file](https://github.com/laravel/laravel/blob/5.6/config/hashing.php) in your own application. Most likely, you should maintain the `bcrypt` driver as your default driver. However, `argon` is also supported.

### Helpers

#### The `e` Helper

In previous versions of Laravel, Blade (and the `e` helper) would not double encode HTML entities. This was not the default behavior of the underlying `htmlspecialchars` function and could lead to unexpected behavior when rendering content or passing in-line JSON content to JavaScript frameworks.

In Laravel 5.6, Blade and the `e` helper will double encode special characters by default. This brings these features into alignment with the default behavior of the underlying `htmlspecialchars` PHP function. If you would like to maintain the previous behavior of preventing double encoding, you may pass `false` as the second argument to the `e` helper:

    <?php echo e($string, false); ?>

### Logging

#### New Configuration File

All logging configuration is now housed in its own `config/logging.php` configuration file. You should place a copy of the [default configuration file](https://github.com/laravel/laravel/blob/5.6/config/logging.php) in your own application and tweak the settings based on your application's needs.

The `log` and `log_level` configuration options may be removed from the `config/app.php` configuration file.

#### The `configureMonologUsing` Method

If you were using the `configureMonologUsing` method to customize the Monolog instance for your application, you should now create a `custom` Log channel. For more information on how to create custom channels, check out the [full logging documentation](/docs/5.6/logging#creating-custom-channels).

#### The Log `Writer` Class

The `Illuminate\Log\Writer` class has been renamed to `Illuminate\Log\Logger`. If you were explicitly type-hinting this class as a dependency of one of your application's classes, you should update the class reference to the new name. Or, alternatively, you should strongly consider type-hinting the standardized `Psr\Log\LoggerInterface` interface instead.

#### The `Illuminate\Contracts\Logging\Log` Interface

This interface has been removed since this interface was a total duplication of the `Psr\Log\LoggerInterface` interface. You should type-hint the `Psr\Log\LoggerInterface` interface instead.

### Mail

#### `withSwiftMessage` Callbacks

In previous releases of Laravel, Swift Messages customization callbacks registered using `withSwiftMessage` were called _after_ the content was already encoded and added to the message. These callbacks are now called _before_ the content is added, which allows you to customize the encoding or other message options as needed.

### Pagination

#### Bootstrap 4

The pagination links generated by the paginator now default to Bootstrap 4. To instruct the paginator to generate Bootstrap 3 links, call the `Paginator::useBootstrapThree` method from the `boot` method of your `AppServiceProvider`:

    <?php

    namespace App\Providers;

    use Illuminate\Pagination\Paginator;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Paginator::useBootstrapThree();
        }
    }

### Resources

#### The `original` Property

The `original` property of [resource responses](/docs/5.6/eloquent-resources) is now set to the original model instead of a JSON string / array. This allows for easier inspection of the response's model during testing.

### Routing

#### Returning Newly Created Models

When returning a newly created Eloquent model directly from a route, the response status will now automatically be set to `201` instead of `200`. If any of your application's tests were explicitly expecting a `200` response, those tests should be updated to expect `201`.

### Trusted Proxies

Due to underlying changes in the trusted proxy functionality of Symfony HttpFoundation, slight changes must be made to your application's `App\Http\Middleware\TrustProxies` middleware.

The `$headers` property, which was previously an array, is now a bit property that accepts several different values. For example, to trust all forwarded headers, you may update your `$headers` property to the following value:

    use Illuminate\Http\Request;

    /**
     * The headers that should be used to detect proxies.
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_ALL;

For more information on the available `$headers` values, check out the full documentation on [trusting proxies](/docs/5.6/requests#configuring-trusted-proxies).

### Validation

#### The `ValidatesWhenResolved` Interface

The `validate` method of the `ValidatesWhenResolved` interface / trait has been renamed to `validateResolved` in order to avoid conflicts with the `$request->validate()` method.

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.5...5.6) and choose which updates are important to you.
