# Eloquent: Serialização

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)
- [Ocultando Atributos na saída JSON](#hiding-attributes-from-json)
- [Acrescentando Valores para a saída JSON](#appending-values-to-json)

<a name="introduction"></a>
## Introdução

Na construção de API's JSON, muitas das vezes você vai precisar converter seus models e relacionamentos para arrays ou JSON. O Eloquent inclui métodos convenientes para fazer essas conversões, bem como controlar quais atributos são incluídos em suas serializações.

<a name="basic-usage"></a>
## Uso Básico

#### Convertendo um Model para um Array

To convert a model and its loaded [relationships](/docs/{{version}}/eloquent-relationships) to an array, you may use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays:

Para converter um modelo e seus relacionamentos carregado [] (/ docs / {{}} / versão eloquentes-relações) para uma matriz, você pode usar o método `toArray`. Este método é recursivo, então todos os atributos e todas as relações (incluindo as relações de relações) serão convertidas para matrizes:

	$user = App\User::with('roles')->first();

	return $user->toArray();

You may also convert [collections](/docs/{{version}}/eloquent-collections) to arrays:

Você também pode converter [coleções] (/ docs / {{}} / versão eloquentes-coleções) para matrizes:

	$users = App\User::all();

	return $users->toArray();

#### Convertendo um Model para um JSON

To convert a model to JSON, you may use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON:

Para converter um modelo para JSON, você pode usar o método `toJson`. Como `toArray`, o método` toJson` é recursivo, então todos os atributos e as relações serão convertidos em JSON:

	$user = App\User::find(1);

	return $user->toJson();

Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method:

Alternativamente, você pode lançar um modelo ou coleção para uma cadeia, que irá chamar automaticamente o método `toJson`:

	$user = App\User::find(1);

	return (string) $user;

Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers:

Como os modelos e coleções são convertidos em JSON quando convertido para uma seqüência de caracteres, você pode retornar Eloquent objetos diretamente de rotas ou controladores da sua aplicação:

	Route::get('users', function () {
		return App\User::all();
	});

<a name="hiding-attributes-from-json"></a>
## Ocultando Atributos na saída JSON

Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property definition to your model:

Às vezes você pode querer limitar os atributos, tais como senhas, que estão incluídos no conjunto do seu modelo ou representação JSON. Para fazer isso, adicione um `definição de propriedade $ hidden` para o seu modelo:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The attributes that should be hidden for arrays.
		 *
		 * @var array
		 */
		protected $hidden = ['password'];
	}

> **Note:** When hiding relationships, use the relationship's **method** name, not its dynamic property name.
> ** Nota: ** Ao ocultar relações, use ** ** método nome, e não o seu nome propriedade dinâmica do relacionamento.

Alternatively, you may use the `visible` property to define a white-list of attributes that should be included in your model's array and JSON representation:

Alternativamente, você pode usar a propriedade `visible` para definir uma lista branca de atributos que devem ser incluídos na matriz do seu modelo e representação JSON:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The attributes that should be visible in arrays.
		 *
		 * @var array
		 */
		protected $visible = ['first_name', 'last_name'];
	}

<a name="appending-values-to-json"></a>
## Acrescentando Valores para a saída JSON

Occasionally, you may need to add array attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/{{version}}/eloquent-mutators) for the value:

Ocasionalmente, você pode precisar adicionar atributos de matriz que não têm uma coluna correspondente em seu banco de dados. Para fazer isso, primeiro definir um [assessor] (/ docs / {{}} / versão eloquentes-Mutators) para o valor:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get the administrator flag for the user.
		 *
		 * @return bool
		 */
		public function getIsAdminAttribute()
		{
			return $this->attributes['admin'] == 'yes';
		}
	}

Once you have created the accessor, add the attribute name to the `appends` property on the model:

Depois de ter criado o acessor, adicione o nome do atributo para a propriedade `appends` no modelo:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The accessors to append to the model's array form.
		 *
		 * @var array
		 */
		protected $appends = ['is_admin'];
	}

Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON forms. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model.

Uma vez que o atributo foi adicionado à lista `appends`, ele será incluído na matriz e JSON ambas as formas do modelo. Atributos no `appends` matriz também irá respeitar o` `visible` e configurações hidden` configurado no modelo.
