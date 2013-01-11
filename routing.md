# Routing

- [Basic Routing](#basic-routing)
- [Route Parameters](#route-parameters)
- [Route Filters](#route-filters)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
- [Sub-Domain Routing](#sub-domain-routing)
- [Throwing 404 Errors](#throwing-404-errors)

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

<a name="route-parameters"></a>
## Route Parameters

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

**Optional Route Parameters**

	Route::get('user/{name?}', function($name)
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
	->where('name', 'A-Za-z');

<a name="route-filters"></a>
## Route Filters

Route filters provide a convenient way of limiting access to a given route, which is useful for creating areas of your site which require authentication. There are several filters included in the Laravel framework, including an `auth` filter, a `guest` filter, and a `csrf`filter. These are located in the `app/filters.php` file.

**Defining A Route Filter**

	Route::filter('old', function()
	{
		if (Input::get('age') < 200)
		{
			return Redirect::to('home');
		}
	}
	});

If a response is returned from a filter, that response will be considered the response to the request and the route will not be executed.

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

	Route::filter('age', function($value)
	{
		//
	});

	Route::get('user', array('before' => 'age:200', function()
	{
		return 'Hello World';
	}));

**Pattern Based Filters**

You may also specify that a filter applies to an entire set of routes based on their URI.

	Route::filter('admin', function()
	{
		//
	});

	Route::when('admin/*', 'admin');

In the example above, the `admin` filter would be applied to all routes beginning with `admin/`. The asterisk is used as a wildcard, and will match any combination of characters.

**Filter Classes**

For advanced filtering, you may wish to use a class instead of a Closure. Since filter classes are resolved out of the application [IoC container](/docs/ioc), you will be able to utilize dependency injection in these filters for greater testability.

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

Now, you may use the route's name when generating URLs or redirects:

	$url = URL::route('profile');

	$redirect = Redirect::route('profile');

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

	Route::group(array('domain' => '{account}.myapp.com', function()
	{

		Route::get('user/{id}', function($account, $id)
		{
			//
		});

	}));

<a name="throwing-404-errors"></a>
## Throwing 404 Errors

There are two ways to manually trigger a 404 error from a route. First, you may use the `App::abort` method:

	App::abort(404);

Second, you may throw an instance of `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

More information on handling 404 exceptions and using custom responses for these errors may be found in the [errors](/docs/errors#handling-404-errors) section of the documentation.
