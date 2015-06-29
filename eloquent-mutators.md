# Eloquent: Mutator

- [Introduzione](#introduzione)
- [Accessor e Mutator](#accessor-mutator)
- [Date Mutator](#date-mutator)
- [Attribute Casting](#attribute-casting)

<a name="introduzione"></a>
## Introduzione

Gli accessor ed i mutator ti permettono di formattare (sia in input che in output) gli attributi del tuo model Eloquent. Ad esempio, immagina di voler usare l'[encrypter](/docs/5.1/encryption) di Laravel per crittare una password quando viene salvata su database, e decrittarla automaticamente quando viene invece recuperata in un secondo momento. Sono due strumenti molto utili, che vedremo a breve.

Inoltre, Eloquent permette di definire ancora più velocemente il casting dei vari attributi, che si tratti di date da convertire in istanze [Carbon](https://github.com/briannesbitt/Carbon) o addirittura da [campi di testo a JSON](#attribute-casting).

<a name="accessor-mutator"></a>
## Accessor e Mutator

#### Definire un Accessor

Per definire un accessor, non devi fare altro che creare un metodo il cui nome è nel formato _getFooAttribute_, dove Foo è l'attributo da recuperare. Guarda l'esempio di seguito, che si occupa di formattare il recupero dell'attributo *first_name*. Una volta definito, l'accessor verrà automaticamente usato ad ogni uso di *$user->first_name*.

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

Come puoi vedere, l'accessor prende in input il valore _$value_ originale, permettendoti di modificarlo come meglio credi per poi ritornarlo. A quel punto, come già detto, accedere al valore desiderato è semplice.

	// first_name è memorizzato su db come "francesco"
	$user = App\User::find(1);

	// in $firstName ci sarà "Francesco"
	$firstName = $user->first_name;

#### Definire un Mutator

Per definire un mutator bisogna usare una sintassi molto simile a quella vista per gli accessor: al posto di _getFooAttribute_, infatti, stavolta avrai _setFooAttribute_. Usando lo stesso esempio appena visto, vediamo come modificare il valore di *first_name* sul model _User_ prima di memorizzarlo.

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

Il mutator riceverà il valore impostato inizialmente come parametro. Nel metodo potrai quindi modificarlo come meglio credi. Quindi, se proviamo a specificare come nome utente "Sally"...

	$user = App\User::find(1);

	$user->first_name = 'Sally';

Il risultato, su database, sarà "sally".

<a name="date-mutator"></a>
## Date Mutator

Di default, Laravel converte le colonne *created_at* ed *updated_at* in istanze di [Carbon](https://github.com/briannesbitt/Carbon), che fornisce out of the box una marea di metodi utili per la gestione delle date.

Nel caso dovessi averne bisogno anche per altri campi, non c'è nessun problema: basta effettuare l'override della proprietà _$dates_ del model desiderato.

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

Quando una colonna viene considerata una data, puoi impostare il suo valore con uno UNIX Timestamp, una stringa nel formato 'Y-m-d' e, ovviamente, un'istanza `DateTime` o `Carbon`. La data inserita viene automaticamente convertita in un valore compatibile con il sistema di database sottostante.

	$user = App\User::find(1);

	$user->disabled_at = Carbon::now();

	$user->save();

Inoltre, in fase di successivo recupero dei dati **tutte queste date vengono riconvertite in istanze [Carbon](https://github.com/briannesbitt/Carbon)**, permettendoti di usarle come meglio credi.

	$user = App\User::find(1);

	return $user->disabled_at->getTimestamp();

<a name="attribute-casting"></a>
## Attribute Casting

La proprietà _$casts_ del tuo model permette di definire, in modo ancora più veloce di quello visto finora, delle trasformazioni dei tuoi attributi in tipi comuni. I tipi supportati per questa conversione veloce sono: `integer`, `real`, `float`, `double`, `string`, `boolean`, `object` and `array`.

Vediamo un esempio pratico: partendo da un attributo *is_admin*, memorizzato come _integer (0 o 1)_, vogliamo che in fase di recupero venga convertito in boolean per poterlo usare in un semplice _if_: 

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

Fatto! La proprietà _$casts_ è un semplice array associativo, dove il nome dell'attributo da convertire è la chiave, mentre il valore indica il tipo di destinazione.

A questo punto possiamo usare *is_admin* facilmente:

	$user = App\User::find(1);

	if ($user->is_admin) {
		//
	}

#### Array Casting

Qualche parola va spesa sul tipo _array_. A volte possiamo avere, su database, dei valori memorizzati come JSON serializzato. In tal caso, usare l'attribute casting su una colonna simile scegliendo come formato di destinazione _array_ può essere molto comodo. Il testo JSON verrà infatti deserializzato automaticamente e sarà pronto per essere usato!

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

A quel punto, una volta definito il cast, accedere all'attributo _options_ sarà un gioco da ragazzi.

	$user = App\User::find(1);

	$options = $user->options;

	$options['key'] = 'value';

	$user->options = $options;

	$user->save();
