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

This view may be returned to the browser like so:

	$router->get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument passed to helper is an array of data that should be made available to the view.

#### Passing Data To Views

	// Using conventional approach
	$view = view('greeting')->with('name', 'Victoria');

	// Using Magic Methods
	$view = view('greeting')->withName('Victoria');

In the example above the variable `$name` would be accessible from the view, and would contain `Victoria`.

If you wish, you may pass an array of data as the second parameter given to the `make` method:

	$view = view('greetings', $data);

#### Sharing Data With All Views

Occasionally, you may need to share a piece of data with all views that are rendered by your application. You have several options: the `view` helper, the `Illuminate\Contracts\View\Factory` [contract](/docs/master/contracts), or a wildcard [view composer](#view-composers).

First, using the `view` helper:

	view()->share('data', [1, 2, 3]);

> **Note:** When the `view` helper is called without arguments, it returns an implementation of the `Illuminate\Contracts\View\Factory` contract.

Alternatively, obtain an instance of the `Illuminate\Contracts\View\Factory` [contract](/docs/master/contracts). Once you have an implementation of the contract, you may use the `share` method to make data available to all views:

In this example, we'll assume we're sharing the data from within a [global HTTP filter](/docs/master/filters). However, you could also share the data from a service provider, or even a controller:

	<?php namespace App\Http\Filters;

	use Illuminate\Http\Request;
	use Illuminate\Contracts\View\Factory as ViewFactory;

	class TestFilter {

		/**
		 * The view factory implementation.
		 */
		protected $view;

		/**
		 * Create a new filter instance.
		 *
		 * @param  ViewFactory  $view
		 * @return void
		 */
		public function __construct(ViewFactory $view)
		{
			$this->view = $view;
		}

		/**
		 * Run the request filter.
		 *
		 * @param  Request  $request
		 * @return mixed
		 */
		public function filter(Request $request)
		{
			$this->view->share('data', [1, 2, 3]);
		}

	}

#### Determining If A View Exists

If you need to determine if a view exists, you again have two options: the `view` helper and the `Illuminate\Contracts\View\Factory` [contract](/docs/master/contracts):

Using the helper:

	if (view()->exists('emails.customer'))
	{
		//
	}

Alternatively, type-hint the `Illuminate\Contracts\View\Factory` contract and use the `exists` method on the resolved instance:

	<?php namespace App\Services;

	use Illuminate\Contracts\View\Factory as ViewFactory;

	class TaskRunner {

		/**
		 * The view factory implementation.
		 */
		protected $view;

		/**
		 * Create a new class instance.
		 *
		 * @param  ViewFactory  $view
		 * @return void
		 */
		public function __construct(ViewFactory $view)
		{
			$this->view = $view;
		}

		/**
		 * Do some work!
		 *
		 * @return void
		 */
		public function performTask()
		{
			if ($this->view->exists('emails.customer'))
			{
				//
			}
		}

	}


<a name="view-composers"></a>
## View Composers

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want bound to a certain view each time that view is rendered, a view composer can organize that code into a single location.

#### Defining A View Composer

Let's organize our view composers within a [service provider](/docs/master/providers). We'll need an instance of the `Illuminate\Contracts\View\Factory` [contract](/docs/master/contracts), so we'll type-hint that in our provider's `boot` method:

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;
	use Illuminate\Contracts\View\Factory as ViewFactory;

	class ComposerServiceProvider extends ServiceProvider {

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot(ViewFactory $view)
		{
			$view->composer('profile', 'App\Http\ViewComposers\ProfileComposer');
		}

	}

> **Note:** Laravel does not include a default directory for view composers. You are free to organize them however you wish.

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

Just before the view is rendered, the composer's `compose` method is called with the `Illuminate\Contracts\View\View` instance. You may use the `with` method to bind any data to the view.

> **Note:** All view composers are resolved via the [service container](/docs/master/container), so you may type-hint any dependencies you need within a composer's constructor.

#### Wildcard View Composers

View composer registrations accept the `*` character as a wildcard, so you may attach a composer to all views like so:

	$this->view->composer('*', 'App\Http\ViewComposers\GlobalComposer');

#### Attaching A Composer To Multiple Views

You may also attach a view composer to multiple views at once:

	$this->view->composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### Defining Multiple Composers

You may use the `composers` method to register a group of composers at the same time:

	$this->view->composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

> **Note:** There is no convention on where composer classes may be stored. You are free to store them anywhere as long as they can be autoloaded by Composer.

### View Creators

View **creators** work almost exactly like view composers; however, they are fired immediately when the view is instantiated. To register a view creator, use the `creator` method on an `Illuminate\Contracts\View\Factory` instance:

	$this->view->creator('profile', 'App\Http\ViewCreators\ProfileCreator');
