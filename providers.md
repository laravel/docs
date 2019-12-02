# Service Providers

- [Introduction](#introduction)
- [Writing Service Providers](#writing-service-providers)
    - [The Register Method](#the-register-method)
    - [The Boot Method](#the-boot-method)
- [Registering Providers](#registering-providers)
- [Deferred Providers](#deferred-providers)

<a name="introduction"></a>
## Introduction

Service providers are the central place of all Laravel application bootstrapping. Your own application, as well as all of Laravel's core services are bootstrapped via service providers.

But, what do we mean by "bootstrapped"? In general, we mean **registering** things, including registering service container bindings, event listeners, middleware, and even routes. Service providers are the central place to configure your application.

If you open the `config/app.php` file included with Laravel, you will see a `providers` array. These are all of the service provider classes that will be loaded for your application. Note that many of these are "deferred" providers, meaning they will not be loaded on every request, but only when the services they provide are actually needed.

In this overview you will learn how to write your own service providers and register them with your Laravel application.

<a name="writing-service-providers"></a>
## Writing Service Providers

All service providers extend the `Illuminate\Support\ServiceProvider` class. Most service providers contain a `register` and a `boot` method. Within the `register` method, you should **only bind things into the [service container](/docs/{{version}}/container)**. You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method.

The Artisan CLI can generate a new provider via the `make:provider` command:

    php artisan make:provider RiakServiceProvider

<a name="the-register-method"></a>
### The Register Method

As mentioned previously, within the `register` method, you should only bind things into the [service container](/docs/{{version}}/container). You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet.

Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `$app` property which provides access to the service container:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Riak\Connection;

    class RiakServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            $this->app->singleton(Connection::class, function ($app) {
                return new Connection(config('riak'));
            });
        }
    }

This service provider only defines a `register` method, and uses that method to define an implementation of `Riak\Connection` in the service container. If you don't understand how the service container works, check out [its documentation](/docs/{{version}}/container).

#### The `bindings` And `singletons` Properties

If your service provider registers many simple bindings, you may wish to use the `bindings` and `singletons` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings:

    <?php

    namespace App\Providers;

    use App\Contracts\DowntimeNotifier;
    use App\Contracts\ServerProvider;
    use App\Services\DigitalOceanServerProvider;
    use App\Services\PingdomDowntimeNotifier;
    use App\Services\ServerToolsProvider;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * All of the container bindings that should be registered.
         *
         * @var array
         */
        public $bindings = [
            ServerProvider::class => DigitalOceanServerProvider::class,
        ];

        /**
         * All of the container singletons that should be registered.
         *
         * @var array
         */
        public $singletons = [
            DowntimeNotifier::class => PingdomDowntimeNotifier::class,
            ServerToolsProvider::class => ServerToolsProvider::class,
        ];
    }

<a name="the-boot-method"></a>
### The Boot Method

So, what if we need to register a [view composer](/docs/{{version}}/views#view-composers) within our service provider? This should be done within the `boot` method. **This method is called after all other service providers have been registered**, meaning you have access to all other services that have been registered by the framework:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;

    class ComposerServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            view()->composer('view', function () {
                //
            });
        }
    }

#### Boot Method Dependency Injection

You may type-hint dependencies for your service provider's `boot` method. The [service container](/docs/{{version}}/container) will automatically inject any dependencies you need:

    use Illuminate\Contracts\Routing\ResponseFactory;

    public function boot(ResponseFactory $response)
    {
        $response->macro('caps', function ($value) {
            //
        });
    }

<a name="registering-providers"></a>
## Registering Providers

All service providers are registered in the `config/app.php` configuration file. This file contains a `providers` array where you can list the class names of your service providers. By default, a set of Laravel core service providers are listed in this array. These providers bootstrap the core Laravel components, such as the mailer, queue, cache, and others.

To register your provider, add it to the array:

    'providers' => [
        // Other Service Providers

        App\Providers\ComposerServiceProvider::class,
    ],

<a name="deferred-providers"></a>
## Deferred Providers

If your provider is **only** registering bindings in the [service container](/docs/{{version}}/container), you may choose to defer its registration until one of the registered bindings is actually needed. Deferring the loading of such a provider will improve the performance of your application, since it is not loaded from the filesystem on every request.

Laravel compiles and stores a list of all of the services supplied by deferred service providers, along with the name of its service provider class. Then, only when you attempt to resolve one of these services does Laravel load the service provider.

To defer the loading of a provider, implement the `\Illuminate\Contracts\Support\DeferrableProvider` interface and define a `provides` method. The `provides` method should return the service container bindings registered by the provider:

    <?php

    namespace App\Providers;

    use Illuminate\Contracts\Support\DeferrableProvider;
    use Illuminate\Support\ServiceProvider;
    use Riak\Connection;

    class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            $this->app->singleton(Connection::class, function ($app) {
                return new Connection($app['config']['riak']);
            });
        }

        /**
         * Get the services provided by the provider.
         *
         * @return array
         */
        public function provides()
        {
            return [Connection::class];
        }
    }
