# HTTP Middleware

- [Introdução](#introduction)
- [Definindo Middleware](#defining-middleware)
- [Registrando Middleware](#registering-middleware)
- [Parâmetros do Middleware](#middleware-parameters)
- [Terminable Middleware](#terminable-middleware)

<a name="introduction"></a>
## Introdução

HTTP middleware fornece um mecanismo conveniente para filtragem das requisições HTTP que entram em sua aplicação. Por exemplo, Laravel inclui um middleware que verifica se o usuário de sua aplicação está autenticado. Se o usuário não estiver autenticado, o middleware irá redirecionar o usuário para a tela de login. No entanto, se o usuário é autenticado, o middleware irá permitir que a requisição siga dentro da aplicação.

Claro, middlewares adicionais podem ser escritos para realizar uma variedade de tarefas além da autenticação. Um CORS middleware pode ser responsável por adicionar os headers apropriados para todas as responses que saem da sua aplicação. Um logging middleware pode logar todas as requisições que chegam em sua aplicação.

Existem vários middlewares já inclusos no framework Laravel, incluindo middleware para manutenção, autenticação, proteção CSRF, entre outros. Todos esses middlewares estão localizados no diretório `app/Http/Middleware`.

<a name="defining-middleware"></a>
## Definindo Middleware

Para criar um novo middleware, use o comando `make:middleware` do Artisan:

	php artisan make:middleware OldMiddleware

Este comando irá colocar a nova classe `OldMiddleware` em seu diretório `app/Http/Middleware`. Neste middleware, vamos somente permitir o acesso a uma rota se o `age` fornecido for maior que 200. Caso contrário, iremos redirecionar os usuários de volta a URI "home".

	<?php namespace App\Http\Middleware;

	use Closure;

	class OldMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') < 200) {
				return redirect('home');
			}

			return $next($request);
		}

	}

Como você pode ver, se o `age` fornecido for menor que `200`, o middleware irá retornar um HTTP redirect para o cliente; caso contrário, a request será passada adiante na sua aplicação. Para repassar a request dentro da aplicação (permitindo que o middleware "passe adiante"), basta chamar o callback `$next` com a `$request`.

É melhor entender os middlewares como uma série de "camadas" por onde as requests HTTP tem que passar antes de alcançar a aplicação. Cada camada pode examinar a request e até mesmo rejeitá-la inteiramente.

### *Before* / *After* Middleware

Se um middleware roda antes ou depois de uma request, depende do próprio middleware. Por exemplo, o middleware a seguir performaria alguma tarefa **antes** da request ser tratada pela aplicação:

	<?php namespace App\Http\Middleware;

	use Closure;

	class BeforeMiddleware
	{
		public function handle($request, Closure $next)
		{
			// Perform action

			return $next($request);
		}
	}

No entanto, este middleware executaria uma tarefa **depois** da request ser tratada pela aplicação:

	<?php namespace App\Http\Middleware;

	use Closure;

	class AfterMiddleware
	{
		public function handle($request, Closure $next)
		{
			$response = $next($request);

			// Perform action

			return $response;
		}
	}

<a name="registering-middleware"></a>
## Registrando Middleware

### Global Middleware

Se você quer que um middleware seja executado durante qualquer requisição HTTP para sua aplicação, basta listar a classe do middleware na propriedade `$middleware` da sua classe `app/Http/Kernel.php`.

### Atribuindo Middlewares às Rotas

Se você gostaria de atribuir middleware a rotas específicas, você deve primeiro atribuir uma chave para o middleware no seu arquivo `app/Http/Kernel.php`. Por padrão, a propriedade `$routeMiddleware` dessa classe contém as entradas para o middleware incluido no Laravel. Para adicionar a sua própria, basta adicioná-la a essa lista e atribuir a chave de sua escolha. Por exemplo:

	// Within App\Http\Kernel Class...

    protected $routeMiddleware = [
        'auth' => 'App\Http\Middleware\Authenticate',
        'auth.basic' => 'Illuminate\Auth\Middleware\AuthenticateWithBasicAuth',
        'guest' => 'App\Http\Middleware\RedirectIfAuthenticated',
    ];

Uma vez que o middleware esteja definido no HTTP kernel, você deve usar a chave `middleware` no array de opções da rota:

	Route::get('admin/profile', ['middleware' => 'auth', function () {
		//
	}]);

<a name="middleware-parameters"></a>
## Parâmetros do Middleware

Middleware pode também receber parâmetros personalizados adicionais. Por exemplo, se sua aplicação precisa verificar que o usuário autenticado tem um determinado "papel" antes de executar uma ação, você pode criar uma `RoleMiddleware` que recebe o nome do papel do usuário como um argumento adicional.

Parâmetros adicionais do middleware serão passados para o middleware depois do argumento `$next`:

	<?php namespace App\Http\Middleware;

	use Closure;

	class RoleMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @param  string  $role
		 * @return mixed
		 */
		public function handle($request, Closure $next, $role)
		{
			if (! $request->user()->hasRole($role)) {
				// Redirect...
			}

			return $next($request);
		}

	}

Parâmetros do Middleware podem ser especificados na definição de uma rota separando o nome do middleware e seus parâmetros com `:`. Múltiplos parâmetros devem ser separados por vírgulas:

	Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
		//
	}]);

<a name="terminable-middleware"></a>
## Terminable Middleware

Alguma vezes um middleware pode precisar realizar algum trabalho depois do HTTP response já ter sido enviado ao browser. Por exemplo, o "session" middleware incluído no Laravel escreve os dados da sessão para armazenamento _depois_ da resposta ter sido enviada ao navegador. Para conseguir fazer isso, defina o middleware como "terminable" adicionando um método `terminate` para o middleware:

	<?php namespace Illuminate\Session\Middleware;

	use Closure;

	class StartSession
	{
		public function handle($request, Closure $next)
		{
			return $next($request);
		}

		public function terminate($request, $response)
		{
			// Store the session data...
		}
	}

O método `terminate` deve receber tanto a requisição (request) quanto a resposta (response). Uma vez definido um terminable middleware, você deve adicioná-lo a sua lista global de middlewares no seu HTTP kernel.
