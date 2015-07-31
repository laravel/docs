# Errori & Logging

- [Introduzione](#introduzione)
- [Configurazione](#configurazione)
- [Gestire Gli Errori](#gestire-errori)
	- [Metodo Report](#metodo-report)
	- [Metodo Render](#metodo-render)
- [Eccezioni HTTP](#eccezioni-http)
	- [Pagine Di Errore HTTP Personalizzate](#pagine-errore-personalizzate)
- [Logging](#logging)

<a name="introduzione"></a>
## Introduzione

Quando inizi un nuovo progetto con Laravel, la gestione degli errori e delle eccezioni è già configurata e pronta per l'uso. In aggiunta, Laravel integra la libreria di logging [Monolog](https://github.com/Seldaek/monolog), che ti offre supporto per il loggin con una serie di potenti handler.

<a name="configurazione"></a>
## Configurazione

#### Dettagli Errore

I dettagli sull'errore che la tua applicazione visualizza nel browser sono controllati dall'opzione `debug` nel tuo file di configurazione `config/app.php`. Di default, questa opzione e impostata a seconda della variabile d'ambiente `APP_DEBUG`, memorizzata nel file `.env`.

Per lo sviluppo locale, dovresti impostare questa variabile `APP_DEBUG` su `true`. Mentre nell'ambiente di produzione, questo valore dovrebbe essere sempre impostato su `false`.

#### Modalità Di Log

Lavarel supporta le seguenti modalità di log: `single`, `daily`, `syslog` ed `errorlog`. Per esempio, se desideri usare il log gioranilero anziché usare un unico file, puoi impostare semplicemente il valore di `log` nel tuo file di configurazione `config/app.php` in questo modo:

	'log' => 'daily'

#### Configurazione Monolog Personalizzata

Se vuoi avere il completo controllo su come Monolog è configurato per la tua applicazione, puoi usare il metodo `configureMonologUsing`. Dovresti la chiamata a questo metodo nel tuo file  `bootstrap/app.php` prima che venga ritornata la variabile `$app`:

	$app->configureMonologUsing(function($monolog) {
		$monolog->pushHandler(...);
	});

	return $app;

<a name="gestire-errori"></a>
## Gestire Gli Errori

Tutte le eccezioni sono gestite dalla classe `App\Exceptions\Handler`. Questa classe contiene due metodi: `report` e `render`. Esamineremo ognuno di questi metodi nel dettaglio.

<a name="metodo-report"></a>
### Il Metodo Report

Il metodo `report` è usato per memorizzare le eccezioni sul file log o per inviarle ad un servizio esterno come [BugSnag](https://bugsnag.com). Di default, il metodo `report`passa l'eccezione all'implementazione di base della classe parent in cui l'eccezzione inserita nel log. In ogni caso, sei libero di memorizzare le eccezioni nel log come desideri. 

Se hai bisogno di eseguire il report di diversi tipi di eccezione in modi differenti, puoi usare l'operatore di comparazione PHP `instanceof`:

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
		if ($e instanceof CustomException) {
			//
		}

		return parent::report($e);
	}

#### Ignorare Eccessioni Per Tipo

La proprietà `$dontReport`dell'handler delle eccezioni contiene un array di tipi di eccezioni che non saranno inserite nel log. Di default, le eccezioni risultanti da errori 404 non sono scritte sul tuo file di log. Puoi anche aggiungere altri tipi di eccezione a questo array se necessario.

<a name="metodo-render"></a>
### Il Metodo Render

Il metodo `render` è responsabile della conversione di una data eccezione in una risposta HTTP che dovrebbe essere ritornata al browser. Di default, l'eccezione è passata all'implementazione base della classe che genera per te una risposta. In ogni modo, sei libero di controllare il tipo di eccezione oppure ritornare una tua risposta personalizzata:

    /**
     * Render an exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $e
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $e)
    {
    	if ($e instanceof CustomException) {
    		return response()->view('errors.custom', [], 500);
    	}

        return parent::render($request, $e);
    }

<a name="eccezioni-http"></a>
## Eccezioni HTTP

Le eccezioni HTTP si riferiscono ad errori che potrebbero verificarsi durante una richiesta del client. Per esempio, può essere un errore di “pagina non trovata” (404), un errore di “non autorizzato” (401) oppure un errore generato da uno sviluppatore con codice 500. Per fare in modo di ritornare una tale risposta, usa la seguente sintassi: 

	abort(404);

Il metodo `abort` lancerà immediatamente un eccezione la quale sarà renderizzata dalla classe handler delle eccezioni. Opzionalmente, puoi anche fornire un testo per la risposta:

	abort(403, 'Unauthorized action.');

Questo metodo può essere usato in qualsiasi momento durante il cilclo di vita della richiesta.

<a name="pagine-errore-personalizzate"></a>
### Pagine Di Errore HTTP Personalizzate

Laravel ti rende la vita facile per ritornare delle pagine di errore personalizzate per i vari codici di stato HTTP. Per esempio, se vuoi personalizzare la pagina di errore con codice di stato HTTP 404, crea un file in `resources/views/errors/404.blade.php`. Questo file verrà utilizzato su tutti gli errori 404 generati dalla tua applicazione.

Queste view all'interno di questa directory dovrebbero essere nominate in modo tale da conincidere con il codice di stato HTTP corrispondente.

<a name="logging"></a>
## Logging

Il meccanismo di logging di Laravel è realizzato usando la potente libreria [Monolog](http://github.com/seldaek/monolog). Di default, Laravel è configurato per creare un log giornaliero per la tua applicazione che è memorizzato nella directory `storage/logs`. Puoi scrivere informazioni nei log usando la [facade](/docs/5.1/facade) `Log`:

	<?php namespace App\Http\Controllers;

	use Log;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			Log::info('Showing user profile for user: '.$id);

			return view('user.profile', ['user' => User::findOrFail($id)]);
		}
	}

Il sistema di logging fornisce sette livelli di log defini nello standard [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, e **alert**.

	Log::debug($error);
	Log::info($error);
	Log::notice($error);
	Log::warning($error);
	Log::error($error);
	Log::critical($error);
	Log::alert($error);

#### Informazioni Contestuali

Se hai bisogno di passare un array ai metodi della classe Log. Questi dati saranno formattati e visualizzati con il messaggio di log: 

	Log::info('User failed to login.', ['id' => $user->id]);

#### Accesso Ad Un Istanza Monolog

Monolog possiede vari hanlder aggiuntivi che puoi usare per il logging. Se hai bisogno, puoi accedere ad un istanza Monolog usata da Laravel in questo modo:

	$monolog = Log::getMonolog();
