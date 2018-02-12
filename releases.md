# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.6](#laravel-5.6)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel's versioning scheme maintains the following convention: `paradigm.major.minor`. Major framework releases are released every six months (February and August), while minor releases may be released as often as every week. Minor releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `5.5.*`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

Paradigm shifting releases are separated by many years and represent fundamental shifts in the framework's architecture and conventions. Currently, there is no paradigm shifting release under development.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.5, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

<a name="laravel-5.6"></a>
## Laravel 5.6

Laravel 5.6 continues the improvements made in Laravel 5.5 by adding an improved logging system, single-server task scheduling, improvements to model serialization, dynamic rate limiting, broadcast channel classes, API resource controller generation, Eloquent date formatting improvements, Blade component aliases, Argon2 password hashing support, inclusion of the Collision package, and more. In addition, all front-end scaffolding has been upgraded to Bootstrap 4.

All underlying Symfony components used by Laravel have been upgraded to the Symfony `~4.0` release series.

The release of Laravel 5.6 coincides with the release of [Spark 6.0](https://spark.laravel.com), the first major upgrade to Laravel Spark since its release. Spark 6.0 introduces per-seat pricing for Stripe and Braintree, localization, Bootstrap 4, an enhanced UI, and Stripe Elements support.

> {tip} This documentation summarizes the most notable improvements to the framework; however, more thorough change logs are always available [on GitHub](https://github.com/laravel/framework/blob/5.6/CHANGELOG-5.6.md).

### Logging Improvements

Laravel 5.6 brings vast improvements to Laravel's logging system. All logging configuration is housed in the new `config/logging.php` configuration file. You may now easily build logging "stacks" that send log messages to multiple handlers. For example, you may send all `debug` level messages to the system log while sending `error` level messages to Slack so that your team can quickly react to errors:

    'channels' => [
        'stack' => [
            'driver' => 'stack',
            'channels' => ['syslog', 'slack'],
        ],
    ],

In addition, it is now easier to customize existing log channels using the logging system's new "tap" functionality. For more information, check out the [full documentation on logging](/docs/{{version}}/logging).

### Single Server Task Scheduling

> {note} To utilize this feature, your application must be using the `memcached` or `redis` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

If your application is running on multiple servers, you may now limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good!

To indicate that the task should run on only one server, you may use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task on the same Cron cycle:

    $schedule->command('report:generate')
             ->fridays()
             ->at('17:00')
             ->onOneServer();

### Dynamic Rate Limiting

When specifying a [rate limit](/docs/{{version}}/routing#rate-limiting) on a group of routes in previous releases of Laravel, you were forced to provide a hard-coded number of maximum requests:

    Route::middleware('auth:api', 'throttle:60,1')->group(function () {
        Route::get('/user', function () {
            //
        });
    });

In Laravel 5.6, you may specify a dynamic request maximum based on an attribute of the authenticated `User` model. For example, if your `User` model contains a `rate_limit` attribute, you may pass the name of the attribute to the `throttle` middleware so that it is used to calculate the maximum request count:

    Route::middleware('auth:api', 'throttle:rate_limit,1')->group(function () {
        Route::get('/user', function () {
            //
        });
    });

### Broadcast Channel Classes

If your application is consuming many different channels, your `routes/channels.php` file could become bulky. So, instead of using Closures to authorize channels, you may now use channel classes. To generate a channel class, use the `make:channel` Artisan command. This command will place a new channel class in the `App/Broadcasting` directory.

    php artisan make:channel OrderChannel

Next, register your channel in your `routes/channels.php` file:

    use App\Broadcasting\OrderChannel;

    Broadcast::channel('order.{order}', OrderChannel::class);

Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization Closure. Of course, you may also take advantage of channel model binding:

    <?php

    namespace App\Broadcasting;

    use App\User;
    use App\Order;

    class OrderChannel
    {
        /**
         * Create a new channel instance.
         *
         * @return void
         */
        public function __construct()
        {
            //
        }

        /**
         * Authenticate the user's access to the channel.
         *
         * @param  \App\User  $user
         * @param  \App\Order  $order
         * @return array|bool
         */
        public function join(User $user, Order $order)
        {
            return $user->id === $order->user_id;
        }
    }

### API Controller Generation

When declaring resource routes that will be consumed by APIs, you will commonly want to exclude routes that present HTML templates such as `create` and `edit`. To generate a resource controller that does not include these methods, you may now use the `--api` switch when executing the `make:controller` command:

    php artisan make:controller API/PhotoController --api

### Model Serialization Improvements

In previous releases of Laravel, queued models would not be restored with their loaded relationships intact. In Laravel 5.6, relationships that were loaded on the model when it was queued are automatically re-loaded when the job is processed by the queue.

### Eloquent Date Casting

You may now individually customize the format of Eloquent date cast columns. To get started, specify the desired date format within the cast declaration. Once specified, this format will be used when serializing the model to an array / JSON:

    protected $casts = [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];

### Blade Component Aliases

If your Blade components are stored in a sub-directory, you may now alias them for easier access. For example, imagine a Blade component that is stored at `resources/views/components/alert.blade.php`. You may use the `component` method to alias the component from `components.alert` to `alert`:

    Blade::component('components.alert', 'alert');

Once the component has been aliased, you may render it using a directive:

    @alert('alert', ['type' => 'danger'])
        You are not allowed to access this resource!
    @endalert

You may omit the component parameters if it has no additional slots:

    @alert
        You are not allowed to access this resource!
    @endalert

### Argon2 Password Hashing

If you are building an application on PHP 7.2.0 or greater, Laravel now supports password hashing via the Argon2 algorithm. The default hash driver for your application is controlled by a new `config/hashing.php` configuration file.

### UUID Methods

Laravel 5.6 introduces two new methods for generating UUIDs: `Str::uuid` and `Str::orderedUuid`. The `orderedUuid` method will generate a timestamp first UUID that is more easily and efficiently indexed by databases such as MySQL. Each of these methods returns a `Ramsey\Uuid\Uuid` object:

    use Illuminate\Support\Str;

    return (string) Str::uuid();

    return (string) Str::orderedUuid();

### Collision

The default `laravel/laravel` application now contains a `dev` Composer dependency for the [Collision](https://github.com/nunomaduro/collision) package maintained by Nuno Maduro. This packages provides beautiful error reporting when interacting with your Laravel application on the command line:

<img src="https://raw.githubusercontent.com/nunomaduro/collision/stable/docs/example.png" width="600" height="388">

### Bootstrap 4

All front-end scaffolding such as the authentication boilerplate and example Vue component have been upgraded to [Bootstrap 4](https://blog.getbootstrap.com/2018/01/18/bootstrap-4/). By default, pagination link generation also now defaults to Bootstrap 4.
