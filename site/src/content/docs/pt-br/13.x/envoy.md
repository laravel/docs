---
title: "Laravel Envoy"
---

- [Introdução](#introduction)
- [Instalação](#installation)
- [Escrevendo Tarefas](#writing-tasks)
    - [Definindo Tarefas](#defining-tasks)
    - [Múltiplos Servidores](#multiple-servers)
    - [Configuração](#setup)
    - [Variáveis](#variables)
    - [Stories](#stories)
    - [Hooks](#completion-hooks)
- [Executando Tarefas](#running-tasks)
    - [Confirmando a Execução de Tarefas](#confirming-task-execution)
- [Notificações](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a id="introduction"></a>
## Introdução

[Laravel Envoy](https://github.com/laravel/envoy) é uma ferramenta para executar tarefas comuns que você roda nos seus servidores remotos. Usando uma sintaxe no estilo [Blade](../blade/), você pode configurar facilmente tarefas para deploy, comandos Artisan e outras operações. Atualmente, o Envoy suporta apenas os sistemas operacionais Mac e Linux. No entanto, é possível obter suporte ao Windows usando o [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

<a id="installation"></a>
## Instalação

Primeiro, instale o Envoy no seu projeto usando o gerenciador de pacotes Composer:

```shell
composer require laravel/envoy --dev
```

Depois que o Envoy estiver instalado, o binário do Envoy estará disponível no diretório `vendor/bin` da sua aplicação:

```shell
php vendor/bin/envoy
```

<a id="writing-tasks"></a>
## Escrevendo Tarefas

<a id="defining-tasks"></a>
### Definindo Tarefas

Tarefas são o bloco de construção básico do Envoy. Elas definem os comandos de shell que devem ser executados nos seus servidores remotos quando a tarefa for invocada. Por exemplo, você pode definir uma tarefa que executa o comando `php artisan queue:restart` em todos os servidores de workers de filas da sua aplicação.

Todas as tarefas do Envoy devem ser definidas em um arquivo `Envoy.blade.php` na raiz da sua aplicação. Aqui está um exemplo para você começar:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

Como você pode ver, um array de `@servers` é definido no topo do arquivo, permitindo referenciar esses servidores pela opção `on` das suas declarações de tarefas. A declaração `@servers` deve sempre ser colocada em uma única linha. Dentro das declarações `@task`, você deve colocar os comandos de shell que devem ser executados nos seus servidores quando a tarefa for invocada.

<a id="local-tasks"></a>
#### Tarefas Locais

Você pode forçar a execução de um script no seu computador local especificando o endereço IP do servidor como `127.0.0.1`:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a id="importing-envoy-tasks"></a>
#### Importando Tarefas do Envoy

Usando a diretiva `@import`, você pode importar outros arquivos do Envoy para que suas stories e tarefas sejam adicionadas às suas. Depois que os arquivos forem importados, você poderá executar as tarefas que eles contêm como se tivessem sido definidas no seu próprio arquivo Envoy:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a id="multiple-servers"></a>
### Múltiplos Servidores

O Envoy permite executar uma tarefa facilmente em vários servidores. Primeiro, adicione servidores extras à sua declaração `@servers`. Cada servidor deve receber um nome único. Depois de definir os servidores adicionais, você pode listar cada um deles no array `on` da tarefa:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a id="parallel-execution"></a>
#### Execução Paralela

Por padrão, as tarefas são executadas em cada servidor de forma serial. Em outras palavras, uma tarefa termina de rodar no primeiro servidor antes de prosseguir para execução no segundo servidor. Se você quiser executar uma tarefa em vários servidores em paralelo, adicione a opção `parallel` à declaração da tarefa:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a id="setup"></a>
### Configuração

Às vezes, você pode precisar executar código PHP arbitrário antes de rodar suas tarefas do Envoy. Você pode usar a diretiva `@setup` para definir um bloco de código PHP que deve ser executado antes das suas tarefas:

```blade
@setup
    $now = new DateTime;
@endsetup
```

Se precisar importar outros arquivos PHP antes de a tarefa ser executada, você pode usar a diretiva `@include` no topo do seu arquivo `Envoy.blade.php`:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a id="variables"></a>
### Variáveis

Se necessário, você pode passar argumentos para as tarefas do Envoy especificando-os na linha de comando ao invocar o Envoy:

```shell
php vendor/bin/envoy run deploy --branch=master
```

Você pode acessar as opções dentro das suas tarefas usando a sintaxe de "echo" do Blade. Você também pode definir estruturas `if` e loops do Blade dentro das suas tarefas. Por exemplo, vamos verificar a presença da variável `$branch` antes de executar o comando `git pull`:

```blade
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask
```

<a id="stories"></a>
### Stories

Stories agrupam um conjunto de tarefas sob um único nome conveniente. Por exemplo, uma story `deploy` pode executar as tarefas `update-code` e `install-dependencies` listando os nomes das tarefas na sua definição:

```blade
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask
```

Depois que a story for escrita, você pode invocá-la da mesma forma que invocaria uma tarefa:

```shell
php vendor/bin/envoy run deploy
```

<a id="completion-hooks"></a>
### Hooks

Quando tarefas e stories são executadas, vários hooks são disparados. Os tipos de hook suportados pelo Envoy são `@before`, `@after`, `@error`, `@success` e `@finished`. Todo o código dentro desses hooks é interpretado como PHP e executado localmente, não nos servidores remotos com os quais suas tarefas interagem.

Você pode definir quantos hooks de cada tipo quiser. Eles serão executados na ordem em que aparecem no seu script do Envoy.

<a id="hook-before"></a>
#### `@before`

Antes de cada execução de tarefa, todos os hooks `@before` registrados no seu script do Envoy serão executados. Os hooks `@before` recebem o nome da tarefa que será executada:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a id="completion-after"></a>
#### `@after`

Após cada execução de tarefa, todos os hooks `@after` registrados no seu script do Envoy serão executados. Os hooks `@after` recebem o nome da tarefa que foi executada:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a id="completion-error"></a>
#### `@error`

Após cada falha de tarefa (que termina com um código de status maior que `0`), todos os hooks `@error` registrados no seu script do Envoy serão executados. Os hooks `@error` recebem o nome da tarefa que foi executada:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a id="completion-success"></a>
#### `@success`

Se todas as tarefas forem executadas sem erros, todos os hooks `@success` registrados no seu script do Envoy serão executados:

```blade
@success
    // ...
@endsuccess
```

<a id="completion-finished"></a>
#### `@finished`

Após a execução de todas as tarefas (independentemente do status de saída), todos os hooks `@finished` serão executados. Os hooks `@finished` recebem o código de status da tarefa concluída, que pode ser `null` ou um `integer` maior ou igual a `0`:

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished
```

<a id="running-tasks"></a>
## Executando Tarefas

Para executar uma tarefa ou story definida no arquivo `Envoy.blade.php` da sua aplicação, execute o comando `run` do Envoy, passando o nome da tarefa ou story que deseja executar. O Envoy executará a tarefa e exibirá a saída dos seus servidores remotos enquanto a tarefa estiver em execução:

```shell
php vendor/bin/envoy run deploy
```

<a id="confirming-task-execution"></a>
### Confirmando a Execução de Tarefas

Se você quiser ser solicitado a confirmar antes de executar uma determinada tarefa nos seus servidores, adicione a diretiva `confirm` à declaração da tarefa. Essa opção é especialmente útil para operações destrutivas:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a id="notifications"></a>
## Notificações

<a id="slack"></a>
### Slack

O Envoy oferece suporte ao envio de notificações para o [Slack](https://slack.com) após a execução de cada tarefa. A diretiva `@slack` aceita uma URL de hook do Slack e um nome de canal / usuário. Você pode obter sua URL de webhook criando uma integração "Incoming WebHooks" no painel de controle do Slack.

Você deve passar a URL completa do webhook como o primeiro argumento da diretiva `@slack`. O segundo argumento da diretiva `@slack` deve ser o nome de um canal (`#channel`) ou de um usuário (`@user`):

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

Por padrão, as notificações do Envoy enviarão ao canal de notificação uma mensagem descrevendo a tarefa que foi executada. No entanto, você pode substituir essa mensagem por uma mensagem personalizada passando um terceiro argumento à diretiva `@slack`:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a id="discord"></a>
### Discord

O Envoy também oferece suporte ao envio de notificações para o [Discord](https://discord.com) após a execução de cada tarefa. A diretiva `@discord` aceita uma URL de hook do Discord e uma mensagem. Você pode obter sua URL de webhook criando um "Webhook" nas Configurações do Servidor e escolhendo em qual canal o webhook deve publicar. Você deve passar a URL completa do Webhook para a diretiva `@discord`:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a id="telegram"></a>
### Telegram

O Envoy também oferece suporte ao envio de notificações para o [Telegram](https://telegram.org) após a execução de cada tarefa. A diretiva `@telegram` aceita um ID de Bot do Telegram e um ID de Chat. Você pode obter seu ID de Bot criando um novo bot usando o [BotFather](https://t.me/botfather). Você pode obter um ID de Chat válido usando o [@username_to_id_bot](https://t.me/username_to_id_bot). Você deve passar o ID do Bot e o ID do Chat completos para a diretiva `@telegram`:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a id="microsoft-teams"></a>
### Microsoft Teams

O Envoy também oferece suporte ao envio de notificações para o [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) após a execução de cada tarefa. A diretiva `@microsoftTeams` aceita um Webhook do Teams (obrigatório), uma mensagem, uma cor de tema (success, info, warning, error) e um array de opções. Você pode obter seu Webhook do Teams criando um novo [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). A API do Teams possui muitos outros atributos para personalizar sua caixa de mensagem, como título, resumo e seções. Você pode encontrar mais informações na [documentação do Microsoft Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). Você deve passar a URL completa do Webhook para a diretiva `@microsoftTeams`:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
