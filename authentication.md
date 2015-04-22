# Authentication

- [Introdução](#introduction)
- [Autenticação de usuários](#authenticating-users)
- [Retrieving The Authenticated User](#retrieving-the-authenticated-user)
- [Protecting Routes](#protecting-routes)
- [HTTP Basic Authentication](#http-basic-authentication)
- [Password Reminders & Reset](#password-reminders-and-reset)
- [Social Authentication](#social-authentication)

<a name="introduction"></a>
## Introdução

Laravel faz a implementação de autenticação de maneira muito simples. Na verdade, quase tudo está previamente configurado para você. O arquivo de configuração da autenticação está localizado no diretório `config/auth.php`, o qual contém muitas opções bem documentadas para adequar o comportamento dos serviços de autenticação.

Por Padrão, Laravel adiciona um modelo `App\User` em seu diretório `app`. Este modelo poderá ser usado com o Driver de Autentição do Eloquent. 

<<<<<<< HEAD
Remember: when building the database schema for this model, make the password column at least 60 characters. Also, before getting started, make sure that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for "remember me" sessions being maintained by your application. This can be done by using `$table->rememberToken();` in a migration. The `scaffold:auth` command will generate these migrations for you.
=======
Lembre-se: quando estiver criando o schema do banco de dados para este modelo, faça com que a coluna password tenha no mínimo 60 caracteres. Também, antes de começar, garanta que a sua tabela `users` (ou equivalente) contenha uma coluna padrão Null `remember_token` com no mínimo 100 caracteres. Esta coluna será usada para armazenar um token de sessões "Lembre-me"  que são mantidas pela sua aplicação. Isto pode ser feito usando o método `$table->rememberToken();` na migração. Por padrão Laravel 5 realiza as migrações para estas colunas. 
>>>>>>> 5.0

Se sua aplicação não estiver utilizando o Eloquent, você pode usar o driver de autenticação `database` que usa o construtor de querys do Laravel. 

<a name="authenticating-users"></a>
## Autenticação de usuários

<<<<<<< HEAD
If you would like, Laravel can scaffold the necessary authentication controllers and views for your application using the `scaffold:auth` command:

	php artisan scaffold:auth

> **Note:** If you prefer to build your authentication system manually, check out the [Manual Authentication](#manual-authentication) section below.

This command will create new controllers, migrations, views, and Less / CSS files for providing authentication. The generated `AuthController` handles new user registration and "logging in", while the `PasswordController` contains the logic to help existing users reset their forgotten passwords.
=======
Laravel vem pré-configurado com duas autenticações relacionadas aos controladores (controllers). O `AuthController`gerencia o registro de novos usuários e a autenticação ("logging in"), enquanto o `PasswordController`contem a lógica para ajudar usuários existentes na recuperação de suas senhas esquecidas.
>>>>>>> 5.0

Cada um destes controladores (controllers) usa um trait para incluir os métodos necessários. Para muitas aplicações você não precisará modificá-los. As visões (views) que estes controladores (controllers) renderizam estão localizadas no diretório `resources/views/auth`. Você pode personaliza-las da maneira que melhor atender à sua aplicação.

### O Registro do usuário

<<<<<<< HEAD
To modify the form fields that are required when a new user registers with your application, you may modify the `AuthController` class. This class is responsible for validating and creating new users of your application.
=======
Para modificar os campos do formulário que são necessários quando um novo usuário se registra em sua aplicação, você pode alterar a classe `App\Services\Registrar`. Essta classe é responsável pela validação e criação de novos usuários em sua aplicação.
>>>>>>> 5.0

The `validator` method of the `AuthController` contains the validation rules for new users of the application, while the `create` method of the `AuthController` is responsible for creating new `User` records in your database. You are free to modify each of these methods as you wish.

<<<<<<< HEAD
<a name="manual-authentication"></a>
#### Manual Authentication

If you choose not to use the authentication scaffolding provided by `scaffold:auth`, you will need to manage the authentication of your users using the Laravel authentication classes directly. Don't worry, it's still a cinch! First, let's check out the `attempt` method:
=======
O método `validator` da classe `Registrar` contem as regras de validação para novos usuários na aplicação, enquanto o método `create` da classe `Registrar` é responsável pela criação do novo registro de `User` (usuário) no banco de dados. Você pode modificar cada um destes métodos para atender às necessidades de sua aplicação. `Registrar` é chamado por `AuthController` por meio dos métodos existentes no trait `AuthenticatesAndRegistersUsers`.

#### Autenticação manual

Se você optar por não utilizar a implementação do provedor `AuthController`, será necessário gerenciar a autenticação de seus usuários usando as classes de autenticação do Laravel diretamente. Não se preocupe, isto é simples. Primeiro vamos verificar um método  `attempt` (tentativa):
>>>>>>> 5.0

	<?php namespace App\Http\Controllers;

	use Auth;
	use Illuminate\Routing\Controller;

	class AuthController extends Controller {

		/**
		 * Handle an authentication attempt.
		 *
		 * @return Response
		 */
		public function authenticate()
		{
			if (Auth::attempt(['email' => $email, 'password' => $password]))
			{
				return redirect()->intended('dashboard');
			}
		}

	}

<<<<<<< HEAD
The `attempt` method accepts an array of key / value pairs as its first argument. The `password` value will be [hashed](/docs/master/hashing). The other values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the hashed `password` value passed to the method via the array. If the two hashed passwords match, a new authenticated session will be started for the user.
=======
O método `attempt` aceita um array de pares  chave / valor como seu primeiro argumento. O valor de `password` (senha) será [criptografado](docs/5.0/hashing). Os demais valores no array serão utilizados para encontrar o usuário no banco de dados. Assim, no exemplo acima, o usuário será recuperado pelo valor da coluna `email`. Se o usuário for encontrado, a senha criptografada armazanada no banco de dados, será comparada com o valor criptografado da senha passado pelo método na array. Se duas senhas criptografadas combinarem com a pesquisada, uma nova seção de usuário autenticado será iniciada.
>>>>>>> 5.0

O método `attempt` irá retornar `true` se a autenticação for realizada com sucesso. Caso contrário irá retornar `false`.

> **Nota:** neste exemplo, `email` não é uma opção obrigatória, ele é usado apenas como um exemplo. Você deverá utilizar qualquer nome de coluna correspondente a um "username" (nome de usuário) em seu banco de dados.

A função de redirecionamento `intended` redirecionará o usuário para a URL que ele estava tentando acessar antes de ser captuado pelo filtro de autenticação. Uma URI de retaguarda deve ser fornecida para o método caso o destino previamente tentado não estiver disponível.

#### Autenticando um usuário com condições

Você também pode adicionar condições extrar para a query de autenticação:

	if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1]))
	{
		// The user is active, not suspended, and exists.
	}

#### Determinando se um usuário está autenticado

Para determinar se um usuário já está autenticado (logged) em sua aplicação, pode-se utilizar o método `check`:

	if (Auth::check())
	{
		// The user is logged in...
	}

#### Authenticating A User And "Remembering" Them

If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method, which will keep the user authenticated indefinitely, or until they manually logout. Of course, your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token.

	if (Auth::attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

If you are "remembering" users, you may use the `viaRemember` method to determine if the user was authenticated using the "remember me" cookie:

	if (Auth::viaRemember())
	{
		//
	}

#### Authenticating Users By ID

To log a user into the application by their ID, use the `loginUsingId` method:

	Auth::loginUsingId(1);

#### Validating User Credentials Without Login

The `validate` method allows you to validate a user's credentials without actually logging them into the application:

	if (Auth::validate($credentials))
	{
		//
	}

#### Logging A User In For A Single Request

You may also use the `once` method to log a user into the application for a single request. No sessions or cookies will be utilized:

	if (Auth::once($credentials))
	{
		//
	}

#### Manually Logging In A User

If you need to log an existing user instance into your application, you may call the `login` method with the user instance:

	Auth::login($user);

This is equivalent to logging in a user via credentials using the `attempt` method.

#### Logging A User Out Of The Application

	Auth::logout();

Of course, if you are using the built-in Laravel authentication controllers, a controller method that handles logging users out of the application is provided out of the box.

#### Authentication Events

When the `attempt` method is called, the `auth.attempt` [event](/docs/master/events) will be fired. If the authentication attempt is successful and the user is logged in, the `auth.login` event will be fired as well.

<a name="retrieving-the-authenticated-user"></a>
## Retrieving The Authenticated User

Once a user is authenticated, there are several ways to obtain an instance of the User.

First, you may access the user from the `Auth` facade:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile()
		{
			if (Auth::user())
			{
				// Auth::user() returns an instance of the authenticated user...
			}
		}

	}

Second, you may access the authenticated user via an `Illuminate\Http\Request` instance:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Request $request)
		{
			if ($request->user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

Thirdly, you may type-hint the `Illuminate\Contracts\Auth\Authenticatable` contract. This type-hint may be added to a controller constructor, controller method, or any other constructor of a class resolved by the [service container](/docs/master/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\Authenticatable;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Authenticatable $user)
		{
			// $user is an instance of the authenticated user...
		}

	}

<a name="protecting-routes"></a>
## Protecting Routes

[Route middleware](/docs/master/middleware) can be used to allow only authenticated users to access a given route. Laravel provides the `auth` middleware by default, and it is defined in `app\Http\Middleware\Authenticate.php`. All you need to do is attach it to a route definition:

	// With A Route Closure...

	Route::get('profile', ['middleware' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// With A Controller...

	Route::get('profile', ['middleware' => 'auth', 'uses' => 'ProfileController@show']);

<a name="http-basic-authentication"></a>
## HTTP Basic Authentication

HTTP Basic Authentication provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` middleware to your route:

#### Protecting A Route With HTTP Basic

	Route::get('profile', ['middleware' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

By default, the `basic` middleware will use the `email` column on the user record as the "username".

#### Setting Up A Stateless HTTP Basic Filter

You may also use HTTP Basic Authentication without setting a user identifier cookie in the session, which is particularly useful for API authentication. To do so, [define a middleware](/docs/master/middleware) that calls the `onceBasic` method:

	public function handle($request, Closure $next)
	{
		return Auth::onceBasic() ?: $next($request);
	}

If you are using PHP FastCGI, HTTP Basic authentication may not work correctly out of the box. The following lines should be added to your `.htaccess` file:

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## Password Reminders & Reset

### Model & Table

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this on each application, Laravel provides convenient methods for sending password reminders and performing password resets.

To get started, verify that your `User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. Of course, the `User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

#### Generating The Reminder Table Migration

Next, a table must be created to store the password reset tokens. The migration for this table is included with Laravel out of the box, and resides in the `database/migrations` directory. So all you need to do is migrate:

	php artisan migrate

### Password Reminder Controller

Laravel also includes an `Auth\PasswordController` that contains the logic necessary to reset user passwords. We've even provided views to get you started! The views are located in the `resources/views/auth` directory. You are free to modify these views as you wish to suit your own application's design.

Your user will receive an e-mail with a link that points to the `getReset` method of the `PasswordController`. This method will render the password reset form and allow users to reset their passwords. After the password is reset, the user will automatically be logged into the application and redirected to `/home`. You can customize the post-reset redirect location by defining a `redirectTo` property on the `PasswordController`:

	protected $redirectTo = '/dashboard';

> **Note:** By default, password reset tokens expire after one hour. You may change this via the `reminder.expire` option in your `config/auth.php` file.

<a name="social-authentication"></a>
## Social Authentication

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). **Socialite currently supports authentication with Facebook, Twitter, Google, GitHub and Bitbucket.**

To get started with Socialite, include the package in your `composer.json` file:

	"laravel/socialite": "~2.0"

Next, register the `Laravel\Socialite\SocialiteServiceProvider` in your `config/app.php` configuration file. You may also register a [facade](/docs/master/facades):

	'Socialize' => 'Laravel\Socialite\Facades\Socialite',

You will need to add credentials for the OAuth services your application utilizes. These credentials should be placed in your `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `google`, or `github`, depending on the providers your application requires. For example:

	'github' => [
		'client_id' => 'your-github-app-id',
		'client_secret' => 'your-github-app-secret',
		'redirect' => 'http://your-callback-url',
	],

Next, you are ready to authenticate users! You will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. Here's an example using the `Socialize` facade:

	public function redirectToProvider()
	{
		return Socialize::with('github')->redirect();
	}

	public function handleProviderCallback()
	{
		$user = Socialize::with('github')->user();

		// $user->token;
	}

The `redirect` method takes care of sending the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider. Before redirecting the user, you may also set "scopes" on the request:

	return Socialize::with('github')->scopes(['scope1', 'scope2'])->redirect();

Once you have a user instance, you can grab a few more details about the user:

#### Retrieving User Details

	$user = Socialize::with('github')->user();

	// OAuth Two Providers
	$token = $user->token;

	// OAuth One Providers
	$token = $user->token;
	$tokenSecret = $user->tokenSecret;

	// All Providers
	$user->getId();
	$user->getNickname();
	$user->getName();
	$user->getEmail();
	$user->getAvatar();
