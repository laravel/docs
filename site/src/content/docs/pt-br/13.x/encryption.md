---
title: "Encryption"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
    - [Rotacionando Chaves de Criptografia de Forma Graciosa](#gracefully-rotating-encryption-keys)
- [Usando o Encrypter](#using-the-encrypter)

<a id="introduction"></a>
## Introdução

Os serviços de criptografia do Laravel fornecem uma interface simples e conveniente para criptografar e descriptografar texto via OpenSSL usando criptografia AES-256 e AES-128. Todos os valores criptografados do Laravel são assinados usando um código de autenticação de mensagem (MAC), de modo que seu valor subjacente não possa ser modificado ou adulterado uma vez criptografado.

<a id="configuration"></a>
## Configuração

Antes de usar o encrypter do Laravel, você deve definir a opção de configuração `key` no seu arquivo de configuração `config/app.php`. Esse valor de configuração é controlado pela variável de ambiente `APP_KEY`. Você deve usar o comando `php artisan key:generate` para gerar o valor dessa variável, pois o comando `key:generate` usará o gerador de bytes aleatórios seguros do PHP para construir uma chave criptograficamente segura para sua aplicação. Normalmente, o valor da variável de ambiente `APP_KEY` será gerado para você durante a [instalação do Laravel](/en/installation/).

<a id="gracefully-rotating-encryption-keys"></a>
### Rotacionando Chaves de Criptografia de Forma Graciosa

Se você alterar a chave de criptografia da sua aplicação, todas as sessões de usuários autenticados serão desconectadas da sua aplicação. Isso acontece porque todos os cookies, incluindo os cookies de sessão, são criptografados pelo Laravel. Além disso, não será mais possível descriptografar nenhum dado que tenha sido criptografado com sua chave de criptografia anterior.

Para mitigar esse problema, o Laravel permite que você liste suas chaves de criptografia anteriores na variável de ambiente `APP_PREVIOUS_KEYS` da sua aplicação. Essa variável pode conter uma lista separada por vírgulas de todas as suas chaves de criptografia anteriores:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

Quando você define essa variável de ambiente, o Laravel sempre usará a chave de criptografia "atual" ao criptografar valores. Porém, ao descriptografar valores, o Laravel tentará primeiro a chave atual e, se a descriptografia falhar usando a chave atual, o Laravel tentará todas as chaves anteriores até que uma delas seja capaz de descriptografar o valor.

Essa abordagem de descriptografia graciosa permite que os usuários continuem usando sua aplicação sem interrupções, mesmo que sua chave de criptografia seja rotacionada.

<a id="using-the-encrypter"></a>
## Usando o Encrypter

<a id="encrypting-a-value"></a>
#### Criptografando um Valor

Você pode criptografar um valor usando o método `encryptString` fornecido pela facade `Crypt`. Todos os valores criptografados são criptografados usando OpenSSL e o cipher AES-256-CBC. Além disso, todos os valores criptografados são assinados com um código de autenticação de mensagem (MAC). O código de autenticação de mensagem integrado impedirá a descriptografia de quaisquer valores que tenham sido adulterados por usuários maliciosos:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a id="decrypting-a-value"></a>
#### Descriptografando um Valor

Você pode descriptografar valores usando o método `decryptString` fornecido pela facade `Crypt`. Se o valor não puder ser descriptografado corretamente, como quando o código de autenticação de mensagem é inválido, uma exceção `Illuminate\Contracts\Encryption\DecryptException` será lançada:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```