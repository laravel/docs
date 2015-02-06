# Ciclo di Vita della Richiesta

- [Introduzione](#introduzione)
- [Overview del Ciclo di Vita](#overview-ciclo-vita)
- [Focus sui Service Provider](#focus-service-provider)

<a name="introduzione"></a>
## Introduzione

Quando usi un qualsiasi tool nel "mondo reale", puoi sentirtici più in confidenza se sai effettivamente come lo strumento in questione funziona. Come puoi ben immaginare, lo sviluppo di applicazioni non fa eccezione. Una volta che hai capito al meglio come lavorare con i tuoi strumenti di sviluppo hai molta più potenza tra le mani.

L'obiettivo di questo piccolo capitolo della guida è di darti una conoscenza di alto livello ma comunque sufficiente a capire come Laravel "funziona". È bello poter dire "magico", ma sapere cosa c'è sotto lo è ancora di più!

Se non dovessi capire tutto al primo tentativo non preoccuparti. Comincia a comprendere queste prime nozioni base e la tua conoscenza crescerà sempre di più, mano a mano che esplorerai le svariate sezioni della documentazione che stai leggendo.

<a name="overview-ciclo-vita"></a>
## Overview del Ciclo di Vita

#### Si Comincia!

Il punto d'ingresso di tutte le richieste è il file `public/index.php`. 

Tutte le richieste infatti vengono reindirizzate a questo file dal tuo server. Il file _index.php_ non contiene, in realtà, molto codice: non è altro che un punto di inizio per il caricamento di tutto il resto del framework.

Il file _index_, infatti, carica l'autoloader generato da Composer e recupera le istanze necessarie a lavorare dal file `bootstrap/app.php`. La prima cosa che viene fatta, quindi, è la creazione dell'istanza del [service container](/container).

#### HTTP / Console Kernel

Il passo successivo da effettuare è mandare la richiesta al Kernel HTTP (o Console, in base al tipo di richiesta). Questi due Kernel servono come centro di smistamento per le varie richieste. Concentriamoci, per ora, sul Kernel HTTP nel file `app/Http/Kernel.php`.

Questo Kernel estende la classe `Illuminate\Foundation\Http\Kernel` che definisce un array di "bootstrapper", i quali verranno eseguiti prima di eseguire la richiesta vera e propria. Questi bootstrapper configurano la gestione degli errori, logging e così via.

Il Kernel inoltre definisce le liste di Middleware da usare. Questi middleware leggono le richieste e svolgono varie operazioni: dal controllo di un'eventuale modalità di manutenzione attiva alla verifica dei token CSRF, e così via.

La segnatura del metodo _handle_ del Kernel HTTP è molto semplice: riceve una _Request_ e ritorna una _Response_. Ecco, pensa al Kernel come una grande scatola nera che rappresenta l'intera applicazione.

#### Service Provider

Una della cose più importanti che fa il Kernel in fase di Bootstrap è il caricamento dei service provider per la tua applicazione. Tutti i service provider sono configurati nel file _config/app.php_, nell'array _providers_. Una volta caricati tutti i provider tramite _register_, il metodo _boot_ verrà richiamato.

#### Invio della Richiesta

Una volta che l'applicazione è stata avviata correttamente, insieme alla registrazione dei service provider, la _Request_ vera e propria verrà passata al router per il dispatch. A questo punto dell'esecuzione sarà il router a capire verso quale route o verso quale controller mandare la richiesta.

<a name="focus-service-provider"></a>
## Focus sui Service Provider

I service provider sono la chiave del bootstrapping di una qualsiasi applicazione Laravel. Una volta che l'istanza dell'applicazione viene creata, infatti, i service provider vengono registrati e la richiesta viene "rigirata" all'applicazione.

Averne una conoscenza aiuta molto. Di default, i service provider si trovano nella cartella _app/Providers_.

Subito dopo la creazione di un progetto, la classe _AppServiceProvider_ è praticamente vuota. Tuttavia, può essere usata senza problemi come punto da cui registrare i vari binding del service container. Per applicazioni più grandi, invece, la cosa migliore da fare è creare più di un service provider adatto allo scopo, in modo tale da rendere la fase di avvio più "granulare" e più gestibile.
