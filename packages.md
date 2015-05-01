# Package Development

- [Introduction](#introduction)
- [Views](#views)
- [Translations](#translations)
- [Configuration](#configuration)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)
- [Routing](#routing)

<a name="introduction"></a>
## Introduction

Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon), or an entire BDD testing framework like [Behat](https://github.com/Behat/Behat).

Of course, there are different types of packages. Some packages are stand-alone, meaning they work with any framework, not just Laravel. Both Carbon and Behat are examples of stand-alone packages. Any of these packages may be used with Laravel by simply requesting them in your `composer.json` file.

On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those that are Laravel specific.

All Laravel packages are distributed via [Packagist](http://packagist.org) and [Composer](http://getcomposer.org), so learning about these wonderful PHP package distribution tools is essential.

<a name="views"></a>
## Views

Your package's internal structure is entirely up to you; however, typically each package will contain one or more [service providers](/docs/{{version}}/providers). The service provider contains any [service container](/docs/{{version}}/container) bindings, as well as instructions as to where package configuration, views, and translation files are located.

### Views

Package views are typically referenced using a double-colon "namespace" syntax:

	return view('package::view.name');

All you need to do is tell Laravel where the views for a given namespace are located. For example, if your package is named "courier", you might add the following to your service provider's `boot` method:

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
	}

Now you may load your package views using the following syntax:

	return view('courier::view.name');

When you use the `loadViewsFrom` method, Laravel actually registers **two** locations for your views: one in the application's `resources/views/vendor` directory and one in the directory you specify. So, using our `courier` example: when requesting a package view, Laravel will first check if a custom version of the view has been provided by the developer in `resources/views/vendor/courier`. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for end-users to customize / override your package's views.

#### Publishing Views

To publish your package's views to the `resources/views/vendor` directory, you should use the `publishes` method from the `boot` method of your service provider:

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

Now, when users of your package execute Laravel's `vendor:publish` command, your views directory will be copied to the specified location.

If you would like to overwrite existing files, use the `--force` switch:

	php artisan vendor:publish --force

> **Note:** You may use the `publishes` method to publish **any** type of file to any location you wish.

<a name="translations"></a>
## Translations

Package translation files are typically referenced using a double-colon syntax:

	return trans('package::file.line');

All you need to do is tell Laravel where the translations for a given namespace are located. For example, if your package is named "courier", you might add the following to your service provider's `boot` method:

	public function boot()
	{
		$this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
	}

Note that within your `translations` folder, you would have further directories for each language, such as `en`, `es`, `ru`, etc.

Now you may load your package translations using the following syntax:

	return trans('courier::file.line');

<a name="configuration"></a>
## Configuration

Typically, you will want to publish your package's configuration file to the application's own `config` directory. This will allow users of your package to easily override your default configuration options.

To publish a configuration file, just use the `publishes` method from the `boot` method of your service provider:

	$this->publishes([
		__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
	]);

Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified location. Of course, once your configuration has been published, it can be accessed like any other configuration file:

	$value = config('courier.option');

You may also choose to merge your own package configuration file with the application's copy. This allows your users to include only the options they actually want to override in the published copy of the configuration. To merge the configurations, use the `mergeConfigFrom` method within your service provider's `register` method:

	$this->mergeConfigFrom(
		__DIR__.'/path/to/config/courier.php', 'courier'
	);

<a name="public-assets"></a>
## Public Assets

Your packages may have assets such as JavaScript, CSS, and images. To publish assets, use the `publishes` method from your service provider's `boot` method. In this example, we will also add a "public" asset group tag.

	$this->publishes([
		__DIR__.'/path/to/assets' => public_path('vendor/courier'),
	], 'public');

Now, when your package's users execute the `vendor:publish` command, your files will be copied to the specified location. Since you typically will need to overwrite the assets every time the package is updated, you may use the `--force` flag:

	php artisan vendor:publish --tag=public --force

If you would like to make sure your public assets are always up-to-date, you can add this command to the `post-update-cmd` list in your `composer.json` file.

<a name="publishing-file-groups"></a>
## Publishing File Groups

You may want to publish groups of files separately. For instance, you might want your users to be able to publish your package's configuration files and asset files separately. You can do this by 'tagging' them:

	// Publish a config file
	$this->publishes([
		__DIR__.'/../config/package.php' => config_path('package.php')
	], 'config');

	// Publish your migrations
	$this->publishes([
		__DIR__.'/../database/migrations/' => database_path('/migrations')
	], 'migrations');

You can then publish these files separately by referencing their tag like so:

	php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"

<a name="routing"></a>
## Routing

To load a routes file for your package, simply `include` it from within your service provider's `boot` method.

#### Including A Routes File From A Service Provider

	public function boot()
	{
		include __DIR__.'/../../routes.php';
	}

> **Note:** If your package is using controllers, you will need to make sure they are properly configured in your `composer.json` file's auto-load section.
