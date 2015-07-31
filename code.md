# Code

- [Introduzione](#introduzione)
	- [Configurazione](#configurazione)
- [Scrivere le Classi Job](#scrivere-classi-job)
	- [Generare le Classi Job](#generare-classi-job)
	- [Struttura di una Classe Job](#struttura-classe-job)
- [Mettere dei Job in Coda](#mettere-job-coda)
	- [Job Dilazionati](#job-dilazionati)
	- [Dispatch di un Job da una Richiesta](#dispatch-job-richiesta)
- [Eseguire il Queue Listener](#eseguire-queue-listener)
	- [Configurare Supervisor](#configurare-supervisor)
	- [Daemon Queue Listener](#daemon-queue-listener)
	- [Deploy con Daemon Queue Listener](#deploy-daemon-queue-listener)
- [Gestire i Job Falliti](#gestire-job-falliti)
	- [Definire degli Eventi per Job Falliti](#eventi-job-falliti)
	- [Riprovare ad Eseguire un Job Fallito](#riprovare-eseguire-job-fallito)

<a name="introduzione"></a>
## Introduzione

Il servizio di code di Laravel fornisce un'API unificata per svariati servizi di code per backend. Le code ti permettono di eseguire in un secondo momento alcuni task specifici, come l'invio di email, in modo tale da non pesare troppo sulla richiesta corrente.

<a name="configurazione"></a>
### Configurazione

Il file di configurazione per il sistema di coda è `config/queue.php`. In questo file potrai trovare i vari dettagli per le connessioni ai vari servizi di questa tipologia. Ci sono svariati driver già compresi nel framework: il classico "database", [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), [Redis](http://redis.io) ed un driver "sincrono" per uso locale.

Puoi anche selezionare, volendo, un _null_ driver che semplicemente prende e scarta ogni job.

### Prerequisiti dei Driver

#### Database

Per usare il driver _database_ avrai bisogno di una tabella dedicata sul database. Tranquillo, niente di complesso: esegui il comando `queue:table` che si occuperà di creare la migration adatta. A quel punto, esegui il comando `migrate`:

	php artisan queue:table
	php artisan migrate

#### Altre Dipendenze

Ogni driver ha le sue specifiche dipendenze. In base a quello che vuoi usare, aggiungi il package corrispondente al file _composer.json_.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~3.0`
- IronMQ: `iron-io/iron_mq ~2.0`
- Redis: `predis/predis ~1.0`

<a name="scrivere-classi-job"></a>
## Scrivere le Classi Job

<a name="generare-classi-job"></a>
### Generare le Classi Job

Di default, tutti i vari job che si possono mettere in coda vengono memorizzati in _app/Jobs_. Puoi generare un nuovo job tramite il comando Artisan

	php artisan make:job SendReminderEmail --queued

In questo caso specifico stiamo creando un job chiamato _SendReminderEmail_ che implementerà, inoltre, l'interfaccia `Illuminate\Contracts\Queue\ShouldQueue`, la quale indica che tale job verrà messo in coda e non eseguito in modo sincrono.

<a name="struttura-classe-job"></a>
### Struttura di una Classe Job

Una classe Job è davvero molto semplice. Normalmente contiene un metodo _handle_ che viene chiamato nel momento in cui il job viene processato dalla coda. Facciamo subito un primo esempio:

	<?php namespace App\Jobs;

	use Mail;
	use App\User;
	use App\Jobs\Job;
	use Illuminate\Contracts\Mail\Mailer;
	use Illuminate\Queue\SerializesModels;
	use Illuminate\Queue\InteractsWithQueue;
	use Illuminate\Contracts\Bus\SelfHandling;
	use Illuminate\Contracts\Queue\ShouldQueue;

	class SendReminderEmail extends Job implements SelfHandling, ShouldQueue
	{
	    use InteractsWithQueue, SerializesModels;

	    protected $user;

	    /**
	     * Create a new job instance.
	     *
	     * @param  User  $user
	     * @return void
	     */
	    public function __construct(User $user)
	    {
	        $this->user = $user;
	    }

	    /**
	     * Execute the job.
	     *
	     * @param  Mailer  $mailer
	     * @return void
	     */
	    public function handle(Mailer $mailer)
	    {
	    	$mailer->send('emails.reminder', ['user' => $this->user], function ($m) {
	    		//
	    	});

	    	$user->reminders()->create(...);
	    }
	}

In questo esempio, stiamo passando un [model Eloquent](/documentazione/5.1/eloquent) direttamente al costruttore del job. Grazie al trait _SerializesModels_, questo verrà automaticamente serializzato e poi deserializzato una volta in fase di processing. Nello specifico, nel caso in cui un tuo job dovesse accettare un model Eloquent nel costruttore, ad essere passato per la serializzazione in realtà sarà solo l'identificatore.

In fase di esecuzione l'istanza vera e propria verrà ripresa e quindi processata all'interno del metodo _handle_. Comodo, e tutto trasparente per lo sviluppatore.

Tra l'altro, è possibile usare la method injection per il metodo _handle_! A tutto il resto ci penserà il [service container](/documentazione/5.1/container).

#### Quando le Cose non Vanno Bene

Se un qualsiasi job lancia un'eccezione di qualsiasi genere, il job viene preso e rimesso in coda, in modo tale da poter riprovarne l'esecuzione. È possibile definire un numero di tentativi massimi per i tuoi job in coda. Tramite un flag: precisamente, il flag _--tries__ che può essere passato a _queue:listen_ o _queue:work_. Se vuoi sapere di più riguardo il listener, [guarda qui](#eseguire-queue-listener).

#### Rilasciare un Job Manualmente

Nel caso in cui tu voglia _rilasciare_ un job manualemente, il trait `InteractsWithQueue` fa al caso tuo. Il metodo ad essere usato, in questo caso, è `release`. Tale metodo accetta un parametro: il numero di secondi da aspettare prima che il job in questione sia nuovamente disponibile.

	public function handle(Mailer $mailer)
	{
		if (condition) {
			$this->release(10);
		}
	}

#### Controllare il Numero di Tentativi

Come già detto poco fa, se viene lanciata un'eccezione durante l'esecuzione del job, questo verrà rilasciato nella queue. Potresti voler controllare a quale tentativo ci si trova: lo puoi fare tramite _attempts_.

	public function handle(Mailer $mailer)
	{
		if ($this->attempts() > 3) {
			//
		}
	}

<a name="mettere-job-coda"></a>
## Mettere dei Job in Coda

Il controller di default di Laravel in `app/Http/Controllers/Controller.php` usa un trait `DispatchesJob`. Tale trait permette di usare, dal controller, alcuni metodi dedicati ai job come ad esempio _dispatch_.

	<?php namespace App\Http\Controllers;

	use App\User;
	use Illuminate\Http\Request;
	use App\Jobs\SendReminderEmail;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Send a reminder e-mail to a given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function sendReminderEmail(Request $request, $id)
		{
			$user = User::findOrFail($id);

			$this->dispatch(new SendReminderEmail($user));
		}
	}

Ovviamente, potresti avere la necessità di eseguire altrove alcuni job e non solo in un controller o da una route. In tal caso, tutto quello che devi fare è includere il trait `DispatchesJobs` nella classe per la quale hai questo bisogno:

	<?php namespace App;

	use Illuminate\Foundation\Bus\DispatchesJobs;

	class ExampleClass
	{
		use DispatchesJobs;
	}

#### Specificare la Coda di un Job

Puoi anche specificare in quale coda mettere un certo job.

Mettere i tuoi job in diverse code vuol dire anche categorizzare e diversificare i tuoi job, dando loro delle priorità anche in base ai vari worker che hai a disposizione. In questo caso, comunque, non parlo di varie connessioni: parlo proprio di varie code per la stessa connessione. Per specificare la coda nella quale "far finire" un certo job, usa _onQueue_.

	<?php namespace App\Http\Controllers;

	use App\User;
	use Illuminate\Http\Request;
	use App\Jobs\SendReminderEmail;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Send a reminder e-mail to a given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function sendReminderEmail(Request $request, $id)
		{
			$user = User::findOrFail($id);

			$job = (new SendReminderEmail($user))->onQueue('emails');

			$this->dispatch($job);
		}
	}

<a name="job-dilazionati"></a>
### Job Dilazionati

A volte potresti dilazionare nel tempo l'esecuzione di un certo job. Ad esempio, immagina un job che manda ad un cliente un email 15 minuti dopo l'iscrizione. Puoi facilmente implementare una richiesta del genere usando il metodo _delay_ sulla tua classe. Il trait contenente il metodo in questo caso è `Illuminate\Bus\Queueable`:

	<?php namespace App\Http\Controllers;

	use App\User;
	use Illuminate\Http\Request;
	use App\Jobs\SendReminderEmail;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Send a reminder e-mail to a given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function sendReminderEmail(Request $request, $id)
		{
			$user = User::findOrFail($id);

			$job = (new SendReminderEmail($user))->delay(60);

			$this->dispatch($job);
		}
	}

In questo esempio stiamo specificando che il job dovrebbe essere ritardato di 60 secondi prima di diventare disponibile ai vari worker.

> **Nota:** il servizio SQS di Amazon ha un delay time massimo di 15 minuti.

<a name="dispatch-job-richiesta"></a>
### Dispatch di un Job da una Richiesta

Mappare alcune variabili di una richiesta HTTP in un job può essere piuttosto comune. Al posto di fare manualmente questa operazione per ogni richiesta, Laravel ha alcuni metodi di comodo da poter usare facilmente per lo scopo. Vediamo insieme il metodo _dispatchFrom_, disponibile nel trait _DispatchesJobs_.

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class CommerceController extends Controller
	{
		/**
		 * Process the given order.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function processOrder(Request $request, $id)
		{
			// Process the request...

			$this->dispatchFrom('App\Jobs\ProcessOrder', $request);
		}
	}

Tale metodo esaminerà il costruttore di un dato job, in modo tale da estrarne eventualmente le variabili dalla richiesta HTTP (o da un qualsiasi oggetto che implementa _ArrayAccess_) per "riempire" in modo coerente il costruttore del job stesso. Così, per fare un esempio, se il nostro job accetta una variabile detta _productId_, verrà cercata una variabile _productId_ nella richiesta.

Puoi anche passare, come terzo argomento, un array al metodo `dispatchFrom`. Tale array viene usato per "riempire" tutti quei parametri che non sono stati riempiti con le variabili prese della richiesta.

	$this->dispatchFrom('App\Jobs\ProcessOrder', $request, [
		'taxPercentage' => 20,
	]);

<a name="eseguire-queue-listener"></a>
## Eseguire il Queue Listener

#### Avviare il Queue Listener

Laravel include un comando Artisan che esegue nuovi job così come vengono messi in coda. Puoi avviare il listener usando _queue:listen_.

	php artisan queue:listen

Puoi anche specificare quale connessione usare per l'operazione.

	php artisan queue:listen connection

Ricorda: una volta avviato, il listener non viene fermato fin quando non viene stoppato manualmente. Una buona idea, per sicurezza, potrebbe essere l'uso di [Supervisor](http://supervisord.org/) per fare in modo che il listener non si fermi in modo indesiderato.

#### Priorità delle Code

Puoi passare una lista di connessioni al comando _queue:listen_ in modo tale da impostare le varie priorità.

	php artisan queue:listen --queue=high,low

In questo esempio, i vari job sulla coda "high" verranno processati sempre prima dei vari job presenti sulla coda "low".

#### Specificare il Timeout di un Job

Puoi anche impostare il timeout (in secondi) per ogni job da eseguire nel listener:

	php artisan queue:listen --timeout=60

#### Specificare la Durata dello Sleep

In aggiunta, puoi specificare anche il numero di secondi di attesa prima di effettuare il polling alla ricerca di nuovi job.

	php artisan queue:listen --sleep=5

Ricorda: la coda "dorme" solo se non ci sono job. Se ci sono altri job la coda continuerà ad essere processata senza pausa.

<a name="configurare-supervisor"></a>
### Configurare Supervisor

Supervisor è un process monitor per Linux, che riavvia automaticamente alcuni comandi (come _queue:listen_ o _queue:work_) se questi falliscono per qualche motivo.

Installarlo è davvero semplice:

	sudo apt-get install supervisor

Il file di configurazione di Supervisor viene tendenzialmente memorizzato in `/etc/supervisor/conf.d`. In questa directory puoi creare a piacimento tanti file di configurazione quanti sono i processi da monitorare. Creiamo, ad esempio, un file per il monitoraggio della coda di Laravel che chiameremo `laravel-worker.conf`.

	[program:laravel-worker]
	process_name=%(program_name)s_%(process_num)02d
	command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --daemon
	autostart=true
	autorestart=true
	user=forge
	numprocs=8
	redirect_stderr=true
	stdout_logfile=/home/forge/app.com/worker.log

In questo esempio, la direttiva `numprocs` "spiegherà" a supervisor di avviare 8 processi `queue:work` e monitorarli, riavviandoli automaticamente in caso di fallimento di qualsiasi genere. Una volta creato il file, ricarica i file di configurazione ed avvia i processi con i seguenti comandi.

	sudo supervisorctl reread
	sudo supervisorctl update
	sudo supervisorctl start laravel-worker

Per maggiori informazioni su Supervisor, dai un'occhiata alla [documentazione sul sito ufficiale](http://supervisord.org/index.html).

<a name="daemon-queue-listener"></a>
### Daemon Queue Listener

Il comando _queue:work_ di artisan include un'opzione _--daemon_ che forza il worker a continuare il processing dei vari job senza dover riavviare il framework. Il risultato, ovviamente, è una riduzione significativa dell'uso della CPU, se comparato al comando _queue:listen_.

Per avviare un worker in modalità demone, usa:

	php artisan queue:work connection --daemon
	php artisan queue:work connection --daemon --sleep=3
	php artisan queue:work connection --daemon --sleep=3 --tries=3

Le opzioni supportate sono le stesse viste per `queue:listen`.

#### Considerazioni per i Daemon Queue Listener

I worker avviati come demoni non riavviano il framework prima di processare ogni lavoro. Tuttavia, il consiglio giusto è di fare tanta attenzione riguardo alle varie risorse da liberare prima di terminare un certo job. Ad esempio, se stai manipolando un'immagine con GD, ricorda di usare _imagedestroy_ prima di terminare le operazioni.

Ricorda inoltre che le connessioni al database potrebbero interrompersi usando un demone long-running. Di conseguenza, usa _DB::reconnect_ per essere sicuro di avere una connessione sempre "fresca".

<a name="deploy-daemon-query-listener"></a>
### Deploy con Daemon Query Listener

Considerando che i daemon queue worker sono dei processi dalla vita piuttosto lunga, sicuramente non saranno capaci di accorgersi di eventuali cambiamenti nel tuo codice senza un riavvio. Per questo motivo, puoi tranquillamente effettuare il restart di tutti i tuoi worker attivi tramite il comando

	php artisan queue:restart

nel tuo script di deploy. Interessante, inoltre, è sapere che tutti i vari job verranno eseguiti e portati a termine. Solo dopo l'esecuzione i vari worker verranno riavviati.

> **Nota:** Questo comando usa il cache system per schedulare il riavvio. Di default APCu non è abilitato per i job via CLI. Se stai usando APCu, assicurati di aggiungere `apc.enable_cli=1` alla configurazione.

<a name="gestire-job-falliti"></a>
## Gestire i Job Falliti

Le cose non vanno sempre come ti aspetti: a volte uno o più job in coda potrebbero fallire. Non ti preoccupare, succede a tutti! Anche ai migliori! Laravel include un sistema piuttosto conveniente che ti permette di specificare il numero massimo di tentativi per ogni job. Una volta superati questi tentativi, il job verrà messo in una tabella *failed_jobs* apposita. Tale tabella, il cui nome è variabile e deciso nel file _config/queue.php_, può essere creata con:

	php artisan queue:failed-table

Eseguendo il [listener](#eseguire-queue-listener) puoi specificare il numero massimo di tentativi per un job tramite l'opzione _--tries_.

	php artisan queue:listen connection-name --tries=3

<a name="eventi-job-falliti"></a>
### Definire degli Eventi per Job Falliti

Se vuoi registrare un evento da richiamare nel momento in cui un job fallisce, puoi usare il metodo _Queue::failing_. Un esempio di uso pratico potrebbe essere l'invio di una notifica e-mail in caso di fallimento, o magari su [HipChat](https://www.hipchat.com). La callback potrebbe essere tranquillamente messa nel service provider `AppServiceProvider`:

	<?php namespace App\Providers;

	use Queue;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			Queue::failing(function ($connection, $job, $data) {
				// Norifica al team...
			});
		}

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

#### Specificare un Comportamento direttamente nella Classe

Se preferisci, puoi avere ancora più controllo sul fallimento dei job definendo un metodo _failed_ direttamente nella classe del job.

	<?php namespace App\Jobs;

	use App\Jobs\Job;
	use Illuminate\Queue\SerializesModels;
	use Illuminate\Queue\InteractsWithQueue;
	use Illuminate\Contracts\Bus\SelfHandling;
	use Illuminate\Contracts\Queue\ShouldQueue;

	class SendReminderEmail extends Job implements SelfHandling, ShouldQueue
	{
	    use InteractsWithQueue, SerializesModels;

	    /**
	     * Execute the job.
	     *
	     * @param  Mailer  $mailer
	     * @return void
	     */
	    public function handle(Mailer $mailer)
	    {
			//
	    }

	    /**
	     * Handle a job failure.
	     *
	     * @return void
	     */
		public function failed()
		{
			// Richiamato quando il job fallisce...
		}
	}

<a name="riprovare-eseguire-job-fallito"></a>
### Riprovare ad Eseguire un Job Fallito

Per visualizzare una lista di tutti i vari job che sono falliti, basta usare il comando Artisan _queue:failed_. 

	php artisan queue:failed

Tale comando elencherà i vari job includendo informazioni sull'id, la connessione, la coda relativa ed il momento in cui il job stesso è fallito. Avere a disposizione l'id può essere utile se si vuole riprovare ad eseguire un job specifico.

In questo modo:

	php artisan queue:retry 5

Per cancellare un job fallito, invece, usa `queue:forget`:

	php artisan queue:forget 5

Infine, per rimuovere dalla tabella tutti i vari job falliti, usa `queue:flush`:

	php artisan queue:flush
