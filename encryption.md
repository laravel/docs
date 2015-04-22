# Encriptação

- [Introdução](#introduction)
- [Basic Usage](#basic-usage)

<a name="introduction"></a>
## Introdução

Laravel fornece facildade para uma forte encriptação AES por meio da extenção PHP Mcrypt


<a name="basic-usage"></a>
## Uso Básico

#### Encriptando um Valor

	$encrypted = Crypt::encrypt('secret');


> **Nota:** Certifique-se de setar uma string radomica de 16, 24 , ou 32 caractéres na opção `key` do arquivo, `config/app.php`. Caso contrário, os valores encriptados não estarão seguros.


#### Decriptando Valores

	$decrypted = Crypt::decrypt($encryptedValue);

#### Setando O Modo e o Cipher

Você pode também setar o cipher e o modo usado pelo ecrypter:

	Crypt::setMode('ctr');

	Crypt::setCipher($cipher);
