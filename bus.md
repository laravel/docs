# Command Bus

- [Introdução](#introduction)
- [Criando Comandos](#creating-commands)
- [Dispatching Commands](#dispatching-commands)
- [Queued Commands](#queued-commands)
- [Command Pipeline](#command-pipeline)

<a name="introduction"></a>
## Introdução

O comando Bus do Laravel é um método conveniente de encapsulamento de tarefas que sua aplicação precisa executar em um "commands"(comando) simples, e facil de entender. Para nos ajudar a entender o propósito dos comandos, vamos imaginar que estamos construindo uma aplicação que permita que os usuários comprem podcasts.

Quando o usuário compra podcast, existem uma variedade de coisas que precisam acontecer. Por exemplo, nos podemos necessitar carregar o cartão de crédito do usuário, registrar a compra no banco de dados, e mandar um e-mail de confirmação de compra. Talvez, também precisaremos realizar algum tipo de validação para saber ser o usuário é autorizado a comprar podcasts. 

Nos podemos colocar toda essa lógica dentro do método do controlador(controller); contudo, isso teria várias desvantagens. A primeira disvatagem é que nosso controlador provavelmente lida com várias outras ações de entrada HTTP, e incluir uma lógica complicada em cada método no controlador logo irá inchar nosso controlador(controller) e com isso fazer com que o mesmo seja dificil de ler. Segundo, é difícil de reusar a lógica de compra de podcast fora do contexto do controlador. Terceiro, é mais difícil para realizar os testes unitários do comando, como também temos que gerar uma solicitação HTTP stub e fazer uma requisição inteira para aplicação para testar a lógica da compra do podcast.

Ao invés de colocar esta lógica no controlador(controller), nos podemos escolher encapsular isto com o objeto "command" (comando), como o comando `PurchasePodcast`(ComparaPodcast).

<a name="creating-commands"></a>
## Criando Comandos

O artisan CLI pode gerar uma nova classe de comento usando o comando `make:command`:

	php artisan make:command PurchasePodcast

A nova classe gerada será alocada no diretório `app/Commands`. Por padrão, o comando contém dois métodos: o contrutor e o método `handle`. É claro que, o contrutor permite que você passe qualquer objeto relavante para o comando, enquanto o método `handle` executa o comando, Por exemplo:

	class PurchasePodcast extends Command implements SelfHandling {

		protected $user, $podcast;

		/**
		 * Create a new command instance.
		 *
		 * @return void
		 */
		public function __construct(User $user, Podcast $podcast)
		{
			$this->user = $user;
			$this->podcast = $podcast;
		}

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle()
		{
			// Handle the logic to purchase the podcast...

			event(new PodcastWasPurchased($this->user, $this->podcast));
		}

	}

The `handle` method may also type-hint dependencies, and they will be automatically injected by the [IoC container](/docs/5.0/container). For example:

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle(BillingGateway $billing)
		{
			// Handle the logic to purchase the podcast...
		}

<a name="dispatching-commands"></a>
## Dispatching Commands

So, once we have created a command, how do we dispatch it? Of course, we could call the `handle` method directly; however, dispatching the command through the Laravel "command bus" has several advantages which we will discuss later.

If you glance at your application's base controller, you will see the `DispatchesCommands` trait. This trait allows us to call the `dispatch` method from any of our controllers. For example:

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}

The command bus will take care of executing the command and calling the IoC container to inject any needed dependencies into the `handle` method.

You may add the `Illuminate\Foundation\Bus\DispatchesCommands` trait to any class you wish. If you would like to receive a command bus instance through the constructor of any of your classes, you may type-hint the `Illuminate\Contracts\Bus\Dispatcher` interface. Finally, you may also use the `Bus` facade to quickly dispatch commands:

		Bus::dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);

### Mapping Command Properties From Requests

It is very common to map HTTP request variables into commands. So, instead of forcing you to do this manually for each request, Laravel provides some helper methods to make it a cinch. Let's take a look at the `dispatchFrom` method available on the `DispatchesCommands` trait:

	$this->dispatchFrom('Command\Class\Name', $request);

This method will examine the constructor of the command class it is given, and then extract variables from the HTTP request (or any other `ArrayAccess` object) to fill the needed constructor parameters of the command. So, if our command class accepts a `firstName` variable in its constructor, the command bus will attempt to pull the `firstName` parameter from the HTTP request.

You may also pass an array as the third argument to the `dispatchFrom` method. This array will be used to fill any constructor parameters that are not available on the request:

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="queued-commands"></a>
## Queued Commands

The command bus is not just for synchronous jobs that run during the current request cycle, but also serves as the primary way to build queued jobs in Laravel. So, how do we instruct command bus to queue our job for background processing instead of running it synchronously? It's easy. Firstly, when generating a new command, just add the `--queued` flag to the command:

	php artisan make:command PurchasePodcast --queued

As you will see, this adds a few more features to the command, namely the `Illuminate\Contracts\Queue\ShouldBeQueued` interface and the `SerializesModels` trait. These instruct the command bus to queue the command, as well as gracefully serialize and deserialize any Eloquent models your command stores as properties.

If you would like to convert an existing command into a queued command, simply implement the `Illuminate\Contracts\Queue\ShouldBeQueued` interface on the class manually. It contains no methods, and merely serves as a "marker interface" for the dispatcher.

Then, just write your command normally. When you dispatch it to the bus that bus will automatically queue the command for background processing. It doesn't get any easier than that.

For more information on interacting with queued commands, view the full [queue documentation](/docs/5.0/queues).

<a name="command-pipeline"></a>
## Command Pipeline

Before a command is dispatched to a handler, you may pass it through other classes in a "pipeline". Command pipes work just like HTTP middleware, except for your commands! For example, a command pipe could wrap the entire command operation within a database transaction, or simply log its execution.

To add a pipe to your bus, call the `pipeThrough` method of the dispatcher from your `App\Providers\BusServiceProvider::boot` method:

	$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

A command pipe is defined with a `handle` method, just like a middleware:

	class UseDatabaseTransactions {

		public function handle($command, $next)
		{
			return DB::transaction(function() use ($command, $next)
			{
				return $next($command);
			}
		}

	}

Command pipe classes are resolved through the [IoC container](/docs/5.0/container), so feel free to type-hint any dependencies you need within their constructors.

You may even define a `Closure` as a command pipe:

	$dispatcher->pipeThrough([function($command, $next)
	{
		return DB::transaction(function() use ($command, $next)
		{
			return $next($command);
		}
	}]);
