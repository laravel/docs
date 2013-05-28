# Facades

- [Introduction](#introduction)
- [Explanation](#explanation)
- [Practical Usage](#practical-usage)
- [Creating Facades](#creating-facades)
- [Mocking Facades](#mocking-facades)

<a name="introduction"></a>
## Introduction

Facades are special classes that are designed to simplify your code. Laravel comes with many Facades, and you have probably been using them without even knowing. When developing your application or package, you may wish to use Facades to shorten up some syntax. Here, we will cover the concept, development, and usage of Facade classes.

> **Note:** Before digging into Facades, it is strongly recommended you are very familiar with the Laravel [IoC container](/docs/ioc).

<a name="explanation"></a>
## Explanation

Facades typicall only contain two methods, a `getFacadeAccessor` method and a `__callStatic` method. The `getFacadeAccessor` method simply returns a string key that can be used to resolve a class out of the [IoC container](/docs/ioc). This class resolved using this key will be called via the `__callStatic` method when methods are called on the Facade.

So, Facades are nothing more than a way to provide shorter syntax to calling classes that available in the application container.

<a name="practical-usage"></a>
## Practical Usage

In the examle below, a call is made to the Laravel cache system. In this case, it appears that the static method `get` is being called on the `Cache` class.

	$value = Cache::get('key');

However, if we look at that `Illuminate\Support\Facades\Cache` class, 

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

Note that the `Cache` Facade extends the base Facade class, and defines a method `getFacadeAccessor()`. Remember, this method's job is to return the name of an IoC binding.

When a user references any static method on the `Cache` Facade, Laravel resolves that IoC binding from the container and runs the requested method (in this case, `get`) against that object.

So, our `Cache::get` call could be re-written like so:

	$value = $app->make('cache')->get('key');

<a name="creating-facades"></a>
## Creating Facades

Creating a Facade for your own application or package is simple. You only need 3 things:

- An IoC Binding.
- A Facade Class.
- A Facade Alias Configuration.

Let's look at an example. Here, we have a class that can be referenced as `PaymentGateway\Payment`.

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			//
		}

	}

A Facade for this class would look like the following:

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

	    protected static function getFacadeAccessor() { return 'payment'; }

	}

Finally, we add our IoC binding, which tells Laravel which object to operate upon when using our Facade.

	App::bind('payment', function()
	{
		return new \PaymentGateway\Payment;
	});

A great place to register this binding would be to create a new [service provider](/docs/ioc#service-providers) named `PaymentServiceProvider`, and add this binding to the `register` method. You can then configure Laravel to load your service provider from the `app/config/app.php` configuration file.

Next, if we wish, we can add an alias for our Facade to the `aliases` array in the `app/config/app.php` configuration file. Now, we can call the `process` method on an instance of the `Payment` class with:

	Payment::process();

<a name="mocking-facades"></a>
## Mocking Facades

Unit testing is an important aspect of why facades work the way that they do. In fact, testability is the primary reason for Facades to even exist. For more information, check out the [mocking facades](/docs/testing#mocking-facades) section of the documentation.
