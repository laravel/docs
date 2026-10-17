---
title: "Localização"
---

- [Introdução](#introduction)
    - [Publicando os Arquivos de Idioma](#publishing-the-language-files)
    - [Configurando o Locale](#configuring-the-locale)
    - [Idioma de Pluralização](#pluralization-language)
- [Definindo Strings de Tradução](#defining-translation-strings)
    - [Usando Chaves Curtas](#using-short-keys)
    - [Usando Strings de Tradução como Chaves](#using-translation-strings-as-keys)
- [Recuperando Strings de Tradução](#retrieving-translation-strings)
    - [Substituindo Parâmetros em Strings de Tradução](#replacing-parameters-in-translation-strings)
    - [Pluralização](#pluralization)
- [Sobrescrevendo Arquivos de Idioma de Pacotes](#overriding-package-language-files)

<a id="introduction"></a>
## Introdução

> **Nota:**
> Por padrão, o esqueleto da aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los através do comando Artisan `lang:publish`.

Os recursos de localização do Laravel fornecem uma maneira conveniente de recuperar strings em vários idiomas, permitindo que você suporte facilmente múltiplos idiomas dentro da sua aplicação.

O Laravel oferece duas maneiras de gerenciar strings de tradução. Primeiro, as strings de idioma podem ser armazenadas em arquivos dentro do diretório `lang` da aplicação. Dentro deste diretório, podem existir subdiretórios para cada idioma suportado pela aplicação. Esta é a abordagem que o Laravel usa para gerenciar strings de tradução de recursos integrados, como as mensagens de erro de validação:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

Ou, as strings de tradução podem ser definidas em arquivos JSON colocados dentro do diretório `lang`. Ao adotar essa abordagem, cada idioma suportado pela sua aplicação teria um arquivo JSON correspondente dentro deste diretório. Esta abordagem é recomendada para aplicações que possuem um grande número de strings traduzíveis:

```text
/lang
    en.json
    es.json
```

Discutiremos cada uma dessas abordagens para gerenciar strings de tradução nesta documentação.

<a id="publishing-the-language-files"></a>
### Publicando os Arquivos de Idioma

Por padrão, o esqueleto da aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel ou criar os seus próprios, deve criar a estrutura do diretório `lang` através do comando Artisan `lang:publish`. O comando `lang:publish` criará o diretório `lang` na sua aplicação e publicará o conjunto padrão de arquivos de idioma usados pelo Laravel:

```shell
php artisan lang:publish
```

<a id="configuring-the-locale"></a>
### Configurando o Locale

O idioma padrão da sua aplicação é armazenado na opção de configuração `locale` do arquivo de configuração `config/app.php`, que normalmente é definida pela variável de ambiente `APP_LOCALE`. Você é livre para modificar este valor de acordo com as necessidades da sua aplicação.

Você também pode configurar um "idioma de fallback", que será usado quando o idioma padrão não contiver uma determinada string de tradução. Assim como o idioma padrão, o idioma de fallback também é configurado no arquivo `config/app.php`, e seu valor normalmente é definido pela variável de ambiente `APP_FALLBACK_LOCALE`.

Você pode modificar o idioma padrão para uma única requisição HTTP em tempo de execução usando o método `setLocale` fornecido pela facade `App`:

```php
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<a id="determining-the-current-locale"></a>
#### Determinando o Locale Atual

Você pode usar os métodos `currentLocale` e `isLocale` na facade `App` para determinar o locale atual ou verificar se o locale é um determinado valor:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a id="pluralization-language"></a>
### Idioma de Pluralização

<style>
.code-list-no-flex-break code {
    display: contents !important;
}
</style>

<div class="code-list-no-flex-break">

Você pode instruir o "pluralizador" do Laravel, usado pelo Eloquent e outras partes do framework para converter strings no singular para o plural, a usar um idioma diferente do inglês. Isso pode ser feito invocando o método `useLanguage` dentro do método `boot` de um dos provedores de serviço da sua aplicação. Os idiomas atualmente suportados pelo pluralizador são: `french`, `norwegian-bokmal`, `portuguese`, `spanish` e `turkish`:

</div>

```php
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> **Aviso:**
> Se você personalizar o idioma do pluralizador, deve definir explicitamente os [nomes de tabela](../eloquent/#table-names) dos seus models Eloquent.

<a id="defining-translation-strings"></a>
## Definindo Strings de Tradução

<a id="using-short-keys"></a>
### Usando Chaves Curtas

Normalmente, as strings de tradução são armazenadas em arquivos dentro do diretório `lang`. Dentro deste diretório, deve haver um subdiretório para cada idioma suportado pela sua aplicação. Esta é a abordagem que o Laravel usa para gerenciar strings de tradução de recursos integrados, como as mensagens de erro de validação:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

Todos os arquivos de idioma retornam um array de strings indexadas por chave. Por exemplo:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> **Aviso:**
> Para idiomas que diferem por território, você deve nomear os diretórios de idioma de acordo com a ISO 15897. Por exemplo, "en_GB" deve ser usado para o inglês britânico em vez de "en-gb".

<a id="using-translation-strings-as-keys"></a>
### Usando Strings de Tradução como Chaves

Para aplicações com um grande número de strings traduzíveis, definir cada string com uma "chave curta" pode se tornar confuso ao referenciar as chaves nas suas views, e é trabalhoso inventar continuamente chaves para cada string de tradução suportada pela sua aplicação.

Por este motivo, o Laravel também oferece suporte para definir strings de tradução usando a tradução "padrão" da string como chave. Os arquivos de idioma que usam strings de tradução como chaves são armazenados como arquivos JSON no diretório `lang`. Por exemplo, se sua aplicação possui uma tradução para o espanhol, você deve criar um arquivo `lang/es.json`:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### Conflitos entre Chaves e Arquivos

Você não deve definir chaves de string de tradução que entrem em conflito com nomes de arquivos de tradução existentes. Por exemplo, traduzir `__('Action')` para o locale "NL" enquanto existe um arquivo `nl/action.php`, mas não existe um arquivo `nl.json`, fará com que o tradutor retorne todo o conteúdo de `nl/action.php`.

<a id="retrieving-translation-strings"></a>
## Recuperando Strings de Tradução

Você pode recuperar strings de tradução dos seus arquivos de idioma usando a função auxiliar `__`. Se você estiver usando "chaves curtas" para definir suas strings de tradução, deve passar para a função `__` o arquivo que contém a chave e a própria chave, usando a sintaxe de "ponto". Por exemplo, vamos recuperar a string de tradução `welcome` do arquivo de idioma `lang/en/messages.php`:

```php
echo __('messages.welcome');
```

Se a string de tradução especificada não existir, a função `__` retornará a chave da string de tradução. Assim, usando o exemplo acima, a função `__` retornaria `messages.welcome` caso a string de tradução não exista.

Se você estiver usando suas [strings de tradução padrão como chaves de tradução](#using-translation-strings-as-keys), deve passar a tradução padrão da sua string para a função `__`:

```php
echo __('I love programming.');
```

Novamente, se a string de tradução não existir, a função `__` retornará a chave da string de tradução que recebeu.

Se você estiver usando o [mecanismo de templates Blade](../blade/), pode usar a sintaxe de saída `{{ }}` para exibir a string de tradução:

```blade
{{ __('messages.welcome') }}
```

<a id="replacing-parameters-in-translation-strings"></a>
### Substituindo Parâmetros em Strings de Tradução

Se desejar, você pode definir placeholders nas suas strings de tradução. Todos os placeholders são prefixados com `:`. Por exemplo, você pode definir uma mensagem de boas-vindas com um placeholder de nome:

```php
'welcome' => 'Welcome, :name',
```

Para substituir os placeholders ao recuperar uma string de tradução, você pode passar um array de substituições como segundo argumento para a função `__`:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

Se o seu placeholder contiver apenas letras maiúsculas, ou tiver apenas a primeira letra em maiúscula, o valor traduzido será capitalizado de acordo:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a id="object-replacement-formatting"></a>
#### Formatação de Substituição de Objetos

Se você tentar fornecer um objeto como placeholder de tradução, o método `__toString` do objeto será invocado. O método [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) é um dos "métodos mágicos" integrados do PHP. No entanto, às vezes você pode não ter controle sobre o método `__toString` de uma determinada classe, como quando a classe com a qual você está interagindo pertence a uma biblioteca de terceiros.

Nesses casos, o Laravel permite que você registre um manipulador de formatação personalizado para aquele tipo específico de objeto. Para isso, você deve invocar o método `stringable` do tradutor. O método `stringable` aceita um closure, que deve tipar o tipo de objeto pelo qual ele é responsável por formatar. Normalmente, o método `stringable` deve ser invocado dentro do método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a id="pluralization"></a>
### Pluralização

A pluralização é um problema complexo, pois diferentes idiomas possuem uma variedade de regras complexas de pluralização; no entanto, o Laravel pode ajudá-lo a traduzir strings de forma diferente com base nas regras de pluralização que você definir. Usando o caractere `|`, você pode distinguir as formas singular e plural de uma string:

```php
'apples' => 'There is one apple|There are many apples',
```

Naturalmente, a pluralização também é suportada ao usar [strings de tradução como chaves](#using-translation-strings-as-keys):

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

Você pode até criar regras de pluralização mais complexas que especificam strings de tradução para múltiplos intervalos de valores:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

Depois de definir uma string de tradução com opções de pluralização, você pode usar a função `trans_choice` para recuperar a linha correspondente a uma determinada "contagem". Neste exemplo, como a contagem é maior que um, a forma plural da string de tradução é retornada:

```php
echo trans_choice('messages.apples', 10);
```

Você também pode definir atributos de placeholder nas strings de pluralização. Esses placeholders podem ser substituídos passando um array como terceiro argumento para a função `trans_choice`:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

Se você quiser exibir o valor inteiro que foi passado para a função `trans_choice`, pode usar o placeholder integrado `:count`:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a id="overriding-package-language-files"></a>
## Sobrescrevendo Arquivos de Idioma de Pacotes

Alguns pacotes podem vir com seus próprios arquivos de idioma. Em vez de alterar os arquivos principais do pacote para ajustar essas linhas, você pode sobrescrevê-las colocando arquivos no diretório `lang/vendor/{package}/{locale}`.

Assim, por exemplo, se você precisar sobrescrever as strings de tradução em inglês de `messages.php` para um pacote chamado `skyrim/hearthfire`, deve colocar um arquivo de idioma em: `lang/vendor/hearthfire/en/messages.php`. Dentro deste arquivo, você deve definir apenas as strings de tradução que deseja sobrescrever. Quaisquer strings de tradução que você não sobrescrever ainda serão carregadas dos arquivos de idioma originais do pacote.
