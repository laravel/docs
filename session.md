# Sessione

- [Configurazione](#configurazione)
- [Usare La Sessione](#usare-la-sessione)
- [Flash Data](#flash-data)
- [Sessione Su Database](#sessione-su-database)
- [Driver Sessione](#driver-sessione)

<a name="configurazione"></a>
## Configurazione

Visto che il protocollo HTTP è stateless, le sessioni forniscono un modo per conservare le informazioni attraverso le varie richieste dell'utente. Laravel fornisce una varietà di API per la gestione delle sessioni. Il supporto a [Memcached](http://memcached.org), [Redis](http://redis.io), e per il database sono già pronti all'uso.

La configurazione per la sessione è salvata in `config/session.php`. Assicurati di leggere bene tutte le opzioni che hai a disposizione per configurare al meglio questo file. Di dafault, Laravel è configurata per utilizzare le sessioni tramite il driver `file` che è sufficiente per la maggior parte delle applicazioni.

Prima di utilizzare Redis per la gestione delle sessioni, è necessario installare un pacchetto aggiuntivo, ovvero `predis/predis` (~1.0) via Composer.

> **Nota:** Se hai bisogno di criptare le sessioni salvate assicurati di impostare nella configurazione il parametro `encrypt` su`true`.

#### Chiavi Riservate

Laravel utilizza per le sessioni interne la chiave `flash`, quindi non dovresti mai utilizzarla come chiave nelle tue sessioni.

<a name="usare-la-sessione"></a>
## Usare La Sessione

#### Salvare Un Valore Nella Sessione

	Session::put('key', 'value');

#### Inserire Un Valore In Un Array In Sessione

	Session::push('user.teams', 'developers');

#### Recuperare Un Valore Dalla Sessione

	$value = Session::get('key');

#### Recuperare Un Valore O Restituire Un Valore Di Default

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

#### Recuperare Un Valore Ed Eliminarlo Dalla Sessione

	$value = Session::pull('key', 'default');

#### Recuperare Tutti I Dati Dalla Sessione

	$data = Session::all();

#### Controllare Se Un Valore Esiste Nella Sessione

	if (Session::has('users'))
	{
		//
	}

#### Rimuovere Un Valore Dalla Sessione

	Session::forget('key');

#### Rimuovere Tutti I Valori Dalla Sessione

	Session::flush();

#### Rigenerare L'ID Della Sessione

	Session::regenerate();

<a name="flash-data"></a>
## Flash Data

Qualche volta potrsti aver bisogno di salvare dei valori nella sessione solo per la richiesta successiva. Puoi farlo utilizzando il metodo `Session::flash`:

	Session::flash('key', 'value');

#### Riutilizzare Gli Stessi Dati Flash Per Un'Altra Richiesta

	Session::reflash();

#### Riutilizzare Solo Una Parte dei Flash Data

	Session::keep(array('username', 'email'));

<a name="sessione-su-database"></a>
## Sessione Su Database

Quando utilizzi il driver `database` per le sessioni, dovrai creare una tabella che conterrà i dati. Qui sotto c'è un esempio per la creazione della tabella utilizzando `Schema`:

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

Ovviamente puoi utilizzare anche il comando Artisan `session:table` che si occuperà di generare la migration per te!

	php artisan session:table

	composer dump-autoload

	php artisan migrate

<a name="driver-sessione"></a>
## Driver Sessione

Il "driver" della sessione definisce dove i dati devono essere salvati per ogni richiesta. Laravel possiede diversi ottimi driver già pronti all'uso:

- `file` - le sessioni saranno salvate in `app/storage/sessions`.
- `cookie` - le sessioni saranno salvate in modo sicuto in cookie criptati.
- `database` - le sessioni saranno salvate nel database utilizzato dalla tua applicazione.
- `memcached` / `redis` - le sessioni saranno salvate in uno di questi velocissimi storage.
- `array` - le sessioni saranno salvate in un semplice array PHP ma non saranno persistenti.

> **Nota:** Il driver array solitamente viene utilizzato per gli [unit test](/docs/master/testing), in questo modo non verranno salvate sessioni.
