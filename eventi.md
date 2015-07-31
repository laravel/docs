# Eventi

- [Introduzione](#introduzione)
- [Registrare Eventi / Listener](#registrare-eventi-e-listener)
- [Definire Gli Eventi](#definire-eventi)
- [Definire I Listener](#definire-listeners)
	- [Gestione Coda Eventi](#gestione-coda-eventi)
- [Lanciare gli Eventi](#lanciare-eventi)
- [Broadcasting Di Eventi](#broadcasting-eventi)
	- [Configurazione](#configurazione-broadcast)
	- [Segnare Eventi Per Il Broadcast](#segnare-eventi-per-broadcast)
	- [Dati Broadcast](#dati-broadcast)
	- [Consuming Event Broadcasts](#consuming-event-broadcasts)
- [Event Subscriber](#event-subscriber)

<a name="introduzione"></a>
## Introduzione

La classe Event fornisce una semplice implementazione di un observer, che permette di gestire la tua applicazione attraverso gli eventi. Le classi eventi sono normalmente salvate nella directory  `app/Events`, mentre i loro handlers sono salvati all'interno di `app/Listeners`.

<a name="registrare-eventi-e-listener"></a>
## Registrare Eventi / Listener

L'`EventServiceProvider` incluso in Laravel offre un modo conventiente per gestire tutti gli handler degli eventi. La proprietà `listen`contiene un array di tutti gli eventi (key) e i loro handler (value). Ovviamente, puoi aggiungere altri eventi a questo array se la tua applicazione ne richiede. Per esempio, aggiungiamo il nostro evento `PodcastWasPurchased`:

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

### Generare Classi Di Event / Listener

Naturalmente, create i file per ogni evento e listener ogni qual volta ne hai bisogno è scomodo. Invece, aggiungi i tuoi handler ed eventi al tuo `EventServiceProvider` ed usa il comando `event:generate`. Questo comando genererà qualsiasi evento o listener presente nel tuo `EventServiceProvider`. Ovviamente, gli eventi o listener già esistenti saranno ignorati:

	php artisan event:generate

<a name="definire-eventi"></a>
## Definire Gli Eventi
Una classe evento è semplicemente un container di dati che mantiene le informazioni relative ad un evento. Per esempio, assumiamo che il nostro evento `PodcastWasPurchased` riceva un oggetto [Eloquent ORM](/docs/5.1/eloquent):

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

Come puoi vedere, questa classe contiene nessuna logica speciale. E' semplicemente un container per l'oggetto `Podcast` che viene acquistato. Il trait `SerializesModels` usato dall'evento serializzerà qualsiasi model Eloquent se l'oggetto evento è serializzato usando la funzione PHP `serialize`.

<a name="definire-listener"></a>
## Definire I Listener

Ora, diamo uno sguardo ai listener per il nostro evento di esempio. Gli event listener ricevono un istanza di un evento nel loro metodo `handle`. Il comando `event:generate` importerà automaticamente la giusta classe dell'evento ed eseguirà un type-hint nel metodo `handle`. All'interno del metodo `handle`, puoi eseguire qualsiasi logica necessaria in risposta all'evento.

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

Il tuo event listener può anche ricevere qualsiasi dipendenza abbia bisogno eseguendo un type-hint nel costruttore. Tutti gli event listener sono risolti da Laravel tramite il [service container](/docs/5.1/container), in questo modo le dipendenza saranno iniettate automaticamente:

	use Illuminate\Contracts\Mail\Mailer;

	public function __construct(Mailer $mailer)
	{
		$this->mailer = $mailer;
	}

#### Fermare La Propagazione Di Un Evento

In alcuni casi, puoi voler fermare la propagazione di un evento per altri listener. Puoi farlo ritornando `false` dal metodo `handle` del tuo listener.

<a name="gestione-code-eventi"></a>
### Gestione Coda Eventi

Hai bisogno di inserire un evento nella [coda](/docs/5.1/code)? Non potrebbe essere più facile. Aggiungi semplicemente l'interfaccia `ShouldQueue` alla classe dell'evento. I Listener generati dal comando Artisan `event:generate` hanno già importata questa interfaccia nel namespace corrente, in questo modo puoi usarla immediatamente:

	<?php namespace App\Listeners;

	use App\Events\PodcastWasPurchased;
	use Illuminate\Queue\InteractsWithQueue;
	use Illuminate\Contracts\Queue\ShouldQueue;

	class EmailPurchaseConfirmation implements ShouldQueue
	{
		//
	}
Questo è tutto! Ora, quando questo listener verrà chiamato per un evento, sarà automaticamente messo in coda dal dispatcher degli eventi usando il [queue system](/docs/5.1/code) di Laravel. Se non si verifica nessuna eccezione quando il listener viene esguito dalla coda, sarà la il sistema di gestione delle code a rimuovere automaticamente dalla coda il listener una volta processato.

#### Accesso Manuale alla Coda

Se hai bisogno di accedere manualmente ai metodi `delete` and `release` della queue,y puoi farlo in questo modo. Il trait `Illuminate\Queue\InteractsWithQueue`, che viene importato di default nei listener generati, ti permette di accedere a questi metodi:

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

<a name="lanciare-eventi"></a>
## Lanciare gli Eventi

Per lanciare un evento, puoi usare la [facade](/docs/5.1/facade) `Event`, passando un istanza dell'evento al metodo `fire`. Il metodo `fire` invierà l'evento a tutti i suoi listener registrati:

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

Alternativamente, puoi usare la funzione helper globale `event` per lanciare gli eventi:

	event(new PodcastWasPurchased($podcast));

<a name="broadcasting-eventi"></a>
##  Broadcasting Di Eventi

In molte moderne applicazioni web, i seb socket sono usati per implementare interfacce utente real-time, live-updating. Quando qualche dato è aggiornato sul server, normalmente viene inviato un messaggio al websocket per essere gestito dal client.

Per assisterti alla realizzazione di applicazioni di questo tipo, Laravel ti rende facile eseguire un "broadcast" dei tuoi eventi su una connessione websocket. Il Broadcasting dei tuoi eventi ti permette di condividere gli stessi nomi di eventi lato server con il tuo client JavaScript.

<a name="configurazione-broadcast"></a>
### Configurazione

Tutte le opzioni per il broadcast degli eventi sono memorizzate nel file di configurazione `config/broadcasting.php`. Laravel supporta diversi driver per il broadcast: [Pusher](https://pusher.com), [Redis](/docs/5.1/redis), e il driver `log` per lo sviluppo in locale e per debugging. E' inclusa una configurazione di esempio per ognuno di questi driver.

#### Prerequisiti Coda

Prima di eseguire il broadcast degli eventi, avrai bisogno di configurare ad eseguire la [queue listener](/docs/5.1/code). Il broadcast degli eventi viene realzizato tramite coda in modo tale che il tempo di risposta della tua applicazione non ne risenta. 

<a name="segnare-eventi-per-broadcast"></a>
### Segnare Eventi Per Il Broadcast

Per informare Laravel che un evento debba essere affetto da broadcast, implementa l'interfaccia `Illuminate\Contracts\Broadcasting\ShouldBroadcast` per la classe dell'evento. L'interfaccia `ShouldBroadcast` richiede di implementare un singolo metodo: `broadcastOn`. Il metodo `broadcastOn` ritorna u array di nomi di "canali" sui quali l'evento dovrebbe essere trasmesso:

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

Quindi, hai solo bisogno di [lanciare l'evento](#lanciare-eventi) come faresti normalmente. Una volta che l'evento viene eseguito, la [queued job](/docs/5.1/code) trasmetterà automaticamente l'evento a seconda del driver specificato.

<a name="dati-broadcast"></a>
### Dati Broadcast

Quando un evento è trasmesso, tutte le sue proprietà `pubbliche` vengono serializzate automaticamente come payload dell'evento, permettendoti di accedere a qualsiasi dato pubblico dalla tua applicazione JavaScript. Così, per esempio, se il tuo evento ha una proprietà pubblica `$user` che contiene un model Eloquent, i dati di payload dovrebbero essere:

	{
		"user": {
			"id": 1,
			"name": "Jonathan Banks"
			...
		}
	}

Tuttavia, se desideri avere un controllo più fine sui dati trasmessi, puoi aggiungere il metodo `broadcastWith` al tuo evento. Questo metodo dovrebbe ritornare un array di dati che tu desideri trasmettere assieme all'evento:

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
### “Aggangiarsi” Al Broadcast di Eventi

#### Pusher

Puoi “aggangiarti” in modo conveniente al broadcast degli eventi usando il driver [Pusher](https://pusher.com) usando gli SDK JavaScript di Pusher. Per esempio, “agganciamoci” all'evento `App\Events\ServerCreated` del nostro precedente esempio:

	this.pusher = new Pusher('pusher-key');

	this.pusherChannel = this.pusher.subscribe('user.' + USER_ID);

	this.pusherChannel.bind('App\\Events\\ServerCreated', function(message) {
		console.log(message.user);
	});

#### Redis

Se stai usando Redis, avrai bisogno di scrivere il tuo personale metodo di "aggancio" per ricevere i messaggi ed inviarli usando la tecnolgia websocket. Per esempio, puoi scegliere di usare la popolare libreria [Socket.io](http://socket.io) scritta in Node.

Usando le librerie Node `socket.io` e `ioredis`, puoi scrivere velocemente un evento da trasmettere per pubblicare tutti glie eventi che sono trasmessi dalla tua applicazione:

	var app = require('http').createServer(handler);
	var io = require('socket.io')(app);

	var Redis = require('ioredis');
	var redis = new Redis();

	app.listen(6001, function() {
		console.log('Server is running!');
	});

	function handler(req, res) {
		res.writeHead(200);
		res.end('');
	}

	io.on('connection', function(socket) {
		//
	});

	redis.psubscribe('*', function(err, count) {
		//
	});

	redis.on('pmessage', function(subscribed, channel, message) {
		message = JSON.parse(message);
		io.emit(channel + ':' + message.event, message.data);
	});

<a name="event-subscribers"></a>
## Event Subscribers

Gli Event subscribers sono classi che puoi registrare per eventi multipli dall’interno della classe stessa. I subscribers dovrebbero definire un metodo `subscribe`, che verrà passato all’istanza del dispatcher degli eventi:

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

#### Registrare Un Event Subscriber

Una volta che il subscriber è stato definito, può essere registrato con il dispatcher dell'evento. Puoi registrare i tuoi subscriber usando la proprietà `$subscribe` in `EventServiceProvider`. Per esempio, aggiungiamo `UserEventListener`.

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
