---
title: "Guia de Atualização"
---

- [Atualizando para o 13.0 a partir do 12.x](#upgrade-13.0)
    - [Atualizando Usando IA](#upgrading-using-ai)

<a id="high-impact-changes"></a>
## Mudanças de Alto Impacto

<div class="content-list" markdown="1">

- [Atualizando as Dependências](#updating-dependencies)
- [Atualizando o Instalador do Laravel](#updating-the-laravel-installer)
- [Proteção Contra Falsificação de Requisições](#request-forgery-protection)

</div>

<a id="medium-impact-changes"></a>
## Mudanças de Impacto Médio

<div class="content-list" markdown="1">

- [Configuração `serializable_classes` do Cache](#cache-serializable_classes-configuration)
- [`upsert` do Database Com MySQL ou MariaDB](#database-upsert-mariadb-mysql)

</div>

<a id="low-impact-changes"></a>
## Mudanças de Baixo Impacto

<div class="content-list" markdown="1">

- [Prefixos de Cache e Nomes de Cookies de Sessão](#cache-prefixes-and-session-cookie-names)
- [A Serialização de Models em Collections Restaura Relações Carregadas Antecipadamente](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` e Valores Padrão de Classe Nullable](#containercall-and-nullable-class-defaults)
- [Precedência no Registro de Rotas de Domínio](#domain-route-registration-precedence)
- [Payload de Exceção do Evento `JobAttempted`](#jobattempted-event-exception-payload)
- [Vinculação do Callback `extend` de Managers](#manager-extend-callback-binding)
- [Queries `DELETE` do MySQL Com `JOIN`, `ORDER BY` e `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [Nomes de Views de Paginação Bootstrap](#pagination-bootstrap-view-names)
- [Geração de Nomes de Tabelas Pivot Polimórficas](#polymorphic-pivot-table-name-generation)
- [Renomeação de Propriedade do Evento `QueueBusy`](#queuebusy-event-property-rename)
- [Configuração `serialization` da Sessão](#session-serialization-configuration)
- [Fábricas `Str` São Resetadas Entre Testes](#str-factories-reset-between-tests)

</div>

<a id="upgrade-13.0"></a>
## Atualizando para o 13.0 a partir do 12.x

#### Tempo Estimado de Atualização: 10 Minutos

> **Nota:**
> Tentamos documentar todas as possíveis mudanças que quebram compatibilidade. Como algumas dessas mudanças estão em partes obscuras do framework, apenas uma parte delas pode afetar sua aplicação. Para economizar tempo, você pode usar o [Shift](https://laravelshift.com). O Shift é um serviço mantido pela comunidade que automatiza atualizações do Laravel.

<a id="upgrading-using-ai"></a>
### Atualizando Usando IA

Você pode automatizar sua atualização usando o [Laravel Boost](https://github.com/laravel/boost). O Boost é um servidor MCP oficial que fornece ao seu assistente de IA prompts guiados de atualização. Depois de instalado em qualquer aplicação Laravel 12, use o comando slash `/upgrade-laravel-v13` no Claude Code, Cursor, OpenCode, Gemini ou VS Code para iniciar a atualização para o Laravel 13. Este comando requer o Laravel Boost `^2.0`.

<a id="updating-dependencies"></a>
### Atualizando as Dependências

**Probabilidade de Impacto: Alta**

Você deve atualizar as seguintes dependências no arquivo `composer.json` da sua aplicação:

<div class="content-list" markdown="1">

- `laravel/framework` para `^13.0`
- `laravel/boost` para `^2.0`
- `laravel/tinker` para `^3.0`
- `phpunit/phpunit` para `^12.0`
- `pestphp/pest` para `^4.0`

</div>

<a id="updating-the-laravel-installer"></a>
### Atualizando o Instalador do Laravel

Se você usa a ferramenta CLI do instalador do Laravel para criar novas aplicações Laravel, deve atualizar sua instalação do instalador para compatibilidade com o Laravel 13.x.

Se você instalou o instalador do Laravel via `composer global require`, pode atualizá-lo usando `composer global update`:

```shell
composer global update laravel/installer
```

Ou, se você usa a cópia do instalador do Laravel incluída no [Laravel Herd](https://herd.laravel.com), deve atualizar sua instalação do Herd para a versão mais recente.

<a id="cache"></a>
### Cache

<a id="cache-prefixes-and-session-cookie-names"></a>
#### Prefixos de Cache e Nomes de Cookies de Sessão

**Probabilidade de Impacto: Baixa**

Os prefixos padrão de cache e de chaves do Redis do Laravel agora usam sufixos com hífen.

Na maioria das aplicações, esta mudança não se aplica, pois os arquivos de configuração da aplicação já definem esses valores. Isso afeta principalmente aplicações que dependem da configuração de fallback no nível do framework quando os valores de configuração correspondentes da aplicação não estão presentes.

Se sua aplicação depende desses padrões gerados, as chaves de cache e os nomes dos cookies de sessão podem mudar após a atualização:

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';
```

Para manter o comportamento anterior, configure explicitamente `CACHE_PREFIX`, `REDIS_PREFIX` e `SESSION_COOKIE` no seu ambiente.

<a id="store-and-repository-contracts-touch"></a>
#### Contratos `Store` e `Repository`: `touch`

**Probabilidade de Impacto: Muito Baixa**

Os contratos de cache agora incluem um método `touch` para estender os TTLs dos itens. Se você mantém implementações personalizadas de store de cache, deve adicionar este método:

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a id="cache-serializable_classes-configuration"></a>
#### Configuração `serializable_classes` do Cache

**Probabilidade de Impacto: Média**

A configuração padrão `cache` da aplicação agora inclui a opção `serializable_classes` definida como `false`. Isso reforça o comportamento de desserialização do cache para ajudar a prevenir ataques de cadeia de gadgets de desserialização do PHP caso o `APP_KEY` da sua aplicação seja vazado. Se a sua aplicação armazena intencionalmente objetos PHP no cache, você deve listar explicitamente as classes que podem ser desserializadas:

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

Se sua aplicação dependia anteriormente da desserialização de objetos arbitrários em cache, você precisará migrar esse uso para listas de permissão explícitas de classes ou para payloads de cache que não sejam objetos (como arrays).

<a id="container"></a>
### Container

<a id="containercall-and-nullable-class-defaults"></a>
#### `Container::call` e Valores Padrão de Classe Nullable

**Probabilidade de Impacto: Baixa**

`Container::call` agora respeita valores padrão de parâmetros de classe nullable quando não existe binding, equiparando-se ao comportamento de injeção no construtor introduzido no Laravel 12:

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

Se a sua lógica de injeção em chamadas de método dependia do comportamento anterior, pode ser necessário atualizá-la.

<a id="contracts"></a>
### Contratos

<a id="dispatcher-contract-dispatchafterresponse"></a>
#### Contrato `Dispatcher`: `dispatchAfterResponse`

**Probabilidade de Impacto: Muito Baixa**

O contrato `Illuminate\Contracts\Bus\Dispatcher` agora inclui o método `dispatchAfterResponse($command, $handler = null)`.

Se você mantém uma implementação personalizada de dispatcher, adicione este método à sua classe.

<a id="responsefactory-contract-eventstream"></a>
#### Contrato `ResponseFactory`: `eventStream`

**Probabilidade de Impacto: Muito Baixa**

O contrato `Illuminate\Contracts\Routing\ResponseFactory` agora inclui uma assinatura `eventStream`.

Se você mantém uma implementação personalizada deste contrato, deve adicionar este método.

<a id="mustverifyemail-contract-markemailasunverified"></a>
#### Contrato `MustVerifyEmail`: `markEmailAsUnverified`

**Probabilidade de Impacto: Muito Baixa**

O contrato `Illuminate\Contracts\Auth\MustVerifyEmail` agora inclui `markEmailAsUnverified()`.

Se você fornece uma implementação personalizada deste contrato, adicione este método para manter a compatibilidade.

<a id="database"></a>
### Database

<a id="database-upsert-mariadb-mysql"></a>
#### `upsert` do Database Com MySQL ou MariaDB

**Probabilidade de Impacto: Média**

O Laravel agora valida se quem chama o método fornece um valor não vazio para `uniqueBy`, e lançará uma `InvalidArgumentException` em vez de gerar SQL inválido.

Embora os drivers de banco de dados MariaDB e MySQL ignorem o valor de `uniqueBy` e sempre usem os índices primários e únicos da tabela para detectar registros existentes, a validação ainda se aplica. Uma `InvalidArgumentException` será lançada se `uniqueBy` estiver vazio.

<a id="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### Queries `DELETE` do MySQL Com `JOIN`, `ORDER BY` e `LIMIT`

**Probabilidade de Impacto: Baixa**

O Laravel agora compila queries `DELETE ... JOIN` completas, incluindo `ORDER BY` e `LIMIT`, para a gramática do MySQL.

Em versões anteriores, as cláusulas `ORDER BY` / `LIMIT` podiam ser silenciosamente ignoradas em deletes com join. No Laravel 13, essas cláusulas são incluídas no SQL gerado. Como resultado, mecanismos de banco de dados que não suportam essa sintaxe (MySQL, e MariaDB anterior à 11.8.1) agora podem lançar uma `QueryException` em vez de executar um delete sem limite.

<a id="eloquent"></a>
### Eloquent

<a id="model-booting-and-nested-instantiation"></a>
#### Inicialização de Models e Instanciação Aninhada

**Probabilidade de Impacto: Muito Baixa**

Criar uma nova instância de model enquanto esse model ainda está sendo inicializado agora é proibido e lança uma `LogicException`.

Isso afeta código que instancia models dentro de métodos `boot` de models ou de métodos `boot*` de traits:

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

Mova esta lógica para fora do ciclo de inicialização para evitar a inicialização aninhada.

<a id="polymorphic-pivot-table-name-generation"></a>
#### Geração de Nomes de Tabelas Pivot Polimórficas

**Probabilidade de Impacto: Baixa**

Quando nomes de tabelas são inferidos para models pivot polimórficos usando classes de model pivot personalizadas, o Laravel agora gera nomes no plural.

Se sua aplicação dependia dos nomes inferidos anteriores no singular para tabelas pivot polimórficas e usava classes pivot personalizadas, você deve definir explicitamente o nome da tabela no seu model pivot.

<a id="collection-model-serialization-restores-eager-loaded-relations"></a>
#### A Serialização de Models em Collections Restaura Relações Carregadas Antecipadamente

**Probabilidade de Impacto: Baixa**

Quando collections de models Eloquent são serializadas e restauradas (como em jobs na fila), as relações carregadas antecipadamente agora são restauradas para os models da collection.

Se o seu código dependia de relações não estarem presentes após a desserialização, pode ser necessário ajustar essa lógica.

<a id="http-client"></a>
### Cliente HTTP

<a id="http-client-response-throw-and-throwif-signatures"></a>
#### Assinaturas de `Response::throw` e `throwIf` do Cliente HTTP

**Probabilidade de Impacto: Muito Baixa**

Os métodos de response do cliente HTTP agora declaram seus parâmetros de callback nas assinaturas dos métodos:

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

Se você sobrescreve esses métodos em classes de response personalizadas, certifique-se de que suas assinaturas de método sejam compatíveis.

<a id="notifications"></a>
### Notificações

<a id="default-password-reset-subject"></a>
#### Assunto Padrão de Redefinição de Senha

**Probabilidade de Impacto: Muito Baixa**

O assunto padrão do e-mail de redefinição de senha do Laravel foi alterado:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

Se seus testes, asserções ou sobrescritas de tradução dependem da string padrão anterior, atualize-os de acordo.

<a id="queued-notifications-and-missing-models"></a>
#### Notificações na Fila e Models Ausentes

**Probabilidade de Impacto: Muito Baixa**

Notificações na fila agora respeitam o atributo `#[DeleteWhenMissingModels]` e a propriedade `$deleteWhenMissingModels` definidos na classe da notificação.

Em versões anteriores, models ausentes ainda podiam fazer com que jobs de notificação na fila falhassem em casos em que você esperava que fossem excluídos.

<a id="queue"></a>
### Fila

<a id="jobattempted-event-exception-payload"></a>
#### Payload de Exceção do Evento `JobAttempted`

**Probabilidade de Impacto: Baixa**

O evento `Illuminate\Queue\Events\JobAttempted` agora expõe o objeto de exceção (ou `null`) via `$exception`, substituindo a antiga propriedade booleana `$exceptionOccurred`:

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

Se você escuta este evento, atualize o código do seu listener de acordo.

<a id="queuebusy-event-property-rename"></a>
#### Renomeação de Propriedade do Evento `QueueBusy`

**Probabilidade de Impacto: Baixa**

A propriedade `$connection` do evento `Illuminate\Queue\Events\QueueBusy` foi renomeada para `$connectionName`, para manter consistência com os demais eventos de fila.

Se seus listeners referenciam `$connection`, atualize-os para `$connectionName`.

<a id="queue-contract-method-additions"></a>
#### Novos Métodos do Contrato `Queue`

**Probabilidade de Impacto: Muito Baixa**

O contrato `Illuminate\Contracts\Queue\Queue` agora inclui métodos de inspeção de tamanho de fila que antes eram declarados apenas em docblocks.

Se você mantém implementações personalizadas de driver de fila deste contrato, adicione implementações para:

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a id="routing"></a>
### Roteamento

<a id="domain-route-registration-precedence"></a>
#### Precedência no Registro de Rotas de Domínio

**Probabilidade de Impacto: Baixa**

Rotas com um domínio explícito agora são priorizadas antes das rotas sem domínio na correspondência de rotas.

Isso permite que rotas catch-all de subdomínio se comportem de forma consistente mesmo quando rotas sem domínio foram registradas antes. Se sua aplicação dependia da precedência de registro anterior entre rotas com e sem domínio, revise o comportamento de correspondência de rotas.

<a id="session"></a>
### Sessão

<a id="session-serialization-configuration"></a>
#### Configuração `serialization` da Sessão

**Probabilidade de Impacto: Baixa**

Para ajudar a prevenir ataques de cadeia de gadgets de desserialização do PHP, o esqueleto padrão da aplicação agora define a opção `serialization` da sessão como `json` no arquivo `config/session.php`.

Se você está atualizando uma aplicação existente e sincronizando seus arquivos de configuração com o esqueleto do Laravel 13, alterar este valor de `php` para `json` invalidará todas as sessões de usuário ativas.

Se você deseja manter as sessões ativas de forma contínua durante a atualização, deve garantir que este valor continue definido como `php`. No entanto, se a sua aplicação não armazena objetos PHP na sessão e você está confortável em exigir que seus usuários façam login novamente, recomendamos alterar este valor para `json` para melhor segurança.

<a id="scheduling"></a>
### Agendamento

<a id="withscheduling-registration-timing"></a>
#### Momento de Registro do `withScheduling`

**Probabilidade de Impacto: Muito Baixa**

Agendamentos registrados via `ApplicationBuilder::withScheduling()` agora são adiados até que `Schedule` seja resolvido.

Se a sua aplicação dependia do momento de registro imediato dos agendamentos durante o bootstrap, pode ser necessário ajustar essa lógica.

<a id="security"></a>
### Segurança

<a id="request-forgery-protection"></a>
#### Proteção Contra Falsificação de Requisições

**Probabilidade de Impacto: Alta**

O middleware CSRF do Laravel foi renomeado de `VerifyCsrfToken` para `PreventRequestForgery`, e agora inclui verificação da origem da requisição usando o cabeçalho `Sec-Fetch-Site`.

`VerifyCsrfToken` e `ValidateCsrfToken` permanecem como aliases obsoletos, mas as referências diretas devem ser atualizadas para `PreventRequestForgery`, especialmente ao excluir middlewares em testes ou definições de rotas:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

A API de configuração de middleware agora também disponibiliza `preventRequestForgery(...)`.

<a id="support"></a>
### Suporte

<a id="manager-extend-callback-binding"></a>
#### Vinculação do Callback `extend` de Managers

**Probabilidade de Impacto: Baixa**

Closures de drivers personalizados registradas via métodos `extend` de managers agora são vinculadas à instância do manager.

Se você dependia anteriormente de outro objeto vinculado (como uma instância de service provider) como `$this` dentro dessas callbacks, deve mover esses valores para capturas de closure usando `use (...)`.

<a id="str-factories-reset-between-tests"></a>
#### Fábricas `Str` São Resetadas Entre Testes

**Probabilidade de Impacto: Baixa**

O Laravel agora reseta fábricas `Str` personalizadas durante o teardown dos testes.

Se seus testes dependiam de fábricas personalizadas de UUID / ULID / strings aleatórias persistirem entre métodos de teste, você deve defini-las em cada teste relevante ou no hook de setup.

<a id="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from` Usa Unicode Sem Escape Por Padrão

**Probabilidade de Impacto: Muito Baixa**

`Illuminate\Support\Js::from` agora usa `JSON_UNESCAPED_UNICODE` por padrão.

Se suas comparações de testes ou de saída do frontend dependiam de sequências Unicode escapadas (por exemplo `\u00e8`), atualize suas expectativas.

<a id="utilities"></a>
### Utilitários

<a id="symfony-polyfill"></a>
#### Polyfill do Symfony para PHP 8.5 e Conflitos de Funções Globais

**Probabilidade de Impacto: Baixa**

O Laravel 13 introduz uma dependência de `symfony/polyfill-php85`. Em versões do PHP abaixo de 8.5, este polyfill define funções globais como `array_first()` e `array_last()`, a menos que já tenham sido definidas antes durante o bootstrap.

Essas funções podem entrar em conflito com pacotes de helpers legados como `laravel/helpers` ou com helpers globais personalizados que usam os mesmos nomes. Por exemplo, o helper histórico `array_first()` aceitava um callback para retornar o primeiro elemento correspondente, enquanto a versão do polyfill retorna apenas o primeiro elemento do array.

Para evitar conflitos e garantir um comportamento consistente entre versões do PHP, você deve preferir os métodos de `Illuminate\Support\Arr`:

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a id="views"></a>
### Views

<a id="pagination-bootstrap-view-names"></a>
#### Nomes de Views de Paginação Bootstrap

**Probabilidade de Impacto: Baixa**

Os nomes internos das views de paginação para os padrões do Bootstrap 3 agora são explícitos:

```text
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

Se sua aplicação referencia diretamente os nomes antigos das views de paginação, atualize essas referências.

<a id="miscellaneous"></a>
### Diversos

Também recomendamos que você veja as mudanças no [repositório GitHub](https://github.com/laravel/laravel) `laravel/laravel`. Embora muitas dessas mudanças não sejam obrigatórias, você pode querer manter esses arquivos sincronizados com sua aplicação. Algumas dessas mudanças serão abordadas neste guia de atualização, mas outras, como mudanças em arquivos de configuração ou comentários, não serão. Você pode visualizar as mudanças facilmente com a [ferramenta de comparação do GitHub](https://github.com/laravel/laravel/compare/12.x...13.x) e escolher quais atualizações são importantes para você.
