# Views & Responses

- [Basic Responses](#basic-responses)
- [Redirects](#redirects)
- [Views](#views)
- [View Composers](#view-composers)
- [Special Responses](#special-responses)

<a name="basic-responses"></a>
## Basic Responses

<a name="returning-strings-from-routes"></a>
**Returning Strings From Routes**

	Route::get('/', function()
	{
		return 'Hello World';
	});

<a name="creating-custom-responses"></a>
**Creating Custom Responses**

A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, providing a variety of methods for building HTTP responses.

	$response = Response::make($contents, $statusCode);

	$response->header('Content-Type', $value);

	return $response;

<a name="attaching-cookies-to-responses"></a>
**Attaching Cookies To Responses**

	$cookie = Cookie::make('name', 'value');

	return Response::make($content)->withCookie($cookie);

<a name="redirects"></a>
## Redirects

<a name="returning-a-redirect"></a>
**Returning A Redirect**

	return Redirect::to('user/login');

<a name="returning-a-redirect-to-a-named-route"></a>
**Returning A Redirect To A Named Route**

	return Redirect::route('login');

<a name="returning-a-redirect-to-a-named-route-with-parameters"></a>
**Returning A Redirect To A Named Route With Parameters**

	return Redirect::route('profile', array(1));

<a name="returning-a-redirect-to-a-named-route-using-named-parameters"></a>
**Returning A Redirect To A Named Route Using Named Parameters**

	return Redirect::route('profile', array('user' => 1));

<a name="returning-a-redirect-to-a-controller-action"></a>
**Returning A Redirect To A Controller Action**

	return Redirect::action('HomeController@index');

<a name="returning-a-redirect-to-a-controller-action-with-parameters"></a>
**Returning A Redirect To A Controller Action With Parameters**

	return Redirect::action('UserController@profile', array(1));

<a name="returning-a-redirect-to-a-controller-action-using-named-parameters"></a>
**Returning A Redirect To A Controller Action Using Named Parameters**

	return Redirect::action('UserController@profile', array('user' => 1));

<a name="views"></a>
## Views

Views typically contain the HTML of your application and provide a convenient way of separating your controller and domain logic from your presentation logic. Views are stored in the `app/views` directory.

A simple view could look something like this:

	<!-- View stored in app/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

This view may be returned to the browser like so:

	Route::get('/', function()
	{
		return View::make('greeting', array('name' => 'Taylor'));
	});

The second argument passed to `View::make` is an array of data that should be made available to the view.

<a name="passing-data-to-views"></a>
**Passing Data To Views**

	$view = View::make('greeting', $data);

	$view = View::make('greeting')->with('name', 'Steve');

In the example above the variable `$name` would be accessible from the view, and would contain `Steve`.

You may also share a piece of data across all views:

	View::share('name', 'Steve');

<a name="passing-a-sub-view-to-a-view"></a>
**Passing A Sub-View To A View**

Sometimes you may wish to pass a view into another view. For example, given a sub-view stored at `app/views/child/view.php`, we could pass it to another view like so:

	$view = View::make('greeting')->nest('child', 'child.view');

	$view = View::make('greeting')->nest('child', 'child.view', $data);

The sub-view can then be rendered from the parent view:

	<html>
		<body>
			<h1>Hello!</h1>
			<?php echo $child; ?>
		</body>
	</html>

<a name="view-composers"></a>
## View Composers

View composers are callbacks or class methods that are called when a view is created. If you have data that you want bound to a given view each time that view is created throughout your application, a view composer can organize that code into a single location. Therefore, view composers may function like "view models" or "presenters".

<a name="defining-a-view-composer"></a>
**Defining A View Composer**

	View::composer('profile', function($view)
	{
		$view->with('count', User::count());
	});

Now each time the `profile` view is created, the `count` data will be bound to the view.

You may also attach a view composer to multiple views at once:

    View::composer(array('profile','dashboard'), function($view)
    {
        $view->with('count', User::count());
    });

If you would rather use a class based composer, which will provide the benefits of being resolved through the application [IoC Container](/docs/ioc), you may do so:

	View::composer('profile', 'ProfileComposer');

A view composer class should be defined like so:

	class ProfileComposer {

		public function compose($view)
		{
			$view->with('count', User::count());
		}

	}

Note that there is no convention on where composer classes may be stored. You are free to store them anywhere as long as they can be autoloaded using the directives in your `composer.json` file.

<a name="special-responses"></a>
## Special Responses

<a name="creating-a-json-response"></a>
**Creating A JSON Response**

	return Response::json(array('name' => 'Steve', 'state' => 'CA'));

<a name="creating-a-jsonp-response"></a>
**Creating A JSONP Response**

	return Response::json(array('name' => 'Steve', 'state' => 'CA'))->setCallback(Input::get('callback'));

<a name="creating-a-file-download-response"></a>
**Creating A File Download Response**

	return Response::download($pathToFile);

	return Response::download($pathToFile, $name, $headers);
