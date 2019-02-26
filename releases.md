# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.8](#laravel-5.8)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel's versioning scheme maintains the following convention: `paradigm.major.minor`. Major framework releases are released every six months (February and August), while minor releases may be released as often as every week. Minor releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `5.7.*`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

Paradigm shifting releases are separated by many years and represent fundamental shifts in the framework's architecture and conventions. Currently, there is no paradigm shifting release under development.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.5, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

| Version | Release | Bug Fixes Until | Security Fixes Until |
| --- | --- | --- | --- |
| 5.0 | February 4th, 2015 | August 4th, 2015 | February 4th, 2016 |
| 5.1 (LTS) | June 9th, 2015 | June 9th, 2017 | June 9th, 2018 |
| 5.2 | December 21st, 2015 | June 21st, 2016 | December 21st, 2016 |
| 5.3 | August 23rd, 2016 | February 23rd, 2017 | August 23rd, 2017 |
| 5.4 | January 24th, 2017 | July 24th, 2017 | January 24th, 2018 |
| 5.5 (LTS) | August 30th, 2017 | August 30th, 2019 | August 30th, 2020 |
| 5.6 | February 7th, 2018 | August 7th, 2018 | February 7th, 2019 |
| 5.7 | September 4th, 2018 | March 4th, 2019 | September 4th, 2019 |
| 5.8 | February 26th, 2019 | August 26th, 2019 | February 26th, 2020 |

<a name="laravel-5.8"></a>
## Laravel 5.8

Laravel 5.8 continues the improvements made in Laravel 5.7 by introducing has-one-through Eloquent relationships, improved email validation, convention based automatic registration of authorization policies, DynamoDB cache and session drivers, improved scheduler timezone configuration, support for assigning multiple authentication guards to broadcast channels, PSR-16 cache driver compliance, improvements to the `artisan serve` command, PHPUnit 8.0 support, Carbon 2.0 support, Pheanstalk 4.0 support, and a variety of other bug fixes and usability improvements.

### Eloquent `HasOneThrough` Relationship

Eloquent now provides support for the `hasOneThrough` relationship type. For example, imagine a Supplier model `hasOne` Account model, and an Account model has one AccountHistory model. You may use a `hasOneThrough` relationship to access a supplier's account history through the account model:

    /**
     * Get the account history for the supplier.
     */
    public function accountHistory()
    {
        return $this->hasOneThrough(AccountHistory::class, Account::class);
    }

### Auto-Discovery Of Model Policies

When using Laravel 5.7, each model's corresponding [authorization policy](/docs/{{version}}/authorization#creating-policies) needed to be explicitly registered in your application's `AuthServiceProvider`:

    /**
     * The policy mappings for the application.
     *
     * @var array
     */
    protected $policies = [
        'App\User' => 'App\Policies\UserPolicy',
    ];

Laravel 5.8 introduces auto-discovery of model policies as long as the model and policy follow standard Laravel naming conventions. Specifically, the policies must be in a `Policies` directory below the directory that contains the models. So, for example, the models may be placed in the `app` directory while the policies may be placed in the `app/Policies` directory. In addition, the policy name must match the model name and have a `Policy` suffix. So, a `User` model would correspond to a `UserPolicy` class.

If you would like to provide your own policy discovery logic, you may register a custom callback using the `Gate::guessPolicyNamesUsing` method. Typically, this method should be called from your application's `AuthServiceProvider`:

    use Illuminate\Support\Facades\Gate;

    Gate::guessPolicyNamesUsing(function ($modelClass) {
        // return policy class name...
    });

> {note} Any policies that are explicitly mapped in your `AuthServiceProvider` will take precedence over any potential auto-discovered policies.

### PSR-16 Cache Compliance

In order to allow a more granular expiration time when storing items and provide compliance with the PSR-16 caching standard, the cache item time-to-live has changed from minutes to seconds. The `put`, `putMany`, `add`, `remember` and `setDefaultCacheTime` methods of the `Illuminate\Cache\Repository` class and its extended classes, as well as the `put` method of each cache store were updated with this changed behavior. See [the related PR](https://github.com/laravel/framework/pull/27276) for more info.

If you are passing an integer to any of these methods, you should update your code to ensure you are now passing the number of seconds you wish the item to remain in the cache. Alternatively, you may pass a `DateTime` instance indicating when the item should expire:

    // Laravel 5.7 - Store item for 30 minutes...
    Cache::put('foo', 'bar', 30);

    // Laravel 5.8 - Store item for 30 seconds...
    Cache::put('foo', 'bar', 30);

    // Laravel 5.7 / 5.8 - Store item for 30 seconds...
    Cache::put('foo', 'bar', now()->addSeconds(30));

### Multiple Broadcast Authentication Guards

In previous releases of Laravel, private and presence broadcast channels authenticated the user via your application's default authentication guard. Beginning in Laravel 5.8, you may now assign multiple guards that should authenticate the incoming request:

    Broadcast::channel('channel', function() {
        // ...
    }, ['guards' => ['web', 'admin']])

### Token Guard Token Hashing

Laravel's `token` guard, which provides basic API authentication, now supports storing API tokens as SHA-256 hashes. This provides improved security over storing plain-text tokens. To learn more about hashed tokens, please review the full [API authentication documentation](/docs/{{version}}/api-authentication).

> **Note:** While Laravel ships with a simple, token based authentication guard, we strongly recommend you consider using [Laravel Passport](/docs/{{version}}/passport) for robust, production applications that offer API authentication.

### Improved Email Validation

Laravel 5.8 introduces improvements to the validator's underlying email validation logic by adopting the `egulias/email-validator` package utilized by SwiftMailer. Laravel's previous email validation logic occasionally considered valid emails, such as `example@bär.se`, to be invalid.

### Default Scheduler Timezone

Laravel allows you to customize the timezone of a scheduled task using the `timezone` method:

    $schedule->command('inspire')
             ->hourly()
             ->timezone('America/Chicago');

However, this can become cumbersome and repetitive if you are specifying the same timezone for all of your scheduled tasks. For that reason, you may now define a `scheduleTimezone` method in your `app/Console/Kernel.php` file. This method should return the default timezone that should be assigned to all scheduled tasks:

    /**
     * Get the timezone that should be used by default for scheduled events.
     *
     * @return \DateTimeZone|string|null
     */
    protected function scheduleTimezone()
    {
        return 'America/Chicago';
    }

### Intermediate Table / Pivot Model Events

In previous versions of Laravel, Eloquent model events were not dispatched when attaching, detaching, or syncing custom intermediate table / "pivot" models of a many-to-many relationship. When using [custom intermediate table models](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models) in Laravel 5.8, these events will now be dispatched.

### Artisan Call Improvements

Laravel allows you to invoke Artisan via the `Artisan::call` method. In previous releases of Laravel, the command's options are passed via an array as the second argument to the method:

    use Illuminate\Support\Facades\Artisan;

    Artisan::call('migrate:install', ['database' => 'foo']);

However, Laravel 5.8 allows you to pass the entire command, including options, as the first string argument to the method:

    Artisan::call('migrate:install --database=foo');

### Mock / Spy Testing Helper Methods

In order to make mocking objects more convenient, new `mock` and `spy` methods have been added to the base Laravel test case class. These methods automatically bind the mocked class into the container. For example:

    // Laravel 5.7
    $this->instance(Service::class, Mockery::mock(Service::class, function ($mock) {
        $mock->shouldReceive('process')->once();
    }));

    // Laravel 5.8
    $this->mock(Service::class, function ($mock) {
        $mock->shouldReceive('process')->once();
    });

### Eloquent Resource Key Preservation

When returning an [Eloquent resource collection](/docs/{{version}}/eloquent-resources) from a route, Laravel resets the collection's keys so that they are in simple numerical order:

    use App\User;
    use App\Http\Resources\User as UserResource;

    Route::get('/user', function () {
        return UserResource::collection(User::all());
    });

When using Laravel 5.8, you may now add a `preserveKeys` property to your resource class indicating if collection keys should be preserved. By default, and to maintain consistency with previous Laravel releases, the keys will be reset by default:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\JsonResource;

    class User extends JsonResource
    {
        /**
         * Indicates if the resource's collection keys should be preserved.
         *
         * @var bool
         */
        public $preserveKeys = true;
    }

When the `preserveKeys` property is set to `true`, collection keys will be preserved:

    use App\User;
    use App\Http\Resources\User as UserResource;

    Route::get('/user', function () {
        return UserResource::collection(User::all()->keyBy->id);
    });

### Higher Order `orWhere` Eloquent Method

In previous releases of Laravel, combining multiple Eloquent model scopes via an `or` query operator required the use of Closure callbacks:

    // scopePopular and scopeActive methods defined on the User model...
    $users = App\User::popular()->orWhere(function (Builder $query) {
        $query->active();
    })->get();

Laravel 5.8 introduces a "higher order" `orWhere` method that allows you to fluently chain these scopes together without the use of Closures:

    $users = App\User::popular()->orWhere->active()->get();

### Artisan Serve Improvements

In previous releases of Laravel, Artisan's `serve` command would serve your application on port `8000`. If another `serve` command process was already listening on this port, an attempt to serve a second application via `serve` would fail. Beginning in Laravel 5.8, `serve` will now scan for available ports up to port `8009`, allowing you to serve multiple applications at once.

### Blade File Mapping

When compiling Blade templates, Laravel now adds a comment to the top of the compiled file which contains the path to the original Blade template.

### DynamoDB Cache / Session Drivers

Laravel 5.8 introduces [DynamoDB](https://aws.amazon.com/dynamodb/) cache and session drivers. DynamoDB is a serverless NoSQL database provided by Amazon Web Services. The default configuration for the `dynamodb` cache driver can be found in the Laravel 5.8 [cache configuration file](https://github.com/laravel/laravel/blob/master/config/cache.php).

### Carbon 2.0 Support

Laravel 5.8 provides support for the `~2.0` release of the Carbon date manipulation library.

### Pheanstalk 4.0 Support

Laravel 5.8 provides support for the `~4.0` release of the Pheanstalk queue library. If you are using Pheanstalk library in your application, please upgrade your library to the `~4.0` release via Composer.
