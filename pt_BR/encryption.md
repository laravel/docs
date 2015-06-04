# Encriptação

- [Configuração](#configuration)
- [Uso Básico](#basic-usage)

<a name="configuration"></a>
## Configuração

Antes de usar o encrypter do Laravel, você deve definir a opção `key` no seu arquivo de configuração `config/app.php` com 32 caracteres , sequência aleatória. Se este valor não estiver corretamente definido, todos os valores criptografados pelo Laravel serão inseguros

<a name="basic-usage"></a>
## Uso Básico

#### Criptografando Um Valor

Você pode criptografar um valor usando o [facade](/docs/{{version}}/facades) `Crypt`. Todos os valores são criptografados usando o OpenSSL e o `AES-128-CBC` cipher. Além disso, todos os valores criptografados são assinados com um código de autenticação de mensagem (MAC) para detectar quaisquer modificações na sequência criptografada.

Por exemplo, nós podemos usar o metodo `encrypt` para criptografar um valor e armazená-lo em um [Eloquent model](/docs/{{version}}/eloquent):

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

#### Descriptografando Um Valor

É claro que você pode descriptografar valores usando o metodo `decrypt` da facade `Crypt`. Se o valor não pode ser descriptografado corretamente, pode ser que o MAC é inválido, uma `Illuminate\Contracts\Encryption\DecryptException` será lançada:

	use Illuminate\Contracts\Encryption\DecryptException;

	try {
		$decrypted = Crypt::decrypt($encryptedValue);
	} catch (DecryptException $e) {
		//
	}
