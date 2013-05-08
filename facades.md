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

The Cache class extends Laravel's Facade class and defines a method called getFacadeAccessor(). This method's job is to return the name of an IoC binding.

When a user references any static method on the Cache class, Laravel resolves that IoC binding from the [IoC container](/docs/ioc) and runs the requested method against that object.

Here's what our example is really doing:

	$value = $app->make('cache')->get('key');

It only appears that the static method get() exists in the Cache class. In reality, the Facade is resolving an instance from the IoC container and calling the get() method on that instance.

<a name="creating-facades"></a>
## Creating Facades

Creating a facade for your own application or package is simple. You only need 3 things.

- an IoC binding
- a facade class
- updated configurations

Let's look at an example. Here we have a class that can be referenced as \PaymentGateway\Payment.

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			// process payment here
		}

	}

Here we have the facade class.

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

	    protected static function getFacadeAccessor(){ return 'payment'; }

	}

Remember, you must provide a static method getFacadeAccessor(). Its job is to return a string with the name of the IoC binding that the facade will utilize.

Next, we add our IoC binding which tells Laravel which object to operate upon when using our facade.

	$this->app->bind('payment', function() {

		return new \PaymentGateway\Payment;

	});

A great place to register this binding would be to create a new [Service Provider](/docs/ioc#service-providers) named PaymentServiceProvider. The binding would be added to to the register() method. You can configure Laravel to load your service provider from the config/app.php configuration file.

Finally, we edit config/app.php and make sure that our facade class is listed under 'aliases' with the rest of the facade classes. Now, we can call the process() method on an instance of the payment class with:

	Payment::process();

<a name="mocking-facades"></a>
## Mocking Facades

Unit-testing testing is an important aspect of why facades work the way that they do. Check the [Mocking Facades](/docs/testing#mocking-facades) section of the documentation for more information.
