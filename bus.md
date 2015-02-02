# Command Bus

- [Introduzione](#introduzione)
- [Creare Comandi](#creare-comandi)
- [Eseguire Comandi](#eseguire-comandi)
- [Comandi Accodati](#comandi-accodati)

<a name="introduzione"></a>
## Introduzione

Il command bus di Laravel rappresenta un mezzo conveniente per incapsulare all'interno di "comandi" semplici e comprensibili i compiti che la tua applicazione deve svolgere. Per comprendere meglio lo scopo dei comandi, immagina di costruire un'applicazione che consente agli utenti di acquistare podcast.

Quando un utente compra un podcast deve succedere tutta una serie di eventi. Ad esempio il costo del podcast deve essere detratto dalla sua carta di credito, deve essere salvato un record nel database che rappresenti l'acquisto e bisogna inviargli un'e-mail di conferma. E magari bisogna anche eseguire qualche sorta di validazione per stabilire se l'utente può comprare o meno il podcast.

Potresti inserire tutta questa logica dentro ad un controller, ma così facendo otterresti molti svantaggi. Il primo svantaggio è che il controller probabilmente gestisce già molte altre richieste HTTP e includere della logica complessa in ciascuna action rischia solo di ingigantirlo e renderlo poco leggibile. In secondo luogo è difficile in questo modo riutilizzare la logica dell'acquisto dei podcast fuori dal contesto del controller. Inoltre tutto ciò rende estremamente complesso effettuare gli unit test, dato che occorre creare stub per le richieste HTTP ed eseguire una richiesta completa verso l'applicazione per testare la logica dell'acquisto dei podcast.

Invece di inserire tale logica nel controller, puoi scegliere di incapsularla dentro un oggetto "comando", come il comando `PurchasePodcast`.

<a name="creare-comandi"></a>
## Creare Comandi

Grazie ad Artisan puoi creare nuovi comandi tramite il terminale con `make:command`:

	php artisan make:command PurchasePodcast

La classe appena creata viene posta nella cartella `app/Commands`. Di default il comando contiene due metodi: il costruttore e il metodo `handle`. Il costruttore ti permette di passare qualsiasi oggetto al comando, mentre il metodo `handle` esegue il comando. Per esempio:

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
			// Gestisci la logica per acquistare il podcast...

			event(new PodcastWasPurchased($this->user, $this->podcast));
		}

	}

Nel metodo `handle` puoi anche fare il type-hint delle dipendenze e queste vengono automaticamente iniettate dall'[IoC container](/docs/master/container). Per esempio:

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle(BillingGateway $billing)
		{
			// Gestisci la logica per acquistare il podcast...
		}

<a name="eseguire-comandi"></a>
## Eseguire Comandi

Come puoi eseguire un comando una volta creato? Puoi richiamare il metodo `handle` direttamente, certo, ma eseguirlo tramite il "command bus" di Laravel ha diversi vantaggi.

Se dai un'occhiata al controller di base della tua applicazione, puoi notare che utilizza il trait `DispatchesCommands`. Tale trait ti consente di richiamare il metodo `dispatch` da qualsiasi controller. Per esempio:

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}

Il command bus si prende l'incarico di eseguire il comando e chiamare l'IoC container per iniettare tutte le dipendenze richieste dal metodo `handle`.

Puoi aggiungere il trait `Illuminate\Foundation\Bus\DispatchesCommands` in qualsiasi classe desideri. Se invece preferisci ricevere un'istanza del command bus, puoi fare il type-hint dell'interfaccia `Illuminate\Contracts\Bus\Dispatcher`. O ancora, puoi usare il facade `Bus` per eseguire rapidamente i comandi:

	Bus::dispatch(
		new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
	);

### Mappare Le Proprietà Dei Comandi Dalle Richieste

È molto comune mappare le variabili delle richieste HTTP nei comandi. Per evitarti questa prassi ad ogni richiesta, Laravel fornisce alcuni utili metodi che la rendono un gioco da ragazzi. Dai un'occhiata al metodo `dispatchFrom` disponibile nel trait `DispatchesCommands`:

	$this->dispatchFrom('Command\Class\Name', $request);

Questo metodo esamina il costruttore del comando passato ed estrae le variabili dalla richiesta HTTP (o qualsiasi altro oggetto implementi `ArrayAccess`) per riempire i parametri richiesti. Quindi se il tuo comando accetta la variabile `firstName` nel suo costruttore, il command bus cerca di estrarlo dalla richiesta HTTP.

Puoi anche passare un array come terzo parametro del metodo `dispatchFrom`. Tale array può essere usato per aggiungere al costruttore delle variabili che non sono presenti nella richiesta:

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="comandi-accodati"></a>
## Comandi Accodati

Il command bus non gestisce solo lavori sincroni avviati durante il ciclo di richiesta corrente, ma in Laravel viene anche usato come mezzo primario per la creazione di lavori accodati. Quindi come puoi istruire il command bus per mettere in coda i tuoi lavori e processarli in background invece di eseguirli in modo sincrono? Facile, per prima cosa aggiungi il flag `--queued` durante la creazione da terminale del nuovo comando:

	php artisan make:command PurchasePodcast --queued

Così facendo aggiungi nuove funzionalità al comando, ossia l'interfaccia `Illuminate\Contracts\Queue\ShouldBeQueued` e il trait `SerializesModels`. Tutto ciò permette al command bus di accodare il comando e di serializzare e deserializzare qualsiasi modello Eloquent che il tuo comando usa come proprietà.

Se vuoi convertire un comando esistente in un comando accodabile, aggiungi semplicemente `Illuminate\Contracts\Queue\ShouldBeQueued` come interfaccia implementata dal comando. Tale interfaccia non contiene metodi e serve solo come "interfaccia segnale" per il dispatcher.

A questo punto scrivi il tuo comando normalmente. Quando viene eseguito dal command bus, questo lo accoda automaticamente per processarlo in background. Non potrebbe essere più semplice.

Per maggiori informazioni su come interagire con i comandi accodati, guarda la [documentazione completa sulle code](/docs/master/queues).
