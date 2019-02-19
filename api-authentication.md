# API Authentication

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Database Migrations](#database-migrations)
- [Generating Tokens](#generating-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing The Token](#passing-the-token)

<a name="introduction"></a>
## Introduction

By default, Laravel ships with an easy way to set up API authentication. It comes with an `api` guard which implements a `token` driver. This driver will authenticate a user by its api token in the database.

> **Note:** while Laravel ships with this simple token based authentication for your api, we strongly recommend to make use of [Laravel Passport](/docs/{{version}}/passport) which provides much better and secure ways for protecting your api.

<a name="configuration"></a>
## Configuration

<a name="database-migrations"></a>
### Database Migrations

Before using the token driver, we'll need to [prepare the database](/docs/{{version}}/migrations). You'll need to add an `api_token` column to your `users` table:

    Schema::table('users', function ($table) {
        $table->string('api_token', 60)->unique()->nullable()->default(null);
    });

Once the migrations have been created, run the `migrate` Artisan command.

<a name="generating-tokens"></a>
## Generating Tokens

API tokens should be unique as they identify a specific user in your database. They should also be hard to guess so we should generate a random string. This can best be done when creating the user, for example, in the `RegisterController`:

    use Illuminate\Support\Str;

    protected function create(array $data)
    {
        return User::create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
            'api_token' => Str::random(60),
        ]);
    }

<a name="protecting-routes"></a>
## Protecting Routes

<a name="via-middleware"></a>
### Via Middleware

Laravel includes an [authentication guard](/docs/{{version}}/authentication#adding-custom-guards) that will validate api tokens on incoming requests. You only need to specify the `auth:api` middleware on any route that require a valid access token:

    Route::middleware('auth:api')->get('/user', function(Request $request) {    
        return $request->user();
    });

Your Laravel app ships with this route by default in the `routes/api.php` file.

<a name="passing-the-token"></a>
### Passing The Token

There are several ways of passing the token to the guard protecting your API routes. We'll go over each of them while using the Guzzle HTTP library:

#### Query String Item

Your application's API consumers can specify their token as a query string item:

    $response = $client->request('GET', '/api/user?api_token='.$token);

#### Request Payload Item

Your application's API consumers can specify their token as a request payload item:

    $response = $client->request('POST', '/api/user', [
        'form_params' => [
            'api_token' => $token,
        ],
        'headers' => [
            'Accept' => 'application/json',
        ],
    ]);

#### Bearer Token

Your application's API consumers can specify their token as a Bearer token:

    $response = $client->request('POST', '/api/user', [
        'headers' => [
            'Accept' => 'application/json',
            'Authorization' => 'Bearer '.$token,
        ],
    ]);
