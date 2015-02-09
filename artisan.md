# Artisan CLI

- [Introduction](#introduction)
- [Usage](#usage)
- [Calling Commands Outside Of CLI](#calling-commands-outside-of-cli)
- [Scheduling Artisan Commands](#scheduling-artisan-commands)

<a name="introduction"></a>
## Introduction

Artisan é o nome da interface da linha de comando incluída no Laravel. Esta interface fornece um bom número de comandos auxiliares para que você use durante o desenvolvimento de sua aplicação. O artisan é impulsionado pelo poderoso componente de Console do Symfony framework.

<a name="usage"></a>
## Usage

#### Listing All Available Commands

Para ver a lista de todos os comandos Artisan, você deve utilizar o comando `list`.

	php artisan list

#### Viewing The Help Screen For A Command

Todos os comandos também incluem uma tela de "help" que mostra e descreve os comandos e seus respectivos parâmetros e opções. Para ver a tela de "help" (ajuda), simplesmente preceda o nome do comando com `help`.

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

You may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/5.0/queues):

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-artisan-commands"></a>
## Scheduling Artisan Commands

In the past, developers have generated a Cron entry for each console command they wished to schedule. However, this is a headache. Your console schedule is no longer in source control, and you must SSH into your server to add the Cron entries. Let's make our lives easier. The Laravel command scheduler allows you to fluently and expressively define your command schedule within Laravel itself, and only a single Cron entry is needed on your server.

Your command schedule is stored in the `app/Console/Kernel.php` file. Within this class you will see a `schedule` method. To help you get started, a simple example is included with the method. You are free to add as many scheduled jobs as you wish to the `Schedule` object. The only Cron entry you need to add to your server is this:

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

This Cron will call the Laravel command scheduler every minute. Then, Laravel evalutes your scheduled jobs and runs the jobs that are due. It couldn't be easier!

### More Scheduling Examples

Let's look at a few more scheduling examples:

#### Scheduling Closures

	$schedule->call(function()
	{
		// Do some task...

	})->hourly();

#### Scheduling Terminal Commands

	$schedule->exec('composer self-update')->daily();

#### Manual Cron Expression

	$schedule->command('foo')->cron('* * * * *');

#### Frequent Jobs

	$schedule->command('foo')->everyFiveMinutes();

	$schedule->command('foo')->everyTenMinutes();

	$schedule->command('foo')->everyThirtyMinutes();

#### Daily Jobs

	$schedule->command('foo')->daily();

#### Daily Jobs At A Specific Time (24 Hour Time)

	$schedule->command('foo')->dailyAt('15:00');

#### Twice Daily Jobs

	$schedule->command('foo')->twiceDaily();

#### Job That Runs Every Weekday

	$schedule->command('foo')->weekdays();

#### Weekly Jobs

	$schedule->command('foo')->weekly();

	// Schedule weekly job for specific day (0-6) and time...
	$schedule->command('foo')->weeklyOn(1, '8:00');

#### Monthly Jobs

	$schedule->command('foo')->monthly();

#### Limit The Environment The Jobs Should Run In

	$schedule->command('foo')->monthly()->environments('production');

#### Indicate The Job Should Run Even When Application Is In Maintenance Mode

	$schedule->command('foo')->monthly()->evenInMaintenanceMode();

#### Only Allow Job To Run When Callback Is True

	$schedule->command('foo')->monthly()->when(function()
	{
		return true;
	});
