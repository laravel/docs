# Upgrade Guide

- [Upgrading To 5.8.0 From 5.7](#upgrade-5.8.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- [Cache TTL In Seconds](#cache-ttl-in-seconds)
- [Markdown File Directory Change](#markdown-file-directory-change)
- [Nexmo / Slack Notification Channels](#nexmo-slack-notification-channels)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [SQLite Version Constraints](#sqlite)
- [Prefer String And Array Classes Over Helpers](#string-and-array-helpers)
- [Deferred Service Providers](#deferred-service-providers)
- [PSR-16 Conformity](#psr-16-conformity)
</div>

<a name="upgrade-5.8.0"></a>
## Upgrading To 5.8.0 From 5.7

#### Estimated Upgrade Time: 30 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.8.*` in your `composer.json` file.

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.8 support.

### The `Application` Contract

#### The `environment` Method

**Likelihood Of Impact: Very Low**

The `environment` method signature of the `Illuminate/Contracts/Foundation/Application` contract [has changed](https://github.com/laravel/framework/pull/26296). If you are implementing this contract in your application, you should update the method signature:

    /**
     * Get or check the current application environment.
     *
     * @param  string|array  $environments
     * @return string|bool
     */
    public function environment(...$environments);

#### Added Methods

**Likelihood Of Impact: Very Low**

The `bootstrapPath`, `configPath`, `databasePath`, `environmentPath`, `resourcePath`, `storagePath`, `resolveProvider`, `bootstrapWith`, `configurationIsCached`, `detectEnvironment`, `environmentFile`, `environmentFilePath`, `getCachedConfigPath`, `getCachedRoutesPath`, `getLocale`, `getNamespace`, `getProviders`, `hasBeenBootstrapped`, `loadDeferredProviders`, `loadEnvironmentFrom`, `routesAreCached`, `setLocale`, `shouldSkipMiddleware` and `terminate`  methods [were added to the `Illuminate/Contracts/Foundation/Application` contract](https://github.com/laravel/framework/pull/26477).

In the very unlikely event you are implementing this interface, you should add these methods to your implementation.

### Cache

<a name="cache-ttl-in-seconds"></a>
#### TTL in seconds

**Likelihood Of Impact: Very High**

In order to allow a more granular expiration time when storing items, the cache item time-to-live has changed from minutes to seconds. The `put`, `putMany`, `add`, `remember` and `setDefaultCacheTime` methods of the `Illuminate\Cache\Repository` class and its extended classes, as well as the `put` method of each cache store were updated with this changed behavior. See [the related PR](https://github.com/laravel/framework/pull/27276) for more info.

If you are passing an integer to any of these methods, you should update your code to ensure you are now passing the number of seconds you wish the item to remain in the cache. Alternatively, you may pass a `DateTime` instance indicating when the item should expire:

    // Laravel 5.7 - Store item for 30 minutes...
    Cache::put('foo', 'bar', 30);

    // Laravel 5.8 - Store item for 30 seconds...
    Cache::put('foo', 'bar', 30);

    // Laravel 5.7 / 5.8 - Store item for 30 seconds...
    Cache::put('foo', 'bar', now()->addSeconds(30));

> {tip} This change makes the Laravel cache system fully compliant with the [PSR-16 caching library standard](https://www.php-fig.org/psr/psr-16/).

#### The `Repository` and `Store` Contracts

**Likelihood Of Impact: Very Low**

In order to be fully compliant with `PSR-16` the return values of the `put` and `forever` methods of the `Illuminate\Contracts\Cache\Repository` contract and the return values of the `put`, `putMany` and `forever` methods of the `Illuminate\Contracts\Cache\Store` contract [have been changed](https://github.com/laravel/framework/pull/26726) from `void` to `bool`.

<a name="psr-16-conformity"></a>
#### PSR-16 Conformity

**Likelihood Of Impact: Medium**

In addition to the return value changes from above, the TTL argument of the `put`, `putMany` and `add` method's of the `Illuminate\Cache\Repository` class was updated to conform better with the PSR-16 spec. The new behavior provides a default of `null` so a call without specifying a TTL will result in storing the cache item forever. Additionally, storing cache items with a TTL of 0 or lower will remove items from the cache. See [the related PR](https://github.com/laravel/framework/pull/27217) for more info.

The `KeyWritten` event [was also updated](https://github.com/laravel/framework/pull/27265) with these changes.

### Collections

#### The `firstWhere` Method

**Likelihood Of Impact: Very Low**

The `firstWhere` method signature [has changed](https://github.com/laravel/framework/pull/26261) to match the `where` method's signature. If you are overriding this method, you should update the method signature to match its parent:

    /**
     * Get the first item by the given key value pair.
     *
     * @param  string  $key
     * @param  mixed  $operator
     * @param  mixed  $value
     * @return mixed
     */
    public function firstWhere($key, $operator = null, $value = null);

### Config

#### `ArrayAccess` Contract Added To The `Repository` Contract

**Likelihood Of Impact: Very Low**

[The `Illuminate\Contracts\Config\Repository` contract](https://github.com/laravel/framework/pull/26747) now extends the `ArrayAccess` contract. If you are implementing the `Repository` interface, your implementation should now also satisfy the `ArrayAccess` contract.

### Console

#### The `Kernel` Contract

**Likelihood Of Impact: Very Low**

The `terminate` method [has been added to the `Illuminate/Contracts/Console/Kernel` contract](https://github.com/laravel/framework/pull/26393). If you are implementing this interface, you should add this method to your implementation.

### Container

#### `ArrayAccess` Contract Added To The `Container` Contract

**Likelihood Of Impact: Very Low**

[The `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26378) now extends the `ArrayAccess` contract. If you are implementing the `Container` interface, your implementation should now also satisfy the `ArrayAccess` contract.

#### The `resolve` Method

**Likelihood Of Impact: Very Low**

The `resolve` method [now accepts](https://github.com/laravel/framework/pull/27066) a new boolean parameter which indicates whether events (resolving callbacks) should be raised/executed during the instantiation of an object. If you are overriding this method, you should update the method signature to match its parent.

#### The `addContextualBinding` Method

**Likelihood Of Impact: Very Low**

The `addContextualBinding` method [was added to the `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26551). If you are implementing this interface, you should add this method to your implementation.

#### The `tagged` Method

**Likelihood Of Impact: Low**

The `tagged` method signature [has been changed](https://github.com/laravel/framework/pull/26953) and it now returns an `iterable` instead of an `array`. If you have type-hinted in your code some parameter which gets the return value of this method with `array`, you should modify the type-hint to `iterable`.

#### The `flush` Method

**Likelihood Of Impact: Very Low**

The `flush` method [was added to the `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26477). If you are implementing this interface, you should add this method to your implementation.

### Database

#### Unquoted MySQL JSON Values

**Likelihood Of Impact: Low**

The query builder will now return unquoted JSON values when using MySQL and MariaDB. This behavior is consistent with the other supported databases:

    $value = DB::table('users')->value('options->language');

    dump($value);

    // Laravel 5.7...
    '"en"'

    // Laravel 5.8...
    'en'

As a result, the `->>` operator is no longer supported or necessary.

<a name="sqlite"></a>
#### SQLite

**Likelihood Of Impact: Medium**

As of Laravel 5.8 the [oldest supported SQLite version](https://github.com/laravel/framework/pull/25995) is SQLite 3.7.11. If you are using an older SQLite version, you should update it (SQLite 3.8.8+ is recommended).

### Eloquent

#### Model names ending with a word with an irregular plural

**Likelihood of Impact: Medium**

As of Laravel 5.8, multi-word model names, ending in a word with an irregular plural [are now correctly pluralized](https://github.com/laravel/framework/pull/26421).

For example:
```php
// Laravel 5.7...
App\Feedback.php -> feedback (correctly pluralized)
App\UserFeedback.php -> user_feedbacks (incorrectly pluralized)

// Laravel 5.8
App\Feedback.php -> feedback (correctly pluralized)
App\UserFeedback.php -> user_feedback (correctly pluralized)
```

If you had a model that was incorrectly pluralized you will need to either add a new migration that renames the table to the new, correct form. Or you can define the old table name in your model using the `$table` property.

#### The `loadCount` Method

**Likelihood Of Impact: Low**

A `loadCount` method has been added to the base `Illuminate\Database\Eloquent\Model` class. If your application also defines a `loadCount` method, it may conflict with Eloquent's definition.

#### The `originalIsEquivalent` Method

**Likelihood Of Impact: Very Low**

The `originalIsEquivalent` method of the `Illuminate\Database\Eloquent\Concerns\HasAttributes` trait [has been changed](https://github.com/laravel/framework/pull/26391) from `protected` to `public`.

#### Automatic Soft-Deleted Casting Of `deleted_at` Property

**Likelihood Of Impact: Low**

The `deleted_at` property [will now be automatically casted](https://github.com/laravel/framework/pull/26985) to a `Carbon` instance when your Eloquent model uses the `Illuminate\Database\Eloquent\SoftDeletes` trait. You can override this behavior by writing your custom accessor for that property or by manually adding it to the `casts` attribute:

    protected $casts = ['deleted_at' => 'string'];

### Events

#### The `fire` Method

**Likelihood Of Impact: Low**

The `fire` method (which was deprecated in Laravel 5.4) of the `Illuminate/Events/Dispatcher` class [has been removed](https://github.com/laravel/framework/pull/26392).
You should use the `dispatch` method instead.

### Exception Handling

#### The `ExceptionHandler` Contract

**Likelihood Of Impact: Low**

The `shouldReport` method [has been added to the `Illuminate\Contracts\Debug\ExceptionHandler` contract](https://github.com/laravel/framework/pull/26193). If you are implementing this interface, you should add this method to your implementation.

#### The `renderHttpException` Method

**Likelihood Of Impact: Low**

The `renderHttpException` method signature of the `Illuminate\Foundation\Exceptions\Handler` class [has changed](https://github.com/laravel/framework/pull/25975). If you are overriding this method in your exception handler, you should update the method signature to match its parent:

    /**
     * Render the given HttpException.
     *
     * @param  \Symfony\Component\HttpKernel\Exception\HttpExceptionInterface  $e
     * @return \Symfony\Component\HttpFoundation\Response
     */
    protected function renderHttpException(HttpExceptionInterface $e);

### Facades

#### Facade Service Resolving

**Likelihood Of Impact: Low**

The `getFacadeAccessor` method may now [only return the string value representing the container identifier of the service](https://github.com/laravel/framework/pull/25525). Previously, this method may have returned an object instance.

### Mail

<a name="markdown-file-directory-change"></a>
### Markdown File Directory Change

**Likelihood Of Impact: High**

If you have published Laravel's Markdown mail components using the `vendor:publish` command, you should rename the `/resources/views/vendor/mail/markdown` directory to `text`.

In addition, the `markdownComponentPaths` method [has been renamed](https://github.com/laravel/framework/pull/26938) to `textComponentPaths`. If you are overriding this method, you should update the method name to match its parent.

#### Method Signature Changes In The `PendingMail` Class

**Likelihood Of Impact: Very Low**

The `send`, `sendNow`, `queue`, `later` and `fill` methods of the `Illuminate\Mail\PendingMail` class [have been changed](https://github.com/laravel/framework/pull/26790) to accept an `Illuminate\Contracts\Mail\Mailable` instance instead of `Illuminate\Mail\Mailable`. If you are overriding some of these methods, you should update their signature to match its parent.

### Queue

#### The `Job` Contract

**Likelihood Of Impact: Very Low**

The `isReleased`, `hasFailed` and `markAsFailed` methods [have been added to the `Illuminate\Contracts\Queue\Job` contract](https://github.com/laravel/framework/pull/26908). If you are implementing this interface, you should add these methods to your implementation.

### Requests

#### The `TransformsRequest` Middleware

**Likelihood Of Impact: Low**

The `transform` method of the `Illuminate\Foundation\Http\Middleware\TransformsRequest` middleware now receives the "fully-qualified" request input key when the input is an array:

    'employee' => [
        'name' => 'Taylor Otwell',
    ],

    /**
     * Transform the given value.
     *
     * @param  string  $key
     * @param  mixed  $value
     * @return mixed
     */
    protected function transform($key, $value)
    {
        dump($key); // 'employee.name' (Laravel 5.8)
        dump($key); // 'name' (Laravel 5.7)
    }

### Routing

#### The `UrlGenerator` Contract

**Likelihood Of Impact: Very Low**

The `previous` method [has been added to the `Illuminate\Contracts\Routing\UrlGenerator` contract](https://github.com/laravel/framework/pull/25616). If you are implementing this interface, you should add this method to your implementation.

#### The `cachedSchema` Property Of `Illuminate/Routing/UrlGenerator`

**Likelihood Of Impact: Very Low**

The `$cachedSchema` property name (which has been deprecated in Laravel `5.7`) of `Illuminate/Routing/UrlGenerator` [has been changed to](https://github.com/laravel/framework/pull/26728) `$cachedScheme`.

### Sessions

#### The `StartSession` Middleware

**Likelihood Of Impact: Very Low**

The session persistence logic has been [moved from the `terminate()` method to the `handle()` method](https://github.com/laravel/framework/pull/26410). If you are overriding one or both of these methods, you should update them to reflect these changes.

### Support

<a name="string-and-array-helpers"></a>
#### Prefer String And Array Classes Over Helpers

**Likelihood Of Impact: Medium**

All `array_*` and `str_*` global helpers [have been deprecated](https://github.com/laravel/framework/pull/26898) and will be moved to an optional package in the future. You should use the `Illuminate\Support\Arr` and `Illuminate\Support\Str` methods directly.

This impact of this change has been marked as `medium` since a future, opt-in package would prevent any breaking changes.

<a name="deferred-service-providers"></a>
#### Deferred Service Providers

**Likelihood Of Impact: Medium**

The `defer` boolean property on the service provider which is/was used to indicate if a provider is deferred [has been deprecated](https://github.com/laravel/framework/pull/27067). In order to mark the service provider as deferred it should implement the `Illuminate\Contracts\Support\DeferrableProvider` contract.

### Validation

#### The `Validator` Contract

**Likelihood Of Impact: Very Low**

The `validated` method [was added to the `Illuminate\Contracts\Validation\Validator` contract](https://github.com/laravel/framework/pull/26419):

    /**
     * Get the attributes and values that were validated.
     *
     * @return array
     */
    public function validated();

If you are implementing this interface, you should add this method to your implementation.

#### The `ValidatesAttributes` Trait

**Likelihood Of Impact: Very Low**

The `parseTable`, `getQueryColumn` and `requireParameterCount` methods of the `Illuminate\Validation\Concerns\ValidatesAttributes` trait have been changed from `protected` to `public`.

#### The `DatabasePresenceVerifier` Class

**Likelihood Of Impact: Very Low**

The `table` method of the `Illuminate\Validation\DatabasePresenceVerifier` class has been changed from `protected` to `public`.

#### The `Validator` Class

**Likelihood Of Impact: Very Low**

The `getPresenceVerifierFor` method of the `Illuminate\Validation\Validator` class [has been changed](https://github.com/laravel/framework/pull/26717) from `protected` to `public`.

#### Email Validation

**Likelihood Of Impact: Very Low**

The email validation rule now checks if the email is [RFC5630](https://tools.ietf.org/html/rfc6530) compliant, making the validation logic consistent with the logic used by SwiftMailer. In Laravel `5.7`, the `email` rule only verified that the email was [RFC822](https://tools.ietf.org/html/rfc822) compliant.

Therefore, when using Laravel 5.8, emails that were previously incorrectly considered invalid will now be considered valid (e.g `hej@bär.se`).  Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/26503).

### View

#### The `getData` Method

**Likelihood Of Impact: Very Low**

The `getData` method [was added to the `Illuminate\Contracts\View\View` contract](https://github.com/laravel/framework/pull/26754). If you are implementing this interface, you should add this method to your implementation.

### Notifications

<a name="nexmo-slack-notification-channels"></a>
#### Nexmo / Slack Notification Channels

**Likelihood Of Impact: High**

The Nexmo and Slack Notification channels have been extracted into first-party packages. To use these channels in your application, require the following packages:

    composer require laravel/nexmo-notification-channel
    composer require laravel/slack-notification-channel

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.7...master) and choose which updates are important to you.
