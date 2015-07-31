# Database: Primi Passi

- [Introduzione](#introduzione)
	- [Configurazione](#configurazione)
- [Eseguire le Query](#eseguire-query)
	- ["Ascoltare" gli Eventi Relativi alle Query](#ascoltare-eventi-query)
- [Transazioni sul Database](#transazioni-database)
- [Usare una Connessione Specifica](#usare-connessione-specifica)

<a name="introduzione"></a>
## Introduzione

Laravel rende semplice la connessione di un database (e successiva esecuzione delle query) attraverso una serie di strumenti, dal SQL grezzo fino ad [Eloquent ORM](/docs/5.1/eloquent), passando per il [query builder](/docs/5.1/database-query-builder).

Di default, Laravel supporta out of the box quattro sistemi di database diversi.

- MySQL
- Postgres
- SQLite
- SQL Server

<a name="configurazione"></a>
### Configurazione

Il file di configurazione relativo alla connessione verso il database è `config/database.php`. Al suo interno potrai definire tutte le connessioni di cui ahi bisogno, oltre a poter specificare quale usare di default. Per comodità, è stato riportato un esempio di connessione per ogni sistema supportato.

Di default, il file di esempio di [configurazione](/docs/5.1/installazione#configurazione-ambiente) è già pronto per essere usato con il database presente su [Laravel Homestead](/docs/5.1/homestead), una macchina virtuale comodissima per lo sviluppo in locale. Chiaramente, sentiti libero di modificare come meglio credi tale file.

#### Connessioni di Scrittura / Lettura

A volte, potresti avere la necessità di usare una certa connessione per le operazioni di lettura, un'altra invece per quelle di scrittura. Laravel rende il processo molto semplice, permettendoti di specificare una connessione di lettura ed una di scrittura.

Per lo scopo vengono usati gli elementi _read_ e _write_ dell'array contenente i dati di configurazione.

	'mysql' => [
		'read' => [
			'host' => '192.168.1.1',
		],
		'write' => [
			'host' => '196.168.1.2'
		],
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	],

Nei due array vanno messe le opzioni che effettivamente sono diverse tra un'operazione e l'altra (_host_ in questo caso), mentre quelle in comune vengono registrate normalmente (_database_, o _driver_). Chiaramente le cose possono cambiare di situazione in situazione: se usi dei nomi diversi per lo stesso database, ma su due server diversi, assicurati di specificare il _database_ sia in _read_ che in _write_, e così via.

<a name="eseguire-query"></a>
## Eseguire le Query

Una volta configurato il database sei pronto ad eseguire le tue prime query. Puoi farlo, comodamente, tramite la Facade _DB_. Tale classe ti fornisce svariati metodi di comodo, come _select_, _update_, _insert_ e _statement_. Vediamoli.

#### Eseguire una Query di Select

Per eseguire una query di selezione semplice usa _select_.

	<?php namespace App\Http\Controllers;

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
			$users = DB::select('select * from users where active = ?', [1]);

			return view('user.index', ['users' => $users]);
		}
	}

Il primo argomento ad essere passato al metodo è la query "grezza", mentre il secondo è un array di parametri che verranno automaticamente usati, da Laravel, per costruire la query finale. Questo tipo di binding inoltre protegge il sistema da eventuali SQL Injection.

Il metodo _select_ ritorna un _array_ di risultati. Ogni risultato all'interno dell'array sarà di tipo _StdClass_, permettendoti di accedere ai singoli campi in questo modo.

	foreach ($users as $user) {
		echo $user->name;
	}

#### Definire i Binding tramite dei Nomi

Al posto di usare _?_ per un binding, puoi assegnare ad un certo parametro un nome. Così:

	$results = DB::select('select * from users where id = :id', ['id' => 1]);

#### Eseguire una Query di Inserimento

Per eseguire una query di inserimento, usa il metodo _insert_ come segue. La sintassi è praticamente identica a quella vista in precedenza: il primo parametro è la query, il secondo l'array di parametri da passare a tale query.

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### Eseguire una Query di Aggiornamento

Il metodo _update_ viene usato per aggiornare dei record esistenti. Il numero di righe interessate da tale modifica verrà ritornato come risultato.

	$affected = DB::update('update users set votes = 100 where name = ?', ['John']);

#### Eseguire una Query di Cancellazione

Per cancellare dei record da un database, usa il metodo _delete_. Anche in questo caso verranno ritornate le righe interessate dalla modifica.

	$deleted = DB::delete('delete from users');

#### Eseguire una Query Generica

Alcune query non ritornano nessun valore. Per questo tipo di operazioni, usa _statement_.

	DB::statement('drop table users');

<a name="ascoltare-eventi-query"></a>
### "Ascoltare" gli Eventi Relativi alle Query

A volte può essere molto utile loggare le query che vengono eseguite dalla propria applicazione. A tal proposito esistono i listener, che ci permettono di rimanere in "ascolto" ogni volta che viene eseguita una query e, di conseguenza, effettuare l'operazione di cui abbiamo bisogno.

Il metodo da usare è _DB:listen_, che prende come unico parametro una _Closure_ che, a sua volta, ha come argomenti la query SQL eseguita, i binding speificati e il momento dell'esecuzione della query stessa.

Il posto migliore per tale "registrazione" può essere un [service provider](/docs/5.1/provider):

	<?php namespace App\Providers;

	use DB;
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
			DB::listen(function($sql, $bindings, $time) {
				//
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

<a name="transazioni-database"></a>
## Transazioni sul Database

Per eseguire un set di operazioni su un database, nel contesto di una specifica transazione, puoi usare il metodo _transaction_ della facade _DB_. Nel momento in cui, per qualsiasi motivo, dovesse essere lanciata un'eccezione, tutte le modifiche verrebbero annullate. In caso contrario, la transazione verrebbe confermata definitivamente. Nessun rollback manuale, per capirci!

	DB::transaction(function () {
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

#### Uso Manuale delle Transazioni

Se preferisci avere il controllo completo su tutto quello che succede in una transazione, puoi usare i metodi _beginTransaction_, per iniziare una transazione:

	DB::beginTransaction();

... `rollBack`, per effettuare il rollback delle operazioni eseguite fino ad un punto specifico:

	DB::rollBack();

... oppure _commit_, nel caso in cui sia andato tutto per il verso giusto.

	DB::commit();

> **Nota:** usando la facade DB è possibile controllare, oltre alle query più "grezze", anche quelle eseguite dal [query builder](/docs/5.1/database-query-builder) e da [Eloquent](/docs/5.1/eloquent).

<a name="usare-connessione-specifica"></a>
## Usare una Connessione Specifica

Quando usi più di una connessione nella stessa applicazione può essere comodo decidere dove usare una, e dove un'altra. Il metodo _connection_ della facade _DB_ è utile in tal senso. Tutto quello che bisogna passargli è il nome della connessione.

	$users = DB::connection('foo')->select(...);

Inoltre, se preferisci, da questo metodo puoi anche accedere all'istanza PDO sottostante tramite _getPDO_.

	$pdo = DB::connection()->getPdo();

> **Nota:** chiamando _connection_ senza nessun parametro, come nell'esempio appena visto, si usa la connessione di default.
