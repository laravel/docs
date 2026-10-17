---
title: "Agendamento de Tarefas"
---

- [Introdução](#introduction)
- [Definindo Agendamentos](#defining-schedules)
    - [Agendando Comandos Artisan](#scheduling-artisan-commands)
    - [Agendando Jobs na Fila](#scheduling-queued-jobs)
    - [Agendando Comandos de Shell](#scheduling-shell-commands)
    - [Opções de Frequência do Agendamento](#schedule-frequency-options)
    - [Fusos Horários](#timezones)
    - [Prevenindo Sobreposição de Tarefas](#preventing-task-overlaps)
    - [Executando Tarefas em Um Único Servidor](#running-tasks-on-one-server)
    - [Tarefas em Segundo Plano](#background-tasks)
    - [Modo de Manutenção](#maintenance-mode)
    - [Pausando Tarefas Agendadas](#pausing-scheduled-tasks)
    - [Grupos de Agendamento](#schedule-groups)
- [Executando o Agendador](#running-the-scheduler)
    - [Tarefas Agendadas com Intervalo Menor que um Minuto](#sub-minute-scheduled-tasks)
    - [Executando o Agendador Localmente](#running-the-scheduler-locally)
- [Saída das Tarefas](#task-output)
- [Hooks de Tarefas](#task-hooks)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

No passado, você pode ter escrito uma entrada de configuração do cron para cada tarefa que precisava agendar no seu servidor. No entanto, isso pode se tornar um problema rapidamente, porque o agendamento das suas tarefas deixa de estar no controle de versão e você precisa acessar o servidor via SSH para visualizar as entradas de cron existentes ou adicionar novas.

O agendador de comandos do Laravel oferece uma abordagem moderna para gerenciar tarefas agendadas no seu servidor. O agendador permite que você defina de forma fluente e expressiva o agendamento dos seus comandos dentro da própria aplicação Laravel. Ao usar o agendador, é necessária apenas uma única entrada de cron no seu servidor. O agendamento das suas tarefas normalmente é definido no arquivo `routes/console.php` da sua aplicação.

<a id="defining-schedules"></a>
## Definindo Agendamentos

Você pode definir todas as suas tarefas agendadas no arquivo `routes/console.php` da sua aplicação. Para começar, vamos ver um exemplo. Neste exemplo, vamos agendar uma closure para ser chamada todos os dias à meia-noite. Dentro da closure, vamos executar uma consulta ao banco de dados para limpar uma tabela:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

Além de agendar usando closures, você também pode agendar [objetos invocáveis](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Objetos invocáveis são classes PHP simples que contêm um método `__invoke`:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

Se você preferir reservar o arquivo `routes/console.php` apenas para definições de comandos, pode usar o método `withSchedule` no arquivo `bootstrap/app.php` da sua aplicação para definir suas tarefas agendadas. Este método aceita uma closure que recebe uma instância do agendador:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

Se você quiser ver uma visão geral das suas tarefas agendadas e a próxima vez em que estão programadas para serem executadas, pode usar o comando Artisan `schedule:list`:

```shell
php artisan schedule:list
```

<a id="scheduling-artisan-commands"></a>
### Agendando Comandos Artisan

Além de agendar closures, você também pode agendar [comandos Artisan](../artisan/) e comandos de sistema. Por exemplo, você pode usar o método `command` para agendar um comando Artisan usando o nome ou a classe do comando.

Ao agendar comandos Artisan usando o nome da classe do comando, você pode passar um array com argumentos adicionais de linha de comando que devem ser fornecidos ao comando quando ele for invocado:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a id="scheduling-artisan-closure-commands"></a>
#### Agendando Comandos Artisan com Closure

Se você quiser agendar um comando Artisan definido por uma closure, pode encadear os métodos relacionados ao agendamento após a definição do comando:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

Se precisar passar argumentos para o comando com closure, você pode fornecê-los ao método `schedule`:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a id="scheduling-queued-jobs"></a>
### Agendando Jobs na Fila

O método `job` pode ser usado para agendar um [job na fila](../queues/). Este método oferece uma forma conveniente de agendar jobs na fila sem usar o método `call` para definir closures que enfileiram o job:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

Argumentos opcionais, o segundo e o terceiro, podem ser fornecidos ao método `job` para especificar o nome da fila e a conexão de fila que devem ser usadas para enfileirar o job:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a id="scheduling-shell-commands"></a>
### Agendando Comandos de Shell

O método `exec` pode ser usado para emitir um comando para o sistema operacional:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a id="schedule-frequency-options"></a>
### Opções de Frequência do Agendamento

Já vimos alguns exemplos de como configurar uma tarefa para ser executada em intervalos específicos. No entanto, existem muitas outras frequências de agendamento que você pode atribuir a uma tarefa:

<div class="overflow-auto">

| Método                             | Descrição                                                 |
| ---------------------------------- | --------------------------------------------------------- |
| `->cron('* * * * *');`             | Executa a tarefa em um agendamento cron personalizado.    |
| `->everySecond();`                 | Executa a tarefa a cada segundo.                          |
| `->everyTwoSeconds();`             | Executa a tarefa a cada dois segundos.                    |
| `->everyFiveSeconds();`            | Executa a tarefa a cada cinco segundos.                   |
| `->everyTenSeconds();`             | Executa a tarefa a cada dez segundos.                     |
| `->everyFifteenSeconds();`         | Executa a tarefa a cada quinze segundos.                  |
| `->everyTwentySeconds();`          | Executa a tarefa a cada vinte segundos.                   |
| `->everyThirtySeconds();`          | Executa a tarefa a cada trinta segundos.                  |
| `->everyMinute();`                 | Executa a tarefa a cada minuto.                           |
| `->everyTwoMinutes();`             | Executa a tarefa a cada dois minutos.                     |
| `->everyThreeMinutes();`           | Executa a tarefa a cada três minutos.                     |
| `->everyFourMinutes();`            | Executa a tarefa a cada quatro minutos.                   |
| `->everyFiveMinutes();`            | Executa a tarefa a cada cinco minutos.                    |
| `->everyTenMinutes();`             | Executa a tarefa a cada dez minutos.                      |
| `->everyFifteenMinutes();`         | Executa a tarefa a cada quinze minutos.                   |
| `->everyThirtyMinutes();`          | Executa a tarefa a cada trinta minutos.                   |
| `->hourly();`                      | Executa a tarefa a cada hora.                             |
| `->hourlyAt(17);`                  | Executa a tarefa a cada hora, aos 17 minutos.             |
| `->everyOddHour($minutes = 0);`    | Executa a tarefa a cada hora ímpar.                       |
| `->everyTwoHours($minutes = 0);`   | Executa a tarefa a cada duas horas.                       |
| `->everyThreeHours($minutes = 0);` | Executa a tarefa a cada três horas.                       |
| `->everyFourHours($minutes = 0);`  | Executa a tarefa a cada quatro horas.                     |
| `->everySixHours($minutes = 0);`   | Executa a tarefa a cada seis horas.                       |
| `->daily();`                       | Executa a tarefa todos os dias à meia-noite.              |
| `->dailyAt('13:00');`              | Executa a tarefa todos os dias às 13:00.                  |
| `->twiceDaily(1, 13);`             | Executa a tarefa diariamente às 1:00 e às 13:00.          |
| `->twiceDailyAt(1, 13, 15);`       | Executa a tarefa diariamente às 1:15 e às 13:15.          |
| `->daysOfMonth([1, 10, 20]);`      | Executa a tarefa em dias específicos do mês.              |
| `->weekly();`                      | Executa a tarefa todo domingo às 00:00.                   |
| `->weeklyOn(1, '8:00');`           | Executa a tarefa toda semana, na segunda-feira, às 8:00.  |
| `->monthly();`                     | Executa a tarefa no primeiro dia de cada mês às 00:00.    |
| `->monthlyOn(4, '15:00');`         | Executa a tarefa todo mês, no dia 4, às 15:00.            |
| `->twiceMonthly(1, 16, '13:00');`  | Executa a tarefa mensalmente, no dia 1 e no dia 16, às 13:00. |
| `->lastDayOfMonth('15:00');`       | Executa a tarefa no último dia do mês às 15:00.           |
| `->quarterly();`                   | Executa a tarefa no primeiro dia de cada trimestre às 00:00. |
| `->quarterlyOn(4, '14:00');`       | Executa a tarefa todo trimestre, no dia 4, às 14:00.      |
| `->yearly();`                      | Executa a tarefa no primeiro dia de cada ano às 00:00.    |
| `->yearlyOn(6, 1, '17:00');`       | Executa a tarefa todo ano, em 1º de junho, às 17:00.      |
| `->timezone('America/New_York');`  | Define o fuso horário da tarefa.                          |

</div>

Esses métodos podem ser combinados com restrições adicionais para criar agendamentos ainda mais refinados que só são executados em determinados dias da semana. Por exemplo, você pode agendar um comando para ser executado semanalmente às segundas-feiras:

```php
use Illuminate\Support\Facades\Schedule;

// Run once per week on Monday at 1 PM...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

A seguir, uma lista de restrições adicionais de agendamento:

<div class="overflow-auto">

| Método                                   | Descrição                                                 |
| ---------------------------------------- | --------------------------------------------------------- |
| `->weekdays();`                          | Limita a tarefa aos dias de semana.                       |
| `->weekends();`                          | Limita a tarefa aos fins de semana.                       |
| `->sundays();`                           | Limita a tarefa ao domingo.                               |
| `->mondays();`                           | Limita a tarefa à segunda-feira.                          |
| `->tuesdays();`                          | Limita a tarefa à terça-feira.                            |
| `->wednesdays();`                        | Limita a tarefa à quarta-feira.                           |
| `->thursdays();`                         | Limita a tarefa à quinta-feira.                           |
| `->fridays();`                           | Limita a tarefa à sexta-feira.                            |
| `->saturdays();`                         | Limita a tarefa ao sábado.                                |
| `->days(array\|mixed);`                  | Limita a tarefa a dias específicos.                       |
| `->between($startTime, $endTime);`       | Limita a tarefa a ser executada entre o horário inicial e o final. |
| `->unlessBetween($startTime, $endTime);` | Limita a tarefa a não ser executada entre o horário inicial e o final. |
| `->when(Closure);`                       | Limita a tarefa com base em um teste lógico.              |
| `->environments($env);`                  | Limita a tarefa a ambientes específicos.                  |

</div>

<a id="day-constraints"></a>
#### Restrições de Dia

O método `days` pode ser usado para limitar a execução de uma tarefa a dias específicos da semana. Por exemplo, você pode agendar um comando para ser executado a cada hora, aos domingos e quartas-feiras:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

Como alternativa, você pode usar as constantes disponíveis na classe `Illuminate\Console\Scheduling\Schedule` ao definir os dias em que uma tarefa deve ser executada:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a id="between-time-constraints"></a>
#### Restrições de Intervalo de Horário

O método `between` pode ser usado para limitar a execução de uma tarefa com base na hora do dia:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

De forma semelhante, o método `unlessBetween` pode ser usado para excluir a execução de uma tarefa durante um período de tempo:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a id="truth-test-constraints"></a>
#### Restrições de Teste Lógico

O método `when` pode ser usado para limitar a execução de uma tarefa com base no resultado de um teste lógico fornecido. Em outras palavras, se a closure fornecida retornar `true`, a tarefa será executada desde que nenhuma outra condição restritiva impeça sua execução:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

O método `skip` pode ser visto como o inverso de `when`. Se o método `skip` retornar `true`, a tarefa agendada não será executada:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

Ao usar métodos `when` encadeados, o comando agendado só será executado se todas as condições `when` retornarem `true`.

<a id="environment-constraints"></a>
#### Restrições de Ambiente

O método `environments` pode ser usado para executar tarefas apenas nos ambientes indicados (conforme definido pela [variável de ambiente](../configuration/#environment-configuration) `APP_ENV`):

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a id="timezones"></a>
### Fusos Horários

Usando o método `timezone`, você pode especificar que o horário de uma tarefa agendada deve ser interpretado dentro de um determinado fuso horário:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00');
```

Se você atribui repetidamente o mesmo fuso horário a todas as suas tarefas agendadas, pode especificar qual fuso horário deve ser atribuído a todos os agendamentos definindo a opção `schedule_timezone` no arquivo de configuração `app` da sua aplicação:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> **Aviso:**
> Lembre-se de que alguns fusos horários utilizam o horário de verão. Quando ocorrem mudanças no horário de verão, sua tarefa agendada pode ser executada duas vezes ou até não ser executada. Por esse motivo, recomendamos evitar o agendamento por fuso horário sempre que possível.

<a id="preventing-task-overlaps"></a>
### Prevenindo Sobreposição de Tarefas

Por padrão, tarefas agendadas serão executadas mesmo que a instância anterior da tarefa ainda esteja em execução. Para evitar isso, você pode usar o método `withoutOverlapping`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

Neste exemplo, o [comando Artisan](../artisan/) `emails:send` será executado a cada minuto, desde que ainda não esteja em execução. O método `withoutOverlapping` é especialmente útil se você tiver tarefas cujo tempo de execução varia drasticamente, impedindo que você preveja exatamente quanto tempo uma determinada tarefa levará.

Se necessário, você pode especificar quantos minutos devem passar até que o bloqueio "sem sobreposição" expire. Por padrão, o bloqueio expira após 24 horas:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

Nos bastidores, o método `withoutOverlapping` utiliza o [cache](../cache/) da sua aplicação para obter bloqueios. Se necessário, você pode limpar esses bloqueios de cache usando o comando Artisan `schedule:clear-cache`. Isso normalmente só é necessário se uma tarefa travar devido a um problema inesperado no servidor.

<a id="running-tasks-on-one-server"></a>
### Executando Tarefas em Um Único Servidor

> **Aviso:**
> Para utilizar este recurso, sua aplicação deve estar usando o driver de cache `database`, `memcached`, `dynamodb` ou `redis` como driver de cache padrão da aplicação. Além disso, todos os servidores devem se comunicar com o mesmo servidor de cache central.

Se o agendador da sua aplicação estiver sendo executado em vários servidores, você pode limitar um job agendado para ser executado apenas em um único servidor. Por exemplo, suponha que você tenha uma tarefa agendada que gera um novo relatório toda sexta-feira à noite. Se o agendador de tarefas estiver sendo executado em três servidores de worker, a tarefa agendada será executada nos três servidores e gerará o relatório três vezes. Não é bom!

Para indicar que a tarefa deve ser executada em apenas um servidor, use o método `onOneServer` ao definir a tarefa agendada. O primeiro servidor a obter a tarefa adquirirá um bloqueio atômico sobre o job para impedir que outros servidores executem a mesma tarefa ao mesmo tempo:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

Para aplicar `onOneServer` a todas as tarefas agendadas, você pode chamar o método `alwaysOnOneServer` no método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Schedule;

public function boot(): void
{
    Schedule::alwaysOnOneServer();
}
```

Closures agendadas sem um [nome](#naming-unique-jobs) são excluídas e continuarão a ser executadas em todos os servidores.

Você pode usar o método `useCache` para personalizar o armazenamento de cache usado pelo agendador para obter os bloqueios atômicos necessários para tarefas de servidor único:

```php
Schedule::useCache('database');
```

<a id="naming-unique-jobs"></a>
#### Nomeando Jobs de Servidor Único

Às vezes, você pode precisar agendar o mesmo job para ser despachado com parâmetros diferentes, mantendo ainda a instrução ao Laravel para executar cada variação do job em um único servidor. Para isso, você pode atribuir a cada definição de agendamento um nome único por meio do método `name`:

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```

De forma semelhante, closures agendadas devem receber um nome se forem destinadas a serem executadas em um único servidor:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a id="background-tasks"></a>
### Tarefas em Segundo Plano

Por padrão, várias tarefas agendadas ao mesmo tempo serão executadas sequencialmente, de acordo com a ordem em que são definidas no seu método `schedule`. Se você tiver tarefas de longa duração, isso pode fazer com que as tarefas seguintes comecem bem mais tarde do que o esperado. Se quiser executar tarefas em segundo plano para que todas possam ser executadas simultaneamente, pode usar o método `runInBackground`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> **Aviso:**
> O método `runInBackground` só pode ser usado ao agendar tarefas por meio dos métodos `command` e `exec`.

<a id="maintenance-mode"></a>
### Modo de Manutenção

As tarefas agendadas da sua aplicação não serão executadas quando a aplicação estiver em [modo de manutenção](../configuration/#maintenance-mode), pois não queremos que suas tarefas interfiram em qualquer manutenção não concluída que você esteja realizando no servidor. No entanto, se quiser forçar a execução de uma tarefa mesmo em modo de manutenção, você pode chamar o método `evenInMaintenanceMode` ao definir a tarefa:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a id="pausing-scheduled-tasks"></a>
### Pausando Tarefas Agendadas

Você pode pausar temporariamente o processamento de tarefas agendadas sem alterar o código implantado, usando o comando Artisan `schedule:pause`:

```shell
php artisan schedule:pause
```

Enquanto o agendador estiver pausado, nenhuma tarefa agendada será executada. Você pode retomar o processamento de tarefas agendadas usando o comando `schedule:continue`:

```shell
php artisan schedule:continue
```

Se uma tarefa ainda deve ser executada enquanto o agendador estiver pausado, você pode marcá-la com o método `evenWhenPaused`:

```php
Schedule::command('emails:send')->evenWhenPaused();
```

<a id="schedule-groups"></a>
### Grupos de Agendamento

Ao definir várias tarefas agendadas com configurações semelhantes, você pode usar o recurso de agrupamento de tarefas do Laravel para evitar repetir as mesmas configurações em cada tarefa. Agrupar tarefas simplifica seu código e garante consistência entre tarefas relacionadas.

Para criar um grupo de tarefas agendadas, invoque os métodos de configuração desejados da tarefa, seguidos do método `group`. O método `group` aceita uma closure responsável por definir as tarefas que compartilham a configuração especificada:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```

<a id="running-the-scheduler"></a>
## Executando o Agendador

Agora que aprendemos a definir tarefas agendadas, vamos discutir como executá-las de fato no nosso servidor. O comando Artisan `schedule:run` avaliará todas as suas tarefas agendadas e determinará se elas precisam ser executadas com base na hora atual do servidor.

Assim, ao usar o agendador do Laravel, só precisamos adicionar uma única entrada de configuração do cron no servidor que executa o comando `schedule:run` a cada minuto. Se você não sabe como adicionar entradas de cron no seu servidor, considere usar uma plataforma gerenciada como o [Laravel Cloud](https://cloud.laravel.com), que pode gerenciar a execução das tarefas agendadas para você:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a id="sub-minute-scheduled-tasks"></a>
### Tarefas Agendadas com Intervalo Menor que um Minuto

Na maioria dos sistemas operacionais, jobs de cron são limitados a executar no máximo uma vez por minuto. No entanto, o agendador do Laravel permite agendar tarefas para serem executadas em intervalos mais frequentes, inclusive até uma vez por segundo:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

Quando tarefas com intervalo menor que um minuto são definidas na sua aplicação, o comando `schedule:run` continuará em execução até o final do minuto atual, em vez de encerrar imediatamente. Isso permite que o comando invoque todas as tarefas necessárias com intervalo menor que um minuto ao longo desse minuto.

Como tarefas com intervalo menor que um minuto que demorem mais do que o esperado podem atrasar a execução das tarefas seguintes, recomenda-se que todas as tarefas com intervalo menor que um minuto despachem jobs na fila ou comandos em segundo plano para processar a tarefa em si:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a id="interrupting-sub-minute-tasks"></a>
#### Interrompendo Tarefas com Intervalo Menor que um Minuto

Como o comando `schedule:run` é executado durante todo o minuto da invocação quando tarefas com intervalo menor que um minuto estão definidas, às vezes você pode precisar interromper o comando ao implantar sua aplicação. Caso contrário, uma instância do comando `schedule:run` que já esteja em execução continuaria usando o código implantado anteriormente da sua aplicação até o final do minuto atual.

Para interromper invocações de `schedule:run` em andamento, você pode adicionar o comando `schedule:interrupt` ao script de implantação da sua aplicação. Este comando deve ser invocado depois que a implantação da aplicação for concluída:

```shell
php artisan schedule:interrupt
```

<a id="running-the-scheduler-locally"></a>
### Executando o Agendador Localmente

Normalmente, você não adicionaria uma entrada de cron do agendador na sua máquina de desenvolvimento local. Em vez disso, você pode usar o comando Artisan `schedule:work`. Este comando será executado em primeiro plano e invocará o agendador a cada minuto até que você encerre o comando. Quando tarefas com intervalo menor que um minuto são definidas, o agendador continuará em execução dentro de cada minuto para processar essas tarefas:

```shell
php artisan schedule:work
```

<a id="task-output"></a>
## Saída das Tarefas

O agendador do Laravel oferece vários métodos práticos para trabalhar com a saída gerada pelas tarefas agendadas. Primeiro, usando o método `sendOutputTo`, você pode enviar a saída para um arquivo para consulta posterior:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

Se você quiser anexar a saída a um determinado arquivo, pode usar o método `appendOutputTo`:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

Usando o método `emailOutputTo`, você pode enviar a saída por e-mail para o endereço de sua escolha. Antes de enviar por e-mail a saída de uma tarefa, você deve configurar os [serviços de e-mail](../mail/) do Laravel:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

Se você quiser enviar a saída por e-mail somente quando o comando Artisan ou de sistema agendado terminar com um código de saída diferente de zero, use o método `emailOutputOnFailure`:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> **Aviso:**
> Os métodos `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo` e `appendOutputTo` são exclusivos dos métodos `command` e `exec`.

<a id="task-hooks"></a>
## Hooks de Tarefas

Usando os métodos `before` e `after`, você pode especificar código a ser executado antes e depois da execução da tarefa agendada:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // The task is about to execute...
    })
    ->after(function () {
        // The task has executed...
    });
```

Os métodos `onSuccess` e `onFailure` permitem especificar código a ser executado caso a tarefa agendada tenha sucesso ou falhe. Uma falha indica que o comando Artisan ou de sistema agendado terminou com um código de saída diferente de zero:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```

Se houver saída disponível do seu comando, você pode acessá-la nos seus hooks `after`, `onSuccess` ou `onFailure` tipando um argumento `Illuminate\Support\Stringable` como o argumento `$output` da definição da closure do hook:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // The task succeeded...
    })
    ->onFailure(function (Stringable $output) {
        // The task failed...
    });
```

<a id="pinging-urls"></a>
#### Pingando URLs

Usando os métodos `pingBefore` e `thenPing`, o agendador pode fazer automaticamente um ping em uma determinada URL antes ou depois da execução de uma tarefa. Este método é útil para notificar um serviço externo, como o [Envoyer](https://envoyer.io), de que sua tarefa agendada está começando ou terminou a execução:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

Os métodos `pingOnSuccess` e `pingOnFailure` podem ser usados para fazer ping em uma determinada URL somente se a tarefa tiver sucesso ou falhar. Uma falha indica que o comando Artisan ou de sistema agendado terminou com um código de saída diferente de zero:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

Os métodos `pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf` e `pingOnFailureIf` podem ser usados para fazer ping em uma determinada URL somente se uma condição fornecida for `true`:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a id="events"></a>
## Eventos

O Laravel dispara vários [eventos](../events/) durante o processo de agendamento. Você pode [definir listeners](../events/) para qualquer um dos seguintes eventos:

<div class="overflow-auto">

| Nome do Evento                                              |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
