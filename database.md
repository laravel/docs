# Uso Base Dei Database

- [Configurazione](#configurazione)
- [Lettura / Scrittura delle Connesioni](#lettura-scrittura-connessioni)
- [Esecuzione Query](#esecuzione-query)
- [Database Transaction](#database-transaction)
- [Connessioni Di Accesso Al DB](#connessioni-di-accesso)
- [Query Logging](#query-logging)

<a name="configurazione"></a>
## Configurazione

Con Laravel connettersi al database ed eseguire queries è davvero un gioco da ragazzi. Il file di configurazione è `config/database.php`. In questo file puoi definire tutte le connessioni ai database, specificandone una di default. Esempi per tutti i sistemi database vengono forniti in questo file.

Attualmente Laravel supporta 4 sistemi database: MySQL, Postgres, SQLite, e SQL Server.

<a name="ettura-scrittura-connessioni"></a>
## Lettura / Scrittura delle Connesioni

Qualche volta potresti desidera di usare una connessione per lo statmente SELECT, un altra per gli statement INSERT, UPDATE e DELETE. Laravel lo rende un gioco da ragazzi, e saranno sempre usate le opportune connesioni mentre stai eseguendo raw query, o query builder, o Eloquent ORM.

Per vedere come le connesioni debbano essere configurate per lettura / scrittura, dai un'occhiata a questo esempio:

	'mysql' => array(
		'read' => array(
			'host' => '192.168.1.1',
		),
		'write' => array(
			'host' => '196.168.1.2'
		),
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	),

Nota che le due chiavi devono essere aggiunte all'array di configurazione: `read` e `write`. Entrambe le chiavi contengono un array con una sola chiave: `host`. Il resto delle opzioni del database per la lettura e scrittura delle connessioni sarà inglobato nell'array principale `mysql`. Quindi, abbiamo solo bisogno di inserire gli elementi negli array `read` e `write` se vogliamo sovrascrivere i valori nell'array principale. In questo caso, `192.168.1.1` sarà usato per la connessione in "lettura", mentre `192.168.1.2` sarà usato per la connessione in "scrittura". Le credenziali del database, prefix, character set, e tutte le altre nell'array `mysql` saranno condivise con entrambe le connessioni.

<a name="esecuzione-query"></a>
## Esecuzione Query

Una volta configurato la connessione al database, puoi eseguire le query usando la facade `DB`.

#### Eseguire Una Query Di Selezione

	$results = DB::select('select * from users where id = ?', [1]);

Il metodo `select` ritornerà sempre un `array` di risultati.

#### Eseguire Uno Statement Insert

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### Eseguire Uno Statement Update

	DB::update('update users set votes = 100 where name = ?', ['John']);

#### Eseguire Uno Statement Delete

	DB::delete('delete from users');

> **Nota:** Gli statement `update` e `delete` ritornano il numero di righe affette dall'operazione.

#### Eseguire Uno Statement Generale

	DB::statement('drop table users');

#### Intercettare Eventi

Puoi anche intercettare eventi per le query usando il metodo `DB::listen`:

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transaction"></a>
## Database Transaction

Per eseuire un insieme di operazioni con le database transaction, puoi usare il metodo `transaction`:

	DB::transaction(function()
	{
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

> **Nota:** Qualsiari eccezione intercettata all'interno di `transaction` dalla Closure eseguirà un rollback delle transazioni in modo automatico.

In alcuni casi puoi aver bisogno di iniziare una transazione stessa:

	DB::beginTransaction();

Puoi eseguire un rollback di una transazione tramite il metodo `rollback`:

	DB::rollback();

Infine, puoi eseguire il commit di una transazione tramite il metodo `commit`:

	DB::commit();

<a name="connessioni-di-accesso"></a>
## Connessioni Di Accesso Al DB

Quando usi connessioni multiple, puoi accederci tramite il metodo `DB::connection`:

	$users = DB::connection('foo')->select(...);

Puoi anche accedere direttamente ai dati attraverso un’istanza PDO:

	$pdo = DB::connection()->getPdo();

Oppure potresti aver bisogno di riconentterti ad un database. Ecco come fare:

	DB::reconnect('foo');

Se hai bisogno di disconnetterti da un database per evitare di eccedere il limite di istanze PDO `max_connections`, usa il metodo `disconnect`:

	DB::disconnect('foo');

<a name="query-logging"></a>
## Query Logging

Di default, Laravel mantiene un log in memoria di tutte le query che sono state eseguite dalla richiesta corrente. Tuttavia, in alcuni casi, come ad esempio nel caso di inserimento di un gran numero di righe, questo può causare un uso eccessivo della memoria da parte della tua applicazione. Per disabilitare il log, puoi usare il metodo `disableQueryLog`:

	DB::connection()->disableQueryLog();

Per recuperare un array delle query eseguite, usa il metodo `getQueryLog`:

       $queries = DB::getQueryLog();
