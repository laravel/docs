# HTTP Controllers

- [Introduction](#introduction)
- [Basic Controllers](#basic-controllers)
- [Controller Filters](#controller-filters)
- [RESTful Resource Controllers](#restful-resource-controllers)
- [Dependency Injection & Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
## Introduction

Instead of defining all of your request handling logic in a single `routes.php` file, you may wish to organize this behavior using Controller classes. Controllers can group related HTTP request handling logic into a class, as well as take advantage of more advanced framework features such as automatic [dependency injection](/docs/master/container).

Controllers are typically stored in the `app/Http/Controllers` directory. However, controllers can technically live in any directory or any sub-directory. Route declarations are not dependent on the location of the controller class file on disk. So, as long as Composer knows how to autoload the controller class, it may be placed anywhere you wish.

<a name="basic-controllers"></a>
## Basic Controllers

Here is an example of a basic controller class:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Users\Repository as UserRepository;

	class UserController extends Controller {

		/**
		 * The user repository instance.
		 */
		protected $users;

		/**
		 * Create a new controller instance.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}

		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			$user = $this->users->find($id);

			return view('user.profile', ['user' => $user]);
		}

	}

All controllers should extend the `Illuminate\Routing\Controller` class. Also note that we are type-hinting a dependency in the controller's constructor. Any dependencies listed in the constructor will automatically be resolved by the [service container](/docs/master/container).

We can route to the controller action like so:

	$router->get('user/{id}', 'UserController@showProfile');

#### Controllers & Namespaces

It is very important to note that we did not need to specify the full controller namespace, only the portion of the class name that comes after the `App\Http\Controllers` namespace "root". Because of the call to the `namespaced` helper in your `App\Providers\RouteServiceProvider` class, this "root" namespace will automatically be prepended to all controller routes you register.

If you choose to nest or organize your controllers using PHP namespaces deeper into the `App\Http\Controllers` directory, simply use the specify the class name relative to the `App\Http\Controllers` root namespace. So, if your full controller class is `App\Http\Controllers\Photos\AdminController`, you would register a route like so:

	$router->get('foo', 'Photos\AdminController@method');

> **Note:** Since we're using [Composer](http://getcomposer.org) to auto-load our PHP classes, controllers may live anywhere on the file system, as long as composer knows how to load them. The controller directory does not enforce any folder structure for your application. Routing to controllers is entirely de-coupled from the file system.

#### Naming Controller Routes

Like Closure routes, you may specify names on controller routes:

	$router->get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

#### URLs To Controller Actions

To generate a URL to a controller action, use the `action` helper method:

	$url = action('FooController@method');

**Again**, you only need to specify the portion of the class that that comes after the `App\Http\Controllers` namespace "root". If you wish to generate a URL to a controller action while using the fully qualified class name, without the URL generator automatically preprending the default namespace, you may use a leading slash:

	$url = action('\Namespace\FooController@method');

You may access the name of the controller action being run using the `currentRouteAction` method:

	$action = $router->currentRouteAction();

<a name="controller-filters"></a>
## Controller Filters

[Filters](/docs/master/filters) may be specified on controller routes like so:

	$router->get('profile', ['before' => 'auth', 'uses' => 'UserController@showProfile']);

However, you may also specify filters from within your controller's constructor:

	class UserController extends Controller {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('auth');

			$this->beforeFilter('csrf', ['on' => 'post']);

			$this->afterFilter('log', ['only' => ['fooAction', 'barAction']]);

			$this->afterFilter('scan', ['except' => ['fooAction', 'barAction']]);
		}

	}

#### Closure Controller Filters

Addtionally, you may even specify controller filters inline using a Closure:

	class UserController extends Controller {

		/**
		 * Instantiate a new UserController instance.
		 *
		 * @return void
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

	class UserController extends Controller {

		/**
		 * Instantiate a new UserController instance.
		 *
		 * @return void
		 */
		public function __construct()
		{
			$this->beforeFilter('@filterRequests');
		}

		/**
		 * Filter the incoming requests.
		 *
		 * @param  Route  $route
		 * @param  Request  $request
		 * @return mixed
		 */
		public function filterRequests($route, $request)
		{
			//
		}

	}

<a name="restful-resource-controllers"></a>
## RESTful Resource Controllers

Resource controllers make it painless to build RESTful controllers around resources. For example, you may wish to create a controller that handles HTTP requests regarding "photos" stored by your application. Using the `make:controller` Artisan command, we can quickly create such a controller:

	php artisan make:controller PhotoController

Next, we register a resourceful route to the controller:

	$router->resource('photo', 'PhotoController');

This single route declaration creates multiple routes to handle a variety of RESTful actions on the photo resource. Likewise, the generated controller will already have methods stubbed for each of these actions, including notes informing you which URIs and verbs they handle.

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

#### Customizing Resource Routes

Additionally, you may specify only a subset of actions to handle on the route:

	$router->resource('photo', 'PhotoController',
					['only' => ['index', 'show']]);

	$router->resource('photo', 'PhotoController',
					['except' => ['create', 'store', 'update', 'destroy']]);

By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your options:

	$router->resource('photo', 'PhotoController',
					['names' => ['create' => 'photo.build']]);

#### Handling Nested Resource Controllers

To "nest" resource controllers, use "dot" notation in your route declaration:

	$router->resource('photos.comments', 'PhotoCommentController');

This route will register a "nested" resource that may be accessed with URLs like the following: `photos/{photoResource}/comments/{commentResource}`.

	class PhotoCommentController extends Controller {

		/**
		 * Show the specified photo comment.
		 *
		 * @param  int  $photoId
		 * @param  int  $commentId
		 * @return Response
		 */
		public function show($photoId, $commentId)
		{
			//
		}

	}

#### Adding Additional Routes To Resource Controllers

If it becomes necessary to add additional routes to a resource controller beyond the default resource routes, you should define those routes before your call to `$router->resource`:

	$router->get('photos/popular');

	$router->resource('photos', 'PhotoController');

<a name="dependency-injection-and-controllers"></a>
## Dependency Injection & Controllers

#### Constructor Injection

As you may have noticed in the examples above, the Laravel [service container](/docs/master/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Users\Repository as UserRepository;

	class UserController extends Controller {

		/**
		 * The user repository instance.
		 */
		protected $users;

		/**
		 * Create a new controller instance.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}

	}

Of course, you may also type-hint any [Laravel contract](/docs/master/contracts). If the container can resolve it, you can type-hint it.

#### Method Injection

In addition to constructor injection, you may also type-hint dependencies on your controller's methods. For example, let's type-hint the `Request` instance on one of our methods:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}

	}

If your controller method is also expecting input from a route parameter, simply list your route arguments after your other dependencies:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}

	}

> **Note:** Method injection is fully compatible with [model binding](/docs/master/routing#route-model-binding). The container will intelligently determine which arguments are model bound and which arguments should be injected.
