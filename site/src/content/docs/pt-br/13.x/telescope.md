---
title: "Laravel Telescope"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Instalação Apenas Local](#local-only-installation)
    - [Configuração](#configuration)
    - [Poda de Dados](#data-pruning)
    - [Autorização do Painel](#dashboard-authorization)
- [Atualizando o Telescope](#upgrading-telescope)
- [Filtragem](#filtering)
    - [Entradas](#filtering-entries)
    - [Lotes](#filtering-batches)
- [Tags](#tagging)
- [Watchers Disponíveis](#available-watchers)
    - [Watcher de Lotes](#batch-watcher)
    - [Watcher de Cache](#cache-watcher)
    - [Watcher de Comandos](#command-watcher)
    - [Watcher de Dumps](#dump-watcher)
    - [Watcher de Eventos](#event-watcher)
    - [Watcher de Exceções](#exception-watcher)
    - [Watcher de Gates](#gate-watcher)
    - [Watcher de Cliente HTTP](#http-client-watcher)
    - [Watcher de Jobs](#job-watcher)
    - [Watcher de Logs](#log-watcher)
    - [Watcher de E-mails](#mail-watcher)
    - [Watcher de Models](#model-watcher)
    - [Watcher de Notificações](#notification-watcher)
    - [Watcher de Consultas](#query-watcher)
    - [Watcher de Redis](#redis-watcher)
    - [Watcher de Requisições](#request-watcher)
    - [Watcher de Agendamentos](#schedule-watcher)
    - [Watcher de Views](#view-watcher)
- [Exibindo Avatares de Usuários](#displaying-user-avatars)

<a id="introduction"></a>
## Introdução

[Laravel Telescope](https://github.com/laravel/telescope) é um excelente companheiro para o seu ambiente de desenvolvimento local do Laravel. O Telescope oferece visibilidade sobre as requisições que chegam à sua aplicação, exceções, entradas de log, consultas ao banco de dados, jobs em fila, e-mails, notificações, operações de cache, tarefas agendadas, dumps de variáveis e muito mais.

<img src="https://laravel.com/img/docs/telescope-example.png">

<a id="installation"></a>
## Instalação

Você pode usar o gerenciador de pacotes Composer para instalar o Telescope no seu projeto Laravel:

```shell
composer require laravel/telescope
```

Após instalar o Telescope, publique seus assets e migrações usando o comando Artisan `telescope:install`. Após instalar o Telescope, você também deve executar o comando `migrate` para criar as tabelas necessárias para armazenar os dados do Telescope:

```shell
php artisan telescope:install

php artisan migrate
```

Por fim, você pode acessar o painel do Telescope pela rota `/telescope`.

<a id="local-only-installation"></a>
### Instalação Apenas Local

Se você planeja usar o Telescope apenas para auxiliar no seu desenvolvimento local, pode instalá-lo usando a flag `--dev`:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

Após executar `telescope:install`, você deve remover o registro do provedor de serviço `TelescopeServiceProvider` do arquivo de configuração `bootstrap/providers.php` da sua aplicação. Em vez disso, registre manualmente os provedores de serviço do Telescope no método `register` da sua classe `App\Providers\AppServiceProvider`. Garantiremos que o ambiente atual seja `local` antes de registrar os provedores:

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

Por fim, você também deve impedir que o pacote Telescope seja [auto-descoberto](../packages/#package-discovery) adicionando o seguinte ao seu arquivo `composer.json`:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a id="configuration"></a>
### Configuração

Após publicar os assets do Telescope, seu arquivo de configuração principal estará localizado em `config/telescope.php`. Este arquivo permite configurar as suas [opções de watchers](#available-watchers). Cada opção de configuração inclui uma descrição de sua finalidade, então não deixe de explorar este arquivo detalhadamente.

Se desejar, você pode desativar completamente a coleta de dados do Telescope usando a opção de configuração `enabled`:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a id="content-security-policy-csp-nonce"></a>
#### Nonce da Política de Segurança de Conteúdo (CSP)

Se você quiser usar um [atributo nonce](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce) nas tags script e style usadas nas views do Telescope como parte da sua [Política de Segurança de Conteúdo](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), você pode usar o método `Telescope::cspNonce` para especificar o nonce a ser usado. Este método normalmente deve ser invocado dentro de um middleware para que um novo nonce seja atribuído a cada requisição:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Telescope\Telescope;
use Symfony\Component\HttpFoundation\Response;

public function handle(Request $request, Closure $next): Response
{
    Telescope::cspNonce('csp-nonce');

    return $next($request);
}
```

Você pode adicionar este middleware à opção `middleware` no arquivo de configuração `config/telescope.php` da sua aplicação:

```php
'middleware' => [
    'web',
    App\Http\Middleware\AddTelescopeCspNonce::class,
    Authorize::class,
],
```

<a id="data-pruning"></a>
### Poda de Dados

Sem a poda, a tabela `telescope_entries` pode acumular registros muito rapidamente. Para mitigar isso, você deve [agendar](../scheduling/) o comando Artisan `telescope:prune` para ser executado diariamente:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

Por padrão, todas as entradas com mais de 24 horas serão podadas. Você pode usar a opção `hours` ao chamar o comando para determinar por quanto tempo reter os dados do Telescope. Por exemplo, o comando a seguir excluirá todos os registros criados há mais de 48 horas:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a id="dashboard-authorization"></a>
### Autorização do Painel

O painel do Telescope pode ser acessado pela rota `/telescope`. Por padrão, você só poderá acessar este painel no ambiente `local`. No arquivo `app/Providers/TelescopeServiceProvider.php`, há uma definição de [gate de autorização](../authorization/#gates). Este gate de autorização controla o acesso ao Telescope em ambientes **não locais**. Você é livre para modificar este gate conforme necessário para restringir o acesso à sua instalação do Telescope:

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> **Aviso:**
> Você deve garantir que altere a variável de ambiente `APP_ENV` para `production` no seu ambiente de produção. Caso contrário, sua instalação do Telescope ficará disponível publicamente.

<a id="upgrading-telescope"></a>
## Atualizando o Telescope

Ao atualizar para uma nova versão principal do Telescope, é importante revisar cuidadosamente [o guia de atualização](https://github.com/laravel/telescope/blob/master/UPGRADE.md).

Além disso, ao atualizar para qualquer nova versão do Telescope, você deve republicar os assets do Telescope:

```shell
php artisan telescope:publish
```

Para manter os assets atualizados e evitar problemas em atualizações futuras, você pode adicionar o comando `vendor:publish --tag=laravel-assets` aos scripts `post-update-cmd` do arquivo `composer.json` da sua aplicação:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a id="filtering"></a>
## Filtragem

<a id="filtering-entries"></a>
### Entradas

Você pode filtrar os dados registrados pelo Telescope através da closure `filter` definida na sua classe `App\Providers\TelescopeServiceProvider`. Por padrão, esta closure registra todos os dados no ambiente `local` e, em todos os outros ambientes, registra apenas exceções reportáveis, jobs com falha, tarefas agendadas e dados com tags monitoradas:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a id="filtering-batches"></a>
### Lotes

Enquanto a closure `filter` filtra os dados de entradas individuais, você pode usar o método `filterBatch` para registrar uma closure que filtra todos os dados de uma determinada requisição ou comando de console. Se a closure retornar `true`, todas as entradas serão registradas pelo Telescope:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a id="tagging"></a>
## Tags

O Telescope permite pesquisar entradas por "tag". Frequentemente, as tags são nomes de classes de models do Eloquent ou IDs de usuários autenticados, que o Telescope adiciona automaticamente às entradas. Ocasionalmente, você pode querer anexar suas próprias tags personalizadas às entradas. Para isso, você pode usar o método `Telescope::tag`. O método `tag` aceita uma closure que deve retornar um array de tags. As tags retornadas pela closure serão mescladas com quaisquer tags que o Telescope anexaria automaticamente à entrada. Normalmente, você deve chamar o método `tag` dentro do método `register` da sua classe `App\Providers\TelescopeServiceProvider`:

```php
use Laravel\Telescope\EntryType;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === EntryType::REQUEST
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
}
```

<a id="available-watchers"></a>
## Watchers Disponíveis

Os "watchers" do Telescope coletam dados da aplicação quando uma requisição ou comando de console é executado. Você pode personalizar a lista de watchers que deseja habilitar no arquivo de configuração `config/telescope.php`:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

Alguns watchers também permitem fornecer opções adicionais de personalização:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],
```

<a id="batch-watcher"></a>
### Watcher de Lotes

O watcher de lotes registra informações sobre os [lotes](../queues/#job-batching) de filas, incluindo as informações do job e da conexão.

<a id="cache-watcher"></a>
### Watcher de Cache

O watcher de cache registra dados quando uma chave de cache é encontrada, não encontrada, atualizada ou esquecida.

<a id="command-watcher"></a>
### Watcher de Comandos

O watcher de comandos registra os argumentos, opções, código de saída e saída sempre que um comando Artisan é executado. Se desejar excluir certos comandos do registro do watcher, você pode especificá-los na opção `ignore` no arquivo `config/telescope.php`:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],
```

<a id="dump-watcher"></a>
### Watcher de Dumps

O watcher de dumps registra e exibe os dumps de variáveis no Telescope. Ao usar o Laravel, as variáveis podem ser exibidas usando a função global `dump`. A aba do watcher de dumps deve estar aberta em um navegador para que o dump seja registrado; caso contrário, os dumps serão ignorados pelo watcher.

<a id="event-watcher"></a>
### Watcher de Eventos

O watcher de eventos registra o payload, os listeners e os dados de broadcast de quaisquer [eventos](../events/) disparados pela sua aplicação. Os eventos internos do framework Laravel são ignorados pelo watcher de eventos.

<a id="exception-watcher"></a>
### Watcher de Exceções

O watcher de exceções registra os dados e o stack trace de quaisquer exceções reportáveis lançadas pela sua aplicação.

<a id="gate-watcher"></a>
### Watcher de Gates

O watcher de gates registra os dados e o resultado das verificações de [gates e policies](../authorization/) realizadas pela sua aplicação. Se desejar excluir certas habilidades do registro do watcher, você pode especificá-las na opção `ignore_abilities` no arquivo `config/telescope.php`:

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],
```

<a id="http-client-watcher"></a>
### Watcher de Cliente HTTP

O watcher de cliente HTTP registra as [requisições HTTP de saída](../http-client/) feitas pela sua aplicação.

<a id="job-watcher"></a>
### Watcher de Jobs

O watcher de jobs registra os dados e o status de quaisquer [jobs](../queues/) disparados pela sua aplicação.

<a id="log-watcher"></a>
### Watcher de Logs

O watcher de logs registra os [dados de log](../logging/) de quaisquer logs escritos pela sua aplicação.

Por padrão, o Telescope registra apenas logs no nível `error` e acima. No entanto, você pode modificar a opção `level` no arquivo `config/telescope.php` da sua aplicação para alterar esse comportamento:

```php
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a id="mail-watcher"></a>
### Watcher de E-mails

O watcher de e-mails permite visualizar no navegador uma prévia dos [e-mails](../mail/) enviados pela sua aplicação, junto com os dados associados. Você também pode baixar o e-mail como um arquivo `.eml`.

<a id="model-watcher"></a>
### Watcher de Models

O watcher de models registra as alterações de models sempre que um [evento de model](../eloquent/#events) do Eloquent é disparado. Você pode especificar quais eventos de model devem ser registrados através da opção `events` do watcher:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

Se desejar registrar o número de models hidratados durante uma determinada requisição, habilite a opção `hydrations`:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],
```

<a id="notification-watcher"></a>
### Watcher de Notificações

O watcher de notificações registra todas as [notificações](../notifications/) enviadas pela sua aplicação. Se a notificação disparar um e-mail e você tiver o watcher de e-mails habilitado, o e-mail também ficará disponível para visualização na tela do watcher de e-mails.

<a id="query-watcher"></a>
### Watcher de Consultas

O watcher de consultas registra o SQL bruto, os bindings e o tempo de execução de todas as consultas executadas pela sua aplicação. O watcher também marca como `slow` quaisquer consultas com mais de 100 milissegundos. Você pode personalizar o limite de consultas lentas usando a opção `slow` do watcher:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],
```

<a id="redis-watcher"></a>
### Watcher de Redis

O watcher de Redis registra todos os comandos [Redis](../redis/) executados pela sua aplicação. Se você estiver usando Redis para cache, os comandos de cache também serão registrados pelo watcher de Redis.

<a id="request-watcher"></a>
### Watcher de Requisições

O watcher de requisições registra os dados da requisição, cabeçalhos, sessão e resposta associados a quaisquer requisições tratadas pela aplicação. Você pode limitar os dados de resposta registrados através da opção `size_limit` (em kilobytes):

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],
```

<a id="schedule-watcher"></a>
### Watcher de Agendamentos

O watcher de agendamentos registra o comando e a saída de quaisquer [tarefas agendadas](../scheduling/) executadas pela sua aplicação.

<a id="view-watcher"></a>
### Watcher de Views

O watcher de views registra o nome, o caminho, os dados e os "composers" utilizados ao renderizar as [views](../views/).

<a id="displaying-user-avatars"></a>
## Exibindo Avatares de Usuários

O painel do Telescope exibe o avatar do usuário que estava autenticado quando uma determinada entrada foi salva. Por padrão, o Telescope obtém os avatares usando o serviço web Gravatar. No entanto, você pode personalizar a URL do avatar registrando um callback na sua classe `App\Providers\TelescopeServiceProvider`. O callback receberá o ID e o endereço de e-mail do usuário e deve retornar a URL da imagem de avatar do usuário:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}
```
