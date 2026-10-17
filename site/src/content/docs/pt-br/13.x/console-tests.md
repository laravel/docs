---
title: "Testes de Console"
---

- [Introdução](#introduction)
- [Expectativas de Sucesso / Falha](#success-failure-expectations)
- [Expectativas de Entrada / Saída](#input-output-expectations)
- [Eventos de Console](#console-events)

<a id="introduction"></a>
## Introdução

Além de simplificar os testes HTTP, o Laravel fornece uma API simples para testar seus [comandos de console personalizados](../artisan/).

<a id="success-failure-expectations"></a>
## Expectativas de Sucesso / Falha

Para começar, vamos explorar como fazer asserções sobre o código de saída de um comando Artisan. Para isso, usaremos o método `artisan` para invocar um comando Artisan a partir do nosso teste. Em seguida, usaremos o método `assertExitCode` para verificar se o comando foi concluído com um determinado código de saída:

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

Você pode usar o método `assertNotExitCode` para verificar se o comando não foi encerrado com um determinado código de saída:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

É claro que, todos os comandos de terminal normalmente são encerrados com o código de status `0` quando são bem-sucedidos e com um código de saída diferente de zero quando não são. Portanto, por conveniência, você pode utilizar as asserções `assertSuccessful` e `assertFailed` para verificar se um determinado comando foi encerrado com um código de saída de sucesso ou não:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a id="input-output-expectations"></a>
## Expectativas de Entrada / Saída

O Laravel permite que você "simule" facilmente a entrada do usuário para seus comandos de console usando o método `expectsQuestion`. Além disso, você pode especificar o código de saída e o texto que espera que o comando de console exiba usando os métodos `assertExitCode` e `expectsOutput`. Por exemplo, considere o seguinte comando de console:

```php
Artisan::command('question', function () {
    $name = $this->ask('What is your name?');

    $language = $this->choice('Which language do you prefer?', [
        'PHP',
        'Ruby',
        'Python',
    ]);

    $this->line('Your name is '.$name.' and you prefer '.$language.'.');
});
```

Você pode testar este comando com o seguinte teste:

```php tab=Pest
test('console command', function () {
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
}
```

Se você estiver utilizando as funções `search` ou `multisearch` fornecidas pelo [Laravel Prompts](../prompts/), você pode usar a asserção `expectsSearch` para simular a entrada do usuário, os resultados da busca e a seleção:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
}
```

Você também pode verificar se um comando de console não gera nenhuma saída usando o método `doesntExpectOutput`:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
}
```

Os métodos `expectsOutputToContain` e `doesntExpectOutputToContain` podem ser usados para fazer asserções sobre uma parte da saída:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
}
```

<a id="confirmation-expectations"></a>
#### Expectativas de Confirmação

Ao escrever um comando que espera uma confirmação na forma de uma resposta "sim" ou "não", você pode utilizar o método `expectsConfirmation`:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a id="table-expectations"></a>
#### Expectativas de Tabela

Se o seu comando exibe uma tabela de informações usando o método `table` do Artisan, pode ser trabalhoso escrever expectativas de saída para a tabela inteira. Em vez disso, você pode usar o método `expectsTable`. Este método aceita os cabeçalhos da tabela como primeiro argumento e os dados da tabela como segundo argumento:

```php
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);
```

<a id="console-events"></a>
## Eventos de Console

Por padrão, os eventos `Illuminate\Console\Events\CommandStarting` e `Illuminate\Console\Events\CommandFinished` não são disparados durante a execução dos testes da sua aplicação. No entanto, você pode habilitar esses eventos para uma determinada classe de teste adicionando a trait `Illuminate\Foundation\Testing\WithConsoleEvents` à classe:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

pest()->use(WithConsoleEvents::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithConsoleEvents;
use Tests\TestCase;

class ConsoleEventTest extends TestCase
{
    use WithConsoleEvents;

    // ...
}
```
