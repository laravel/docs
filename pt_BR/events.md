# Eventos

- [Introdução](#introduction)
- [Registrando Eventos / Ouvintes](#registering-events-and-listeners)
- [Definindo Eventos](#defining-events)
- [Definindo Ouvintes](#defining-listeners)
	- [Queued Event Listeners](#queued-event-listeners)
- [Disparando Eventos](#firing-events)
- [Transmitindo Eventos](#broadcasting-events)
	- [Configuração](#broadcast-configuration)
	- [Fazendo eventos para Transmissão](#marking-events-for-broadcast)
	- [Transmitindo Dados](#broadcast-data)
	- [Consumindo Transmissões de Eventos](#consuming-event-broadcasts)
- [Event Subscribers](#event-subscribers)

<a name="introduction"></a>
## Introdução

Os eventos do Laravel fornecem uma implementação simples do padrão "observer", permitindo que você assine e escute eventos em sua aplicação. Classes de eventos são tipicamente armazenadas no diretório `app/Events`, enquanto seus ouvintes são armazenados no diretório `app\Listeners`.

<a name="registering-events-and-listeners"></a>
## Registrando Eventos / Ouvintes

A classe `EventServiceProvider` incluída com sua aplicação Laravel fornece um lugar conveniente para registrar todos os ouvintes de eventos. A propriedade `listen` contém um *array* com todos os eventos (chaves) e seus ouvintes (valores). Você pode adicionar a este *array* quantos eventos sua aplicação necessitar. Por exemplo, vamos adicionar nosso evento `PodcastWasPurchased`:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
	'App\Events\PodcastWasPurchased' => [
		'App\Listeners\EmailPurchaseConfirmation',
	],
];
```

### Gerando Classes de Evento / Ouvinte

A tarefa de gerar manualmente os arquivos para cada evento e ouvinte é tediosa. Ao invés disso, simplesmente adicione ouvintes e eventos
ao seu `EventServiceProvider` e use o comando `event:generate`. Este comando irá gerar qualquer evento ou ouvinte que for listado no seu
`EventServiceProvider`. Eventos e ouvintes que já existirem não serão afetados:

	php artisan event:generate

<a name="defining-events"></a>
## Definindo Eventos

Uma classe de evento é simplesmente um recipiente de dados que armazena as informações relacionadas ao evento. Por exemplo, vamos
assumir que nosso evento `PodcastWasPurchased` recebe um objeto [Eloquent](/docs/{{version}}/eloquent):

```
<?php namespace App\Events;

use App\Podcast;
use App\Events\Event;
use Illuminate\Queue\SerializesModels;

class PodcastWasPurchased extends Event
{
    use SerializesModels;

    public $podcast;

    /**
     * Create a new event instance.
     *
     * @param  Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }
}
```
Como você pode ver, esta classe de evento não contém nenhuma lógica especial. Ela é um simples recipiente para o objeto `Podcast` que foi
comprado. A *trait* `SerializesModels` utilizada pelo evento irá *serializar* qualquer *model* Eloquent se o evento for *serializado*
utilizando a função do php `serialize`.

<a name="defining-event-listeners"></a>
## Definindo Ouvintes de Evento

Prosseguindo, vamos dar uma olhada no ouvinte para o nosso evento de exemplo. Ouvintes recebem a instância do evento no seu método
`handle`. O comando `event:generate` irá automaticamente importar a classe de evento apropriada e adicioná-la no método `handle`. No método
`handle` você deve realizar toda a lógica necessária para responder ao evento.

```
<?php namespace App\Listeners;

use App\Events\PodcastWasPurchased;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;

class EmailPurchaseConfirmation
{
    /**
     * Create the event listener.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Handle the event.
     *
     * @param  PodcastWasPurchased  $event
     * @return void
     */
    public function handle(PodcastWasPurchased $event)
    {
        // Access the podcast using $event->podcast...
    }
}
```

Seu ouvinte deve também adicionar qualquer dependências necessária no seu construtor. Todos os ouvintes de eventos são resolvidos através do
[service container](/docs/{{version}}/container) do Laravel, de modo que as dependências serão automaticamente injetadas:

```
use Illuminate\Contracts\Mail\Mailer;

public function __construct(Mailer $mailer)
{
	$this->mailer = $mailer;
}
```

#### Impedindo a propagação dos eventos

Algumas vezes você desejará impedir a propagação de um evento para outros ouvintes. Você deve fazer isso retornando `false` do método
`handle` do seu ouvinte.

<a name="queued-event-listeners"></a>
### Enfileirando ouvintes de eventos

Precisa colocar um ouvinte de evento em uma [fila](/docs/{{version}}/queues)? Isto não poderia ser mais fácil. Simplesmente adicione
a interface `ShouldQueue` ao seu ouvinte. Ouvintes gerados pelo comando `event:generate` já possuem essa interface importada no namespace
atual, então você pode utilizá-la imediatamente:

```
<?php namespace App\Listeners;

use App\Events\PodcastWasPurchased;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;

class EmailPurchaseConfirmation implements ShouldQueue
{
	//
}
```

È isto! Agora, quando este ouvinte for chamado por um evento, ele será enfileirado automaticamente pelo disparador de eventos usando o
[sistema de filas](/docs/{{version}}/queues) do Laravel. Se nenhuma exceção for lançada quando o ouvinte é executado na fila, o evento
enfileirado será excluído automaticamente depois que for processado.


#### Acessando a fila manualmente

Se você necessita acessar os métodos `delete` e `release` do `job` enfileirado, você pode fazê-lo. A trait `Illuminate\Queue\InteractsWithQueue`,
que é importada por padrão nos eventos gerados, permite acesso a estes métodos:

```
<?php namespace App\Listeners;

use App\Events\PodcastWasPurchased;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;

class EmailPurchaseConfirmation implements ShouldQueue
{
	use InteractsWithQueue;

	public function handle(PodcastWasPurchased $event)
	{
		if (true) {
			$this->release(30);
		}
	}
}
```

<a name="firing-events"></a>
## Disparando Eventos

Para disparar um evento, você deve usar a [facade](/docs/{{version}}/facades) `Event`, passando uma instância do evento para o método
`fire`. O método `fire` irá disparar o evento para todos os seus ouvintes registrados:


```
<?php namespace App\Http\Controllers;

use Event;
use App\Podcast;
use App\Events\PodcastWasPurchased;
use App\Http\Controllers\Controller;

class UserController extends Controller
{
	/**
	 * Show the profile for the given user.
	 *
	 * @param  int  $userId
	 * @param  int  $podcastId
	 * @return Response
	 */
	public function purchasePodcast($userId, $podcastId)
	{
		$podcast = Podcast::findOrFail($podcastId);

		// Purchase podcast logic...

		Event::fire(new PodcastWasPurchased($podcast));
	}
}
```

Como alternativa, você pode usar a função global `event` para disparar eventos:

	event(new PodcastWasPurchased($podcast));

<a name="broadcasting-events"></a>
## Trasmitindo Eventos

Em muitas aplicações web modernas, *websockets* são usados para implementar atualizações em tempo real para suas interfaces de usuário.
Quando algum dado é atualizado no servidor, uma mensagem é tipicamente enviada sobre uma conexão de *websocket* para ser processada pelo
cliente.

Para ajudá-lo a construir esse tipo de aplicação, o Laravel possui um jeito fácil de "transmitir" seus eventos sobre uma conexão de *websocket*. Transmistir seus eventos Laravel permite a você compartilhar os mesmos nomes de eventos entre o código *server-side* e seu
framework Javascript *client-side*.

<a name="broadcast-configuration"></a>
### Configuração

Todas as configuração de "propagação" de eventos são armazenadas no arquivo de configuração `config/broadcasting.php`. O Laravel suporta
diversos *drivers* nativamente: [Pusher](https://pusher.com), [Redis](/docs/{{version}}/redis), e um *driver* `log` para desenvolvimento
local e depuração. Está incluso um exemplo de configuração para cada um desses *drivers*.

#### Pre-requisitos para a propagação de eventos

As seguintes dependências são necessárias para propagação de eventos:

- Pusher: `pusher/pusher-php-server ~2.0`
- Redis: `predis/predis ~1.0`

#### Pre-requisito de fila

Antes de transmitir os eventos, você também precisa configurar e executar um [queue listener](/docs/{{version}}/queues). Todas as
transmissões de eventos são realizadas através de filas para que o tempo de resposta de sua aplicação não seja afetado seriamente.


<a name="marking-events-for-broadcast"></a>
### Marcando eventos para transmissão

Para informar o Laravel que dado evento deve ser transmitido, você  deve implementar a interface `Illuminate\Contracts\Broadcasting\ShouldBroadcast` na classe de evento. A interface `ShouldBroadcast` necessita que você implemente um único método: `broadcastOn`. O método `broadcastOn` deve retornar um *array* com os nomes dos "canais" para os quais o evento deve ser transmitido.

```
<?php namespace App\Events;

use App\User;
use App\Events\Event;
use Illuminate\Queue\SerializesModels;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

class ServerCreated extends Event implements ShouldBroadcast
{
    use SerializesModels;

    public $user;

    /**
     * Create a new event instance.
     *
     * @return void
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * Get the channels the event should be broadcast on.
     *
     * @return array
     */
    public function broadcastOn()
    {
        return ['user.'.$this->user->id];
    }
}
```

Uma vez que o evento foi [disparado](#firing-events), um [queued job](/docs/{{version}}/queues) irá automaticamente transmitir o evento
sobre o *driver* de transmissão definido.


<a name="broadcast-data"></a>
### Transmitindo dados


Quando um evento é transmitido, todas as suas propriedades  `public` são automaticamente *serializadas* e transmitidas com os dados do evento,
permitindo que você acessse quaisquer propriedades públicas da sua aplicação Javascript. Então, por exemplo, se seu evento tem uma única propriedade pública `$user` que contém um *model* Eloquent, os dados transmitidos serão:

	{
		"user": {
			"id": 1,
			"name": "Jonathan Banks"
			...
		}
	}

Contudo, se você deseja ter um controle maior sobre os dados transmitidos, você deve adicionar um método `broadcastWith` ao seu evento. Este método deve retornar um *array* com os dados que você deseja transmitir com o evento:


    /**
     * Get the data to broadcast.
     *
     * @return array
     */
    public function broadcastWith()
    {
        return ['user' => $this->user->id];
    }

<a name="consuming-event-broadcasts"></a>
### Consumindo eventos transmitidos

#### Pusher

Você pode consumir eventos transmitidos usando o *driver* [Pusher](https://pusher.com) usando o SDK Javascript do Pusher. Por exemplo, vamos consumir o evento `App\Events\ServerCreated` do nosso exemplo anterior:

	this.pusher = new Pusher('pusher-key');

	this.pusherChannel = this.pusher.subscribe('user.' + USER_ID);

	this.pusherChannel.bind('App\\Events\\ServerCreated', function(message) {
		console.log(message.user);
	});

<a name="event-subscribers"></a>
## Event Subscribers

Event subscribers são classe que podem assinar à múltiplos eventos dentro da própria classe, permitindo que vocẽ defina diversos manipuladores de eventos em uma única classe. Subscribers devem definir um método `subscribe`, que será passado uma instância do disparador de eventos:

	<?php namespace App\Listeners;

	class UserEventListener {

		/**
		 * Handle user login events.
		 */
		public function onUserLogin($event) {}

		/**
		 * Handle user logout events.
		 */
		public function onUserLogout($event) {}

		/**
		 * Register the listeners for the subscriber.
		 *
		 * @param  Illuminate\Events\Dispatcher  $events
		 * @return array
		 */
		public function subscribe($events)
		{
			$events->listen(
				'App\Events\UserLoggedIn',
				'App\Listeners\UserEventListener@onUserLogin'
			);

			$events->listen(
				'App\Events\UserLoggedOut',
				'App\Listeners\UserEventListener@onUserLogout'
			);
		}

	}

#### Registrando um Event Subscriber

Uma vez que o assinante foi definido, você deve registrar com o disparador de eventos. Você deve registrar usando a propriedade `$subscribe` no `EventServiceProvider`. Por exemplo, vamos adicionar o `UserEventListener`.

    <?php namespace App\Providers;

    use Illuminate\Contracts\Events\Dispatcher as DispatcherContract;
    use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

    class EventServiceProvider extends ServiceProvider
    {
        /**
         * The event listener mappings for the application.
         *
         * @var array
         */
        protected $listen = [
            //
        ];

        /**
         * The subscriber classes to register.
         *
         * @var array
         */
        protected $subscribe = [
            'App\Listeners\UserEventListener',
        ];
    }
