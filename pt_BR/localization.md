# Localização

- [Intrudução](#introduction)
- [Utilização Básica](#basic-usage)
    - [Pluralização](#pluralization)
- [Sobrescrevendo Arquivos de Linguagem de Terceiros](#overriding-vendor-language-files)

<a name="introduction"></a>
## Introdução

O Laravel provê uma maneira conveniente de recuperar strings baseadas em diferentes idiomas, permitindo a você facilmente dar suporte a múltiplos idiomas em sua aplicação.

As strings de linguagem ficam armazenadas em arquivos dentro do diretório `resources/lang`. Dentro desse diretório deve haver um sub-diretório para cada linguagem que sua aplicação dará suporte.

    /resources
        /lang
            /en
                messages.php
            /es
                messages.php

Todos os arquivos simplesmente retornam um array associativo de strings. Por exemplo:

    <?php

    return [
        'welcome' => 'Welcome to our application'
    ];


#### Configurando o Locale

A linguagem padrão da sua aplicação está no arquivo de configuração `config/app.php`. E é claro, você pode modificar esse valor para se adaptar às necessidades da sua aplicação. Você também pode alternar entre linguagens durante a execução da aplicação usando o método `setLocale` do facade `App`:

    Route::get('welcome/{locale}', function ($locale) {
        App::setLocale($locale);

        //
    });

Você também deve configurar uma linguagem de "fallback" (reserva), que será usada em casos da linguagem ativa não conter uma determinada linha. Como a linguagem padrão, o fallback pode ser configurado em `config/app.php`:

    'fallback_locale' => 'en',

<a name="basic-usage"></a>
## Utilização Básica

Você pode obter linhas dos seus arquivos de linguagem usando a função utilitária `trans`. Essa função aceita o nome do arquivo e a chave (índice) da linha da linguagem em seu primeiro argumento. Por exemplo, vamos recuperar a linha `welcome` do arquivo de `resources/lang/en/messages.php`:

    echo trans('messages.welcome');

E é claro, se você está usando os [templates Blade](/docs/{{version}}/blade), você pode usar a sintaxe `{{ }}` para "echo" (imprimir, exibir) a string:

    {{ trans('messages.welcome') }}


Se você especificou uma chave cujo a tradução não existe, a função `trans` irá retornar essa chave. Então, usando o exemplo anterior, a função `trans` retornaria `messages.welcome` se essa chave não existisse no arquivo `messages.php`.

#### Sobrescrevendo Parâmetros

Se você desejar, você pode definir place-holders nas suas strings de linguagem. Todos os place-holders devem ser prefixados com `:`. Por exemplo, você pode definir uma mensagem de `welcome` com um nome de place-holder:

    'welcome' => 'Welcome, :name',

Para substituir esse place-holder quando recupera essa linha, passe um array associativo com as substituições como segundo argumento para a função `trans`:

    echo trans('messages.welcome', ['name' => 'Dayle']);

<a name="pluralization"></a>
### Pluralização

Pluralização é um problema complexo, diferentes linguagens tem uma variedade de regras complexas para isso. Usando o caractere "pipe", você pode distinguir uma string no singular de outra no plural:

    'apples' => 'There is one apple|There are many apples',

Então, você pode usar a função `trans_choice` para recuperar essa linha baseado em uma "count" (quantidade). Neste exemplo, o `count` é maior que um, a forma plural da string será retornada:

    echo trans_choice('messages.apples', 10);

Você pode criar até regras mais complexas de pluralização:

    'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="overriding-vendor-language-files"></a>
## Sobrescrevendo Arquivos de Linguagem de Terceiros

Alguns pacotes podem conter seus próprios arquivos de linguagem. Ao invés de hackear o core do pacote para corrigir algumas linhas, você pode sobrescrevê-las criando seus próprios arquivos no diretório `resources/lang/vendor/{package}/{locale}`.

Então, por exemplo, se você precisa sobrescrever a linguagem English no arquivo `messages.php` de um pacote chamado `skyrim/hearthfire`, você pode adicionar o arquivo de linguagem em `resources/lang/vendor/hearthfire/en/messages.php`. Nesse arquivo você deve definir somente as linhas que gostaria de sobrescrever. As linhas que você não sobrescrever ainda serão lidas do arquivo de linguagem original do pacote.
