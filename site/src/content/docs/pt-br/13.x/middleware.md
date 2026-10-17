---
title: "Middleware"
---

- [Introdução](#introduction)
- [Definindo Middleware](#defining-middleware)
- [Registrando Middleware](#registering-middleware)
    - [Middleware Global](#global-middleware)
    - [Atribuindo Middleware a Rotas](#assigning-middleware-to-routes)
    - [Grupos de Middleware](#middleware-groups)
    - [Aliases de Middleware](#middleware-aliases)
    - [Ordenando Middleware](#sorting-middleware)
- [Parâmetros de Middleware](#middleware-parameters)
- [Middleware Terminável](#terminable-middleware)

<a id="introduction"></a>
## Introdução

Middleware fornece um mecanismo conveniente para inspecionar e filtrar requisições HTTP entrando em sua aplicação. Por exemplo, o Laravel inclui um middleware que verifica se o usuário da sua aplicação está autenticado. Se o usuário não estiver autenticado, o middleware redirecionará o usuário para a tela de login da sua aplicação. No entanto, se o usuário estiver autenticado, o middleware permitirá que a requisição prossiga mais adiante na aplicação.

Middleware adicional pode ser escrito para realizar uma variedade de tarefas além da autenticação. Por exemplo, um middleware de logging pode registrar todas as requisições recebidas na sua aplicação. Uma variedade de middleware estão incluídos no Laravel, incluindo middleware para autenticação e proteção CSRF; no entanto, todos os middleware definidos pelo usuário estão tipicamente localizados no diretório `app/Http/Middleware` da sua aplicação.

<a id="defining-middleware"></a>
## Definindo Middleware

Para criar um novo middleware, use o comando Artisan `make:middleware`:

```shell
php artisan make:middleware EnsureTokenIsValid
```

Este comando colocará uma nova classe `EnsureTokenIsValid` dentro do seu diretório `app/Http/Middleware`. Neste middleware, nós apenas permitiremos acesso à rota se o input `token` fornecido corresponder a um valor especificado. Caso contrário, nós redirecionaremos os usuários de volta para a URI `/home`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('/home');
        }

        return $next($request);
    }
}
```

Como você pode ver, se o `token` fornecido não corresponder ao nosso token secreto, o middleware retornará um redirecionamento HTTP para o cliente; caso contrário, a requisição será passada mais adiante na aplicação. Para passar a requisição mais profundamente na aplicação (permitindo que o middleware "passe"), você deve chamar o callback `$next` com o `$request`.

É melhor imaginar middleware como uma série de "camadas" que as requisições HTTP devem passar antes de atingir sua aplicação. Cada camada pode examinar a requisição e até rejeitá-la completamente.

> **Nota:**
> Todos os middleware são resolvidos via [container de serviço](../container/), então você pode usar type-hint de quaisquer dependências que precisar dentro do construtor de um middleware.

<a id="middleware-and-responses"></a>
#### Middleware e Respostas

Claro, um middleware pode realizar tarefas antes ou depois de passar a requisição mais profundamente na aplicação. Por exemplo, o seguinte middleware realizaria alguma tarefa **antes** que a requisição seja tratada pela aplicação:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class BeforeMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Perform action

        return $next($request);
    }
}
```

No entanto, este middleware realizaria sua tarefa **depois** que a requisição seja tratada pela aplicação:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AfterMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Perform action

        return $response;
    }
}
```

<a id="registering-middleware"></a>
## Registrando Middleware

<a id="global-middleware"></a>
### Middleware Global

Se você deseja que um middleware seja executado durante cada requisição HTTP para sua aplicação, você pode adicioná-lo à pilha de middleware global no arquivo `bootstrap/app.php` da sua aplicação:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

O objeto `$middleware` fornecido ao closure `withMiddleware` é uma instância de `Illuminate\Foundation\Configuration\Middleware` e é responsável por gerenciar os middleware atribuídos às rotas da sua aplicação. O método `append` adiciona o middleware ao final da lista de middleware global. Se você gostaria de adicionar um middleware ao início da lista, você deve usar o método `prepend`.

<a id="manually-managing-laravels-default-global-middleware"></a>
#### Gerenciando Manualmente o Middleware Global Padrão do Laravel

Se você gostaria de gerenciar a pilha de middleware global do Laravel manualmente, você pode fornecer a pilha padrão de middleware global do Laravel ao método `use`. Então, você pode ajustar a pilha de middleware padrão conforme necessário:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->use([
        \Illuminate\Http\Middleware\ValidatePathEncoding::class,
        \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class,
        // \Illuminate\Http\Middleware\TrustHosts::class,
        \Illuminate\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Http\Middleware\ValidatePostSize::class,
        \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ]);
})
```

<a id="assigning-middleware-to-routes"></a>
### Atribuindo Middleware a Rotas

Se você gostaria de atribuir middleware a rotas específicas, você pode invocar o método `middleware` ao definir a rota:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

Você pode atribuir múltiplos middleware à rota passando um array de nomes de middleware ao método `middleware`:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a id="excluding-middleware"></a>
#### Excluindo Middleware

Ao atribuir middleware a um grupo de rotas, você ocasionalmente pode precisar impedir que o middleware seja aplicado a uma rota individual dentro do grupo. Você pode conseguir isso usando o método `withoutMiddleware`:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        // ...
    });

    Route::get('/profile', function () {
        // ...
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```

Você também pode excluir um determinado conjunto de middleware de todo um [grupo](../routing/#route-groups) de definições de rotas:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

O método `withoutMiddleware` só pode remover middleware de rota e não se aplica a [middleware global](#global-middleware).

<a id="middleware-groups"></a>
### Grupos de Middleware

Às vezes, você pode querer agrupar vários middleware sob uma única chave para torná-los mais fáceis de atribuir a rotas. Você pode conseguir isso usando o método `appendToGroup` no arquivo `bootstrap/app.php` da sua aplicação:

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->appendToGroup('group-name', [
        First::class,
        Second::class,
    ]);

    $middleware->prependToGroup('group-name', [
        First::class,
        Second::class,
    ]);
})
```

Grupos de middleware podem ser atribuídos a rotas e ações de controller usando a mesma sintaxe que middleware individual:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a id="laravels-default-middleware-groups"></a>
#### Grupos de Middleware Padrão do Laravel

O Laravel inclui grupos de middleware `web` e `api` predefinidos que contêm middleware comuns que você pode querer aplicar às suas rotas web e API. Lembre-se, o Laravel aplica automaticamente esses grupos de middleware aos arquivos correspondentes `routes/web.php` e `routes/api.php`:

<div class="overflow-auto">

| O Grupo de Middleware `web`                                |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| O Grupo de Middleware `api`                         |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

Se você gostaria de adicionar ou prefixar middleware a esses grupos, você pode usar os métodos `web` e `api` no arquivo `bootstrap/app.php` da sua aplicação. Os métodos `web` e `api` são alternativas convenientes ao método `appendToGroup`:

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

Você pode até substituir uma das entradas do grupo de middleware padrão do Laravel com um middleware personalizado seu:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

Ou, você pode remover um middleware completamente:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a id="manually-managing-laravels-default-middleware-groups"></a>
#### Gerenciando Manualmente os Grupos de Middleware Padrão do Laravel

Se você gostaria de gerenciar manualmente todos os middleware dentro dos grupos de middleware padrão `web` e `api` do Laravel, você pode redefinir os grupos completamente. O exemplo abaixo definirá os grupos de middleware `web` e `api` com seus middleware padrão, permitindo que você os personalize conforme necessário:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
    ]);

    $middleware->group('api', [
        // \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        // 'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ]);
})
```

> **Nota:**
> Por padrão, os grupos de middleware `web` e `api` são automaticamente aplicados aos arquivos correspondentes `routes/web.php` e `routes/api.php` da sua aplicação pelo arquivo `bootstrap/app.php`.

<a id="middleware-aliases"></a>
### Aliases de Middleware

Você pode atribuir aliases a middleware no arquivo `bootstrap/app.php` da sua aplicação. Aliases de middleware permitem que você defina um alias curto para uma determinada classe de middleware, o que pode ser especialmente útil para middleware com nomes de classes longos:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

Uma vez que o alias de middleware tenha sido definido no arquivo `bootstrap/app.php` da sua aplicação, você pode usar o alias ao atribuir o middleware às rotas:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

Para conveniência, alguns dos middleware integrados do Laravel têm aliases definidos por padrão. Por exemplo, o middleware `auth` é um alias para o middleware `Illuminate\Auth\Middleware\Authenticate`. Abaixo está uma lista dos aliases de middleware padrão:

<div class="overflow-auto">

| Alias              | Middleware                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------- |
| `auth`             | `Illuminate\Auth\Middleware\Authenticate`                                                                     |
| `auth.basic`       | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                        |
| `auth.session`     | `Illuminate\Session\Middleware\AuthenticateSession`                                                           |
| `cache.headers`    | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                  |
| `can`              | `Illuminate\Auth\Middleware\Authorize`                                                                        |
| `guest`            | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                          |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword`                                                                  |
| `precognitive`     | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                            |
| `signed`           | `Illuminate\Routing\Middleware\ValidateSignature`                                                             |
| `subscribed`       | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                           |
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` ou `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                            |

</div>

<a id="sorting-middleware"></a>
### Ordenando Middleware

Raramente, você pode precisar que seus middleware sejam executados em uma ordem específica, mas não ter controle sobre sua ordem quando são atribuídos à rota. Nessas situações, você pode especificar a prioridade do seu middleware usando o método `priority` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ]);
})
```

Se você gostaria de adicionar middleware à lista de prioridade existente sem substituí-la, você pode usar os métodos `prependToPriorityList` ou `appendToPriorityList`. O método `prependToPriorityList` insere o middleware dado antes de outro middleware, enquanto o método `appendToPriorityList` o insere após outro middleware:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\EnsureTokenIsValid::class,
    );

    $middleware->appendToPriorityList(
        after: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        append: \App\Http\Middleware\EnsureUserIsSubscribed::class,
    );
})
```

Os argumentos `before` e `after` também podem ser um array de classes de middleware.

<a id="middleware-parameters"></a>
## Parâmetros de Middleware

Middleware também podem receber parâmetros adicionais. Por exemplo, se sua aplicação precisa verificar que o usuário autenticado tem uma determinada "função" antes de realizar uma determinada ação, você poderia criar um middleware `EnsureUserHasRole` que recebe um nome de função como um argumento adicional.

Parâmetros adicionais de middleware serão passados ao middleware após o argumento `$next`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // Redirect...
        }

        return $next($request);
    }
}
```

Parâmetros de middleware podem ser especificados ao definir a rota separando o nome do middleware e os parâmetros com `:`:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

Múltiplos parâmetros podem ser delimitados por vírgulas:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a id="terminable-middleware"></a>
## Middleware Terminável

Às vezes, um middleware pode precisar fazer algum trabalho depois que a resposta HTTP tenha sido enviada ao navegador. Se você definir um método `terminate` no seu middleware e seu servidor web estiver usando [FastCGI](https://www.php.net/manual/en/install.fpm.php), o método `terminate` será automaticamente chamado após a resposta ser enviada ao navegador:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

O método `terminate` deve receber tanto a requisição quanto a resposta. Uma vez que você tenha definido um middleware terminável, você deve adicioná-lo à lista de rotas ou middleware global no arquivo `bootstrap/app.php` da sua aplicação.

Ao chamar o método `terminate` no seu middleware, o Laravel resolverá uma nova instância do middleware do [container de serviço](../container/). Se você gostaria de usar a mesma instância de middleware quando os métodos `handle` e `terminate` forem chamados, registre o middleware com o container usando o método `singleton` do container. Tipicamente isso deve ser feito no método `register` do seu `AppServiceProvider`:

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```