# Configurazione

- [Introduzione](#introduzione)
- [Dopo l'Installazione](#dopo-installazione)
- [Accesso alle Impostazioni](#accesso-impostazioni)
- [Configurazione dell'Ambiente](#configurazione-ambiente)
- [Modalità di Manutenzione](#modalita-manutenzione)

<a name="introduzione"></a>
## Introduzione

Tutti i file di configurazione di Laravel si trovano nella cartella _config_. Ogni singola opzione è stata ampiamente documentata e spiegata (tramite i commenti), quindi la cosa migliore che puoi fare è aprire i singoli file e vedere tu stesso cosa c'è da sistemare per le tue necessità. È sicuramente il modo migliore per acquisire più familiarità con il sistema!

<a name="dopo-installazione"></a>
## Dopo l'Installazione

### Nome dell'Applicazione

Subito dopo aver installato Laravel potresti voler assegnare "un nome" alla tua applicazione. Di default, infatti, la directory _app_ è legata al namespace _App_, soggetto ad autoload con Composer seguendo gli [standard PSR-4 per l'autoloading](http://www.php-fig.org/psr/psr-4/). Tuttavia, potresti avere voglia di cambiare il nome del namespace usato: puoi farlo tranquillamente usando l'apposito comando _app:name_.

Ad esempio, supponiamo che tu voglia chiamare l'applicazione "Horsefly":

	php artisan app:name Horsefly

Chiaramente, rinominare la tua applicazione è totalmente opzionale. Sei liberissimo di lasciare il namespace _App_.

<a name="accesso-impostazioni"></a>
## Accesso alle Impostazioni

Puoi accedere facilmente alle impostazioni della tua applicazione tramite la Facade _Config_.

	$value = Config::get('app.timezone');

	Config::set('app.timezone', 'America/Chicago');

In alternativa, c'è a disposizione anche una funzione helper _config_.

	$value = config('app.timezone');

<a name="configurazione-ambiente"></a>
## Configurazione dell'Ambiente

Risulta spesso molto utile avere a disposizione valori di configurazioni diversi in base all'ambiente di lavoro in cui ci si trova. Per esempio, localmente potremmo voler usare un driver di cache diverso da quello in produzione. Tramite la configurazione basata sull'ambiente di lavoro, si può fare e soprattutto si può fare facilmente.

Nello specifico, Laravel usa la libreria [DotEnv](https://github.com/vlucas/phpdotenv) di Vance Lucas. In un'installazione "fresca fresca" di Laravel troverai un file _.env.example_. Se hai creato un nuovo progetto tramite Composer, invece, il file molto probabilmente sarà già stato rinominato in _.env_.

Tutte le variabili presenti in questo file vengono caricate nell'array _super-global_ *$_ENV*, quando la tua applicazione riceve una richiesta. Puoi usare quindi l'helper _env()_ per recuperare i vari valori da questo array. Se guardi un po' i vari file di configurazione, infatti, noterai che questa funzione viene usata spesso!

Sentiti libero di modificare come meglio credi le tue variabili per l'ambiente locale, così come per quello di produzione. Ad ogni modo, il tuo file _.env_ non dovrebbe essere soggetto a commit in caso di controllo di versione, dato che ogni sviluppatore (o server) potrebbe richiederne uno differente o personalizzato ad hoc.

Se stai sviluppando in team, inoltre, assicurati che venga comunque incluso un _.env.example_, in modo da offrire a chiunque una base di partenza per iniziare a lavorare velocemente al progetto in tempo prossimo allo zero.

#### Accedere alle Impostazioni dell'Ambiente Corrente

Puoi accedere alle impostazioni dell'ambiente corrente tramite il metodo _environment()_ dell'istanza di _Application_:

	$environment = $app->environment();

Puoi anche passare un argomento (o più di uno) al metodo in modo tale da controllare se ci si trova in un certo ambiente oppure no.

	if ($app->environment('local'))
	{
		// Siamo in ambiente 'local'
	}

	if ($app->environment('local', 'staging'))
	{
		// Siamo in ambiente 'local' O 'staging'
	}

Per ottenere un istanza dell'applicazione, risolvi il contratto `Illuminate\Contracts\Foundation\Application` usando il [service container](/container). Se invece stai lavorando in un [service provider](/provider), ricorda sempre che puoi accedere ad un'istanza dell'applicazione tramite_$this->app_.

Puoi inoltre accedere ad un'istanza dell'applicazione tramite il metodo helper _app_ oppure con la Facade _App_.

	$environment = app()->environment();

	$environment = App::environment();

<a name="modalita-manutenzione"></a>
## Modalità di Manutenzione

Se la tua applicazione è in modalità di manutenzione, una view personalizzata verrà mostrata per tutte le richieste in arrivo. Tale funzionalità rende semplice "disabilitare" la tua applicazione per un po', magari durante un update o durante un'operazione di manutenzione. Un controllo di stato di manutenzione è già presente nello stack dell'applicazione. Se quindi il tuo progetto dovesse trovarsi in manutenzione verrà restituita una _HttpException_ con uno status code 503.

Abilitare la modalità di manutenzione è semplicissimo, se si usa Artisan.

	php artisan down

Per ritornare in piena attività, invece, basta usare _up_.

	php artisan up

### Template per la Modalità di Manutenzione

Un template di default per la modalità di manutenzione si può trovare in `resources/templates/errors/503.blade.php`.

### Modalità di Manutenzione e Code

Se la tua applicazione è in modalità di manutenzione, nessun [lavoro in coda](/code) viene eseguito. Una volta ritornata in attività l'applicazione, anche i job cominceranno ad essere nuovamente eseguiti.
