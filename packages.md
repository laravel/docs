# Package Development

- [Introduction](#introduction)
- [Service Providers](#service-providers)
- [Routing](#routing)
- [Resources](#resources)
    - [Views](#views)
    - [Translations](#translations)
    - [Configuration](#configuration)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)

<a name="introduction"></a>
## Introduction

Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon), or an entire BDD testing framework like [Behat](https://github.com/Behat/Behat).

Of course, there are different types of packages. Some packages are stand-alone, meaning they work with any framework, not just Laravel. Both Carbon and Behat are examples of stand-alone packages. Any of these packages may be used with Laravel by simply requesting them in your `composer.json` file.

On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those packages that are Laravel specific.

<a name="service-providers"></a>
## Service Providers

[Service providers](/docs/{{version}}/providers) are the connection points between your package and Laravel. A service provider is responsible for binding things into Laravel's [service container](/docs/{{version}}/container) and informing Laravel where to load package resources such as views, configuration, and localization files.

A service provider extends the `Illuminate\Support\ServiceProvider` class and contains two methods: `register` and `boot`. The base `ServiceProvider` class is located in the `illuminate/support` Composer package, which you should add to your own package's dependencies.

To learn more about the structure and purpose of service providers, check out [their documentation](/docs/{{version}}/providers).

<a name="routing"></a>
## Routing

To define routes for your package, simply `require` the routes file from within your package service provider's `boot` method. From within your routes file, you may use the `Route` facade to [register routes](/docs/{{version}}/routing) just as you would within a typical Laravel application:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        if (! $this->app->routesAreCached()) {
            require __DIR__.'/../../routes.php';
        }
    }

<a name="resources"></a>
## Resources

<a name="views"></a>
### Views

To register your package's [views](/docs/{{version}}/views) with Laravel, you need to tell Laravel where the views are located. You may do this using the service provider's `loadViewsFrom` method. The `loadViewsFrom` method accepts two arguments: the path to your view templates and your package's name. For example, if your package name is "courier", add the following to your service provider's `boot` method:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
    }

Package views are referenced using a double-colon `package::view` syntax. So, you may load the `admin` view from the `courier` package like so:

    Route::get('admin', function () {
        return view('courier::admin');
    });

#### Overriding Package Views

When you use the `loadViewsFrom` method, Laravel actually registers **two** locations for your views: one in the application's `resources/views/vendor` directory and one in the directory you specify. So, using our `courier` example: when requesting a package view, Laravel will first check if a custom version of the view has been provided by the developer in `resources/views/vendor/courier`. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for end-users to customize / override your package's views.

#### Publishing Views

If you would like to make your views available for publishing to the application's `resources/views/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package view paths and their corresponding publish locations.

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

        $this->publishes([
            __DIR__.'/path/to/views' => resource_path('views/vendor/courier'),
        ]);
    }

Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's views will be copied to the specified location.

<a name="translations"></a>
### Translations

If your package contains [translation files](/docs/{{version}}/localization), you may use the `loadTranslationsFrom` method to inform Laravel how to load them. For example, if your package is named "courier", you should add the following to your service provider's `boot` method:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
    }

Package translations are referenced using a double-colon `package::file.line` syntax. So, you may load the `courier` package's `welcome` line from the `messages` file like so:

    echo trans('courier::messages.welcome');

#### Publishing Translations

If you would like to publish your package's translations to the application's `resources/lang/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package paths and their corresponding publish locations. For example, to publish the translation files for our example `courier` package:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');

        $this->publishes([
            __DIR__.'/path/to/translations' => resource_path('lang/vendor/courier'),
        ]);
    }

Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's translations will be published to the specified location.

<a name="configuration"></a>
### Configuration

Typically, you will want to publish your package's configuration file to the application's own `config` directory. This will allow users of your package to easily override your default configuration options. To publish a configuration file, just use the `publishes` method from the `boot` method of your service provider:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
        ]);
    }

Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified location. Of course, once your configuration has been published, it can be accessed like any other configuration file:

    $value = config('courier.option');

#### Default Package Configuration

You may also choose to merge your own package configuration file with the application's copy. This allows your users to include only the options they actually want to override in the published copy of the configuration. To merge the configurations, use the `mergeConfigFrom` method within your service provider's `register` method:

    /**
     * Register bindings in the container.
     *
     * @return void
     */
    public function register()
    {
        $this->mergeConfigFrom(
            __DIR__.'/path/to/config/courier.php', 'courier'
        );
    }

<a name="public-assets"></a>
## Public Assets

Your packages may have assets such as JavaScript, CSS, and images. To publish these assets to the application's `public` directory, use the service provider's `publishes` method. In this example, we will also add a `public` asset group tag, which may be used to publish groups of related assets:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/path/to/assets' => public_path('vendor/courier'),
        ], 'public');
    }

Now, when your package's users execute the `vendor:publish` command, your assets will be copied to the specified location. Since you typically will need to overwrite the assets every time the package is updated, you may use the `--force` flag:

    php artisan vendor:publish --tag=public --force

If you would like to make sure your public assets are always up-to-date, you can add this command to the `post-update-cmd` list in your `composer.json` file.

<a name="publishing-file-groups"></a>
## Publishing File Groups

You may want to publish groups of package assets and resources separately. For instance, you might want your users to be able to publish your package's configuration files without being forced to publish your package's assets at the same time. You may do this by "tagging" them when calling the `publishes` method. For example, let's define two publish groups in the `boot` method of a package service provider:

    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../config/package.php' => config_path('package.php')
        ], 'config');

        $this->publishes([
            __DIR__.'/../database/migrations/' => database_path('migrations')
        ], 'migrations');
    }

Now your users may publish these groups separately by referencing their tag name when using the `vendor:publish` Artisan command:

    php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"
