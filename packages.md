# Sviluppo Di Package

- [Introduzione](#introduzione)
- [View](#view)
- [Traduzioni](#traduzioni)
- [Configurazione](#configurazione)
- [Routing](#routing)

<a name="introduzione"></a>
## Introduzione

I packages rappresentano la strada per aggiungere funzionalità a Laravel. I package possono essere un po' di tutto da usare per lavorare con le date come [Carbon](https://github.com/briannesbitt/Carbon), o un intero testing framework come [Behat](https://github.com/Behat/Behat).

Come puoi ben intuire, ci sono svariati tipi di package. Alucni sono stand-alone, significa che possono lavorare con qualsiasi framework, non solo con Laravel. Entrabi i package Carbon e Behat sono esempi di package stand-alone. Qualsiasi di questi package può essere usato con Laravel aggiungendoli al file `composer.json`.

Altri package sono realizzati specificatamente per essere usati con Laravel. Questi package possono avere route, controller, view e configurazioni specifiche intese a migliorare la tua applicazione. Questa parte della guida si concentrerà essenzialmente sui package specifici per Laravel.

Tutti i package di Laravel sono distribuiti via [Packagist](http://packagist.org) e [Composer](http://getcomposer.org), quindi documentati e fai tuoi questi meravigliosi tool di distribuzione dei package PHP.

<a name="view"></a>
## View

La struttura interna del tuo package è completamente nelle tue mani; normalmente ogni package conterrà uno o più [service providers](/docs/master/providers). Il service provider contieni qualsiasi binding [IoC](/docs/master/container), così come le istruzione su dove si trovano le configurazioni del package, le view ed i file di traduzione.

### View

Le view del package sono referenciate usando la sintassi double-colon (doppio punto, ::):

	return view('package::view.name');

Tutto quello che hai bisogno di fare è dire a Laravel dove sono posizionate le view per un dato namespace. Per esempio, se il tuo package si chiama “courier”, potresti aggiungere il codice seguente al metodo boot del tuo service provider:

	public function boot()
	{
		$this->loadViewsFrom('courier', __DIR__.'/path/to/views');
	}

Ora puoi caricare le view del package usando la seguente sintassi:

	return view('courier::view.name');

Quando usi il metodo `loadViewsFrom`, Laravel registra **due** percorsi per le tue view: una nella directory dell'applicazione `resources/views/vendor` e l'altra nella directory da te specificata. Quindi, ritornado al nostro esempio `courier`: quando viene richiesta una view di un package, Laravel controllerà per primo se esiste una versione personalizzata della view fornita dallo sviluppatore in `resources/views/vendor/courier`. Quindi, se non esiste una versione personalizzata, Laravel ricercherà nella directory delle view del tuo package tramite la chiamata a `loadViewsFrom`. Questo è estremanente utile per l'utente finale per personalizzare / sovrascrivere le view del tuo package.

#### Publicare Le View

Per pubblicare le view del tuo package nella directory `resource/views/vendor`, puoi usare il metodo `publishes` nel metodo `boot` del tuo service provider:

	public function boot()
	{
		$this->loadViewsFrom('courier', __DIR__.'/path/to/views');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

Ora, quando un utente che ha scaricato il tuo package, lo esegue con Laravel usando il comando `vendor:publish`, la directory delle tue view sarà copiata nella posizione specifica.

> **Nota:** Puoi usare il metodo `publishes` per pubblicare **qualsiasi** tipo di file verso qualsiasi posizione desideri.

<a name="traduzioni"></a>
## Traduzioni

I file di traduzione del package sono normalmente refernziati usando la sintassi double-colon:

	return trans('package::file.line');

Tutto quello di cui hai bisogno è di dire a Laravel dove si trovano i file di traduzione per un dato namespace. Per esempio, se il tuo package è chiamato "courier", puoi aggiungere la seguente linea di codice nel metodo `boot` del tuo service provider:

	public function boot()
	{
		$this->loadTranslationsFrom('courier', __DIR__.'/path/to/translations');
	}

Nota che all'interno della cartella `translations`, puoi avere altre directory per ogni lingua tu abbia fornito come `en`, `es`, `ru`, etc.

Ora puoi caricare le tue traduzioni usando la seguenti sintassi:

	return trans('courier::file.line');

<a name="configurazione"></a>
## Configurazione

Normalmente, vorrai pubblicare il file di configurazione del tuo package nella directory`config` della propria applicazione. Questo permettà agli utenti che usano il tuo package di sovrascrivere le tue configurazioni di default.

Per pubblicare un file di configurazione, basta usare il metodo `publishes` dal metodo `boot` del tuo service provider:

	$this->publishes([
		__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
	]);

Ora, quando gli utenti eseguiranno il comando di Laravel `vendor:publish`, i tuoi file saranno copiati in una specifica posizione. Ovviamente, una volta che la configurazione è stata pubblicata, sarà accessibile come qualsiai altro file di configurazione:

	$value = config('courier.option');

Puoi anche scegliere di unire il file di configurazione del tuo package con una copia dell'applicazione. Questo permette agli utenti di includere solo le opzioni che realmente vogliono sovrascrivere nella copia pubblicata della configurazione. Per unire le configurazioni, usa il metodo `mergeConfigFrom` nel metodo `register` del tuo service provider:

	$this->mergeConfigFrom(
		'courier', __DIR__.'/path/to/config/courier.php'
	);

<a name="routing"></a>
## Routing

Per caricare un file di route per il tuo package, includilo semplicemente nel metodo `boot` del tuo service provider.

#### Includere Un File Di Route Da Un Service Provider

	public function boot()
	{
		include __DIR__.'/../../routes.php';
	}

> **Nota:** Se il tuo package usa dei controller, avrai bisogno di essere sicuro che siano configurati in modo opportuno nella sezione auto-load del tuo file `composer.json`.
