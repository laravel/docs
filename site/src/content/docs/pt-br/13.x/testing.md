---
title: "Testes: Primeiros Passos"
---

- [Introdução](#introduction)
- [Ambiente](#environment)
- [Criando Testes](#creating-tests)
- [Executando Testes](#running-tests)
    - [Executando Testes em Paralelo](#running-tests-in-parallel)
    - [Relatando a Cobertura de Testes](#reporting-test-coverage)
    - [Perfilando Testes](#profiling-tests)
- [Cache de Configuração](#configuration-caching)

<a id="introduction"></a>
## Introdução

O Laravel foi construído pensando em testes. De fato, o suporte para testes com [Pest](https://pestphp.com) e [PHPUnit](https://phpunit.de) já vem incluído e um arquivo `phpunit.xml` já está configurado para sua aplicação. O framework também vem com métodos auxiliares convenientes que permitem testar suas aplicações de forma expressiva.

Por padrão, o diretório `tests` da sua aplicação contém dois diretórios: `Feature` e `Unit`. Testes unitários são testes que focam em uma porção muito pequena e isolada do seu código. De fato, a maioria dos testes unitários provavelmente foca em um único método. Testes dentro do seu diretório de testes "Unit" não inicializam sua aplicação Laravel e, portanto, são incapazes de acessar o banco de dados da sua aplicação ou outros serviços do framework.

Testes de feature podem testar uma porção maior do seu código, incluindo como vários objetos interagem entre si ou até mesmo uma requisição HTTP completa para um endpoint JSON. **Geralmente, a maioria dos seus testes deve ser de feature. Esses tipos de testes fornecem a maior confiança de que seu sistema como um todo está funcionando conforme o esperado.**

Um arquivo `ExampleTest.php` é fornecido em ambos os diretórios de testes `Feature` e `Unit`. Após instalar uma nova aplicação Laravel, execute os comandos `vendor/bin/pest`, `vendor/bin/phpunit` ou `php artisan test` para rodar seus testes.

<a id="environment"></a>
## Ambiente

Ao executar testes, o Laravel definirá automaticamente o [ambiente de configuração](../configuration/#environment-configuration) para `testing` por causa das variáveis de ambiente definidas no arquivo `phpunit.xml`. O Laravel também configura automaticamente a sessão e o cache para o driver `array`, de modo que nenhum dado de sessão ou cache seja persistido durante os testes.

Você é livre para definir outros valores de configuração de ambiente de teste conforme necessário. As variáveis de ambiente `testing` podem ser configuradas no arquivo `phpunit.xml` da sua aplicação, mas certifique-se de limpar seu cache de configuração usando o comando Artisan `config:clear` antes de executar seus testes!

<a id="the-env-testing-environment-file"></a>
#### O Arquivo de Ambiente `.env.testing`

Além disso, você pode criar um arquivo `.env.testing` na raiz do seu projeto. Este arquivo será usado em vez do arquivo `.env` ao executar testes do Pest e do PHPUnit ou ao executar comandos Artisan com a opção `--env=testing`.

<a id="creating-tests"></a>
## Criando Testes

Para criar um novo caso de teste, use o comando Artisan `make:test`. Por padrão, os testes serão colocados no diretório `tests/Feature`:

```shell
php artisan make:test UserTest
```

Se você quiser criar um teste dentro do diretório `tests/Unit`, você pode usar a opção `--unit` ao executar o comando `make:test`:

```shell
php artisan make:test UserTest --unit
```

Se você tiver uma classe de teste que depende principalmente dos recursos de teste do Laravel, mas um método de teste específico não precisa que o framework seja inicializado, você pode aplicar o atributo `#[UnitTest]` a esse método para pular a inicialização da aplicação apenas para esse teste.

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\Attributes\UnitTest;
use Tests\TestCase;

class LocationServiceTest extends TestCase
{
    public function test_get_coordinates_resolves_address(): void
    {
        // This test uses Laravel's testing features...
    }

    #[UnitTest]
    public function test_get_state_returns_state_from_abbreviation(): void
    {
        // This test runs without booting the application...
    }
}
```

> **Nota:**
> Os stubs de teste podem ser personalizados usando a [publicação de stubs](../artisan/#stub-customization).

Uma vez que o teste tenha sido gerado, você pode definir o teste como faria normalmente usando Pest ou PHPUnit. Para executar seus testes, execute o comando `vendor/bin/pest`, `vendor/bin/phpunit` ou `php artisan test` a partir do seu terminal:

```php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> **Aviso:**
> Se você definir seus próprios métodos `setUp` / `tearDown` dentro de uma classe de teste, certifique-se de chamar os respectivos métodos `parent::setUp()` / `parent::tearDown()` na classe pai. Tipicamente, você deve invocar `parent::setUp()` no início do seu próprio método `setUp` e `parent::tearDown()` no final do seu método `tearDown`.

<a id="running-tests"></a>
## Executando Testes

Como mencionado anteriormente, uma vez que você tenha escrito testes, você pode executá-los usando `pest` ou `phpunit`:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

Além dos comandos `pest` ou `phpunit`, você pode usar o comando Artisan `test` para executar seus testes. O executor de testes do Artisan fornece relatórios de teste detalhados para facilitar o desenvolvimento e a depuração:

```shell
php artisan test
```

Quaisquer argumentos que possam ser passados para os comandos `pest` ou `phpunit` também podem ser passados para o comando Artisan `test`:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a id="running-tests-in-parallel"></a>
### Executando Testes em Paralelo

Por padrão, o Laravel e o Pest / PHPUnit executam seus testes sequencialmente dentro de um único processo. No entanto, você pode reduzir bastante o tempo necessário para executar seus testes rodando-os simultaneamente em múltiplos processos. Para começar, você deve instalar o pacote Composer `brianium/paratest` como uma dependência de desenvolvimento ("dev"). Em seguida, inclua a opção `--parallel` ao executar o comando Artisan `test`:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

Por padrão, o Laravel criará tantos processos quantos forem os núcleos de CPU disponíveis na sua máquina. No entanto, você pode ajustar o número de processos usando a opção `--processes`:

```shell
php artisan test --parallel --processes=4
```

> **Aviso:**
> Ao executar testes em paralelo, algumas opções do Pest / PHPUnit (como `--do-not-cache-result`) podem não estar disponíveis.

<a id="parallel-testing-and-databases"></a>
#### Testes em Paralelo e Bancos de Dados

Contanto que você tenha configurado uma conexão de banco de dados primária, o Laravel lida automaticamente com a criação e migração de um banco de dados de teste para cada processo paralelo que está executando seus testes. Os bancos de dados de teste terão como sufixo um token de processo que é único por processo. Por exemplo, se você tiver dois processos de teste paralelos, o Laravel criará e usará os bancos de dados de teste `your_db_test_1` e `your_db_test_2`.

Por padrão, os bancos de dados de teste persistem entre as chamadas ao comando Artisan `test` para que possam ser usados novamente por invocações subsequentes do `test`. No entanto, você pode recriá-los usando a opção `--recreate-databases`:

```shell
php artisan test --parallel --recreate-databases
```

<a id="parallel-testing-hooks"></a>
#### Hooks de Testes em Paralelo

Ocasionalmente, você pode precisar preparar certos recursos usados pelos testes da sua aplicação para que possam ser usados com segurança por múltiplos processos de teste.

Usando a facade `ParallelTesting`, você pode especificar código a ser executado no `setUp` e no `tearDown` de um processo ou caso de teste. As closures fornecidas recebem as variáveis `$token` e `$testCase`, que contêm o token do processo e o caso de teste atual, respectivamente:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function (int $token) {
            // ...
        });
    }
}
```

<a id="accessing-the-parallel-testing-token"></a>
#### Acessando o Token de Testes em Paralelo

Se você quiser acessar o "token" do processo paralelo atual a partir de qualquer outro local no código de teste da sua aplicação, você pode usar o método `token`. Este token é um identificador de string único para um processo de teste individual e pode ser usado para segmentar recursos entre processos de teste paralelos. Por exemplo, o Laravel automaticamente anexa este token ao final dos bancos de dados de teste criados por cada processo de teste em paralelo:

    $token = ParallelTesting::token();

<a id="reporting-test-coverage"></a>
### Relatando a Cobertura de Testes

> **Aviso:**
> Este recurso requer [Xdebug](https://xdebug.org) ou [PCOV](https://pecl.php.net/package/pcov).

Ao executar os testes da sua aplicação, você pode querer determinar se seus casos de teste estão realmente cobrindo o código da aplicação e quanto do código da aplicação é usado ao executar seus testes. Para fazer isso, você pode fornecer a opção `--coverage` ao invocar o comando `test`:

```shell
php artisan test --coverage
```

<a id="enforcing-a-minimum-coverage-threshold"></a>
#### Impondo um Limite Mínimo de Cobertura

Você pode usar a opção `--min` para definir um limite mínimo de cobertura de testes para sua aplicação. A suíte de testes falhará se este limite não for atingido:

```shell
php artisan test --coverage --min=80.3
```

<a id="profiling-tests"></a>
### Perfilando Testes

O executor de testes do Artisan também inclui um mecanismo conveniente para listar os testes mais lentos da sua aplicação. Invoque o comando `test` com a opção `--profile` para receber uma lista dos seus dez testes mais lentos, permitindo que você investigue facilmente quais testes podem ser melhorados para acelerar sua suíte de testes:

```shell
php artisan test --profile
```

<a id="configuration-caching"></a>
## Cache de Configuração

Ao executar testes, o Laravel inicializa a aplicação para cada método de teste individual. Sem um arquivo de configuração em cache, cada arquivo de configuração da sua aplicação deve ser carregado no início de um teste. Para construir a configuração uma vez e reutilizá-la para todos os testes em uma única execução, você pode usar a trait `Illuminate\Foundation\Testing\WithCachedConfig`:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}
```
