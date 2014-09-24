# Route Filters

- [Introduction](#introduction)
- [The Filter Service Provider](#the-filter-service-provider)
- [Creating A Filter](#creating-a-filter)
- [Attaching Filters To Routes](#attaching-filters-to-routes)

<a name="introduction"></a>
## Introduction

Route filters provide a convenient method of limiting access to a given route. For example, you may easily limit route access to users who are authenticated or are administrators.

There are several filters included in the Laravel framework, including an `auth` filter, an `auth.basic` filter, a `guest` filter, and a `csrf` filter. All of these filters are located in the `app/Http/Filters` directory.

<a name="the-filter-service-provider"></a>
## The Filter Service Provider

The filter service provider looks different than most other service providers because it extends the `Illuminate\Routing\Providers\FilterServiceProvider` class, which allows us to remove boilerplate bootstrapping code.

For example, to define a filter that should run before **every** request to the application, simply list the filter class to the `$before` property. To define a filter that should run after every request, list the filter in the `$after` property.

Route filters are listed in the `$filters` property, and are assigned a short-hand "key". This key is used to attach the filter to a given route when the route is defined.

<a name="creating-a-filter"></a>
## Creating A Filter

To create a new route filter, use the `make:filter` Artisan command:

	php artisan filter:make OldFilter

This command will place a new `OldFilter` class within your `app/Http/Filters` directory. In this filter, we will only allow access to the route if the supplied `age` is greater than 200. Otherwise, we will redirect the users back to the "home" URI.

	<?php namespace App\Http\Filters;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Route;

	class OldFilter {

		/**
		 * Run the request filter.
		 *
		 * @param  Route  $route
		 * @param  Request  $request
		 * @return mixed
		 */
		public function filter(Route $route, Request $request)
		{
			if ($request->input('age') < 200)
			{
				return redirect('home');
			}
		}

	}

If the filter returns a response, that response is considered the response to the request and the route will not execute. Any `after` filters on the route are also cancelled.

To register the filter with your application, you should add it to the array of route filters in the `FilterServiceProvider` class:

	/**
	 * All available route filters.
	 *
	 * @var array
	 */
	protected $filters = [
		// ...
		'old' => 'App\Http\Filters\OldFilter',
	];

#### Creating "After" Filters

When generating a filter that is intended to be run after routes are executed, use the `--after` switch. When this switch is present, the generated filter's method signature when include a `Response` argument:

	php artisan make:filter FooFilter --after

#### Creating Global Filters

If you are creating a filter that should run before or after **every** request (a global filter), use the `--global` switch:

	php artisan make:filter FooFilter --global

	php artisan make:filter FooFilter --global --after

<a name="attaching-filters-to-routes"></a>
## Attaching Filters To Routes

To attach a filter to a route, you should use the `before` and `after` array keys:

	// Filter Executed Before Route...

	$router->get('user', ['before' => 'old', function()
	{
		return 'You are over 200 years old!';
	}]);

	// Filter Executed After Route...

	$router->get('user', ['after' => 'log', function()
	{
		//
	}]);

#### Attaching A Filter To A Controller Action

	$router->get('user', ['before' => 'old', 'uses' => 'UserController@showProfile']);

#### Attaching Multiple Filters To A Route

	$router->get('user', ['before' => 'auth|old', function()
	{
		return 'You are authenticated and over 200 years old!';
	}]);

#### Attaching Multiple Filters Via Array

	$router->get('user', ['before' => ['auth', 'old'], function()
	{
		return 'You are authenticated and over 200 years old!';
	}]);

### Specifying Filter Parameters

You may also pass values to filters. For example, this is how you pass values to a "before" filter:

	public function filter(Route $route, Request $request, $minimumAge)
	{
		//
	}

	$router->get('user', ['before' => 'age:200', function()
	{
		return 'Hello World';
	}]);

However, when passing filter values to an "after" filter, the value will be sent after the third argument, which is the Response:

	public function filter(Route $route, Request $request, Response $response, $value)
	{
		//
	}

### Pattern Based Filters

You may also specify that a filter applies to an entire set of routes based on their URI. You should register these pattern based filters within your `app/Providers/RouteServiceProvider.php` file's `before` method:

	public function before(Router $router, UrlGenerator $url)
	{
		$router->when('admin/*', 'admin');
	}

In the example above, the `admin` filter would be applied to all routes beginning with `admin/`. The asterisk is used as a wildcard, and will match any combination of characters.

You may also constrain pattern filters by HTTP verbs:

	public function before(Router $router, UrlGenerator $url)
	{
		$router->when('admin/*', 'admin', ['post']);
	}