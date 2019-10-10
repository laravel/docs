# 加密

- [前言](#前言)
- [設定](#設定)
- [基本用法](#基本用法)

## 前言

Laravel 的加密器採用 OpenSSL 提供的 AES-256 與 AES-128 進行加密。非常建議您使用 Laravel 內建的加密功能，而不要試圖推出 `自家` 的加密演算法。Laravel 所有加密過後的值都會被簽署文件訊息鑑別碼（MAC），因此這些底層的值被加密後就無法被竄改。

## 設定

在使用 Laravel 的加密器前，你應該先設定 `config/app.php` 設定檔中的 `key` 選項，設定值需要是 32 個字元的隨機字串。您應該使用 `php artisan key：generate` 指令來生成密鑰，因為 `Artisan` 指令將使用 PHP 的安全隨機位元組產生器來構建您的密鑰。如果沒有適當地設定這個值，所有被 Laravel 加密的值將是不安全的。

## 基本用法

#### 加密一個值

你可以藉由 `encrypt` 輔助方法加密一個值。所有被加密的值都會使用 OpenSSL 與 `AES-256-CBC` 加密。此外，所有加密過後的值都會被簽署文件訊息鑑別碼 (MAC)，以偵測加密字串是否被竄改。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\User;
    use Illuminate\Http\Request;

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
                'secret' => encrypt($request->secret),
            ])->save();
        }
    }

#### 無序列化加密

值在加密的過程中是通過 `序列化` 的方式來允許物件與陣列進行加密。因此，非PHP的用戶端需要 `反序列化` 加密資料。如果您不想透過 `序列化` 的方式進行加密和解密值，則可以使用 `Crypt` Facades 的 `encryptString` 和 `decryptString` 方法：

    use Illuminate\Support\Facades\Crypt;

    $encrypted = Crypt::encryptString('Hello world.');

    $decrypted = Crypt::decryptString($encrypted);

#### 解密一個值

你可以使用 `decrypt` 方法來解密值。如果該值無法被適當地解密，像是文件訊息鑑別碼無效等因素，將會拋出一個 `Illuminate\Contracts\Encryption\DecryptException` ：

    use Illuminate\Contracts\Encryption\DecryptException;

    try {
        $decrypted = decrypt($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
