# IoC Container

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
- [Where To Register Bindings](#where-to-register)
- [Automatic Resolution](#automatic-resolution)
- [Practical Usage](#practical-usage)
- [Service Providers](#service-providers)
- [Container Events](#container-events)

<a name="introduction"></a>
## Introduction

The Laravel inversion of control container is a powerful tool for managing class dependencies. Dependency injection is a method of removing hard-coded class dependencies. Instead, the dependencies are injected at run-time, allowing for greater flexibility as dependency implementations may be swapped easily.

Understanding the Laravel IoC container is essential to building a powerful, large application, as well as for contributing to the Laravel core itself.

<a name="basic-usage"></a>
## Basic Usage

#### Binding A Type Into The Container

There are two ways the IoC container can resolve dependencies: via Closure callbacks or automatic resolution. First, we'll explore Closure callbacks. First, a "type" may be bound into the container:

	App::bind('foo', function($app)
	{
		return new FooBar;
	});

#### Resolving A Type From The Container

	$value = App::make('foo');

When the `App::make` method is called, the Closure callback is executed and the result is returned.

#### Binding A "Shared" Type Into The Container

Sometimes, you may wish to bind something into the container that should only be resolved once, and the same instance should be returned on subsequent calls into the container:

	App::singleton('foo', function()
	{
		return new FooBar;
	});

#### Binding An Existing Instance Into The Container

You may also bind an existing object instance into the container using the `instance` method:

	$foo = new Foo;

	App::instance('foo', $foo);

<a name="where-to-register"></a>
## Where To Register Bindings

IoC bindings, like event handlers or route filters, generally fall under the title of "bootstrap code". In other words, they prepare your application to actually handle requests, and usually need to be executed before a route or controller is actually called. Like most other bootstrap code, the `start` files are always an option for registering IoC bindings. Alternatively, you could create an `app/ioc.php` (filename does not matter) file and require that file from your `start` file.

If your application has a very large number of IoC bindings, or you simply wish to organize your IoC bindings in separate files by category, you may register your bindings in a [service provider](#service-providers).

<a name="automatic-resolution"></a>
## Automatic Resolution

#### Resolving A Class

The IoC container is powerful enough to resolve classes without any configuration at all in many scenarios. For example:

	class FooBar {

		public function __construct(Baz $baz)
		{
			$this->baz = $baz;
		}

	}

	$fooBar = App::make('FooBar');

Note that even though we did not register the FooBar class in the container, the container will still be able to resolve the class, even injecting the `Baz` dependency automatically!

When a type is not bound in the container, it will use PHP's Reflection facilities to inspect the class and read the constructor's type-hints. Using this information, the container can automatically build an instance of the class.

#### Binding An Interface To An Implementation

However, in some cases, a class may depend on an interface implementation, not a "concrete type". When this is the case, the `App::bind` method must be used to inform the container which interface implementation to inject:

	App::bind('UserRepositoryInterface', 'DbUserRepository');

Now consider the following controller:

	class UserController extends BaseController {

		public function __construct(UserRepositoryInterface $users)
		{
			$this->users = $users;
		}

	}

Since we have bound the `UserRepositoryInterface` to a concrete type, the `DbUserRepository` will automatically be injected into this controller when it is created.

<a name="practical-usage"></a>
## Practical Usage

Laravel provides several opportunities to use the IoC container to increase the flexibility and testability of your application. One primary example is when resolving controllers. All controllers are resolved through the IoC container, meaning you can type-hint dependencies in a controller constructor, and they will automatically be injected.

#### Type-Hinting Controller Dependencies

	class OrderController extends BaseController {

		public function __construct(OrderRepository $orders)
		{
			$this->orders = $orders;
		}

		public function getIndex()
		{
			$all = $this->orders->all();

			return View::make('orders', compact('all'));
		}

	}

In this example, the `OrderRepository` class will automatically be injected into the controller. This means that when [unit testing](/docs/4.2/testing) a "mock" `OrderRepository` may be bound into the container and injected into the controller, allowing for painless stubbing of database layer interaction.

#### Other Examples Of IoC Usage

[Filters](/docs/4.2/routing#route-filters), [composers](/docs/4.2/responses#view-composers), and [event handlers](/docs/4.2/events#using-classes-as-listeners) may also be resolved out of the IoC container. When registering them, simply give the name of the class that should be used:

	Route::filter('foo', 'FooFilter');

	View::composer('foo', 'FooComposer');

	Event::listen('foo', 'FooHandler');

<a name="service-providers"></a>
## Service Providers

Service providers are a great way to group related IoC registrations in a single location. Think of them as a way to bootstrap components in your application. Within a service provider, you might register a custom authentication driver, register your application's repository classes with the IoC container, or even setup a custom Artisan command.

In fact, most of the core Laravel components include service providers. All of the registered service providers for your application are listed in the `providers` array of the `app/config/app.php` configuration file.

#### Defining A Service Provider

To create a service provider, simply extend the `Illuminate\Support\ServiceProvider` class and define a `register` method:

	use Illuminate\Support\ServiceProvider;

	class FooServiceProvider extends ServiceProvider {

		public function register()
		{
			$this->app->bind('foo', function()
			{
				return new Foo;
			});
		}

	}

Note that in the `register` method, the application IoC container is available to you via the `$this->app` property. Once you have created a provider and are ready to register it with your application, simply add it to the `providers` array in your `app` configuration file.

#### Registering A Service Provider At Run-Time

You may also register a service provider at run-time using the `App::register` method:

	App::register('FooServiceProvider');

<a name="container-events"></a>
## Container Events

#### Registering A Resolving Listener

The container fires an event each time it resolves an object. You may listen to this event using the `resolving` method:

	App::resolvingAny(function($object)
	{
		//
	});

	App::resolving('foo', function($foo)
	{
		//
	});

Note that the object that was resolved will be passed to the callback.
