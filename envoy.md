# Envoy Task Runner

- [Introduction](#introduction)
    - [Installation](#installation)
- [Writing Tasks](#writing-tasks)
    - [Setup](#setup)
    - [Variables](#variables)
    - [Stories](#stories)
    - [Multiple Servers](#multiple-servers)
- [Running Tasks](#running-tasks)
    - [Confirming Task Execution](#confirming-task-execution)
- [Notifications](#notifications)
    - [Slack](#slack)

<a name="introduction"></a>
## Introduction

[Laravel Envoy](https://github.com/laravel/envoy) provides a clean, minimal syntax for defining common tasks you run on your remote servers. Using Blade style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems.

<a name="installation"></a>
### Installation

First, install Envoy using the Composer `global require` command:

    composer global require "laravel/envoy=~1.0"

Since global Composer libraries can sometimes cause package version conflicts, you may wish to consider using `cgr`, which is a drop-in replacement for the `composer global require` command. The `cgr` library's installation instructions can be [found on GitHub](https://github.com/consolidation-org/cgr).

> {note} Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `envoy` executable is found when running the `envoy` command in your terminal.

#### Updating Envoy

You may also use Composer to keep your Envoy installation up to date. Issuing the `composer global update` command will update all of your globally installed Composer packages:

    composer global update

<a name="writing-tasks"></a>
## Writing Tasks

All of your Envoy tasks should be defined in an `Envoy.blade.php` file in the root of your project. Here's an example to get you started:

    @servers(['web' => ['user@192.168.1.1']])

    @task('foo', ['on' => 'web'])
        ls -la
    @endtask

As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers in the `on` option of your task declarations. Within your `@task` declarations, you should place the Bash code that should run on your server when the task is executed.

You can force a script to run locally by specifying the server's IP address as `127.0.0.1`:

    @servers(['localhost' => '127.0.0.1'])

<a name="setup"></a>
### Setup

Sometimes, you may need to execute some PHP code before executing your Envoy tasks. You may use the ```@setup``` directive to declare variables and do other general PHP work before any of your other tasks are executed:

    @setup
        $now = new DateTime();

        $environment = isset($env) ? $env : "testing";
    @endsetup

If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file:

    @include('vendor/autoload.php')

    @task('foo')
        # ...
    @endtask

<a name="variables"></a>
### Variables

If needed, you may pass option values into Envoy tasks using the command line:

    envoy run deploy --branch=master

You may access the options in your tasks via Blade's "echo" syntax. Of course, you may also use `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command:

    @servers(['web' => '192.168.1.1'])

    @task('deploy', ['on' => 'web'])
        cd site

        @if ($branch)
            git pull origin {{ $branch }}
        @endif

        php artisan migrate
    @endtask

<a name="stories"></a>
### Stories

Stories group a set of tasks under a single, convenient name, allowing you to group small, focused tasks into large tasks. For instance, a `deploy` story may run the `git` and `composer` tasks by listing the task names within its definition:

    @servers(['web' => '192.168.1.1'])

    @story('deploy')
        git
        composer
    @endstory

    @task('git')
        git pull origin master
    @endtask

    @task('composer')
        composer install
    @endtask

Once the story has been written, you may run it just like a typical task:

    envoy run deploy

<a name="multiple-servers"></a>
### Multiple Servers

Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers, list each of the servers in the task's `on` array:

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2']])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

#### Parallel Execution

By default, tasks will be executed on each server serially. In other words, a task will finish running on the first server before proceeding to execute on the second server. If you would like to run a task across multiple servers in parallel, add the `parallel` option to your task declaration:

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="running-tasks"></a>
## Running Tasks

To run a task or story that is defined in your `Envoy.blade.php` file, execute Envoy's `run` command, passing the name of the task or story you would like to execute. Envoy will run the task and display the output from the servers as the task is running:

    envoy run task

<a name="confirming-task-execution"></a>
### Confirming Task Execution

If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations:

    @task('deploy', ['on' => 'web', 'confirm' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="notifications"></a>
<a name="hipchat-notifications"></a>
## Notifications

<a name="slack"></a>
### Slack

Envoy also supports sending notifications to [Slack](https://slack.com) after each task is executed. The `@slack` directive accepts a Slack hook URL and a channel name. You may retrieve your webhook URL by creating an "Incoming WebHooks" integration in your Slack control panel. You should pass the entire webhook URL into the `@slack` directive:

    @finished
        @slack('webhook-url', '#bots')
    @endfinished

You may provide one of the following as the channel argument:

<div class="content-list" markdown="1">
- To send the notification to a channel: `#channel`
- To send the notification to a user: `@user`
</div>

