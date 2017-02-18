# HTTP Routing

- [Básico sobre Rotas](#basic-routing)
- [Parâmetros](#route-parameters)
	- [Parâmetros Obrigatórios](#required-parameters)
	- [Parâmetros Opcionais](#parameters-optional-parameters)
	- [Restrições por Expressões Regulares](#parameters-regular-expression-constraints)
- [Rotas Nomeadas](#named-routes)
- [Grupo de Rotas](#route-groups)
	- [Middleware](#route-group-middleware)
	- [Namespaces](#route-group-namespaces)
	- [Rotas e sub-domínios](#route-group-sub-domain-routing)
	- [Prefixos para Rotas](#route-group-prefixes)
- [Proteção CSRF](#csrf-protection)
	- [Introdução](#csrf-introduction)
	- [Excluindo URIs](#csrf-excluding-uris)
	- [X-CSRF-Token](#csrf-x-csrf-token)
	- [X-XSRF-Token](#csrf-x-xsrf-token)
- [Spoofing do Método do Formulário](#form-method-spoofing)
- [Disparando Erros 404](#throwing-404-errors)

<a name="basic-routing"></a>
## O Básico das Rotas

Você vai definir a maioria das rotas para a sua aplicação no arquivo `app/Http/routes.php`, que é carregado por `App\Providers\RouteServiceProvider`. As rotas básicas no Laravel aceitam um URL e uma `Closure`:

	Route::get('/', function () {
		return 'Olá Mundo';
	});

	Route::post('foo/bar', function () {
		return 'Olá Mundo';
	});

	Route::put('foo/bar', function () {
		//
	});

	Route::delete('foo/bar', function () {
		//
	});

#### Registrando uma rota para múltiplos verbos HTTP

Às vezes você pode querer registrar uma rota que responderá a vários verbos HTTP. Você pode fazer isso usando o método `match` no [facade](/docs/{{version}}/facades) `Route`:

	Route::match(['get', 'post'], '/', function () {
		return 'Olá Mundo';
	});

Ou, você pode escolher registrar uma rota que responde a todos os verbos HTTP usando o método `any`:

	Route::any('foo', function () {
		return 'Olá Mundo';
	});

#### Gerando URLs para Rotas

Você pode gerar URLs para rotas na sua aplicação usando a função utilitária `url`:

	$url = url('foo');

<a name="route-parameters"></a>
## Parâmetros para Rotas

<a name="required-parameters"></a>
### Parâmetros Requeridos para Rotas

Claro que, às vezes você terá que capturar pedaços da URI dentro de sua rota. Por exemplo, você pode precisar capturar o ID do usuário da URL. Você pode capturar o ID do usuário através da definição dos parâmetros da rota:

	Route::get('user/{id}', function ($id) {
		return 'User '.$id;
	});

Você pode definir quantos parâmetros sua rota precisar:

	Route::get('posts/{post}/comments/{comment}', function ($post, $comment) {
		//
	});

Os parâmetros de rota devem ser colocados dentro de chaves. Os parâmetros serão passados em uma `Closure`, quando a rota é executada.

> **Nota:** Os parâmetros não podem conter o caracter `-`. No lugar dele você pode usar o caractere (`_`).

<a name="parameters-optional-parameters"></a>
### Parâmetros Opcionais

Ocasionalmente, você pode precisar especificar um parâmetro de rota, mas tornar a presença desse parâmetro opcional na rota. Você pode fazer isso, colocando uma `?` após o nome do parâmetro:

	Route::get('user/{name?}', function ($name = null) {
		return $name;
	});

	Route::get('user/{name?}', function ($name = 'John') {
		return $name;
	});

<a name="parameters-regular-expression-constraints"></a>
### Restrições por Expressões Regulares

Você pode restringir o formato dos seus parâmetros de rota usando o método `where` em uma instância de rota. O método `where` aceita o nome do parâmetro e uma expressão regular que define como o parâmetro deve ser restringido:

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
#### Constantes Globais

Se você precissar verificar em muitas rotas um parâmetro com uma expressão regular, você pode usar o método `pattern`. Você deve definir esses padrões no método `boot` de seus `RouteServiceProvider`:

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

Definido o padrão, ele é automaticamente aplicado para todas as rotas usando o mesmo parâmetro:

	Route::get('user/{id}', function ($id) {
		// Somente direciona se {id} for um número.
	});

<a name="named-routes"></a>
## Nomes para Rotas

Rotas nomeadas permitem a geração convenientemente de URLs ou redirecionamentos para uma rota específica. Você pode especificar um nome para a rota utilizando `as` ao definir a rota:

	Route::get('user/profile', ['as' => 'profile', function () {
		//
	}]);

Você também pode especificar nomes de rota para ações do controller:

	Route::get('user/profile', [
		'as' => 'profile', 'uses' => 'UserController@showProfile'
	]);

Depois de atribuir um nome a uma determinada rota, você pode usar o nome da rota ao gerar URLs ou redirecionar através da função `route`:

	$url = route('profile');

	$redirect = redirect()->route('profile');

Se a rota tem parâmetros definidos, você pode passar os parâmetros como o segundo argumento para a função `route`. Os parâmetros dados serão automaticamente inserido na URL:

	Route::get('user/{id}/profile', ['as' => 'profile', function ($id) {
		//
	}]);

	$url = route('profile', ['id' => 1]);

<a name="route-groups"></a>
## Grupos para Rotas

Grupos de rotas permitem que você compartilhe atributos de rotas, como middleware ou namespaces, para um grande número de rotas sem a necessidade de definir os atributos em cada rota individualmente. Atributos compartilhados são especificados em um formato de array, enviados pelo método `Route::group`.

Para saber mais sobre grupos de rotas, vamos percorrer vários casos de uso comuns para o recurso.

<a name="route-group-middleware"></a>
### Middleware

Para atribuir um middleware para todas as rotas dentro de um grupo, você pode usar a chave `middleware` no array passado. Middlewares serão executadas na ordem que você definir esse array:

	Route::group(['middleware' => 'auth'], function () {
		Route::get('/', function ()	{
			// Uses Auth Middleware
		});

		Route::get('user/profile', function () {
			// Uses Auth Middleware
		});
	});

<a name="route-group-namespaces"></a>
### Namespaces

Outro caso de uso comum para grupos de rotas é atribuir o mesmo namespace PHP a um grupo de controllers. Você pode usar o parâmetro `namespace` em seu array para especificar o namespace para todos os controllers dentro do grupo:

	Route::group(['namespace' => 'Admin'], function()
	{
		// Controllers Within The "App\Http\Controllers\Admin" Namespace

		Route::group(['namespace' => 'User'], function()
		{
			// Controllers Within The "App\Http\Controllers\Admin\User" Namespace
		});
	});

Lembre, por padrão, o `RouteServiceProvider` inclui seu arquivo `routes.php` dentro de um namespace, permitindo-lhe registar as rotas do controller sem especificar o prefixo `App\Http\Controllers`. Então, só é preciso especificar o nome que vem após a base `App\Http\Controllers`.

<a name="route-group-sub-domain-routing"></a>
### Rotas e Subdomínios

Grupos de rota também podem ser utilizados para encaminhar subdomínios. Subdomínios podem ser atribuídos nos parâmetros de rota como URIs, permitindo que você capture uma parte do subdomínio para uso em sua rota ou controller. O subdomínio pode ser especificado usando a chave `domain` no array:

	Route::group(['domain' => '{account}.myapp.com'], function () {
		Route::get('user/{id}', function ($account, $id) {
			//
		});
	});

<a name="route-group-prefixes"></a>
### Prefixos para Rotas

Você pode usar o parâmetro `prefix` do array passado ao método `group` para prefixar cada rota no grupo com um determinado URI. Por exemplo, você pode querer prefixar todos os URIs de rota dentro do grupo com `admin`:

	Route::group(['prefix' => 'admin'], function () {
		Route::get('users', function ()	{
			// Essa rota terá a URL "/admin/users"
		});
	});

Você também pode usar o parâmetro `prefix` para especificar parâmetros comuns para as suas rotas agrupadas:

	Route::group(['prefix' => 'accounts/{account_id}'], function () {
		Route::get('detail', function ($account_id)	{
			// Handles Requests To admin/user
		});
	});

<a name="csrf-protection"></a>
## Proteção CSRF

<a name="csrf-introduction"></a>
### Introdução

O Laravel torna fácil proteger sua aplicação de ataques [cross-site request forgeries](http://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF). CSRF é uma forma de explorar maliciosamente comandos (requisições) em nome do usuário autorizado.

Laravel gera automaticamente um "token" CSRF para cada sessão do usuário ativo. Esse token é utilizado para verificar se o usuário autenticado é o único que realmente está fazendo as solicitações para o aplicativo. Para gerar um campo de entrada oculto `_token` contendo o token CSRF, você pode usar a função utilitária `csrf_field`:

	<?php echo csrf_field(); ?>

O utilitário `csrf_field` gera o seguinte html:

	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

E claro, usando no [template blade](/docs/{{version}}/templates):

	{!! csrf_field() !!}

Você não precisa verificar manualmente o token CSRF nos verbos HTTP: POST, PUT ou DELETE. O [HTTP middleware](/docs/{{version}}/middleware) `VerifyCsrfToken` irá verificar o token na entrada do pedido corresponde ao token armazenado na sessão.

<a name="csrf-excluding-uris"></a>
### Excluindo URLs dda Proteção CSRF

Às vezes você pode querer excluir um conjunto de URIs de proteção CSRF. Por exemplo, se você estiver usando [Stripe](https://stripe.com) para processar pagamentos e estão utilizando seu sistema webhook, você terá que excluir as rotas do webhook da proteção CSRF de Laravel.

Você pode excluir URIs, adicionando-as a propriedade `$except` do middleware `VerifyCsrfToken`:

	<?php namespace App\Http\Middleware;

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

Além de verificar se token CSRF foi enviado via POST, o middleware `VerifyCsrfToken` também irá verificar o `X-CSRF-TOKEN`. Você poderia, por exemplo, armazenar o token em um tag "meta":

	<meta name="csrf-token" content="{{ csrf_token() }}">

Depois de ter criado a tag `meta`, você pode instruir uma biblioteca como jQuery para adicionar o token para todos os cabeçalhos de solicitação. Isto proporciona, conveniente proteção CSRF simples para seus aplicativos baseados em AJAX:

	$.ajaxSetup({
			headers: {
				'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
			}
	});

<a name="csrf-x-xsrf-token"></a>
### X-XSRF-TOKEN

Laravel também armazena o token `CSRF` em um cookie `XSRF-TOKEN`. Você pode usar o valor do cookie para definir o cabeçalho de solicitação `X-XSRF-TOKEN`. Alguns frameworks JavaScript, como angular, fazem isso automaticamente para você. É improvável que você irá precisar usar esse valor manualmente.

<a name="form-method-spoofing"></a>
## Burlando o Métodos do Formulário

Formulários HTML não suportam os verbos `PUT`, ações `PATCH` ou `DELETE`. Assim, ao definir rotas `PUT`, `PATCH` ou `DELETE` em um formulário HTML, você precisará adicionar um campo `_method` oculto ao formulário. O valor enviado com o campo `_method` vai ser usado como o nome do verbo HTTP:

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
	</form>

<a name="throwing-404-errors"></a>
## Disparando Erros 404

Existem duas maneiras de disparar manualmente um erro 404 a partir de uma rota. Primeiro, você pode usar a função utilitária `abort`. O `abort` simplesmente lança uma exceção `Symfony\Component\HttpFoundation\Exception\HttpException` com o código de status especificado:

	abort(404);

Em segundo lugar, você pode lançar manualmente uma instância de `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

Mais informações sobre como manusear exceções 404 e usar respostas personalizadas para esses erros podem ser encontrados aqui [Errors](/docs/{{version}}/errors#http-exceções).
