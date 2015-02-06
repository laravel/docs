# Schema Builder

- [Introduzione](#introduzione)
- [Creare ed Eliminare Tabelle](#creare-eliminare-tabelle)
- [Aggiunta di Colonne](#aggiunta-colonne)
- [Modifica delle Colonne](#modifica-colonne)
- [Rinominare una Colonna](#rinominare-colonna)
- [Cancellare una Colonna](#cancellare-colonna)
- [Controlli di Esistenza](#controlli-esistenza)
- [Aggiunta di Indici](#aggiunta-indici)
- [Chiavi Esterne](#chiavi-esterne)
- [Cancellare gli Indici](#cancellare-indici)
- [Cancellazione Timestamp e Soft Delete](#cancellazione-timestamp)
- [Motori di Storage](#motori-storage)

<a name="introduzione"></a>
## Introduzione

La classe _Schema_ di Laravel fornisce un modo molto comodo di modificare le tabelle del proprio database indipendentemente dal sistema usato. Funziona bene con tutti i driver supportati da Laravel, e presenta un'API unificata.

<a name="creare-eliminare-tabelle"></a>
## Creare ed Eliminare Tabelle

Per creare una nuova tabella sul database, usa il metodo _Schema::create_:

	Schema::create('users', function($table)
	{
		$table->increments('id');
	});

Il primo argomento ad essere passato è il nome della tabella, mentre il secondo è una _Closure_ che riceve come argomento un oggetto di tipo _Blueprint_ che può essere usato per definire i campi della nuova tabella.

Per cambiare il nome ad una tabella esistente, invece, si usa _rename_:

	Schema::rename($from, $to);

Puoi specificare, se necessario, quale connessione usare per ogni singola operazione tramite il metodo _Schema::connection_.

	Schema::connection('foo')->create('users', function($table)
	{
		$table->increments('id');
	});

Per eliminare una tabella, invece, usa il metodo `Schema::drop`:

	Schema::drop('users');

	Schema::dropIfExists('users');

<a name="aggiunta-colonne"></a>
## Aggiunta di Colonne

Per aggiornare una tabella esistente puoi usare invece il metodo _Schema::table_.

	Schema::table('users', function($table)
	{
		$table->string('email');
	});

Il table builder contiene una nutrita schiera di metodi che puoi usare per costruire le tue tabelle.

Command  | Description
------------- | -------------
`$table->bigIncrements('id');`  |  ID autoincrementante, usando un equivalente di "big integer".
`$table->bigInteger('votes');`  |  BIGINT o equivalente
`$table->binary('data');`  |  BLOB o equivalente
`$table->boolean('confirmed');`  |  BOOLEAN o equivalente
`$table->char('name', 4);`  |  CHAR o equivalente, con lunghezza specificata
`$table->date('created_at');`  |  DATE o equivalente
`$table->dateTime('created_at');`  |  DATETIME o equivalente
`$table->decimal('amount', 5, 2);`  |  DECIMAL o equivalente con precisione e scala
`$table->double('column', 15, 8);`  |  DOUBLE o equivalente con precisione di 15 cifre, di cui 8 dopo il punto decimale
`$table->enum('choices', array('foo', 'bar'));` | ENUM o equivalente
`$table->float('amount');`  |  FLOAT o equivalente
`$table->increments('id');`  |  ID intero autoincrementante, usando INT o equivalente.
`$table->integer('votes');`  |  INTEGER o equivalente
`$table->json('options');`  |  JSON o equivalente
`$table->longText('description');`  |  LONGTEXT o equivalente
`$table->mediumInteger('numbers');`  |  MEDIUMINT o equivalente
`$table->mediumText('description');`  |  MEDIUMTEXT o equivalente
`$table->morphs('taggable');`  |  Aggiunge un INTEGER `taggable_id` e una STRING `taggable_type`
`$table->nullableTimestamps();`  |  Come `timestamps()`, ma permette il NULL
`$table->smallInteger('votes');`  |  SMALLINT o equivalente
`$table->tinyInteger('numbers');`  |  TINYINT o equivalente
`$table->softDeletes();`  |  Aggiunge **deleted\_at** per le soft delete
`$table->string('email');`  |  VARCHAR o equivalente
`$table->string('name', 100);`  |  VARCHAR o equivalente, con lunghezza definita
`$table->text('description');`  |  TEXT o equivalente
`$table->time('sunrise');`  |  TIME o equivalente
`$table->timestamp('added_on');`  |  TIMESTAMP o equivalente
`$table->timestamps();`  |  Aggiunge **created\_at** ed **updated\_at**
`$table->rememberToken();`  |  Aggiunge `remember_token` come VARCHAR(100) NULL
`->nullable()`  |  Specifica che la colonna data permetterà l'uso di NULL
`->default($value)`  |  Specifica un valore di default per la colonna
`->unsigned()`  |  Imposta un INTEGER come UNSIGNED

#### Uso di After su MySQL

Se stai usando MySQL, puoi decidere di creare un certo campo _dopo_ uno già esistente:

	$table->string('name')->after('email');

<a name="modifica-colonne"></a>
## Modifica delle Colonne

A volte potrebbe verificarsi la necessità di modificare una colonna già esistente. Ad esempio, potresti voler incrementare la grandezza di un certo campo. Il metodo _change_ serve proprio allo scopo! Proviamo ad incrementare la grandezza di _name_ da 20 a 50.

	Schema::table('users', function($table)
	{
		$table->string('name', 50)->change();
	});

Potremmo inoltre modificare una colonna facendo in modo che, da questo momento in poi, possa accettare anche il NULL.

	Schema::table('users', function($table)
	{
		$table->string('name', 50)->nullable()->change();
	});

<a name="rinominare-colonna"></a>
## Rinominare una Colonna

Per rinominare una colonna usa il metodo _renameColumn_ dello Schema Builder. Prima di cambiare il nome di una colonna assicurati però di aggiungere la dipendenza _doctrine/dbal_ al tuo file _composer.json_.

	Schema::table('users', function($table)
	{
		$table->renameColumn('from', 'to');
	});

> **Nota:** Il cambio di nome per un campo `enum` non è supportato al momento.

<a name="cancellare-colonna"></a>
## Cancellare una Colonna

Per cancellare una colonna usa il metodo _dropColumn_.

To drop a column, you may use the `dropColumn` method on the Schema builder. Assicurati però di aggiungere la dipendenza _doctrine/dbal_ al tuo file _composer.json_.

#### Cancellare una Colonna

	Schema::table('users', function($table)
	{
		$table->dropColumn('votes');
	});

#### Cancellare più Colonne Insieme

	Schema::table('users', function($table)
	{
		$table->dropColumn(array('votes', 'avatar', 'location'));
	});

<a name="controlli-esistenza"></a>
## Controlli di Esistenza

#### Controllare l'Esistenza di una Tabella

Puoi controllare l'esistenza di una tabella o di una specifica colonna tramite i due metodi _hasTable_ ed _hasColumn_.

	if (Schema::hasTable('users'))
	{
		//
	}

#### Controlla l'Esistenza di una Colonna

	if (Schema::hasColumn('users', 'email'))
	{
		//
	}

<a name="aggiunta-indici"></a>
## Aggiunta di Indici

Lo Schema Builder di Laravel supporta svariati tipi di indice. Ci sono due modi per crearli: puoi specificarne durante la creazione di una colonna specifica, o puoi aggiungerne separatamente in un secondo momento.

Quindi, così:

	$table->string('email')->unique();

oppure così.

Comando  | Descrizione
------------- | -------------
`$table->primary('id');`  |  Aggiunge una chiave primaria
`$table->primary(array('first', 'last'));`  |  Aggiunge una chiave composta
`$table->unique('email');`  |  Aggiunge un indice unico
`$table->index('state');`  |  Aggiunge un indice

<a name="chiavi-esterne"></a>
## Chiavi Esterne

Laravel ovviamente supporta anche la possibilità di aggiungere chiavi esterne e constraint alle tue tabelle.

	$table->integer('user_id')->unsigned();
	$table->foreign('user_id')->references('id')->on('users');

In questo esempio stiamo specificando che la colonna _user_id_ si riferisce alla colonna _id_ sulla tabella _user_. Ricorda che bisogna sempre creare prima la chiave esterna!

Puoi anche specificare delle opzioni per le condizioni di "on delete" o "on update".

	$table->foreign('user_id')
          ->references('id')->on('users')
          ->onDelete('cascade');

Per cancellare una chiave esterna usa il metodo _dropForeign_. La naming convention da usare è quella che vedi di seguito:

	$table->dropForeign('posts_user_id_foreign');

> **Nota:** Quando crei una chiave esterna che fa riferimento ad un intero autoincrementante, specifica sempre che tale colonna è anche _unsigned_.

<a name="cancellare-indici"></a>
## Cancellare gli Indici

Per cancellare un indice devi specificarne il nome. Laravel usa una sua convenzione per l'assegnazione dei nomi di default. Semplicemente, concatena il nome della tabella e della colonna nell'indice, quindi il tipo di indice.

Ecco qualche esempio:

Comando  | Descrizione
------------- | -------------
`$table->dropPrimary('users_id_primary');`  |  Cancella la chiave primaria dalla tabella _users_
`$table->dropUnique('users_email_unique');`  |  Cancella la chiave unica dalla tabella _users_
`$table->dropIndex('geo_state_index');`  |  Cancella l'indice dalla tabella _geo_

<a name="cancellazione-timestamp"></a>
## Cancellazione Timestamp e Soft Delete

Per cancellare le colonne di tipo `timestamps`, `nullableTimestamps` o `softDeletes` puoi usare i seguenti metodi.

Comando  | Descrizione
------------- | -------------
`$table->dropTimestamps();`  |  Cancella **created\_at** ed **updated\_at** dalla tabella
`$table->dropSoftDeletes();`  |  Cancella **deleted\_at** dalla tabella

<a name="motori-storage"></a>
## Motori di Storage

Per decidere quale motore usare per una certa tabella, specificane la proprietà _engine_.

    Schema::create('users', function($table)
    {
        $table->engine = 'InnoDB';

        $table->string('email');
    });
