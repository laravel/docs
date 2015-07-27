# Eloquent: Primi Passi

- [Introduzione](#introduzione)
- [Definire i Model](#definire-model)
	- [Le Convenzioni di un Model Eloquent](#convenzioni-model-eloquent)
- [Ricerca di Più Model](#ricerca-piu-model)
- [Recuperare Model Singoli / Aggregati](#recuperare-model-singoli)
	- [Recuperare gli Aggregati](#recuperare-aggregati)
- [Inserimento ed Update di Model](#inserimento-update-model)
	- [Insert Semplici](#insert-semplici)
	- [Update Semplici](#update-semplici)
	- [Assegnamento di Massa](#assegnamento-massa)
- [Cancellazione dei Model](#cancellazione-model)
	- [Soft Deleting](#soft-deleting)
	- [Query sui Soft Deleted Model](#query-soft-deleted-model)
- [Query Scope](#query-scope)
- [Eventi](#eventi)
	- [Uso Base](#eventi-uso-base)

<a name="introduzione"></a>
## Introduzione

Eloquent ORM, la bellissima e comoda implementazione di Active Record fornite out of the box con Laravel, ti permette di lavorare con estrema facilità su ltuo database. Ogni tabella del database ha un suo "Model" corrispondente, che a sua volta viene usato appunto per comunicare e lavorare con tale tabella. I model ti permettono di effettuare delle query, così come le varie operazioni di inserimento, modifica e cancellazione.

Prima di iniziare, assicurati di aver configurato correttamente la tua connessione in _config/database.php_. Per maggiori informazioni sulla configurazione del tuo database, dai uno sguardo a [questa pagina dedicata](/docs/5.1/database#configurazione).

<a name="definire-model"></a>
## Definire i Model

Iniziamo dalla creazione di un model Eloquent. Normalmente saranno piazzati nella directory _app_, ma puoi comunque decidere di metterli altrove, in base alle tue esigenze. In ogni caso, assicurati che le impostazioni nel tuo file _composer.json_ permettano l'autoloading in modo corretto. Tutti i model estendono la classe `Illuminate\Database\Eloquent\Model`.

Il modo più semplice di creare un model è l'uso del comando `make:model` [di Artisan](/docs/5.1/artisan):

	php artisan make:model User

Puoi anche generare una [migration per il database](/docs/5.1/schema#migration) per l'occasione. In tal caso usa l'opzione `--migration` o `-m`:

	php artisan make:model User --migration

	php artisan make:model User -m

<a name="convenzioni-model-eloquent"></a>
### Le Convenzioni di un Model Eloquent

Bene, adesso osserva questa classe di esempio _Flight_. Si tratta di un model e può essere usata per recuperare o memorizzare informazioni nella tabella _flights_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
	    //
	}

Cosa? Tutto qui? Si: continua a leggere per capire perché.

#### Nomi delle Tabelle

Se ci fai caso, non abbiamo riportato da nessuna parte il collegamento tra _Flight_, il model, e _flights_, la tabella. Eppure, il model così com'è funziona. Questo perché, a meno che non venga specificato diversamente, Laravel cercherà automaticamente di usare la tabella dal nome equivalente al plurale _snake case_ della classe. Insomma, Laravel assumerà da _Flight_ l'esistenza di una tabella _flights_. Comodo, eh?

In caso tu voglia usare una tabella diversa, comunque, non c'è problema. Basta specificare la proprietà _table_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The table associated with the model.
		 *
		 * @var string
		 */
		protected $table = 'my_flights';
	}

#### Chiavi Primarie

Eloquent assumerà inoltre la presenza di una chiave primaria per ogni tabella, chiamata _id_. Come per il nome della tabella, se vuoi puoi definire una proprietà _primaryId_.

#### Timestamp

Di default, Eloquent si aspetta di poter usare due colonne *created_at* ed *updated_at* per ogni tabella, realizzate ad hoc per tenere traccia della data di creazione e dell'ultimo update. Nel caso in cui tu non voglia usare questa feature per un model in particolare, puoi sempre impostare su _false_ la proprietà _timestamps_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * Indicates if the model should be timestamped.
		 *
		 * @var bool
		 */
		public $timestamps = false;
	}

Puoi modificare il formato del tuo timestamp, se vuoi: basta usare la proprietà _dateFormat_ del tuo model. Tale proprietà determinerà il formato di salvataggio su database, così come quello adoperato durante la serializzazione del dato come array o JSON.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The storage format of the model's date columns.
		 *
		 * @var string
		 */
		protected $dateFormat = 'U';
	}

<a name="ricerca-piu-model"></a>
## Ricerca di Più Model

Una volta creato il tuo model e la [tabella corrispondente su database](/docs/5.1/schema), sei pronto per iniziare a lavorare. Per capirci, puoi immaginare il tuo model come una versione avanzata del [query builder](/docs/5.1/query-builder) che hai visto prima. Ecco un primo esempio:

	<?php namespace App\Http\Controllers;

	use App\Flight;
	use App\Http\Controllers\Controller;

	class FlightController extends Controller
	{
		/**
		 * Show a list of all available flights.
		 *
		 * @return Response
		 */
		public function index()
		{
			$flights = Flight::all();

			return view('flight.index', ['flights' => $flights]);
		}
	}

#### Accedere ai Valori delle Colonne

Una volta ottenuta un'istanza di un model, puoi accedervi come fai normalmente con un qualsiasi oggetto. Ad esempio, dato un elenco di voli, ecco come accedere al nome di ognuno di essi:

	foreach ($flights as $flight) {
		echo $flight->name;
	}

#### Aggiunta di Condizioni Ulteriori

Il metodo _all_ recupera tutti i risultati presenti sulla tabella del model. Tuttavia, come già detto, puoi usare il model come un query builder: il che vuol dire che puoi aggiungervi ulteriori condizioni in fase di ricerca. Le stesse viste prima, proprio per il query builder. Il metodo _get_ viene usato per recuperare i risultati effettuando la query.

	$flights = App\Flight::where('active', 1)
				   ->orderBy('name', 'desc')
				   ->take(10)
				   ->get();

> **Nota:** visto che i model Eloquent sono dei query builder, dai un'occhiata alla reference dei metodi del [query builder](/docs/5.1/query-builder). Puoi usarli tutti.

#### Collezioni

I metodi trigger _all_ e _get_ di Eloquent ritornano in genere un "array" di risultati, un insieme. È il momento di fare chiarezza: per essere precisi, viene ritornata un'istanza di `Illuminate\Database\Eloquent\Collection`. La classe _Collection_ [fornisce svariati metodi molto utili](/docs/5.1/eloquent-collection) per lavorare adeguatamente con i risultati delle proprie query. Come già visto prima, comunque, nulla ti vieta di iterare all'interno della collection come fosse un array. La semplicità prima di tutto:

	foreach ($flights as $flight) {
		echo $flight->name;
	}

#### Chunking dei Risultati

Quando c'è da processare svariate migliaia di record, puoi usare _chunk_. Tale metodo recupererà una "parte" dei model Eloquent, dandoli in pasto ad una specifica _Closure_ che si occupi di processarli.

	Flight::chunk(200, function ($flights) {
		foreach ($flights as $flight) {
			//
		}
	});

Il primo parametro passato al metodo è il numero di record che vuoi ricevere per ogni _chunk_. La closure passata come secondo argomento, invece, viene richiamata per ogni singolo _chunk_ recuperato dal database.

<a name="recuperare-model-singoli"></a>
## Recuperare Model Singoli / Aggregati

Ovviamente, in aggiunta al recupero di tutti i record di una certa tabella, puoi anche recuperare un singolo record usando i metodi _find_ o _first_. Al posto di ritornare una collezione, stavolta, questi metodi ritorneranno la singola istanza.

	// Recupera un model partendo dalla sua chiave primaria...
	$flight = App\Flight::find(1);

	// Recupera il primo model che rispetta delle condizioni...
	$flight = App\Flight::where('active', 1)->first();

#### Eccezioni "Not Found"

A volte potresti voler decidere di lanciare un'eccezione qualora un model non venga trovato. Può essere particolarmente utile lavorando con i controller o con le route. I metodi _findOrFail_ o _firstOrFail_ recupereranno ugualmente il primo record del risultato. Tuttavia, in caso di risultato non trovato, verrà lanciata un'eccezione di tipo `Illuminate\Database\Eloquent\ModelNotFoundException`:

	$model = App\Flight::findOrFail(1);
	$model = App\Flight::where('legs', '>', 100)->firstOrFail();

Se tale eccezione non viene presa in considerazione da un eventuale blocco _try/catch_, una risposta HTTP 404 viene rimandata all'utente.

If the exception is not caught, a `404` HTTP response is automatically sent back to the user, so it is not necessary to write explicit checks to return `404` responses when using these methods:

	Route::get('/api/flights/{id}', function ($id) {
		return App\Flight::findOrFail($id);
	});

<a name="recuperare-aggregati"></a>
### Recuperare gli Aggregati

Visto che si parla di un query builder "speciale", anche in Eloquent puoi usare le funzioni aggregato come _count_, _sum_, _max_ e così via. Tali metodi ritornano un valore scalare appropriato, al posto di istanze del model.

	$count = App\Flight::where('active', 1)->count();
	$max = App\Flight::where('active', 1)->max('price');

<a name="inserimento-update-model"></a>
## Inserimento ed Update di Model

<a name="insert-semplici"></a>
### Insert Semplici

Per creare un nuovo record nel tuo database, crea una nuova instanza del model, imposta gli attributi come desideri e, quindi, chiama il metodo _save()_.

	<?php namespace App\Http\Controllers;

	use App\Flight;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class FlightController extends Controller
	{
		/**
		 * Create a new flight instance.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			// Validate the request...

			$flight = new Flight;

			$flight->name = $request->name;

			$flight->save();
		}
	}

In questo esempio, assegnamo il parametro _name_ all'attributo _name_ dell'istanza di _App\Flight_. Richiamando il metodo _save()_, il record verrà salvato su database. I timestamp *created_at* ed *updated_at* verranno automaticamente salvati, senza la necessità di impostarli manualmente.

<a name="update-semplici"></a>
### Update Semplici

Il metodo _save()_ può essere usato anche per l'update di un model e non solo per il suo inserimento. Per aggiornare un model con nuovi valori, tuttavia, devi prima recuperarlo. In un secondo momento devi impostare i nuovi valori di cui hai bisogno e, infine, salvi le modifiche sul database richiamando, appunto, _save()_.

	$flight = App\Flight::find(1);

	$flight->name = 'New Flight Name';

	$flight->save();

Gli aggiornamenti possono essere effettuati anche su determinati set di risultati che rispettano determinate condizioni. In questo esempio, tutti i voli attivi con destinazione "San Diego" vengono impostati come "spostati" (delayed).

	App\Flight::where('active', 1)
			  ->where('destination', 'San Diego')
			  ->update(['delayed' => 1]);

Il metodo _update_ prende in input un array associativo (colonna > valore) che rappresenta l'insieme delle colonne da aggiornare con i relativi nuovi valori.

<a name="assegnamento-massa"></a>
### Assegnamento di Massa

Il metodo _save_ non è l'unico modo che hai a disposizione per salvare un nuovo record. Un'alternativa, infatti, è il metodo _create_, che tra l'altro restituisce un'istanza del model appena creato (e salvato). Non può essere usato, però, se non sono stati impostati gli attributi interessati tramite le proprietà _fillable_ o _guarded_ del model. 

Di default, per motivi di sicurezza, i model Eloquent sono protetti dall'assegnamento di massa. Il metodo _create_ prende in input un semplice array associativo con i vari nomi/valori delle colonne per quel record. Se non si ha il pieno controllo di quello che si sta inserendo, il risultato potrebbe risultare sgradevole e, appunto, poco sicuro. Senza considerare inoltre i possibili attacchi tramite una semplice richiesta HTTP!

La prima cosa da fare è assegnare i valori giusti alla proprietà _fillable_. Ad esempio, aggiungiamo la proprietà _name_ del model _Flight_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The attributes that are mass assignable.
		 *
		 * @var array
		 */
		protected $fillable = ['name'];
	}

Adesso che l'attributo è incluso nell'array _fillable_, possiamo procedere con la chiamata al metodo _create_. Come già detto prima, il metodo restituirà l'istanza appena creata del model, usabile come si desidera.

	$flight = App\Flight::create(['name' => 'Flight 10']);

While `$fillable` serves as a "white list" of attributes that should be mass assignable, you may also choose to use `$guarded`. The `$guarded` property should contain an array of attributes that you do not want to be mass assignable. All other attributes not in the array will be mass assignable. So, `$guarded` functions like a "black list". Of course, you should use either `$fillable` or `$guarded` - not both:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The attributes that aren't mass assignable.
		 *
		 * @var array
		 */
		protected $guarded = ['price'];
	}

In the example above, all attributes **except for `price`** will be mass assignable.

#### Other Creation Methods

There are two other methods you may use to create models by mass assigning attributes: `firstOrCreate` and `firstOrNew`. The `firstOrCreate` method will attempt to locate a database record using the given column / value pairs. If the model can not be found in the database, a record will be inserted with the given attributes.

The `firstOrNew` method, like `firstOrCreate` will attempt to locate a record in the database matching the given attributes. However, if a model is not found, a new model instance will be returned. Note that the model returned by `firstOrNew` has not yet been persisted to the database. You will need to call `save` manually to persist it:

	// Retrieve the flight by the attributes, or create it if it doesn't exist...
	$flight = App\Flight::firstOrCreate(['name' => 'Flight 10']);

	// Retrieve the flight by the attributes, or instantiate a new instance...
	$flight = App\Flight::firstOrNew(['name' => 'Flight 10']);

<a name="cancellazione-model"></a>
## Cancellazione dei Model

Per cancellare un model, semplicemente, richiama il metodo _delete_ sull'istanza desiderata.

	$flight = App\Flight::find(1);

	$flight->delete();

#### Cancella un Model partendo dalla Chiave Primaria

Nell'esempio appena visto, hai recuperato il model da cancellare per poi richiamare il metodo _delete_. Tuttavia, se conosci già la chiave primaria dell'elemento da eliminare, puoi usare il metodo _destroy_.

	App\Flight::destroy(1);

	App\Flight::destroy([1, 2, 3]);

	App\Flight::destroy(1, 2, 3);

Nel secondo esempio, al posto di una singola chiave primaria, ne abbiamo passata più di una. Gli elementi 1, 2 e 3 verranno eliminati. Il terzo esempio porta allo stesso risultato ma con una sintassi leggermente diversa. A te la scelta!

#### Cancellare un Model Partendo da una Query

Ovviamente, puoi anche cancellare un model partendo da una serie di condizioni. In questo esempio stiamo cancellando tutti i voli marcati come inattivi.

	$deletedRows = App\Flight::where('votes', '>', 100)->delete();

<a name="soft-deleting"></a>
### Soft Deleting

In aggiunta alla rimozione effettiva dei record dal database, Eloquent offre anche una feature detta "soft delete". In poche parole, se per un model è attivata l'opzione, in caso di _delete_ il record non verrà rimosso fisicamente, ma verrà invece modificato con l'aggiunta del momento della "cancellazione" in un campo *deleted_at*. Di default questo campo ha come valore _null_: per ogni valore diverso, Eloquent tratta il record corrispondente come cancellato a tutti gli effetti.

Per abilitare questa feature, usa il trait `Illuminate\Database\Eloquent\SoftDeletes` ed aggiungi il campo `deleted_at` alla proprietà `$dates`.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;
	use Illuminate\Database\Eloquent\SoftDeletes;

	class Flight extends Model
	{
		use SoftDeletes;

		/**
		 * The attributes that should be mutated to dates.
		 *
		 * @var array
		 */
		protected $dates = ['deleted_at'];
	}

Ovviamente devi aggiungere anche la colonna corrispondente al tuo database. Lo [schema builder](/docs/5.1/schema) di Laravel conta già un helper dedicato alla creazione di tale colonna:

	Schema::table('flights', function ($table) {
		$table->softDeletes();
	});

Da questo momento, ogni volta che richiamerai _delete_ sul tuo model, verrà semplicemente inserito il valore della data/ora attuale in *deleted_at*. A tutto il resto, poi, ci penserà Laravel, sia in fase di lettura che di scrittura.

Per capire se un record è stato cancellato "in modo soft", usa il metodo _trashed_:

	if ($flight->trashed()) {
		//
	}

<a name="query-soft-deleted-model"></a>
### Query sui Soft Deleted Model

#### Includere i Soft Deleted Model nel Risultato

Come notato poco fa, Eloquent escluderà tutti i risultati che sono stati "cancellati". Tuttavia, per qualche motivo, potresti aver bisogno di includere nel risultato anche queste voci: in tal caso, ricorda di usare il metodo _withTrashed_.

	$flights = App\Flight::withTrashed()
					->where('account_id', 1)
					->get();

Il metodo _withTrashed_ può essere usato anche su una query di una [relazione](/docs/5.1/eloquent-relationships):

	$flight->history()->withTrashed()->get();

#### Recuperare solo i Soft Deleted Model

Usando _onlyTrashed_, invece, recupererai **solo** i model che hai "cancellato".

	$flights = App\Flight::onlyTrashed()
					->where('airline_id', 1)
					->get();

#### Ripristinare un Record Soft Deleted

A volte potresti voler annullare la cancellazione di un record soft deleted. Tutto quello che devi fare, in tal caso, è usare il metodo _restore_ sull'istanza desiderata.

	$flight->restore();

Esattamente come prima, inoltre, puoi usare il metodo _restore_ anche specificando delle condizioni:

	App\Flight::withTrashed()
			->where('airline_id', 1)
			->restore();

Inoltre, puoi usare _restore_ anche sulle [relazioni](/docs/5.1/eloquent-relationships):

	$flight->history()->restore();

#### Cancellare in modo Permanente dei Model

Il soft delete, come appena visto, **non** cancella fisicamente il record. Potrebbe tuttavia accadere di averne la necessità. In questo caso, usa il metodo _forceDelete_ ed il gioco è fatto!

	// Forziamo la cancellazione di una singola istanza...
	$flight->forceDelete();

	// Forziamo la cancellazione di tutti i model correlati...
	$flight->history()->forceDelete();

<a name="query-scope"></a>
## Query Scope

Le Query Scope ti permettono di definire dei set comuni di condizioni da poter riutilizzare successivamente nella tua applicazione. Facciamo un esempio per capirci meglio: immagina di dover recuperare, abbastanza spesso, gli utenti più "popolari". Per definire uno scope, aggiungi il prefisso _scope_ ad un nuovo metodo apposito.

Come nell'esempio di seguito:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Scope a query to only include popular users.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopePopular($query)
		{
			return $query->where('votes', '>', 100);
		}

		/**
		 * Scope a query to only include active users.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopeActive($query)
		{
			return $query->where('active', 1);
		}
	}

#### Usare uno Scope

Una volta definito uno scope, puoi usarlo in fase di query del model stesso. Non hai bisogno di includere però il prefisso _scope_: guarda questo esempio.

	$users = App\User::popular()->women()->orderBy('created_at')->get();

Nel model abbiamo dichiarato _scopePopular_ ma in fase di query usiamo solo _popular_.

#### Scope Dinamici

Eloquent permette anche la dichiarazione di specifici scope dinamici, che accettano parametri. Non devi fare altro che aggiungere i tuoi parametri allo scope, il resto è automatico. Basta dichiararli **dopo** il parametro _$query_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Scope a query to only include users of a given type.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopeOfType($query, $type)
		{
			return $query->where('type', $type);
		}
	}

Passare il parametro necessario in fase di chiamata sarà semplicissimo:

	$users = App\User::ofType('admin')->get();

<a name="eventi"></a>
## Eventi

I model Eloquent, quando usati, scatenano svariati eventi che ti permettono di personalizzare il loro comportamento durante l'esecuzione seguendo il paradigma della programmazione guidata dagli eventi. Tali eventi vengono ovviamente scatenati in diversi "momenti" del ciclo di vita del model stesso: già i nomi (`creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `restoring` e `restored`) rendono l'idea.

Vediamo come usarli.

<a name="eventi-uso-base"></a>
### Uso Base

Ogni volta che un model viene salvato per la prima volta, gli eventi _creating_ e _created_ vengono scatenati. Se un model esiste già nel database e su di esso viene richiamato il metodo _save_, allora vengono scatenati gli eventi _updating_ ed _updated_. In entrambi i casi, inoltre, _saving_ e _saved_ vengono scatenati.

Uno dei posti "adatti" per la gestione degli eventi può essere un [service provider](/docs/5.1/provider) apposito. Ecco un esempio in funzione: in questo caso stiamo gestendo l'evento _creating_ per la classe _User_. Alla creazione di una nuova istanza, prima del salvataggio (siamo in _creating_, non _created_) eseguiremo delle operazioni di validazione.

Nota: in questo caso la gestione di questi eventi viene messa nel metodo _boot_. 

	<?php namespace App\Providers;

	use App\User;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			User::creating(function ($user) {
				if ( ! $user->isValid()) {
					return false;
				}
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
