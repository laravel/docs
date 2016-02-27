# Envoy / Tarefas SSH 

- [Introdução](#introduction)
- [Escrevendo Tarefas](#writing-tasks)
	- [Variáveis da Tarefa](#task-variables)
	- [Múltiplos Servidores](#envoy-multiple-servers)
	- [Macros das Tarefas](#envoy-task-macros)
- [Executando Tarefas](#envoy-running-tasks)
- [Notificações](#envoy-notifications)
	- [HipChat](#hipchat)
	- [Slack](#slack)

<a name="introduction"></a>
## Introdução

[Laravel Envoy](https://github.com/laravel/envoy) provê uma sintaxe limpa e mínima para definir tarefas comuns para rodar em servidores remotos. Usando o estilo da sintaxe do Blade você facilmente definir tarefas para deploy (instalação ou atualização da aplicação no servidor remoto), comandos artisan e outros. Atualmente, Envoy suporta servidores com sistema operacional Mac e Linux.

<a name="envoy-installation"></a>
### Instalação

Primeiro, instale o Envoy usando o comando `global` do Composer:

	composer global require "laravel/envoy=~1.0"

Certifique-se de que o diretório `~/.composer/vendor/bin` esteja no PATH para que seja possível executar o comando `envoy` a partir do terminal.

#### Atualizando o Envoy

Você também deve usar o Composer para manter a instalação do Envoy atualizada:

	composer global update

<a name="writing-tasks"></a>
## Escrevendo Tarefas

Todas as suas tarefas para o Envoy devem ser definidas no arquivo `Envoy.blade.php` na pasta principal do seu projeto. Aqui um exemplo para você começar:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

Como pode ver, um array de `@servers` (servidores) é definido no topo do arquivo, permitindo a você referenciá-los na opção `on` da declaração da tarefa. Dentro da declaração da `@task` (tarefa) você deve colocar códigos Bash (comandos de terminal) que serão executados no seu servidor  quando a tarefa for executada.

#### Bootstrapping

Algumas vezes você pode precisar executar algum código PHP antes de sua tarefa ser executada. Você pode usar a diretiva `@setup` para declarar variáveis ou escrever códigos gerais PHP para usar dentro do arquivo Envoy:

	@setup
		$now = new DateTime();
    
		$environment = isset($env) ? $env : "testing";
	@endsetup

Você também pode usar a diretiva `@include` para incluir arquivos PHP externos:

	@include('vendor/autoload.php');

#### Confirmando Tarefas

Se você gostaria de enviar pra o terminal uma confirmação antes de executar a tarefa nos servidores, você pode adicionar a opção `confirm` na declaração da sua tarefa:

	@task('deploy', ['on' => 'web', 'confirm' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="task-variables"></a>
### Variáveis das Tarefas

Se precisar, você pode passar variáveis para o arquivo Envoy usando a linha de comando, permitindo que customize suas tarefas:

	envoy run deploy --branch=master

Você pode usar essas opções nas suas tarefas com a mesma sintaxe do Blade para "echo" (imprimir):

	@servers(['web' => '192.168.1.1'])

	@task('deploy', ['on' => 'web'])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-multiple-servers"></a>
### Múltiplos Servidores

Você pode facilmente rodar a tarefa em múltipos servidores. Primeiro, adicione os servidores na declaração dos `@servers`. Cada servidor deve ter uma nome único. Depois de definir os servidores, você simplesmente listá-los na declaração da tarefa no array `on`:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

Por padrão, a tarefa será executada em cada servidor serialmente. Isso significa que a tarefa deve terminar num servidor antes de ser executada no próximo.

#### Execução Paralela

Se você gostaria de rodar as tarefas em múltiplos servidores em paralelo, adicione a opção `parallel` na declaração da sua tarefa:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-task-macros"></a>
### Macros de Tarefas

Macros permitem a você definir um conjunto de tarefas para rodar em sequência usando um único comando. Por exemplo, uma macro de `deploy` pode rodar as tarefas do `git` e do `composer`:

	@servers(['web' => '192.168.1.1'])

	@macro('deploy')
		git
		composer
	@endmacro

	@task('git')
		git pull origin master
	@endtask

	@task('composer')
		composer install
	@endtask

Uma vez definida a macro, você pode executá-la por um único e simples comando:

	envoy run deploy

<a name="envoy-running-tasks"></a>
## Executando Tarefas

Para executar suas tarefas no arquivo `Envoy.blade.php`, execute o comando do Envoy `run`, passando para o comando o nome da tarefa ou macro que você gostaria de executar. O Envoy executará a tarefa e exibirá a saída do servidor enquanto a tarefa estiver rodando:

	envoy run task

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
## Notificações

<a name="hipchat"></a>
### HipChat

Depois de executar uma tarefa, você pode enviar uma notificação à sua equipe numa sala do HipChat usando a diretiva do Envoy `@hipchat`. A diretiva aceita o API Token, o nome da sala, o nome do usuário que será exibido, e a mensagem que você gostaria de enviar:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

	@after
		@hipchat('token', 'room', 'Envoy')
	@endafter

Se você desejar, você pode também passar uma mensagem customizada para a sala do HipChat. Qualquer variável disponível para suas tarefas do Envoy também estarão disponíveis enquanto você constrói sua mensagem:

	@after
		@hipchat('token', 'room', 'Envoy', "{$task} ran in the {$env} environment.")
	@endafter

<a name="slack"></a>
### Slack

Em adição ao HipChat, o Envoy também permite enviar mensagens de notificação ao [Slack](https://slack.com). A diretiva `@slack` aceita um [Slack Webhook URL](https://my.slack.com/services/new/incoming-webhook/), o nome do canal, e a mensagem que você gostaria de enviar para o canal:

	@after
		@slack('hook', 'channel', 'message')
	@endafter

Você pode conseguir uma Webhook URL criando uma integração [Incoming WebHooks](https://my.slack.com/services/new/incoming-webhook/) no  site do Slack. O argumento `hook` deve ser uma URL completa provida pelo serviço. Por exemplo:

	https://hooks.slack.com/services/ZZZZZZZZZ/YYYYYYYYY/XXXXXXXXXXXXXXX

Você também pode passar uma da seguintes opções para o argumento `channel`:

- Para enviar a notificação para um canal: `#channel`
- Para enviar a notificação para um usuário: `@user`



