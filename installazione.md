# Installazione

- [Installazione](#installazione)
- [Configurazione](#configurazione)
	- [Configurazione Base](#configurazione-base)
	- [Configurazione Ambiente](#configurazione-ambiente)
	- [Configurazioni Cache](#configurazioni-cache)
	- [Accesso ai Valori di Configurazione](#accesso-valori-configurazione)
	- [Dare un Nome alla Tua Applicazione](#dare-nome-alla-tua-applicazione)
- [Modalità di Manutenzione](#modalita-manutenzione)

<a name="installazione"></a>
## Installazione

### Requisiti Server

Laravel richiede alcuni requisiti di sistema. Ovviamente, tutti questi requisiti sono soddisfatti dalla macchina virtuale di [Laravel Homestead](/docs/5.1/homestead):

<div class="content-list" markdown="1">
- PHP >= 5.5.9
- OpenSSL PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension
</div>

<a name="installare-laravel"></a>
### Installare Laravel

Laravel utilizza [Composer](http://getcomposer.org) per gestire le sue dipendenze. Quindi, prima di usare Laravel, assicurati di avere installato Composer sulla tua macchina.

#### Tramite Laravel Installer

Per prima cosa, scarica Laravel installer usando Composer:

	composer global require "laravel/installer=~1.1"

Assicurati di aggiungere la directory `~/.composer/vendor/bin` nella variabile di sistema PATH della tua macchina, in modo che l'eseguibile `laravel` venga riconosciuto dal tuo sistema.

Una volta installato, usa il comando `laravel new` per creare una nuova installazione di Laravel nella directory da te specificata. Per esempio, `laravel new blog` creerà una directory chiamata `blog` contenente una nuova installazione di Laravel cont tutte le dipendenze già installate. Questo metodo di installazione è più veloce rispetto all'installazione tramite Composer:

	laravel new blog

#### Tramite Composer Create-Project

Puoi anche installare Laravel usando il comando `create-project` di Composer da terminale:

	composer create-project laravel/laravel --prefer-dist

<a name="configurazione"></a>
## Configurazione

<a name="configurazione-base"></a>
### Configurazione Base

Tutti i file di configurazione di Laravel sono salvati nella directory `config`. Ogni opzione è documentata, quindi sentiti libero di darci un'occhiata per acquisire familiarità con le varie opzioni disponibili.

#### Permessi Directory

Dopo aver installato Laravel, devi configurare alcuni permessi. Le directory all'interno di `storage` e `bootstrap/cache` dovrebbero essere scrivibili da tuo web server. Se stai usando[Homestead](/docs/5.1/homestead), questi permessi sono già settati.

#### Chiave dell'Applicazione

Il successivo passo che dovresti fare dopo l'installazione di Laravel e di impostare la chiave della tua applicazione ad una stringa casuale. Se hai installato Laravel tramite Composer o Laravel installer, questa chiave è già stata impostata per te tramite il comando `key:generate`. Solitamente, questa stringa dovrebbe essere composta da 32 caratteri. La chaive può essere impostata nel file di configurazione d'ambiente `.env`. Se non hai rinominato il file`.env.example` in `.env`, dovresti farlo ora.. **Se la chiave dell'applicazione non è impostata, le sessioni utente e altri dati crittografati non saranno sicuri!**

#### Configurazioni Aggiuntive

Laravel non ha bisogno di altre configurazioni. Sei libero di iniziare a sviluppare la tua applicazione! Tuttavia, portesti rivederti il file `config/app.php` e la sua documentazione. Il file contiene diverse opzioni come il `timezone` e `locale` che puoi cambiare liberamente in base alla tua applicazione.

Puoi configurare inoltre alcuni componenti aggiuntivi di Laravel, come:

- [Cache](/docs/5.1/cache#configurazione)
- [Database](/docs/5.1/database#configurazione)
- [Sessioni](/docs/5.1/sessioni#configurazione)

Una volta installato Laravel, puoi anche [configurare il tuo ambiente in locale](/docs/5.1/installazione#configurazione-ambiente).

<a name="riscrittura-url"></a>
#### Riscrittura URL

**Apache**

Il framework lavora con un file `public/.htaccess` usato per permettere gli URL senza `index.php`. Se usi Apache per eseguire la tua applicazione, assicurati di abilitare il modulo `mod_rewrite`.

Se il file `.htaccess` usato con Laravel non dovesse funzionare con la tua installazione di Apache, prova questa configurazione:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

**Nginx**

Su Nginx, invece, puoi usare le seguenti direttive nel tuo file di configurazione per ottenere lo stesso risultato:

	location / {
		try_files $uri $uri/ /index.php?$query_string;
	}

Ovviamente, quando usi [Homestead](/docs/5.1/homestead), la riscrittura degli indirizzi è sarà configurata automaticamente.

<a name="configurazione-ambiente"></a>
### Configurazione Ambiente

Spesso è utile avere differenti valori basati sull'ambiente sul quale viene eseguita l'applicazione. Per esempio, potresti usare diversi driver di cache in locale diversamente da come si farebbe su un server di produzione. E' davvero facile usare le configurazioni d'ambiente.

Per renderlo un gioco da ragazzi, Laravel usa la libreria PHP [DotEnv](https://github.com/vlucas/phpdotenv) di Vance Lucas. In una nuova installazione di Laravel, la directory principale della tua applicazione conterrà un file `.env.example`. Se installi Laravel tramite Composer, questo file sarà automaticamente rinominato in `.env`.Altrimenti, devi rinominarlo manualmente.

Tutte le variabili presenti in questo file vengono caricate nell'array super-global $_ENV, quando la tua applicazione riceve una richiesta. Puoi usare quindi l'helper env() per recuperare i vari valori da questo array. Se guardi un po' i vari file di configurazione, infatti, noterai che questa funzione viene usata spesso!

Sentiti libero di modificare come meglio credi le tue variabili per l'ambiente locale, così come per quello di produzione. Ad ogni modo, il tuo file .env non dovrebbe essere soggetto a commit in caso di controllo di versione, dato che ogni sviluppatore (o server) potrebbe richiederne uno differente o personalizzato ad hoc.

Se stai sviluppando in team, assicurati che venga comunque incluso un file `.env.example` con la tua applicazione. Inserendo dei valori place-holder values nel file di configurazione di esempio, gli altri sviluppatori del tuo team possono chiaramente vedere quali variabili d'ambiente sono necessarie per eseguire la tua applicazione.

#### Accedere alle Impostazioni dell'Ambiente Corrente

uoi accedere alle impostazioni dell'ambiente corrente tramite il metodo `environment` della facade`App`:

	$environment = App::environment();

Puoi anche passare un argomento (o più di uno) al metodo in modo tale da controllare se ci si trova in un certo ambiente oppure no. Puoi anche passare valori multipli se necessario:

	if (App::environment('local')) {
		// The environment is local
	}

	if (App::environment('local', 'staging')) {
		// The environment is either local OR staging...
	}

All'instanza dell'applicazione si può accedere anche tramite l'helper `app`:

	$environment = app()->environment();

<a name="configurazioni-cache"></a>
### Configurazioni Cache

Per rendere la tua applicazione più veloce, potresti mettere in cache tutti i tuoi file di configurazione in un singolo file usando il comando Artisan `config:cache`. Questo comando combinerà tutte le opzioni di configurazione per la tua applicazione in un singolo file che potrà poi essere caricato più velocemente dal framework.

Dovresti eseguire il comando `config:cache` come parte delle tue operazioni di deploy.

<a name="accesso-valori-configurazione"></a>
### Accesso ai Valori di Configurazione

Puoi facilmente accedere ai tuoi valori di configurazione usando l'helper globale `config`. Ai valori di configurazione si può accedere tramite la sintassi"dot", che include il nome del file e l'opzione alla quale vuoi accedere. Può anche essere specificato un valore di default e in caso l'opzione non esiste verrà ritornato:

	$value = config('app.timezone');

Per impostare un valore di configurazione in runtime, basta passare un array all'helper `config`:

	config(['app.timezone' => 'America/Chicago']);

<a name="dare-nome-alla-tua-applicazione"></a>
### Dare un Nome alla Tua Applicazione

Dopo aver installato Laravel, potresti dare un “nome” alla tua applicazione. Di default, la directory `app` è inclusa sotto il namespace`App`, è caricato da Composer usando lo [standard autoloading PSR-4](http://www.php-fig.org/psr/psr-4/). Tuttavia, puoi cambiare il namespace per la tua applicazione, è lo puoi fare con il comando Artisan `app:name`.

Per esempio, se la tua applicazione s ichiama "LaravelItalia", puoi eseguire il comando dalla root della tua installazione di laravel in questo modo:

	php artisan app:name LaravelItalia

Rinominare la tua applicazione è facoltativo, se libero di mantenere il namespace `App` se lo desideri.

<a name="modalita-manutenzione"></a>
## Modalità di Manutenzione

Se la tua applicazione è in modalità di manutenzione, una view personalizzata verrà mostrata per tutte le richieste in arrivo. Tale funzionalità rende semplice "disabilitare" la tua applicazione per un po', magari durante un update o durante un'operazione di manutenzione. Un controllo di stato di manutenzione è già presente nello stack dell'applicazione. Se quindi il tuo progetto dovesse trovarsi in manutenzione verrà restituita una HttpException con uno status code 503. 

Abilitare la modalità di manutenzione è semplicissimo, se si usa Artisan:

	php artisan down

Per ritornare in piena attività, invece, basta usare up:

	php artisan up

### Template Modalità di Manutenzione

Di default il template per la modalità di manutenzione si trova in `resources/views/errors/503.blade.php`.

### Modalità di Manutenzione & Code

Mente la tua applicazione è in modalità di manutenzione, non verrà gestita nessuna [coda jobs](/docs/5.1/code). Le code ritorneranno ad essere gestite una volta che l'applicazione sarà uscita dalla modalità di manutenzione.
