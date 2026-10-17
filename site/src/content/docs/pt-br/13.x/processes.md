---
title: "Processes"
---

- [Introdução](#introduction)
- [Invocando Processos](#invoking-processes)
    - [Opções de Processo](#process-options)
    - [Saída do Processo](#process-output)
    - [Pipelines](#process-pipelines)
- [Processos Assíncronos](#asynchronous-processes)
    - [IDs e Sinais de Processo](#process-ids-and-signals)
    - [Saída de Processo Assíncrono](#asynchronous-process-output)
    - [Timeouts de Processo Assíncrono](#asynchronous-process-timeouts)
- [Processos Concorrentes](#concurrent-processes)
    - [Nomeando Processos do Pool](#naming-pool-processes)
    - [IDs e Sinais de Processo do Pool](#pool-process-ids-and-signals)
- [Testes](#testing)
    - [Simulando Processos](#faking-processes)
    - [Simulando Processos Específicos](#faking-specific-processes)
    - [Simulando Sequências de Processos](#faking-process-sequences)
    - [Simulando Ciclos de Vida de Processos Assíncronos](#faking-asynchronous-process-lifecycles)
    - [Asserções Disponíveis](#available-assertions)
    - [Prevenindo Processos Perdidos](#preventing-stray-processes)

<a id="introduction"></a>
## Introdução

O Laravel fornece uma API expressiva e minimalista em torno do [componente Process do Symfony](https://symfony.com/doc/current/components/process.html), permitindo que você invoque convenientemente processos externos a partir da sua aplicação Laravel. Os recursos de processos do Laravel são focados nos casos de uso mais comuns e em uma experiência maravilhosa para o desenvolvedor.

<a id="invoking-processes"></a>
## Invocando Processos

Para invocar um processo, você pode usar os métodos `run` e `start` oferecidos pela facade `Process`. O método `run` invocará um processo e aguardará a conclusão da execução do processo, enquanto o método `start` é usado para a execução assíncrona de processos. Examinaremos ambas as abordagens nesta documentação. Primeiro, vamos examinar como invocar um processo básico e síncrono e inspecionar seu resultado:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

Claro, a instância de `Illuminate\Contracts\Process\ProcessResult` retornada pelo método `run` oferece uma variedade de métodos úteis que podem ser usados para inspecionar o resultado do processo:

```php
$result = Process::run('ls -la');

$result->command();
$result->successful();
$result->failed();
$result->output();
$result->errorOutput();
$result->exitCode();
```

<a id="throwing-exceptions"></a>
#### Lançando Exceções

Se você tiver um resultado de processo e quiser lançar uma instância de `Illuminate\Process\Exceptions\ProcessFailedException` se o código de saída for maior que zero (indicando falha), você pode usar os métodos `throw` e `throwIf`. Se o processo não falhou, a instância de `ProcessResult` será retornada:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a id="process-options"></a>
### Opções de Processo

Claro, você pode precisar personalizar o comportamento de um processo antes de invocá-lo. Felizmente, o Laravel permite que você ajuste uma variedade de recursos do processo, como o diretório de trabalho, o timeout e as variáveis de ambiente.

<a id="working-directory-path"></a>
#### Caminho do Diretório de Trabalho

Você pode usar o método `path` para especificar o diretório de trabalho do processo. Se este método não for invocado, o processo herdará o diretório de trabalho do script PHP em execução no momento:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a id="input"></a>
#### Entrada

Você pode fornecer entrada por meio da "entrada padrão" (standard input) do processo usando o método `input`:

```php
$result = Process::input('Hello World')->run('cat');
```

<a id="timeouts"></a>
#### Timeouts

Por padrão, os processos lançarão uma instância de `Illuminate\Process\Exceptions\ProcessTimedOutException` após executarem por mais de 60 segundos. No entanto, você pode personalizar esse comportamento por meio do método `timeout`:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

Os métodos `timeout` e `idleTimeout` também aceitam instâncias de `CarbonInterval`:

```php
use function Illuminate\Support\minutes;

$result = Process::timeout(minutes(2))->run('bash import.sh');
```

Ou, se você quiser desabilitar completamente o timeout do processo, pode invocar o método `forever`:

```php
$result = Process::forever()->run('bash import.sh');
```

O método `idleTimeout` pode ser usado para especificar o número máximo de segundos que o processo pode rodar sem retornar qualquer saída:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a id="environment-variables"></a>
#### Variáveis de Ambiente

Variáveis de ambiente podem ser fornecidas ao processo por meio do método `env`. O processo invocado também herdará todas as variáveis de ambiente definidas pelo seu sistema:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

Se você quiser remover uma variável de ambiente herdada do processo invocado, pode fornecer essa variável de ambiente com um valor de `false`:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a id="tty-mode"></a>
#### Modo TTY

O método `tty` pode ser usado para habilitar o modo TTY para o seu processo. O modo TTY conecta a entrada e a saída do processo à entrada e à saída do seu programa, permitindo que seu processo abra um editor como o Vim ou o Nano como um processo:

```php
Process::forever()->tty()->run('vim');
```

> **Warning:**
> O modo TTY não é suportado no Windows.

<a id="process-output"></a>
### Saída do Processo

Como discutido anteriormente, a saída do processo pode ser acessada usando os métodos `output` (stdout) e `errorOutput` (stderr) em um resultado de processo:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

No entanto, a saída também pode ser coletada em tempo real passando uma closure como o segundo argumento para o método `run`. A closure receberá dois argumentos: o "tipo" de saída (`stdout` ou `stderr`) e a própria string de saída:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

O Laravel também oferece os métodos `seeInOutput` e `seeInErrorOutput`, que fornecem uma maneira conveniente de determinar se uma determinada string estava contida na saída do processo:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a id="disabling-process-output"></a>
#### Desabilitando a Saída do Processo

Se o seu processo está escrevendo uma quantidade significativa de saída na qual você não está interessado, você pode economizar memória desabilitando completamente a recuperação da saída. Para fazer isso, invoque o método `quietly` ao construir o processo:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a id="process-pipelines"></a>
### Pipelines

Às vezes, você pode querer tornar a saída de um processo a entrada de outro processo. Isso é frequentemente chamado de "piping" (encanamento) da saída de um processo para outro. O método `pipe` fornecido pela facade `Process` torna isso fácil de realizar. O método `pipe` executará os processos encadeados de forma síncrona e retornará o resultado do processo para o último processo no pipeline:

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

Se você não precisar personalizar os processos individuais que compõem o pipeline, pode simplesmente passar um array de strings de comando para o método `pipe`:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

A saída do processo pode ser coletada em tempo real passando uma closure como o segundo argumento para o método `pipe`. A closure receberá dois argumentos: o "tipo" de saída (`stdout` ou `stderr`) e a própria string de saída:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

O Laravel também permite que você atribua chaves de string a cada processo dentro de um pipeline por meio do método `as`. Essa chave também será passada para a closure de saída fornecida ao método `pipe`, permitindo que você determine a qual processo a saída pertence:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a id="asynchronous-processes"></a>
## Processos Assíncronos

Enquanto o método `run` invoca processos de forma síncrona, o método `start` pode ser usado para invocar um processo de forma assíncrona. Isso permite que sua aplicação continue realizando outras tarefas enquanto o processo roda em segundo plano. Uma vez que o processo tenha sido invocado, você pode utilizar o método `running` para determinar se o processo ainda está rodando:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

Como você deve ter notado, você pode invocar o método `wait` para aguardar até que o processo termine de executar e recuperar a instância de `ProcessResult`:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a id="process-ids-and-signals"></a>
### IDs e Sinais de Processo

O método `id` pode ser usado para recuperar o ID de processo atribuído pelo sistema operacional ao processo em execução:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

Você pode usar o método `signal` para enviar um "sinal" para o processo em execução. Uma lista de constantes de sinal predefinidas pode ser encontrada na [documentação do PHP](https://www.php.net/manual/en/pcntl.constants.php):

```php
$process->signal(SIGUSR2);
```

<a id="asynchronous-process-output"></a>
### Saída de Processo Assíncrono

Enquanto um processo assíncrono está rodando, você pode acessar toda a sua saída atual usando os métodos `output` e `errorOutput`; no entanto, você pode utilizar os métodos `latestOutput` e `latestErrorOutput` para acessar a saída do processo que ocorreu desde a última vez que a saída foi recuperada:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

Assim como o método `run`, a saída também pode ser coletada em tempo real de processos assíncronos passando uma closure como o segundo argumento para o método `start`. A closure receberá dois argumentos: o "tipo" de saída (`stdout` ou `stderr`) e a própria string de saída:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

Em vez de aguardar até que o processo tenha terminado, você pode usar o método `waitUntil` para parar de aguardar com base na saída do processo. O Laravel parará de aguardar a conclusão do processo quando a closure fornecida ao método `waitUntil` retornar `true`:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a id="asynchronous-process-timeouts"></a>
### Timeouts de Processo Assíncrono

Enquanto um processo assíncrono está rodando, você pode verificar se o processo não atingiu o timeout usando o método `ensureNotTimedOut`. Este método lançará uma [exceção de timeout](#timeouts) se o processo tiver atingido o timeout:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a id="concurrent-processes"></a>
## Processos Concorrentes

O Laravel também torna muito fácil gerenciar um pool de processos concorrentes e assíncronos, permitindo que você execute facilmente muitas tarefas simultaneamente. Para começar, invoque o método `pool`, que aceita uma closure que recebe uma instância de `Illuminate\Process\Pool`.

Dentro desta closure, você pode definir os processos que pertencem ao pool. Uma vez que um pool de processos seja iniciado por meio do método `start`, você pode acessar a [collection](/en/collections/) de processos em execução por meio do método `running`:

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

Como você pode ver, você pode aguardar que todos os processos do pool terminem de executar e resolver seus resultados por meio do método `wait`. O método `wait` retorna um objeto acessível como array que permite acessar a instância de `ProcessResult` de cada processo no pool pela sua chave:

```php
$results = $pool->wait();

echo $results[0]->output();
```

Ou, por conveniência, o método `concurrently` pode ser usado para iniciar um pool de processos assíncronos e aguardar imediatamente seus resultados. Isso pode fornecer uma sintaxe particularmente expressiva quando combinado com as capacidades de desestruturação de arrays do PHP:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a id="naming-pool-processes"></a>
### Nomeando Processos do Pool

Acessar os resultados do pool de processos por meio de uma chave numérica não é muito expressivo; portanto, o Laravel permite que você atribua chaves de string a cada processo dentro de um pool por meio do método `as`. Essa chave também será passada para a closure fornecida ao método `start`, permitindo que você determine a qual processo a saída pertence:

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

<a id="pool-process-ids-and-signals"></a>
### IDs e Sinais de Processo do Pool

Como o método `running` do pool de processos fornece uma collection de todos os processos invocados dentro do pool, você pode acessar facilmente os IDs dos processos subjacentes do pool:

```php
$processIds = $pool->running()->map->id();
```

E, por conveniência, você pode invocar o método `signal` em um pool de processos para enviar um sinal para cada processo dentro do pool:

```php
$pool->signal(SIGUSR2);
```

<a id="testing"></a>
## Testes

Muitos serviços do Laravel fornecem funcionalidades para ajudá-lo a escrever testes de forma fácil e expressiva, e o serviço de processos do Laravel não é exceção. O método `fake` da facade `Process` permite que você instrua o Laravel a retornar resultados simulados / fictícios quando os processos são invocados.

<a id="faking-processes"></a>
### Simulando Processos

Para explorar a capacidade do Laravel de simular processos, vamos imaginar uma rota que invoca um processo:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

Ao testar esta rota, podemos instruir o Laravel a retornar um resultado de processo falso e bem-sucedido para cada processo invocado chamando o método `fake` na facade `Process` sem argumentos. Além disso, podemos até [afirmar](#available-assertions) que um determinado processo foi "executado":

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // Asserção de processo simples...
    Process::assertRan('bash import.sh');

    // Ou, inspecionando a configuração do processo...
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

        // Asserção de processo simples...
        Process::assertRan('bash import.sh');

        // Ou, inspecionando a configuração do processo...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

Como discutido, invocar o método `fake` na facade `Process` instruirá o Laravel a sempre retornar um resultado de processo bem-sucedido sem saída. No entanto, você pode facilmente especificar a saída e o código de saída para processos simulados usando o método `result` da facade `Process`:

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```

<a id="faking-specific-processes"></a>
### Simulando Processos Específicos

Como você deve ter notado em um exemplo anterior, a facade `Process` permite que você especifique resultados simulados diferentes por processo passando um array para o método `fake`.

As chaves do array devem representar os padrões de comando que você deseja simular e seus resultados associados. O caractere `*` pode ser usado como um caractere curinga. Quaisquer comandos de processo que não tenham sido simulados serão realmente invocados. Você pode usar o método `result` da facade `Process` para construir resultados simulados / falsos para esses comandos:

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

Se você não precisar personalizar o código de saída ou a saída de erro de um processo simulado, pode achar mais conveniente especificar os resultados do processo simulado como strings simples:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a id="faking-process-sequences"></a>
### Simulando Sequências de Processos

Se o código que você está testando invoca vários processos com o mesmo comando, você pode querer atribuir um resultado de processo simulado diferente a cada invocação do processo. Você pode fazer isso por meio do método `sequence` da facade `Process`:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a id="faking-asynchronous-process-lifecycles"></a>
### Simulando Ciclos de Vida de Processos Assíncronos

Até agora, discutimos principalmente a simulação de processos que são invocados de forma síncrona usando o método `run`. No entanto, se você estiver tentando testar código que interage com processos assíncronos invocados por meio do `start`, pode precisar de uma abordagem mais sofisticada para descrever seus processos simulados.

Por exemplo, vamos imaginar a seguinte rota que interage com um processo assíncrono:

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

Para simular corretamente este processo, precisamos ser capazes de descrever quantas vezes o método `running` deve retornar `true`. Além disso, podemos querer especificar várias linhas de saída que devem ser retornadas em sequência. Para fazer isso, podemos usar o método `describe` da facade `Process`:

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

Vamos nos aprofundar no exemplo acima. Usando os métodos `output` e `errorOutput`, podemos especificar várias linhas de saída que serão retornadas em sequência. O método `exitCode` pode ser usado para especificar o código de saída final do processo simulado. Por fim, o método `iterations` pode ser usado para especificar quantas vezes o método `running` deve retornar `true`.

<a id="available-assertions"></a>
### Asserções Disponíveis

Como [discutido anteriormente](#faking-processes), o Laravel fornece várias asserções de processo para seus testes de funcionalidade. Discutiremos cada uma dessas asserções abaixo.

<a id="assert-process-ran"></a>
#### assertRan

Afirma que um determinado processo foi invocado:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

Quando o processo foi invocado com um array de argumentos, você pode passar o mesmo array para a asserção:

```php
Process::assertRan(['php', 'artisan', 'migrate']);
```

Os métodos `assertRanTimes` e `assertDidntRun` também aceitam comandos em array.

O método `assertRan` também aceita uma closure, que receberá uma instância de um processo e um resultado de processo, permitindo que você inspecione as opções configuradas do processo. Se esta closure retornar `true`, a asserção "passará":

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

O `$process` passado para a closure do `assertRan` é uma instância de `Illuminate\Process\PendingProcess`, enquanto o `$result` é uma instância de `Illuminate\Contracts\Process\ProcessResult`.

<a id="assert-process-didnt-run"></a>
#### assertDidntRun

Afirma que um determinado processo não foi invocado:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

Assim como o método `assertRan`, o método `assertDidntRun` também aceita uma closure, que receberá uma instância de um processo e um resultado de processo, permitindo que você inspecione as opções configuradas do processo. Se esta closure retornar `true`, a asserção "falhará":

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a id="assert-process-ran-times"></a>
#### assertRanTimes

Afirma que um determinado processo foi invocado um determinado número de vezes:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

O método `assertRanTimes` também aceita uma closure, que receberá uma instância de `PendingProcess` e `ProcessResult`, permitindo que você inspecione as opções configuradas do processo. Se esta closure retornar `true` e o processo foi invocado o número especificado de vezes, a asserção "passará":

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a id="assert-processes-ran-in-order"></a>
#### assertRanInOrder

Afirma que os processos foram invocados em uma determinada ordem:

```php
Process::assertRanInOrder([
    'git fetch',
    'composer install',
]);
```

O método `assertRanInOrder` aceita strings de comando, arrays de argumentos de comando ou closures como as outras asserções de processo.

<a id="preventing-stray-processes"></a>
### Prevenindo Processos Perdidos

Se você quiser garantir que todos os processos invocados tenham sido simulados ao longo do seu teste individual ou da sua suíte de testes completa, você pode chamar o método `preventStrayProcesses`. Após chamar este método, quaisquer processos que não tenham um resultado simulado correspondente lançarão uma exceção em vez de iniciar um processo real:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// A resposta simulada é retornada...
Process::run('ls -la');

// Uma exceção é lançada...
Process::run('bash import.sh');
```
