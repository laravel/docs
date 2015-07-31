# View

- [Uso Base](#uso-base)
	- [Pssare Dati Alle View](#passare-dati-alle-view)
	- [Condividere Dati Con Tutte Le View](#condividere-dati-con-tutte-le-view)
- [View Composers](#view-composers)

<a name="uso-base"></a>
## Uso Base

Le View contengono il codice HTML utilizzato dalla tua applicazione, e ha l'utile funzione di separare il Controller e la logica dal'interfaccia grafica. Le View sono salvate nella cartella `resources/views`.

Ecco un semplice esempio di view:

	<!-- View stored in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Hello, <?php echo $name; ?></h1>
		</body>
	</html>

Puoi ritornare una view usando la funzione di helper globale `view` in questo modo:

	Route::get('/', function ()	{
		return view('greeting', ['name' => 'James']);
	});

Come puoi vedere, il primo parametro passato all'helper `view` corrisponde al nome del file della view presente nella directory `resources/views`. Il secondo parametro passato all'helper è un arrau di dati che saranno resi disponibili nella view. In questo caso, stiamo passando la variabile `name`, la quale ssarà visualizzta nella view eseguendo un `echo` sulla variabile.

Ovviamente, le view possono anche essere annidate all'interno di sub directory di `resources/views`. Puoi usare la notazione "dot" per referenziare delle view annidate. Per esmpio, se la tua view profile si trova in `resources/views/admin/profile.php`, puoi referenziarla in questo modo:

	return view('admin.profile', $data);

#### Determinare se una View Esiste

Se hai bisogno di determinare se una view esiste, puoi usare il metodo `exists` dopo la chiamata all'helper `view` senza parametri. Questo metodo ritornerà `true` se la view è presente sul disco:

	if (view()->exists('emails.customer')) {
		//
	}

Quando il metodo helper `view` è richiamato senza parmaetri, viene ritornata un istanza di `Illuminate\Contracts\View\Factory`, che ti permette di accedere ai metodi di questa factory.
<a name="dati-view"></a>
### Dati View

<a name="passare-dati-alle-view"></a>
#### Pssare Dati Alle View

Come hai visto nel precedente esempio, puoi passare facilmente un array di dati alle view:

	return view('greetings', ['name' => 'Victoria']);

Quando passi informazioni in questa modo, `$data` deve essere una rray con coppie di chiave/valore. Nella tua view, puoi accedere ad ogni valore usando la chiave corrispondente, come `<?php echo $key; ?>`. Come alternativa al passaggio di un array di dati completo all'helper `view`, puoi usare il metodo `with` per aggiungere singoli dati alla view:

	$view = view('greeting')->with('name', 'Victoria');

<a name="condividere-dati-con-tutte-le-view"></a>
#### Condividere Dati Con Tutte Le View

Qualche volta potresti aver bisogno di condividere alcuni dati tra tutte le view utilizzate dalla tua applicazione. Puoi farlo usando il metodo `share`. Solitamente, puoi inserire la chiamata a `share` all'interno del metodo `boot` di un service provider. Sei libero di aggiungerle in `AppServiceProvider` o generare un service provider separato per usarle:

	<?php namespace App\Providers;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			view()->share('key', 'value');
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

<a name="view-composer"></a>
## View Composer
Le View composer sono delle callback o metodi di una classe che sono chiamati quando una view viene visualizzata. Se hai dei dati che vuoi rendere disponibili ogni volta che una view viene utilizzata le view composer sono il posto ideale dove scrivere tutta la logica.

Andiamo a registrare le nostre view composer all'interno del [service provider](/docs/5.1/provider). Useremo l'helper `view` per accedere all'implementazione del contract `Illuminate\Contracts\View\Factory`. Ricordati, Laravel non include una directory di default per le view composer. Sei libero di organizzarle come meglio desideri. Per esempio, puoi crare una directory `App\Http\ViewComposers`:

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider
	{
		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot()
		{
			// Using class based composers...
			view()->composer(
				'profile', 'App\Http\ViewComposers\ProfileComposer'
			);

			// Using Closure based composers...
			view()->composer('dashboard', function ($view) {

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

Ricorda, se crei un nuovo service provider per contenere le tue view composer, dovrai aggiunge il nuovo service provider all'array `providers` nel file di configurazione `config/app.php`.

Ora che abbiamo registrato il composer, il metodo `ProfileComposer@compose` sarà eseguito ogni volta che la view `profile` sarà visualizzata. Quindi, definiamo la nostra classe composer:

	<?php namespace App\Http\ViewComposers;

	use Illuminate\Contracts\View\View;
	use Illuminate\Users\Repository as UserRepository;

	class ProfileComposer
	{
		/**
		 * The user repository implementation.
		 *
		 * @var UserRepository
		 */
		protected $users;

		/**
		 * Create a new profile composer.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			// Dependencies automatically resolved by service container...
			$this->users = $users;
		}

		/**
		 * Bind data to the view.
		 *
		 * @param  View  $view
		 * @return void
		 */
		public function compose(View $view)
		{
			$view->with('count', $this->users->count());
		}
	}

Appena prima che la view venga visualizzata, il metodo del composer `compose` è richiamato con l'istanza di `Illuminate\Contracts\View\View`. Puoi usare il meteodo `with`per aggiungere dati alla view.

> **Nota:** Tutte le view composer sono risolte tramite [service container](/docs/5.1/container), quindi puoi importare qualsiasi dipendenza tu abbia bisogno all'interno del construttore della classe composer creata.

#### Collegare Un Composer A Più View

Puoi anche collegare una view composer a più view alla volta, passando un array di view come primo parametro del metodo `composer`:

	view()->composer(
		['profile', 'dashboard'],
		'App\Http\ViewComposers\MyViewComposer'
	);

Il metodo `composer` accetta il carattere `*` come wildcard, permettendoti di collegare un composer a tutte le view:

	view()->composer('*', function ($view) {
		//
	});

### View Creator

Le View **creator** sono molto simili ai view composer; tuttavia, questi vengono eseguiti immeditamente dopo che la view viene istanziata. Per registrare un view creator, utilizza il metodo `creator:

	view()->creator('profile', 'App\Http\ViewCreators\ProfileCreator');
