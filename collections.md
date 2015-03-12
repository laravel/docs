# Collections

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)

<a name="introduction"></a>
## Introdução


A classe `Illuminate\Support\Collection` um nativo, conveniente warapper para trabalhar com arrays de dados. Por exemplo, dê uma olhada no seguinte código. Usaremos o helper `collect` para criar uma nova instância de uma coleção a partir de um array:

	$collection = collect(['taylor', 'abigail', null])->map(function($name)
	{
		return strtoupper($name);
	})
	->reject(function($name)
	{
		return is_null($value);
	});


Como você pode ver, a classe `Collection` permite que você chame encadeadamento métodos para realizar nativamente mapeamento e redução do array subjacente. Em geral, todo método `Collection` retorna uma nova instância inteira de `Collection`. Para mais detalhes, continue lendo! 


<a name="basic-usage"></a>
## Uso Básico

#### Criado Coleções


Como mencionado acima, o helper `collect` retornará uma nova instância de `Illuminate\Support\Collection` para o array dado. Você pode também usar o comando `make` na classe `Collection`:

	$collection = collect([1, 2, 3]);

	$collection = Collection::make([1, 2, 3]);


É claro, que objetos de coleções [Eloquent](/docs/5.0/eloquent) sempre retornam como instâncias de `Collection`; contudo, você deve se sentir livre para usar a classe `Collection` quando isto for conveniente para sua aplicação.

#### Explore a Coleção

Ao invés de listar todos os métodos (que são muitos) a Api de `Collection` é disponibilizada, dê uma olhada na [API documentation for the class](http://laravel.com/api/master/Illuminate/Support/Collection.html)!
