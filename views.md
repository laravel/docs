# Views / Blade Templating

- [Basic Usage](#basic-usage)
	- [Passing Data To Views](#passing-data-to-views)
	- [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
- [Blade Templating](#blade-templating)
	- [Blade Control Structures](#blade-control-structures)
	- [Blade Service Injection](#blade-service-injection)
	- [Extending Blade](#extending-blade)

<a name="basic-usage"></a>
## Basic Usage

Views contain the HTML served by your application, and serve as a convenient method of separating your controller and application logic from your presentation logic. Views are stored in the `resources/views` directory.

A simple view looks like this:

	<!-- View stored in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

The view may be returned to the browser like so:

	Route::get('/', function ()	{
		return view('greeting', ['name' => 'James']);
	});

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument passed to helper is an array of data that should be made available to the view.

Of course, views may also be nested within sub-directories of the `resources/views` directory. For example, if your view is stored at `resources/views/admin/profile.php`, it should be returned like so:

	return view('admin.profile', $data);

#### Determining If A View Exists

If you need to determine if a view exists, you may use the `exists` method. This method will return `true` if the view exists on disk:

	if (view()->exists('emails.customer')) {
		//
	}

<a name="view-data"></a>
### View Data

<a name="passing-data-to-views"></a>
#### Passing Data To Views

As you saw in the previous examples, you may easily pass an array of data to views:

	return view('greetings', ['name' => 'Victoria']);

When passing information in this manner, `$data` should be an array with key/value pairs. Inside your view, you can then access each value using it's corresponding key, like `{{ $key }}` (assuming `$data['key']` exists). The view can then access that data to display it within its HTML. In addition to passing an array of data as the second argument to the `view` function, you may also use the `with` method to add individual pieces of data to the view:

	$view = view('greeting')->with('name', 'Victoria');

In the example above, the variable `$name` is made accessible to the view and contains the string `Victoria`.

<a name="sharing-data-with-all-views"></a>
#### Sharing Data With All Views

Occasionally, you may need to share a piece of data with all views that are rendered by your application. You may do so using the `share` method. Typically, you would place calls to the `share` method within a service provider's `boot` method. You are free to add them to the `AppServiceProvider` or generate a separate service provider to house them.

When the `view` helper is called without arguments, it returns an implementation of the `Illuminate\Contracts\View\Factory` [contract](/docs/{{version}}/contracts), allowing us to call additional methods like `share`:

	<?php namespace App\Providers;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			view()->share('key', 'value');
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

<a name="view-composers"></a>
## View Composers

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer organizes that logic into a single location.

Let's organize our view composers within a [service provider](/docs/{{version}}/providers). We'll use the `view` helper to access the underlying `Illuminate\Contracts\View\Factory` contract implementation:

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider
	{
		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot()
		{
			// Using class based composers...
			view()->composer('profile', 'App\Http\ViewComposers\ProfileComposer');

			// Using Closure based composers...
			view()->composer('dashboard', function ($view) {

			});
		}

		/**
		 * Register
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

	class ProfileComposer
	{
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

#### Attaching A Composer To Multiple Views

You may attach a view composer to multiple views at once by passing an array of views as the first argument to the `composer` method:

	view()->composer(
		['profile', 'dashboard'],
		'App\Http\ViewComposers\MyViewComposer'
	);

The `composer` method accepts the `*` character as a wildcard, allowing you to attach a composer to all views:

	view()->composer('*', function ($view) {
		//
	});

### View Creators

View **creators** are very similar to view composers; however, they are fired immediately when the view is instantiated instead of waiting until the view is about to render. To register a view creator, use the `creator` method:

	view()->creator('profile', 'App\Http\ViewCreators\ProfileCreator');

<a name="blade-templating"></a>
## Blade Templating

Blade is the simple, yet powerful templating engine provided with Laravel. The core benefits of Blade are _template inheritance_ and _sections_. All Blade template files should use the `.blade.php` extension, and are typically stored in `resources/views`.

#### Defining A Blade Layout

Let's take a look at a simple Blade templating example. First, we will examine a "master" template. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view.

	<!-- Stored in resources/views/layouts/master.blade.php -->

	<html>
		<head>
			<title>App Name - @yield('title')</title>
		</head>
		<body>
			@section('sidebar')
				This is the master sidebar.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

#### Using A Blade Layout

Once we have defined our template, we can use the Blade `@extends` directive to inject content into this template from a "child" page of our application.

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

Note that views which `extend` a Blade layout simply override sections from the layout. Content of the layout can be included in a child view using the `@@parent` directive in a section, allowing you to append to the contents of a layout section such as a sidebar or footer.

#### Default Yield Content

Sometimes, such as when you are not sure if a section has been defined, you may wish to pass a default value to the `@yield` directive. You may pass the default value as the second argument:

	@yield('section', 'Default Content')

<a name="other-blade-control-structures"></a>
## Other Blade Control Structures

#### Echoing Data

	Hello, {{ $name }}.

	The current UNIX timestamp is {{ time() }}.

> **Note:** Blade `{{ }}` statements are automatically send through PHP's `htmlentities` function to prevent XSS attacks.

#### Echoing Data After Checking For Existence

Sometimes you may wish to echo a variable, but you aren't sure if the variable has been set. Basically, you want to do this:

	{{ isset($name) ? $name : 'Default' }}

However, instead of writing a ternary statement, Blade allows you to use the following convenient short-cut:

	{{ $name or 'Default' }}

#### Displaying Raw Text With Curly Braces

If you need to display a string that is wrapped in curly braces, you may escape the Blade behavior by prefixing your text with an `@` symbol:

	@{{ This will not be processed by Blade }}

If you don't want the data to be escaped, you may use the following syntax:

	Hello, {!! $name !!}.

> **Note:** Be very careful when echoing content that is supplied by users of your application. Always use the double curly brace syntax to escape any HTML entities in the content.

#### If Statements

	@if (count($records) === 1)
		I have one record!
	@elseif (count($records) > 1)
		I have multiple records!
	@else
		I don't have any records!
	@endif

	@unless (Auth::check())
		You are not signed in.
	@endunless

#### Loops

	@for ($i = 0; $i < 10; $i++)
		The current value is {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>This is user {{ $user->id }}</p>
	@endforeach

	@forelse ($users as $user)
		<li>{{ $user->name }}</li>
	@empty
		<p>No users</p>
	@endforelse

	@while (true)
		<p>I'm looping forever.</p>
	@endwhile

#### Including Sub-Views

	@include('view.name')

You may also pass an array of data to the included view:

	@include('view.name', ['some' => 'data'])

#### Overwriting Sections

To overwrite a section entirely, you may use the `overwrite` statement:

	@extends('list.item.container')

	@section('list.item.content')
		<p>This is an item of type {{ $item->type }}</p>
	@overwrite

#### Displaying Language Lines

	@lang('language.line')

	@choice('language.line', 1)

#### Comments

	{{-- This comment will not be in the rendered HTML --}}

<a name="blade-service-injection"></a>
### Blade Service Injection

The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/{{version}}/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class / interface name of the service you wish to resolve:

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
	</div>

<a name="extending-blade"></a>
### Extending Blade

Blade even allows you to define your own custom directives. You can use the `directive` method to register a directive. When the Blade compiler encounters the directive, it calls the provided callback with its parameter. This allows you to replace your directives with any logic as complex as you want.

The following example creates a `@datetime($var)` directive which formats a given `$var`:

	Blade::directive('datetime', function($expression) {
		return "<?php echo with{$expression}->format('m/d/Y H:i'); ?>";
	});

The final PHP executed by this directive will be:

	<?php echo with($var)->format('m/d/Y H:i'); ?>

