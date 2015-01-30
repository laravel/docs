# Views

- [Utilizzo Base](#basic-usage)
- [View Composers](#view-composers)

<a name="basic-usage"></a>
## Utilizzo Base

Le Views contengono il codice HTML utilizzato dalla tua applicazione, e ha l'utile funzione di separare il Controller e la logica dal'interfaccia grafica. Le Views sono salvate nella cartella `resources/views`.

Ecco un semplice esempio di view:

	<!-- View salvata in resources/views/greeting.php -->

	<html>
		<body>
			<h1>Ciao, <?php echo $name; ?></h1>
		</body>
	</html>

Una view può essere restituita al browser in questo modo:

	Route::get('/', function()
	{
		return view('greeting', ['name' => 'James']);
	});

Come puoi vedere, il primo argomento passato all'helper `view` corrisponde al nome del file da caricare dalla cartella `resources/views`. Il secondo argomento passato all'helper è un array di dati che saranno resi disponibili all'interno della view.

Le views possono essere salvate anche in sotto-cartelle create all'interno della catella `resources/views`. Per esempio, se la tua view è salvata in `resources/views/admin/profile.php`, dovrai restituirla al browser in questo modo:

	return view('admin.profile', $data);

#### Passare Dati Alle Views

	// Approccio classico
	$view = view('greeting')->with('name', 'Victoria');

	// Utilizzo dei Magic Method
	$view = view('greeting')->withName('Victoria');

Nell'esempio precedente, la variabile `$name` sarà acessibile dalla view e conterrà il nome `Victoria`.

Se vuoi, puoi anche passare un array di dati alla view semplicemente usandolo come secondo parametro:

	$view = view('greetings', $data);

#### Condividere Dati Con Tutte Le View

Qualche volta potresti aver bisogno di condividere alcuni dati tra tutte le view utilizzae dalla tua applicazione. Ci sono diversi modi per farlo: l'helper `view`, il [contratto](/docs/master/contracts) `Illuminate\Contracts\View\Factory`, o la wildcard [view composer](#view-composers).

Ecco un esempio di condivisione con l'helper view:

	view()->share('data', [1, 2, 3]);

Puoi anche utilizzare la facade `View`:

	View::share('data', [1, 2, 3]);

Solitamente le chiamate al metodo `share` vengono fatte all'interno del metodo di `boot` di un service provider. Sei libero di aggiungerle all'interno di `AppServiceProvider` o di creare un tuo service provider.

> **Nota:** Quando l'helper `view` viene chiamato senza nessun argomento, viene restituita una implementazione del contratto `Illuminate\Contracts\View\Factory`.

#### Determinare Se Una View Esiste

Se devi controllare se una view esiste lo puoi fare utilizzando il metodo `exists`:

Utilizzo tramite helper:

	if (view()->exists('emails.customer'))
	{
		//
	}

### Restituire Una View Tramite Il Suo Path

Se lo desideri, puoi generare una view utilizzando il suo path assoluto:

	return view()->file($pathToFile);

<a name="view-composers"></a>
## View Composers

Le View composers sono delle callbacks o metodi di una classe che sono chiamati quando viene mostrata una view. Se hai dei dati che vuoi rendere disponibili ogni volta che una view viene utilizzata le view composers sono il posto ideale dove scrivere tutta la logica.

#### Definire Una View Composer

Organizziamo le view composers all'interno di un [service provider](/docs/master/providers). Utilizzeremo la facade `View` per accedere all'implementazione del contratto `Illuminate\Contracts\View\Factory`:

	<?php namespace App\Providers;

	use View;
	use Illuminate\Support\ServiceProvider;

	class ComposerServiceProvider extends ServiceProvider {

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function boot()
		{
			// Using class based composers...
			View::composer('profile', 'App\Http\ViewComposers\ProfileComposer');

			// Using Closure based composers...
			View::composer('dashboard', function()
			{

			});
		}

	}

> **Nota:** Laravel non include di default una cartella per le view composers. Sei libero di organizzarle come preferisci e di salvarle dove ti è più comodo. Per esempio potresti creare la cartella `App\Http\Composers`.

Adesso che hai registrato il tuo composer, il metodo `ProfileComposer@compose` sarà eseguito ogni volta he la view `profile`viene utilizzata. Definiamo una classe:

	<?php namespace App\Http\Composers;

	use Illuminate\Contracts\View\View;
	use Illuminate\Users\Repository as UserRepository;

	class ProfileComposer {

		/**
		 * Implementazione dell'user repository
		 *
		 * @var UserRepository
		 */
		protected $users;

		/**
		 * Crea un nuovo profile composer.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			// Le dipendenze sono automaticamente risolte dal service container
			$this->users = $users;
		}

		/**
		 * Lega i dati alla view.
		 *
		 * @param  View  $view
		 * @return void
		 */
		public function compose(View $view)
		{
			$view->with('count', $this->users->count());
		}

	}

Poco prima che la view venga utilizzata il metodo compose della classe appena creata viene chiamato dall'istanza `Illuminate\Contracts\View\View`. Puoi usare il metodo `with` per legare i dati alla view.

> **Nota:** Tutte le view composers sono risolte attraverso il [service container](/docs/master/container), quindi puoi aggiungere tutte le dipendenze che ti servono all'interno del costruttore del tuo composer.

#### Wildcard View Composers

Il metodo `composer` accetta il carattere `*` come wildcard, quindi puoi attaccare il composer a tutte le view in questo modo:

	View::composer('*', function()
	{
		//
	});

#### Attaccare Un Composer A Multiple Views

Puoi anche attaccare il composer a più views in una volta sola utilizzando:

	View::composer(['profile', 'dashboard'], 'App\Http\ViewComposers\MyViewComposer');

#### Definire Multipli Composer

Puoi utilizzare il metodo `composers` per registrare un gruppo di composer nello stesso momento:

	View::composers([
		'App\Http\ViewComposers\AdminComposer' => ['admin.index', 'admin.profile'],
		'App\Http\ViewComposers\UserComposer' => 'user',
		'App\Http\ViewComposers\ProductComposer' => 'product'
	]);

### View Creators

I View **creators** funzionano quasi allo stesso modo dei view composers; Questi però vengono eseguiti immeditamente dopo che la view viene istanziata. Per registrare un view creator, utilizza il metodo `creator`:

	View::creator('profile', 'App\Http\ViewCreators\ProfileCreator');
