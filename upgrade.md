# Upgrade Guide

- [Upgrading To 8.0 From 7.x](#upgrade-8.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- [Model Factories](#model-factories)
- [Queue `retryAfter` Method](#queue-retry-after-method)
- [Queue `timeoutAt` Property](#queue-timeout-at-property)
- [Queue `allOnQueue` and `allOnConnection`](#queue-allOnQueue-allOnConnection)
- [Pagination Defaults](#pagination-defaults)
- [Seeder & Factory Namespaces](#seeder-factory-namespaces)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [PHP 7.3.0 Required](#php-7.3.0-required)
- [Failed Jobs Table Batch Support](#failed-jobs-table-batch-support)
- [Maintenance Mode Updates](#maintenance-mode-updates)
- [The `php artisan down --message` Option](#artisan-down-message)
- [The `assertExactJson` Method](#assert-exact-json-method)
</div>

<a name="upgrade-8.0"></a>
## Upgrading To 8.0 From 7.x

<a name="estimated-upgrade-time-15-minutes"></a>
#### Estimated Upgrade Time: 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

<a name="php-7.3.0-required"></a>
### PHP 7.3.0 Required

**Likelihood Of Impact: Medium**

The new minimum PHP version is now 7.3.0.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update the following dependencies in your `composer.json` file:

<div class="content-list" markdown="1">
- `guzzlehttp/guzzle` to `^7.0.1`
- `facade/ignition` to `^2.3.6`
- `laravel/framework` to `^8.0`
- `laravel/ui` to `^3.0`
- `nunomaduro/collision` to `^5.0`
- `phpunit/phpunit` to `^9.0`
</div>

The following first-party packages have new major releases to support Laravel 8. If applicable, you should read their individual upgrade guides before upgrading:

<div class="content-list" markdown="1">
- [Horizon v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)
</div>

In addition, the Laravel installer has been updated to support `composer create-project` and Laravel Jetstream. Any installer older than 4.0 will cease to work after October 2020. You should upgrade your global installer to `^4.0` as soon as possible.

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 8 support.

<a name="collections"></a>
### Collections

<a name="the-isset-method"></a>
#### The `isset` Method

**Likelihood Of Impact: Low**

To be consistent with typical PHP behavior, the `offsetExists` method of `Illuminate\Support\Collection` has been updated to use `isset` instead of `array_key_exists`. This may present a change in behavior when dealing with collection items that have a value of `null`:

    $collection = collect([null]);

    // Laravel 7.x - true
    isset($collection[0]);

    // Laravel 8.x - false
    isset($collection[0]);

<a name="database"></a>
### Database

<a name="seeder-factory-namespaces"></a>
#### Seeder & Factory Namespaces

**Likelihood Of Impact: High**

Seeders and factories are now namespaced. To accommodate for these changes, add the `Database\Seeders` namespace to your seeder classes. In addition, the previous `database/seeds` directory should be renamed to `database/seeders`:

    <?php

    namespace Database\Seeders;

    use App\Models\User;
    use Illuminate\Database\Seeder;

    class DatabaseSeeder extends Seeder
    {
        /**
         * Seed the application's database.
         *
         * @return void
         */
        public function run()
        {
            ...
        }
    }

If you are choosing to use the `laravel/legacy-factories` package, no changes to your factory classes are required. However, if you are upgrading your factories, you should add the `Database\Factories` namespace to those classes.

Next, in your `composer.json` file, remove `classmap` block from the `autoload` section and add the new namespaced class directory mappings:

    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\Factories\\": "database/factories/",
            "Database\\Seeders\\": "database/seeders/"
        }
    },

<a name="eloquent"></a>
### Eloquent

<a name="model-factories"></a>
#### Model Factories

**Likelihood Of Impact: High**

Laravel's [model factories](/docs/{{version}}/database-testing#defining-model-factories) feature has been totally rewritten to support classes and is not compatible with Laravel 7.x style factories. However, to ease the upgrade process, a new `laravel/legacy-factories` package has been created to continue using your existing factories with Laravel 8.x. You may install this package via Composer:

    composer require laravel/legacy-factories

<a name="the-castable-interface"></a>
#### The `Castable` Interface

**Likelihood Of Impact: Low**

The `castUsing` method of the `Castable` interface has been updated to accept an array of arguments. If you are implementing this interface you should update your implementation accordingly:

    public static function castUsing(array $arguments);

<a name="increment-decrement-events"></a>
#### Increment / Decrement Events

**Likelihood Of Impact: Low**

Proper "update" and "save" related model events will now be dispatched when executing the `increment` or `decrement` methods on Eloquent model instances.

<a name="events"></a>
### Events

<a name="the-event-service-provider-class"></a>
#### The `EventServiceProvider` Class

**Likelihood Of Impact: Low**

If your `App\Providers\EventServiceProvider` class contains a `register` function, you should ensure that you call `parent::register` at the beginning of this method. Otherwise, your application's events will not be registered.

<a name="the-dispatcher-contract"></a>
#### The `Dispatcher` Contract

**Likelihood Of Impact: Low**

The `listen` method of the `Illuminate\Contracts\Events\Dispatcher` contract has been updated to make the `$listener` property optional. This change was made to support automatic detection of handled event types via reflection. If you are manually implementing this interface, you should update your implementation accordingly:

    public function listen($events, $listener = null);

<a name="framework"></a>
### Framework

<a name="maintenance-mode-updates"></a>
#### Maintenance Mode Updates

**Likelihood Of Impact: Optional**

The [maintenance mode](/docs/{{version}}/configuration#maintenance-mode) feature of Laravel has been improved in Laravel 8.x. Pre-rendering the maintenance mode template is now supported and eliminates the chances of end users encountering errors during maintenance mode. However, to support this, the following lines must be added to your `public/index.php` file. These lines should be placed directly under the existing `LARAVEL_START` constant definition:

    define('LARAVEL_START', microtime(true));

    if (file_exists(__DIR__.'/../storage/framework/maintenance.php')) {
        require __DIR__.'/../storage/framework/maintenance.php';
    }

<a name="artisan-down-message"></a>
#### The `php artisan down --message` Option

**Likelihood Of Impact: Medium**

The `--message` option of the `php artisan down` command has been removed. As an alternative, consider [pre-rendering your maintenance mode views](/docs/{{version}}/configuration#maintenance-mode) with the message of your choice.

<a name="php-artisan-serve-no-reload-option"></a>
#### The `php artisan serve --no-reload` Option

**Likelihood Of Impact: Low**

A `--no-reload` option has been added to the `php artisan serve` command. This will instruct the built-in server to not reload the server when environment file changes are detected. This option is primarily helpful when running Laravel Dusk tests in a CI environment.

<a name="manager-app-property"></a>
#### Manager `$app` Property

**Likelihood Of Impact: Low**

The previously deprecated `$app` property of the `Illuminate\Support\Manager` class has been removed. If you were relying on this property, you should use the `$container` property instead.

<a name="the-elixir-helper"></a>
#### The `elixir` Helper

**Likelihood Of Impact: Low**

The previously deprecated `elixir` helper has been removed. Applications still using this method are encouraged to upgrade to [Laravel Mix](https://github.com/JeffreyWay/laravel-mix).

<a name="mail"></a>
### Mail

<a name="the-sendnow-method"></a>
#### The `sendNow` Method

**Likelihood Of Impact: Low**

The previously deprecated `sendNow` method has been removed. Instead, please use the `send` method.

<a name="pagination"></a>
### Pagination

<a name="pagination-defaults"></a>
#### Pagination Defaults

**Likelihood Of Impact: High**

The paginator now uses the [Tailwind CSS framework](https://tailwindcss.com) for its default styling. In order to keep using Bootstrap, you should add the following method call to the `boot` method of your application's `AppServiceProvider`:

    use Illuminate\Pagination\Paginator;

    Paginator::useBootstrap();

<a name="queue"></a>
### Queue

<a name="queue-retry-after-method"></a>
#### The `retryAfter` Method

**Likelihood Of Impact: High**

For consistency with other features of Laravel, the `retryAfter` method and `retryAfter` property of queued jobs, mailers, notifications, and listeners have been renamed to `backoff`. You should update the name of this method / property in the relevant classes in your application.

<a name="queue-timeout-at-property"></a>
#### The `timeoutAt` Property

**Likelihood Of Impact: High**

The `timeoutAt` property of queued jobs, notifications, and listeners has been renamed to `retryUntil`. You should update the name of this property in the relevant classes in your application.

<a name="queue-allOnQueue-allOnConnection"></a>
#### The `allOnQueue()` / `allOnConnection()` Methods

**Likelihood Of Impact: High**

For consistency with other dispatching methods, the `allOnQueue()` and `allOnConnection()` methods used with job chaining have been removed. You may use the `onQueue()` and `onConnection()` methods instead. These methods should be called before calling the `dispatch` method:

    ProcessPodcast::withChain([
        new OptimizePodcast,
        new ReleasePodcast
    ])->onConnection('redis')->onQueue('podcasts')->dispatch();

Note that this change only affects code using the `withChain` method. The `allOnQueue()` and `allOnConnection()` are still available when using the global `dispatch()` helper.

<a name="failed-jobs-table-batch-support"></a>
#### Failed Jobs Table Batch Support

**Likelihood Of Impact: Optional**

If you plan to use the [job batching](/docs/{{version}}/queues#job-batching) features of Laravel 8.x, your `failed_jobs` database table will need to be updated. First, a new `uuid` column should be added to your table:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('failed_jobs', function (Blueprint $table) {
        $table->string('uuid')->after('id')->nullable()->unique();
    });

Next, the `failed.driver` configuration option within your `queue` configuration file should be updated to `database-uuids`.

In addition, you may wish to generate UUIDs for your existing failed jobs:

    DB::table('failed_jobs')->whereNull('uuid')->cursor()->each(function ($job) {
        DB::table('failed_jobs')
            ->where('id', $job->id)
            ->update(['uuid' => (string) Illuminate\Support\Str::uuid()]);
    });

<a name="routing"></a>
### Routing

<a name="automatic-controller-namespace-prefixing"></a>
#### Automatic Controller Namespace Prefixing

**Likelihood Of Impact: Optional**

In previous releases of Laravel, the `RouteServiceProvider` class contained a `$namespace` property with a value of `App\Http\Controllers`. This value of this property was used to automatically prefix controller route declarations and controller route URL generation such as when calling the `action` helper.

In Laravel 8, this property is set to `null` by default. This allows your controller route declarations to use the standard PHP callable syntax, which provides better support for jumping to the controller class in many IDEs:

    use App\Http\Controllers\UserController;

    // Using PHP callable syntax...
    Route::get('/users', [UserController::class, 'index']);

    // Using string syntax...
    Route::get('/users', 'App\Http\Controllers\UserController@index');

In most cases, this won't impact applications that are being upgraded because your `RouteServiceProvider` will still contain the `$namespace` property with its previous value. However, if you upgrade your application by creating a brand new Laravel project, you may encounter this as a breaking change.

If you would like to continue using the original auto-prefixed controller routing, you can simply set the value of the `$namespace` property within your `RouteServiceProvider` and update the route registrations within the `boot` method to use the `$namespace` property:

    class RouteServiceProvider extends ServiceProvider
    {
        /**
         * The path to the "home" route for your application.
         *
         * This is used by Laravel authentication to redirect users after login.
         *
         * @var string
         */
        public const HOME = '/home';

        /**
         * If specified, this namespace is automatically applied to your controller routes.
         *
         * In addition, it is set as the URL generator's root namespace.
         *
         * @var string
         */
        protected $namespace = 'App\Http\Controllers';

        /**
         * Define your route model bindings, pattern filters, etc.
         *
         * @return void
         */
        public function boot()
        {
            $this->configureRateLimiting();

            $this->routes(function () {
                Route::middleware('web')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/web.php'));

                Route::prefix('api')
                    ->middleware('api')
                    ->namespace($this->namespace)
                    ->group(base_path('routes/api.php'));
            });
        }

        /**
         * Configure the rate limiters for the application.
         *
         * @return void
         */
        protected function configureRateLimiting()
        {
            RateLimiter::for('api', function (Request $request) {
                return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());
            });
        }
    }

<a name="scheduling"></a>
### Scheduling

<a name="the-cron-expression-library"></a>
#### The `cron-expression` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `dragonmantank/cron-expression` has been updated from `2.x` to `3.x`. This should not cause any breaking change in your application unless you are interacting with the `cron-expression` library directly. If you are interacting with this library directly, please review its [change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md).

<a name="session"></a>
### Session

<a name="the-session-contract"></a>
#### The `Session` Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Session\Session` contract has received a new `pull` method. If you are implementing this contract manually, you should update your implementation accordingly:

    /**
     * Get the value of a given key and then forget it.
     *
     * @param  string  $key
     * @param  mixed  $default
     * @return mixed
     */
    public function pull($key, $default = null);

<a name="testing"></a>
### Testing

<a name="decode-response-json-method"></a>
#### The `decodeResponseJson` Method

**Likelihood Of Impact: Low**

The `decodeResponseJson` method that belongs to the `Illuminate\Testing\TestResponse` class no longer accepts any arguments. Please consider using the `json` method instead.

<a name="assert-exact-json-method"></a>
#### The `assertExactJson` Method

**Likelihood Of Impact: Medium**

The `assertExactJson` method now requires numeric keys of compared arrays to match and be in the same order. If you would like to compare JSON against an array without requiring numerically keyed arrays to have the same order, you may use the `assertSimilarJson` method instead.

<a name="validation"></a>
### Validation

<a name="database-rule-connections"></a>
### Database Rule Connections

**Likelihood Of Impact: Low**

The `unique` and `exists` rules will now respect the specified connection name (accessed via the model's `getConnectionName` method) of Eloquent models when performing queries.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...8.x) and choose which updates are important to you.
