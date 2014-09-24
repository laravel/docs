<a name="views"></a>
## Views

Views typically contain the HTML of your application and provide a convenient way of separating your controller and domain logic from your presentation logic. Views are stored in the `resources/views` directory.

A simple view could look something like this:

	<!-- View stored in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

This view may be returned to the browser like so:

	$router->get('/', function()
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

Sometimes you may wish to pass a view into another view. For example, given a sub-view stored at `resources/views/child/view.php`, we could pass it to another view like so:

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

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want bound to a given view each time that view is rendered throughout your application, a view composer can organize that code into a single location. Therefore, view composers may function like "view models" or "presenters". To organize your view composers, you may wish to create a new [service provider](/docs/ioc#service-providers):

#### Defining A View Composer

For example, using the `make:provider` Artisan command, you may wish to create a `ComposerServiceProvider` class, and register your view composers in the `boot` method of that provider:

	public function before()
	{
		View::composer('profile', function($view)
		{
			$view->with('count', User::count());
		});
	}

Now each time the `profile` view is rendered, the `count` data will be bound to the view.

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
