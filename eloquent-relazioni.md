# Eloquent: Relationships

- [Introduzione](#introduzione)
- [Definire le Relazioni](#definire-relazioni)
	- [Uno a Uno](#uno-a-uno)
	- [Uno a Molti](#uno-a-molti)
	- [Molti a Molti](#molti-a-molti)
	- [Ha Molti Tramite](#ha-molti-tramite)
	- [Relazioni Polimorfiche](#relazioni-polimorfiche)
	- [Relazioni Polimorfiche Molti a Molti](#relazioni-polimorfiche-molti-a-molti)
- [Interrogare le Relazioni](#interrogare-relazioni)
	- [Eager Loading](#eager-loading)
	- [Eager Loading e Condizioni](#eager-loading-condizioni)
	- [Lazy Eager Loading](#lazy-eager-loading)
- [Inserire Model Correlati](#inserire-model-correlati)
	- [Inserimenti e Relazioni Molti a Molti](#inserimenti-relazioni-molti-a-molti)

<a name="introduzione"></a>
## Introduzione

Le tabelle di un database, spesso, hanno delle relazioni di vario tipo che le legano tra loro. Ad esempio, un post può avere dei commenti correlati, così come un ordine di un e-commerce può avere dei prodotti ad esso associati. Uno degli obiettivi di Eloquent è renderti la vita più semplice mentre lavori con queste relazioni.

Come? Tramite il supporto di tutte le relazioni tipiche (one to one, one to many, many to many) e di altre più complesse:

- [Uno a Uno](#uno-a-uno)
- [Uno a Molti](#uno-a-molti)
- [Molti a Molti](#molti-a-molti)
- [Ha Molti Tramite](#ha-molti-tramite)
- [Relazine Polimorfica](#relazione-polimorfica)
- [Relazione Polimorfica Molti a Molti](#relazione-polimorfica-molti-molti)

<a name="definire-relazioni"></a>
## Definire le Relazioni

Per definire una relazione con Eloquent basta aggiungere un metodo al tuo model, dove necessario. Tali metodi, quindi, possono essere riutilizzati dopo nel codice come dei [query builder](/docs/5.1/database-query-builder). Ecco un esempio per rendere subito l'idea:

	$user->posts()->where('active', 1)->get();

Semplice da leggere, vero?

Bene: prima di capire come usare le relazioni, però, vediamo come definirle. Una ad una.

<a name="uno-a-uno"></a>
### Uno a Uno

Una relazione uno a uno è la più semplice delle relazioni. Immagina, ad esempio, di avere un elenco di utenti. Tutti questi utenti hanno, ad essi associato, un telefono. Un utente non può avere più di un telefono per volta. Quindi, in ogni caso, un utente avrà uno ed un solo telefono associato. Avremo un model _User_ ed un _Phone_.

Per definire una relazione del genere basta creare un metodo simile nella classe _User_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get the phone record associated with the user.
		 */
		public function phone()
		{
			return $this->hasOne('App\Phone');
		}
	}

Il nome del metodo, _phone_, non è necessariamente il nome del model a cui è "diretta" tale relazione. In questo caso è stato scelto per comodità. In questo metodo c'è una singola istruzione, _$this->hasOne_. Il parametro passato è il nome del model a cui fa riferimento tale relazione.

A quel punto, il telefono dell'utente può essere "recuperato" tramite un semplice:

	$phone = User::find(1)->phone;

Esatto, non viene chiamato come metodo: Eloquent supporta infatti l'uso delle [proprietà dinamiche](#proprieta-dinamiche). Tali proprietà "speciali" ti permettono di accedere al valore ritornato dai metodi delle relazioni come fossero proprietà.

Eloquent, di default, assume che la chiave esterna da te usata abbia un nome basato su quello del model. Ad esempio, suppone che nella tabella dei telefoni _phones_ ci sia una chiave esterna *user_id*, derivata da _User_, il nome del model. Se non dovesse essere questo il tuo caso, ricorda che puoi sempre specificare anche un secondo parametro, dopo il nome della classe del model "target" della relazione.

	return $this->hasOne('App\Phone', 'altra_chiave_esterna');

Inoltre, Eloquent assume anche che la chiave primaria, di default, sia _id_. Se la cosa non dovesse riflettere le tue necessità, anche in questo caso puoi scegliere di cambiare le cose specificando un terzo parametro:

	return $this->hasOne('App\Phone', 'altra_chiave_esterna', 'altra_chiave_locale');

#### Definire l'Inverso della Relazione

Ok, possiamo accedere al model _Phone_ dal nostro _User_. Adesso, definiamo una relazione inversa, che partendo dal model _Phone_ ci permetta di accedere all'_User_ corrispondente. Lo si può fare, in modo molto veloce, con il metodo _belongsTo_:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Phone extends Model
	{
		/**
		 * Get the user that owns the phone.
		 */
		public function user()
		{
			return $this->belongsTo('App\User');
		}
	}

Nell'esempio appena visto, Eloquent proverà a cercare l'utente a cui il campo *user_id* fa riferimento. Userà, proprio come fa con _hasOne_ delle chiavi esterne e locali seguendo una certa consuetudine: esaminando il nome della relazione e mettendoci subito dopo un *_id*. Nulla comunque ti vieta di definire una chiave esterna diversa:

	/**
	 * Get the user that owns the phone.
	 */
	public function user()
	{
		return $this->belongsTo('App\User', 'altra_chiave_esterna');
	}

Se il model "proprietario" non usa _id_ come chiave primaria, puoi specificare un nome alternativo per il campo come terzo parametro del metodo:

	/**
	 * Get the user that owns the phone.
	 */
	public function user()
	{
		return $this->belongsTo('App\User', 'altra_chiave_esterna', 'altra_chiave_locale');
	}

<a name="uno-a-molti"></a>
### Uno a Molti

Una relazione "uno a molti" viene usata per definire delle relazioni in cui un singolo model può avere, ad esso associati, più di un model di un altro tipo. L'esempio per eccellenza in questo caso è il post di un blog che può presentare più di un commento da parte dei lettori. Realizziamo proprio questo esempio, iniziando dal metodo _hasMany_ adatto all'esigenza.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Post extends Model
	{
		/**
		 * Get the comments for the blog post.
		 */
		public function comments()
		{
			return $this->hasMany('App\Comment');
		}
	}

Ricorda: Eloquent determinerà automaticamente il nome della chiave esterna da usare seguendo la stessa convenzione vista prima. In questo caso specifico, sulla tabella dei commenti verrà cercato il campo *post_id*.

Una volta definita la relazione, accedere ai commenti è semplicissimo: basta usare la proprietà _comments_. Come già detto in precedenza, per via delle dynamic properties.

	$comments = App\Post::find(1)->comments;

	foreach ($comments as $comment) {
		//
	}

Ovviamente, dato che le relazioni possono anche "fungere" da query builder, puoi aggiungere altre condizioni specifiche alla query da effettuare. In tal caso devi usare il metodo vero e proprio:

	$comments = App\Post::find(1)->comments()->where('title', 'foo')->first();

Come già visto per _hasOne_, puoi sovrascrivere le convenzioni per quanto riguarda le chiavi esterne e locali.

	return $this->hasMany('App\Comment', 'altra_chiave_esterna');

	return $this->hasMany('App\Comment', 'altra_chiave_esterna', 'altra_chiave_locale');

#### Definire l'Inverso della Relazione

Ora che abbiamo l'accesso a tutti i commenti del post, vediamo come risalire ad un post partendo da un commento specifico. Definire l'inverso di una relazione uno a molti è facile: basta usare _belongsTo_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Comment extends Model
	{
		/**
		 * Get the post that owns the comment.
		 */
		public function post()
		{
			return $this->belongsTo('App\Post');
		}
	}

Una volta definita, si può accedere all'elemento "proprietario" usando la proprietà dinamica associata.

	$comment = App\Comment::find(1);

	echo $comment->post->title;

Nell'esempio qui sopra, Eloquent effettuerà lo stesso lavoro visto in precedenza. Cercherà il campo *post_id* e da quel punto risalirà al post "proprietario" del commento.

Anche qui possiamo decidere di sovrascrivere il nome della chiave esterna:

	/**
	 * Get the post that owns the comment.
	 */
	public function post()
	{
		return $this->belongsTo('App\Post', 'altra_chiave_esterna');
	}

E la chiave locale, nel caso non sia _id_:

	/**
	 * Get the post that owns the comment.
	 */
	public function post()
	{
		return $this->belongsTo('App\Post', 'altra_chiave_esterna', 'altra_chiave_locale');
	}

<a name="molti-a-molti"></a>
### Molti a Molti

Le relazioni molti a molti sono leggermente più complesse di quelle viste finora. Un esempio classico di una relazione del genere riguarda un sistema che gestisce degli utenti che, a loro volta, possono avere uno o più ruoli ad essi associati. Ad esempio, più di un utente può avere un ruolo "Amministratore" associato, ed un altro utente magari può avere più di un ruolo ad egli collegato. Per definire una simile relazione bisogna usare una tabella intermedia, detta "pivot". Tale tabella, il cui nome deriverà da quelli scelti per i model in ordine alfabetico, conterrà le chiavi esterne interessate nella relazione.

Ad esempio, nel caso _User_ e _Role_, avremo le due tabelle _users_, _roles_ e *role_user*. All'interno di *role_user* troveremo due campi *role_id* ed *user_id*. 

Le relazioni molti a molti vengono definite tramite un metodo che richiama _belongsToMany_. Definiamo la relazione necessaria al model _User_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The roles that belong to the user.
		 */
		public function roles()
		{
			return $this->belongsToMany('App\Role');
		}
	}

Accedere ai ruoli di un utente, a quel punto, funziona esattamente come visto prima.

	$user = App\User::find(1);

	foreach ($user->roles as $role) {
		//
	}

Si può anche usare il metodo per avere un query builder con cui effettuare ricerche più complesse.

	$roles = App\User::find(1)->roles()->orderBy('name')->get();

Come menzionato in precedenza, per determinare il nome della tabella necessaria, Eloquent di default unisce, in ordine alfabetico, i due nomi dei model interessati. Puoi chiaramente specificare un nome tuo, se preferisci, passando il nome della tabella come secondo parametro di _belongsToMany_.

	return $this->belongsToMany('App\Role', 'user_roles');

Puoi inoltre cambiare il nome delle chiavi che Eloquent deve usare per effettuare le query.

	return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'role_id');

#### Definire l'Inverso della Relazione

Stavolta le cose sono più semplici: per definire l'inverso di un _belongsToMany_, logicamente, basta usare un altro _belongsToMany_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Role extends Model
	{
		/**
		 * The users that belong to the role.
		 */
		public function users()
		{
			return $this->belongsToMany('App\User');
		}
	}

Esatto: esattamente la stessa. Con le stesse identiche regole viste poco fa.

#### Recuperare i Dati della Tabella Pivot

Come abbiamo visto poco fa, le relazioni molti a molti hanno bisogno di tabelle intermedie. Eloquent offre svariati modi, e tutti molto veloci, di lavorare con questi dati "intermedi". Un modo è quello di usare l'attributo _pivot_ sui model interessati:

	$user = App\User::find(1);

	foreach ($user->roles as $role) {
		echo $role->pivot->created_at;
	}

Di default, gli unici dati disponibili in fase di lettura saranno le chiavi esterne presenti sulla tabella pivot. Potresti tuttavia voler inserire altri campi, o magari leggere i timestamp relativi ad un'assegnazione. In tal caso, puoi usare _withPivot_:

	return $this->belongsToMany('App\Role')->withPivot('altro_campo_da_includere', 'altro_campo_da_includere_2');

Per quanto riguarda i timestamp, invece:

	return $this->belongsToMany('App\Role')->withTimestamps();

<a name="ha-molti-tramite"></a>
### Ha Molti Tramite

La relazione "ha molti tramite" è una scorciatoia molto comoda che Eloquent mette a disposizione per accedere a relazioni separate da altre relazioni intermedie. Immagina un model _Country_, che ha ad esso associati dei _Post_ tramite un altro model _User_ in mezzo. Qualcosa che, a tabelle, può essere descritto così:

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

Nonostante la tabella _posts_ non contenga un campo *country_id*, la relazione _hasManyThrough_ permette di accedere velocemente ai post di un determinato paese attraverso la sintassi `$country->posts`. Eloquent, autonomamente, calcola tutto quello che serve. Vediamo come definirla:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Country extends Model
	{
		/**
		 * Get all of the posts for the country.
		 */
		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'App\User');
		}
	}

Il primo argomento che viene passato è il nome del model finale a cui accedere, mentre il secondo è quello intermedio. Anche qui vengono seguite delle convenzioni, ma si possono facilmente sovrascrivere specificando altri due parametri: la chiave esterna sul model intermedio e quella esterna sul model finale. Così:

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'App\User', 'country_id', 'user_id');
		}

	}

<a name="relazioni-polimorfiche"></a>
### Relazioni Polimorfiche

#### Struttura della Tabella

Le relazioni polimorfiche permettono ad un model di "appartenere" a più di un tipo di model allo stesso tempo, tramite la stessa associazione. Immagina di voler memorizzare delle foto, sia per i membri del tuo staff che per i tuoi prodotti. Usando le relazioni polimorfiche potrai definire una sola tabella _photos_ per entrambi gli scenari.

Vediamo la struttura richiesta a livello di tabelle per una relazione del genere:

	staff
		id - integer
		name - string

	products
		id - integer
		price - integer

	photos
		id - integer
		path - string
		imageable_id - integer
		imageable_type - string

Come puoi ben immaginare, i campi chiave sono `imageable_id` ed `imageable_type` sulla tabella `photos`. `imageable_type` conterrà il nome della classe del model "proprietario". La colonna `imageable_id`, invece, la sua chiave primaria.

Anche in questo caso, una volta definiti i dati sarà Eloquent a fare tutto il resto.

#### Struttura dei Model

Adesso vediamo le varie definizioni dei model da usare:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Photo extends Model
	{
		/**
		 * Get all of the owning imageable models.
		 */
		public function imageable()
		{
			return $this->morphTo();
		}
	}

	class Staff extends Model
	{
		/**
		 * Get all of the staff member's photos.
		 */
		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}
	}

	class Product extends Model
	{
		/**
		 * Get all of the product's photos.
		 */
		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}
	}

#### Recuperare i Dati da una Relazione Polimorfica

Una volta che il tuo database ed i tuoi model sono stati definiti, puoi accedere alla tua relazione normalmente, attraverso i model. Ad esempio, così si può accedere all'insieme delle foto di un membro dello staff:

	$staff = App\Staff::find(1);

	foreach ($staff->photos as $photo) {
		//
	}

Partendo da una foto, invece, puoi accedere al "proprietario" dell'elemento tramite il metodo (o proprietà dinamica, se si preferisce) `imageable`.

	$photo = App\Photo::find(1);

	$imageable = $photo->imageable;

La relazione _imageable_ sul model _Photo_ potrà ritornare sia un'istanza di _Staff_ che di _Product_, in base al tipo del "proprietario".

<a name="relazioni-polimorfiche-molti-a-molti"></a>
### Relazioni Polimorfiche Molti a Molti

#### Struttura delle Tabelle

In aggiunta alla classica relazione polimorfica, Eloquent ne mette a disposizione una variante "molti a molti". Ad esempio, due model _Post_ e _Video_ potrebbero condividere una relazione polimorfica con un altro model _Tag_. D'altronde, sia un post che un video potrebbero essere associati, con una molti a molti, ad uno o più tag. Usare una polimorfica molti a molti permette di avere una sola "lista" di tag condivisi, tra post e video.

Iniziamo dalla struttura delle tabelle:

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

#### Struttura dei Model

Iniziamo dai _Post_ e _Video_, che presenteranno un metodo _tags_ che richiama il metodo _morphToMany_ della classe base _Eloquent_. Nell'esempio di seguito, ecco che succede al model _Post_. Lo stesso andrà fatto per _Video_.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Post extends Model
	{
		/**
		 * Get all of the tags for the post.
		 */
		public function tags()
		{
			return $this->morphToMany('App\Tag', 'taggable');
		}
	}

#### Definire l'Inverso della Relazione

A questo punto, sul model _Tag_, va definito un metodo per ognuno dei model correlati. In questo caso quindi definiremo _posts()_ e _videos()_:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Tag extends Model
	{
		/**
		 * Get all of the posts that are assigned this tag.
		 */
		public function posts()
		{
			return $this->morphedByMany('App\Post', 'taggable');
		}

		/**
		 * Get all of the videos that are assigned this tag.
		 */
		public function videos()
		{
			return $this->morphedByMany('App\Video', 'taggable');
		}
	}

#### Recuperare i Dati della Relazione

Una volta che la tabella ed i model sono stati definiti, puoi accedere alla relazione come di consueto tramite i tuoi model: nell'esempio di seguito accedo a tutti i tag di un post, tramite proprietà dinamica.

	$post = App\Post::find(1);

	foreach ($post->tags as $tag) {
		//
	}

Per recuperare l'elemento "proprietario", invece, basta richiamare il metodo che effettua la chiamata a _morphedByMany_. Nel nostro caso, i metodi _posts_ e _videos_.

	$tag = App\Tag::find(1);

	foreach ($tag->videos as $video) {
		//
	}

<a name="interrogare-relazioni"></a>
## Interrogare le Relazioni

Avrai sicuramente notato, a questo punto, che le relazioni in Eloquent vengono definite attraverso la definizione di metodi. Puoi accedere subito agli elementi interessati da questa relazione tramite proprietà dinamica, ma che succede se richiami il metodo normalmente? Ogni metodo di una relazione ritorna un'istanza di un [query builder](/docs/5.1/database-query-builder), che puoi usare per aggiungere ulteriori condizioni alla tua richiesta e renderla più specifica.

Per esempio, immagina un blog in cui ogni _User_ ha uno o più _Post_ associati.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get all of the posts for the user.
		 */
		public function posts()
		{
			return $this->hasMany('App\Post');
		}
	}

Puoi tranquillamente richiamare la relazione _posts_ aggiungendo ulteriori condizioni alla relazione così:

	$user = App\User::find(1);

	$user->posts()->where('active', 1)->get();

Nota bene che puoi usare ogni singolo metodo che il [query builder](/docs/5.1/database-query-builder) ti mette a disposizione!

#### Metodi Vs. Proprietà Dinamiche

Quando non hai bisogno di aggiungere ulteriori condizioni ad una query di relazione, puoi usare senza problemi le proprietà dinamiche: per proprietà dinamica, lo ripeto, intendo accedere al metodo della relazione usando lo stesso nome, ma come se fosse una proprietà.

Così:

	$user = App\User::find(1);

	foreach ($user->posts as $post) {
		//
	}

Le proprietà dinamiche sono caratterizzate dal "lazy loading". Vuol dire che la query corrispondente verrà eseguita **solo** qualora la proprietà venisse richiamata. Per questo motivo, spesso gli sviluppatori preferiscono fare ricorso all'[eager loading](#eager-loading) per "pre-caricare" le relazioni che sicuramente verranno usate. Tale tecnica, come vedremo a breve, permette un grande risparmio in termini di risorse e chiamate al database.

#### Query sull'Esistenza di una Relazione

Quando accedi ai record di un certo model, potresti voler "limitare" i tuoi risultati in base all'esistenza di una certa relazione. Immagina ad esempio di voler recuperare i vari post che hanno almeno un commento. Il metodo _has_ ci viene in soccorso:

	// Post con almeno un commento...
	$posts = App\Post::has('comments')->get();

Puoi anche specificare un operatore ed un termine di paragone per personalizzare la richiesta

	// Post con almeno tre commenti...
	$posts = Post::has('comments', '>=', 3)->get();

Il metodo "has", inoltre, supporta la dot notation. Il che vuol dire che, per recuperare un ipotetico elenco di post con almeno un commento, a sua volta con almeno un voto...

	// Post con almeno un commento ed un voto...
	$posts = Post::has('comments.votes')->get();

Se hai bisogno di ulteriore potenza, puoi usare anche _whereHas_ o _orWhereHas_. Questi metodi ti permettono di aggiungere ulteriori condizioni a quelle già viste:

	// Recupera tutti i post con almeno un commento che a sua volta contiene la parola "foo"...
	$posts = Post::whereHas('comments', function ($q) {
		$q->where('content', 'like', 'foo%');
	})->get();

<a name="eager-loading"></a>
### Eager Loading

Quando accedi alle relazioni Eloquent usando le proprietà dinamiche, i dati della relazione vengono caricati in base alla necessità, al momento della richiesta e non prima. Tuttavia, Eloquent offre una funzionalità chiamata Eager Loading, che permette di risolvere il problema piuttosto fastidioso detto "N + 1 query".

Facciamo un esempio per capirci meglio. Ecco un model _Book_, che possiede un metodo _author()_ che ne identifica l'autore.

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Book extends Model
	{
		/**
		 * Get the author that wrote the book.
		 */
		public function author()
		{
			return $this->belongsTo('App\Author');
		}
	}

Recuperiamo, ora, tutti i libri ed il rispettivo nome dell'autore.

	$books = App\Book::all();

	foreach ($books as $book) {
		echo $book->author->name;
	}

Tale blocco consiste in una query per recuperare tutti i libri presenti, ed un'altra query per ogni libro per cercarne l'autore. Ora, con 25 libri arriviamo ad un totale di 26 query (1 per i libri, 25 per gli autori). Tramite l'Eager Loading possiamo ridurre tutto a 2 query. Come? Tramite l'uso di _with()_.

	$books = App\Book::with('author')->get();

	foreach ($books as $book) {
		echo $book->author->name;
	}

Cosa è successo? Semplice: le uniche due query ad essere eseguite, ora, saranno

	select * from books

	select * from authors where id in (1, 2, 3, 4, 5, ...)

#### Eager Loading per più Relazioni

Puoi usare l'Eager Loading anche per più relazioni diverse inerenti lo stesso model. Come nell'esempio di seguito:

	$books = App\Book::with('author', 'publisher')->get();

Basta passare più argomenti al metodo _with()_.

#### Eager Loading Nidificato

Tramite la sintassi "dot", puoi usare l'Eager Loading nidificato. Nell'esempio di seguito, usiamo l'Eager Loading per caricare tutti gli autori dei libri, e per tutti gli autori i loro contatti personali. Tutto con una singola istruzione:

	$books = Book::with('author.contacts')->get();

<a name="eager-loading-condizioni"></a>
### Eager Loading e Condizioni

A volte potresti voler usare l'Eager Loading su una relazione, specificando in aggiunta delle condizioni per la query di Eager Loading. Puoi farlo senza problemi così:

	$users = App\User::with(['posts' => function ($query) {
		$query->where('title', 'like', '%first%');

	}])->get();

In questo esempio, Eloquent effettua l'Eager Loading solo dei post il cui titolo contiene la parola "first". Ovviamente, puoi chiamare qualsiasi altro metodo del [query builder](/docs/5.1/database-query-builder).

	$users = App\User::with(['posts' => function ($query) {
		$query->orderBy('created_at', 'desc');

	}])->get();

<a name="lazy-eager-loading"></a>
### Lazy Eager Loading

Altre volte, potresti avere la necessità di usare l'Eager Loading solo in alcuni casi, a determinate condizioni. Tranquillo, in questo caso basta usare il metodo _load()_.

	$books = App\Book::all();

	if ($someCondition) {
		$books->load('author', 'publisher');
	}

Per aggiungere ulteriori condizioni, inoltre, basta usare una closure in questo modo:

	$books->load(['author' => function ($query) {
		$query->orderBy('published_date', 'asc');
	}]);

<a name="inserire-model-correlati"></a>
## Inserire Model Correlati

#### Il Metodo Save

Eloquent offre un modo piuttosto veloce di aggiungere nuovi model partendo da una relazione. In modo tale da ritrovarsi il record appena salvato già fornito di tutte le informazioni relative alla relazione stessa. Ad esempio, supponiamo di inserire un nuovo _Comment_ per un post specifico. Al posto di impostare manualmente il *post_id*, puoi inserire il commento tramite il metodo _save()_ della relazione.

	$comment = new App\Comment(['message' => 'A new comment.']);

	$post = App\Post::find(1);

	$comment = $post->comments()->save($comment);

Nota che non abbiamo usato _comments()_ come una proprietà dinamica, ma come metodo da richiamare per ottenere un'istanza della relazione. A quel punto Eloquent fa da solo tutto il resto.

Puoi anche salvare più di un model alla volta, tramite _saveMany_.

	$post = App\Post::find(1);

	$post->comments()->saveMany([
		new App\Comment(['message' => 'A new comment.']),
		new App\Comment(['message' => 'Another comment.']),
	]);

#### Save e le Relazioni Molti a Molti

Quando lavori con le relazioni molti a molti, il metodo _save()_ accetta un array di campi addizionali della tabella pivot intermedia come secondo parametro.

	App\User::find(1)->roles()->save($role, ['expires' => $expires]);

#### Il Metodo Create

In aggiunta a _save()_ e _saveMany()_, puoi anche usare il metodo _create()_, che accetta un array di attributi, crea il model e lo inserisce nel database salvando il record corrispondente. A differenza di _save()_ e _saveMany()_, _create()_ accetta un semplice array associativo al posto di un'istanza di model.

	$post = App\Post::find(1);

	$comment = $post->comments()->create([
		'message' => 'A new comment.',
	]);

Nota: prima di usare il metodo _create()_, dai uno sguardo alle regole dell'[assegnamento di massa](/docs/5.1/eloquent#assegnamento-massa).

<a name="inserimenti-relazioni-molti-a-molti"></a>
### Inserimenti e Relazioni Molti a Molti

#### Attaching / Detaching

Quando lavori con le relazioni molti a molti, Eloquent offre dei metodi helper aggiuntivi che ora andiamo a scoprire. Immagina di avere un utente che può avere più ruoli, ed un ruolo che può contare più utenti associati. Puoi usare il metodo _attach()_ per associare un ruolo ad un utente.

	$user = App\User::find(1);

	$user->roles()->attach($roleId);

Oltre all'id del ruolo, puoi anche passare un set di attributi da salvare sulla tabella pivot.

	$user->roles()->attach($roleId, ['expires' => $expires]);

Così come aggiungi, puoi voler rimuovere. In questo caso il metodo da usare è _detach()_.

	// Rimuovi l'associazione ruolo-utente...
	$user->roles()->detach($roleId);

	// Rimuovi tutte le associazioni con i ruoli di un certo utente...
	$user->roles()->detach();

Per convenienza, i metodi _attach_ e _detach_ accettano anche degli array di id.

	$user = App\User::find(1);

	$user->roles()->detach([1, 2, 3]);

	$user->roles()->attach([1 => ['expires' => $expires], 2, 3]);

#### Il Metodo Sync

Se preferisci, puoi usare il metodo _sync()_ per costruire le associazioni molti a molti. Il metodo _sync_ accetta un array di id da usare per l'associazione. Allo stesso tempo, tale metodo controlla se ci sono delle associazioni preccedenti e, se non risultano presenti nell'array di id passati, vengono rimosse.

	$user->roles()->sync([1, 2, 3]);

Anche in questo caso puoi passare dei dati ulteriori per ogni singola associazione, se vuoi.

	$user->roles()->sync([1 => ['expires' => true], 2, 3]);

In ogni caso, tramite il metodo _sync_, alla fine dell'operazione, avrai creato un'associazione per ogni id presente nell'array. Una scorciatoia molto, molto comoda.
