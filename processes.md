---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Процеси

- [Вступ](#introduction)
- [Виклик процесів](#invoking-processes)
    - [Опції процесу](#process-options)
    - [Вивід процесу](#process-output)
    - [Конвеєри](#process-pipelines)
- [Асинхронні процеси](#asynchronous-processes)
    - [ID процесів і сигнали](#process-ids-and-signals)
    - [Вивід асинхронних процесів](#asynchronous-process-output)
    - [Таймаути асинхронних процесів](#asynchronous-process-timeouts)
- [Паралельні процеси](#concurrent-processes)
    - [Іменування процесів пулу](#naming-pool-processes)
    - [ID процесів пулу та сигнали](#pool-process-ids-and-signals)
- [Тестування](#testing)
    - [Підміна процесів](#faking-processes)
    - [Підміна конкретних процесів](#faking-specific-processes)
    - [Підміна послідовностей процесів](#faking-process-sequences)
    - [Підміна життєвого циклу асинхронних процесів](#faking-asynchronous-process-lifecycles)
    - [Доступні перевірки](#available-assertions)
    - [Запобігання «блукаючим» процесам](#preventing-stray-processes)

<a name="introduction"></a>
## Вступ

Laravel надає виразний мінімалістичний API навколо [компонента Symfony Process](https://symfony.com/doc/current/components/process.html), який дозволяє зручно викликати зовнішні процеси з вашого застосунку Laravel. Можливості роботи з процесами в Laravel зосереджені на найпоширеніших сценаріях і чудовому досвіді розробника.

<a name="invoking-processes"></a>
## Виклик процесів

Щоб викликати процес, скористайтеся методами `run` та `start` фасаду `Process`. Метод `run` викликає процес і чекає на завершення його виконання, а метод `start` призначений для асинхронного виконання. Ми розглянемо обидва підходи в цій документації. Спершу подивімося, як викликати простий синхронний процес і оглянути його результат:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

Звісно, екземпляр `Illuminate\Contracts\Process\ProcessResult`, який повертає метод `run`, пропонує низку корисних методів для огляду результату процесу:

```php
$result = Process::run('ls -la');

$result->command();
$result->successful();
$result->failed();
$result->output();
$result->errorOutput();
$result->exitCode();
```

<a name="throwing-exceptions"></a>
#### Викидання винятків

Якщо ви маєте результат процесу й хочете викинути екземпляр `Illuminate\Process\Exceptions\ProcessFailedException`, коли код виходу більший за нуль (що означає невдачу), скористайтеся методами `throw` та `throwIf`. Якщо процес не провалився, буде повернуто екземпляр `ProcessResult`:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### Опції процесу

Звісно, вам може знадобитися налаштувати поведінку процесу перед його викликом. На щастя, Laravel дозволяє підкрутити різні характеристики процесу: робочий каталог, таймаут і змінні середовища.

<a name="working-directory-path"></a>
#### Шлях робочого каталогу

Метод `path` дозволяє вказати робочий каталог процесу. Якщо цей метод не викликано, процес успадкує робочий каталог PHP-скрипта, що виконується:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### Ввід

Ви можете передати ввід через «стандартний ввід» процесу методом `input`:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### Таймаути

За замовчуванням процеси викидають екземпляр `Illuminate\Process\Exceptions\ProcessTimedOutException` після понад 60 секунд виконання. Проте ви можете змінити цю поведінку методом `timeout`:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

Методи `timeout` та `idleTimeout` також приймають екземпляри `CarbonInterval`:

```php
use function Illuminate\Support\minutes;

$result = Process::timeout(minutes(2))->run('bash import.sh');
```

Або ж, якщо ви хочете вимкнути таймаут процесу взагалі, викличте метод `forever`:

```php
$result = Process::forever()->run('bash import.sh');
```

Метод `idleTimeout` дозволяє вказати максимальну кількість секунд, які процес може працювати, не повертаючи жодного виводу:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### Змінні середовища

Змінні середовища можна передати процесу методом `env`. Викликаний процес також успадкує всі змінні середовища, задані вашою системою:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

Якщо ви хочете прибрати успадковану змінну середовища з викликаного процесу, передайте цій змінній значення `false`:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### Режим TTY

Метод `tty` дозволяє увімкнути для вашого процесу режим TTY. Режим TTY під'єднує ввід і вивід процесу до вводу й виводу вашої програми, дозволяючи процесу відкрити редактор на кшталт Vim чи Nano:

```php
Process::forever()->tty()->run('vim');
```

> [!WARNING]
> Режим TTY не підтримується у Windows.

<a name="process-output"></a>
### Вивід процесу

Як уже згадувалося, до виводу процесу можна звернутися методами `output` (stdout) та `errorOutput` (stderr) на результаті процесу:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

Проте вивід можна збирати й у реальному часі, передавши замикання другим аргументом методу `run`. Замикання отримає два аргументи: «тип» виводу (`stdout` чи `stderr`) і сам рядок виводу:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel також пропонує методи `seeInOutput` та `seeInErrorOutput`, які дають зручний спосіб визначити, чи містив вивід процесу заданий рядок:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### Вимкнення виводу процесу

Якщо ваш процес пише багато виводу, який вас не цікавить, ви можете заощадити пам'ять, вимкнувши отримання виводу взагалі. Для цього викличте метод `quietly` під час побудови процесу:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### Конвеєри

Інколи вам може захотітися зробити вивід одного процесу вводом іншого. Це часто називають «пайпінгом» виводу одного процесу в інший. Метод `pipe` фасаду `Process` спрощує це завдання. Метод `pipe` виконає процеси конвеєра синхронно й поверне результат останнього процесу в конвеєрі:

```php
use Illuminate\Process\Pipe;
use Illuminate\Support\Facades\Process;

$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
});

if ($result->successful()) {
    // ...
}
```

Якщо вам не потрібно налаштовувати окремі процеси конвеєра, ви можете просто передати методу `pipe` масив рядків-команд:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

Вивід процесу можна збирати в реальному часі, передавши замикання другим аргументом методу `pipe`. Замикання отримає два аргументи: «тип» виводу (`stdout` чи `stderr`) і сам рядок виводу:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel також дозволяє призначати рядкові ключі кожному процесу конвеєра методом `as`. Цей ключ також буде передано до замикання виводу, переданого методу `pipe`, тож ви зможете визначити, якому процесу належить вивід:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## Асинхронні процеси

Якщо метод `run` викликає процеси синхронно, то метод `start` дозволяє викликати процес асинхронно. Це дає вашому застосунку змогу виконувати інші задачі, доки процес працює у фоні. Щойно процес викликано, ви можете скористатися методом `running`, щоб визначити, чи він ще працює:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

Як ви могли помітити, ви можете викликати метод `wait`, щоб дочекатися завершення процесу й отримати екземпляр `ProcessResult`:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### ID процесів і сигнали

Метод `id` дозволяє дізнатися ID запущеного процесу, призначений операційною системою:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

Метод `signal` дозволяє надіслати «сигнал» запущеному процесу. Список наперед визначених констант сигналів можна знайти в [документації PHP](https://www.php.net/manual/en/pcntl.constants.php):

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### Вивід асинхронних процесів

Доки асинхронний процес працює, ви можете звернутися до всього його поточного виводу методами `output` та `errorOutput`; проте методи `latestOutput` і `latestErrorOutput` дозволяють отримати вивід процесу, що з'явився з моменту останнього отримання:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

Як і з методом `run`, вивід асинхронних процесів можна збирати в реальному часі, передавши замикання другим аргументом методу `start`. Замикання отримає два аргументи: «тип» виводу (`stdout` чи `stderr`) і сам рядок виводу:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

Замість чекати на завершення процесу, ви можете скористатися методом `waitUntil`, щоб припинити очікування на основі виводу процесу. Laravel перестане чекати на завершення процесу, коли замикання, передане методу `waitUntil`, поверне `true`:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### Таймаути асинхронних процесів

Доки асинхронний процес працює, ви можете перевірити, що він не вичерпав таймаут, методом `ensureNotTimedOut`. Цей метод викине [виняток таймауту](#timeouts), якщо процес його вичерпав:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## Паралельні процеси

Laravel також дуже спрощує керування пулом паралельних асинхронних процесів, дозволяючи легко виконувати багато задач одночасно. Для початку викличте метод `pool`, який приймає замикання, що отримує екземпляр `Illuminate\Process\Pool`.

У цьому замиканні ви можете описати процеси, які належать пулу. Щойно пул процесів запущено методом `start`, ви можете звернутися до [колекції](/docs/{{version}}/collections) запущених процесів методом `running`:

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

$pool = Process::pool(function (Pool $pool) {
    $pool->path(__DIR__)->command('bash import-1.sh');
    $pool->path(__DIR__)->command('bash import-2.sh');
    $pool->path(__DIR__)->command('bash import-3.sh');
})->start(function (string $type, string $output, int $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();
```

Як бачите, ви можете дочекатися завершення всіх процесів пулу й отримати їхні результати методом `wait`. Метод `wait` повертає об'єкт із доступом як до масиву, що дозволяє звертатися до екземпляра `ProcessResult` кожного процесу пулу за його ключем:

```php
$results = $pool->wait();

echo $results[0]->output();
```

Або ж, для зручності, метод `concurrently` дозволяє запустити асинхронний пул процесів і одразу дочекатися його результатів. Це дає особливо виразний синтаксис у поєднанні з деструктуризацією масивів PHP:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### Іменування процесів пулу

Звертатися до результатів пулу за числовим ключем не надто виразно; тому Laravel дозволяє призначати рядкові ключі кожному процесу пулу методом `as`. Цей ключ також буде передано до замикання, переданого методу `start`, тож ви зможете визначити, якому процесу належить вивід:

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->as('first')->command('bash import-1.sh');
    $pool->as('second')->command('bash import-2.sh');
    $pool->as('third')->command('bash import-3.sh');
})->start(function (string $type, string $output, string $key) {
    // ...
});

$results = $pool->wait();

return $results['first']->output();
```

<a name="pool-process-ids-and-signals"></a>
### ID процесів пулу та сигнали

Оскільки метод `running` пулу процесів надає колекцію всіх викликаних у пулі процесів, ви можете легко дістати ID цих процесів:

```php
$processIds = $pool->running()->each->id();
```

А для зручності ви можете викликати на пулі процесів метод `signal`, щоб надіслати сигнал кожному процесу пулу:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## Тестування

Багато сервісів Laravel надають можливості, які допомагають легко й виразно писати тести, і сервіс процесів Laravel не виняток. Метод `fake` фасаду `Process` дозволяє сказати Laravel повертати підставні / фіктивні результати під час виклику процесів.

<a name="faking-processes"></a>
### Підміна процесів

Щоб дослідити можливості Laravel з підміни процесів, уявімо маршрут, який викликає процес:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

Тестуючи цей маршрут, ми можемо сказати Laravel повертати фейковий успішний результат для кожного викликаного процесу, викликавши метод `fake` фасаду `Process` без аргументів. Ба більше, ми можемо навіть [перевірити](#available-assertions), що заданий процес було «запущено»:

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // Simple process assertion...
    Process::assertRan('bash import.sh');

    // Or, inspecting the process configuration...
    Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
        return $process->command === 'bash import.sh' &&
               $process->timeout === 60;
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // Simple process assertion...
        Process::assertRan('bash import.sh');

        // Or, inspecting the process configuration...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

Як уже зазначалося, виклик методу `fake` фасаду `Process` змусить Laravel завжди повертати успішний результат процесу без виводу. Проте ви легко можете задати вивід і код виходу підмінених процесів методом `result` фасаду `Process`:

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```

<a name="faking-specific-processes"></a>
### Підміна конкретних процесів

Як ви могли помітити в попередньому прикладі, фасад `Process` дозволяє задавати різні фейкові результати для різних процесів, передавши методу `fake` масив.

Ключі масиву мають бути шаблонами команд, які ви хочете підмінити, а значення - відповідними результатами. Символ `*` можна використовувати як підстановку. Будь-які команди процесів, які не підмінено, буде викликано насправді. Щоб побудувати підставні / фейкові результати для цих команд, скористайтеся методом `result` фасаду `Process`:

```php
Process::fake([
    'cat *' => Process::result(
        output: 'Test "cat" output',
    ),
    'ls *' => Process::result(
        output: 'Test "ls" output',
    ),
]);
```

Якщо вам не потрібно налаштовувати код виходу чи вивід помилок підміненого процесу, вам може бути зручніше задати фейкові результати простими рядками:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### Підміна послідовностей процесів

Якщо код, який ви тестуєте, викликає кілька процесів з однаковою командою, ви можете захотіти призначити кожному виклику інший фейковий результат. Це робиться методом `sequence` фасаду `Process`:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### Підміна життєвого циклу асинхронних процесів

Досі ми переважно обговорювали підміну процесів, які викликаються синхронно методом `run`. Проте, якщо ви намагаєтеся тестувати код, який працює з асинхронними процесами, запущеними через `start`, вам може знадобитися складніший підхід до опису фейкових процесів.

Наприклад, уявімо такий маршрут, який працює з асинхронним процесом:

```php
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    $process = Process::start('bash import.sh');

    while ($process->running()) {
        Log::info($process->latestOutput());
        Log::info($process->latestErrorOutput());
    }

    return 'Done';
});
```

Щоб коректно підмінити цей процес, нам потрібно описати, скільки разів метод `running` має повертати `true`. Крім того, ми можемо хотіти вказати кілька рядків виводу, які слід повертати послідовно. Для цього ми можемо скористатися методом `describe` фасаду `Process`:

```php
Process::fake([
    'bash import.sh' => Process::describe()
        ->output('First line of standard output')
        ->errorOutput('First line of error output')
        ->output('Second line of standard output')
        ->exitCode(0)
        ->iterations(3),
]);
```

Розберімо приклад вище. Методами `output` та `errorOutput` ми можемо задати кілька рядків виводу, які повертатимуться послідовно. Метод `exitCode` дозволяє задати фінальний код виходу фейкового процесу. Нарешті, метод `iterations` дозволяє вказати, скільки разів метод `running` має повертати `true`.

<a name="available-assertions"></a>
### Доступні перевірки

Як [зазначалося раніше](#faking-processes), Laravel надає кілька перевірок процесів для ваших функціональних тестів. Розгляньмо кожну з них нижче.

<a name="assert-process-ran"></a>
#### assertRan

Перевірити, що заданий процес було викликано:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

Метод `assertRan` також приймає замикання, яке отримає екземпляр процесу та результат процесу, дозволяючи оглянути налаштовані опції процесу. Якщо це замикання поверне `true`, перевірка «пройде»:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`$process`, переданий до замикання `assertRan`, є екземпляром `Illuminate\Process\PendingProcess`, а `$result` - екземпляром `Illuminate\Contracts\Process\ProcessResult`.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

Перевірити, що заданий процес не було викликано:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

Як і метод `assertRan`, метод `assertDidntRun` також приймає замикання, яке отримає екземпляр процесу та результат процесу, дозволяючи оглянути налаштовані опції процесу. Якщо це замикання поверне `true`, перевірка «провалиться»:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

Перевірити, що заданий процес було викликано задану кількість разів:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

Метод `assertRanTimes` також приймає замикання, яке отримає екземпляри `PendingProcess` та `ProcessResult`, дозволяючи оглянути налаштовані опції процесу. Якщо це замикання поверне `true` і процес було викликано вказану кількість разів, перевірка «пройде»:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### Запобігання «блукаючим» процесам

Якщо ви хочете переконатися, що всі викликані процеси підмінено в окремому тесті чи в усьому наборі тестів, викличте метод `preventStrayProcesses`. Після виклику цього методу будь-які процеси, для яких немає відповідного фейкового результату, викидатимуть виняток замість того, щоб запускати справжній процес:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// Fake response is returned...
Process::run('ls -la');

// An exception is thrown...
Process::run('bash import.sh');
```
