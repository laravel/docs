# Agendamento de Tarefas

- [Introdução](#introduction)
- [Definindo Agendamentos](#defining-schedules)
    - [Opções de Frequência de Agendamento](#schedule-frequency-options)
    - [Prevenir Sobreposições de Tarefa](#preventing-task-overlaps)
- [Saída da Tarefa](#task-output)
- [Hooks da Tarefa](#task-hooks)

<a name="introduction"></a>
## Introdução

No passado, os desenvolvedores precisavam gerar uma entrada na Cron para cada tarefa a qual queriam agendar. No entanto, isto é uma dor de cabeça. Sua agenda de tarefas não está no fonte da aplicação, além de ser necessário uma chave SSH no servidor para adicionar as entradas Cron. Com o agendamento de tarefas do Laravel podemos transferir os agendamentos para dentro da aplicação, sendo necessária apenas uma entrada Cron em seu servidor. 

Sua programação de tarefas é definida no método `schedule` do arquivo `app/Console/Kernel.php`. Para ajudar você a começar, um exemplo simples está incluído com o método. Você é livre para adicionar tantas tarefas agendadas como você deseja para o objeto `Schedule`.

### Iniciando o Agendador

Está é a única entrada Cron que você precisa adicionar em seu servidor:

    * * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

Este Cron irá chamar o comando agendador do Laravel a cada um minuto. Assim, o Laravel avalia as tarefas agendadas e executa as que são devidas.

<a name="defining-schedules"></a>
## Definindo Agendamentos

Você pode definir todas as suas tarefas agendadas no método `schedule` da classe `App\Console\Kernel`. Para começar, vamos olhar um exemplo de agendamento de uma tarefa. Neste exemplo, vamos agendar uma `Closure` a ser chamada todos os dias à meia-noite. Dentro da `Closure` vamos executar uma consulta de banco de dados para limpar uma tabela:

    <?php

    namespace App\Console;

    use DB;
    use Illuminate\Console\Scheduling\Schedule;
    use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

    class Kernel extends ConsoleKernel
    {
        /**
         * The Artisan commands provided by your application.
         *
         * @var array
         */
        protected $commands = [
            'App\Console\Commands\Inspire',
        ];

        /**
         * Define the application's command schedule.
         *
         * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
         * @return void
         */
        protected function schedule(Schedule $schedule)
        {
            $schedule->call(function () {
                DB::table('recent_users')->delete();
            })->daily();
        }
    }

Além do agendamento usando chamadas `Closure`, você também pode agendar [Comandos Artisan](/docs/{{version}}/artisan)  e comandos do sistema operacional. Por exemplo, você pode usar o método `command` para agendar um comando Artisan:

    $schedule->command('emails:send --force')->daily();

O comando `exec` pode ser utilizado para emitir um comando ao sistema operacional:

    $schedule->exec('node /home/forge/script.js')->daily();

<a name="schedule-frequency-options"></a>
### Opções de Frequência de Agendamento

É claro que há uma variedade de horários que você pode atribuir a sua tarefa:

Método  | Descrição
------------- | -------------
`->cron('* * * * *');`  |  Executar a tarefa em uma programação personalizada na Cron
`->everyMinute();`  |  Executar a tarefa a cada minuto
`->everyFiveMinutes();`  |  Executar a tarefa a cada cinco minutos
`->everyTenMinutes();`  |  Executar a tarefa a cada dez minutos
`->everyThirtyMinutes();`  |  Executar a tarefa a cada trinta minutos
`->hourly();`  |  Executar a tarefa a cada hora
`->daily();`  |  Executar a tarefa todos os dias à meia-noite
`->dailyAt('13:00');`  |  Executar a tarefa todos os dias às 13:00 hs
`->twiceDaily();`  |  Executar a tarefa diariamente 1:00 e 13:00 hs
`->weekly();`  |  Executar a tarefa todas as semanas
`->monthly();`  |  Executa a tarefa todas os meses

Estes métodos podem ser combinados com restrições adicionais, criando um agendamento mais preciso que só funcionam em determinados dias da semana. Por exemplo, para agendar um comando para executar semanalmente na segunda-feira:

    $schedule->call(function () {
        // Executa uma vez por semana na segunda-feira às 13:00 hs...
    })->weekly()->mondays()->at('13:00');

Abaixo está uma lista das restrições de programação adicionais:

Método  | Descrição
------------- | -------------
`->weekdays();`  |  Limitar a tarefa para os dias de semana
`->sundays();`  |  Limitar a tarefa para o Domingo
`->mondays();`  |  Limitar a tarefa para a Segunda-feira
`->tuesdays();`  |  Limitar a tarefa para a Terça-feira
`->wednesdays();`  |  Limitar a tarefa para a Quarta-feira
`->thursdays();`  |  Limitar a tarefa para a Quinta-feira
`->fridays();`  |  Limitar a tarefa para a Sexta-feira
`->saturdays();`  |  Limitar a tarefa para o Sábado
`->when(Closure);`  |  Limitar a tarefa com base em um teste de veracidade

#### Restrições com teste de veracidade

O método `when` pode ser utilizado para limitar a execução de uma tarefa com base no resultado de um determinado teste de veracidade. Em outras palavras, se a `Closure` retornar true, a tarefa será executada enquanto não existirem outras condições que impeçam a execução da tarefa:

    $schedule->command('emails:send')->daily()->when(function () {
        return true;
    });

<a name="preventing-task-overlaps"></a>
### Prevenir Sobreposições de Tarefa

Por padrão, as tarefas agendadas serão executadas mesmo se a instância anterior da tarefa ainda estiver em execução. Para evitar isso, você pode usar o método `withoutOverlapping`:

    $schedule->command('emails:send')->withoutOverlapping();

Neste exemplo, o `emails:send` [Comandos Artisan](/docs/{{version}}/artisan) será executado a cada minuto se não estiver já em execução. O método `withoutOverlapping` é especialmente útil se você tem tarefas que variam drasticamente em seu tempo de execução, impedindo você de prever exatamente quanto tempo uma determinada tarefa levará.

<a name="task-output"></a>
## Saída da Tarefa

O agendador do Laravel fornece vários métodos convenientes para trabalhar com a saída gerada por tarefas agendadas. Em primeiro lugar, usando o método `sendOutputTo`, você pode enviar a saída para um arquivo para inspeção posterior:

    $schedule->command('emails:send')
             ->daily()
             ->sendOutputTo($filePath);

Usando o método `emailOutputTo`, você pode enviar um e-mail com a saída para um endereço de sua escolha. Note que a saída deve primeiro ser enviada para um arquivo usando o método `sendOutputTo`. Além disso, antes de enviar e-mails com a saída de uma tarefa, você deve configurar o [serviço de email](/docs/{{version}}/mail)  do Laravel. 

    $schedule->command('foo')
             ->daily()
             ->sendOutputTo($filePath)
             ->emailOutputTo('foo@example.com');

> **Nota:** Os métodos `emailOutputTo` e `sendOutputTo` são exclusivos para o  método `command` e não são suportados pelo método `call`.

<a name="task-hooks"></a>
## Hooks da Tarefa

Usando os métodos `before` e `after`, você pode especificar o código a ser executado antes e depois da tarefa agendada ser executada:

    $schedule->command('emails:send')
             ->daily()
             ->before(function () {
                 // A tarefa está prestes a começar...
             })
             ->after(function () {
                 // A tarefa foi finalizada...
             });

#### Efetuando Ping de URLs

Usando os métodos `pingBefore` and `thenPing` , o programador pode fazer um ping automaticamente em uma determinada URL antes ou depois de uma tarefa ser concluída. Este método é útil para notificar um serviço externo, como o [Laravel Envoyer](https://envoyer.io), que a sua tarefa agendada está começando ou foi concluída:

    $schedule->command('emails:send')
             ->daily()
             ->pingBefore($url)
             ->thenPing($url);

Para usar o `pingBefore($url)` ou `thenPing($url)` é necessário a biblioteca Guzzle HTTP . Você pode adicionar o Guzzle ao seu projeto adicionando a linha seguinte ao seu arquivo `composer.json`:

    "guzzlehttp/guzzle": "~5.3|~6.0"
