# Release Notes

- [Versioning Scheme](#versioning-scheme)
    - [Exceptions](#exceptions)
- [Support Policy](#support-policy)
- [Laravel 8](#laravel-8)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~September), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^8.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

<a name="exceptions"></a>
### Exceptions

<a name="named-arguments"></a>
#### Named Arguments

At this time, PHP's [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) functionality are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function parameters when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 6, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/{{version}}/database#introduction).

| Version | Release | Bug Fixes Until | Security Fixes Until |
| --- | --- | --- | --- |
| 6 (LTS) | September 3rd, 2019 | September 7th, 2021 | September 6th, 2022 |
| 7 | March 3rd, 2020 | October 6th, 2020 | March 3rd, 2021 |
| 8 | September 8th, 2020 | March 1st, 2022 | September 6th, 2022 |
| 9 (LTS) | September, 2021 | September, 2023 | September, 2024 |
| 10 | September, 2022 | March, 2024 | September, 2024 |

<a name="laravel-8"></a>
## Laravel 8

Laravel 8 continues the improvements made in Laravel 7.x by introducing Laravel Jetstream, model factory classes, migration squashing, job batching, improved rate limiting, queue improvements, dynamic Blade components, Tailwind pagination views, time testing helpers, improvements to `artisan serve`, event listener improvements, and a variety of other bug fixes and usability improvements.

<a name="laravel-jetstream"></a>
### Laravel Jetstream

_Laravel Jetstream was written by [Taylor Otwell](https://github.com/taylorotwell)_.

[Laravel Jetstream](https://jetstream.laravel.com) is a beautifully designed application scaffolding for Laravel. Jetstream provides the perfect starting point for your next project and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Laravel Jetstream replaces and improves upon the legacy authentication UI scaffolding available for previous versions of Laravel.

Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) scaffolding.

<a name="models-directory"></a>
### Models Directory

By overwhelming community demand, the default Laravel application skeleton now contains an `app/Models` directory. We hope you enjoy this new home for your Eloquent models! All relevant generator commands have been updated to assume models exist within the `app/Models` directory if it exists. If the directory does not exist, the framework will assume your models should be placed within the `app` directory.

<a name="model-factory-classes"></a>
### Model Factory Classes

_Model factory classes were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Eloquent [model factories](/docs/{{version}}/database-testing#defining-model-factories) have been entirely re-written as class based factories and improved to have first-class relationship support. For example, the `UserFactory` included with Laravel is written like so:

    <?php

    namespace Database\Factories;

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Factory;
    use Illuminate\Support\Str;

    class UserFactory extends Factory
    {
        /**
         * The name of the factory's corresponding model.
         *
         * @var string
         */
        protected $model = User::class;

        /**
         * Define the model's default state.
         *
         * @return array
         */
        public function definition()
        {
            return [
                'name' => $this->faker->name(),
                'email' => $this->faker->unique()->safeEmail(),
                'email_verified_at' => now(),
                'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
                'remember_token' => Str::random(10),
            ];
        }
    }

Thanks to the new `HasFactory` trait available on generated models, the model factory may be used like so:

    use App\Models\User;

    User::factory()->count(50)->create();

Since model factories are now simple PHP classes, state transformations may be written as class methods. In addition, you may add any other helper classes to your Eloquent model factory as needed.

For example, your `User` model might have a `suspended` state that modifies one of its default attribute values. You may define your state transformations using the base factory's `state` method. You may name your state method anything you like. After all, it's just a typical PHP method:

    /**
     * Indicate that the user is suspended.
     *
     * @return \Illuminate\Database\Eloquent\Factories\Factory
     */
    public function suspended()
    {
        return $this->state([
            'account_status' => 'suspended',
        ]);
    }

After defining the state transformation method, we may use it like so:

    use App\Models\User;

    User::factory()->count(5)->suspended()->create();

As mentioned, Laravel 8's model factories contain first class support for relationships. So, assuming our `User` model has a `posts` relationship method, we may simply run the following code to generate a user with three posts:

    $users = User::factory()
                ->hasPosts(3, [
                    'published' => false,
                ])
                ->create();

To ease the upgrade process, the [laravel/legacy-factories](https://github.com/laravel/legacy-factories) package has been released to provide support for the previous iteration of model factories within Laravel 8.x.

Laravel's re-written factories contain many more features that we think you will love. To learn more about model factories, please consult the [database testing documentation](/docs/{{version}}/database-testing#defining-model-factories).

<a name="migration-squashing"></a>
### Migration Squashing

_Migration squashing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

As you build your application, you may accumulate more and more migrations over time. This can lead to your migration directory becoming bloated with potentially hundreds of migrations. If you're using MySQL or PostgreSQL, you may now "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command:

    php artisan schema:dump

    // Dump the current database schema and prune all existing migrations...
    php artisan schema:dump --prune

When you execute this command, Laravel will write a "schema" file to your `database/schema` directory. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute the schema file's SQL first. After executing the schema file's commands, Laravel will execute any remaining migrations that were not part of the schema dump.

<a name="job-batching"></a>
### Job Batching

_Job batching was contributed by [Taylor Otwell](https://github.com/taylorotwell) & [Mohamed Said](https://github.com/themsaid)_.

Laravel's job batching feature allows you to easily execute a batch of jobs and then perform some action when the batch of jobs has completed executing.

The new `batch` method of the `Bus` facade may be used to dispatch a batch of jobs. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked:

    use App\Jobs\ProcessPodcast;
    use App\Podcast;
    use Illuminate\Bus\Batch;
    use Illuminate\Support\Facades\Bus;
    use Throwable;

    $batch = Bus::batch([
        new ProcessPodcast(Podcast::find(1)),
        new ProcessPodcast(Podcast::find(2)),
        new ProcessPodcast(Podcast::find(3)),
        new ProcessPodcast(Podcast::find(4)),
        new ProcessPodcast(Podcast::find(5)),
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->catch(function (Batch $batch, Throwable $e) {
        // First batch job failure detected...
    })->finally(function (Batch $batch) {
        // The batch has finished executing...
    })->dispatch();

    return $batch->id;

To learn more about job batching, please consult the [queue documentation](/docs/{{version}}/queues#job-batching).

<a name="improved-rate-limiting"></a>
### Improved Rate Limiting

_Rate limiting improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Laravel's request rate limiter feature has been augmented with more flexibility and power, while still maintaining backwards compatibility with previous release's `throttle` middleware API.

Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned this rate limiter:

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Support\Facades\RateLimiter;

    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });

Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user:

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100);
    });

Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit:

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100)->by($request->ip());
    });

Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/{{version}}/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route:

    Route::middleware(['throttle:uploads'])->group(function () {
        Route::post('/audio', function () {
            //
        });

        Route::post('/video', function () {
            //
        });
    });

To learn more about rate limiting, please consult the [routing documentation](/docs/{{version}}/routing#rate-limiting).

<a name="improved-maintenance-mode"></a>
### Improved Maintenance Mode

_Maintenance mode improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from [Spatie](https://spatie.be)_.

In previous releases of Laravel, the `php artisan down` maintenance mode feature may be bypassed using an "allow list" of IP addresses that were allowed to access the application. This feature has been removed in favor of a simpler "secret" / token solution.

While in maintenance mode, you may use the `secret` option to specify a maintenance mode bypass token:

    php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"

After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser:

    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### Pre-Rendering The Maintenance Mode View

If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine.

For this reason, Laravel now allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option:

    php artisan down --render="errors::503"

<a name="closure-dispatch-chain-catch"></a>
### Closure Dispatch / Chain `catch`

_Catch improvements were contributed by [Mohamed Said](https://github.com/themsaid)_.

Using the new `catch` method, you may now provide a closure that should be executed if a queued closure fails to complete successfully after exhausting all of your queue's configured retry attempts:

    use Throwable;

    dispatch(function () use ($podcast) {
        $podcast->publish();
    })->catch(function (Throwable $e) {
        // This job has failed...
    });

<a name="dynamic-blade-components"></a>
### Dynamic Blade Components

_Dynamic Blade components were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may now use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable:

    <x-dynamic-component :component="$componentName" class="mt-4" />

To learn more about Blade components, please consult the [Blade documentation](/docs/{{version}}/blade#components).

<a name="event-listener-improvements"></a>
### Event Listener Improvements

_Event listener improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Closure based event listeners may now be registered by only passing the closure to the `Event::listen` method. Laravel will inspect the closure to determine which type of event the listener handles:

    use App\Events\PodcastProcessed;
    use Illuminate\Support\Facades\Event;

    Event::listen(function (PodcastProcessed $event) {
        //
    });

In addition, closure based event listeners may now be marked as queueable using the `Illuminate\Events\queueable` function:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    }));

Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener:

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // The queued listener failed...
    }));

<a name="time-testing-helpers"></a>
### Time Testing Helpers

_Time testing helpers were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from Ruby on Rails_.

When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Laravel's base feature test class now includes helpers that allow you to manipulate the current time:

    public function testTimeCanBeManipulated()
    {
        // Travel into the future...
        $this->travel(5)->milliseconds();
        $this->travel(5)->seconds();
        $this->travel(5)->minutes();
        $this->travel(5)->hours();
        $this->travel(5)->days();
        $this->travel(5)->weeks();
        $this->travel(5)->years();

        // Travel into the past...
        $this->travel(-5)->hours();

        // Travel to an explicit time...
        $this->travelTo(now()->subHours(6));

        // Return back to the present time...
        $this->travelBack();
    }

<a name="artisan-serve-improvements"></a>
### Artisan `serve` Improvements

_Artisan `serve` improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

The Artisan `serve` command has been improved with automatic reloading when environment variable changes are detected within your local `.env` file. Previously, the command had to be manually stopped and restarted.

<a name="tailwind-pagination-views"></a>
### Tailwind Pagination Views

The Laravel paginator has been updated to use the [Tailwind CSS](https://tailwindcss.com) framework by default. Tailwind CSS is a highly customizable, low-level CSS framework that gives you all of the building blocks you need to build bespoke designs without any annoying opinionated styles you have to fight to override. Of course, Bootstrap 3 and 4 views remain available as well.

<a name="routing-namespace-updates"></a>
### Routing Namespace Updates

In previous releases of Laravel, the `RouteServiceProvider` contained a `$namespace` property. This property's value would automatically be prefixed onto controller route definitions and calls to the `action` helper / `URL::action` method. In Laravel 8.x, this property is `null` by default. This means that no automatic namespace prefixing will be done by Laravel. Therefore, in new Laravel 8.x applications, controller route definitions should be defined using standard PHP callable syntax:

    use App\Http\Controllers\UserController;

    Route::get('/users', [UserController::class, 'index']);

Calls to the `action` related methods should use the same callable syntax:

    action([UserController::class, 'index']);

    return Redirect::action([UserController::class, 'index']);

If you prefer Laravel 7.x style controller route prefixing, you may simply add the `$namespace` property into your application's `RouteServiceProvider`.

> {note} This change only affects new Laravel 8.x applications. Applications upgrading from Laravel 7.x will still have the `$namespace` property in their `RouteServiceProvider`.
