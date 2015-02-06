# Service Provider

- [Introduzione](#introduzione)
- [Esempio Di Provider Base](#esempio-provider-base)
- [Registrazione Provider](#registrazione-provider)
- [Provider Differiti](#provider-differiti)

<a name="introduzione"></a>
## Introduzione

I service provider sono la parte centrale delle operazioni di avvio dell'applicazione di Laravel.
La tua applicazione, così come il core service di Laravel viene avviato dai service provider.

Ma, cosa intendiamo con “avviati”? In generale, intendiamo la **registrazione** di qualcosa, includendo la registrazione dei binding nel container, la creazione di eventi, filtri, e route. I service provider sono la parte centrale della configurazione della tua applicazione.

Se apri il file il file `config/app.php`, noterai un array `providers`. Questi sono tutte le classi di service provider che saranno caricati per la tua applicazione. Ovviamente, molti di loro sono provider “differiti”, significa cioè, che non saranno caricati per ogni richiesta, ma solo quando i servizi forniti saranno necessari.

In questa visione generate imparerai come scrivere i tuoi service provider e registrarli nella tua applicazione Laravel.

<a name="esempio-provider-base"></a>
## Esempio Di Provider Base

Tutti i service provider estendono la classe `Illuminate\Support\ServiceProvider`. Questa classe astratta richiede che tu definisca almeno un metodo nel tuo provider: il metodo `register`. All'interno del metodo `register`, **dovrai eseguire il bind nel [service container](/docs/master/container)**. Non dovrai mai tentare di registrare qualsiasi tra eventi, route o altre funzionalità nel metodo `register`.

I comandi CLI di Artisan possono generare facilmente un nuovo provider tramite il comando `make:provider`:

	php artisan make:provider RiakServiceProvider

### Il Metodo Register

Ora, dai un occhiata a questo service provider di base:

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			$this->app->singleton('Riak\Contracts\Connection', function($app)
			{
				return new Connection($app['config']['riak']);
			});
		}

	}

Questo service provider definisce solo il metodo `register`, ed usa il metodo per definire un'implementazione di `Riak\Contracts\Connection` nel service container. Se non hai presente come il service container lavora, non preoccuparti [lo vedremo presto](/docs/master/container).

Questa classe è definita sotto il namespace `App\Providers` dal momento che rappresenta la posizione di default dei service provider in Laravel. Tuttavia, sei libero di cambiarlo come meglio preferisci. I tuoi service provider possono essere posizionani dovunque visto che Composer può comunque caricarli.

### Il Metodo Boot

Ora, di cosa abbiamo bisogno per registrare un evento all'interno del nostro service provider ? Questo può essere fatto dal metodo `boot`. **Questo metodo è chiamato dopo che tutti gli altri service provider sono stati registrati**, nel senso che puoi accedere agli altri servizi registrati col framework.

	<?php namespace App\Providers;

	use Event;
	use Illuminate\Support\ServiceProvider;

	class EventServiceProvider extends ServiceProvider {

		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Event::listen('SomeEvent', 'SomeEventHandler');
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}

	}

Siamo in grando di inserire le dipendenze per il nostro metodo `boot`. Il service container inietterà automaticamente le dipendenze necessarie:

	use Illuminate\Contracts\Events\Dispatcher;

	public function boot(Dispatcher $events)
	{
		$events->listen('SomeEvent', 'SomeEventHandler');
	}

<a name="registrazione-provider"></a>
## Registrazione Provider

Tutti i service provider, sono registrati nel file di configurazione `config/app.php`. Questo file contiene un array `providers` dove puoi scorrere la lista dei nomi dei tuoi service provider. Di default, viene inserita un'insieme del core dei service provider di Laravel. Questi provider avviano i componenti del cuore di Laravel, come i service mailer, queue, cache ed altri.

Per registrare il tuo provider, aggiungi semplicemente questa riga all'array:

	'providers' => [
		// Other Service Providers

		'App\Providers\AppServiceProvider',
	],

<a name="provider-differiti></a>
## Provider Differiti

Se il tuo provider è registrato **soltanto** come binding nel [service container](/docs/master/container), puoi scegliere di differire la sua registrazione solo se il binding registrato è strettamente necessario. Differire il caricamento di un provider migliorerà le prestazioni della tua applicazione, dal momento che non viene caricato nel filesystem ad ogni richiesta.

Per differire il caricamento di un provider, imposta la proprietà `defer` su `true` e definisci un metodo `provides`. Il metodo `provides` ritorna il binding del service container che il provider registra:

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * Indicates if loading of the provider is deferred.
		 *
		 * @var bool
		 */
		protected $defer = true;

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			$this->app->singleton('Riak\Contracts\Connection', function($app)
			{
				return new Connection($app['config']['riak']);
			});
		}

		/**
		 * Get the services provided by the provider.
		 *
		 * @return array
		 */
		public function provides()
		{
			return ['Riak\Contracts\Connection'];
		}

	}

Laravel compila e memorizza una lista di tutti i servizi forniti dai service provider differiti, insieme al nome della classe dei suoi service provider. Quindi, solo quando si tenta di risolvere uno di questi servizi Laravel carica il service provider appropriato.
