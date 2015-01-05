# HTTP Routing

- [Basic Routing](#basic-routing)
- [CSRF Protection](#csrf-protection)
- [Route Parameters](#route-parameters)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
- [Route Model Binding](#route-model-binding)
- [Throwing 404 Errors](#throwing-404-errors)

<a name="basic-routing"></a>
## Basic Routing

You will define most of the routes for your application in the `app/Http/routes.php` file, which is loaded by the `App\Providers\RouteServiceProvider` class.

Within the `routes.php` file, the `$router` variable is available as an instance of the Laravel router, and may be used to register all of your routes. The simplest Laravel route consists of a URI and a Closure callback:

#### Basic GET Route

	$router->get('/', function()
	{
		return 'Hello World';
	});

#### Basic POST Route

	$router->post('foo/bar', function()
	{
		return 'Hello World';
	});

#### Registering A Route For Multiple Verbs

	$router->match(['get', 'post'], '/', function()
	{
		return 'Hello World';
	});

#### Registering A Route That Responds To Any HTTP Verb

	$router->any('foo', function()
	{
		return 'Hello World';
	});

Often, you will need to generate URLs to your routes, you may do so using the `url` helper:

	$url = url('foo');

<a name="csrf-protection"></a>
## CSRF Protection

Laravel provides an easy method of protecting your application from [cross-site request forgeries](http://en.wikipedia.org/wiki/Cross-site_request_forgery). Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of the authenticated user.

Laravel automatically generates a CSRF "token" for each active user session being managed by the application. This token can be used to help verify that the authenticated user is the one actually making the requests to the application.

#### Insert The CSRF Token Into A Form

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

You do not need to manually verify the CSRF token on POST, PUT, or DELETE requests. The `VerifyCsrfToken` HTTP middleware will verify token in the request input matches the token stored in the session.

<a name="route-parameters"></a>
## Route Parameters

Of course, you can capture segments of the request URI within your route:

#### Basic Route Parameter

	$router->get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

#### Optional Route Parameters

	$router->get('user/{name?}', function($name = null)
	{
		return $name;
	});

#### Optional Route Parameters With Default Value

	$router->get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

#### Regular Expression Parameter Constraints

	$router->get('user/{name}', function($name)
	{
		//
	})
	->where('name', '[A-Za-z]+');

	$router->get('user/{id}', function($id)
	{
		//
	})
	->where('id', '[0-9]+');

#### Passing An Array Of Constraints

	$router->get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+'])

#### Defining Global Patterns

If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `before` method of your `RouteServiceProvider`:

	$router->pattern('id', '[0-9]+');

Once the pattern has been defined, it is applied to all routes using that parameter:

	$router->get('user/{id}', function($id)
	{
		// Only called if {id} is numeric.
	});

#### Accessing A Route Parameter Value

If you need to access a route parameter value outside of a route, use the `input` method. For instance, within a filter class, do something like the following:

	public function filter($route, $request)
	{
		if ($route->input('id') == 1)
		{
			//
		}
	}

<a name="named-routes"></a>
## Named Routes

Named routes allow you to conveniently generate URLs or redirects for a specific route. You may specify a name for a route with the `as` array key:

	$router->get('user/profile', ['as' => 'profile', function()
	{
		//
	}]);

You may also specify route names for controller actions:

	$router->get('user/profile', ['as' => 'profile', 'uses' => 'UserController@showProfile']);

Now, you may use the route's name when generating URLs or redirects:

	$url = route('profile');

	$redirect = redirect(route('profile'));

The `currentRouteName` method returns the name of the route handling the current request:

	$name = $router->currentRouteName();

<a name="route-groups"></a>
## Route Groups

Sometimes you may need to apply filters to a group of routes. Instead of specifying the filter on each route, you may use a route group:

	$router->group(['before' => 'auth'], function($router)
	{
		$router->get('/', function()
		{
			// Has Auth Filter
		});

		$router->get('user/profile', function()
		{
			// Has Auth Filter
		});
	});

You may use the `namespace` parameter within your `group` array to specify the namespace for all controllers within the group:

	$router->group(['namespace' => 'Admin'], function($router)
	{
		//
	});

> **Note:** By default, the `RouteServiceProvider` includes your `routes.php` file within a namespace group, allowing you to register controller routes without specifying the full namespace.

<a name="sub-domain-routing"></a>
### Sub-Domain Routing

Laravel routes can also handle wildcard sub-domains, and will pass your wildcard parameters from the domain:

#### Registering Sub-Domain Routes

	$router->group(['domain' => '{account}.myapp.com'], function($router)
	{

		$router->get('user/{id}', function($account, $id)
		{
			//
		});

	});

<a name="route-prefixing"></a>
### Route Prefixing

A group of routes may be prefixed by using the `prefix` option in the attributes array of a group:

	$router->group(['prefix' => 'admin'], function($router)
	{

		$router->get('user', function()
		{
			//
		});

	});

<a name="route-model-binding"></a>
## Route Model Binding

Laravel model binding provides a convenient way to inject class instances into your routes. For example, instead of injecting a user's ID, you can inject the entire User class instance that matches the given ID.

First, use the router's `model` method to specify the class for a given parameter. You should define your model bindings in the `RouteServiceProvider::before` method:

#### Binding A Parameter To A Model

	public function before(Router $router, UrlGenerator $url)
	{
		$router->model('user', 'App\User');
	}

Next, define a route that contains a `{user}` parameter:

	$router->get('profile/{user}', function(App\User $user)
	{
		//
	});

Since we have bound the `{user}` parameter to the `App\User` model, a `User` instance will be injected into the route. So, for example, a request to `profile/1` will inject the `User` instance which has an ID of 1.

> **Note:** If a matching model instance is not found in the database, a 404 error will be thrown.

If you wish to specify your own "not found" behavior, pass a Closure as the third argument to the `model` method:

	public function before(Router $router, UrlGenerator $url)
	{
		$router->model('user', 'User', function()
		{
			throw new NotFoundHttpException;
		});
	}

If you wish to use your own resolution logic, you should use the `Router::bind` method. The Closure you pass to the `bind` method will receive the value of the URI segment, and should return an instance of the class you want to be injected into the route:

	public function before(Router $router, UrlGenerator $url)
	{
		$router->bind('user', function($value)
		{
			return User::where('name', $value)->first();
		});
	}

<a name="throwing-404-errors"></a>
## Throwing 404 Errors

There are two ways to manually trigger a 404 error from a route. First, you may use the `abort` helper:

	abort(404);

The `abort` helper simply throws a `Symfony\Component\HttpFoundation\Exception\HttpException` with the specified status code.

Secondly, you may manually throw an instance of `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

More information on handling 404 exceptions and using custom responses for these errors may be found in the [errors](/docs/master/errors#handling-404-errors) section of the documentation.
