# Laravel Elixir

- [Introduzione](#introduzione)
- [Installazione & Setup](#installazione)
- [Avviare Elixir](#avviare-elixir)
- [Lavorare Con gli Stylesheet](#lavorare-con-gli-stylesheet)
	- [Less](#less)
	- [Sass](#sass)
	- [Plain CSS](#plain-css)
	- [Source Maps](#css-source-maps)
- [Lavorare con gli Script](#lavorare-con-gli-script)
	- [CoffeeScript](#coffeescript)
	- [Browserify](#browserify)
	- [Babel](#babel)
	- [Script](#javascript)
- [Versionamento / Cache Busting](#versionamento-e-cache-busting)
- [Richiamare Task Gulp Esistenti](#richiamare-task-gulp-esistenti)
- [Creare Estensioni Per Elixir](#creare-estensioni-per-elixir)

<a name="introduzione"></a>
## Introduzione

Laravel Elixir fornisce delle API per definire dei task [Gulp](http://gulpjs.com) per la tua applicazione. Elixir supporta molti comuni pre-processori CSS e JavaScript e supporta anche molti strumenti per il testing. Utilizzando il concatenamento dei metodi, Elixir to permette di impostare delle pipeline per i tuoi asset. Per esempio:


	elixir(function(mix) {
		mix.sass('app.scss')
	 		.coffee('app.coffee');
	});


Se hai già provato ad utilizzare Gulp per compilare gli asset ma questo ti ha solo confuso le idee, amerai Elixir. Elixir non è uno strumento necessario per lo sviluppo della tua applicazione, sei libero di utilizzare qualsiasi altro strumento tu voglia.

<a name="installazione"></a>
## Installazione & Setup

### Installare Node

Prima di utilizzare Elixir, devi assicurarti che Node.js sia installato sulla tua macchina.

    node -v

Laravel Homestead include già tutto quello di cui hai bisogno; se non stai utilizzando Vagrant, puoi facilmente installare Node visitando [la loro pagina di download](http://nodejs.org/download/).

### Gulp

Il secondo passo è quello di installare [Gulp](http://gulpjs.com) come pacchetto globale:

    npm install --global gulp

### Laravel Elixir

Il passo finale è quello di installare Elixir! In una nuova installazione di Laravel troverai nella root principale un file chiamato `package.json`. Questo file è molto simile al file `composer.json`, tranne per il fatto che questo definisce le dipendenze di Node. Puoi installare tutte le dipendenze del file semplicemente digitando:

	npm install

<a name="running-elixir"></a>
## Avviare Elixir

Elixir è costruito su [Gulp](http://gulpjs.com), quindi per avviare i tuoi task è sufficiente utilizzare il comando `gulp` dal tuo terminale. Aggiungendo il flag `--production` Elixir eseguirà la minimizzazione ( minify ) dei file CSS e JavaScript:

	// Esegui tutti i task...
	gulp

	// Esegui tutti i task e minimizza tutti i file CSS e JavaScript...
	gulp --production

#### Controlla Se Gli Asset Vengono Modificati

Eseguire ogni volta il comando `gulp` nel terminale ogni volta che si aggiorna un file è una operazione ripetitiva e noiosa. per questo motivo puoi usare il comando `gulp watch` che continuerà a controllare tutti i tuoi file e, se noterà un cambiamento, si occuperà di compilare automaticamente tutte le risorse.

	gulp watch

<a name="lavorare-con-gli-stylesheet"></a>
## Lavorare Con gli Stylesheet

Il file `gulpfile.js` che si trova nella root del progetto contiene tutti i task di Elixir. I task possono essere concatenati in modo da definire esattamente come gli asset devono essere compilati.

<a name="less"></a>
### Less

Per compilare [Less](http://lesscss.org/) in CSS, devi utilizzare il metodo `less`. Il metodo `less` assume che i tuoi file siano salvati nella cartella `resources/assets/less`. Per default, una volta compilati i file questi vengono salvati in `public/css/app.css`:


	elixir(function(mix) {
		mix.less("app.less");
	});


Puoi combinare più file Less all'interno di un unico file CSS. Anche in questo caso il file generato sarà salvato in `public/css/app.css`. Se preferisci utilizzare un percorso diverso per il file di output lo puoi fare passandolo al metodo `less` come secondo argomento:

	elixir(function(mix) {
		mix.less([
			"app.less",
			"controllers.less"
		], "public/assets/css");
	});

<a name="sass"></a>
### Sass

Il metodo `sass` ti consente di compilare [Sass](http://sass-lang.com/) in CSS. Elixir assumerà che i file siano salvati all'interno della cartella `resources/assets/sass`, puoi utilizzare il comando in questo modo:

	elixir(function(mix) {
		mix.sass("app.scss");
	});

Come già detto per il metodo `less`, puoi compilare più file in un unico CSS e puoi cambiare la destinazione a tuo piacimento:

	elixir(function(mix) {
		mix.sass([
			"app.scss",
			"controllers.scss"
		], "public/assets/css");
	});

#### Ruby Sass

Dietro le quinte, Elixir utilizza la libreria LibSass per la compilazione dei file. In alcuni casi, potrebbe tornarti utile la versione Ruby che, seppur più lenta, ha molte più funzionalità. Assumendo che tu abbia sia la versione Sass che Ruby installata (`gem install sass`), puoi utilizzare il compilatore Ruby in questo modo:

	elixir(function(mix) {
		mix.rubySass("app.scss");
	});

<a name="plain-css"></a>
### Plain CSS

Se hai bisogno di combinare dei semplici file CSS in un unico file, puoi utilizzare il metodo `styles`. I Path passati a questo metodo sono relativi alla cartella `resources/assets/css` e saranno salvati in `public/css/all.css`:

	elixir(function(mix) {
		mix.styles([
			"normalize.css",
			"main.css"
		]);
	});

Anche in questo caso puoi definire un percorso diverso come cartella di uscita:

	elixir(function(mix) {
		mix.styles([
			"normalize.css",
			"main.css"
		], "public/assets/css");
	});

<a name="css-source-maps"></a>
### Source Maps

Le Source map sono abilitate di default. Quindi per ogni file compilato troverai anche il corrispettivo `*.css.map` all'interno della stessa cartella. Questa mappatura ti permette di tenere traccia degli stili compilati.

Se non vuoi che le source map siano generate per i CSS puoi disabilitarle attraverso una opzione nella configurazione:

	elixir.config.sourcemaps = false;

	elixir(function(mix) {
		mix.sass("app.scss");
	});

<a name="lavorare-con-gli-script"></a>
## Lavorare Con Gli Script

Elixir fornisce anche diverse funzioni che ti aiutano a lavorare con i file JavaScript come ad esempio la compilazione ECMAScript 6, CoffeeScript, Browserify, minimizzazione ( minify ), e la più semplice concatenazione di file.

<a name="coffeescript"></a>
### CoffeeScript

Il metodo `coffee` può essere usato per compilare [CoffeeScript](http://coffeescript.org/) in normale JavaScript. La funzione `coffee` accetta un array di file CoffeeScript salvati nella cartella `resources/assets/coffee` e genera un singolo file chiamato `app.js` all'interno della cartella `public/js`:

	elixir(function(mix) {
		mix.coffee(['app.coffee', 'controllers.coffee']);
	});

<a name="browserify"></a>
### Browserify

Elixir possiede anche il metodo `browserify`.

Questo task assume che i file siano salvati in `resources/assets/js` e creerò un unico file in `public/js/bundle.js`:

elixir(function(mix) {
	mix.browserify('index.js');
});

<a name="babel"></a>
### Babel

Il metodo `babel` può essere utilizzato per compilare [EcmaScript 6 and 7](https://babeljs.io/docs/learn-es2015/) in semplice JavaScript. Questa funzione accetta un array di file salvati nella cartella `resources/assets/js` e genera un singolo file chiamato `all.js` all'interno della cartella `public/js`:

	elixir(function(mix) {
		mix.babel([
      		"order.js",
          "product.js"
      ]);
	});

Per cambiare la cartella di destinazione puoi semplicemente indicarla come secondo argomento della funzione. Questa funzione è del tutto identica a `mix.scripts()`, in più si occupa di compilare i file Babel.


<a name="javascript"></a>
### Script

Se hai più file JavaScript e li fuoi unire in un unico file puoi usare il metodo `scripts`.

Il metodo `scripts` assume che tutti i Path siano relativi alla cartella `resources/assets/js`, e creerà il nuovo file all'interno di `public/js/all.js`:

	elixir(function(mix) {
		mix.scripts([
			"jquery.js",
			"app.js"
		]);
	});

Se hai bisogno di concatenare più categorie di file puoi fare più chiamate al metodo `scripts`. Il secondo argomento definisce il nome del file risultante:

	elixir(function(mix) {
   	 	mix.scripts(['app.js', 'controllers.js'], 'public/js/app.js')
   	    	.scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
	});

Se hai bisogno di cobinare tutte gli script che si trovano all'interno di una cartella puoi utilizzare il metodo `scriptsIn`. Il risultato sarà salvato in `public/js/all.js`:

	elixir(function(mix) {
		mix.scriptsIn("public/js/some/directory");
	});

<a name="versionamento-e-cache-busting"></a>
## Versionamento / Cache Busting

Molti sviluppatori fanno in modo di aggiungere un timestamp come suffisso ai loro asset compilati così da forzare i browser a riscaricare la risorsa in caso di cambiamenti. Elixir è in grado di aiutarti anche in questo aspetto mettendoti a disposizione il metodo `version`.

Il metodo `version` accetta il nome del file della risorsa relativamente alla cartella `public`, e farà in modo di aggiungere un hash univoco al nome del file permettendoti di sfruttare al massimo la cache e fare in modo che i browser riscarichino le risorse quando necessario. Per esempio il nome generato sarà qualcosa di simile a: `all-16d570a7.css`:

	elixir(function(mix) {
		mix.version("css/all.css");
	});

Dopo aver generato il file, puoi utilizzare all'interno delle [view](/docs/5.1/view) l'helper `elixir` che è una funzione globale di Laravel che automaticamente caricherà la risorsa corretta:

	<link rel="stylesheet" href="{{ elixir('css/all.css') }}">

#### Versionare Più File

Puoi anche passare un array al metodo `version` per poter versionare più file:

	elixir(function(mix) {
		mix.version(["css/all.css", "js/app.js"]);
	});

Una volta generati i file puoi usare l'helper `elixir` per generare l'url al file. Ricorda, devi solo passare il nome del file alla funzione `elixir`. Il nome con l'hash verrà ricavato in modo automatico:

	<link rel="stylesheet" href="{{ elixir('css/all.css') }}">

	<script src="{{ elixir('js/app.js') }}"></script>

<a name="richiamare-task-gulp-esistenti"></a>
## Richiamare Task Gulp Esistenti

Se hai bisogno di richiamare un pre-esistente task di Gulp attraverso Elixir, puoi farlo utilizzando il metodo `task`. Per esempio, immagina di avere un task Gulp che ogni volta che viene chiamato mostra un testo nella console:

	gulp.task("speak", function() {
		var message = "Tea...Earl Grey...Hot";

		gulp.src("").pipe(shell("say " + message));
	});

Se hai bisogno di richiamare questo task con Elixir, usa il metodo `mix.task` e passa come argomento il nome del task:

	elixir(function(mix) {
   		mix.task('speak');
	});

#### Watcher Personalizzati

Se hai bisogno di creare un watcher che avvii dei task personalizzati ogni volta che un file viene modificato, puoi farlo passando una espressione regolare come secondo argomento al metodo `task`:

	elixir(function(mix) {
   		mix.task('speak', 'app/**/*.php');
	});

<a name="creare-estensioni-per-elixir"></a>
## Creare Estensioni Per Elixir

Se hai bisogno di più flessibilità di quella che può darti il metodo `task` di Elixir, puoi crearti una tua estensione. Le estensioni Elixir ti consentono di passare argomenti ai tuoi task personali. Per esempio puoi creare una estensione in questo modo:

	// File: elixir-extensions.js

	var gulp = require("gulp");
	var shell = require("gulp-shell");
	var elixir = require("laravel-elixir");

	elixir.extend("speak", function(message) {

		gulp.task("speak", function() {
			gulp.src("").pipe(shell("say " + message));
		});

		return this.queueTask("speak");

	 });

Tutto qui! Puoi inserirlo sia all'inizio del tuo Gulpfile, oppure in un file separato. Per esempio se salvi la tua estensione in `elixir-extensions.js`, puoi richiamare il file dal `Gulpfile` principale in questo modo:

	// File: Gulpfile.js

	var elixir = require("laravel-elixir");

	require("./elixir-tasks")

	elixir(function(mix) {
		mix.speak("Tea, Earl Grey, Hot");
	});

#### Watcher personalizzati

Se vuoi che un task personalizzato venga avviato quando esegui il comando `gulp watch`, puoi registrare il tuo watcher:

	this.registerWatcher("speak", "app/**/*.php");

	return this.queueTask("speak");
