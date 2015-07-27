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

<style>
	#collection-method-list > p {
		column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
		column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
	}

	#collection-method-list a {
		display: block;
	}
</style>

<div id="collection-method-list" markdown="1">
[all](/docs/5.1/collection#method-all)
[chunk](/docs/5.1/collection#method-chunk)
[collapse](/docs/5.1/collection#method-collapse)
[contains](/docs/5.1/collection#method-contains)
[count](/docs/5.1/collection#method-count)
[diff](/docs/5.1/collection#method-diff)
[each](/docs/5.1/collection#method-each)
[filter](/docs/5.1/collection#method-filter)
[first](/docs/5.1/collection#method-first)
[flatten](/docs/5.1/collection#method-flatten)
[flip](/docs/5.1/collection#method-flip)
[forget](/docs/5.1/collection#method-forget)
[forPage](/docs/5.1/collection#method-forpage)
[get](/docs/5.1/collection#method-get)
[groupBy](/docs/5.1/collection#method-groupby)
[has](/docs/5.1/collection#method-has)
[implode](/docs/5.1/collection#method-implode)
[intersect](/docs/5.1/collection#method-intersect)
[isEmpty](/docs/5.1/collection#method-isempty)
[keyBy](/docs/5.1/collection#method-keyby)
[keys](/docs/5.1/collection#method-keys)
[last](/docs/5.1/collection#method-last)
[map](/docs/5.1/collection#method-map)
[merge](/docs/5.1/collection#method-merge)
[pluck](/docs/5.1/collection#method-pluck)
[pop](/docs/5.1/collection#method-pop)
[prepend](/docs/5.1/collection#method-prepend)
[pull](/docs/5.1/collection#method-pull)
[push](/docs/5.1/collection#method-push)
[put](/docs/5.1/collection#method-put)
[random](/docs/5.1/collection#method-random)
[reduce](/docs/5.1/collection#method-reduce)
[reject](/docs/5.1/collection#method-reject)
[reverse](/docs/5.1/collection#method-reverse)
[search](/docs/5.1/collection#method-search)
[shift](/docs/5.1/collection#method-shift)
[shuffle](/docs/5.1/collection#method-shuffle)
[slice](/docs/5.1/collection#method-slice)
[sort](/docs/5.1/collection#method-sort)
[sortBy](/docs/5.1/collection#method-sortby)
[sortByDesc](/docs/5.1/collection#method-sortbydesc)
[splice](/docs/5.1/collection#method-splice)
[sum](/docs/5.1/collection#method-sum)
[take](/docs/5.1/collection#method-take)
[toArray](/docs/5.1/collection#method-toarray)
[toJson](/docs/5.1/collection#method-tojson)
[transform](/docs/5.1/collection#method-transform)
[unique](/docs/5.1/collection#method-unique)
[values](/docs/5.1/collection#method-values)
[where](/docs/5.1/collection#method-where)
[whereLoose](/docs/5.1/collection#method-whereloose)
[zip](/docs/5.1/collection#method-zip)
</div>

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
