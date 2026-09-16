# Concurrency

- [Introduction](#introduction)
- [Running Concurrent Tasks](#running-concurrent-tasks)
    - [Named Results](#named-results)
    - [Task Timeouts](#task-timeouts)
- [Queue Driver](#queue-driver)
    - [Queue Driver Configuration](#queue-driver-configuration)
    - [Queue Task Timeouts](#queue-task-timeouts)
    - [Queue and Cache Failover](#queue-and-cache-failover)
- [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

<a name="introduction"></a>
## Introduction

Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently.

<a name="how-it-works"></a>
#### How it Works

When using the default `process` driver, Laravel achieves concurrency by serializing the given closures and dispatching them to a hidden Artisan CLI command, which unserializes the closures and invokes it within its own PHP process. After the closure has been invoked, the resulting value is serialized back to the parent process.

The `Concurrency` facade supports four drivers: `process` (the default), `fork`, `sync`, and `queue`.

The `fork` driver offers improved performance compared to the default `process` driver, but it may only be used within PHP's CLI context, as PHP does not support forking during web requests. Before using the `fork` driver, you need to install the `spatie/fork` package:

```shell
composer require spatie/fork
```

The `sync` driver is primarily useful during testing when you want to disable all concurrency and simply execute the given closures in sequence within the parent process.

The [queue driver](#queue-driver) executes the given closures using your application's queue workers and returns their results through a shared cache store.

<a name="running-concurrent-tasks"></a>
## Running Concurrent Tasks

To run concurrent tasks, you may invoke the `Concurrency` facade's `run` method. The `run` method accepts an array of closures which should be executed concurrently:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

To use a specific driver, you may use the `driver` method:

```php
$results = Concurrency::driver('fork')->run(...);
```

Or, to change the default concurrency driver, you should publish the `concurrency` configuration file via the `config:publish` Artisan command and update the `default` option within the file:

```shell
php artisan config:publish concurrency
```

<a name="named-results"></a>
### Named Results

If you would like to access concurrent task results by name rather than by position, you may provide an associative array of closures. Each result will be returned using the same key as its corresponding closure:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

$results = Concurrency::run([
    'users' => fn () => DB::table('users')->count(),
    'orders' => fn () => DB::table('orders')->count(),
]);

$userCount = $results['users'];
$orderCount = $results['orders'];
```

<a name="task-timeouts"></a>
### Task Timeouts

When using the `process` driver (the default), you may specify a maximum number of seconds a concurrent task is allowed to run before it is terminated by providing a timeout to the `run` method:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);
```

You may also provide a `CarbonInterval` instance if you prefer a more expressive timeout definition:

```php
use Illuminate\Support\Facades\Concurrency;

use function Illuminate\Support\seconds;

Concurrency::run([...], timeout: seconds(30));
```

The `queue` driver also accepts a timeout, but it limits how long the caller waits for results. For more information, consult the [queue task timeout documentation](#queue-task-timeouts).

<a name="queue-driver"></a>
## Queue Driver

The `queue` driver allows you to execute concurrent tasks using your application's queue workers, which may run on other servers. The `run` method waits for the tasks to finish and returns their results:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::driver('queue')->run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

To process tasks on queue workers, you should [start queue workers](/docs/{{version}}/queues#running-the-queue-worker) for the connection that will process your tasks. You should also configure a cache store, such as Redis, Memcached, or a database, that both the calling application and the workers can access. A local `array` cache store cannot share results between processes. Connections using the `deferred`, `background`, or `null` queue drivers are not supported.

The `sync` queue connection runs tasks in the current process, so it does not require a worker or a shared cache store.

If you call `run` from a queued job, ensure that other workers are available to process its tasks. Otherwise, the job may wait until it times out. Tasks are dispatched immediately, even within a [database transaction](/docs/{{version}}/queues#jobs-and-database-transactions), so they may not see changes that have not been committed.

If a task fails, `run` throws an exception in the calling process. Failures on queue workers also use Laravel's normal [failed job handling](/docs/{{version}}/queues#dealing-with-failed-jobs). Tasks dispatched by `run` are configured for a single attempt. As with other queued jobs, a task may run more than once, so it should be safe to repeat.

<a name="queue-driver-configuration"></a>
### Queue Driver Configuration

By default, the driver uses your application's default queue connection and cache store. You may specify a different connection, queue, or cache store using the `onConnection`, `onQueue`, and `store` methods:

```php
$results = Concurrency::driver('queue')
    ->onConnection('redis')
    ->onQueue('reports')
    ->store('redis')
    ->run([...]);
```

To change these defaults, you may update the `drivers.queue` options in your application's published `config/concurrency.php` configuration file. You may also configure additional queue drivers with their own names:

```php
'drivers' => [
    // ...

    'reports' => [
        'driver' => 'queue',
        'connection' => 'redis',
        'queue' => 'reports',
        'store' => 'redis',
        'timeout' => 60,
    ],
],
```

You may then use the named driver when running tasks:

```php
$results = Concurrency::driver('reports')->run([...]);
```

You may also add a `poll` option to the driver's configuration to change how often Laravel checks for results, in milliseconds. The default is `100`.

The optional `ttl` option sets the expiration time for cached task data, in seconds. Laravel uses at least the timeout plus 60 seconds, even if a shorter expiration time is configured. Results are removed when the run finishes.

<a name="queue-task-timeouts"></a>
### Queue Task Timeouts

By default, the queue driver waits up to 60 seconds for results, including time spent waiting in the queue. You may change this using the driver's `timeout` configuration option or provide a timeout when calling `run`:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

$results = Concurrency::driver('queue')->run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);
```

If the timeout is exceeded before all results are available, Laravel throws an `Illuminate\Concurrency\TaskTimedOutException`. Tasks that have not started are skipped, but stopping the wait does not interrupt tasks that are already running. For connections with a `retry_after` option, its value should be greater than the timeout you use for concurrent tasks. For more information, consult the [job expiration and timeout documentation](/docs/{{version}}/queues#job-expirations-and-timeouts).

<a name="queue-and-cache-failover"></a>
### Queue and Cache Failover

You may use a [failover queue connection](/docs/{{version}}/queues#queue-failover) to dispatch tasks. Each connection in the list must use a supported queue driver. If the connection falls back to the `sync` queue connection, tasks run one after another in the current process without a worker and may take longer than the configured timeout.

A single shared cache store is recommended for results. When using a [failover cache store](/docs/{{version}}/cache#cache-failover), each store must be shared by the calling application and its workers. Results written to a backup store may become unavailable when the primary store recovers, causing the run to time out.

<a name="deferring-concurrent-tasks"></a>
## Deferring Concurrent Tasks

If you would like to execute an array of closures concurrently, but are not interested in the results returned by those closures, you should consider using the `defer` method. When the `defer` method is invoked, the given closures are not executed immediately. Instead, Laravel will execute the closures concurrently after the HTTP response has been sent to the user:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```

When using the `queue` driver, the `defer` method dispatches tasks to the queue after the response has been sent. Queue workers process the tasks using the normal queue retry settings, and Laravel does not wait to collect their results. If you use a `sync` queue connection, the tasks run in the current process instead:

```php
Concurrency::driver('queue')->onQueue('metrics')->defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```
