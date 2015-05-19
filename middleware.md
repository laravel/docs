# HTTP Middleware

- [Introduction](#introduction)
- [Defining Middleware](#defining-middleware)
- [Registering Middleware](#registering-middleware)
- [Terminable Middleware](#terminable-middleware)

<a name="introduction"></a>
## Introduction

HTTP middleware provide a convenient mechanism for filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application.

Of course, middleware can be written to perform a variety of tasks besides authentication. A CORS middleware might be responsible for adding the proper headers to all responses leaving your application. A logging middleware might log all incoming requests to your application.

There are several middleware included in the Laravel framework, including middleware for maintenance, authentication, CSRF protection, and more. All of these middleware are located in the `app/Http/Middleware` directory.

<a name="defining-middleware"></a>
## Defining Middleware

To create a new middleware, use the `make:middleware` Artisan command:

	php artisan make:middleware OldMiddleware

This command will place a new `OldMiddleware` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `age` is greater than 200. Otherwise, we will redirect the users back to the "home" URI.

	<?php namespace App\Http\Middleware;
	
	use Closure;

	class OldMiddleware {

		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
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

It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely.

### *Before* / *After* Middleware

Whether a middleware runs before or after a request depends on the middleware itself. This middleware would perform some task **before** the request is handled by the application:

	<?php namespace App\Http\Middleware;
	
	use Closure;

	class BeforeMiddleware implements Middleware {

		public function handle($request, Closure $next)
		{
			// Perform action

			return $next($request);
		}
	}

However, this middleware would perform its task **after** the request is handled by the application:

	<?php namespace App\Http\Middleware;
	
	use Closure;

	class AfterMiddleware implements Middleware {

		public function handle($request, Closure $next)
		{
			$response = $next($request);

			// Perform action

			return $response;
		}
	}

<a name="registering-middleware"></a>
## Registering Middleware

### Global Middleware

If you want a middleware to be run during every HTTP request to your application, simply list the middleware class in the `$middleware` property of your `app/Http/Kernel.php` class.

### Assigning Middleware To Routes

If you would like to assign middleware to specific routes, you should first assign the middleware a short-hand key in your `app/Http/Kernel.php` file. By default, the `$routeMiddleware` property of this class contains entries for the middleware included with Laravel. To add your own, simply append it to this list and assign it a key of your choosing.

Once the middleware has been defined in the HTTP kernel, you may use the `middleware` key in the route options array:

	Route::get('admin/profile', ['middleware' => 'auth', function()
	{
		//
	}]);

<a name="terminable-middleware"></a>
## Terminable Middleware

Sometimes a middleware may need to do some work after the HTTP response has already been sent to the browser. For example, the "session" middleware included with Laravel writes the session data to storage _after_ the response has been sent to the browser. To accomplish this, you may define the middleware as "terminable".

	use Closure;
	use Illuminate\Contracts\Routing\TerminableMiddleware;

	class StartSession implements TerminableMiddleware {

		public function handle($request, Closure $next)
		{
			return $next($request);
		}

		public function terminate($request, $response)
		{
			// Store the session data...
		}

	}

As you can see, in addition to defining a `handle` method, `TerminableMiddleware` define a `terminate` method. This method receives both the request and the response. Once you have defined a terminable middleware, you should add it to the list of global middlewares in your HTTP kernel.
