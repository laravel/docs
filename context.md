# Context

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Capturing Context](#capturing-context)

<a name="introduction"></a>
## Introduction

Context enables you to capture and share information about requests, jobs, and commands running in your application. This captured information is shared with logs, giving you further insight into the history that occurred before a log entry was written, and also queued jobs, allowing you to trace execution flows throughout a distributed system.

<a name="how-it-works"></a>
## How it Works

To get started, you may [add information to Context](#capturing-context) by using the `Context` facade. In this example, we use a [middleware](/docs/{{version}}/middleware) to add the request URL and a unique trace ID on every incoming request:

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

Information added to Context is automatically appended as metadata to any [logging](/docs/{{version}}/logging) that you perform throughout the request. This allows information passed to individual log entries to be differentiated from the information shared via Context.

```php
Log::info('User logged in.', ['auth_id' => Auth::id()]);
```

The written log contains the `auth_id` passed to the log entry, but it also contains the `url` and `trace_id` as metadata:

```
User logged in. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Additionally, information added to Context is made available to jobs dispatched to the queue. Imagine we dispatch a `ProcessPodcast` queued job after adding some information to Context:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

When the job is dispatched, any information currently Context is rehydrated into Context when the job executes. If our job's handle method was to write a log entry:

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

The resulting log entry would contain the Context added during the HTTP request:

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Although we have focused on the first-party logging related features of Context, the following documentation will show you that Context allows you to share information across the HTTP request / queued job boundary and even add information that is not shared with log entries by default.
