# Release Notes

- [Support Policy](#support-policy)
- [Laravel 5.4](#laravel-5.4)
- [Laravel 5.3](#laravel-5.3)
- [Laravel 5.2](#laravel-5.2)
- [Laravel 5.1.11](#laravel-5.1.11)
- [Laravel 5.1.4](#laravel-5.1.4)
- [Laravel 5.1](#laravel-5.1)
- [Laravel 5.0](#laravel-5.0)
- [Laravel 4.2](#laravel-4.2)
- [Laravel 4.1](#laravel-4.1)

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.1, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

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

<a name="laravel-5.3"></a>
## Laravel 5.3

Laravel 5.3 continues the improvements made in Laravel 5.2 by adding a driver based [notification system](/docs/5.3/notifications), robust realtime support via [Laravel Echo](/docs/5.3/broadcasting), painless OAuth2 servers via [Laravel Passport](/docs/5.3/passport), full-text model searching via [Laravel Scout](/docs/5.3/scout), Webpack support in Laravel Elixir, "mailable" objects, explicit separation of `web` and `api` routes, Closure based console commands, convenient helpers for storing uploaded files, support for POPO and single-action controllers, improved default frontend scaffolding, and more.

### Notifications

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/9) for this feature available on Laracasts.

Laravel Notifications provide a simple, expressive API for sending notifications across a variety of delivery channels such as email, Slack, SMS, and more. For example, you may define a notification that an invoice has been paid and deliver that notification via email and SMS. Then, you may send the notification using a single, simple method:

    $user->notify(new InvoicePaid($invoice));

There is already a wide variety of [community written drivers](http://laravel-notification-channels.com) for notifications, including support for iOS and Android notifications. To learn more about notifications, be sure to check out the [full notification documentation](/docs/5.3/notifications).

### WebSockets / Event Broadcasting

While event broadcasting existed in previous versions of Laravel, the Laravel 5.3 release greatly improves this feature of the framework by adding channel-level authentication for private and presence WebSocket channels:

    /*
     * Authenticate the channel subscription...
     */
    Broadcast::channel('orders.*', function ($user, $orderId) {
        return $user->placedOrder($orderId);
    });

Laravel Echo, a new JavaScript package installable via NPM, has also been released to provide a simple, beautiful API for subscribing to channels and listening for your server-side events in your client-side JavaScript application. Echo includes support for [Pusher](https://pusher.com) and [Socket.io](http://socket.io):

    Echo.channel('orders.' + orderId)
        .listen('ShippingStatusUpdated', (e) => {
            console.log(e.description);
        });

In addition to subscribing to traditional channels, Laravel Echo also makes it a breeze to subscribe to presence channels which provide information about who is listening on a given channel:

    Echo.join('chat.' + roomId)
        .here((users) => {
            //
        })
        .joining((user) => {
            console.log(user.name);
        })
        .leaving((user) => {
            console.log(user.name);
        });

To learn more about Echo and event broadcasting, check out the [full documentation](/docs/5.3/broadcasting).

### Laravel Passport (OAuth2 Server)

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/13) for this feature available on Laracasts.

Laravel 5.3 makes API authentication a breeze using [Laravel Passport](/docs/{{version}}/passport), which provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Alex Bilbie.

Passport makes it painless to issue access tokens via OAuth2 authorization codes. You may also allow your users to create "personal access tokens" via your web UI. To get you started quickly, Passport includes [Vue components](https://vuejs.org) that can serve as a starting point for your OAuth2 dashboard, allowing users to create clients, revoke access tokens, and more:

    <passport-clients></passport-clients>
    <passport-authorized-clients></passport-authorized-clients>
    <passport-personal-access-tokens></passport-personal-access-tokens>

If you do not want to use the Vue components, you are welcome to provide your own frontend dashboard for managing clients and access tokens. Passport exposes a simple JSON API that you may use with any JavaScript framework you choose.

Of course, Passport also makes it simple to define access token scopes that may be requested by application's consuming your API:

    Passport::tokensCan([
        'place-orders' => 'Place new orders',
        'check-status' => 'Check order status',
    ]);

In addition, Passport includes helpful middleware for verifying that an access token authenticated request contains the necessary token scopes:

    Route::get('/orders/{order}/status', function (Order $order) {
        // Access token has "check-status" scope...
    })->middleware('scope:check-status');

Lastly, Passport includes support for consuming your own API from your JavaScript application without worrying about passing access tokens. Passport achieves this through encrypted JWT cookies and synchronized CSRF tokens, allowing you to focus on what matters: your application. For more information on Passport, be sure to check out its [full documentation](/docs/5.3/passport).

### Search (Laravel Scout)

Laravel Scout provides a simple, driver based solution for adding full-text search to your [Eloquent models](/docs/5.3/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records. Currently, Scout ships with an [Algolia](https://www.algolia.com/) driver; however, writing custom drivers is simple and you are free to extend Scout with your own search implementations.

Making models searchable is as simple as adding a `Searchable` trait to the model:

    <?php

    namespace App;

    use Laravel\Scout\Searchable;
    use Illuminate\Database\Eloquent\Model;

    class Post extends Model
    {
        use Searchable;
    }

Once the trait has been added to your model, its information will be kept in sync with your search indexes by simply saving the model:

    $order = new Order;

    // ...

    $order->save();

Once your models have been indexed, its a breeze to perform full-text searches across all of your models. You may even paginate your search results:

    return Order::search('Star Trek')->get();

    return Order::search('Star Trek')->where('user_id', 1)->paginate();

Of course, Scout has many more features which are covered in the [full documentation](/docs/5.3/scout).

### Mailable Objects

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/6) for this feature available on Laracasts.

Laravel 5.3 ships with support for mailable objects. These objects allow you to represent your email messages as a simple objects instead of customizing mail messages within Closures. For example, you may define a simple mailable object for a "welcome" email:

    class WelcomeMessage extends Mailable
    {
        use Queueable, SerializesModels;

        /**
         * Build the message.
         *
         * @return $this
         */
        public function build()
        {
            return $this->view('emails.welcome');
        }
    }

Once the mailable object has been defined, you can send it to a user using a simple, expressive API. Mailable objects are great for discovering the intent of your messages while scanning your code:

    Mail::to($user)->send(new WelcomeMessage);

Of course, you may also mark mailable objects as "queueable" so that they will be sent in the background by your queue workers:

    class WelcomeMessage extends Mailable implements ShouldQueue
    {
        //
    }

For more information on mailable objects, be sure to check out the [mail documentation](/docs/5.3/mail).

### Storing Uploaded Files

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/12) for this feature available on Laracasts.

In web applications, one of the most common use-cases for storing files is storing user uploaded files such as profile pictures, photos, and documents. Laravel 5.3 makes it very easy to store uploaded files using the new `store` method on an uploaded file instance. Simply call the `store` method with the path at which you wish to store the uploaded file:

    /**
     * Update the avatar for the user.
     *
     * @param  Request  $request
     * @return Response
     */
    public function update(Request $request)
    {
        $path = $request->file('avatar')->store('avatars', 's3');

        return $path;
    }

For more information on storing uploaded files, check out the [full documentation](/docs/{{version}}/filesystem#file-uploads).


### Webpack & Laravel Elixir

Along with Laravel 5.3, Laravel Elixir 6.0 has been released with baked-in support for the Webpack and Rollup JavaScript module bundlers. By default, the Laravel 5.3 `gulpfile.js` file now uses Webpack to compile your JavaScript. The [full Laravel Elixir documentation](/docs/5.3/elixir) contains more information on both of these bundlers:

    elixir(mix => {
        mix.sass('app.scss')
           .webpack('app.js');
    });

### Frontend Structure

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/4) for this feature available on Laracasts.

Laravel 5.3 ships with a more modern frontend structure. This primarily affects the `make:auth` authentication scaffolding. Instead of loading frontend assets from a CDN, dependencies are specified in the default `package.json` file.

In addition, support for single file [Vue components](https://vuejs.org) is now included out of the box. A sample `Example.vue` component is included in the `resources/assets/js/components` directory. In addition, the new `resources/assets/js/app.js` file bootstraps and configures your JavaScript libraries and, if applicable, Vue components.

This structure provides more guidance on how to begin developing modern, robust JavaScript applications, without requiring your application to use any given JavaScript or CSS framework. For more information on getting started with modern Laravel frontend development, check out the new [introductory frontend documentation](/docs/5.3/frontend).

### Routes Files

By default, fresh Laravel 5.3 applications contain two HTTP route files in a new top-level `routes` directory. The `web` and `api` route files provide more explicit guidance in how to split the routes for your web interface and your API. The routes in the `api` route file are automatically assigned the `api` prefix by the `RouteServiceProvider`.

### Closure Console Commands

In addition to being defined as command classes, Artisan commands may now be defined as simple Closures in the `commands` method of your `app/Console/Kernel.php` file. In fresh Laravel 5.3 applications, the `commands` method loads a `routes/console.php` file which allows you to define your Console commands as route-like, Closure based entry points into your application:

    Artisan::command('build {project}', function ($project) {
        $this->info('Building project...');
    });

For more information on Closure commands, check out the [full Artisan documentation](/docs/5.3/artisan#closure-commands).

### The `$loop` Variable

> {video} There is a free [video tutorial](https://laracasts.com/series/whats-new-in-laravel-5-3/episodes/7) for this feature available on Laracasts.

When looping within a Blade template, a `$loop` variable will be available inside of your loop. This variable provides access to some useful bits of information such as the current loop index and whether this is the first or last iteration through the loop:

    @foreach ($users as $user)
        @if ($loop->first)
            This is the first iteration.
        @endif

        @if ($loop->last)
            This is the last iteration.
        @endif

        <p>This is user {{ $user->id }}</p>
    @endforeach

For more information, consult the [full Blade documentation](/docs/5.3/blade#the-loop-variable).

<a name="laravel-5.2"></a>
## Laravel 5.2

Laravel 5.2 continues the improvements made in Laravel 5.1 by adding multiple authentication driver support, implicit model binding, simplified Eloquent global scopes, opt-in authentication scaffolding, middleware groups, rate limiting middleware, array validation improvements, and more.

### Authentication Drivers / "Multi-Auth"

In previous versions of Laravel, only the default, session-based authentication driver was supported out of the box, and you could not have more than one authenticatable model instance per application.

However, in Laravel 5.2, you may define additional authentication drivers as well define multiple authenticatable models or user tables, and control their authentication process separately from each other. For example, if your application has one database table for "admin" users and one database table for "student" users, you may now use the `Auth` methods to authenticate against each of these tables separately.

### Authentication Scaffolding

Laravel already makes it easy to handle authentication on the back-end; however, Laravel 5.2 provides a convenient, lightning-fast way to scaffold the authentication views for your front-end. Simply execute the `make:auth` command on your terminal:

    php artisan make:auth

This command will generate plain, Bootstrap compatible views for user login, registration, and password reset. The command will also update your routes file with the appropriate routes.

> {note} This feature is only meant to be used on new applications, not during application upgrades.

### Implicit Model Binding

Implicit model binding makes it painless to inject relevant models directly into your routes and controllers. For example, assume you have a route defined like the following:

    use App\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

In Laravel 5.1, you would typically need to use the `Route::model` method to instruct Laravel to inject the `App\User` instance that matches the `{user}` parameter in your route definition. However, in Laravel 5.2, the framework will **automatically** inject this model based on the URI segment, allowing you to quickly gain access to the model instances you need.

Laravel will automatically inject the model when the route parameter segment (`{user}`) matches the route Closure or controller method's corresponding variable name (`$user`) and the variable is type-hinting an Eloquent model class.

### Middleware Groups

Middleware groups allow you to group several route middleware under a single, convenient key, allowing you to assign several middleware to a route at once. For example, this can be useful when building a web UI and an API within the same application. You may group the session and CSRF routes into a `web` group, and perhaps the rate limiter in the `api` group.

In fact, the default Laravel 5.2 application structure takes exactly this approach. For example, in the default `App\Http\Kernel.php` file you will find the following:

    /**
     * The application's route middleware groups.
     *
     * @var array
     */
    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            \App\Http\Middleware\VerifyCsrfToken::class,
        ],

        'api' => [
            'throttle:60,1',
        ],
    ];

Then, the `web` group may be assigned to routes like so:

    Route::group(['middleware' => ['web']], function () {
        //
    });

However, keep in mind the `web` middleware group is *already* applied to your routes by default since the `RouteServiceProvider` includes it in the default middleware group.

### Rate Limiting

A new rate limiter middleware is now included with the framework, allowing you to easily limit the number of requests that a given IP address can make to a route over a specified number of minutes. For example, to limit a route to 60 requests every minute from a single IP address, you may do the following:

    Route::get('/api/users', ['middleware' => 'throttle:60,1', function () {
        //
    }]);

### Array Validation

Validating array form input fields is much easier in Laravel 5.2. For example, to validate that each e-mail in a given array input field is unique, you may do the following:

    $validator = Validator::make($request->all(), [
        'person.*.email' => 'email|unique:users'
    ]);

Likewise, you may use the `*` character when specifying your validation messages in your language files, making it a breeze to use a single validation message for array based fields:

    'custom' => [
        'person.*.email' => [
            'unique' => 'Each person must have a unique e-mail address',
        ]
    ],

### Bail Validation Rule

A new `bail` validation rule has been added, which instructs the validator to stop validating after the first validation failure for a given rule. For example, you may now prevent the validator from running a `unique` check if an attribute fails an `integer` check:

    $this->validate($request, [
        'user_id' => 'bail|integer|unique:users'
    ]);

### Eloquent Global Scope Improvements

In previous versions of Laravel, global Eloquent scopes were complicated and error-prone to implement; however, in Laravel 5.2, global query scopes only require you to implement a single, simple method: `apply`.

For more information on writing global scopes, check out the full [Eloquent documentation](/docs/{{version}}/eloquent#global-scopes).

<a name="laravel-5.1.11"></a>
## Laravel 5.1.11

Laravel 5.1.11 introduces [authorization](/docs/{{version}}/authorization) support out of the box! Conveniently organize your application's authorization logic using simple callbacks or policy classes, and authorize actions using simple, expressive methods.

For more information, please refer to the [authorization documentation](/docs/{{version}}/authorization).

<a name="laravel-5.1.4"></a>
## Laravel 5.1.4

Laravel 5.1.4 introduces simple login throttling to the framework. Consult the [authentication documentation](/docs/{{version}}/authentication#authentication-throttling) for more information.

<a name="laravel-5.1"></a>
## Laravel 5.1

Laravel 5.1 continues the improvements made in Laravel 5.0 by adopting PSR-2 and adding event broadcasting, middleware parameters, Artisan improvements, and more.

### PHP 5.5.9+

Since PHP 5.4 will enter "end of life" in September and will no longer receive security updates from the PHP development team, Laravel 5.1 requires PHP 5.5.9 or greater. PHP 5.5.9 allows compatibility with the latest versions of popular PHP libraries such as Guzzle and the AWS SDK.

### LTS

 Laravel 5.1 is the first release of Laravel to receive **long term support**. Laravel 5.1 will receive bug fixes for 2 years and security fixes for 3 years. This support window is the largest ever provided for Laravel and provides stability and peace of mind for larger, enterprise clients and customers.

### PSR-2

The [PSR-2 coding style guide](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) has been adopted as the default style guide for the Laravel framework. Additionally, all generators have been updated to generate PSR-2 compatible syntax.

### Documentation

Every page of the Laravel documentation has been meticulously reviewed and dramatically improved. All code examples have also been reviewed and expanded to provide more relevance and context.

### Event Broadcasting

In many modern web applications, web sockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a websocket connection to be handled by the client.

To assist you in building these types of applications, Laravel makes it easy to "broadcast" your events over a websocket connection. Broadcasting your Laravel events allows you to share the same event names between your server-side code and your client-side JavaScript framework.

To learn more about event broadcasting, check out the [event documentation](/docs/{{version}}/events#broadcasting-events).

### Middleware Parameters

Middleware can now receive additional custom parameters. For example, if your application needs to verify that the authenticated user has a given "role" before performing a given action, you could create a `RoleMiddleware` that receives a role name as an additional argument:

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class RoleMiddleware
    {
        /**
         * Run the request filter.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @param  string  $role
         * @return mixed
         */
        public function handle($request, Closure $next, $role)
        {
            if (! $request->user()->hasRole($role)) {
                // Redirect...
            }

            return $next($request);
        }

    }

Middleware parameters may be specified when defining the route by separating the middleware name and parameters with a `:`. Multiple parameters should be delimited by commas:

    Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
        //
    }]);

For more information on middleware, check out the [middleware documentation](/docs/{{version}}/middleware).

### Testing Overhaul

The built-in testing capabilities of Laravel have been dramatically improved. A variety of new methods provide a fluent, expressive interface for interacting with your application and examining its responses. For example, check out the following test:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

For more information on testing, check out the [testing documentation](/docs/{{version}}/testing).

### Model Factories

Laravel now ships with an easy way to create stub Eloquent models using [model factories](/docs/{{version}}/database-testing#writing-factories). Model factories allow you to easily define a set of "default" attributes for your Eloquent model, and then generate test model instances for your tests or database seeds. Model factories also take advantage of the powerful [Faker](https://github.com/fzaninotto/Faker) PHP library for generating random attribute data:

    $factory->define(App\User::class, function ($faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => str_random(10),
            'remember_token' => str_random(10),
        ];
    });

For more information on model factories, check out [the documentation](/docs/{{version}}/database-testing#writing-factories).

### Artisan Improvements

Artisan commands may now be defined using a simple, route-like "signature", which provides an extremely simple interface for defining command line arguments and options. For example, you may define a simple command and its options like so:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--force}';

For more information on defining Artisan commands, consult the [Artisan documentation](/docs/{{version}}/artisan).

### Folder Structure

To better express intent, the `app/Commands` directory has been renamed to `app/Jobs`. Additionally, the `app/Handlers` directory has been consolidated into a single `app/Listeners` directory which simply contains event listeners. However, this is not a breaking change and you are not required to update to the new folder structure to use Laravel 5.1.

### Encryption

In previous versions of Laravel, encryption was handled by the `mcrypt` PHP extension. However, beginning in Laravel 5.1, encryption is handled by the `openssl` extension, which is more actively maintained.

<a name="laravel-5.0"></a>
## Laravel 5.0

Laravel 5.0 introduces a fresh application structure to the default Laravel project. This new structure serves as a better foundation for building a robust application in Laravel, as well as embraces new auto-loading standards (PSR-4) throughout the application. First, let's examine some of the major changes:

### New Folder Structure

The old `app/models` directory has been entirely removed. Instead, all of your code lives directly within the `app` folder, and, by default, is organized to the `App` namespace. This default namespace can be quickly changed using the new `app:name` Artisan command.

Controllers, middleware, and requests (a new type of class in Laravel 5.0) are now grouped under the `app/Http` directory, as they are all classes related to the HTTP transport layer of your application. Instead of a single, flat file of route filters, all middleware are now broken into their own class files.

A new `app/Providers` directory replaces the `app/start` files from previous versions of Laravel 4.x. These service providers provide various bootstrapping functions to your application, such as error handling, logging, route loading, and more. Of course, you are free to create additional service providers for your application.

Application language files and views have been moved to the `resources` directory.

### Contracts

All major Laravel components implement interfaces which are located in the `illuminate/contracts` repository. This repository has no external dependencies. Having a convenient, centrally located set of interfaces you may use for decoupling and dependency injection will serve as an easy alternative option to Laravel Facades.

For more information on contracts, consult the [full documentation](/docs/{{version}}/contracts).

### Route Cache

If your application is made up entirely of controller routes, you may utilize the new `route:cache` Artisan command to drastically speed up the registration of your routes. This is primarily useful on applications with 100+ routes and will **drastically** speed up this portion of your application.

### Route Middleware

In addition to Laravel 4 style route "filters", Laravel 5 now supports HTTP middleware, and the included authentication and CSRF "filters" have been converted to middleware. Middleware provides a single, consistent interface to replace all types of filters, allowing you to easily inspect, and even reject, requests before they enter your application.

For more information on middleware, check out [the documentation](/docs/{{version}}/middleware).

### Controller Method Injection

In addition to the existing constructor injection, you may now type-hint dependencies on controller methods. The [service container](/docs/{{version}}/container) will automatically inject the dependencies, even if the route contains other parameters:

    public function createPost(Request $request, PostRepository $posts)
    {
        //
    }

### Authentication Scaffolding

User registration, authentication, and password reset controllers are now included out of the box, as well as simple corresponding views, which are located at `resources/views/auth`. In addition, a "users" table migration has been included with the framework. Including these simple resources allows rapid development of application ideas without bogging down on authentication boilerplate. The authentication views may be accessed on the `auth/login` and `auth/register` routes. The `App\Services\Auth\Registrar` service is responsible for user validation and creation.

### Event Objects

You may now define events as objects instead of simply using strings. For example, check out the following event:

    <?php

    class PodcastWasPurchased
    {
        public $podcast;

        public function __construct(Podcast $podcast)
        {
            $this->podcast = $podcast;
        }
    }

The event may be dispatched like normal:

    Event::fire(new PodcastWasPurchased($podcast));

Of course, your event handler will receive the event object instead of a list of data:

    <?php

    class ReportPodcastPurchase
    {
        public function handle(PodcastWasPurchased $event)
        {
            //
        }
    }

For more information on working with events, check out the [full documentation](/docs/{{version}}/events).

### Commands / Queueing

In addition to the queue job format supported in Laravel 4, Laravel 5 allows you to represent your queued jobs as simple command objects. These commands live in the `app/Commands` directory. Here's a sample command:

    <?php

    class PurchasePodcast extends Command implements SelfHandling, ShouldBeQueued
    {
        use SerializesModels;

        protected $user, $podcast;

        /**
         * Create a new command instance.
         *
         * @return void
         */
        public function __construct(User $user, Podcast $podcast)
        {
            $this->user = $user;
            $this->podcast = $podcast;
        }

        /**
         * Execute the command.
         *
         * @return void
         */
        public function handle()
        {
            // Handle the logic to purchase the podcast...

            event(new PodcastWasPurchased($this->user, $this->podcast));
        }
    }

The base Laravel controller utilizes the new `DispatchesCommands` trait, allowing you to easily dispatch your commands for execution:

    $this->dispatch(new PurchasePodcastCommand($user, $podcast));

Of course, you may also use commands for tasks that are executed synchronously (are not queued). In fact, using commands is a great way to encapsulate complex tasks your application needs to perform. For more information, check out the [command bus](/docs/{{version}}/bus) documentation.

### Database Queue

A `database` queue driver is now included in Laravel, providing a simple, local queue driver that requires no extra package installation beyond your database software.

### Laravel Scheduler

In the past, developers have generated a Cron entry for each console command they wished to schedule. However, this is a headache. Your console schedule is no longer in source control, and you must SSH into your server to add the Cron entries. Let's make our lives easier. The Laravel command scheduler allows you to fluently and expressively define your command schedule within Laravel itself, and only a single Cron entry is needed on your server.

It looks like this:

    $schedule->command('artisan:command')->dailyAt('15:00');

Of course, check out the [full documentation](/docs/{{version}}/scheduling) to learn all about the scheduler!

### Tinker / Psysh

The `php artisan tinker` command now utilizes [Psysh](https://github.com/bobthecow/psysh) by Justin Hileman, a more robust REPL for PHP. If you liked Boris in Laravel 4, you're going to love Psysh. Even better, it works on Windows! To get started, just try:

    php artisan tinker

### DotEnv

Instead of a variety of confusing, nested environment configuration directories, Laravel 5 now utilizes [DotEnv](https://github.com/vlucas/phpdotenv) by Vance Lucas. This library provides a super simple way to manage your environment configuration, and makes environment detection in Laravel 5 a breeze. For more details, check out the full [configuration documentation](/docs/{{version}}/installation#environment-configuration).

### Laravel Elixir

Laravel Elixir, by Jeffrey Way, provides a fluent, expressive interface to compiling and concatenating your assets. If you've ever been intimidated by learning Grunt or Gulp, fear no more. Elixir makes it a cinch to get started using Gulp to compile your Less, Sass, and CoffeeScript. It can even run your tests for you!

For more information on Elixir, check out the [full documentation](/docs/{{version}}/elixir).

### Laravel Socialite

Laravel Socialite is an optional, Laravel 5.0+ compatible package that provides totally painless authentication with OAuth providers. Currently, Socialite supports Facebook, Twitter, Google, and GitHub. Here's what it looks like:

    public function redirectForAuth()
    {
        return Socialize::with('twitter')->redirect();
    }

    public function getUserFromProvider()
    {
        $user = Socialize::with('twitter')->user();
    }

No more spending hours writing OAuth authentication flows. Get started in minutes! The [full documentation](/docs/{{version}}/authentication#social-authentication) has all the details.

### Flysystem Integration

Laravel now includes the powerful [Flysystem](https://github.com/thephpleague/flysystem) filesystem abstraction library, providing pain free integration with local, Amazon S3, and Rackspace cloud storage - all with one, unified and elegant API! Storing a file in Amazon S3 is now as simple as:

    Storage::put('file.txt', 'contents');

For more information on the Laravel Flysystem integration, consult the [full documentation](/docs/{{version}}/filesystem).

### Form Requests

Laravel 5.0 introduces **form requests**, which extend the `Illuminate\Foundation\Http\FormRequest` class. These request objects can be combined with controller method injection to provide a boiler-plate free method of validating user input. Let's dig in and look at a sample `FormRequest`:

    <?php

    namespace App\Http\Requests;

    class RegisterRequest extends FormRequest
    {
        public function rules()
        {
            return [
                'email' => 'required|email|unique:users',
                'password' => 'required|confirmed|min:8',
            ];
        }

        public function authorize()
        {
            return true;
        }
    }

Once the class has been defined, we can type-hint it on our controller action:

    public function register(RegisterRequest $request)
    {
        var_dump($request->input());
    }

When the Laravel service container identifies that the class it is injecting is a `FormRequest` instance, the request will **automatically be validated**. This means that if your controller action is called, you can safely assume the HTTP request input has been validated according to the rules you specified in your form request class. Even more, if the request is invalid, an HTTP redirect, which you may customize, will automatically be issued, and the error messages will be either flashed to the session or converted to JSON. **Form validation has never been more simple.** For more information on `FormRequest` validation, check out the [documentation](/docs/{{version}}/validation#form-request-validation).

### Simple Controller Request Validation

The Laravel 5 base controller now includes a `ValidatesRequests` trait. This trait provides a simple `validate` method to validate incoming requests. If `FormRequests` are a little too much for your application, check this out:

    public function createPost(Request $request)
    {
        $this->validate($request, [
            'title' => 'required|max:255',
            'body' => 'required',
        ]);
    }

If the validation fails, an exception will be thrown and the proper HTTP response will automatically be sent back to the browser. The validation errors will even be flashed to the session! If the request was an AJAX request, Laravel even takes care of sending a JSON representation of the validation errors back to you.

For more information on this new method, check out [the documentation](/docs/{{version}}/validation#validation-quickstart).

### New Generators

To complement the new default application structure, new Artisan generator commands have been added to the framework. See `php artisan list` for more details.

### Configuration Cache

You may now cache all of your configuration in a single file using the `config:cache` command.

### Symfony VarDumper

The popular `dd` helper function, which dumps variable debug information, has been upgraded to use the amazing Symfony VarDumper. This provides color-coded output and even collapsing of arrays. Just try the following in your project:

    dd([1, 2, 3]);

<a name="laravel-4.2"></a>
## Laravel 4.2

The full change list for this release by running the `php artisan changes` command from a 4.2 installation, or by [viewing the change file on Github](https://github.com/laravel/framework/blob/4.2/src/Illuminate/Foundation/changes.json). These notes only cover the major enhancements and changes for the release.

> {note} During the 4.2 release cycle, many small bug fixes and enhancements were incorporated into the various Laravel 4.1 point releases. So, be sure to check the change list for Laravel 4.1 as well!

### PHP 5.4 Requirement

Laravel 4.2 requires PHP 5.4 or greater. This upgraded PHP requirement allows us to use new PHP features such as traits to provide more expressive interfaces for tools like [Laravel Cashier](/docs/billing). PHP 5.4 also brings significant speed and performance improvements over PHP 5.3.

### Laravel Forge

Laravel Forge, a new web based application, provides a simple way to create and manage PHP servers on the cloud of your choice, including Linode, DigitalOcean, Rackspace, and Amazon EC2. Supporting automated Nginx configuration, SSH key access, Cron job automation, server monitoring via NewRelic & Papertrail, "Push To Deploy", Laravel queue worker configuration, and more, Forge provides the simplest and most affordable way to launch all of your Laravel applications.

The default Laravel 4.2 installation's `app/config/database.php` configuration file is now configured for Forge usage by default, allowing for more convenient deployment of fresh applications onto the platform.

More information about Laravel Forge can be found on the [official Forge website](https://forge.laravel.com).

### Laravel Homestead

Laravel Homestead is an official Vagrant environment for developing robust Laravel and PHP applications. The vast majority of the boxes' provisioning needs are handled before the box is packaged for distribution, allowing the box to boot extremely quickly. Homestead includes Nginx 1.6, PHP 5.6, MySQL, Postgres, Redis, Memcached, Beanstalk, Node, Gulp, Grunt, & Bower. Homestead includes a simple `Homestead.yaml` configuration file for managing multiple Laravel applications on a single box.

The default Laravel 4.2 installation now includes an `app/config/local/database.php` configuration file that is configured to use the Homestead database out of the box, making Laravel initial installation and configuration more convenient.

The official documentation has also been updated to include [Homestead documentation](/docs/homestead).

### Laravel Cashier

Laravel Cashier is a simple, expressive library for managing subscription billing with Stripe. With the introduction of Laravel 4.2, we are including Cashier documentation along with the main Laravel documentation, though installation of the component itself is still optional. This release of Cashier brings numerous bug fixes, multi-currency support, and compatibility with the latest Stripe API.

### Daemon Queue Workers

The Artisan `queue:work` command now supports a `--daemon` option to start a worker in "daemon mode", meaning the worker will continue to process jobs without ever re-booting the framework. This results in a significant reduction in CPU usage at the cost of a slightly more complex application deployment process.

More information about daemon queue workers can be found in the [queue documentation](/docs/queues#daemon-queue-worker).

### Mail API Drivers

Laravel 4.2 introduces new Mailgun and Mandrill API drivers for the `Mail` functions. For many applications, this provides a faster and more reliable method of sending e-mails than the SMTP options. The new drivers utilize the Guzzle 4 HTTP library.

### Soft Deleting Traits

A much cleaner architecture for "soft deletes" and other "global scopes" has been introduced via PHP 5.4 traits. This new architecture allows for the easier construction of similar global traits, and a cleaner separation of concerns within the framework itself.

More information on the new `SoftDeletingTrait` may be found in the [Eloquent documentation](/docs/eloquent#soft-deleting).

### Convenient Auth & Remindable Traits

The default Laravel 4.2 installation now uses simple traits for including the needed properties for the authentication and password reminder user interfaces. This provides a much cleaner default `User` model file out of the box.

### "Simple Paginate"

A new `simplePaginate` method was added to the query and Eloquent builder which allows for more efficient queries when using simple "Next" and "Previous" links in your pagination view.

### Migration Confirmation

In production, destructive migration operations will now ask for confirmation. Commands may be forced to run without any prompts using the `--force` command.

<a name="laravel-4.1"></a>
## Laravel 4.1

### Full Change List

The full change list for this release by running the `php artisan changes` command from a 4.1 installation, or by [viewing the change file on Github](https://github.com/laravel/framework/blob/4.1/src/Illuminate/Foundation/changes.json). These notes only cover the major enhancements and changes for the release.

### New SSH Component

An entirely new `SSH` component has been introduced with this release. This feature allows you to easily SSH into remote servers and run commands. To learn more, consult the [SSH component documentation](/docs/ssh).

The new `php artisan tail` command utilizes the new SSH component. For more information, consult the `tail` [command documentation](http://laravel.com/docs/ssh#tailing-remote-logs).

### Boris In Tinker

The `php artisan tinker` command now utilizes the [Boris REPL](https://github.com/d11wtq/boris) if your system supports it. The `readline` and `pcntl` PHP extensions must be installed to use this feature. If you do not have these extensions, the shell from 4.0 will be used.

### Eloquent Improvements

A new `hasManyThrough` relationship has been added to Eloquent. To learn how to use it, consult the [Eloquent documentation](/docs/eloquent#has-many-through).

A new `whereHas` method has also been introduced to allow [retrieving models based on relationship constraints](/docs/eloquent#querying-relations).

### Database Read / Write Connections

Automatic handling of separate read / write connections is now available throughout the database layer, including the query builder and Eloquent. For more information, consult [the documentation](/docs/database#read-write-connections).

### Queue Priority

Queue priorities are now supported by passing a comma-delimited list to the `queue:listen` command.

### Failed Queue Job Handling

The queue facilities now include automatic handling of failed jobs when using the new `--tries` switch on `queue:listen`. More information on handling failed jobs can be found in the [queue documentation](/docs/queues#failed-jobs).

### Cache Tags

Cache "sections" have been superseded by "tags". Cache tags allow you to assign multiple "tags" to a cache item, and flush all items assigned to a single tag. More information on using cache tags may be found in the [cache documentation](/docs/cache#cache-tags).

### Flexible Password Reminders

The password reminder engine has been changed to provide greater developer flexibility when validating passwords, flashing status messages to the session, etc. For more information on using the enhanced password reminder engine, [consult the documentation](/docs/security#password-reminders-and-reset).

### Improved Routing Engine

Laravel 4.1 features a totally re-written routing layer. The API is the same; however, registering routes is a full 100% faster compared to 4.0. The entire engine has been greatly simplified, and the dependency on Symfony Routing has been minimized to the compiling of route expressions.

### Improved Session Engine

With this release, we're also introducing an entirely new session engine. Similar to the routing improvements, the new session layer is leaner and faster. We are no longer using Symfony's (and therefore PHP's) session handling facilities, and are using a custom solution that is simpler and easier to maintain.

### Doctrine DBAL

If you are using the `renameColumn` function in your migrations, you will need to add the `doctrine/dbal` dependency to your `composer.json` file. This package is no longer included in Laravel by default.
