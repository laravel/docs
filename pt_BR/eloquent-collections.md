# Eloquent: Coleções

- [Introdução](#introduction)
- [Métodos Disponíveis](#available-methods)
- [Coleções Personalizadas](#custom-collections)

<a name="introduction"></a>
## Introdução

Todos os múltiplos resultados retornados pelo Eloquent são uma instância do objeto `Illuminate\Database\Eloquent\Collection`, incluindo os resultados obtidos através do método `get` ou acessados por meio de um relacionamento. O objeto de coleção do Eloquent estende a [collection básica](/docs/{{version}}/collections) do Laravel, por isso, naturalmente herda dezenas de métodos utilizados para trabalhar fluentemente com a arrays subjacentes de models Eloquent.

Claro que, todas as coleções (collections) também servem como iteradores, permitindo fazermos loop sobre elas como se fossem arrays PHP simples:

	$users = App\User::where('active', 1)->get();

	foreach ($users as $user) {
		echo $user->name;
	}

No entanto, as coleções são muito mais poderosas do que os arrays e expõe uma variedade de métodos para mapear/iterar pelos elementos da collection utilizando uma interface intuitiva. Por exemplo, vamos remover todos os models inativos e reunir o primeiro nome para cada usuário restante:


	$users = App\User::where('active', 1)->get();

	$names = $users->reject(function ($user) {
		return $user->active === false;
	})
	->map(function ($user) {
		return $user->name;
	});

<a name="available-methods"></a>
## Métodos Disponíveis

### A Coleção Básica

Todas as coleções Eloquent estendem a base do objeto [Laravel collection](/docs/{{version}}/collections) portanto, elas herdam todos os métodos fortes fornecidos pela classe base de collection:

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
[all](/docs/{{version}}/collections#method-all)
[chunk](/docs/{{version}}/collections#method-chunk)
[collapse](/docs/{{version}}/collections#method-collapse)
[contains](/docs/{{version}}/collections#method-contains)
[count](/docs/{{version}}/collections#method-count)
[diff](/docs/{{version}}/collections#method-diff)
[each](/docs/{{version}}/collections#method-each)
[filter](/docs/{{version}}/collections#method-filter)
[first](/docs/{{version}}/collections#method-first)
[flatten](/docs/{{version}}/collections#method-flatten)
[flip](/docs/{{version}}/collections#method-flip)
[forget](/docs/{{version}}/collections#method-forget)
[forPage](/docs/{{version}}/collections#method-forpage)
[get](/docs/{{version}}/collections#method-get)
[groupBy](/docs/{{version}}/collections#method-groupby)
[has](/docs/{{version}}/collections#method-has)
[implode](/docs/{{version}}/collections#method-implode)
[intersect](/docs/{{version}}/collections#method-intersect)
[isEmpty](/docs/{{version}}/collections#method-isempty)
[keyBy](/docs/{{version}}/collections#method-keyby)
[keys](/docs/{{version}}/collections#method-keys)
[last](/docs/{{version}}/collections#method-last)
[map](/docs/{{version}}/collections#method-map)
[merge](/docs/{{version}}/collections#method-merge)
[pluck](/docs/{{version}}/collections#method-pluck)
[pop](/docs/{{version}}/collections#method-pop)
[prepend](/docs/{{version}}/collections#method-prepend)
[pull](/docs/{{version}}/collections#method-pull)
[push](/docs/{{version}}/collections#method-push)
[put](/docs/{{version}}/collections#method-put)
[random](/docs/{{version}}/collections#method-random)
[reduce](/docs/{{version}}/collections#method-reduce)
[reject](/docs/{{version}}/collections#method-reject)
[reverse](/docs/{{version}}/collections#method-reverse)
[search](/docs/{{version}}/collections#method-search)
[shift](/docs/{{version}}/collections#method-shift)
[shuffle](/docs/{{version}}/collections#method-shuffle)
[slice](/docs/{{version}}/collections#method-slice)
[sort](/docs/{{version}}/collections#method-sort)
[sortBy](/docs/{{version}}/collections#method-sortby)
[sortByDesc](/docs/{{version}}/collections#method-sortbydesc)
[splice](/docs/{{version}}/collections#method-splice)
[sum](/docs/{{version}}/collections#method-sum)
[take](/docs/{{version}}/collections#method-take)
[toArray](/docs/{{version}}/collections#method-toarray)
[toJson](/docs/{{version}}/collections#method-tojson)
[transform](/docs/{{version}}/collections#method-transform)
[unique](/docs/{{version}}/collections#method-unique)
[values](/docs/{{version}}/collections#method-values)
[where](/docs/{{version}}/collections#method-where)
[whereLoose](/docs/{{version}}/collections#method-whereloose)
[zip](/docs/{{version}}/collections#method-zip)
</div>

<a name="custom-collections"></a>
## Coleções Personalizadas

Se você precisar usar um objeto `Collection` personalizado com seus próprios métodos de estensão, você pode sobrescrever o método `newCollection` em seu model:


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

Uma vez definido o método `newCollection` em seu model, você receberá uma instância da sua coleção personalizada do Eloquent que retornará sempre um objeto do tipo `Collection`. Se você necessita de uma coleção personalizada para cada model seu, você deverá substituir o método `newCollection` em uma classe model básica e estende-la em todos os seus models.
