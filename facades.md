# Facades

- [Introduction](#introduction)
- [Example](#example)
- [Creating Facades](#creating-facades)
- [Mocking Facades](#mocking-facades)

<a name="introduction"></a>
## Introduction

Facades are special classes that are designed to simplify your code.

Laravel comes with many facades, and you've probably been using them without knowing. While it's not necessary to understand how they work, you may find that you'd like to create your own for use within your applications and packages.

<a name="example"></a>
## Example

Here is a simple example of requesting data from Laravel's cache system. The data identified by the key "key" will be returned and stored in the variable $value. In this example, it appears that the static method get() is being called on the Cache class.

	$value = Cache::get('key');

Let's take a look at the Cache class.

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

As you can see, there is no static method get(). What's really happening?

The Cache class extends Laravel's Facade class and defines a method called getFacadeAccessor(). This method's job is to return the name of an IoC binding.

When a user references any static method on the Cache class, Laravel resolves that IoC binding from the [IoC container](/docs/ioc) and runs the requested method against that object.

Here's what our example is really doing:

	$value = $app->make('cache')->get('key');

It only appears that the static method get() exists in the Cache class. In reality, the Facade is resolving an instance from the IoC container and calling the get() method on that instance.

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
