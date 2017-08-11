# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.5](#laravel-5.5)
- [Laravel 5.4.22](#laravel-5.4.22)
- [Laravel 5.4](#laravel-5.4)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel's versioning scheme maintains the following convention: `paradigm.minor.patch`. Minor framework releases are released every six months (January and July), while patch releases may be released as often as every week. Patch releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `5.4.*`, since minor releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new minor release in one day or less.

Paradigm shifting releases are separated by many years and represent fundamental shifts in the framework's architecture and conventions. Currently, there is no paradigm shifting release under development.

#### Why Doesn't Laravel Use Semantic Versioning?

On one hand, all optional components of Laravel (Cashier, Dusk, Valet, Socialite, etc.) **do** use semantic versioning. However, the Laravel framework itself does not. The reason for this is because semantic versioning is a "reductionist" way of determining if two pieces of code are compatible. Even when using semantic versioning, you still must install the upgraded package and run your automated test suite to know if anything is *actually* incompatible with your code base.

So, instead, the Laravel framework uses a versioning scheme that is more communicative of the actual scope of the release. Furthermore, since patch releases **never** contain intentional breaking changes, you should never receive a breaking change as long as your version constraints follow the `paradigm.minor.*` convention.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.1, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

<a name="laravel-5.5"></a>
## Laravel 5.5

Laravel 5.5 continues the improvements made in Laravel 5.4 by adding package auto-detection, auto-registration of console commands, queued job chaining, renderable mailables, renderable and reportable exceptions, more consistent exception handling, database testing improvements, simpler custom validation rules, React front-end presets, `Route::view` and `Route::redirect` methods, "locks" for the Memcached and Redis cache drivers, on-demand notifications, headless Chrome support in Dusk, convenient Blade shortcuts, improved trusted proxy support, and more.

In addition, Laravel 5.5 coincides with the release of [Laravel Horizon](http://horizon.laravel.com), a beautiful new queue dashboard and configuration system for your Redis based Laravel queues.

> {tip} This documentation summarizes the most notable improvements to the framework; however, more thorough change logs are always available [on GitHub](https://github.com/laravel/framework/blob/5.5/CHANGELOG-5.5.md).

### Laravel Horizon

Horizon provides a beautiful dashboard and code-driven configuration for your Laravel powered Redis queues. Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures.

All of your worker configuration is stored in a single, simple configuration file, allowing your configuration to stay in source control where your entire team can collaborate.

For more information on Horizon, check out the [full Horizon documentation](/docs/{{version}}/horizon)

### Package Discovery

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

### Console Command Auto-Registration

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

### Validation Rule Objects

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

Once the rule has been defined, you may use it by simply passing an instance of the rule object with your other validation rules:

    use App\Rules\ValidName;

    $this->validate($request, [
        'name' => ['required', new ValidName],
    ]);

### Trusted Proxy Integration

When running applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links.

To solve this, many Laravel users install the [Trusted Proxies](https://github.com/fideloper/TrustedProxy) package by Chris Fidao. Since this is such a common use case, Chris' package now ships with Laravel 5.5 by default.

A new `App\Http\Middleware\TrustProxies` middleware is included in the default Laravel 5.5 application and allows you to quickly customize the proxies that should be trusted by your application:

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


### Renderable Mailables

### Renderable & Reportable Exceptions

### Consistent Exception Handling

### Cache Locks

### Blade Improvements

### New Routing Methods

<a name="laravel-5.4.22"></a>
## Laravel 5.4.22

Laravel 5.4.22 patches a security vulnerability in the Laravel 5.4 release series that allows phishing attempts on users of the application. Using the password reset system, malicious users can attempt to trick your users into entering their login credentials into a separate application that they control. Since the password reset notification uses the host of the incoming request to build the password reset URL, the host of the password reset URL may be spoofed. If users do not notice that they are not on their intended application's domain, they may accidentally enter their login credentials into a malicious application.

In Laravel 5.1 applications, the password reset notification is maintained by the developer, so this vulnerability may or may not be present. You should verify that your application generates an absolute URL for password reset links:

    {{ url('http://example.com/password/reset/'.$token) }}

<a name="laravel-5.4"></a>
## Laravel 5.4

Laravel 5.4 continues the improvements made in Laravel 5.3 by adding support for [Markdown based emails and notifications](/docs/5.4/mail#markdown-mailables), the [Laravel Dusk](/docs/5.4/dusk) browser automation and testing framework, Laravel Mix, Blade "components" and "slots", route model binding on broadcast channels, higher order messages for Collections, object-based Eloquent events, job-level "retry" and "timeout" settings, "realtime" facades, improved support for Redis Cluster, custom pivot table models, middleware for request input trimming and cleaning, and more. In addition, the entire codebase of the framework was reviewed and refactored for general cleanliness.

> {tip} This documentation summarizes the most notable improvements to the framework; however, more thorough change logs are always available [on GitHub](https://github.com/laravel/framework/blob/5.4/CHANGELOG-5.4.md).

### Markdown Mail & Notifications

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/7) for this feature available on Laracasts.

Markdown mailable messages allow you to take advantage of the pre-built templates and components of mail notifications in your mailables. Since the messages are written in Markdown, Laravel is able to render beautiful, responsive HTML templates for the messages while also automatically generating a plain-text counterpart. For example, a Markdown email might look something like the following:

    @component('mail::message')
    # Order Shipped

    Your order has been shipped!

    @component('mail::button', ['url' => $url])
    View Order
    @endcomponent

    Next Steps:

    - Track Your Order On Our Website
    - Pre-Sign For Delivery

    Thanks,<br>
    {{ config('app.name') }}
    @endcomponent

Using this simple Markdown template, Laravel is able to generate a responsive HTML email and plain-text counterpart:

<img src="https://laravel.com/assets/img/examples/markdown.png" width="551" height="596">

To read more about Markdown mail and notifications, check out the full [mail](/docs/5.4/mail) and [notification](/docs/5.4/notifications) documentation.

> {tip} You may export all of the Markdown mail components to your own application for customization. To export the components, use the `vendor:publish` Artisan command to publish the `laravel-mail` asset tag.

### Laravel Dusk

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/9) for this feature available on Laracasts.

Laravel Dusk provides an expressive, easy-to-use browser automation and testing API. By default, Dusk does not require you to install JDK or Selenium on your machine. Instead, Dusk uses a standalone [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) installation. However, you are free to utilize any other Selenium compatible driver you wish.

Since Dusk operates using a real browser, you are able to easily test and interact with your applications that heavily use JavaScript:

    /**
     * A basic browser test example.
     *
     * @return void
     */
    public function testBasicExample()
    {
        $user = factory(User::class)->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function ($browser) use ($user) {
            $browser->loginAs($user)
                    ->visit('/home')
                    ->press('Create Playlist')
                    ->whenAvailable('.playlist-modal', function ($modal) {
                        $modal->type('name', 'My Playlist')
                              ->press('Create');
                    });

            $browser->waitForText('Playlist Created');
        });
    }

For more information on Dusk, consult the full [Dusk documentation](/docs/5.4/dusk).

### Laravel Mix

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/3) for this feature available on Laracasts.

Laravel Mix is the spiritual successor of Laravel Elixir, and its entirely based on Webpack instead of Gulp. Laravel Mix provides a fluent API for defining Webpack build steps for your Laravel application using several common CSS and JavaScript pre-processors. Through simple method chaining, you can fluently define your asset pipeline. For example:

    mix.js('resources/assets/js/app.js', 'public/js')
       .sass('resources/assets/sass/app.scss', 'public/css');

### Blade Components & Slots

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/6) for this feature available on Laracasts.

Blade components and slots provide similar benefits to sections and layouts; however, some may find the mental model of components and slots easier to understand. First, let's imagine a reusable "alert" component we would like to reuse throughout our application:

    <!-- /resources/views/alert.blade.php -->

    <div class="alert alert-danger">
        {{ $slot }}
    </div>

The `{{ $slot }}` variable will contain the content we wish to inject into the component. Now, to construct this component, we can use the `@component` Blade directive:

    @component('alert')
        <strong>Whoops!</strong> Something went wrong!
    @endcomponent

Named slots allow you to provide multiple slots into a single component:

    <!-- /resources/views/alert.blade.php -->

    <div class="alert alert-danger">
        <div class="alert-title">{{ $title }}</div>

        {{ $slot }}
    </div>

Named slots may be injected using the `@slot` directive. Any content is not within a `@slot` directive will be passed to the component in the `$slot` variable:

    @component('alert')
        @slot('title')
            Forbidden
        @endslot

        You are not allowed to access this resource!
    @endcomponent

To read more about components and slots, consult the full [Blade documentation](/docs/5.4/blade).

### Broadcast Model Binding

Just like HTTP routes, channel routes may now take advantage of implicit and explicit [route model binding](/docs/5.4/routing#route-model-binding). For example, instead of receiving the string or numeric order ID, you may request an actual `Order` model instance:

    use App\Order;

    Broadcast::channel('order.{order}', function ($user, Order $order) {
        return $user->id === $order->user_id;
    });

To read more about broadcast model binding, consult the full [event broadcasting](/docs/5.4/broadcasting) documentation.

### Collection Higher Order Messages

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/2) for this feature available on Laracasts.

Collections now provide support for "higher order messages", which are short-cuts for performing common actions on collections. The collection methods that provide higher order messages are: `contains`, `each`, `every`, `filter`, `first`, `map`, `partition`, `reject`, `sortBy`, `sortByDesc`, and `sum`.

Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection:

    $users = User::where('votes', '>', 500)->get();

    $users->each->markAsVip();

Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users:

    $users = User::where('group', 'Development')->get();

    return $users->sum->votes;

### Object Based Eloquent Events

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/10) for this feature available on Laracasts.

Eloquent event handlers may now be mapped to event objects. This provides a more intuitive way of handling Eloquent events and makes it easier to test the events. To get started, define an `$events` property on your Eloquent model that maps various points of the Eloquent model's lifecycle to your own [event classes](/docs/5.4/events):

    <?php

    namespace App;

    use App\Events\UserSaved;
    use App\Events\UserDeleted;
    use Illuminate\Notifications\Notifiable;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable
    {
        use Notifiable;

        /**
         * The event map for the model.
         *
         * @var array
         */
        protected $events = [
            'saved' => UserSaved::class,
            'deleted' => UserDeleted::class,
        ];
    }

### Job Level Retry & Timeout

Previously, queue job "retry" and "timeout" settings could only be configured globally for all jobs on the command line. However, in Laravel 5.4, these settings may be configured on a per-job basis by defining them directly on the job class:

    <?php

    namespace App\Jobs;

    class ProcessPodcast implements ShouldQueue
    {
        /**
         * The number of times the job may be attempted.
         *
         * @var int
         */
        public $tries = 5;

        /**
         * The number of seconds the job can run before timing out.
         *
         * @var int
         */
        public $timeout = 120;
    }

For more information about these settings, consult the full [queue documentation](/docs/5.4/queues).

### Request Sanitization Middleware

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/1) for this feature available on Laracasts.

Laravel 5.4 includes two new middleware in the default middleware stack: `TrimStrings` and `ConvertEmptyStringsToNull`:

    /**
     * The application's global HTTP middleware stack.
     *
     * These middleware are run during every request to your application.
     *
     * @var array
     */
    protected $middleware = [
        \Illuminate\Foundation\Http\Middleware\CheckForMaintenanceMode::class,
        \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
        \App\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ];

These middleware will automatically trim request input values and convert any empty strings to `null`. This helps you normalize the input for every request entering into your application and not have to worry about continually calling the `trim` function in every route and controller.

### "Realtime" Facades

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-4/episodes/8) for this feature available on Laracasts.

Previously, only Laravel's own built-in services exposed [facades](/docs/5.4/facades), which provide quick, terse access to their methods via the service container. However, in Laravel 5.4, you may easily convert any of your application's classes into a facade in realtime simply by prefixing the imported class name with `Facades`. For example, imagine your application contains a class like the following:

    <?php

    namespace App\Services;

    class PaymentGateway
    {
        protected $tax;

        /**
         * Create a new payment gateway instance.
         *
         * @param  TaxCalculator  $tax
         * @return void
         */
        public function __construct(TaxCalculator $tax)
        {
            $this->tax = $tax;
        }

        /**
         * Pay the given amount.
         *
         * @param  int  $amount
         * @return void
         */
        public function pay($amount)
        {
            // Pay an amount...
        }
    }

You may easily use this class as a facade like so:

    use Facades\ {
        App\Services\PaymentGateway
    };

    Route::get('/pay/{amount}', function ($amount) {
        PaymentGateway::pay($amount);
    });

Of course, if you leverage a realtime facade in this way, you may easily write a test for the interaction using Laravel's [facade mocking capabilities](/docs/5.4/mocking):

    PaymentGateway::shouldReceive('pay')->with('100');

### Custom Pivot Table Models

In Laravel 5.3, all "pivot" table models for `belongsToMany` relationships used the same built-in `Pivot` model instance. In Laravel 5.4, you may define custom models for your pivot tables. If you would like to define a custom model to represent the intermediate table of your relationship, use the `using` method when defining the relationship:

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Role extends Model
    {
        /**
         * The users that belong to the role.
         */
        public function users()
        {
            return $this->belongsToMany('App\User')->using('App\UserRole');
        }
    }

### Improved Redis Cluster Support

Previously, it was not possible to define Redis connections to single hosts and to clusters in the same application. In Laravel 5.4, you may now define Redis connections to multiple single hosts and multiple clusters within the same application. For more information on Redis in Laravel, please consult the full [Redis documentation](/docs/5.4/redis).

<a name="utf8mb4"></a>
### Migration Default String Length

Laravel 5.4 uses the `utf8mb4` character set by default, which includes support for storing "emojis" in the database. If you are upgrading your application from Laravel 5.3, you are not required to switch to this character set.

If you choose to switch to this character set manually and are running a version of MySQL older than the 5.7.7 release, you may need to manually configure the default string length generated by migrations. You may configure this by calling the `Schema::defaultStringLength` method within your `AppServiceProvider`:

    use Illuminate\Support\Facades\Schema;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Schema::defaultStringLength(191);
    }
