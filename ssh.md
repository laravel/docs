# SSH

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Tasks](#tasks)
- [SFTP Downloads](#sftp-downloads)
- [SFTP Uploads](#sftp-uploads)
- [Tailing Remote Logs](#tailing-remote-logs)
- [Envoy Task Runner](#envoy-task-runner)

<a name="configuration"></a>
## Configuration

Laravel includes a simple way to SSH into remote servers and run commands, allowing you to easily build Artisan tasks that work on remote servers. The `SSH` facade provides the access point to connecting to your remote servers and running commands.

The configuration file is located at `app/config/remote.php`, and contains all of the options you need to configure your remote connections. The `connections` array contains a list of your servers keyed by name. Simply populate the credentials in the `connections` array and you will be ready to start running remote tasks. Note that the `SSH` can authenticate using either a password or an SSH key.

> **Note:** Need to easily run a variety of tasks on your remote server? Check out the [Envoy task runner](#envoy-task-runner)!

<a name="basic-usage"></a>
## Basic Usage

#### Running Commands On The Default Server

To run commands on your `default` remote connection, use the `SSH::run` method:

	SSH::run(array(
		'cd /var/www',
		'git pull origin master',
	));

#### Running Commands On A Specific Connection

Alternatively, you may run commands on a specific connection using the `into` method:

	SSH::into('staging')->run(array(
		'cd /var/www',
		'git pull origin master',
	));

#### Catching Output From Commands

You may catch the "live" output of your remote commands by passing a Closure into the `run` method:

	SSH::run($commands, function($line)
	{
		echo $line.PHP_EOL;
	});

## Tasks
<a name="tasks"></a>

If you need to define a group of commands that should always be run together, you may use the `define` method to define a `task`:

	SSH::into('staging')->define('deploy', array(
		'cd /var/www',
		'git pull origin master',
		'php artisan migrate',
	));

Once the task has been defined, you may use the `task` method to run it:

	SSH::into('staging')->task('deploy', function($line)
	{
		echo $line.PHP_EOL;
	});

<a name="sftp-downloads"></a>
## SFTP Downloads

The `SSH` class includes a simple way to download files using the `get` and `getString` methods:

	SSH::into('staging')->get($remotePath, $localPath);

	$contents = SSH::into('staging')->getString($remotePath);

<a name="sftp-uploads"></a>
## SFTP Uploads

The `SSH` class also includes a simple way to upload files, or even strings, to the server using the `put` and `putString` methods:

	SSH::into('staging')->put($localFile, $remotePath);

	SSH::into('staging')->putString($remotePath, 'Foo');

<a name="tailing-remote-logs"></a>
## Tailing Remote Logs

Laravel includes a helpful command for tailing the `laravel.log` files on any of your remote connections. Simply use the `tail` Artisan command and specify the name of the remote connection you would like to tail:

	php artisan tail staging

	php artisan tail staging --path=/path/to/log.file

<a name="envoy-task-runner"></a>
## Envoy Task Runner

- [Installation](#envoy-installation)
- [Running Tasks](#envoy-running-tasks)
- [Multiple Servers](#envoy-multiple-servers)
- [Parallel Execution](#envoy-parallel-execution)
- [Task Macros](#envoy-task-macros)
- [Notifications](#envoy-notifications)
- [Updating Envoy](#envoy-updating-envoy)

Laravel Envoy provides a clean, minimal syntax for defining common tasks you run on your remote servers. Using a [Blade](/docs/4.2/templates#blade-templating) style syntax, you can easily setup tasks for deployment, Artisan commands, and more.

> **Note:** Envoy requires PHP version 5.4 or greater, and only runs on Mac / Linux operating systems.

<a name="envoy-installation"></a>
### Installation

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
### Running Tasks

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

<a name="envoy-multiple-servers"></a>
### Multiple Servers

You may easily run a task across multiple servers. Simply list the servers in the task declaration:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

By default, the task will be executed on each server serially. Meaning, the task will finish running on the first server before proceeding to execute on the next server.

<a name="envoy-parallel-execution"></a>
### Parallel Execution

If you would like to run a task across multiple servers in parallel, simply add the `parallel` option to your task declaration:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-task-macros"></a>
### Task Macros

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
### Notifications

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
		@slack('team', 'token', 'channel')
	@endafter

<a name="envoy-updating-envoy"></a>
### Updating Envoy

To update Envoy, simply run the `self-update` command:

	envoy self-update

If your Envoy installation is in `/usr/local/bin`, you may need to use `sudo`:

	composer global update
