# Facades

- [Introduction](#introduction)
- [Examples](#examples)
- [Creating Facades](#creating-facades)
- [Mocking a Facade](#mocking-a-facade)

<a name="introduction"></a>
## Introduction

Laravel makes use of a design pattern called [the facade pattern](http://en.wikipedia.org/wiki/Facade_pattern). In short, a facade is a tool that is designed to simplify complex implementation.

Many facades are provided by Laravel. While it's not necessary to understand how they work, you may find that you'd like to create your own for use within your applications and packages.

<a name="examples"></a>
## Examples

Here is a simple example of requesting data from Laravel's cache system. The data identified by the key "key" will be returned and stored in the variable $value.

	$value = Cache::get('key');

In this example, it appears that the static method get() is being called on the Cache class.

Let's take a look at the Cache class.

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

As you can see there is no static method get(). What's really happening?

The Cache class extends the Facade class and defines a method called getFacadeAccessor(). This method's job is to return the name of an IoC binding.

When a user references any static method on the Cache class, Laravel resolves that IoC binding from the [IoC container](/docs/ioc) and runs the requested method against that object.

Here's what's really happening.

	$value = $app->make('cache')->get('key');

It only appears that the static method get() exists in the Cache class. In reality, the Facade is resolving an instance from the IoC container and calling the get() method on that instance.

**A More Complex Example**

	Route::get('/', function()
	{
		return 'Hello World';
	});

In this example you can see that the Route class' get() method is being called statically. Let's take a look at the Route class.

	class Route extends Facade {

		/**
		 * Register a new filter with the application.
		 *
		 * @param  string   $name
		 * @param  Closure|string  $callback
		 * @return void
		 */
		public static function filter($name, $callback)
		{
			return static::$app['router']->addFilter($name, $callback);
		}

		/**
		 * Tie a registered middleware to a URI pattern.
		 *
		 * @param  string  $pattern
		 * @param  string|array  $name
		 * @return void
		 */
		public static function when($pattern, $name)
		{
			return static::$app['router']->matchFilter($pattern, $name);
		}

		/**
		 * Determine if the current route matches a given name.
		 *
		 * @param  string  $name
		 * @return bool
		 */
		public static function is($name)
		{
			return static::$app['router']->currentRouteNamed($name);
		}

		/**
		 * Determine if the current route uses a given controller action.
		 *
		 * @param  string  $action
		 * @return bool
		 */
		public static function uses($action)
		{
			return static::$app['router']->currentRouteUses($action);
		}

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'router'; }

	}


As you can see, there is no static get() method. The getFacadeAcessor() method defines the IoC binding that should be used for this facade. In this example, the 'router' binding is resolved from the [IoC container](/docs/ioc) and the get() method is called on that object.

Here's another way of looking at the route registration without facades.

	$app->make('router')->get('/', function()
	{
		return 'Hello World';
	});

In this example, you'll also notice many additional methods have been added to the Route class. This is because the filter(), when(), is() and uses() methods all have different names on the router object.

Laravel is all about nice expressive names, so these methods have been added to prevent the need to use Route::currentRouteNamed($action) in favor of Route::is($action).

<a name="creating-facades"></a>
## Creating Facades

Creating a facade for your own application is simple.

- First, decide to which IoC binding you want the facade class to be tied.
- Then, create your facade class extending Laravel's Facade class.
- Finally, make sure that your facade class can be accessed anywhere. The easiest way to do this is by adding an alias to you config/app.php file with the rest of the facades.

Let's look at an example. In this example we have a class called \PaymentGateway\Payment.

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			// process payment here
		}

	}

We want to access the process() method with Payment::process(). So, let's create a facade class. Be sure to provide a static method getFacadeAccessor() which returns a string with the name of the IoC binding.

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

	    protected static function getFacadeAccessor(){ return 'payment'; }

	}

Finally, we can add our IoC binding.

	$this->app->bind('payment', function() {

		return new \PaymentGateway\Payment;

	});

A great place to register this IoC binding would be to create a new [Service Provider](/docs/ioc#service-providers) named PaymentServiceProvider and adding the binding to the register() method. Don't forget to reference the facade class and the service provider in your config/app.php!

<a name="mocking-facades"></a>
## Mocking Facades

Unit-testing testing is an important aspect of why facades work the way that they do. Check the [Mocking Facades](/docs/testing#mocking-facades) section of the documentation for more information.
