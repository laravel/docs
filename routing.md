# HTTP Routing

- [Basic Routing](#basic-routing)
- [CSRF Protection](#csrf-protection)
- [Method Spoofing](#method-spoofing)
- [Route Parameters](#route-parameters)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
- [Route Model Binding](#route-model-binding)
- [Throwing 404 Errors](#throwing-404-errors)

<a name="basic-routing"></a>
## Basic Routing

You will define most of the routes for your application in the `app/Http/routes.php` file, which is loaded by the `App\Providers\RouteServiceProvider` class. The most basic Laravel routes simply accept a URI and a `Closure`:

#### Basic GET Route

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### Other Basic Routes Route

	Route::post('foo/bar', function()
	{
		return 'Hello World';
	});

	Route::put('foo/bar', function()
	{
		//
	});

	Route::delete('foo/bar', function()
	{
		//
	});

#### Registering A Route For Multiple Verbs

	Route::match(['get', 'post'], '/', function()
	{
		return 'Hello World';
	});

#### Registering A Route That Responds To Any HTTP Verb

	Route::any('foo', function()
	{
		return 'Hello World';
	});

Often, you will need to generate URLs to your routes, you may do so using the `url` helper:

	$url = url('foo');

<a name="csrf-protection"></a>
## CSRF Protection

Laravel makes it easy to protect your application from [cross-site request forgeries](http://en.wikipedia.org/wiki/Cross-site_request_forgery). Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of the authenticated user.

Laravel automatically generates a CSRF "token" for each active user session managed by the application. This token is used to verify that the authenticated user is the one actually making the requests to the application.

#### Insert The CSRF Token Into A Form

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

Of course, using the Blade [templating engine](/docs/master/templating):

	<input type="hidden" name="_token" value="{{ csrf_token() }}">

You do not need to manually verify the CSRF token on POST, PUT, or DELETE requests. The `VerifyCsrfToken` [HTTP middleware](/docs/master/middleware) will verify token in the request input matches the token stored in the session.

In addition to looking for the CSRF token as a "POST" parameter, the middleware will also check for the `X-XSRF-TOKEN` request header, which is commonly used by JavaScript frameworks.

<a name="method-spoofing"></a>
## Method Spoofing

HTML forms do not support `PUT` or `DELETE` actions. So, when defining `PUT` or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form.

The value sent with the `_method` field will be used as the HTTP request method. For example:

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
    	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">
    </form>

<a name="route-parameters"></a>
## Route Parameters

Of course, you can capture segments of the request URI within your route:

#### Basic Route Parameter

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

#### Optional Route Parameters

	Route::get('user/{name?}', function($name = null)
	{
		return $name;
	});

#### Optional Route Parameters With Default Value

	Route::get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

#### Regular Expression Parameter Constraints

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

#### Passing An Array Of Constraints

	Route::get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+'])

#### Defining Global Patterns

If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `before` method of your `RouteServiceProvider`:

	$router->pattern('id', '[0-9]+');

Once the pattern has been defined, it is applied to all routes using that parameter:

	Route::get('user/{id}', function($id)
	{
		// Only called if {id} is numeric.
	});

#### Accessing A Route Parameter Value

If you need to access a route parameter value outside of a route, use the `input` method:

	if ($route->input('id') == 1)
	{
		//
	}

You may also access the current route parameters via the `Illuminate\Http\Request` instance. The request instance for the current request may be accessed via the `Request` facade, or by type-hinting the `Illuminate\Http\Request` where dependencies are injected:

	use Illuminate\Http\Request;

	Route::get('user/{id}', function(Request $request, $id)
	{
		if ($request->route('id'))
		{
			//
		}
	});

<a name="named-routes"></a>
## Named Routes

Named routes allow you to conveniently generate URLs or redirects for a specific route. You may specify a name for a route with the `as` array key:

	Route::get('user/profile', ['as' => 'profile', function()
	{
		//
	}]);

You may also specify route names for controller actions:

	Route::get('user/profile', [
        'as' => 'profile', 'uses' => 'UserController@showProfile'
	]);

Now, you may use the route's name when generating URLs or redirects:

	$url = route('profile');

	$redirect = redirect()->route('profile');

The `currentRouteName` method returns the name of the route handling the current request:

	$name = Route::currentRouteName();

<a name="route-groups"></a>
## Route Groups

Sometimes you may need to apply filters to a group of routes. Instead of specifying the filter on each route, you may use a route group:

	Route::group(['before' => 'auth'], function()
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

You may use the `namespace` parameter within your `group` array to specify the namespace for all controllers within the group:

	Route::group(['namespace' => 'Admin'], function()
	{
		//
	});

> **Note:** By default, the `RouteServiceProvider` includes your `routes.php` file within a namespace group, allowing you to register controller routes without specifying the full namespace.

<a name="sub-domain-routing"></a>
### Sub-Domain Routing

Laravel routes also handle wildcard sub-domains, and will pass your wildcard parameters from the domain:

#### Registering Sub-Domain Routes

	Route::group(['domain' => '{account}.myapp.com'], function()
	{

		Route::get('user/{id}', function($account, $id)
		{
			//
		});

	});

<a name="route-prefixing"></a>
### Route Prefixing

A group of routes may be prefixed by using the `prefix` option in the attributes array of a group:

	Route::group(['prefix' => 'admin'], function()
	{

		Route::get('user', function()
		{
			//
		});

	});

<a name="route-model-binding"></a>
## Route Model Binding

Laravel model binding provides a convenient way to inject class instances into your routes. For example, instead of injecting a user's ID, you can inject the entire User class instance that matches the given ID.

First, use the router's `model` method to specify the class for a given parameter. You should define your model bindings in the `RouteServiceProvider::boot` method:

#### Binding A Parameter To A Model

	public function boot(Router $router)
	{
		parent::boot($router);

		$router->model('user', 'App\User');
	}

Next, define a route that contains a `{user}` parameter:

	Route::get('profile/{user}', function(App\User $user)
	{
		//
	});

Since we have bound the `{user}` parameter to the `App\User` model, a `User` instance will be injected into the route. So, for example, a request to `profile/1` will inject the `User` instance which has an ID of 1.

> **Note:** If a matching model instance is not found in the database, a 404 error will be thrown.

If you wish to specify your own "not found" behavior, pass a Closure as the third argument to the `model` method:

	Route::model('user', 'User', function()
	{
		throw new NotFoundHttpException;
	});

If you wish to use your own resolution logic, you should use the `Router::bind` method. The Closure you pass to the `bind` method will receive the value of the URI segment, and should return an instance of the class you want to be injected into the route:

	Route::bind('user', function($value)
	{
		return User::where('name', $value)->first();
	});

<a name="throwing-404-errors"></a>
## Throwing 404 Errors

There are two ways to manually trigger a 404 error from a route. First, you may use the `abort` helper:

	abort(404);

The `abort` helper simply throws a `Symfony\Component\HttpFoundation\Exception\HttpException` with the specified status code.

Secondly, you may manually throw an instance of `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

More information on handling 404 exceptions and using custom responses for these errors may be found in the [errors](/docs/master/errors#http-exceptions) section of the documentation.
