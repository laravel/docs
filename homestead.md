# Laravel Homestead

- [Introduzione](#introduzione)
- [Installazione & Setup](#installazione-e-setup)
	- [Primo Step](#primo-step)
	- [Configurare Homestead](#configurare-homestead)
	- [Avviare La Vagrant Box](#avviare-vagrant-box)
- [Uso quotidiano](#uso-quotidiano)
	- [Connessione tramite SSH](#connessione-tramite-ssh)
	- [Connessione ai Database](#connessione-database)
	- [Aggiunta di Altri Siti](#aggiunta-altri-siti)
	- [Porte](#porte)
- [Blackfire Profiler](#blackfire-profiler)

<a name="introduzione"></a>
## Introduzione

L'obiettivo di Laravel è migliorare l'esperienza di sviluppo PHP. La cosa, ovviamente, include anche l'ambiente di lavoro locale. [Vagrant](http://vagrantup.com) fornisce un modo semplice ed elegante di gestire delle macchine virtuali.

Laravel Homestead è la nostra "box" ufficiale già pronta per Vagrant che ti permette di avere a disposizione un ambiente di lavoro in locale completo di tutto quello di cui hai bisogno, senza dover stare ad installare ogni volta PHP, HHVM e tutto il resto dello stack di cui necessiti. Tra l'altro, una delle cose più interessanti di Vagrant è che è possibile distruggere al volo una macchina e ricostruirla se qualcosa va storto, ma senza perdere i file del tuo progetto! Il tutto in pochi minuti.

Homestead lavora senza problemi su Windows, Mac e sistemi Linux. Include un web server Nginx, PHP 5.6, MySQL, Postgres, Redis, Memcached e tanti altri software utili per lo sviluppo di applicazioni Laravel.

> **Nota:** Se stai lavorando con Windows, potresti avere la necessità di attivare la virtualizzazione hardware dal BIOS (VT-x). Solitamente può essera attivata dal BIOS.

Al momento, Homestead usa Vagrant 1.7.

<a name="software-incluso"></a>
### Software Incluso

- Ubuntu 14.04
- PHP 5.6
- HHVM
- Nginx
- MySQL
- Postgres
- Node (With PM2, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/docs/5.1/envoy)
- [Blackfire Profiler](#blackfire-profiler)

<a name="installazione-e-setup"></a>
## Installazione & Setup

<a name="primo-step"></a>
### Primo Step

Prima di eseguire il tuo ambiente Homestead, devi necessariamente installare [VirtualBox](https://www.virtualbox.org/wiki/Downloads) o [VMWare](http://www.vmware.com) così come [Vagrant](http://www.vagrantup.com/downloads.html). Entrambi questi software hanno degli installer visuali facilissimi da usare, per tutti i sistemi operativi.

Per usare il provider VMware, hai necessita di compare entrambi VMware Fusion / Desktop e il plugin [VMware Vagrant plug-in](http://www.vagrantup.com/vmware). VMware fornisce una condivisione di cartella molto più veloce come prestazioni.

#### Installare Homestead Vagrant Box

Una volta installati VirtualBox / VMware e Vagrant, il passo successivo è aggiungere la box di `laravel/homestead` alla tua installazione usando i seguenti comandi nel tuo terminale. Richiede pochissimi minuti (in base alla velocità della tua connessione).

	vagrant box add laravel/homestead

Se il comando non và a buon fine, puoi usare una vecchia versione di Vagrant che richiede il seguente URL:

	vagrant box add laravel/homestead https://atlas.hashicorp.com/laravel/boxes/homestead

#### Clonare Il Repository Homestead

Puoi installare Homestead semplicemente clonando il repository. Considera la clonazione del repository, in una cartella `Homestead` all'interno della tua directory "home", come il box Homestead che fungerà da host per tutti i tuoi progetti Laravel:

	git clone https://github.com/laravel/homestead.git Homestead

Una volta clonato il repository di Homestead, esegui il comando `bash init.sh` dalla directory Homestead per creare il file di configurazione `Homestead.yaml`. Il file `Homestead.yaml` sarà salvato nella directory `~/.homestead`:

	bash init.sh

<a name="configurare-homestead"></a>
### Configurare Homestead

#### Imposta il tuo Provider

La chiave `provider` nel file `Homestead.yaml` indica quale provider di Vagrant dovrebbe essere usato: `virtualbox` o `vmware_fusion`. Puoi impostare uno dei due a sceonda delle tue esigenze:

	provider: virtualbox

#### Impostare la Chiave SSH

Nel file `Homestead.yaml`, dovresti configurare anche il percorso della tua chiave pubblica SSH. Non hai una chiave SSH? Con Mac e Linuz, puoi solitamente creare una chiave SSH usando il seguente comando:

	ssh-keygen -t rsa -C "you@homestead"

Con Windows, puoi installare [Git](http://git-scm.com/) ed usare la shell "Git Bash" inclusa con Git per generare la chiave SSH. In alternariva, puoi usare [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) and [PuTTYgen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Una volta create la chiave SSH, specifica il path della chiave pubblica nella proprietà `authorize` del file `Homestead.yaml`.

#### Configura le Cartelle Condivise

La proprietà `folders` nel file `Homestead.yaml` elenca tutte le cartelle che vengono condivise tra la tua macchina locale e quella virtuale. Ad ogni cambiamento di uno di questi file, questi vengono sincronizzati tra le due macchine. Puoi configurare quante cartelle condivise hai bisogno, se necessario:

	folders:
	    - map: ~/Code
	      to: /home/vagrant/Code

Per abilitare [NFS](http://docs.vagrantup.com/v2/synced-folders/nfs.html), aggiungi un flag alla tua configurazione:

	folders:
	    - map: ~/Code
	      to: /home/vagrant/Code
	      type: "nfs"

#### Configura i siti Nginx

Non sei familiare con il mondo Nginx? E che problema c'è? La proprietà `sites` permette di mappare un certo "dominio" con una cartella del tuo ambiente Homestead. Una configurazione di esempio è già presente in Homestead.yaml. Esattamente come per le cartelle condivise, puoi aggiungerne quanti ne vuoi. Homestead può garantire un conveniente, ambiente virtualizzato per goni progetto Laravel al quale stai lavorando:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public

Puoi anche specificare per quali siti usare [HHVM](http://hhvm.com) impostando l'opzione `hhvm` a `true`:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public
	      hhvm: true

Di default, ogni sito sarà accessibile tramite protocollo HTTP sulla porta 8000 e tramite protocollo HTTPS sulla porta 44300.

#### Il File Hosts

Non dimenticare di aggiungere il “dominio” per i tuoi siti Nginx al file `hosts` sul tuo computer! Il file `hosts` reindirizzerà le tue richieste per il dominio locale all'interno dell'ambiente Homestead. Su Mac e Linux, questo file si trova in `/etc/hosts`. Su Windows, lo trovi in `C:\Windows\System32\drivers\etc\hosts`. Questa linea da aggiungere a questo file dovrebbe essere come la seguente:

	192.168.10.10  homestead.app

Assicurati che l'indirizzo IP della lista sia settato nel file `Homestead.yaml`. Una volta aggiunto il dominio al file `hosts`, puoi accedere al sito tramite browser!

	http://homestead.app

<a name="avviare-vagrant-box"></a>
### Avviare La Vagrant Box

Una volta modificato il file `Homestead.yaml`, esegui il comando `vagrant up` dalla cartella Homestead. Vagrant avvierà la macchia virtuale e automaticamente configurerà le tue cartelle condivise e i tuoi siti Nginx automaticamente.

Per distruggere la macchina, puoi usare il comando `vagrant destroy --force`.

<a name="uso-quotidiano"></a>
## Uso Quotidiano

<a name="connessione-tramite-ssh"></a>
### Connessione tramite SSH

Puoi connetterti nella tua macchina virtuale tramite SSH digitando il comando `vagrant ssh` dalla tua cartella Homestead.

Ma, se dovrai accedere frequentemente tramite SSH alla tua macchina Homestad, prendi in considerazione la creazione di un "alias" sulla macchina locale per accedere più velocemente tramite SSH nel box Homestead. Una volta creato l'alias, usa semplicemente il comando "vm" 
per connetterti tramite SSH nella tua macchina Homestead da qualsiasi punto del tuo sistema:

	alias vm="ssh vagrant@127.0.0.1 -p 2222"

<a name="connessione-database"></a>
### Connessione ai Database

Un database homestead è già pronto per essere usato in caso di bisogno, sia in MySQL che in Postgres. Per una maggiore convenienza, inoltre, Laravel è normalmente configurato per usare di default questo database.
Per connetterti al tuo database sulla macchina virtuale dalla macchina fisica, non devi fare altro che usare l'IP `127.0.0.1` con la porta 33060 (MySQL) o 54320 (Postgres). Lo username e la password di default sono, in entrambi i casi, `homestead` / `secret`.

> **Nota:** dovresti usare sempre queste porte non-standard in caso di connessione al database dalla macchina fisica principale. Nei tuoi file di configurazione di Laravel invece userai la 3306 e 5432, dato che l'applicazione viene eseguita sulla macchina virtuale. 

<a name="aggiunta-altri-siti"></a>
### Aggiunta di Altri Siti

Una volta che il tuo sistema è avviato ed attivo, potresti voler aggiungere altri siti al file di configurazione. Puoi farlo tranquillamente modificando come meglio ritieni il file Homestead.yaml, quindi provvedendo ad eseguire il comando `vagrant provision`.

> **Nota:** Questo processo è distruttivo. Quando si esegue il comando `provision`, i tuoi database esistenti verrano distrutti e poi ricreati.

<a name="porte"></a>
### Porte

Di default, le seguenti porte sono già state sistemate per lavorare con Homestead:

- **SSH:** 2222 &rarr; Forwards alla 22
- **HTTP:** 8000 &rarr; Forwards alla 80
- **HTTPS:** 44300 &rarr; Forwards alla 443
- **MySQL:** 33060 &rarr; Forwards alla 3306
- **Postgres:** 54320 &rarr; Forwards alla 5432

#### Forward di Porte Aggiuntivi

Se lo desideri, puoi aggiungere forward aggiuntivi alle porte per Vagrant, specificando il loro protocollo:

	ports:
	    - send: 93000
	      to: 9300
	    - send: 7777
	      to: 777
	      protocol: udp

<a name="blackfire-profiler"></a>
## Blackfire Profiler

[Blackfire Profiler](https://blackfire.io) di SensioLabs raccoglie automaticamente i dati sull' esecuzione del codice, ad esempio RAM, tempo di esecuzione della CPU, e l'I/O del disco. Homestead rende facile utilizzare questo profiler per le proprie applicazioni. 

Tutti i package necessari sono già stati installati nel box Homestead, imposta semplicemente impostare l'id e il token del **Server** Blackfire nel tuo file `Homestead.yaml` file:

	blackfire:
	    - id: your-server-id
	      token: your-server-token
	      client-id: your-client-id
	      client-token: your-client-token

Una volta configurate le tue credenziali di Blackfire, ri esegui il comando `vagrant provision` dalla tua directory Homestead. Ovviamente, assicurati di rileggerti la [documentazione Blackfire](https://blackfire.io/getting-started) per imparare come installare le estensioni Blackfire per il tuo browser web.
