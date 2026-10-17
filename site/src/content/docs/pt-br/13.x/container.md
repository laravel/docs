---
title: "Container de Serviço"
---

- [Introdução](#introduction)
    - [Resolução com Zero Configuração](#zero-configuration-resolution)
    - [Quando Utilizar o Container](#when-to-use-the-container)
- [Binding](#binding)
    - [Fundamentos de Binding](#binding-basics)
    - [Vinculando Interfaces a Implementações](#binding-interfaces-to-implementations)
    - [Binding Contextual](#contextual-binding)
    - [Atributos Contextuais](#contextual-attributes)
    - [Vinculando Primitivos](#binding-primitives)
    - [Vinculando Variadics Tipados](#binding-typed-variadics)
    - [Tagging](#tagging)
    - [Estendendo Bindings](#extending-bindings)
- [Resolução](#resolving)
    - [O Método Make](#the-make-method)
    - [Injeção Automática](#automatic-injection)
- [Invocação e Injeção de Métodos](#method-invocation-and-injection)
- [Eventos do Container](#container-events)
    - [Rebinding](#rebinding)
- [PSR-11](#psr-11)

<a id="introduction"></a>
## Introdução

O container de serviço do Laravel é uma ferramenta poderosa para gerenciar dependências de classes e realizar injeção de dependência. Injeção de dependência é uma frase sofisticada que essencialmente significa isso: dependências de classes são "injetadas" na classe via o construtor ou, em alguns casos, métodos "setter".

Vejamos um exemplo simples:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

Neste exemplo, o `PodcastController` precisa recuperar podcasts de uma fonte de dados como Apple Music. Então, vamos **injetar** um serviço capaz de recuperar podcasts. Como o serviço é injetado, somos capazes de facilmente "mockar", ou criar uma implementação fictícia do serviço `AppleMusic` ao testar nossa aplicação.

Um entendimento profundo do container de serviço do Laravel é essencial para construir uma aplicação poderosa e grande, bem como para contribuir com o próprio núcleo do Laravel.

<a id="zero-configuration-resolution"></a>
### Resolução com Zero Configuração

Se uma classe não tem dependências ou depende apenas de outras classes concretas (não interfaces), o container não precisa ser instruído sobre como resolver essa classe. Por exemplo, você pode colocar o seguinte código em seu arquivo `routes/web.php`:

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    dd($service::class);
});
```

Neste exemplo, acessar a rota `/` da sua aplicação resolverá automaticamente a classe `Service` e a injetará no handler da sua rota. Isso é revolucionário. Significa que você pode desenvolver sua aplicação e aproveitar a injeção de dependência sem se preocupar com arquivos de configuração inchados.

Felizmente, muitas das classes que você estará escrevendo ao construir uma aplicação Laravel recebem automaticamente suas dependências via o container, incluindo [controllers](../controllers/), [ouvintes de eventos](../events/), [middleware](../middleware/), e mais. Além disso, você pode usar type-hint de dependências no método `handle` de [jobs enfileirados](../queues/). Uma vez que você experimenta o poder da injeção de dependência automática e com zero configuração, parece impossível desenvolver sem ela.

<a id="when-to-use-the-container"></a>
### Quando Utilizar o Container

Graças à resolução com zero configuração, você frequentemente usará type-hint de dependências em rotas, controllers, ouvintes de eventos e em outros lugares sem nunca interagir manualmente com o container. Por exemplo, você pode usar type-hint do objeto `Illuminate\Http\Request` na definição da sua rota para que você possa acessar facilmente a requisição atual. Embora nunca tenhamos que interagir com o container para escrever este código, ele está gerenciando a injeção dessas dependências nos bastidores:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

Em muitos casos, graças à injeção de dependência automática e [facades](../facades/), você pode construir aplicações Laravel sem **nunca** vincular ou resolver manualmente qualquer coisa do container. **Então, quando você interagiria manualmente com o container?** Vamos examinar duas situações.

Primeiro, se você escreve uma classe que implementa uma interface e deseja usar type-hint dessa interface em uma rota ou construtor de classe, você deve [dizer ao container como resolver essa interface](#binding-interfaces-to-implementations). Em segundo lugar, se você está [escrevendo um pacote Laravel](../packages/) que planeja compartilhar com outros desenvolvedores Laravel, você pode precisar vincular os serviços do seu pacote ao container.

<a id="binding"></a>
## Binding

<a id="binding-basics"></a>
### Fundamentos de Binding

<a id="simple-bindings"></a>
#### Bindings Simples

Quase todos os seus bindings do container de serviço serão registrados dentro de [provedores de serviço](../providers/), então a maioria desses exemplos demonstrará o uso do container nesse contexto.

Dentro de um provedor de serviço, você sempre tem acesso ao container via a propriedade `$this->app`. Podemos registrar um binding usando o método `bind`, passando o nome da classe ou interface que desejamos registrar junto com um closure que retorne uma instância da classe:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Note que recebemos o próprio container como um argumento para o resolvedor. Podemos então usar o container para resolver subdependências do objeto que estamos construindo.

Como mencionado, você normalmente estará interagindo com o container dentro de provedores de serviço; no entanto, se você gostaria de interagir com o container fora de um provedor de serviço, você pode fazer isso via a [facade](../facades/) `App`:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

Você pode usar o método `bindIf` para registrar um binding no container apenas se um binding ainda não tiver sido registrado para o tipo fornecido:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Para conveniência, você pode omitir fornecer o nome da classe ou interface que deseja registrar como um argumento separado e, em vez disso, permitir que o Laravel infira o tipo a partir do tipo de retorno do closure que você fornece ao método `bind`:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> **Nota:**
> Não há necessidade de vincular classes ao container se elas não dependem de nenhuma interface. O container não precisa ser instruído sobre como construir esses objetos, já que pode resolvê-los automaticamente usando reflexão.

<a id="binding-a-singleton"></a>
#### Vinculando um Singleton

O método `singleton` vincula uma classe ou interface ao container que deve ser resolvida apenas uma vez. Uma vez que um binding singleton seja resolvido, a mesma instância do objeto será retornada em chamadas subsequentes ao container:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Você pode usar o método `singletonIf` para registrar um binding singleton no container apenas se um binding ainda não tiver sido registrado para o tipo fornecido:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a id="singleton-attribute"></a>
#### Atributo Singleton

Alternativamente, você pode marcar uma interface ou classe com o atributo `#[Singleton]` para indicar ao container que ela deve ser resolvida apenas uma vez:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Singleton;

#[Singleton]
class Transistor
{
    // ...
}
```

<a id="binding-scoped"></a>
#### Vinculando Singletons com Escopo

O método `scoped` vincula uma classe ou interface ao container que deve ser resolvida apenas uma vez dentro de um determinado ciclo de vida de requisição / job do Laravel. Embora este método seja semelhante ao método `singleton`, instâncias registradas usando o método `scoped` serão limpas sempre que a aplicação Laravel iniciar um novo "ciclo de vida", como quando um worker do [Laravel Octane](../octane/) processa uma nova requisição ou quando um [worker de fila](../queues/) do Laravel processa um novo job:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

Você pode usar o método `scopedIf` para registrar um binding com escopo no container apenas se um binding ainda não tiver sido registrado para o tipo fornecido:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a id="scoped-attribute"></a>
#### Atributo Scoped

Alternativamente, você pode marcar uma interface ou classe com o atributo `#[Scoped]` para indicar ao container que ela deve ser resolvida apenas uma vez dentro de um determinado ciclo de vida de requisição / job do Laravel:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Scoped;

#[Scoped]
class Transistor
{
    // ...
}
```

<a id="binding-instances"></a>
#### Vinculando Instâncias

Você também pode vincular uma instância de objeto existente ao container usando o método `instance`. A instância fornecida será sempre retornada em chamadas subsequentes ao container:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a id="binding-interfaces-to-implementations"></a>
### Vinculando Interfaces a Implementações

Um recurso muito poderoso do container de serviço é sua capacidade de vincular uma interface a uma determinada implementação. Por exemplo, vamos supor que temos uma interface `EventPusher` e uma implementação `RedisEventPusher`. Uma vez que tenhamos codificado nossa implementação `RedisEventPusher` dessa interface, podemos registrá-la com o container de serviço assim:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

Esta instrução diz ao container que ele deve injetar o `RedisEventPusher` quando uma classe precisar de uma implementação de `EventPusher`. Agora podemos usar type-hint da interface `EventPusher` no construtor de uma classe que é resolvida pelo container. Lembre-se, controllers, ouvintes de eventos, middleware e vários outros tipos de classes dentro de aplicações Laravel são sempre resolvidos usando o container:

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a id="bind-attribute"></a>
#### Atributo Bind

O Laravel também fornece um atributo `Bind` para maior conveniência. Você pode aplicar este atributo a qualquer interface para dizer ao Laravel qual implementação deve ser injetada automaticamente sempre que essa interface for solicitada. Ao usar o atributo `Bind`, não há necessidade de realizar nenhum registro de serviço adicional nos provedores de serviço da sua aplicação.

Além disso, múltiplos atributos `Bind` podem ser colocados em uma interface para configurar uma implementação diferente que deve ser injetada para um determinado conjunto de ambientes:

```php
<?php

namespace App\Contracts;

use App\Services\FakeEventPusher;
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;

#[Bind(RedisEventPusher::class)]
#[Bind(FakeEventPusher::class, environments: ['local', 'testing'])]
interface EventPusher
{
    // ...
}
```

Além disso, atributos [Singleton](#singleton-attribute) e [Scoped](#scoped-attribute) podem ser aplicados para indicar se os bindings do container devem ser resolvidos uma vez ou uma vez por requisição / ciclo de vida de job:

```php
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;
use Illuminate\Container\Attributes\Singleton;

#[Bind(RedisEventPusher::class)]
#[Singleton]
interface EventPusher
{
    // ...
}
```

Para bindings que dependem de uma condição arbitrária, você pode usar o atributo `BindWhen`. O closure pode receber o container e deve retornar `true` quando o binding deve ser aplicado. Os atributos `Bind` e `BindWhen` são avaliados na ordem em que são declarados:

```php
use App\Services\BetaEventPusher;
use Illuminate\Container\Attributes\BindWhen;
use Laravel\Pennant\Feature;

#[BindWhen(BetaEventPusher::class, static fn () => Feature::active('beta-events'))]
interface EventPusher
{
    // ...
}
```

> **Nota:**
> O atributo `BindWhen` requer PHP 8.5 ou superior.

<a id="contextual-binding"></a>
### Binding Contextual

Às vezes, você pode ter duas classes que utilizam a mesma interface, mas deseja injetar implementações diferentes em cada classe. Por exemplo, dois controllers podem depender de diferentes implementações do [contrato](../contracts/) `Illuminate\Contracts\Filesystem\Filesystem`. O Laravel fornece uma interface simples e fluida para definir esse comportamento:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\UploadController;
use App\Http\Controllers\VideoController;
use Illuminate\Contracts\Filesystem\Filesystem;
use Illuminate\Support\Facades\Storage;

$this->app->when(PhotoController::class)
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('local');
    });

$this->app->when([VideoController::class, UploadController::class])
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('s3');
    });
```

<a id="contextual-attributes"></a>
### Atributos Contextuais

Como o binding contextual é frequentemente usado para injetar implementações de drivers ou valores de configuração, o Laravel oferece uma variedade de atributos de binding contextual que permitem injetar esses tipos de valores sem definir manualmente os bindings contextuais nos seus provedores de serviço.

Por exemplo, o atributo `Storage` pode ser usado para injetar um [disco de armazenamento](../filesystem/) específico:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    ) {
        // ...
    }
}
```

Além do atributo `Storage`, o Laravel oferece atributos `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RequestAttribute`, `RouteParameter` e [Tag](#tagging):

```php
<?php

namespace App\Http\Controllers;

use App\Contracts\UserRepository;
use App\Models\Organization;
use App\Models\Photo;
use App\Repositories\DatabaseRepository;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
use Illuminate\Container\Attributes\DB;
use Illuminate\Container\Attributes\Give;
use Illuminate\Container\Attributes\Log;
use Illuminate\Container\Attributes\RequestAttribute;
use Illuminate\Container\Attributes\RouteParameter;
use Illuminate\Container\Attributes\Tag;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Database\Connection;
use Psr\Log\LoggerInterface;

class PhotoController extends Controller
{
    public function __construct(
        #[Auth('web')] protected Guard $auth,
        #[Cache('redis')] protected Repository $cache,
        #[Config('app.timezone')] protected string $timezone,
        #[Context('uuid')] protected string $uuid,
        #[Context('ulid', hidden: true)] protected string $ulid,
        #[DB('mysql')] protected Connection $connection,
        #[Give(DatabaseRepository::class)] protected UserRepository $users,
        #[Log('daily')] protected LoggerInterface $log,
        #[RequestAttribute('organization')] protected Organization $organization,
        #[RouteParameter] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

O atributo `RouteParameter` resolverá o parâmetro da rota correspondente ao nome da variável. Se necessário, você pode especificar o nome do parâmetro da rota explicitamente: `#[RouteParameter('photo')]`.

O atributo `RequestAttribute` resolverá o valor armazenado sob a chave fornecida no [saco de atributos](https://symfony.com/doc/current/components/http_foundation.html#accessing-request-data) da requisição atual: `#[RequestAttribute('organization')]`.

Além disso, o Laravel fornece um atributo `CurrentUser` para injetar o usuário atualmente autenticado em uma determinada rota ou classe:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a id="defining-custom-attributes"></a>
#### Definindo Atributos Personalizados

Você pode criar seus próprios atributos contextuais implementando o contrato `Illuminate\Contracts\Container\ContextualAttribute`. O container chamará o método `resolve` do seu atributo, que deve resolver o valor que deve ser injetado na classe que utiliza o atributo. No exemplo abaixo, vamos reimplementar o atributo `Config` integrado do Laravel:

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;
use ReflectionParameter;

#[Attribute(Attribute::TARGET_PARAMETER)]
class Config implements ContextualAttribute
{
    /**
     * Create a new attribute instance.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * Resolve the configuration value.
     *
     * @param  self  $attribute
     * @param  \Illuminate\Contracts\Container\Container  $container
     * @param  \ReflectionParameter  $parameter
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container, ReflectionParameter $parameter)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```

<a id="binding-primitives"></a>
### Vinculando Primitivos

Às vezes, você pode ter uma classe que recebe algumas classes injetadas, mas também precisa de um valor primitivo injetado, como um inteiro. Você pode facilmente usar binding contextual para injetar qualquer valor que sua classe precise:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

Às vezes, uma classe pode depender de um array de instâncias [etiquetadas](#tagging). Usando o método `giveTagged`, você pode facilmente injetar todos os bindings do container com essa tag:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

Se você precisar injetar um valor de um dos arquivos de configuração da sua aplicação, você pode usar o método `giveConfig`:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a id="binding-typed-variadics"></a>
### Vinculando Variadics Tipados

Ocasionalmente, você pode ter uma classe que recebe um array de objetos tipados usando um argumento variádico no construtor:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * The filter instances.
     *
     * @var array
     */
    protected $filters;

    /**
     * Create a new class instance.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

Usando binding contextual, você pode resolver essa dependência fornecendo ao método `give` um closure que retorne um array de instâncias resolvidas de `Filter`:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give(function (Application $app) {
          return [
              $app->make(NullFilter::class),
              $app->make(ProfanityFilter::class),
              $app->make(TooLongFilter::class),
          ];
    });
```

Para conveniência, você também pode apenas fornecer um array de nomes de classes para serem resolvidas pelo container sempre que `Firewall` precisar de instâncias de `Filter`:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give([
        NullFilter::class,
        ProfanityFilter::class,
        TooLongFilter::class,
    ]);
```

<a id="variadic-tag-dependencies"></a>
#### Dependências Variádicas com Tag

Às vezes, uma classe pode ter uma dependência variádica que é tipada como uma determinada classe (`Report ...$reports`). Usando os métodos `needs` e `giveTagged`, você pode facilmente injetar todos os bindings do container com essa [tag](#tagging) para a dependência fornecida:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a id="tagging"></a>
### Tagging

Ocasionalmente, você pode precisar resolver todas as bindings de uma certa "categoria". Por exemplo, talvez você esteja construindo um analisador de relatórios que recebe um array de muitas diferentes implementações da interface `Report`. Depois de registrar as implementações de `Report`, você pode atribuir a elas uma tag usando o método `tag`:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

Uma vez que os serviços tenham sido etiquetados, você pode facilmente resolvê-los todos via o método `tagged` do container:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a id="extending-bindings"></a>
### Estendendo Bindings

O método `extend` permite a modificação de serviços resolvidos. Por exemplo, quando um serviço é resolvido, você pode executar código adicional para decorar ou configurar o serviço. O método `extend` aceita dois argumentos, a classe do serviço que você está estendendo e um closure que deve retornar o serviço modificado. O closure recebe o serviço sendo resolvido e a instância do container:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a id="resolving"></a>
## Resolução

<a id="the-make-method"></a>
### O Método `make`

Você pode usar o método `make` para resolver uma instância de classe a partir do container. O método `make` aceita o nome da classe ou interface que você deseja resolver:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

Se algumas das dependências da sua classe não forem resolvíveis via o container, você pode injetá-las passando-as como um array associativo no método `makeWith`. Por exemplo, podemos passar manualmente o argumento do construtor `$id` exigido pelo serviço `Transistor`:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

O método `bound` pode ser usado para determinar se uma classe ou interface foi explicitamente vinculada no container:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

Se você estiver fora de um provedor de serviço em um local do seu código que não tem acesso à variável `$app`, você pode usar a [facade](../facades/) `App` ou o [helper](../helpers/#method-app) `app` para resolver uma instância de classe a partir do container:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

Se você gostaria de ter a própria instância do container Laravel injetada em uma classe que está sendo resolvida pelo container, você pode usar type-hint da classe `Illuminate\Container\Container` no construtor da sua classe:

```php
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container,
) {}
```

<a id="automatic-injection"></a>
### Injeção Automática

Alternativamente, e importante, você pode usar type-hint da dependência no construtor de uma classe que é resolvida pelo container, incluindo [controllers](../controllers/), [ouvintes de eventos](../events/), [middleware](../middleware/), e mais. Além disso, você pode usar type-hint de dependências no método `handle` de [jobs enfileirados](../queues/). Na prática, é assim que a maioria dos seus objetos deve ser resolvida pelo container.

Por exemplo, você pode usar type-hint de um serviço definido pela sua aplicação no construtor de um controller. O serviço será automaticamente resolvido e injetado na classe:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a id="method-invocation-and-injection"></a>
## Invocação e Injeção de Métodos

Às vezes, você pode desejar invocar um método em uma instância de objeto enquanto permite que o container injete automaticamente as dependências desse método. Por exemplo, dada a seguinte classe:

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * Generate a new podcast stats report.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

Você pode invocar o método `generate` via o container assim:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

O método `call` aceita qualquer callable PHP. O método `call` do container pode até ser usado para invocar um closure enquanto injeta automaticamente suas dependências:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a id="container-events"></a>
## Eventos do Container

O container de serviço dispara um evento cada vez que resolve um objeto. Você pode ouvir esse evento usando o método `resolving`:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // Called when container resolves objects of type "Transistor"...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // Called when container resolves object of any type...
});
```

Como você pode ver, o objeto sendo resolvido será passado para o callback, permitindo que você defina quaisquer propriedades adicionais no objeto antes que ele seja entregue ao seu consumidor.

<a id="rebinding"></a>
### Rebinding

O método `rebinding` permite que você ouça quando um serviço é revinculado ao container, significando que ele é registrado novamente ou sobrescrito após seu binding inicial. Isso pode ser útil quando você precisa atualizar dependências ou modificar comportamento cada vez que um binding específico é atualizado:

```php
use App\Contracts\PodcastPublisher;
use App\Services\SpotifyPublisher;
use App\Services\TransistorPublisher;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(PodcastPublisher::class, SpotifyPublisher::class);

$this->app->rebinding(
    PodcastPublisher::class,
    function (Application $app, PodcastPublisher $newInstance) {
        //
    },
);

// New binding will trigger rebinding closure...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a id="psr-11"></a>
## PSR-11

O container de serviço do Laravel implementa a interface [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md). Portanto, você pode usar type-hint da interface de container PSR-11 para obter uma instância do container Laravel:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

Uma exceção é lançada se o identificador fornecido não puder ser resolvido. A exceção será uma instância de `Psr\Container\NotFoundExceptionInterface` se o identificador nunca foi vinculado. Se o identificador foi vinculado mas não pôde ser resolvido, uma instância de `Psr\Container\ContainerExceptionInterface` será lançada.