# API Authentication (Passport)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [OAuth2 Using Authorization Codes](#oauth2-using-authorization-codes)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating A Personal Access Client](#)
    - [Managing Personal Access Tokens](#)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing The Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Assigning Scopes To Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [Calling Your Own API](#)

<a name="introduction"></a>
## Introduction

Laravel already makes it easy to perform authentication via traditional login forms, but what about APIs? APIs typically use tokens to authenticate users and do not maintain session state between requests. Laravel makes API authentication a breeze using Laravel Passport, a package that brings a full OAuth2 server implementation into your Laravel application in a matter of minutes.

> {note} This documentation assumes you are already familiar with OAuth2. If you do not know anything about OAuth2, consider familiarizing yourself with the general terminology and features of OAuth2 before continuing.

<a name="installation"></a>
## Installation

To get started, install Passport via the Composer package manager:

    composer require laravel/passport

Next, register the Passport service provider in the `providers` array of your `config/app.php` configuration file:

    Laravel\Passport\PassportServiceProvider::class,

The Passport service provider registers its own database migration directory with the framework, so you should migrate your database after registering the provider. The Passport migrations will create the tables your application needs to store clients and access tokens:

    php artisan migrate

Next, you should run the `passport:install` command. This command will create the encryption keys needed to generate secure access tokens. In addition, the command will create a "personal access" client which will be used to generate personal access tokens:

    php artisan passport:install

After running this command, add the `Laravel\Passport\HasApiTokens` trait to your `App\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes:

    <?php

    namespace App;

    use Laravel\Passport\HasApiTokens;
    use Illuminate\Notifications\Notifiable;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable
    {
        use HasApiTokens, Notifiable;
    }

Next, you should call the `Passport::routes` method within the `boot` method of your `AuthServiceProvider`. This method will register the routes necessary to issue access tokens and revoke access tokens, clients, and personal access tokens:

    <?php

    namespace App\Providers;

    use Laravel\Passport\Passport;
    use Illuminate\Support\Facades\Gate;
    use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * The policy mappings for the application.
         *
         * @var array
         */
        protected $policies = [
            'App\Model' => 'App\Policies\ModelPolicy',
        ];

        /**
         * Register any authentication / authorization services.
         *
         * @return void
         */
        public function boot()
        {
            $this->registerPolicies();

            Passport::routes();
        }
    }

Finally, in your `config/auth.php` configuration file, you should set the `driver` option of the `api` authentication guard to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests:

    'guards' => [
        'web' => [
            'driver' => 'session',
            'provider' => 'users',
        ],

        'api' => [
            'driver' => 'passport',
            'provider' => 'users',
        ],
    ],

<a name="configuration"></a>
### Configuration

#### Token Lifetimes

By default, Passport issues long-lived access tokens that never need to be refreshed. If you would like to configure a shorter token lifetime, you may use the `tokensExpireIn` and `refreshTokensExpireIn` methods. These methods should be called from the `boot` method of your `AuthServiceProvider`:

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Passport::routes();

        Passport::tokensExpireIn(Carbon::now()->addDays(15));

        Passport::refreshTokensExpireIn(Carbon::now()->addDays(30));
    }

<a name="oauth2-using-authorization-codes"></a>
### OAuth2 Using Authorization Codes

Using OAuth2 with authorization codes is probably how most developers are familiar with OAuth2. When using authorization codes, the client will redirect a user to your server where they will either approve or deny the request to issue the client an access token. Passport makes it very simple for your application to issue access tokens to clients in this way.

<a name="managing-clients"></a>
### Managing Clients

First, developers that want to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URL that your application can redirect to after users approve their request for authorization.

#### The `passport:client` Command

The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create your own clients for testing your OAuth2 functionality. When you run the `client` command, Passport will prompt you for more information about your client:

    php artisan passport:client

#### JSON API

Since your users will not be able to utilize the `client` command, Passport provides a JSON API that you may use to create clients. This saves you the trouble of having to manually code controllers for creating, updating, and deleting clients.

> {tip} The routes to send requests to the Passport controllers were registered when you called the `Passport::routes` method in your `AuthServiceProvider`.

However, you will need to pair Passport's JSON API with your own frontend to provide a dashboard for your users to manage their clients. Below, we'll review all of the API endpoints for managing clients. For convenience, we'll use [Vue](https://vuejs.org) to demonstrate making HTTP requests to the endpoints.

#### `GET /oauth/clients`

This route returns all of the clients for the authenticated user. This is primarily useful for listing all of the user's clients so that they may edit or delete them:

    this.$http.get('/oauth/clients')
        .then(response => {
            console.log(response.data);
        });

#### `POST /oauth/clients`

This route is used to create new clients. It requires two pieces of data: the client's `name` and a `redirect` URL. The `redirect` URL is where the user will be redirected after approving or denying a request for authorization.

When a client is created, it will be issued a client ID and client "secret". These values will be used when requesting access tokens from your application. The client creation route will return the new client instance:

    const data = {
        name: 'Client Name',
        redirect: 'http://example.com/callback'
    };

    this.$http.post('/oauth/clients', data)
        .then(response => {
            console.log(response.data);
        })
        .catch (response => {
            // List errors on response...
        });

#### `PUT /oauth/clients/{client-id}`

This route is used to update clients. It requires two pieces of data: the client's `name` and a `redirect` URL. The `redirect` URL is where the user will be redirected after approving or denying a request for authorization. The route will return the updated client instance:

    const data = {
        name: 'New Client Name',
        redirect: 'http://example.com/callback'
    };

    this.$http.put('/oauth/clients/' + clientId, data)
        .then(response => {
            console.log(response.data);
        })
        .catch (response => {
            // List errors on response...
        });

#### `DELETE /oauth/clients/{client-id}`

This route is used to delete clients:

    this.$http.delete('/oauth/clients/' + clientId)
        .then(response => {
            //
        });

<a name="requesting-tokens"></a>
### Requesting Tokens

#### Redirecting For Authorization

Once a client has been created, developer's may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application like so:

    Route::get('/redirect', function () {
        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://example.com/callback',
            'response_type' => 'code',
            'scope' => '',
        ]);

        return redirect('http://your-app.com/oauth/authorize?'.$query);
    });

When receiving authorization requests, Passport will automatically display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created.

#### Converting Authorization Codes To Access Tokens

If the user approves the authorization request and is redirected to the consuming application, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by when the user approved the authorization request. In this example, we'll use the Guzzle HTTP library to make the request:

    Route::get('/callback', function (Request $request) {
        $http = new GuzzleHttp\Client;

        $response = $http->post('http://your-app.com/oauth/token', [
            'form_params' => [
                'grant_type' => 'authorization_code',
                'client_id' => 'client-id',
                'client_secret' => 'client-secret',
                'redirect_uri' => 'http://example.com/callback',
                'code' => $request->code,
            ],
        ]);

        return json_decode((string) $response->getBody(), true);
    });

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

<a name="refreshing-tokens"></a>
### Refreshing Tokens

If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued. In this example, we'll use the Guzzle HTTP library to refresh the token:

    $http = new GuzzleHttp\Client;

    $response = $http->post('http://your-app.com/oauth/token', [
        'form_params' => [
            'grant_type' => 'refresh_token',
            'refresh_token' => 'the-refresh-token',
            'client_id' => 'client-id',
            'client_secret' => 'client-secret',
            'scope' => '',
        ],
    ]);

    return json_decode((string) $response->getBody(), true);

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

<a name="personal-access-tokens"></a>
## Personal Access Tokens

Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general.

> {note} Personal access tokens are always long-lived. Their lifetime is not modified when using the `tokensExpireIn` or `refreshTokensExpireIn` methods.

<a name="creating-a-personal-access-client"></a>
### Creating A Personal Access Client

Before your application can issue personal access tokens, you will need to create a personal access client. You may do this using the `passport:client` command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command:

    php artisan passport:client --personal

<a name="managing-personal-access-tokens"></a>
### Managing Personal Access Tokens

Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument:

    $user = App\User::find(1);

    $token = $user->createToken('Token Name')->accessToken;

    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

#### JSON API

Passport also includes a JSON API for managing personal access tokens. You may pair this with your own frontend to offer your users a dashboard for managing personal access tokens. Below, we'll review all of the API endpoints for managing personal access tokens. For convenience, we'll use [Vue](https://vuejs.org) to demonstrate making HTTP requests to the endpoints.

#### `GET /oauth/scopes`

This route returns all of the [scopes](#scopes) defined for your application. You may use this route to list the scopes a user may assign to a personal access token:

    this.$http.get('/oauth/scopes')
        .then(response => {
            console.log(response.data);
        });

#### `GET /oauth/personal-access-tokens`

This route returns all of the personal access tokens that the user has created. This is primarily useful for listing all of the user's token so that they may edit or delete them:

    this.$http.get('/oauth/personal-access-tokens')
        .then(response => {
            console.log(response.data);
        });

#### `POST /oauth/personal-access-tokens`

This route is used to create new personal access tokens. It requires two pieces of data: the token's `name` and the `scopes` that should be assigned to the token:

    const data = {
        name: 'Token Name',
        scopes: []
    };

    this.$http.post('/oauth/personal-access-tokens', data)
        .then(response => {
            console.log(response.data.accessToken);
        })
        .catch (response => {
            // List errors on response...
        });

#### `DELETE /oauth/personal-access-tokens/{token-id}`

This route may be used to delete personal access tokens:

    this.$http.delete('/oauth/personal-access-tokens/' + tokenId);

<a name="protecting-routes"></a>
## Protecting Routes

<a name="via-middleware"></a>
### Via Middleware

Passport includes an [authentication guard](/docs/{{version}}/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured your `api` guard to use the `passport` driver in your `config/auth.php` configuration file, you only need to specify the `auth:api` middleware on any routes that should require an access token:

    Route::get('/user', function () {
        //
    })->middleware('auth:api');

> {tip} The `RouteServiceProvider` included with fresh Laravel applications already loads the `api` route file within a route group containing the `auth:api` middleware. So, there is no need to manually assign this middleware to all the routes in your `api` routes file.

<a name="passing-the-access-token"></a>
### Passing The Access Token

When calling routes that are protected by Passport, your application's API consumers will need to specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the Guzzle HTTP library:

    $response = $client->request('GET', '/api/user', [
        'headers' => [
            'Accept' => 'application/json',
            'Authorization' => 'Bearer '.$accessToken,
        ],
    ]);

<a name="token-scopes"></a>
## Token Scopes


<a name="defining-scopes"></a>
### Defining Scopes

Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf.

You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your `AuthServiceProvider`. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and is displayed to the user on the authorization approval screen when a consuming application requests a token with that scope:

    use Laravel\Passport\Passport;

    Passport::tokensCan([
        'place-orders' => 'Place orders on your behalf',
        'check-status' => 'Check the status of your orders',
    ]);

<a name="assigning-scopes-to-tokens"></a>
### Assigning Scopes To Tokens

#### When Requesting Authorization Codes

When requesting an access token using the authorization code grant, you should specify your desired scopes as the `scope` query string parameter using a space-delimited string:

    Route::get('/redirect', function () {
        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://example.com/callback',
            'response_type' => 'code',
            'scope' => 'place-orders check-status',
        ]);

        return redirect('http://your-app.com/oauth/authorize?'.$query);
    });

#### When Issuing Personal Access Tokens

If you are issuing personal access tokens using the `createToken` method on a `User` model instance, you may pass the array of desired scopes as the second argument to the method:

    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

<a name="checking-scopes"></a>
### Checking Scopes

Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token containing a scope. To get started, add the following middleware to the `$routeMiddleware` property of your `app/Http/Kernel.php` file:

    'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
    'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,

#### Check For All Scopes

The `scopes` middleware may be assigned to a route to verify that the incoming request's access token has *all* of the listed scopes:

    Route::get('/orders', function () {
        // Access token has both "check-status" and "place-orders" scopes...
    })->middleware('scopes:check-status,place-orders');

#### Check For Any Scopes

The `scope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes:

    Route::get('/orders', function () {
        // Access token has either "check-status" or "place-orders" scope...
    })->middleware('scope:check-status,place-orders');

#### Checking Scopes On A Token Instance

Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `User` model instance:

    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        if ($request->user()->tokenCan('place-orders')) {
            //
        }
    });
