# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
- [Provider Configuration](#provider-configuration)
- [Protecting Sensitive Configuration](#protecting-sensitive-configuration)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
## Introduction

All of the configuration files for the Laravel framework are stored in the `app/config` directory. Each option in every file is documented, so feel free to look through the files and get familiar with the options available to you.

Sometimes you may need to access configuration values at run-time. You may do so using the `Config` class:

#### Accessing A Configuration Value

	Config::get('app.timezone');

You may also specify a default value to return if the configuration option does not exist:

	$timezone = Config::get('app.timezone', 'UTC');

#### Setting A Configuration Value

Notice that "dot" style syntax may be used to access values in the various files. You may also set configuration values at run-time:

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

If you need more flexible environment detection, you may pass a `Closure` to the `detectEnvironment` method, allowing you to implement environment detection however you wish:

	$env = $app->detectEnvironment(function()
	{
		return $_SERVER['MY_LARAVEL_ENV'];
	});

#### Accessing The Current Application Environment

You may access the current application environment via the `environment` method:

	$environment = App::environment();

You may also pass arguments to the `environment` method to check if the environment matches a given value:

	if (App::environment('local'))
	{
		// The environment is local
	}

	if (App::environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

<a name="provider-configuration"></a>
### Provider Configuration

When using environment configuration, you may want to "append" environment [service providers](/docs/4.2/ioc#service-providers) to your primary `app` configuration file. However, if you try this, you will notice the environment `app` providers are overriding the providers in your primary `app` configuration file. To force the providers to be appended, use the `append_config` helper method in your environment `app` configuration file:

	'providers' => append_config(array(
		'LocalOnlyServiceProvider',
	))

<a name="protecting-sensitive-configuration"></a>
## Protecting Sensitive Configuration

For "real" applications, it is advisable to keep all of your sensitive configuration out of your configuration files. Things such as database passwords, Stripe API keys, and encryption keys should be kept out of your configuration files whenever possible. So, where should we place them? Thankfully, Laravel provides a very simple solution to protecting these types of configuration items using "dot" files.

First, [configure your application](/docs/4.2/configuration#environment-configuration) to recognize your machine as being in the `local` environment. Next, create a `.env.local.php` file within the root of your project, which is usually the same directory that contains your `composer.json` file. The `.env.local.php` should return an array of key-value pairs, much like a typical Laravel configuration file:

	<?php

	return array(

		'TEST_STRIPE_KEY' => 'super-secret-sauce',

	);

All of the key-value pairs returned by this file will automatically be available via the `$_ENV` and `$_SERVER` PHP "superglobals". You may now reference these globals from within your configuration files:

	'key' => $_ENV['TEST_STRIPE_KEY']

Be sure to add the `.env.local.php` file to your `.gitignore` file. This will allow other developers on your team to create their own local environment configuration, as well as hide your sensitive configuration items from source control.

Now, on your production server, create a `.env.php` file in your project root that contains the corresponding values for your production environment. Like the `.env.local.php` file, the production `.env.php` file should never be included in source control.

> **Note:** You may create a file for each environment supported by your application. For example, the `development` environment will load the `.env.development.php` file if it exists. However, the `production` environment always uses the `.env.php` file.

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all routes into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A call to the `App::down` method is already present in your `app/start/global.php` file. The response from this method will be sent to users when your application is in maintenance mode.

To enable maintenance mode, simply execute the `down` Artisan command:

	php artisan down

To disable maintenance mode, use the `up` command:

	php artisan up

To show a custom view when your application is in maintenance mode, you may add something like the following to your application's `app/start/global.php` file:

	App::down(function()
	{
		return Response::view('maintenance', array(), 503);
	});

If the Closure passed to the `down` method returns `NULL`, maintenance mode will be ignored for that request.

### Maintenance Mode & Queues

While your application is in maintenance mode, no [queue jobs](/docs/4.2/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.
