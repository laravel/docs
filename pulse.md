# Laravel Pulse

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Dashboard](#dashboard)
    - [Authorization](#dashboard-authorization)
    - [Customization](#dashboard-customization)
    - [Resolving Users](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [Capturing Entries](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtering](#filtering)
- [Performance](#performance)
    - [Using a Different Database](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [Sampling](#sampling)
    - [Trimming](#trimming)
    - [Handling Pulse Exceptions](#pulse-exceptions)
- [Custom Cards](#custom-cards)
    - [Card Components](#custom-card-components)
    - [Styling](#custom-card-styling)
    - [Data Capture and Aggregation](#custom-card-data)

<a name="introduction"></a>
## Introduction

[Laravel Pulse](https://github.com/laravel/pulse) delivers at-a-glance insights into your application's performance and usage. With Pulse, you can track down bottlenecks like slow jobs and endpoints, find your most active users, and more.

For in-depth debugging of individual events, check out [Laravel Telescope](/docs/{{version}}/telescope).

<a name="installation"></a>
## Installation

> [!WARNING]
> Pulse's first-party storage implementation currently requires a MySQL, MariaDB, or PostgreSQL database. If you are using a different database engine, you will need a separate MySQL, MariaDB, or PostgreSQL database for your Pulse data.

You may install Pulse using the Composer package manager:

```shell
composer require laravel/pulse
```

Next, you should publish the Pulse configuration and migration files using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

Finally, you should run the `migrate` command in order to create the tables needed to store Pulse's data:

```shell
php artisan migrate
```

Once Pulse's database migrations have been run, you may access the Pulse dashboard via the `/pulse` route.

> [!NOTE]
> If you do not want to store Pulse data in your application's primary database, you may [specify a dedicated database connection](#using-a-different-database).

<a name="configuration"></a>
### Configuration

Many of Pulse's configuration options can be controlled using environment variables. To see the available options, register new recorders, or configure advanced options, you may publish the `config/pulse.php` configuration file:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## Dashboard

<a name="dashboard-authorization"></a>
### Authorization

The Pulse dashboard may be accessed via the `/pulse` route. By default, you will only be able to access this dashboard in the `local` environment, so you will need to configure authorization for your production environments by customizing the `'viewPulse'` authorization gate. You can accomplish this within your application's `app/Providers/AppServiceProvider.php` file:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a name="dashboard-customization"></a>
### Customization

The Pulse dashboard cards and layout may be configured by publishing the dashboard view. The dashboard view will be published to `resources/views/vendor/pulse/dashboard.blade.php`:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

The dashboard is powered by [Livewire](https://livewire.laravel.com/), and allows you to customize the cards and layout without needing to rebuild any JavaScript assets.

Within this file, the `<x-pulse>` component is responsible for rendering the dashboard and provides a grid layout for the cards. If you would like the dashboard to span the full width of the screen, you may provide the `full-width` prop to the component:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

By default, the `<x-pulse>` component will create a 12 column grid, but you may customize this using the `cols` prop:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

Each card accepts a `cols` and `rows` prop to control the space and positioning:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

Most cards also accept an `expand` prop to show the full card instead of scrolling:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### Resolving Users

For cards that display information about your users, such as the Application Usage card, Pulse will only record the user's ID. When rendering the dashboard, Pulse will resolve the `name` and `email` fields from your default `Authenticatable` model and display avatars using the Gravatar web service.

You may customize the fields and avatar by invoking the `Pulse::user` method within your application's `App\Providers\AppServiceProvider` class.

The `user` method accepts a closure which will receive the `Authenticatable` model to be displayed and should return an array containing `name`, `extra`, and `avatar` information for the user:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> [!NOTE]
> You may completely customize how the authenticated user is captured and retrieved by implementing the `Laravel\Pulse\Contracts\ResolvesUsers` contract and binding it in Laravel's [service container](/docs/{{version}}/container#binding-a-singleton).

<a name="dashboard-cards"></a>
### Cards

<a name="servers-card"></a>
#### Servers

The `<livewire:pulse.servers />` card displays system resource usage for all servers running the `pulse:check` command. Please refer to the documentation regarding the [servers recorder](#servers-recorder) for more information on system resource reporting.

If you replace a server in your infrastructure, you may wish to stop displaying the inactive server in the Pulse dashboard after a given duration. You may accomplish this using the `ignore-after` prop, which accepts the number of seconds after which inactive servers should be removed from the Pulse dashboard. Alternatively, you may provide a relative time formatted string, such as `1 hour` or `3 days and 1 hour`:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### Application Usage

The `<livewire:pulse.usage />` card displays the top 10 users making requests to your application, dispatching jobs, and experiencing slow requests.

If you wish to view all usage metrics on screen at the same time, you may include the card multiple times and specify the `type` attribute:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

To learn how to customize how Pulse retrieves and displays user information, consult our documentation on [resolving users](#dashboard-resolving-users).

> [!NOTE]
> If your application receives a lot of requests or dispatches a lot of jobs, you may wish to enable [sampling](#sampling). See the [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), and [slow jobs recorder](#slow-jobs-recorder) documentation for more information.

<a name="exceptions-card"></a>
#### Exceptions

The `<livewire:pulse.exceptions />` card shows the frequency and recency of exceptions occurring in your application. By default, exceptions are grouped based on the exception class and location where it occurred. See the [exceptions recorder](#exceptions-recorder) documentation for more information.

<a name="queues-card"></a>
#### Queues

The `<livewire:pulse.queues />` card shows the throughput of the queues in your application, including the number of jobs queued, processing, processed, released, and failed. See the [queues recorder](#queues-recorder) documentation for more information.

<a name="slow-requests-card"></a>
#### Slow Requests

The `<livewire:pulse.slow-requests />` card shows incoming requests to your application that exceed the configured threshold, which is 1,000ms by default. See the [slow requests recorder](#slow-requests-recorder) documentation for more information.

<a name="slow-jobs-card"></a>
#### Slow Jobs

The `<livewire:pulse.slow-jobs />` card shows the queued jobs in your application that exceed the configured threshold, which is 1,000ms by default. See the [slow jobs recorder](#slow-jobs-recorder) documentation for more information.

<a name="slow-queries-card"></a>
#### Slow Queries

The `<livewire:pulse.slow-queries />` card shows the database queries in your application that exceed the configured threshold, which is 1,000ms by default.

By default, slow queries are grouped based on the SQL query (without bindings) and the location where it occurred, but you may choose to not capture the location if you wish to group solely on the SQL query.

If you encounter rendering performance issues due to extremely large SQL queries receiving syntax highlighting, you may disable highlighting by adding the `without-highlighting` prop:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

See the [slow queries recorder](#slow-queries-recorder) documentation for more information.

<a name="slow-outgoing-requests-card"></a>
#### Slow Outgoing Requests

The `<livewire:pulse.slow-outgoing-requests />` card shows outgoing requests made using Laravel's [HTTP client](/docs/{{version}}/http-client) that exceed the configured threshold, which is 1,000ms by default.

By default, entries will be grouped by the full URL. However, you may wish to normalize or group similar outgoing requests using regular expressions. See the [slow outgoing requests recorder](#slow-outgoing-requests-recorder) documentation for more information.

<a name="cache-card"></a>
#### Cache

The `<livewire:pulse.cache />` card shows the cache hit and miss statistics for your application, both globally and for individual keys.

By default, entries will be grouped by key. However, you may wish to normalize or group similar keys using regular expressions. See the [cache interactions recorder](#cache-interactions-recorder) documentation for more information.

<a name="capturing-entries"></a>
## Capturing Entries

Most Pulse recorders will automatically capture entries based on framework events dispatched by Laravel. However, the [servers recorder](#servers-recorder) and some third-party cards must poll for information regularly. To use these cards, you must run the `pulse:check` daemon on all of your individual application servers:

```php
php artisan pulse:check
```

> [!NOTE]
> To keep the `pulse:check` process running permanently in the background, you should use a process monitor such as Supervisor to ensure that the command does not stop running.

As the `pulse:check` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse uses the [cache](/docs/{{version}}/cache) to store restart signals, so you should verify that a cache driver is properly configured for your application before using this feature.

<a name="recorders"></a>
### Recorders

Recorders are responsible for capturing entries from your application to be recorded in the Pulse database. Recorders are registered and configured in the `recorders` section of the [Pulse configuration file](#configuration).

<a name="cache-interactions-recorder"></a>
#### Cache Interactions

The `CacheInteractions` recorder captures information about the [cache](/docs/{{version}}/cache) hits and misses occurring in your application for display on the [Cache](#cache-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored key patterns.

You may also configure key grouping so that similar keys are grouped as a single entry. For example, you may wish to remove unique IDs from keys caching the same type of information. Groups are configured using a regular expression to "find and replace" parts of the key. An example is included in the configuration file:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

The first pattern that matches will be used. If no patterns match, then the key will be captured as-is.

<a name="exceptions-recorder"></a>
#### Exceptions

The `Exceptions` recorder captures information about reportable exceptions occurring in your application for display on the [Exceptions](#exceptions-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored exceptions patterns. You may also configure whether to capture the location that the exception originated from. The captured location will be displayed on the Pulse dashboard which can help to track down the exception origin; however, if the same exception occurs in multiple locations then it will appear multiple times for each unique location.

<a name="queues-recorder"></a>
#### Queues

The `Queues` recorder captures information about your applications queues for display on the [Queues](#queues-card).

You may optionally adjust the [sample rate](#sampling) and ignored jobs patterns.

<a name="slow-jobs-recorder"></a>
#### Slow Jobs

The `SlowJobs` recorder captures information about slow jobs occurring in your application for display on the [Slow Jobs](#slow-jobs-recorder) card.

You may optionally adjust the slow job threshold, [sample rate](#sampling), and ignored job patterns.

You may have some jobs that you expect to take longer than others. In those cases, you may configure per-job thresholds:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

If no regular expression patterns match the job's classname, then the `'default'` value will be used.

<a name="slow-outgoing-requests-recorder"></a>
#### Slow Outgoing Requests

The `SlowOutgoingRequests` recorder captures information about outgoing HTTP requests made using Laravel's [HTTP client](/docs/{{version}}/http-client) that exceed the configured threshold for display on the [Slow Outgoing Requests](#slow-outgoing-requests-card) card.

You may optionally adjust the slow outgoing request threshold, [sample rate](#sampling), and ignored URL patterns.

You may have some outgoing requests that you expect to take longer than others. In those cases, you may configure per-request thresholds:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

If no regular expression patterns match the request's URL, then the `'default'` value will be used.

You may also configure URL grouping so that similar URLs are grouped as a single entry. For example, you may wish to remove unique IDs from URL paths or group by domain only. Groups are configured using a regular expression to "find and replace" parts of the URL. Some examples are included in the configuration file:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

The first pattern that matches will be used. If no patterns match, then the URL will be captured as-is.

<a name="slow-queries-recorder"></a>
#### Slow Queries

The `SlowQueries` recorder captures any database queries in your application that exceed the configured threshold for display on the [Slow Queries](#slow-queries-card) card.

You may optionally adjust the slow query threshold, [sample rate](#sampling), and ignored query patterns. You may also configure whether to capture the query location. The captured location will be displayed on the Pulse dashboard which can help to track down the query origin; however, if the same query is made in multiple locations then it will appear multiple times for each unique location.

You may have some queries that you expect to take longer than others. In those cases, you may configure per-query thresholds:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

If no regular expression patterns match the query's SQL, then the `'default'` value will be used.

<a name="slow-requests-recorder"></a>
#### Slow Requests

The `Requests` recorder captures information about requests made to your application for display on the [Slow Requests](#slow-requests-card) and [Application Usage](#application-usage-card) cards.

You may optionally adjust the slow route threshold, [sample rate](#sampling), and ignored paths.

You may have some requests that you expect to take longer than others. In those cases, you may configure per-request thresholds:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

If no regular expression patterns match the request's URL, then the `'default'` value will be used.

<a name="servers-recorder"></a>
#### Servers

The `Servers` recorder captures CPU, memory, and storage usage of the servers that power your application for display on the [Servers](#servers-card) card. This recorder requires the [pulse:check command](#capturing-entries) to be running on each of the servers you wish to monitor.

Each reporting server must have a unique name. By default, Pulse will use the value returned by PHP's `gethostname` function. If you wish to customize this, you may set the `PULSE_SERVER_NAME` environment variable:

```env
PULSE_SERVER_NAME=load-balancer
```

The Pulse configuration file also allows you to customize the directories that are monitored.

<a name="user-jobs-recorder"></a>
#### User Jobs

The `UserJobs` recorder captures information about the users dispatching jobs in your application for display on the [Application Usage](#application-usage-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored job patterns.

<a name="user-requests-recorder"></a>
#### User Requests

The `UserRequests` recorder captures information about the users making requests to your application for display on the [Application Usage](#application-usage-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored URL patterns.

<a name="filtering"></a>
### Filtering

As we have seen, many [recorders](#recorders) offer the ability to, via configuration, "ignore" incoming entries based on their value, such as a request's URL. But, sometimes it may be useful to filter out records based on other factors, such as the currently authenticated user. To filter out these records, you may pass a closure to Pulse's `filter` method. Typically, the `filter` method should be invoked within the `boot` method of your application's `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a name="performance"></a>
## Performance

Pulse has been designed to drop into an existing application without requiring any additional infrastructure. However, for high-traffic applications, there are several ways of removing any impact Pulse may have on your application's performance.

<a name="using-a-different-database"></a>
### Using a Different Database

For high-traffic applications, you may prefer to use a dedicated database connection for Pulse to avoid impacting your application database.

You may customize the [database connection](/docs/{{version}}/database#configuration) used by Pulse by setting the `PULSE_DB_CONNECTION` environment variable.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis Ingest

> [!WARNING]
> The Redis Ingest requires Redis 6.2 or greater and `phpredis` or `predis` as the application's configured Redis client driver.

By default, Pulse will store entries directly to the [configured database connection](#using-a-different-database) after the HTTP response has been sent to the client or a job has been processed; however, you may use Pulse's Redis ingest driver to send entries to a Redis stream instead. This can be enabled by configuring the `PULSE_INGEST_DRIVER` environment variable:

```ini
PULSE_INGEST_DRIVER=redis
```

Pulse will use your default [Redis connection](/docs/{{version}}/redis#configuration) by default, but you may customize this via the `PULSE_REDIS_CONNECTION` environment variable:

```ini
PULSE_REDIS_CONNECTION=pulse
```

When using the Redis ingest, you will need to run the `pulse:work` command to monitor the stream and move entries from Redis into Pulse's database tables.

```php
php artisan pulse:work
```

> [!NOTE]
> To keep the `pulse:work` process running permanently in the background, you should use a process monitor such as Supervisor to ensure that the Pulse worker does not stop running.

As the `pulse:work` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse uses the [cache](/docs/{{version}}/cache) to store restart signals, so you should verify that a cache driver is properly configured for your application before using this feature.

<a name="sampling"></a>
### Sampling

By default, Pulse will capture every relevant event that occurs in your application. For high-traffic applications, this can result in needing to aggregate millions of database rows in the dashboard, especially for longer time periods.

You may instead choose to enable "sampling" on certain Pulse data recorders. For example, setting the sample rate to `0.1` on the [User Requests](#user-requests-recorder) recorder will mean that you only record approximately 10% of the requests to your application. In the dashboard, the values will be scaled up and prefixed with a `~` to indicate that they are an approximation.

In general, the more entries you have for a particular metric, the lower you can safely set the sample rate without sacrificing too much accuracy.

<a name="trimming"></a>
### Trimming

Pulse will automatically trim its stored entries once they are outside of the dashboard window. Trimming occurs when ingesting data using a lottery system which may be customized in the Pulse [configuration file](#configuration).

<a name="pulse-exceptions"></a>
### Handling Pulse Exceptions

If an exception occurs while capturing Pulse data, such as being unable to connect to the storage database, Pulse will silently fail to avoid impacting your application.

If you wish to customize how these exceptions are handled, you may provide a closure to the `handleExceptionsUsing` method:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
## Custom Cards

Pulse allows you to build custom cards to display data relevant to your application's specific needs. Pulse uses [Livewire](https://livewire.laravel.com), so you may want to [review its documentation](https://livewire.laravel.com/docs) before building your first custom card.

<a name="custom-card-components"></a>
### Card Components

Creating a custom card in Laravel Pulse starts with extending the base `Card` Livewire component and defining a corresponding view:

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

When using Livewire's [lazy loading](https://livewire.laravel.com/docs/lazy) feature, The `Card` component will automatically provide a placeholder that respects the `cols` and `rows` attributes passed to your component.

When writing your Pulse card's corresponding view, you may leverage Pulse's Blade components for a consistent look and feel:

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

The `$cols`, `$rows`, `$class`, and `$expand` variables should be passed to their respective Blade components so the card layout may be customized from the dashboard view. You may also wish to include the `wire:poll.5s=""` attribute in your view to have the card automatically update.

Once you have defined your Livewire component and template, the card may be included in your [dashboard view](#dashboard-customization):

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> If your card is included in a package, you will need to register the component with Livewire using the `Livewire::component` method.

<a name="custom-card-styling"></a>
### Styling

If your card requires additional styling beyond the classes and components included with Pulse, there are a few options for including custom CSS for your cards.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite Integration

If your custom card lives within your application's code base and you are using Laravel's [Vite integration](/docs/{{version}}/vite), you may update your `vite.config.js` file to include a dedicated CSS entry point for your card:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

You may then use the `@vite` Blade directive in your [dashboard view](#dashboard-customization), specifying the CSS entrypoint for your card:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS Files

For other use cases, including Pulse cards contained within a package, you may instruct Pulse to load additional stylesheets by defining a `css` method on your Livewire component that returns the file path to your CSS file:

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

When this card is included on the dashboard, Pulse will automatically include the contents of this file within a `<style>` tag so it does not need to be published to the `public` directory.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

When using Tailwind CSS, you should create a dedicated Tailwind configuration file to avoid loading unnecessary CSS or conflicting with Pulse's Tailwind classes:

```js
export default {
    darkMode: 'class',
    important: '#top-sellers',
    content: [
        './resources/views/livewire/pulse/top-sellers.blade.php',
    ],
    corePlugins: {
        preflight: false,
    },
};
```

You may then specify the configuration file in your CSS entrypoint:

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

You will also need to include an `id` or `class` attribute in your card's view that matches the selector passed to Tailwind's [important selector strategy](https://tailwindcss.com/docs/configuration#selector-strategy):

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### Data Capture and Aggregation

Custom cards may fetch and display data from anywhere; however, you may wish to leverage Pulse's powerful and efficient data recording and aggregation system.

<a name="custom-card-data-capture"></a>
#### Capturing Entries

Pulse allows you to record "entries" using the `Pulse::record` method:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

The first argument provided to the `record` method is the `type` for the entry you are recording, while the second argument is the `key` that determines how the aggregated data should be grouped. For most aggregation methods you will also need to specify a `value` to be aggregated. In the example above, the value being aggregated is `$sale->amount`. You may then invoke one or more aggregation methods (such as `sum`) so that Pulse may capture pre-aggregated values into "buckets" for efficient retrieval later.

The available aggregation methods are:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> When building a card package that captures the currently authenticated user ID, you should use the `Pulse::resolveAuthenticatedUserId()` method, which respects any [user resolver customizations](#dashboard-resolving-users) made to the application.

<a name="custom-card-data-retrieval"></a>
#### Retrieving Aggregate Data

When extending Pulse's `Card` Livewire component, you may use the `aggregate` method to retrieve aggregated data for the period being viewed in the dashboard:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

The `aggregate` method returns a collection of PHP `stdClass` objects. Each object will contain the `key` property captured earlier, along with keys for each of the requested aggregates:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse will primarily retrieve data from the pre-aggregated buckets; therefore, the specified aggregates must have been captured up-front using the `Pulse::record` method. The oldest bucket will typically fall partially outside the period, so Pulse will aggregate the oldest entries to fill the gap and give an accurate value for the entire period, without needing to aggregate the entire period on each poll request.

You may also retrieve a total value for a given type by using the `aggregateTotal` method. For example, the following method would retrieve the total of all user sales instead of grouping them by user.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### Displaying Users

When working with aggregates that record a user ID as the key, you may resolve the keys to user records using the `Pulse::resolveUsers` method:

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

The `find` method returns an object containing `name`, `extra`, and `avatar` keys, which you may optionally pass directly to the `<x-pulse::user-card>` Blade component:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### Custom Recorders

Package authors may wish to provide recorder classes to allow users to configure the capturing of data.

Recorders are registered in the `recorders` section of the application's `config/pulse.php` configuration file:

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

Recorders may listen to events by specifying a `$listen` property. Pulse will automatically register the listeners and call the recorders `record` method:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```
