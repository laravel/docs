# Controllers

- [Basic Controllers](#basic-controllers)
- [Controller Filters](#controller-filters)
- [Controller Layouts](/docs/templates#controller-layouts)
- [RESTful Controllers](#restful-controllers)
- [Resource Controllers](#resource-controllers)

<a name="basic-controllers"></a>
## Basic Controllers

Instead of defining all of your route-level logic in a single `routes.php` file, you may wish to organize this behavior using Controller classes. Controllers can group related route logic into a class, as well as take advantage of more advanced framework features such as automatic [dependency injection](/docs/ioc).

Controllers are typically stored in the `app/controllers` directory, and this directory is registered in the `classmap` option of your `composer.json` file by default.

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

All controllers should extend the `BaseController` class. The `BaseController` is also stored in the `app/controllers` directory, and may be used as a place to put shared controller logic. The `BaseController` extends the framework's `Controller` class. Now, We can route to this controller action like so:

	Route::get('user/{id}', 'UserController@showProfile');

If you choose to nest or organize your controller using PHP namespaces, simply use the fully qualified class name when defining the route:

	Route::get('foo', 'Namespace\FooController@method');

You may also specify names on controller routes:

	Route::get('foo', array('uses' => 'FooController@method',
											'as' => 'name'));

> **Note:** After creating a new class, make sure to run `composer dump-autoload` from the command line. This will allow the framework to automatically load your class.

<a name="controller-filters"></a>
## Controller Filters

[Filters](/docs/routing#route-filters) may be specified on controller routes similar to "regular" routes:

	Route::get('profile', array('before' => 'auth',
				'uses' => 'UserController@showProfile'));

However, you may also specify filters from within your controller:

	class UserController extends BaseController {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->beforeFilter('auth');

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

<a name="restful-controllers"></a>
## RESTful Controllers

Laravel allows you to easily define a single route to handle every action in a controller using simple, REST naming conventions. First, define the route using the `Route::controller` method:

**Defining A RESTful Controller**

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

	}

The `index` methods (`getIndex` etc) will respond to the root URI handled by the controller, which, in this case, is `users/`. Also take a look at the [Resource Controller actions](#resource-controller-actions) down below.

If your controller action contains multiple words, you may access the action using "dash" syntax in the URI. For example, the following controller action on our `UserController` would respond to the `users/admin-profile` URI:

	public function getAdminProfile() {}

<a name="resource-controllers"></a>
## Resource Controllers

Resource controllers make it easier to build RESTful controllers around resources. For example, you may wish to create a controller that manages "photos" stored by your application. Using the `controller:make` command via the Artisan CLI and the `Route::resource` method, we can quickly create such a controller.

To create the controller via the command line, execute the following command:

	php artisan controller:make PhotoController

Now we can register a resourceful route to the controller:

	Route::resource('photo', 'PhotoController');

This single route declaration creates multiple routes to handle a variety of RESTful actions on the photo resource. Likewise, the generated controller will already have stubbed methods for each of these actions with notes informing you which URIs and verbs they handle.

<a name="resource-controller-actions"></a>
**Actions Handled By Resource Controller**

Verb      | Path                  | Action
----------|-----------------------|--------------
GET       | /resource             | index
GET       | /resource/create      | create
POST      | /resource             | store
GET       | /resource/{id}        | show
GET       | /resource/{id}/edit   | edit
PUT/PATCH | /resource/{id}        | update
DELETE    | /resource/{id}        | destroy

Sometimes you may only need to handle a subset of the resource actions:

	php artisan controller:make PhotoController --only=index,show

	php artisan controller:make PhotoController --except=index

And, you may also specify a subset of actions to handle on the route:

	Route::resource('photo', 'PhotoController',
					array('only' => array('index', 'show')));
