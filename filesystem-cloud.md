# Filesystem / Cloud

- [Introduzione](#introduzione)
- [Configurazione](#configurazione)
- [Uso Base](#uso-base)

<a name="introduzione"></a>
## Introduzione

A partire da Laravel 5.0, per la gestione del file system viene usato il fantastico package [Flysystem](https://github.com/thephpleague/flysystem) di Frank de Jonge. Questa integrazione ti permetterà, in modo semplice e veloce, di lavorare non solo con il file system locale, ma anche con Amazon S3, Rackspace e tante altre possibilità! Inoltre, cambiare file system richiederà pochissimo tempo, dato che l'API rimane la stessa per ogni sistema.

<a name="configurazione"></a>
## Configurazione

Il file di configurazione del filesystem si trova in `config/filesystems.php`. In questo file potrai definire tutti i tuoi "dischi". Ogni disco rappresenta una specifica location per la memorizzazione dei tuoi file. Per renderti meglio l'idea, in questo config file ci sono già alcuni dischi di esempio pre-impostati.

Ricorda, comunque, che per lavorare con S3 o Rackspace avrai bisogno di installare altri package aggiuntivi:

- Amazon S3: `league/flysystem-aws-s3-v2 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

Mantenendo la linea di Laravel per questo genere di cose, potrai definire quanti dischi desideri, e anche più di uno sullo stesso driver.

Usando il _local_ driver, quello di default, noterai che tutte le operazioni sui file sono relative alla _root_ directory contenuta nel file di configurazione. Di default, tale valore è impostato in _storage/app_. Nulla comunque ti vieta di cambiarlo come meglio credi.

Ad ogni modo, usando le impostazioni di default, per scrivere del testo nel file `storage/app/file.txt` ti basterà, semplicemente:

	Storage::disk('local')->put('file.txt', 'Contents');

<a name="uso-base"></a>
## Uso Base

Puoi usare la facade _Storage_ per effettuare tutte le interazioni con il tuo filesystem. Oppure puoi effettuare il type-hint di `Illuminate\Contracts\Filesystem\Factory` nel caso in cui tu lo preferisca.

Vediamo adesso qualche esempio pratico.

#### Definisci il Disco da Usare

	$disk = Storage::disk('s3');

	$disk = Storage::disk('local');

#### Chiamata di un Metodo su un Certo Disco

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Determinare se un File Esiste

	if (Storage::exists('file.jpg'))
	{
		//
	}

#### Recuperare i Contenuti di un File

	$contents = Storage::get('file.jpg');

#### Scrivere i Contenuti di un File

	Storage::put('file.jpg', $contents);

#### Inserire dei Contenuti in un File, all'Inizio

	Storage::prepend('file.log', 'Prepended Text');

#### Aggiungere dei Contenuti ad un File

	Storage::append('file.log', 'Appended Text');

#### Cancellare un File

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

#### Copiare un File

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

#### Spostare un File

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### Ottenere le Dimensioni di un File

	$size = Storage::size('file1.jpg');

#### Ottenere la Data di Ultima Modifica

	$time = Storage::lastModified('file1.jpg');

#### Ottenere tutti i File di una Cartella

	$files = Storage::files($directory);

	// Ricorsivamente...
	$files = Storage::allFiles($directory);

#### Ottenere tutte le Cartelle in una Cartella

	$directories = Storage::directories($directory);

	// Ricorsivamente...
	$directories = Storage::allDirectories($directory);

#### Creare una Cartella

	Storage::makeDirectory($directory);

#### Cancellare una Cartella

	Storage::deleteDirectory($directory);
