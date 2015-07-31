# Struttura dell'Applicazione

- [Introduzione](#introduzione)
- [La Root Directory](#la-root-directory)
- [La Directory App](#la-directory-app)
- [Namespacing della Tua Applicazione](#namespacing-della-tua-applicazione)

<a name="introduzione"></a>
## Introduzione

Di default, l'obiettivo della struttura attuale della cartella di un progetto Laravel è offrirti un ottimo punto di partenza per applicazioni sia grandi che piccole. Ad ogni modo, comunque, sentiti libero di modificare tutto come meglio credi. Nella pratica Laravel non impone nessuna struttura fissa e nessuna regola su dove mettere una classe: tutto quello che serve è sapere se Composer può caricare la classe di cui abbiamo bisogno.

<a name="la-root-directory"></a>
## La Root Directory

La root directory di una nuova installazione di Laravel contiene varie cartelle:

La cartella `app`, che come puoi sicuramente aspettarti, contiene il codice della tua applicazione. Ne parleremo meglio tra qualche riga.

La cartella `bootstrap` contiene tutti i file di cui il framework ha bisogno per configurare l'autoloading, così come la cartella `cache` che contiene alcuni file generati per ottimizzare il processo di boostrap del framework.

La cartella `config`, come è implicito nel nome, contiene tutti i file di configurazione della tua applicazione.

La cartella `database` contiene tutti i file delle migration e dei seed del tuo database. Se lo desideri, puoi anche usare questa cartella per un database SQLite.

La cartella `public` contiene il file di "ingresso" della tua applicazione e i tuoi asset (immagini, JavaScript, CSS e così via).

La cartella `resources` contiene le view, gli asset "grezzi" (LESS, SASS, CoffeeScript) ed i file per la localizzazione.

La cartella `storage` contiene i template Blade compilati, dati di sessione, cache e così via. Questa cartella è situata all'interno di `app`, contiene le cartelle `framework` e `logs`. La cartella `app` può essere usata per memorizzare qualsiasi file utilizzato dalla tua applicazione. La cartella `framework` è usata per memorizzare file generati dal framework e file generati dalla cache. In fine, la cartella `logs` contiene i file di log della tua applicazione.

La cartella `tests` contiene i test della tua applicazione. Viene offerto un esempio, incluso in Laravel, di test con [PHPUnit](https://phpunit.de/).

La cartella `vendor` contiene le dipendenze installate via [Composer](https://getcomposer.org).

<a name="la-directory-app"></a>
## La Directory App

Il "cuore" della tua applicazione è in app. Di default, questa directory ha un namespace "App" associato automaticamente, a sua volta caricato tramite Composer usando [lo standard PSR-4](http://www.php-fig.org/psr/psr-4/). **Puoi cambiare questo namespace quando vuoi tramite il comando `app:name` di Artisan**.

La cartella `app` contiene a sua volta svariate directory come `Console`, `Http` e `Providers`. Innanzitutto, immagina `Console` ed `Http` come un'interfaccia alla tua vera applicazione. Il protocollo HTTP e CLI sono entrambi dei meccanismi di interazione con un'applicazione, ma non contengono davvero una logica. Insomma: sono solo due modi di interagire con la stessa applicazione. La cartella `Console` contiene tutti i tuoi comandi Artisan, mentre la cartella `Http` contiene i tuoi controller, filtri e richieste.

La cartella `Jobs`, ovviamente, ospita le [code di job](/documentazione/5.1/code) per la tua applicazione. I Job possono essere messi in coda dalla tua applicazione, così come possono essere eseguiti in modo sincroni con il ciclo di vita della richiesta corrente.

La cartella `Events`, come puoi aspettarti, ospita le [classi degli eventi](/documentazione/5.1/eventi). Gli eventi possono essere utilizzati per “allertare” altre parti della tua applicazione in seguito ad una determinata azione.

La cartella `Listeners` contiene le classi handler per gli eventi. Gli Handler ricevono un evento and ed eseguono una logica in risposta all'evento che è stato richiamato. Per esempio, un evento `UserRegistered` potrebbe essere gestito da un listener `SendWelcomeEmail`.

La cartella `Exceptions` contiene gli handler per l'eccezioni per la tua applicazione, ed è anche un ottimo posto in cui sistemare le varie eccezioni speciali e personalizate della tua applicazione.

> **Nota:** Molte delle classi presenti nella cartella `app` possono essere generate tramite dei comandi Artisan. Usa il comando `php artisan list make` per vederli tutti nello specifico.

<a name="namespacing-della-tua-applicazione"></a>
## Namespacing della Tua Applicazione

Come detto già in precedenza, il namespace di deafult di una nuova applicazione è `App`;, ma nulla ti vieta di cambiare questo namespace in un altro più adatto al caso. Se è questo il tuo bisogno, usa il comando:

	php artisan app:name SocialNet

Ovviamente, sei libero di usare il namespace `App`.
