# Sviluppo di Package

- [Introduzione](#introduzione)
- [Service Provider](#service-provider)
- [Routing](#routing)
- [Risorse](#risorse)
	- [View](#view)
	- [Traduzioni](#traduzioni)
	- [Configurazione](#configurazioni)
- [Asset Pubblici](#asset-pubblici)
- [Pubblicare Gruppi di File](#pubblicare-gruppi-file)

<a name="introduzione"></a>
## Introduzione

I package sono il modo migliore di aggiungere delle nuove funzionalità a Laravel. Un package può svolgere qualsiasi compito: dal gestire al meglio le date, come fa [Carbon](https://github.com/briannesbitt/Carbon), fino al costituire un intero BDD testing framework come [Behat](https://github.com/Behat/Behat).

Di conseguenza, come puoi facilmente immaginare, ci sono svariati tipi di package. Alcuni di questi sono stand-alone: funzioneranno con qualsiasi framework e non solo con Laravel. Carbon e Behat sono di questo tipo. Per lavorarci non dovrai fare altro che aggiungerli al tuo file _composer.json_.

Dall'altra parte puoi trovare dei package creati proprio per Laravel. Questi package avranno le proprie route, controller, view e così via. Questa parte della documentazione coprirà di più questa seconda tipologia di package.

<a name="service-provider"></a>
## Service Provider

I [service provider](/docs/5.1/provider) sono il punto di connessione tra un package e Laravel. Un service provider ha la responsabilità di effettuare i binding dei vari "oggetti" di un package nel [service container](/docs/5.1/container) ed informare Laravel come e dove caricare le diverse risorse, come view, file di configurazione e così via.

Un service provider estende la classe `Illuminate\Support\ServiceProvider` e contiene due metodi: `register` e `boot`. La classe base `ServiceProvider` si trova nel package `illuminate/support`, che dovresti quindi aggiungere alle tue dipendenze nel caso in cui tu voglia creare un package tutto tuo.

Se vuoi avere più informazioni sui service provider, dai uno sguardo alla [pagina dedicata qui sulla documentazione](/docs/5.1/provider).

<a name="routing"></a>
## Routing

Per definire le route del tuo package, tutto quello che devi fare è effettuare il _require_ del file dal metodo _boot_ del service provider. Dal route file in questione potresti continuare ad usare tranquillamente la facade _Route_ per [registrare le route](/docs/5.1/routing) di cui hai bisogno:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		if (! $this->app->routesAreCached()) {
			require __DIR__.'/../../routes.php';
		}
	}

<a name="risorse"></a>
## Risorse

<a name="view"></a>
### View

Per registrare le [view](/docs/5.1/view) del tuo package dovrai spiegare a Laravel dove cercare tali view. Nulla di complesso: basterà usare il metodo _loadViewsFrom_ del service provider. Il metodo accetta due argomenti: il path della cartella dove tieni le view ed il nome del package. Supponendo che il tuo package si chiami _courier_, ecco un esempio di istruzione da mettere nel metodo _boot_.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
	}

Le view di un package vengono "referenziate" usando due volte il carattere dei due punti, con una sintassi del genere:

	package::view

Quindi, ad esempio, per caricare la view "admin" del package _courier_ dovrai usare:

	Route::get('admin', function () {
		return view('courier::admin');
	});

#### Sovrascrivere le View di un Package

Quando usi _loadViewsFrom_ Laravel registra *due* location per le tue view. Una è nella tua applicazione, in _resources/views/vendor_ ed una nella directory da te specificata. Quindi, ad esempio, usando il nostro package _courier_, Laravel controllerà prima se la versione "custom" di una view è stata messa in _resources/views/vendor/courier_. In caso contrario, la view verrà cercata nel path specificato nella chiamata a _loadViewFrom_.

#### Pubblicare le View

A volte potresti avere la necessità di rendere disponibili le view del tuo package nella cartella _resources/views/vendor_. Il metodo da usare, in questo caso, è _publishes_. Tale metodo accetta un array di percorsi con i rispettivi path di pubblicazione.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

A quel punto, usando il comando Artisan _vendor:publish_, Laravel copierà tutte le view nel path specificato.

Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your views package's will be copied to the specified location.

<a name="traduzioni"></a>
### Traduzioni

Se il tuo package contiene dei [file di traduzione](/docs/5.1/localization), potrai usare il metodo `loadTranslationsFrom` per spiegare a Laravel dove trovare tali file. Ad esempio:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
	}

Le traduzioni vengono referenziate allo stesso modo dele view. La sintassi è

	package::file.linea_da_tradurre

Quindi, per mostrare la linea _welcome_ del file _messages_ del package _courier_, userai

	echo trans('courier::messages.welcome');

<a name="configurazioni"></a>
### Configurazione

Molto probabilmente, nei tuoi package inserirai alcune informazioni in specifici file di configurazione. Altrettanto probabilmente vorrai pubblicare tali file all'interno della cartella _config- della tua applicazione. Pubblicare un file di configurazione è molto semplice: innanzitutto, devi usare il metodo _publishes_ dal metodo _boot_ del tuo service provider.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
		]);
	}

A questo punto non rimane altro che eseguire il comando `vendor:publish` ed il file sarà subito disponibile. La sintassi per accedervi sarà esattamente la stessa usata in precedenza.

	$value = config('courier.option');

#### Configurazione di Default del Package

Potresti scegliere, eventualmente, di "fondere" i file di configurazione del tuo package con quelli dell'applicazione. In questo modo, l'utente finale dovrà solo specificare le opzioni che vuole davvero sovrascrivere, sistemandole nella copia pubblicata del file di configurazione. Se vuoi offrire questa possibilità il metodo da usare è `mergeConfigFrom`, che va chiamato a sua volta dal metodo `register` del service provider:

	/**
	 * Register bindings in the container.
	 *
	 * @return void
	 */
	public function register()
	{
		$this->mergeConfigFrom(
			__DIR__.'/path/to/config/courier.php', 'courier'
		);
	}

<a name="asset-pubblici"></a>
## Asset Pubblici

I tuoi package potrebbero aver bisogno di asset Javascript, CSS oppure immagini. Nessun problema, anche qui il metodo _publishes_ viene in tuo soccorso come visto per i file di configurazione.

In questo esempio abbiamo aggiunto anche un tag _public_ tra i parametri del metodo _publishes_ per identificare questi tag.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/path/to/assets' => public_path('vendor/courier'),
		], 'public');
	}

Non rimane che usare _vendor:publish_ (in questo caso, per uno specifico tag) ed il gioco è fatto! Ho inoltre usato il flag _--force_ per forzare il publishing dei file.

	php artisan vendor:publish --tag=public --force

<a name="pubblicare-gruppi-file"></a>
## Pubblicare Gruppi di File

Un'altra cosa che potrebbe essere utile è la pubblicazione di gruppi di asset e risorse in modo separato. Ad esempio, immagina di poter pubblicare i file di configurazione del tuo package senza però dover pubblicare gli altri asset allo stesso tempo. Una soluzione ottima, come hai visto poco fa, è il tagging.

Il suo funzionamento è semplice: ogni volta che chiami il metodo _publishes_, puoi assegnare un tag agli asset pubblicati specificando tale tag come parametro aggiuntivo. Definiamo ad esempio due gruppi: _config_ e _migrations_.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/../config/package.php' => config_path('package.php')
		], 'config');

		$this->publishes([
			__DIR__.'/../database/migrations/' => database_path('/migrations')
		], 'migrations');
	}

Il gioco è fatto: adesso, per pubblicare SOLO i file di configurazione, dovrai usare

	php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"
