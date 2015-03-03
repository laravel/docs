# Eloquent ORM

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)
- [Assegnamento di Massa](#assegnamento-massa)
- [Insert, Update e Delete](#insert-update-delete)
- [Soft Deleting](#soft-deleting)
- [Timestamp](#timestamp)
- [Query Scope](#query-scope)
- [Global Scope](#global-scope)
- [Relazioni](#relazioni)
- [Interrogare Le Relazioni](#interrogare-relazioni)
- [Eager Loading](#eager-loading)
- [Relazioni ed Inserimento di Model](#relazioni-inserimento-model)
- [Lavorare con i Timestamp dei Parent](#lavorare-timestamp-parent)
- [Lavorare con le Tabelle Pivot](#lavorare-tabelle-pivot)
- [Le Collection](#collection)
- [Accessor e Mutator](#accessor-e-mutator)
- [Date Mutator](#date-mutator)
- [Casting degli Attributi](#casting-attributi)
- [Eventi del Model](#eventi-model)
- [Model Observer](#model-observer)
- [Convertire in Array o JSON](#convertire-array-json)

<a name="introduzione"></a>
## Introduzione

Eloquent è l'ORM incluso in Laravel: un'implementazione di Active Record potente e semplice che ti permette di lavorare agevolmente con il tuo database. Ogni tabella nel tuo database trova una sua corrispondenza in un "Model", il quale ha proprio il compito di gestire l'interazione con la tabella stessa.

Prima di iniziare, comunque, assicurati di configurare una connessione in _config/database.php_.

<a name="uso-base"></a>
## Uso Base

Per iniziare, crea il tuo primo model Eloquent. Tipicamente, un model va messo nella cartella _app_. Ad ogni modo sei libero di posizionare il tuo file dove meglio credi: l'importante è che venga "coperto" dall'autoloading, in accordo con le regole specificate nel file _composer.json_. Tutti i modelli Eloquent estendono `Illuminate\Database\Eloquent\Model`.

#### Definire un Model

	class User extends Model {}

Se ci fai caso, non abbiamo specificato neanche il nome della tabella da usare per il model _User_. Automaticamente, infatti, Laravel prova ad indovinare quale tabella usare trasformando il nome del model in plurale ed in lettere minuscole. Tale nome verrà "usato" a meno di specifiche diverse. Per decidere tu quale tabella usare, infatti, puoi definire la proprietà _table_ sul model:

	class User extends Model {

		protected $table = 'my_users';

	}

> **Nota:** Eloquent assume che ogni tabella possiede una chiave primaria di nome _id_. Se non è questo il caso della tua tabella, puoi specificare il nome del campo usato al posto di id tramite la proprietà _primaryKey_. Inoltre, puoi anche decidere di usare, per un singolo model, una connessione ben definita. La proprietà da usare, in tal caso, è _connection_.

Una volta definito il model si è già pronti a selezionare record, crearne di nuovi ed in generale lavorare con la tabella.

> **Nota:** avrai bisogno di due campi _updated_at_ e _created_at_, di default, sulla tua tabella. Se non volessi farne uso, specifica la proprietà _timestamp_ del model come _false_.

#### Recuperare tutti i Record

	$users = User::all();

#### Recuperare un Record in base alla Chiave Primaria

	$user = User::find(1);

	var_dump($user->name);

> **Nota:** tutti i metodi usabili nel contesto del query builder sono disponibili anche per Eloquent.

#### Recuperare un Record in base alla Chiave Primaria, oppure Lanciare un'Eccezione

A volte potresti avere la necessità di lanciare un'eccezione in caso di record non trovato. Tramite _findOrFail_ puoi facilmente implementare un comportamento del genere.

	$model = User::findOrFail(1);

	$model = User::where('votes', '>', 100)->firstOrFail();

Potrai gestire quindi il tuo "errore" tramite _App::error_, ed in modo più specifico potrai anche registrare un hander dedicato al problema.

	use Illuminate\Database\Eloquent\ModelNotFoundException;

	App::error(function(ModelNotFoundException $e)
	{
		return Response::make('Not Found', 404);
	});

#### Query tramite un Model Eloquent

	$users = User::where('votes', '>', 100)->take(10)->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### Aggregati di Eloquent

Se vuoi, puoi usare gli aggregati visti nel query builder.

	$count = User::where('votes', '>', 100)->count();

In caso, inoltre, di una query eccessivamente difficile puoi sempre usare il metodo _whereRaw_.

	$users = User::whereRaw('age > ? and votes = 100', array(25))->get();

#### Chunking del Risultato

Nel caso in cui tu debba processare un sacco (migliaia) di record Eloquent, il metodo _chunk_ ti permetterà di farlo senza divorare tutta la RAM a disposizione:

	User::chunk(200, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

Il primo argomento passato al metodo è il numero di record da ricevere per ogni "gruppo". La closure passata come secondo argomento, invece, serve a definire cosa fare con ogni singolo gruppo di record preso dal database.

#### Specificare la Connessione al Database

Abbiamo visto che è possibile specificare quale connessione usare per ogni singolo Model. Non è abbastanza? Bene, è possibile specificare quale connessione usare per ogni singola query!

	$user = User::on('connection-name')->find(1);

Se stai usando delle connessioni _read / write_, potresti forzare una query ad usare una connessione di tipo _write_ in questo modo:

	$user = User::onWriteConnection()->find(1);

<a name="assegnamento-massa"></a>
## Assegnamento di Massa

Quando crei un nuovo model, ti trovi a passare tutta una serie di attributi al costruttore del model stesso. Questi attributi vengono assegnati al model tramite _mass assignment_, o assegnamento di massa. Si tratta, in effetti, di un modo molto conveniente che, tuttavia, potrebbe portare a svariate preoccupazioni inerenti la sicurezza se si prende la cosa troppo alla leggera. Per questo motivo, di default i model di Eloquent sono "protetti" dal mass-assignment.

Puoi comunque specificare quali singoli campi proteggere e quali no, tramite le proprietà _fillable_ e _guarded_.

#### Definire gli attributi Fillable su un Model

La proprietà _fillable_ serve a specificare quali attributi devono essere assegnabili tramite il mass-assignment. Eloquent permette di farlo sia a livello di classe che a livello di istanza.

	class User extends Model {

		protected $fillable = array('first_name', 'last_name', 'email');

	}

In questo esempio, solo i tre attributi in lista saranno assegnabili in massa.

#### Definire degli attributi Guarded

Eloquent permette anche di effettuare l'operazione inversa di quella appena vista: al posto di specificare quali attributi rendere _fillable_, è possibile definire quali devono essere _guarded_, ovvero protetti. In poche parole, si fa una blacklist al posto di una whitelist.

	class User extends Model {

		protected $guarded = array('id', 'password');

	}

> **Nota:** se usi _guarded_ nel tuo model ricorda di non passare mai l'array _Input::get()_ o qualsiasi altra forma grezza di input, in quanto ogni colonna non protetta potrebbe comunque essere soggetta a problemi.

#### Blocco di tutti gli attributi dal Mass Assignment

Nell'esempio appena visto, gli attributi _id_ e _password_ non possono essere soggetti a mass-assignment, mentre tutti gli altri attributi si. Se desideri, puoi bloccare **tutti** gli attributi tramite la semplice notazione:

	protected $guarded = array('*');

<a name="insert-update-delete"></a>
## Insert, Update e Delete

Creare un nuovo record nel database è semplice tanto quanto creare un nuovo oggetto.

#### Salvare un Nuovo Record

	$user = new User;

	$user->name = 'John';

	$user->save();

> **Nota:** tipicamente, un model Eloquent usa delle chiavi auto-incrementanti. Tuttavia, nel caso desiderassi tu stesso specificare le chiavi da usare, imposta la proprietà _incrementing_ del tuo model come _false_.

Puoi inoltre usare il metodo _create_ per salvare un model con una sola istruzione. L'istanza del model appena creato verrà ritornata dal metodo stesso. Ricorda tuttavia che prima di lavorare con questo metodo devi impostare gli attributi _fillable_ o _guarded_, visto che di default sono protetti dal mass assignment.

Dopo aver salvato o creato un nuovo model tramite ID auto-incrementante, puoi recuperare il nuovo ID accedendo all'attributo _id_ dell'oggetto stesso:

	$insertedId = $user->id;

#### Usare il metodo Create del Model

	// Creare un nuovo utente sul Database...
	$user = User::create(array('name' => 'John'));

	// Recuperare l'utente in base ad un attributo, o crearlo in caso non esista...
	$user = User::firstOrCreate(array('name' => 'John'));

	// Recuperare l'utente in base ad un attributo, o creare una nuova istanza...
	$user = User::firstOrNew(array('name' => 'John'));

#### Update di un Model

Per aggiornare un model devi innanzitutto prelevarne il record dal database. Una volta modificato, quindi, usa il metodo _save_ per salvarne i cambiamenti.

	$user = User::find(1);

	$user->email = 'john@foo.com';

	$user->save();

#### Salvare un Model con le sue Relazioni

A volte potresti voler salvare non solo un model, ma anche tutte le sue relazioni. Se è questo il caso, usa il metodo _push_:

	$user->push();

Se necessario puoi anche salvare un certo set di model in base a condizioni:

	$affectedRows = User::where('votes', '>', 100)->update(array('status' => 2));

> **Nota:** in questo caso non verranno però lanciati gli eventi relativi al model.

#### Cancellare un Model

Per cancellare un model puoi usare il metodo _delete_ dell'istanza desiderata.

	$user = User::find(1);

	$user->delete();

#### Cancellare un Model in Base alla (alle) Chiave Primaria

	User::destroy(1);

	User::destroy(array(1, 2, 3));

	User::destroy(1, 2, 3);

Ovviamente, puoi eseguire tale query anche se un set specifico di model:

	$affectedRows = User::where('votes', '>', 100)->delete();

#### Aggiornare Esclusivamente i Timestamp di un Model

Potresti avere, a volte, la necessità di aggiornare solo i timestamp di un model e non i suoi dati. In tal caso, usa il metodo _touch_:

	$user->touch();

<a name="soft-deleting"></a>
## Soft Deleting

Cancellare con il soft delete un model significa non cancellarlo davvero. In realtà, infatti, tutto quello che viene fatto è l'aggiornamento del campo _deleted_at_ sul record. Per abilitare il soft deleting su un model devi applicare al model il trait _SoftDeletes_:

	use Illuminate\Database\Eloquent\SoftDeletes;

	class User extends Model {

		use SoftDeletes;

		protected $dates = ['deleted_at'];

	}

Puoi aggiungere velocemente un campo _deleted_at_ ad una tabella tramite il metodo _softDeletes_ in una migration:

	$table->softDeletes();

Da questo momento in poi il model è abilitato per lo scopo e la chiamata del metodo _delete_ eviterà la cancellazione fisica, occupandosi invece di modificare il campo _deleted_at_ in modo opportuno. I deleted model, ovviamente, non saranno più inclusi nei risultati delle query.

#### Forzare i Risultati per Ottenere anche i Model Cancellati

Per forzare l'uscita, tra i risultati, dei model cancellati, usa _withTrashed_:

	$users = User::withTrashed()->where('account_id', 1)->get();

Il metodo _withTrashed_ può anche essere usato sulla definizione di una relazione:

	$user->posts()->withTrashed()->get();

Nel caso in cui tu voglia recuperare solo i model "cancellati", ecco come fare:

	$users = User::onlyTrashed()->where('account_id', 1)->get();

Per "riabilitare" un model precedentemente cancellato tramite soft delete, quindi, usa _restore_:

	$user->restore();

Puoi anche usare _restore_ su una query:

	User::withTrashed()->where('account_id', 1)->restore();

Il metodo _restore_, inoltre, può essere usato anche su una relazione:

	$user->posts()->restore();

Se vuoi davvero rimuovere un model da un database, infine, puoi usare il metodo _forceDelete_...

	$user->forceDelete();

... che lavora tranquillamente anche sulle relazioni:

	$user->posts()->forceDelete();

Per determinare se una certa istanza è stata "cancellata", puoi usare il metodo _trashed_:

	if ($user->trashed())
	{
		//
	}

<a name="timestamp"></a>
## Timestamp

Di default, Eloquent gestisce in modo autonomo i campi _created_at_ e _updated_at_. Tutto quello che devi fare, infatti, è crearli in fase di preparazione dello schema del database. Disattivare questa funzionalità è semplice: basta impostare su _false_ la proprietà _timestamps_ del model:

#### Disabilitare la Gestione Automatica dei Timestamp

	class User extends Model {

		protected $table = 'users';

		public $timestamps = false;

	}

#### Scegliere il Formato dei Timestamp

Nel caso in cui dovessi avere bisogno di personalizzare il formato dei tuoi timestamp, usa _getDateFormat_ nel tuo model:

	class User extends Model {

		protected function getDateFormat()
		{
			return 'U';
		}

	}

<a name="query-scope"></a>
## Query Scope

#### Definire un Query Scope

Gli scope ti permettono di ri-usare una certa logica più velocemente all'interno dei tuoi model. Per definirne, inserisci come prefisso del metodo _scope_:

	class User extends Model {

		public function scopePopular($query)
		{
			return $query->where('votes', '>', 100);
		}

		public function scopeWomen($query)
		{
			return $query->whereGender('W');
		}

	}

#### Usare un Query Scope

	$users = User::popular()->women()->orderBy('created_at')->get();

#### Dynamic Scope

A volte potresti voler creare uno scope che accetta dei parametri: niente di complesso. Aggiungi i tuoi parametri al metodo in questo modo:

	class User extends Model {

		public function scopeOfType($query, $type)
		{
			return $query->whereType($type);
		}

	}

A quel punto, per usarlo...

	$users = User::ofType('member')->get();

<a name="global-scope"></a>
## Global Scope

Laravel ed Eloquent permettono, oltre alla definizione di scope, anche la possibilità di definire degli scope "speciali" che si possono applicare ad ogni query, per ogni model. Per fare ciò si usa una combinazione di trait PHP ed un'implementazione di `Illuminate\Database\Eloquent\ScopeInterface`.

Innanzitutto, definiamo un trait. Per questo esempio useremo _SoftDeletes_ già presente in Laravel.

	trait SoftDeletes {

		/**
		 * Boot the soft deleting trait for a model.
		 *
		 * @return void
		 */
		public static function bootSoftDeletes()
		{
			static::addGlobalScope(new SoftDeletingScope);
		}

	}

Se un model Eloquent usa un trait che possiede un metodo che segue la convenzione _bootNameOfTrait_, tale metodo verrà richiamato al momento dell'avvio del model stesso. Ti darà quindi l'opportunità di registrare un global scope o fare qualsiasi altra cosa tu voglia. Ogni scope deve implementare la _ScopeInterface_ che richiede la definizione di due metodi: _apply_ e _remove_.

Il metodo _apply_ riceve un oggetto di tipo `Illuminate\Database\Eloquent\Builder` ed è responsabile dell'aggiunta di ogni clausola _where_ addizionale che la scope globale ha l'obiettivo di aggiungere. Il metodo _remove_ invece prende un oggetto di classe _Builder_ ed è responsabile per annullare tutto quello che è stato fatto da _apply_ in precedenza.

Nel caso della feature di Soft Delete, quindi:

	/**
	 * Apply the scope to a given Eloquent query builder.
	 *
	 * @param  \Illuminate\Database\Eloquent\Builder  $builder
	 * @return void
	 */
	public function apply(Builder $builder)
	{
		$model = $builder->getModel();

		$builder->whereNull($model->getQualifiedDeletedAtColumn());
	}

	/**
	 * Remove the scope from the given Eloquent query builder.
	 *
	 * @param  \Illuminate\Database\Eloquent\Builder  $builder
	 * @return void
	 */
	public function remove(Builder $builder)
	{
		$column = $builder->getModel()->getQualifiedDeletedAtColumn();

		$query = $builder->getQuery();

		foreach ((array) $query->wheres as $key => $where)
		{
			// If the where clause is a soft delete date constraint, we will remove it from
			// the query and reset the keys on the wheres. This allows this developer to
			// include deleted model in a relationship result set that is lazy loaded.
			if ($this->isSoftDeleteConstraint($where, $column))
			{
				unset($query->wheres[$key]);

				$query->wheres = array_values($query->wheres);
			}
		}
	}

<a name="relazioni"></a>
## Relazioni

Molto probabilmente, le tabelle del tuo database sono legate l'una all'altra da una relazione. Ad esempio, un post può avere alcuni commenti relativi, o un ordine può avere un utente di riferimento che lo ha piazzato. Oltre a fare tutto quello che abbiamo visto finora, Eloquent gestisce al meglio tutte le tipologie di relazioni possibili.

Precisamente:

- [Uno ad Uno](#uno-ad-uno)
- [Uno a Molti](#uno-a-molti)
- [Molti a Molti](#molti-a-molti)
- [Ha Molti Tramite](#ha-molti-tramite)
- [Relazioni Polimorfiche](#relazioni-polimorfiche)
- [Relazioni Polimorfiche Molti a Molti](#relazioni-polimorfiche-molti-a-molti)

<a name="uno-ad-uno"></a>
### Uno ad Uno

#### Definire una Relazione Uno ad Uno

Una relazione uno ad uno è quella più basilare. Ad esempio, uno _User_ del tuo sistema può avere collegato un _Phone_ (telefono). Definiamo subito questa relazione in Eloquent.

	class User extends Model {

		public function phone()
		{
			return $this->hasOne('App\Phone');
		}

	}

Il primo argomento passato a _hasOne_ è il nome del model "legato". Visto che la relazione adesso è definita (non serve fare altro) si possono recuperarne i dati tramite le [proprietà dinamiche](#proprieta-dinamiche):

	$phone = User::find(1)->phone;

La Query SQL corrispondente sarà:

	select * from users where id = 1

	select * from phones where user_id = 1

Se ci fai caso, Eloquent cerca ancora una volta di "indovinare" il nome della chiave esterna basandosi su una convenzione facilmente intuibile. Tale comportamento, come sempre, è modificabile facilmente specificando un secondo parametro al metodo _hasOne_ (il nome della chiave esterna), e volendo anche un terzo parametro (nome della chiave locale).

	return $this->hasOne('App\Phone', 'foreign_key');

	return $this->hasOne('App\Phone', 'foreign_key', 'local_key');

#### Definire l'Inverso di una Relazione

Definire l'inverso di una relazione è tanto semplice quanto definire una relazione: basta usare _belongsTo_.

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User');
		}

	}

Nell'esempio visto appena sopra, Eloquent cercherà una colonna _user_id_ nella tabella _phones_. Esattamente come prima, nel caso in cui tu voglia defnire un nome diverso da quello suggerito dalla convenzione per il nome della chiave locale, tutto quello che devi fare è specificare un secondo parametro.

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User', 'local_key');
		}

	}

Opzionalmente puoi decidere di passare un terzo parametro, che specifichi il nome della colonna associata sulla tabella _parent_:

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User', 'local_key', 'parent_key');
		}

	}

<a name="uno-a-molti"></a>
### Uno a Molti

Uno degli esempi più classici di relazione uno a molti è il post di un blog che conta più commenti ad esso legati. Possiamo modellare la relazione in questo modo:

	class Post extends Model {

		public function comments()
		{
			return $this->hasMany('App\Comment');
		}

	}

Esattamente come prima, tramite proprietà dinamiche si può facilmente accedere ai dati desiderati:

	$comments = Post::find(1)->comments;

Nel caso in cui, invece, dovessi trovarti nella necessità di "aggiungere" altre condizioni strada facendo, usa _comments_ come metodo:

	$comments = Post::find(1)->comments()->where('title', '=', 'foo')->first();

Ancora, come già visto in precedenza, nulla ti vieta di sovrascrivere le chiavi esterne passando un secondo argomento (ed un terzo) per il metodo _hasMany_.

	return $this->hasMany('App\Comment', 'foreign_key');

	return $this->hasMany('App\Comment', 'foreign_key', 'local_key');

#### Definire l'Inverso della Relazione

Per definire l'inverso di una relazione molti a molti si usa il _belongsTo_:

	class Comment extends Model {

		public function post()
		{
			return $this->belongsTo('App\Post');
		}

	}

<a name="molti-a-molti"></a>
### Molti a Molti

Le relazioni molti a molti sono quelle più complicate. Ancora una volta, facciamo un esempio classico per capirci meglio: un tipico sistema che gestisca un insieme di utenti ed i loro ruoli all'interno del sistema. Ad esempio, più utenti possono avere il ruolo "Admin". Per implementare tale sistema servono, innanzitutto, tre tabelle: _users_, _roles_ e _role_user_. Questa terza tabella segue una convenzione molto semplice: nomi dei model in minuscolo, singolari, separati da underscore ed in ordine alfabetico.

Tale tabella deve avere due campi _user_id_ e _role_id_.

A questo punto, definire la relazione è semplice: basta usare _belongsToMany_.

	class User extends Model {

		public function roles()
		{
			return $this->belongsToMany('App\Role');
		}

	}

A questo punto possiamo lavorare con la relazione tramite il model _User_:

	$roles = User::find(1)->roles;

Nel caso in cui volessimo usare un nome non convenzionale per la tabella pivot, basta specificarne un nome nuovo come secondo argomento di _belongsToMany_.

	return $this->belongsToMany('App\Role', 'user_roles');

Chiaramente puoi sovrascrivere anche i nomi da usare per i campi riguardanti la relazione.

	return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'foo_id');

Ecco quindi come definire l'inverso della relazione, dal punto di vista del ruolo e non dell'utente:

	class Role extends Model {

		public function users()
		{
			return $this->belongsToMany('App\User');
		}

	}

<a name="ha-molti-tramite"></a>
### Ha Molti Tramite

La relazione "ha molti tramite" permette di usare una scorciatoia piuttosto conveniente per l'accesso a relazioni "distanti" tramite altre relazioni intermedie. Ad esempio, un model _Country_ potrebbe avere svariati _Post_ attraverso un altro model _User_. Le tabelle in gioco potrebbero essere, per questo esempio, le seguenti:

	countries
		id - integer
		name - string

	users
		id - integer
		country_id - integer
		name - string

	posts
		id - integer
		user_id - integer
		title - string

Anche se la tabella _posts_ non ha di certo una chiave _country_id_, tramite _hasManyThrough_ è possibile definire una relazione che permette di accedere ai post di una certa nazione tramite _$country->posts_.

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'User');
		}

	}

Come al solito, anche in questo caso è possibile specificare nomi diversi da quelli che seguono la convenzione, in caso di necessità.

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'User', 'country_id', 'user_id');
		}

	}

<a name="relazioni-polimorfiche"></a>
### Relazioni Polimorfiche

Le relazioni polimorfiche permettono ad un certo model di "appartenere" a più di un model, ma in una singola associazione. Per fare un esempio pratico, immagina di avere il model di una foto che può appartenere ad un membro dello staff di un organizzazione, oppure ad un ordine piazzato da un cliente. Potremmo definire la relazione in questo modo:

	class Photo extends Model {

		public function imageable()
		{
			return $this->morphTo();
		}

	}

	class Staff extends Model {

		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}

	}

	class Order extends Model {

		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}

	}

#### Recuperare i Dati di una Relazione Polimorfica

Una volta definita la relazione è possibile recuperare i dati normalmente:

	$staff = Staff::find(1);

	foreach ($staff->photos as $photo)
	{
		//
	}

#### Recuperare il "Proprietario" della Relazione

Quello che hai appena visto è molto utile, sicuramente, ma la vera magia della relazione polimorfica arriva ora: come accedere all'oggetto "proprietario" senza sapere di chi si tratta?

	$photo = Photo::find(1);

	$imageable = $photo->imageable;

La relazione _imageable_ del model Photo ritornerà, in base alla necessità, un'istanza di _Staff_ o _Order_, automaticamente.

#### Struttura di una Tabella per Relazioni Polimorfiche

Per capire meglio come funziona tutto, dai uno sguardo alla struttura del database da usare per una relazione polimorfica.

	staff
		id - integer
		name - string

	orders
		id - integer
		price - integer

	photos
		id - integer
		path - string
		imageable_id - integer
		imageable_type - string

Il campo chiave da osservare qui è _imageable_id_ e _imageable_type_ sulla tabella _photos_. _Id_ conterrà l'id del proprietario, a prescindere da quale entità sia. Il tipo di questa, infatti, verrà definito in _type_. Questi due dati permettono all'ORM di fare tutto il lavoro necessario.

<a name="relazioni-polimorfiche-molti-a-molti"></a>
### Relazioni Polimorfiche Molti a Molti

#### Struttura delle Tabelle per una Relazione Polimorfica Molti a Molti

In aggiunta alla classica relazione polimorfica, se ne hai bisogno, puoi specificare una relazione polimorfica molti a molti. Ad esempio, un _Post_ e un _Video_ possono condividere la relazione polimorfica che li lega ad un certo _Tag_.

Vediamo, per questa situazione, una struttura delle tabelle da usare.

	posts
		id - integer
		name - string

	videos
		id - integer
		name - string

	tags
		id - integer
		name - string

	taggables
		tag_id - integer
		taggable_id - integer
		taggable_type - string

Creata la struttura siamo pronti a creare la relazione tra model. Sia _Post_ che _Video_ useranno _morphToMany_ per la definizione della relazione.

	class Post extends Model {

		public function tags()
		{
			return $this->morphToMany('App\Tag', 'taggable');
		}

	}

Il model _Tag_ implementerà un metodo per ognuna delle possibilità:

	class Tag extends Model {

		public function posts()
		{
			return $this->morphedByMany('App\Post', 'taggable');
		}

		public function videos()
		{
			return $this->morphedByMany('App\Video', 'taggable');
		}

	}

<a name="interrogare-relazioni"></a>
## Interrogare le Relazioni

#### Interrogare le Relazioni in Fase di Select

Accedendo ad i record di un model, potresti voler filtrare i risultati in base all'esistenza di una certa relazione. Ad esempio, potresti voler prelevare tutti i post del tuo blog che hanno almeno un commento:

	$posts = Post::has('comments')->get();

Volendo puoi anche dare un minimo ben definito che non sia zero:

	$posts = Post::has('comments', '>=', 3)->get();

Si possono innestare anche più relazioni con un la dot notation:

	$posts = Post::has('comments.votes')->get();

Hai bisogno di più potenza? No problem: usa _whereHas_ e _orWhereHas_ per specificare una _Closure_ da usare come meglio credi.

	$posts = Post::whereHas('comments', function($q)
	{
		$q->where('content', 'like', 'foo%');

	})->get();

<a name="proprieta-dinamiche"></a>
### Proprietà Dinamiche

Eloquent ti permette di accedere alle tue relazioni attraverso proprietà dinamiche. In caso d'uso, Eloquent carica automaticamente tutto quello che serve ed è anche abbastanza "intelligente" da capire qunado serve usare _get()_ (in caso di uno a molti) o _first()_ (in caso di uno ad uno). Il risultato sarà quindi accessibile tramite una proprietà dinamica dallo stesso nome della relazione. Ecco un esempio:

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User');
		}

	}

	$phone = Phone::find(1);

Quindi, al posto di ottenere l'indirizzo email in questo modo:

	echo $phone->user()->first()->email;

Basterà fare così:

	echo $phone->user->email;

> **Nota:** le Relazioni che ritornano più di un risultato fanno uso di un'istanza di una classe `Illuminate\Database\Eloquent\Collection`.

<a name="eager-loading"></a>
## Eager Loading

L'Eager Loading è un'ottima soluzione in caso di esecuzione di un numero spropositato di query. Ipotizza la presenza di un model _Book_ legato ad un _Author_. La relazione verrebbe così definita:

	class Book extends Model {

		public function author()
		{
			return $this->belongsTo('App\Author');
		}

	}

Ora, considera il seguente codice:

	foreach (Book::all() as $book)
	{
		echo $book->author->name;
	}

Tale loop eseguirà una query per recuperare l'elenco dei libri, quindi altre cento (una per ogni libro) dato che c'è bisogno di sapere il nome dell'autore. Con 100 libri eseguiremmo 101 query.

L'Eager Loading riduce drasticamente tale numero, tramite l'uso del metodo _with_.

	foreach (Book::with('author')->get() as $book)
	{
		echo $book->author->name;
	}

Con questa piccola modifica, il numero di query scende da 101 a... 2!

	select * from books

	select * from authors where id in (1, 2, 3, 4, 5, ...)

Ovviamente puoi anche eseguire l'Eager Loading per più relazioni contemporaneamente...

	$books = Book::with('author', 'publisher')->get();

... incluse delle relazioni "annidate"!

	$books = Book::with('author.contacts')->get();

### Eager Load e Condizioni

A volte potresti voler effettuare l'eager loading specificando però delle condizioni per l'operazione.

	$users = User::with(array('posts' => function($query)
	{
		$query->where('title', 'like', '%first%');

	}))->get();

La cosa però non si limita solo a semplici condizioni where: se preferisci puoi anche eseguire, ad esempio, l'ordinamento in questo modo:

	$users = User::with(array('posts' => function($query)
	{
		$query->orderBy('created_at', 'desc');

	}))->get();

### Eager Loading "Pigro"

Puoi anche effettuare un caricamento di dati partendo da una collection esistente. Può essere molto utile per decidere dinamicamente quando e come caricare un certo model, magari in combinazione con il sistema di cache.

	$books = Book::all();

	$books->load('author', 'publisher');

<a name="relazioni-inserimento-model"></a>
## Relazioni ed Inserimento di Model

#### Attach di un Model soggetto a Relazione

Spesso avrai il bisogno di inserire un nuovo model basandoti su una relazione. Ad esempio, pensa ad un inserimento di un nuovo commento per un post. Al posto di impostare manualmente un eventuale _post_id_, potresti inserire il model del commento partendo da _Post_. In questo modo:

	$comment = new Comment(array('message' => 'A new comment.'));

	$post = Post::find(1);

	$comment = $post->comments()->save($comment);

In questo esempio, _post_id_ viene automaticamente impostato correttamente.

In caso di inserimenti multipli, invece...

	$comments = array(
		new Comment(array('message' => 'A new comment.')),
		new Comment(array('message' => 'Another comment.')),
		new Comment(array('message' => 'The latest comment.'))
	);

	$post = Post::find(1);

	$post->comments()->saveMany($comments);

### Associare un Model (Belongs To)

Aggiornando una relazione soggetta a _belongsTo_ puoi usare il metodo _associate_. Tale metodo imposterà automaticamente la chiave esterna sul model "figlio".

	$account = Account::find(10);

	$user->account()->associate($account);

	$user->save();

### Inserimento Model Correlati (Molti a Molti)

Il principio visto finora vale anche per le relazioni molti a molti. Usiamo l'esempio visto prima di _User_ e _Role_. Possiamo associare un nuovo ruolo ad un certo utente facilmente, tramite _attach_.

#### Attach in una Relazione Molti a Molti

	$user = User::find(1);

	$user->roles()->attach(1);

Puoi anche passare un'array di attributi per aggiungere dei dati sulla tabella pivot.

	$user->roles()->attach(1, array('expires' => $expires));

Ovviamente, l'opposto di _attach_ è _detach_.

	$user->roles()->detach(1);

Sia _attach_ che _detach_ possono prendere in input un array di id.

	$user = User::find(1);

	$user->roles()->detach([1, 2, 3]);

	$user->roles()->attach([1 => ['attribute1' => 'value1'], 2, 3]);

#### Usare Sync per le Relazioni Molti a Molti

Oltre ai metodi appena visti, a disposizione c'è anche _sync_, che prende in input un array di ID. Alla fine dell'operazione, solo gli id nella lista saranno presenti sulla tabella intermedia dei pivot. Viene, insomma, effettuato un calcolo intelligente dei delta sia negativi che positivi.

	$user->roles()->sync(array(1, 2, 3));

#### Aggiunta di Dati in fase di Syncing

	$user->roles()->sync(array(1 => array('expires' => true)));

Addirittura, se ne hai necessità puoi creare al volo un model soggetto a relazione, salvandolo ed associandolo in un solo colpo. Basta usare _save_:

	$role = new Role(array('name' => 'Editor'));

	User::find(1)->roles()->save($role);

In questo esempio, il nuovo _Role_ viene salvato ed agganciato al model _User_. Se necessario puoi passare anche in questo caso un array di attributi per aggiungere dati extra alla relazione.

	User::find(1)->roles()->save($role, array('expires' => $expires));

<a name="lavorare-timestamp-parent"></a>
## Lavorare con i Timestamp dei Parent

Quando un model è soggetto ad una relazione _belongsTo_ con un altro model, come ad esempio _Comment_ che appartiene a _Post_, potrebbe essere utile lavorare con i timestamp dell'elemento parent della relazione. Ancora una volta Eloquent rende semplice una tale operazione, semplicemente usando la proprietà _$touches_:

	class Comment extends Model {

		protected $touches = array('post');

		public function post()
		{
			return $this->belongsTo('App\Post');
		}

	}

Da questo momento in poi, ad ogni aggiunta/aggiornamento di un commento, la colonna _updated_at_ del relativo _Post_ verrà aggiornata:

	$comment = Comment::find(1);

	$comment->text = 'Edit to this comment!';

	$comment->save();

<a name="lavorare-tabelle-pivot"></a>
## Lavorare con le Tabelle Pivot

Come hai sicuramente già visto, arrivato a questo punto, lavorare con una relazione molti a molti implica la presenza di una tabella intermedia. Eloquent offre svariate possibilità per lavorare con tale tabella di mezzo. Facciamo un esempio: supponiamo di avere il nostro _User_ con svariati _Role_ di competenza. Abbiamo bisogno di accedere ad un'informazione specifica sulla relazione tra l'utente specifico ed il ruolo specifico.

Ecco come fare:

	$user = User::find(1);

	foreach ($user->roles as $role)
	{
		echo $role->pivot->created_at;
	}

Al _Role_ model viene automaticamente assegnato un attributo _pivot_ che contiene una rappresentazione della tabella intermedia, e può essere usata esattamente come ogni altro model.

Di default, solo le chiavi della relazione saranno presenti nell'oggetto _pivot_. In caso tu voglia includere altri attributi, specificali in fase di definizione della relazione.

	return $this->belongsToMany('App\Role')->withPivot('foo', 'bar');

Adesso, _foo_ e _bar_ saranno accessibili tramite l'oggetto _pivot_.

Puoi inoltre decidere di includere dei timestamp per i record sulla tabella pivot (visto che di default, per queste tabelle, non vengono inseriti).

	return $this->belongsToMany('App\Role')->withTimestamps();

#### Cancellare i Record su una Tabella Pivot

Per cancellare tutti i record su una tabella pivot, basta usare il metodo _detach_.

	User::find(1)->roles()->detach();

Ovviamente, quest'operazione non cancella anche i record su _roles_, ma solo quelli intermedi.

#### Aggiornamento di un Record sulla Tabella Pivot

A volte potresti ritrovarti la necessità di aggiornare dei dati sulla tabella pivot, senza però effettuare un detach. Tutto quello che devi fare, in tal caso, è usare `updateExistingPivot`:

	User::find(1)->roles()->updateExistingPivot($roleId, $attributes);

#### Definire un Model per un Pivot

Se preferisci, puoi optare per la definizione di un model separato per gestire al meglio un pivot. La prima cosa da fare è creare una "base" che estenda Eloquent. Negli altri model interessati, quindi, estendi questa base al posto di usare quella classica. Nel model di base appena realizzato quindi usa la seguente funzione che ritorna l'istanza del custom pivot.

	public function newPivot(Model $parent, array $attributes, $table, $exists)
	{
		return new YourCustomPivot($parent, $attributes, $table, $exists);
	}

<a name="collection"></a>
## Le Collection

Ogni set di risultati di Eloquent, che sia tramite relazione o tramite il semplice _get_, viene ritornato tramite un oggetto collection. Tale oggetto implementa l'interfaccia PHP `IteratorAggregate`. In questo modo può essere iterato come un array normale. Tuttavia, in aggiunta alle operazione base, permette anche la definizione di altri metodi. Vediamo un po' quali ci vengono messi a disposizione.

#### Controllare se una Collection ha una certa Chiave

Vogliamo determinare se una collection contiene l'elemento che ha una certa chiave primaria. _contains_ fa al caso nostro:

	$roles = User::find(1)->roles;

	if ($roles->contains(2))
	{
		//
	}

Le collection possono anche essere convertite velocemente in array, o JSON.

	$roles = User::find(1)->roles->toArray();

	$roles = User::find(1)->roles->toJson();

Se una collection viene convertita in stringa, verrà convertita automaticamente in JSON.

	$roles = (string) User::find(1)->roles;

#### Iterare in una Collection

Una collcetion Eloquent contiene inoltre una serie di metodi utili per il looping e il filtraggio di elementi al suo interno.

	$roles = $user->roles->each(function($role)
	{
		//
	});

#### Filtraggio

Filtrare una collection significa specificare una callback che verrà usata per eseguire un'operazione di controllo sull'elemento attuale dell'iterazione. Se tale controllo ritorna _true_, allora l'elemento rimane dentro.

	$users = $users->filter(function($user)
	{
		return $user->isAdmin();
	});

> **Nota:** se filtri una collection e la converti poi in JSON, usa `values()` per resettare le chiavi dell'array.

#### Applicare una Callback ad Ogni Elemento

	$roles = User::find(1)->roles;

	$roles->each(function($role)
	{
		//
	});

#### Ordinamento della Collection in Base ad un Valore

	$roles = $roles->sortBy(function($role)
	{
		return $role->created_at;
	});

#### Ordinamento della Collection in Base ad un Valore #2

	$roles = $roles->sortBy('created_at');

#### Return di una Collection Personalizzata

Se può servirti, puoi far ritornare ad un metodo una collection personalizzata a cui aggiungere i tuoi metodi. Basta effettuare l'override del metodo _newCollection_.

	class User extends Model {

		public function newCollection(array $models = array())
		{
			return new CustomCollection($models);
		}

	}

<a name="accessor-e-mutator"></a>
## Accessor e Mutator

#### Definire un Accessor

Eloquent ti da la possibilità di trasformare gli attributi del tuo model quando li usi (sia in input che output). Definire un accessor, ovvero un metodo che restituisce una versione "trasformata" di un attributo, è davvero semplice. Basta seguire la notazione _getFooAttribute_, dove _foo_ è l'attributo da usare.

Un esempio:

	class User extends Model {

		public function getFirstNameAttribute($value)
		{
			return ucfirst($value);
		}

	}

Cosa è successo? L'attributo *first_name* ha un accessor. Nel momento in cui richiediamo tale attributo, tramite un semplice _$user->first_name_, viene eseguito il metodo che restituisce una versione della stringa con la prima lettera maiuscola. L'attributo in se non viene modificato.

#### Definire un Mutator

Un mutator è l'esatto opposto dell'accessor. Se l'accessor trasforma un attributo restituendone come output la versione "modificata", il mutator invece trasforma un dato in input, cambiando quindi il dato inserito nell'attributo.

	class User extends Model {

		public function setFirstNameAttribute($value)
		{
			$this->attributes['first_name'] = strtolower($value);
		}

	}

<a name="date-mutator"></a>
## Date Mutator

Di default, Eloquent converte i campi _created_at_ e _updated_at_ in istanze di [Carbon](https://github.com/briannesbitt/Carbon), package dedicato al lavoro con le date. Estende la classe PHP nativa _DateTime_.

Per una maggiore comodità puoi specificare quali campi trasformare automaticamente e quali invece disabilitare, effettuando l'override del metodo _getDates_ del model.

	public function getDates()
	{
		return array('created_at');
	}

Per disabilitare totalmente la trasformazione delle date non devi fare altro che ritornare un array vuoto.

	public function getDates()
	{
		return array();
	}

<a name="casting-attributi"></a>
## Casting degli Attributi

Potresti trovarti, di tanto in tanto, di fronte alla necessità di convertire sempre un certo campo in un certo formato. In tal caso, usare la proprietà _casts_ del tuo model risolverebbe ogni tuo problema. Puoi infatti specificare per quale attributo effettuare l'operazione e, ovviamente, il formato di destinazione della conversione.

	/**
	 * @var array
	 */
	protected $casts = [
		'is_admin' => 'boolean',
	];

Da questo momento in poi, il valore di _is_admin_ verrà automaticamente convertito in booleano. Tipicamente è memorizzato nel database come un integer. Gli altri valori supportati per la conversione sono `integer`, `real`, `float`, `double`, `string`, `boolean`, ed `array`.

Il cast in _array_ è particolarmente utile se stai lavorando con colonne che hanno come valori dei JSON serializzati. Immagina un campo _TEXT_ che contiene del JSON serializzato. Aggiungendo il cast come _array_ avresti il dato pronto all'uso senza nessuna ulteriore modifica.

Un esempio? Eccolo:

	/**
	 * @var array
	 */
	protected $casts = [
		'options' => 'array',
	];

Da questo momento in poi, usando il model Corrispondente...

	$user = User::find(1);

	// $options è un array...
	$options = $user->options;

	// options viene automaticamente serializzato come JSON
	$user->options = ['foo' => 'bar'];

<a name="eventi-model"></a>
## Eventi del Model

I model di Eloquent sono progettati per lanciare, in determinati momenti della loro "vita", determinati eventi. Ne sono vari: `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `restoring`, `restored`. I nomi non dovrebbero lasciare spazio a dubbi.

Ad esempio, per intenderci, nel momento in cui un elemento viene creato per la prima volta, gli eventi _creating_ e _created_ vengono lanciati. Ci sono poi _updating_ e _updated_ in caso di aggiornamento, e così via.

#### Cancellare un'Operazione di Salvataggio con un Evento

Nel caso in cui gli eventi _creating_, _updating_, _saving_ e _deleting_ dovessero ritornare _false_, le azioni rispettive verrebbero cancellate.

	User::creating(function($user)
	{
		if ( ! $user->isValid()) return false;
	});

#### Dove Registrare un Event Listener?

La classe _EventListenerProvider_ è stata creata appositamente per permetterti di registrare dei binding dedicati agli eventi dei model. Ad esempio:

	/**
	 * @param  \Illuminate\Contracts\Events\Dispatcher  $events
	 * @return void
	 */
	public function boot(DispatcherContract $events)
	{
		parent::boot($events);

		User::creating(function($user)
		{
			//
		});
	}

<a name="model-observer"></a>
## Model Observer

Gli eventi dei model sono interessanti, vero, ma si può fare di meglio. Si può decidere, infatti, di creare un Model Observer. Una classe observer può implementare tutti i metodi che equivalgono agli eventi di un model. Tuttavia, a differenza del semplice listener, l'approccio è molto più pulito ed elegante.

Ecco qui di seguito un esempio di observer:

	class UserObserver {

		public function saving($model)
		{
			//
		}

		public function saved($model)
		{
			//
		}

	}

Basta quindi usare il metodo _observe_ per registrare un nuovo observer.

	User::observe(new UserObserver);

<a name="convertire-array-json"></a>
## Convertire in Array o JSON

#### Convertire un Model in Array

Quando costruisci un'API potresti avere la necessità di convertire velocemente un tuo model (e rispettive relazioni) in JSON. Eloquent, out of the box, include dei metodi per ottenere il risultato velocemente.

Uno di questi è _toArray_.

	$user = User::with('roles')->first();

	return $user->toArray();

Nota bene che l'intera collection viene convertita senza problemi in array.

	return User::all()->toArray();

#### Convertire un Model in JSON

Stessa cosa vale per il formato JSON: basta usare _toJson_.

	return User::find(1)->toJson();

#### Return di un Model da una Route

Ci hai fatto già caso? Se ritorni un model o una collection da una route, questi verranno convertiti immediatamente in JSON!

	Route::get('users', function()
	{
		return User::all();
	});

#### Nascondere gli Attributi in Fase di Conversione

A volte potresti avere la necessità di limitare il numero di attributi mandati in output durante una conversione, che sia in JSON o semplice array. Ricorda che c'è la proprietà _hidden_!

	class User extends Model {

		protected $hidden = array('password');

	}

> **Nota:** desideri nascondere un'intera relazione? Ricorda di usare il nome del metodo e non quello del dynamic accessor.

Con _hidden_, comunque, puoi definire una "blacklist". Se vuoi usare l'approccio inverso, allora ti conviene usare l'attributo _$visible_.

	protected $visible = array('first_name', 'last_name');

Occasionalmente, potresti aver bisogno di aggiungere alcuni attributi che in realtà non hanno una corrispondenza con una colonna del database. Puoi definire un accessor per tale valore senza problemi.

	public function getIsAdminAttribute()
	{
		return $this->attributes['admin'] == 'yes';
	}

Una volta creato l'accessor, specifica il campo nell'array _$appends_ del tuo model.

	protected $appends = array('is_admin');

Una volta che l'attributo viene aggiunto, questo verrà automaticamente considerato anche in caso di conversione in array o JSON. Gli attributi in _appends_ rispettano inoltre le regole specificate in _visible_ e _hidden_, se presenti.
