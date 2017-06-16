# Controllers

- [Basic Controllers](#basic-controllers)
- [Controller Filters](#controller-filters)
- [Implicit Controllers](#implicit-controllers)
- [RESTful Resource Controllers](#restful-resource-controllers)
- [Handling Missing Methods](#handling-missing-methods)

<a name="basic-controllers"></a>
## Basic Controllers

Instead of defining all of your route-level logic in a single `routes.php` file, you may wish to organize this behavior using Controller classes. Controllers can group related route logic into a class, as well as take advantage of more advanced framework features such as automatic [dependency injection](/docs/4.2/ioc).

Controllers are typically stored in the `app/controllers` directory, and this directory is registered in the `classmap` option of your `composer.json` file by default. However, controllers can technically live in any directory or any sub-directory. Route declarations are not dependent on the location of the controller class file on disk. So, as long as Composer knows how to autoload the controller class, it may be placed anywhere you wish.

Here is an example of a basic controller class:

	class UserController extends BaseController {

		/**
		 * Show the profile for the given user.
		 */
		public function showProfile($id)
		{
			$user = User::find($id);

			return View::make('user.profile', array('user' => $user));
		}

	}

All controllers should extend the `BaseController` class. The `BaseController` is also stored in the `app/controllers` directory, and may be used as a place to put shared controller logic. The `BaseController` extends the framework's `Controller` class. Now, we can route to this controller action like so:

	Route::get('user/{id}', 'UserController@showProfile');

If you choose to nest or organize your controller using PHP namespaces, simply use the fully qualified class name when defining the route:

	Route::get('foo', 'Namespace\FooController@method');

> **Note:** Since we're using [Composer](http://getcomposer.org) to auto-load our PHP classes, controllers may live anywhere on the file system, as long as composer knows how to load them. The controller directory does not enforce any folder structure for your application. Routing to controllers is entirely de-coupled from the file system.

You may also specify names on controller routes:

	Route::get('foo', array('uses' => 'FooController@method', 'as' => 'name'));

To generate a URL to a controller action, you may use the `URL::action` method or the `action` helper method:

	$url = URL::action('FooController@method');

	$url = action('FooController@method');

You may access the name of the controller action being run using the `currentRouteAction` method:

	$action = Route::currentRouteAction();

<a name="controller-filters"></a>
## Controller Filters

[Filters](/docs/4.2/routing#route-filters) may be specified on controller routes similar to "regular" routes:

	Route::get('profile', array('before' => 'auth',
				'uses' => 'UserController@showProfile'));

However, you may also specify filters from within your controller:

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('auth', array('except' => 'getLogin'));

			$this->beforeFilter('csrf', array('on' => 'post'));

			$this->afterFilter('log', array('only' =>
								array('fooAction', 'barAction')));
		}

	}

You may also specify controller filters inline using a Closure:

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter(function()
			{
				//
			});
		}

	}

If you would like to use another method on the controller as a filter, you may use `@` syntax to define the filter:

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('@filterRequests');
		}

		/**
		 * Filter the incoming requests.
		 */
		public function filterRequests($route, $request)
		{
			//
		}

	}

<a name="implicit-controllers"></a>
## Implicit Controllers

Laravel allows you to easily define a single route to handle every action in a controller. First, define the route using the `Route::controller` method:

	Route::controller('users', 'UserController');

The `controller` method accepts two arguments. The first is the base URI the controller handles, while the second is the class name of the controller. Next, just add methods to your controller, prefixed with the HTTP verb they respond to:

	class UserController extends BaseController {

		public function getIndex()
		{
			//
		}

		public function postProfile()
		{
			//
		}

		public function anyLogin()
		{
			//
		}

	}

The `index` methods will respond to the root URI handled by the controller, which, in this case, is `users`.

If your controller action contains multiple words, you may access the action using "dash" syntax in the URI. For example, the following controller action on our `UserController` would respond to the `users/admin-profile` URI:

	public function getAdminProfile() {}

<a name="restful-resource-controllers"></a>
## RESTful Resource Controllers

Resource controllers make it easier to build RESTful controllers around resources. For example, you may wish to create a controller that manages "photos" stored by your application. Using the `controller:make` command via the Artisan CLI and the `Route::resource` method, we can quickly create such a controller.

To create the controller via the command line, execute the following command:

	php artisan controller:make PhotoController

Now we can register a resourceful route to the controller:

	Route::resource('photo', 'PhotoController');

This single route declaration creates multiple routes to handle a variety of RESTful actions on the photo resource. Likewise, the generated controller will already have stubbed methods for each of these actions with notes informing you which URIs and verbs they handle.

#### Actions Handled By Resource Controller

Verb      | Path                        | Action       | Route Name
----------|-----------------------------|--------------|---------------------
GET       | /resource                   | index        | resource.index
GET       | /resource/create            | create       | resource.create
POST      | /resource                   | store        | resource.store
GET       | /resource/{resource}        | show         | resource.show
GET       | /resource/{resource}/edit   | edit         | resource.edit
PUT/PATCH | /resource/{resource}        | update       | resource.update
DELETE    | /resource/{resource}        | destroy      | resource.destroy

Sometimes you may only need to handle a subset of the resource actions:

	php artisan controller:make PhotoController --only=index,show

	php artisan controller:make PhotoController --except=index

And, you may also specify a subset of actions to handle on the route:

	Route::resource('photo', 'PhotoController',
					array('only' => array('index', 'show')));

	Route::resource('photo', 'PhotoController',
					array('except' => array('create', 'store', 'update', 'destroy')));

By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your options:

	Route::resource('photo', 'PhotoController',
					array('names' => array('create' => 'photo.build')));

#### Handling Nested Resource Controllers

To "nest" resource controllers, use "dot" notation in your route declaration:

	Route::resource('photos.comments', 'PhotoCommentController');

This route will register a "nested" resource that may be accessed with URLs like the following: `photos/{photoResource}/comments/{commentResource}`.

	class PhotoCommentController extends BaseController {

		public function show($photoId, $commentId)
		{
			//
		}

	}

#### Adding Additional Routes To Resource Controllers

If it becomes necessary for you to add additional routes to a resource controller beyond the default resource routes, you should define those routes before your call to `Route::resource`:

	Route::get('photos/popular', 'PhotoController@method');
	Route::resource('photos', 'PhotoController');

<a name="handling-missing-methods"></a>
## Handling Missing Methods

When using `Route::controller`, a catch-all method may be defined which will be called when no other matching method is found on a given controller. The method should be named `missingMethod`, and receives the method and parameter array for the request:

#### Defining A Catch-All Method

	public function missingMethod($parameters = array())
	{
		//
	}

If you are using resource controllers, you should define a `__call` magic method on the controller to handle any missing methods.
