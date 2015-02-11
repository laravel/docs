# Extending The Framework

- [Introduction](#introduction)
- [Managers & Factories](#managers-and-factories)
- [Where To Extend](#where-to-extend)
- [Cache](#cache)
- [Session](#session)
- [Authentication](#authentication)
- [IoC Based Extension](#ioc-based-extension)
- [Request Extension](#request-extension)

<a name="introduction"></a>
## Introduction

Laravel offers many extension points for you to customize the behavior of the framework's core components, or even replace them entirely. For example, the hashing facilities are defined by a `HasherInterface` contract, which you may implement based on your application's requirements. You may also extend the `Request` object, allowing you to add your own convenient "helper" methods. You may even add entirely new authentication, cache, and session drivers!

Laravel components are generally extended in two ways: binding new implementations in the IoC container, or registering an extension with a `Manager` class, which are implementations of the "Factory" design pattern. In this chapter we'll explore the various methods of extending the framework and examine the necessary code.

> **Note:** Remember, Laravel components are typically extended in one of two ways: IoC bindings and the `Manager` classes. The manager classes serve as an implementation of the "factory" design pattern, and are responsible for instantiating driver based facilities such as cache and session.

<a name="managers-and-factories"></a>
## Managers & Factories

Laravel has several `Manager` classes that manage the creation of driver-based components. These include the cache, session, authentication, and queue components. The manager class is responsible for creating a particular driver implementation based on the application's configuration. For example, the `CacheManager` class can create APC, Memcached, File, and various other implementations of cache drivers.

Each of these managers includes an `extend` method which may be used to easily inject new driver resolution functionality into the manager. We'll cover each of these managers below, with examples of how to inject custom driver support into each of them.

> **Note:** Take a moment to explore the various `Manager` classes that ship with Laravel, such as the `CacheManager` and `SessionManager`. Reading through these classes will give you a more thorough understanding of how Laravel works under the hood. All manager classes extend the `Illuminate\Support\Manager` base class, which provides some helpful, common functionality for each manager.

<a name="where-to-extend"></a>
## Where To Extend

This documentation covers how to extend a variety of Laravel's components, but you may be wondering where to place your extension code. Like most other bootstrapping code, you are free to place some extensions in your `start` files. Cache and Auth extensions are good candidates for this approach. Other extensions, like `Session`, must be placed in the `register` method of a service provider since they are needed very early in the request life-cycle.

<a name="cache"></a>
## Cache

To extend the Laravel cache facility, we will use the `extend` method on the `CacheManager`, which is used to bind a custom driver resolver to the manager, and is common across all manager classes. For example, to register a new cache driver named "mongo", we would do the following:

	Cache::extend('mongo', function($app)
	{
		// Return Illuminate\Cache\Repository instance...
	});

The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `app/config/cache.php` configuration file. The second argument is a Closure that should return an `Illuminate\Cache\Repository` instance. The Closure will be passed an `$app` instance, which is an instance of `Illuminate\Foundation\Application` and an IoC container.

To create our custom cache driver, we first need to implement the `Illuminate\Cache\StoreInterface` contract. So, our MongoDB cache implementation would look something like this:

	class MongoStore implements Illuminate\Cache\StoreInterface {

		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}

	}

We just need to implement each of these methods using a MongoDB connection. Once our implementation is complete, we can finish our custom driver registration:

	use Illuminate\Cache\Repository;

	Cache::extend('mongo', function($app)
	{
		return new Repository(new MongoStore);
	});

As you can see in the example above, you may use the base `Illuminate\Cache\Repository` when creating custom cache drivers. There is typically no need to create your own repository class.

If you're wondering where to put your custom cache driver code, consider making it available on Packagist! Or, you could create an `Extensions` namespace within your application's primary folder. For example, if the application is named `Snappy`, you could place the cache extension in `app/Snappy/Extensions/MongoStore.php`. However, keep in mind that Laravel does not have a rigid application structure and you are free to organize your application according to your preferences.

> **Note:** If you're ever wondering where to put a piece of code, always consider a service provider. As we've discussed, using a service provider to organize framework extensions is a great way to organize your code.

<a name="session"></a>
## Session

Extending Laravel with a custom session driver is just as easy as extending the cache system. Again, we will use the `extend` method to register our custom code:

	Session::extend('mongo', function($app)
	{
		// Return implementation of SessionHandlerInterface
	});

### Where To Extend The Session

Session extensions need to be registered differently than other extensions like Cache and Auth. Since sessions are started very early in the request-lifecycle, registering the extensions in a `start` file will happen too late. Instead, a [service provider](/docs/4.2/ioc#service-providers) will be needed. You should place your session extension code in the `register` method of your service provider, and the provider should be placed **below** the default `Illuminate\Session\SessionServiceProvider` in the `providers` configuration array.

### Writing The Session Extension

Note that our custom session driver should implement the `SessionHandlerInterface`. This interface is included in the PHP 5.4+ core. If you are using PHP 5.3, the interface will be defined for you by Laravel so you have forward-compatibility. This interface contains just a few simple methods we need to implement. A stubbed MongoDB implementation would look something like this:

	class MongoHandler implements SessionHandlerInterface {

		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}

	}

Since these methods are not as readily understandable as the cache `StoreInterface`, let's quickly cover what each of the methods do:

- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will almost never need to put anything in this method. You can leave it as an empty stub. It is simply a fact of poor interface design (which we'll discuss later) that PHP requires us to implement this method.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB, Dynamo, etc.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.

Once the `SessionHandlerInterface` has been implemented, we are ready to register it with the Session manager:

	Session::extend('mongo', function($app)
	{
		return new MongoHandler;
	});

Once the session driver has been registered, we may use the `mongo` driver in our `app/config/session.php` configuration file.

> **Note:** Remember, if you write a custom session handler, share it on Packagist!

<a name="authentication"></a>
## Authentication

Authentication may be extended the same way as the cache and session facilities. Again, we will use the `extend` method we have become familiar with:

	Auth::extend('riak', function($app)
	{
		// Return implementation of Illuminate\Auth\UserProviderInterface
	});

The `UserProviderInterface` implementations are only responsible for fetching a `UserInterface` implementation out of a persistent storage system, such as MySQL, Riak, etc. These two interfaces allow the Laravel authentication mechanisms to continue functioning regardless of how the user data is stored or what type of class is used to represent it.

Let's take a look at the `UserProviderInterface`:

	interface UserProviderInterface {

		public function retrieveById($identifier);
		public function retrieveByToken($identifier, $token);
		public function updateRememberToken(UserInterface $user, $token);
		public function retrieveByCredentials(array $credentials);
		public function validateCredentials(UserInterface $user, array $credentials);

	}

The `retrieveById` function typically receives a numeric key representing the user, such as an auto-incrementing ID from a MySQL database. The `UserInterface` implementation matching the ID should be retrieved and returned by the method.

The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, stored in a field `remember_token`. As with with previous method, the `UserInterface` implementation should be returned.

The `updateRememberToken` method updates the `$user` field `remember_token` with the new `$token`. The new token can be either a fresh token, assigned on successfull "remember me" login attempt, or a null when user is logged out.

The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to sign into an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition on `$credentials['username']`. **This method should not attempt to do any password validation or authentication.**

The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method might compare the `$user->getAuthPassword()` string to a `Hash::make` of `$credentials['password']`.

Now that we have explored each of the methods on the `UserProviderInterface`, let's take a look at the `UserInterface`. Remember, the provider should return implementations of this interface from the `retrieveById` and `retrieveByCredentials` methods:

	interface UserInterface {

		public function getAuthIdentifier();
		public function getAuthPassword();

	}

This interface is simple. The `getAuthIdentifier` method should return the "primary key" of the user. In a MySQL back-end, again, this would be the auto-incrementing primary key. The `getAuthPassword` should return the user's hashed password. This interface allows the authentication system to work with any User class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes a `User` class in the `app/models` directory which implements this interface, so you may consult this class for an implementation example.

Finally, once we have implemented the `UserProviderInterface`, we are ready to register our extension with the `Auth` facade:

	Auth::extend('riak', function($app)
	{
		return new RiakUserProvider($app['riak.connection']);
	});

After you have registered the driver with the `extend` method, you switch to the new driver in your `app/config/auth.php` configuration file.

<a name="ioc-based-extension"></a>
## IoC Based Extension

Almost every service provider included with the Laravel framework binds objects into the IoC container. You can find a list of your application's service providers in the `app/config/app.php` configuration file. As you have time, you should skim through each of these provider's source code. By doing so, you will gain a much better understanding of what each provider adds to the framework, as well as what keys are used to bind various services into the IoC container.

For example, the `HashServiceProvider` binds a `hash` key into the IoC container, which resolves into a `Illuminate\Hashing\BcryptHasher` instance. You can easily extend and override this class within your own application by overriding this IoC binding. For example:

	class SnappyHashProvider extends Illuminate\Hashing\HashServiceProvider {

		public function boot()
		{
			App::bindShared('hash', function()
			{
				return new Snappy\Hashing\ScryptHasher;
			});

			parent::boot();
		}

	}

Note that this class extends the `HashServiceProvider`, not the default `ServiceProvider` base class. Once you have extended the service provider, swap out the `HashServiceProvider` in your `app/config/app.php` configuration file with the name of your extended provider.

This is the general method of extending any core class that is bound in the container. Essentially every core class is bound in the container in this fashion, and can be overridden. Again, reading through the included framework service providers will familiarize you with where various classes are bound into the container, and what keys they are bound by. This is a great way to learn more about how Laravel is put together.

<a name="request-extension"></a>
## Request Extension

Because it is such a foundational piece of the framework and is instantiated very early in the request cycle, extending the `Request` class works a little differently than the previous examples.

First, extend the class like normal:

	<?php namespace QuickBill\Extensions;

	class Request extends \Illuminate\Http\Request {

		// Custom, helpful methods here...

	}

Once you have extended the class, open the `bootstrap/start.php` file. This file is one of the very first files to be included on each request to your application. Note that the first action performed is the creation of the Laravel `$app` instance:

	$app = new \Illuminate\Foundation\Application;

When a new application instance is created, it will create a new `Illuminate\Http\Request` instance and bind it to the IoC container using the `request` key. So, we need a way to specify a custom class that should be used as the "default" request type, right? And, thankfully, the `requestClass` method on the application instance does just this! So, we can add this line at the very top of our `bootstrap/start.php` file:

	use Illuminate\Foundation\Application;

	Application::requestClass('QuickBill\Extensions\Request');

Once you have specified the custom request class, Laravel will use this class anytime it creates a `Request` instance, conveniently allowing you to always have an instance of your custom request class available, even in unit tests!
