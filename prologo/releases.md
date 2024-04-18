# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 11](#laravel-11)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^11.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

<a name="named-arguments"></a>
#### Named Arguments

[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future.

<a name="support-policy"></a>
## Support Policy

For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/{{version}}/database#introduction).


<div class="overflow-auto">

| Version | PHP (*) | Release | Bug Fixes Until | Security Fixes Until |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | February 8th, 2022 | August 8th, 2023 | February 6th, 2024 |
| 10 | 8.1 - 8.3 | February 14th, 2023 | August 6th, 2024 | February 4th, 2025 |
| 11 | 8.2 - 8.3 | March 12th, 2024 | September 3rd, 2025 | March 12th, 2026 |
| 12 | 8.2 - 8.3 | Q1 2025 | Q3, 2026 | Q1, 2027 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) Supported PHP versions

<a name="laravel-11"></a>
## Laravel 11

Laravel 11 continues the improvements made in Laravel 10.x by introducing a streamlined application structure, per-second rate limiting, health routing, graceful encryption key rotation, queue testing improvements, [Resend](https://resend.com) mail transport, Prompt validator integration, new Artisan commands, and more. In addition, Laravel Reverb, a first-party, scalable WebSocket server has been introduced to provide robust real-time capabilities to your applications.

<a name="php-8"></a>
### PHP 8.2

Laravel 11.x requires a minimum PHP version of 8.2.

<a name="structure"></a>
### Streamlined Application Structure

_Laravel's streamlined application structure was developed by [Taylor Otwell](https://github.com/taylorotwell) and [Nuno Maduro](https://github.com/nunomaduro)_.

Laravel 11 introduces a streamlined application structure for **new** Laravel applications, without requiring any changes to existing applications. The new application structure is intended to provide a leaner, more modern experience, while retaining many of the concepts that Laravel developers are already familiar with. Below we will discuss the highlights of Laravel's new application structure.

#### The Application Bootstrap File

The `bootstrap/app.php` file has been revitalized as a code-first application configuration file. From this file, you may now customize your application's routing, middleware, service providers, exception handling, and more. This file unifies a variety of high-level application behavior settings that were previously scattered throughout your application's file structure:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

<a name="service-providers"></a>
#### Service Providers

Instead of the default Laravel application structure containing five service providers, Laravel 11 only includes a single `AppServiceProvider`. The functionality of the previous service providers has been incorporated into the `bootstrap/app.php`, is handled automatically by the framework, or may be placed in your application's `AppServiceProvider`.

For example, event discovery is now enabled by default, largely eliminating the need for manual registration of events and their listeners. However, if you do need to manually register events, you may simply do so in the `AppServiceProvider`. Similarly, route model bindings or authorization gates you may have previously registered in the `AuthServiceProvider` may also be registered in the `AppServiceProvider`.

<a name="opt-in-routing"></a>
#### Opt-in API and Broadcast Routing

The `api.php` and `channels.php` route files are no longer present by default, as many applications do not require these files. Instead, they may be created using simple Artisan commands:

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
#### Middleware

Previously, new Laravel applications included nine middleware. These middleware performed a variety of tasks such as authenticating requests, trimming input strings, and validating CSRF tokens.

In Laravel 11, these middleware have been moved into the framework itself, so that they do not add bulk to your application's structure. New methods for customizing the behavior of these middleware have been added to the framework and may be invoked from your application's `bootstrap/app.php` file:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(
        except: ['stripe/*']
    );

    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ])
})
```

Since all middleware can be easily customized via your application's `bootstrap/app.php`, the need for a separate HTTP "kernel" class has been eliminated.

<a name="scheduling"></a>
#### Scheduling

Using a new `Schedule` facade, scheduled tasks may now be defined directly in your application's `routes/console.php` file, eliminating the need for a separate console "kernel" class:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
#### Exception Handling

Like routing and middleware, exception handling can now be customized from your application's `bootstrap/app.php` file instead of a separate exception handler class, reducing the overall number of files included in a new Laravel application:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport(MissedFlightException::class);

    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<a name="base-controller-class"></a>
#### Base `Controller` Class

The base controller included in new Laravel applications has been simplified. It no longer extends Laravel's internal `Controller` class, and the `AuthorizesRequests` and `ValidatesRequests` traits have been removed, as they may be included in your application's individual controllers if desired:

    <?php

    namespace App\Http\Controllers;

    abstract class Controller
    {
        //
    }

<a name="application-defaults"></a>
#### Application Defaults

By default, new Laravel applications use SQLite for database storage, as well as the `database` driver for Laravel's session, cache, and queue. This allows you to begin building your application immediately after creating a new Laravel application, without being required to install additional software or create additional database migrations.

In addition, over time, the `database` drivers for these Laravel services have become robust enough for production usage in many application contexts; therefore, they provide a sensible, unified choice for both local and production applications.

<a name="reverb"></a>
### Laravel Reverb

_Laravel Reverb was developed by [Joe Dixon](https://github.com/joedixon)_.

[Laravel Reverb](https://reverb.laravel.com) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel’s existing suite of event broadcasting tools, such as Laravel Echo.

```shell
php artisan reverb:start
```

In addition, Reverb supports horizontal scaling via Redis's publish / subscribe capabilities, allowing you to distribute your WebSocket traffic across multiple backend Reverb servers all supporting a single, high-demand application.

For more information on Laravel Reverb, please consult the complete [Reverb documentation](/docs/{{version}}/reverb).

<a name="rate-limiting"></a>
### Per-Second Rate Limiting

_Per-second rate limiting was contributed by [Tim MacDonald](https://github.com/timacdonald)_.

Laravel now supports "per-second" rate limiting for all rate limiters, including those for HTTP requests and queued jobs. Previously, Laravel's rate limiters were limited to "per-minute" granularity:

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

For more information on rate limiting in Laravel, check out the [rate limiting documentation](/docs/{{version}}/routing#rate-limiting).

<a name="health"></a>
### Health Routing

_Health routing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

New Laravel 11 applications include a `health` routing directive, which instructs Laravel to define a simple health-check endpoint that may be invoked by third-party application health monitoring services or orchestration systems like Kubernetes. By default, this route is served at `/up`:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

When HTTP requests are made to this route, Laravel will also dispatch a `DiagnosingHealth` event, allowing you to perform additional health checks that are relevant to your application.

<a name="encryption"></a>
### Graceful Encryption Key Rotation

_Graceful encryption key rotation was contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Since Laravel encrypts all cookies, including your application's session cookie, essentially every request to a Laravel application relies on encryption. However, because of this, rotating your application's encryption key would log all users out of your application. In addition, decrypting data that was encrypted by the previous encryption key becomes impossible.

Laravel 11 allows you to define your application's previous encryption keys as a comma-delimited list via the `APP_PREVIOUS_KEYS` environment variable.

When encrypting values, Laravel will always use the "current" encryption key, which is within the `APP_KEY` environment variable. When decrypting values, Laravel will first try the current key. If decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value.

This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated.

For more information on encryption in Laravel, check out the [encryption documentation](/docs/{{version}}/encryption).

<a name="automatic-password-rehashing"></a>
### Automatic Password Rehashing

_Automatic password rehashing was contributed by [Stephen Rees-Carter](https://github.com/valorin)_.

Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via the `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable.

Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will now gracefully and automatically rehash user passwords as users authenticate with your application.

<a name="prompt-validation"></a>
### Prompt Validation

_Prompt validator integration was contributed by [Andrea Marco Sartori](https://github.com/cerbero90)_.

[Laravel Prompts](/docs/{{version}}/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation.

Laravel Prompts supports input validation via closures:

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

However, this can become cumbersome when dealing with many inputs or complicated validation scenarios. Therefore, in Laravel 11, you may utilize the full power of Laravel's [validator](/docs/{{version}}/validation) when validating prompt inputs:

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
### Queue Interaction Testing

_Queue interaction testing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Previously, attempting to test that a queued job was released, deleted, or manually failed was cumbersome and required the definition of custom queue fakes and stubs. However, in Laravel 11, you may easily test for these queue interactions using the `withFakeQueueInteractions` method:

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

For more information on testing queued jobs, check out the [queue documentation](/docs/{{version}}/queues#testing).

<a name="new-artisan-commands"></a>
### New Artisan Commands

_Class creation Artisan commands were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

New Artisan commands have been added to allow the quick creation of classes, enums, interfaces, and traits:

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
### Model Casts Improvements

_Model casts improvements were contributed by [Nuno Maduro](https://github.com/nunomaduro)_.

Laravel 11 supports defining your model's casts using a method instead of a property. This allows for streamlined, fluent cast definitions, especially when using casts with arguments:

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsCollection::using(OptionCollection::class),
                      // AsEncryptedCollection::using(OptionCollection::class),
                      // AsEnumArrayObject::using(OptionEnum::class),
                      // AsEnumCollection::using(OptionEnum::class),
        ];
    }

For more information on attribute casting, review the [Eloquent documentation](/docs/{{version}}/eloquent-mutators#attribute-casting).

<a name="the-once-function"></a>
### The `once` Function

_The `once` helper was contributed by [Taylor Otwell](https://github.com/taylorotwell)_ and _[Nuno Maduro](https://github.com/nunomaduro)_.

The `once` helper function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result:

    function random(): int
    {
        return once(function () {
            return random_int(1, 1000);
        });
    }

    random(); // 123
    random(); // 123 (cached result)
    random(); // 123 (cached result)

For more information on the `once` helper, check out the [helpers documentation](/docs/{{version}}/helpers#method-once).

<a name="database-performance"></a>
### Improved Performance When Testing With In-Memory Databases

_Improved in-memory database testing performance was contributed by [Anders Jenbo](https://github.com/AJenbo)_

Laravel 11 offers a significant speed boost when using the `:memory:` SQLite database during testing. To accomplish this, Laravel now maintains a reference to PHP's PDO object and reuses it across connections, often cutting total test run time in half.

<a name="mariadb"></a>
### Improved Support for MariaDB

_Improved support for MariaDB was contributed by [Jonas Staudenmeir](https://github.com/staudenmeir) and [Julius Kiekbusch](https://github.com/Jubeki)_

Laravel 11 includes improved support for MariaDB. In previous Laravel releases, you could use MariaDB via Laravel's MySQL driver. However, Laravel 11 now includes a dedicated MariaDB driver which provides better defaults for this database system.

For more information on Laravel's database drivers, check out the [database documentation](/docs/{{version}}/database).

<a name="inspecting-database"></a>
### Inspecting Databases and Improved Schema Operations

_Improved schema operations and database inspection was contributed by [Hafez Divandari](https://github.com/hafezdivandari)_

Laravel 11 provides additional database schema operation and inspection methods, including the native modifying, renaming, and dropping of columns. Furthermore, advanced spatial types, non-default schema names, and native schema methods for manipulating tables, views, columns, indexes, and foreign keys are provided:

    use Illuminate\Support\Facades\Schema;

    $tables = Schema::getTables();
    $views = Schema::getViews();
    $columns = Schema::getColumns('users');
    $indexes = Schema::getIndexes('users');
    $foreignKeys = Schema::getForeignKeys('users');
