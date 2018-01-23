# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.5](#laravel-5.5)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel's versioning scheme maintains the following convention: `paradigm.major.minor`. Major framework releases are released every six months (February and August), while minor releases may be released as often as every week. Minor releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `5.5.*`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

Paradigm shifting releases are separated by many years and represent fundamental shifts in the framework's architecture and conventions. Currently, there is no paradigm shifting release under development.

#### Why Doesn't Laravel Use Semantic Versioning?

On one hand, all optional components of Laravel (Cashier, Dusk, Valet, Socialite, etc.) **do** use semantic versioning. However, the Laravel framework itself does not. The reason for this is because semantic versioning is a "reductionist" way of determining if two pieces of code are compatible. Even when using semantic versioning, you still must install the upgraded package and run your automated test suite to know if anything is *actually* incompatible with your code base.

So, instead, the Laravel framework uses a versioning scheme that is more communicative of the actual scope of the release. Furthermore, since minor releases **never** contain intentional breaking changes, you should never receive a breaking change as long as your version constraints follow the `paradigm.major.*` convention.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.5, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

<a name="laravel-5.5"></a>
## Laravel 5.5 (LTS)

Laravel 5.5 continues the improvements made in Laravel 5.4 by adding package auto-detection, API resources / transformations, auto-registration of console commands, queued job chaining, queued job rate limiting, time based job attempts, renderable mailables, renderable and reportable exceptions, more consistent exception handling, database testing improvements, simpler custom validation rules, React front-end presets, `Route::view` and `Route::redirect` methods, "locks" for the Memcached and Redis cache drivers, on-demand notifications, headless Chrome support in Dusk, convenient Blade shortcuts, improved trusted proxy support, and more.

In addition, Laravel 5.5 coincides with the release of [Laravel Horizon](https://horizon.laravel.com), a beautiful new queue dashboard and configuration system for your Redis based Laravel queues.

> {tip} This documentation summarizes the most notable improvements to the framework; however, more thorough change logs are always available [on GitHub](https://github.com/laravel/framework/blob/5.5/CHANGELOG-5.5.md).

### Laravel Horizon

Horizon provides a beautiful dashboard and code-driven configuration for your Laravel powered Redis queues. Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures.

All of your worker configuration is stored in a single, simple configuration file, allowing your configuration to stay in source control where your entire team can collaborate.

For more information on Horizon, check out the [full Horizon documentation](/docs/{{version}}/horizon)

### Package Discovery

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/5) for this feature available on Laracasts.

In previous versions of Laravel, installing a package typically required several additional steps such as adding the service provider to your `app` configuration file and registering any relevant facades. However, beginning with Laravel 5.5, Laravel can automatically detect and register service providers and facades for you.

For example, you can experience this by installing the popular `barryvdh/laravel-debugbar` package into your Laravel application. Once the package is installed via Composer, the debug bar will be available to your application with no additional configuration:

    composer require barryvdh/laravel-debugbar

Package developers only need to add their service providers and facades to their package's `composer.json` file:

    "extra": {
        "laravel": {
            "providers": [
                "Laravel\\Tinker\\TinkerServiceProvider"
            ]
        }
    },

For more information on updating your packages to use service provider and facade discovery, check out the full documentation on [package development](/docs/{{version}}/packages).

### API Resources

When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. Laravel's resource classes allow you to expressively and easily transform your models and model collections into JSON.

A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` class:

    <?php

    namespace App\Http\Resources;

    use Illuminate\Http\Resources\Json\Resource;

    class UserResource extends Resource
    {
        /**
         * Transform the resource into an array.
         *
         * @param  \Illuminate\Http\Request
         * @return array
         */
        public function toArray($request)
        {
            return [
                'id' => $this->id,
                'name' => $this->name,
                'email' => $this->email,
                'created_at' => $this->created_at,
                'updated_at' => $this->updated_at,
            ];
        }
    }

Of course, this is only the most basic example of an API resource. Laravel also provides a variety of methods to help you when building your resources and resource collections. For more information, check out the [full documentation](/docs/{{version}}/eloquent-resources) on API resources.

### Console Command Auto-Registration

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/12) for this feature available on Laracasts.

When creating new console commands, you no longer are required to manually list them in the `$commands` property of your Console kernel. Instead, a new `load` method is called from the `commands` method of your kernel, which will scan the given directory for any console commands and register them automatically:

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');

        // ...
    }

### New Frontend Presets

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/4) for this feature available on Laracasts.

While the basic Vue scaffolding is still included in Laravel 5.5, several new frontend preset options are now available. In a fresh Laravel application, you can swap the Vue scaffolding for React scaffolding using the `preset` command:

    php artisan preset react

Or, you can remove the JavaScript and CSS framework scaffolding entirely using the `none` preset. This preset will leave your application with a plain Sass file and a few simple JavaScript utilities:

    php artisan preset none

> {note} These commands are only intended to be run on fresh Laravel installations. They should not be used on existing applications.

### Queued Job Chaining

Job chaining allows you to specify a list of queued jobs that should be run in sequence. If one job in the sequence fails, the rest of the jobs will not be run. To execute a queued job chain, you may use the `withChain` method on any of your dispatchable jobs:

    ProvisionServer::withChain([
        new InstallNginx,
        new InstallPhp
    ])->dispatch();

### Queued Job Rate Limiting

If your application interacts with Redis, you may now throttle your queued jobs by time or concurrency. This feature can be of assistance when your queued jobs are interacting with APIs that are also rate limited. For example, you may throttle a given type of job to only run 10 times every 60 seconds:

    Redis::throttle('key')->allow(10)->every(60)->then(function () {
        // Job logic...
    }, function () {
        // Could not obtain lock...

        return $this->release(10);
    });

> {tip} In the example above, the `key` may be any string that uniquely identifies the type of job you would like to rate limit. For example, you may wish to construct the key based on the class name of the job and the IDs of the Eloquent models it operates on.

Alternatively, you may specify the maximum number of workers that may simultaneously process a given job. This can be helpful when a queued job is modifying a resource that should only be modified by one job at a time. For example, we may limit jobs of a given type to only be processed by one worker at a time:

    Redis::funnel('key')->limit(1)->then(function () {
        // Job logic...
    }, function () {
        // Could not obtain lock...

        return $this->release(10);
    });

### Time Based Job Attempts

As an alternative to defining how many times a job may be attempted before it fails, you may now define a time at which the job should timeout. This allows a job to be attempted any number of times within a given time frame. To define the time at which a job should timeout, add a `retryUntil` method to your job class:

    /**
     * Determine the time at which the job should timeout.
     *
     * @return \DateTime
     */
    public function retryUntil()
    {
        return now()->addSeconds(5);
    }

> {tip} You may also define a `retryUntil` method on your queued event listeners.

### Validation Rule Objects

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/7) for this feature available on Laracasts.

Validation rule objects provide a new, compact way of adding custom validation rules to your application. In previous versions of Laravel, the `Validator::extend` method was used to add custom validation rules via Closures. However, this can grow cumbersome. In Laravel 5.5, a new `make:rule` Artisan command will generate a new validation rule in the `app/Rules` directory:

    php artisan make:rule ValidName

A rule object only has two methods: `passes` and `message`. The `passes` method receives the attribute value and name, and should return `true` or `false` depending on whether the attribute value is valid or not. The `message` method should return the validation error message that should be used when validation fails:

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;

    class ValidName implements Rule
    {
        /**
         * Determine if the validation rule passes.
         *
         * @param  string  $attribute
         * @param  mixed  $value
         * @return bool
         */
        public function passes($attribute, $value)
        {
            return strlen($value) === 6;
        }

        /**
         * Get the validation error message.
         *
         * @return string
         */
        public function message()
        {
            return 'The name must be six characters long.';
        }
    }

Once the rule has been defined, you may use it by passing an instance of the rule object with your other validation rules:

    use App\Rules\ValidName;

    $request->validate([
        'name' => ['required', new ValidName],
    ]);

### Trusted Proxy Integration

When running applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links.

To solve this, many Laravel users install the [Trusted Proxies](https://github.com/fideloper/TrustedProxy) package by Chris Fidao. Since this is such a common use case, Chris' package now ships with Laravel 5.5 by default.

A new `App\Http\Middleware\TrustProxies` middleware is included in the default Laravel 5.5 application. This middleware allows you to quickly customize the proxies that should be trusted by your application:

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Http\Request;
    use Fideloper\Proxy\TrustProxies as Middleware;

    class TrustProxies extends Middleware
    {
        /**
         * The trusted proxies for this application.
         *
         * @var array
         */
        protected $proxies;

        /**
         * The current proxy header mappings.
         *
         * @var array
         */
        protected $headers = [
            Request::HEADER_FORWARDED => 'FORWARDED',
            Request::HEADER_X_FORWARDED_FOR => 'X_FORWARDED_FOR',
            Request::HEADER_X_FORWARDED_HOST => 'X_FORWARDED_HOST',
            Request::HEADER_X_FORWARDED_PORT => 'X_FORWARDED_PORT',
            Request::HEADER_X_FORWARDED_PROTO => 'X_FORWARDED_PROTO',
        ];
    }

### On-Demand Notifications

Sometimes you may need to send a notification to someone who is not stored as a "user" of your application. Using the new `Notification::route` method, you may specify ad-hoc notification routing information before sending the notification:

    Notification::route('mail', 'taylor@laravel.com')
                ->route('nexmo', '5555555555')
                ->send(new InvoicePaid($invoice));

### Renderable Mailables

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/6) for this feature available on Laracasts.

Mailables can now be returned directly from routes, allowing you to quickly preview your mailable's designs in the browser:

    Route::get('/mailable', function () {
        $invoice = App\Invoice::find(1);

        return new App\Mail\InvoicePaid($invoice);
    });

### Renderable & Reportable Exceptions

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/18) for this feature available on Laracasts.

In previous versions of Laravel, you may have had to resort to "type checking" in your exception handler in order to render a custom response for a given exception. For instance, you may have written code like this in your exception handler's `render` method:

    /**
     * Render an exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $exception
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $exception)
    {
        if ($exception instanceof SpecialException) {
            return response(...);
        }

        return parent::render($request, $exception);
    }

In Laravel 5.5, you may now define a `render` method directly on your exceptions. This allows you to place the custom response rendering logic directly on the exception, which helps avoid conditional logic accumulation in your exception handler. If you would like to also customize the reporting logic for the exception, you may define a `report` method on the class:

    <?php

    namespace App\Exceptions;

    use Exception;

    class SpecialException extends Exception
    {
        /**
         * Report the exception.
         *
         * @return void
         */
        public function report()
        {
            //
        }

        /**
         * Report the exception.
         *
         * @param  \Illuminate\Http\Request
         * @return void
         */
        public function render($request)
        {
            return response(...);
        }
    }

### Request Validation

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/2) for this feature available on Laracasts.

The `Illuminate\Http\Request` object now provides a `validate` method, allowing you to quickly validate an incoming request from a route Closure or controller:

    use Illuminate\Http\Request;

    Route::get('/comment', function (Request $request) {
        $request->validate([
            'title' => 'required|string',
            'body' => 'required|string',
        ]);

        // ...
    });

### Consistent Exception Handling

Validation exception handling is now consistent throughout the framework. Previously, there were multiple locations in the framework that required customization to change the default format for JSON validation error responses. In addition, the default format for JSON validation responses in Laravel 5.5 now adheres to the following convention:

    {
        "message": "The given data was invalid.",
        "errors": {
            "field-1": [
                "Error 1",
                "Error 2"
            ],
            "field-2": [
                "Error 1",
                "Error 2"
            ],
        }
    }

All JSON validation error formatting can be controlled by defining a single method on your `App\Exceptions\Handler` class. For example, the following customization will format JSON validation responses using the Laravel 5.4 convention.

    use Illuminate\Validation\ValidationException;

    /**
     * Convert a validation exception into a JSON response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Illuminate\Validation\ValidationException  $exception
     * @return \Illuminate\Http\JsonResponse
     */
    protected function invalidJson($request, ValidationException $exception)
    {
        return response()->json($exception->errors(), $exception->status);
    }

### Cache Locks

The Redis and Memcached cache drivers now have support for obtaining and releasing atomic "locks". This provides a simple method of obtaining arbitrary locks without worrying about race conditions. For example, before performing a task, you may wish to obtain a lock so no other processes attempt the same task that is already in progress:

    if (Cache::lock('lock-name', 60)->get()) {
        // Lock obtained for 60 seconds, continue processing...

        Cache::lock('lock-name')->release();
    } else {
        // Lock was not able to be obtained...
    }

Or, you may pass a Closure to the `get` method. The Closure will only be executed if the lock can be obtained and the lock will automatically be released after the Closure is executed:

    Cache::lock('lock-name', 60)->get(function () {
        // Lock obtained for 60 seconds...
    });

In addition, you may "block" until the lock becomes available:

    if (Cache::lock('lock-name', 60)->block(10)) {
        // Wait for a maximum of 10 seconds for the lock to become available...
    }

### Blade Improvements

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/10) for this feature available on Laracasts.

Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade now provides a `Blade::if` method which allows you to quickly define custom conditional directives using Closures. For example, let's define a custom conditional that checks the current application environment. We may do this in the `boot` method of our `AppServiceProvider`:

    use Illuminate\Support\Facades\Blade;

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::if('env', function ($environment) {
            return app()->environment($environment);
        });
    }

Once the custom conditional has been defined, we can easily use it on our templates:

    @env('local')
        // The application is in the local environment...
    @else
        // The application is not in the local environment...
    @endenv

In addition to the ability to easily define custom Blade conditional directives, new shortcuts have been added to quickly check the authentication status of the current user:

    @auth
        // The user is authenticated...
    @endauth

    @guest
        // The user is not authenticated...
    @endguest

### New Routing Methods

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-5/episodes/16) for this feature available on Laracasts.

If you are defining a route that redirects to another URI, you may now use the `Route::redirect` method. This method provides a convenient shortcut so that you do not have to define a full route or controller for performing a simple redirect:

    Route::redirect('/here', '/there', 301);

If your route only needs to return a view, you may now use the `Route::view` method. Like the `redirect` method, this method provides a simple shortcut so that you do not have to define a full route or controller. The `view` method accepts a URI as its first argument and a view name as its second argument. In addition, you may provide an array of data to pass to the view as an optional third argument:

    Route::view('/welcome', 'welcome');

    Route::view('/welcome', 'welcome', ['name' => 'Taylor']);

### "Sticky" Database Connections

#### The `sticky` Option

When configuring read / write database connections, a new `sticky` configuration option is available:

    'mysql' => [
        'read' => [
            'host' => '192.168.1.1',
        ],
        'write' => [
            'host' => '196.168.1.2'
        ],
        'sticky'    => true,
        'driver'    => 'mysql',
        'database'  => 'database',
        'username'  => 'root',
        'password'  => '',
        'charset' => 'utf8mb4',
        'collation' => 'utf8mb4_unicode_ci',
        'prefix'    => '',
    ],

The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application.
