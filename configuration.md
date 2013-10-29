# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
## Introduction

All of the configuration files for the Laravel framework are stored in the `app/config` directory. Each option in every file is documented, so feel free to look through the files and get familiar with the options available to you.

Sometimes you may need to access configuration values at run-time. You may do so using the `Config` class:

**Accessing A Configuration Value**

	Config::get('app.timezone');

You may also specify a default value to return if the configuration option does not exist:

	$timezone = Config::get('app.timezone', 'UTC');

Notice that "dot" style syntax may be used to access values in the various files. You may also set configuration values at run-time:

**Setting A Configuration Value**

	Config::set('database.default', 'sqlite');

Configuration values that are set at run-time are only set for the current request, and will not be carried over to subsequent requests.

<a name="environment-configuration"></a>
## Environment Configuration

It is often helpful to have different configuration values based on the environment the application is running in. For example, you may wish to use a different cache driver on your local development machine than on the production server. It is easy to accomplish this using environment based configuration.

Simply create a folder within the `config` directory that matches your environment name, such as `local`. Next, create the configuration files you wish to override and specify the options for that environment. For example, to override the cache driver for the local environment, you would create a `cache.php` file in `app/config/local` with the following content:

	<?php

	return array(

		'driver' => 'file',

	);

> **Note:** Do not use 'testing' as an environment name. This is reserved for unit testing.

Notice that you do not have to specify _every_ option that is in the base configuration file, but only the options you wish to override. The environment configuration files will "cascade" over the base files.

Next, we need to instruct the framework how to determine which environment it is running in. The default environment is always `production`. However, you may setup other environments within the `bootstrap/start.php` file at the root of your installation. In this file you will find an `$app->detectEnvironment` call. The array passed to this method is used to determine the current environment. You may add other environments and machine names to the array as needed.

    <?php

    $env = $app->detectEnvironment(array(

        'local' => array('your-machine-name'),

    ));

In this example, 'local' is the name of the environment and 'your-machine-name' is the hostname of your server. On Linux and Mac, you may determine your hostname using the `hostname` terminal command.

You may also pass a `Closure` to the `detectEnvironment` method, allowing you to implement your own environment detection:

	$env = $app->detectEnvironment(function()
	{
		return $_SERVER['MY_LARAVEL_ENV'];
	});

You may access the current application environment via the `environment` method:

**Accessing The Current Application Environment**

	$environment = App::environment();

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all routes into your application. This makes it easy to "disable" your application while it is updating. A call to the `App::down` method is already present in your `app/start/global.php` file. The response from this method will be sent to users when your application is in maintenance mode.

To enable maintenance mode, simply execute the `down` Artisan command:

	php artisan down

To disable maintenance mode, use the `up` command:

	php artisan up

To show a custom view when your application is in maintenance mode, you may add something like the following to your application's `app/start/global.php` file:

	App::down(function()
	{
		return Response::view('maintenance', array(), 503);
	});
