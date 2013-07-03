# Routing

- [Basic Routing](#basic-routing)
- [Route Parameters](#route-parameters)
- [Route Filters](#route-filters)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
- [Sub-Domain Routing](#sub-domain-routing)
- [Route Prefixing](#route-prefixing)
- [Route Model Binding](#route-model-binding)
- [Throwing 404 Errors](#throwing-404-errors)
- [Routing To Controllers](#routing-to-controllers)

<a name="basic-routing"></a>
## Basic Routing

Most of the routes for your application will be defined in the `app/routes.php` file. The simplest Laravel routes consist of a URI and a Closure callback.

**Basic GET Route**

	Route::get('/', function()
	{
		return 'Hello World';
	});

**Basic POST Route**

	Route::post('foo/bar', function()
	{
		return 'Hello World';
	});

**Registering A Route Responding To Any HTTP Verb**

	Route::any('foo', function()
	{
		return 'Hello World';
	});

**Forcing A Route To Be Served Over HTTPS**

	Route::get('foo', array('https', function()
	{
		return 'Must be over HTTPS';
	}));

Often, you will need to generate URLs to your routes, you may do so using the `URL::to` method:

	$url = URL::to('foo');

<a name="route-parameters"></a>
## Route Parameters

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

**Optional Route Parameters**

	Route::get('user/{name?}', function($name = null)
	{
		return $name;
	});

**Optional Route Parameters With Defaults**

	Route::get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

**Regular Expression Route Constraints**

	Route::get('user/{name}', function($name)
	{
		//
	})
	->where('name', '[A-Za-z]+');

	Route::get('user/{id}', function($id)
	{
		//
	})
	->where('id', '[0-9]+');

Of course, you may pass an array of constraints when necessary:

	Route::get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(array('id' => '[0-9]+', 'name' => '[a-z]+'))

<a name="route-filters"></a>
## Route Filters

Route filters provide a convenient way of limiting access to a given route, which is useful for creating areas of your site which require authentication. There are several filters included in the Laravel framework, including an `auth` filter, an `auth.basic` filter, a `guest` filter, and a `csrf`filter. These are located in the `app/filters.php` file.

**Defining A Route Filter**

	Route::filter('old', function()
	{
		if (Input::get('age') < 200)
		{
			return Redirect::to('home');
		}
	});

If a response is returned from a filter, that response will be considered the response to the request and the route will not be executed, and any `after` filters on the route will also be cancelled.

**Attaching A Filter To A Route**

	Route::get('user', array('before' => 'old', function()
	{
		return 'You are over 200 years old!';
	}));

**Attaching Multiple Filters To A Route**

	Route::get('user', array('before' => 'auth|old', function()
	{
		return 'You are authenticated and over 200 years old!';
	}));

**Specifying Filter Parameters**

	Route::filter('age', function($route, $request, $value)
	{
		//
	});

	Route::get('user', array('before' => 'age:200', function()
	{
		return 'Hello World';
	}));

After filters receive a `$response` as the third argument passed to the filter:

	Route::filter('log', function($route, $request, $response, $value)
	{
		//
	});

**Pattern Based Filters**

You may also specify that a filter applies to an entire set of routes based on their URI.

	Route::filter('admin', function()
	{
		//
	});

	Route::when('admin/*', 'admin');

In the example above, the `admin` filter would be applied to all routes beginning with `admin/`. The asterisk is used as a wildcard, and will match any combination of characters.

You may also constrain pattern filters by HTTP verbs:

	Route::when('admin/*', 'admin', array('post'));

**Filter Classes**

For advanced filtering, you may wish to use a class instead of a Closure. Since filter classes are resolved out of the application [IoC Container](/docs/ioc), you will be able to utilize dependency injection in these filters for greater testability.

**Defining A Filter Class**

	class FooFilter {

		public function filter()
		{
			// Filter logic...
		}

	}

**Registering A Class Based Filter**

	Route::filter('foo', 'FooFilter');

<a name="named-routes"></a>
## Named Routes

Named routes make referring to routes when generating redirects or URLs more convenient. You may specify a name for a route like so:

	Route::get('user/profile', array('as' => 'profile', function()
	{
		//
	}));

You may also specify route names for controller actions:

	Route::get('user/profile', array('as' => 'profile', 'uses' => 'UserController@showProfile'));

Now, you may use the route's name when generating URLs or redirects:

	$url = URL::route('profile');

	$redirect = Redirect::route('profile');

You may access the name of a route that is running via the `currentRouteName` method:

	$name = Route::currentRouteName();

<a name="route-groups"></a>
## Route Groups

Sometimes you may need to apply filters to a group of routes. Instead of specifying the filter on each route, you may use a route group:

	Route::group(array('before' => 'auth'), function()
	{
		Route::get('/', function()
		{
			// Has Auth Filter
		});

		Route::get('user/profile', function()
		{
			// Has Auth Filter
		});
	});

<a name="sub-domain-routing"></a>
## Sub-Domain Routing

Laravel routes are also able to handle wildcard sub-domains, and pass you wildcard parameters from the domain:

**Registering Sub-Domain Routes**

	Route::group(array('domain' => '{account}.myapp.com'), function()
	{

		Route::get('user/{id}', function($account, $id)
		{
			//
		});

	});
<a name="route-prefixing"></a>
## Route Prefixing

A group of routes may be prefixed by using the `prefix` option in the attributes array of a group:

**Prefixing Grouped Routes**

	Route::group(array('prefix' => 'admin'), function()
	{

		Route::get('user', function()
		{
			//
		});

	});

<a name="route-model-binding"></a>
## Route Model Binding

Model binding provides a convenient way to inject model instances into your routes. For example, instead of injecting a user's ID, you can inject the entire User model instance that matches the given ID. First, use the `Route::model` method to specify the model that should be used for a given parameter:

**Binding A Parameter To A Model**

	Route::model('user', 'User');

Next, define a route that contains a `{user}` parameter:

	Route::get('profile/{user}', function(User $user)
	{
		//
	});

Since we have bound the `{user}` parameter to the `User` model, a `User` instance will be injected into the route. So, for example, a request to `profile/1` will inject the `User` instance which has an ID of 1.

> **Note:** If a matching model instance is not found in the database, a 404 error will be thrown.

If you wish to specify your own "not found" behavior, you may pass a Closure as the third argument to the `model` method:

	Route::model('user', 'User', function()
	{
		throw new NotFoundException;
	});

Sometimes you may wish to use your own resolver for route parameters. Simply use the `Route::bind` method:

	Route::bind('user', function($value, $route)
	{
		return User::where('name', $value)->first();
	});

<a name="throwing-404-errors"></a>
## Throwing 404 Errors

There are two ways to manually trigger a 404 error from a route. First, you may use the `App::abort` method:

	App::abort(404);

Second, you may throw an instance of `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

More information on handling 404 exceptions and using custom responses for these errors may be found in the [errors](/docs/errors#handling-404-errors) section of the documentation.

<a name="routing-to-controllers"></a>
## Routing To Controllers

Laravel allows you to not only route to Closures, but also to controller classes, and even allows the creation of [resource controllers](/docs/controllers#resource-controllers).

See the documentation on [Controllers](/docs/controllers) for more details.
