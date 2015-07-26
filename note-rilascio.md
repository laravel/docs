# Note di Rilascio

- [Policy di Support](#policy-supporto)
- [Laravel 5.1](#laravel-5.1)
- [Laravel 5.0](#laravel-5.0)

<a name="policy-supporto"></a>
## Policy di Supporto

Per le release LTS, come Laravel 5.1, il bug fixing verrà portato avanti per due anni, mentre le security fix per un tempo di tre anni. Tali release garantiranno una maggiore "finestra" temporale di supporto e manutenzione.

Per le release normali, il bux fixing rimane quello previsto di sei mesi e le fix relative alla sicurezza vengono garantite per un anno.

<a name="laravel-5.1"></a>
## Laravel 5.1

Laravel 5.1 continua il lavoro di miglioramento già svolto per Laravel 5.0, adottando lo standard PSR-2 ed aggiungendo il broadcasting di eventi, la possibilità di specificare dei parametri per i Middleware, svariati miglioramenti ad Artisan e tanto altro.

### PHP 5.5.9+

Visto che PHP 5.4 entrerà nella fase "end of life" a partire da Settembre, con la conseguente assenza di update alla sicurezza da parte del team PHP, Laravel 5.1 richiederà almeno PHP 5.5.9 per funzionare correttamente. Tale scelta permetterà una maggiore compatibilità, inoltre, con tutte le librerie più popolari come Guzzle o AWS SDK.

### LTS

Laravel 5.1 è la prima release di Laravel a ricevere il cosiddetto **long term support**. Verrà garantito il bug fixing per due anni e la cura necessaria per le fix riguardanti la sicurezza per tre anni. 

Una scelta del genere permette una maggiore stabilità nel tempo, con un occhio di riguardo per realtà enterprise.

### PSR-2

Il [PSR-2 coding style](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) è stato adottato come stile di default per la scrittura del framework. Inoltre, tutti i generatori sono stati aggiornati in modo tale da creare una sintassi compatibile PSR-2.

### Documentazione

Ogni singola pagina della documentazione di Laravel è stata rivista e migliorata meticolosamente. Tutti gli esempi sono stati risistemati dove necessario, a volte anche aggiornati per fornire una migliore rilevanza riguardo il contesto. 

### Broadcasting di Eventi

In molte applicazioni web moderne, l'uso di web socket per la creazione di interfacce utente real-time è piuttosto diffuso. Quando alcuni dati vengono aggiornati sul server, un messaggio viene inviato al client tramite una connessione websocket dedicata in modo tale da "reagire" adeguatamente. 

Per darti una mano nella creazione di queste applicazioni, Laravel rende più semplice il "broadcasting" di un evento su una connessione websocket. In questo modo potrai, agevolmente, condividere i tuoi eventi con un framework javascript client-side.

Per saperne di più, dai uno sguardo alla [sezione dedicata](/docs/5.1/events#broadcasting-events) della documentazione.

### Parametri per i Middleware

I Middleware adesso possono ricevere dei parametri aggiuntivi. Ad esempio, nel caso in cui la tua applicazione abbia bisogno di verificare se l'utente attivo ha un certo "ruolo" prima di effettuare un'azione, puoi creare un `RoleMiddleware` che riceve il ruolo come parametro:

	<?php namespace App\Http\Middleware;

	use Closure;

	class RoleMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @param  string  $role
		 * @return mixed
		 */
		public function handle($request, Closure $next, $role)
		{
			if (! $request->user()->hasRole($role)) {
				// Redirect...
			}

			return $next($request);
		}

	}

I parametri per i Middleware possono essere specificati in fase di definizione della route in questo modo, tramite l'uso dei due punti ":" come separatore tra nome del middleware e parametro:

	Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
		//
	}]);

In caso di più parametri, basta separarli con una virgola.

Se vuoi saperne di più, dai uno sguardo alla [pagina della documentazione dedicata](/docs/5.1/middleware).

### Testing Migliorato

Le capacità built-in di Laravel di testing sono notevolmente migliorate. Sono stati creati svariati metodi dalla sintassi semplice ed espressiva, per creare delle vere e proprie interazioni con la tua applicazione.

Guarda questo esempio:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

Per maggiori informazioni, guarda [la pagina del testing sulla documentazione](/docs/5.1/testing).

### Model Factory

Tramite le [Model Factory](/docs/5.1/testing#model-factories), testare un'applicazione diventa una passeggiata. Ti permettono, infatti, di definire in modo piuttosto veloce degli attributi di default per uno specifico model Eloquent e generare quindi svariate istanze (tramite anche l'uso di [Faker](https://github.com/fzaninotto/Faker), per i dati casuali).

	$factory->define('App\User', function ($faker) {
	    return [
	        'name' => $faker->name,
	        'email' => $faker->email,
	        'password' => str_random(10),
	        'remember_token' => str_random(10),
	    ];
	});

### Artisan Migliorato

I comandi Artisan adesso possono essere definiti tramite una semplice segnatura simile a quella usata nelle route. Nell'esempio di seguito è stato generato un comando con un parametro ed un'opzione:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--force}';

Se vuoi saperne di più, leggi la [pagina dedicata ad Artisan sulla documentazione](/docs/5.1/artisan).

### Struttura delle Cartelle

Per una migliore "espressione di intenti", la cartella `app/Commands` è stata rinominata in `app/Jobs`. In aggiunta, la cartella `app/Handlers` è stata consolidata in una singola cartella `app/Listeners` che contiene i vari listener. Tuttavia, non si tratta di un cambiamento determinate per il funzionamento del framework. Se stai facendo un update dalla vecchia versione non è strettamente indispensabile.

### Crittografia

Nelle precedenti versioni di Laravel, la crittografia è stata gestita dall'estensione `mcrypt`. Da questa nuova versione, invece, verrà usata `openssl` per via della sua manutenzione più frequente.

<a name="laravel-5.0"></a>
## Laravel 5.0

Laravel 5.0 introduce una nuova struttura di default per il proprio progetto. Questa nuova struttura ridefinita rappresenta l'insieme delle fondamenta ideali per costruire un'applicazione più robusta con Laravel, aderendo inoltre agli standard di caricamento automatico PSR-4. Ecco alcune delle novità principali.

### Nuova Struttura delle Directory

La vecchia cartella _app/models_ è stata rimossa totalmente. Tutto il codice viene messo invece nella cartella _app_ e, di default, viene indicato con il namespace _App_. Questo namespace, comunque, può essere agevolmente cambiato tramite il comando _app:name_ di Artisan.

I controller, i middleware e le request (un nuovo tipo di classe in Laravel 5) sono ora raggruppati in _app/Http_, dato che sono tutti collegati al layer HTTP della tua applicazione. Inoltre, al posto di usare un singolo file come avveniva per i filtri, ora i middleware sono stati inseriti in una specifica cartella e per ognuno di viene specificata una classe ad-hoc.

La cartella _app/Providers_ sostituisce invece i file presenti in _app/start_. Tali servizi sono necessari al bootstrapping di varie funzionalità dell'applicazione, come per esempio la gestione degli errori, logging, route loading e così via. Nulla ti vieta di creare altri provider per la tua applicazione.

I file di lingua e delle view sono stati spostati, invece, in _resources_.

### Contratti

Tutti i componenti più importanti del framework implementano delle interfacce, localizzate nel repository _illuminate/contracts_ che non presenta dipendenze esterne. Con un set centralizzato di interfacce, adesso, sarà più semplice creare alternative ai componenti che vorrai sostituire.

Se vuoi maggiori informazioni a riguardo, dai un'occhiata alla [pagina dedicata](/contratti).

### Route Cache

Se la tua applicazione è composta interamente di controller route potresti voler provare ad usare il nuovo comando _route:cache_, che incrementa in modo esponenziale la velocità di registrazione delle route. Il comando è particolarmente comodo in applicazioni con più di 100 route.

### Route Middleware

Oltre ai filtri più "classici" visti in Laravel 4, la versione 5 supporta i middleware HTTP. Tutti i filtri esistenti, inoltre, sono stati convertiti in middleware. Un middleware permette di fornire una singola interfaccia consistente per sostituire definitivamente i filtri. Ti permette di analizzare (ed eventualmente rifiutare) una certa richiesta prima ancora di entrare nell'applicazione vera e propria.

Per maggiori informazioni, dai un'occhiata [alla documentazione](/middleware).

### Controller Method Injection

In aggiunta alla possibilità di effettuare l'injection nel costruttore di una classe, adesso puoi effettaure il type-hint delle dipendenze direttamente in un metodo specifico. L'IoC Container si occuperà automaticamente di risolvere ed iniettare la dipendenza necessaria, anche se la route contiene dei parametri!

	public function createPost(Request $request, PostRepository $posts)
	{
		//
	}

### Scaffolding del Sistema di Autenticazione

La registrazione dell'utente, l'autenticazione e il controller dedicato al reset della password sono ora inclusi out of the box. Allo stesso modo è possibile trovare un insieme di view corrispondenti in _resources/views/auth_. Inoltre, sono state incluse anche alcune migration dedicate al sistema di autenticazione, in modo tale da farti avere in pochi secondi una struttura base già funzionante.

### Event Object

In Laravel 5 puoi definire gli eventi come oggeti, per non limitarti più a semplici stringhe. Ecco un esempio in azione.

	class PodcastWasPurchased {

		public $podcast;

		public function __construct(Podcast $podcast)
		{
			$this->podcast = $podcast;
		}

	}

L'evento può essere ora "lanciato" così:

	Event::fire(new PodcastWasPurchased($podcast));

Chiaramente, il tuo event handler corrispondente adesso riceverà un oggetto vero e proprio al posto di un semplice elenco di elementi.

	class ReportPodcastPurchase {

		public function handle(PodcastWasPurchased $event)
		{
			//
		}

	}

Se vuoi saperne di più, dai uno sguardo [alla documentazione](/eventi).

### Comandi / Code

In aggiunta al sistema di job in coda già presente in Laravel 4, Laravel 5 ti permette di rappresentare i vari job direttamente come command object. Tali classi si possono trovare in _app/Commands_. Eccone un esempio:

	class PurchasePodcast extends Command implements SelfHandling, ShouldBeQueued {

		use SerializesModels;

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

Il controller base di Laravel utilizza il trait _DispatchesCommands_ che permette di effettuare facilmente il dispatch di comandi da eseguire.

	$this->dispatch(new PurchasePodcastCommand($user, $podcast));

Ovviamente, puoi usare i comandi anche per effettuare task che sono eseguiti in modo sincrono (non in coda). Se ci pensi, usare i comandi può essere un ottimo modo di incapsulare task più complessi nella tua applicazione.

Nel caso volessi saperne di più, dai un'occhiata [alla documentazione](/bus) relativa.

### Coda "del Database"

In Laravel 5 è stato incluso un driver _database_ per le code, in modo tale da permetterti di usare, nel caso ne avessi bisogno, un sistema molto semplice e locale di code senza nessuna installazione di software ulteriore.

### Laravel Socialite

Laravel Socialite è un package opzionale (compatibile al 100% con Laravel 5.0) che permette di effettuare l'autenticazione con svariati OAuth Provider senza problemi. Socialite supporta Facebook, Twitter, Google e Github.

Di seguito un esempio di uso:

	public function redirectForAuth()
	{
		return Socialize::with('twitter')->redirect();
	}

	public function getUserFromProvider()
	{
		$user = Socialize::with('twitter')->user();
	}

Insomma, non dovrai più perdere ore di lavoro per scrivere i flow di autenticazione per i siti più svariati... niente male, vero? La [documentazione](/autenticazione#autenticazione-social) ha tutti gli altri dettagli, nel caso dovessi averne bisogno.

### Flysystem

Laravel ora include il potente sistema [Flysystem](https://github.com/thephpleague/flysystem), che permette di astrarre facilmente il filesystem attraverso svariati driver: dal filesystem locale ad Amazon S3, passando per Rackspace o SFTP. Tutto con una sola interfaccia:

	Storage::put('file.txt', 'contents');

Anche in questo caso, sulla [documentazione](/filesystem-cloud) troverai tutte le informazioni necessarie.

### Form Request

Laravel 5.0 introduce le **form requesT**, che estendono la classe _Illuminate\Foundation\Http\FormRequest_. Questi oggetti possono essere combinati con la tecnica di method injection nei controller per creare un metodo di validazione dei dati pulito ed efficiente. Eccone un esempio:

	<?php 

		namespace App\Http\Requests;

		class RegisterRequest extends FormRequest {

			public function rules()
			{
				return [
					'email' => 'required|email|unique:users',
					'password' => 'required|confirmed|min:8',
				];
			}

			public function authorize()
			{
				return true;
			}

		}

Una volta definita la classe, si può facilmente effettuare il type-hint dove necessario:

	public function register(RegisterRequest $request)
	{
		var_dump($request->input());
	}

Quando il Container IoC di Laravel identifica che si sta iniettando è un'istanza di _FormRequest_, tale request verrà **automaticamente validata**. Questo vuol dire che nel momento in cui la action specifica verrà richiamata, i dati verranno validati senza problemi secondo le regole da te specificate. In caso di validazione non superata, inoltre, potrai predisporre facilmente un redirect personalizzabile con eventuali messaggi di errore, che potranno essere sia "flashati" come di consueto che convertiti in JSON.

**Più semplice di così!**

Se vuoi saperne di più... [documentazione](/validazione#validazione-form-request)!

### Validazione Semplice nel Controller

Volendo, è possibile inoltre effettuare una validazione base tramite il trait _ValidatesRequests_. Il che significa che, da adesso, se necessario puoi anche usare un metodo come il seguente:

	public function createPost(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|max:255',
			'body' => 'required',
		]);
	}

Se la validazione non va a buon fine, verrà lanciata un'eccezione ed un'apposita risposta HTTP verrà automaticamente rimandata al browser. Gli errori di validazione verranno inoltre flashati in sessione. Ancora più interessante è sapere che in caso di metodo AJAX, Laravel **automaticamente** ritornerà un messaggio di errore appositamente formattato.

Per saperne di più, dai un'occhiata a [questa pagina](/validazione#validazione-controller).

### Nuovi Generatori

Da Laravel 5.0, i comandi di generazione di codice sono stati aggiunti ad Artisan. Puoi vederli tramite il comando _php artisan list_.

### Configuration Cache

Se dovessi averne bisogno, potrai mettere in cache tutti i tuoi file di configurazione usandone uno solo, tramite il comando _config:cache_.
