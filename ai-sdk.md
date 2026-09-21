# Laravel AI SDK

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Custom Base URLs](#custom-base-urls)
    - [OpenAI-Compatible Providers](#openai-compatible-providers)
    - [Provider Support](#provider-support)
- [Agents](#agents)
    - [Prompting](#prompting)
    - [Conversation Context](#conversation-context)
    - [Structured Output](#structured-output)
    - [Attachments](#attachments)
    - [Streaming](#streaming)
    - [Broadcasting](#broadcasting)
    - [Queueing](#queueing)
    - [Tools](#tools)
    - [Deferred Tool Loading](#deferred-tool-loading)
    - [File Storage Tools](#file-storage-tools)
    - [MCP Tools](#mcp-tools)
    - [Provider Tools](#provider-tools)
    - [Sub-Agents](#sub-agents)
    - [Middleware](#middleware)
    - [Anonymous Agents](#anonymous-agents)
    - [Agent Configuration](#agent-configuration)
    - [Provider Options](#provider-options)
    - [Prompt Caching](#prompt-caching)
- [Human Tool Approval](#human-tool-approval)
    - [Complete Approval Flow](#complete-approval-flow)
- [Images](#images)
- [Audio (TTS)](#audio)
- [Transcription (STT)](#transcription)
- [Text Summarization](#text-summarization)
- [Embeddings](#embeddings)
    - [Multimodal Embeddings](#multimodal-embeddings)
    - [Querying Embeddings](#querying-embeddings)
    - [Caching Embeddings](#caching-embeddings)
- [Reranking](#reranking)
- [Classification](#classification)
- [Files](#files)
- [Vector Stores](#vector-stores)
    - [Adding Files to Stores](#adding-files-to-stores)
- [Usage](#usage)
- [Failover](#failover)
- [Testing](#testing)
    - [Agents](#testing-agents)
    - [Images](#testing-images)
    - [Audio](#testing-audio)
    - [Transcriptions](#testing-transcriptions)
    - [Embeddings](#testing-embeddings)
    - [Reranking](#testing-reranking)
    - [Classification](#testing-classification)
    - [Files](#testing-files)
    - [Vector Stores](#testing-vector-stores)
- [Events](#events)

<a name="introduction"></a>
## Introduction

The [Laravel AI SDK](https://github.com/laravel/ai) provides a unified, expressive API for interacting with AI providers such as OpenAI, Anthropic, Gemini, and more. With the AI SDK, you can build intelligent agents with tools and structured output, generate images, synthesize and transcribe audio, create vector embeddings, and much more — all using a consistent, Laravel-friendly interface.

<a name="installation"></a>
## Installation

You can install the Laravel AI SDK via Composer:

```shell
composer require laravel/ai
```

Next, you should publish the AI SDK configuration and migration files using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

Finally, you should run your application's database migrations. This will create a `agent_conversations` and `agent_conversation_messages` table that the AI SDK uses to power its conversation storage:

```shell
php artisan migrate
```

<a name="configuration"></a>
### Configuration

You may define your AI provider credentials in your application's `config/ai.php` configuration file or as environment variables in your application's `.env` file:

```ini
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
COHERE_API_KEY=
DEEPSEEK_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_URL=
OPENROUTER_API_KEY=
JINA_API_KEY=
TYPESAFE_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```

The default models used for text, images, audio, transcription, and embeddings may also be configured in your application's `config/ai.php` configuration file.

<a name="custom-base-urls"></a>
### Custom Base URLs

By default, the Laravel AI SDK connects directly to each provider's public API endpoint. However, you may need to route requests through a different endpoint - for example, when using a proxy service to centralize API key management, implement rate limiting, or route traffic through a corporate gateway.

You may configure custom base URLs by adding a `url` parameter to your provider configuration:

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```

This is useful when routing requests through a proxy service (such as LiteLLM or Azure OpenAI Gateway) or using alternative endpoints.

Custom base URLs are supported for the following providers: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, and OpenRouter.

<a name="openai-compatible-providers"></a>
### OpenAI-Compatible Providers

If you are using an OpenAI-compatible API, such as LM Studio, vLLM, Together, Fireworks, or a local gateway, you may configure an `openai-compatible` provider. The `url` option is required, while the `key` option is optional and will be sent as a bearer token when present:

```php
'providers' => [
    'local' => [
        'driver' => 'openai-compatible',
        'url' => env('LOCAL_AI_URL'),
        'key' => env('LOCAL_AI_API_KEY'),
    ],
],
```

Once configured, you may use the named provider like any other provider:

```php
agent()->prompt('What is Laravel?', provider: 'local', model: 'local-model');
```

You may also configure a default text model for the provider so that you do not need to pass a model explicitly:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'text' => [
            'default' => env('LOCAL_AI_MODEL'),
        ],
    ],
],
```

You may add custom HTTP headers to every outgoing request for the provider by defining a `headers` array in its configuration. This is useful when an endpoint requires an additional identifying or authentication header beyond the bearer token:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'headers' => [
        'X-Tenant-Id' => env('LOCAL_AI_TENANT_ID'),
    ],
],
```

OpenAI-compatible providers support text generation, streaming, tools, structured output, image attachments, embeddings, and transcription. If your endpoint requires additional request body fields, provide them using [provider options](#provider-options).

<a name="openai-compatible-embeddings"></a>
#### OpenAI-Compatible Embeddings

Since arbitrary endpoints have no known models, you must configure a default embeddings model to use `embeddings()` with an OpenAI-compatible provider. You may also configure a fixed dimensions value; if omitted, the request is sent without a `dimensions` parameter and the model's native dimensions are used.

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'embeddings' => [
            'default' => 'text-embedding-qwen3-embedding-0.6b',
            'dimensions' => 1024, // optional
        ],
    ],
],
```

<a name="openai-compatible-transcriptions"></a>
#### OpenAI-Compatible Transcriptions

Likewise, you must configure a default transcription model to use `Transcription` with an OpenAI-compatible provider. The audio will be uploaded to the endpoint's `/audio/transcriptions` route as a standard multipart request:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'transcription' => [
            'default' => 'whisper-1',
        ],
    ],
],
```

> [!NOTE]
> OpenAI-compatible and Groq providers do not support diarization. Invoking the `diarize` method when using these providers will throw an exception.

<a name="provider-support"></a>
### Provider Support

The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature:

<div class="overflow-auto">

| Feature | Providers |
|---|---|
| Text | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| Images | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter |
| TTS | OpenAI, ElevenLabs, Gemini, Mistral |
| STT | OpenAI, OpenAI Compatible, ElevenLabs, Groq, Mistral, Gemini |
| Embeddings | OpenAI, OpenAI Compatible, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |
| Reranking | Cohere, Jina, VoyageAI, Bedrock, OpenRouter |
| Classification | TypeSafe, OpenRouter |
| Files | OpenAI, Anthropic, Gemini, Azure, OpenRouter |

</div>

The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings:

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::OpenAiCompatible;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## Agents

Agents are the fundamental building block for interacting with AI providers in the Laravel AI SDK. Each agent is a dedicated PHP class that encapsulates the instructions, conversation context, tools, and output schema needed to interact with a large language model. Think of an agent as a specialized assistant — a sales coach, a document analyzer, a support bot — that you configure once and prompt as needed throughout your application.

You can create an agent via the `make:agent` Artisan command:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

Within the generated agent class, you can define the system prompt / instructions, message context, available tools, and output schema (if applicable):

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\RetrievePreviousTranscripts;
use App\Models\History;
use App\Models\User;
use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Messages\Message;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * Get the list of messages comprising the conversation so far.
     */
    public function messages(): iterable
    {
        return History::where('user_id', $this->user->id)
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->map(function ($message) {
                return new Message($message->role, $message->content);
            })->all();
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RetrievePreviousTranscripts,
        ];
    }

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'feedback' => $schema->string()->required(),
            'score' => $schema->integer()->min(1)->max(10)->required(),
        ];
    }
}
```

<a name="prompting"></a>
### Prompting

To prompt an agent, first create an instance using the `make` method or standard instantiation, then call `prompt`:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

The `make` method resolves your agent from the container, allowing automatic dependency injection. You may also pass arguments to the agent's constructor:

```php
$agent = SalesCoach::make(user: $user);
```

By passing additional arguments to the `prompt` method, you may override the default provider, model, or HTTP timeout when prompting:

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 120,
);
```

<a name="raw-http-responses"></a>
#### Raw HTTP Responses

Every response returned from a text-generating agent exposes the raw HTTP response from the underlying provider API call via a `raw` property. This gives you access to provider-specific information that isn't part of the AI SDK's generic response - rate-limit headers, request IDs, or other exact payload fields:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->raw; // Illuminate\Http\Client\Response|null

$response->raw->header('X-RateLimit-Remaining-Requests');
$response->raw->json('id');
```

In a tool-call loop, each step retains the raw response of its own request:

```php
foreach ($response->steps as $step) {
    $step->raw?->header('X-RateLimit-Remaining-Requests');
}
```

> **Note:** The `raw` property is `null` when streaming a response, when using the Bedrock provider (which performs its API calls via the AWS SDK instead of an HTTP client), and on faked responses unless one is provided explicitly via `withRawResponse`.

<a name="conversation-context"></a>
### Conversation Context

If your agent implements the `Conversational` interface, you may use the `messages` method to return the previous conversation context, if applicable:

```php
/**
 * Get the list of messages comprising the conversation so far.
 */
public function messages(): iterable
{
    return $this->user->history->map(fn ($message) => new Message(
        $message->role, $message->content,
    ))->all();
}
```

If your agent does not implement the `Conversational` interface, you may use the `withMessages` method to provide the conversation history for a single run, such as a history posted by your application's frontend:

```php
use Laravel\Ai\Messages\Message;

$response = (new SalesCoach)
    ->withMessages([
        new Message('user', 'Analyze this sales transcript...'),
        new Message('assistant', 'The rep never asked for the close.'),
    ])
    ->prompt('What should they say next time?');
```

Agents that implement the `Conversational` interface load their own history, so combining the two approaches will throw a `LogicException`.

<a name="remembering-conversations"></a>
#### Remembering Conversations

> **Warning:** Before using the `RemembersConversations` trait, you should publish and run the AI SDK migrations using the `vendor:publish` Artisan command. These migrations will create the necessary database tables to store conversations.

If you would like Laravel to automatically store and retrieve conversation history for your agent, you may use the `RemembersConversations` trait. This trait provides a simple way to persist conversation messages to the database without manually implementing the `Conversational` interface:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, Conversational
{
    use Promptable, RemembersConversations;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

When using the `RemembersConversations` trait, do not manually define a `messages` method in your agent class. If a `messages` method is present, it will take precedence over the trait's implementation and conversation history will not be loaded from the database.

To start a new conversation for a user, call the `forUser` method before prompting:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

The conversation ID is returned on the response and can be stored for future reference. If you would like to retrieve all of a user's conversations using Eloquent, you may add the `HasConversations` trait to your user model:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Ai\Concerns\HasConversations;

class User extends Authenticatable
{
    use HasConversations;
}
```

Once the trait has been added to your model, you may retrieve and query the user's conversations via the `conversations` relationship:

```php
$conversations = $user->conversations()
    ->latest('updated_at')
    ->paginate(20);
```

To continue an existing conversation, use the `continue` method:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

The `continueOrStart` method may be used to continue the given conversation, or start a new conversation if the given ID is `null`:

```php
$response = (new SalesCoach)
    ->continueOrStart($conversationId, as: $user)
    ->prompt('Hello!');
```

When using the `RemembersConversations` trait, previous messages are automatically loaded and included in the conversation context when prompting. New messages (both user and assistant) are automatically stored after each interaction. Each response also contains the IDs of the conversation and messages that were stored:

```php
$response->conversationId;
$response->userMessageId;
$response->assistantMessageId;
```

<a name="conversation-participants"></a>
#### Conversation Participants

Although users are the most common conversation participants, conversations may belong to any Eloquent model. Use the `forParticipant` method to start a conversation for another type of model:

```php
$response = (new SalesCoach)
    ->forParticipant($team)
    ->prompt('Review our latest sales results.');
```

The participant's morph class and primary key are stored with the conversation. Therefore, models of different types that have the same primary key, such as `User` ID `1` and `Team` ID `1`, have separate conversation histories. The `forUser` method is an alias for `forParticipant`.

You may continue the participant's most recent conversation with the agent using the `continueLastConversation` method. Conversations are scoped to the agent, so only conversations that the agent participated in will be continued:

```php
$response = (new SalesCoach)
    ->continueLastConversation($team)
    ->prompt('Tell me more about that.');
```

When continuing a specific conversation, pass the participant to the `continue` method:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $team)
    ->prompt('Tell me more about that.');
```

The `HasConversations` trait may be added to any Eloquent model that participates in conversations. The resulting `conversations` relationship is a polymorphic relationship scoped to that model's type and primary key. You may also access the participant that owns a conversation through its inverse relationship:

```php
$conversations = $team->conversations;

$participant = $conversation->participant;
```

If your application uses multiple participant model types, you should consider defining an [Eloquent morph map](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types) so that stored participant types are not coupled to your model class names.

> [!WARNING]
> The `continue` and `continueOrStart` methods do not verify that the given participant owns the conversation. Your application should authorize access to the conversation before continuing it.

<a name="inspecting-stored-conversations"></a>
#### Inspecting Stored Conversations

When rendering a conversation, you typically need more information than the messages that are sent to the model. You may resolve the conversation store from the service container to read the stored messages without querying the AI SDK's tables directly:

```php
use Laravel\Ai\Contracts\ConversationStore;

$store = app(ConversationStore::class);
```

Messages are paginated newest first using a cursor and are returned as `StoredMessage` instances, which contain each message's ID, timestamps, usage, metadata, and attachments:

```php
$messages = $store->paginateConversationMessages($conversationId, perPage: 25);

foreach ($messages as $message) {
    $message->id;
    $message->role;
    $message->content;
    $message->createdAt;
    $message->usage;
}
```

Each turn is stored as a list of steps, with one step per round-trip to the provider, and each tool result is recorded on the tool call that produced it. The `toolCalls`, `providerToolCalls`, and `toolResults` methods flatten these steps in order, so you do not need to traverse them yourself:

```php
$message->steps;

$message->toolCalls();
$message->providerToolCalls();
$message->toolResults();
```

A tool call contains a `result` once it has been executed. Tool calls that contain an `approval_reason` but no `result` are still awaiting a [tool approval](#human-tool-approval), while the `approvalRequestedAt` property contains the time the turn was paused.

Before continuing a conversation ID provided by your application's frontend, you should verify that the conversation was stored for the given participant:

```php
abort_unless($store->conversationBelongsTo(
    $conversationId, $user->getMorphClass(), $user->getKey()
), 403);
```

If the most recent turn is paused awaiting [tool approval](#human-tool-approval), you may render its pending tool calls after a page reload without resuming the run:

```php
foreach ($store->pendingApprovalsFor($conversationId) as $approval) {
    // $approval->id, $approval->tool, $approval->arguments, $approval->reason...
}
```

These methods are defined by the `PaginatesConversations`, `VerifiesConversationOwnership`, and `ResolvesPendingApprovals` contracts. The included database store implements all three, while a custom store may implement only the contracts it needs.

<a name="structured-output"></a>
### Structured Output

If you would like your agent to return structured output, implement the `HasStructuredOutput` interface, which requires that your agent define a `schema` method:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

When prompting an agent that returns structured output, you can access the returned `StructuredAgentResponse` like an array:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="structured-output-nested-objects"></a>
#### Nested Objects

To define nested structured output, use the `object` method with a closure:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
            'metadata' => $schema->object(fn ($schema) => [
                'confidence' => $schema->string()->enum(['low', 'medium', 'high'])->required(),
                'language' => $schema->string()->required(),
            ])->required(),
        ];
    }
}
```

<a name="structured-output-arrays-of-objects"></a>
#### Arrays of Objects

If your agent should return a list of structured items, combine the `array` and `object` methods:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'feedback' => $schema->array()
            ->items(
                $schema->object(fn ($schema) => [
                    'comment' => $schema->string()->required(),
                    'score' => $schema->integer()->required(),
                ])
            )
            ->required(),
    ];
}
```

If a value may match one of several schemas, use the `anyOf` method:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'content' => $schema->anyOf([
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['article'])->required(),
                'title' => $schema->string()->required(),
            ]),
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['image'])->required(),
                'url' => $schema->string()->required(),
            ]),
        ])->required(),
    ];
}
```

<a name="attachments"></a>
### Attachments

When prompting, you may also pass attachments with the prompt to allow the model to inspect images and documents:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // Attach a document from a filesystem disk...
        Files\Document::fromPath('/home/laravel/transcript.md'), // Attach a document from a local path...
        $request->file('transcript'), // Attach an uploaded file...
    ]
);
```

Likewise, the `Laravel\Ai\Files\Image` class may be used to attach images to a prompt:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'), // Attach an image from a filesystem disk...
        Files\Image::fromPath('/home/laravel/photo.jpg'), // Attach an image from a local path...
        $request->file('photo'), // Attach an uploaded file...
    ]
);
```

<a name="streaming"></a>
### Streaming

You may stream an agent's response by invoking the `stream` method. The returned `StreamableAgentResponse` may be returned from a route to automatically send a streaming response (SSE) to the client:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

The `then` method may be used to provide a closure that will be invoked when the entire response has been streamed to the client:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage...
        });
});
```

Alternatively, you may iterate through the streamed events manually:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

The response also contains the model's reasoning and any sources it cited. Both are stored with the assistant message when using the `RemembersConversations` trait:

```php
use Laravel\Ai\Responses\StreamedAgentResponse;

(new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->then(function (StreamedAgentResponse $response) {
        $response->reasoning; // '' unless the model returned reasoning text...
        $response->meta->citations;
    });
```

Reasoning is available on responses returned by the `prompt` method as well, so a response does not need to be streamed in order to inspect it.

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
<a name="stream-protocols"></a>
#### Stream Protocols

By default, a streamed response emits the AI SDK's own events. However, you may instruct the response to use a frontend streaming protocol instead.

You may stream the events using the [Vercel AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol) by invoking the `usingVercelDataProtocol` method on the streamable response:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

You may pass a message ID if your application's frontend assigns its own:

```php
->usingVercelDataProtocol($request->string('messageId'));
```

Likewise, the `usingAgentUserInteractionProtocol` method may be used to stream the [Agent User Interaction (AG-UI) protocol](https://docs.ag-ui.com), which is supported by clients such as CopilotKit:

```php
Route::post('/coach', function (Request $request) {
    return (new SalesCoach)
        ->forUser($request->user())
        ->stream($request->string('prompt'))
        ->usingAgentUserInteractionProtocol();
});
```

Both of the method's arguments are optional and default to the conversation ID and the invocation ID:

```php
->usingAgentUserInteractionProtocol(
    threadId: $request->input('threadId'),
    runId: $request->input('runId'),
);
```

To use a protocol that the AI SDK does not implement, you may pass your own `Laravel\Ai\Streaming\Protocols\StreamProtocol` implementation to the `usingProtocol` method:

```php
use App\Ai\Protocols\CustomProtocol;

return (new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->usingProtocol(new CustomProtocol);
```

<a name="chat-requests"></a>
#### Chat Requests

Frontends that use these protocols post their entire conversation history, the newest user message, and any tool approval responses. The `Vercel` and `AgentUserInteraction` classes may be used to convert such a request into a chat that agents accept directly:

```php
use Laravel\Ai\Vercel\Vercel;

Route::post('/chat', function (Request $request) {
    $chat = Vercel::chat($request);

    return (new SupportAgent)
        ->withMessages($chat->history())
        ->stream($chat)
        ->usingProtocol($chat->protocol());
});
```

If the request contains [approval decisions](#human-tool-approval), the agent will resume using them. Otherwise, the agent is prompted with the request's newest user message and attachments. The `protocol` method returns the protocol used by the client. Agents that implement the `Conversational` interface load their own history, so the `withMessages` method may be omitted.

The `AgentUserInteraction::chat` method provides the same API for AG-UI clients, in addition to the request's thread and run IDs:

```php
use Laravel\Ai\AgentUserInteraction\AgentUserInteraction;

$chat = AgentUserInteraction::chat($request);

$chat->threadId();
$chat->runId();
```

Stored messages may also be converted back into the format a client expects, allowing you to hydrate a conversation the client did not stream. The `AgentUserInteraction::toClientState` method additionally returns any pending approval interrupts:

```php
$messages = $conversation->messages()->oldest()->get();

return ['messages' => Vercel::toUiMessages($messages)];

return AgentUserInteraction::toClientState($messages);
```

<a name="broadcasting"></a>
### Broadcasting

You may broadcast streamed events in a few different ways. First, you can simply invoke the `broadcast` or `broadcastNow` method on a streamed event:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

Or, you can invoke an agent's `broadcastOnQueue` method to queue the agent operation and broadcast the streamed events as they are available:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="skipping-oversized-events"></a>
#### Skipping Oversized Events

Some broadcasting platforms limit WebSocket messages to around 10KB. Data-heavy stream events, like large tool results, can exceed this limit and cause broadcasting to fail. You may exclude specific event types from broadcasting using the `WithoutBroadcasting` attribute:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\WithoutBroadcasting;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;
use Laravel\Ai\Streaming\Events\ToolCall;
use Laravel\Ai\Streaming\Events\ToolResult;

#[WithoutBroadcasting(ToolCall::class, ToolResult::class)]
class SearchAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```

The excluded events are never broadcast, but they are still persisted to the `agent_conversation_messages` table, so your frontend can load the full tool data after the stream completes. This works for both queued (`broadcastOnQueue`) and synchronous (`broadcast` / `broadcastNow`) broadcasting.

<a name="queueing"></a>
### Queueing

Using an agent's `queue` method, you may prompt the agent, but allow it to process the response in the background, keeping your application feeling fast and responsive. The `then` and `catch` methods may be used to register closures that will be invoked when a response is available or if an exception occurs:

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    (new SalesCoach)
        ->queue($request->input('transcript'))
        ->then(function (AgentResponse $response) {
            // ...
        })
        ->catch(function (Throwable $e) {
            // ...
        });

    return back();
});
```

<a name="tools"></a>
### Tools

Tools may be used to give agents additional functionality that they can utilize while responding to prompts. Tools can be created using the `make:tool` Artisan command:

```shell
php artisan make:tool RandomNumberGenerator
```

The generated tool will be placed in your application's `app/Ai/Tools` directory. Each tool contains a `handle` method that will be invoked by the agent when it needs to utilize the tool:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class RandomNumberGenerator implements Tool
{
    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'min' => $schema->integer()->min(0)->required(),
            'max' => $schema->integer()->required(),
        ];
    }
}
```

Once you have defined your tool, you may return it from the `tools` method of any of your agents:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        new RandomNumberGenerator,
    ];
}
```

<a name="runtime-tool-overrides"></a>
#### Runtime Tool Overrides

The `withTools` method may be used to replace the tools declared by an agent instance. This is useful for per-tenant or feature flagged tool sets:

```php
$response = (new SupportAgent)
    ->withTools([new LookupOrder])
    ->prompt('Where is order 12345?');
```

You may also pass a closure, which receives the agent's declared tools, allowing you to append to or filter them:

```php
$response = (new SupportAgent)
    ->withTools(fn (array $tools) => [...$tools, new LookupOrder])
    ->prompt('Where is order 12345?');
```

<a name="validating-tool-arguments"></a>
#### Validating Tool Arguments

Although your tool's schema constrains the arguments a model may provide, you may validate the incoming arguments using the request's `validate` method:

```php
public function handle(Request $request): Stringable|string
{
    $validated = $request->validate([
        'city' => 'required|string',
        'days' => 'required|integer|max:7',
    ]);

    return $this->forecast($validated['city'], $validated['days']);
}
```

When validation fails, the validation messages are returned to the model as the tool's result, allowing it to correct the arguments and call the tool again.

<a name="repairing-tool-calls"></a>
#### Repairing Tool Calls

Use the `RepairToolCalls` attribute to let an agent recover when a model calls an unknown local tool. Laravel returns the failed call to the model with the names of the available local tools, allowing it to correct the call:

```php
use Laravel\Ai\Attributes\RepairToolCalls;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

#[RepairToolCalls]
class SupportAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```

When Laravel derives the maximum number of steps automatically, this attribute adds one step for the repaired call. Explicit `MaxSteps` limits are unchanged.

<a name="similarity-search"></a>
#### Similarity Search

The `SimilaritySearch` tool allows agents to search for documents similar to a given query using vector embeddings stored in your database. This is useful for retrieval-augmented generation (RAG) when you want to give agents access to search your application's data.

The simplest way to create a similarity search tool is using the `usingModel` method with an Eloquent model that has vector embeddings:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        SimilaritySearch::usingModel(Document::class, 'embedding'),
    ];
}
```

The first argument is the Eloquent model class, and the second argument is the column containing the vector embeddings.

You may also provide a minimum similarity threshold between `0.0` and `1.0` and a closure to customize the query:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

For more control, you may create a similarity search tool with a custom closure that returns the search results:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        new SimilaritySearch(using: function (string $query) {
            return Document::query()
                ->where('user_id', $this->user->id)
                ->whereVectorSimilarTo('embedding', $query)
                ->limit(10)
                ->get();
        }),
    ];
}
```

You may customize the tool's description using the `withDescription` method:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="deferred-tool-loading"></a>
### Deferred Tool Loading

By default, every tool an agent exposes is sent to the provider with each request. When an agent provides a large number of tools, this consumes tokens and may reduce the accuracy of the model's tool selection. Using the `ToolSearch` provider tool with OpenAI or Anthropic, you may defer tool definitions so that the provider only loads them when they are needed:

```php
use App\Ai\Tools\RefundOrder;
use App\Ai\Tools\SearchInvoices;
use App\Ai\Tools\Weather;
use Laravel\Ai\Providers\Tools\ToolSearch;

public function tools(): iterable
{
    return [
        new Weather,
        new ToolSearch(tools: [
            new SearchInvoices,
            new RefundOrder,
        ]),
    ];
}
```

The wrapped tools do not require any modification. The provider will search for and load them when they are relevant to the prompt, after which the agent may call them like any other tool.

When using Anthropic, the `strategy` argument may be used to determine how the provider should search for deferred tools. The supported strategies are `regex` (default) and `bm25`:

```php
new ToolSearch(tools: [new SearchInvoices], strategy: 'bm25'),
```

When using Anthropic, additional provider-specific options may be passed to the search tool using the `withProviderOptions` method:

```php
(new ToolSearch(tools: [new SearchInvoices]))
    ->withProviderOptions(['cache_control' => ['type' => 'ephemeral']]),
```

> [!WARNING]
> Providers that do not support tool search will throw an exception rather than silently discarding the deferred tools. In addition, Anthropic requires that at least one tool is provided outside of the `ToolSearch` wrapper.

<a name="file-storage-tools"></a>
### File Storage Tools

The `FileStorage` tool factory allows you to give agents access to a Laravel [filesystem disk](/docs/{{version}}/filesystem). The `all` method returns tools that allow the agent to list, read, inspect, generate URLs for, write, delete, and copy files on the given disk:

```php
use Laravel\Ai\Tools\FileStorage;

public function tools(): iterable
{
    return FileStorage::all('local');
}
```

If your agent should only be able to inspect files, use the `readOnly` method:

```php
return FileStorage::readOnly('local');
```

These methods return an `Illuminate\Support\Collection`, allowing you to further filter the tools that are provided to the agent:

```php
use Laravel\Ai\Tools\Filesystem\DeleteFile;

return FileStorage::all('s3')
    ->reject(fn ($tool) => $tool instanceof DeleteFile);
```

<a name="mcp-tools"></a>
### MCP Tools

If your application uses [Laravel MCP](/docs/{{version}}/mcp), you may give your agents tools exposed by [Model Context Protocol](https://modelcontextprotocol.io) servers. Using the [Laravel MCP client](/docs/{{version}}/mcp#client), you may connect to a remote or local MCP server and pass its tools directly to your agent.

> [!NOTE]
> MCP tools require the [Laravel MCP](/docs/{{version}}/mcp) package to be installed in your application.

Because an MCP client's `tools` method returns a collection, spread it into your agent's `tools` array using the `...` operator:

```php
use App\Ai\Tools\RandomNumberGenerator;
use Laravel\Mcp\Client;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        ...Client::web('https://mcp.example.com')
            ->withToken($token)
            ->tools(),

        new RandomNumberGenerator,
    ];
}
```

The AI SDK automatically wraps each MCP tool so the agent can call it like any other tool. You may also use a [named MCP client](/docs/{{version}}/mcp#named-clients):

```php
use Laravel\Mcp\Facades\Mcp;

public function tools(): iterable
{
    return [
        ...Mcp::client('github')->tools(),
    ];
}
```

Or connect to a [local MCP server](/docs/{{version}}/mcp#client-connecting):

```php
use Laravel\Mcp\Client;

public function tools(): iterable
{
    return [
        ...Client::local('php', ['artisan', 'mcp:start'])->tools(),
    ];
}
```

For more information on creating and authenticating MCP clients, including bearer tokens and OAuth, consult the [MCP client documentation](/docs/{{version}}/mcp#client).

<a name="provider-tools"></a>
### Provider Tools

Provider tools are special tools implemented natively by AI providers, offering capabilities like web searching, URL fetching, and file searching. Unlike regular tools, provider tools are executed by the provider itself rather than your application.

Provider tools can be returned by your agent's `tools` method.

<a name="web-search"></a>
#### Web Search

The `WebSearch` provider tool allows agents to search the web for real-time information. This is useful for answering questions about current events, recent data, or topics that may have changed since the model's training cutoff.

**Supported providers:** Anthropic, OpenAI, Azure, Gemini, xAI, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

You may configure the web search tool to limit the number of searches or restrict results to specific domains:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

To refine search results based on user location, use the `location` method:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### Web Fetch

The `WebFetch` provider tool allows agents to fetch and read the contents of web pages. This is useful when you need the agent to analyze specific URLs or retrieve detailed information from known web pages.

**Supported providers:** Anthropic, Gemini, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

You may configure the web fetch tool to limit the number of fetches or restrict to specific domains:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### File Search

The `FileSearch` provider tool allows agents to search through [files](#files) stored in [vector stores](#vector-stores). This enables retrieval-augmented generation (RAG) by allowing the agent to search your uploaded documents for relevant information.

**Supported providers:** OpenAI, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

You may provide multiple vector store IDs to search across multiple stores:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

If your files have [metadata](#adding-files-to-stores), you may filter the search results by providing a `where` argument. For simple equality filters, pass an array:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

For more complex filters, you may pass a closure that receives a `FileSearchQuery` instance:

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="code-execution"></a>
#### Code Execution

The `CodeExecution` provider tool allows agents to run code in a sandbox hosted by the AI provider. This is useful for performing calculations and analyzing data.

**Supported providers:** Anthropic, OpenAI, Azure, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\CodeExecution;

public function tools(): iterable
{
    return [new CodeExecution];
}
```

When using OpenAI or Azure, you may make [stored files](#files) available to the sandbox via provider options:

```php
(new CodeExecution)->withProviderOptions([
    'container' => ['type' => 'auto', 'file_ids' => ['file_123']],
]);
```

<a name="sub-agents"></a>
### Sub-Agents

Agents may also be returned from another agent's `tools` method. When an agent is returned as a tool, the parent agent may delegate a specific task to the sub-agent and use the sub-agent's response while answering the original prompt. This is useful when a general-purpose agent needs access to specialized agents with their own instructions, tools, model configuration, or provider preferences.

For example, a customer support agent could delegate refund eligibility questions to a dedicated refunds agent:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

class CustomerSupportAgent implements Agent, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You help customers with account, order, and billing questions. Delegate refund policy questions to the refunds specialist.';
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RefundsAgent,
        ];
    }
}
```

To customize how the sub-agent is exposed to the parent agent, implement the `CanActAsTool` interface on the sub-agent and define a tool-facing name and description:

```php
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Contracts\CanActAsTool;
use Laravel\Ai\Enums\Lab;

#[Provider(Lab::Anthropic)]
class RefundsAgent implements Agent, CanActAsTool, HasTools
{
    /**
     * Get the agent's tool name.
     */
    public function name(): string
    {
        return 'refunds_specialist';
    }

    /**
     * Get the agent's tool description.
     */
    public function description(): string
    {
        return 'Determine whether an order is eligible for a refund and explain the next step.';
    }

    // ...
}
```

If a sub-agent does not implement `CanActAsTool`, Laravel will use the agent's class basename as the tool name and a generic description that asks the parent agent to pass a clear, self-contained task description. Each sub-agent invocation runs in isolation and does not receive the parent agent's conversation history.

When the parent agent is [streaming](#streaming), its sub-agents stream as well. The parent agent emits `ToolResult` events containing the text the sub-agent has produced so far. These events are marked as preliminary and are followed by the tool call's final result, so you may skip them when iterating events manually:

```php
use Laravel\Ai\Streaming\Events\ToolResult;

foreach ($stream as $event) {
    if ($event instanceof ToolResult && $event->preliminary) {
        continue;
    }

    // ...
}
```

Response values such as `text`, `usage`, and `toolResults` ignore preliminary events. The [Vercel protocol](#stream-protocols) renders them as native streaming tool output, so `useChat` displays the progress without any custom code, while the AG-UI protocol reports them as activity snapshots. The completed response's text, reasoning, citations, and usage include those of the sub-agent.

<a name="middleware"></a>
### Middleware

Agents support middleware, allowing you to intercept and modify each generation step before it is sent to the provider. Middleware is invoked once per step, so a run that takes three steps will invoke it three times. Middleware can be created using the `make:agent-middleware` Artisan command:

```shell
php artisan make:agent-middleware LogPrompts
```

The generated middleware will be placed in your application's `app/Ai/Middleware` directory. To add middleware to an agent, implement the `HasMiddleware` interface and define a `middleware` method that returns an array of middleware classes:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Middleware\LogPrompts;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasMiddleware;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasMiddleware
{
    use Promptable;

    // ...

    /**
     * Get the agent's middleware.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

Each middleware class should define a `handle` method that receives a `PendingStep` and a `Closure` that passes the step to the next middleware:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Laravel\Ai\PendingStep;

class LogPrompts
{
    /**
     * Handle the pending generation step.
     */
    public function handle(PendingStep $step, Closure $next)
    {
        Log::info('Prompting agent', ['model' => $step->model]);

        return $next($step);
    }
}
```

In addition to the `provider`, `model`, `instructions`, `messages`, and `tools` that are about to be sent, the step exposes the steps that have already completed, their usage, and the progress of the run:

```php
$step->number;
$step->isFirstStep();
$step->isFinalStep;
```

The `withModel`, `withInstructions`, `withMessages`, `withTools`, `onlyTools`, `withoutTools`, `withToolChoice`, `withMaxTokens`, and `withProviderOptions` methods each return a copy of the step. For example, you may remove an expensive tool once the agent has used it:

```php
public function handle(PendingStep $step, Closure $next)
{
    if (! $step->isFirstStep()) {
        $step = $step->withoutTools('SearchDocumentation');
    }

    return $next($step);
}
```

Or, you may keep a long tool calling loop within the context window by summarizing the middle of the conversation:

```php
use App\Ai\Agents\Summarizer;
use Laravel\Ai\Messages\UserMessage;

public function handle(PendingStep $step, Closure $next)
{
    if (count($step->messages) > 40) {
        $summary = (new Summarizer)->prompt(
            collect(array_slice($step->messages, 1, -10))->map->content->implode("\n"),
        )->text;

        $step = $step->withMessages([
            $step->messages[0],
            new UserMessage("Summary of the conversation so far: {$summary}"),
            ...array_slice($step->messages, -10),
        ]);
    }

    return $next($step);
}
```

Messages given to a step only replace the messages that step sends. The run's history continues to grow from the original messages.

You may use the `then` method to execute code once the model has answered the step, before its tool calls are executed. This works for both synchronous and streaming responses:

```php
use Laravel\Ai\Gateway\StepResponse;

public function handle(PendingStep $step, Closure $next)
{
    return $next($step)->then(function (StepResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

Middleware must return the result of `$next`, or its own `StepResponse` to answer the step without invoking the model, such as when serving a cached response. Returning any other value will throw a `LogicException`.

<a name="anonymous-agents"></a>
### Anonymous Agents

Sometimes you may want to quickly interact with a model without creating a dedicated agent class. You can create an ad-hoc, anonymous agent using the `agent` function:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```

Anonymous agents may also produce structured output:

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100');
```

<a name="agent-configuration"></a>
### Agent Configuration

You may configure text generation options for an agent using PHP attributes. The following attributes are available:

- `MaxSteps`: The maximum number of steps the agent may take when using tools.
- `MaxTokens`: The maximum number of tokens the model may generate.
- `Model`: The model the agent should use.
- `Provider`: The AI provider (or providers for failover) to use for the agent.
- `Temperature`: The sampling temperature to use for generation (0.0 to 1.0).
- `Timeout`: The HTTP timeout in seconds for agent requests (default: 60).
- `TopP`: The nucleus sampling probability to use for generation (0.0 to 1.0).
- `UseCheapestModel`: Use the provider's cheapest text model for cost optimization.
- `UseSmartestModel`: Use the provider's most capable text model for complex tasks.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Attributes\TopP;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
#[Model('claude-sonnet-5')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
#[TopP(0.9)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

The `UseCheapestModel` and `UseSmartestModel` attributes allow you to automatically select the most cost-effective or most capable model for a given provider without specifying a model name. This is useful when you want to optimize for cost or capability across different providers:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // Will use the cheapest model (e.g., Haiku)...
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // Will use the most capable model (e.g., Opus)...
}
```

> [!NOTE]
> The underlying model selected by `UseCheapestModel` and `UseSmartestModel` may change between releases of the Laravel AI SDK as providers release new models. Switching models can introduce behavioral changes, deprecated parameters, and significant cost differences. If you need a stable, predictable model and pricing, specify the model explicitly using the `Model` attribute.

<a name="provider-options"></a>
### Provider Options

If your agent needs to pass provider-specific options (such as OpenAI reasoning effort or penalty settings), implement the `HasProviderOptions` contract and define a `providerOptions` method:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasProviderOptions;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasProviderOptions
{
    use Promptable;

    // ...

    /**
     * Get provider-specific generation options.
     */
    public function providerOptions(Lab|string $provider): array
    {
        return match ($provider) {
            Lab::OpenAI => [
                'reasoning' => ['effort' => 'low'],
                'frequency_penalty' => 0.5,
                'presence_penalty' => 0.3,
            ],
            Lab::Anthropic => [
                'thinking' => ['budget_tokens' => 1024],
                'cache_control' => ['type' => 'ephemeral'],
            ],
            default => [],
        };
    }
}
```

The `providerOptions` method receives the provider currently being used (`Lab` enum or string), allowing you to return different options per provider. This is especially useful when using [failover](#failover), since each fallback provider can receive its own configuration.

The Anthropic example above also enables [prompt caching](#prompt-caching) via `cache_control`.

The [image](#images), [audio](#audio), [transcription](#transcription), [embedding](#embeddings), and [reranking](#reranking) builders accept provider options as well:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')
    ->withProviderOptions(['speed' => 1.25])
    ->generate();
```

You may also pass a closure instead of an array, which will receive the provider currently being used.

<a name="custom-http-headers"></a>
#### Custom HTTP Headers

Headers configured for a provider within your application's `config/ai.php` configuration file are sent with every request that provider makes. To send headers on a per request basis, such as metadata used by an AI gateway, you may use the `withHeaders` method, which is available on the image, audio, transcription, embedding, and reranking builders, as well as on [file uploads](#files):

```php
use Laravel\Ai\Embeddings;

$embeddings = Embeddings::for($chunks)
    ->withHeaders(['cf-aig-metadata' => json_encode(['team' => $team->id])])
    ->withProviderOptions(['dimensions' => 1024])
    ->generate();
```

Headers may also be given as a closure, which receives the provider currently being used. Headers are never sent as request parameters and never affect [embedding cache keys](#caching-embeddings).

<a name="prompt-caching"></a>
### Prompt Caching

Most providers cache repeated prompt prefixes automatically and bill the cached portion at a discount. OpenAI, Gemini, Groq, DeepSeek, and xAI require no configuration, and you may inspect the savings via the response's usage:

```php
$response->usage->cacheReadInputTokens;
$response->usage->cacheWriteInputTokens;
```

Both of these counts are subsets of the input token total, which is discussed further in the [usage documentation](#usage).

The `anthropic` and `bedrock` providers only cache when asked. The `CacheInstructions` and `CacheToolDefinitions` attributes place a cache breakpoint at the end of your agent's instructions and tool definitions, so every conversation reads that prefix from the cache instead of writing it again:

```php
use Laravel\Ai\Attributes\CacheInstructions;
use Laravel\Ai\Attributes\CacheToolDefinitions;

#[CacheInstructions]
#[CacheToolDefinitions]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

If your instructions change on every request, such as when they embed the current date, use `CacheToolDefinitions` alone. Caching a prefix that changes on every request creates a new cache entry each time, so you pay to write it to the cache without ever reusing it.

Providers that do not support these attributes ignore them, so an agent may safely declare them while using [failover](#failover).

Cached prefixes are retained for five minutes by default. Anthropic may retain them for an hour if you pass a TTL to the attribute:

```php
#[CacheInstructions('1h')]
#[CacheToolDefinitions('1h')]
```

Alternatively, Anthropic's automatic caching may be enabled via a top-level `cache_control` [provider option](#provider-options). This places a single breakpoint after the last block of the request, so the breakpoint advances as the conversation grows and each turn reads the previous turns from the cache. Both mechanisms may be combined.

> [!WARNING]
> Because providers build prompts in the order tools, instructions, and messages, caching instructions for an hour also requires caching tool definitions for an hour. Mixing the two throws an `InvalidArgumentException`.

<a name="human-tool-approval"></a>
## Human Tool Approval

> [!WARNING]
> Tool approval requires the paused turn's history to be available when the run is resumed. You should either use a `Conversational` agent, such as one using the `RemembersConversations` trait, or provide the history from your application's frontend using the [`withMessages` method](#conversation-context). Agents that do neither will throw an `ApprovalNotResumableException` when a tool pauses.

Tools that perform sensitive or irreversible actions may require human approval before they are executed. To make a tool approvable, implement the `Approvable` contract and use the `InteractsWithApprovals` trait. Approvable tools require approval by default:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Illuminate\Support\Facades\Storage;
use Laravel\Ai\Concerns\InteractsWithApprovals;
use Laravel\Ai\Contracts\Approvable;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class DeleteFile implements Approvable, Tool
{
    use InteractsWithApprovals;

    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'Delete a file from storage.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        Storage::delete($request['path']);

        return "Deleted [{$request['path']}].";
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'path' => $schema->string()->required(),
        ];
    }
}
```

To determine whether approval is needed based on the tool call's arguments, define a `needsApproval` method on the tool. This method may return a boolean or an `Approval` instance that includes a reason for the approval request:

```php
use Laravel\Ai\Approvals\Approval;

/**
 * Determine whether the tool needs approval for the given request.
 */
protected function needsApproval(Request $request): Approval|bool
{
    return str_starts_with($request['path'], 'temporary/')
        ? false
        : Approval::required('This will permanently delete a file.');
}
```

You may override a tool's approval requirement when returning it from an agent's `tools` method:

```php
public function tools(): iterable
{
    return [
        (new SendNotification)->withoutApproval(),
        (new DeleteFile)->requireApproval('Deletion review required.'),
    ];
}
```

When an approvable tool is called, the agent pauses before executing it. You may inspect the response's pending approvals, which contain each tool call's ID, tool name, arguments, and approval reason:

```php
$response = (new FileAssistant)
    ->forUser($user)
    ->prompt('Delete the old invoice.');

if ($response->hasPendingApprovals()) {
    foreach ($response->pendingApprovals as $approval) {
        // $approval->id
        // $approval->tool
        // $approval->arguments
        // $approval->reason
    }
}
```

To resume the agent, continue the conversation and provide a `Decisions` instance containing a decision for each pending tool call. Decisions may approve the call, reject it, or edit its arguments before execution:

```php
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt(Decisions::from([
        'call_abc' => Decision::approve(),
        'call_ghi' => Decision::reject('The invoice must be retained.'),
    ]));
```

> [!IMPORTANT]
> Paused turns are matched by their conversation and pending tool calls, not by the participant that paused them. Therefore, your application should authorize access to the conversation before resuming it, as demonstrated in the [complete approval flow](#complete-approval-flow), or verify access using the conversation store's `conversationBelongsTo` method.

The boolean values `true` and `false` may be used as shorthand for approval and rejection. Every pending tool call must receive a decision. Unknown, missing, or previously resolved tool call IDs will cause an `ApprovalMismatchException` to be thrown. You may provide a default for calls without an explicit decision using the `approveRemaining` or `rejectRemaining` methods:

```php
$decisions = Decisions::from([
    'call_abc' => true,
])->rejectRemaining('Not approved.');

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt($decisions);
```

A rejection with a result, such as `Decision::reject('Not approved.')`, is returned to the model so it may continue responding. A rejection without a result stops the generation loop after recording the rejection.

Tool approval is supported by the `prompt`, `stream`, `queue`, `broadcast`, `broadcastNow`, and `broadcastOnQueue` methods.

During streaming and broadcasting, a pause is represented by a `tool_approval_request` event. When using the [Vercel AI SDK stream protocol](#stream-protocols), approval requests and results are emitted using the protocol's native tool approval parts, and the Agent User Interaction protocol reports them as interrupts.

Clients that use either protocol post their decisions along with the rest of the conversation, so a [chat request](#chat-requests) may be passed directly to the agent:

```php
$chat = Vercel::chat($request);

return (new FileAssistant)
    ->continue($conversationId, as: $request->user())
    ->stream($chat)
    ->usingProtocol($chat->protocol());
```

A resumed run is merged into the turn that it paused on, so each turn is stored as a single assistant message. The response's `assistantMessageId` contains the ID of the paused message, and that message's usage includes both the pause and the resume.

For queued agents, the resulting response is passed to the `then` callback, and Laravel also dispatches a `ToolApprovalRequested` event.

Laravel stores the result of an approved tool before asking the model to continue. If generation then fails, the approval has already been resolved. Continue the conversation with a normal text prompt instead of submitting the same approval decisions again.

<a name="complete-approval-flow"></a>
### Complete Approval Flow

The following route demonstrates a complete approval flow, accepting either a new text prompt or approval decisions from the chat screen. This example assumes the application's `User` model uses the `HasConversations` trait:

```php
use App\Ai\Agents\FileAssistant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Route;
use Illuminate\Validation\Rule;
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Models\Conversation;

Route::post('/chat/{conversation}', function (Request $request, Conversation $conversation) {
    Gate::authorize('view', $conversation);

    $validated = $request->validate([
        'message' => ['nullable', 'string', 'required_without:decisions', 'prohibits:decisions'],
        'decisions' => ['nullable', 'array', 'required_without:message', 'prohibits:message'],
        'decisions.*.action' => ['required_with:decisions', Rule::in(['approve', 'reject'])],
        'decisions.*.result' => ['nullable', 'string'],
    ]);

    $prompt = isset($validated['decisions'])
        ? Decisions::from(collect($validated['decisions'])->map(
            fn (array $decision) => match ($decision['action']) {
                'approve' => Decision::approve(),
                'reject' => Decision::reject($decision['result'] ?? null),
            }
        )->all())
        : $validated['message'];

    $response = (new FileAssistant)
        ->continue($conversation->id, as: $request->user())
        ->prompt($prompt);

    return [
        'conversation_id' => $response->conversationId,
        'status' => $response->hasPendingApprovals() ? 'awaiting_approval' : 'complete',
        'message' => $response->text,
        'approvals' => $response->pendingApprovals,
    ];
})->middleware('auth');
```

When the response status is `awaiting_approval`, the chat screen should render the pending approvals and submit the user's choices to the same endpoint using the tool call ID as each decision's key. Otherwise, the screen may submit a plain `message` value:

```json
{
    "decisions": {
        "call_abc": {
            "action": "approve"
        },
        "call_def": {
            "action": "reject",
            "result": "The invoice must be retained."
        }
    }
}
```

<a name="images"></a>
## Images

The `Laravel\Ai\Image` class may be used to generate images using the `openai`, `gemini`, or `xai` providers:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

The `square`, `portrait`, and `landscape` methods may be used to control the aspect ratio of the image, while the `quality` method may be used to guide the model on final image quality (`high`, `medium`, `low`). The `timeout` method may be used to specify the HTTP timeout in seconds:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

You may attach reference images using the `attachments` method:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```

Some providers may generate multiple images in a single request. OpenAI, Azure, and xAI accept an `n` [provider option](#provider-options), and the response will contain every image that was returned:

```php
$response = Image::of('A donut sitting on the kitchen counter')
    ->withProviderOptions(['n' => 4])
    ->generate();

count($response);           // 4
$response->images;          // A collection of generated images...
$response->firstImage();    // The first generated image...
```

Generated images may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

Image generation may also be queued:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Responses\ImageResponse;

Image::of('A donut sitting on the kitchen counter')
    ->portrait()
    ->queue()
    ->then(function (ImageResponse $image) {
        $path = $image->store();

        // ...
    });
```

<a name="audio"></a>
## Audio

The `Laravel\Ai\Audio` class may be used to generate audio from the given text:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

You may also generate audio from a string using the `toAudio` method available via Laravel's `Stringable` class:

```php
use Illuminate\Support\Str;

$audio = Str::of('I love coding with Laravel.')->toAudio();
```

The `male`, `female`, and `voice` methods may be used to determine the voice of the generated audio:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

Similarly, the `instructions` method may be used to dynamically coach the model on how the generated audio should sound:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

Generated audio may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

Audio generation may also be queued:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Responses\AudioResponse;

Audio::of('I love coding with Laravel.')
    ->queue()
    ->then(function (AudioResponse $audio) {
        $path = $audio->store();

        // ...
    });
```

<a name="transcription"></a>
## Transcriptions

The `Laravel\Ai\Transcription` class may be used to generate a transcript of the given audio:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

The `diarize` method may be used to indicate you would like the response to include the diarized transcript in addition to the raw text transcript, allowing you to access the segmented transcript by speaker:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

Transcription generation may also be queued:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Responses\TranscriptionResponse;

Transcription::fromStorage('audio.mp3')
    ->queue()
    ->then(function (TranscriptionResponse $transcript) {
        // ...
    });
```

<a name="text-summarization"></a>
## Text Summarization

You may summarize text using the `summarize` method available via Laravel's `Stringable` class. By default, the summary will contain no more than three sentences and will be generated using the configured provider's cheapest text model:

```php
use Illuminate\Support\Str;

$summary = Str::of($article)->summarize();
```

You may specify the maximum number of sentences, provider, model, and timeout used to generate the summary. The `Str` class also offers a static version of the method:

```php
use Laravel\Ai\Enums\Lab;

$summary = Str::of($article)->summarize(
    sentences: 4,
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 30,
);

$summary = Str::summarize($article, sentences: 4);
```

<a name="embeddings"></a>
## Embeddings

You may easily generate vector embeddings for any given string using the new `toEmbeddings` method available via Laravel's `Stringable` class:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

Alternatively, you may use the `Embeddings` class to generate embeddings for multiple inputs at once:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

You may specify the dimensions and provider for the embeddings:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="multimodal-embeddings"></a>
### Multimodal Embeddings

In addition to strings, the `Embeddings::for` method accepts image, audio, document, and video inputs, allowing you to generate embeddings for non-text content. Gemini supports image, audio, document, and video embeddings, while VoyageAI supports image and video embeddings:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

$response = Embeddings::for([
    'A vineyard at sunset.',
    Image::fromStorage('vineyard.jpg'),
    Video::fromPath('/home/laravel/tour.mp4'),
])->generate(Lab::Gemini);
```

Multimodal inputs use the same [file classes used for attachments](#attachments). These files may be created from a local path, a filesystem disk, a remote URL, or Base64-encoded content. Images, documents, and videos may also be created from uploaded files, while documents may be created from raw string content:

```php
use Laravel\Ai\Files\Audio;
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

Image::fromPath('/home/laravel/photo.jpg');
Image::fromStorage('photo.jpg');
Image::fromUpload($request->file('photo'));

Audio::fromPath('/home/laravel/clip.mp3');
Audio::fromStorage('clip.mp3');
Audio::fromUpload($request->file('clip.mp3'));

Video::fromPath('/home/laravel/video.mp4');
Video::fromStorage('video.mp4');
Video::fromUpload($request->file('video'));

Document::fromUrl('https://example.com/report.pdf');
Document::fromString('Laravel is a PHP framework.', 'text/plain');
Document::fromUpload($request->file('report'));
```

> [!NOTE]
> VoyageAI does not allow remote URL media and Base64-encoded media to be mixed in a single request. Local, stored, and uploaded files are sent as Base64-encoded content, and text inputs may be combined with either media source. Consult your provider's documentation to determine which multimodal models and inputs are available.

<a name="querying-embeddings"></a>
### Querying Embeddings

Once you have generated embeddings, you will typically store them in a `vector` column in your database for later querying. Laravel provides native support for vector columns on PostgreSQL via the `pgvector` extension and MariaDB. To get started, define a `vector` column in your migration, specifying the number of dimensions:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536);
    $table->timestamps();
});
```

You may also add a vector index to speed up similarity searches. When calling `index` on a vector column, Laravel will automatically create an HNSW index with cosine distance:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

On your Eloquent model, you should cast the vector column using the `AsVector` cast:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```

To query for similar records, use the `whereVectorSimilarTo` method. This method filters results by a minimum cosine similarity (between `0.0` and `1.0`, where `1.0` is identical) and orders the results by similarity:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

The `$queryEmbedding` may be an array of floats or a plain string. When a string is given, Laravel will automatically generate embeddings for it:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

If you need more control, you may use the lower-level `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods independently:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

If you would like to give an agent the ability to perform similarity searches as a tool, check out the [Similarity Search](#similarity-search) tool documentation.

> [!NOTE]
> Vector queries are currently supported on PostgreSQL connections using the `pgvector` extension and MariaDB 11.7 or later.

<a name="caching-embeddings"></a>
### Caching Embeddings

Embedding generation can be cached to avoid redundant API calls for identical inputs. To enable caching, set the `ai.caching.embeddings.cache` configuration option to `true`:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        'individually' => true,
        // ...
    ],
],
```

When caching is enabled, embeddings are cached for 30 days. The cache key is based on the provider, model, dimensions, and input content, ensuring that identical requests return cached results while different configurations generate fresh embeddings.

By default, each input's embedding is cached under its own key, so a later request may hit the cache for inputs it has seen before even when the set of inputs or their order has changed. To instead cache the entire set of inputs under a single key, set the `ai.caching.embeddings.individually` configuration option to `false`.

You may also enable caching for a specific request using the `cache` method, even when global caching is disabled:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

You may specify a custom cache duration in seconds:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```

The `toEmbeddings` Stringable method also accepts a `cache` argument:

```php
// Cache with default duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// Cache for a specific duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## Reranking

Reranking allows you to reorder a list of documents based on their relevance to a given query. This is useful for improving search results by using semantic understanding:

The `Laravel\Ai\Reranking` class may be used to rerank documents:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// Access the top result...
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (original position)
```

The `limit` method may be used to restrict the number of results returned, while the `timeout` method may be used to specify the HTTP timeout in seconds, which defaults to 30:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->timeout(60)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### Reranking Collections

For convenience, Laravel collections may be reranked using the `rerank` macro. The first argument specifies which field(s) to use for reranking, and the second argument is the query:

```php
// Rerank by a single field...
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// Rerank by multiple fields (sent as JSON)...
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// Rerank using a closure to build the document...
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

You may also limit the number of results and specify a provider:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: Lab::Cohere,
    timeout: 60,
);
```

<a name="classification"></a>
## Classification

> [!WARNING]
> Classification is currently experimental and its API may change in future minor releases of the AI SDK.

Classification allows you to ask a fixed set of questions about a given string or array of data and receive a typed answer, backed by a probability, for each question instead of free-form text. This is useful for routing, moderation, and scoring, where decisions need to be thresholded and tested.

The `Laravel\Ai\Classification` class may be used to classify content. Each question is given a key, and the corresponding answer may be retrieved from the response using that key:

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Classification\Boolean;
use Laravel\Ai\Classification\Choice;
use Laravel\Ai\Classification\Score;

$result = Classification::of($supportRequest)
    ->questions([
        'urgent' => new Boolean('Does this request need an immediate response?', [
            'true' => 'Explicitly time-sensitive',
            'false' => 'No urgency expressed',
        ]),
        'department' => new Choice('Which team should handle this request?', [
            'billing' => 'Payments, invoices, and refunds',
            'technical' => 'Bugs, outages, and integrations',
            'sales' => 'Pricing, plans, and upgrades',
        ]),
        'frustration' => new Score('How frustrated is the customer?', [
            'Calm',
            'Frustrated',
            'Very angry',
        ]),
    ])
    ->classify();
```

`Boolean` questions return the probability that the answer is "true". The `isTrue` method may be used to determine whether that probability meets a given threshold, which defaults to `0.5`:

```php
$result['urgent']->probability;             // 0.94
$result['urgent']->isTrue(threshold: 0.8);  // true
```

`Choice` questions return one of the given options along with the probability of each option. The `confidence` property will be `null` when the provider is unable to measure it:

```php
$result['department']->choice;                      // 'technical'
$result['department']->probabilityOf('technical');  // 0.87
$result['department']->probabilities;               // ['billing' => 0.08, 'technical' => 0.87, 'sales' => 0.05]
$result['department']->confidence;                  // 0.82
```

`Score` questions return a position on the ordered levels that were provided. The `score` property is probability-weighted and may fall between two levels, while the `level` and `label` methods describe the most probable level:

```php
$result['frustration']->score;          // 1.24, the probability-weighted level
$result['frustration']->level();        // 1, the most probable level
$result['frustration']->label();        // 'Frustrated'
$result['frustration']->normalized();   // 0.62, the score as a fraction of the highest level
$result['frustration']->probabilities;  // [0.12, 0.52, 0.36]
```

The criteria given to a `Boolean` question, the option descriptions given to a `Choice` question, and the levels given to a `Score` question may each be an array when a single sentence is not sufficient. `Choice` questions require at least two options, while `Score` questions require at least two levels.

The response may be iterated, counted, and accessed as an array. In addition, the `answer` method may be used to retrieve a single answer, while the `collect` method returns all of the answers as a [collection](/docs/{{version}}/collections):

```php
$result->answer('urgent');
$result->collect();

$result->usage;
$result->meta->provider;
```

By default, classification is performed by [TypeSafe](https://typesafe.ai). You may change this using the `default_for_classification` option within your application's `config/ai.php` configuration file. You may also specify the provider and model when classifying:

```php
use Laravel\Ai\Enums\Lab;

$result = Classification::of($supportRequest)
    ->questions($questions)
    ->classify(Lab::OpenRouter, 'model-name');
```

The `timeout` method may be used to specify the HTTP timeout in seconds, which defaults to 30. [Provider options](#provider-options) and custom headers may be given as well:

```php
$result = Classification::of($supportRequest)
    ->questions($questions)
    ->timeout(60)
    ->withProviderOptions(['temperature' => 0])
    ->classify();
```

<a name="files"></a>
## Files

The `Laravel\Ai\Files` class or the individual file classes may be used to store files with your AI provider for later use in conversations. This is useful for large documents or files you want to reference multiple times without re-uploading:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// Store a file from a local path...
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// Store a file that is stored on a filesystem disk...
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// Store a file that is stored on a remote URL...
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

You may also store raw content or uploaded files:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```

Once a file has been stored, you may reference the file when generating text via agents instead of re-uploading the file:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id') // Attach a stored document...
    ]
);
```

To retrieve a previously stored file, use the `get` method on a file instance:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

To delete a file from the provider, use the `delete` method:

```php
Document::fromId('file-id')->delete();
```

By default, the `Files` class uses the default AI provider configured in your application's `config/ai.php` configuration file. For most operations, you may specify a different provider using the `provider` argument:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

You may pass provider-specific upload options using the `withProviderOptions` method. For example, you may set OpenAI's file `purpose`:

```php
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/knowledge.txt')
    ->withProviderOptions(['purpose' => 'assistants'])
    ->put();
```

To scope options per provider, pass a closure that receives the current provider:

```php
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/training.jsonl')
    ->withProviderOptions(fn (Lab|string $provider) => match ($provider) {
        Lab::OpenAI => ['purpose' => 'fine-tune'],
        default => [],
    })
    ->put();
```

<a name="using-stored-files-in-conversations"></a>
### Using Stored Files in Conversations

Once a file has been stored with a provider, you may reference it in agent conversations using the `fromId` method on the `Document` or `Image` classes:

```php
use App\Ai\Agents\DocumentAnalyzer;
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

$stored = Document::fromPath('/path/to/report.pdf')->put();

$response = (new DocumentAnalyzer)->prompt(
    'Summarize this document.',
    attachments: [
        Document::fromId($stored->id),
    ],
);
```

Similarly, stored images may be referenced using the `Image` class:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Image;

$stored = Image::fromPath('/path/to/photo.jpg')->put();

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Image::fromId($stored->id),
    ],
);
```

<a name="vector-stores"></a>
## Vector Stores

Vector stores allow you to create searchable collections of files that can be used for retrieval-augmented generation (RAG). The `Laravel\Ai\Stores` class provides methods for creating, retrieving, and deleting vector stores:

```php
use Laravel\Ai\Stores;

// Create a new vector store...
$store = Stores::create('Knowledge Base');

// Create a store with additional options...
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

To retrieve an existing vector store by its ID, use the `get` method:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

To delete a vector store, use the `delete` method on the `Stores` class or the store instance:

```php
use Laravel\Ai\Stores;

// Delete by ID...
Stores::delete('store_id');

// Or delete via a store instance...
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### Adding Files to Stores

Once you have a vector store, you may add [files](#files) to it using the `add` method. Files added to a store are automatically indexed for semantic searching using the [file search provider tool](#file-search):

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// Add a file that has already been stored with the provider...
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// Or, store and add a file in one step...
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:** Typically, when adding previously stored files to vector stores, the returned document ID will match the file's previously assigned ID; however, some vector storage providers may return a new, different "document ID". Therefore, it's recommended that you always store both IDs in your database for future reference.

When adding a file to a Gemini store, Laravel waits for the import to finish so that the document is searchable once the call returns. A `Laravel\Ai\Exceptions\AiException` will be thrown if the import fails or exceeds five minutes, so you may wish to add Gemini files from a [queued job](/docs/{{version}}/queues).

You may attach metadata to files when adding them to a store. This metadata can later be used to filter search results when using the [file search provider tool](#file-search):

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

To remove a file from a store, use the `remove` method:

```php
$store->remove('file_id');
```

Removing a file from a vector store does not remove it from the provider's [file storage](#files). To remove a file from the vector store and delete it permanently from file storage, use the `deleteFile` argument:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="usage"></a>
## Usage

Every response contains a `usage` property describing what the request consumed. The input and output counts are totals, so tokens counted as cached or reasoning tokens are also included in the total they belong to:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->usage->inputTokens;
$response->usage->outputTokens;
$response->usage->totalTokens();
```

Text generation returns a `Laravel\Ai\Responses\Data\TextUsage` instance, which breaks these totals down further. Each of these values will be `null` when the provider does not report it, distinguishing an unreported count from zero:

```php
$response->usage->cacheReadInputTokens;   // Subset of the input tokens read from a prompt cache...
$response->usage->cacheWriteInputTokens;  // Subset of the input tokens written to a prompt cache...
$response->usage->reasoningTokens;        // Subset of the output tokens spent on reasoning...

$response->usage->uncachedInputTokens();  // Input tokens that were neither read from nor written to the cache...
```

Cache reads, cache writes, and uncached input are billed at different rates, so you should price these three counts separately instead of using the input total alone.

The remaining capabilities return a usage object containing the counts specific to them:

<div class="overflow-auto">

| Capability | Usage object | Adds |
|---|---|---|
| Text, classification | `TextUsage` | Cache read, cache write, and reasoning tokens |
| Images | `ImageUsage` | `imageInputTokens` and `imageOutputTokens` |
| Transcription | `TranscriptionUsage` | `audioSeconds`, the duration of the transcribed audio |
| Reranking | `RerankingUsage` | `searchUnits`, which some providers bill instead of tokens |
| Audio, embeddings | `Usage` | |

</div>

Not every provider reports every count. Image and transcription models that a provider routes through its chat models report cache and reasoning counts, while other providers leave them `null`:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Transcription;

Image::of('A donut sitting on the kitchen counter')->generate()->usage->imageOutputTokens;

Transcription::fromPath('/home/laravel/meeting.mp3')->generate()->usage->audioSeconds;
```

<a name="failover"></a>
## Failover

When prompting or generating other media, you may provide an array of providers / models to automatically failover to a backup provider / model if a service interruption or rate limit is encountered on the primary provider:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

Failover only occurs when a `FailoverableException` is thrown — such as a rate limit (`RateLimitedException`), an overloaded or unavailable provider (`ProviderOverloadedException`), or insufficient credits (`InsufficientCreditsException`). Ordinary errors, like a validation or bad request error, will not trigger failover.

When you pass a plain list of providers, such as `[Lab::OpenAI, Lab::Anthropic]`, each provider uses its default model. To specify a particular model for each provider in the failover chain, pass an associative array keyed by the provider, using the `Lab` enum's `value` as the key (enum cases cannot be used directly as PHP array keys):

```php
use Laravel\Ai\Enums\Lab;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [
        Lab::Gemini->value => 'gemini-3-flash-preview',
        Lab::DeepSeek->value => 'deepseek-v4-pro',
    ],
);
```

<a name="testing"></a>
## Testing

When faking queued image, audio, transcription, or embeddings generation, any `then` callback registered on the queued generation will be invoked with the faked response, allowing you to test the logic contained within the callback. If you would prefer that these callbacks are not invoked, you may fake the queue using `Queue::fake()` as well.

<a name="testing-agents"></a>
### Agents

To fake an agent's responses during tests, call the `fake` method on the agent class. You may optionally provide an array of responses or a closure:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// Automatically generate a fixed response for every prompt...
SalesCoach::fake();

// Provide a list of prompt responses...
SalesCoach::fake([
    'First response',
    'Second response',
]);

// Dynamically handle prompt responses based on the incoming prompt...
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

When faking an agent that returns structured output, you may provide arrays as responses. The agent will return a structured response containing the given data:

```php
SalesCoach::fake([
    ['score' => 87],
]);
```

You may also fake a response that is awaiting tool approval:

```php
use Laravel\Ai\Approvals\PendingApproval;
use Laravel\Ai\Responses\AgentResponse;

FileAssistant::fake([
    AgentResponse::fakeWithPendingApprovals([
        new PendingApproval(
            id: 'call_abc',
            tool: 'DeleteFile',
            arguments: ['path' => 'invoice.pdf'],
            reason: 'This will permanently delete a file.',
        ),
    ]),
]);

$response = (new FileAssistant)->prompt('Delete the invoice.');

$response->hasPendingApprovals(); // true
```

You may also fake a response that includes reasoning. The fake emits reasoning events, so the reasoning is reported on streamed runs as well:

```php
use Laravel\Ai\Responses\AgentResponse;

SalesCoach::fake([
    AgentResponse::fakeWithReasoning('They asked about pricing.', 'Plans start at $10.'),
]);

$response = (new SalesCoach)->stream('What does it cost?');

foreach ($response as $event) {
    // ...
}

$response->reasoning; // 'They asked about pricing.'
```

> **Note:** When `Agent::fake()` is invoked on an agent that returns structured output and fake output was not explicitly provided, Laravel will automatically generate fake data that matches your agent's defined output schema.

After prompting the agent, you may make assertions about the prompts that were received:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertPromptedTimes(3);

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

When asserting an approval continuation, you may inspect the prompt's approval decisions:

```php
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Prompts\AgentPrompt;

FileAssistant::fake();

(new FileAssistant)->prompt(Decisions::from([
    'call_abc' => true,
]));

FileAssistant::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->hasApprovalDecisions()
        && $prompt->approvalDecisions->get('call_abc')->isApproved();
});
```

For queued agent invocations, use the queued assertion methods:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

To ensure all agent invocations have a corresponding fake response, you may use `preventStrayPrompts`. If an agent is invoked without a defined fake response, an exception will be thrown:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### Images

Image generations may be faked by invoking the `fake` method on the `Image` class. Once image has been faked, various assertions may be performed against the recorded image generation prompts:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// Automatically generate a fixed response for every prompt...
Image::fake();

// Provide a list of prompt responses...
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

After generating images, you may make assertions about the prompts that were received:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

For queued image generations, use the queued assertion methods:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

To ensure all image generations have a corresponding fake response, you may use `preventStrayImages`. If an image is generated without a defined fake response, an exception will be thrown:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### Audio

Audio generations may be faked by invoking the `fake` method on the `Audio` class. Once audio has been faked, various assertions may be performed against the recorded audio generation prompts:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// Automatically generate a fixed response for every prompt...
Audio::fake();

// Provide a list of prompt responses...
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

After generating audio, you may make assertions about the prompts that were received:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

For queued audio generations, use the queued assertion methods:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

To ensure all audio generations have a corresponding fake response, you may use `preventStrayAudio`. If audio is generated without a defined fake response, an exception will be thrown:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### Transcriptions

Transcription generations may be faked by invoking the `fake` method on the `Transcription` class. Once transcription has been faked, various assertions may be performed against the recorded transcription generation prompts:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// Automatically generate a fixed response for every prompt...
Transcription::fake();

// Provide a list of prompt responses...
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// Dynamically handle prompt responses based on the incoming prompt...
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

After generating transcriptions, you may make assertions about the prompts that were received:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

For queued transcription generations, use the queued assertion methods:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

To ensure all transcription generations have a corresponding fake response, you may use `preventStrayTranscriptions`. If a transcription is generated without a defined fake response, an exception will be thrown:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### Embeddings

Embeddings generations may be faked by invoking the `fake` method on the `Embeddings` class. Once embeddings has been faked, various assertions may be performed against the recorded embeddings generation prompts:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// Automatically generate fake embeddings of the proper dimensions for every prompt...
Embeddings::fake();

// Provide a list of prompt responses...
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// Dynamically handle prompt responses based on the incoming prompt...
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

After generating embeddings, you may make assertions about the prompts that were received:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

For queued embeddings generations, use the queued assertion methods:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

To ensure all embeddings generations have a corresponding fake response, you may use `preventStrayEmbeddings`. If embeddings are generated without a defined fake response, an exception will be thrown:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### Reranking

Reranking operations may be faked by invoking the `fake` method on the `Reranking` class:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// Automatically generate a fake reranked responses...
Reranking::fake();

// Provide custom responses...
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

After reranking, you may make assertions about the operations that were performed:

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
```

<a name="testing-classification"></a>
### Classification

Classification may be faked by invoking the `fake` method on the `Classification` class. If no custom responses are provided, Laravel will automatically generate answers that match the shape of each question:

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Prompts\ClassificationPrompt;
use Laravel\Ai\Responses\Data\BooleanAnswer;
use Laravel\Ai\Responses\Data\ChoiceAnswer;

// Automatically generate fake answers...
Classification::fake();

// Provide answers for specific questions...
Classification::fake([
    [
        'urgent' => new BooleanAnswer(0.94),
        'department' => new ChoiceAnswer('technical', [
            'billing' => 0.08,
            'technical' => 0.87,
            'sales' => 0.05,
        ], confidence: 0.82),
    ],
]);

// Build answers from the prompt...
Classification::fake(fn (ClassificationPrompt $prompt) => [
    'urgent' => new BooleanAnswer($prompt->contains('ASAP') ? 1.0 : 0.0),
]);
```

Questions that are omitted from a fake response will still receive a generated answer, so your tests only need to provide the answers they make assertions against.

After classifying, you may make assertions about the operations that were performed:

```php
Classification::assertClassified(function (ClassificationPrompt $prompt) {
    return $prompt->contains('refund') && $prompt->asks('department');
});

Classification::assertNotClassified(
    fn (ClassificationPrompt $prompt) => $prompt->asks('sentiment')
);

Classification::assertNothingClassified();
```

<a name="testing-files"></a>
### Files

File operations may be faked by invoking the `fake` method on the `Files` class:

```php
use Laravel\Ai\Files;

Files::fake();
```

Once file operations have been faked, you may make assertions about the uploads and deletions that occurred:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// Store files...
Document::fromString('Hello, Laravel!', mimeType: 'text/plain')
    ->as('hello.txt')
    ->put();

// Make assertions...
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain'
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

For asserting against file deletions, you may pass a file ID:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### Vector Stores

Vector store operations may be faked by invoking the `fake` method on the `Stores` class. Faking stores will also fake [file operations](#files) automatically:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

Once store operations have been faked, you may make assertions about the stores that were created or deleted:

```php
use Laravel\Ai\Stores;

// Create store...
$store = Stores::create('Knowledge Base');

// Make assertions...
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

For asserting against store deletions, you may provide the store ID:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

To assert files were added or removed from a store, use the assertion methods on a given `Store` instance:

```php
Stores::fake();

$store = Stores::get('store_id');

// Add / remove files...
$store->add('added_id');
$store->remove('removed_id');

// Make assertions...
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

If a file is stored in the provider's [file storage](#files) and added to a vector store in the same request, you may not know the file's provider ID. In this case, you can pass a closure to the `assertAdded` method to assert against the content of the added file:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## Events

The Laravel AI SDK dispatches a variety of [events](/docs/{{version}}/events), including:

- `AddingFileToStore`
- `AgentFailed`
- `AgentFailedOver`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `Classified`
- `Classifying`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `ProviderFailedOver`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StartingStep`
- `StepCompleted`
- `StepFailed`
- `StoreCreated`
- `StoreDeleted`
- `StoringFile`
- `StreamingAgent`
- `ToolApprovalRequested`
- `ToolApprovalResolved`
- `ToolFailed`
- `ToolInvoked`
- `TranscriptionGenerated`

You can listen to any of these events to log or store AI SDK usage information.
