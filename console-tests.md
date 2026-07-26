---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Тестування консольних команд

- [Вступ](#introduction)
- [Очікування успіху / невдачі](#success-failure-expectations)
- [Очікування щодо вводу / виводу](#input-output-expectations)
- [Консольні події](#console-events)

<a name="introduction"></a>
## Вступ

Окрім спрощення тестування HTTP, Laravel надає простий API для тестування [власних консольних команд](/docs/{{version}}/artisan) вашого застосунку.

<a name="success-failure-expectations"></a>
## Очікування успіху / невдачі

Для початку розгляньмо, як робити твердження щодо коду виходу артизан-команди. Для цього ми скористаємося методом `artisan`, щоб викликати артизан-команду з нашого тесту. Далі методом `assertExitCode` перевіримо, що команда завершилася із заданим кодом виходу:

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

Метод `assertNotExitCode` дозволяє перевірити, що команда завершилася не із заданим кодом виходу:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

Звісно, всі термінальні команди зазвичай завершуються з кодом статусу `0`, коли вони успішні, і з ненульовим кодом, коли ні. Тому для зручності ви можете скористатися твердженнями `assertSuccessful` та `assertFailed`, щоб перевірити, чи завершилася команда з успішним кодом виходу:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
## Очікування щодо вводу / виводу

Laravel дозволяє легко «підробити» ввід користувача для ваших консольних команд методом `expectsQuestion`. Крім того, ви можете вказати код виходу й текст, який очікуєте побачити у виводі команди, методами `assertExitCode` та `expectsOutput`. Розгляньмо, наприклад, таку консольну команду:

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

Протестувати цю команду можна таким тестом:

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

Якщо ви користуєтеся функціями `search` чи `multisearch` із [Laravel Prompts](/docs/{{version}}/prompts), скористайтеся твердженням `expectsSearch`, щоб підробити ввід користувача, результати пошуку та вибір:

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

Ви також можете перевірити, що консольна команда не дає жодного виводу, методом `doesntExpectOutput`:

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

Методи `expectsOutputToContain` та `doesntExpectOutputToContain` дозволяють робити твердження щодо частини виводу:

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

<a name="confirmation-expectations"></a>
#### Очікування підтвердження

Пишучи команду, яка очікує підтвердження у вигляді відповіді «так» чи «ні», скористайтеся методом `expectsConfirmation`:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
#### Очікування щодо таблиць

Якщо ваша команда показує таблицю з інформацією через артизан-метод `table`, писати очікування щодо виводу всієї таблиці буває незручно. Натомість скористайтеся методом `expectsTable`. Він приймає заголовки таблиці першим аргументом і дані таблиці другим:

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

<a name="console-events"></a>
## Консольні події

За замовчуванням події `Illuminate\Console\Events\CommandStarting` та `Illuminate\Console\Events\CommandFinished` не відправляються під час прогону тестів вашого застосунку. Проте ви можете ввімкнути ці події для певного тестового класу, додавши до нього трейт `Illuminate\Foundation\Testing\WithConsoleEvents`:

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
