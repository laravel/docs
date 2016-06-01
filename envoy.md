# Envoy Task Runner

- [Introduction](#introduction)
- [Writing Tasks](#writing-tasks)
    - [Task Variables](#task-variables)
    - [Multiple Servers](#envoy-multiple-servers)
    - [Task Macros](#envoy-task-macros)
- [Running Tasks](#envoy-running-tasks)
- [Notifications](#envoy-notifications)
    - [HipChat](#hipchat)
    - [Slack](#slack)

<a name="introduction"></a>
## Introduction

[Laravel Envoy](https://github.com/laravel/envoy) provides a clean, minimal syntax for defining common tasks you run on your remote servers. Using a Blade style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems.

<a name="envoy-installation"></a>
### Installation

First, install Envoy using the Composer `global` command:

    composer global require "laravel/envoy=~1.0"

Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `envoy` executable is found when you run the `envoy` command in your terminal.

#### Updating Envoy

You may also use Composer to keep your Envoy installation up to date:

    composer global update

<a name="writing-tasks"></a>
## Writing Tasks

All of your Envoy tasks should be defined in an `Envoy.blade.php` file in the root of your project. Here's an example to get you started:

    @servers(['web' => 'user@192.168.1.1'])

    @task('foo', ['on' => 'web'])
        ls -la
    @endtask

As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers in the `on` option of your task declarations. Within your `@task` declarations, you should place the Bash code that will be run on your server when the task is executed.

#### Local Tasks

You can define a script to run locally by defining a server reference to the local host:

    @servers(['localhost' => '127.0.0.1'])

#### Bootstrapping

Sometimes, you may need to execute some PHP code before evaluating your Envoy tasks. You may use the ```@setup``` directive to declare variables and do general PHP work inside the Envoy file:

    @setup
        $now = new DateTime();

        $environment = isset($env) ? $env : "testing";
    @endsetup

You may also use ```@include``` to include any outside PHP files:

    @include('vendor/autoload.php')

#### Confirming Tasks

If you would like to be prompted for confirmation before running a given task on your servers, you may add the `confirm` directive to your task declaration:

    @task('deploy', ['on' => 'web', 'confirm' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="task-variables"></a>
### Task Variables

If needed, you may pass variables into the Envoy file using command line switches, allowing you to customize your tasks:

    envoy run deploy --branch=master

You may use the options in your tasks via Blade's "echo" syntax:

    @servers(['web' => '192.168.1.1'])

    @task('deploy', ['on' => 'web'])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="envoy-multiple-servers"></a>
### Multiple Servers

You may easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers, simply list the servers in the task declaration's `on` array:

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2']])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

By default, the task will be executed on each server serially. Meaning, the task will finish running on the first server before proceeding to execute on the next server.

#### Parallel Execution

If you would like to run a task across multiple servers in parallel, add the `parallel` option to your task declaration:

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="envoy-task-macros"></a>
### Task Macros

Macros allow you to define a set of tasks to be run in sequence using a single command. For instance, a `deploy` macro may run the `git` and `composer` tasks:

    @servers(['web' => '192.168.1.1'])

    @macro('deploy')
        git
        composer
    @endmacro

    @task('git')
        git pull origin master
    @endtask

    @task('composer')
        composer install
    @endtask

Once the macro has been defined, you may run it via single, simple command:

    envoy run deploy

<a name="envoy-running-tasks"></a>
## Running Tasks

To run a task from your `Envoy.blade.php` file, execute Envoy's `run` command, passing the command the name of the task or macro you would like to execute. Envoy will run the task and display the output from the servers as the task is running:

    envoy run task

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
## Notifications

<a name="hipchat"></a>
### HipChat

After running a task, you may send a notification to your team's HipChat room using Envoy's `@hipchat` directive. The directive accepts an API token, the name of the room, and the username to be displayed as the sender of the message:

    @servers(['web' => '192.168.1.1'])

    @task('foo', ['on' => 'web'])
        ls -la
    @endtask

    @after
        @hipchat('token', 'room', 'Envoy')
    @endafter

If you wish, you may also pass a custom message to send to the HipChat room. Any variables available to your Envoy tasks will also be available when constructing the message:

    @after
        @hipchat('token', 'room', 'Envoy', "$task ran in the $env environment.")
    @endafter

<a name="slack"></a>
### Slack

In addition to HipChat, Envoy also supports sending notifications to [Slack](https://slack.com). The `@slack` directive accepts a Slack hook URL, a channel name, and the message you wish to send to the channel:

    @after
        @slack('hook', 'channel', 'message')
    @endafter

You may retrieve your webhook URL by creating an `Incoming WebHooks` integration on Slack's website. The `hook` argument should be the entire webhook URL provided by the Incoming Webhooks Slack Integration. For example:

    https://hooks.slack.com/services/ZZZZZZZZZ/YYYYYYYYY/XXXXXXXXXXXXXXX

You may provide one of the following as the channel argument:

- To send the notification to a channel: `#channel`
- To send the notification to a user: `@user`

