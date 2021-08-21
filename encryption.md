# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Using The Encrypter](#using-the-encrypter)

<a name="introduction"></a>
## Introduction

Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value can not be modified or tampered with once encrypted.

<a name="configuration"></a>
## Configuration

Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/{{version}}/installation).

> {note} When the value of `APP_KEY` is changed or rotated, you won't be able to decrypt previously encrypted data

<a name="using-the-encrypter"></a>
## Using The Encrypter

<a name="encrypting-a-value"></a>
#### Encrypting A Value

You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Models\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Crypt;

    class DigitalOceanTokenController extends Controller
    {
        /**
         * Store a DigitalOcean API token for the user.
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
#### Decrypting A Value

You may decrypt values using the `decryptString` method provided by the `Crypt` facade. If the value can not be properly decrypted, such as when the message authentication code is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown:

    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        //
    }
