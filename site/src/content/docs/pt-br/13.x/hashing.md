---
title: "Hashing"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
- [Uso Básico](#basic-usage)
    - [Gerando Hash de Senhas](#hashing-passwords)
    - [Verificando se uma Senha Corresponde a um Hash](#verifying-that-a-password-matches-a-hash)
    - [Determinando se uma Senha Precisa ser Re-hasheada](#determining-if-a-password-needs-to-be-rehashed)
- [Verificação do Algoritmo de Hash](#hash-algorithm-verification)

<a id="introduction"></a>
## Introdução

A [facade](/en/facades/) `Hash` do Laravel fornece hashing seguro com Bcrypt e Argon2 para armazenar senhas de usuários. Se você estiver usando um dos [starter kits de aplicação do Laravel](/en/starter-kits/), o Bcrypt será usado por padrão para registro e autenticação.

O Bcrypt é uma ótima escolha para gerar hash de senhas porque seu "fator de trabalho" (work factor) é ajustável, o que significa que o tempo necessário para gerar um hash pode ser aumentado conforme o poder de hardware aumenta. Ao gerar hash de senhas, lento é bom. Quanto mais tempo um algoritmo leva para gerar o hash de uma senha, mais tempo leva para usuários maliciosos gerarem "rainbow tables" de todos os valores de hash de string possíveis que podem ser usados em ataques de força bruta contra aplicações.

<a id="configuration"></a>
## Configuração

Por padrão, o Laravel usa o driver de hashing `bcrypt` ao gerar hash de dados. No entanto, vários outros drivers de hashing são suportados, incluindo [argon](https://en.wikipedia.org/wiki/Argon2) e [argon2id](https://en.wikipedia.org/wiki/Argon2).

Você pode especificar o driver de hashing da sua aplicação usando a variável de ambiente `HASH_DRIVER`. Mas, se quiser personalizar todas as opções do driver de hashing do Laravel, você deve publicar o arquivo de configuração `hashing` completo usando o comando Artisan `config:publish`:

```shell
php artisan config:publish hashing
```

<a id="basic-usage"></a>
## Uso Básico

<a id="hashing-passwords"></a>
### Gerando Hash de Senhas

Você pode gerar o hash de uma senha chamando o método `make` na facade `Hash`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     */
    public function update(Request $request): RedirectResponse
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a id="adjusting-the-bcrypt-work-factor"></a>
#### Ajustando o Work Factor do Bcrypt

Se você estiver usando o algoritmo Bcrypt, o método `make` permite gerenciar o work factor do algoritmo usando a opção `rounds`; no entanto, o work factor padrão gerenciado pelo Laravel é aceitável para a maioria das aplicações:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a id="adjusting-the-argon2-work-factor"></a>
#### Ajustando o Work Factor do Argon2

Se você estiver usando o algoritmo Argon2, o método `make` permite gerenciar o work factor do algoritmo usando as opções `memory`, `time` e `threads`; no entanto, os valores padrão gerenciados pelo Laravel são aceitáveis para a maioria das aplicações:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> **Note:**
> Para mais informações sobre essas opções, consulte a [documentação oficial do PHP sobre o hashing com Argon](https://secure.php.net/manual/en/function.password-hash.php).

<a id="verifying-that-a-password-matches-a-hash"></a>
### Verificando se uma Senha Corresponde a um Hash

O método `check` fornecido pela facade `Hash` permite verificar se uma determinada string de texto puro corresponde a um determinado hash:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a id="determining-if-a-password-needs-to-be-rehashed"></a>
### Determinando se uma Senha Precisa ser Re-hasheada

O método `needsRehash` fornecido pela facade `Hash` permite determinar se o work factor usado pelo hasher mudou desde que a senha foi hasheada. Algumas aplicações optam por realizar essa verificação durante o processo de autenticação da aplicação:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a id="hash-algorithm-verification"></a>
## Verificação do Algoritmo de Hash

Para prevenir a manipulação do algoritmo de hash, o método `Hash::check` do Laravel primeiro verificará se o hash fornecido foi gerado usando o algoritmo de hashing selecionado pela aplicação. Se os algoritmos forem diferentes, uma exceção `RuntimeException` será lançada.

Esse é o comportamento esperado para a maioria das aplicações, onde não se espera que o algoritmo de hashing mude e algoritmos diferentes podem ser uma indicação de um ataque malicioso. No entanto, se você precisar suportar múltiplos algoritmos de hashing na sua aplicação, como ao migrar de um algoritmo para outro, você pode desabilitar a verificação do algoritmo de hash definindo a variável de ambiente `HASH_VERIFY` como `false`:

```ini
HASH_VERIFY=false
```