# Eloquent: Mutators

- [Introdução](#introduction)
- [Accessors e Mutators](#accessors-and-mutators)
- [Mutators para Datas](#date-mutators)
- [Convertendo Atributos](#attribute-casting)

<a name="introduction"></a>
## Introdução

Accessors e mutators permitem que você formate atributos Eloquent ao recuperar-los a partir de um model ou ao definir seu valor. Por exemplo, você pode querer usar o [Laravel encrypter](/docs/{{version}}/encryption) para criptografar um valor, enquanto ele é armazenado no banco de dados, e, em seguida, automaticamente descriptografar o atributo quando você acessá-lo em um model Eloquent.

Além de accessors e mutators personalizados, o Eloquent também pode converter automaticamente campos do tipo data para instâncias de [Carbon](https://github.com/briannesbitt/Carbon) ou mesmo [converter campos do tipo texto para JSON](#attribute-casting).

<a name="accessors-and-mutators"></a>
## Accessors e Mutators

#### Definindo um Accessor

Para definir um accessor, crie um método `getFooAttribute` em seu model onde `Foo` é o nome da coluna que você deseja acessar em *"CamelCase"*. Neste exemplo, vamos definir um accessor para o atributo `first_name`. O accessor será automaticamente chamado pelo Eloquent ao se tentar recuperar o valor de `first_name`:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Get the user's first name.
		 *
		 * @param  string  $value
		 * @return string
		 */
		public function getFirstNameAttribute($value)
		{
			return ucfirst($value);
		}
	}

Como você pode ver, o valor original da coluna é passado para o accessor, o que lhe permite manipular e retornar o valor. Para acessar o valor do mutator, você pode simplesmente acessar o atributo `first_name`:

	$user = App\User::find(1);

	$firstName = $user->first_name;

#### Definindo um Mutator

Para definir um mutator, defina um método `setFooAttribute` em seu modelo onde` Foo` é o nome da coluna que você deseja acessar em "camelcase". Então, mais uma vez, vamos definir um mutator para o atributo `first_name`. Este mutator será chamado automaticamente ao tentarmos definir o valor do atributo `first_name` no model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Set the user's first name.
		 *
		 * @param  string  $value
		 * @return string
		 */
		public function setFirstNameAttribute($value)
		{
			$this->attributes['first_name'] = strtolower($value);
		}
	}

O mutator vai receber o valor que está sendo definido no atributo, o que lhe permite manipular o valor e atribuir o valor manipulado no `$atributo` interno do model Eloquent. Assim, por exemplo, se tentarmos atribuir o valor `Sally` para o atributo `first_name`:

	$user = App\User::find(1);

	$user->first_name = 'Sally';

Neste exemplo, a função `setFirstNameAttribute` será chamada com o valor `Sally`. Então, o mutator aplica a função `strtolower` ao valor passado e atribui este valor ao array de `$atributos`.

<a name="date-mutators"></a>
## Mutators para Datas

Por padrão, o Eloquent irá converter as colunas  `updated_at` e `created_at` para instâncias de [Carbon](https://github.com/briannesbitt/Carbon), que fornecem uma variedade de métodos de helpful, e estende a classe nativa do PHP `DateTime`.

Você pode definir os campos que serão automaticamente tranformados, ou até mesmo desativar esta transformação, substituindo a propriedade `$dates` do seu model:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The attributes that should be mutated to dates.
		 *
		 * @var array
		 */
		protected $dates = ['created_at', 'updated_at', 'disabled_at'];
	}

Quando uma coluna é considerada como uma data, você pode defini-la como um UNIX timestamp, uma string de data (`Y-m-d`), uma string de data e hora, e claro, uma instância de `DateTime` / `Carbon`, e o valor da data será armazenado corretamente em seu banco de dados:

	$user = App\User::find(1);

	$user->disabled_at = Carbon::now();

	$user->save();

Como mencionado acima, ao recuperar atributos listados em sua propriedade `$dates`, eles serão automaticamente convertido para instâncias de [Carbon](https://github.com/briannesbitt/Carbon), permitindo que você use qualquer um dos métodos da classe Carbon em seus atributos:

	$user = App\User::find(1);

	return $user->disabled_at->getTimestamp();

<a name="attribute-casting"></a>
## Convertendo Atributos

A propriedade `$casts` em seu model proporciona um método conveniente para conversão de atributos em tipos de dados comuns. A propriedade `$casts` deve ser um array onde a sua chave é o nome do atributo que está sendo convertido, enquanto o seu valor é o tipo em que você deseja converter a coluna. Os tipos para conversão suportados são: `integer`, `real`, `float`, `double`, `string`, `boolean`, `object` e `array`.

Por exemplo, vamos converter o atributo `is_admin`, que está armazenado em nosso banco de dados como um número inteiro (`0` ou `1`) para um valor booleano:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The attributes that should be casted to native types.
		 *
		 * @var array
		 */
		protected $casts = [
			'is_admin' => 'boolean',
		];
	}

Agora, o atributo `is_admin` sempre será convertido para um tipo booleano quando você acessá-lo, mesmo que o valor intrínseco esteja armazenado no banco de dados como um número inteiro:

	$user = App\User::find(1);

	if ($user->is_admin) {
		//
	}

#### Convertendo em Array

A conversão para o tipo `array` é particularmente útil quando se trabalha com colunas que armazenam dados como JSON serializado. Por exemplo, se seu banco de dados possui um campo do tipo `TEXT` que contenha JSON serializado, acrescentando o tipo `array` para a conversão de um atributo, fará com que automaticamente este atributo seja desserializado em um array PHP, quando você acessá-lo em seu model Eloquent:

	<?php namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * The attributes that should be casted to native types.
		 *
		 * @var array
		 */
		protected $casts = [
			'options' => 'array',
		];
	}

Uma vez que a conversão é definida, você pode acessar o atributo `options` que ele será automaticamente desserializado do formato JSON para um array PHP. Da mesma forma que ao definirmos um valor para o atributo `options`, fará com que o array seja automaticamente serializado de volta para o formato JSON sendo antão armazenado:

	$user = App\User::find(1);

	$options = $user->options;

	$options['key'] = 'value';

	$user->options = $options;

	$user->save();
