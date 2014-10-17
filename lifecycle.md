# Request Lifecycle

- [Introduction](#introduction)
- [Lifecycle Overview](#lifecycle-overview)
- [Focus On Service Providers](#focus-on-service-providers)

<a name="introduction"></a>
## Introduction

When using any tool in the "real world", you feel more confident if you understand how that tool works. Application development is no different. When you understand how your development tools function, you feel more comfortable and confident using them.

The goal of this document is to give you a good, high-level overview of how the Laravel framework "works". By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications.

If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation.

<a name="lifecycle-overview"></a>
## Lifecycle Overview

#### First Things

The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is simply a starting point for loading the rest of the framework.

The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/start.php`. The first action taken by Laravel itself is to create an instance of the application / service container.

#### Environment Detection

Next, Laravel detects the application environment by loading the `bootstrap/environment.php` file. The environment determines which versions of configuration files will be loaded for the given request.

#### Error Handling

After the Application is created and the environment has been detected, the exception / error handling services are started. This is done by the `Illuminate\Foundation\start.php` script which is included in the `laravel/framework` Composer package.

#### Service Providers

Next, we are ready to load all of the configured [service providers](/docs/master/providers). All of the service providers for the application are configured in the `config/app.php` configuration file's `providers` array. First, the `register` method will be called on all providers. The `boot` method will not be called until an HTTP request or console command has actually been dispatched to the application.

#### Dispatch Request

Finally, we are ready to dispatch the HTTP request to the application. The Laravel application's `handle` method will be called with a `Symfony\Component\HttpFoundation\Request` instance. At this point, the `boot` method is called on all of the registered service providers. Once the service providers are booted, the request is handed to the router and dispatched to a route / controller.

<a name="focus-on-service-providers"></a>
## Focus On Service Providers

Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple!

Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Of course, your application's default service providers are stored in the `app/Providers` directory. By default, several are shipped with your application, and handle things like bootstrapping error handling, logging, etc.

By default, the `AppServiceProvider` is blank. This provider is a great place to add your application's own bootstrapping and service container bindings. Of course, for large applications, you may wish to create several service providers, each with a more granular type of bootstrapping. For example, you might create an `EventsServiceProvider` that only registers event listeners.
