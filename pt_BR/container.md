# Service Container

- [Introdução](#introduction)
- [Atrelando (Binding)](#binding)
	- [Atrelando Interfaces Para Implementações](#binding-interfaces-to-implementations)
	- [Atrelamento Contextual](#contextual-binding)
	- [Tagging](#tagging)
- [Resolvendo Atrelamentos](#resolving)
- [Eventos do Container](#container-events)

<a name="introduction"></a>
## Introdução

O service container do Laravel é uma ferramenta poderosa para gerenciamento das dependências das suas classes e fazer injeção de dependência. Injetação de dependencia é um a frase bonita pra: as dependências das classes são "injetadas" via construtor ou, em alguns casos, nos métodos "setter".

Vamos ver um exemplo simples:

	<?php namespace App\Jobs;

	use App\User;
	use Illuminate\Contracts\Mail\Mailer;
	use Illuminate\Contracts\Bus\SelfHandling;

	class PurchasePodcast implements SelfHandling
	{
		/**
		 * The mailer implementation.
		 */
		protected $mailer;

		/**
		 * Create a new instance.
		 *
		 * @param  Mailer  $mailer
		 * @return void
		 */
		public function __construct(Mailer $mailer)
		{
			$this->mailer = $mailer;
		}

		/**
		 * Purchase a podcast.
		 *
		 * @return void
		 */
		public function handle()
		{
			//
		}
	}

Neste exemplo, a tarefa `PurchasePodcast` precisa enviar e-mails quando um podcast é comprado. Então, nós iremos **injetar** um serviço que é capaz de enviar e-mails. Como o serviço é injetado, nós poderemos facilmente trocá-lo por outra implementação. Nós também podemos facilmente fazer ["mock"](http://pt.wikipedia.org/wiki/Objeto_Mock) deles, ou criar uma implementação qualquer do Mailer enquanto testa a aplicação.

Um entendimento profundo do service container do Laravel é essencial para construir aplicações grandes e poderosas, e também para contribuir com o core do Laravel.

<a name="binding"></a>
## Atrelando (Binding)

Quase todos os atrelamentos de service container serão registrados dentro de um
[service providers](/docs/{{version}}/providers), então, todos os exemplos irão demonstrar como usar o container nesse contexto. Entretanto, não é necessário atrelar classes ao container se você só precisa da interface. O container não precisa ser instruído a como construir esses objetos, desde que ele possa automaticamente resolver o objeto "concreto" usando o serviço de reflexão do PHP.

Dentro de um service provider, você sempre tem acesso ao container através da variável da instância `$this->app`. Nós podemos registrar um atrelamento usando o método `bind`, passando a classe ou o nome da interface que nós queremos registrar dentro de um `Closure` (função anônima) que retorna uma instância da classe:

	$this->app->bind('HelpSpot\API', function ($app) {
		return new HelpSpot\API($app['HttpClient']);
	});

Note que o `Closure` recebe o próprio container como argumento. Nós podemos usá-lo para resolver sub-dependências do objeto que estamos construindo.

#### Atrelando um Singleton

O método `singleton` atrela uma classe ou interface ao container que será resolvida apenas uma vez, e então a mesma intância será retornada nas chamadas subsequentes ao container:

	$this->app->singleton('FooBar', function ($app) {
		return new FooBar($app['SomethingElse']);
	});

#### Atrelando Instâncias

Você também pode atrelar instâncias de objetos existentes ao container usando o método `instance`. A instância será sempre a mesma retornada em todas as chamadas subsequentes ao container:

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

<a name="binding-interfaces-to-implementations"></a>
### Atrelando Interfaces às Implementações

A característica mais poderosa do service container é sua habilidade de atrelar interfaces a uma implementação. Por exemplo, vamos assumir que nós temos uma interface `EventPusher` e uma implementação `RedisEventPusher`. Uma vez que nós construimos o `RedisEventPusher` como implementação da interface `EventPusher`, nós podemos registrá-la ao service container dessa forma:

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\RedisEventPusher');

Isso dirá ao container que deve injetar `RedisEventPusher` quando uma classe precisar da implementação de `EventPusher`. Agora nós podemos "type-hint" (forçar o tipo) a interface `EventPusher` num construtor ou qualquer local onde dependencias são injetadas pelo service container:

	use App\Contracts\EventPusher;

	/**
	 * Create a new class instance.
	 *
	 * @param  EventPusher  $pusher
	 * @return void
	 */
	public function __construct(EventPusher $pusher)
	{
		$this->pusher = $pusher;
	}

<a name="contextual-binding"></a>
### Atrelamento Contextual

As vezes você pode ter duas classes que utilizam a mesma interface, mas você gostaria de injetar diferentes implementações dentro dessa classe. Por exemplo, quando nosso sistema recebe uma nova Order (Encomenda), nós podemos querer enviar um evento via [PubNub](http://www.pubnub.com/) e também Pusher. O Laravel provê uma maneira simples e fluente de definir esse comportamento.

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give('App\Services\PubNubEventPusher');

Você pode até passar um `Closure` ao método `give`:

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give(function () {
	          		// Resolve dependency...
	          	});

<a name="tagging"></a>
### Tagging

Ocasionalmente, você pode precisar resolver todas as dependência de atrelamento de uma certa "categoria". Por exemplo, talvez você esteja construindo um agregador de relatório que recebe um array de muitas implementações da interface `Report`. Depois de registrar a implementação de `Report`, você pode atribuí-la a uma tag usando o método `tag`:

	$this->app->bind('SpeedReport', function () {
		//
	});

	$this->app->bind('MemoryReport', function () {
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');


Uma vez que os serviços receberam uma tag, você pode facilmente resolvê-las através do método  `tagged`:

	$this->app->bind('ReportAggregator', function ($app) {
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="resolving"></a>
## Resolvendo Atrelamentos

Existem várias maneiras de resolver algumas coisas fora do container. Primeiro, você pode usar o método `make`, que aceita o nome da classe ou interface que você quer resolver:

	$fooBar = $this->app->make('FooBar');

Segundo, você pode acessar o container como se fosse um array, desde que o seu PHP implemente a interface `ArrayAccess`:

	$fooBar = $this->app['FooBar'];

E por último, porém mais importante, você pode simplesmente usar o "type-hint" da dependência no construtor da classe que é resolvida pelo container, que são [controllers](/docs/{{version}}/controllers), [event listeners](/docs/{{version}}/events), [queue jobs](/docs/{{version}}/queues), [middleware](/docs/{{version}}/middleware) e outras. Na prática, é assim que a maioria de seus objetos são resolvidos pelo container.

O container irá automaticamente injetar a dependência que ele resolveu para suas classes. Por exemplo, você pode "type-hint" um repositório definido pela sua aplicação no construtor de um controller. O repositório será automaticamente resolvido e injetado nessa classe:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Users\Repository as UserRepository;

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

		/**
		 * Show the user with the given ID.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function show($id)
		{
			//
		}
	}

<a name="container-events"></a>
## Eventos do Container

O service container lança um evento toda vez que resolve um objeto. Você pode escutar esses eventos usando o método `resolving`:

	$this->app->resolving(function ($object, $app) {
		// Called when container resolves object of any type...
	});

	$this->app->resolving(function (FooBar $fooBar, $app) {
		// Called when container resolves objects of type "FooBar"...
	});

Como você viu, o objeto resolvido será automaticamente passado para o `Clojure`, permitindo que você configure qualquer propriedade adicional no objeto antes dele ser usado.
