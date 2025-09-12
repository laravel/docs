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
    - [Tool Responses](#tool-responses)

<a name="introduction"></a>
## Introduction

[Laravel MCP](https://github.com/laravel/mcp) provides a simple and elegant way for AI clients to interact with your Laravel application through the Model Context Protocol. It offers an expressive, fluent interface for defining servers, tools, resources, and prompts that enable AI-powered interactions with your application.

<a name="installation"></a>
## Installation

To get started, install Laravel MCP into your project using the Composer package manager:

```shell
composer require laravel/mcp
```

After installing Laravel MCP, you may execute the `vendor:publish` Artisan command, which will publish the `routes/ai.php` file where you'll define your MCP servers:

```shell
php artisan vendor:publish --tag=ai-routes
```

This command will create the `routes/ai.php` file in your application's `routes` directory that you use to register your MCP servers.

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
    protected array $tools = [
        // ExampleTool::class,
    ];

    protected array $resources = [
        // ExampleResource::class,
    ];

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
    ->middleware(['auth:api', 'throttle:60,1']);
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

By default, the tool's name and title are derived from the class name. As example, `CurrentWeatherTool` will have a `current_weather` name and `Current Weather Tool` title. You may customize these values by overriding the `$name` and `$title` properties:

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

The Laravel service container is used to resolve all tools. As a result, you are able to type-hint any dependencies your tool may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance:

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
        protected WeatherRepository $users,
    ) {}
    
    //
}
```

In addition to constructor injection, you may also type-hint dependencies in your tool's `handle()` method. The service container will automatically resolve and inject the dependencies when the method is called:

```php
<?php

namespace App\Http\Mcp\Tools;

use App\Services\WeatherService;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool call.
     */
    public function handle(Request $request, WeatherService $weather): Response
    {
        //
        
        $forecast = $weather->getForecastFor($location);
        
        //
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
use Laravel\Mcp\Server\Tools\Annotations\Title;
use Laravel\Mcp\Server\Tool;

#[Title('Get Current Weather')]
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
                'total' => count($items),
                'item' => $item,
            ]);
            
            $forecasts[] = Response::text($this->forecastFor($location));
        }
        
        yield $responses;
    }
}
```

When using web-based servers, streaming responses automatically open an SSE (Server-Sent Events) stream, sending each yielded message as an event to the client.
