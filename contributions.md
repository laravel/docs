# Guida Di Contribuzione

- [Bug Reports](#bug-reports)
- [Discussioni sullo Sviluppo del Core](#discussioni-sviluppo-core)
- [Quale Branch?](#quale-branch)
- [Vulnerabilità e Sicurezza](#vulnerabilita-e-sicurezza)
- [Coding Style](#coding-style)

<a name="bug-reports"></a>
## Bug Reports

Per incoraggiare una collaborazione più attiva, Laravel raccomanda fortemente le pull request, senza limitarsi al bug reporting. Un "bug report" può comunque essere inviato sotto forma di una pull request contenente un test fallito.

Tuttavia, se dovessi decidere di inviare un bug report, cerca di indicare nel modo più chiaro possibile il titolo ed una descrizione del problema. Dovresti inoltre inserire quante più informazioni ed un esempio di codice che dimostri tale problema. L'obiettivo di un bug report è migliorare la tua vita (e quella di altri). 

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

Le discussioni riguardanti i bug, nuove feautre, ed implementazioni di feature esistenti si svolgono nel canale `#internals` di Slack team [LaraChat](http://larachat.co). Taylor Otwelll, solitamente sarà presnete nel canale  typically present in the channel nei giorni feriali dalle 8am-5pm (UTC-06:00, America/Chicago), Sporadicamente lo puoi trovare anche in altri momenti oltre quelli citati.

<a name="quale-branch"></a>
## Quale Branch?

**Tutti** i bug fix dovrebbero essere inviati alla versione stable più recente. Non bisogna **mai** inviare un bug fix alla versione master del progetto.

Le Feature **Minori** che sono **totalmente retrocompatibili** con la release attuale di Laravel possono essere inviate all'ultima branch stable.

Le Feature **Maggiori** di nuova introduzione dovrebbero essere inviate alla master branch, che contiene la versione "in arrivo" di Laravel.

Se non sei sicuro di come regolarti, chiedi direttamente a Taylor nel IRC canale `#laravel-dev`.

<a name="vulnerabilita-e-sicurezza"></a>
## Vulnerabilità e Sicurezza

Se scopri una vulnerabilità di sicurezza in Laravel, invia una mail a Taylor Otwell all'indirizzo <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. Ogni vulnerabilità riguardante la sicurezza verrà prontamente sistemata.

<a name="coding-style"></a>
## Coding Style

Laravel segue lo standard [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) per la scrittura del codice e lo standard [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) per l'autoloading standard.
