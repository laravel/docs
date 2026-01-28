# Laravel Boost

- [Introduction](#introduction)
- [Installation](#installation)
    - [Keeping Boost Resources Updated](#keeping-boost-resources-updated)
    - [Set Up Your Agents](#set-up-your-agents)
- [MCP Server](#mcp-server)
    - [Available MCP Tools](#available-mcp-tools)
    - [Manually Registering the MCP Server](#manually-registering-the-mcp-server)
- [AI Guidelines](#ai-guidelines)
    - [Available AI Guidelines](#available-ai-guidelines)
    - [Adding Custom AI Guidelines](#adding-custom-ai-guidelines)
    - [Overriding Boost AI Guidelines](#overriding-boost-ai-guidelines)
    - [Third-Party Package AI Guidelines](#third-party-package-ai-guidelines)
- [Agent Skills](#agent-skills)
    - [Available Skills](#available-skills)
    - [Custom Skills](#custom-skills)
    - [Overriding Skills](#overriding-skills)
    - [Third-Party Package Skills](#third-party-package-skills)
- [Guidelines vs. Skills](#guidelines-vs-skills)
- [Documentation API](#documentation-api)
- [Extending Boost](#extending-boost)
    - [Adding Support for Other IDEs / AI Agents](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## Introduction

Laravel Boost accelerates AI-assisted development by providing the essential guidelines and agent skills that help AI agents write high-quality Laravel applications that adhere to Laravel best practices.

Boost also provides a powerful Laravel ecosystem documentation API that combines a built-in MCP tool with an extensive knowledge base containing over 17,000 pieces of Laravel-specific information, all enhanced by semantic search capabilities using embeddings for precise, context-aware results. Boost instructs AI agents like Claude Code and Cursor to use this API to learn about the latest Laravel features and best practices.

<a name="installation"></a>
## Installation

Laravel Boost can be installed via Composer:

```shell
composer require laravel/boost --dev
```

Next, install the MCP server and coding guidelines:

```shell
php artisan boost:install
```

The `boost:install` command will generate the relevant agent guideline and skill files for the coding agents you selected during the installation process.

Once Laravel Boost has been installed, you're ready to start coding with Cursor, Claude Code, or your AI agent of choice.

> [!NOTE]
> Feel free to add the generated MCP configuration file (`.mcp.json`), guideline files (`CLAUDE.md`, `AGENTS.md`, `junie/`, etc.), and the `boost.json` configuration file to your application's `.gitignore`, as these files are automatically regenerated when running `boost:install` and `boost:update`.

<a name="set-up-your-agents"></a>
### Set Up Your Agents

#### Cursor

1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "/open MCP Settings"
3. Turn the toggle on for `laravel-boost`

#### Claude Code

Claude Code support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

```shell
claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

#### Codex

Codex support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

```shell
codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

#### Gemini CLI

Gemini CLI support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

```shell
gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

#### GitHub Copilot (VS Code)

1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "MCP: List Servers"
3. Arrow to `laravel-boost` and press `enter`
4. Choose "Start server"

#### Junie

1. Press `shift` twice to open the command palette
2. Search "MCP Settings" and press `enter`
3. Check the box next to `laravel-boost`
4. Click "Apply" at the bottom right

<a name="keeping-boost-resources-updated"></a>
### Keeping Boost Resources Updated

You may want to periodically update your local Boost resources (AI guidelines and skills) to ensure they reflect the latest versions of the Laravel ecosystem packages you have installed. To do so, you can use the `boost:update` Artisan command.

```shell
php artisan boost:update
```

You may also automate this process by adding it to your Composer "post-update-cmd" scripts:

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```

<a name="mcp-server"></a>
## MCP Server

Laravel Boost provides an MCP (Model Context Protocol) server that exposes tools for AI agents to interact with your Laravel application. These tools give agents the ability to inspect your application's structure, query the database, execute code, and more.

<a name="available-mcp-tools"></a>
### Available MCP Tools

| Name                       | Notes                                                                                                          |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| Application Info           | Read PHP & Laravel versions, database engine, list of ecosystem packages with versions, and Eloquent models    |
| Browser Logs               | Read logs and errors from the browser                                                                          |
| Database Connections       | Inspect available database connections, including the default connection                                       |
| Database Query             | Execute a query against the database                                                                           |
| Database Schema            | Read the database schema                                                                                       |
| Get Absolute URL           | Convert relative path URIs to absolute so agents generate valid URLs                                           |
| Get Config                 | Get a value from the configuration files using "dot" notation                                                  |
| Last Error                 | Read the last error from the application's log files                                                           |
| List Artisan Commands      | Inspect the available Artisan commands                                                                         |
| List Available Config Keys | Inspect the available configuration keys                                                                       |
| List Available Env Vars    | Inspect the available environment variable keys                                                                |
| List Routes                | Inspect the application's routes                                                                               |
| Read Log Entries           | Read the last N log entries                                                                                    |
| Search Docs                | Query the Laravel hosted documentation API service to retrieve documentation based on installed packages       |
| Tinker                     | Execute arbitrary code within the context of the application                                                   |

<a name="manually-registering-the-mcp-server"></a>
### Manually Registering the MCP Server

Sometimes you may need to manually register the Laravel Boost MCP server with your editor of choice. You should register the MCP server using the following details:

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

JSON example:

```json
{
    "mcpServers": {
        "laravel-boost": {
            "command": "php",
            "args": ["artisan", "boost:mcp"]
        }
    }
}
```

<a name="ai-guidelines"></a>
## AI Guidelines

AI guidelines are composable instruction files that are loaded upfront to provide AI agents with essential context about Laravel ecosystem packages. These guidelines contain core conventions, best practices, and framework-specific patterns that help agents generate consistent, high-quality code.

<a name="available-ai-guidelines"></a>
### Available AI Guidelines

Laravel Boost includes AI guidelines for the following packages and frameworks. The `core` guidelines provide generic, generalized advice to the AI for the given package that is applicable across all versions.

| Package            | Versions Supported     |
|--------------------|------------------------|
| Core & Boost       | core                   |
| Laravel Framework  | core, 10.x, 11.x, 12.x |
| Livewire           | core, 2.x, 3.x, 4.x    |
| Flux UI            | core, free, pro        |
| Folio              | core                   |
| Herd               | core                   |
| Inertia Laravel    | core, 1.x, 2.x         |
| Inertia React      | core, 1.x, 2.x         |
| Inertia Vue        | core, 1.x, 2.x         |
| Inertia Svelte     | core, 1.x, 2.x         |
| MCP                | core                   |
| Pennant            | core                   |
| Pest               | core, 3.x, 4.x         |
| PHPUnit            | core                   |
| Pint               | core                   |
| Sail               | core                   |
| Tailwind CSS       | core, 3.x, 4.x         |
| Livewire Volt      | core                   |
| Wayfinder          | core                   |
| Enforce Tests      | conditional            |

> **Note:** To keep your AI guidelines up-to-date, see the [Keeping Boost Resources Updated](#keeping-boost-resources-updated) section.

<a name="adding-custom-ai-guidelines"></a>
### Adding Custom AI Guidelines

To augment Laravel Boost with your own custom AI guidelines, add `.blade.php` or `.md` files to your application's `.ai/guidelines/*` directory. These files will automatically be included with Laravel Boost's guidelines when you run `boost:install`.

<a name="overriding-boost-ai-guidelines"></a>
### Overriding Boost AI Guidelines

You can override Boost's built-in AI guidelines by creating your own custom guidelines with matching file paths. When you create a custom guideline that matches an existing Boost guideline path, Boost will use your custom version instead of the built-in one.

For example, to override Boost's "Inertia React v2 Form Guidance" guidelines, create a file at `.ai/guidelines/inertia-react/2/forms.blade.php`. When you run `boost:install`, Boost will include your custom guideline instead of the default one.

<a name="third-party-package-ai-guidelines"></a>
### Third-Party Package AI Guidelines

If you maintain a third-party package and would like Boost to include AI guidelines for it, you can do so by adding a `resources/boost/guidelines/core.blade.php` file to your package. When users of your package run `php artisan boost:install`, Boost will automatically load your guidelines.

AI guidelines should provide a short overview of what your package does, outline any required file structure or conventions, and explain how to create or use its main features (with example commands or code snippets). Keep them concise, actionable, and focused on best practices so AI can generate correct code for your users. Here is an example:

```php
## Package Name

This package provides [brief description of functionality].

### Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

<a name="agent-skills"></a>
## Agent Skills

[Agent Skills](https://agentskills.io/home) are lightweight, targeted knowledge modules that agents can activate on-demand when working on specific domains. Unlike guidelines, which are loaded upfront, skills allow detailed patterns and best practices to be loaded only when relevant, reducing context bloat and improving the relevance of AI-generated code.

When you run `boost:install` and select skills as a feature, skills are automatically installed based on the packages detected in your `composer.json`. For example, if your project includes `livewire/livewire`, the `livewire-development` skill will be installed automatically.

<a name="available-skills"></a>
### Available Skills

| Skill                        | Package      |
|------------------------------|--------------|
| fluxui-development           | Flux UI      |
| folio-routing                | Folio        |
| inertia-react-development    | Inertia React|
| inertia-svelte-development   | Inertia Svelte|
| inertia-vue-development      | Inertia Vue  |
| livewire-development         | Livewire     |
| mcp-development              | MCP          |
| pennant-development          | Pennant      |
| pest-testing                 | Pest         |
| tailwindcss-development      | Tailwind CSS |
| volt-development             | Volt         |
| wayfinder-development        | Wayfinder    |

> **Note:** To keep your skills up-to-date, see the [Keeping Boost Resources Updated](#keeping-boost-resources-updated) section.

<a name="custom-skills"></a>
### Custom Skills

To create your own custom skills, add a `SKILL.md` file to your application's `.ai/skills/{skill-name}/` directory. When you run `boost:update`, your custom skills will be installed alongside Boost's built-in skills.

For example, to create a custom skill for your application's domain logic:

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### Overriding Skills

You can override Boost's built-in skills by creating your own custom skills with matching names. When you create a custom skill that matches an existing Boost skill name, Boost will use your custom version instead of the built-in one.

For example, to override Boost's `livewire-development` skill, create a file at `.ai/skills/livewire-development/SKILL.md`. When you run `boost:update`, Boost will include your custom skill instead of the default one.

<a name="third-party-package-skills"></a>
### Third-Party Package Skills

If you maintain a third-party package and would like Boost to include skills for it, you can do so by adding a `resources/boost/skills/{skill-name}/SKILL.md` file to your package. When users of your package run `php artisan boost:install`, Boost will automatically install your skills based on user preference.

Boost Skills support the [Agent Skills format](https://agentskills.io/what-are-skills) and should be structured as a folder containing a `SKILL.md` file with YAML frontmatter and Markdown instructions. The `SKILL.md` file must include required frontmatter (`name` and `description`) and can optionally include scripts, templates, and reference materials.

Skills should outline any required file structure or conventions, and explain how to create or use its main features (with example commands or code snippets). Keep them concise, actionable, and focused on best practices so AI can generate correct code for your users:

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## When to use this skill
Use this skill when working with PackageName features...

## Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

$result = PackageName::featureTwo($param1, $param2);
```

<a name="guidelines-vs-skills"></a>
## Guidelines vs. Skills

Laravel Boost provides two distinct ways to give AI agents context about your application: **guidelines** and **skills**.

**Guidelines** are loaded upfront when the AI agent starts, providing essential context about Laravel conventions and best practices that apply broadly across your codebase.

**Skills** are activated on-demand when working on specific tasks, containing detailed patterns for particular domains (like Livewire components or Pest tests). Loading skills only when relevant reduces context bloat and improves code quality.

| Aspect | Guidelines | Skills |
|--------|------------|--------|
| **Loaded** | Upfront, always present | On-demand, when relevant |
| **Scope** | Broad, foundational | Focused, task-specific |
| **Purpose** | Core conventions & best practices | Detailed implementation patterns |

<a name="documentation-api"></a>
## Documentation API

Laravel Boost includes a Documentation API that provides AI agents with access to an extensive knowledge base containing over 17,000 pieces of Laravel-specific information. The API uses semantic search with embeddings to deliver precise, context-aware results.

The `Search Docs` MCP tool allows agents to query the Laravel hosted documentation API service to retrieve documentation based on your installed packages. Boost's AI guidelines and skills will automatically instruct your coding agent to use this API.

| Package         | Versions Supported |
|-----------------|--------------------|
| Laravel Framework | 10.x, 11.x, 12.x   |
| Filament        | 2.x, 3.x, 4.x, 5.x |
| Flux UI         | 2.x Free, 2.x Pro  |
| Inertia         | 1.x, 2.x           |
| Livewire        | 1.x, 2.x, 3.x, 4.x |
| Nova            | 4.x, 5.x           |
| Pest            | 3.x, 4.x           |
| Tailwind CSS    | 3.x, 4.x           |

<a name="extending-boost"></a>
## Extending Boost

Boost works with many popular IDEs and AI agents out of the box. If your coding tool isn't supported yet, you can create your own agent and integrate it with Boost.

<a name="adding-support-for-other-ides-ai-agents"></a>
### Adding Support for Other IDEs / AI Agents

To add support for a new IDE or AI agent, create a class that extends `Laravel\Boost\Install\Agents\Agent` and implement one or more of the following contracts depending on what you need:

- `Laravel\Boost\Contracts\SupportsGuidelines` - Adds support for AI guidelines.
- `Laravel\Boost\Contracts\SupportsMcp` - Adds support for MCP.
- `Laravel\Boost\Contracts\SupportsSkills` - Adds support for Agent Skills.

<a name="writing-the-agent"></a>
#### Writing the Agent

```php
<?php

declare(strict_types=1);

namespace App;

use Laravel\Boost\Contracts\SupportsGuidelines;
use Laravel\Boost\Contracts\SupportsMcp;
use Laravel\Boost\Contracts\SupportsSkills;
use Laravel\Boost\Install\Agents\Agent;

class CustomAgent extends Agent implements SupportsGuidelines, SupportsMcp, SupportsSkills
{
    // Your implementation...
}
```

For an example implementation, see [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php).

<a name="registering-the-agent"></a>
#### Registering the Agent

Register your custom agent in the `boot` method of your application's `App\Providers\AppServiceProvider`:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

Once registered, your agent will be available for selection when running `php artisan boost:install`.
