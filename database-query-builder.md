# Database: Query Builder

- [Introduzione](#introduzione)
- [I Risultati di una Query](#risultati-query)
	- [Aggregati](#aggregati)
- [Select](#select)
- [Join](#join)
- [Unioni](#unioni)
- [Clausole Where](#clausole-where)
	- [Clausole Where Avanzate](#clausole-where-avanzate)
- [Ordinamento, Raggruppamento, Limit ed Offset](#ordinamento-raggruppamento-limit-offset)
- [Inserimenti](#inserimenti)
- [Aggiornamenti](#aggiornamenti)
- [Cancellazioni](#cancellazioni)
- [Blocco Pessimistico](#blocco-pessimistico)

<a name="introduzione"></a>
## Introduzione

Il quer
Inoltre, puoi inserire anche più di un record alla volta specificando un array di elementi, sempre nello stesso formato.
y builder di Laravel offre un modo molto conveniente e semplice di creare (ed eseguire) le query sul tuo datbase. Può essere usato per effettuare la> **Nota:** il query builder di Laravel usa il binding dei parametri presenti in PDO per proteggere le tue applicazioni da eventuali SQL Injection. Non avrai bisogno quindi di ripulire le varie stringhe prima di essere "passate".

<a name="risultati-query"></a>
## I Risultati di una Query

#### Tutte iel Auto-Incrementantia

Se la tabella che stai usando ha un id auto-incrementante, usa _insertGetId_ per ottenere l'id dell'elemento appena ottenuto.
certa tabella. Partendo da questa istanza possiamo concatenarvi uno o più metodi per porre delle condizioni, quindi concludere tale catena con un metodo _trigger_ che recupera a tutti gli effetti i risultati.

Partiamo dal caso più semplice: recuperiamo tutti i record di una tabella.

	<?php aame usando tp\Control il metodo _insertGetId_ si aspetterà di trovare una colonna _id_. Se non è questo il caso, allora passa il nome della colonna scelta come secondo parametro. lers;

	use DB;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show a list of all of the application's users.
		 *
		 * @return Response
		 */
		public function index()
		{
			$users = DB::table('users')->get();

			return view('user.index', ['users' => $users]);
		}
	}

Un po' come visto per le query grezze, il metodo _get_ ritorna un _array_ di risultati in cui ognuno di questi è un'istanza della classe _StdClass_. Per accedere ad ogni valore basta specificare il nome di tale proprietà come un qualsiasi attributo.

	foreach ($users as $user) {
		echo $user->name;
	}

#### Recuperare una Singola Riga / Colonna da una Tabella

Se vuoi recuperare una singola riga dal database, usa il metodo _first_. Il metodo ritornerà la prima occorrenza del record cercato, sempre come oggetto di tipo _StdClass_ (non più un array, stavolta, ma una singola istanza).

	$user = DB::table('users')->where('name', 'John')->first();

	echo $user->name;

Potresti, inoltre, avere la necessità di prendere il valore di una singola colonna di un singolo record. Puoi usare come nell'esempio seguente il metodo _value_.

	$email = DB::table('users')->where('name', 'John')->value('email');

Verrà ritornato direttamente l'indirizzo email di John.

#### Chunking dei Risultati

Nel caso in cui dovessi aver bisogno di lavorare con migliaia di record in una volta, considera l'uso del metodo _chunk_. Tale metodo recupera solo una parte dei risultati, e tale parte viene data in pasto ad una _Closure_ nella quale puoi decidere, successivamente, cosa farci. Può essere un ottimo strumento da usare, ad esempio, per un [comando Artisan](/docs/5.1/artisan) che processa migliaia di record alla volta.

	DB::table('users')->chunk(100, function($users) {
		foreach ($users as $user) {
			//
		}
	});

Puoi inoltre far ritornare _false_ alla closure per interrompere l'elaborazione.

	DB::table('users')->chunk(100, function($users) {
		// Process the records...

		return false;
	});

#### Recuperare una Lista di Valori di una Colonna

Se vuoi recuperare una lista dei valori di una specifica colonna, usa il metodo _lists_. In questo esempio stiamo recuperando un array di nomi di ruoli...

	$titles = DB::table('roles')->lists('title');

	foreach ($titles as $title) {
		echo $title;
	}

Puoi anche specificare una chiave da usare per l'array ritornato:

	$roles = DB::table('roles')->lists('title', 'name');

	foreach ($roles as $name => $title) {
		echo $title;
	}

<a name="aggregati"></a>
### Aggregati

Il query builder presenta anche una serie di metodi aggregato, come _count_, _max_, _min_, _avg_ e _sum_. Puoi chiamare uno qualsiasi di questi metodi dopo la creazione della query. Così:

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

Ovviamente, puoi combinare insieme questi metodi con altre clausole.

	$price = DB::table('orders')
					->where('finalized', 1)
					->avg('price');

<a name="select"></a>
## Select

#### Definire una Clausola Select

Chiaramente, non sempre avrai bisogno di selezionare tutte le colonne da una tabella. Usando il metodo _select_ potrai specificare un set di colonne da prelevare.

In questo modo:

	$users = DB::table('users')->select('name', 'email as user_email')->get();

Il metodo _distinct_, inoltre, ti permette di forzare la query in modo tale da farle ritornare solo dei valori distinti.

	$users = DB::table('users')->distinct()->get();

Se hai già un'istanza del query builder a tua disposizione e vuoi aggiungere una colonna ad una clausola select già esistente, usa _addSelect_.

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### Espressioni "Grezze"

In alcuni casi, potrebbe presentarsi la necessità di inserire delle query molto particolari in altre. Il metodo _DB::raw_ può venire in tuo soccorso, usato in combinazione con altri metodi del query builder!

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="join"></a>
## Join

#### Inner Join

Il query builder può essere usato anche per scrivere delle join. Per una semplice _inner join_ basta usare il metodo _join_ sull'istanza del query builder che stai usando. Il primo argomento ad essere passato è il nome della tabella con la quale effettuare l'operazione, mentre i successivi parametri definiscono le colonne da considerare per effettuare la join.

Nulla ti vieta inoltre di effettuare join multiple. Guarda qui:

	$users = DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.*', 'contacts.phone', 'orders.price')
	            ->get();

#### Left Join

Per effettuare una _left join_ al posto di una _inner join_, usa il metodo _leftJoin_. La segnatura del metodo è la stessa di _join_.

	$users = DB::table('users')
		    	->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    	->get();

#### Join Avanzate

A volte potresti voler costruire delle join più avanzate. Puoi farlo passando una _Closure_ come secondo argomento del metodo _join_. Tale _Closure_ riceverà un oggetto di tipo _JoinClause_, che potrai usare per specificare le varie condizioni della join in questione:

	DB::table('users')
	        ->join('contacts', function ($join) {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

Se vuoi, inoltre, puoi usare all'interno della closure i metodi _where_ ed _orWhere_ come nell'esempio seguente:

	DB::table('users')
	        ->join('contacts', function ($join) {
	        	$join->on('users.id', '=', 'contacts.user_id')
	        	     ->where('contacts.user_id', '>', 5);
	        })
	        ->get();

<a name="unioni"></a>
## Unioni

Tramite il metodo _union_, il query builder permette di effettuare un unione di due diverse query. L'esempio base, questo di seguito, prevede la creazione di una query (da notare l'assenza di un metodo trigger come _get_ o _first_) che va poi "unita" alla seconda query tramite _union_.

	$first = DB::table('users')
				->whereNull('first_name');

	$users = DB::table('users')
				->whereNull('last_name')
				->union($first)
				->get();

C'è anche un altro metodo disponibile: _unionAll_, che ha la stessa segnatura di _union_.

<a name="clausole-where"></a>
## Clausole Where

#### Where Semplici

Per aggiungere una clausola _where_ ad una query, usa il metodo _where_ sull'istanza del query builder. La versione più semplice di una where richiede tre parametri: il primo è il nome della colonna, il secondo è l'operatore, il terzo invece è il termine con il quale effettuare il controllo.

Ecco un semplice esempio: qui si stanno selezionando tutti gli utenti il cui voto è uguale a 100.

	$users = DB::table('users')->where('votes', '=', 100)->get();

Per convenienza, se hai bisogno di verificare una semplice uguaglianza, puoi evitare l'operatore, passando come secondo parametro direttamente il termine:

	$users = DB::table('users')->where('votes', 100)->get();

Ecco altri operatori che puoi usare quando scrivi un where. Sono quelli tendenzialmente supportati da un qualsiasi database system.

	$users = DB::table('users')
					->where('votes', '>=', 100)
					->get();

	$users = DB::table('users')
					->where('votes', '<>', 100)
					->get();

	$users = DB::table('users')
					->where('name', 'like', 'T%')
					->get();

#### Or

Puoi concatenare, una dopo l'altra, svariate condizioni. Puoi anche aggiungerne alcune che prevedano un "o" e non un "e" (come congiunzione). In questo caso, al posto di _where_, usa _orWhere_.

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

#### Clausole Where Aggiuntive

**whereBetween**

Il metodo _whereBetween_ ti consente di verificare se una certa colonna ha un valore in un determinato range, o meno.

	$users = DB::table('users')
	                    ->whereBetween('votes', [1, 100])->get();

**whereNotBetween**

Il metodo _whereNotBetween_ verifica che il valore di una certa colonna stia al di fuori di due valori.

	$users = DB::table('users')
	                    ->whereNotBetween('votes', [1, 100])
	                    ->get();

**whereIn / whereNotIn**

Il metodo _whereIn_ verifica che il valore di una certa colonna si trovi in uno specifico array.

	$users = DB::table('users')
	                    ->whereIn('id', [1, 2, 3])
	                    ->get();

Il metodo _whereNotIn_, invece, si assicura del contrario.

	$users = DB::table('users')
	                    ->whereNotIn('id', [1, 2, 3])
	                    ->get();

**whereNull / whereNotNull**

Il metodo _whereNull_ verifica che il valore di una certa colonna sia _NULL_.

	$users = DB::table('users')
	                    ->whereNull('updated_at')
	                    ->get();

Il metodo _whereNotNull_, invece, verifica l'esatto contrario.

	$users = DB::table('users')
	                    ->whereNotNull('updated_at')
	                    ->get();

<a name="clausole-where-avanzate"></a>
## Clausole Where Avanzate

#### Raggruppamento di Parametri

A volte avrai la nacessità di creare della clausole where più avanzate, come un _where exists_ oppure un raggruppamento di parametri nidificati. Il query builder, per (tua) fortuna, li gestisce senza problemi! Per iniziare, guardiamo all'esempio di seguito:

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function ($query) {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

Come puoi vedere, abbiamo passato una _Closure_ al metodo _orWhere_ che spiega al query builder di creare un gruppo di condizioni. La _Closure_ riceverà un'istanza del query builder, sulla quale impostare le varie condizioni corrispondenti. L'esempio appena visto, infatti, produrrà la seguente query SQL:

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Exists

Il metodo _whereExists_ ti permette di scrivere delle query _where exists_, appunto. Anche queste accettano una _Closure_ come parametro. Ecco un esempio pratico all'opera.

	DB::table('users')
	            ->whereExists(function ($query) {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

La query SQL corrispondente a queste istruzioni sarà la seguente:

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="ordinamento-raggruppamento-limit-offset"></a>
## Ordinamento, Raggruppamento, Limit ed Offset

#### orderBy

Il metodo _orderBy_ ti permette di ordinare i risultati in base al valore di una certa colonna. Il primo argomento che viene passato è il nome della colonna di riferimento, mentre il secondo serve a controllare la direzione dell'ordinamento. I valori possono essere "asc" o "desc".

	$users = DB::table('users')
					->orderBy('name', 'desc')
					->get();

#### groupBy / having / havingRaw

I metodi _groupBy_ ed _having_ ti permettono di raggruppare i risultati della query. Il metodo _having_ è simile al _where_ nella segnatura:

	$users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

Il metodo _havingRaw_ può essere usato per impostare una stringa "grezza" come valore per la clausola _having_. Nell'esempio seguente stiamo cercando tutti i dipartimenti con più di $2500 di vendite.

	$users = DB::table('orders')
					->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > 2500')
                    ->get();

#### skip / take

Per limitare il numero di risultati ritornati dalla query, o per saltarne un certo numero (si parla di offset in questo caso) puoi usare i metodi _skip_ e _take_.

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="inserimenti"></a>
## Inserimenti

Il query builder offre il metodo _insert_ per quanto riguarda gli inserimenti di nuovi record nel database. Tale metodo accetta un array di nomi di colonne e valori (come array associativo) in questo modo:

	DB::table('users')->insert(
		['email' => 'john@example.com', 'votes' => 0]
	);

Inoltre, puoi inserire anche più di un record alla volta specificando un array di elementi, sempre nello stesso formato.

	DB::table('users')->insert([
		['email' => 'taylor@example.com', 'votes' => 0],
		['email' => 'dayle@example.com', 'votes' => 0]
	]);

#### ID Auto-Incrementanti

Se la tabella che stai usando ha un id auto-incrementante, usa _insertGetId_ per ottenere l'id dell'elemento appena ottenuto.

	$id = DB::table('users')->insertGetId(
		['email' => 'john@example.com', 'votes' => 0]
	);

> **Nota:** usando PostgreSQL il metodo _insertGetId_ si aspetterà di trovare una colonna _id_. Se non è questo il caso, allora passa il nome della colonna scelta come secondo parametro.  the insertGetId method expects the auto-incrementing column to be named `id`. If you would like to retrieve the ID from a different "sequence", you may pass the sequence name as the second parameter to the `insertGetId` method.

<a name="aggiornamenti"></a>
## Aggiornamenti

Ovviamente, in aggiunta all'inserimento di record nel database, il query builder può inoltre aggiornare un record esistente usando il metodo _update_. Tale metodo accetta, come per _insert_, un array associativo contenente le colonne da aggiornare. Per dare una condizione all'aggiornamento si può usare tutto quello che già si è visto in precedenza.

In questo esempio stiamo modificando la colonna _votes_ per l'utente dall'id uguale ad 1.

	DB::table('users')
	            ->where('id', 1)
	            ->update(['votes' => 1]);

#### Incremento / Decremento

Il query builder, inoltre, offre alcuni metodi di comodo per incrementare o decrementare il valore di una certa colonna. Si tratta di una scorciatoia, creata appositamente per offrirti una sintassi più espressiva.

Tutti questi metodi accettano almeno un parametro: la colonna da aggiornare. Un secondo parametro, opzionale, indica una quantità da usare come valore per l'operazione.

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

Tramite l'aggiunta di un terzo parametro, inoltre, puoi effettuare un ulteriore update di altri campi.

	DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="cancellazioni"></a>
## Cancellazioni

Anche la cancellazione di uno o più record viene inclusa tra le feature del query builder. Ecco come cancellare, ad esempio, tutti i record dalla tabella _users_.

	DB::table('users')->delete();

Puoi "condizionare" l'operazione di cancellazione come già avvenuto per l'update:

	DB::table('users')->where('votes', '<', 100)->delete();

... infine, puoi scegliere di "troncare" l'intera tabella, ovvero cancellare tutti i record e resettare l'ID auto-incrementante.

	DB::table('users')->truncate();

<a name="blocco-pessimistico"></a>
## Blocco Pessimistico

Il query builder include, inoltre, alcune funzioni piuttosto utili per il cosiddetto "pessimistic locking".

In poche parole, durante una transazione il pessimistic locking permette di bloccare eventuali transazioni in conflitto con quella corrente. Può essere utile in caso di forte necessità di integrità e di prevenzione.

Il metodo da usare è `sharedLock`: previene ogni modifica sui record selezionati fin quando la transazione corrente non è conclusa.

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

In alternativa, puoi usare anche `lockForUpdate`. Se decidi di usarlo, ricorda che questo metodo evita eventuali update e selezioni con un altro lock.

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
