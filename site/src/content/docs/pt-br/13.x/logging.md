---
title: "Logging"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
    - [Drivers de Canal Disponíveis](#available-channel-drivers)
    - [Pré-requisitos de Canal](#channel-prerequisites)
    - [Registrando Avisos de Depreciação em Log](#logging-deprecation-warnings)
- [Construindo Pilhas de Log](#building-log-stacks)
- [Escrevendo Mensagens de Log](#writing-log-messages)
    - [Informação Contextual](#contextual-information)
    - [Escrevendo em Canais Específicos](#writing-to-specific-channels)
- [Personalização de Canal Monolog](#monolog-channel-customization)
    - [Personalizando o Monolog para Canais](#customizing-monolog-for-channels)
    - [Criando Canais de Handler Monolog](#creating-monolog-handler-channels)
    - [Criando Canais Personalizados via Factories](#creating-custom-channels-via-factories)
- [Acompanhando Mensagens de Log Usando o Pail](#tailing-log-messages-using-pail)
    - [Instalação](#pail-installation)
    - [Uso](#pail-usage)
    - [Filtrando Logs](#pail-filtering-logs)

<a id="introduction"></a>
## Introdução

Para ajudar você a saber mais sobre o que está acontecendo dentro da sua aplicação, o Laravel fornece serviços de logging robustos que permitem registrar mensagens em arquivos, no log de erros do sistema e até mesmo no Slack para notificar toda a sua equipe.

O logging do Laravel é baseado em "canais". Cada canal representa uma maneira específica de escrever informações de log. Por exemplo, o canal `single` escreve arquivos de log em um único arquivo de log, enquanto o canal `slack` envia mensagens de log para o Slack. Mensagens de log podem ser escritas em múltiplos canais com base em sua severidade.

Nos bastidores, o Laravel utiliza a biblioteca [Monolog](https://github.com/Seldaek/monolog), que fornece suporte para uma variedade de handlers de log poderosos. O Laravel torna muito fácil configurar esses handlers, permitindo que você os combine e misture para personalizar o tratamento de log da sua aplicação.

<a id="configuration"></a>
## Configuração

Todas as opções de configuração que controlam o comportamento de logging da sua aplicação estão alojadas no arquivo de configuração `config/logging.php`. Este arquivo permite que você configure os canais de log da sua aplicação, então certifique-se de revisar cada um dos canais disponíveis e suas opções. Vamos revisar algumas opções comuns abaixo.

Por padrão, o Laravel usará o canal `stack` ao registrar mensagens em log. O canal `stack` é usado para agregar múltiplos canais de log em um único canal. Para mais informações sobre a construção de pilhas, confira a [documentação abaixo](#building-log-stacks).

<a id="available-channel-drivers"></a>
### Drivers de Canal Disponíveis

Cada canal de log é alimentado por um "driver". O driver determina como e onde a mensagem de log é efetivamente registrada. Os seguintes drivers de canal de log estão disponíveis em toda aplicação Laravel. Uma entrada para a maioria desses drivers já está presente no arquivo de configuração `config/logging.php` da sua aplicação, então certifique-se de revisar este arquivo para se familiarizar com seu conteúdo:

<div class="overflow-auto">

| Name         | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| `custom`     | A driver that calls a specified factory to create a channel.         |
| `daily`      | A `RotatingFileHandler` based Monolog driver which rotates daily.    |
| `monthly`    | A `RotatingFileHandler` based Monolog driver which rotates monthly.  |
| `errorlog`   | An `ErrorLogHandler` based Monolog driver.                           |
| `monolog`    | A Monolog factory driver that may use any supported Monolog handler. |
| `single`     | A single file or path based logger channel (`StreamHandler`).        |
| `slack`      | A `SlackWebhookHandler` based Monolog driver.                        |
| `stack`      | A wrapper to facilitate creating "multi-channel" channels.           |
| `syslog`     | A `SyslogHandler` based Monolog driver.                              |

</div>

> **Nota:**
> Confira a documentação sobre [personalização avançada de canal](#monolog-channel-customization) para saber mais sobre os drivers `monolog` e `custom`.

<a id="configuring-the-channel-name"></a>
#### Configurando o Nome do Canal

Por padrão, o Monolog é instanciado com um "nome de canal" que corresponde ao ambiente atual, como `production` ou `local`. Para alterar este valor, você pode adicionar uma opção `name` à configuração do seu canal:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a id="channel-prerequisites"></a>
### Pré-requisitos de Canal

<a id="configuring-the-single-daily-and-monthly-channels"></a>
#### Configurando os Canais Single, Daily e Monthly

Os canais `single`, `daily` e `monthly` têm três opções de configuração opcionais: `bubble`, `permission` e `locking`.

<div class="overflow-auto">

| Name         | Description                                                                   | Default |
| ------------ | ----------------------------------------------------------------------------- | ------- |
| `bubble`     | Indicates if messages should bubble up to other channels after being handled. | `true`  |
| `locking`    | Attempt to lock the log file before writing to it.                            | `false` |
| `permission` | The log file's permissions.                                                   | `0644`  |

</div>

Adicionalmente, a política de retenção para os canais `daily` e `monthly` pode ser configurada através da opção de configuração `max_files`. A variável de ambiente `LOG_DAILY_DAYS` também pode ser usada para configurar a retenção do canal `daily`.

<a id="configuring-the-papertrail-channel"></a>
#### Configurando o Canal Papertrail

O canal `papertrail` requer as opções de configuração `host` e `port`. Elas podem ser definidas através das variáveis de ambiente `PAPERTRAIL_URL` e `PAPERTRAIL_PORT`. Você pode obter esses valores no [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app).

<a id="configuring-the-slack-channel"></a>
#### Configurando o Canal Slack

O canal `slack` requer uma opção de configuração `url`. Este valor pode ser definido através da variável de ambiente `LOG_SLACK_WEBHOOK_URL`. Esta URL deve corresponder a uma URL de um [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) que você configurou para sua equipe do Slack.

Por padrão, o Slack receberá apenas logs no nível `critical` e acima; no entanto, você pode ajustar isso usando a variável de ambiente `LOG_LEVEL` ou modificando a opção de configuração `level` dentro do array de configuração do seu canal de log do Slack.

<a id="logging-deprecation-warnings"></a>
### Registrando Avisos de Depreciação em Log

PHP, Laravel e outras bibliotecas frequentemente notificam seus usuários de que alguns de seus recursos foram depreciados e serão removidos em uma versão futura. Se você gostaria de registrar esses avisos de depreciação em log, você pode especificar seu canal de log `deprecations` preferido usando a variável de ambiente `LOG_DEPRECATIONS_CHANNEL`, ou dentro do arquivo de configuração `config/logging.php` da sua aplicação:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

Ou, você pode definir um canal de log chamado `deprecations`. Se um canal de log com este nome existir, ele sempre será usado para registrar depreciações em log:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a id="building-log-stacks"></a>
## Construindo Pilhas de Log

Como mencionado anteriormente, o driver `stack` permite que você combine múltiplos canais em um único canal de log por conveniência. Para ilustrar como usar pilhas de log, vamos dar uma olhada em uma configuração de exemplo que você pode ver em uma aplicação de produção:

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'], // [tl! add]
        'ignore_exceptions' => false,
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => env('LOG_LEVEL', 'debug'),
        'facility' => env('LOG_SYSLOG_FACILITY', LOG_USER),
        'replace_placeholders' => true,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => env('LOG_SLACK_USERNAME', 'Laravel Log'),
        'emoji' => env('LOG_SLACK_EMOJI', ':boom:'),
        'level' => env('LOG_LEVEL', 'critical'),
        'replace_placeholders' => true,
    ],
],
```

Vamos dissecar esta configuração. Primeiro, observe que nosso canal `stack` agrega dois outros canais através de sua opção `channels`: `syslog` e `slack`. Então, ao registrar mensagens em log, ambos esses canais terão a oportunidade de registrar a mensagem. No entanto, como veremos abaixo, se esses canais efetivamente registram a mensagem pode ser determinado pela severidade / "nível" da mensagem.

<a id="log-levels"></a>
#### Níveis de Log

Observe a opção de configuração `level` presente nas configurações dos canais `syslog` e `slack` no exemplo acima. Esta opção determina o "nível" mínimo que uma mensagem deve ter para ser registrada pelo canal. O Monolog, que alimenta os serviços de logging do Laravel, oferece todos os níveis de log definidos na [especificação RFC 5424](https://tools.ietf.org/html/rfc5424). Em ordem decrescente de severidade, esses níveis de log são: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, e **debug**.

Então, imagine que registramos uma mensagem usando o método `debug`:

```php
Log::debug('An informational message.');
```

Dada a nossa configuração, o canal `syslog` escreverá a mensagem no log do sistema; no entanto, como a mensagem de erro não é `critical` ou acima, ela não será enviada ao Slack. No entanto, se registrarmos uma mensagem `emergency`, ela será enviada tanto ao log do sistema quanto ao Slack, já que o nível `emergency` está acima do nosso limiar de nível mínimo para ambos os canais:

```php
Log::emergency('The system is down!');
```

<a id="writing-log-messages"></a>
## Escrevendo Mensagens de Log

Você pode escrever informações nos logs usando a [facade](../facades/) `Log`. Como mencionado anteriormente, o logger fornece os oito níveis de logging definidos na [especificação RFC 5424](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** e **debug**:

```php
use Illuminate\Support\Facades\Log;

Log::emergency($message);
Log::alert($message);
Log::critical($message);
Log::error($message);
Log::warning($message);
Log::notice($message);
Log::info($message);
Log::debug($message);
```

Você pode chamar qualquer um desses métodos para registrar uma mensagem no nível correspondente. Por padrão, a mensagem será escrita no canal de log padrão conforme configurado pelo seu arquivo de configuração `logging`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        Log::info('Showing the user profile for user: {id}', ['id' => $id]);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<a id="contextual-information"></a>
### Informação Contextual

Um array de dados contextuais pode ser passado aos métodos de log. Esses dados contextuais serão formatados e exibidos com a mensagem de log:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

Ocasionalmente, você pode desejar especificar algumas informações contextuais que devem ser incluídas em todas as entradas de log subsequentes em um canal específico. Por exemplo, você pode desejar registrar um ID de requisição que esteja associado a cada requisição recebida pela sua aplicação. Para fazer isso, você pode chamar o método `withContext` da facade `Log`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        $response = $next($request);

        $response->headers->set('Request-Id', $requestId);

        return $response;
    }
}
```

Se você gostaria de compartilhar informações contextuais entre _todos_ os canais de logging, você pode invocar o método `Log::shareContext()`. Este método fornecerá as informações contextuais a todos os canais criados e a quaisquer canais que forem criados subsequentemente:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::shareContext([
            'request-id' => $requestId
        ]);

        // ...
    }
}
```

> **Nota:**
> Se você precisar compartilhar contexto de log ao processar jobs enfileirados, você pode utilizar [job middleware](../queues/#job-middleware).

<a id="writing-to-specific-channels"></a>
### Escrevendo em Canais Específicos

Às vezes você pode desejar registrar uma mensagem em um canal diferente do canal padrão da sua aplicação. Você pode usar o método `channel` na facade `Log` para recuperar e registrar em qualquer canal definido no seu arquivo de configuração:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

Se você gostaria de criar uma pilha de logging sob demanda consistindo de múltiplos canais, você pode usar o método `stack`:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a id="on-demand-channels"></a>
#### Canais Sob Demanda

Também é possível criar um canal sob demanda fornecendo a configuração em tempo de execução sem que essa configuração esteja presente no arquivo de configuração `logging` da sua aplicação. Para fazer isso, você pode passar um array de configuração ao método `build` da facade `Log`:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

Você também pode desejar incluir um canal sob demanda em uma pilha de logging sob demanda. Isso pode ser alcançado incluindo sua instância de canal sob demanda no array passado ao método `stack`:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a id="monolog-channel-customization"></a>
## Personalização de Canal Monolog

<a id="customizing-monolog-for-channels"></a>
### Personalizando o Monolog para Canais

Às vezes você pode precisar de controle completo sobre como o Monolog é configurado para um canal existente. Por exemplo, você pode querer configurar uma implementação personalizada de `FormatterInterface` do Monolog para o canal `single` nativo do Laravel.

Para começar, defina um array `tap` na configuração do canal. O array `tap` deve conter uma lista de classes que devem ter a oportunidade de personalizar (ou "tap" em) a instância do Monolog após ela ser criada. Não há um local convencional onde essas classes devam ser colocadas, então você é livre para criar um diretório dentro da sua aplicação para conter essas classes:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

Uma vez que você tenha configurado a opção `tap` no seu canal, você está pronto para definir a classe que personalizará sua instância do Monolog. Esta classe só precisa de um único método: `__invoke`, que recebe uma instância de `Illuminate\Log\Logger`. A instância de `Illuminate\Log\Logger` encaminha todas as chamadas de método para a instância subjacente do Monolog:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
     */
    public function __invoke(Logger $logger): void
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```

> **Nota:**
> Todas as suas classes "tap" são resolvidas pelo [service container](../container/), então quaisquer dependências de construtor que elas requeiram serão automaticamente injetadas.

<a id="creating-monolog-handler-channels"></a>
### Criando Canais de Handler Monolog

O Monolog tem uma variedade de [handlers disponíveis](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) e o Laravel não inclui um canal nativo para cada um deles. Em alguns casos, você pode desejar criar um canal personalizado que seja meramente uma instância de um handler Monolog específico que não tem um driver de log Laravel correspondente. Esses canais podem ser facilmente criados usando o driver `monolog`.

Ao usar o driver `monolog`, a opção de configuração `handler` é usada para especificar qual handler será instanciado. Opcionalmente, quaisquer parâmetros de construtor que o handler necessite podem ser especificados usando a opção de configuração `handler_with`:

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'handler_with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a id="monolog-formatters"></a>
#### Formatters do Monolog

Ao usar o driver `monolog`, o `LineFormatter` do Monolog será usado como o formatter padrão. No entanto, você pode personalizar o tipo de formatter passado ao handler usando as opções de configuração `formatter` e `formatter_with`:

```php
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```

Se você estiver usando um handler Monolog que seja capaz de fornecer seu próprio formatter, você pode definir o valor da opção de configuração `formatter` como `default`:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a id="monolog-processors"></a>
#### Processors do Monolog

O Monolog também pode processar mensagens antes de registrá-las em log. Você pode criar seus próprios processors ou usar os [processors existentes oferecidos pelo Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor).

Se você gostaria de personalizar os processors para um driver `monolog`, adicione um valor de configuração `processors` à configuração do seu canal:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // Simple syntax...
        Monolog\Processor\MemoryUsageProcessor::class,

        // With options...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a id="creating-custom-channels-via-factories"></a>
### Criando Canais Personalizados via Factories

Se você gostaria de definir um canal totalmente personalizado no qual você tem controle completo sobre a instanciação e configuração do Monolog, você pode especificar um tipo de driver `custom` no seu arquivo de configuração `config/logging.php`. Sua configuração deve incluir uma opção `via` que contenha o nome da classe factory que será invocada para criar a instância do Monolog:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

Uma vez que você tenha configurado o canal de driver `custom`, você está pronto para definir a classe que criará sua instância do Monolog. Esta classe só precisa de um único método `__invoke` que deve retornar a instância do logger Monolog. O método receberá o array de configuração dos canais como seu único argumento:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a id="tailing-log-messages-using-pail"></a>
## Acompanhando Mensagens de Log Usando o Pail

Frequentemente você pode precisar acompanhar os logs da sua aplicação em tempo real. Por exemplo, ao depurar um problema ou ao monitorar os logs da sua aplicação em busca de tipos específicos de erros.

O Laravel Pail é um pacote que permite que você mergulhe facilmente nos arquivos de log da sua aplicação Laravel diretamente da linha de comando. Ao contrário do comando `tail` padrão, o Pail foi projetado para funcionar com qualquer driver de log, incluindo [Laravel Nightwatch](https://nightwatch.laravel.com), Sentry, ou Flare. Além disso, o Pail fornece um conjunto de filtros úteis para ajudar você a encontrar rapidamente o que está procurando.

<img src="https://laravel.com/img/docs/pail-example.png">

<a id="pail-installation"></a>
### Instalação

> **Aviso:**
> O Laravel Pail requer a extensão PHP [PCNTL](https://www.php.net/manual/en/book.pcntl.php).

Para começar, instale o Pail no seu projeto usando o gerenciador de pacotes Composer:

```shell
composer require --dev laravel/pail
```

<a id="pail-usage"></a>
### Uso

Para começar a acompanhar logs, execute o comando `pail`:

```shell
php artisan pail
```

Para aumentar a verbosidade da saída e evitar truncamento (…), use a opção `-v`:

```shell
php artisan pail -v
```

Para verbosidade máxima e para exibir stack traces de exceções, use a opção `-vv`:

```shell
php artisan pail -vv
```

Para parar de acompanhar logs, pressione `Ctrl+C` a qualquer momento.

<a id="pail-filtering-logs"></a>
### Filtrando Logs

<a id="pail-filtering-logs-filter-option"></a>
#### `--filter`

Você pode usar a opção `--filter` para filtrar logs pelo seu tipo, arquivo, mensagem e conteúdo do stack trace:

```shell
php artisan pail --filter="QueryException"
```

<a id="pail-filtering-logs-message-option"></a>
#### `--message`

Para filtrar logs apenas pela sua mensagem, você pode usar a opção `--message`:

```shell
php artisan pail --message="User created"
```

<a id="pail-filtering-logs-level-option"></a>
#### `--level`

A opção `--level` pode ser usada para filtrar logs pelo seu [nível de log](#log-levels):

```shell
php artisan pail --level=error
```

<a id="pail-filtering-logs-user-option"></a>
#### `--user`

Para exibir apenas logs que foram escritos enquanto um determinado usuário estava autenticado, você pode fornecer o ID do usuário à opção `--user`:

```shell
php artisan pail --user=1
```
