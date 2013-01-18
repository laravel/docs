# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)

<a name="introduction"></a>
## Introduction

All of the configuration files for the Laravel framework are stored in the `app/config` directory. Each option in every file is documented, so feel free to look through the files and get familiar with the options available to you.

Sometimes you may need to access configuration values at run-time. You may do so using the `Config` class:

**Accessing A Configuration Value**

	Config::get('app.timezone');

Notice that "dot" style syntax may be used to access values in the various files. You may also set configuration values at run-time:

**Setting A Configuration Value**

	Config::set('database.default', 'sqlite');

<a name="environment-configuration"></a>
## Environment Configuration

It is often helpful to have different configuration values based on the environment the application is running in. For example, you may wish to use a different cache driver on your local development machine than on the production server. It is easy to accomplish this using environment based configuration.

Simply create a folder within the `config` directory that matches your environment name, such as `local`. Next, create the configuration files you wish to override and specify the options for that environment. For example, to override the cache driver for the local environment, you would create a `cache.php` file in `app/config/local` with the following content:

	<?php

	return array(

		'driver' => 'file',

	);

Notice that you do not have to specify _every_ option that is in the base configuration file, but only the options you wish to override. The environment configuration files will "cascade" over the base files.

Next, we need to instruct the framework how to determine which environment it is running in. The default environment is always `production`. However, you may setup other environments within the `start.php` file at the root of your installation. In this file you will find an `$app->detectEnvironment` call. The array passed to this method is used to determine the current environment. You may add other environments and machine names to the array as needed.

A good example for local development is:

	'local' => array('http://localhost*', '*.dev'),
	
This will set the current environment to 'local' if your app is served from localhost (and anything after that) or if you have configured a virtual host which ends in .dev. For example:

	http://laravel4app.dev
	
