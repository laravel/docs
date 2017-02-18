# HTTP Controllers

- [Introdução](#introduction)
- [O Básico Controllers](#basic-controllers)
- [Controller Middleware](#controller-middleware)
- [Controllers de Recursos RESTful](#restful-resource-controllers)
	- [Rotas Parciais de Recursos](#restful-partial-resource-routes)
	- [Nomeando Rotas de Recurso](#restful-naming-resource-routes)
	- [Recursos Aninhados](#restful-nested-resources)
	- [Complementando os Controllers de Resource](#restful-supplementing-resource-controllers)
- [Controllers Implícitos](#implicit-controllers)
- [Injeção de Dependência & Controllers](#dependency-injection-and-controllers)
- [Fazendo Cache das Rotas](#route-caching)

<a name="introduction"></a>
## Introdução

Ao invés de definir toda a lógica das suas requisições em um único arquivo `routes.php`, você pode organizar esse comportamento em classes Controller. Elas podem agrupar a lógica das suas requisições HTTP e ficam, normalmente, no diretório `app/Http/Controllers`.

<a name="basic-controllers"></a>
## O Básico dos Controllers

Aqui um exemplo básico de uma classe Controller. Todos os controllers do Laravel devem estender a classe controller base incluída por padrão na instalação:

	<?php namespace App\Http\Controllers;

	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			return view('user.profile', ['user' => User::findOrFail($id)]);
		}
	}

Nós podemos definir uma rota para a ação do controller da seguinte forma:

	Route::get('user/{id}', 'UserController@showProfile');

Agora, quando uma requisição combinar com a URI especificada na rota, o método `showProfile` no do controller `UserController` será executado. E é claro, os parâmetros também serão passados para o método.

#### Controllers & Namespaces

É muito importante notar que nós não precisamos especificar o namespace completo do controller. Nós só definimos uma parte do nome que vem depois do namespace principal `App\Http\Controllers`. Por padrão, o `RouteServiceProvider` lerá o arquivo `routes.php` dentro de um grupo que contém o namespace principal dos controllers.

Se você escolher organizar seus controllers usando namespaces em subdiretórios do namespace `App\Http\Controllers`, você pode simplesmente especificar o nome da classe relativo ao namespace principal `App\Http\Controllers`. Então, se o namespace completo do seu controller for `App\Http\Controllers\Photos\AdminController`, você pode registrar uma rota para ele da seguinte maneira:

	Route::get('foo', 'Photos\AdminController@method');

#### Nomeando as Rotas dos Controllers

Igual a um Closure de rota, você pode especificar nomes para rotas de controllers:

	Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

Uma vez que você deu um nome para uma rota de controller, você pode facilmente gerar URLs para ela da seguinte maneira:

	$url = route('name');

Você também pode usar o nome do método do controller para gerar URLs, utilizando a função utilitária `action`:

	$url = action('FooController@method')

<a name="controller-middleware"></a>
## Controller Middleware

Você pode atribuir um [Middleware](/docs/{{version}}/middleware) para um controller assim:

	Route::get('profile', [
		'middleware' => 'auth',
		'uses' => 'UserController@showProfile'
	]);

Entretanto, é mais conveniente especificar o middleware no construtor do controller. Usando o método `middleware` a partir do construtor você pode facilmente atribuir um middleware ao controller. Você pode até restringir o middleware para certos métodos do controller:

	class UserController extends Controller
	{
		/**
		 * Instantiate a new UserController instance.
		 *
		 * @return void
		 */
		public function __construct()
		{
			$this->middleware('auth');

			$this->middleware('log', ['only' => ['fooAction', 'barAction']]);

			$this->middleware('subscribed', ['except' => ['fooAction', 'barAction']]);
		}
	}

<a name="restful-resource-controllers"></a>
## RESTful Resource Controllers

Resource controller torna menos dolorosa a construção de recursos RESTful. Por exemplo, você pode querer criar um controller que recebe requisições HTTP para armazenar fotos. Usando o comando Artisan `make:controller` você pode rapidamente criar esse controller:

	php artisan make:controller PhotoController

O comando Artisan ira gerar um arquivo controller em `app/Http/Controllers/PhotoController.php`. O controller conterá métodos para cada operação disponvível para o recurso (resource).

Em seguida, você pode registrar uma rota de controller de recurso da seguinte forma:

	Route::resource('photo', 'PhotoController');

Essa única declaração da rota cria multiplas ações RESTful para o recurso fotos (photos). O controller gerado conterá métodos para cada uma dessas ações, incluindo notas informando a você quais URIs e verbos eles lidam.

#### Ações do Controller de Recursos

Verbo     | Caminho               | Ação (Action)| Nome da Rota
----------|-----------------------|--------------|---------------------
GET       | `/photo`              | index        | photo.index
GET       | `/photo/create`       | create       | photo.create
POST      | `/photo`              | store        | photo.store
GET       | `/photo/{photo}`      | show         | photo.show
GET       | `/photo/{photo}/edit` | edit         | photo.edit
PUT/PATCH | `/photo/{photo}`      | update       | photo.update
DELETE    | `/photo/{photo}`      | destroy      | photo.destroy

<a name="restful-partial-resource-routes"></a>
#### Rotas Parciais de Recursos

Quando declara uma rota de recurso você pode especificar um subconjunto de ações que aquela rota lidará:

	Route::resource('photo', 'PhotoController',
					['only' => ['index', 'show']]);

	Route::resource('photo', 'PhotoController',
					['except' => ['create', 'store', 'update', 'destroy']]);

<a name="restful-naming-resource-routes"></a>
#### Nomeando Rotas de Recursos

Por padrão, todos as ações dos controllers de recursos tem um nome, entretanto, você pode sobrescrever esses nomes passando um array `names` com suas opções:

	Route::resource('photo', 'PhotoController',
					['names' => ['create' => 'photo.build']]);

<a name="restful-nested-resources"></a>
#### Recursos Aninhados

Algumas vezes você pode precisar definir rotas para um recurso "aninhado". Por exemplo, o recurso foto (photo) pode ter multiplos comentários (comments) que devem ser atribuidos à foto. Para aninhar esse controller de recurso, use a notação "dot" (ponto) na declaração da rota:

	Route::resource('photos.comments', 'PhotoCommentController');

Essa rota registrará um recurso aninhado que pode ser acessado com URLs da seguinte forma: `photos/{photos}/comments/{comments}`.

	<?php namespace App\Http\Controllers;

	use App\Http\Controllers\Controller;

	class PhotoCommentController extends Controller {

		/**
		 * Show the specified photo comment.
		 *
		 * @param  int  $photoId
		 * @param  int  $commentId
		 * @return Response
		 */
		public function show($photoId, $commentId)
		{
			//
		}

	}

<a name="restful-supplementing-resource-controllers"></a>
#### Complementando os Resource Controllers

Se for necessário adicionar rotas ao seu recurso controller além das rotas padrões, você pode definir essas rotas antes da chamada ao `Route::resource`. De outra forma as rotas definidas pelo `resource` poderão ter precedência maior do que as que você definiu:

	Route::get('photos/popular', 'PhotoController@method');

	Route::resource('photos', 'PhotoController');

<a name="implicit-controllers"></a>
## Controllers Implícitos

O Laravel permite que você defina facilmente rotas únicas para lidar com cada método no controller. Primeiro, defina a rota usando `Route::controller`, esse método aceita dois argumentos, o primeiro é a URI, enquanto o segundo é o nome da classe do controller:

	Route::controller('users', 'UserController');

Em seguida, simplesmente adicione métodos ao seu controller. O nome dos métodos devem começar com o verbo HTTP que eles respondem seguidos pelo título da URI:

 	<?php namespace App\Http\Controllers;

	class UserController extends Controller
	{
		/**
		 * Responds to requests to GET /users
		 */
		public function getIndex()
		{
			//
		}

		/**
		 * Responds to requests to GET /users/show/1
		 */
		public function getShow($id)
		{
			//
		}

		/**
		 * Responds to requests to GET /users/admin-profile
		 */
		public function getAdminProfile()
		{
			//
		}

		/**
		 * Responds to requests to POST /users/profile
		 */
		public function postProfile()
		{
			//
		}
	}

Como pode ver no exemplo acima, o método `index` responderá a URI principal do controller, que nesse caso é `users`. Observe também que o camel-case "AdminProfile" se tornará "admin-profile" e ficará disponível, nesse caso, como "/users/admin-profile".

#### Atribuindo rotas nomeadas

Se você gostaria de [nomear](/docs/{{version}}/routing#named-routes) algumas das suas rotas para controller, você pode passar um array de nomes como terceiro arguemnto ao método `controller`:

	Route::controller('users', 'UserController', [
		'getShow' => 'user.show',
	]);

<a name="dependency-injection-and-controllers"></a>
## Injeção de Dependência & Controllers

#### Injeção no Construtor

O  [service container](/docs/{{version}}/container) do Laravel é usado para resolver todos os controllers do Laravel. Como resultado, você pode indicar o tipo (type-hint) de qualquer dependência que seu controller possa precisar. As dependências serão automáticamente resolvidas e injetadas na instância do construtor:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\UserRepository;

	class UserController extends Controller
	{
		/**
		 * The user repository instance.
		 */
		protected $users;

		/**
		 * Create a new controller instance.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}
	}

E é claro, você também pode indicar o tipo de qualquer [contrato do Laravel](/docs/{{version}}/contracts). Se o container pode ser resolvido, você pode indicá-lo.


#### Injeção no Método

Você também pode injetar dependências nos métodos das ações dos seus controllers. Por exemplo, vamos indicar o tipo `Illuminate\Http\Request` em um dos nossos métodos:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}
	}

Se o método do seu controller também espera parâmetros da rota, simplesmente liste os argumentos da rota depois das suas dependências:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the specified user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}
	}

<a name="route-caching"></a>
## Fazendo Cache das Rotas

Se sua aplicação é está usando exclusivamente rotas baseadas em controllers, você pode usar o cache de rotas do Laravel. Usando o cache você reduz drásticamente o tempo gasto para registrar todas as rotas da sua aplicação. Em alguns casos, o registro das suas rotas pode ser 100x mais rápido! Para gerar o cache das rotas, basta executar o comando Artisan `route:cache`:

	php artisan route:cache

E é isso, suas rotas estaram um arquivo de cache e ele será usado no lugar de `app/Http/routes.php`. **Mas lembre-se, se você adicionar qualquer nova rota você precisará refazer o cache das rotas.** Por causa disso, você só deve executar o comando `route:cache` durante o deploy do seu projeto.

Para remover o arquivo de cache das rotas sem gerar um novo cache, use o comando Artisan `route:clear`:

	php artisan route:clear
