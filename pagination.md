# Pagination

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)
	- [Paginare i Risultati del Query Builder](#paginare-risultati-query-builder)
	- [Paginare i Risultati di Eloquent](#paginare-risultati-eloquent)
	- [Creare Manualmente un Paginator](#creare-manualmente-paginator)
- [Mostrare i Risultati in una View](#mostrare-risultati-view)
- [Convertire i Risultati in JSON](#convertire-risultati-json)

<a name="introduzione"></a>
## Introduzione

In alcuni framework implementare la paginazione dei dati può essere davvero molto, molto doloroso. In Laravel per fortuna è tutto molto più semplice. Automaticamente, infatti, è capace di generare tutto l'insieme di tag e link necessari, tra l'altro compatibili con [Bootstrap](http://getbootstrap.com/)!

<a name="uso-base"></a>
## Uso Base

<a name="paginare-risultati-query-builder"></a>
### Paginare i Risultati del Query Builder

Ci sono svariati modi di paginare degli elementi. Quello più semplice, sicuramente, è l'uso di _paginate_ del [query builder](/docs/5.1/queries) o di un [model Eloquent](/docs/5.1/eloquent). Il metodo `paginate` è presente out of the box in Laravel e fornisce tutto il necessario a creare i link adatti, partendo da un semplice parametro GET _?page_. Tale valore sarebbe automaticamente gestito da Laravel, che si occuperebbe di inserirlo nei vari link generati dal paginatore.

Tuttavia, una cosa alla volta. Innanzitutto, vediamo come usare il metodo _paginate_ su una query. In questo esempio l'unico argomento passato è il numero di elementi da mostrare "per pagina". 

	<?php namespace App\Http\Controllers;

	use DB;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show all of the users for the application.
		 *
		 * @return Response
		 */
		public function index()
		{
			$users = DB::table('users')->paginate(15);

			return view('user.index', ['users' => $users]);
		}
	}

> **Nota:** al momento, le operazioni di paginazione che usano _groupBy_ non possono essere eseguite in modo molto efficace da Laravel. Il consiglio che ti diamo è, in tal caso, di usare un manual paginator.

#### "Paginazione Semplice"

Se vuoi mostrare solo dei semplici link _Precedenti_ e _Successivi_, puoi usare il metodo _simplePaginate_ per effettuare una query ancora più performante. Può essere un soluzione molto utile per dataset grandi e per i quali NON hai bisogno di mostrare i link per ogni singola pagina.

	$users = DB::table('users')->simplePaginate(15);

<a name="paginare-risultati-eloquent"></a>
### Paginare i Risultati di Eloquent

Puoi anche paginare i risultati ottenuti usando [Eloquent](/docs/5.1/eloquent). In questo esempio di seguito, pagineremo i risultati partendo dal model _User_. Precisamente, quindici risultati per pagina. La sintassi è praticamente identica.

	$users = App\User::paginate(15);

Ovviamente, puoi anche richiamare il metodo _paginate_ dopo aver definito alcune condizioni sulla query.

	$users = User::where('votes', '>', 100)->paginate(15);

Anche qui, infine, puoi usare _simplePaginate_.

	$users = User::where('votes', '>', 100)->simplePaginate(15);

<a name="creare-manualmente-paginator"></a>
### Creare Manualmente un Paginator

A volte, potresti avere la necessità di creare manualmente un'istanza di un paginator, partendo magari da un array di elementi. Puoi farlo partendo da un'istanza di Illuminate\Pagination\Paginator` o `Illuminate\Pagination\LengthAwarePaginator`, in base alle tue necessità.

La classe _Paginator_ non ha bisogno di sapere il numero totale degli elementi nel set risultante. Tuttavia, per questo motivo, tale classe non ha i metodi per recuperare l'indice dell'ultima pagina. La classe `LengthAwarePaginator` prende più o meno gli stessi parametri in input di _Paginator_. Tuttavia, ha bisogno di sapere il conteggio preciso degli elementi nel set.

In altre parole, _Paginator_ corrisponde al _simplePaginate_ visto prima. Mentre `LengthAwarePaginator` viene usato per _paginate_.

In fase di creazione manuale di un paginator potresti avere la necessità di "affettare" l'array in più parti uguali. Se non sei sicuro sul come muoverti, dai un'occhiata alla funzione PHP [array_slice](http://php.net/manual/en/function.array-slice.php).

<a name="mostrare-risultati-view"></a>
## Mostrare i Risultati in una View

Quando chiami il metodo _paginate_ o _simplePaginate_ sul query builder o Eloquent, ti ritroverai con un'istanza del paginator. Due istanze diverse, in realtà: di `Illuminate\Pagination\Paginator` (_simplePaginate_) oppure di `Illuminate\Pagination\LengthAwarePaginator` (_paginate_). Questi oggetti contengono i risultati, insieme ad una serie di metodi di comodo da usare, come ad esempio _render_.

	<div class="container">
		@foreach ($users as $user)
			{{ $user->name }}
		@endforeach
	</div>

	{!! $users->render() !!}

Il metodo _render_ si occuperà, automaticamente, di disegnare tutti i link necessari alla paginazione. Tali link conterranno già tutti gli attributi necessari per lavorare con [Bootstrap CSS framework](https://getbootstrap.com), oltre a degli URL contenenti il "?page" di cui abbiamo parlato in precedenza.

> **Nota:** ricorda che se stai usando Blade, devi effettuare l'output dei link usando {!! e !!}, visto che non devi effettuarne l'escape.

#### Personalizzare l'URI del Paginator

Il metodo _setPath_ ti permette di personalizzare l'URI usato dal paginator in fase di generazione dei link. Ad esempio, nel caso in cui volessi far generare al paginator dei link nel formato `http://example.com/custom/url?page=N`, dovresti specificare:

	Route::get('users', function () {
		$users = App\User::paginate(15);

		$users->setPath('custom/url');

		//
	});

#### Aggiungere Informazioni ai Link

Se vuoi, puoi aggiungere altre informazioni aggiuntive ai link generati dal paginator tramite il metodo _appends_. Supponiamo di voler aggiungere `&sort=yes` ad ogni singolo link. Come fare?

Così:

	{!! $users->appends(['sort' => 'votes'])->render() !!}

Inoltre, se preferisci, puoi anche decidere di aggiungere un "hash fragment" ad ogni URL. Ad esempio, nel caso in cui volessimo aggiungere _#foo_ alla fine di ogni link, dovremmo scrivere...

	{!! $users->fragment('foo')->render() !!}

#### Metodi Helper Aggiuntivi

Oltre ai metodi appena visti ce ne sono anche altri! Eccoli. Scommetto che sono anche semplici da comprendere...

- `$results->count()`
- `$results->currentPage()`
- `$results->hasMorePages()`
- `$results->lastPage() (Not available when using simplePaginate)`
- `$results->nextPageUrl()`
- `$results->perPage()`
- `$results->total() (Not available when using simplePaginate)`
- `$results->url($page)`

<a name="convertire-risultati-json"></a>
## Convertire i Risultati in JSON

Il paginator di Laravel implementa il contract `Illuminate\Contracts\Support\JsonableInterface` ed espone il metodo `toJson`. Di conseguenza, sappi che è davvero semplice convertire in JSON il risultato di questa operazione.

Innanzitutto, ricorda che puoi convertire in JSON automaticamente un risultato di paginazione se ritorni da una route o da una action di un controller tale risultato.

	Route::get('users', function () {
		return App\User::paginate();
	});

Le informazioni incluse saranno tutte quelle meta informazioni indispensabili come _total_, *current_page*, *last_page* e così via. Ecco come apparirà un JSON di esempio partendo dal risultato di una paginazione.

#### Esempio di JSON

	{
	   "total": 50,
	   "per_page": 15,
	   "current_page": 1,
	   "last_page": 4,
	   "next_page_url": "http://laravel.app?page=2",
	   "prev_page_url": null,
	   "from": 1,
	   "to": 15,
	   "data":[
			{
				// Result Object
			},
			{
				// Result Object
			}
	   ]
	}
