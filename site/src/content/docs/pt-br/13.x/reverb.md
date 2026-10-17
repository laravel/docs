---
title: "Laravel Reverb"
---

- [Introdução](#introduction)
- [Instalação](#installation)
- [Configuração](#configuration)
    - [Credenciais da Aplicação](#application-credentials)
    - [Origens Permitidas](#allowed-origins)
    - [Aplicações Adicionais](#additional-applications)
    - [SSL](#ssl)
- [Executando o Servidor](#running-server)
    - [Depuração](#debugging)
    - [Reiniciando](#restarting)
- [Monitoramento](#monitoring)
- [Executando o Reverb em Produção](#production)
    - [Arquivos Abertos](#open-files)
    - [Event Loop](#event-loop)
    - [Servidor Web](#web-server)
    - [Portas](#ports)
    - [Gerenciamento de Processos](#process-management)
    - [Escalabilidade](#scaling)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

[Laravel Reverb](https://github.com/laravel/reverb) traz comunicação WebSocket em tempo real, extremamente rápida e escalável, diretamente para a sua aplicação Laravel, e oferece integração perfeita com o conjunto existente de [ferramentas de broadcasting de eventos](../broadcasting/) do Laravel.

<a id="installation"></a>
## Instalação

Você pode instalar o Reverb usando o comando Artisan `install:broadcasting`:

```shell
php artisan install:broadcasting
```

<a id="configuration"></a>
## Configuração

Nos bastidores, o comando Artisan `install:broadcasting` executará o comando `reverb:install`, que instalará o Reverb com um conjunto sensato de opções de configuração padrão. Se você quiser fazer alguma alteração de configuração, pode fazê-la atualizando as variáveis de ambiente do Reverb ou o arquivo de configuração `config/reverb.php`.

<a id="application-credentials"></a>
### Credenciais da Aplicação

Para estabelecer uma conexão com o Reverb, um conjunto de credenciais de "aplicação" do Reverb deve ser trocado entre o cliente e o servidor. Essas credenciais são configuradas no servidor e são usadas para verificar a requisição do cliente. Você pode definir essas credenciais usando as seguintes variáveis de ambiente:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a id="allowed-origins"></a>
### Origens Permitidas

Você também pode definir as origens de onde as requisições do cliente podem se originar, atualizando o valor da opção `allowed_origins` na seção `apps` do arquivo de configuração `config/reverb.php`. Quaisquer requisições de uma origem não listada nas suas origens permitidas serão rejeitadas. Você pode permitir todas as origens usando `*`:

```php
'apps' => [
    [
        'app_id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]
```

<a id="additional-applications"></a>
### Aplicações Adicionais

Tipicamente, o Reverb fornece um servidor WebSocket para a aplicação na qual está instalado. No entanto, também é possível servir mais de uma aplicação usando uma única instalação do Reverb.

Por exemplo, você pode querer manter uma única aplicação Laravel que, por meio do Reverb, fornece conectividade WebSocket para múltiplas aplicações. Isso pode ser feito definindo múltiplos `apps` no arquivo de configuração `config/reverb.php` da sua aplicação:

```php
'apps' => [
    [
        'app_id' => 'my-app-one',
        // ...
    ],
    [
        'app_id' => 'my-app-two',
        // ...
    ],
],
```

<a id="ssl"></a>
### SSL

Na maioria dos casos, as conexões WebSocket seguras são tratadas pelo servidor web de entrada (Nginx, etc.) antes que a requisição seja encaminhada ao seu servidor Reverb.

No entanto, às vezes pode ser útil, como durante o desenvolvimento local, que o servidor Reverb trate conexões seguras diretamente. Se você estiver usando o recurso de site seguro do [Laravel Herd](https://herd.laravel.com) ou estiver usando o [Laravel Valet](../valet/) e tiver executado o [comando secure](../valet/#securing-sites) na sua aplicação, você pode usar o certificado do Herd / Valet gerado para o seu site para proteger suas conexões Reverb. Para isso, defina a variável de ambiente `REVERB_HOST` com o hostname do seu site ou passe explicitamente a opção de hostname ao iniciar o servidor Reverb:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Como os domínios do Herd e do Valet resolvem para `localhost`, executar o comando acima fará com que o seu servidor Reverb fique acessível pelo protocolo WebSocket seguro (`wss`) em `wss://laravel.test:8080`.

Você também pode escolher manualmente um certificado definindo as opções `tls` no arquivo de configuração `config/reverb.php` da sua aplicação. Dentro do array de opções `tls`, você pode fornecer quaisquer opções suportadas pelas [opções de contexto SSL do PHP](https://www.php.net/manual/en/context.ssl.php):

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a id="running-server"></a>
## Executando o Servidor

O servidor Reverb pode ser iniciado usando o comando Artisan `reverb:start`:

```shell
php artisan reverb:start
```

Por padrão, o servidor Reverb será iniciado em `0.0.0.0:8080`, tornando-o acessível a partir de todas as interfaces de rede.

Se você precisar especificar um host ou porta personalizados, pode fazê-lo pelas opções `--host` e `--port` ao iniciar o servidor:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

Alternativamente, você pode definir as variáveis de ambiente `REVERB_SERVER_HOST` e `REVERB_SERVER_PORT` no arquivo de configuração `.env` da sua aplicação.

As variáveis de ambiente `REVERB_SERVER_HOST` e `REVERB_SERVER_PORT` não devem ser confundidas com `REVERB_HOST` e `REVERB_PORT`. As primeiras especificam o host e a porta nos quais o próprio servidor Reverb será executado, enquanto o segundo par instrui o Laravel sobre para onde enviar as mensagens de broadcast. Por exemplo, em um ambiente de produção, você pode encaminhar requisições do seu hostname público do Reverb na porta `443` para um servidor Reverb operando em `0.0.0.0:8080`. Nesse cenário, suas variáveis de ambiente seriam definidas da seguinte forma:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a id="debugging"></a>
### Depuração

Para melhorar o desempenho, o Reverb não exibe nenhuma informação de depuração por padrão. Se você quiser ver o fluxo de dados que passa pelo seu servidor Reverb, pode fornecer a opção `--debug` ao comando `reverb:start`:

```shell
php artisan reverb:start --debug
```

<a id="restarting"></a>
### Reiniciando

Como o Reverb é um processo de longa duração, alterações no seu código não serão refletidas sem reiniciar o servidor por meio do comando Artisan `reverb:restart`.

O comando `reverb:restart` garante que todas as conexões sejam encerradas graciosamente antes de parar o servidor. Se você estiver executando o Reverb com um gerenciador de processos como o Supervisor, o servidor será reiniciado automaticamente pelo gerenciador de processos após o término de todas as conexões:

```shell
php artisan reverb:restart
```

<a id="monitoring"></a>
## Monitoramento

O Reverb pode ser monitorado por meio de uma integração com o [Laravel Pulse](../pulse/). Ao habilitar a integração do Pulse com o Reverb, você pode acompanhar o número de conexões e mensagens processadas pelo seu servidor.

Para habilitar a integração, primeiro certifique-se de ter [instalado o Pulse](../pulse/#installation). Em seguida, adicione quaisquer um dos recorders do Reverb ao arquivo de configuração `config/pulse.php` da sua aplicação:

```php
use Laravel\Reverb\Pulse\Recorders\ReverbConnections;
use Laravel\Reverb\Pulse\Recorders\ReverbMessages;

'recorders' => [
    ReverbConnections::class => [
        'sample_rate' => 1,
    ],

    ReverbMessages::class => [
        'sample_rate' => 1,
    ],

    // ...
],
```

Em seguida, adicione os cards do Pulse de cada recorder ao seu [dashboard do Pulse](../pulse/#dashboard-customization):

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

A atividade de conexão é registrada consultando periodicamente por novas atualizações. Para garantir que essas informações sejam renderizadas corretamente no dashboard do Pulse, você deve executar o daemon `pulse:check` no seu servidor Reverb. Se você estiver executando o Reverb em uma configuração [escalada horizontalmente](#scaling), você deve executar esse daemon em apenas um dos seus servidores.

<a id="production"></a>
## Executando o Reverb em Produção

Devido à natureza de longa duração dos servidores WebSocket, pode ser necessário fazer algumas otimizações no seu servidor e no ambiente de hospedagem para garantir que seu servidor Reverb consiga lidar de forma eficaz com o número ideal de conexões para os recursos disponíveis no seu servidor.

> **Nota:**
> O [Laravel Cloud](https://cloud.laravel.com) oferece infraestrutura WebSocket totalmente gerenciada, com tecnologia de clusters do Laravel Reverb, permitindo que você escale e publique aplicações com Reverb sem gerenciar infraestrutura.

<a id="open-files"></a>
### Arquivos Abertos

Cada conexão WebSocket é mantida em memória até que o cliente ou o servidor se desconecte. Em ambientes Unix e semelhantes ao Unix, cada conexão é representada por um arquivo. No entanto, geralmente há limites para o número de arquivos abertos permitidos, tanto no nível do sistema operacional quanto no nível da aplicação.

<a id="operating-system"></a>
#### Sistema Operacional

Em um sistema operacional baseado em Unix, você pode determinar o número permitido de arquivos abertos usando o comando `ulimit`:

```shell
ulimit -n
```

Este comando exibirá os limites de arquivos abertos permitidos para diferentes usuários. Você pode atualizar esses valores editando o arquivo `/etc/security/limits.conf`. Por exemplo, atualizar o número máximo de arquivos abertos para 10.000 para o usuário `forge` ficaria assim:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a id="event-loop"></a>
### Event Loop

Nos bastidores, o Reverb usa um event loop do ReactPHP para gerenciar as conexões WebSocket no servidor. Por padrão, esse event loop é alimentado por `stream_select`, que não requer nenhuma extensão adicional. No entanto, `stream_select` normalmente é limitado a 1.024 arquivos abertos. Assim, se você planeja lidar com mais de 1.000 conexões simultâneas, precisará usar um event loop alternativo que não esteja sujeito às mesmas restrições.

O Reverb mudará automaticamente para um loop baseado em `ext-uv` quando disponível. Esta extensão do PHP pode ser instalada via PECL:

```shell
pecl install uv
```

<a id="web-server"></a>
### Servidor Web

Na maioria dos casos, o Reverb é executado em uma porta não exposta à web no seu servidor. Assim, para encaminhar o tráfego para o Reverb, você deve configurar um proxy reverso. Supondo que o Reverb esteja rodando no host `0.0.0.0` e na porta `8080` e que seu servidor utilize o servidor web Nginx, um proxy reverso pode ser definido para o seu servidor Reverb usando a seguinte configuração de site do Nginx:

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://0.0.0.0:8080;
    }

    ...
}
```

> **Aviso:**
> O Reverb escuta conexões WebSocket em `/app` e trata requisições de API em `/apps`. Você deve garantir que o servidor web que trata as requisições do Reverb consiga servir ambas as URIs. Se você estiver usando o [Laravel Forge](https://forge.laravel.com) para gerenciar seus servidores, seu servidor Reverb será configurado corretamente por padrão.

Tipicamente, os servidores web são configurados para limitar o número de conexões permitidas, a fim de evitar sobrecarga do servidor. Para aumentar o número de conexões permitidas em um servidor web Nginx para 10.000, os valores `worker_rlimit_nofile` e `worker_connections` do arquivo `nginx.conf` devem ser atualizados:

```nginx
user forge;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
worker_rlimit_nofile 10000;

events {
  worker_connections 10000;
  multi_accept on;
}
```

A configuração acima permitirá que até 10.000 workers do Nginx por processo sejam criados. Além disso, essa configuração define o limite de arquivos abertos do Nginx em 10.000.

<a id="ports"></a>
### Portas

Sistemas operacionais baseados em Unix normalmente limitam o número de portas que podem ser abertas no servidor. Você pode ver o intervalo permitido atual pelo seguinte comando:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

A saída acima mostra que o servidor pode lidar com no máximo 28.231 (60.999 - 32.768) conexões, já que cada conexão requer uma porta livre. Embora recomendemos o [escalonamento horizontal](#scaling) para aumentar o número de conexões permitidas, você pode aumentar o número de portas abertas disponíveis atualizando o intervalo de portas permitido no arquivo de configuração `/etc/sysctl.conf` do seu servidor.

<a id="process-management"></a>
### Gerenciamento de Processos

Na maioria dos casos, você deve usar um gerenciador de processos como o Supervisor para garantir que o servidor Reverb esteja sempre em execução. Se você estiver usando o Supervisor para executar o Reverb, deve atualizar a configuração `minfds` do arquivo `supervisor.conf` do seu servidor para garantir que o Supervisor consiga abrir os arquivos necessários para tratar conexões com o seu servidor Reverb:

```ini
[supervisord]
...
minfds=10000
```

<a id="scaling"></a>
### Escalabilidade

Se você precisar lidar com mais conexões do que um único servidor permite, pode escalar seu servidor Reverb horizontalmente. Utilizando as capacidades de publicação / assinatura do Redis, o Reverb consegue gerenciar conexões entre múltiplos servidores. Quando uma mensagem é recebida por um dos servidores Reverb da sua aplicação, o servidor usará o Redis para publicar a mensagem recebida em todos os outros servidores.

Para habilitar o escalonamento horizontal, você deve definir a variável de ambiente `REVERB_SCALING_ENABLED` como `true` no arquivo de configuração `.env` da sua aplicação:

```env
REVERB_SCALING_ENABLED=true
```

Em seguida, você deve ter um servidor Redis central e dedicado, com o qual todos os servidores Reverb irão se comunicar. O Reverb usará a [conexão Redis padrão configurada para sua aplicação](../redis/#configuration) para publicar mensagens em todos os seus servidores Reverb.

Depois de habilitar a opção de escalabilidade do Reverb e configurar um servidor Redis, basta invocar o comando `reverb:start` em múltiplos servidores que consigam se comunicar com o seu servidor Redis. Esses servidores Reverb devem ser colocados atrás de um load balancer que distribua as requisições recebidas de forma uniforme entre os servidores.

<a id="events"></a>
## Eventos

O Reverb dispara eventos internos durante o ciclo de vida de uma conexão e do tratamento de mensagens. Você pode [escutar esses eventos](../events/) para executar ações quando conexões forem gerenciadas ou mensagens forem trocadas.

Os seguintes eventos são disparados pelo Reverb:

#### `Laravel\Reverb\Events\ChannelCreated`

Disparado quando um canal é criado. Isso normalmente ocorre quando a primeira conexão se inscreve em um canal específico. O evento recebe a instância de `Laravel\Reverb\Protocols\Pusher\Channel`.

#### `Laravel\Reverb\Events\ChannelRemoved`

Disparado quando um canal é removido. Isso normalmente ocorre quando a última conexão cancela a inscrição em um canal. O evento recebe a instância de `Laravel\Reverb\Protocols\Pusher\Channel`.

#### `Laravel\Reverb\Events\ConnectionPruned`

Disparado quando uma conexão obsoleta é removida pelo servidor. O evento recebe a instância de `Laravel\Reverb\Contracts\Connection`.

#### `Laravel\Reverb\Events\MessageReceived`

Disparado quando uma mensagem é recebida de uma conexão de cliente. O evento recebe a instância de `Laravel\Reverb\Contracts\Connection` e a string bruta `$message`.

#### `Laravel\Reverb\Events\MessageSent`

Disparado quando uma mensagem é enviada para uma conexão de cliente. O evento recebe a instância de `Laravel\Reverb\Contracts\Connection` e a string bruta `$message`.
