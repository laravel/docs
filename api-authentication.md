# API Authentication

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Database Migrations](#database-preparation)
- [Generating Tokens](#generating-tokens)
- [Protecting Routes](#protecting-routes)
- [Passing Tokens In Requests](#passing-tokens-in-requests)

<a name="introduction"></a>
## Introduction

By default, Laravel ships with a simple solution to API authentication via a random token assigned to each user of your application. In your `config/auth.php` configuration file, an `api` guard is already defined and utilizes a `token` driver. This driver is responsible for inspecting the API token on the incoming request and verifying that it matches the user's assigned token in the database.

> **Note:** While Laravel ships with a simple, token based authentication guard, we strongly recommend you consider using [Laravel Passport](/docs/{{version}}/passport) for robust, production applications that offer API authentication.

<a name="configuration"></a>
## Configuration

<a name="database-preparation"></a>
### Database Preparation

Before using the `token` driver, you will need to [create a migration](/docs/{{version}}/migrations) which adds an `api_token` column to your `users` table:

    Schema::table('users', function ($table) {
        $table->string('api_token', 60)->after('password')
                            ->unique()
                            ->nullable()
                            ->default(null);
    });

Once the migration has been created, run the `migrate` Artisan command.

<a name="generating-tokens"></a>
## Generating Tokens

Once the `api_token` column has been added to your `users` table, you are ready to assign random API tokens to each user that registers with your application. You should assign these tokens when a `User` model is created for the user during registration. When using the [authentication scaffolding](/docs/{{version}}/authentication#authentication-quickstart) provided by the `make:auth` Artisan command, this may be done in the `create` method of the `RegisterController`:

    use Illuminate\Support\Str;
    use Illuminate\Support\Facades\Hash;

    /**
     * Create a new user instance after a valid registration.
     *
     * @param  array  $data
     * @return \App\User
     */
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

Laravel includes an [authentication guard](/docs/{{version}}/authentication#adding-custom-guards) that will automatically validate API tokens on incoming requests. You only need to specify the `auth:api` middleware on any route that requires a valid access token:

    use Illuminate\Http\Request;

    Route::middleware('auth:api')->get('/user', function(Request $request) {
        return $request->user();
    });

<a name="passing-tokens-in-requests"></a>
## Passing Tokens In Requests

There are several ways of passing the API token to your application. We'll discuss each of these approaches while using the Guzzle HTTP library to demonstrate their usage. You may choose any of these approaches based on the needs of your application.

#### Query String

Your application's API consumers may specify their token as an `api_token` query string value:

    $response = $client->request('GET', '/api/user?api_token='.$token);

#### Request Payload

Your application's API consumers may include their API token in the request's form parameters as an `api_token`:

    $response = $client->request('POST', '/api/user', [
        'headers' => [
            'Accept' => 'application/json',
        ],
        'form_params' => [
            'api_token' => $token,
        ],
    ]);

#### Bearer Token

Your application's API consumers may provide their API token as a `Bearer` token in the `Authorization` header of the request:

    $response = $client->request('POST', '/api/user', [
        'headers' => [
            'Authorization' => 'Bearer '.$token,
            'Accept' => 'application/json',
        ],
    ]);
