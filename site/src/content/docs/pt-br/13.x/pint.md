---
title: "Laravel Pint"
---

- [Introdução](#introduction)
- [Instalação](#installation)
- [Executando o Pint](#running-pint)
- [Configurando o Pint](#configuring-pint)
    - [Presets](#presets)
    - [Regras](#rules)
    - [Excluindo Arquivos / Pastas](#excluding-files-or-folders)
- [Integração Contínua](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a id="introduction"></a>
## Introdução

[Laravel Pint](https://github.com/laravel/pint) é um corretor de estilo de código PHP opinativo, feito para minimalistas. O Pint é construído sobre o [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) e torna simples garantir que o estilo do seu código permaneça limpo e consistente.

O Pint é instalado automaticamente em todas as novas aplicações Laravel, para que você possa começar a usá-lo imediatamente. Por padrão, o Pint não requer nenhuma configuração e corrigirá problemas de estilo de código seguindo o estilo de código opinativo do Laravel.

<a id="installation"></a>
## Instalação

O Pint está incluído nas versões recentes do framework Laravel, então a instalação normalmente é desnecessária. No entanto, para aplicações mais antigas, você pode instalar o Laravel Pint via Composer:

```shell
composer require laravel/pint --dev
```

<a id="running-pint"></a>
## Executando o Pint

Você pode instruir o Pint a corrigir problemas de estilo de código invocando o binário `pint`, disponível no diretório `vendor/bin` do seu projeto:

```shell
./vendor/bin/pint
```

Se você quiser que o Pint seja executado em modo paralelo (experimental) para melhor desempenho, pode usar a opção `--parallel`:

```shell
./vendor/bin/pint --parallel
```

O modo paralelo também permite especificar o número máximo de processos a executar através da opção `--max-processes`. Se esta opção não for fornecida, o Pint usará todos os núcleos disponíveis na sua máquina:

```shell
./vendor/bin/pint --parallel --max-processes=4
```

Você também pode executar o Pint em arquivos ou diretórios específicos:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Por padrão, o Pint não formata templates Blade. Se você também quiser formatar seus arquivos `.blade.php`, pode usar a opção `--blade`, que habilita a regra [`Pint/laravel_blade`](#laravel-blade) apenas para a execução atual, sem modificar seu arquivo `pint.json`:

```shell
./vendor/bin/pint --blade
```

O Pint exibirá uma lista detalhada de todos os arquivos que ele atualiza. Você pode ver ainda mais detalhes sobre as alterações do Pint fornecendo a opção `-v` ao invocá-lo:

```shell
./vendor/bin/pint -v
```

Se você quiser que o Pint apenas inspecione seu código em busca de erros de estilo, sem realmente alterar os arquivos, pode usar a opção `--test`. O Pint retornará um código de saída diferente de zero se forem encontrados erros de estilo de código:

```shell
./vendor/bin/pint --test
```

Se você quiser que o Pint modifique apenas os arquivos que diferem da branch fornecida, de acordo com o Git, pode usar a opção `--diff=[branch]`. Isso pode ser usado de forma eficaz no seu ambiente de CI (como GitHub Actions) para economizar tempo, inspecionando apenas arquivos novos ou modificados:

```shell
./vendor/bin/pint --diff=main
```

Se você quiser que o Pint modifique apenas os arquivos que possuem alterações não commitadas, de acordo com o Git, use a opção `--dirty`:

```shell
./vendor/bin/pint --dirty
```

Se você quiser que o Pint corrija quaisquer arquivos com erros de estilo de código, mas também encerre com um código de saída diferente de zero caso algum erro tenha sido corrigido, pode usar a opção `--repair`:

```shell
./vendor/bin/pint --repair
```

<a id="configuring-pint"></a>
## Configurando o Pint

Como mencionado anteriormente, o Pint não requer nenhuma configuração. No entanto, se você quiser personalizar os presets, as regras ou as pastas inspecionadas, pode fazê-lo criando um arquivo `pint.json` no diretório raiz do seu projeto:

```json
{
    "preset": "laravel"
}
```

Além disso, se você quiser usar um `pint.json` de um diretório específico, pode fornecer a opção `--config` ao invocar o Pint:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a id="presets"></a>
### Presets

Presets definem um conjunto de regras que podem ser usadas para corrigir problemas de estilo de código no seu código. Por padrão, o Pint usa o preset `laravel`, que corrige problemas seguindo o estilo de código opinativo do Laravel. No entanto, você pode especificar um preset diferente fornecendo a opção `--preset` ao Pint:

```shell
./vendor/bin/pint --preset psr12
```

Se preferir, você também pode definir o preset no arquivo `pint.json` do seu projeto:

```json
{
    "preset": "psr12"
}
```

Os presets atualmente suportados pelo Pint são: `laravel`, `per`, `psr12`, `symfony` e `empty`.

<a id="rules"></a>
### Regras

Regras são diretrizes de estilo que o Pint usará para corrigir problemas de estilo de código no seu código. Como mencionado acima, os presets são grupos predefinidos de regras que devem ser perfeitos para a maioria dos projetos PHP, então normalmente você não precisará se preocupar com as regras individuais que eles contêm.

No entanto, se desejar, você pode habilitar ou desabilitar regras específicas no seu arquivo `pint.json` ou usar o preset `empty` e definir as regras do zero:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}
```

O Pint é construído sobre o [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Portanto, você pode usar qualquer uma de suas regras para corrigir problemas de estilo de código no seu projeto: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a id="custom-rules"></a>
#### Regras Personalizadas

Além das regras do PHP CS Fixer, o Pint fornece regras personalizadas com o prefixo `Pint/`. Essas regras não são habilitadas por padrão, mas você pode habilitá-las no seu arquivo `pint.json`.

<a id="laravel-blade"></a>
##### `Pint/laravel_blade`

Esta regra formata seus templates Blade, aplicando indentação, espaçamento e formatação de atributos consistentes aos seus arquivos `.blade.php`. Por padrão, o Pint não formata arquivos Blade, então você deve habilitar esta regra no seu arquivo `pint.json` para optar por ela:

```json
{
    "preset": "laravel",
    "rules": {
        "Pint/laravel_blade": true
    }
}
```

Uma vez habilitada, o Pint formatará seus templates Blade, além dos seus arquivos PHP, sempre que for executado:

```shell
./vendor/bin/pint
```

Alternativamente, se você quiser habilitar esta regra para uma única execução, sem modificar seu arquivo `pint.json`, pode usar a opção `--blade`:

```shell
./vendor/bin/pint --blade
```

Nos bastidores, esta regra usa o [Prettier](https://prettier.io) junto com os plugins `prettier-plugin-blade` e `prettier-plugin-tailwindcss`, então o [Node.js](https://nodejs.org) precisa estar instalado na sua máquina. Na primeira vez que você executar o Pint com esta regra habilitada, o Pint detectará quaisquer dependências do Prettier ausentes e solicitará que você as instale.

> **Nota:**
> Esta regra ignora automaticamente arquivos que normalmente dependem da própria formatação, como as diretrizes do [Laravel Boost](https://github.com/laravel/boost) e as views de e-mail localizadas nos diretórios `resources/views/emails` e `resources/views/mail`.

<a id="phpdoc-type-annotations-only"></a>
##### `Pint/phpdoc_type_annotations_only`

Esta regra remove todos os comentários e a prosa de docblocks do seu código, mantendo apenas as linhas que contêm anotações `@`, como `@param`, `@return`, `@var`, `@phpstan-type`, etc.:

```php
/**
 * Get the posts for the user. [tl! remove]
 * [tl! remove]
 * @return HasMany<Post, $this>
 */
public function posts(): HasMany
```

Comentários de uma única linha e comentários de bloco sem anotações `@` são removidos por completo. Se você quiser manter um comentário específico, pode prefixá-lo com `@note`, `@warning` ou `@todo`:

```php
// @note This comment will be preserved.
```

Para habilitar esta regra, adicione-a ao seu arquivo `pint.json`:

```json
{
    "preset": "laravel",
    "rules": {
        "Pint/phpdoc_type_annotations_only": true
    }
}
```

> **Nota:**
> Esta regra ignora automaticamente arquivos do diretório `config`, pois os arquivos de configuração normalmente dependem de comentários para documentação.

<a id="excluding-files-or-folders"></a>
### Excluindo Arquivos / Pastas

Por padrão, o Pint inspecionará todos os arquivos `.php` do seu projeto, exceto os do diretório `vendor`. Se você quiser excluir mais pastas, pode fazê-lo usando a opção de configuração `exclude`:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

Se você quiser excluir todos os arquivos que contenham um determinado padrão de nome, pode fazê-lo usando a opção de configuração `notName`:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

Se você quiser excluir um arquivo fornecendo o caminho exato até ele, pode fazê-lo usando a opção de configuração `notPath`:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a id="continuous-integration"></a>
## Integração Contínua

<a id="running-tests-on-github-actions"></a>
### GitHub Actions

Para automatizar a verificação de estilo do seu projeto com o Laravel Pint, você pode configurar o [GitHub Actions](https://github.com/features/actions) para executar o Pint sempre que novo código for enviado ao GitHub. Primeiro, certifique-se de conceder "Read and write permissions" aos workflows no GitHub em **Settings > Actions > General > Workflow permissions**. Em seguida, crie um arquivo `.github/workflows/lint.yml` com o seguinte conteúdo:

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          tools: pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v6
```
