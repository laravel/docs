# Struttura dell'Applicazione

- [Introduzione](#introduzione)
- [La Root Directory](#root-directory)
- [La Directory app](#directory-app)
- [Namespacing della Tua Applicazione](#namespacing-tua-applicazione)

<a name="introduzione"></a>
## Introduzione

Di default, l'obiettivo della struttura attuale della cartella di un progetto Laravel è offrirti un ottimo punto di partenza per applicazioni sia grandi che piccole. Ad ogni modo, comunque, sentiti libero di modificare tutto come meglio credi. Nella pratica Laravel non impone nessuna struttura fissa e nessuna regola su dove mettere una classe: tutto quello che serve è sapere se Composer può caricare la classe di cui abbiamo bisogno.

<a name="root-directory"></a>
## La Root Directory

La cartella principale di un'installazione fresca fresca di Laravel contiene le seguenti cartelle.

La cartella `app`, che come puoi sicuramente aspettarti, contiene il codice della tua applicazione. Ne parleremo meglio tra qualche riga.

La cartella `bootstrap` contiene tutti i file di cui il framework ha bisogno per configurare l'autoloading.

La cartella `config` contiene tutti i file di configurazione.

La cartella `database` contiene i file delle migration e del seeding del tuo database.

La cartella `public` contiene il file di "ingresso" della tua applicazione e i tuoi asset (immagini, JavaScript, CSS e così via).

La cartella `resources` contiene le view, gli asset "grezzi" (LESS, SASS, CoffeeScript) ed i file per la localizzazione.

La cartella `storage` contiene i template Blade compilati, dati di sessione, cache e così via.

La cartella `tests` contiene i test della tua applicazione.

La cartella `vendor` contiene le dipendenze installate via Compsoer.

<a name="directory-app"></a>
## La Directory app

Il "cuore" della tua applicazione è in _app_. Di default, questa directory ha un namespace "App" associato automaticamente, a sua volta caricato tramite Composer usando [lo standard PSR-4](http://www.php-fig.org/psr/psr-4/). **Puoi cambiare questo namespace quando vuoi tramite il comando `app:name` di Artisan**.

La cartella _app_ contiene a sua volta svariate directory come _Console_, _Http_ e _Providers_. Innanzitutto, immagina _Console_ ed _Http_ come un'interfaccia alla tua vera applicazione. Il protocollo HTTP e CLI sono entrambi dei meccanismi di interazione con un'applicazione, ma non contengono davvero una logica. Insomma: sono solo due modi di interagire con la stessa applicazione.

La cartella _Commands_ ospita invece i comandi della tua applicazione. Puoi vedere i comandi come un lavoro che può essere messo in coda dalla tua applicazione, così come dei task specifici che puoi avviare in modo sincrono quando ritieni opportuno.

La cartella _Events_, come puoi ben immaginare, ospita invece le classi dei vari eventi. Usare delle classi per rappresentare un evento, vero, non è necessario. Tuttavia, nel caso tu decidessi di adottare questa pratica, questa sarà la cartella in cui verranno creati dal comando _make_ di Artisan.

La cartella _Handlers_ contiene invece le classi degli handler, sia per i comandi che per gli eventi. Gli handler ricevono un particolare comando o evento ed eseguono una certa serie di istruzioni in risposta a quello che succede.

La cartella _Services_ contiene svariati servizi "helper" per la tua applicazione. Ad esempio, il servizio _Registrar_ incluso con Laravel si occupa di validare e creare i nuovi utenti della tua applicazione. Un altro esempio di servizio può essere l'interazione con un'API esterna, un sistema di metriche o, perché no, un "qualcosa" che si occupi di aggregare dati dalla tua stessa applicazione.

La cartella _Exceptions_ contiene invece tutti gli handler per le eccezioni ed è inoltre un ottimo posto in cui sistemare le varie eccezioni speciali e personalizate della tua applicazione.

> **Nota:** molte delle classi presenti nella cartella _app_ possono essere generate tramite dei comandi Artisan. Usa il comando `php artisan list make` per vederli tutti nello specifico.

<a name="namespacing-tua-applicazione"></a>
## Namespacing della Tua Applicazione

Come detto già in precedenza, il namespace di deafult di una nuova applicazione è _App_, ma nulla ti vieta di cambiare questo namespace in un altro più adatto al caso. Se è questo il tuo bisogno, usa il comando `app:name`.

Eccone un esempio d'uso, in cui rinominiamo il namespace dell'applicazione attuale in "SocialNet":

	php artisan app:name SocialNet
