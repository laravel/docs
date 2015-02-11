# Artisan Development

- [Introduction](#introduction)
- [Building A Command](#building-a-command)
- [Registering Commands](#registering-commands)
- [Calling Other Commands](#calling-other-commands)

<a name="introduction"></a>
## Introduction

In addition to the commands provided with Artisan, you may also build your own custom commands for working with your application. You may store your custom commands in the `app/commands` directory; however, you are free to choose your own storage location as long as your commands can be autoloaded based on your `composer.json` settings.

<a name="building-a-command"></a>
## Building A Command

### Generating The Class

To create a new command, you may use the `command:make` Artisan command, which will generate a command stub to help you get started:

#### Generate A New Command Class

	php artisan command:make FooCommand

By default, generated commands will be stored in the `app/commands` directory; however, you may specify custom path or namespace:

	php artisan command:make FooCommand --path=app/classes --namespace=Classes

When creating the command, the `--command` option may be used to assign the terminal command name:

	php artisan command:make AssignUsers --command=users:assign

### Writing The Command

Once your command is generated, you should fill out the `name` and `description` properties of the class, which will be used when displaying your command on the `list` screen.

The `fire` method will be called when your command is executed. You may place any command logic in this method.

### Arguments & Options

The `getArguments` and `getOptions` methods are where you may define any arguments or options your command receives. Both of these methods return an array of commands, which are described by a list of array options.

When defining `arguments`, the array definition values represent the following:

	array($name, $mode, $description, $defaultValue)

The argument `mode` may be any of the following: `InputArgument::REQUIRED` or `InputArgument::OPTIONAL`.

When defining `options`, the array definition values represent the following:

	array($name, $shortcut, $mode, $description, $defaultValue)

For options, the argument `mode` may be: `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

The `VALUE_IS_ARRAY` mode indicates that the switch may be used multiple times when calling the command:

	php artisan foo --option=bar --option=baz

The `VALUE_NONE` option indicates that the option is simply used as a "switch":

	php artisan foo --option

### Retrieving Input

While your command is executing, you will obviously need to access the values for the arguments and options accepted by your application. To do so, you may use the `argument` and `option` methods:

#### Retrieving The Value Of A Command Argument

	$value = $this->argument('name');

#### Retrieving All Arguments

	$arguments = $this->argument();

#### Retrieving The Value Of A Command Option

	$value = $this->option('name');

#### Retrieving All Options

	$options = $this->option();

### Writing Output

To send output to the console, you may use the `info`, `comment`, `question` and `error` methods. Each of these methods will use the appropriate ANSI colors for their purpose.

#### Sending Information To The Console

	$this->info('Display this on the screen');

#### Sending An Error Message To The Console

	$this->error('Something went wrong!');

### Asking Questions

You may also use the `ask` and `confirm` methods to prompt the user for input:

#### Asking The User For Input

	$name = $this->ask('What is your name?');

#### Asking The User For Secret Input

	$password = $this->secret('What is the password?');

#### Asking The User For Confirmation

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

You may also specify a default value to the `confirm` method, which should be `true` or `false`:

	$this->confirm($question, true);

<a name="registering-commands"></a>
## Registering Commands

#### Registering An Artisan Command

Once your command is finished, you need to register it with Artisan so it will be available for use. This is typically done in the `app/start/artisan.php` file. Within this file, you may use the `Artisan::add` method to register the command:

	Artisan::add(new CustomCommand);

#### Registering A Command That Is In The IoC Container

If your command is registered in the application [IoC container](/docs/4.2/ioc), you may use the `Artisan::resolve` method to make it available to Artisan:

	Artisan::resolve('binding.name');

#### Registering Commands In A Service Provider

If you need to register commands from within a service provider, you should call the `commands` method from the provider's `boot` method, passing the [IoC container](/docs/4.2/ioc) binding for the command:

	public function boot()
	{
		$this->commands('command.binding');
	}

<a name="calling-other-commands"></a>
## Calling Other Commands

Sometimes you may wish to call other commands from your command. You may do so using the `call` method:

	$this->call('command:name', array('argument' => 'foo', '--option' => 'bar'));
