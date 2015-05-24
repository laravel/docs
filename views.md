# Views

- [Basic Usage](#basic-usage)
- [View Composers](#view-composers)

<a name="basic-usage"></a>
## Basic Usage

Views contain the HTML served by your application, and serve as a convenient method of separating your controller and domain logic from your presentation logic. Views are stored in the `resources/views` directory.

A simple view looks like this:

	<!-- View stored in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

The view may be returned to the browser like so:

	Route::get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument passed to helper is an array of data that should be made available to the view.

Of course, views may also be nested within sub-directories of the `resources/views` directory. For example, if your view is stored at `resources/views/admin/profile.php`, it should be returned like so:

	return view('admin.profile', $data);

#### Passing Data To Views

	// Using conventional approach
	$view = view('greeting')->with('name', 'Victoria');

	// Using Magic Methods
	$view = view('greeting')->withName('Victoria');

In the example above, the variable `$name` is made accessible to the view and contains `Victoria`.

If you wish, you may pass an array of data as the second parameter to the `view` helper:

	$view = view('greetings', $data);

When passing information in this manner, `$data` should be an array with key/value pairs. Inside your view, you can then access each value using it's corresponding key, like `{{ $key }}` (assuming `$data['key']` exists).

#### Sharing Data With All Views

Occasionally, you may need to share a piece of data with all views that are rendered by your application. You have several options: the `view` helper, the `Illuminate\Contracts\View\Factory` [contract](/docs/{{version}}/contracts), or a wildcard [view composer](#view-composers).

For example, using the `view` helper:

	view()->share('data', [1, 2, 3]);

You may also use the `View` facade:

	View::share('data', [1, 2, 3]);

Typically, you would place calls to the `share` method within a service provider's `boot` method. You are free to add them to the `AppServiceProvider` or generate a separate service provider to house them.

> **Note:** When the `view` helper is called without arguments, it returns an implementation of the `Illuminate\Contracts\View\Factory` contract.

#### Determining If A View Exists

If you need to determine if a view exists, you may use the `exists` method:

	if (view()->exists('emails.customer'))
	{
		//
	}

#### Returning A View From A File Path

If you wish, you may generate a view from a fully-qualified file path:

	return view()->file($pathToFile, $data);

<a name="view-composers"></a>
## View Composers

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer organizes that logic into a single location.

#### Defining A View Composer

Let's organize our view composers within a [service provider](/docs/{{version}}/providers). We'll use the `View` facade to access the underlying `Illuminate\Contracts\View\Factory` contract implementation:

	<?php namespace App\Providers;

	use View;
	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider {

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot()
		{
			// Using class based composers...
			View::composer('profile', 'App\Http\ViewComposers\ProfileComposer');

			// Using Closure based composers...
			View::composer('dashboard', function($view)
			{

			});
		}

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}

	}

> **Note:** Laravel does not include a default directory for view composers. You are free to organize them however you wish. For example, you could create an `App\Http\ViewComposers` directory.

Remember, you will need to add the service provider to the `providers` array in the `config/app.php` configuration file.

Now that we have registered the composer, the `ProfileComposer@compose` method will be executed each time the `profile` view is being rendered. So, let's define the composer class:

	<?php namespace App\Http\ViewComposers;

	use Illuminate\Contracts\View\View;
	use Illuminate\Users\Repository as UserRepository;

	class ProfileComposer {

		/**
		 * The user repository implementation.
		 *
		 * @var UserRepository
		 */
		protected $users;

		/**
		 * Create a new profile composer.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			// Dependencies automatically resolved by service container...
			$this->users = $users;
		}

		/**
		 * Bind data to the view.
		 *
		 * @param  View  $view
		 * @return void
		 */
		public function compose(View $view)
		{
			$view->with('count', $this->users->count());
		}

	}

Just before the view is rendered, the composer's `compose` method is called with the `Illuminate\Contracts\View\View` instance. You may use the `with` method to bind data to the view.

> **Note:** All view composers are resolved via the [service container](/docs/{{version}}/container), so you may type-hint any dependencies you need within a composer's constructor.

#### Wildcard View Composers

The `composer` method accepts the `*` character as a wildcard, so you may attach a composer to all views like so:

	View::composer('*', function($view)
	{
		//
	});

#### Attaching A Composer To Multiple Views

You may also attach a view composer to multiple views at once:

	View::composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### Defining Multiple Composers

You may use the `composers` method to register a group of composers at the same time:

	View::composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

### View Creators

View **creators** work almost exactly like view composers; however, they are fired immediately when the view is instantiated. To register a view creator, use the `creator` method:

	View::creator('profile', 'App\Http\ViewCreators\ProfileCreator');
