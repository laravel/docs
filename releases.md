# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 13](#laravel-13)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^13.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

<a name="named-arguments"></a>
#### Named Arguments

[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future.

<a name="support-policy"></a>
## Support Policy

For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/{{version}}/database#introduction).

<div class="overflow-auto">

| Version | PHP (*)   | Release             | Bug Fixes Until     | Security Fixes Until |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1 - 8.3 | February 14th, 2023 | August 6th, 2024    | February 4th, 2025   |
| 11      | 8.2 - 8.4 | March 12th, 2024    | September 3rd, 2025 | March 12th, 2026     |
| 12      | 8.2 - 8.5 | February 24th, 2025 | August 13th, 2026   | February 24th, 2027  |
| 13      | 8.3 - 8.5 | March 17th, 2026    | Q3 2027             | March 17th, 2028     |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) Supported PHP versions

<a name="laravel-13"></a>
## Laravel 13

Laravel 13 continues Laravel's annual release cadence with a focus on AI-native workflows, stronger defaults, and more expressive developer APIs. This release includes first-party AI primitives, JSON:API resources, semantic / vector search capabilities, and incremental improvements across queues, cache, and security.

<a name="minimal-breaking-changes"></a>
### Minimal Breaking Changes

Much of our focus during this release cycle has been minimizing breaking changes. Instead, we have dedicated ourselves to shipping continuous quality-of-life improvements throughout the year that do not break existing applications.

Therefore, the Laravel 13 release is a relatively minor upgrade in terms of effort, while still delivering substantial new capabilities. In light of this, most Laravel applications may upgrade to Laravel 13 without changing much application code.

<a name="php-8"></a>
### PHP 8.3

Laravel 13.x requires a minimum PHP version of 8.3.

<a name="ai-sdk"></a>
### Laravel AI SDK

Laravel 13 introduces the first-party [Laravel AI SDK](https://laravel.com/ai), providing a unified API for text generation, tool-calling agents, embeddings, audio, images, and vector-store integrations.

With the AI SDK, you can build provider-agnostic AI features while keeping a consistent, Laravel-native developer experience.

For example, a basic agent can be prompted with a single call:

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

The Laravel AI SDK can also generate images, audio, and embeddings:

For visual generation use cases, the SDK offers a clean API for creating images from plain-language prompts:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

For voice experiences, you can synthesize natural-sounding audio from text for assistants, narrations, and accessibility features:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

And for semantic search and retrieval workflows, you can generate embeddings directly from strings:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a name="json-api"></a>
### JSON:API Resources

Laravel now includes first-party [JSON:API resources](/docs/{{version}}/eloquent-resources#jsonapi-resources), making it straightforward to return responses compliant with the JSON:API specification.

JSON:API resources handle resource object serialization, relationship inclusion, sparse fieldsets, links, and JSON:API-compliant response headers.

<a name="request-forgery-protection"></a>
### Request Forgery Protection

For security, Laravel's [request forgery protection](/docs/{{version}}/csrf#preventing-csrf-requests) middleware has been enhanced and formalized as `PreventRequestForgery`, adding origin-aware request verification while preserving compatibility with token-based CSRF protection.

<a name="queue-routing"></a>
### Queue Routing

Laravel 13 adds [queue routing by class](/docs/{{version}}/queues#queue-routing) via `Queue::route(...)`, allowing you to define default queue / connection routing rules for specific jobs in a central place:

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a name="php-attributes"></a>
### Expanded PHP Attributes

Laravel 13 continues to expand first-party PHP attribute support across the framework, making common configuration and behavioral concerns more declarative and colocated with your classes and methods.

Notable additions include controller and authorization attributes like [`#[Middleware]`](/docs/{{version}}/controllers#controller-middleware) and [`#[Authorize]`](/docs/{{version}}/controllers#authorization-attributes), as well as queue-oriented job controls like [`#[Tries]`](/docs/{{version}}/queues#max-job-attempts-and-timeout), [`#[Backoff]`](/docs/{{version}}/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/{{version}}/queues#max-job-attempts-and-timeout), and [`#[FailOnTimeout]`](/docs/{{version}}/queues#failing-on-timeout).

For example, controller middleware and policy checks can now be declared directly on classes and methods:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}
```

Additional attributes have also been introduced across Eloquent, events, notifications, validation, testing, and resource serialization APIs, giving you a consistent attribute-first option in more areas of the framework.

<a name="cache-touch"></a>
### Cache TTL Extension

Laravel now includes [`Cache::touch(...)`](/docs/{{version}}/cache), which lets you extend an existing cache item's TTL without retrieving and re-storing its value.

<a name="semantic-search"></a>
### Semantic / Vector Search

Laravel 13 deepens its semantic search story with native vector query support, embedding workflows, and related APIs documented across [search](/docs/{{version}}/search#semantic-vector-search), [queries](/docs/{{version}}/queries#vector-similarity-clauses), and the [AI SDK](/docs/{{version}}/ai-sdk#embeddings).

These features make it straightforward to build AI-powered search experiences using PostgreSQL + `pgvector`, including similarity search against embeddings generated directly from strings.

For example, you may run semantic similarity searches directly from the query builder:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```
