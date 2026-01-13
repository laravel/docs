# AI Assisted Development

- [Introduction](#introduction)
    - [Why Laravel for AI Development?](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [Installation](#installation)
    - [Available Tools](#available-tools)
    - [AI Guidelines](#ai-guidelines)
    - [Documentation Search](#documentation-search)
    - [IDE Integration](#ide-integration)
- [Custom Boost Guidelines](#custom-guidelines)
    - [Adding Project Guidelines](#adding-project-guidelines)
    - [Package Guidelines](#package-guidelines)

<a name="introduction"></a>
## Introduction

Laravel is uniquely positioned to be the best framework for AI assisted and agentic development. The rise of AI coding agents like [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), and [GitHub Copilot](https://github.com/features/copilot) has transformed how developers write code. These tools can generate entire features, debug complex issues, and refactor code at unprecedented speed - but their effectiveness depends heavily on how well they understand your codebase.

<a name="why-laravel-for-ai-development"></a>
### Why Laravel for AI Development?

Laravel's opinionated conventions and well-defined structure make it an ideal framework for AI assisted development. When you ask an AI agent to add a controller, it knows exactly where to place it. When you need a new migration, the naming conventions and file locations are predictable. This consistency eliminates the guesswork that often trips up AI tools in more flexible frameworks.

Beyond file organization, Laravel's expressive syntax and comprehensive documentation give AI agents the context they need to generate accurate, idiomatic code. Features like Eloquent relationships, form requests, and middleware follow patterns that agents can reliably understand and replicate. The result is AI-generated code that looks like it was written by a seasoned Laravel developer, not stitched together from generic PHP snippets.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost) bridges the gap between AI coding agents and your Laravel application. Boost is an MCP (Model Context Protocol) server equipped with over 15 specialized tools that provide AI agents with deep insight into your application's structure, database, routes, and more. When you install Boost, your AI agent transforms from a general-purpose code assistant into a Laravel expert that understands your specific application.

Boost provides three major capabilities: a suite of MCP tools for inspecting and interacting with your application, composable AI guidelines crafted specifically for the Laravel ecosystem, and a powerful documentation API containing over 17,000 pieces of Laravel-specific knowledge.

<a name="installation"></a>
### Installation

Boost can be installed in Laravel 10, 11, and 12 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency:

```shell
composer require laravel/boost --dev
```

Once installed, run the interactive installer:

```shell
php artisan boost:install
```

The installer will auto-detect your IDE and AI agents, allowing you to select the integrations that make sense for your project. Boost will generate the necessary configuration files, such as `.mcp.json` for MCP-compatible editors and guideline files for AI context.

> [!NOTE]
> Generated configuration files like `.mcp.json`, `CLAUDE.md`, and `boost.json` can be safely added to your `.gitignore` if you prefer each developer to configure their own environment.

<a name="available-tools"></a>
### Available Tools

Boost exposes a comprehensive set of tools to AI agents via the Model Context Protocol. These tools allow agents to deeply understand and interact with your Laravel application:

<div class="content-list" markdown="1">

- **Application Introspection** - Query your PHP and Laravel versions, list installed packages, and inspect your application's configuration and environment variables.
- **Database Tools** - Inspect your database schema, execute read-only queries, and understand your data structure without leaving the conversation.
- **Route Inspection** - List all registered routes with their middleware, controllers, and parameters.
- **Artisan Commands** - Discover available Artisan commands and their arguments, enabling agents to suggest and execute the right commands for your task.
- **Log Analysis** - Read and analyze your application's log files to help debug issues.
- **Browser Logs** - Access browser console logs and errors when developing with Laravel's frontend tools.
- **Tinker Integration** - Execute PHP code in the context of your application via Laravel Tinker, allowing agents to test hypotheses and verify behavior.
- **Documentation Search** - Search Laravel ecosystem documentation with results tailored to your installed package versions.

</div>

<a name="ai-guidelines"></a>
### AI Guidelines

Boost includes a comprehensive set of AI guidelines specifically crafted for the Laravel ecosystem. These guidelines teach AI agents how to write idiomatic Laravel code, follow framework conventions, and avoid common pitfalls. Guidelines are composable and version-aware, meaning agents receive instructions appropriate for your exact package versions.

Guidelines are available for Laravel itself and over 16 packages in the Laravel ecosystem, including:

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, and 4.x)
- Inertia.js (React and Vue variants)
- Tailwind CSS (3.x and 4.x)
- Filament (3.x and 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- And many more

</div>

When you run `boost:install`, Boost automatically detects which packages your application uses and assembles the relevant guidelines into your project's AI context files.

<a name="documentation-search"></a>
### Documentation Search

Boost includes a powerful documentation API that gives AI agents access to over 17,000 pieces of Laravel ecosystem documentation. Unlike generic web searches, this documentation is indexed, vectorized, and filtered to match your exact package versions.

When an agent needs to understand how a feature works, it can search Boost's documentation API and receive accurate, version-specific information. This eliminates the common problem of AI agents suggesting deprecated methods or syntax from older framework versions.

<a name="ide-integration"></a>
### IDE Integration

Boost integrates with popular IDEs and AI tools that support the Model Context Protocol. Here's how to enable Boost in a few popular editors:

```text tab="Claude Code"
// torchlight! {"lineNumbers": false}
Boost is typically detected automatically. If manual setup is needed:

1. Open a terminal in your project directory
2. Run: claude mcp add laravel-boost -- php artisan boost:mcp
```

```text tab=Cursor
// torchlight! {"lineNumbers": false}
1. Open the command palette (Cmd+Shift+P or Ctrl+Shift+P)
2. Select "MCP: Open Settings"
3. Toggle on the "laravel-boost" option
```

```text tab="VS Code"
// torchlight! {"lineNumbers": false}
1. Open the command palette (Cmd+Shift+P or Ctrl+Shift+P)
2. Select "MCP: List Servers"
3. Navigate to "laravel-boost" and press enter
4. Select "Start server"
```

```text tab=PhpStorm
// torchlight! {"lineNumbers": false}
1. Press Shift twice to open Search Everywhere
2. Search for "MCP Settings" and press enter
3. Enable the checkbox next to "laravel-boost"
4. Click "Apply"
```

```text tab=Codex
// torchlight! {"lineNumbers": false}
Boost is typically detected automatically. If manual setup is needed:

1. Open a terminal in your project directory
2. Run: codex mcp add -- php artisan boost:mcp
```

```text tab=Gemini
// torchlight! {"lineNumbers": false}
Boost is typically detected automatically. If manual setup is needed:

1. Open a terminal in your project directory
2. Run: gemini mcp add laravel-boost -- php artisan boost:mcp
```

<a name="custom-guidelines"></a>
## Custom Boost Guidelines

While Boost's built-in guidelines cover the Laravel ecosystem comprehensively, you may want to add project-specific instructions for your AI agents.

<a name="adding-project-guidelines"></a>
### Adding Project Guidelines

To add custom guidelines for your project, create `.blade.php` or `.md` files in your application's `.ai/guidelines` directory:

```text
.ai/
└── guidelines/
    └── api-conventions.md
    ├── architecture.md
    ├── testing-standards.blade.php
```

These files will automatically be included when you run `boost:install`. Use these guidelines to document your team's coding standards, architectural decisions, domain-specific terminology, or any other context that would help AI agents write better code for your project.

<a name="package-guidelines"></a>
### Package Guidelines

If you maintain a Laravel package and want to provide AI guidelines for your users, you can include guidelines in your package's `resources/boost/guidelines` directory:

```text
resources/
└── boost/
    └── guidelines/
        └── core.blade.php
```

AI guidelines should provide a short overview of what your package does, outline any required file structure or conventions, and explain how to create or use its main features (with example commands or code snippets). Keep them concise, actionable, and focused on best practices so AI can generate correct code for your users. Here is an example:

```md
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

When users install Boost in an application that includes your package, your guidelines will automatically be discovered and included in their AI context. This allows package authors to help AI agents understand how to properly use their packages.
