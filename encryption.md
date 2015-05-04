# Encryption

- [Basic Usage](#basic-usage)

<a name="basic-usage"></a>
## Basic Usage

#### Encrypting A Value

You may encrypt a value using the `Crypt` [facade](/docs/{{version}}/facades). All encrypted values are signed with a MAC to detect any modifications to the encrypted string.

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

> **Note:** Be sure to set a 32 character random string in the `key` option of the `config/app.php` file. Otherwise, encrypted values will not be secure.

#### Decrypting A Value

Of course, you may decrypt values using the `decrypt` method on the `Crypt` facade:

	$decrypted = Crypt::decrypt($encryptedValue);
