# Encryption

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)

<a name="configuration"></a>
## Configuration

Before using Laravel's encrypter, you should set the `key` option of your `config/app.php` configuration file to a 32 character, random string. If this value is not properly set, all values encrypted by Laravel will be insecure.

<a name="basic-usage"></a>
## Basic Usage

#### Encrypting A Value

You may encrypt a value using the `Crypt` [facade](/docs/{{version}}/facades). All encrypted values are encrypted using OpenSSL and the `AES-256-CBC` cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC) to detect any modifications to the encrypted string.

For example, we may use the `encrypt` method to encrypt a secret and store it on an [Eloquent model](/docs/{{version}}/eloquent):

    <?php

    namespace App\Http\Controllers;

    use Crypt;
    use App\User;
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

> **Note:** Encrypted values are passed through `serialize` during encryption, which allows for "encryption" of objects and arrays. Thus, non-PHP clients receiving encrypted values will need to `unserialize` the data.

#### Decrypting A Value

Of course, you may decrypt values using the `decrypt` method on the `Crypt` facade. If the value can not be properly decrypted, such as when the MAC is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown:

    use Illuminate\Contracts\Encryption\DecryptException;

    try {
        $decrypted = Crypt::decrypt($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
