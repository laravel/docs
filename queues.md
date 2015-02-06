# Code

- [Configurazione](#configurazione)
- [Uso Base](#uso-base)
- [Closure in Coda!](#clousure-coda)
- [Eseguire il Queue Listener](#eseguire-queue-listener)
- [Il Demone del Queue Worker](#demone-queue-worker)
- [Code Push](#code-push)
- [Job Falliti](#job-falliti)

<a name="configurazione"></a>
## Configurazione

Il componente _Queue_ di Laravel offre un'interfaccia unificata a svariati servizi di gestione delle code. Le code ti permettono di schedulare una certa operazione che ha bisogno di un certo tempo piuttosto lungo per la sua esecuzione, perlomeno in rapporto ad una normale richiesta al server. L'invio di email schedulato e non immediato, ad esempio, può velocizzare tantissime richieste.

Il file di configurazione per le code è memorizzato in _config/queue.php_. In questo file troverai tutte le opzioni di configurazione per ognuno dei driver inclusi out of the box con il framework. Nello specifico, i driver riguardano il database,[ Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), [Redis](http://redis.io), null, ed un driver sincrono (per uso locale). Il driver _null_ serve semplicemente ad indicare che non c'è bisogno di mettere in coda una o più operazioni.

### Tabella delle Code

Per usare il driver _database_ avrai bisogno di una tabella che contenga i dati dei vari cronjob. Per generare una migration utile, usa `queue:table`.

	php artisan queue:table

### Altre Dipendenze

Per usare il componente con altri driver potresti aver bisogno di alcune dipendenze.

Eccole:

- Amazon SQS: `aws/aws-sdk-php`
- Beanstalkd: `pda/pheanstalk ~3.0`
- IronMQ: `iron-io/iron_mq`
- Redis: `predis/predis ~1.0`

<a name="uso-base"></a>
## Uso Base

#### Inserire in Coda un Lavoro

Tutti i vari job che si possono mettere in coda vanno messi in _App\Commands_. Per generare un nuovo comando, usa Artisan:

	php artisan make:command SendEmail --queued

Per inserire quindi un nuovo job in coda, usa _push_.

	Queue::push(new SendEmail($message));

Di default, il comando `make:command` di Artisan genera una classe completa di metodo _handle_, che viene richiamato in fase di esecuzione del job in coda. Tieni in considerazione che puoi effettuare senza problemi la method injection di eventuali dipendenze necessarie gestite automaticamente dall'[IoC container](/container).

	public function handle(UserRepository $users)
	{
		//
	}

Nel caso in cui volessi specificare un'intera classe separata per il tuo handler, aggiungi il flag `--handler` a `make:command`:

	php artisan make:command SendEmail --queued --handler

L'handler verrà posizionato in `App\Handlers\Commands` e verrà risolto direttamente dal Container.

#### Specificare la Coda / Tube per un certo Job

Puoi decidere in quale coda inserire un certo job.

	Queue::pushOn('emails', new SendEmail($message));

#### Passare lo Stesso Payload a più Job

Potresti voler passare lo stesso insieme di dati a più job in coda. Usa `Queue::bulk`:

	Queue::bulk(array(new SendEmail($message), new AnotherCommand));

#### Dilazionare l'Esecuzione di un Job

A volte potresti voler dilazionare l'esecuzione di un certo job. Ad esempio, potresti voler inviare un'email ad un cliente 15 minuti dopo la sua registrazione. Basta usare il metodo `Queue::later`, in questo caso:

	$date = Carbon::now()->addMinutes(15);

	Queue::later($date, new SendEmail($message));

In questo esempio stiamo usando [Carbon](https://github.com/briannesbitt/Carbon) per specificare il delay da assegnare al job. Alternativamente, puoi passare al metodo il numero di secondi di delay che desideri.

> **Nota:** Amazon SQS ha un delay massimo di 900 secondi (15 Minuti).

#### Code e Model di Eloquent

Nel caso in cui un job in coda prendesse come parametro del costruttore un model Eloquent, solo l'identificatore principale verrebbe serializzato. Una volta avviato il job in questione, invece, il sistema si occuperebbe automaticamente di recuperare l'istanza completa dal database ed usarla. È una tecnica degna di nota che permette di evitare di occupare molta memoria inutilmente.

#### Cancellare un Job

Dopo aver processato un job, questo viene cancellato dalla coda. Se non vengono lanciate eccezioni durante l'esecuzione, la procedura di eliminazione viene svolta automaticamente.

Se invece vuoi cancellare o "rilasciare" un certo job manualmente, il trait `Illuminate\Queue\InteractsWithQueue` offre l'accesso alle procedure di cui si ha bisogno. Il metodo di _release_ accetta un singolo parametro in input: il numero di secondi che vuoi aspettare prima di rendere il job nuovamente "disponibile".

	public function handle(SendEmail $command)
	{
		if (true)
		{
			$this->release(30);
		}
	}

#### "Rilasciare" un Job in Coda

Nel caso in cui venga sollevata un'eccezione durante l'elaborazione di un job, questo verrà automaticamente risistemato in coda, in modo tale da poter effettuare un altro tentativo. Puoi definire, tramite il flag `--tries`, il numero di tentativi.

#### Controllare il Numero di Tentativi

Se vuoi sapere quanti tentativi sono stati fatti da un certo job, usa _attempts_:

	if ($this->attempts() > 3)
	{
		//
	}

> **Nota:** ricorda di usare il trait `Illuminate\Queue\InteractsWithQueue` se vuoi richiamare questo metodo.

<a name="clousure-coda"></a>
## Closure in Coda!

Se dovessi averne bisogno, puoi decidere anche di mettere una semplice Closure in coda. Per le operazioni più semplici può risultare una comoda scorciatoia.

#### Mandare in Coda una Closure

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

> **Nota:** al posto di rendere alcuni oggetti disponibili alla closure tramite _use_, passa invece le chiavi principali e recupera nuovamente i dati. Si tratta di una procedura più sicura che evita svariati comportamenti inaspettati in fase di serializzazione.

Usando le [push queues](#push-queues) di Iron.io, inoltre, dovresti prendere altre precauzioni aggiuntive. L'end point che riceve i messaggi in coda verificherà anche un token legato alla singola request. Ad esempio, il tuo end point potrebbe essere simile a `https://yourapp.com/queue/receive?token=SecretToken`. Controlla il token prima di lavorare la richiesta.

<a name="eseguire-queue-listener"></a>
## Eseguire il Queue Listener

Laravel include, di default, un task Artisan che si occuperà di eseguire tutti i nuovi job messi in coda. Tale comando è `queue:listen`:

#### Il Queue Listener

	php artisan queue:listen

Puoi anche specificare quale connessione usare per il listener:

	php artisan queue:listen connection

> **Nota:** una volta che il listener inizia a lavorare, continua fin quando non viene fermato manualmente. Se dovessi averne bisogno, quindi, usa un process monitor come [Supervisor](http://supervisord.org/) per assicurarti che tutto vada liscio.

Puoi passare anche una serie di connessioni separate da virgola al comando _listen_ per impostare le priorità:

	php artisan queue:listen --queue=high,low

In questo caso, i vari job presenti in _high_ verranno processati prima di quelli presenti in _low_.

#### Specifica il Timeout per un Job

Puoi specificare il timeout di un job in secondi:

	php artisan queue:listen --timeout=60

#### Specifica i Secondi di Attesa prima del Polling

	php artisan queue:listen --sleep=5

> **Nota:** una coda "dorme" solo se non ci sono job da eseguire.

#### Processare Solo il Primo Job in Coda

	php artisan queue:work

<a name="demone-queue-worker"></a>
## Il Demone del Queue Worker

Il comando `queue:work` include anche un flag `--daemon` che forza il worker a proseguire nel processing dei vari job senza riavviare di volta in volta il framework. Il risultato è una riduzione significativa dell'utilizzo della CPU rispetto ad un _queue:listen_.

	php artisan queue:work connection --daemon

	php artisan queue:work connection --daemon --sleep=3

	php artisan queue:work connection --daemon --sleep=3 --tries=3

Come puoi vedere, il comando _queue:work_ supporta tutti i vari flag visti prima per `queue:listen`.

### Deploy con il Demone del Queue Worker

Il miglior modo di effettuare il deploy di un'applicazione usando i vari worker è di mettere l'applicazione in modalità di manutenzione all'inizio del deploy. Puoi farlo tramite _php artisan down_. Una volta che l'applicazione è in manutenzione, Laravel non accetta più job da mettere in coda, ma continuerà a processare quelli già presenti.

Includi inoltre nel tuo script di deploy il comando di _restart_:

	php artisan queue:restart

> **Nota:** il comando fa affidamento al sistema di cache per schedulare il riavvio. Di default, APCu non lavora con i comandi via CLI. Se usi APCu ricorda di aggiungere al tuo file di configurazione `apc.enable_cli=1`.

### Scrivere Codice per un Worker

I queue worker non riavviano il framework prima di processare ogni job. In ogni caso dovresti comunque fare attenzione a liberare la memoria (soprattutto dagli oggetti più pesanti) prima della fine del job. Ad esempio, se stai lavorando con la libreria GD per le immagini, usa _imagedestroy_ quando hai finito.

Per motivi simili potresti avere qualche problema con la connessione al database. Per essere sicuro di avere sempre una connessione "fresca" usa il metodo `DB::reconnect`.

<a name="code-push"></a>
## Code Push

Le code push ti permettono di usare le varie facility di Laravel dedicate alle code senza dover lavorare con demoni e background listener di ogni sorta. Questo sistema è supportato solo dal driver di [Iron.io](http://iron.io). Prima di iniziare crea un account su Iron.io ed inserisci le credenziali nel file `config/queue.php`.

#### Registrare un Subscriver

Puoi usare il comando `queue:subscribe` di Artisan per registrare un endpoint che riceva i nuovi job.

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

Eseguendo il login su Iron vedrai quindi la cosa, così come l'URL specificata. Crea quindi una route per _queue/receive_ in questo modo:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

Il metodo _marshal_ si occuperà di fare tutto il resto.

<a name="job-falliti"></a>
## Job Falliti

Visto che le cose non vanno sempre come le pianifichi, alcuni job potrebbero fallire. Come hai già visto prima, puoi assegnare il numero di tentativi da effettuare. Cosa fare, però, nel caso in cui volessi segnarti tutto quello che ti sfugge?

Puoi usare il comando `queue:failed-table` per creare una tabella `failed_jobs`.

	php artisan queue:failed-table

Specifica il numero massimo di tentativi...

	php artisan queue:listen connection-name --tries=3

ed è fatta! Gli eventuali job non andati a buon fine verranno registrati qui.

Se dovessi averne bisogno, inoltre, c'è il metodo `Queue::failing` che ti permette di specificare cosa fare in caso di faillimento di un job.

	Queue::failing(function($connection, $job, $data)
	{
		//
	});

In ogni classe di un job, inoltre, puoi specificare un metodo _failed_ che ti permette di decidere cosa fare per il singolo job in caso di fallimento.

	public function failed()
	{
		// Called when the job is failing...
	}

### Riprovare ad Eseguire i Job Falliti

Per visualizzare una lista dei vari job non andati a buon fine, usa

	php artisan queue:failed

Da questa lista puoi ottenere i vari ID, che puoi usare per riprovare un job fallito tramite _retry_:

	php artisan queue:retry 5

Per cancellare un job andato male, invece, puoi usare _forget_.

	php artisan queue:forget 5

Infine, usa _flush_ per cancellare tutto quello che non è andato bene.

	php artisan queue:flush
