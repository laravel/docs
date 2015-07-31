# Filesystem / Cloud Storage

- [Introduzione](#introduzione)
- [Configurazione](#configurazione)
- [Utilizzo Base](#utilizzo-base)
	- [Ottenere Istanze Del Disco](#ottenere-istanze-del-disco)
	- [Recuperare File](#recuperare-file)
	- [Salvare File](#salvare-file)
	- [Eliminare File](#eliminare-file)
	- [Cartelle](#cartelle)
- [Filesystem Personalizzati](#filesystem-personalizzati)

<a name="introduzione"></a>
## Introduzione

Laravel fornisce un potente sistema di astrazione del filesystem grazie allo straordinario package [Flysystem](https://github.com/thephpleague/flysystem) sviluppato da Frank de Jonge. La sua integrazione con Laravel permette di utilizzare in modo semplice driver per lavorare con il filesystem locale, con Amazon S3 e con Rackspace Cloud Storage. E' molto semplice cambiare queste tipologie di storage in quanto le API da utilizzare sarano sempre le stesse.

<a name="configurazione"></a>
## Configurazione

Il file di configurazione del filesystem si trova in `config/filesystems.php`. All'interno di questo file puoi configurare tutti i tuoi "dischi". Ogni disco rappresenta un particolare driver e una particolare posizione. Nel file sono inclusi esempi di configurazione epr ognuno dei driver supportati, così ti sarà facile modificare la configurazione in base alle tue esigenze.

Puoi configurare tutti i dischi che ti servono e più dischi possono usare gli stessi driver.

#### Il Driver Locale
Quando utilizzi il driver `local` tutte le operazioni saranno relative alla cartella `root` definita nel file di configurazione. Per default il valore di questa cartella è impostato a `storage/app`. Questo esempio ti permette di salvare un file in `storage/app/file.txt`:

	Storage::disk('local')->put('file.txt', 'Contenuto');

#### Prerequisiti Per Gli Altri Driver

Prima di utilizzare i driver per S3 o Rackspace, devi installare i rispettivi package tramite Composer:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

<a name="utilizzo-base"></a>
## Utilizzo Base

<a name="ottenere-istanze-del-disco"></a>
### Ottenere Istanze Del Disco

La facade `Storage` può essere utilizzata per lavorare con qualsiasi dei dischi configurati. Per esempio puoi utilizzare il metodo `put` per salvare una immagine nel disco di default. Se richiami la facede `Storage` senza specificare un disco, il metodo utilizzerà il disco impostato come default:

	<?php namespace App\Http\Controllers;

	use Storage;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Aggiorna l'immagine di Avatar
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function updateAvatar(Request $request, $id)
		{
			$user = User::findOrFail($id);

			Storage::put(
				'avatars/'.$user->id,
				file_get_contents($request->file('avatar')->getRealPath())
			);
		}
	}

Se utilizzi diversi dischi, puoi accedervi utilizzando il metodo `disk`. In questo modo tutti i metodi successivi faranno riferimento al disco specificato.

	$disk = Storage::disk('s3');

	$contents = Storage::disk('local')->get('file.jpg')

<a name="recuperare-file"></a>
### Recuperare File

Il metodo `get` può essere utilizzato per recuperare il contenuto di un file specificato:

	$contents = Storage::get('file.jpg');

Il metodo `exists` può essere utilizzato per determinere se uno specifico file esiste sul disco indicato:

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Informazioni Meta Del File

Il metodo `size` può essere utilizzato per recuperare il peso del file in byte:

	$size = Storage::size('file1.jpg');

Il metodo `lastModified` restituisce il timestamp UNIX dell'ultima volta che il file è stato modificato:

	$time = Storage::lastModified('file1.jpg');

<a name="salvare-file"></a>
### Salvare File

Il metodo `put` può essere utilizzato per salvare un file sul un disco. Puoi anche passare una `resource` al metodo `put` per utilizzare il supporto stream dei Flysystem. L'utilizzo degli stream è consigliato quando si ha a che fare con file di grandi dimensioni:

	Storage::put('file.jpg', $contents);

	Storage::put('file.jpg', $resource);

Il metodo `copy` può essere utilizzato per spostare un file esistente in una nuova locazione del disco:

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

Il metodo `copy` può essere utilizzato per spostare un file esistente in una nuova locazione del disco:

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### Anteporre / Aggiungere Ad Un File

I metodi `prepend` e `append`ti permettono di aggiungere contenuto all'inizio o alla fine di un file:

	Storage::prepend('file.log', 'Testo da aggiungere in testa');

	Storage::append('file.log', 'Testo da aggiungere in coda');

<a name="eliminare-file"></a>
### Eliminare File

Il metodo `delete` accetta come argomento il nome del file da cancellare oppure un array contenente più nomi da eliminare:

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

<a name="cartelle"></a>
### Cartelle

#### Recupera Tutti I File Di Una Cartella

Il metodo `files` restituisce un array contenente tutti i file presenti all'interno di una specifica cartella. Se vuoi recuperare un elenco di tutti i file presenti in una cartella e nelle sue sotto-cartelle devi utilizzare il metodo `allFiles`:

	$files = Storage::files($directory);

	$files = Storage::allFiles($directory);

#### Recupera Tutte Le Cartelle Dentro Ad Una Cartella

Il metodo `directories` restituisce tutte le cartelle che sono presenti all'interno di una cartella specifica. Puoi utilizzare il metodo `allDirectories` per recuperare tutte le cartelle e le sotto-cartelle presenti in una cartella specificata:

	$directories = Storage::directories($directory);

	// Ricorsiva...
	$directories = Storage::allDirectories($directory);

#### Creare Una Cartella

Il metodo `makeDirectory` creearà una cartella, incluse eventuali sotto-cartelle:

	Storage::makeDirectory($directory);

#### Cancellare Una Cartella

Infine, puoi usare il metodo `deleteDirectory` per eliminare una cartella e tutti i file contenuti:

	Storage::deleteDirectory($directory);

<a name="filesystem-personalizzati"></a>
## Filesystem Personalizzati

L'integrazione di Laravel con Flysystem fornisce diversi "driver" senza bisogno di configurazione; tuttavia, Flysystem non è limitato a questi e possiede diversi adattori (adapters) per molti altri storage system. Puoi creare driver personalizzati se vuoi utilizzare uno di questi adapters all'interno della tua applicazione Laravel.

Per creare un filesystem personalizzato devi per prima cosa creare un [service provider](/documentazione/5.1/provider) come ad esempio `DropboxServiceProvider`. Nel metodo `boot` del nuovo provider puoi usare la facade `Storage` e il metodo `extend` per definire il tuo filesystem:

	<?php namespace App\Providers;

	use Storage;
	use League\Flysystem\Filesystem;
	use Dropbox\Client as DropboxClient;
	use Illuminate\Support\ServiceProvider;
	use League\Flysystem\Dropbox\DropboxAdapter;

	class DropboxServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Storage::extend('dropbox', function($app, $config) {
				$client = new DropboxClient(
					$config['accessToken'], $config['clientIdentifier']
				);

				return new Filesystem(new DropboxAdapter($client));
			});
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

Il primo argomento del metodo `extend` è il nome del driver mentre il secondo argomento è una Closure che riceve le variabili `$app` e `$config`. La Closure dovrà restituire una istanza di `League\Flysystem\Filesystem`. La variabile `$config` conterrà i valori definiti in `config/filesystems.php` per il disco specificato.

Una volta che hai creato il service provider e registrato l'estensione potrai utilizzare il driver `dropbox` nel file di configurazione `config/filesystem.php`.
