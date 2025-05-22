# Context

- [Introduction](#introduction)
    - [How it Works](#how-it-works)
- [Capturing Context](#capturing-context)
    - [Stacks](#stacks)
- [Retrieving Context](#retrieving-context)
    - [Determining Item Existence](#determining-item-existence)
- [Removing Context](#removing-context)
- [Hidden Context](#hidden-context)
- [Events](#events)
    - [Dehydrating](#dehydrating)
    - [Hydrated](#hydrated)

<a name="introduction"></a>
## Introduction

Laravel's "context" capabilities enable you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is also included in logs written by your application, giving you deeper insight into the surrounding code execution history that occurred before a log entry was written and allowing you to trace execution flows throughout a distributed system.

<a name="how-it-works"></a>
### How it Works

The best way to understand Laravel's context capabilities is to see it in action using  the built-in logging features. To get started, you may [add information to the context](#capturing-context) using the `Context` facade. In this example, we will use a [middleware](/docs/{{version}}/middleware) to add the request URL and a unique trace ID to the context on every incoming request:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}
```

Information added to the context is automatically appended as metadata to any [log entries](/docs/{{version}}/logging) that are written throughout the request. Appending context as metadata allows information passed to individual log entries to be differentiated from the information shared via `Context`. For example, imagine we write the following log entry:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

The written log will contain the `auth_id` passed to the log entry, but it will also contain the context's `url` and `trace_id` as metadata:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Information added to the context is also made available to jobs dispatched to the queue. For example, imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to the context:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

When the job is dispatched, any information currently stored in the context is captured and shared with the job. The captured information is then hydrated back into the current context while the job is executing. So, if our job's handle method was to write to the log:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}
```

The resulting log entry would contain the information that was added to the context during the request that originally dispatched the job:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Although we have focused on the built-in logging related features of Laravel's context, the following documentation will illustrate how context allows you to share information across the HTTP request / queued job boundary and even how to add [hidden context data](#hidden-context) that is not written with log entries.

<a name="capturing-context"></a>
## Capturing Context

You may store information in the current context using the `Context` facade's `add` method:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

To add multiple items at once, you may pass an associative array to the `add` method:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

The `add` method will override any existing value that shares the same key. If you only wish to add information to the context if the key does not already exist, you may use the `addIf` method:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

Context also provides convenient methods for incrementing or decrementing a given key. Both of these methods accept at least one argument: the key to track. A second argument may be provided to specify the amount by which the key should be incremented or decremented:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### Conditional Context

The `when` method may be used to add data to the context based on a given condition. The first closure provided to the `when` method will be invoked if the given condition evaluates to `true`, while the second closure will be invoked if the condition evaluates to `false`:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="scoped-context"></a>
#### Scoped Context

The `scope` method provides a way to temporarily modify the context during the execution of a given callback and restore the context to its original state when the callback finishes executing. Additionally, you can pass extra data that should be merged into the context (as the second and third arguments) while the closure executes.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> [!WARNING]
> If an object within the context is modified inside the scoped closure, that mutation will be reflected outside of the scope.

<a name="stacks"></a>
### Stacks

Context offers the ability to create "stacks", which are lists of data stored in the order that they were added. You can add information to a stack by invoking the `push` method:

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

Stacks can be useful to capture historical information about a request, such as events that are happening throughout your application. For example, you could create an event listener to push to a stack every time a query is executed, capturing the query SQL and duration as a tuple:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

You may determine if a value is in a stack using the `stackContains` and `hiddenStackContains` methods:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

The `stackContains` and `hiddenStackContains` methods also accept a closure as their second argument, allowing more control over the value comparison operation:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## Retrieving Context

You may retrieve information from the context using the `Context` facade's `get` method:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

The `only` and `except` methods may be used to retrieve a subset of the information in the context:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

The `pull` method may be used to retrieve information from the context and immediately remove it from the context:

```php
$value = Context::pull('key');
```

If context data is stored in a [stack](#stacks), you may pop items from the stack using the `pop` method:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

If you would like to retrieve all of the information stored in the context, you may invoke the `all` method:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### Determining Item Existence

You may use the `has` and `missing` methods to determine if the context has any value stored for the given key:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

The `has` method will return `true` regardless of the value stored. So, for example, a key with a `null` value will be considered present:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## Removing Context

The `forget` method may be used to remove a key and its value from the current context:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

You may forget several keys at once by providing an array to the `forget` method:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## Hidden Context

Context offers the ability to store "hidden" data. This hidden information is not appended to logs, and is not accessible via the data retrieval methods documented above. Context provides a different set of methods to interact with hidden context information:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

The "hidden" methods mirror the functionality of the non-hidden methods documented above:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## Events

Context dispatches two events that allow you to hook into the hydration and dehydration process of the context.

To illustrate how these events may be used, imagine that in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture this value during the request and restore it on the queue, ensuring notifications sent on the queue have the correct `app.locale` value. We can use context's events and [hidden](#hidden-context) data to achieve this, which the following documentation will illustrate.

<a name="dehydrating"></a>
### Dehydrating

Whenever a job is dispatched to the queue the data in the context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` method allows you to register a closure that will be invoked during the dehydration process. Within this closure, you may make changes to the data that will be shared with the queued job.

Typically, you should register `dehydrating` callbacks within the `boot` method of your application's `AppServiceProvider` class:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}
```

> [!NOTE]
> You should not use the `Context` facade within the `dehydrating` callback, as that will change the context of the current process. Ensure you only make changes to the repository passed to the callback.

<a name="hydrated"></a>
### Hydrated

Whenever a queued job begins executing on the queue, any context that was shared with the job will be "hydrated" back into the current context. The `Context::hydrated` method allows you to register a closure that will be invoked during the hydration process.

Typically, you should register `hydrated` callbacks within the `boot` method of your application's `AppServiceProvider` class:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> [!NOTE]
> You should not use the `Context` facade within the `hydrated` callback and instead ensure you only make changes to the repository passed to the callback.
