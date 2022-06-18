# 加密

- [加密](#加密)
  - [介紹](#介紹)
  - [設定](#設定)
  - [使用加密](#使用加密)
      - [加密一個值](#加密一個值)
      - [解密一個值](#解密一個值)

<a name="introduction"></a>
## 介紹


Laravel 的加密服務提供一個簡單、方便的介面使用 OpenSSL 所提供的 AES-256 和 AES-128 去加密及解密文字。所有 Laravel 加密值都會用到訊息認證碼（MAC），因此原始值在加密後不會被再次修改。


<a name="configuration"></a>
## 設定


在使用 Laravel 加密器之前，請務必在 config/app.php 設定檔設定 key 選項。這個設定項由環境變量 `APP_KEY` 設定。你應該使用 `php artisan key:generate` 指令來產生這個金鑰，因為`key:generate` 這個指令會使用 PHP 的安全隨機字元產生器來產生金鑰。如果這個值還未設定，所有 Laravel 加密的值都不會是安全的。
一般來說，在 [Laravel's installation](/docs/{{version}}/installation) 中會生成 `APP_KEY` 環境變數的值。

<a name="using-the-encrypter"></a>
## 使用加密

<a name="encrypting-a-value"></a>
#### 加密一個值


你可以使用 `Crypt` Facades 提供的 `encryptString` 來加密一個值。所有加密的值都使用 OpenSSL 的 AES-256-CBC 來進行加密。此外，所有加密過的值都會使用消息認證碼(MAC) 來簽名，並用來避免被惡意用戶竄改： 

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Crypt;

    class DigitalOceanTokenController extends Controller
    {
        /**
         * 為使用者儲存 DigitalOcean API 標記。
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function storeSecret(Request $request)
        {
            $request->user()->fill([
                'token' => Crypt::encryptString($request->token),
            ])->save();
        }
    }

<a name="decrypting-a-value"></a>
#### 解密一個值


你可以使用 `Crypt` Facades 提供的 `decryptString` 來進行解密。如果該值不能被正確解密，例如消息認證碼（MAC）無效時，會拋出異常 `Illuminate\Contracts\Encryption\DecryptException`：


    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
