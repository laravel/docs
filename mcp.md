# Laravel MCP

- [Introduction](#introduction)
- [Installation](#installation)
    - [Publishing Routes](#publishing-routes)
- [Creating Servers](#creating-servers)
    - [Server Registration](#server-registration)
    - [Web Servers](#web-servers)
    - [Local Servers](#local-servers)
- [Creating Tools](#creating-tools)
    - [Tool Name, Title, and Description](#tool-name-title-and-description)
    - [Tool Input Schemas](#tool-input-schemas)
    - [Validating Tool Arguments](#validating-tool-arguments)
    - [Tool Dependency Injection](#tool-dependency-injection)
    - [Tool Annotations](#tool-annotations)
    - [Conditional Tool Registration](#conditional-tool-registration)
    - [Tool Responses](#tool-responses)
- [Creating Prompts](#creating-prompts)
    - [Prompt Name, Title, and Description](#prompt-name-title-and-description)
    - [Prompt Arguments](#prompt-arguments)
    - [Validating Prompt Arguments](#validating-prompt-arguments)
    - [Prompt Dependency Injection](#prompt-dependency-injection)
    - [Conditional Prompt Registration](#conditional-prompt-registration)
    - [Prompt Responses](#prompt-responses)
- [Creating Resources](#creating-resources)
    - [Resource Name, Title, and Description](#resource-name-title-and-description)
    - [Resource Content](#resource-content)
    - [Resource URI and MIME Type](#resource-uri-and-mime-type)
    - [Binary Resources](#binary-resources)
    - [Resource Dependency Injection](#resource-dependency-injection)
    - [Conditional Resource Registration](#conditional-resource-registration)
- [Testing Servers](#testing-servers)

<a name="introduction"></a>
## Introduction

[Laravel MCP](https://github.com/laravel/mcp) provides a simple and elegant way for AI clients to interact with your Laravel application through the Model Context Protocol. It offers an expressive, fluent interface for defining servers, tools, resources, and prompts that enable AI-powered interactions with your application.

<a name="installation"></a>
## Installation

To get started, install Laravel MCP into your project using the Composer package manager:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### Publishing Routes

After installing Laravel MCP, execute the `vendor:publish` Artisan command to publish the `routes/ai.php` file where you will define your MCP servers:

```shell
php artisan vendor:publish --tag=ai-routes
```

This command creates the `routes/ai.php` file in your application's `routes` directory, which you will use to register your MCP servers.

<a name="creating-servers"></a>
## Creating Servers

You may create an MCP server by using the `make:mcp-server` Artisan command. Servers act as the central communication point that exposes MCP methods like tools, resources, and prompts to AI clients:

```shell
php artisan make:mcp-server WeatherServer
```

This command will create a new server class in the `app/Mcp/Servers` directory. The generated server class extends Laravel MCP's base `Laravel\Mcp\Server` class and provides properties for registering tools, resources, and prompts:

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The tools registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // ExampleTool::class,
    ];

    /**
     * The resources registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // ExampleResource::class,
    ];

    /**
     * The prompts registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        // ExamplePrompt::class,
    ];
}
```

<a name="server-registration"></a>
### Server Registration

Once you've created a server, you must register it in your `routes/ai.php` file to make it accessible. Laravel MCP provides two methods for registering servers: `web()` for HTTP-accessible servers and `local()` for command-line servers.

<a name="web-servers"></a>
### Web Servers

Web servers are accessible via HTTP POST requests, making them ideal for remote AI clients or web-based integrations. Register a web server using the `web()` method:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

You may also apply middleware to protect your web servers:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:60,1']);
```

<a name="local-servers"></a>
### Local Servers

Local servers run as Artisan commands, perfect for development, testing, or local AI assistant integrations. Register a local server using the `local()` method:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

Once registered, you can start the server using the `mcp:start` command:

```shell
php artisan mcp:start weather
```

<a name="creating-tools"></a>
## Creating Tools

Tools enable your server to expose functionality that AI clients can call. They allow language models to perform actions, run code, or interact with external systems. Create a tool using the `make:mcp-tool` Artisan command:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

After creating a tool, register it in your server's `$tools` property:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The tools registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

### Tool Name, Title, and Description

By default, the tool's name and title are derived from the class name. For example, `CurrentWeatherTool` will have a `current_weather` name and `Current Weather Tool` title. You may customize these values by overriding the `$name` and `$title` properties:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * The tool's name.
     */
    protected string $name = 'get_optimistic_weather';
    
    /**
     * The tool's title.
     */
    protected string $title = 'Get Optimistic Weather Forecast';
    
    //
}

On the other hand, the tool's description is not automatically generated. You should always provide a meaningful description by overriding the `$description` property:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * The tool's description.
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';
    
    //
}
```

<a name="tool-input-schemas"></a>
### Tool Input Schemas

Tools can define input schemas to specify what arguments they accept from AI clients. Use Laravel's `Illuminate\JsonSchema\JsonSchema` builder to define your tool's input requirements:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Get the tool's input schema.
     *
     * @return array<string, JsonSchema>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for')
                ->required(),
            
            'units' => $schema->enum(['celsius', 'fahrenheit'])
                ->description('Temperature units to use')
                ->default('celsius'),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### Validating Tool Arguments

JSON Schema definitions provide a basic structure for tool arguments, but you may also want to enforce more complex validation rules.

Laravel MCP integrates seamlessly with Laravel's validation system. You may validate incoming tool arguments within your tool's `handle()` method:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool call.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);
        
        // Fetch weather data using the validated arguments...
    }
}
```

<a name="tool-dependency-injection"></a>
#### Tool Dependency Injection

The Laravel service container is used to resolve all tools. As a result, you are able to type-hint any dependencies your tool may need in its constructor. The declared dependencies will automatically be resolved and injected into the tool instance:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Create a new tool instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}
    
    //
}
```

In addition to constructor injection, you may also type-hint dependencies in your tool's `handle()` method. The service container will automatically resolve and inject the dependencies when the method is called:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool call.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $location = $request->get('location');

        $forecast = $weather->getForecastFor($location);

        //
    }
}
```

<a name="tool-annotations"></a>
### Tool Annotations

You may enhance your tools with annotations to provide additional metadata to AI clients. These annotations help AI models understand the tool's behavior and capabilities:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tool;

#[IsReadOnly]
#[IsIdempotent]
class CurrentWeatherTool extends Tool
{
    //
}
```

Available annotations include:

| Annotation         | Type    | Description                                                                                     |
| ------------------ | ------- | ----------------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`    | boolean | Indicates the tool does not modify its environment                                            |
| `#[IsDestructive]` | boolean | Indicates the tool may perform destructive updates (only meaningful when not read-only)       |
| `#[IsIdempotent]`  | boolean | Indicates repeated calls with same arguments have no additional effect (when not read-only)   |
| `#[IsOpenWorld]`   | boolean | Indicates the tool may interact with external entities                                        |

<a name="conditional-tool-registration"></a>
### Conditional Tool Registration

You may conditionally register tools at runtime by implementing the `shouldRegister` method in your tool class. This method allows you to determine whether a tool should be available based on application state, configuration, or request parameters:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Determine if the tool should be registered.
     */
    public function shouldRegister(): bool
    {
        return config('features.weather_tools_enabled', false);
    }
}
```

The `shouldRegister` method can also accept the current `Request` instance, allowing you to make registration decisions based on request parameters:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Determine if the tool should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->isSubscribed() ?? false;
    }
}
```

When a tool's `shouldRegister` method returns `false`, it will not appear in the list of available tools and cannot be invoked by AI clients.

<a name="tool-responses"></a>
### Tool Responses

Tools must return an instance of `Laravel\Mcp\Response`. The Response class provides several convenient methods for creating different types of responses:

#### Plain Text Responses

For simple text responses, use the `text()` method:

```php
return Response::text('The current weather in ' . $location . ' is 72°F and sunny.');
```

#### Error Responses

To indicate an error occurred during tool execution, use the `error()` method:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### Multiple Content Responses

Tools can return multiple pieces of content by returning an array of Response instances:

```php
/**
 * Handle the tool call.
 *
 * @return array<int, \Laravel\Mcp\Response>
 */
public function handle(Request $request): array
{
    $summary = Response::text('Weather Summary: Sunny, 72°F');
    $details = Response::text('**Detailed Forecast**\n- Morning: 65°F\n- Afternoon: 78°F\n- Evening: 70°F');
    
    return [$summary, $details];
}
```

<a name="streaming-responses"></a>
#### Streaming Responses

For long-running operations or real-time data streaming, tools can return a generator from their `handle()` method. This enables sending intermediate updates to the client before the final response:

```php
<?php

namespace App\Mcp\Tools;

use Generator;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool call.
     *
     * @return \Generator<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): Generator
    {
        $locations = $request->array('locations');
        
        $forecasts = [];

        foreach ($locations as $index => $location) {
            // Send progress notification
            yield Response::notification('processing/progress', [
                'current' => $index + 1,
                'total' => count($locations),
                'location' => $location,
            ]);

            yield Response::text($this->forecastFor($location));
        }
    }
}
```

When using web-based servers, streaming responses automatically open an SSE (Server-Sent Events) stream, sending each yielded message as an event to the client.

<a name="creating-prompts"></a>
## Creating Prompts

Prompts enable your server to share reusable prompt templates that AI clients can use to interact with language models. They provide a standardized way to structure common queries and interactions. Create a prompt using the `make:mcp-prompt` Artisan command:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

After creating a prompt, register it in your server's `$prompts` property:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The prompts registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

<a name="prompt-name-title-and-description"></a>
### Prompt Name, Title, and Description

By default, the prompt's name and title are derived from the class name. For example, `DescribeWeatherPrompt` will have a `describe_weather` name and `Describe Weather Prompt` title. You may customize these values by overriding the `$name` and `$title` properties:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * The prompt's name.
     */
    protected string $name = 'weather_assistant';
    
    /**
     * The prompt's title.
     */
    protected string $title = 'Weather Assistant Prompt';
    
    //
}
```

On the other hand, the prompt's description is not automatically generated. You should always provide a meaningful description by overriding the `$description` property:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * The prompt's description.
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';
    
    //
}
```

<a name="prompt-arguments"></a>
### Prompt Arguments

Prompts can define arguments that allow AI clients to customize the prompt template with specific values. Use the `arguments()` method to define what parameters your prompt accepts:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Get the prompt's arguments.
     *
     * @return array<int, \Laravel\Mcp\Server\Prompts\Argument>
     */
    public function arguments(): array
    {
        return [
            new Argument(
                name: 'tone',
                description: 'The tone to use in the weather description (e.g., formal, casual, humorous)',
                required: true,
            ),
        ];
    }
}
```

<a name="validating-prompt-arguments"></a>
### Validating Prompt Arguments

Prompt arguments are automatically validated based on their definition, but you may also want to enforce more complex validation rules.

Laravel MCP integrates seamlessly with Laravel's validation system. You may validate incoming prompt arguments within your prompt's `handle()` method:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);
        
        $tone = $validated['tone'];
        
        // Generate the prompt response using the given tone...
    }
}
```

<a name="prompt-dependency-injection"></a>
### Prompt Dependency Injection

The Laravel service container is used to resolve all prompts. As a result, you are able to type-hint any dependencies your prompt may need in its constructor. The declared dependencies will automatically be resolved and injected into the prompt instance:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Create a new prompt instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}
    
    //
}
```

In addition to constructor injection, you may also type-hint dependencies in your prompt's `handle()` method. The service container will automatically resolve and inject the dependencies when the method is called:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        //

        $isAvailable = $weather->isServiceAvailable();

        //
    }
}
```

<a name="conditional-prompt-registration"></a>
### Conditional Prompt Registration

You may conditionally register prompts at runtime by implementing the `shouldRegister` method in your prompt class. This method allows you to determine whether a prompt should be available based on application state, configuration, or request parameters:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * Determine if the prompt should be registered.
     */
    public function shouldRegister(): bool
    {
        return config('features.weather_prompts_enabled', false);
    }
}
```

The `shouldRegister` method can also accept the current `Request` instance, allowing you to make registration decisions based on request parameters:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * Determine if the prompt should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->isSubscribed() ?? false;
    }
}
```

When a prompt's `shouldRegister` method returns `false`, it will not appear in the list of available prompts and cannot be invoked by AI clients.

<a name="prompt-responses"></a>
### Prompt Responses

Prompts may return a single `Laravel\Mcp\Response` or an iterable of `Laravel\Mcp\Response` instances. These responses encapsulate the content that will be sent to the AI client:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     *
     * @return array<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): array
    {
        $tone = $request->string('tone');
        
        $systemMessage = "You are a helpful weather assistant. Please provide a weather description in a {$tone} tone.";
        $userMessage = "What is the current weather like in New York City?";
        
        return [
            Response::text($systemMessage)->asAssistant(),
            Response::text($userMessage),
        ];
    }
}
```

You can use the `asAssistant()` method to indicate that a response message should be treated as coming from the AI assistant, while regular messages are treated as user input.

<a name="creating-resources"></a>
## Creating Resources

Resources enable your server to expose data and content that AI clients can read and use as context when interacting with language models. They provide a way to share static or dynamic information like documentation, configuration, or any data that helps inform AI responses. Create a resource using the `make:mcp-resource` Artisan command:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

After creating a resource, register it in your server's `$resources` property:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The resources registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

<a name="resource-name-title-and-description"></a>
### Resource Name, Title, and Description

By default, the resource's name and title are derived from the class name. For example, `WeatherGuidelinesResource` will have a `weather_guidelines` name and `Weather Guidelines Resource` title. You may customize these values by overriding the `$name` and `$title` properties:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * The resource's name.
     */
    protected string $name = 'weather_api_docs';
    
    /**
     * The resource's title.
     */
    protected string $title = 'Weather API Documentation';
    
    //
}
```

On the other hand, the resource's description is not automatically generated. You should always provide a meaningful description by overriding the `$description` property:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * The resource's description.
     */
    protected string $description = 'Comprehensive guidelines for using the Weather API.';
    
    //
}
```

<a name="resource-content"></a>
### Resource Content

Resources must implement the `read()` method to provide their content. This method should return the actual data that will be sent to AI clients:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Get the resource's content.
     */
    public function read(): string
    {
        return file_get_contents(resource_path('weather/guidelines.md'));
    }
}
```

<a name="resource-uri-and-mime-type"></a>
### Resource URI and MIME Type

Resources are identified by a URI and have an associated MIME type. You can customize these by overriding the `uri()` and `mimeType()` methods:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Get the resource's URI.
     */
    public function uri(): string
    {
        return 'weather://guidelines/api-documentation';
    }
    
    /**
     * Get the resource's MIME type.
     */
    public function mimeType(): string
    {
        return 'text/markdown';
    }
    
    /**
     * Get the resource's content.
     */
    public function read(): string
    {
        return file_get_contents(resource_path('weather/guidelines.md'));
    }
}
```

<a name="binary-resources"></a>
### Binary Resources

Resources can also serve binary content like images or other non-text files. The framework automatically detects binary content and handles it appropriately:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherMapResource extends Resource
{
    /**
     * The resource's description.
     */
    protected string $description = 'Current weather radar map image.';
    
    /**
     * Get the resource's content.
     */
    public function read(): string
    {
        return file_get_contents(storage_path('weather/current-radar.png'));
    }
    
    /**
     * Get the resource's URI.
     */
    public function uri(): string
    {
        return 'weather://maps/current-radar';
    }
    
    /**
     * Get the resource's MIME type.
     */
    public function mimeType(): string
    {
        return 'image/png';
    }
}
```

<a name="resource-dependency-injection"></a>
### Resource Dependency Injection

The Laravel service container is used to resolve all resources. As a result, you are able to type-hint any dependencies your resource may need in its constructor. The declared dependencies will automatically be resolved and injected into the resource instance:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use App\Services\CacheService;
use Laravel\Mcp\Server\Resource;

class WeatherHistoryResource extends Resource
{
    /**
     * Create a new resource instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
        protected CacheService $cache,
    ) {}
    
    /**
     * Get the resource's content.
     */
    public function read(): string
    {
        return $this->cache->remember('weather-history', 3600, function () {
            return $this->weather->getHistoricalData();
        });
    }
}
```

<a name="conditional-resource-registration"></a>
### Conditional Resource Registration

You may conditionally register resources at runtime by implementing the `shouldRegister` method in your resource class. This method allows you to determine whether a resource should be available based on application state, configuration, or request parameters:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class PremiumWeatherDataResource extends Resource
{
    /**
     * Determine if the resource should be registered.
     */
    public function shouldRegister(): bool
    {
        return config('features.premium_weather_data_enabled', false);
    }
}
```

The `shouldRegister` method can also accept the current `Request` instance, allowing you to make registration decisions based on request parameters:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class DetailedWeatherResource extends Resource
{
    /**
     * Determine if the resource should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->hasFeature('detailed_weather') ?? false;
    }
}
```

When a resource's `shouldRegister` method returns `false`, it will not appear in the list of available resources and cannot be accessed by AI clients.


<a name="testing-servers"></a>
## Testing Servers

The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is an interactive tool for testing and debugging your MCP servers. Use it to connect to your server, verify authentication, and try out tools, resources, and prompts.

Run the inspector for a server you registered (for example, a local server named "weather"):

```shell
php artisan mcp:inspector weather
```

This command launches the MCP Inspector and provides the client settings you can copy into your MCP client to ensure everything is configured correctly. If your web server is protected by middleware (e.g., authentication), make sure to include the required headers (such as an Authorization bearer token) when connecting.
