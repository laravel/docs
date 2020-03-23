# Laravel Sanctum

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Installation](#installation)
- [API Token Authentication](#api-token-authentication)
    - [Issuing API Tokens](#issuing-api-tokens)
    - [Token Abilities](#token-abilities)
    - [Protecting Routes](#protecting-routes)
    - [Revoking Tokens](#revoking-tokens)
- [SPA Authentication](#spa-authentication)
    - [Configuration](#spa-configuration)
    - [Authenticating](#spa-authenticating)
    - [Protecting Routes](#protecting-spa-routes)
    - [Authorizing Private Broadcast Channels](#authorizing-private-broadcast-channels)
- [Mobile Application Authentication](#mobile-application-authentication)
    - [Issuing API Tokens](#issuing-mobile-api-tokens)
    - [Protecting Routes](#protecting-mobile-api-routes)
    - [Revoking Tokens](#revoking-mobile-api-tokens)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction

Laravel Sanctum provides a featherweight authentication system for SPAs (single page applications), mobile applications, and simple, token based APIs. Sanctum allows each user of your application to generate multiple API tokens for their account. These tokens may be granted abilities / scopes which specify which actions the tokens are allowed to perform.

<a name="how-it-works"></a>
### How It Works

#### API Tokens

Laravel Sanctum exists to solve two separate problems. First, it is a simple package to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub "access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime.

Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming requests via the `Authorization` header which should contain a valid API token.

#### SPA Authentication

> {tip} It is perfectly fine to use Sanctum only for API token authentication or only for SPA authentication. Just because you use Sanctum does not mean you are required to use both features it offers.

Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI.

For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend.

<a name="installation"></a>
## Installation

You may install Laravel Sanctum via Composer:

    composer require laravel/sanctum

Next, you should publish the Sanctum configuration and migration files using the `vendor:publish` Artisan command. The `sanctum` configuration file will be placed in your `config` directory:

    php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"

Finally, you should run your database migrations. Sanctum will create one database table in which to store API tokens:

    php artisan migrate

Next, if you plan to utilize Sanctum to authenticate an SPA, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file:

    use Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful;

    'api' => [
        EnsureFrontendRequestsAreStateful::class,
        'throttle:60,1',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

#### Migration Customization

If you are not going to use Sanctum's default migrations, you should call the `Sanctum::ignoreMigrations` method in the `register` method of your `AppServiceProvider`. You may export the default migrations using `php artisan vendor:publish --tag=sanctum-migrations`.

<a name="api-token-authentication"></a>
## API Token Authentication

> {tip} You should not use API tokens to authenticate your own first-party SPA. Instead, use Sanctum's built-in [SPA authentication](#spa-authentication).

<a name="issuing-api-tokens"></a>
### Issuing API Tokens

Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token.

To begin issuing tokens for users, your User model should use the `HasApiTokens` trait:

    use Laravel\Sanctum\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, Notifiable;
    }

To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created:

    $token = $user->createToken('token-name');

    return $token->plainTextToken;

You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait:

    foreach ($user->tokens as $token) {
        //
    }

<a name="token-abilities"></a>
### Token Abilities

Sanctum allows you to assign "abilities" to tokens, similar to OAuth "scopes". You may pass an array of string abilities as the second argument to the `createToken` method:

    return $user->createToken('token-name', ['server:update'])->plainTextToken;

When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` method:

    if ($user->tokenCan('server:update')) {
        //
    }

> {tip} For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication).

<a name="protecting-routes"></a>
### Protecting Routes

To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-tokens"></a>
### Revoking Tokens

You may "revoke" tokens by deleting them from your database using the `tokens` relationship that is provided by the `HasApiTokens` trait:

    // Revoke all tokens...
    $user->tokens()->delete();

    // Revoke a specific token...
    $user->tokens()->where('id', $id)->delete();

<a name="spa-authentication"></a>
## SPA Authentication

Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI.

For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend.

> {note} In order to authenticate, your SPA and API must share the same top-level domain. However, they may be placed on different subdomains.

<a name="spa-configuration"></a>
### Configuration

#### Configuring Your First-Party Domains

First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API.

#### Sanctum Middleware

Next, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file. This middleware is responsible for ensuring that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens:

    use Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful;

    'api' => [
        EnsureFrontendRequestsAreStateful::class,
        'throttle:60,1',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

<a name="cors-and-cookies"></a>
#### CORS & Cookies

If you are having trouble authenticating with your application from an SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings.

You should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True` by setting the `supports_credentials` option within your application's `cors` configuration file to `true`.

In addition, you should enable the `withCredentials` option on your global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file:

    axios.defaults.withCredentials = true;

Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may do this by prefixing the domain with a leading `.` within your `session` configuration file:

    'domain' => '.domain.com',

<a name="spa-authenticating"></a>
### Authenticating

To authenticate your SPA, your SPA's login page should first make a request to the `/sanctum/csrf-cookie` route to initialize CSRF protection for the application:

    axios.get('/sanctum/csrf-cookie').then(response => {
        // Login...
    });

Once CSRF protection has been initialized, you should make a `POST` request to the typical Laravel `/login` route. This `/login` route may be provided by the `laravel/ui` [authentication scaffolding](/docs/{{version}}/authentication#introduction) package.

If the login request is successful, you will be authenticated and subsequent requests to your API routes will automatically be authenticated via the session cookie that the Laravel backend issued to your client.

> {tip} You are free to write your own `/login` endpoint; however, you should ensure that it authenticates the user using the standard, [session based authentication services that Laravel provides](/docs/{{version}}/authentication#authenticating-users).

<a name="protecting-spa-routes"></a>
### Protecting Routes

To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="authorizing-private-broadcast-channels"></a>
### Authorizing Private Broadcast Channels

If your SPA needs to authenticate with [private / presence broadcast channels](/docs/{{version}}/broadcasting#authorizing-channels), you should place the `Broadcast::routes` method call within your `routes/api.php` file:

    Broadcast::routes(['middleware' => ['auth:sanctum']]);

Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/{{version}}/broadcasting#installing-laravel-echo). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies):

    window.Echo = new Echo({
        broadcaster: "pusher",
        cluster: process.env.MIX_PUSHER_APP_CLUSTER,
        encrypted: true,
        key: process.env.MIX_PUSHER_APP_KEY,
        authorizer: (channel, options) => {
            return {
                authorize: (socketId, callback) => {
                    axios.post('/api/broadcasting/auth', {
                        socket_id: socketId,
                        channel_name: channel.name
                    })
                    .then(response => {
                        callback(false, response.data);
                    })
                    .catch(error => {
                        callback(true, error);
                    });
                }
            };
        },
    })

<a name="mobile-application-authentication"></a>
## Mobile Application Authentication

You may use Sanctum tokens to authenticate your mobile application's requests to your API. The process for authenticating mobile application requests is similar to authenticating third-party API requests; however, there are small differences in how you will issue the API tokens.

<a name="issuing-mobile-api-tokens"></a>
### Issuing API Tokens

To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The endpoint will return the plain-text Sanctum token which may then be stored on the mobile device and used to make additional API requests:

    use App\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Validation\ValidationException;

    Route::post('/sanctum/token', function (Request $request) {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
            'device_name' => 'required'
        ]);

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        return $user->createToken($request->device_name)->plainTextToken;
    });

When the mobile device uses the token to make an API request to your application, it should pass the token in the `Authorization` header as a `Bearer` token.

> {tip} When issuing tokens for a mobile application, you are also free to specify [token abilities](#token-abilities)

<a name="protecting-mobile-api-routes"></a>
### Protecting Routes

As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes. Typically, you will attach this guard to the routes defined within your `routes/api.php` file:

    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

<a name="revoking-mobile-api-tokens"></a>
### Revoking Tokens

To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `HasApiTokens` trait:

    // Revoke all tokens...
    $user->tokens()->delete();

    // Revoke a specific token...
    $user->tokens()->where('id', $id)->delete();

<a name="testing"></a>
## Testing

While testing, the `Sanctum::actingAs` method may be used to authenticate a user and specify which abilities are granted to their token:

    use App\User;
    use Laravel\Sanctum\Sanctum;

    public function test_task_list_can_be_retrieved()
    {
        Sanctum::actingAs(
            factory(User::class)->create(),
            ['view-tasks']
        );

        $response = $this->get('/api/task');

        $response->assertOk();
    }

If you would like to grant all abilities to the token, you should include `*` in the ability list provided to the `actingAs` method:

    Sanctum::actingAs(
        factory(User::class)->create(),
        ['*']
    );
