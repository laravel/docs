# Eloquent: Collection

- [Introduzione](#introduzione)
- [Metodi Disponibili](#metodi-disponibili)
- [Collection Personalizzate](#collection-personalizzate)

<a name="introduzione"></a>
## Introduzione

Tutti i set di risultati (non le singole istanze, ma i set) sono a loro volta istanze della classe `Illuminate\Database\Eloquent\Collection`. Tale classe estende a sua volta la [base collection](/docs/5.1/collection). Molti dei metodi ereditati, quindi, sono quelli della classe base, adattati però a lavorare bene con le istanze dei model Eloquent.

Ovviamente, ogni collection serve anche da iteratore, permettendoti di "loopare" al suo interno come fosse un semplice array:

	$users = App\User::where('active', 1)->get();

	foreach ($users as $user) {
		echo $user->name;
	}

Tuttavia, le collection sono molto più potenti di quello che sembrano. Tra le varie cose interessanti, ad esempio, espongono alcuni metodi dedicati alle operazioni di map/reduce sugli elementi.

Facciamo una prova: rimuoviamo tutti i model degli utenti inattivi e raccogliamo i nomi dei rimanenti.

	$users = App\User::where('active', 1)->get();

	$names = $users->reject(function ($user) {
		return $user->active === false;
	})
	->map(function ($user) {
		return $user->name;
	});

<a name="metodi-disponibili"></a>
## Metodi Disponibili

### La Collection Base

Tutte le Eloquent collection estendono la [base collection](/docs/5.1/collection) di Laravel. Ad ogni modo, ereditano tutti i gli utili metodi della classe base:

* [all](/docs/5.1/collection#metodo-all)
* [chunk](/docs/5.1/collection#metodo-chunk)
* [collapse](/docs/5.1/collection#metodo-collapse)
* [contains](/docs/5.1/collection#metodo-contains)
* [count](/docs/5.1/collection#metodo-count)
* [diff](/docs/5.1/collection#metodo-diff)
* [each](/docs/5.1/collection#metodo-each)
* [filter](/docs/5.1/collection#metodo-filter)
* [first](/docs/5.1/collection#metodo-first)
* [flatten](/docs/5.1/collection#metodo-flatten)
* [flip](/docs/5.1/collection#metodo-flip)
* [forget](/docs/5.1/collection#metodo-forget)
* [forPage](/docs/5.1/collection#metodo-forpage)
* [get](/docs/5.1/collection#metodo-get)
* [groupBy](/docs/5.1/collection#metodo-groupby)
* [has](/docs/5.1/collection#metodo-has)
* [implode](/docs/5.1/collection#metodo-implode)
* [intersect](/docs/5.1/collection#metodo-intersect)
* [isEmpty](/docs/5.1/collection#metodo-isempty)
* [keyBy](/docs/5.1/collection#metodo-keyby)
* [keys](/docs/5.1/collection#metodo-keys)
* [last](/docs/5.1/collection#metodo-last)
* [map](/docs/5.1/collection#metodo-map)
* [merge](/docs/5.1/collection#metodo-merge)
* [pluck](/docs/5.1/collection#metodo-pluck)
* [pop](/docs/5.1/collection#metodo-pop)
* [prepend](/docs/5.1/collection#metodo-prepend)
* [pull](/docs/5.1/collection#metodo-pull)
* [push](/docs/5.1/collection#metodo-push)
* [put](/docs/5.1/collection#metodo-put)
* [random](/docs/5.1/collection#metodo-random)
* [reduce](/docs/5.1/collection#metodo-reduce)
* [reject](/docs/5.1/collection#metodo-reject)
* [reverse](/docs/5.1/collection#metodo-reverse)
* [search](/docs/5.1/collection#metodo-search)
* [shift](/docs/5.1/collection#metodo-shift)
* [shuffle](/docs/5.1/collection#metodo-shuffle)
* [slice](/docs/5.1/collection#metodo-slice)
* [sort](/docs/5.1/collection#metodo-sort)
* [sortBy](/docs/5.1/collection#metodo-sortby)
* [sortByDesc](/docs/5.1/collection#metodo-sortbydesc)
* [splice](/docs/5.1/collection#metodo-splice)
* [sum](/docs/5.1/collection#metodo-sum)
* [take](/docs/5.1/collection#metodo-take)
* [toArray](/docs/5.1/collection#metodo-toarray)
* [toJson](/docs/5.1/collection#metodo-tojson)
* [transform](/docs/5.1/collection#metodo-transform)
* [unique](/docs/5.1/collection#metodo-unique)
* [values](/docs/5.1/collection#metodo-values)
* [where](/docs/5.1/collection#metodo-where)
* [whereLoose](/docs/5.1/collection#metodo-whereloose)
* [zip](/docs/5.1/collection#metodo-zip)

<a name="collection-personalizzate"></a>
## Collection Personalizzate

Potresti aver bisogno di usare, per un tuo model in particolare, una _Collection_ personalizzata da estendere con i tuoi metodi. Nessun problema, effettua l'override del metodo _newCollection_ nel tuo model.

	<?php namespace App;

	use App\CustomCollection;
	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Create a new Eloquent Collection instance.
		 *
		 * @param  array  $models
		 * @return \Illuminate\Database\Eloquent\Collection
		 */
		public function newCollection(array $models = [])
		{
			return new CustomCollection($models);
		}
	}

Una volta definito il metodo _newCollection_, riceverai un'istanza della collection personalizzata ogni volta che Eloquent ritornerà un'istanza di una collection per tale model. Per intenderci, verrà ritornata la tua collection personalizzata ogni volta che userai i metodi _get_, _all_ e così via.
