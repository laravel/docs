# Eloquent: Serializzazione

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)
- [Nascondere degli Attributi nel JSON](#nascondere-attributi-json)
- [Aggiungere degli Attributi nel JSON](#aggiungere-attributi-json)

<a name="introduzione"></a>
## Introduzione

Ti è mai capitato di costruire delle API JSON? Si? Beh, probabilmente avrai avuto la necessità di convertire i dati ottenuti dalle tue chiamate in JSON. Realizzare API con Laravel ed Eloquent, sotto questo punto di vista, è ancora più comodo! Eloquent infatti presenta alcuni metodi per effettuare queste conversioni in modo semplice e veloce.

<a name="uso-base"></a>
## Uso Base

#### Da Model ad Array

Per convertire un model e le sue eventuali [relazioni](/docs/5.1/eloquent-relazioni) in un array, puoi usare il metodo _toArray_. Il metodo è ricorsivo, quindi non dovrai preoccuparti dei vari sotto-elementi.

	$user = App\User::with('roles')->first();

	return $user->toArray();

Tale utility è disponibile anche per le [collection](/docs/5.1/eloquent-collection):

	$users = App\User::all();

	return $users->toArray();

#### Da Model a JSON

Per convertire un model in JSON puoi usare il metodo _toJson_. Esattamente come avvenuto per `toArray`, anche _toJson_ è ricorsivo.

	$user = App\User::find(1);

	return $user->toJson();

Il metodo _toJson_, inoltre, viene richiamato anche nell'eventualità di un cast in string dell'istanza risultante (che sia un model o una collection):

	$user = App\User::find(1);

	return (string) $user;

Tra l'altro, partendo da questa ultima osservazione, in una qualsiasi route o action di un tuo controller puoi tranquillamente ritornare una cosa del genere:

	Route::get('users', function () {
		return App\User::all();
	});

<a name="nascondere-attributi-json"></a>
## Nascondere degli Attributi nel JSON

A volte potresti avere la necessità di limitare gli attributi da mandare in output. Immagina un campo password: non sarebbe esattamente il massimo della sicurezza mandarlo in output come se niente fosse. Puoi ovviare al problema in modo molto semplice aggiungendo i campi che vuoi nascondere all'array _$hidden_ del tuo model.

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

> **Nota:** se vuoi nascondere dei dati inerenti ad una relazione, usa il nome del **metodo** e non quello della proprietà dinamica.

In alternativa puoi sempre usare la proprietà _visible_ per definire una white-list di attributi da mostrare.

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

<a name="aggiungere-attributi-json"></a>
## Aggiungere degli Attributi nel JSON

Così come puoi togliere, puoi anche aggiungere. A volte potresti avere la necessità di aggiungere dei nuovi attributi al tuo JSON. Nessun problema: non devi fare altro che definire un [accessor](/docs/5.1/eloquent-mutator) per tale attributo.

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

Una volta che hai creato l'accessor, aggiungilo alla proprietà/array _$appends_ del model.

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

Una volta aggiungo all'array, il nuovo attributo sarà incluso nel JSON risultante (vale anche per il metodo _toArray_). Ricorda, inoltre, che gli attributi in _appends_ rispettano le regole specificate in _hidden_ e _visible_.
