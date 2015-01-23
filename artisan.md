# Artisan CLI

- [Introduction](#introduction)
- [Usage](#usage)
- [Calling Commands Outside Of CLI](#calling-commands-outside-of-cli)

<a name="introduction"></a>
## Introduction

Artisan is the name of the command-line interface included with Laravel. It provides a number of helpful commands for your use while developing your application. It is driven by the powerful Symfony Console component.

<a name="usage"></a>
## Usage

#### Listing All Available Commands

To view a list of all available Artisan commands, you may use the `list` command:

	php artisan list

#### Viewing The Help Screen For A Command

Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, simply precede the name of the command with `help`:

	php artisan help migrate

#### Specifying The Configuration Environment

You may specify the configuration environment that should be used while running a command using the `--env` switch:

	php artisan migrate --env=local

#### Displaying Your Current Laravel Version

You may also view the current version of your Laravel installation using the `--version` option:

	php artisan --version

<a name="calling-commands-outside-of-cli"></a>
## Calling Commands Outside Of CLI

Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to fire an Artisan command from an HTTP route. Just use the `Artisan` facade:

	Route::get('/foo', function()
	{
		$exitCode = Artisan::call('command:name', ['--option' => 'foo']);

		//
	});

You may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/master/queues):

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});
