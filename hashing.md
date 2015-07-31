# Hashing

- [Introduzione](#introduzione)
- [Utilizzo base](#utilizzo-base)

<a name="introduzione"></a>
## Introduzione

La [facade](/documentazione/5.1/facade) `Hash` di Laravel fornisce tramite l'utilizzo di Bcrypt un hashing sicuro per salvare le password degli utenti. Se stai utilizzando il controller `AuthController` incluso con l'installazione di Laravel, stai anche utilizzando automaticamente Bcrypt per la registrazione e l'autenticazione.

Bcrypt è una ottima soluzione per creare l'hash di una password perchè il suo "work factor" è modificabile, questo vuol dire che il tempo di generazione dell'hash può essere incrementato se si dispone di un hardware più potente.

<a name="utilizzo-base"></a>
## Utilizzo base

Puoi creare un hash di una password semplicemente richiamando il metodo `make` tramite la facade `Hash`:

	<?php namespace App\Http\Controllers;

	use Hash;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Aggiorna la password dell'utente
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function updatePassword(Request $request, $id)
		{
			$user = User::findOrFail($id);

			// Qui la validazione della password, come ad esempio la lunghezza minima

			$user->fill([
				'password' => Hash::make($request->newPassword)
			])->save();
		}
	}

In alternativa, puoi utilizzare anche l'helper `bcrypt` che è una funzione disponibile globalmente:

	bcrypt('testo-in-chiaro');

#### Verifica Di Una Password Con Il Suo Hash

Il metodo `check` ti permette di verificare se il testo passato come primo argomento corrisponde all'hash passato come secondo argomento. Tuttavia, se utilizzi il controller `AuthController` [incluso in Laravel](/documentazione/5.1/autenticazione), non hai bisogno di richiamare direttamente questo metodo in quanto viene chiamato automaticamente dal controller:

	if (Hash::check('password-in-chiaro', $hashedPassword)) {
		// le password corrispondono...
	}

#### Controllare Se Una Password Deve Essere Ri-hashata

Il metodo `needsRehash` ti permette di determianre se il "work factor" utilizzato per creare l'hash della password è cambiato. Nel caso in cui questo valore fosse stato modificato dopo la creazione della password, questo metodo ti permette di rigenerare l'hash corretto:

	if (Hash::needsRehash($hashed)) {
		$hashed = Hash::make('password-in-chiaro');
	}
