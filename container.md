# Service Container

- [Introduzione](#introduzione)
- [Binding](#binding)
	- [Legare Interfacce A Implementazioni](#legare-interfacce-a-implementazioni)
	- [Binding Contestuale](#binding-contestuale)
	- [Tagging](#tagging)
- [Risoluzioni](#risoluzioni)
- [Eventi del Container](#eventi-del-container)

<a name="introduzione"></a>
## Introduzione

Il service container di Laravel è un potente strumento per gestire le dipendenze di una classe. Dependency injection è un parolone che sostanzialmente significa questo: le dipendenze di una classe sono "iniettate" nella classe stessa tramite il costruttore o, in alcuni casi, dei metodi "setter".

Ecco un esempio:

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

In questo esempio, `PurchasePodcast` ha bisogno di inviare una mail quando viene acquistato un podcast. Perciò viene **iniettato** un servizio in grado di inviare e-mail. Grazie a questa iniezione, hai la possibilità di sostituire tale servizio quando vuoi con un'altra implementazione. Inoltre semplifica la "simulazione" o creazione di finte implementazioni del mailer durante il test della tua applicazione.

Una profonda comprensione del service container di Laravel è essenziale per creare applicazioni grandi e potenti, ed è ugualmente necessaria per contribuire al core di Laravel stesso.

<a name="binding"></a>
## Binding

Quasi tutti i binding vengono registrati all'interno dei [service provider](/docs/{{version}}/providers), sperciò tutti i seguenti esempi dimostrano come usare il container in quel contesto. In ogni modo, non hai alcun bisogno di eseguire il bind delle classi nel container the non dipendono da nessuna interfaccia. Il container non ha bisogno di essere istruito su come costruire questi oggetti, dal momento che può risolvere automaticamente come oggetti "concreti" tramite i servizi di riflessione di PHP.

All'interno del service provider, puoi sempre avere accesso al container tramite l'istanza `$this->app`. Puoi registrare un binding usando il metodo `bind`, passando il nome della classe o dell'interfaccia che vuoi registrare tramite una `Closure` che ritorna un istanza della classe:

	$this->app->bind('HelpSpot\API', function ($app) {
		return new HelpSpot\API($app['HttpClient']);
	});

Nota che il metodo riceve il container stesso come parametro. Puoi usarlo per risolvere delle sotto-dipendenze degli oggetti che costruisci.

#### Binding Di Un Singleton

Il metodo `singleton` registra una classe o interfaccia all'interno del container che dovrebbe essere istanziato solo una volta, e la stessa istanza dovrebbe essere restituita in tutte le seguenti chiamate al container:

	$this->app->singleton('FooBar', function ($app) {
		return new FooBar($app['SomethingElse']);
	});

#### Binding Di Instanze

Puoi anche registrare un istanza di un oggetto esistente nel container usando il metodo `instance`. Così facendo l'istanza fornita viene sempre restituita nelle successive chiamate al container:

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

<a name="legare-interfacce-a-implementazioni"></a>
### Legare Interfacce A Implementazioni

Una funzionalità molto potente del service container è la sua abilità nel legare un interfaccia ad una data implementazione. Per esempio, supponi che la tua applicazione integri un interfaccia `EventPusher` ed una sua implementazione `RedisEventPusher`. Una volta implementata la nostra interfaccia `RedisEventPusher`, possiamo registrarla con il service container in questo modo:

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\RedisEventPusher');

Questo informa il container che dovrebbe iniettare `RedisEventPusher` quando una classe necessita un implementazione di `EventPusher`. Ora, possiamo importare l'interfaccia `EventPusher` nel costruttore, o in qualsiasi altro punto dove le dipendenze sono iniettate dal service container:

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

<a name="binding-contestuale"></a>
### Binding Contestuale

A volte potresti avere due classi che usano la stessa interfaccia, ma volere iniettare due implementazioni diverse. Per esempio quando il tuo sistema riceve un nuovo Order, potresti voler inviare un evento tramite [PubNub](http://www.pubnub.com/) piuttosto che Pusher. Laravel fornisce un'interfaccia semplice e armoniosa per definire tale comportamento:

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give('App\Services\PubNubEventPusher');

Puoi anche passare una Closure al metodo `give`:

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give(function () {
	          		// Resolve dependency...
	          	});

<a name="tagging"></a>
### Tagging

Di tanto in tanto potresti aver bisogno di risolvere tutti i binding di una certa "categoria". Ad esempio immagina di costruire un aggregatore di report che riceve un array con molte implementazioni diverse dell'interfaccia `Report`. Dopo aver registrato tutte le implementazioni di `Report`, puoi assegnare un tag a tali registrazioni tramite il metodo `tag`:

	$this->app->bind('SpeedReport', function () {
		//
	});

	$this->app->bind('MemoryReport', function () {
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

Una volta che il servizio è stato taggato, puoi risolverlo facilmente tramite il metodo `tagged`:

	$this->app->bind('ReportAggregator', function ($app) {
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="risoluzioni"></a>
## Risoluzioni

Esistono diversi modi per risolvere (o istanziare) qualcosa registrato nel container. Per prima cosa puoi usare il metodo `make`, che acceteta il nome della classe o dell'interfaccia che vuoi risolvere:

	$fooBar = $this->app->make('FooBar');

ppure puoi accedere al container come se fosse un array, dal momento che implementa l'interfaccia di PHP `ArrayAccess`:

	$fooBar = $this->app['FooBar'];

Infine, ma molto importante, puoi semplicemente fare il "type-hint" di una dipendenza nel costruttore di una classe risolta in automatico dal container, come i [controllers](/docs/{{version}}/controllers), gli [event listeners](/docs/{{version}}/events), i [queue jobs](/docs/{{version}}/queues), i [middleware](/docs/{{version}}/middleware) e altro ancora. In questo modo il container inietta automaticamente le dipendenze.

Il contenitore inietterà automaticamente le dipendenze per le classi da risolvere. Ad esempio, puoi importare un repository definito per la tua applicazione nel costruttore di un controller. Il repository verrà automaticamente risolto e iniettato nella classe: 

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

<a name="eventi-del-container"></a>
## Eventi del Container

Il container lancia un evento ogni volta che risolve un oggetto. Puoi ascoltare tale evento usando il metodo `resolving`:

	$this->app->resolving(function ($object, $app) {
		// Called when container resolves object of any type...
	});

	$this->app->resolving(function (FooBar $fooBar, $app) {
		// Called when container resolves objects of type "FooBar"...
	});

Come puoi vedere, l'oggetto che viene risolto viene passato al callback, permettendoti di impostare qualsiasi altra proprietà aggiuntiva sull'oggetto.
