# HTTP Routing

- [Basic Routing](#basic-routing)
- [Route Parameters](#route-parameters)
    - [Required Parameters](#required-parameters)
    - [Optional Parameters](#parameters-optional-parameters)
    - [Regular Expression Constraints](#parameters-regular-expression-constraints)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Namespaces](#route-group-namespaces)
    - [Sub-Domain Routing](#route-group-sub-domain-routing)
    - [Route Prefixes](#route-group-prefixes)
- [CSRF Protection](#csrf-protection)
    - [Introduction](#csrf-introduction)
    - [Excluding URIs](#csrf-excluding-uris)
    - [X-CSRF-Token](#csrf-x-csrf-token)
    - [X-XSRF-Token](#csrf-x-xsrf-token)
- [Route Model Binding](#route-model-binding)
- [Form Method Spoofing](#form-method-spoofing)
- [Accessing The Current Route](#accessing-the-current-route)

<a name="basic-routing"></a>
## Basic Routing

All Laravel routes are defined in the `app/Http/routes.php` file, which is automatically loaded by the framework. The most basic Laravel routes simply accept a URI and a `Closure`, providing a very simple and expressive method of defining routes:

    Route::get('foo', function () {
        return 'Hello World';
    });

#### The Default Routes File

The default `routes.php` file is loaded by the `RouteServiceProvider` and is automatically included in the `web` middleware group, which provides access to session state and CSRF protection. Most of the routes for your application will be defined within this file.

#### Available Router Methods

The router allows you to register routes that respond to any HTTP verb:

    Route::get($uri, $callback);
    Route::post($uri, $callback);
    Route::put($uri, $callback);
    Route::patch($uri, $callback);
    Route::delete($uri, $callback);
    Route::options($uri, $callback);

Sometimes you may need to register a route that responds to multiple HTTP verbs. You may do so using the `match` method. Or, you may even register a route that responds to all HTTP verbs using the `any` method:

    Route::match(['get', 'post'], '/', function () {
        //
    });

    Route::any('foo', function () {
        //
    });

<a name="route-parameters"></a>
## Route Parameters

<a name="required-parameters"></a>
### Required Parameters

Of course, sometimes you will need to capture segments of the URI within your route. For example, you may need to capture a user's ID from the URL. You may do so by defining route parameters:

    Route::get('user/{id}', function ($id) {
        return 'User '.$id;
    });

You may define as many route parameters as required by your route:

    Route::get('posts/{post}/comments/{comment}', function ($postId, $commentId) {
        //
    });

Route parameters are always encased within "curly" braces. The parameters will be passed into your route's `Closure` when the route is executed.

> **Note:** Route parameters cannot contain the `-` character. Use an underscore (`_`) instead.

<a name="parameters-optional-parameters"></a>
### Optional Parameters

Occasionally you may need to specify a route parameter, but make the presence of that route parameter optional. You may do so by placing a `?` mark after the parameter name. Make sure to give the route's corresponding variable a default value:

    Route::get('user/{name?}', function ($name = null) {
        return $name;
    });

    Route::get('user/{name?}', function ($name = 'John') {
        return $name;
    });

<a name="parameters-regular-expression-constraints"></a>
### Regular Expression Constraints

You may constrain the format of your route parameters using the `where` method on a route instance. The `where` method accepts the name of the parameter and a regular expression defining how the parameter should be constrained:

    Route::get('user/{name}', function ($name) {
        //
    })
    ->where('name', '[A-Za-z]+');

    Route::get('user/{id}', function ($id) {
        //
    })
    ->where('id', '[0-9]+');

    Route::get('user/{id}/{name}', function ($id, $name) {
        //
    })
    ->where(['id' => '[0-9]+', 'name' => '[a-z]+']);

<a name="parameters-global-constraints"></a>
#### Global Constraints

If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `boot` method of your `RouteServiceProvider`:

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @param  \Illuminate\Routing\Router  $router
     * @return void
     */
    public function boot(Router $router)
    {
        $router->pattern('id', '[0-9]+');

        parent::boot($router);
    }

Once the pattern has been defined, it is automatically applied to all routes using that parameter name:

    Route::get('user/{id}', function ($id) {
        // Only called if {id} is numeric.
    });

<a name="named-routes"></a>
## Named Routes

Named routes allow the convenient generation of URLs or redirects for specific routes. You may specify a name for a route using the `as` array key when defining the route:

    Route::get('user/profile', ['as' => 'profile', function () {
        //
    }]);

You may also specify route names for controller actions:

    Route::get('user/profile', [
        'as' => 'profile', 'uses' => 'UserController@showProfile'
    ]);

Alternatively, instead of specifying the route name in the route array definition, you may chain the `name` method onto the end of the route definition:

    Route::get('user/profile', 'UserController@showProfile')->name('profile');

#### Route Groups & Named Routes

If you are using [route groups](#route-groups), you may specify an `as` keyword in the route group attribute array, allowing you to set a common route name prefix for all routes within the group:

    Route::group(['as' => 'admin::'], function () {
        Route::get('dashboard', ['as' => 'dashboard', function () {
            // Route named "admin::dashboard"
        }]);
    });

#### Generating URLs To Named Routes

Once you have assigned a name to a given route, you may use the route's name when generating URLs or redirects via the global `route` function:

    // Generating URLs...
    $url = route('profile');

    // Generating Redirects...
    return redirect()->route('profile');

If the named route defines parameters, you may pass the parameters as the second argument to the `route` function. The given parameters will automatically be inserted into the URL in their correct positions:

    Route::get('user/{id}/profile', ['as' => 'profile', function ($id) {
        //
    }]);

    $url = route('profile', ['id' => 1]);

<a name="route-groups"></a>
## Route Groups

Route groups allow you to share route attributes, such as middleware or namespaces, across a large number of routes without needing to define those attributes on each individual route. Shared attributes are specified in an array format as the first parameter to the `Route::group` method.

To learn more about route groups, we'll walk through several common use-cases for the feature.

<a name="route-group-middleware"></a>
### Middleware

To assign middleware to all routes within a group, you may use the `middleware` key in the group attribute array. Middleware will be executed in the order you define this array:

    Route::group(['middleware' => 'auth'], function () {
        Route::get('/', function ()    {
            // Uses Auth Middleware
        });

        Route::get('user/profile', function () {
            // Uses Auth Middleware
        });
    });

<a name="route-group-namespaces"></a>
### Namespaces

Another common use-case for route groups is assigning the same PHP namespace to a group of controllers. You may use the `namespace` parameter in your group attribute array to specify the namespace for all controllers within the group:

    Route::group(['namespace' => 'Admin'], function()
    {
        // Controllers Within The "App\Http\Controllers\Admin" Namespace

        Route::group(['namespace' => 'User'], function() {
            // Controllers Within The "App\Http\Controllers\Admin\User" Namespace
        });
    });

Remember, by default, the `RouteServiceProvider` includes your `routes.php` file within a namespace group, allowing you to register controller routes without specifying the full `App\Http\Controllers` namespace prefix. So, we only need to specify the portion of the namespace that comes after the base `App\Http\Controllers` namespace.

<a name="route-group-sub-domain-routing"></a>
### Sub-Domain Routing

Route groups may also be used to route wildcard sub-domains. Sub-domains may be assigned route parameters just like route URIs, allowing you to capture a portion of the sub-domain for usage in your route or controller. The sub-domain may be specified using the `domain` key on the group attribute array:

    Route::group(['domain' => '{account}.myapp.com'], function () {
        Route::get('user/{id}', function ($account, $id) {
            //
        });
    });

<a name="route-group-prefixes"></a>
### Route Prefixes

The `prefix` group attribute may be used to prefix each route in the group with a given URI. For example, you may want to prefix all route URIs within the group with `admin`:

    Route::group(['prefix' => 'admin'], function () {
        Route::get('users', function ()    {
            // Matches The "/admin/users" URL
        });
    });

You may also use the `prefix` parameter to specify common parameters for your grouped routes:

    Route::group(['prefix' => 'accounts/{account_id}'], function () {
        Route::get('detail', function ($accountId)    {
            // Matches The "/accounts/{account_id}/detail" URL
        });
    });

<a name="csrf-protection"></a>
## CSRF Protection

<a name="csrf-introduction"></a>
### Introduction

Laravel makes it easy to protect your application from [cross-site request forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) attacks. Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of an authenticated user.

Laravel automatically generates a CSRF "token" for each active user session managed by the application. This token is used to verify that the authenticated user is the one actually making the requests to the application.

Anytime you define a HTML form in your application, you should include a hidden CSRF token field in the form so that the CSRF protection middleware will be able to validate the request. To generate a hidden input field `_token` containing the CSRF token, you may use the `csrf_field` helper function:

    // Vanilla PHP
    <?php echo csrf_field(); ?>

    // Blade Template Syntax
    {{ csrf_field() }}

The `csrf_field` helper function generates the following HTML:

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

You do not need to manually verify the CSRF token on POST, PUT, or DELETE requests. The `VerifyCsrfToken` [middleware](/docs/{{version}}/middleware), which is included in the `web` middleware group, will automatically verify that the token in the request input matches the token stored in the session.

<a name="csrf-excluding-uris"></a>
### Excluding URIs From CSRF Protection

Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your webhook handler route from Laravel's CSRF protection.

You may exclude URIs by defining their routes outside of the `web` middleware group that is included in the default `routes.php` file, or by adding the URIs to the `$except` property of the `VerifyCsrfToken` middleware:

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as BaseVerifier;

    class VerifyCsrfToken extends BaseVerifier
    {
        /**
         * The URIs that should be excluded from CSRF verification.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
        ];
    }

<a name="csrf-x-csrf-token"></a>
### X-CSRF-TOKEN

In addition to checking for the CSRF token as a POST parameter, the Laravel `VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in a "meta" tag:

    <meta name="csrf-token" content="{{ csrf_token() }}">

Once you have created the `meta` tag, you can instruct a library like jQuery to add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications:

    $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
    });

<a name="csrf-x-xsrf-token"></a>
### X-XSRF-TOKEN

Laravel also stores the CSRF token in a `XSRF-TOKEN` cookie. You can use the cookie value to set the `X-XSRF-TOKEN` request header. Some JavaScript frameworks, like Angular, do this automatically for you. It is unlikely that you will need to use this value manually.

<a name="route-model-binding"></a>
## Route Model Binding

Laravel route model binding provides a convenient way to inject model instances into your routes. For example, instead of injecting a user's ID, you can inject the entire `User` model instance that matches the given ID.

### Implicit Binding

Laravel will automatically resolve type-hinted Eloquent models defined in routes or controller actions whose variable names match a route segment name. For example:

    Route::get('api/users/{user}', function (App\User $user) {
        return $user->email;
    });

In this example, since the Eloquent type-hinted `$user` variable defined on the route matches the `{user}` segment in the route's URI, Laravel will automatically inject the model instance that has an ID matching the corresponding value from the request URI.

If a matching model instance is not found in the database, a 404 HTTP response will be automatically generated.

#### Customizing The Key Name

If you would like the implicit model binding to use a database column other than `id` when retrieving models, you may override the `getRouteKeyName` method on your Eloquent model:

    /**
     * Get the route key for the model.
     *
     * @return string
     */
    public function getRouteKeyName()
    {
        return 'slug';
    }

### Explicit Binding

To register an explicit binding, use the router's `model` method to specify the class for a given parameter. You should define your model bindings in the `RouteServiceProvider::boot` method:

#### Binding A Parameter To A Model

    public function boot(Router $router)
    {
        parent::boot($router);

        $router->model('user', 'App\User');
    }

Next, define a route that contains a `{user}` parameter:

    $router->get('profile/{user}', function(App\User $user) {
        //
    });

Since we have bound the `{user}` parameter to the `App\User` model, a `User` instance will be injected into the route. So, for example, a request to `profile/1` will inject the `User` instance which has an ID of 1.

If a matching model instance is not found in the database, a 404 HTTP response will be automatically generated.

#### Customizing The Resolution Logic

If you wish to use your own resolution logic, you should use the `Route::bind` method. The `Closure` you pass to the `bind` method will receive the value of the URI segment, and should return an instance of the class you want to be injected into the route:

    $router->bind('user', function ($value) {
        return App\User::where('name', $value)->first();
    });

#### Customizing The "Not Found" Behavior

If you wish to specify your own "not found" behavior, pass a `Closure` as the third argument to the `model` method:

    $router->model('user', 'App\User', function () {
        throw new NotFoundHttpException;
    });

<a name="form-method-spoofing"></a>
## Form Method Spoofing

HTML forms do not support `PUT`, `PATCH` or `DELETE` actions. So, when defining `PUT`, `PATCH` or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form. The value sent with the `_method` field will be used as the HTTP request method:

    <form action="/foo/bar" method="POST">
        <input type="hidden" name="_method" value="PUT">
        <input type="hidden" name="_token" value="{{ csrf_token() }}">
    </form>

To generate the hidden input field `_method`, you may also use the `method_field` helper function:

    <?php echo method_field('PUT'); ?>

Of course, using the Blade [templating engine](/docs/{{version}}/blade):

    {{ method_field('PUT') }}

<a name="accessing-the-current-route"></a>
## Accessing The Current Route

The `Route::current()` method will return the route handling the current HTTP request, allowing you to inspect the full `Illuminate\Routing\Route` instance:

    $route = Route::current();

    $name = $route->getName();

    $actionName = $route->getActionName();

You may also use the `currentRouteName` and `currentRouteAction` helper methods on the `Route` facade to access the current route's name or action:

    $name = Route::currentRouteName();

    $action = Route::currentRouteAction();

Please refer to the API documentation for both the [underlying class of the Route facade](http://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) and [Route instance](http://laravel.com/api/{{version}}/Illuminate/Routing/Route.html) to review all accessible methods.
