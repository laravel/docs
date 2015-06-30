# Service Provider

- [Introduzione](#introduzione)
- [Scrivere Un Service Provider](#scrivere-service-provider)
	- [Il Metodo Register](#il-metodo-register)
	- [Il Metodo Boot](#il-metodo-boot)
- [Registare I Provider](#registrare-provider)
- [Provider Differiti](#provider-differiti)

<a name="introduzione"></a>
## Introduzione

I service provider sono la parte centrale delle operazioni di avvio dell'applicazione di Laravel. La tua applicazione, così come il core service di Laravel viene avviato dai service provider.

Ma, cosa intendiamo con “avviati”? In generale, intendiamo la **registrazione** di qualcosa, includendo la registrazione dei binding nel container, la creazione di eventi, filtri, e route. I service provider sono la parte centrale della configurazione della tua applicazione. 

Se apri il file `config/app.php` incluso con Laravel, noterai un array `providers`. Questi sono tuttie le classi service provider che saranno caricati per la tua applicazione. Ovviamente, molti di questi provider sono dei provider “differiti”, nel senso che non saranno caricati ad ogni richiesta, ma solo quando realmente necessari.

In questa visione generate imparerai come scrivere i tuoi service provider e registrarli nella tua applicazione Laravel.

<a name="scrivere-service-provider"></a>
## Scrivere Un Service Provider

Tutti i service provider estendono la classe `Illuminate\Support\ServiceProvider`. Questa classe astratta richiede che tu definisca almeno un metodo nel tuo provider: `register`. All'interno del metodo `register`, dovrai **eseguire il bind nel [service container](/docs/{{version}}/container)**. Non dovrai mai tentare di registrare qualsiasi tra eventi, route o altre funzionalità nel metodo `register`.

Puoi generare un nuovo provider tramite il comando Artisan `make:provider`:

	php artisan make:provider RiakServiceProvider

<a name="il-metodo-register"></a>
### Il Metodo Register

Come detto precedentemente, all'interno del  metodo `register`, dovrai eseguire il bind nel  [service container](/docs/{{version}}/container). Non dovrai mai tentare di registrare qualsiasi tra eventi, route o altre funzionalità all'interno del metodo `register`. Altrimenti, potresti accidentalmente usare un service provider che non è stato ancora caricato.

Ora, diamo uno squadro a questo semplice service provider:

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider
	{
		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			$this->app->singleton('Riak\Contracts\Connection', function ($app) {
				return new Connection(config('riak'));
			});
		}
	}

Questo service provider definisce solo il metodo `register`, ed usa questo metodo per definire un implementazione di `Riak\Contracts\Connection` nel service container. Se non hai ancora capito come funziona il service container, dai un occhiata alla [sua documentazione](/docs/{{version}}/container).

<a name="il-metodo-boot"></a>
### Il Metodo Boot

Ora, di cosa abbiamo bisogno per registrare un evento all'interno del nostro service provider ? Questo può essere fatto dal metodo `boot`. **Questo metodo è chiamato dopo che tutti gli altri service provider sono stati registrati**, nel senso che puoi accedere agli altri servizi registrati col framework.

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;

	class EventServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			view()->composer('view', function () {
				//
			});
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

#### Dependency Injection nel Metodo Boot

Abbiamo la possibilità di inserire le dipendenze per il nostro metodo `boot`. Il [service container](/docs/{{version}}/container) inietterà automaticamente le dipendenze necessarie: 

	use Illuminate\Contracts\Routing\ResponseFactory;

	public function boot(ResponseFactory $factory)
	{
		$factory->macro('caps', function ($value) {
			//
		});
	}

<a name="registrare-provider"></a>
## Registare I Provider

Tutti i service provider sono registrati nel file `config/app.php`. Questo file contiene un array `providers` dove puoi scorrere la lista dei nomi dei tuoi service provider. viene inserita un'insieme del core dei service provider di Laravel. avviano i componenti del cuore di Laravel, come i service  mailer, queue, cache, ed altri.

Per registrare il tuo provider, aggiungilo all'array:

	'providers' => [
		// Other Service Providers

		'App\Providers\AppServiceProvider',
	],

<a name="provider-differiti"></a>
## Provider Differiti

Se il tuo provider è registrato **solo**come binding nel [service container](/docs/{{version}}/container), puoi scegliere di differire la sua registrazione solo se il binding registrato è strettamente necessario. Differire il caricamento di un provider migliorerà le prestazioni della tua applicazione, dal momento che non viene caricato nel filesystem ad ogni richiesta.

Per differire il caricamento di un provider, imposta la proprietà `defer` su `true` e definisci un metodo `provides`. Il metodo `provides`ritorna il binding del service container che il provider registra: 

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider
	{
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
			$this->app->singleton('Riak\Contracts\Connection', function ($app) {
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
