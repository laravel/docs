# Upgrade Guide

- [Upgrading To 5.2.0 From 5.1](#upgrade-5.2.0)
- [Upgrading To 5.1.11](#upgrade-5.1.11)
- [Upgrading To 5.1.0](#upgrade-5.1.0)
- [Upgrading To 5.0.16](#upgrade-5.0.16)
- [Upgrading To 5.0 From 4.2](#upgrade-5.0)
- [Upgrading To 4.2 From 4.1](#upgrade-4.2)
- [Upgrading To 4.1.29 From <= 4.1.x](#upgrade-4.1.29)
- [Upgrading To 4.1.26 From <= 4.1.25](#upgrade-4.1.26)
- [Upgrading To 4.1 From 4.0](#upgrade-4.1)

<a name="upgrade-5.2.0"></a>
## Upgrading To 5.2.0 From 5.1

#### Estimated Upgrade Time: Less Than 1 Hour

> **Note:** We attempt to provide a very comprehensive listing of every possible breaking change made to the framework. However, many of these changes may not apply to your own application.

### Updating Dependencies

Update your `composer.json` file to point to `laravel/framework 5.2.*`.

Add `"symfony/dom-crawler": "~3.0"` and `"symfony/css-selector": "~3.0"` to the `require-dev` section of your `composer.json` file.

### Authentication

#### Configuration File

You should update your `config/auth.php` configuration file with the following: [https://github.com/laravel/laravel/blob/638b261a68913bae9a64f6d540612b862fa3c4dd/config/auth.php](https://github.com/laravel/laravel/blob/638b261a68913bae9a64f6d540612b862fa3c4dd/config/auth.php)

Once you have updated the file with a fresh copy, set your authentication configuration options to their desired value based on your old configuration file. If you were using the typical, Eloquent based authentication services available in Laravel 5.1, most values should remain the same.

Take special note of the `passwords.users.email` configuration option in the new `auth.php` configuration file and verify that the view path matches the actual view path for your application, as the default path to this view was changed in Laravel 5.2. If the default value in the new configuration file does not match your existing view, update the configuration option.

#### Contracts

If you are implementing the `Illuminate\Contracts\Auth\Authenticatable` contract but are **not** using the `Authenticatable` trait, you should add a new `getAuthIdentifierName` method to your contract implementation. Typically, this method will return the column name of the "primary key" of your authenticatable entity. For example: `id`.

This is unlikely to affect your application unless you were manually implementing this interface.

#### Custom Drivers

If you are using the `Auth::extend` method to define a custom method of retrieving users, you should now use `Auth::provider` to define your custom user provider. Once you have defined the custom provider, you may configure it in the `providers` array of your new `auth.php` configuration file.

For more information on custom authentication providers, consult the [full authentication documentation](/docs/{{version}}/authentication).

#### Redirection

The `loginPath()` method has been removed from `Illuminate\Foundation\Auth\AuthenticatesUsers`, so placing a `$loginPath` variable in your `AuthController` is no longer required. By default, the trait will always redirect users back to their previous location on authentication errors.

### Authorization

The `Illuminate\Auth\Access\UnauthorizedException` has been renamed to `Illuminate\Auth\Access\AuthorizationException`. This is unlikely to affect your application if you are not manually catching this exception.

### Collections

#### Eloquent Base Collections

The Eloquent collection instance now returns a base Collection (`Illuminate\Support\Collection`) for the following methods: `pluck`, `keys`, `zip`, `collapse`, `flatten`, `flip`.

#### Key Preservation

The `slice`, `chunk`, and `reverse` methods now preserve keys on the collection. If you do not want these methods to preserve keys, use the `values` method on the `Collection` instance.

### Composer Class

The `Illuminate\Foundation\Composer` class has been moved to `Illuminate\Support\Composer`. This is unlikely to affect your application if you were not manually using this class.

### Commands And Handlers

#### Self-Handling Commands

You no longer need to implement the `SelfHandling` contract on your jobs / commands. All jobs are now self-handling by default, so you can remove this interface from your classes.

#### Separate Commands & Handlers

The Laravel 5.2 command bus now only supports self-handling commands and no longer supports separate commands and handlers.

If you would like to continue using separate commands and handlers, you may install a Laravel Collective package which provides backwards-compatible support for this: [https://github.com/LaravelCollective/bus](https://github.com/laravelcollective/bus)

### Configuration

#### Environment Value

Add an `env` configuration option to your `app.php` configuration file that looks like the following:

    'env' => env('APP_ENV', 'production'),

#### Caching And Env

If you are using the `config:cache` command during deployment, you **must** make sure that you are only calling the `env` function from within your configuration files, and not from anywhere else in your application.

If you are calling `env` from within your application, it is strongly recommended you add proper configuration values to your configuration files and call `env` from that location instead, allowing you to convert your `env` calls to `config` calls.

#### Compiled Classes

If present, remove the following lines from `config/compile.php` in the `files` array:

    realpath(__DIR__.'/../app/Providers/BusServiceProvider.php'),
    realpath(__DIR__.'/../app/Providers/ConfigServiceProvider.php'),

Not doing so can trigger an error when running `php artisan optimize` if the service providers listed here do not exist.

### CSRF Verification

CSRF verification is no longer automatically performed when running unit tests. This is unlikely to affect your application.

### Database

#### MySQL Dates

Starting with MySQL 5.7, `0000-00-00 00:00:00` is no longer considered a valid date, since `strict` mode is enabled by default. All timestamp columns should receive a valid default value when you insert records into your database. You may use the `useCurrent` method in your migrations to default the timestamp columns to the current timestamps, or you may make the timestamps `nullable` to allow `null` values:

    $table->timestamp('foo')->nullable();

    $table->timestamp('foo')->useCurrent();

    $table->nullableTimestamps();

#### MySQL JSON Column Type

The `json` column type now creates actual JSON columns when used by the MySQL driver. If you are not running MySQL 5.7 or above, this column type will not be available to you. Instead, use the `text` column type in your migration.

#### Seeding

When running database seeds, all Eloquent models are now unguarded by default. Previously a call to `Model::unguard()` was required. You can call `Model::reguard()` at the top of your `DatabaseSeeder` class if you would like models to be guarded during seeding.

### Eloquent

#### Date Casts

Any attributes that have been added to your `$casts` property as `date` or `datetime` will now be converted to a string when `toArray` is called on the model or collection of models. This makes the date casting conversion consistent with dates specified in your `$dates` array.

#### Global Scopes

The global scopes implementation has been re-written to be much easier to use. Your global scopes no longer need a `remove` method, so it may be removed from any global scopes you have written.

If you were calling `getQuery` on an Eloquent query builder to access the underlying query builder instance, you should now call `toBase`.

If you were calling the `remove` method directly for any reason, you should change this call to `$eloquentBuilder->withoutGlobalScope($scope)`.

New methods `withoutGlobalScope` and `withoutGlobalScopes` have been added to the Eloquent query builder. Any calls to `$model->removeGlobalScopes($builder)` may be changed to simply `$builder->withoutGlobalScopes()`.

#### Primary keys

By default, Eloquent assumes your primary keys are integers and will automatically cast them to integers. For any primary key that is not an integer you should override the `$incrementing` property on your Eloquent model to `false`:

    /**
     * Indicates if the IDs are auto-incrementing.
     *
     * @var bool
     */
    public $incrementing = true;

### Events

#### Core Event Objects

Some of the core events fired by Laravel now use event objects instead of string event names and dynamic parameters. Below is a list of the old event names and their new object based counterparts:

Old  | New
------------- | -------------
`artisan.start`  |  `Illuminate\Console\Events\ArtisanStarting`
`auth.attempting`  |  `Illuminate\Auth\Events\Attempting`
`auth.login`  |  `Illuminate\Auth\Events\Login`
`auth.logout`  |  `Illuminate\Auth\Events\Logout`
`cache.missed`  |  `Illuminate\Cache\Events\CacheMissed`
`cache.hit`  |  `Illuminate\Cache\Events\CacheHit`
`cache.write`  |  `Illuminate\Cache\Events\KeyWritten`
`cache.delete`  |  `Illuminate\Cache\Events\KeyForgotten`
`connection.{name}.beginTransaction`  |  `Illuminate\Database\Events\TransactionBeginning`
`connection.{name}.committed`  |  `Illuminate\Database\Events\TransactionCommitted`
`connection.{name}.rollingBack`  |  `Illuminate\Database\Events\TransactionRolledBack`
`illuminate.query`  |  `Illuminate\Database\Events\QueryExecuted`
`illuminate.queue.before`  |  `Illuminate\Queue\Events\JobProcessing`
`illuminate.queue.after`  |  `Illuminate\Queue\Events\JobProcessed`
`illuminate.queue.failed`  |  `Illuminate\Queue\Events\JobFailed`
`illuminate.queue.stopping`  |  `Illuminate\Queue\Events\WorkerStopping`
`mailer.sending`  |  `Illuminate\Mail\Events\MessageSending`
`router.matched`  |  `Illuminate\Routing\Events\RouteMatched`

Each of these event objects contains **exactly** the same parameters that were passed to the event handler in Laravel 5.1. For example, if you were using `DB::listen` in 5.1.*, you may update your code like so for 5.2.*:

    DB::listen(function ($event) {
        dump($event->sql);
        dump($event->bindings);
    });

You may check out each of the new event object classes to see their public properties.

### Exception Handling

Your `App\Exceptions\Handler` class' `$dontReport` property should be updated to include at least the following exception types:

    use Illuminate\Validation\ValidationException;
    use Illuminate\Auth\Access\AuthorizationException;
    use Illuminate\Database\Eloquent\ModelNotFoundException;
    use Symfony\Component\HttpKernel\Exception\HttpException;

    /**
     * A list of the exception types that should not be reported.
     *
     * @var array
     */
    protected $dontReport = [
        AuthorizationException::class,
        HttpException::class,
        ModelNotFoundException::class,
        ValidationException::class,
    ];

### Helper Functions

The `url()` helper function now returns a `Illuminate\Routing\UrlGenerator` instance when no path is provided.

### Implicit Model Binding

Laravel 5.2 includes "implicit model binding", a convenient new feature to automatically inject model instances into routes and controllers based on the identifier present in the URI. However, this does change the behavior of routes and controllers that type-hint model instances.

If you were type-hinting a model instance in your route or controller and were expecting an **empty** model instance to be injected, you should remove this type-hint and create an empty model instance directly within your route or controller; otherwise, Laravel will attempt to retrieve an existing model instance from the database based on the identifier present in the route's URI.

### IronMQ

The IronMQ queue driver has been moved into its own package and is no longer shipped with the core framework.

[http://github.com/LaravelCollective/iron-queue](http://github.com/laravelcollective/iron-queue)

### Jobs / Queue

The `php artisan make:job` command now creates a "queued" job class definition by default. If you would like to create a "sync" job, use the `--sync` option when issuing the command.

### Mail

The `pretend` mail configuration option has been removed. Instead, use the `log` mail driver, which performs the same function as `pretend` and logs even more information about the mail message.

### Pagination

To be consistent with other URLs generated by the framework, the paginator URLs no longer contain a trailing slash. This is unlikely to affect your application.

### Service Providers

The `Illuminate\Foundation\Providers\ArtisanServiceProvider` should be removed from your service provider list in your `app.php` configuration file.

The `Illuminate\Routing\ControllerServiceProvider` should be removed from your service provider list in your `app.php` configuration file.

### Sessions

Because of changes to the authentication system, any existing sessions will be invalidated when you upgrade to Laravel 5.2.

#### Database Session Driver

A new `database` session driver has been written for the framework which includes more information about the user such as their user ID, IP address, and user-agent. If you would like to continue using the old driver you may specify the `legacy-database` driver in your `session.php` configuration file.

If you would like to use the new driver, you should add the `user_id (nullable integer)`, `ip_address (nullable string)`, and `user_agent (text)` columns to your session database table.

### Stringy

The "Stringy" library is no longer included with the framework. You may install it manually via Composer if you wish to use it in your application.

### Validation

#### Exception Types

The `ValidatesRequests` trait now throws an instance of `Illuminate\Foundation\Validation\ValidationException` instead of throwing an instance of `Illuminate\Http\Exception\HttpResponseException`. This is unlikely to affect your application unless you were manually catching this exception.

### Deprecations

The following features are deprecated in 5.2 and will be removed in the 5.3 release in June 2016:

- `Illuminate\Contracts\Bus\SelfHandling` contract. Can be removed from jobs.
- The `lists` method on the Collection, query builder and Eloquent query builder objects has been renamed to `pluck`. The method signature remains the same.
- Implicit controller routes using `Route::controller` have been deprecated. Please use explicit route registration in your routes file. This will likely be extracted into a package.
- The `get`, `post`, and other route helper functions have been removed. You may use the `Route` facade instead.
- The `database` session driver from 5.1 has been renamed to `legacy-database` and will be removed. Consult notes on the "database session driver" above for more information.
- The `Str::randomBytes` function has been deprecated in favor of the `random_bytes` native PHP function.
- The `Str::equals` function has been deprecated in favor of the `hash_equals` native PHP function.
- `Illuminate\View\Expression` has been deprecated in favor of `Illuminate\Support\HtmlString`.
- The `WincacheStore` cache driver has been removed.

<a name="upgrade-5.1.11"></a>
## Upgrading To 5.1.11

Laravel 5.1.11 includes support for [authorization](/docs/{{version}}/authorization) and [policies](/docs/{{version}}/authorization#policies). Incorporating these new features into your existing Laravel 5.1 applications is simple.

> **Note:** These upgrades are **optional**, and ignoring them will not affect your application.

#### Create The Policies Directory

First, create an empty `app/Policies` directory within your application.

#### Create / Register The AuthServiceProvider & Gate Facade

Create a `AuthServiceProvider` within your `app/Providers` directory. You may copy the contents of the default provider [from GitHub](https://raw.githubusercontent.com/laravel/laravel/master/app/Providers/AuthServiceProvider.php). Remember to change the provider's namespace if your application is using a custom namespace. After creating the provider, be sure to register it in your `app.php` configuration file's `providers` array.

Also, you should register the `Gate` facade in your `app.php` configuration file's `aliases` array:

    'Gate' => Illuminate\Support\Facades\Gate::class,

#### Update The User Model

Secondly, use the `Illuminate\Foundation\Auth\Access\Authorizable` trait and `Illuminate\Contracts\Auth\Access\Authorizable` contract on your `App\User` model:

    <?php

    namespace App;

    use Illuminate\Auth\Authenticatable;
    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Auth\Passwords\CanResetPassword;
    use Illuminate\Foundation\Auth\Access\Authorizable;
    use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
    use Illuminate\Contracts\Auth\Access\Authorizable as AuthorizableContract;
    use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;

    class User extends Model implements AuthenticatableContract,
                                        AuthorizableContract,
                                        CanResetPasswordContract
    {
        use Authenticatable, Authorizable, CanResetPassword;
    }

#### Update The Base Controller

Next, update your base `App\Http\Controllers\Controller` controller to use the `Illuminate\Foundation\Auth\Access\AuthorizesRequests` trait:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Foundation\Bus\DispatchesJobs;
    use Illuminate\Routing\Controller as BaseController;
    use Illuminate\Foundation\Validation\ValidatesRequests;
    use Illuminate\Foundation\Auth\Access\AuthorizesRequests;

    abstract class Controller extends BaseController
    {
        use AuthorizesRequests, DispatchesJobs, ValidatesRequests;
    }

<a name="upgrade-5.1.0"></a>
## Upgrading To 5.1.0

#### Estimated Upgrade Time: Less Than 1 Hour

### Update `bootstrap/autoload.php`

Update the `$compiledPath` variable in `bootstrap/autoload.php` to the following:

    $compiledPath = __DIR__.'/cache/compiled.php';

### Create `bootstrap/cache` Directory

Within your `bootstrap` directory, create a `cache` directory (`bootstrap/cache`). Place a `.gitignore` file in this directory with the following contents:

    *
    !.gitignore

This directory should be writable, and will be used by the framework to store temporary optimization files like `compiled.php`, `routes.php`, `config.php`, and `services.json`.

### Add `BroadcastServiceProvider` Provider

Within your `config/app.php` configuration file, add `Illuminate\Broadcasting\BroadcastServiceProvider` to the `providers` array.

### Authentication

If you are using the provided `AuthController` which uses the `AuthenticatesAndRegistersUsers` trait, you will need to make a few changes to how new users are validated and created.

First, you no longer need to pass the `Guard` and `Registrar` instances to the base constructor. You can remove these dependencies entirely from your controller's constructor.

Secondly, the `App\Services\Registrar` class used in Laravel 5.0 is no longer needed. You can simply copy and paste your `validator` and `create` method from this class directly into your `AuthController`. No other changes should need to be made to these methods; however, you should be sure to import the `Validator` facade and your `User` model at the top of your `AuthController`.

#### Password Controller

The included `PasswordController` no longer requires any dependencies in its constructor. You may remove both of the dependencies that were required under 5.0.

### Validation

If you are overriding the `formatValidationErrors` method on your base controller class, you should now type-hint the `Illuminate\Contracts\Validation\Validator` contract instead of the concrete `Illuminate\Validation\Validator` instance.

Likewise, if you are overriding the `formatErrors` method on the base form request class, you should now type-hint `Illuminate\Contracts\Validation\Validator` contract instead of the concrete `Illuminate\Validation\Validator` instance.

### Migrations

If you have any migrations that rename a column or any migrations that drop columns from a SQLite database, you will need to add the `doctrine/dbal` dependency to your `composer.json` file and run the `composer update` command in your terminal to install the library.

### Eloquent

#### The `create` Method

Eloquent's `create` method can now be called without any parameters. If you are overriding the `create` method in your own models, set the default value of the `$attributes` parameter to an array:

    public static function create(array $attributes = [])
    {
        // Your custom implementation
    }

#### The `find` Method

If you are overriding the `find` method in your own models and calling `parent::find()` within your custom method, you should now change it to call the `find` method on the Eloquent query builder:

    public static function find($id, $columns = ['*'])
    {
        $model = static::query()->find($id, $columns);

        // ...

        return $model;
    }

#### The `lists` Method

The `lists` method now returns a `Collection` instance instead of a plain array for Eloquent queries. If you would like to convert the `Collection` into a plain array, use the `all` method:

    User::lists('id')->all();

Be aware that the Query Builder `lists` method still returns an array.

#### Date Formatting

Previously, the storage format for Eloquent date fields could be modified by overriding the `getDateFormat` method on your model. This is still possible; however, for convenience you may simply specify a `$dateFormat` property on the model instead of overriding the method.

The date format is also now applied when serializing a model to an `array` or JSON. This may change the format of your JSON serialized date fields when migrating from Laravel 5.0 to 5.1. To set a specific date format for serialized models, you may override the `serializeDate(DateTime $date)` method on your model. This method allows you to have granular control over the formatting of serialized Eloquent date fields without changing their storage format.

### The Collection Class

#### The `sort` Method

The `sort` method now returns a fresh collection instance instead of modifying the existing collection:

    $collection = $collection->sort($callback);

#### The `sortBy` Method

The `sortBy` method now returns a fresh collection instance instead of modifying the existing collection:

    $collection = $collection->sortBy('name');

#### The `groupBy` Method

The `groupBy` method now returns `Collection` instances for each item in the parent `Collection`. If you would like to convert all of the items back to plain arrays, you may `map` over them:

    $collection->groupBy('type')->map(function($item)
    {
        return $item->all();
    });

#### The `lists` Method

The `lists` method now returns a `Collection` instance instead of a plain array. If you would like to convert the `Collection` into a plain array, use the `all` method:

    $collection->lists('id')->all();

### Commands & Handlers

The `app/Commands` directory has been renamed to `app/Jobs`. However, you are not required to move all of your commands to the new location, and you may continue using the `make:command` and `handler:command` Artisan commands to generate your classes.

Likewise, the `app/Handlers` directory has been renamed to `app/Listeners` and now only contains event listeners. However, you are not required to move or rename your existing command and event handlers, and you may continue to use the `handler:event` command to generate event handlers.

By providing backwards compatibility for the Laravel 5.0 folder structure, you may upgrade your applications to Laravel 5.1 and slowly upgrade your events and commands to their new locations when it is convenient for you or your team.

### Blade

The `createMatcher`, `createOpenMatcher`, and `createPlainMatcher` methods have been removed from the Blade compiler. Use the new `directive` method to create custom directives for Blade in Laravel 5.1. Consult the [extending blade](/docs/{{version}}/blade#extending-blade) documentation for more information.

### Tests

Add the protected `$baseUrl` property to the `tests/TestCase.php` file:

    protected $baseUrl = 'http://localhost';

### Translation Files

The default directory for published language files for vendor packages has been moved. Move any vendor package language files from `resources/lang/packages/{locale}/{namespace}` to `resources/lang/vendor/{namespace}/{locale}` directory. For example, `Acme/Anvil` package's `acme/anvil::foo` namespaced English language file would be moved from `resources/lang/packages/en/acme/anvil/foo.php` to `resources/lang/vendor/acme/anvil/en/foo.php`.

### Amazon Web Services SDK

If you are using the AWS SQS queue driver or the AWS SES e-mail driver, you should update your installed AWS PHP SDK to version 3.0.

If you are using the Amazon S3 filesystem driver, you will need to update the corresponding Flysystem package via Composer:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`

### Deprecations

The following Laravel features have been deprecated and will be removed entirely with the release of Laravel 5.2 in December 2015:

<div class="content-list" markdown="1">
- Route filters have been deprecated in preference of [middleware](/docs/{{version}}/middleware).
- The `Illuminate\Contracts\Routing\Middleware` contract has been deprecated. No contract is required on your middleware. In addition, the `TerminableMiddleware` contract has also been deprecated. Instead of implementing the interface, simply define a `terminate` method on your middleware.
- The `Illuminate\Contracts\Queue\ShouldBeQueued` contract has been deprecated in favor of `Illuminate\Contracts\Queue\ShouldQueue`.
- Iron.io "push queues" have been deprecated in favor of typical Iron.io queues and [queue listeners](/docs/{{version}}/queues#running-the-queue-listener).
- The `Illuminate\Foundation\Bus\DispatchesCommands` trait has been deprecated and renamed to `Illuminate\Foundation\Bus\DispatchesJobs`.
- `Illuminate\Container\BindingResolutionException` has been moved to `Illuminate\Contracts\Container\BindingResolutionException`.
- The service container's `bindShared` method has been deprecated in favor of the `singleton` method.
- The Eloquent and query builder `pluck` method has been deprecated and renamed to `value`.
- The collection `fetch` method has been deprecated in favor of the `pluck` method.
- The `array_fetch` helper has been deprecated in favor of the `array_pluck` method.
</div>

<a name="upgrade-5.0.16"></a>
## Upgrading To 5.0.16

In your `bootstrap/autoload.php` file, update the `$compiledPath` variable to:

    $compiledPath = __DIR__.'/../vendor/compiled.php';


### Service Providers

The `App\Providers\BusServiceProvider` may be removed from your service provider list in your `app.php` configuration file.

The `App\Providers\ConfigServiceProvider` may be removed from your service provider list in your `app.php` configuration file.


<a name="upgrade-5.0"></a>
## Upgrading To 5.0 From 4.2

### Fresh Install, Then Migrate

The recommended method of upgrading is to create a new Laravel `5.0` install and then to copy your `4.2` site's unique application files into the new application. This would include controllers, routes, Eloquent models, Artisan commands, assets, and other code specific files to your application.

To start, [install a new Laravel 5.0 application](/docs/5.0/installation) into a fresh directory in your local environment.  Do not install any versions newer than 5.0 yet, since we need to complete the migration steps for 5.0 first. We'll discuss each piece of the migration process in further detail below.

### Composer Dependencies & Packages

Don't forget to copy any additional Composer dependencies into your 5.0 application. This includes third-party code such as SDKs.

Some Laravel-specific packages may not be compatible with Laravel 5 on initial release. Check with your package's maintainer to determine the proper version of the package for Laravel 5. Once you have added any additional Composer dependencies your application needs, run `composer update`.

### Namespacing

By default, Laravel 4 applications did not utilize namespacing within your application code. So, for example, all Eloquent models and controllers simply lived in the "global" namespace. For a quicker migration, you can simply leave these classes in the global namespace in Laravel 5 as well.

### Configuration

#### Migrating Environment Variables

Copy the new `.env.example` file to `.env`, which is the `5.0` equivalent of the old `.env.php` file. Set any appropriate values there, like your `APP_ENV` and `APP_KEY` (your encryption key), your database credentials, and your cache and session drivers.

Additionally, copy any custom values you had in your old `.env.php` file and place them in both `.env` (the real value for your local environment) and `.env.example` (a sample instructional value for other team members).

For more information on environment configuration, view the [full documentation](/docs/{{version}}/installation#environment-configuration).

> **Note:** You will need to place the appropriate `.env` file and values on your production server before deploying your Laravel 5 application.

#### Configuration Files

Laravel 5.0 no longer uses `app/config/{environmentName}/` directories to provide specific configuration files for a given environment. Instead, move any configuration values that vary by environment into `.env`, and then access them in your configuration files using `env('key', 'default value')`. You will see examples of this in the `config/database.php` configuration file.

Set the config files in the `config/` directory to represent either the values that are consistent across all of your environments, or set them to use `env()` to load values that vary by environment.

Remember, if you add more keys to `.env` file, add sample values to the `.env.example` file as well. This will help your other team members create their own `.env` files.

### Routes

Copy and paste your old `routes.php` file into your new `app/Http/routes.php`.

### Controllers

Next, move all of your controllers into the `app/Http/Controllers` directory. Since we are not going to migrate to full namespacing in this guide, add the `app/Http/Controllers` directory to the `classmap` directive of your `composer.json` file. Next, you can remove the namespace from the abstract `app/Http/Controllers/Controller.php` base class. Verify that your migrated controllers are extending this base class.

In your `app/Providers/RouteServiceProvider.php` file, set the `namespace` property to `null`.

### Route Filters

Copy your filter bindings from `app/filters.php` and place them into the `boot()` method of `app/Providers/RouteServiceProvider.php`. Add `use Illuminate\Support\Facades\Route;` in the `app/Providers/RouteServiceProvider.php` in order to continue using the `Route` Facade.

You do not need to move over any of the default Laravel 4.0 filters such as `auth` and `csrf`; they're all here, but as middleware. Edit any routes or controllers that reference the old default filters (e.g. `['before' => 'auth']`) and change them to reference the new middleware (e.g. `['middleware' => 'auth'].`)

Filters are not removed in Laravel 5. You can still bind and use your own custom filters using `before` and `after`.

### Global CSRF

By default, [CSRF protection](/docs/{{version}}/routing#csrf-protection) is enabled on all routes. If you'd like to disable this, or only manually enable it on certain routes, remove this line from `App\Http\Kernel`'s `middleware` array:

    'App\Http\Middleware\VerifyCsrfToken',

If you want to use it elsewhere, add this line to `$routeMiddleware`:

    'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

Now you can add the middleware to individual routes / controllers using `['middleware' => 'csrf']` on the route. For more information on middleware, consult the [full documentation](/docs/{{version}}/middleware).

### Eloquent Models

Feel free to create a new `app/Models` directory to house your Eloquent models. Again, add this directory to the `classmap` directive of your `composer.json` file.

Update any models using `SoftDeletingTrait` to use `Illuminate\Database\Eloquent\SoftDeletes`.

#### Eloquent Caching

Eloquent no longer provides the `remember` method for caching queries. You now are responsible for caching your queries manually using the `Cache::remember` function. For more information on caching, consult the [full documentation](/docs/{{version}}/cache).

### User Authentication Model

To upgrade your `User` model for Laravel 5's authentication system, follow these instructions:

**Delete the following from your `use` block:**

```php
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
```

**Add the following to your `use` block:**

```php
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
```

**Remove the UserInterface and RemindableInterface interfaces.**

**Mark the class as implementing the following interfaces:**

```php
implements AuthenticatableContract, CanResetPasswordContract
```

**Include the following traits within the class declaration:**

```php
use Authenticatable, CanResetPassword;
```

**If you used them, remove `Illuminate\Auth\Reminders\RemindableTrait`  and `Illuminate\Auth\UserTrait` from your use block and your class declaration.**

### Cashier User Changes

The name of the trait and interface used by [Laravel Cashier](/docs/{{version}}/billing) has changed. Instead of using `BillableTrait`, use the `Laravel\Cashier\Billable` trait. And, instead of `Laravel\Cashier\BillableInterface` implement the `Laravel\Cashier\Contracts\Billable` interface instead. No other method changes are required.

### Artisan Commands

Move all of your command classes from your old `app/commands` directory to the new `app/Console/Commands` directory. Next, add the `app/Console/Commands` directory to the `classmap` directive of your `composer.json` file.

Then, copy your list of Artisan commands from `start/artisan.php` into the `commands` array of the `app/Console/Kernel.php` file.

### Database Migrations & Seeds

Delete the two migrations included with Laravel 5.0, since you should already have the users table in your database.

Move all of your migration classes from the old `app/database/migrations` directory to the new `database/migrations`. All of your seeds should be moved from `app/database/seeds` to `database/seeds`.

### Global IoC Bindings

If you have any [service container](/docs/{{version}}/container) bindings in `start/global.php`, move them all to the `register` method of the `app/Providers/AppServiceProvider.php` file. You may need to import the `App` facade.

Optionally, you may break these bindings up into separate service providers by category.

### Views

Move your views from `app/views` to the new `resources/views` directory.

### Blade Tag Changes

For better security by default, Laravel 5.0 escapes all output from both the `{{ }}` and `{{{ }}}` Blade directives. A new `{!! !!}` directive has been introduced to display raw, unescaped output. The most secure option when upgrading your application is to only use the new `{!! !!}` directive when you are **certain** that it is safe to display raw output.

However, if you **must** use the old Blade syntax, add the following lines at the bottom of `AppServiceProvider@register`:

```php
\Blade::setRawTags('{{', '}}');
\Blade::setContentTags('{{{', '}}}');
\Blade::setEscapedContentTags('{{{', '}}}');
```

This should not be done lightly, and may make your application more vulnerable to XSS exploits. Also, comments with `{{--` will no longer work.

### Translation Files

Move your language files from `app/lang` to the new `resources/lang` directory.

### Public Directory

Copy your application's public assets from your `4.2` application's `public` directory to your new application's `public` directory. Be sure to keep the `5.0` version of `index.php`.

### Tests

Move your tests from `app/tests` to the new `tests` directory.

### Misc. Files

Copy in any other files in your project. For example, `.scrutinizer.yml`, `bower.json` and other similar tooling configuration files.

You may move your Sass, Less, or CoffeeScript to any location you wish. The `resources/assets` directory could be a good default location.

### Form & HTML Helpers

If you're using Form or HTML helpers, you will see an error stating `class 'Form' not found` or `class 'Html' not found`. The Form and HTML helpers have been deprecated in Laravel 5.0; however, there are community-driven replacements such as those maintained by the [Laravel Collective](http://laravelcollective.com/docs/{{version}}/html).

For example, you may add `"laravelcollective/html": "~5.0"` to your `composer.json` file's `require` section.

You'll also need to add the Form and HTML facades and service provider. Edit `config/app.php` and add this line to the 'providers' array:

    'Collective\Html\HtmlServiceProvider',

Next, add these lines to the 'aliases' array:

    'Form' => 'Collective\Html\FormFacade',
    'Html' => 'Collective\Html\HtmlFacade',

### CacheManager

If your application code was injecting `Illuminate\Cache\CacheManager` to get a non-Facade version of Laravel's cache, inject `Illuminate\Contracts\Cache\Repository` instead.

### Pagination

Replace any calls to `$paginator->links()` with `$paginator->render()`.

Replace any calls to `$paginator->getFrom()` and `$paginator->getTo()` with `$paginator->firstItem()` and `$paginator->lastItem()` respectively.

Remove the "get" prefix from calls to `$paginator->getPerPage()`, `$paginator->getCurrentPage()`, `$paginator->getLastPage()` and `$paginator->getTotal()` (e.g. `$paginator->perPage()`).

### Beanstalk Queuing

Laravel 5.0 now requires `"pda/pheanstalk": "~3.0"` instead of `"pda/pheanstalk": "~2.1"`.

### Remote

The Remote component has been deprecated.

### Workbench

The Workbench component has been deprecated.

<a name="upgrade-4.2"></a>
## Upgrading To 4.2 From 4.1

### PHP 5.4+

Laravel 4.2 requires PHP 5.4.0 or greater.

### Encryption Defaults

Add a new `cipher` option in your `app/config/app.php` configuration file. The value of this option should be `MCRYPT_RIJNDAEL_256`.

    'cipher' => MCRYPT_RIJNDAEL_256

This setting may be used to control the default cipher used by the Laravel encryption facilities.

> **Note:** In Laravel 4.2, the default cipher is `MCRYPT_RIJNDAEL_128` (AES), which is considered to be the most secure cipher. Changing the cipher back to `MCRYPT_RIJNDAEL_256` is required to decrypt cookies/values that were encrypted in Laravel <= 4.1

### Soft Deleting Models Now Use Traits

If you are using soft deleting models, the `softDeletes` property has been removed. You must now use the `SoftDeletingTrait` like so:

    use Illuminate\Database\Eloquent\SoftDeletingTrait;

    class User extends Eloquent
    {
        use SoftDeletingTrait;
    }

You must also manually add the `deleted_at` column to your `dates` property:

    class User extends Eloquent
    {
        use SoftDeletingTrait;

        protected $dates = ['deleted_at'];
    }

The API for all soft delete operations remains the same.

> **Note:** The `SoftDeletingTrait` can not be applied on a base model. It must be used on an actual model class.

### View / Pagination Environment Renamed

If you are directly referencing the `Illuminate\View\Environment` class or `Illuminate\Pagination\Environment` class, update your code to reference `Illuminate\View\Factory` and `Illuminate\Pagination\Factory` instead. These two classes have been renamed to better reflect their function.

### Additional Parameter On Pagination Presenter

If you are extending the `Illuminate\Pagination\Presenter` class, the abstract method `getPageLinkWrapper` signature has changed to add the `rel` argument:

    abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Iron.Io Queue Encryption

If you are using the Iron.io queue driver, you will need to add a new `encrypt` option to your queue configuration file:

    'encrypt' => true

<a name="upgrade-4.1.29"></a>
## Upgrading To 4.1.29 From <= 4.1.x

Laravel 4.1.29 improves the column quoting for all database drivers. This protects your application from some mass assignment vulnerabilities when **not** using the `fillable` property on models. If you are using the `fillable` property on your models to protect against mass assignment, your application is not vulnerable. However, if you are using `guarded` and are passing a user controlled array into an "update" or "save" type function, you should upgrade to `4.1.29` immediately as your application may be at risk of mass assignment.

To upgrade to Laravel 4.1.29, simply `composer update`. No breaking changes are introduced in this release.

<a name="upgrade-4.1.26"></a>
## Upgrading To 4.1.26 From <= 4.1.25

Laravel 4.1.26 introduces security improvements for "remember me" cookies. Before this update, if a remember cookie was hijacked by another malicious user, the cookie would remain valid for a long period of time, even after the true owner of the account reset their password, logged out, etc.

This change requires the addition of a new `remember_token` column to your `users` (or equivalent) database table. After this change, a fresh token will be assigned to the user each time they login to your application. The token will also be refreshed when the user logs out of the application. The implications of this change are: if a "remember me" cookie is hijacked, simply logging out of the application will invalidate the cookie.

### Upgrade Path

First, add a new, nullable `remember_token` of VARCHAR(100), TEXT, or equivalent to your `users` table.

Next, if you are using the Eloquent authentication driver, update your `User` class with the following three methods:

    public function getRememberToken()
    {
        return $this->remember_token;
    }

    public function setRememberToken($value)
    {
        $this->remember_token = $value;
    }

    public function getRememberTokenName()
    {
        return 'remember_token';
    }

> **Note:** All existing "remember me" sessions will be invalidated by this change, so all users will be forced to re-authenticate with your application.

### Package Maintainers

Two new methods were added to the `Illuminate\Auth\UserProviderInterface` interface. Sample implementations may be found in the default drivers:

    public function retrieveByToken($identifier, $token);

    public function updateRememberToken(UserInterface $user, $token);

The `Illuminate\Auth\UserInterface` also received the three new methods described in the "Upgrade Path".

<a name="upgrade-4.1"></a>
## Upgrading To 4.1 From 4.0

### Upgrading Your Composer Dependency

To upgrade your application to Laravel 4.1, change your `laravel/framework` version to `4.1.*` in your `composer.json` file.

### Replacing Files

Replace your `public/index.php` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/v4.1.0/public/index.php).

Replace your `artisan` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/v4.1.0/artisan).

### Adding Configuration Files & Options

Update your `aliases` and `providers` arrays in your `app/config/app.php` configuration file. The updated values for these arrays can be found [in this file](https://github.com/laravel/laravel/blob/v4.1.0/app/config/app.php). Be sure to add your custom and package service providers / aliases back to the arrays.

Add the new `app/config/remote.php` file [from the repository](https://github.com/laravel/laravel/blob/v4.1.0/app/config/remote.php).

Add the new `expire_on_close` configuration option to your `app/config/session.php` file. The default value should be `false`.

Add the new `failed` configuration section to your `app/config/queue.php` file. Here are the default values for the section:

    'failed' => [
        'database' => 'mysql', 'table' => 'failed_jobs',
    ],

**(Optional)** Update the `pagination` configuration option in your `app/config/view.php` file to `pagination::slider-3`.

### Controller Updates

If `app/controllers/BaseController.php` has a `use` statement at the top, change `use Illuminate\Routing\Controllers\Controller;` to `use Illuminate\Routing\Controller;`.

### Password Reminders Updates

Password reminders have been overhauled for greater flexibility. You may examine the new stub controller by running the `php artisan auth:reminders-controller` Artisan command. You may also browse the [updated documentation](/docs/4.1/security#password-reminders-and-reset) and update your application accordingly.

Update your `app/lang/en/reminders.php` language file to match [this updated file](https://github.com/laravel/laravel/blob/v4.1.0/app/lang/en/reminders.php).

### Environment Detection Updates

For security reasons, URL domains may no longer be used to detect your application environment. These values are easily spoofable and allow attackers to modify the environment for a request. You should convert your environment detection to use machine host names (`hostname` command on Mac, Linux, and Windows).

### Simpler Log Files

Laravel now generates a single log file: `app/storage/logs/laravel.log`. However, you may still configure this behavior in your `app/start/global.php` file.

### Removing Redirect Trailing Slash

In your `bootstrap/start.php` file, remove the call to `$app->redirectIfTrailingSlash()`. This method is no longer needed as this functionality is now handled by the `.htaccess` file included with the framework.

Next, replace your Apache `.htaccess` file with [this new one](https://github.com/laravel/laravel/blob/v4.1.0/public/.htaccess) that handles trailing slashes.

### Current Route Access

The current route is now accessed via `Route::current()` instead of `Route::getCurrentRoute()`.

### Composer Update

Once you have completed the changes above, you can run the `composer update` function to update your core application files! If you receive class load errors, try running the `update` command with the `--no-scripts` option enabled like so: `composer update --no-scripts`.

### Wildcard Event Listeners

The wildcard event listeners no longer append the event to your handler functions parameters. If you require finding the event that was fired you should use `Event::firing()`.
