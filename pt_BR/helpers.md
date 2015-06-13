# Funções Helper

- [Introdução](#introduction)
- [Métodos Disponíveis](#available-methods)

<a name="introduction"></a>
## Introdução

Laravel inclui uma variedade de funções "helper". Muitas dessas funções são usadas pelo framework em si; Contudo, você é livre para usá-las em suas aplicações se você achar conveniente.

<a name="available-methods"></a>
## Métodos Disponíveis

<style>
	.collection-method-list > p {
		column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
		column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
	}

	.collection-method-list a {
		display: block;
	}
</style>

### Arrays

<div class="collection-method-list" markdown="1">
[array_add](#method-array-add)
[array_divide](#method-array-divide)
[array_dot](#method-array-dot)
[array_except](#method-array-except)
[array_first](#method-array-first)
[array_flatten](#method-array-flatten)
[array_forget](#method-array-forget)
[array_get](#method-array-get)
[array_only](#method-array-only)
[array_pluck](#method-array-pluck)
[array_pull](#method-array-pull)
[array_set](#method-array-set)
[array_sort](#method-array-sort)
[array_where](#method-array-where)
[head](#method-head)
[last](#method-last)
</div>

### Paths

<div class="collection-method-list" markdown="1">
[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[public_path](#method-public-path)
[storage_path](#method-storage-path)
</div>

### Strings

<div class="collection-method-list" markdown="1">
[camel_case](#method-camel-case)
[class_basename](#method-class-basename)
[e](#method-e)
[ends_with](#method-ends-with)
[snake_case](#method-snake-case)
[str_limit](#method-str-limit)
[starts_with](#method-starts-with)
[str_contains](#method-str-contains)
[str_finish](#method-str-finish)
[str_is](#method-str-is)
[str_plural](#method-str-plural)
[str_random](#method-str-random)
[str_singular](#method-str-singular)
[str_slug](#method-str-slug)
[studly_case](#method-studly-case)
[trans](#method-trans)
[trans_choice](#method-trans-choice)
</div>

### URLs

<div class="collection-method-list" markdown="1">
[action](#method-action)
[route](#method-route)
[url](#method-url)
</div>

### Miscellaneous

<div class="collection-method-list" markdown="1">
[csrf_token](#method-csrf-token)
[dd](#method-dd)
[elixir](#method-elixir)
[env](#method-env)
[event](#method-event)
[response](#method-response)
[value](#method-value)
[view](#method-view)
[with](#method-with)
</div>

<a name="method-listing"></a>
## Listando os Métodos

<style>
	#collection-method code {
		font-size: 14px;
	}

	#collection-method:not(.first-collection-method) {
		margin-top: 50px;
	}
</style>

<a name="method-array-add"></a>
#### `array_add()` {#collection-method .first-collection-method}

A função `array_add` adiciona um item chave / valor para o array se a chave ainda não existir no array:

	$array = array_add(['name' => 'Desk'], 'price', 100);

	// ['name' => 'Desk', 'price' => 100]

<a name="method-array-divide"></a>
#### `array_divide()` {#collection-method}

A função `array_divide` retorna 2 arrays, um contendo as chaves e outro contendo os valores do array original:

	list($keys, $values) = array_divide(['name' => 'Desk']);

	// $keys: ['name']

	// $values: ['Desk']

<a name="method-array-dot"></a>
#### `array_dot()` {#collection-method}

A função `array_dot` nivela um array multi-dimensional em um único nível que usa um "." para indicar a profundidade:

	$array = array_dot(['foo' => ['bar' => 'baz']]);

	// ['foo.bar' => 'baz'];

<a name="method-array-except"></a>
#### `array_except()` {#collection-method}

O método `array_except` remove os itens chave / valor do array:

	$array = ['name' => 'Desk', 'price' => 100];

	$array = array_except($array, ['price']);

	// ['name' => 'Desk']

<a name="method-array-first"></a>
#### `array_first()` {#collection-method}

O método `array_first` retorna o primeiro elemento de um array que passar por um determinado teste da verdade:

	$array = [100, 200, 300];

	$value = array_first($array, function ($key, $value) {
		return $value >= 150;
	});

	// 200

O valor padrão também pode ser passado como terceiro parâmetro do método. Este valor será retornado se nenhum valor passar no teste da verdade.

	$value = array_first($array, $callback, $default);

<a name="method-array-flatten"></a>
#### `array_flatten()` {#collection-method}

O método `array_flatten` nivelará um array multi-dimensional num único nível.

	$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

	$array = array_flatten($array);

	// ['Joe', 'PHP', 'Ruby'];

<a name="method-array-forget"></a>
#### `array_forget()` {#collection-method}

O método `array_forget` remove um item chave / valor de um array que usa um "." para indicar a profundidade:

	$array = ['products' => ['desk' => ['price' => 100]]];

	array_forget($array, 'products.desk');

	// ['products' => []]

<a name="method-array-get"></a>
#### `array_get()` {#collection-method}

O método `array_get` recupera um valor de um array usando o "." para indicar a profundidade:

	$array = ['products' => ['desk' => ['price' => 100]]];

	$value = array_get($array, 'products.desk');

	// ['price' => 100]

A função `array_get` também aceita um valor padrão que será retornado caso a chave especificada não exista:

	$value = array_get($array, 'names.john', 'default');

<a name="method-array-only"></a>
#### `array_only()` {#collection-method}

O método `array_only` retornará somente os itens chave / valor do array dado:

	$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

	$array = array_only($array, ['name', 'price']);

	// ['name' => 'Desk', 'price' => 100]

<a name="method-array-pluck"></a>
#### `array_pluck()` {#collection-method}

O método `array_pluck` arrancará uma lista dos itens chave / valor do array:

	$array = [
		['developer' => ['name' => 'Taylor']],
		['developer' => ['name' => 'Abigail']]
	];

	$array = array_pluck($array, 'developer.name');

	// ['Taylor', 'Abigail'];

<a name="method-array-pull"></a>
#### `array_pull()` {#collection-method}

O método `array_pull` retornará e removerá um item chave / valor do array:

	$array = ['name' => 'Desk', 'price' => 100];

	$name = array_pull($array, 'name');

	// $name: Desk

	// $array: ['price' => 100]

<a name="method-array-set"></a>
#### `array_set()` {#collection-method}

O método `array_set` seta um valor dentro de um array usando o "." para indicar profundidade:

	$array = ['products' => ['desk' => ['price' => 100]]];

	array_set($array, 'products.desk.price', 200);

	// ['products' => ['desk' => ['price' => 200]]]

<a name="method-array-sort"></a>
#### `array_sort()` {#collection-method}

O método `array_sort` sorteia o array através dos resultados da Closure passada:

	$array = [
		['name' => 'Desk'],
		['name' => 'Chair'],
	];

	$array = array_values(array_sort($array, function ($value) {
		return $value['name'];
	}));

	/*
		[
			['name' => 'Chair'],
			['name' => 'Desk'],
		]
	*/

<a name="method-array-where"></a>
#### `array_where()` {#collection-method}

A função `array_where` filtra o array usando a Closure passada:

	$array = [100, '200', 300, '400', 500];

	$array = array_where($array, function ($key, $value) {
		return is_string($value);
	});

	// [1 => 200, 3 => 400]

<a name="method-head"></a>
#### `head()` {#collection-method}

A função `head` simplesmente retorna o primeiro elemento do array passado:

	$array = [100, 200, 300];

	$first = head($array);

	// 100

<a name="method-last"></a>
#### `last()` {#collection-method}

A função `last` retorna o último elemento do array passado:

	$array = [100, 200, 300];

	$last = last($array);

	// 300

<a name="paths"></a>
## Paths

<a name="method-app-path"></a>
#### `app_path()` {#collection-method}

A função `app_path` retorna o caminho completo do diretório `app`:

	$path = app_path();

Você pode também utilizar a função `app_path` para retornar um caminho completo de um arquivo em relação ao diretório da aplicação:

	$path = app_path('Http/Controllers/Controller.php');

<a name="method-base-path"></a>
#### `base_path()` {#collection-method}

A função `base_path` retorna o caminho completo do diretório raís do projeto:

	$path = base_path();

Você pode também utilizar a função `base_path` para gerar um caminho completo de um arquivo relativo ao diretório raís do projeto:

	$path = base_path('vendor/bin');

<a name="method-config-path"></a>
#### `config_path()` {#collection-method}

A função `config_path` retorna o caminho completo do diretório de configuração da aplicação:

	$path = config_path();

<a name="method-database-path"></a>
#### `database_path()` {#collection-method}

A função `database_path` retorna o caminho completo do diretório de banco de dados da aplicação:

	$path = database_path();

<a name="method-public-path"></a>
#### `public_path()` {#collection-method}

A função `publi_path` retorna o caminho completo do diretório `public`:

	$path = public_path();

<a name="method-storage-path"></a>
#### `storage_path()` {#collection-method}

A função `storage_path` retorna o caminho completo do diretório `storage`:

	$path = storage_path();

Você pode também utilizar a função `storage_pat` para retornar o caminho completo de um arquivo passado relativo ao diretório storage:

	$path = storage_path('app/file.txt');

<a name="strings"></a>
## Strings

<a name="method-camel-case"></a>
#### `camel_case()` {#collection-method}

A função `camel_case` converte uma string para `camelCase`:

	$camel = camel_case('foo_bar');

	// fooBar

<a name="method-class-basename"></a>
#### `class_basename()` {#collection-method}

O `class_basename` retorna o nome da classe de uma classe passada com o seu namespace, que será removido:

	$class = class_basename('Foo\Bar\Baz');

	// Baz

<a name="method-e"></a>
#### `e()` {#collection-method}

A função `e` abre `htmlentities` de uma string passada:

	echo e('<html>foo</html>');

<a name="method-ends-with"></a>
#### `ends_with()` {#collection-method}

A função `ends_with` determina se uma string termina com o valor passado:

	$value = ends_with('This is my name', 'name');

	// true

<a name="method-snake-case"></a>
#### `snake_case()` {#collection-method}

A função `snake_case` converte uma string para `snake_case`:

	$snake = snake_case('fooBar');

	// foo_bar

<a name="method-str-limit"></a>
#### `str_limit()` {#collection-method}

O função `string_limit` limita o número de caracteres de uma string. A função aceita uma string como primeiro argumento e, no segundo, o número máximo de caracteres a ser retornado:

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

<a name="method-starts-with"></a>
#### `starts_with()` {#collection-method}

A função `starts_with` determina se uma string começa com um valor passado:

	$value = starts_with('This is my name', 'This');

	// true

<a name="method-str-contains"></a>
#### `str_contains()` {#collection-method}
A função `str_contains` verifica se uma string passada contém o valor passado:

	$value = str_contains('This is my name', 'my');

	// true

<a name="method-str-finish"></a>
#### `str_finish()` {#collection-method}

A função `str_finish` adiciona um caractere no final de uma string caso ele não seja o último caractere dessa string:

	$string = str_finish('this/string', '/');

	// this/string/

<a name="method-str-is"></a>
#### `str_is()` {#collection-method}

A função `str_is` determina se uma string passada corresponde a um determinado padrão. Asterisco pode ser usado para indicar caracteres coringa:

	$value = str_is('foo*', 'foobar');

	// true

	$value = str_is('baz*', 'foobar');

	// false

<a name="method-str-plural"></a>
#### `str_plural()` {#collection-method}

A função `str_plural` converte uma string para o seu formato plural. Esta função atualmente, suporta somente a línga inglesa:

	$plural = str_plural('car');

	// cars

	$plural = str_plural('child');

	// children

<a name="method-str-random"></a>
#### `str_random()` {#collection-method}

A função `str_random` gera uma string randômica com o tamanho passado:

	$string = str_random(40);

<a name="method-str-singular"></a>
#### `str_singular()` {#collection-method}

A função `str_singular` converte uma string para o formto singular. Esta função atualmente só suporta a língua inglesa:

	$singular = str_singular('cars');

	// car

<a name="method-str-slug"></a>
#### `str_slug()` {#collection-method}

A função `str_slug` retorna um "slug" da string passada:

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

<a name="method-studly-case"></a>
#### `studly_case()` {#collection-method}

A função `studly_case` converte uma string para `StudlyCase`:

	$value = studly_case('foo_bar');

	// FooBar

<a name="method-trans"></a>
#### `trans()` {#collection-method}

A função `trans` retorna uma linha da linguagem passada usando seus [arquivos de localização](/docs/{{version}}/localization):

	echo trans('validation.required'):

<a name="method-trans-choice"></a>
#### `trans_choice()` {#collection-method}

A função `trans_choice` retorna uma linha da linguagem com inflexão:

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## URLs

<a name="method-action"></a>
#### `action()` {#collection-method}

A função `action` gera uma URL para a ação do controller passado. Você não precisa inserir o namespace do controller. Em vez disso, passe o nome da classe relativa para o namespace `App\Http\Controllers`:

	$url = action('HomeController@getIndex');

Se o método aceitar parâmetros de rota, você pode passar um segundo argumento no método:

	$url = action('UserController@profile', ['id' => 1]);

<a name="method-route"></a>
#### `route()` {#collection-method}

A função `route` gera uma URL para uma rota nomeada:

	$url = route('routeName');

Se a rota aceitar parâmetros, você pode passar um segundo argumento para o método:

	$url = route('routeName', ['id' => 1]);

<a name="method-url"></a>
#### `url()` {#collection-method}

A função `url` gera uma url completa de um caminho especificado:

	echo url('user/profile');

	echo url('user/profile', [1]);

<a name="miscellaneous"></a>
## Variados

<a name="method-csrf-token"></a>
#### `csrf_token()` {#collection-method}

A função `csrf_token` recupera o valor do atual toke CSRF:

	$token = csrf_token();

<a name="method-dd"></a>
#### `dd()` {#collection-method}

A função `dd` despeja uma variável e encerra a execução do script:

	dd($value);

<a name="method-elixir"></a>
#### `elixir()` {#collection-method}

A função `elixir` retorna o caminho para o arquivo [Elixir](/docs/{{version}}/elixir) versionado:

	elixir($file);

<a name="method-env"></a>
#### `env()` {#collection-method}

A função `env` retorna o valor de uma varíavel de ambiente ou retorna um valor padrão

	$env = env('APP_ENV');

	// Retorna um valor padrão se a variável não existir...
	$env = env('APP_ENV', 'production');

<a name="method-event"></a>
#### `event()` {#collection-method}

A função `event` dispacha o [evento](/docs/{{version}}/events) passado para seus listeners:

	event(new UserRegistered($user));

<a name="method-response"></a>
#### `response()` {#collection-method}

A função `response` cria uma instância de [response](/docs/{{version}}/responses) ou obtém uma instância de response factory:

	return response('Hello World', 200, $headers);

	return response()->json(['foo' => 'bar'], 200, $headers);

<a name="method-value"></a>
#### `value()` {#collection-method}

O comportamento da função `value` simplesmente retornará o valor que for passado. Porém, se você passar uma `Closure`, a `Closure` será executada e resultado será seu valor retornado:

	$value = value(function() { return 'bar'; });

<a name="method-view"></a>
#### `view()` {#collection-method}

A função `view` retorna uma instância da [view](/docs/{{version}}/views):

	return view('auth.login');

<a name="method-with"></a>
#### `with()` {#collection-method}

A função `with` retorna o valor que é passado. Esta função é últil para métodos de encadeamento onde de outra forma, isto seria impossível:

	$value = with(new Foo)->work();
