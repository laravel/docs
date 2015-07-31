# Crittografia

- [Configurazione](#configurazione)
- [Uso Base](#uso-base)

<a name="configurazione"></a>
## Configurazione

Prima di usare l'encrypter di Laravel, ricorda di impostare l'opzione _key_ del file `config/app.php` con una stringa di 32 caratteri. Meglio se a caso. 

> Nota: se non imposti tale valore, tutti i valori criptati dalla tua applicazione **non saranno sicuri**.

<a name="uso-base"></a>
## Uso Base

#### Crittare un Valore

Puoi crittare un valore usando la [facade](/documentazione/5.1/facade) apposita `Crypt`. Tutti i valori vengono trattati usando OpenSSL ed il cipher `AES-128-CBC`. Tutti i valori crittati, inoltre, vengono "firmati" con un MAC per individuare ogni tentativo di modifica del valore.

Per crittare un valore puoi usare il metodo `encrypt`:

	<?php namespace App\Http\Controllers;

	use Crypt;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Store a secret message for the user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function storeSecret(Request $request, $id)
		{
			$user = User::findOrFail($id);

			$user->fill([
				'secret' => Crypt::encrypt($request->secret)
			])->save();
		}
	}

In questo caso, abbiamo preso il valore di _$request->secret_ e lo stiamo memorizzando, crittato, in un'istanza di _User_.

#### Decrittare un Valore

Chiaramente è possibile anche l'operazione inversa: in questo caso, il metodo da usare sarà `decrypt` sempre della facade `Crypt`. In caso di problemi durante l'operazione, verrà lanciata un'eccezione di tipo `Illuminate\Contracts\Encryption\DecryptException`:

	use Illuminate\Contracts\Encryption\DecryptException;

	try {
		$decrypted = Crypt::decrypt($encryptedValue);
	} catch (DecryptException $e) {
		//
	}
