# HTTP Middleware

- [Introduction](#introduction)
- [Defining Middleware](#defining-middleware)
- [Registering Middleware](#registering-middleware)

<a name="introduction"></a>
## Introduction

HTTP middleware provide a convenient mechanism for filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application.

Of course, middleware can be written to perform a variety of tasks besides authentication. A CORS middleware might be responsible for adding the proper headers to all responses leaving your application. A logging middleware might log all incoming requests to your application.

There are several middleware included in the Laravel framework, including middleware for maintenance, authentication, CSRF protection, and more. All of these middleware are located in the `app/Http/Middleware` directory.

<a name="defining-middleware"></a>
## Defining Middleware

To create a new route filter, use the `make:middleware` Artisan command:

	php artisan make:middleware OldMiddleware

This command will place a new `OldMiddleware` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `age` is greater than 200. Otherwise, we will redirect the users back to the "home" URI.

	<?php namespace App\Http\Middleware;

	use Illuminate\Contracts\Routing\Middleware;

	class OldMiddleware implements Middleware {

		/**
		 * Run the request filter.
		 *
		 * @param  Request  $request
		 * @param  Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') < 200)
			{
				return redirect('home');
			}

			return $next($request);
		}

	}

As you can see, if the given `age` is less than `200`, the middleware will return an HTTP redirect to the client; otherwise, the request will be passed further into the application. To pass the request deeper into the application (allowing the middleware to "pass"), simply call the `$next` callback with the `$request`.

<a name="registering-middleware"></a>
## Registering Middleware

### Global Middleware

If you want a middleware to be run during every HTTP request to your applciation, simply list the middleware class in the `$middleware` property of your `app/Http/Kernel.php` class.

### Assigning Middleware To Routes

If you would like to assign middleware to specific routes, you should first assign a short-hand key in your `app/Providers/RouteServiceProvider.php` file. By default, the `$middleware` property of this service provider contains entries for the middleware included with Laravel. To add your own, simply append it to this list and assign it a key of your choosing.

Once the middleware has been defined in `RouteServiceProvider`, you may use the `middleware` key in the route options array:

	$router->get('admin/profile', ['middleware' => 'auth', function()
	{
		//
	}]);