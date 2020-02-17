# Laravel Airlock

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Installation](#installation)
- [API Token Authentication](#api-token-authentication)
    - [Issuing API Tokens](#issuing-api-tokens)
    - [Token Abilities](#token-abilities)
    - [Protecting Routes](#protecting-routes)
    - [Revoking Tokens](#revoking-tokens)
- [SPA Authentication](#spa-authentication)
    - [Configuration](#cors-and-cookies)
    - [Authenticating](#authenticating)
    - [Protecting Routes](#protecting-spa-routes)
- [Mobile Application Authentication](#mobile-application-authentication)
    - [Issuing API Tokens](#issuing-mobile-api-tokens)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction

Laravel Airlock provides a featherweight authentication system for SPAs (single page applications), mobile applications, and simple, token based APIs. Airlock allows each user of your application to generate multiple API tokens for their account. These tokens may be granted abilities / scopes which specify which actions the tokens are allowed to perform.

<a name="how-it-works"></a>
### How It Works

#### API Tokens

Laravel Airlock exists to solve two separate problems. First, it is a simple package to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub "access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Airlock to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime.

Laravel Airlock offers this feature by storing user API tokens in a single database table and authenticating incoming requests via the `Authorization` header which should contain a valid API token.

#### SPA Authentication

> {tip} It is perfectly fine to use Airlock only for API token authentication or only for SPA authentication. Just because you use Airlock does not mean you are required to use both features it offers.

Second, Airlock exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI.

For this feature, Airlock does not use tokens of any kind. Instead, Airlock simply uses Laravel's built-in cookie based session authentication services. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. Airlock will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend.

<a name="installation"></a>
## Installation

You may install Laravel Airlock via Composer:

    composer require laravel/airlock

Next, you should publish the Airlock configuration and migration files using the `vendor:publish` Artisan command. The `airlock` configuration file will be placed in your `config` directory:

    php artisan vendor:publish --provider="Laravel\Airlock\AirlockServiceProvider"

Finally, you should run your database migrations. By default, Airlock will create one database table in which to store API tokens:

    php artisan migrate

Next, if you plan to utilize Airlock to authenticate an SPA, you should add Airlock's middleware to your `api` middleware group within your `app/Http/Kernel.php` file:

    use Laravel\Airlock\Http\Middleware\EnsureFrontendRequestsAreStateful;

    'api' => [
        EnsureFrontendRequestsAreStateful::class,
        'throttle:60,1',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

