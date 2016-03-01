# Eloquent: Serialização

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)
- [Ocultando Atributos na saída JSON](#hiding-attributes-from-json)
- [Acrescentando Valores para a saída JSON](#appending-values-to-json)

<a name="introduction"></a>
## Introdução

Na construção de API's JSON, muitas das vezes você vai precisar converter seus models e relacionamentos para arrays ou JSON. O Eloquent inclui métodos convenientes para fazer essas conversões, bem como para controlar quais atributos são incluídos em suas serializações.

<a name="basic-usage"></a>
## Uso Básico

#### Convertendo um Model para um Array

Para converter um model e seus [relacionamentos](/docs/{{version}}/eloquent-relationships) para um array, você pode usar o método `toArray`. Este método é recursivo, logo todos os atributos e todos os relacionamentos (incluindo os relacionamentos dos relacionamentos) serão convertidas para arrays:

	$user = App\User::with('roles')->first();

	return $user->toArray();

Você também pode converter [collections](/docs/{{version}}/eloquent-collections) em arrays:

	$users = App\User::all();

	return $users->toArray();

#### Convertendo um Model para um JSON

Para converter um model para JSON, você pode usar o método `toJson`. Assim como o `toArray`, o método` toJson` também é recursivo, então todos os atributos e os relacionamentos serão convertidos em JSON:

	$user = App\User::find(1);

	return $user->toJson();

Alternativamente, você pode transformar um model ou collection em uma string, o que irá chamar automaticamente o método `toJson`:

	$user = App\User::find(1);

	return (string) $user;

Dado que os models e collections são convertidos em JSON quando transformados em uma string, você pode retornar objetos Eloquent diretamente a partir das rotas ou controllers de sua aplicação:

	Route::get('users', function () {
		return App\User::all();
	});

<a name="hiding-attributes-from-json"></a>
## Ocultando Atributos na saída JSON

Às vezes você pode querer limitar os atributos, tais como senhas, que estejam inclusos na representação do seu model convertido em array ou JSON. Para fazer isso, adicione a propriedade `$hidden` em seu model:

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

> **Nota:** Ao ocultar relacionamentos, use o nome do **method** do relacionamento, e não o nome da sua propriedade dinâmica.

Alternativamente, você pode usar a propriedade `visible` para definir uma white-list de atributos que devem ser inclusos na representação do seu model, seja ela array ou JSON:

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

Ocasionalmente, você pode precisar adicionar um array de atributos que não possuam uma coluna correspondente em seu banco de dados. Para fazer isso, primeiro defina um [accessor](/docs/{{version}}/eloquent-mutators) para o valor:

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

Depois de criado o accessor, adicione o nome do atributo à propriedade `appends` no model:

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

Uma vez que o atributo foi adicionado à lista `appends`, ele será incluído em ambas as representações do model, seja array ou JSON. Os atributos contidos no array `appends` também irão respeitar as propriedades `visible` e `hidden` configuradas no model.
