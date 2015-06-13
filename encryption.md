# Encryption

- [設定](#configuration)
- [基本使用](#basic-usage)

<a name="configuration"></a>
## 設定

在使用 Laravel 的加密前，你應該先設定 `config/app.php` 中的 `key` 值，該設定值需包含32個不規則字元組成（可為大寫、小寫字母與數字）。如果沒有設定這個值，所有被加密過的值都不安全。

<a name="basic-usage"></a>
## 基本使用

#### 加密

你可以使用 `Crypt` [facade](/docs/{{version}}/facades) 加密一個值。所有被加密的值都會使用 OpenSSL 與 `AES-256-CBC` 規則。此外，所有加密過後的值都會被簽署驗證資訊（ MAC ），以確認加密值是否被竄改。

在以下的例子中，我們使用 `Crypt` 中的 `encrypt` 方法，將加密過後的資料存入 [Eloquent ORM](/docs/{{version}}/eloquent)：

	<?php

	namespace App\Http\Controllers;

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

#### 解密

當然，你可以用 `Crypt` 中的 `decrypt` 方法去解密。如果該資料無法被解密，像是驗證資訊（ MAC ）不合格等因素，將會擲出 `Illuminate\Contracts\Encryption\DecryptException`：

	use Illuminate\Contracts\Encryption\DecryptException;

	try {
		$decrypted = Crypt::decrypt($encryptedValue);
	} catch (DecryptException $e) {
		//
	}
