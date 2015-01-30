# Laravel Homestead

- [Introduzione](#introduzione)
- [Software Incluso](#software-incluso)
- [Installazione e Setup](#installazione-setup)
- [Uso Quotidiano](#uso-quotidiano)
- [Porte](#porte)

<a name="introduzione"></a>
## Introduzione

L'obiettivo di Laravel è migliorare l'esperienza di sviluppo PHP. La cosa, ovviamente, include anche l'ambiente di lavoro locale. [Vagrant](http://vagrantup.com) fornisce un modo semplice ed elegante di gestire delle macchine virtuali.

Laravel **Homestead** è la nostra "box" ufficiale già pronta per Vagrant che ti permette di avere a disposizione un ambiente di lavoro in locale completo di tutto quello di cui hai bisogno, senza dover stare ad installare ogni volta PHP, HHVM e tutto il resto dello stack di cui necessiti. Tra l'altro, una delle cose più interessanti di Vagrant è che è possibile distruggere al volo una macchina e ricostruirla se qualcosa va storto, ma senza perdere i file del tuo progetto!

Il tutto in pochi minuti.

Homestead lavora senza problemi su Windows, Mac e sistemi Linux. Include un web server Nginx, PHP 5.6, MySQL, Postgres, Redis, Memcached e tanti altri software utili per lo sviluppo di applicazioni Laravel.

> **Nota:** Se stai lavorando con Windows, potresti avere la necessità di attivare la virtualizzazione hardware dal BIOS (VT-x).

Al momento, Homestead usa Vagrant 1.6.

<a name="software-incluso"></a>
## Software Incluso

- Ubuntu 14.04
- PHP 5.6
- HHVM
- Nginx
- MySQL
- Postgres
- Node (con Bower, Grunt e Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/ssh#envoy)
- Fabric + HipChat Extension

<a name="installazione-setup"></a>
## Installazione e Setup

### Installazione di VirtualBox e Vagrant

Prima di lanciare il tuo ambiente di lavoro con Homestead, devi necessariamente installare [VirtualBox](https://www.virtualbox.org/wiki/Downloads) e [Vagrant](http://www.vagrantup.com/downloads.html). Entrambi questi software hanno degli installer visuali facilissimi da usare, per tutti i sistemi operativi.

### Aggiunta della Box

Una volta installati VirtualBox e Vagrant, il passo successivo è aggiungere la box di Homestead alla tua installazione. Lo si può fare tramite un semplice comando da terminale e richiede pochissimi minuti (in base alla velocità della tua connessione).

	vagrant box add laravel/homestead

### Installare Homestead

#### Con Composer + PHP Tool

Una volta che la box è stata aggiunta correttamente, puoi procedere con l'installazione vera e propria. Sei pronto ad installare il tool Homestead direttamente da linea di comando, con Composer.

	composer global require "laravel/homestead=~2.0"

Fai in modo che il percorso `~/.composer/vendor/bin` venga inserito nella tua variabile d'ambiente PATH, in modo tale da avere a disposizione il tool ovunque.

A questo punto esegui il comando _init_ per creare un file di configurazione _Homestead.yaml_.

	homestead init

Tale file verrà posizionato nella directory `~/.homestead`. Se stai usando un sistema Linux o Mac, puoi anche modificare da linea di comando il file con il comando _edit_.

	homestead edit

#### Installazione via Git, senza PHP

In alternativa, puoi decidere di non voler installare PHP sulla tua macchina in locale. Perfetto: puoi installare Homestead semplicemente clonando il suo repository. Considera comunque che ti conviene clonare il repository dentro una cartella _Homestead_ nella tua directory "home", dato che comunque ne avrai bisogno per tutti i tuoi progetti.

	git clone https://github.com/laravel/homestead.git Homestead

Una volta installato il tool da linea di comando, esegui `bash init.sh` per creare il file `Homestead.yaml` di configurazione:

	bash init.sh

Il file verrà messo, in ogni caso, in `~/.homestead`.

### Imposta la Chiave SSH

Lo step successivo è modificare il file _Homestead.yaml_. In questo file puoi configurare il percorso per la tua chiave SSH pubblica, così come le cartelle che verranno condivise tra la tua macchina e quella virtuale.

Se non hai una chiave SSH non ti preoccupare. Basta usare il comando

	ssh-keygen -t rsa -C "you@homestead"

Per generarla. Se hai Windows, considera l'installazione di git e usa la _Git Bash_ inclusa.

Una volta creata la chiave, specificane il percorso in _Homestead.yaml_, in corrispondenza di `authorize`.

### Configura le Cartelle Condivise

La proprietà _folders_ nel file _Homestead.yaml_ elenca tutte le cartelle che vengono condivise tra la tua macchina locale e quella virtuale. Ad ogni cambiamento di uno di questi file, questi vengono sincronizzati tra le due macchine.

### Configura i siti Nginx

Non sei familiare con il mondo Nginx? E che problema c'è? La proprietà _sites_ permette di mappare un certo dominio con una cartella del tuo ambiente Homestead. Una configurazione di esempio è già presente in _Homestead.yaml_. Esattamente come per le cartelle condivise, puoi aggiungerne quanti ne vuoi.

Puoi anche specificare per quali siti usare [HHVM](http://hhvm.com) tramite questo semplice flag:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public
	      hhvm: true

### Bash Alias

Per aggiungere gli alias alla tua Homestead box, usa il file _aliases_ nella cartella `~/.homestead`.

### Lancio della Vagrant Box

Adesso che è tutto pronto nel file _Homestead.yaml_ è arrivato il momento di usare il comando

	homestead up

per lanciare la tua box. Nel caso in cui tu non abbia usato il tool di homestead, allora usa

	vagrant up

nella cartella in cui hai clonato il repository.

Vagrant avvierà la macchina virtuale e configurerà tutto il necessario per iniziare a lavorare. Nel caso in cui to voglia "distruggere" la macchina (potrebbe non servirti più) usa il comando _homestead destroy_.

Per leggere una lista completa di tutti i comandi che puoi usare, invece, usa _homestead list_.

Non scordarti di aggiungere i domini che hai specificato nel file dei siti di Nginx sulla tua macchina. Il file _hosts_ si occuperà di effettuare il redirect delle singole richieste in base al dominio specificato. In Linux e Mac puoi trovare questo file in `/etc/hosts`. Su Windows, invece, lo trovi in `C:\Windows\System32\drivers\etc\hosts`.

Ecco un esempio di aggiunta del dominio:

	192.168.10.10  homestead.app

Dove _192.168.10.10_ è l'IP da te specificato in _Homestead.yaml_. L'app sarà quindi raggiungibile tramite l'indirizzo:

	http://homestead.app

Adesso vediamo cos'altro possiamo fare con la macchina virtuale!

<a name="uso-quotidiano"></a>
## Uso Quotidiano

### Connessione tramite SSH

Connetterti alla tua macchina virtuale Homestead è semplice: usa _homestead ssh_ e sei dentro.

### Connessione ai Database

Un database _homestead_ è già pronto per essere usato in caso di bisogno, sia in MySQL che in Postgres. Per una maggiore convenienza, inoltre, Laravel è normalmente configurato per usare di default questo database.

Per connetterti al tuo database sulla macchina virtuale dalla macchina fisica, non devi fare altro che usare l'IP _127.0.0.1_ con la porta 33060 (MySQL) o 54320 (Postgres). Lo username e la password di default sono, in entrambi i casi, _homestead/secret_.

> **Nota:** dovresti usare sempre queste porte non-standard in caso di connessione al database dalla macchina fisica principale. Nei tuoi file di configurazione di Laravel invece userai la 3306 e 5432, dato che l'applicazione viene eseguita _sulla_ macchina virtuale.

### Aggiunta di Altri Siti

Una volta che il tuo sistema è avviato ed attivo, potresti voler aggiungere altri siti al file di configurazione. Puoi farlo tranquillamente modificando come meglio ritieni il file _Homestead.yaml_, quindi provvedendo ad eseguire il comando _vagrant provision_.

In alternativa, puoi sempre usare il comando _serve_ direttamente dalla macchina virtuale, tramite SSH.

	serve domain.app /home/vagrant/Code/path/to/public/directory

> **Nota:** In ogni caso, ricorda sempre di aggiungere il nuovo sito nel file _hosts_ sulla tua macchina!

<a name="porte"></a>
## Porte

Le seguenti porte sono già state sistemate per lavorare con Homestead:

- **SSH:** 2222 -> Forward alla 22
- **HTTP:** 8000 -> Forward alla 80
- **MySQL:** 33060 -> Forward alla 3306
- **Postgres:** 54320 -> Forward alla 5432
