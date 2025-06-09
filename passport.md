# Laravel Passport

- [Introduction](#introduction)
    - [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
    - [Overriding Routes](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Managing Tokens](#managing-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [Creating the Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Creating a Device Code Grant Client](#creating-a-device-authorization-grant-client)
    - [Requesting Tokens](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Creating a Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing the User Provider](#customizing-the-user-provider)
    - [Customizing the Username Field](#customizing-the-username-field)
    - [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating a Personal Access Client](#creating-a-personal-access-client)
    - [Customizing the User Provider](#customizing-the-user-provider-for-pat)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [SPA Authentication](#spa-authentication)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction

[Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp.

> [!NOTE]
> This documentation assumes you are already familiar with OAuth2. If you do not know anything about OAuth2, consider familiarizing yourself with the general [terminology](https://oauth2.thephpleague.com/terminology/) and features of OAuth2 before continuing.

<a name="passport-or-sanctum"></a>
### Passport or Sanctum?

Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/{{version}}/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport.

However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/{{version}}/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience.

<a name="installation"></a>
## Installation

You may install Laravel Passport via the `install:api` Artisan command:

```shell
php artisan install:api --passport
```

This command will publish and run the database migrations necessary for creating the tables your application needs to store OAuth2 clients and access tokens. The command will also create the encryption keys required to generate secure access tokens.

After running the `install:api` command, add the `Laravel\Passport\HasApiTokens` trait and `Laravel\Passport\Contracts\OAuthenticatable` interface to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

Finally, in your application's `config/auth.php` configuration file, you should define an `api` authentication guard and set the `driver` option to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests:

```php
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
```

<a name="deploying-passport"></a>
### Deploying Passport

When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control:

```shell
php artisan passport:keys
```

If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### Loading Keys From the Environment

Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --tag=passport-config
```

After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Upgrading Passport

When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md).

<a name="configuration"></a>
## Configuration

<a name="token-lifetimes"></a>
### Token Lifetimes

By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```

> [!WARNING]
> The `expires_at` columns on Passport's database tables are read-only and for display purposes only. When issuing tokens, Passport stores the expiration information within the signed and encrypted tokens. If you need to invalidate a token you should [revoke it](#revoking-tokens).

<a name="overriding-default-models"></a>
### Overriding Default Models

You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class)
}
```

<a name="overriding-routes"></a>
### Overriding Routes

Sometimes you may wish to customize the routes defined by Passport. To achieve this, you first need to ignore the routes registered by Passport by adding `Passport::ignoreRoutes` to the `register` method of your application's `AppServiceProvider`:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

Then, you may copy the routes defined by Passport in [its routes file](https://github.com/laravel/passport/blob/master/routes/web.php) to your application's `routes/web.php` file and modify them to your liking:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="authorization-code-grant"></a>
## Authorization Code Grant

Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client.

To get started, we need to instruct Passport how to return our "authorization" view.

All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::authorizationView('auth.oauth.authorize');

    // By providing a closure...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```

Passport will automatically define the `/oauth/authorize` route that returns this view. Your `auth.oauth.authorize` template should include a form that makes a POST request to the `passport.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.authorizations.deny` route to deny the authorization. The `passport.authorizations.approve` and `passport.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields.

<a name="managing-clients"></a>
### Managing Clients

Developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URI that your application can redirect to after users approve their request for authorization.

<a name="managing-first-party-clients"></a>
#### First-Party Clients

The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create first-party clients or testing your OAuth2 functionality. When you run the `passport:client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret:

```shell
php artisan passport:client
```

If you would like to allow multiple redirect URIs for your client, you may specify them using a comma-delimited list when prompted for the URI by the `passport:client` command. Any URIs which contain commas should be URI encoded:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### Third-Party Clients

Since your application's users will not be able to utilize the `passport:client` command, you may use `createAuthorizationCodeGrantClient` method of the `Laravel\Passport\ClientRepository` class to register a client for a given user:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// Creating an OAuth app client that belongs to the given user...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// Retrieving all the OAuth app clients that belong to the user...
$clients = $user->oauthApps()->get();
```

The `createAuthorizationCodeGrantClient` method returns an instance of `Laravel\Passport\Client`. You may display the `$client->id` as the client ID and `$client->plainSecret` as the client secret to the user.

<a name="requesting-tokens"></a>
### Requesting Tokens

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### Redirecting for Authorization

Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

The `prompt` parameter may be used to specify the authentication behavior of the Passport application.

If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session.

If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes.

> [!NOTE]
> Remember, the `/oauth/authorize` route is already defined by Passport. You do not need to manually define this route.

<a name="approving-the-request"></a>
#### Approving the Request

When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created.

Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### Converting Authorization Codes to Access Tokens

If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

> [!NOTE]
> Like the `/oauth/authorize` route, the `/oauth/token` route is defined for you by Passport. There is no need to manually define this route.

<a name="managing-tokens"></a>
### Managing Tokens

You may retrieve user's authorized tokens using the `tokens` method of the `Laravel\Passport\HasApiTokens` trait. For example, this may be used to offer your users a dashboard to keep track of their connections with third-party applications:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Retrieving all of the valid tokens for the user...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// Retrieving all the user's connections to third-party OAuth app clients...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```

<a name="refreshing-tokens"></a>
### Refreshing Tokens

If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

<a name="revoking-tokens"></a>
### Revoking Tokens

You may revoke a token by using the `revoke` method on the `Laravel\Passport\Token` model. You may revoke a token's refresh token using the `revoke` method on the `Laravel\Passport\RefreshToken` model:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Revoke an access token...
$token->revoke();

// Revoke the token's refresh token...
$token->refreshToken?->revoke();

// Revoke all of the user's tokens...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### Purging Tokens

When tokens have been revoked or expired, you might want to purge them from the database. Passport's included `passport:purge` Artisan command can do this for you:

```shell
# Purge revoked and expired tokens, auth codes, and device codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens, auth codes, and device codes...
php artisan passport:purge --revoked

# Only purge expired tokens, auth codes, and device codes...
php artisan passport:purge --expired
```

You may also configure a [scheduled job](/docs/{{version}}/scheduling) in your application's `routes/console.php` file to automatically prune your tokens on a schedule:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## Authorization Code Grant With PKCE

The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or mobile applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token.

<a name="creating-a-auth-pkce-grant-client"></a>
### Creating the Client

Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### Requesting Tokens

<a name="code-verifier-code-challenge"></a>
#### Code Verifier and Code Challenge

As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token.

The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and  `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636).

The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### Redirecting for Authorization

Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### Converting Authorization Codes to Access Tokens

If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant.

If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="device-authorization-grant"></a>
## Device Authorization Grant

The OAuth2 device authorization grant allows browserless or limited input devices, such as TVs and game consoles, to obtain an access token by exchanging a "device code". When using device flow, the device client will instruct the user to use a secondary device, such as a computer or a smartphone and connect to your server where they will enter the provided "user code" and either approve or deny the access request.

To get started, we need to instruct Passport how to return our "user code" and "authorization" views.

All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // By providing a closure...
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```

Passport will automatically define routes that return these views. Your `auth.oauth.device.user-code` template should include a form that makes a GET request to the `passport.device.authorizations.authorize` route. The `passport.device.authorizations.authorize` route expects a `user_code` query parameter.

Your `auth.oauth.device.authorize` template should include a form that makes a POST request to the `passport.device.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.device.authorizations.deny` route to deny the authorization. The `passport.device.authorizations.approve` and `passport.device.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields.

<a name="creating-a-device-authorization-grant-client"></a>
### Creating a Device Authorization Grant Client

Before your application can issue tokens via the device authorization grant, you will need to create a device flow enabled client. You may do this using the `passport:client` Artisan command with the `--device` option. This command will create a first-party device flow enabled client and provide you with a client ID and secret:

```shell
php artisan passport:client --device
```

Additionally, you may use `createDeviceAuthorizationGrantClient` method on the `ClientRepository` class to register a third-party client that belongs to the given user:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```

<a name="requesting-device-authorization-grant-tokens"></a>
### Requesting Tokens

<a name="device-code"></a>
#### Requesting a Device Code

Once a client has been created, developers may use their client ID to request a device code from your application. First, the consuming device should make a `POST` request to your application's `/oauth/device/code` route to request a device code:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

This will return a JSON response containing `device_code`, `user_code`, `verification_uri`, `interval`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the device code expires. The `interval` attribute contains the number of seconds the consuming device should wait between requests when polling `/oauth/token` route to avoid rate limit errors.

> [!NOTE]
> Remember, the `/oauth/device/code` route is already defined by Passport. You do not need to manually define this route.

<a name="user-code"></a>
#### Displaying the Verification URI and User Code

Once a device code request has been obtained, the consuming device should instruct the user to use another device and visit the provided `verification_uri` and enter the `user_code` in order to approve the authorization request.

<a name="polling-token-request"></a>
#### Polling Token Request

Since the user will be using a separate device to grant (or deny) access, the consuming device should poll your application's `/oauth/token` route to determine when the user has responded to the request. The consuming device should use the minimum polling `interval` provided in the JSON response when requesting device code to avoid rate limit errors:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

If the user has approved the authorization request, this will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

<a name="password-grant"></a>
## Password Grant

> [!WARNING]
> We no longer recommend using password grant tokens. Instead, you should choose [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow.

To enable the password grant, call the `enablePasswordGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
### Creating a Password Grant Client

Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### Requesting Tokens

Once you have enabled the grant and have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by Passport so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> Remember, access tokens are long-lived by default. However, you are free to [configure your maximum access token lifetime](#configuration) if needed.

<a name="requesting-all-scopes"></a>
### Requesting All Scopes

When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### Customizing the User Provider

If your application uses more than one [authentication user provider](/docs/{{version}}/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized.

<a name="customizing-the-username-field"></a>
### Customizing the Username Field

When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### Customizing the Password Validation

When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## Implicit Grant

> [!WARNING]
> We no longer recommend using implicit grant tokens. Instead, you should choose [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

Before your application can issue tokens via the implicit grant, you will need to create an implicit grant client. You may do this using the `passport:client` Artisan command with the `--implicit` option.

```shell
php artisan passport:client --implicit
```

Once the grant has been enabled and an implicit client has been created, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> Remember, the `/oauth/authorize` route is already defined by Passport. You do not need to manually define this route.

<a name="client-credentials-grant"></a>
## Client Credentials Grant

The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API.

Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command:

```shell
php artisan passport:client --client
```

Next, assign the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware to a route:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

To restrict access to the route to specific scopes, you may provide a list of the required scopes to the `using` method`:

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create');
```

<a name="retrieving-tokens"></a>
### Retrieving Tokens

To retrieve a token using this grant type, make a request to the `oauth/token` endpoint:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## Personal Access Tokens

Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general.

> [!NOTE]
> If your application is using Passport primarily to issue personal access tokens, consider using [Laravel Sanctum](/docs/{{version}}/sanctum), Laravel's light-weight first-party library for issuing API access tokens.

<a name="creating-a-personal-access-client"></a>
### Creating a Personal Access Client

Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command:

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### Customizing the User Provider

If your application uses more than one [authentication user provider](/docs/{{version}}/authentication#introduction), you may specify which user provider the personal access grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --personal` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized.

<a name="managing-personal-access-tokens"></a>
### Managing Personal Access Tokens

Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Creating a token without scopes...
$token = $user->createToken('My Token')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// Creating a token with all scopes...
$token = $user->createToken('My Token', ['*'])->accessToken;

// Retrieving all the valid personal access tokens that belong to the user...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## Protecting Routes

<a name="via-middleware"></a>
### Via Middleware

Passport includes an [authentication guard](/docs/{{version}}/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token:

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```

> [!WARNING]
> If you are using the [client credentials grant](#client-credentials-grant), you should use [the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware](#client-credentials-grant) to protect your routes instead of the `auth:api` middleware.

<a name="multiple-authentication-guards"></a>
#### Multiple Authentication Guards

If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file:

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```

The following route will utilize the `api-customers` guard, which uses the `customers` user provider, to authenticate incoming requests:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> For more information on using multiple user providers with Passport, please consult the [personal access tokens documentation](#customizing-the-user-provider-for-pat) and [password grant documentation](#customizing-the-user-provider).

<a name="passing-the-access-token"></a>
### Passing the Access Token

When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the `Http` Facade:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## Token Scopes

Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf.

<a name="defining-scopes"></a>
### Defining Scopes

You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### Default Scope

If a client does not request any specific scopes, you may configure your Passport server to attach default scopes to the token using the `defaultScopes` method. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### Assigning Scopes to Tokens

<a name="when-requesting-authorization-codes"></a>
#### When Requesting Authorization Codes

When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
#### When Issuing Personal Access Tokens

If you are issuing personal access tokens using the `App\Models\User` model's `createToken` method, you may pass the array of desired scopes as the second argument to the method:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### Checking Scopes

Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope.

<a name="check-for-all-scopes"></a>
#### Check For All Scopes

The `Laravel\Passport\Http\Middleware\CheckToken` middleware may be assigned to a route to verify that the incoming request's access token has all the listed scopes:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create');
```

<a name="check-for-any-scopes"></a>
#### Check for Any Scopes

The `Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create');
```

<a name="checking-scopes-on-a-token-instance"></a>
#### Checking Scopes on a Token Instance

Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### Additional Scope Methods

The `scopeIds` method will return an array of all defined IDs / names:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`:

```php
Passport::scopes();
```

The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

You may determine if a given scope has been defined using the `hasScope` method:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA Authentication

When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers.

Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is append the `CreateFreshApiToken` middleware to the `web` middleware group in your application's `bootstrap/app.php` file:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> You should ensure that the `CreateFreshApiToken` middleware is the last middleware listed in your middleware stack.

This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### Customizing the Cookie Name

If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF Protection

When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding included with the skeleton application and all starter kits includes an [Axios](https://github.com/axios/axios) instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests.

> [!NOTE]
> If you choose to send the `X-CSRF-TOKEN` header instead of `X-XSRF-TOKEN`, you will need to use the unencrypted token provided by `csrf_token()`.

<a name="events"></a>
## Events

Passport raises events when issuing access tokens and refresh tokens. You may [listen for these events](/docs/{{version}}/events) to prune or revoke other access tokens in your database:

<div class="overflow-auto">

| Event Name                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## Testing

Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token:

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```

Passport's `actingAsClient` method may be used to specify the currently authenticated client as well as its scopes. The first argument given to the `actingAsClient` method is the client instance and the second is an array of scopes that should be granted to the client's token:

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```
