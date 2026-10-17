---
title: "Laravel Pulse"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Configuração](#configuration)
- [Painel](#dashboard)
    - [Autorização](#dashboard-authorization)
    - [Personalização](#dashboard-customization)
    - [Resolvendo Usuários](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [Capturando Entradas](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtragem](#filtering)
- [Desempenho](#performance)
    - [Usando um Banco de Dados Diferente](#using-a-different-database)
    - [Ingestão via Redis](#ingest)
    - [Amostragem](#sampling)
    - [Limpeza](#trimming)
    - [Tratando Exceções do Pulse](#pulse-exceptions)
- [Cards Personalizados](#custom-cards)
    - [Componentes de Card](#custom-card-components)
    - [Estilização](#custom-card-styling)
    - [Captura e Agregação de Dados](#custom-card-data)

<a id="introduction"></a>
## Introdução

[Laravel Pulse](https://github.com/laravel/pulse) oferece insights rápidos sobre o desempenho e o uso da sua aplicação. Com o Pulse, você pode identificar gargalos como jobs e endpoints lentos, descobrir seus usuários mais ativos, e muito mais.

Para uma depuração detalhada de eventos individuais, confira o [Laravel Telescope](../telescope/).

<a id="installation"></a>
## Instalação

> **Aviso:**
> O armazenamento oficial do Pulse atualmente requer um banco de dados MySQL, MariaDB ou PostgreSQL. Se você estiver usando outro mecanismo de banco de dados, será necessário um banco de dados separado MySQL, MariaDB ou PostgreSQL para os dados do Pulse.

Você pode instalar o Pulse usando o gerenciador de pacotes Composer:

```shell
composer require laravel/pulse
```

Em seguida, você deve publicar os arquivos de configuração e de migração do Pulse usando o comando Artisan `vendor:publish`:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

Por fim, você deve executar o comando `migrate` para criar as tabelas necessárias para armazenar os dados do Pulse:

```shell
php artisan migrate
```

Depois que as migrações de banco de dados do Pulse forem executadas, você poderá acessar o painel do Pulse pela rota `/pulse`.

> **Nota:**
> Se você não quiser armazenar os dados do Pulse no banco de dados principal da sua aplicação, você pode [especificar uma conexão de banco de dados dedicada](#using-a-different-database).

<a id="configuration"></a>
### Configuração

Muitas das opções de configuração do Pulse podem ser controladas por meio de variáveis de ambiente. Para ver as opções disponíveis, registrar novos recorders ou configurar opções avançadas, você pode publicar o arquivo de configuração `config/pulse.php`:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a id="dashboard"></a>
## Painel

<a id="dashboard-authorization"></a>
### Autorização

O painel do Pulse pode ser acessado pela rota `/pulse`. Por padrão, você só conseguirá acessar este painel no ambiente `local`, então será necessário configurar a autorização para os seus ambientes de produção, personalizando o gate de autorização `'viewPulse'`. Você pode fazer isso no arquivo `app/Providers/AppServiceProvider.php` da sua aplicação:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a id="dashboard-customization"></a>
### Personalização

Os cards e o layout do painel do Pulse podem ser configurados publicando a view do painel. A view do painel será publicada em `resources/views/vendor/pulse/dashboard.blade.php`:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

O painel é alimentado pelo [Livewire](https://livewire.laravel.com/) e permite que você personalize os cards e o layout sem precisar recompilar nenhum asset JavaScript.

Dentro deste arquivo, o componente `<x-pulse>` é responsável por renderizar o painel e fornece um layout em grade para os cards. Se você quiser que o painel ocupe toda a largura da tela, pode passar a propriedade `full-width` para o componente:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

Por padrão, o componente `<x-pulse>` criará uma grade de 12 colunas, mas você pode personalizar isso usando a propriedade `cols`:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

Cada card aceita as propriedades `cols` e `rows` para controlar o espaço e o posicionamento:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

A maioria dos cards também aceita a propriedade `expand` para exibir o card completo em vez de usar rolagem:

```blade
<livewire:pulse.slow-queries expand />
```

<a id="dashboard-resolving-users"></a>
### Resolvendo Usuários

Para os cards que exibem informações sobre seus usuários, como o card de Uso da Aplicação, o Pulse registrará apenas o ID do usuário. Ao renderizar o painel, o Pulse resolverá os campos `name` e `email` a partir do seu model `Authenticatable` padrão e exibirá avatares usando o serviço web Gravatar.

Você pode personalizar os campos e o avatar invocando o método `Pulse::user` dentro da classe `App\Providers\AppServiceProvider` da sua aplicação.

O método `user` aceita uma closure que receberá o model `Authenticatable` a ser exibido e deve retornar um array contendo as informações `name`, `extra` e `avatar` do usuário:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> **Nota:**
> Você pode personalizar completamente a forma como o usuário autenticado é capturado e recuperado implementando o contrato `Laravel\Pulse\Contracts\ResolvesUsers` e registrando-o no [container de serviços](../container/#binding-a-singleton) do Laravel.

<a id="dashboard-cards"></a>
### Cards

<a id="servers-card"></a>
#### Servers

O card `<livewire:pulse.servers />` exibe o uso de recursos do sistema para todos os servidores que executam o comando `pulse:check`. Consulte a documentação sobre o [recorder de servers](#servers-recorder) para mais informações sobre o relatório de recursos do sistema.

Se você substituir um servidor na sua infraestrutura, pode querer deixar de exibir o servidor inativo no painel do Pulse após um determinado período. Você pode fazer isso usando a propriedade `ignore-after`, que aceita o número de segundos após o qual os servidores inativos devem ser removidos do painel do Pulse. Como alternativa, você pode fornecer uma string de tempo relativo, como `1 hour` ou `3 days and 1 hour`:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a id="application-usage-card"></a>
#### Application Usage

O card `<livewire:pulse.usage />` exibe os 10 principais usuários que fazem requisições à sua aplicação, despacham jobs e experimentam requisições lentas.

Se você quiser visualizar todas as métricas de uso na tela ao mesmo tempo, pode incluir o card várias vezes e especificar o atributo `type`:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Para aprender como personalizar a forma como o Pulse recupera e exibe as informações dos usuários, consulte nossa documentação sobre [resolvendo usuários](#dashboard-resolving-users).

> **Nota:**
> Se a sua aplicação recebe muitas requisições ou despacha muitos jobs, você pode querer habilitar a [amostragem](#sampling). Consulte a documentação dos recorders [de requisições de usuários](#user-requests-recorder), [de jobs de usuários](#user-jobs-recorder) e [de jobs lentos](#slow-jobs-recorder) para mais informações.

<a id="exceptions-card"></a>
#### Exceptions

O card `<livewire:pulse.exceptions />` mostra a frequência e a recência das exceções que ocorrem na sua aplicação. Por padrão, as exceções são agrupadas com base na classe da exceção e no local onde ela ocorreu. Consulte a documentação do [recorder de exceções](#exceptions-recorder) para mais informações.

<a id="queues-card"></a>
#### Queues

O card `<livewire:pulse.queues />` mostra a vazão das filas da sua aplicação, incluindo a quantidade de jobs enfileirados, em processamento, processados, liberados e com falha. Consulte a documentação do [recorder de filas](#queues-recorder) para mais informações.

<a id="slow-requests-card"></a>
#### Slow Requests

O card `<livewire:pulse.slow-requests />` mostra as requisições recebidas pela sua aplicação que excedem o limite configurado, que é de 1.000ms por padrão. Consulte a documentação do [recorder de requisições lentas](#slow-requests-recorder) para mais informações.

<a id="slow-jobs-card"></a>
#### Slow Jobs

O card `<livewire:pulse.slow-jobs />` mostra os jobs enfileirados na sua aplicação que excedem o limite configurado, que é de 1.000ms por padrão. Consulte a documentação do [recorder de jobs lentos](#slow-jobs-recorder) para mais informações.

<a id="slow-queries-card"></a>
#### Slow Queries

O card `<livewire:pulse.slow-queries />` mostra as consultas ao banco de dados da sua aplicação que excedem o limite configurado, que é de 1.000ms por padrão.

Por padrão, as consultas lentas são agrupadas com base na query SQL (sem os bindings) e no local onde ocorreram, mas você pode optar por não capturar o local se quiser agrupar apenas pela query SQL.

Se você encontrar problemas de desempenho de renderização devido a queries SQL extremamente grandes recebendo destaque de sintaxe, pode desabilitar o destaque adicionando a propriedade `without-highlighting`:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

Consulte a documentação do [recorder de consultas lentas](#slow-queries-recorder) para mais informações.

<a id="slow-outgoing-requests-card"></a>
#### Slow Outgoing Requests

O card `<livewire:pulse.slow-outgoing-requests />` mostra as requisições de saída feitas usando o [cliente HTTP](../http-client/) do Laravel que excedem o limite configurado, que é de 1.000ms por padrão.

Por padrão, as entradas serão agrupadas pela URL completa. No entanto, você pode querer normalizar ou agrupar requisições de saída semelhantes usando expressões regulares. Consulte a documentação do [recorder de requisições de saída lentas](#slow-outgoing-requests-recorder) para mais informações.

<a id="cache-card"></a>
#### Cache

O card `<livewire:pulse.cache />` mostra as estatísticas de acertos e erros de cache da sua aplicação, tanto globais quanto para chaves individuais.

Por padrão, as entradas serão agrupadas por chave. No entanto, você pode querer normalizar ou agrupar chaves semelhantes usando expressões regulares. Consulte a documentação do [recorder de interações com o cache](#cache-interactions-recorder) para mais informações.

<a id="capturing-entries"></a>
## Capturando Entradas

A maioria dos recorders do Pulse captura entradas automaticamente com base em eventos do framework disparados pelo Laravel. No entanto, o [recorder de servers](#servers-recorder) e alguns cards de terceiros precisam consultar informações regularmente. Para usar esses cards, você deve executar o daemon `pulse:check` em todos os seus servidores de aplicação:

```shell
php artisan pulse:check
```

> **Nota:**
> Para manter o processo `pulse:check` em execução permanentemente em segundo plano, você deve usar um monitor de processos como o Supervisor para garantir que o comando não pare de executar.

Como o comando `pulse:check` é um processo de longa duração, ele não verá alterações no seu código sem ser reiniciado. Você deve reiniciar o comando de forma graciosa chamando o comando `pulse:restart` durante o processo de deploy da sua aplicação:

```shell
php artisan pulse:restart
```

> **Nota:**
> O Pulse usa o [cache](../cache/) para armazenar os sinais de reinicialização, então você deve verificar se um driver de cache está configurado corretamente para sua aplicação antes de usar este recurso.

<a id="recorders"></a>
### Recorders

Os recorders são responsáveis por capturar entradas da sua aplicação para serem registradas no banco de dados do Pulse. Os recorders são registrados e configurados na seção `recorders` do [arquivo de configuração do Pulse](#configuration).

<a id="cache-interactions-recorder"></a>
#### Cache Interactions

O recorder `CacheInteractions` captura informações sobre os acertos e erros de [cache](../cache/) que ocorrem na sua aplicação para exibição no card [Cache](#cache-card).

Opcionalmente, você pode ajustar a [taxa de amostragem](#sampling) e os padrões de chaves ignoradas.

Você também pode configurar o agrupamento de chaves para que chaves semelhantes sejam agrupadas como uma única entrada. Por exemplo, você pode querer remover IDs únicos de chaves que armazenam em cache o mesmo tipo de informação. Os grupos são configurados usando uma expressão regular para "encontrar e substituir" partes da chave. Um exemplo está incluído no arquivo de configuração:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

O primeiro padrão que corresponder será utilizado. Se nenhum padrão corresponder, a chave será capturada como está.

<a id="exceptions-recorder"></a>
#### Exceptions

O recorder `Exceptions` captura informações sobre as exceções reportáveis que ocorrem na sua aplicação para exibição no card [Exceptions](#exceptions-card).

Opcionalmente, você pode ajustar a [taxa de amostragem](#sampling) e os padrões de exceções ignoradas. Você também pode configurar se deve capturar o local de onde a exceção se originou. O local capturado será exibido no painel do Pulse, o que pode ajudar a rastrear a origem da exceção; no entanto, se a mesma exceção ocorrer em vários locais, ela aparecerá várias vezes, uma para cada local único.

<a id="queues-recorder"></a>
#### Queues

O recorder `Queues` captura informações sobre as filas da sua aplicação para exibição no card [Queues](#queues-card).

Opcionalmente, você pode ajustar a [taxa de amostragem](#sampling) e os padrões de jobs ignorados.

<a id="slow-jobs-recorder"></a>
#### Slow Jobs

O recorder `SlowJobs` captura informações sobre os jobs lentos que ocorrem na sua aplicação para exibição no card [Slow Jobs](#slow-jobs-recorder).

Opcionalmente, você pode ajustar o limite de job lento, a [taxa de amostragem](#sampling) e os padrões de jobs ignorados.

Você pode ter alguns jobs que espera que demorem mais que outros. Nesses casos, você pode configurar limites por job:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

Se nenhum padrão de expressão regular corresponder ao nome da classe do job, o valor `'default'` será utilizado.

<a id="slow-outgoing-requests-recorder"></a>
#### Slow Outgoing Requests

O recorder `SlowOutgoingRequests` captura informações sobre as requisições HTTP de saída feitas usando o [cliente HTTP](../http-client/) do Laravel que excedem o limite configurado, para exibição no card [Slow Outgoing Requests](#slow-outgoing-requests-card).

Opcionalmente, você pode ajustar o limite de requisição de saída lenta, a [taxa de amostragem](#sampling) e os padrões de URLs ignoradas.

Você pode ter algumas requisições de saída que espera que demorem mais que outras. Nesses casos, você pode configurar limites por requisição:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

Se nenhum padrão de expressão regular corresponder à URL da requisição, o valor `'default'` será utilizado.

Você também pode configurar o agrupamento de URLs para que URLs semelhantes sejam agrupadas como uma única entrada. Por exemplo, você pode querer remover IDs únicos dos caminhos das URLs ou agrupar apenas por domínio. Os grupos são configurados usando uma expressão regular para "encontrar e substituir" partes da URL. Alguns exemplos estão incluídos no arquivo de configuração:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

O primeiro padrão que corresponder será utilizado. Se nenhum padrão corresponder, a URL será capturada como está.

<a id="slow-queries-recorder"></a>
#### Slow Queries

O recorder `SlowQueries` captura quaisquer consultas ao banco de dados da sua aplicação que excedem o limite configurado, para exibição no card [Slow Queries](#slow-queries-card).

Opcionalmente, você pode ajustar o limite de consulta lenta, a [taxa de amostragem](#sampling) e os padrões de consultas ignoradas. Você também pode configurar se deve capturar o local da consulta. O local capturado será exibido no painel do Pulse, o que pode ajudar a rastrear a origem da consulta; no entanto, se a mesma consulta for feita em vários locais, ela aparecerá várias vezes, uma para cada local único.

Você pode ter algumas consultas que espera que demorem mais que outras. Nesses casos, você pode configurar limites por consulta:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

Se nenhum padrão de expressão regular corresponder ao SQL da consulta, o valor `'default'` será utilizado.

<a id="slow-requests-recorder"></a>
#### Slow Requests

O recorder `Requests` captura informações sobre as requisições feitas à sua aplicação para exibição nos cards [Slow Requests](#slow-requests-card) e [Application Usage](#application-usage-card).

Opcionalmente, você pode ajustar o limite de rota lenta, a [taxa de amostragem](#sampling) e os caminhos ignorados.

Você pode ter algumas requisições que espera que demorem mais que outras. Nesses casos, você pode configurar limites por requisição:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

Se nenhum padrão de expressão regular corresponder à URL da requisição, o valor `'default'` será utilizado.

<a id="servers-recorder"></a>
#### Servers

O recorder `Servers` captura o uso de CPU, memória e armazenamento dos servidores que sustentam sua aplicação para exibição no card [Servers](#servers-card). Este recorder requer que o [comando pulse:check](#capturing-entries) esteja em execução em cada um dos servidores que você deseja monitorar.

Cada servidor que relata deve ter um nome único. Por padrão, o Pulse usará o valor retornado pela função `gethostname` do PHP. Se você quiser personalizar isso, pode definir a variável de ambiente `PULSE_SERVER_NAME`:

```env
PULSE_SERVER_NAME=load-balancer
```

O arquivo de configuração do Pulse também permite personalizar os diretórios que são monitorados.

<a id="user-jobs-recorder"></a>
#### User Jobs

O recorder `UserJobs` captura informações sobre os usuários que despacham jobs na sua aplicação para exibição no card [Application Usage](#application-usage-card).

Opcionalmente, você pode ajustar a [taxa de amostragem](#sampling) e os padrões de jobs ignorados.

<a id="user-requests-recorder"></a>
#### User Requests

O recorder `UserRequests` captura informações sobre os usuários que fazem requisições à sua aplicação para exibição no card [Application Usage](#application-usage-card).

Opcionalmente, você pode ajustar a [taxa de amostragem](#sampling) e os padrões de URLs ignoradas.

<a id="filtering"></a>
### Filtragem

Como vimos, muitos [recorders](#recorders) oferecem a possibilidade, por meio de configuração, de "ignorar" entradas recebidas com base no seu valor, como a URL de uma requisição. Mas, às vezes, pode ser útil filtrar registros com base em outros fatores, como o usuário autenticado no momento. Para filtrar esses registros, você pode passar uma closure para o método `filter` do Pulse. Normalmente, o método `filter` deve ser invocado dentro do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a id="performance"></a>
## Desempenho

O Pulse foi projetado para ser adicionado a uma aplicação existente sem exigir nenhuma infraestrutura adicional. No entanto, para aplicações com alto tráfego, há várias formas de remover qualquer impacto que o Pulse possa ter no desempenho da sua aplicação.

<a id="using-a-different-database"></a>
### Usando um Banco de Dados Diferente

Para aplicações com alto tráfego, você pode preferir usar uma conexão de banco de dados dedicada para o Pulse, a fim de evitar impacto no banco de dados da sua aplicação.

Você pode personalizar a [conexão de banco de dados](../database/#configuration) usada pelo Pulse definindo a variável de ambiente `PULSE_DB_CONNECTION`.

```env
PULSE_DB_CONNECTION=pulse
```

<a id="ingest"></a>
### Ingestão via Redis

> **Aviso:**
> A ingestão via Redis requer o Redis 6.2 ou superior e `phpredis` ou `predis` como o driver de cliente Redis configurado na aplicação.

Por padrão, o Pulse armazenará as entradas diretamente na [conexão de banco de dados configurada](#using-a-different-database) após a resposta HTTP ser enviada ao cliente ou um job ser processado. No entanto, você pode usar o driver de ingestão via Redis do Pulse para enviar as entradas para um stream do Redis. Isso pode ser habilitado configurando a variável de ambiente `PULSE_INGEST_DRIVER`:

```ini
PULSE_INGEST_DRIVER=redis
```

Por padrão, o Pulse usará sua [conexão Redis](../redis/#configuration) padrão, mas você pode personalizar isso pela variável de ambiente `PULSE_REDIS_CONNECTION`:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> **Aviso:**
> Ao usar o driver de ingestão via Redis, sua instalação do Pulse deve sempre usar uma conexão Redis diferente da de sua fila baseada em Redis, se aplicável.

Ao usar a ingestão via Redis, você precisará executar o comando `pulse:work` para monitorar o stream e mover as entradas do Redis para as tabelas de banco de dados do Pulse.

```shell
php artisan pulse:work
```

> **Nota:**
> Para manter o processo `pulse:work` em execução permanentemente em segundo plano, você deve usar um monitor de processos como o Supervisor para garantir que o worker do Pulse não pare de executar.

Como o comando `pulse:work` é um processo de longa duração, ele não verá alterações no seu código sem ser reiniciado. Você deve reiniciar o comando de forma graciosa chamando o comando `pulse:restart` durante o processo de deploy da sua aplicação:

```shell
php artisan pulse:restart
```

> **Nota:**
> O Pulse usa o [cache](../cache/) para armazenar os sinais de reinicialização, então você deve verificar se um driver de cache está configurado corretamente para sua aplicação antes de usar este recurso.

<a id="sampling"></a>
### Amostragem

Por padrão, o Pulse capturará todos os eventos relevantes que ocorrem na sua aplicação. Para aplicações com alto tráfego, isso pode resultar na necessidade de agregar milhões de linhas do banco de dados no painel, especialmente para períodos mais longos.

Você pode, em vez disso, optar por habilitar a "amostragem" em determinados recorders de dados do Pulse. Por exemplo, definir a taxa de amostragem como `0.1` no recorder [User Requests](#user-requests-recorder) significará que você registrará apenas aproximadamente 10% das requisições à sua aplicação. No painel, os valores serão escalonados e prefixados com um `~` para indicar que são uma aproximação.

Em geral, quanto mais entradas você tiver para uma determinada métrica, mais baixa você pode definir a taxa de amostragem sem sacrificar muita precisão.

<a id="trimming"></a>
### Limpeza

O Pulse removerá automaticamente as entradas armazenadas assim que elas estiverem fora da janela do painel. A limpeza ocorre durante a ingestão de dados, usando um sistema de sorteio que pode ser personalizado no [arquivo de configuração](#configuration) do Pulse.

<a id="pulse-exceptions"></a>
### Tratando Exceções do Pulse

Se ocorrer uma exceção durante a captura de dados do Pulse, como a impossibilidade de se conectar ao banco de dados de armazenamento, o Pulse falhará silenciosamente para evitar impacto na sua aplicação.

Se você quiser personalizar como essas exceções são tratadas, pode fornecer uma closure ao método `handleExceptionsUsing`:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a id="custom-cards"></a>
## Cards Personalizados

O Pulse permite que você crie cards personalizados para exibir dados relevantes para as necessidades específicas da sua aplicação. O Pulse usa o [Livewire](https://livewire.laravel.com), então você pode querer [consultar a documentação dele](https://livewire.laravel.com/docs) antes de criar seu primeiro card personalizado.

<a id="custom-card-components"></a>
### Componentes de Card

Criar um card personalizado no Laravel Pulse começa estendendo o componente Livewire base `Card` e definindo uma view correspondente:

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

Ao usar o recurso de [carregamento preguiçoso](https://livewire.laravel.com/docs/lazy) do Livewire, o componente `Card` fornecerá automaticamente um placeholder que respeita os atributos `cols` e `rows` passados ao seu componente.

Ao escrever a view correspondente do seu card do Pulse, você pode aproveitar os componentes Blade do Pulse para manter uma aparência e sensação consistentes:

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

As variáveis `$cols`, `$rows`, `$class` e `$expand` devem ser passadas para seus respectivos componentes Blade para que o layout do card possa ser personalizado a partir da view do painel. Você também pode querer incluir o atributo `wire:poll.5s=""` na sua view para que o card seja atualizado automaticamente.

Depois de definir seu componente Livewire e seu template, o card poderá ser incluído na sua [view do painel](#dashboard-customization):

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> **Nota:**
> Se o seu card estiver incluído em um pacote, você precisará registrar o componente no Livewire usando o método `Livewire::component`.

<a id="custom-card-styling"></a>
### Estilização

Se o seu card precisar de estilização adicional além das classes e componentes incluídos no Pulse, há algumas opções para incluir CSS personalizado nos seus cards.

<a id="custom-card-styling-vite"></a>
#### Integração com Vite do Laravel

Se o seu card personalizado estiver dentro da base de código da sua aplicação e você estiver usando a [integração com Vite](../vite/) do Laravel, você pode atualizar o arquivo `vite.config.js` para incluir um ponto de entrada CSS dedicado para o seu card:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

Você pode então usar a diretiva Blade `@vite` na sua [view do painel](#dashboard-customization), especificando o ponto de entrada CSS do seu card:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a id="custom-card-styling-css"></a>
#### Arquivos CSS

Para outros casos de uso, incluindo cards do Pulse contidos em um pacote, você pode instruir o Pulse a carregar folhas de estilo adicionais definindo um método `css` no seu componente Livewire que retorna o caminho do arquivo CSS:

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

Quando este card estiver incluído no painel, o Pulse incluirá automaticamente o conteúdo deste arquivo dentro de uma tag `<style>`, para que ele não precise ser publicado no diretório `public`.

<a id="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Ao usar o Tailwind CSS, você deve criar um ponto de entrada CSS dedicado. O exemplo a seguir exclui os estilos base [Preflight](https://tailwindcss.com/docs/preflight) do Tailwind, que já são incluídos pelo Pulse, e limita o escopo do Tailwind usando um seletor CSS para evitar conflitos com as classes Tailwind do Pulse:

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```

Você também precisará incluir um atributo `id` ou `class` na view do seu card que corresponda ao seletor CSS do seu ponto de entrada:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a id="custom-card-data"></a>
### Captura e Agregação de Dados

Cards personalizados podem buscar e exibir dados de qualquer lugar; no entanto, você pode querer aproveitar o poderoso e eficiente sistema de registro e agregação de dados do Pulse.

<a id="custom-card-data-capture"></a>
#### Capturando Entradas

O Pulse permite que você registre "entradas" usando o método `Pulse::record`:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

O primeiro argumento fornecido ao método `record` é o `type` da entrada que você está registrando, enquanto o segundo argumento é a `key` que determina como os dados agregados devem ser agrupados. Para a maioria dos métodos de agregação, você também precisará especificar um `value` a ser agregado. No exemplo acima, o valor agregado é `$sale->amount`. Você pode então invocar um ou mais métodos de agregação (como `sum`) para que o Pulse possa capturar valores pré-agregados em "buckets" para uma recuperação eficiente posteriormente.

Os métodos de agregação disponíveis são:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> **Nota:**
> Ao criar um pacote de card que captura o ID do usuário autenticado no momento, você deve usar o método `Pulse::resolveAuthenticatedUserId()`, que respeita quaisquer [personalizações do resolvedor de usuários](#dashboard-resolving-users) feitas na aplicação.

<a id="custom-card-data-retrieval"></a>
#### Recuperando Dados Agregados

Ao estender o componente Livewire `Card` do Pulse, você pode usar o método `aggregate` para recuperar dados agregados do período visualizado no painel:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

O método `aggregate` retorna uma coleção de objetos PHP `stdClass`. Cada objeto conterá a propriedade `key` capturada anteriormente, junto com as chaves para cada uma das agregações solicitadas:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

O Pulse recuperará os dados principalmente dos buckets pré-agregados; portanto, as agregações especificadas devem ter sido capturadas antecipadamente usando o método `Pulse::record`. O bucket mais antigo normalmente cairá parcialmente fora do período, então o Pulse agregará as entradas mais antigas para preencher a lacuna e fornecer um valor preciso para todo o período, sem precisar agregar o período inteiro a cada requisição de polling.

Você também pode recuperar um valor total para um determinado tipo usando o método `aggregateTotal`. Por exemplo, o método a seguir recuperaria o total de todas as vendas de usuários em vez de agrupá-las por usuário.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a id="custom-card-displaying-users"></a>
#### Exibindo Usuários

Ao trabalhar com agregações que registram um ID de usuário como chave, você pode resolver as chaves para registros de usuários usando o método `Pulse::resolveUsers`:

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

O método `find` retorna um objeto contendo as chaves `name`, `extra` e `avatar`, que você pode opcionalmente passar diretamente para o componente Blade `<x-pulse::user-card>`:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a id="custom-recorders"></a>
#### Recorders Personalizados

Autores de pacotes podem querer fornecer classes de recorder para permitir que os usuários configurem a captura de dados.

Os recorders são registrados na seção `recorders` do arquivo de configuração `config/pulse.php` da aplicação:

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

Os recorders podem escutar eventos especificando uma propriedade `$listen`. O Pulse registrará automaticamente os listeners e chamará o método `record` do recorder:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```
