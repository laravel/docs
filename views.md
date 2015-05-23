# Views / Blade Templating

- [Basic Usage](#basic-usage)
	- [Passing Data To Views](#passing-data-to-views)
	- [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
- [Blade Templating](#blade-templating)
	- [Template Inheritance](#blade-template-inheritance)
	- [Displaying Data](#blade-displaying-data)
	- [Control Structures](#blade-control-structures)
	- [Service Injection](#blade-service-injection)
	- [Extending Blade](#extending-blade)

<a name="basic-usage"></a>
## Basic Usage

Views contain the HTML served by your application and separate your controller / application logic from your presentation logic. Views are stored in the `resources/views` directory.

A simple view might look something like this:

	<!-- View stored in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

Since this view is stored at `resources/views/greeting.php`, we may return it using the global `view` helper function like so:

	Route::get('/', function ()	{
		return view('greeting', ['name' => 'James']);
	});

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument passed to helper is an array of data that should be made available to the view. In this case, we are passing the `name` variable, which is displayed in the view by simply executing `echo` on the variable.

Of course, views may also be nested within sub-directories of the `resources/views` directory. "Dot" notation may be used to reference nested views. For example, if your view is stored at `resources/views/admin/profile.php`, you may reference it like so:

	return view('admin.profile', $data);

#### Determining If A View Exists

If you need to determine if a view exists, you may use the `exists` method after calling the `view` helper with no arguments. This method will return `true` if the view exists on disk:

	if (view()->exists('emails.customer')) {
		//
	}

When the `view` helper is called without arguments, an instance of `Illuminate\Contracts\View\Factory` is returned, giving you access to any of the factory's methods.

<a name="view-data"></a>
### View Data

<a name="passing-data-to-views"></a>
#### Passing Data To Views

As you saw in the previous examples, you may easily pass an array of data to views:

	return view('greetings', ['name' => 'Victoria']);

When passing information in this manner, `$data` should be an array with key/value pairs. Inside your view, you can then access each value using it's corresponding key, such as `<?php echo $key; ?>`. As an alternative to passing a complete array of data to the `view` helper function, you may use the `with` method to add individual pieces of data to the view:

	$view = view('greeting')->with('name', 'Victoria');

<a name="sharing-data-with-all-views"></a>
#### Sharing Data With All Views

Occasionally, you may need to share a piece of data with all views that are rendered by your application. You may do so using the view factory's `share` method. Typically, you would place calls to `share` within a service provider's `boot` method. You are free to add them to the `AppServiceProvider` or generate a separate service provider to house them:

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

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer can help you organize that logic into a single location.

Let's register our view composers within a [service provider](/docs/{{version}}/providers). We'll use the `view` helper to access the underlying `Illuminate\Contracts\View\Factory` contract implementation. Remember, Laravel does not include a default directory for view composers. You are free to organize them however you wish. For example, you could create an `App\Http\ViewComposers` directory:

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
			view()->composer(
				'profile', 'App\Http\ViewComposers\ProfileComposer'
			);

			// Using Closure based composers...
			view()->composer('dashboard', function ($view) {

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

Remember, if you create a new service provider to contain your view composer registrations, you will need to add the service provider to the `providers` array in the `config/app.php` configuration file.

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

Blade is the simple, yet powerful templating engine provided with Laravel. Unlike other popular PHP templating engines, Blade does not restrict you from using plain PHP code in your views. All Blade views are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade view files use the `.blade.php` file extension and are typically stored in the `resources/views` directory.

<a name="blade-template-inheritance"></a>
### Template Inheritance

#### Defining A Layout

Two of the primary benefits of using Blade are _template inheritance_ and _sections_. To get started, let's take a look at a simple example. First, we will examine a "master" page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view:

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

As you can see, this file contains typical HTML mark-up. However, take note of the `@section` and `@yield` directives. The `@section` directive, as the name implies, defines a section of content, while the `@yield` directive is used to display the contents of a given section.

Now that we have defined a layout for our application, let's define a child page that inherits the layout.

#### Extending A Layout

When defining a child page, you may use the Blade `@extends` directive to specify which layout the child page should "inherit". Views which `@extend` a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`:

	<!-- Stored in resources/views/layouts/child.blade.php -->

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered.

Of course, just like plain PHP views, Blade views may be returned from routes using the global `view` helper function:

	Route::get('blade', function () {
		return view('child');
	});

<a name="blade-displaying-data"></a>
### Displaying Data

You may display data passed to your Blade views by wrapping the variable in "curly" braces. For example, given the following route:

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

You may display the contents of the `name` variable like so:

	Hello, {{ $name }}.

Of course, you are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement:

	The current UNIX timestamp is {{ time() }}.

> **Note:** Blade `{{ }}` statements are automatically send through PHP's `htmlentities` function to prevent XSS attacks.

#### Blade & JavaScript Frameworks

Since many JavaScript frameworks also use "curly" braces to indicate a given expression  should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example:

	<h1>Laravel</h1>

	Hello, @{{ name }}.

In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to instead by rendered by your JavaScript framework.

#### Echoing Data If It Exists

Sometimes you may wish to echo a variable, but you aren't sure if the variable has been set. We can express this in verbose PHP code like so:

	{{ isset($name) ? $name : 'Default' }}

However, instead of writing a ternary statement, Blade provides you with the following convenient short-cut:

	{{ $name or 'Default' }}

In this example, if the `$name` variable exists, its value will be displayed. However, if it does not exists, the word `Default` will be displayed.

#### Displaying Unescaped Data

By default, Blade `{{ }}` statements are automatically send through PHP's `htmlentities` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax:

	Hello, {!! $name !!}.

> **Note:** Be very careful when echoing content that is supplied by users of your application. Always use the double curly brace syntax to escape any HTML entities in the content.

<a name="blade-control-structures"></a>
### Control Structures

In addition to template inheritance and displaying data, Blade also provides convenient short-cuts for common PHP control structures, such as conditional statements and loops. These short-cuts provide a very clean, terse way of working with PHP control structures, while also remaining familiar to their PHP counterparts.

#### If Statements

You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts:

	@if (count($records) === 1)
		I have one record!
	@elseif (count($records) > 1)
		I have multiple records!
	@else
		I don't have any records!
	@endif

For convenience, Blade also provides an `@unless` directive:

	@unless (Auth::check())
		You are not signed in.
	@endunless

#### Loops

In addition to conditional statements, Blade provides simple directives for working with PHP's supported loop structures. Again, each of these directives functions identically to their PHP counterparts:

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

Blade's `@include` directive, allows you to easily include a Blade view from within an existing view. All variables that are available to the parent view will be made available to the included view:

	<div>
		@include('shared.errors')

		<form>
			<!-- Form Contents -->
		</form>
	</div>

Even though the included view will inherit all data available in the parent view, you may also pass an array of extra data to the included view:

	@include('view.name', ['some' => 'data'])

#### Comments

Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application:

	{{-- This comment will not be present in the rendered HTML --}}

<a name="blade-service-injection"></a>
### Service Injection

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

As you can see, Laravel's `with` helper function was used in this directive. The `with` helper simply returns the object / value it is given, allowing for convenient method chaining. The final PHP generated by this directive will be:

	<?php echo with($var)->format('m/d/Y H:i'); ?>

