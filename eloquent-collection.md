# Eloquent: Collection

- [Introduzione](#introduzione)
- [Metodi Disponibili](#metodi-disponibili)
- [Collection Personalizzate](#collection-personalizzate)

<a name="introduzione"></a>
## Introduzione

Tutti i set di risultati (non le singole istanze, ma i set) sono a loro volta istanze della classe `Illuminate\Database\Eloquent\Collection`. Tale classe estende a sua volta la [base collection](/documentazione/5.1/collection). Molti dei metodi ereditati, quindi, sono quelli della classe base, adattati però a lavorare bene con le istanze dei model Eloquent.

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

Tutte le Eloquent collection estendono la [base collection](/documentazione/5.1/collection) di Laravel. Ad ogni modo, ereditano tutti i gli utili metodi della classe base:

* [all](/documentazione/5.1/collection#metodo-all)
* [chunk](/documentazione/5.1/collection#metodo-chunk)
* [collapse](/documentazione/5.1/collection#metodo-collapse)
* [contains](/documentazione/5.1/collection#metodo-contains)
* [count](/documentazione/5.1/collection#metodo-count)
* [diff](/documentazione/5.1/collection#metodo-diff)
* [each](/documentazione/5.1/collection#metodo-each)
* [filter](/documentazione/5.1/collection#metodo-filter)
* [first](/documentazione/5.1/collection#metodo-first)
* [flatten](/documentazione/5.1/collection#metodo-flatten)
* [flip](/documentazione/5.1/collection#metodo-flip)
* [forget](/documentazione/5.1/collection#metodo-forget)
* [forPage](/documentazione/5.1/collection#metodo-forpage)
* [get](/documentazione/5.1/collection#metodo-get)
* [groupBy](/documentazione/5.1/collection#metodo-groupby)
* [has](/documentazione/5.1/collection#metodo-has)
* [implode](/documentazione/5.1/collection#metodo-implode)
* [intersect](/documentazione/5.1/collection#metodo-intersect)
* [isEmpty](/documentazione/5.1/collection#metodo-isempty)
* [keyBy](/documentazione/5.1/collection#metodo-keyby)
* [keys](/documentazione/5.1/collection#metodo-keys)
* [last](/documentazione/5.1/collection#metodo-last)
* [map](/documentazione/5.1/collection#metodo-map)
* [merge](/documentazione/5.1/collection#metodo-merge)
* [pluck](/documentazione/5.1/collection#metodo-pluck)
* [pop](/documentazione/5.1/collection#metodo-pop)
* [prepend](/documentazione/5.1/collection#metodo-prepend)
* [pull](/documentazione/5.1/collection#metodo-pull)
* [push](/documentazione/5.1/collection#metodo-push)
* [put](/documentazione/5.1/collection#metodo-put)
* [random](/documentazione/5.1/collection#metodo-random)
* [reduce](/documentazione/5.1/collection#metodo-reduce)
* [reject](/documentazione/5.1/collection#metodo-reject)
* [reverse](/documentazione/5.1/collection#metodo-reverse)
* [search](/documentazione/5.1/collection#metodo-search)
* [shift](/documentazione/5.1/collection#metodo-shift)
* [shuffle](/documentazione/5.1/collection#metodo-shuffle)
* [slice](/documentazione/5.1/collection#metodo-slice)
* [sort](/documentazione/5.1/collection#metodo-sort)
* [sortBy](/documentazione/5.1/collection#metodo-sortby)
* [sortByDesc](/documentazione/5.1/collection#metodo-sortbydesc)
* [splice](/documentazione/5.1/collection#metodo-splice)
* [sum](/documentazione/5.1/collection#metodo-sum)
* [take](/documentazione/5.1/collection#metodo-take)
* [toArray](/documentazione/5.1/collection#metodo-toarray)
* [toJson](/documentazione/5.1/collection#metodo-tojson)
* [transform](/documentazione/5.1/collection#metodo-transform)
* [unique](/documentazione/5.1/collection#metodo-unique)
* [values](/documentazione/5.1/collection#metodo-values)
* [where](/documentazione/5.1/collection#metodo-where)
* [whereLoose](/documentazione/5.1/collection#metodo-whereloose)
* [zip](/documentazione/5.1/collection#metodo-zip)

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
