# Facades

- [Introduction](#introduction)
- [Explanation](#explanation)
- [Practical Usage](#practical-usage)
- [Creating Facades](#creating-facades)
- [Mocking Facades](#mocking-facades)
- [Facade Class Reference](#facade-class-reference)

<a name="introduction"></a>
## Introduction

Facades provide a "static" interface to classes that are available in the application's [IoC container](/docs/4.2/ioc). Laravel ships with many facades, and you have probably been using them without even knowing it! Laravel "facades" serve as "static proxies" to underlying classes in the IoC container, providing the benefit of a terse, expressive syntax while maintaining more testability and flexibility than traditional static methods.

Occasionally, You may wish to create your own facades for your applications and packages, so let's explore the concept, development and usage of these classes.

> **Note:** Before digging into facades, it is strongly recommended that you become very familiar with the Laravel [IoC container](/docs/4.2/ioc).

<a name="explanation"></a>
## Explanation

In the context of a Laravel application, a facade is a class that provides access to an object from the container. The machinery that makes this work is in the `Facade` class. Laravel's facades, and any custom facades you create, will extend the base `Facade` class.

Your facade class only needs to implement a single method: `getFacadeAccessor`. It's the `getFacadeAccessor` method's job to define what to resolve from the container. The `Facade` base class makes use of the `__callStatic()` magic-method to defer calls from your facade to the resolved object.

So, when you make a facade call like `Cache::get`, Laravel resolves the Cache manager class out of the IoC container and calls the `get` method on the class. In technical terms, Laravel Facades are a convenient syntax for using the Laravel IoC container as a service locator.

<a name="practical-usage"></a>
## Practical Usage

In the example below, a call is made to the Laravel cache system. By glancing at this code, one might assume that the static method `get` is being called on the `Cache` class.

	$value = Cache::get('key');

However, if we look at that `Illuminate\Support\Facades\Cache` class, you'll see that there is no static method `get`:

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

The Cache class extends the base `Facade` class and defines a method `getFacadeAccessor()`. Remember, this method's job is to return the name of an IoC binding.

When a user references any static method on the `Cache` facade, Laravel resolves the `cache` binding from the IoC container and runs the requested method (in this case, `get`) against that object.

So, our `Cache::get` call could be re-written like so:

	$value = $app->make('cache')->get('key');

<a name="creating-facades"></a>
## Creating Facades

Creating a facade for your own application or package is simple. You only need 3 things:

- An IoC binding.
- A facade class.
- A facade alias configuration.

Let's look at an example. Here, we have a class defined as `PaymentGateway\Payment`.

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			//
		}

	}

This class might live in your `app/models` directory, or any other directory that Composer knows how to auto-load.

We need to be able to resolve this class from the IoC container. So, let's add a binding:

	App::bind('payment', function()
	{
		return new \PaymentGateway\Payment;
	});

A great place to register this binding would be to create a new [service provider](/docs/4.2/ioc#service-providers) named `PaymentServiceProvider`, and add this binding to the `register` method. You can then configure Laravel to load your service provider from the `app/config/app.php` configuration file.

Next, we can create our own facade class:

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

		protected static function getFacadeAccessor() { return 'payment'; }

	}

Finally, if we wish, we can add an alias for our facade to the `aliases` array in the `app/config/app.php` configuration file. Now, we can call the `process` method on an instance of the `Payment` class.

	Payment::process();

### A Note On Auto-Loading Aliases

Classes in the `aliases` array are not available in some instances because [PHP will not attempt to autoload undefined type-hinted classes](https://bugs.php.net/bug.php?id=39003). If `\ServiceWrapper\ApiTimeoutException` is aliased to `ApiTimeoutException`, a `catch(ApiTimeoutException $e)` outside of the namespace `\ServiceWrapper` will never catch the exception, even if one is thrown. A similar problem is found in Models which have type hints to aliased classes. The only workaround is to forego aliasing and `use` the classes you wish to type hint at the top of each file which requires them.

<a name="mocking-facades"></a>
## Mocking Facades

Unit testing is an important aspect of why facades work the way that they do. In fact, testability is the primary reason for facades to even exist. For more information, check out the [mocking facades](/docs/4.2/testing#mocking-facades) section of the documentation.

<a name="facade-class-reference"></a>
## Facade Class Reference

Below you will find every facade and its underlying class. This is a useful tool for quickly digging into the API documentation for a given facade root. The [IoC binding](/docs/4.2/ioc) key is also included where applicable.

Facade  |  Class  |  IoC Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](http://laravel.com/api/4.2/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/4.2/Illuminate/Console/Application.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/4.2/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Auth\Guard](http://laravel.com/api/4.2/Illuminate/Auth/Guard.html)  |
Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/4.2/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/4.2/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](http://laravel.com/api/4.2/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/4.2/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/4.2/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/4.2/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](http://laravel.com/api/4.2/Illuminate/Database/Connection.html)  |
Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/4.2/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/4.2/Illuminate/Filesystem/Filesystem.html)  |  `files`
Form  |  [Illuminate\Html\FormBuilder](http://laravel.com/api/4.2/Illuminate/Html/FormBuilder.html)  |  `form`
Hash  |  [Illuminate\Hashing\HasherInterface](http://laravel.com/api/4.2/Illuminate/Hashing/HasherInterface.html)  |  `hash`
HTML  |  [Illuminate\Html\HtmlBuilder](http://laravel.com/api/4.2/Illuminate/Html/HtmlBuilder.html)  |  `html`
Input  |  [Illuminate\Http\Request](http://laravel.com/api/4.2/Illuminate/Http/Request.html)  |  `request`
Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/4.2/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](http://laravel.com/api/4.2/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/4.2/Illuminate/Mail/Mailer.html)  |  `mailer`
Paginator  |  [Illuminate\Pagination\Factory](http://laravel.com/api/4.2/Illuminate/Pagination/Factory.html)  |  `paginator`
Paginator (Instance)  |  [Illuminate\Pagination\Paginator](http://laravel.com/api/4.2/Illuminate/Pagination/Paginator.html)  |
Password  |  [Illuminate\Auth\Reminders\PasswordBroker](http://laravel.com/api/4.2/Illuminate/Auth/Reminders/PasswordBroker.html)  |  `auth.reminder`
Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/4.2/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/4.2/Illuminate/Queue/QueueInterface.html)  |
Queue (Base Class) |  [Illuminate\Queue\Queue](http://laravel.com/api/4.2/Illuminate/Queue/Queue.html)  |
Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/4.2/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/4.2/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](http://laravel.com/api/4.2/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Support\Facades\Response](http://laravel.com/api/4.2/Illuminate/Support/Facades/Response.html)  |
Route  |  [Illuminate\Routing\Router](http://laravel.com/api/4.2/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/4.2/Illuminate/Database/Schema/Blueprint.html)  |
Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/4.2/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](http://laravel.com/api/4.2/Illuminate/Session/Store.html)  |
SSH  |  [Illuminate\Remote\RemoteManager](http://laravel.com/api/4.2/Illuminate/Remote/RemoteManager.html)  |  `remote`
SSH (Instance)  |  [Illuminate\Remote\Connection](http://laravel.com/api/4.2/Illuminate/Remote/Connection.html)  |
URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/4.2/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/4.2/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](http://laravel.com/api/4.2/Illuminate/Validation/Validator.html) |
View  |  [Illuminate\View\Factory](http://laravel.com/api/4.2/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](http://laravel.com/api/4.2/Illuminate/View/View.html)  |
