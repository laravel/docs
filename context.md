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

<a name="introduction"></a>
## Introduction

Context enables you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is shared with logs, giving you deeper insight into the history that occurred before a log entry was written, and queued jobs, allowing you to trace execution flows throughout a distributed system.

<a name="how-it-works"></a>
### How it Works

The best way to understand Context is to see it in action with the built-in logging features. To get started, you may [add information to Context](#capturing-context) by using the `Context` facade. In this example, we use a [middleware](/docs/{{version}}/middleware) to add the request URL and a unique trace ID on every incoming request:

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

When the job is dispatched, any information currently Context is captured and shared with the job, which is then rehydrated into Context when the job is executing. If our job's handle method was to write a log entry:

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

The `add` method will override any existing value that shares the same key. If you only wish to add information to Context if the key does not already exist you may use the `addIf` method.

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

<a name="determining-item-existence"></a>
### Determining Item Existence

You may use the `has` method to determine if Context has any value stored for the given key.

```php
if (Context::has('key')) {
    // ...
}
```

This will return `true` regardless of the value stored, i.e., a key with a `null` value will return `true`.

```php
Context::add('key', null);

Context::has('key');
// true
```
