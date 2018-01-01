# Laravel Socialite

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Routing](#routing)
- [Optional Parameters](#optional-parameters)
- [Access Scopes](#access-scopes)
- [Stateless Authentication](#stateless-authentication)
- [Retrieving User Details](#retrieving-user-details)

<a name="introduction"></a>
## Introduction

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication with Facebook, Twitter, LinkedIn, Google, GitHub and Bitbucket.

> {tip} Adapters for other platforms are listed at the community driven [Socialite Providers](https://socialiteproviders.github.io/) website.

<a name="installation"></a>
## Installation

To get started with Socialite, use Composer to add the package to your project's dependencies:

    composer require laravel/socialite

<a name="configuration"></a>
## Configuration

Before using Socialite, you will also need to add credentials for the OAuth services your application utilizes. These credentials should be placed in your `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `linkedin`, `google`, `github` or `bitbucket`, depending on the providers your application requires. For example:

    'github' => [
        'client_id' => env('GITHUB_CLIENT_ID'),         // Your GitHub Client ID
        'client_secret' => env('GITHUB_CLIENT_SECRET'), // Your GitHub Client Secret
        'redirect' => 'http://your-callback-url',
    ],

> {tip} If the `redirect` option contains a relative path, it will automatically be resolved to a fully qualified URL.

<a name="routing"></a>
## Routing

Next, you are ready to authenticate users! You will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. We will access Socialite using the `Socialite` facade:

    <?php

    namespace App\Http\Controllers\Auth;

    use Socialite;

    class LoginController extends Controller
    {
        /**
         * Redirect the user to the GitHub authentication page.
         *
         * @return \Illuminate\Http\Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * Obtain the user information from GitHub.
         *
         * @return \Illuminate\Http\Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

The `redirect` method takes care of sending the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider.

Of course, you will need to define routes to your controller methods:

    Route::get('login/github', 'Auth\LoginController@redirectToProvider');
    Route::get('login/github/callback', 'Auth\LoginController@handleProviderCallback');

<a name="optional-parameters"></a>
## Optional Parameters

A number of OAuth providers support optional parameters in the redirect request. To include any optional parameters in the request, call the `with` method with an associative array:

    return Socialite::driver('google')
        ->with(['hd' => 'example.com'])
        ->redirect();

> {note} When using the `with` method, be careful not to pass any reserved keywords such as `state` or `response_type`.

<a name="access-scopes"></a>
## Access Scopes

Before redirecting the user, you may also add additional "scopes" on the request using the `scopes` method. This method will merge all existing scopes with the ones you supply:

    return Socialite::driver('github')
        ->scopes(['read:user', 'public_repo'])
        ->redirect();

You can overwrite all exisiting scopes using the `setScopes` method:

    return Socialite::driver('github')
        ->setScopes(['read:user', 'public_repo'])
        ->redirect();

<a name="stateless-authentication"></a>
## Stateless Authentication

The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to an API:

    return Socialite::driver('google')->stateless()->user();

<a name="retrieving-user-details"></a>
## Retrieving User Details

Once you have a user instance, you can grab a few more details about the user:

    $user = Socialite::driver('github')->user();

    // OAuth Two Providers
    $token = $user->token;
    $refreshToken = $user->refreshToken; // not always provided
    $expiresIn = $user->expiresIn;

    // OAuth One Providers
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All Providers
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

#### Retrieving User Details From A Token (OAuth2)

If you already have a valid access token for a user, you can retrieve their details using the `userFromToken` method:

    $user = Socialite::driver('github')->userFromToken($token);
    
#### Retrieving User Details From A Token And Secret (OAuth1)

If you already have a valid pair of token / secret for a user, you can retrieve their details using the `userFromTokenAndSecret` method:

    $user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);
