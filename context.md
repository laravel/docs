# Context

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Capturing Context](#capturing-context)
    - [Stacks](#stacks)
- [Retrieving Context](#retrieving-context)
    - [Determining Item Existence](#determining-item-existence)
- [Removing Context](#removing-context)
- [Hidden Context](#hidden-context)
- [Events](#events)
    - [Dehydrating](#dehydrating)
    - [Hydrating](#hydrating)

<a name="introduction"></a>
## Introduction

Context enables you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is shared with logs, giving you deeper insight into the history that occurred before a log entry was written, and queued jobs, allowing you to trace execution flows throughout a distributed system.

<a name="how-it-works"></a>
### How it Works

The best way to understand Context is to see it in action with the built-in logging features. To get started, you may [add information to Context](#capturing-context) by using the `Context` façade. In this example, we use a [middleware](/docs/{{version}}/middleware) to add the request URL and a unique trace ID on every incoming request:

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

Information added to Context is automatically appended as metadata to any [logging](/docs/{{version}}/logging) that you perform throughout the request. Appending as metadata allows information passed to individual log entries to be differentiated from the information shared via Context.

```php
Log::info('User logged in.', ['auth_id' => Auth::id()]);
```

The written log contains the `auth_id` passed to the log entry, but it also contains the `url` and `trace_id` as metadata:

```
User logged in. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Information added to Context is also made available to jobs dispatched to the queue. Imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to Context:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

When the job is dispatched, any information currently Context is captured and shared with the job, which is then hydrated into Context when the job is executing. If our job's handle method was to write a log entry:

```php
class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

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

The log entry would contain the information added to Context during the request:

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Although we have focused on the built-in logging related features of Context, the following documentation will illustrate that Context allows you to share information across the HTTP request / queued job boundary and even add information that is not shared with log entries by default.

<a name="capturing-context"></a>
## Capturing Context

You may capture information with Context by using the Context facade's `add` method:

```php
Context::add('key', 'value');
```

If you wish to add multiple items at once, you may also pass an associative array to the `add` method:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

The `add` method will override any existing value that shares the same key. If you only wish to add information to Context if the key does not already exist you may use the `addIf` method:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::add('key', 'second');

Context::get('key');
// "second"

Context::addIf('key', 'third');

Context::get('key');
// "second"
```

The `addIf` method will not override the value even when the existing value is `null`:

```php
Context::add('key', null);

Context::get('key');
// null

Context::addIf('key', 'value');
// null
```

<a name="stacks"></a>
### Stacks

Context offers the ability to create "stacks", which are lists of data stored in the order that they where added. You can add information to a stack by calling the `push` method:

```php
Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

Stacks can be useful to capture historical information about a request, such as events that are happening throughout your system. You could, for example, set up an event listener to push to a stack every time a query is executed in your application capturing the query duration and query SQL as a tuple:

```php
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

<a name="retrieving-context"></a>
## Retrieving Context

You may retrieve information for Context by using the `Context` facade's `get` method:

```php
$value = Context::get('key');
```

The `only` method will retrieve a subset of the information in Context:

```php
$data = Context::only(['first_key', 'second_key']);
```

If you wish to retrieve all the information stored in Context, you may use the `all` method:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### Determining Item Existence

You may use the `has` method to determine if Context has any value stored for the given key:

```php
if (Context::has('key')) {
    // ...
}
```

This will return `true` regardless of the value stored, i.e., a key with a `null` value will return `true`:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## Removing Context

The `forget` method removes a key and its value from Context:

```php
Context::add(['first_key' => 'first_value', 'second_key' => 'second_value']);

Context::forget('first_key');

Context::all();

// ['second_key' => 'second_value']
```

You may forget several keys by passing an array:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## Hidden Context

Context offers the ability to store "hidden" information. This hidden information is not appended to logs, unlike what we demonstrated in [how it works](#how-it-works), and is not accessible via the methods above. Context provides a different set of methods to interact with hidden information specifically.

```php
Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

The "hidden" methods mirror the functionality of the non-hidden methods outlined above:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## Events

Context offers two events that allow you to hook into the dehydrating and hydrating process of Context.

To illustrate how these events may be used, imagine in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture the value during the request and restore it on the queue. This will ensure that any notifications sent on the queue also have the correct `app.locale` value. We will use Context's events and [hidden](#hidden-context) information to achieve this.

<a name="dehydrating"></a>
### Dehydrating

Whenever a job is dispatched to the queue the information in Context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` hook allows you to intercept the dehydration process and make changes to the information that will be shared with the queued job.

Typically, you register a callback within the `boot` method of your application's `AppServiceProvider` class:

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
> You should not use the `Context` facade within the callback, as that will change the Context of the current process. Ensure you only make changes to the repository passed to the callback.

<a name="hydrating"></a>
### Hydrating

Whenever a queued job begins executing on the queue, any Context that was shared with the job will be "hydrated" back into Context. The `Context::hydrating` hook allows you to intercept the hydration process when needed. 

Typically, you register a callback within the `boot` method of your application's `AppServiceProvider` class:


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
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> [!NOTE]
> You should not use the `Context` facade within the callback, as that will change the Context of the current process. Ensure you only make changes to the repository passed to the callback.
