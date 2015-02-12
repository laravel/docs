# Artisan CLI

- [Introdução](#introduction)
- [Uso](#usage)
- [Chamando os Comandos de Fora do CLI](#calling-commands-outside-of-cli)
- [Agendando Comandos Artisan](#scheduling-artisan-commands)

<a name="introduction"></a>
## Introdução

Artisan é o nome da interface da linha de comando incluída no Laravel. Esta interface fornece um bom número de comandos auxiliares para que você use durante o desenvolvimento de sua aplicação. O artisan é impulsionado pelo poderoso componente de Console do Symfony framework.

<a name="usage"></a>
## Uso

#### Listando todos os comandos Disponíveis

Para ver a lista de todos os comandos Artisan, você deve utilizar o comando `list`.

	php artisan list

#### Visualizando a Tela de Ajuda para um Comando

Todos os comandos também incluem uma tela de "help" que mostra e descreve os comandos e seus respectivos parâmetros e opções. Para ver a tela de "help" (ajuda), simplesmente preceda o nome do comando com `help`.

	php artisan help migrate

#### Especificando O Ambiente de Configuração

Você pode especificar o ambiente em que o comando é executando usando o prefixo `--env`:

	php artisan migrate --env=local

#### Exibindo Sua Versão Atual do Laravel

Você também pode ver a versão atual do instalação do seu Laravel utilizando a opção `--version`:

	php artisan --version

<a name="calling-commands-outside-of-cli"></a>
## Chamando os Comandos de Fora do CLI

Algumas vezes você pode desejar executatar o comando Artisan de fora do CLI. Por exemplo, vocẽ pode desejar executar o comando Artisan de uma rota HTTP. Apenas use a fachada `Artisan`:

	Route::get('/foo', function()
	{
		$exitCode = Artisan::call('command:name', ['--option' => 'foo']);

		//
	});

Você pode até enfileirar comandos Artisan para que eles sejam processados em segundo plano pelo seu [queue workers](/docs/5.0/queues):

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-artisan-commands"></a>
## Agendando Comandos Artisan

No passado, desenvolvedores teêm gerado uma entrada de Cron para cada comando que eles queriam agendar. Contudo, isto é uma baita dor de cabeça. Seu console de agendamento não está mais no controle de origem, e você deve realizar uma conexão SSH com o seu servidor para dar entradas de Cron. Vamos fazer sua nossas vidas mais fáceis. O comando agendados do Laravel lhe permite nativamente definir seu comando agendador apenas com o próprio Laravel, e apenas uma entrada de Cron se faz necessária no seu servidor.

Seu comando agendador é armazenado no arquivo `app/Console/Kernel.php`. Dentro desta classe você verá o método `schedule`. Para ajudar você a começar, um simples exemplo é incluído com o método. Sinta-se a vontade para adicionar quantas tarefas agendadas você desejar para o objeto `Schedule`. A única entrada de Cron que você precisa adicionar para o seu servidor é esta:

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

Este Cron(tarefa agendada) chamará o comando de agendamento do Laravel todo minuto. Em seguida, Laravel avalia sua tarefa agendada e executa os que são devidos. Não poderia ser mais fácil do que isto. 


### Mais Exemplos de Agendamento 

Vamos dar uma olhada em mais alguns exemplos de agendamentos:

#### Agendamentos com Closures

	$schedule->call(function()
	{
		// Do some task...

	})->hourly();

#### Comandos de Agendamento via Terminal

	$schedule->exec('composer self-update')->daily();

#### Expressão Manual de Cron 

	$schedule->command('foo')->cron('* * * * *');

#### Tarefas Frequentes

	$schedule->command('foo')->everyFiveMinutes();

	$schedule->command('foo')->everyTenMinutes();

	$schedule->command('foo')->everyThirtyMinutes();

#### Tarefas Diárias

	$schedule->command('foo')->daily();

#### Tarefas Diárias em Um Horário Específico (24 Horas)

	$schedule->command('foo')->dailyAt('15:00');

#### Tarefas Realizadas Duas Vezes ao Dia 

	$schedule->command('foo')->twiceDaily();

#### Tarefas Executadas Todos os Dias da Semana

	$schedule->command('foo')->weekdays();

#### Tarefas Realizadas em um Dia da Semana em Específico 

	$schedule->command('foo')->weekly();

	// Schedule weekly job for specific day (0-6) and time...
	$schedule->command('foo')->weeklyOn(1, '8:00');

#### Tarefas Mensais

	$schedule->command('foo')->monthly();

#### Limitando os Ambientes em que as Tarefas Devem ser Executadas 

	$schedule->command('foo')->monthly()->environments('production');

#### Indicando se a Execução da Tarefa Deve ser Relizada Mesmo Quando Aplicação Está em Manutenção 

	$schedule->command('foo')->monthly()->evenInMaintenanceMode();

#### Permitindo que a Tarefa Seja Executada Apenas Quando o Retorno do Callback Seja Verdadeiro

	$schedule->command('foo')->monthly()->when(function()
	{
		return true;
	});
