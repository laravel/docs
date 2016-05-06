# Views

- [Basic Usage](#basic-usage)
    - [Passing Data To Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)

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

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument passed to helper is an array of data that should be made available to the view. In this case, we are passing the `name` variable, which is displayed in the view by executing `echo` on the variable.

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

When passing information in this manner, `$data` should be an array with key/value pairs. Inside your view, you can then access each value using its corresponding key, such as `<?php echo $key; ?>`. As an alternative to passing a complete array of data to the `view` helper function, you may use the `with` method to add individual pieces of data to the view:

    return view('greeting')->with('name', 'Victoria');

<a name="sharing-data-with-all-views"></a>
#### Sharing Data With All Views

Occasionally, you may need to share a piece of data with all views that are rendered by your application. You may do so using the view factory's `share` method. Typically, you should place calls to `share` within a service provider's `boot` method. You are free to add them to the `AppServiceProvider` or generate a separate service provider to house them:

    <?php

    namespace App\Providers;

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

    <?php

    namespace App\Providers;

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
                //
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

    <?php

    namespace App\Http\ViewComposers;

    use Illuminate\View\View;
    use App\Repositories\UserRepository;

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

Just before the view is rendered, the composer's `compose` method is called with the `Illuminate\View\View` instance. You may use the `with` method to bind data to the view.

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
