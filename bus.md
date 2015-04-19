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
O méotodo `handle` também pode tipar tipar dependencias, e elas irão ser automaticamente injetadoas pelo [IoC container](/docs/5.0/container). Por exemplo:

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
## Despachando Comandos

Então, umas vez que criamos o comando, como poderemos despacha-lo? É claro que, nos podemos chamar o método `handle` diretamento; entretanto, há várias vantagens em despachar o comando por meio do Laravel "command bus", essas serão discutidas mais tarde.

Se você der uma olhada no controller base da sua aplicação, você verá a trait `DispatchesCommands`. Esta trait nos permite chmar o méotodo `dispatch` de qualquer um de nossos controllers. Por exemplo:

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}
O comando bus irá cuidar da execução do comando e chamar o container IoC para injetar qualquer dependência necessária ao método `handle`.

Você pode adicionar a trait `Illuminate\Foundation\Bus\DispatchesCommands` em qualquer classe que você desejar. Se você gostaria de receber a instância do comando bus por meio do contrutor de qualquer de suas classes, você pode sugerir o tipar a interface `Illuminate\Contracts\Bus\Dispatcher`. Finanlmente, você pode também usar a fachada `Bus`para rapidamente dipachar comandos:

		Bus::dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);

### Mapeando Propriedades do comando a partir da requests

Isso é bem comum para mapear variáveis de requests(requisições) HTTP em comandos. Então, ao invés de forçar você a fazer isto manualmente para cada requisição, Laravel disponibiliza alguns métodos helpers para tornar isso mais fácil. Vamos dar uma olhada no método `dispatchFrom` disponível na trait `DispatchesCommands`.

	$this->dispatchFrom('Command\Class\Name', $request);

Este método irá examinar o construtor da classe comando concedida, e em seguida, extrai variáveis da requisição HTTP( ou qualquer oturo objeto `ArrayAccess` ) para preencher os parâmetros do construtor do comando. Assim, se a nossa classe comando aceitar uma vaiável  `firstName` em seu construtor, o comando bus tentará puxar o parâmetro `firstName` a partir da requisição HTTP. 

Você também pode passar um array como o terceiro argumento para o método `dispatchFrom`. Este array irá ser usado para preecher qualquer parâmetro do contrutor que não estiver disponível na request.

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="queued-commands"></a>
## Comandos Queued

O comando bus não serve apenas para sincronizar jobs(tarefas agendadas) que são executados durante o ciclo requisição atual, mas também servem como a principal maneira de construir jobs em fila no Laravel. Então, como vamos instruir o comando bus para enfileirar o nosso job para o processamento em segundo plano ao invés de executa-lo sincronizadamente? Isto é fácil. Primeiramente, quando estivermos gerando um novo comando, devemos adicionar a flag (mais um parâmetro) `--queued` ao comando:

	php artisan make:command PurchasePodcast --queued

Como você vai ver, isso adiciona mais algumas funcionalidades para comando, ou seja, a interface `Illuminate\Contracts\Queue\ShouldBeQueued` e a trait `SerializesModels`. Estes instruem o comando bus a enfileirar os comandos, bem como graciosamente serializa e desserializa qualquer modelo Eloquent do seu comando armazenando como propriedades.

Se você desejar converter a um comando existente em um comando queued, simplesminte implemente a interface `Illuminate\Contracts\Queue\ShouldBeQueued` na classe manualmente. Esta interface não contém métódos, e serve apenas como uma "marker interface"(interface marcadora) para o despachante.

Em seguida, apenas escreva seu comando normalmente. Quando você dispacha isto para o "bus" o bus será automaticamente enfileirado no processamento em segundo plano. Isto não tem como ser mais fácil.

Para mais informações de como interagir com os comandos queued, veja a documentação completa [queue documentation](/docs/5.0/queues)..


<a name="command-pipeline"></a>
## Comando em Pipeline

Antes de um comando ser despachado ao manipulador, você pode passar isso por meio de outras classes em um "pipeline". Comando pipes funcionam como um middleware HTTP, exceto para seus comandos! Por exemplo, um comando pipe pode envolver todo a operação do comando dentro de uma transação com banco de dados, ou simplesmente registrar a sua execução.

Para adicionar o pipe em seu comando bus, chame o méotodo `pipeThrough` do despachante a partir do seu método `App\Providers\BusServiceProvider::boot`:

	$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

O comando pipe é definido com o método `handle`, apenas como um middleware:

	class UseDatabaseTransactions {

		public function handle($command, $next)
		{
			return DB::transaction(function() use ($command, $next)
			{
				return $next($command);
			}
		}

	}

As classes comando pipe são resolvidas através do [IoC container](/docs/5.0/container), então sinta-se livre para tipar qualquer dependencia que você precisar dentro dos seus contrutores.

Você pode até mesmo definir um `Closure` como um comando pipe:

	$dispatcher->pipeThrough([function($command, $next)
	{
		return DB::transaction(function() use ($command, $next)
		{
			return $next($command);
		}
	}]);
