# Redis

- [Introduzione](#introduzione)
	- [Configurazione](#configurazione)
- [Uso Base](#uso-base)
	- [Pipelining dei Comandi](#pipelining-comandi)
- [Pub / Sub](#pubsub)

<a name="introduzione"></a>
## Introduzione

[Redis](http://redis.io) è un sistema di storage piuttosto avanzato che lavora sul principio chiave-valore. Può essere considerato un data structure server, visto che una chiave può contenere una [stringa](http://redis.io/topics/data-types#strings), un [hash](http://redis.io/topics/data-types#hashes), una [lista](http://redis.io/topics/data-types#lists), un [set](http://redis.io/topics/data-types#sets), ed un [sorted set](http://redis.io/topics/data-types#sorted-sets). 

Prima di usare Redis con Laravel, comunque, assicurati di aver installato il package `predis/predis` (~1.0) via Composer.

<a name="configurazione"></a>
### Configurazione

Per configurare la tua applicazione in modo tale da farle usare Redis, aggiungi i dati relativi alla connessione in _config/database.php_. Nel file avrai già notato, probabilmente, un array _redis_ contenente i vari dati di configurazione.

    'redis' => [

        'cluster' => false,

        'default' => [
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'database' => 0,
        ],

    ],

Per scopi di sviluppo locali, la configurazione già esistente dovrebbe essere sufficiente, o comunque coprire buona parte dei casi. Ad ogni modo, sentiti libero di modificare le opzioni come meglio credi.

L'opzione _cluster_ serve ad indicare al client Redis di effettuare lo sharding client-side sui vari nodi, in modo tale da creare un pool e risparmiare una significativa quantità di RAM. Tuttavia, ricorda che lo sharding client-side non gestisce il failover. Viene usato spesso per i dati in cache disponibili da altri primary data store.

Se il tuo server Redis richiede l'autenticazione, puoi specificare la password aggiungendo un elemento _password_ all'array nel file di configurazione.

> **Nota:** se hai installato l'estensione Redis tramite PECL, dovrai rinominare l'alias per Redis nel file `config/app.php`.

<a name="uso-base"></a>
## Uso Base

Puoi interagire con Redis richiamando i vari metodi messi a disposizione sulla [facade](/docs/5.1/facade). Puoi richiamare tutti i <a href="http://redis.io/commands" target="_blank">comandi disponibili</a> tramite dynamic method. Questi verranno passati direttamente al server. Ad esempio, proviamo a chiamare il comando GET usando il metodo `get`:

	<?php namespace App\Http\Controllers;

	use Redis;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			$user = Redis::get('user:profile:'.$id);

			return view('user.profile', ['user' => $user]);
		}
	}

Come forse avrai già immaginato, Laravel fa uso dei magic method per passare i vari comandi al server Redis. Tutto quello che devi fare è passare gli argomenti come se stessi chiamando il comando stesso.

	Redis::set('name', 'Taylor');

	$values = Redis::lrange('names', 5, 10);

In alternativa, puoi passare i comandi al server usando il metodo _command_, che accetta il nome del comando come primo argomento, quindi un array di valori come parametri per esso.

	$values = Redis::command('lrange', [5, 10]);

#### Usare più Connessioni a Redis

Puoi ottenere un'istanza di Redis usando il metodo `Redis::connection`:

	$redis = Redis::connection();

Otterrai l'istanza relativa alla connessione di default. Tuttavia, potresti voler ottenere un'istanza per una connessione specifica. In tal caso, specifica un parametro in _connection_ che indichi quale connessione usare.

	$redis = Redis::connection('other');

<a name="pipelining-comandi"></a>
### Pipelining dei Comandi

Il pipelining viene usato quando devi inviare, al server, un insieme di comandi da eseguire in una sola operazione. Il metodo _pipeline_ accetta un argomento solo: una closure che riceve un'istanza Redis. Puoi quindi definire tutti i comandi che vuoi: verranno tutti eseguiti in un'unica operazione.

	Redis::pipeline(function ($pipe) {
		for ($i = 0; $i < 1000; $i++) {
			$pipe->set("key:$i", $i);
		}
	});

<a name="pubsub"></a>
## Pub / Sub

Laravel fornisce un'interfaccia piuttosto comoda ai comandi _publish_ e _subscribe_ di Redis. Questi comandi ti permettono di rimanere in ascolto per dei messaggi su specifici "canali". Puoi pubblicare tali messaggi anche da altre applicazioni, usando anche altri linguaggi, ed il risultato è una comunicazione comoda e funzionale tra processi vari ed eventuali.

Innanzitutto, configuriamo un listener su un canale via Redis, usando il metodo _subscribe_. Piazzeremo questa chiamata in un [comando Artisan](/docs/5.1/artisan), visto che stiamo iniziando un processo long-running.

	<?php namespace App\Console\Commands;

	use Redis;
	use Illuminate\Console\Command;

	class RedisSubscribe extends Command
	{
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

	    /**
	     * The console command description.
	     *
	     * @var string
	     */
	    protected $description = 'Subscribe to a Redis channel';

	    /**
	     * Execute the console command.
	     *
	     * @return mixed
	     */
	    public function handle()
	    {
			Redis::subscribe(['test-channel'], function($message) {
				echo $message;
			});
	    }
	}

Da questo momento in poi possiamo pubblicare dei messaggi sul canale usando il metodo _publish_.

	Route::get('publish', function () {
		// Route logic...

		Redis::publish('test-channel', json_encode(['foo' => 'bar']));
	});

#### Iscrizioni con Wildcard

Usando il metodo `psubscribe` è possibile iscriversi ad un canale con wildcard, che è molto utile per il catch di tutti i messaggi su tutti i canali. Il nome del canale _$channel_ verrà passato come secondo argomento della Closure.

	Redis::psubscribe(['*'], function($message, $channel) {
		echo $message;
	});

	Redis::psubscribe(['users.*'], function($message, $channel) {
		echo $message;
	});
