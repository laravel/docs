# Errori & Logging

- [Configurazione](#configurazione)
- [Gestire Gli Errori](#gestire-gli-errori)
- [HTTP Exception](#http-exception)
- [Logging](#logging)

<a name="configurazione"></a>
## Configurazione

Il debugging della tua applicazione è configurato nella classe bootstrapper `Illuminate\Foundation\Bootstrap\ConfigureLogging`. Questa classe utilizza l'opzione di configurazione `log` del file `config/app.php`.

Di default, il logger è configurato per essere aggiornare il file log giornalmente; tuttavia, puoi personalizzare questa funzionalità se necessario.
By default, the logger is configured to use daily log files; however, you may customize this behavior as needed. Dal momento in cui Laravel usa la popolare libreria di logging [Monolog](https://github.com/Seldaek/monolog), puoi usufruire dei molti metodi che Monolog offre per gestire il log.

Per esempio, se vuoi usare un singolo file log invece che dei log giornalieri, puoi eseguire la modifica seguente al file di configurazione `config/app.php`:

	'log' => 'single'

Laravel supporta le modalità di log `single`, `daily`, e `syslog`. Tuttavia, sei libero di personalizzare il logging per la tua applicazione come desideri, sovrascrivendo la calsse bootstrapper  `ConfigureLogging`.

### Dettagli Errori

La quantità di dettagli d'errore che la tua applicazione visualizza è gestita dall'opzione di configurazione `app.debug` nel file di configurazione `config/app.php`. Di default, quest'opzione di configurazione è impostata in modo tale da rispettare la variabile d'ambiente `APP_DEBUG`, memorizzata nel file `.env`.

Per lo sviluppo in locale, dovresti impostare la variabile d'ambiente `APP_DEBUG` su `true`. **Nel tuo ambiente di produzione, questo valore dovrebbe essere imposto `false`.**

<a name="gestione-errori"></a>
## Gestione Errori

Tutte le eccezioni sono gestite dalla classe `App\Exceptions\Handler`. Questa classe contiene due metodi: `report` e `render`.

Il metodo `report` è usato per memorizzare le eccezioni sul file log o per essere inviate ad un servizio esterno come [BugSnag](https://bugsnag.com). Di default, il metodo `report` passa l'eccezione all'implementazione di base della classe parent in cui l'eccezzione inserita nel log. In ogni caso, sei libero di memorizzare le eccezioni nel log come desideri. Se hai bisogno di eseguire il report di diversi tipi di eccezione in modi differenti, puoi usare l'operatore di comparazione PHP  `instanceof`:

	/**
	 * Report or log an exception.
	 *
	 * This is a great spot to send exceptions to Sentry, Bugsnag, etc.
	 *
	 * @param  \Exception  $e
	 * @return void
	 */
	public function report(Exception $e)
	{
		if ($e instanceof CustomException)
		{
			//
		}

		return parent::report($e);
	}

Il metodo `render` è responsabile della conversione dell'eccezione in una risposta HTTP che dovrebbe essere ri-inviata al browser. Di default, l'eccezione è passata alla classe base che genera per te le risposte. Tuttavia, sei libero di controllare il tipo di eccezione o ritornare una risposta personalizzata.

La proprietà `dontReport` dell'handler delle eccezioni contiene un array di tipi di eccezioni che non saranno inserite nel log. Di default, le eccezioni risultanti da errori 404 non sono scritte sul tuo file di log. Puoi anche aggiungere altri tipi di eccezione a questo array se necessario.

<a name="http-exception"></a>
## HTTP Exception

Le eccezioni HTTP si riferiscono ad errori che potrebbero verificarsi durante una richiesta del client. Per esempio, può essere un errore di “pagina non trovata” (404), un errore di “non autorizzato” (401) oppure un errore generato da uno sviluppatore con codice 500. Per fare in modo di ritornare una tale risposta, usa la seguente sintassi:

	abort(404);

In modo opzionale, puoi fornire una risposta:

	abort(403, 'Unauthorized action.');

Questo metodo può essere usato tutte le volte durante il lifecycle di una richiesta.

### Custom 404 Error Page

Per ritonare una view personalizzata per tutti gli errori 404, crea un file `resources/views/errors/404.blade.php`. Questa view sarà visualizzata per tutti gli errori 404 generati dalla tua applicazione.

<a name="logging"></a>
## Logging

meccanismi di logging di Laravel sono costruiti usando il potente [Monolog](http://github.com/seldaek/monolog). Di default, Laravel è configurato in modo tale da creare un log giornaliero per la tua applicazione memorizzandolo nella directory `storage/logs`. Puoi registrare informazioni nel file di log del tipo:

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

Il sistema di logging fornisce sette livelli di log defini nello standard [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, ed **alert**.

Se hai bisogno di passare un array ai metodi della classe Log, puoi farlo nel seguente modo:

	Log::info('Log message', ['context' => 'Other helpful information']);

Monolog dispone di una varietà di gestori aggiuntivi che si possono usare per il logging. Se necessario, puoi accedere all’istanza Monolog sottostante utilizzata da Laravel in questo modo: 

	$monolog = Log::getMonolog();

Puoi anche registrare ubn evento per intercettare tutti i messaggi passati al log:

#### Creare Un Listener Del Log

	Log::listen(function($level, $message, $context)
	{
		//
	});
