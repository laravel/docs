# Eventi

- [Uso Base](#uso-base)
- [Gestione Coda Eventi](#gestione-coda-eventi)
- [Event Subscribers](#event-subscribers)

<a name="uso-base"></a>
## Uso Base

La classe Event fornisce una semplice implementazione di un observer, che permette di gestire la tua applicazione attraverso gli eventi. Le classi eventi sono normalmente salvate nella directory `app/Events`, mentre i loro handlers sono salvati all'interno di `app/Handlers/Events`.

Puoi generare una nuova classe evento usando lo strumento Artisan CLI:

	php artisan make:event PodcastWasPurchased

#### Registrazione Di Un Evento

L'`EventServiceProvider` incluso in Laravel offre un modo conventiente per gestire tutti gli handler degli eventi. La proprietà `listen` contiene un array di tutti gli eventi (key) e i loro handler (value). Ovviamente, puoi aggiungere altri eventi a questo array se la tua applicazione ne richiede.
Per esempio, aggiungiamo il nostro evento `PodcastWasPurchased`:

	/**
	 * The event handler mappings for the application.
	 *
	 * @var array
	 */
	protected $listen = [
		'App\Events\PodcastWasPurchased' => [
			'App\Handlers\Events\EmailPurchaseConfirmation@handle',
		],
	];

Per generare un handler per un evento, usa il comando Artisan CLI `handler:event`:

	php artisan handler:event EmailPurchaseConfirmation --event=PodcastWasPurchased

Naturalmente, l'esecuzione manuale dei comandi `make:event` e `handler:event`da richiamare ogni volta che hai bisogno di un evento o di un handler è scomodo. Invece, aggiungi i tuoi handler ed eventi al tuo `EventServiceProvider` ed usa il comando `event:generate`. Questo comando genererà qualsiasi evento o handler inserito in `EventServiceProvider:

	php artisan event:generate

#### Lanciare Un Evento

Ora siamo pronti a lancaire il nostro evento usando la facade `Event`:

	$response = Event::fire(new PodcastWasPurchased($podcast));

Il metodo `fire` ritorna un array di risposte che puoi usare per controllare cosa accade successivamente nella tua applicazione.

Puoi inoltre usare l'helper `event` per lanciare un evento:

	event(new PodcastWasPurchased($podcast));

#### Closure Listener

Puoi anche evitare di creare la classe handler del tuo evento usando il metodo listen. Per esempio, nel metodo `boot` del tuo `EventServiceProvider`, potresti fare come segue:

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// Handle the event...
	});

#### Fermare La Propagazione Di Un Evento

A volte può succedere che tu debba fermare la propagazione di un evento per altri listener. Puoi farlo restituendo `false` dal tuo handler:

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// Handle the event...

		return false;
	});

<a name="gestione-coda-eventi"></a>
## Gestione Coda Eventi

Hai bisogno di inserire un evento in [coda](/code) ? Non potrebbe essere più facile. Quando generi un handler, semplicemente usa il flag `--queued`:

	php artisan handler:make SendPurchaseConfirmation --event=PodcastWasPurchased --queued

Questo comando genererà una classe handler che implementa l'interfaccia  `Illuminate\Contracts\Queue\ShouldBeQueued`. Ed è fatta! Ora quando questo handler è chiamato per un evento, verrà automaticamente messo in coda dall'event dispatcher.

Se non si presentano errori quando l'handler viene eseguito dalla coda, il job queue verrà cancellato automaticamente a termine della sua esecuzione. Se hai bisogno di accedere ai metodi della coda `delete` e `release`, puoi falro. Il trait `Illuminate\Queue\InteractsWithQueue`, che è incluso di default dall'handler della coda, ti dà la possibilità di accedere a questi metodi:

	public function handle(PodcastWasPurchased $event)
	{
		if (true)
		{
			$this->release(30);
		}
	}

Se hai un handler esistente e vorresti convertirlo in un handler di coda, è sufficiente aggiungere manualmente l'interfaccia `ShouldBeQueued` alla classe.

<a name="event-subscribers"></a>
## Event Subscribers

#### Definire Un Event Subscriber

Gli Event subscribers sono classi che puoi registrare per eventi multipli dall’interno della classe stessa. I subscribers dovrebbero definire un metodo `subscribe`, che verrà passato all’istanza del dispatcher degli eventi:

	class UserEventHandler {

		/**
		 * Handle user login events.
		 */
		public function onUserLogin($event)
		{
			//
		}

		/**
		 * Handle user logout events.
		 */
		public function onUserLogout($event)
		{
			//
		}

		/**
		 * Register the listeners for the subscriber.
		 *
		 * @param  Illuminate\Events\Dispatcher  $events
		 * @return array
		 */
		public function subscribe($events)
		{
			$events->listen('App\Events\UserLoggedIn', 'UserEventHandler@onUserLogin');

			$events->listen('App\Events\UserLoggedOut', 'UserEventHandler@onUserLogout');
		}

	}

#### Registrare Un Event Subscriber


Una volta che il subscriber è stato definito, è possibile registrarlo con la classe `Event`.

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

Alternativamente puoi anche usare l'[IoC Container](/container) per risolvere il tuo subscriber.
Per falro, è sufficiente passare il nome del tuo subscriber al metodo `subscribe`:

	Event::subscribe('UserEventHandler');
