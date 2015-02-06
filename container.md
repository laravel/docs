# Service Container

- [Introduzione](#introduzione)
- [Utilizzo Base](#utilizzo-base)
- [Legare Interfacce A Implementazioni](#legare-interfacce-a-implementazioni)
- [Binding Contestuale](#binding-contestuale)
- [Tagging](#tagging)
- [Applicazioni Pratiche](#applicazioni-pratiche)
- [Eventi Del Container](#eventi-del-container)

<a name="introduzione"></a>
## Introduzione

Il service container di Laravel è un potente strumento per gestire le dipendenze di una classe. Dependency injection è un parolone che sostanzialmente significa questo: le dipendenze di una classe sono "iniettate" nella classe stessa tramite il costruttore o, in alcuni casi, dei metodi "setter".

Ecco un esempio:

	<?php namespace App\Handlers\Commands;

	use App\User;
	use App\Commands\PurchasePodcast;
	use Illuminate\Contracts\Mail\Mailer;

	class PurchasePodcastHandler {

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
		 * @param  PurchasePodcastCommand  $command
		 * @return void
		 */
		public function handle(PurchasePodcastCommand $command)
		{
			//
		}

	}

In questo esempio, il command handler `PurchasePodcast` ha bisogno di inviare delle e-mail quando un podcast viene acquistato. Perciò viene **iniettato** un servizio in grado di inviare e-mail. Grazie a questa iniezione, hai la possibilità di sostituire tale servizio quando vuoi con un'altra implementazione. Inoltre semplifica la "simulazione" o creazione di finte implementazioni del mailer durante il test della tua applicazione.

Una profonda comprensione del service container di Laravel è essenziale per creare applicazioni grandi e potenti, ed è ugualmente necessaria per contribuire al core di Laravel stesso.

<a name="utilizzo-base"></a>
## Utilizzo Base

### Binding

Quasi tutti i binding vengono registrati all'interno dei [service provider](/provider), perciò tutti i seguenti esempi dimostrano come usare il container in quel contesto. Ad ogni modo, se hai bisogno di un'istanza del container in qualsiasi altro punto della tua applicazione, ad esempio una factory, puoi effettuare il type-hinting dell'interfaccia `Illuminate\Contracts\Container\Container` e un'istanza del container viene automaticamente iniettata per te. In alternativa, puoi usare il facade `App` per accedere al container.

#### Registrare Un Resolver Base

All'interno del service provider, puoi sempre accedere al container tramite la proprietà `$this->app`.

Esistono molti modi con cui il service container può registrare le dipendenze, come richiamare delle callback (Closure) e legare le interfacce alle relative implementazioni. Un resolver di Closure viene registrato nel container con una chiave (di solito il nome di una classe) e una Closure che restituisce un qualche valore:

	$this->app->bind('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### Registrare Un Singleton

A volte potresti voler registrare qualcosa nel container che dovrebbe essere istanziato solo una volta, e la stessa istanza dovrebbe essere restituita in tutte le seguenti chiamate al container:

	$this->app->singleton('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### Registrare Un'Istanza Nel Container

Puoi anche registrare nel container un oggetto già istanziato usando il metodo `instance`. Così facendo l'istanza fornita viene sempre restituita nelle successive chiamate al container:

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

### Risoluzioni

Esistono diversi modi per risolvere (o istanziare) qualcosa registrato nel container. Per prima cosa puoi usare il metodo `make`:

	$fooBar = $this->app->make('FooBar');

Oppure puoi accedere al container come se fosse un array, dal momento che implementa l'interfaccia `ArrayAccess`:

	$fooBar = $this->app['FooBar'];

Infine, ma molto importante, puoi semplicemente fare il "type-hint" di una dipendenza nel costruttore di una classe risolta in automatico dal container, come i controller, gli event listener, i queue job, i filtri e altro ancora. In questo modo il container inietta automaticamente le dipendenze:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Users\Repository as UserRepository;

	class UserController extends Controller {

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

<a name="legare-interfacce-a-implementazioni"></a>
## Legare Interfacce A Implementazioni

### Iniettare Dipendenze Concrete

Una funzionalità molto potente del service container è la sua abilità nel legare un interfaccia ad una data implementazione. Per esempio, supponi che la tua applicazione integri [Pusher](https://pusher.com), il servizio web per inviare e ricevere eventi in tempo reale. Se usi l'SDK PHP di Pusher puoi iniettare un istanza del suo client all'interno di una classe:

	<?php namespace App\Handlers\Commands;

	use App\Commands\CreateOrder;
	use Pusher\Client as PusherClient;

	class CreateOrderHandler {

		/**
		 * The Pusher SDK client instance.
		 */
		protected $pusher;

		/**
		 * Create a new order handler instance.
		 *
		 * @param  PusherClient  $pusher
		 * @return void
		 */
		public function __construct(PusherClient $pusher)
		{
			$this->pusher = $pusher;
		}

		/**
		 * Execute the given command.
		 *
		 * @param  CreateOrder  $command
		 * @return void
		 */
		public function execute(CreateOrder $command)
		{
			//
		}

	}

In questo esempio fai bene a iniettare la dipendenza della classe, però stai forzando la tua applicazione ad usare l'SDK di Pusher. Se i metodi dell'SDK di Pusher cambiano o vuoi rimpiazzare Pusher del tutto, sei costretto a cambiare tutto il codice di `CreateOrderHandler`.

### Programmare Un'Interfaccia

Per "isolare" `CreateOrderHandler` dalle modifiche dell'event pushing, puoi definire un'interfaccia `EventPusher` e un'implementazione `PusherEventPusher`:

	<?php namespace App\Contracts;

	interface EventPusher {

		/**
		 * Push a new event to all clients.
		 *
		 * @param  string  $event
		 * @param  array  $data
		 * @return void
		 */
		public function push($event, array $data);

	}

Una volta scritto il codice per `PusherEventPusher` che implementa l'interfaccia creata, puoi registrarlo nel service container in questo modo:

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\PusherEventPusher');

Questo suggerisce al container che deve iniettare `PusherEventPusher` quando una classe ha bisogno di un'implementazione per l'interfaccia `EventPusher`. Ora puoi fare il type-hint dell'interfaccia `EventPusher` nel costruttore:

		/**
		 * Create a new order handler instance.
		 *
		 * @param  EventPusher  $pusher
		 * @return void
		 */
		public function __construct(EventPusher $pusher)
		{
			$this->pusher = $pusher;
		}

<a name="binding-contestuale"></a>
## Binding Contestuale

A volte potresti avere due classi che usano la stessa interfaccia, ma volere iniettare due implementazioni diverse. Per esempio quando il tuo sistema riceve un nuovo Order, potresti voler inviare un evento tramite [PubNub](http://www.pubnub.com/) piuttosto che Pusher. Laravel fornisce un'interfaccia semplice e armoniosa per definire tale comportamento:

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give('App\Services\PubNubEventPusher');

<a name="tagging"></a>
## Tagging

Di tanto in tanto potresti aver bisogno di risolvere tutti i binding di una certa "categoria". Ad esempio immagina di costruire un aggregatore di report che riceve un array con molte implementazioni diverse dell'interfaccia `Report`. Dopo aver registrato tutte le implementazioni di `Report`, puoi assegnare un tag a tali registrazioni tramite il metodo `tag`:

	$this->app->bind('SpeedReport', function()
	{
		//
	});

	$this->app->bind('MemoryReport', function()
	{
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

Una volta che i servizi sono stati taggati, puoi facilmente risolverli tutti tramite il metodo `tagged`:

	$this->app->bind('ReportAggregator', function($app)
	{
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="applicazioni-pratiche"></a>
## Applicazioni Pratiche

Grazie al service container, Laravel fornisce molte opportunità per aumentare la flessibilità e testabilità delle tue applicazioni. Un esempio basilare è quando avviene la risoluzione dei controller. Tutti i controller vengono risolti tramite il service container, ciò significa che puoi fare il type-hint delle dipendenze nel costruttore di un controller e queste vengono automaticamente iniettate.

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\OrderRepository;

	class OrdersController extends Controller {

		/**
		 * The order repository instance.
		 */
		protected $orders;

		/**
		 * Create a controller instance.
		 *
		 * @param  OrderRepository  $orders
		 * @return void
		 */
		public function __construct(OrderRepository $orders)
		{
			$this->orders = $orders;
		}

		/**
		 * Show all of the orders.
		 *
		 * @return Response
		 */
		public function index()
		{
			$all = $this->orders->all();

			return view('orders', ['all' => $all]);
		}

	}

In questo esempio la classe `OrderRepository` viene automaticamente iniettata nel controller. In questo modo durante gli [unit test](/testing) puoi registrare una "simulazione" di `OrderRepository` nel container, evitando ad esempio le interazioni con il database.

#### Altri Esempi Sull'Uso Del Container

I controller non sono le uniche classi che Laravel risolve usando il service container. Puoi fare il type-hint anche delle dipendenze delle Closure delle route, filtri, queue job, event listeners e altro ancora. Fai riferimento alla loro documentazione per ulteriori esempi.

<a name="eventi-del-container"></a>
## Eventi Del Container

#### Registrare Un Listener Di Risoluzioni

Il container lancia un evento ogni volta che risolve un oggetto. Puoi ascoltare tale evento usando il metodo `resolving`:

	$this->app->resolving(function($object, $app)
	{
		// Viene chiamato quando il container risolve un oggetto di qualsiasi tipo...
	});

	$this->app->resolving(function(FooBar $fooBar, $app)
	{
		// Viene chiamato quando il container risolve un oggetto di tipo "FooBar"...
	});

L'oggetto risolto viene passato alla callback.
