# Hashing

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)

<a name="introduction"></a>
## Introdução

O Laravel `Hash` [facade](/docs/{{version}}/facades) fornece um seguro Bcrypt hashing para armazenar senhas dos usuários. Se você está usando o controller `AuthController`, que está incluso na sua aplicação Laravel, ele vai automaticamente usar o Bcrypt para registro e autenticação.

Bcrypt é uma excelente opção para hashing de senhas porque seu "fator de trabalho" é ajustável, o que significa que o tempo que leva para gerar um hash pode ser aumentado com incremento de hardware.

<a name="basic-usage"></a>
## Uso Básico

Você pode aplicar o hash para uma senha chamando o método `make` no facade `Hash`:

	<?php namespace App\Http\Controllers;

	use Hash;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the password for the user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function updatePassword(Request $request, $id)
		{
			$user = User::findOrFail($id);

			// Validate the new password length...

			$user->fill([
				'password' => Hash::make($request->newPassword)
			])->save();
		}
	}

De forma alternativa, você pode também usar a função helper global `bcrypt`:

	bcrypt('plain-text');

#### Verificando uma Senha contra um Hash

O método `check` permite verificar que uma string de texto fornecida corresponde a um determinado hash fornecido. No entando, se você está usando o `AuthController` [incluso no Laravel](/docs/{{version}}/authentication), você provavelmente não vai precisar usar isso diretamente, já que o controller de autenticação incluso automaticamente chama esse método:

	if (Hash::check('plain-text', $hashedPassword)) {
		// The passwords match...
	}

#### Checando se uma Senha precisa de um novo Hash

A função `needsRehash` permite determinar se o fator de trabalho usado pelo hasher foi modificado desde a última vez que foi gerado um hash para a senha:

	if (Hash::needsRehash($hashed)) {
		$hashed = Hash::make('plain-text');
	}
