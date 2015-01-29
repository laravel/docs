# Contribuire

- [Bug Report](#bug-report)
- [Discussioni sullo Sviluppo del Core](#discussioni-sviluppo-core)
- [Quale Branch?](#quale-branch)
- [Vulnerabilità e Sicurezza](#vulenarabilita-sicurezza)
- [Coding Style](#coding-style)

<a name="bug-reports"></a>
## Bug Reports

Per incoraggiare una collaborazione più attiva, Laravel raccomanda fortemente le pull request, senza limitarsi al bug reporting. Un "bug report" può comunque essere inviato sotto forma di una pull request contenente un test fallito.

Tuttavia, se dovessi decidere di inviare un bug report, cerca di indicare nel modo più chiaro possibile il titolo ed una descrizione del problema. Dovresti inoltre inserire quante più informazioni ed un esempio di codice che dimostri tale problema. L'obiettivo di un bug report è migliorare la tua vita (e quella di altri).

Ad ogni modo, non aspettarti una risoluzione automatica del bug: vediamo i bug report come un invito (ad altri) a collaborare al progetto.

Tutto il codice sorgente di Laravel è ospitato su GitHub. Ci sono svariati repository a disposizione:

- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Cashier](https://github.com/laravel/cashier)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Website](https://github.com/laravel/laravel.com)
- [Laravel Art](https://github.com/laravel/art)

<a name="discussioni-sviluppo-core"></a>
## Discussioni sullo Sviluppo del Core

Le discussioni riguardo bug, nuove feature ed implementazioni di feature esistenti si svolgono nel canale `#laravel-dev` su IRC (Freenode). Potrai trovarci Taylor Otwell, creatore di Laravel, durante la settimana dalle 8am alle 5pm (UTC-06:00, America/Chicago). Sporadicamente lo puoi trovare anche in altri momenti oltre quelli citati.

Il canale `#laravel-dev` è aperto a tutti, per cui sei il benvenuto anche solo per osservare cosa succede.

<a name="quale-branch"></a>
## Quale Branch?

**Tutti** i bug fix dovrebbero essere inviati alla versione stable più recente. Non bisogna mai inviare un bug fix alla versione **master** del progetto.

**Le Feature Minori** che sono **totalmente retrocompatibili** con la release attuale di Laravel possono essere inviate all'ultima branch stable.

**Le Feature Maggiori** di nuova introduzione dovrebbero essere inviate alla *master* branch, che contiene la versione "in arrivo" di Laravel.

Se non sei sicuro di come regolarti, chiedi direttamente a Taylor in `#laravel-dev`.

<a name="vulenarabilita-sicurezza"></a>
## Vulnerabilità e Sicurezza

Se scopri una vulnerabilità di sicurezza in Laravel, invia una mail a Taylor Otwell all'indirizzo <a href="mailto:taylorotwell@gmail.com">taylorotwell@gmail.com</a>. Ogni vulnerabilità riguardante la sicurezza verrà prontamente sistemata.

<a name="coding-style"></a>
## Coding Style

Laravel segue lo standard [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md) e [PSR-1](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-1-basic-coding-standard.md) per quanto riguarda la scrittura del codice.

In aggiunta a questi standard, è possibile seguire queste comode linee guida:

- La dichiarazione del namespace di una classe dovrebbe trovarsi sulla stessa linea di `<?php`.
- La parentesi graffa di apertura di una classe `{` deve trovarsi sulla stessa linea del nome della classe.
- Funzioni e controlli devono usare lo stile di Allman nella scrittura delle parentesi.
- Indenta con tab, allinea con gli spazi.

Per chi non ne fosse a conoscenza, questo è lo stile di Allman.

	while ($x == $y)
	{
	    something();
	    somethingelse();
	}

	function myFunction()
	{
		// logica qui...
	}
