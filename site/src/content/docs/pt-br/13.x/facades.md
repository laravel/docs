---
title: "Facades"
---

- [Introdução](#introduction)
- [Quando Utilizar Facades](#when-to-use-facades)
    - [Facades vs. Injeção de Dependência](#facades-vs-dependency-injection)
    - [Facades vs. Funções Auxiliares](#facades-vs-helper-functions)
- [Como Facades Funcionam](#how-facades-work)
- [Facades em Tempo Real](#real-time-facades)
- [Referência de Classes Facade](#facade-class-reference)

<a id="introduction"></a>
## Introdução

Ao longo da documentação do Laravel, você verá exemplos de código que interage com os recursos do Laravel via "facades". Facades fornecem uma interface "estática" para classes que estão disponíveis no [container de serviço](../container/) da aplicação. O Laravel vem com muitas facades que fornecem acesso a quase todos os recursos do Laravel.

As facades do Laravel servem como "proxies estáticos" para as classes subjacentes no container de serviço, proporcionando o benefício de uma sintaxe concisa e expressiva, mantendo mais testabilidade e flexibilidade do que métodos estáticos tradicionais. Está perfeitamente bem se você não entender completamente como as facades funcionam - apenas siga em frente e continue aprendendo sobre o Laravel.

Todas as facades do Laravel são definidas no namespace `Illuminate\Support\Facades`. Então, podemos facilmente acessar uma facade assim:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Ao longo da documentação do Laravel, muitos dos exemplos usarão facades para demonstrar vários recursos do framework.

<a id="helper-functions"></a>
#### Funções Auxiliares

Para complementar as facades, o Laravel oferece uma variedade de "funções auxiliares" globais que tornam ainda mais fácil interagir com recursos comuns do Laravel. Algumas das funções auxiliares comuns com as quais você pode interagir são `view`, `response`, `url`, `config`, e mais. Cada função auxiliar oferecida pelo Laravel é documentada com seu recurso correspondente; no entanto, uma lista completa está disponível na [documentação dedicada de helpers](../helpers/).

Por exemplo, em vez de usar a facade `Illuminate\Support\Facades\Response` para gerar uma resposta JSON, podemos simplesmente usar a função `response`. Como as funções auxiliares estão globalmente disponíveis, você não precisa importar nenhuma classe para usá-las:

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});
```

<a id="when-to-use-facades"></a>
## Quando Utilizar Facades

As facades têm muitos benefícios. Elas fornecem uma sintaxe concisa e memorável que permite usar os recursos do Laravel sem lembrar de nomes longos de classes que devem ser injetados ou configurados manualmente. Além disso, por causa de seu uso exclusivo dos métodos dinâmicos do PHP, elas são fáceis de testar.

No entanto, alguns cuidados devem ser tomados ao usar facades. O principal perigo das facades é o "escopo crescente" da classe. Como as facades são tão fáceis de usar e não requerem injeção, pode ser fácil deixar suas classes continuarem crescendo e usar muitas facades em uma única classe. Usando injeção de dependência, esse potencial é mitigado pelo feedback visual que um construtor grande dá que sua classe está ficando grande demais. Então, ao usar facades, preste atenção especial ao tamanho da sua classe para que seu escopo de responsabilidade permaneça estreito. Se sua classe estiver ficando grande demais, considere dividi-la em múltiplas classes menores.

<a id="facades-vs-dependency-injection"></a>
### Facades vs. Injeção de Dependência

Um dos principais benefícios da injeção de dependência é a capacidade de trocar implementações da classe injetada. Isso é útil durante testes, já que você pode injetar um mock ou stub e afirmar que vários métodos foram chamados no stub.

Tipicamente, não seria possível fazer mock ou stub de um método de classe verdadeiramente estático. No entanto, como as facades usam métodos dinâmicos para fazer proxy de chamadas de métodos para objetos resolvidos do container de serviço, na verdade podemos testar facades da mesma forma que testaríamos uma instância de classe injetada. Por exemplo, dada a seguinte rota:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Usando os métodos de teste de facade do Laravel, podemos escrever o seguinte teste para verificar que o método `Cache::get` foi chamado com o argumento que esperávamos:

```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a id="facades-vs-helper-functions"></a>
### Facades vs. Funções Auxiliares

Além das facades, o Laravel inclui uma variedade de funções "auxiliares" que podem realizar tarefas comuns como gerar views, disparar eventos, despachar jobs ou enviar respostas HTTP. Muitas dessas funções auxiliares realizam a mesma função que uma facade correspondente. Por exemplo, esta chamada de facade e chamada de função auxiliar são equivalentes:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

Não há absolutamente nenhuma diferença prática entre facades e funções auxiliares. Ao usar funções auxiliares, você ainda pode testá-las exatamente como testaria a facade correspondente. Por exemplo, dada a seguinte rota:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

O helper `cache` vai chamar o método `get` na classe subjacente da facade `Cache`. Então, mesmo que estejamos usando a função auxiliar, podemos escrever o seguinte teste para verificar que o método foi chamado com o argumento que esperávamos:

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a id="how-facades-work"></a>
## Como Facades Funcionam

Em uma aplicação Laravel, uma facade é uma classe que fornece acesso a um objeto do container. O mecanismo que faz isso funcionar está na classe `Facade`. As facades do Laravel, e quaisquer facades personalizadas que você criar, estenderão a classe base `Illuminate\Support\Facades\Facade`.

A classe base `Facade` usa o método mágico `__callStatic()` para adiar chamadas da sua facade para um objeto resolvido do container. No exemplo abaixo, uma chamada é feita ao sistema de cache do Laravel. Ao dar uma olhada neste código, alguém pode supor que o método estático `get` está sendo chamado na classe `Cache`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

Observe que perto do topo do arquivo estamos "importando" a facade `Cache`. Esta facade serve como um proxy para acessar a implementação subjacente da interface `Illuminate\Contracts\Cache\Factory`. Quaisquer chamadas que fizermos usando a facade serão passadas para a instância subjacente do serviço de cache do Laravel.

Se olharmos aquela classe `Illuminate\Support\Facades\Cache`, você verá que não há método estático `get`:

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

Em vez disso, a facade `Cache` estende a classe base `Facade` e define o método `getFacadeAccessor()`. O trabalho deste método é retornar o nome de um binding do container de serviço. Quando um usuário referencia qualquer método estático na facade `Cache`, o Laravel resolve o binding `cache` do [container de serviço](../container/) e executa o método solicitado (neste caso, `get`) naquele objeto.

<a id="real-time-facades"></a>
## Facades em Tempo Real

Usando facades em tempo real, você pode tratar qualquer classe em sua aplicação como se fosse uma facade. Para ilustrar como isso pode ser usado, vamos primeiro examinar algum código que não usa facades em tempo real. Por exemplo, vamos supor que nosso modelo `Podcast` tem um método `publish`. No entanto, para publicar o podcast, precisamos injetar uma instância de `Publisher`:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

Injetar uma implementação de publisher no método nos permite facilmente testar o método em isolamento, já que podemos fazer mock do publisher injetado. No entanto, requer que sempre passemos uma instância de publisher cada vez que chamamos o método `publish`. Usando facades em tempo real, podemos manter a mesma testabilidade sem sermos obrigados a passar explicitamente uma instância de `Publisher`. Para gerar uma facade em tempo real, prefixe o namespace da classe importada com `Facades`:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}
```

Quando a facade em tempo real é usada, a implementação do publisher será resolvida do container de serviço usando a porção do nome da classe ou interface que aparece após o prefixo `Facades`. Ao testar, podemos usar os helpers de teste de facade integrados do Laravel para fazer mock desta chamada de método:

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a id="facade-class-reference"></a>
## Referência de Classes Facade

Abaixo você encontrará cada facade e sua classe subjacente. Esta é uma ferramenta útil para mergulhar rapidamente na documentação da API para uma determinada raiz de facade. A chave de [binding do container de serviço](../container/) também é incluída onde aplicável.

<div class="overflow-auto">

| Facade | Classe | Binding do Container de Serviço |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Console/Kernel.html) | &nbsp; |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (Instance) | [Illuminate\Cache\Repository](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Cloud | [Illuminate\Foundation\Cloud\CloudManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Foundation/Cloud/CloudManager.html) | &nbsp; |
| Config | [Illuminate\Config\Repository](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Support/DateFactory.html) | `date` |
| DB (Instance) | [Illuminate\Database\Connection](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Log/LogManager.html) | `log` |
| Mail (Instance) | [Illuminate\Mail\Mailer](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Mail | [Illuminate\Mail\MailManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Mail/MailManager.html) | `mail.manager` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Http/Request.html) | `request` |
| Response (Instance) | [Illuminate\Http\Response](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (Instance) | [Illuminate\Session\Store](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Session/SessionManager.html) | `session` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>