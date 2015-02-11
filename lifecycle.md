# Request Lifecycle

- [Overview](#overview)
- [Request Lifecycle](#request-lifecycle)
- [Start Files](#start-files)
- [Application Events](#application-events)

<a name="overview"></a>
## Overview

When using any tool in the "real world", you feel more confident if you understand how that tool works. Application development is no different. When you understand how your development tools function, you feel more comfortable and confident using them. The goal of this document is to give you a good, high-level overview of how the Laravel framework "works". By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. In addition to a high-level overview of the request lifecycle, we'll cover "start" files and application events.

If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation.

<a name="request-lifecycle"></a>
## Request Lifecycle

All requests into your application are directed through the `public/index.php` script. When using Apache, the `.htaccess` file that ships with Laravel handles the passing of all requests to `index.php`. From here, Laravel begins the process of handling the requests and returning a response to the client. Getting a general idea for the Laravel bootstrap process will be useful, so we'll cover that now!

By far, the most important concept to grasp when learning about Laravel's bootstrap process is **Service Providers**. You can find a list of service providers by opening your `app/config/app.php` configuration file and finding the `providers` array. These providers serve as the primary bootstrapping mechanism for Laravel. But, before we dig into service providers, let's go back to `index.php`. After a request enters your `index.php` file, the `bootstrap/start.php` file will be loaded. This file creates the new Laravel `Application` object, which also serves as an [IoC container](/docs/4.2/ioc).

After creating the `Application` object, a few project paths will be set and [environment detection](/docs/4.2/configuration#environment-configuration) will be performed. Then, an internal Laravel bootstrap script will be called. This file lives deep within the Laravel source, and sets a few more settings based on your configuration files, such as timezone, error reporting, etc. But, in addition to setting these rather trivial configuration options, it also does something very important: registers all of the service providers configured for your application.

Simple service providers only have one method: `register`. This `register` method is called when the service provider is registered with the application object via the application's own `register` method. Within this method, service providers register things with the [IoC container](/docs/4.2/ioc). Essentially, each service provider binds one or more [closures](http://us3.php.net/manual/en/functions.anonymous.php) into the container, which allows you to access those bound services within your application. So, for example, the `QueueServiceProvider` registers closures that resolve the various [Queue](/docs/4.2/queues) related classes. Of course, service providers may be used for any bootstrapping task, not just registering things with the IoC container. A service provider may register event listeners, view composers, Artisan commands, and more.

After all of the service providers have been registered, your `app/start` files will be loaded. Lastly, your `app/routes.php` file will be loaded. Once your `routes.php` file has been loaded, the Request object is sent to the application so that it may be dispatched to a route.

So, let's summarize:

1. Request enters `public/index.php` file.
2. `bootstrap/start.php` file creates Application and detects environment.
3. Internal `framework/start.php` file configures settings and loads service providers.
4. Application `app/start` files are loaded.
5. Application `app/routes.php` file is loaded.
6. Request object sent to Application, which returns Response object.
7. Response object sent back to client.

Now that you have a good idea of how a request to a Laravel application is handled, let's take a closer look at "start" files!

<a name="start-files"></a>
## Start Files

Your application's start files are stored at `app/start`. By default, three are included with your application: `global.php`, `local.php`, and `artisan.php`. For more information about `artisan.php`, refer to the documentation on the [Artisan command line](/docs/4.2/commands#registering-commands).

The `global.php` start file contains a few basic items by default, such as the registration of the [Logger](/docs/4.2/errors) and the inclusion of your `app/filters.php` file. However, you are free to add anything to this file that you wish. It will be automatically included on _every_ request to your application, regardless of environment. The `local.php` file, on the other hand, is only called when the application is executing in the `local` environment. For more information on environments, check out the [configuration](/docs/4.2/configuration) documentation.

Of course, if you have other environments in addition to `local`, you may create start files for those environments as well. They will be automatically included when your application is running in that environment. So, for example, if you have a `development` environment configured in your `bootstrap/start.php` file, you may create a `app/start/development.php` file, which will be included when any requests enter the application in that environment.

### What To Place In Start Files

Start files serve as a simple place to place any "bootstrapping" code. For example, you could register a View composer, configure your logging preferences, set some PHP settings, etc. It's totally up to you. Of course, throwing all of your bootstrapping code into your start files can get messy. For large applications, or if you feel your start files are getting messy, consider moving some bootstrapping code into [service providers](/docs/4.2/ioc#service-providers).

<a name="application-events"></a>
## Application Events

#### Registering Application Events

You may also do pre and post request processing by registering `before`, `after`, `finish`, and `shutdown` application events:

	App::before(function($request)
	{
		//
	});

	App::after(function($request, $response)
	{
		//
	});

Listeners to these events will be run `before` and `after` each request to your application. These events can be helpful for global filtering or global modification of responses. You may register them in one of your `start` files or in a [service provider](/docs/4.2/ioc#service-providers).

You may also register a listener on the `matched` event, which is fired when an incoming request has been matched to a route but that route has not yet been executed:

	Route::matched(function($route, $request)
	{
		//
	});

The `finish` event is called after the response from your application has been sent back to the client. This is a good place to do any last minute processing your application requires. The `shutdown` event is called immediately after all of the `finish` event handlers finish processing, and is the last opportunity to do any work before the script terminates. Most likely, you will not have a need to use either of these events.
