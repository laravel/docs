# 加密

- [設定](#configuration)
- [基本用法](#basic-usage)

<a name="configuration"></a>
## 設定

在使用 Laravel 的加密器前，你應該先設定 `config/app.php` 設定檔中的 `key` 選項，設定值需要是 32 個字元的隨機字串。如果沒有適當地設定這個值，所有被 Laravel 加密的值將是不安全的。

<a name="basic-usage"></a>
## 基本用法

#### 加密一個值

你可以藉由 `Crypt` [facade](/docs/{{version}}/facades) 加密一個值。所有被加密的值都會使用 OpenSSL 與 `AES-256-CBC` 加密。此外，所有加密過後的值都會被簽署文件訊息鑑別碼 (MAC)，以偵測加密字串是否被竄改。

例如，我們可以使用 `encrypt` 方法加密機密資訊，並把它儲存在 [Eloquent 模型](/docs/{{version}}/eloquent)中：

    <?php

    namespace App\Http\Controllers;

    use Crypt;
    use App\User;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 儲存使用者的機密訊息。
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

#### 解密一個值

當然，你可以使用 `Crypt` facade 上的 `decrypt` 方法來解密值。如果該值無法被適當地解密，像是文件訊息鑑別碼無效等因素，將會拋出一個 `Illuminate\Contracts\Encryption\DecryptException`：

    use Illuminate\Contracts\Encryption\DecryptException;

    try {
        $decrypted = Crypt::decrypt($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
