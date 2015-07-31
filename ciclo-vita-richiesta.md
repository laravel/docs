# Ciclo di Vita della Richiesta

- [Introduzione](#introduzione)
- [Overview del Ciclo di Vita](#overview-ciclo-di-vita)
- [Focus sui Service Provider](#focus-sui-service-provider)

<a name="introduzione"></a>
## Introduzione

Quando usi un qualsiasi tool nel "mondo reale", puoi sentirtici più in confidenza se sai effettivamente come lo strumento in questione funziona. Come puoi ben immaginare, lo sviluppo di applicazioni non fa eccezione. Una volta che hai capito al meglio come lavorare con i tuoi strumenti di sviluppo hai molta più potenza tra le mani.

L'obiettivo di questo piccolo capitolo della guida è di darti una conoscenza di alto livello ma comunque sufficiente a capire come Laravel "funziona". È bello poter dire "magico", ma sapere cosa c'è sotto lo è ancora di più!

Se non dovessi capire tutto al primo tentativo non preoccuparti. Comincia a comprendere queste prime nozioni base e la tua conoscenza crescerà sempre di più, mano a mano che esplorerai le svariate sezioni della documentazione che stai leggendo.

<a name="overview-ciclo-di-vita"></a>
## Overview del Ciclo di Vita

### Prima Osservazione

Il punto d'ingresso di tutte le richieste di un applicazione Laravel è il file `public/index.php`. Tutte le richieste sono indirizzate a questo file dalla configurazione del tuo web server (Apache / Nginx). Il file `index.php` non contiene, in realtà, molto codice: non è altro che un punto di inizio per il caricamento di tutto il resto del framework.

Il file `index.php` carica l'autoloader generato da Composer, e recupera le istanze necessarie a lavorare dal file `bootstrap/app.php`. La prima cosa che viene fatta, quindi, è la creazione dell'istanza del [service container](/documentazione/5.1/container).

### HTTP / Console Kernels

Il passo successivo da effettuare è mandare la richiesta al Kernel HTTP (o Console, in base al tipo di richiesta). Questi due Kernel servono come centro di smistamento per le varie richieste. Concentriamoci, per ora, sul Kernel HTTP nel file `app/Http/Kernel.php`.

Questo Kernel estende la classe `Illuminate\Foundation\Http\Kernel`, che definisce un array di `bootstrapper`, i quali verranno eseguiti prima di eseguire la richiesta vera e propria. Questi bootstrapper configurano la gestione degli errori, logging, [determinano l'ambiente dell'applicazione](/documentazione/5.1/installatzone#configurazione-ambiente), ed eseguono altre operazioni che devono essere eseguite prima che la richiesta venga gestita.

Il Kernel inoltre definisce le liste di [middleware](/documentazione/5.1/middleware) da usare. Questi middleware gestiscono la lettura e scrittura delle [sessioni HTTP ](/documentazione/5.1/sessioni), determinato se l'applicazione è in uno stato di maintenance mode, [verificatno il token CSRF](/documentazione/5.1/routing#protezione-csrf), e così via.

La segnatura del metodo `handle` del Kernel HTTP è molto semplice: riceva una `Request` e ritorna una `Response`. Ecco, pensa al Kernel come una grande scatola nera che rappresenta l'intera applicazione. Dai al Kernel delle richieste HTTP e “lui” ti ritornerà risposte HTTP.

#### Service Provider

Una della cose più importanti che fa il Kernel in fase di Bootstrap è il caricamento dei [service provider](/documentazione/5.1/providers) per la tua applicazione. Tutti i service provider per l'applicazione sono configurati nell'array `providers` del file di configurazione `config/app.php`. Una volta caricati tutti i provider tramite register, il metodo boot verrà richiamato.

I service provider sono responsabili del caricamento di vari compomenti del framework, come il database, le code, la validazione, e le componenti del routing. Visto che caricano e configurano tutte le feature offerte dal framework, i service provider rappresentano un'aspetto molto importante dell'intero processo di caricamento di Laravel.

#### Invio della Richiesta

Una volta che l'applicazione è stata caricata e tutti i service provider sono stati registrati, la `Request` vera e propria verrà passata al router per il dispatch. A questo punto dell'esecuzione sarà il router a capire verso quale route o verso quale controller mandare la richiesta, così come l'esecuzione di qualsiasi middleware specifico.

<a name="focus-sui-service-provider"></a>
## Focus sui Service Provider

I service provider sono la chiave del bootstrapping di una qualsiasi applicazione Laravel. Una volta che l'istanza dell'applicazione viene creata, infatti, i service provider vengono registrati e la richiesta viene "rigirata" all'applicazione.

Averne una conoscenza aiuta molto. Di default, i service provider si trovano nella cartella  `app/Providers`.

Subito dopo la creazione di un progetto, la classe `AppServiceProvider`è praticamente vuota. Tuttavia, può essere usata senza problemi come punto da cui registrare i vari binding del service container. Per applicazioni più grandi, invece, la cosa migliore da fare è creare più di un service provider adatto allo scopo, in modo tale da rendere la fase di avvio più "granulare" e più gestibile.
