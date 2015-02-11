# Views & Responses

- [Basic Responses](#basic-responses)
- [Redirects](#redirects)
- [Views](#views)
- [View Composers](#view-composers)
- [Special Responses](#special-responses)
- [Response Macros](#response-macros)

<a name="basic-responses"></a>
## Basic Responses

#### Returning Strings From Routes

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### Creating Custom Responses

A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, providing a variety of methods for building HTTP responses.

	$response = Response::make($contents, $statusCode);

	$response->header('Content-Type', $value);

	return $response;

If you need access to the `Response` class methods, but want to return a view as the response content, you may use the `Response::view` method for convenience:

	return Response::view('hello')->header('Content-Type', $type);

#### Attaching Cookies To Responses

	$cookie = Cookie::make('name', 'value');

	return Response::make($content)->withCookie($cookie);

<a name="redirects"></a>
## Redirects

#### Returning A Redirect

	return Redirect::to('user/login');

#### Returning A Redirect With Flash Data

	return Redirect::to('user/login')->with('message', 'Login Failed');

> **Note:** Since the `with` method flashes data to the session, you may retrieve the data using the typical `Session::get` method.

#### Returning A Redirect To A Named Route

	return Redirect::route('login');

#### Returning A Redirect To A Named Route With Parameters

	return Redirect::route('profile', array(1));

#### Returning A Redirect To A Named Route Using Named Parameters

	return Redirect::route('profile', array('user' => 1));

#### Returning A Redirect To A Controller Action

	return Redirect::action('HomeController@index');

#### Returning A Redirect To A Controller Action With Parameters

	return Redirect::action('UserController@profile', array(1));

#### Returning A Redirect To A Controller Action Using Named Parameters

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

#### Passing Data To Views

	// Using conventional approach
	$view = View::make('greeting')->with('name', 'Steve');

	// Using Magic Methods
	$view = View::make('greeting')->withName('steve');

In the example above the variable `$name` would be accessible from the view, and would contain `Steve`.

If you wish, you may pass an array of data as the second parameter given to the `make` method:

	$view = View::make('greetings', $data);

You may also share a piece of data across all views:

	View::share('name', 'Steve');

#### Passing A Sub-View To A View

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

#### Determining If A View Exists

If you need to check if a view exists, use the `View::exists` method:

	if (View::exists('emails.customer'))
	{
		//
	}

<a name="view-composers"></a>
## View Composers

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want bound to a given view each time that view is rendered throughout your application, a view composer can organize that code into a single location. Therefore, view composers may function like "view models" or "presenters".

#### Defining A View Composer

	View::composer('profile', function($view)
	{
		$view->with('count', User::count());
	});

Now each time the `profile` view is rendered, the `count` data will be bound to the view.

You may also attach a view composer to multiple views at once:

    View::composer(array('profile','dashboard'), function($view)
    {
        $view->with('count', User::count());
    });

If you would rather use a class based composer, which will provide the benefits of being resolved through the application [IoC Container](/docs/4.2/ioc), you may do so:

	View::composer('profile', 'ProfileComposer');

A view composer class should be defined like so:

	class ProfileComposer {

		public function compose($view)
		{
			$view->with('count', User::count());
		}

	}

#### Defining Multiple Composers

You may use the `composers` method to register a group of composers at the same time:

	View::composers(array(
		'AdminComposer' => array('admin.index', 'admin.profile'),
		'UserComposer' => 'user',
		'ProductComposer@create' => 'product'
	));

> **Note:** There is no convention on where composer classes may be stored. You are free to store them anywhere as long as they can be autoloaded using the directives in your `composer.json` file.

### View Creators

View **creators** work almost exactly like view composers; however, they are fired immediately when the view is instantiated. To register a view creator, simply use the `creator` method:

	View::creator('profile', function($view)
	{
		$view->with('count', User::count());
	});

<a name="special-responses"></a>
## Special Responses

#### Creating A JSON Response

	return Response::json(array('name' => 'Steve', 'state' => 'CA'));

#### Creating A JSONP Response

	return Response::json(array('name' => 'Steve', 'state' => 'CA'))->setCallback(Input::get('callback'));

#### Creating A File Download Response

	return Response::download($pathToFile);

	return Response::download($pathToFile, $name, $headers);

> **Note:** Symfony HttpFoundation, which manages file downloads, requires the file being downloaded to have an ASCII file name.

<a name="response-macros"></a>
## Response Macros

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `Response::macro` method:

	Response::macro('caps', function($value)
	{
		return Response::make(strtoupper($value));
	});

The `macro` function accepts a name as its first argument, and a Closure as its second. The macro's Closure will be executed when calling the macro name on the `Response` class:

	return Response::caps('foo');

You may define your macros in one of your `app/start` files. Alternatively, you may organize your macros into a separate file which is included from one of your `start` files.
