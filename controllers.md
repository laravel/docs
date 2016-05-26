# HTTP Controllers

- [Introduction](#introduction)
- [Basic Controllers](#basic-controllers)
- [Controller Middleware](#controller-middleware)
- [RESTful Resource Controllers](#restful-resource-controllers)
    - [Partial Resource Routes](#restful-partial-resource-routes)
    - [Naming Resource Routes](#restful-naming-resource-routes)
    - [Naming Resource Route Parameters](#restful-naming-resource-route-parameters)
    - [Supplementing Resource Controllers](#restful-supplementing-resource-controllers)
- [Dependency Injection & Controllers](#dependency-injection-and-controllers)
- [Route Caching](#route-caching)

<a name="introduction"></a>
## Introduction

Instead of defining all of your request handling logic in a single `routes.php` file, you may wish to organize this behavior using Controller classes. Controllers can group related HTTP request handling logic into a class. Controllers are stored in the `app/Http/Controllers` directory.

<a name="basic-controllers"></a>
## Basic Controllers

Here is an example of a basic controller class. All Laravel controllers should extend the base controller class included with the default Laravel installation:

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            return view('user.profile', ['user' => User::findOrFail($id)]);
        }
    }

We can route to the controller action like so:

    Route::get('user/{id}', 'UserController@showProfile');

Now, when a request matches the specified route URI, the `showProfile` method on the `UserController` class will be executed. Of course, the route parameters will also be passed to the method.

#### Controllers & Namespaces

It is very important to note that we did not need to specify the full controller namespace when defining the controller route. We only defined the portion of the class name that comes after the `App\Http\Controllers` namespace "root". By default, the `RouteServiceProvider` will load the `routes.php` file within a route group containing the root controller namespace.

If you choose to nest or organize your controllers using PHP namespaces deeper into the `App\Http\Controllers` directory, simply use the specific class name relative to the `App\Http\Controllers` root namespace. So, if your full controller class is `App\Http\Controllers\Photos\AdminController`, you would register a route like so:

    Route::get('foo', 'Photos\AdminController@method');

#### Naming Controller Routes

Like Closure routes, you may specify names on controller routes:

    Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

You may also use the `route` helper to generate a URL to a named controller route:

    $url = route('name');

<a name="controller-middleware"></a>
## Controller Middleware

[Middleware](/docs/{{version}}/middleware) may be assigned to the controller's routes like so:

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'UserController@showProfile'
    ]);

However, it is more convenient to specify middleware within your controller's constructor. Using the `middleware` method from your controller's constructor, you may easily assign middleware to the controller. You may even restrict the middleware to only certain methods on the controller class:

    class UserController extends Controller
    {
        /**
         * Instantiate a new UserController instance.
         *
         * @return void
         */
        public function __construct()
        {
            $this->middleware('auth');

            $this->middleware('log', ['only' => [
                'fooAction',
                'barAction',
            ]]);

            $this->middleware('subscribed', ['except' => [
                'fooAction',
                'barAction',
            ]]);
        }
    }

<a name="restful-resource-controllers"></a>
## RESTful Resource Controllers

Resource controllers make it painless to build RESTful controllers around resources. For example, you may wish to create a controller that handles HTTP requests regarding "photos" stored by your application. Using the `make:controller` Artisan command, we can quickly create such a controller:

    php artisan make:controller PhotoController --resource

The Artisan command will generate a controller file at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations.

Next, you may register a resourceful route to the controller:

    Route::resource('photo', 'PhotoController');

This single route declaration creates multiple routes to handle a variety of RESTful actions on the photo resource. Likewise, the generated controller will already have methods stubbed for each of these actions, including notes informing you which URIs and verbs they handle.

#### Actions Handled By Resource Controller

Verb      | Path                  | Action       | Route Name
----------|-----------------------|--------------|---------------------
GET       | `/photo`              | index        | photo.index
GET       | `/photo/create`       | create       | photo.create
POST      | `/photo`              | store        | photo.store
GET       | `/photo/{photo}`      | show         | photo.show
GET       | `/photo/{photo}/edit` | edit         | photo.edit
PUT/PATCH | `/photo/{photo}`      | update       | photo.update
DELETE    | `/photo/{photo}`      | destroy      | photo.destroy

Remember, since HTML forms can't make PUT, PATCH, or DELETE requests, you will need to add a hidden `_method` field to spoof these HTTP verbs:

    <input type="hidden" name="_method" value="PUT">

<a name="restful-partial-resource-routes"></a>
#### Partial Resource Routes

When declaring a resource route, you may specify a subset of actions to handle on the route:

    Route::resource('photo', 'PhotoController', ['only' => [
        'index', 'show'
    ]]);

    Route::resource('photo', 'PhotoController', ['except' => [
        'create', 'store', 'update', 'destroy'
    ]]);

<a name="restful-naming-resource-routes"></a>
#### Naming Resource Routes

By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your options:

    Route::resource('photo', 'PhotoController', ['names' => [
        'create' => 'photo.build'
    ]]);

<a name="restful-naming-resource-route-parameters"></a>
#### Naming Resource Route Parameters

By default, `Route::resource` will create the route parameters for your resource routes based on the resource name. You can easily override this on a per resource basis by passing `parameters` in the options array. The `parameters` array should be an associative array of resource names and parameter names:

    Route::resource('user', 'AdminUserController', ['parameters' => [
        'user' => 'admin_user'
    ]]);

 The example above generates the following URIs for the resource's `show` route:

    /user/{admin_user}

Instead of passing an array of parameter names, you may also simply pass the word `singular` to instruct Laravel to use the default parameter names, but "singularize" them:

    Route::resource('users.photos', 'PhotoController', [
        'parameters' => 'singular'
    ]);

    // /users/{user}/photos/{photo}

Alternatively, you may set your resource route parameters to be globally singular or set a global mapping for your resource parameter names:

    Route::singularResourceParameters();

    Route::resourceParameters([
        'user' => 'person', 'photo' => 'image'
    ]);

When customizing resource parameters, it's important to keep the naming priority in mind:

1. The parameters explicitly passed to `Route::resource`.
2. The global parameter mappings set via `Route::resourceParameters`.
3. The `singular` setting passed via the `parameters` array to `Route::resource` or set via `Route::singularResourceParameters`.
4. The default behavior.

<a name="restful-supplementing-resource-controllers"></a>
#### Supplementing Resource Controllers

If it becomes necessary to add additional routes to a resource controller beyond the default resource routes, you should define those routes before your call to `Route::resource`; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes:

    Route::get('photos/popular', 'PhotoController@method');

    Route::resource('photos', 'PhotoController');

<a name="dependency-injection-and-controllers"></a>
## Dependency Injection & Controllers

#### Constructor Injection

The Laravel [service container](/docs/{{version}}/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The dependencies will automatically be resolved and injected into the controller instance:

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * The user repository instance.
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }
    }

Of course, you may also type-hint any [Laravel contract](/docs/{{version}}/contracts). If the container can resolve it, you can type-hint it.

#### Method Injection

In addition to constructor injection, you may also type-hint dependencies on your controller's action methods. For example, let's type-hint the `Illuminate\Http\Request` instance on one of our methods:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Store a new user.
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $name = $request->input('name');

            //
        }
    }

If your controller method is also expecting input from a route parameter, simply list your route arguments after your other dependencies. For example, if your route is defined like so:

    Route::put('user/{id}', 'UserController@update');

You may still type-hint the `Illuminate\Http\Request` and access your route parameter `id` by defining your controller method like the following:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Update the specified user.
         *
         * @param  Request  $request
         * @param  string  $id
         * @return Response
         */
        public function update(Request $request, $id)
        {
            //
        }
    }

<a name="route-caching"></a>
## Route Caching

> **Note:** Route caching does not work with Closure based routes. To use route caching, you must convert any Closure routes to use controller classes.

If your application is exclusively using controller based routes, you should take advantage of Laravel's route cache. Using the route cache will drastically decrease the amount of time it takes to register all of your application's routes. In some cases, your route registration may even be up to 100x faster! To generate a route cache, just execute the `route:cache` Artisan command:

    php artisan route:cache

That's all there is to it! Your cached routes file will now be used instead of your `app/Http/routes.php` file. Remember, if you add any new routes you will need to generate a fresh route cache. Because of this, you should only run the `route:cache` command during your project's deployment.

To remove the cached routes file without generating a new cache, use the `route:clear` command:

    php artisan route:clear
