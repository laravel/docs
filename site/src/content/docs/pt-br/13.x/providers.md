---
title: "Provedores de Serviço"
---

- [Introdução](#introduction)
- [Escrevendo Provedores de Serviço](#writing-service-providers)
    - [O Método Register](#the-register-method)
    - [O Método Boot](#the-boot-method)
- [Registrando Provedores](#registering-providers)
- [Provedores Adiados](#deferred-providers)

<a id="introduction"></a>
## Introdução

Os provedores de serviço são o local central de toda a inicialização de aplicações Laravel. Sua própria aplicação, bem como todos os serviços principais do Laravel, são inicializados via provedores de serviço.

Mas, o que queremos dizer com "inicializados"? Em geral, queremos dizer **registrar** coisas, incluindo registros de bindings do container de serviço, ouvintes de eventos, middleware, e até rotas. Os provedores de serviço são o local central para configurar sua aplicação.

O Laravel usa dezenas de provedores de serviço internamente para inicializar seus serviços principais, como o mailer, fila, cache e outros. Muitos desses provedores são provedores "adiados", significando que eles não serão carregados em cada requisição, mas apenas quando os serviços que eles fornecem forem realmente necessários.

Todos os provedores de serviço definidos pelo usuário são registrados no arquivo `bootstrap/providers.php`. Na documentação a seguir, você aprenderá como escrever seus próprios provedores de serviço e registrá-los com sua aplicação Laravel.

> **Nota:**
> Se você gostaria de aprender mais sobre como o Laravel trata requisições e funciona internamente, confira nossa documentação sobre o [ciclo de vida da requisição](../lifecycle/) do Laravel.

<a id="writing-service-providers"></a>
## Escrevendo Provedores de Serviço

Todos os provedores de serviço estendem a classe `Illuminate\Support\ServiceProvider`. A maioria dos provedores de serviço contém um método `register` e um método `boot`. Dentro do método `register`, você deve **apenas vincular coisas ao [container de serviço](../container/)**. Você nunca deve tentar registrar qualquer ouvinte de evento, rota ou qualquer outra peça de funcionalidade dentro do método `register`.

A CLI do Artisan pode gerar um novo provedor via o comando `make:provider`. O Laravel registrará automaticamente seu novo provedor no arquivo `bootstrap/providers.php` da sua aplicação:

```shell
php artisan make:provider RiakServiceProvider
```

<a id="the-register-method"></a>
### O Método Register

Como mencionado anteriormente, dentro do método `register`, você deve apenas vincular coisas ao [container de serviço](../container/). Você nunca deve tentar registrar qualquer ouvinte de evento, rota ou qualquer outra peça de funcionalidade dentro do método `register`. Caso contrário, você pode acidentalmente usar um serviço que é fornecido por um provedor de serviço que ainda não foi carregado.

Vamos dar uma olhada em um provedor de serviço básico. Dentro de qualquer um dos métodos do seu provedor de serviço, você sempre tem acesso à propriedade `$app` que fornece acesso ao container de serviço:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

Este provedor de serviço apenas define um método `register`, e usa esse método para definir uma implementação de `App\Services\Riak\Connection` no container de serviço. Se você ainda não está familiarizado com o container de serviço do Laravel, confira [sua documentação](../container/).

<a id="the-bindings-and-singletons-properties"></a>
#### As Propriedades `bindings` e `singletons`

Se seu provedor de serviço registra muitos bindings simples, você pode desejar usar as propriedades `bindings` e `singletons` em vez de registrar manualmente cada binding do container. Quando o provedor de serviço é carregado pelo framework, ele verificará automaticamente essas propriedades e registrará seus bindings:

```php
<?php

namespace App\Providers;

use App\Contracts\DowntimeNotifier;
use App\Contracts\ServerProvider;
use App\Services\DigitalOceanServerProvider;
use App\Services\PingdomDowntimeNotifier;
use App\Services\ServerToolsProvider;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * All of the container bindings that should be registered.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * All of the container singletons that should be registered.
     *
     * @var array
     */
    public $singletons = [
        DowntimeNotifier::class => PingdomDowntimeNotifier::class,
        ServerProvider::class => ServerToolsProvider::class,
    ];
}
```

<a id="the-boot-method"></a>
### O Método Boot

Então, e se precisarmos registrar um [view composer](../views/#view-composers) dentro do nosso provedor de serviço? Isso deve ser feito dentro do método `boot`. **Este método é chamado depois que todos os outros provedores de serviço tenham sido registrados**, significando que você tem acesso a todos os outros serviços que foram registrados pelo framework:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::composer('view', function () {
            // ...
        });
    }
}
```

<a id="boot-method-dependency-injection"></a>
#### Injeção de Dependência no Método Boot

Você pode usar type-hint de dependências para o método `boot` do seu provedor de serviço. O [container de serviço](../container/) injetará automaticamente quaisquer dependências que você precisar:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a id="registering-providers"></a>
## Registrando Provedores

Todos os provedores de serviço são registrados no arquivo de configuração `bootstrap/providers.php`. Este arquivo retorna um array que contém os nomes das classes dos provedores de serviço da sua aplicação:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

Quando você invoca o comando Artisan `make:provider`, o Laravel adicionará automaticamente o provedor gerado ao arquivo `bootstrap/providers.php`. No entanto, se você tiver criado manualmente a classe do provedor, você deve adicionar manualmente a classe do provedor ao array:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a id="deferred-providers"></a>
## Provedores Adiados

Se seu provedor está **apenas** registrando bindings no [container de serviço](../container/), você pode escolher adiar seu registro até que um dos bindings registrados seja realmente necessário. Adiar o carregamento de tal provedor melhorará o desempenho da sua aplicação, já que ele não é carregado do sistema de arquivos em cada requisição.

O Laravel compila e armazena uma lista de todos os serviços fornecidos por provedores de serviço adiados, junto com o nome da classe do provedor de serviço. Então, apenas quando você tenta resolver um desses serviços é que o Laravel carrega o provedor de serviço.

Para adiar o carregamento de um provedor, implemente a interface `\Illuminate\Contracts\Support\DeferrableProvider` e defina um método `provides`. O método `provides` deve retornar os bindings do container de serviço registrados pelo provedor:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```