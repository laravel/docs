# Package Development

- [Introduction](#introduction)
- [Creating A Package](#creating-a-package)
- [Package Structure](#package-structure)
- [Service Providers](#service-providers)
- [Deferred Providers](#deferred-providers)
- [Package Conventions](#package-conventions)
- [Development Workflow](#development-workflow)
- [Package Routing](#package-routing)
- [Package Configuration](#package-configuration)
- [Package Views](#package-views)
- [Package Migrations](#package-migrations)
- [Package Assets](#package-assets)
- [Publishing Packages](#publishing-packages)

<a name="introduction"></a>
## Introduction

Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon), or an entire BDD testing framework like [Behat](https://github.com/Behat/Behat).

Of course, there are different types of packages. Some packages are stand-alone, meaning they work with any framework, not just Laravel. Both Carbon and Behat are examples of stand-alone packages. Any of these packages may be used with Laravel by simply requesting them in your `composer.json` file.

On the other hand, other packages are specifically intended for use with Laravel. In previous versions of Laravel, these types of packages were called "bundles". These packages may have routes, controllers, views, configuration, and migrations specifically intended to enhance a Laravel application. As no special process is needed to develop stand-alone packages, this guide primarily covers the development of those that are Laravel specific.

All Laravel packages are distributed via [Packagist](http://packagist.org) and [Composer](http://getcomposer.org), so learning about these wonderful PHP package distribution tools is essential.

<a name="creating-a-package"></a>
## Creating A Package

The easiest way to create a new package for use with Laravel is the `workbench` Artisan command. First, you will need to set a few options in the `app/config/workbench.php` file. In that file, you will find a `name` and `email` option. These values will be used to generate a `composer.json` file for your new package. Once you have supplied those values, you are ready to build a workbench package!

#### Issuing The Workbench Artisan Command

	php artisan workbench vendor/package --resources

The vendor name is a way to distinguish your package from other packages of the same name from different authors. For example, if I (Taylor Otwell) were to create a new package named "Zapper", the vendor name could be `Taylor` while the package name would be `Zapper`. By default, the workbench will create framework agnostic packages; however, the `resources` command tells the workbench to generate the package with Laravel specific directories such as `migrations`, `views`, `config`, etc.

Once the `workbench` command has been executed, your package will be available within the `workbench` directory of your Laravel installation. Next, you should register the `ServiceProvider` that was created for your package. You may register the provider by adding it to the `providers` array in the `app/config/app.php` file. This will instruct Laravel to load your package when your application starts. Service providers use a `[Package]ServiceProvider` naming convention. So, using the example above, you would add `Taylor\Zapper\ZapperServiceProvider` to the `providers` array.

Once the provider has been registered, you are ready to start developing your package! However, before diving in, you may wish to review the sections below to get more familiar with the package structure and development workflow.

> **Note:** If your service provider cannot be found, run the `php artisan dump-autoload` command from your application's root directory

<a name="package-structure"></a>
## Package Structure

When using the `workbench` command, your package will be setup with conventions that allow the package to integrate well with other parts of the Laravel framework:

#### Basic Package Directory Structure

	/src
		/Vendor
			/Package
				PackageServiceProvider.php
		/config
		/lang
		/migrations
		/views
	/tests
	/public

Let's explore this structure further. The `src/Vendor/Package` directory is the home of all of your package's classes, including the `ServiceProvider`. The `config`, `lang`, `migrations`, and `views` directories, as you might guess, contain the corresponding resources for your package. Packages may have any of these resources, just like "regular" applications.

<a name="service-providers"></a>
## Service Providers

Service providers are simply bootstrap classes for packages. By default, they contain two methods: `boot` and `register`. Within these methods you may do anything you like: include a routes file, register bindings in the IoC container, attach to events, or anything else you wish to do.

The `register` method is called immediately when the service provider is registered, while the `boot` command is only called right before a request is routed. So, if actions in your service provider rely on another service provider already being registered, or you are overriding services bound by another provider, you should use the `boot` method.

When creating a package using the `workbench`, the `boot` command will already contain one action:

	$this->package('vendor/package');

This method allows Laravel to know how to properly load the views, configuration, and other resources for your application. In general, there should be no need for you to change this line of code, as it will setup the package using the workbench conventions.

By default, after registering a package, its resources will be available using the "package" half of `vendor/package`. However, you may pass a second argument into the `package` method to override this behavior. For example:

	// Passing custom namespace to package method
	$this->package('vendor/package', 'custom-namespace');

	// Package resources now accessed via custom-namespace
	$view = View::make('custom-namespace::foo');

There is not a "default location" for service provider classes. You may put them anywhere you like, perhaps organizing them in a `Providers` namespace within your `app` directory. The file may be placed anywhere, as long as Composer's [auto-loading facilities](http://getcomposer.org/doc/01-basic-usage.md#autoloading) know how to load the class.

If you have changed the location of your package's resources, such as configuration files or views, you should pass a third argument to the `package` method which specifies the location of your resources:

	$this->package('vendor/package', null, '/path/to/resources');

<a name="deferred-providers"></a>
## Deferred Providers

If you are writing a service provider that does not register any resources such as configuration or views, you may choose to make your provider "deferred". A deferred service provider is only loaded and registered when one of the services it provides is actually needed by the application IoC container. If none of the provider's services are needed for a given request cycle, the provider is never loaded.

To defer the execution of your service provider, set the `defer` property on the provider to `true`:

	protected $defer = true;

Next you should override the `provides` method from the base `Illuminate\Support\ServiceProvider` class and return an array of all of the bindings that your provider adds to the IoC container. For example, if your provider registers `package.service` and `package.another-service` in the IoC container, your `provides` method should look like this:

	public function provides()
	{
		return array('package.service', 'package.another-service');
	}

<a name="package-conventions"></a>
## Package Conventions

When utilizing resources from a package, such as configuration items or views, a double-colon syntax will generally be used:

#### Loading A View From A Package

	return View::make('package::view.name');

#### Retrieving A Package Configuration Item

	return Config::get('package::group.option');

> **Note:** If your package contains migrations, consider prefixing the migration name with your package name to avoid potential class name conflicts with other packages.

<a name="development-workflow"></a>
## Development Workflow

When developing a package, it is useful to be able to develop within the context of an application, allowing you to easily view and experiment with your templates, etc. So, to get started, install a fresh copy of the Laravel framework, then use the `workbench` command to create your package structure.

After the `workbench` command has created your package. You may `git init` from the `workbench/[vendor]/[package]` directory and `git push` your package straight from the workbench! This will allow you to conveniently develop the package in an application context without being bogged down by constant `composer update` commands.

Since your packages are in the `workbench` directory, you may be wondering how Composer knows to autoload your package's files. When the `workbench` directory exists, Laravel will intelligently scan it for packages, loading their Composer autoload files when the application starts!

If you need to regenerate your package's autoload files, you may use the `php artisan dump-autoload` command. This command will regenerate the autoload files for your root project, as well as any workbenches you have created.

#### Running The Artisan Autoload Command

	php artisan dump-autoload

<a name="package-routing"></a>
## Package Routing

In prior versions of Laravel, a `handles` clause was used to specify which URIs a package could respond to. However, in Laravel 4, a package may respond to any URI. To load a routes file for your package, simply `include` it from within your service provider's `boot` method.

#### Including A Routes File From A Service Provider

	public function boot()
	{
		$this->package('vendor/package');

		include __DIR__.'/../../routes.php';
	}

> **Note:** If your package is using controllers, you will need to make sure they are properly configured in your `composer.json` file's auto-load section.

<a name="package-configuration"></a>
## Package Configuration

#### Accessing Package Configuration Files

Some packages may require configuration files. These files should be defined in the same way as typical application configuration files. And, when using the default `$this->package` method of registering resources in your service provider, may be accessed using the usual "double-colon" syntax:

	Config::get('package::file.option');

#### Accessing Single File Package Configuration

However, if your package contains a single configuration file, you may simply name the file `config.php`. When this is done, you may access the options directly, without specifying the file name:

	Config::get('package::option');

#### Registering A Resource Namespace Manually

Sometimes, you may wish to register package resources such as views outside of the typical `$this->package` method. Typically, this would only be done if the resources were not in a conventional location. To register the resources manually, you may use the `addNamespace` method of the `View`, `Lang`, and `Config` classes:

	View::addNamespace('package', __DIR__.'/path/to/views');

Once the namespace has been registered, you may use the namespace name and the "double colon" syntax to access the resources:

	return View::make('package::view.name');

The method signature for `addNamespace` is identical on the `View`, `Lang`, and `Config` classes.

### Cascading Configuration Files

When other developers install your package, they may wish to override some of the configuration options. However, if they change the values in your package source code, they will be overwritten the next time Composer updates the package. Instead, the `config:publish` artisan command should be used:

	php artisan config:publish vendor/package

When this command is executed, the configuration files for your application will be copied to `app/config/packages/vendor/package` where they can be safely modified by the developer!

> **Note:** The developer may also create environment specific configuration files for your package by placing them in `app/config/packages/vendor/package/environment`.

<a name="package-views"></a>
## Package Views

If you are using a package in your application, you may occasionally wish to customize the package's views. You can easily export the package views to your own `app/views` directory using the `view:publish` Artisan command:

	php artisan view:publish vendor/package

This command will move the package's views into the `app/views/packages` directory. If this directory doesn't already exist, it will be created when you run the command. Once the views have been published, you may tweak them to your liking! The exported views will automatically take precedence over the package's own view files.

<a name="package-migrations"></a>
## Package Migrations

#### Creating Migrations For Workbench Packages

You may easily create and run migrations for any of your packages. To create a migration for a package in the workbench, use the `--bench` option:

	php artisan migrate:make create_users_table --bench="vendor/package"

#### Running Migrations For Workbench Packages

	php artisan migrate --bench="vendor/package"

#### Running Migrations For An Installed Package

To run migrations for a finished package that was installed via Composer into the `vendor` directory, you may use the `--package` directive:

	php artisan migrate --package="vendor/package"

<a name="package-assets"></a>
## Package Assets

#### Moving Package Assets To Public

Some packages may have assets such as JavaScript, CSS, and images. However, we are unable to link to assets in the `vendor` or `workbench` directories, so we need a way to move these assets into the `public` directory of our application. The `asset:publish` command will take care of this for you:

	php artisan asset:publish

	php artisan asset:publish vendor/package

If the package is still in the `workbench`, use the `--bench` directive:

	php artisan asset:publish --bench="vendor/package"

This command will move the assets into the `public/packages` directory according to the vendor and package name. So, a package named `userscape/kudos` would have its assets moved to `public/packages/userscape/kudos`. Using this asset publishing convention allows you to safely code asset paths in your package's views.

<a name="publishing-packages"></a>
## Publishing Packages

When your package is ready to publish, you should submit the package to the [Packagist](http://packagist.org) repository. If the package is specific to Laravel, consider adding a `laravel` tag to your package's `composer.json` file.

Also, it is courteous and helpful to tag your releases so that developers can depend on stable versions when requesting your package in their `composer.json` files. If a stable version is not ready, consider using the `branch-alias` Composer directive.

Once your package has been published, feel free to continue developing it within the application context created by `workbench`. This is a great way to continue to conveniently develop the package even after it has been published.

Some organizations choose to host their own private repository of packages for their own developers. If you are interested in doing this, review the documentation for the [Satis](http://github.com/composer/satis) project provided by the Composer team.
