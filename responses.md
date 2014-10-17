# HTTP Responses

- [Basic Responses](#basic-responses)
- [Redirects](#redirects)
- [Other Responses](#other-responses)
- [Response Macros](#response-macros)

<a name="basic-responses"></a>
## Basic Responses

#### Returning Strings From Routes

The most basic response from a Laravel route is a string:

	$router->get('/', function()
	{
		return 'Hello World';
	});

#### Creating Custom Responses

However, for most routes and controller actions, you will be returning a full `Illuminate\Http\Response` instance or a [view](/docs/master/views). Returning a full `Response` instance allows you customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, providing a variety of methods for building HTTP responses:

	use Illuminate\Http\Response;

	return (new Response($content, $status))
	              ->header('Content-Type', $value);

> **Note:** For a full list of available `Response` methods, check out its [API documentation](http://laravel.com/api/4.2/Illuminate/Http/Response.html) and the [Symfony API documentation](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/Response.html).

#### Sending A View In A Response

If you need access to the `Response` class methods, but want to return a view as the response content, you may use the `view` helper for convenience:

	return (new Response(view('hello')))->header('Content-Type', $type);

#### Attaching Cookies To Responses

	return (new Response($content))->withCookie(cookie('name', 'value'));

#### The Response Factory

The `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/master/contracts) provides a variety of helpful methods for generating `Response` and `RedirectResponse` instances.

<a name="redirects"></a>
## Redirects

Redirect responses are typically instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL.

#### Returning A Redirect

There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the `redirect` helper method. When testing, it is not common to mock the creation of a redirect response, so using the helper method is almost always acceptable:

	return redirect('user/login');

#### Returning A Redirect With Flash Data

Redirecting to a new URL and [flashing data to the session](/docs/master/session) are typically done at the same time. So, for convenience, you can create a `RedirectResponse` instance **and** flash data to the session in a single method chain:

	return redirect('user/login')->with('message', 'Login Failed');

#### Returning A Redirect To A Named Route

When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method:

	return redirect()->route('login');

#### Returning A Redirect To A Named Route With Parameters

If your route has parameters, you may pass them as the second argument to the `route` method.

	// For a route with the following URI: profile/{id}

	return redirect()->route('profile', [1]);

#### Returning A Redirect To A Named Route Using Named Parameters

	// For a route with the following URI: profile/{user}

	return redirect()->route('profile', ['user' => 1]);

#### Returning A Redirect To A Controller Action

Similarly to generating `RedirectResponse` instances to named routes, you may also generate redirects to [controller actions](/docs/master/controllers):

	return redirect()->action('HomeController@index');

> **Note:** You do not need to specify the full namespace to the controller. Only specify the portion of the controller that comes after the `App\Http\Controllers` portion of the namespace. The root portion namespace will be automatically preprended for you.

#### Returning A Redirect To A Controller Action With Parameters

	return redirect()->action('UserController@profile', [1]);

#### Returning A Redirect To A Controller Action Using Named Parameters

	return redirect()->action('UserController@profile', ['user' => 1]);

<a name="other-responses"></a>
## Other Responses

The `response` helper may be used to conveniently generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/master/contracts) is returned. This contract provides several helpful methods for generating responses.

#### Creating A JSON Response

The `json` method will automatically set the `Content-Type` header to `application/json`:

	return response()->json(['name' => 'Steve', 'state' => 'CA']);

#### Creating A JSONP Response

	return response()->json(['name' => 'Steve', 'state' => 'CA'])
	                 ->setCallback($request->input('callback'));

#### Creating A File Download Response

	return response()->download($pathToFile);

	return response()->download($pathToFile, $name, $headers);

> **Note:** Symfony HttpFoundation, which manages file downloads, requires the file being downloaded to have an ASCII file name.

<a name="response-macros"></a>
## Response Macros

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on an implementation of `Illuminate\Contracts\Routing\ResponseFactory`.

For example, from a [service provider's](/docs/master/providers) `boot` method:

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;
	use Illuminate\Contracts\Routing\ResponseFactory;

	class ResponseMacroServiceProvider extends ServiceProvider {

		/**
		 * Perform post-registration booting of services.
		 *
		 * @param  ResponseFactory  $events
		 * @return void
		 */
		public function boot(ResponseFactory $response)
		{
			$response->macro('caps', function($value) use ($response)
			{
				return $response->make(strtoupper($value));
			});
		}

	}

The `macro` function accepts a name as its first argument, and a Closure as its second. The macro's Closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper:

	return response()->caps('foo');
