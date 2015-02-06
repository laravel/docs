# Redis

- [Introduzione](#introduzione)
- [Configurazione](#configurazione)
- [Uso](#uso)
- [Pipelining](#pipelining)

<a name="introduzione"></a>
## Introduzione

[Redis](http://redis.io) è un sistema di memorizzazione di dati chiave-valore, open source. Spesso viene definito come data structure server dato che ogni chiave può corrispondere ad una [stringa](http://redis.io/topics/data-types#strings), [hash](http://redis.io/topics/data-types#hashes), [lista](http://redis.io/topics/data-types#lists), [set](http://redis.io/topics/data-types#sets) o [set ordinato](http://redis.io/topics/data-types#sorted-sets).

Prima di usare Redis con Laravel, assicurati di aggiungere il package `predis/predis` (~1.0) con Composer.

> **Nota:** se hai installato l'estensione PHP Redis tramite PECL, dovrai rinominare l'alias per Redis in `config/app.php`.

<a name="configurazione"></a>
## Configurazione

Tutto quello che riguarda la configurazione di Redis per la tua applicazione può essere trovato in `config/database.php`. In questo file infatti puoi vedere un array `redis` contenente delle impostazioni di default:

	'redis' => [

		'cluster' => true,

		'default' => ['host' => '127.0.0.1', 'port' => 6379],

	],

Per semplici scopo di sviluppo, come configurazione dovrebbe essere più che sufficiente. Ad ogni modo sentiti libero di modificare tutto come meglio credi in base al tuo ambiente di sviluppo. Dai ad ogni server un nome e specifica host e porta da usare.

L'opzione _cluster_ serve a spiegare al client Redis di Laravel di effettuare lo sharding client-side sui vari nodi, in modo tale da migliorare le performance attraverso la creazione di maggiore zone libere nella RAM. Tuttavia, il client-side sharding ha i suoi pro e i contro, quindi adatta tutto alle tue necessità dopo aver analizzato la situazione.

Se il tuo server Redis ha bisogno di autenticazione, puoi fornire una password aggiungendo un elemento all'array che dalla chiave _password_.

<a name="uso"></a>
## Uso

Puoi ottenere un'istanza di Redis usando il metodo `Redis::connection`:

	$redis = Redis::connection();

Se non stai usando il Clustering, puoi decidere di richiamare un server specifico.

	$redis = Redis::connection('other');

Una volta ottenuta l'istanza del client puoi lavorarci come meglio credi attraverso i vari [comandi](http://redis.io/commands). Laravel, nello specifico, usa dei magic method per il passaggio dei comandi al server Redis.

	$redis->set('name', 'Taylor');

	$name = $redis->get('name');

	$values = $redis->lrange('names', 5, 10);

I parametri per ogni comando vengono passati direttamente tramite il metodo. Ovviamente, non c'è bisogno di usare necessariamente i magic method: c'è il metodo _command_ da usare se lo ritieni opportuno.

	$values = $redis->command('lrange', array(5, 10));

Inoltre, se stai eseguendo dei metodi sulla connessione di defaul, nulla ti vieta di usare i magic method statici sulla classe _Redis_ direttamente.

	Redis::set('name', 'Taylor');

	$name = Redis::get('name');

	$values = Redis::lrange('names', 5, 10);

> **Nota:** Dei driver Redis per la [cache](/cache) e le [sessioni](/sessioni) sono inclusi con Laravel, se dovessi averne bisogno.

<a name="pipelining"></a>
## Pipelining

Il pipelining è una tecnica che dovresti prendere in considerazione nel caso in cui ti trovassi a dover mandare un sacco di comandi al server in una sola volta.

Per usarla basta il comando _pipeline_:

#### Piping di più Comandi Verso il Server

	Redis::pipeline(function($pipe)
	{
		for ($i = 0; $i < 1000; $i++)
		{
			$pipe->set("key:$i", $i);
		}
	});
