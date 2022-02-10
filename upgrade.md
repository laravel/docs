# Upgrade Guide

- [Upgrading To 5.8.0 From 5.7](#upgrade-5.8.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Cache TTL In Seconds](#cache-ttl-in-seconds)
- [Cache Lock Safety Improvements](#cache-lock-safety-improvements)
- [Environment Variable Parsing](#environment-variable-parsing)
- [Markdown File Directory Change](#markdown-file-directory-change)
- [Nexmo / Slack Notification Channels](#nexmo-slack-notification-channels)
- [New Default Password Length](#new-default-password-length)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Container Generators & Tagged Services](#container-generators)
- [SQLite Version Constraints](#sqlite)
- [Prefer String And Array Classes Over Helpers](#string-and-array-helpers)
- [Deferred Service Providers](#deferred-service-providers)
- [PSR-16 Conformity](#psr-16-conformity)
- [Model Names Ending With Irregular Plurals](#model-names-ending-with-irregular-plurals)
- [Custom Pivot Models With Incrementing IDs](#custom-pivot-models-with-incrementing-ids)
- [Pheanstalk 4.0](#pheanstalk-4)
- [Carbon 2.0](#carbon-2.0)
</div>

<a name="upgrade-5.8.0"></a>
## Upgrading To 5.8.0 From 5.7

#### Estimated Upgrade Time: 1 Hour

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update your `laravel/framework` dependency to `5.8.*` in your `composer.json` file.

Next, examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.8 support.

<a name="the-application-contract"></a>
### The `Application` Contract

#### The `environment` Method

**Likelihood Of Impact: Very Low**

The `environment` method signature of the `Illuminate\Contracts\Foundation\Application` contract [has changed](https://github.com/laravel/framework/pull/26296). If you are implementing this contract in your application, you should update the method signature:

    /**
     * Get or check the current application environment.
     *
     * @param  string|array  $environments
     * @return string|bool
     */
    public function environment(...$environments);

#### Added Methods

**Likelihood Of Impact: Very Low**

The `bootstrapPath`, `configPath`, `databasePath`, `environmentPath`, `resourcePath`, `storagePath`, `resolveProvider`, `bootstrapWith`, `configurationIsCached`, `detectEnvironment`, `environmentFile`, `environmentFilePath`, `getCachedConfigPath`, `getCachedRoutesPath`, `getLocale`, `getNamespace`, `getProviders`, `hasBeenBootstrapped`, `loadDeferredProviders`, `loadEnvironmentFrom`, `routesAreCached`, `setLocale`, `shouldSkipMiddleware` and `terminate`  methods [were added to the `Illuminate\Contracts\Foundation\Application` contract](https://github.com/laravel/framework/pull/26477).

In the very unlikely event you are implementing this interface, you should add these methods to your implementation.

<a name="authentication"></a>
### Authentication

#### Password Reset Notification Route Parameter

**Likelihood Of Impact: Low**

When a user requests a link to reset their password, Laravel generates the URL using the `route` helper to create a URL to the `password.reset` named route. When using Laravel 5.7, the token is passed to the `route` helper without an explicit name, like so:

    route('password.reset', $token);

When using Laravel 5.8, the token is passed to the `route` helper as an explicit parameter:

    route('password.reset', ['token' => $token]);

Therefore, if you are defining your own `password.reset` route, you should ensure that it contains a `{token}` parameter in its URI.

<a name="new-default-password-length"></a>
#### New Default Password Length

**Likelihood Of Impact: High**

The required password length when choosing or resetting a password was [changed to eight characters](https://github.com/laravel/framework/pull/25957). You should update any validation rules or logic within your application to match this new eight character default.

If you need to preserve the previous six character length or a different length, you may extend the `Illuminate\Auth\Passwords\PasswordBroker` class and overwrite the `validatePasswordWithDefaults` method with custom logic.

<a name="cache"></a>
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

<a name="psr-16-conformity"></a>
#### PSR-16 Conformity

**Likelihood Of Impact: Medium**

In addition to [the return value changes from below](#the-repository-and-store-contracts), the TTL argument of the `put`, `putMany` and `add` method's of the `Illuminate\Cache\Repository` class was updated to conform better with the PSR-16 spec. The new behavior provides a default of `null` so a call without specifying a TTL will result in storing the cache item forever. Additionally, storing cache items with a TTL of 0 or lower will remove items from the cache. See [the related PR](https://github.com/laravel/framework/pull/27217) for more info.

The `KeyWritten` event [was also updated](https://github.com/laravel/framework/pull/27265) with these changes.

<a name="cache-lock-safety-improvements"></a>
#### Lock Safety Improvements

**Likelihood Of Impact: High**

In Laravel 5.7 and prior versions of Laravel, the "atomic lock" feature provided by some cache drivers could have unexpected behavior leading to the early release of locks.

For example: **Client A** acquires lock `foo` with a 10 second expiration. **Client A** actually takes 20 seconds to finish its task. The lock is released automatically by the cache system 10 seconds into **Client A's** processing time. **Client B** acquires lock `foo`. **Client A** finally finishes its task and releases lock `foo`, inadvertently releasing **Client B's** hold on the lock. **Client C** is now able to acquire the lock.

In order to mitigate this scenario, locks are now generated with an embedded "scope token" which allows the framework to ensure that, under normal circumstances, only the proper owner of a lock can release a lock.

If you are using the `Cache::lock()->get(Closure)` method of interacting with locks, no changes are required:

    Cache::lock('foo', 10)->get(function () {
        // Lock will be released safely automatically...
    });

However, if you are manually calling `Cache::lock()->release()`, you must update your code to maintain an instance of the lock. Then, after you are done performing your task, you may call the `release` method on **the same lock instance**. For example:

    if (($lock = Cache::lock('foo', 10))->get()) {
        // Perform task...

        $lock->release();
    }

Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token:

    // Within Controller...
    $podcast = Podcast::find(1);

    if (($lock = Cache::lock('foo', 120))->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

    // Within ProcessPodcast Job...
    Cache::restoreLock('foo', $this->owner)->release();

If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method:

    Cache::lock('foo')->forceRelease();

<a name="the-repository-and-store-contracts"></a>
#### The `Repository` and `Store` Contracts

**Likelihood Of Impact: Very Low**

In order to be fully compliant with `PSR-16` the return values of the `put` and `forever` methods of the `Illuminate\Contracts\Cache\Repository` contract and the return values of the `put`, `putMany` and `forever` methods of the `Illuminate\Contracts\Cache\Store` contract [have been changed](https://github.com/laravel/framework/pull/26726) from `void` to `bool`.

<a name="carbon-2.0"></a>
### Carbon 2.0

**Likelihood Of Impact: Medium**

Laravel now supports both Carbon 1 and Carbon 2; therefore, Composer will try to upgrade to Carbon 2.0 if no other compatibility issues with any other packages are detected. Please review the [migration guide for Carbon 2.0](https://carbon.nesbot.com/docs/#api-carbon-2).

<a name="collections"></a>
### Collections

#### The `add` Method

**Likelihood Of Impact: Very Low**

The `add` method [has been moved](https://github.com/laravel/framework/pull/27082) from the Eloquent collection class to the base collection class. If you are extending `Illuminate\Support\Collection` and your extended class has an `add` method, make sure the method signature matches its parent:

    public function add($item);

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

<a name="console"></a>
### Console

#### The `Kernel` Contract

**Likelihood Of Impact: Very Low**

The `terminate` method [has been added to the `Illuminate\Contracts\Console\Kernel` contract](https://github.com/laravel/framework/pull/26393). If you are implementing this interface, you should add this method to your implementation.

<a name="container"></a>
### Container

<a name="container-generators"></a>
#### Generators & Tagged Services

**Likelihood Of Impact: Medium**

The container's `tagged` method now utilizes PHP generators to lazy-instantiate the services with a given tag. This provides a performance improvement if you are not utilizing every tagged service.

Because of this change, the `tagged` method now returns an `iterable` instead of an `array`. If you are type-hinting the return value of this method, you should ensure that your type-hint is changed to `iterable`.

In addition, it is no longer possible to directly access a tagged service by its array offset value, such as `$container->tagged('foo')[0]`.

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

<a name="database"></a>
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

#### Migrations & `bigIncrements`

**Likelihood Of Impact: None**

[As of Laravel 5.8](https://github.com/laravel/framework/pull/26472), migration stubs use the `bigIncrements` method on ID columns by default. Previously, ID columns were created using the `increments` method.

This will not affect any existing code in your project; however, be aware that foreign key columns must be of the same type. Therefore, a column created using the `increments` method can not reference a column created using the `bigIncrements` method.

<a name="eloquent"></a>
### Eloquent

<a name="model-names-ending-with-irregular-plurals"></a>
#### Model Names Ending With Irregular Plurals

**Likelihood Of Impact: Medium**

As of Laravel 5.8, multi-word model names ending in a word with an irregular plural [are now correctly pluralized](https://github.com/laravel/framework/pull/26421).

    // Laravel 5.7...
    App\Feedback.php -> feedback (correctly pluralized)
    App\UserFeedback.php -> user_feedbacks (incorrectly pluralized)

    // Laravel 5.8
    App\Feedback.php -> feedback (correctly pluralized)
    App\UserFeedback.php -> user_feedback (correctly pluralized)

If you have a model that was incorrectly pluralized, you may continue using the old table name by defining a `$table` property on your model:

    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'user_feedbacks';

<a name="custom-pivot-models-with-incrementing-ids"></a>
#### Custom Pivot Models With Incrementing IDs

If you have defined a many-to-many relationship that uses a custom pivot model, and that pivot model has an auto-incrementing primary key, you should ensure your custom pivot model class defines an `incrementing` property that is set to `true`:

    /**
     * Indicates if the IDs are auto-incrementing.
     *
     * @var bool
     */
    public $incrementing = true;

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

#### BelongsTo `getForeignKey` & `getOwnerKey` Methods

**Likelihood Of Impact: Low**

The `getForeignKey`, `getQualifiedForeignKey`, and `getOwnerKey` methods of the `BelongsTo` relationship have been renamed to `getForeignKeyName`, `getQualifiedForeignKeyName`, and `getOwnerKeyName` respectively, making the method names consistent with the other relationships offered by Laravel.

<a name="environment-variable-parsing"></a>
### Environment Variable Parsing

**Likelihood Of Impact: High**

The [phpdotenv](https://github.com/vlucas/phpdotenv) package that is used to parse `.env` files has released a new major version, which may impact the results returned from the `env` helper. Specifically, the `#` character in an unquoted value will now be considered a comment instead of part of the value:

Previous behavior:

    ENV_VALUE=foo#bar

    env('ENV_VALUE'); // foo#bar

New behavior:

    ENV_VALUE=foo#bar
    env('ENV_VALUE'); // foo

To preserve the previous behavior, you may wrap the environment values in quotes:

    ENV_VALUE="foo#bar"

    env('ENV_VALUE'); // foo#bar

For more information, please refer to the [phpdotenv upgrade guide](https://github.com/vlucas/phpdotenv/blob/master/UPGRADING.md).

<a name="events"></a>
### Events

#### The `fire` Method

**Likelihood Of Impact: Low**

The `fire` method (which was deprecated in Laravel 5.4) of the `Illuminate\Events\Dispatcher` class [has been removed](https://github.com/laravel/framework/pull/26392).
You should use the `dispatch` method instead.

<a name="exception-handling"></a>
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

<a name="mail"></a>
### Mail

<a name="markdown-file-directory-change"></a>
<a name="markdown-file-directory-change"></a>
### Markdown File Directory Change

**Likelihood Of Impact: High**

If you have published Laravel's Markdown mail components using the `vendor:publish` command, you should rename the `/resources/views/vendor/mail/markdown` directory to `/resources/views/vendor/mail/text`.

In addition, the `markdownComponentPaths` method [has been renamed](https://github.com/laravel/framework/pull/26938) to `textComponentPaths`. If you are overriding this method, you should update the method name to match its parent.

#### Method Signature Changes In The `PendingMail` Class

**Likelihood Of Impact: Very Low**

The `send`, `sendNow`, `queue`, `later` and `fill` methods of the `Illuminate\Mail\PendingMail` class [have been changed](https://github.com/laravel/framework/pull/26790) to accept an `Illuminate\Contracts\Mail\Mailable` instance instead of `Illuminate\Mail\Mailable`. If you are overriding some of these methods, you should update their signature to match its parent.

<a name="queue"></a>
### Queue

<a name="pheanstalk-4"></a>
#### Pheanstalk 4.0

**Likelihood Of Impact: Medium**

Laravel 5.8 provides support for the `~4.0` release of the Pheanstalk queue library. If you are using Pheanstalk library in your application, please upgrade your library to the `~4.0` release via Composer.

#### The `Job` Contract

**Likelihood Of Impact: Very Low**

The `isReleased`, `hasFailed` and `markAsFailed` methods [have been added to the `Illuminate\Contracts\Queue\Job` contract](https://github.com/laravel/framework/pull/26908). If you are implementing this interface, you should add these methods to your implementation.

#### The `Job::failed` & `FailingJob` Class

**Likelihood Of Impact: Very Low**

When a queued job failed in Laravel 5.7, the queue worker executed the `FailingJob::handle` method. In Laravel 5.8, the logic contained in the `FailingJob` class has been moved to a `fail` method directly on the job class itself. Because of this, a `fail` method has been added to the `Illuminate\Contracts\Queue\Job` contract.

The base `Illuminate\Queue\Jobs\Job` class contains the implementation of `fail` and no code changes should be required by typical application code. However, if you are building custom queue driver which utilizes a job class that **does not** extend the base job class offered by Laravel, you should implement the `fail` method manually in your custom job class. You may refer to Laravel's base job class as a reference implementation.

This change allows custom queue drivers to have more control over the job deletion process.

#### Redis Blocking Pop

**Likelihood Of Impact: Very Low**

Using the "blocking pop" feature of the Redis queue driver is now safe. Previously, there was a small chance that a queued job could be lost if the Redis server or worker crashed at the same time the job was retrieved. In order to make blocking pops safe, a new Redis list with suffix `:notify` is created for each Laravel queue.

<a name="requests"></a>
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

<a name="routing"></a>
### Routing

#### The `UrlGenerator` Contract

**Likelihood Of Impact: Very Low**

The `previous` method [has been added to the `Illuminate\Contracts\Routing\UrlGenerator` contract](https://github.com/laravel/framework/pull/25616). If you are implementing this interface, you should add this method to your implementation.

#### The `cachedSchema` Property Of `Illuminate\Routing\UrlGenerator`

**Likelihood Of Impact: Very Low**

The `$cachedSchema` property name (which has been deprecated in Laravel `5.7`) of `Illuminate\Routing\UrlGenerator` [has been changed to](https://github.com/laravel/framework/pull/26728) `$cachedScheme`.

<a name="sessions"></a>
### Sessions

#### The `StartSession` Middleware

**Likelihood Of Impact: Very Low**

The session persistence logic has been [moved from the `terminate()` method to the `handle()` method](https://github.com/laravel/framework/pull/26410). If you are overriding one or both of these methods, you should update them to reflect these changes.

<a name="support"></a>
### Support

<a name="string-and-array-helpers"></a>
#### Prefer String And Array Classes Over Helpers

**Likelihood Of Impact: Medium**

All `array_*` and `str_*` global helpers [have been deprecated](https://github.com/laravel/framework/pull/26898). You should use the `Illuminate\Support\Arr` and `Illuminate\Support\Str` methods directly.

The impact of this change has been marked as `medium` since the helpers have been moved to the new [laravel/helpers](https://github.com/laravel/helpers) package which offers a backwards compatibility layer for all of the global array and string functions.

If you choose to update your Laravel application's views to use the class based methods, you should clear your compiled views which may still be using the global helpers:

    php artisan view:clear

<a name="deferred-service-providers"></a>
#### Deferred Service Providers

**Likelihood Of Impact: Medium**

The `defer` boolean property on the service provider which is/was used to indicate if a provider is deferred [has been deprecated](https://github.com/laravel/framework/pull/27067). In order to mark the service provider as deferred it should implement the `Illuminate\Contracts\Support\DeferrableProvider` contract.

#### Read-Only `env` Helper

**Likelihood Of Impact: Low**

Previously, the `env` helper could retrieve values from environment variables which were changed at runtime. In Laravel 5.8, the `env` helper treats environment variables as immutable. If you would like to change an environment variable at runtime, consider using a configuration value that can be retrieved using the `config` helper:

Previous behavior:

    dump(env('APP_ENV')); // local

    putenv('APP_ENV=staging');

    dump(env('APP_ENV')); // staging

New behavior:

    dump(env('APP_ENV')); // local

    putenv('APP_ENV=staging');

    dump(env('APP_ENV')); // local

<a name="testing"></a>
### Testing

#### The `setUp` & `tearDown` Methods

The `setUp` and `tearDown` methods now require a void return type:

    protected function setUp(): void
    protected function tearDown(): void

#### PHPUnit 8

**Likelihood Of Impact: Optional**

By default, Laravel 5.8 uses PHPUnit 7. However, you may optionally upgrade to PHPUnit 8, which requires PHP >= 7.2. In addition, please read through the entire list of changes in [the PHPUnit 8 release announcement](https://phpunit.de/announcements/phpunit-8.html).

<a name="validation"></a>
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

The email validation rule now checks if the email is [RFC6530](https://tools.ietf.org/html/rfc6530) compliant, making the validation logic consistent with the logic used by SwiftMailer. In Laravel `5.7`, the `email` rule only verified that the email was [RFC822](https://tools.ietf.org/html/rfc822) compliant.

Therefore, when using Laravel 5.8, emails that were previously incorrectly considered invalid will now be considered valid (e.g `hej@bär.se`).  Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/26503).

<a name="view"></a>
### View

#### The `getData` Method

**Likelihood Of Impact: Very Low**

The `getData` method [was added to the `Illuminate\Contracts\View\View` contract](https://github.com/laravel/framework/pull/26754). If you are implementing this interface, you should add this method to your implementation.

<a name="notifications"></a>
### Notifications

<a name="nexmo-slack-notification-channels"></a>
#### Nexmo / Slack Notification Channels

**Likelihood Of Impact: High**

The Nexmo and Slack Notification channels have been extracted into first-party packages. To use these channels in your application, require the following packages:

    composer require laravel/nexmo-notification-channel
    composer require laravel/slack-notification-channel

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.7...5.8) and choose which updates are important to you.
