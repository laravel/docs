# Query Builder

- [Introduzione](#introduzione)
- [Select](#select)
- [Join](#join)
- [Where Avanzati](#where-avanzati)
- [Aggregati](#aggregati)
- [Raw Expressions](#raw-expressions)
- [Insert](#inserts)
- [Update](#updates)
- [Delete](#deletes)
- [Union](#unions)
- [Blocco Pessimistico](#blocco-pessimistico)

<a name="introduzione"></a>
## Introduzione

Il sistema di query building fornisce una comoda interfaccia per eseguire le tue queries. Può essere usato per eseguire molte altre operazioni sui database, ed è compatibile con tutti i database supportati da Laravel.

> **Nota:** Il query builder di Laravel usa il binding dei parametri PDO per proteggere la tua applicazione dagli attacchi di SQL injection. Non è necessario ripulire le stringhe passate come bindings.

<a name="select"></a>
## Select

#### Recuperare Tutte Le Righe Da Una Tabella

	$users = DB::table('users')->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### Chunking Dei Risultati Di Una Tabella

	DB::table('users')->chunk(100, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

Puoi arrestare il chunk dei dati ritornando `false` dalla `Closure` passata come secondo parametro del metodo chun:

	DB::table('users')->chunk(100, function($users)
	{
		//

		return false;
	});

#### Recuperare Una Singola Riga Da Una Tabella

	$user = DB::table('users')->where('name', 'John')->first();

	var_dump($user->name);

#### Recuperare Una Singola Colonna Da Una Riga

	$name = DB::table('users')->where('name', 'John')->pluck('name');

#### Recuperare Una Lista Di Valori Delle Colonne

	$roles = DB::table('roles')->lists('title');

Questo metodo ritornerà un array di titoli di ruoli. Puoi anche specificare una chiave di colonna personalizzata per l'array che verrà ritornato:

	$roles = DB::table('roles')->lists('title', 'name');

#### Specificare Una Clausula Select

	$users = DB::table('users')->select('name', 'email')->get();

	$users = DB::table('users')->distinct()->get();

	$users = DB::table('users')->select('name as user_name')->get();

#### Aggiungere Una Clausula Select Ad Una Query Esistente

	$query = DB::table('users')->select('name');

	$users = $query->addSelect('age')->get();

#### Uusare L'Operatore Where

	$users = DB::table('users')->where('votes', '>', 100)->get();

#### Statment Or

	$users = DB::table('users')
	                    ->where('votes', '>', 100)
	                    ->orWhere('name', 'John')
	                    ->get();

#### Usare Where Between

	$users = DB::table('users')
	                    ->whereBetween('votes', array(1, 100))->get();

#### Usare Where Not Between

	$users = DB::table('users')
	                    ->whereNotBetween('votes', array(1, 100))->get();

#### Usare Where In Con Un Array

	$users = DB::table('users')
	                    ->whereIn('id', array(1, 2, 3))->get();

	$users = DB::table('users')
	                    ->whereNotIn('id', array(1, 2, 3))->get();

#### Usare Where Null Per Recuperare Righe Con Campi Nulli

	$users = DB::table('users')
	                    ->whereNull('updated_at')->get();

#### Order By, Group By, Ed Having

	$users = DB::table('users')
	                    ->orderBy('name', 'desc')
	                    ->groupBy('count')
	                    ->having('count', '>', 100)
	                    ->get();

#### Offset & Limit

	$users = DB::table('users')->skip(10)->take(5)->get();

<a name="join"></a>
## Join

Il query builder può essere usato per scrivere degli statment di join. Dai un'occhiata ai seguenti esempi:

#### Join Statement Base

	DB::table('users')
	            ->join('contacts', 'users.id', '=', 'contacts.user_id')
	            ->join('orders', 'users.id', '=', 'orders.user_id')
	            ->select('users.id', 'contacts.phone', 'orders.price')
	            ->get();

#### Statement Left Join

	DB::table('users')
		    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
		    ->get();

Puoi specificare anche più clausule join avanzate:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')->orOn(...);
	        })
	        ->get();

Se preferisci usare una clausula stile "where" nelle tue join, puoi usare i metodi `where` e `orWhere` in una join. Invece di confrontare due colonne, questi metodi confronteranno la colonna con un valore:

	DB::table('users')
	        ->join('contacts', function($join)
	        {
	        	$join->on('users.id', '=', 'contacts.user_id')
	        	     ->where('contacts.user_id', '>', 5);
	        })
	        ->get();

<a name="where-avanzati"></a>
## Where Avanzati

#### Raggruppamento Di Parametri

In alcuni casi puoi aver necessità di creare delle clausule where avanzate come ad esempio "where exists" oppure raggruppare parametri annidati. Il query builder di Laravel può gestirlo come segue:

	DB::table('users')
	            ->where('name', '=', 'John')
	            ->orWhere(function($query)
	            {
	            	$query->where('votes', '>', 100)
	            	      ->where('title', '<>', 'Admin');
	            })
	            ->get();

La query sopra produrrà il seguente codice SQL:

	select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Statement Exists

	DB::table('users')
	            ->whereExists(function($query)
	            {
	            	$query->select(DB::raw(1))
	            	      ->from('orders')
	            	      ->whereRaw('orders.user_id = users.id');
	            })
	            ->get();

La query sopra produrrà il seguente codice SQL:

	select * from users
	where exists (
		select 1 from orders where orders.user_id = users.id
	)

<a name="aggregati"></a>
## Aggregati

Il query builder offre anche una serie di metodi aggregati, come `count`, `max`, `min`, `avg`, e `sum`.

#### Usare I Metodi Aggregati

	$users = DB::table('users')->count();

	$price = DB::table('orders')->max('price');

	$price = DB::table('orders')->min('price');

	$price = DB::table('orders')->avg('price');

	$total = DB::table('users')->sum('votes');

<a name="raw-expressions"></a>
## Raw Expressions

In alcuni casi puoi aver bisogno di usare dell'espressioni grezze in una query. Queste espressioni saranno iniettate nella query come stringhe, quindi fai attenzione a non creare situazioni di SQL injection! Per creare un'espressione grezza, puoi usare il metodo `DB::raw`:

#### Using A Raw Expression

	$users = DB::table('users')
	                     ->select(DB::raw('count(*) as user_count, status'))
	                     ->where('status', '<>', 1)
	                     ->groupBy('status')
	                     ->get();

<a name="insert"></a>
## Insert

#### Inserire Delle Righe In Una Tabella

	DB::table('users')->insert(
		array('email' => 'john@example.com', 'votes' => 0)
	);

#### Inserire Righe In Una Tabella Con ID Auto-Incrementante

Se una tabella ha un id auto-incrementante, usa `insertGetId` per inserire un record e recuperare l'id:

	$id = DB::table('users')->insertGetId(
		array('email' => 'john@example.com', 'votes' => 0)
	);

> **Nota:** Quando usi PostgreSQL il metodo insertGetId si aspetta che la colonna auto-incrementante sia chiamata "id".

#### Inserire Righe Multiple In Una Tabella

	DB::table('users')->insert(array(
		array('email' => 'taylor@example.com', 'votes' => 0),
		array('email' => 'dayle@example.com', 'votes' => 0),
	));

<a name="update"></a>
## Update

#### Aggiornare Delle Righe Di Una Tabella

	DB::table('users')
	            ->where('id', 1)
	            ->update(array('votes' => 1));

#### Incrementare o Decrementare Un Valore Di Una Colonna

	DB::table('users')->increment('votes');

	DB::table('users')->increment('votes', 5);

	DB::table('users')->decrement('votes');

	DB::table('users')->decrement('votes', 5);

Puoi specificare anche delle colonne aggiuntive da aggiornare:

	DB::table('users')->increment('votes', 1, array('name' => 'John'));

<a name="delete"></a>
## Delete

#### Eliminare Delle Righe Da Una Tabella

	DB::table('users')->where('votes', '<', 100)->delete();

#### Eliminare Tutte Le Righe Di Una Tabella

	DB::table('users')->delete();

#### Operazione di Truncate Table

	DB::table('users')->truncate();

<a name="union"></a>
## Union

Il query builder offre un modo veloce di “unire” insieme due query:

	$first = DB::table('users')->whereNull('first_name');

	$users = DB::table('users')->whereNull('last_name')->union($first)->get();

Puoi utilizzare anche il metodo `unionAll` allo stesso modo di `union`.

<a name="blocco-pessimistico"></a>
## Blocco Pessimistico

Il query builder include alcune funzioni per aiutarti ad eseguire un "blocco pessimistico" sui tuoi statment SELECT.

Per eseguire uno statment SELECT con un "blocco condiviso", puoi usare il metodo `sharedLock` su una query:

	DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

Per eseguire un “blocco per l'aggiornamento” su uno statment SELECT, puoi usare il metodo `lockForUpdate` su una query:

	DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
