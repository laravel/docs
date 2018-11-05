# Upgrade Guide

- [Upgrading To 5.7.0 From 5.6](#upgrade-5.7.0)

<a name="upgrade-5.7.0"></a>
## Upgrading To 5.7.0 From 5.6

#### Estimated Upgrade Time: 10 - 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.7.*` in your `composer.json` file.

If you are using Laravel Passport, you should update your `laravel/passport` dependency to `^7.0` in your `composer.json` file.

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

### Artisan

#### Scheduled Job Connection & Queues

**Likelihood Of Impact: Low**

The `$schedule->job` method now respects the `queue` and `connection` properties on the job class if a connection / job is not explicitly passed into the `job` method.

Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/25216).

### Assets

#### Asset Directory Flattened

**Likelihood Of Impact: None**

For new Laravel 5.7 applications, the assets directory that contains the scripts and styles has been flattened into the `resources` directory. This **will not** affect existing applications and does not require changes to your existing applications.

However, if you wish to make this change, you should move all files from the `resources/assets/*` directory up one level:

- From `resources/assets/js/*` to `resources/js/*`
- From `resources/assets/sass/*` to `resources/sass/*`

Then, update any reference to the old directories in your `webpack.mix.js` file:

    mix.js('resources/js/app.js', 'public/js')
       .sass('resources/sass/app.scss', 'public/css');

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

### Authorization

#### The `Gate` Contract

**Likelihood Of Impact: Very Low**

The `raw` method was changed from `protected` to `public` visibility. In addition, it [was added to the `Illuminate\Contracts\Auth\Access\Gate` contract](https://github.com/laravel/framework/pull/25143):

    /**
     * Get the raw result from the authorization callback.
     *
     * @param  string  $ability
     * @param  array|mixed  $arguments
     * @return mixed
     */
    public function raw($ability, $arguments = []);

If you are implementing this interface, you should add this method to your implementation.

#### The `Login` Event

**Likelihood Of Impact: Very Low**

The `__construct` method of `Illuminate\Auth\Events\Login` event has a new `$guard` argument:

    /**
     * Create a new event instance.
     *
     * @param  string  $guard
     * @param  \Illuminate\Contracts\Auth\Authenticatable  $user
     * @param  bool  $remember
     * @return void
     */
    public function __construct($guard, $user, $remember)

If you are dispatching this event manually within your application, you'll need to pass this new argument into the event's constructor. The following example passes the default framework guard to the Login event:

    use Illuminate\Auth\Events\Login;

    event(new Login(config('auth.defaults.guard'), $user, $remember))

### Blade

#### The `or` Operator

**Likelihood Of Impact: High**

The Blade "or" operator has been removed in favor of PHP's built-in `??` "null coalesce" operator, which has the same purpose and functionality:

    // Laravel 5.6...
    {{ $foo or 'default' }}

    // Laravel 5.7...
    {{ $foo ?? 'default' }}

### Cache

**Likelihood Of Impact: Very High**

A new `data` directory has been added to `storage/framework/cache`. You should create this directory in your own application:

    mkdir -p storage/framework/cache/data

Then, add a [.gitignore](https://github.com/laravel/laravel/blob/76369205c8715a4a8d0d73061aa042a74fd402dc/storage/framework/cache/data/.gitignore) file to the newly created `data` directory:

    cp storage/framework/cache/.gitignore storage/framework/cache/data/.gitignore

Finally, ensure that the [storage/framework/cache/.gitignore](https://github.com/laravel/laravel/blob/76369205c8715a4a8d0d73061aa042a74fd402dc/storage/framework/cache/.gitignore) file is updated as follows:

    *
    !data/
    !.gitignore

### Carbon

**Likelihood Of Impact: Very Low**

Carbon "macros" are now handled by the Carbon library directly instead of Laravel's extension of the library. We do not expect this to break your code; however, [please make us aware of any problems you encounter related to this change](https://github.com/laravel/framework/pull/23938).

### Collections

#### The `split` Method

**Likelihood Of Impact: Low**

The `split` method [has been updated to always return the requested number of "groups"](https://github.com/laravel/framework/pull/24088), unless the total number of items in the original collection is less than the requested collection count. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution.

### Cookie

#### `Factory` Contract Method Signature

**Likelihood Of Impact: Very Low**

The signatures of the `make` and `forever` methods of the `Illuminate\Contracts\Cookie\Factory` interface [have been changed](https://github.com/laravel/framework/pull/23200). If you are implementing this interface, you should update these methods in your implementation.

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

#### The `ConnectionInterface` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Database\ConnectionInterface` contract's `select` and `selectOne` method signatures have been updated to accommodate the new `$useReadPdo` argument:

    /**
     * Run a select statement and return a single result.
     *
     * @param  string  $query
     * @param  array   $bindings
     * @param  bool  $useReadPdo
     * @return mixed
     */
    public function selectOne($query, $bindings = [], $useReadPdo = true);

    /**
     * Run a select statement against the database.
     *
     * @param  string  $query
     * @param  array   $bindings
     * @param  bool  $useReadPdo
     * @return array
     */
    public function select($query, $bindings = [], $useReadPdo = true);

In addition, the `cursor` method was added to the contract:

    /**
     * Run a select statement against the database and returns a generator.
     *
     * @param  string  $query
     * @param  array  $bindings
     * @param  bool  $useReadPdo
     * @return \Generator
     */
    public function cursor($query, $bindings = [], $useReadPdo = true);

If you are implementing this interface, you should add this method to your implementation.

#### Migration Command Output

**Likelihood Of Impact: Very Low**

The core migration commands have been [updated to set the output instance on the migrator class](https://github.com/laravel/framework/pull/24811). If you were overriding or extending the migration commands, you should remove references to `$this->migrator->getNotes()` and use `$this->migrator->setOutput($this->output)` instead.

#### SQL Server Driver Priority

**Likelihood Of Impact: Low**

Prior to Laravel 5.7, the `PDO_DBLIB` driver was used as the default SQL Server PDO driver. This driver is considered deprecated by Microsoft. As of Laravel 5.7, `PDO_SQLSRV` will be used as the default driver if it is available. Alternatively, you may choose to use the `PDO_ODBC` driver:

    'sqlsrv' => [
        // ...
        'odbc' => true,
        'odbc_datasource_name' => 'your-odbc-dsn',
    ],

If neither of these drivers are available, Laravel will use the `PDO_DBLIB` driver.

#### SQLite Foreign Keys

**Likelihood Of Impact: Medium**

SQLite does not support dropping foreign keys. For that reason, using the `dropForeign` method on a table now throws an exception. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution.

If you run your migrations on multiple types of databases, consider using `DB::getDriverName()` in your migrations to skip unsupported foreign key methods for SQLite.

### Debug

#### Dumper Classes

**Likelihood Of Impact: Very Low**

The `Illuminate\Support\Debug\Dumper` and `Illuminate\Support\Debug\HtmlDumper` classes have been removed in favor of using Symfony's native variable dumpers: `Symfony\Component\VarDumper\VarDumper` and `Symfony\Component\VarDumper\Dumper\HtmlDumper`.

### Eloquent

#### The `latest` / `oldest` Methods

**Likelihood Of Impact: Low**

The Eloquent query builder's `latest` and `oldest` methods have been updated to respect custom "created at" timestamp columns that may be specified on your Eloquent models. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution.

#### The `wasChanged` Method

**Likelihood Of Impact: Very Low**

An Eloquent model's changes are now available to the `wasChanged` method **before** firing the `updated` model event. Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/25026).

#### PostgreSQL Special Float Values

**Likelihood Of Impact: Low**

PostgreSQL supports the float values `Infinity`, `-Infinity` and `NaN`. Prior to Laravel 5.7, these were cast to `0` when the Eloquent casting type for the column was `float`, `double`, or `real`.

As of Laravel 5.7, these values will be cast to the corresponding PHP constants `INF`, `-INF`, and `NAN`.

### Email Verification

**Likelihood Of Impact: Optional**

If you choose to use Laravel's new [email verification services](/docs/{{version}}/verification), you will need to add additional scaffolding to your application. First, add the `VerificationController` to your application: [App\Http\Controllers\Auth\VerificationController](https://github.com/laravel/laravel/blob/master/app/Http/Controllers/Auth/VerificationController.php).

You will also need to modify your `App\User` model to implement the `MustVerifyEmail` contract:

    <?php

    namespace App;

    use Illuminate\Notifications\Notifiable;
    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

In order to use the `verified` middleware so that only verified users may access a given route, you will need to update the `$routeMiddleware` property of your `app/Http/Kernel.php` file to include the new middleware:

    // Within App\Http\Kernel Class...

    protected $routeMiddleware = [
        'auth' => \Illuminate\Auth\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];

You will also need the verification view stub. This view should be placed at `resources/views/auth/verify.blade.php`. You may obtain the view's contents [on GitHub](https://github.com/laravel/framework/blob/5.7/src/Illuminate/Auth/Console/stubs/make/views/auth/verify.stub).

Next, your user table must contain an `email_verified_at` column to store the date and time that the email address was verified:

    $table->timestamp('email_verified_at')->nullable();

In order to send the email when a user is registered, you should register following events and listeners in your [App\Providers\EventServiceProvider](https://github.com/laravel/laravel/blob/master/app/Providers/EventServiceProvider.php) class:

    use Illuminate\Auth\Events\Registered;
    use Illuminate\Auth\Listeners\SendEmailVerificationNotification;

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        Registered::class => [
            SendEmailVerificationNotification::class,
        ],
    ];

Finally, when calling the `Auth::routes` method, you should pass the `verify` option to the method:

    Auth::routes(['verify' => true]);

### Filesystem

#### `Filesystem` Contract Methods

**Likelihood Of Impact: Low**

The `readStream` and `writeStream` methods [have been added to the `Illuminate\Contracts\Filesystem\Filesystem` contract](https://github.com/laravel/framework/pull/23755). If you are implementing this interface, you should add these methods to your implementation.

### Hashing

#### `Hash::check` Method

**Likelihood Of Impact: None**

The `check` method now **optionally** checks if the algorithm of the hash matches the configured algorithm.

### Mail

#### Mailable Dynamic Variable Casing

**Likelihood Of Impact: Medium**

Variables that are dynamically passed to mailable views [are now automatically "camel cased"](https://github.com/laravel/framework/pull/24232), which makes mailable dynamic variable behavior consistent with dynamic view variables. Dynamic mailable variables are not a documented Laravel feature, so likelihood of impact to your application is low.

#### Template Theme

**Likelihood Of Impact: Medium**

If you have customized the default theme styles used for Markdown mailable templates, you will need to re-publish and make your customizations again. The button color classes have been renamed from 'blue', 'green', and 'red' to 'primary', 'success', and 'error'.

### Queue

#### `QUEUE_DRIVER` Environment Variable

**Likelihood Of Impact: Very Low**

The `QUEUE_DRIVER` environment variable has been renamed to `QUEUE_CONNECTION`. This should not affect existing applications that you are upgrading unless you intentionally modify your `config/queue.php` configuration file to match Laravel 5.7's.

### Routing

#### The `Route::redirect` Method

**Likelihood Of Impact: High**

The `Route::redirect` method now returns a `302` HTTP status code redirect. The `permanentRedirect` method has been added to allow `301` redirects.

    // Return a 302 redirect...
    Route::redirect('/foo', '/bar');

    // Return a 301 redirect...
    Route::redirect('/foo', '/bar', 301);

    // Return a 301 redirect...
    Route::permanentRedirect('/foo', '/bar');

#### The `addRoute` Method

**Likelihood Of Impact: Low**

The `addRoute` method of the `Illuminate\Routing\Router` class has been changed from `protected` to `public`.

### Validation

#### Nested Validation Data

**Likelihood Of Impact: Medium**

In previous versions of Laravel, the `validate` method did not return the correct data for nested validation rules. This has been corrected in Laravel 5.7:

    $data = Validator::make([
        'person' => [
            'name' => 'Taylor',
            'job' => 'Developer'
        ]
    ], ['person.name' => 'required'])->validate();

    dump($data);

    // Prior Behavior...
    ['person' => ['name' => 'Taylor', 'job' => 'Developer']]

    // New Behavior...
    ['person' => ['name' => 'Taylor']]

#### The `Validator` Contract

**Likelihood Of Impact: Very Low**

The `validate` method [was added to the `Illuminate\Contracts\Validation\Validator` contract](https://github.com/laravel/framework/pull/25128):

    /**
     * Run the validator's rules against its data.
     *
     * @return array
     */
    public function validate();

If you are implementing this interface, you should add this method to your implementation.

### Testing

**Likelihood of Impact: Medium**

Laravel 5.7 introduces improved testing tools for Artisan commands. By default, Artisan command output is now mocked. If you are relying on the `artisan` method to run commands as part of your test, you should use `Artisan::call` or define `public $mockConsoleOutput = false` as a property in your test class.

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.6...master) and choose which updates are important to you.
