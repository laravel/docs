# Database: Migration

- [Introduzione](#introduzione)
- [Generare una Migration](#generare-migration)
- [Struttura di una Migration](#struttura-migration)
- [Eseguire una Migration](#eseguire-migration)
	- [Rollback di una Migration](#rollback-migration)
- [Scrivere una Migration](#scrivere-migration)
	- [Creare le Tabelle](#creare-tabelle)
	- [Rinominare / Cancellare una Tabella](#rinominare-cancellare-tabella)
	- [Aggiungere le Colonne](#aggiungere-colonne)
	- [Modificare le Colonne](#modificare-colonne)
	- [Cancellare le Colonne](#eliminare-colonne)
	- [Creare gli Indici](#creare-indici)
	- [Cancellare gli Indici](#cancellare-indici)
	- [Chiavi Esterne](#chiavi-esterne)

<a name="introduzione"></a>
## Introduzione

Potremmo definire le migration come una sorta di sistema di controllo di versione per il tuo database. In modo piuttosto agevole, infatti, un team potrà modificare e condividere lo schema del database. Usando Laravel, molto probabilmente userai spesso il sistema di Migration con lo Schema Builder. 

La facade `Schema` offre una serie di funzionalità dedicate allo scopo, agnostiche rispetto al database. Di conseguenza, con lo stesso set di metodi costruirai il tuo schema senza cambiare il tuo codice di una sola virgola se, al posto di MySQL, un giorno ti stanchi ci metti SQL Server. O qualsiasi altro database system per il quale riesci a trovare un driver. Comodo, no?

<a name="generare-migration"></a>
## Generare una Migration

Per generare una migration, usa il [comando Artisan](/documentazione/5.1/artisan) `make:migration`:

	php artisan make:migration create_users_table

La nuova migration verrà messa in `database/migrations`. Ogni file generato avrà un nome contenente un timestamp, che permette a Laravel di ordinarle cronologicamente.

Le opzioni _--table_ e _--create_ consentono di indicare il nome di una tabella e se tale migration sta creando una nuova tabella nello schema. In questo modo, nella migration risultante, verranno aggiunte delle istruzioni di comodo in modo tale da poter raggiungere il proprio obiettivo ancora più velocemente.

	php artisan make:migration add_votes_to_users_table --table=users
	php artisan make:migration create_users_table --create=users

<a name="struttura-migration"></a>
## Struttura di una Migration

Una classe migration contiene normalmente due metodi: `up` e `down`. Il loro scopo è complementare: _up_ infatti viene eseguito quando viene eseguita la migration stessa. Il metodo _down_, al contrario, viene eseguito quando effettui il _rollback_, ovvero quando vuoi annullare quello che il metodo _up_ ha fatto.

Grazie a questo sistema, tornare ad una versione precedente del tuo database è semplicissimo!

In entrambi i metodi potrai usare lo _Schema Builder_ senza problemi, per creare e modificare in modo espressivo le tue tabelle. Per saperne di più a riguardo, [controlla la parte dedicata della documentazione](#creare-tabelle). Ecco, in questo esempio, una migration che crea una tabella _flights_.

	<?php

	use Illuminate\Database\Schema\Blueprint;
	use Illuminate\Database\Migrations\Migration;

	class CreateFlightsTable extends Migration
	{
	    /**
	     * Run the migrations.
	     *
	     * @return void
	     */
	    public function up()
	    {
	        Schema::create('flights', function (Blueprint $table) {
	            $table->increments('id');
	            $table->string('name');
	            $table->string('airline');
	            $table->timestamps();
	        });
	    }

	    /**
	     * Reverse the migrations.
	     *
	     * @return void
	     */
	    public function down()
	    {
	        Schema::drop('flights');
	    }
	}


<a name="eseguire-migration"></a>
## Eseguire una Migration

Per eseguire tutte le migration della tua applicazione, usa il comando Artisan _migrate_.

	php artisan migrate

> **Nota** se ricevi un errore di tipo "class not found", prova ad eseguire il comando _composer dump-autoload_, quindi riavvia il comando _php artisan migrate_.

#### Forzare l'Esecuzione di una Migration

Alcune operazioni effettuate durante l'esecuzione di una migration possono essere distruttive e portarti a perdere dei dati. Come protezione da qualcosa del genere, se sei in produzione ti verrà chiesta una conferma prima di eseguire qualsiasi migration. Nel caso in cui tu voglia forzare l'esecuzione senza ulteriori conferme, usa il flag _--force_.

	php artisan migrate --force

<a name="rollback-migration"></a>
### Rollback di una Migration

Tramite l'operazione di rollback è possibile tornare indietro, allo stato del database prima di una certa migration. Il comando _rollback_ rende possibile tutto ciò.

	php artisan migrate:rollback

> Attenzione: l'operazione di rollback annulla l'effetto dell'ultimo "batch" di migration. 

Per farti capire meglio, facciamo un esempio. Immagina di avere tre migration. Esegui il comando _migrate_ e le modifiche vengono fisicamente effettuate. Successivamente hai bisogno di fare altre modifiche, che vai a sistemare in altri due file appositamente creati. 

Esegui di nuovo _migrate_: i batch in totale sono due. Il primo, comprendente i primi tre file, ed il secondo con gli altri due successivi.

Se in questo specifico momento esegui _migrate:rollback_, verranno annullate le modifiche solo dell'ultimo batch, cioè degli ultimi due file di migration.

Tornando a noi, il comando `migrate:reset` invece farà tabula rasa di tutto quello che il sistema di migration ha svolto sul tuo database.

	php artisan migrate:reset

#### Rollback / Migrate in un Singolo Comando

A volte potresti avere la necessità di effettuare un rollback e subito dopo reinstallare tutto. In questo caso, il comando _migrate:refresh_ fa al caso tuo.

	php artisan migrate:refresh

	php artisan migrate:refresh --seed

<a name="scrivere-migration"></a>
## Scrivere una Migration

<a name="creare-tabelle"></a>
### Creare le Tabelle

Per creare una nuova tabella, usa il metodo _create_ dello Schema Builder (la facade _Schema_). Tale metodo accetta due argomenti: il primo è il nome della tabella, il secondo una _Closure_ che riceve un oggetto _Blueprint_ dal quale definirai tutti i dettagli della nuova tabella.

	Schema::create('users', function ($table) {
		$table->increments('id');
	});

Ovviamente, in fase di creazione della tabella puoi usare tutti i metodi dedicati alla [creazione delle colonne](#aggiungere-colonne).

#### Controllare l'Esistenza di una Tabella o di una Colonna

Puoi controllare facilmente l'esistenza di una tabella o di una colonna usando i metodi _hasTable_ o _hasColumn_.

	if (Schema::hasTable('users')) {
		//
	}

	if (Schema::hasColumn('users', 'email')) {
		//
	}

#### Connessione e Motore di Storage

Se vuoi effettuare una certa operazione su una specifica connessione, usa il metodo _connection_ prima di _create_.

	Schema::connection('foo')->create('users', function ($table) {
		$table->increments('id');
	});

Inoltre, usa la proprietà _engine_ dell'oggetto _$table_ per definire il motore di storage da usare.

	Schema::create('users', function ($table) {
		$table->engine = 'InnoDB';

		$table->increments('id');
	});

<a name="rinominare-cancellare-tabella"></a>
### Rinominare / Cancellare una Tabella

Puoi rinominare una tabella usando _rename_:

	Schema::rename($from, $to);

Per cancellarla, invece, puoi usare _drop_ oppure _dropIfExists_ che, come il nome suggerisce, cancella la tabella solo se esiste. In caso contrario, non verrà sollevato alcun errore, a differenza di _drop_.

	Schema::drop('users');

	Schema::dropIfExists('users');

<a name="aggiungere-colonne"></a>
### Aggiungere le Colonne

Puoi aggiornare una tabella esistente usando il metodo _table_ della facade _Schema_ esattamente come _create_, _table_ accetta due parametri: il nome della tabella e la _Closure_ che accetta un oggetto di tipo _Blueprint_ da usare per modificare la struttura della tabella.

Vediamo adesso i metodi da usare per *aggiungere* nuove colonne ad una tabella, sia in fase di creazione che di modifica.

	Schema::table('users', function ($table) {
		$table->string('email');
	});

#### Tipologie di Colonne

Lo schema builder contiene una serie di metodi che puoi usare per aggiungere colonne di vario genere.

* `$table->bigIncrements('id');`  |  ID autoincrementante usando un "big integer" o equivalente.
* `$table->bigInteger('votes');`  |  BIGINT o l'equivalente per il database system scelto.
* `$table->binary('data');`  |  BLOB o l'equivalente per il database system scelto.
* `$table->boolean('confirmed');`  |  BOOLEAN o l'equivalente per il database system scelto.
* `$table->char('name', 4);`  |  CHAR o equivalente, con lunghezza definita.
* `$table->date('created_at');`  |  DATE o l'equivalente per il database system scelto.
* `$table->dateTime('created_at');`  |  DATETIME o l'equivalente per il database system scelto.
* `$table->decimal('amount', 5, 2);`  |  DECIMAL o equivalente, con precisione e scala.
* `$table->double('column', 15, 8);`  |  DOUBLE o equivalente, con 15 cifre in totale di cui 8 dopo la virgola.
* `$table->enum('choices', ['foo', 'bar']);` | ENUM o l'equivalente per il database system scelto.
* `$table->float('amount');`  |  FLOAT o l'equivalente per il database system scelto.
* `$table->increments('id');`  |  ID autoincrementante (chiave primaria).
* `$table->integer('votes');`  |  INTEGER o l'equivalente per il database system scelto.
* `$table->json('options');`  |  JSON o l'equivalente per il database system scelto.
* `$table->jsonb('options');`  |  JSONB o l'equivalente per il database system scelto.
* `$table->longText('description');`  |  LONGTEXT o l'equivalente per il database system scelto.
* `$table->mediumInteger('numbers');`  |  MEDIUMINT o l'equivalente per il database system scelto.
* `$table->mediumText('description');`  |  MEDIUMTEXT o l'equivalente per il database system scelto.
* `$table->morphs('taggable');`  |  Aggiunge due campi, un INTEGER `taggable_id` e una STRING `taggable_type`.
* `$table->nullableTimestamps();`  |  Come `timestamps()`, però ammette anche NULL come valore.
* `$table->rememberToken();`  |  Aggiunge `remember_token` come VARCHAR(100) NULL.
* `$table->smallInteger('votes');`  |  SMALLINT o l'equivalente per il database system scelto.
* `$table->softDeletes();`  |  Aggiunge `deleted_at` per la funzionalità di soft delete.
* `$table->string('email');`  |  VARCHAR o equivalente.
* `$table->string('name', 100);`  |  VARCHAR o equivalente, con lunghezza specificata.
* `$table->text('description');`  |  TEXT o l'equivalente per il database system scelto.
* `$table->time('sunrise');`  |  TIME o l'equivalente per il database system scelto.
* `$table->tinyInteger('numbers');`  |  TINYINT o l'equivalente per il database system scelto.
* `$table->timestamp('added_on');`  |  TIMESTAMP o l'equivalente per il database system scelto.
* `$table->timestamps();`  |  Aggiunge le colonne `created_at` ed `updated_at`.

#### Modificatori per le Colonne

In aggiunta ai tipi di colonne appena visti, ci sono svariati modificatori che puoi usare in fase di creazione di nuove colonne. Ad esempio, per rendere una colonna aperta al valore NULL, puoi usare _nullable_ così:

	Schema::table('users', function ($table) {
		$table->string('email')->nullable();
	});

Ecco di seguito una serie di modificatori:

* `->after('column')`  |  Pone una colonna "dopo" un'altra (vale solo per MySQL)
* `->nullable()`  |  Permette ad una colonna di assumere il valore NULL;
* `->default($value)`  |  Specifica un valore di "default" per la colonna;
* `->unsigned()`  |  Imposta una colonna `integer` come `UNSIGNED`

<a name="modificare-colonne"></a>
### Modificare le Colonne

#### Prerequisiti

Prima di modificare le colonne, assicurati di aver installato la dipendenza _doctrine/dbal_ inserendola nel file _composer.json_. Tale libreria è infatti indispensabile per poter determinare lo stato attuale di una colonna e creare la query SQL necessaria alla sua modifica.

#### Aggiornare gli Attributi di una Colonna

Il metodo _change_ ti permette di modificare una colonna esistente assegnandole un nuovo tipo, o modificandone gli attributi. Nel seguente esempio stiamo aumentando la lunghezza della colonna _name_ fino a 50 caratteri.

	Schema::table('users', function ($table) {
		$table->string('name', 50)->change();
	});

Possiamo anche assegnare alla colonna un modificatore come _nullable_.

	Schema::table('users', function ($table) {
		$table->string('name', 50)->nullable()->change();
	});

#### Rinominare le Colonne

Per rinominare le colonne basta usare il metodo _renameColumn_ come segue.

	Schema::table('users', function ($table) {
		$table->renameColumn('from', 'to');
	});

> **Nota:** al momento non è supportata l'operazione di cambio del nome di una colonna di tipo _enum_.

<a name="eliminare-colonne"></a>
### Cancellare le Colonne

Per cancellare una colonna usa il metodo _dropColumn_ dello Schema Builder:

	Schema::table('users', function ($table) {
		$table->dropColumn('votes');
	});

Puoi anche cancellarne più di una alla volta, passando un array di stringhe al posto di una singola.

	Schema::table('users', function ($table) {
		$table->dropColumn(['votes', 'avatar', 'location']);
	});

<a name="creare-indici"></a>
### Creare gli Indici

Lo Schema Builder supporta, ovviamente, anche la creazione e modifica di svariati tipi di indici. Iniziamo da un semplice esempio: un indice che specifica che il valore di una colonna dovrebbe essere sempre unico.

	$table->string('email')->unique();

In alternativa, puoi creare l'indice anche dopo la creazione della colonna, in un secondo momento.

	$table->unique('email');

Puoi anche passare un array di colonne in modo tale da creare un indice composto.

	$table->index(['account_id', 'created_at']);

#### Tipologie di Indici

* `$table->primary('id');`  |  Aggiunge una chiave primaria.
* `$table->primary(['first', 'last']);`  |  Aggiunge un indice composto.
* `$table->unique('email');`  |  Aggiunge un indice unico.
* `$table->index('state');`  |  Aggiunge un indice base.

<a name="cancellare-indici"></a>
### Cancellare gli Indici

Per cancellare un indice devi fondamentalmente specificare il nome dell'indice in un metodo apposito, con una nomenclatura apposita. Ecco alcuni esempi:

* `$table->dropPrimary('users_id_primary');`  |  Cancella una chiave primaria dalla tabella "users".
* `$table->dropUnique('users_email_unique');`  |  Cancella un indice unico dalla tabella "users".
* `$table->dropIndex('geo_state_index');`  |  Cancella un indice base dalla tabella "geo".

Come puoi notare, la nomenclatura segue questo standard:

	nome-tabella_nome-campo_tipo-indice

<a name="chiavi-esterne"></a>
### Chiavi Esterne

Laravel supporta anche la creazione di chiavi esterne, tipicamente usate per assicurarsi un'integretà referenziale a livello di database. Ad esempio, definiamo una colonna *user_id* per la tabella _posts_ che fa riferimento alla colonna _id_ sulla tabella _users_.

	Schema::table('posts', function ($table) {
		$table->integer('user_id')->unsigned();

		$table->foreign('user_id')->references('id')->on('users');
	});

Puoi anche specificare una specifica azione per l'on delete e l'on update, se necessario.

	$table->foreign('user_id')
          ->references('id')->on('users')
          ->onDelete('cascade');

Per cancellare una chiave esterna, puoi usare il metodo _dropForeign_. Le chiavi esterne usano la stessa regola di nomenclatura degli indici. Di conseguenza, tutto quello che dovrai specificare nel metodo sarà un nome nel formato

To drop a foreign key, you may use the `dropForeign` method. Foreign key constraints use the same naming convention as indexes. So, we will concatenate the table name and the columns in the constraint then suffix the name with "_foreign":

	nome-tabella_nome-campo_foreign

... ad esempio così:

	$table->dropForeign('posts_user_id_foreign');
