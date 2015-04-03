# HTTP Routing

- [Basic Routing](#basic-routing)
- [Route Parameters](#route-parameters)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
- [CSRF Protection](#csrf-protection)
- [Method Spoofing](#method-spoofing)
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

#### Other Basic Routes

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

#### Routing Requests To Controllers

If you are interested in routing requests to classes, check out the documentation on [controllers](/docs/controllers).

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

If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `boot` method of your `RouteServiceProvider`:

	$router->pattern('id', '[0-9]+');

Once the pattern has been defined, it is applied to all routes using that parameter:

	Route::get('user/{id}', function($id)
	{
		// Only called if {id} is numeric.
	});

#### Accessing A Route Parameter Value

You may access the current route parameters via the `Illuminate\Http\Request` instance. The request instance for the current request may be accessed via the `Request` facade, or by type-hinting the `Illuminate\Http\Request` where dependencies are injected:

	use Illuminate\Http\Request;

	Route::get('user/{id}', function(Request $request, $id)
	{
		if ($request->route('id'))
		{
			//
		}
	});

Alternatively, to access the values within a controller:

	// Import The Request At The Top Of Class...
	use Illuminate\Http\Request;

	public function index(Request $request)
	{
		if ($request->route('id'))
		{
			//
		}
	}

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

The `currentRouteName` method returns the name of the route handling the current request. You may call this method using the `Route` facade:

	$name = Route::currentRouteName();

Don't forget to import the `Route` facade into your current namespace when calling this method.

<a name="route-groups"></a>
## Route Groups

Sometimes you may need to apply middleware to a group of routes. Instead of specifying the middleware on each route, you may use a route group:

Shared attributes are specified in an array format as the first parameter to the `Route::group` method.

<a name="route-group-middleware"></a>
### Middleware

Middleware is applied to all routes within the group by defining the list of middleware with the `middleware` parameter on the group attribute array. Middleware will be executed in the order you define this array:

	Route::group(['middleware' => 'foo|bar'], function()
	{
		Route::get('/', function()
		{
			// Uses Auth Middleware
		});

		Route::get('user/profile', function()
		{
			// Uses Auth Middleware
		});

	});

<a name="route-group-namespace"></a>
### Namespaces

You may use the `namespace` parameter in your group attribute array to specify the namespace for all controllers within the group:

	Route::group(['namespace' => 'Admin'], function()
	{
		// Controllers Within The "App\Http\Controllers\Admin" Namespace

		Route::group(['namespace' => 'User'], function()
		{
			// Controllers Within The "App\Http\Controllers\Admin\User" Namespace
		});
	});

> **Note:** By default, the `RouteServiceProvider` includes your `routes.php` file within a namespace group, allowing you to register controller routes without specifying the full `App\Http\Controllers` namespace prefix.

<a name="sub-domain-routing"></a>
### Sub-Domain Routing

Laravel routes can also handle wildcard sub-domains, and will pass your wildcard parameters from the domain:

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
		Route::get('users', function()
		{
			// Matches The "/admin/users" URL
		});
	});

You can also utilize the `prefix` parameter to pass common parameters to your routes:

#### Registering a URL parameter in a route prefix

	Route::group(['prefix' => 'accounts/{account_id}'], function()
	{
		Route::get('detail', function($account_id)
		{
			// Handles Requests To admin/user
		});
	});

You can even define parameter constraints for the named parameters in your prefix:

	Route::group([
		'prefix' => 'accounts/{account_id}',
		'where' => ['account_id' => '[0-9]+'],
	], function() {

		// Define Routes Here
	});

<a name="csrf-protection"></a>
## CSRF Protection

Laravel makes it easy to protect your application from [cross-site request forgeries](http://en.wikipedia.org/wiki/Cross-site_request_forgery). Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of the authenticated user.

Laravel automatically generates a CSRF "token" for each active user session managed by the application. This token is used to verify that the authenticated user is the one actually making the requests to the application.

#### Insert The CSRF Token Into A Form

	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

Of course, using the Blade [templating engine](/docs/master/templating):

	<input type="hidden" name="_token" value="{{ csrf_token() }}">

You do not need to manually verify the CSRF token on POST, PUT, or DELETE requests. The `VerifyCsrfToken` [HTTP middleware](/docs/master/middleware) will verify token in the request input matches the token stored in the session.

#### X-CSRF-TOKEN

In addition to looking for the CSRF token as a "POST" parameter, the middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in a "meta" tag and instruct jQuery to add it to all request headers:

	<meta name="csrf-token" content="{{ csrf_token() }}" />

	$.ajaxSetup({
		headers: {
			'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
		}
	});

Now all AJAX requests will automatically include the CSRF token:

	$.ajax({
	   url: "/foo/bar",
	})

#### X-XSRF-TOKEN

Laravel also stores the CSRF token in a `XSRF-TOKEN` cookie. You can use the cookie value to set the `X-XSRF-TOKEN` request header. Some Javascript frameworks, like Angular, do this automatically for you.

> Note: The difference between the `X-CSRF-TOKEN` and `X-XSRF-TOKEN` is that the first uses a plain text value and the latter uses an encrypted value, because cookies in Laravel are always encrypted.

<a name="method-spoofing"></a>
## Method Spoofing

HTML forms do not support `PUT`, `PATCH` or `DELETE` actions. So, when defining `PUT`, `PATCH` or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form.

The value sent with the `_method` field will be used as the HTTP request method. For example:

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
	</form>

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
