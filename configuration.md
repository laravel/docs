# Configuration

- [Introduction](#introduction)
- [After Installation](#after-installation)
- [Environment Configuration](#environment-configuration)
- [Protecting Sensitive Configuration](#protecting-sensitive-configuration)
- [Maintenance Mode](#maintenance-mode)
- [Pretty URLs](#pretty-urls)

<a name="introduction"></a>
## Introduction

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

<a name="configuration"></a>
## After Installation

### Naming Your Application

The first thing you should do after installing Laravel is name your application. By default, the `app` directory is namespaced under `App`, and autoloaded by Composer using the [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/). However, you should change the namespace to match the name of your application, which you can easily do via the `app:name` Artisan command.

For example, if your application is named "Horsefly", you should run the following command from the root of your installation:

	php artisan app:name Horsefly

### Other Configuration

Laravel needs very little configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your location.

Once Laravel is installed, you should also [configure your local environment](/docs/master/configuration#environment-configuration). This will allow you to receive detailed error messages when developing on your local machine. By default, detailed error reporting is disabled in your production configuration file.

> **Note:** You should never have the `app.debug` configuration option set to `true` for a production application.

<a name="permissions"></a>
### Permissions

The `storage` directory requires write access by the web server.

<a name="environment-configuration"></a>
## Environment Configuration

It is often helpful to have different configuration values based on the environment the application is running in. For example, you may wish to use a different cache driver on your local development machine than on the production server. It is easy to accomplish this using environment based configuration.

To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file. If you wish, you may rename this file to `.env`. All of the variables listed in this file will be loaded into the `$_ENV` PHP super-global when your application receives a request. You may use the `env` helper to retrieve values from these variables. In fact, if you review the Laravel configuration files, you will notice several of the options already using this helper!

Feel free to modify your environment variables as needed for your own local development server, as well as your production environment. However, your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration.

#### Accessing The Current Application Environment

You may access the current application environment via the `environment` method on the `Application` instance:

	$environment = $app->environment();

You may also pass arguments to the `environment` method to check if the environment matches a given value:

	if ($app->environment('local'))
	{
		// The environment is local
	}

	if ($app->environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

To obtain an instance of the application, resolve the `Illuminate\Contracts\Foundation\Application` contract via the [service container](/docs/master/container). Of course, if you are within a [service provider](/docs/master/providers), the application instance is available via the `$this->app` instance variable.

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all routes into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, an `HttpException` will be thrown with a status code of 503.

To enable maintenance mode, simply execute the `down` Artisan command:

	php artisan down

To disable maintenance mode, use the `up` command:

	php artisan up

### Maintenance Mode Response Template

The default template for maintenance mode responses is located in `resources/templates/errors/503.blade.php`.

### Maintenance Mode & Queues

While your application is in maintenance mode, no [queued jobs](/docs/master/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.

<a name="pretty-urls"></a>
## Pretty URLs

### Apache

The framework ships with a `public/.htaccess` file that is used to allow URLs without `index.php`. If you use Apache to serve your Laravel application, be sure to enable the `mod_rewrite` module.

If the `.htaccess` file that ships with Laravel does not work with your Apache installation, try this one:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

On Nginx, the following directive in your site configuration will allow "pretty" URLs:

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

Of course, when using [Homestead](/docs/master/homestead), pretty URLs will be configured automatically.
