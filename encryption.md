# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Using The Encrypter](#using-the-encrypter)

<a name="introduction"></a>
## Introduction

Laravel's encrypter uses OpenSSL to provide AES-256 and AES-128 encryption. You are strongly encouraged to use Laravel's built-in encryption facilities and not attempt to roll your own "home grown" encryption algorithms. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value can not be modified once encrypted.

<a name="configuration"></a>
## Configuration

Before using Laravel's encrypter, you must set a `key` option in your `config/app.php` configuration file. You should use the `php artisan key:generate` command to generate this key since this Artisan command will use PHP's secure random bytes generator to build your key. If this value is not properly set, all values encrypted by Laravel will be insecure.

<a name="using-the-encrypter"></a>
## Using The Encrypter

#### Encrypting A Value

You may encrypt a value using the `encryptString` method of the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the `AES-256-CBC` cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC) to detect any modifications to the encrypted string:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Crypt;

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
                'secret' => Crypt::encryptString($request->secret),
            ])->save();
        }
    }

#### Decrypting A Value

You may decrypt values using the `decryptString` method of the `Crypt` facade. If the value can not be properly decrypted, such as when the MAC is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown:

    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
