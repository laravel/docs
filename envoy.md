# Envoy Task Runner

- [Introduction](#introduction)
- [Installation](#envoy-installation)
- [Running Tasks](#envoy-running-tasks)
- [Multiple Servers](#envoy-multiple-servers)
- [Parallel Execution](#envoy-parallel-execution)
- [Task Macros](#envoy-task-macros)
- [Notifications](#envoy-notifications)
- [Updating Envoy](#envoy-updating-envoy)

<a name="introduction"></a>
## Introduction

[Laravel Envoy](https://github.com/laravel/envoy) provides a clean, minimal syntax for defining common tasks you run on your remote servers. Using a Blade style syntax, you can easily setup tasks for deployment, Artisan commands, and more.

> **Note:** Envoy requires PHP version 5.4 or greater, and only runs on Mac / Linux operating systems.

<a name="envoy-installation"></a>
## Installation

First, install Envoy using the Composer `global` command:

	composer global require "laravel/envoy=~1.0"

Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `envoy` executable is found when you run the `envoy` command in your terminal.

Next, create an `Envoy.blade.php` file in the root of your project. Here's an example to get you started:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

As you can see, an array of `@servers` is defined at the top of the file. You can reference these servers in the `on` option of your task declarations. Within your `@task` declarations you should place the Bash code that will be run on your server when the task is executed.

The `init` command may be used to easily create a stub Envoy file:

	envoy init user@192.168.1.1

<a name="envoy-running-tasks"></a>
## Running Tasks

To run a task, use the `run` command of your Envoy installation:

	envoy run foo

If needed, you may pass variables into the Envoy file using command line switches:

	envoy run deploy --branch=master

You may use the options via the Blade syntax you are used to:

	@servers(['web' => '192.168.1.1'])

	@task('deploy', ['on' => 'web'])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

#### Bootstrapping

You may use the ```@setup``` directive to declare variables and do general PHP work inside the Envoy file:

	@setup
		$now = new DateTime();

		$environment = isset($env) ? $env : "testing";
	@endsetup

You may also use ```@include``` to include any PHP files:

	@include('vendor/autoload.php');

#### Confirming Tasks Before Running

If you would like to be prompted for confirmation before running a given task on your servers, you may use the `confirm` directive:

	@task('deploy', ['on' => 'web', 'confirm' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-multiple-servers"></a>
## Multiple Servers

You may easily run a task across multiple servers. Simply list the servers in the task declaration:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

By default, the task will be executed on each server serially. Meaning, the task will finish running on the first server before proceeding to execute on the next server.

<a name="envoy-parallel-execution"></a>
## Parallel Execution

If you would like to run a task across multiple servers in parallel, simply add the `parallel` option to your task declaration:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-task-macros"></a>
## Task Macros

Macros allow you to define a set of tasks to be run in sequence using a single command. For instance:

	@servers(['web' => '192.168.1.1'])

	@macro('deploy')
		foo
		bar
	@endmacro

	@task('foo')
		echo "HELLO"
	@endtask

	@task('bar')
		echo "WORLD"
	@endtask

The `deploy` macro can now be run via a single, simple command:

	envoy run deploy

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
## Notifications

#### HipChat

After running a task, you may send a notification to your team's HipChat room using the simple `@hipchat` directive:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

	@after
		@hipchat('token', 'room', 'Envoy')
	@endafter

You can also specify a custom message to the hipchat room. Any variables declared in ```@setup``` or included with ```@include``` will be available for use in the message:

	@after
		@hipchat('token', 'room', 'Envoy', "$task ran on [$environment]")
	@endafter

This is an amazingly simple way to keep your team notified of the tasks being run on the server.

#### Slack

The following syntax may be used to send a notification to [Slack](https://slack.com):

	@after
		@slack('hook', 'channel', 'message')
	@endafter

You may retrieve your webhook URL by creating an `Incoming WebHooks` integration on Slack's website. The `hook` argument should be the entire webhook URL provided by the Incoming Webhooks Slack Integration. For example:

	https://hooks.slack.com/services/ZZZZZZZZZ/YYYYYYYYY/XXXXXXXXXXXXXXX

You may provide one of the following for the channel argument:

- To send the notification to a channel: `#channel`
- To send the notification to a user: `@user`

If no `channel` argument is provided the default channel will be used.

> Note: Slack notifications will only be sent if all tasks complete successfully.

<a name="envoy-updating-envoy"></a>
## Updating Envoy

To update Envoy, simply use Composer:

	composer global update

