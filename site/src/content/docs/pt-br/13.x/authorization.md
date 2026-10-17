---
title: "Autorização"
---

- [Introdução](#introduction)
- [Gates](#gates)
    - [Escrevendo Gates](#writing-gates)
    - [Autorizando Ações](#authorizing-actions-via-gates)
    - [Respostas de Gate](#gate-responses)
    - [Interceptando Verificações de Gate](#intercepting-gate-checks)
    - [Autorização Inline](#inline-authorization)
- [Criando Policies](#creating-policies)
    - [Gerando Policies](#generating-policies)
    - [Registrando Policies](#registering-policies)
- [Escrevendo Policies](#writing-policies)
    - [Métodos de Policy](#policy-methods)
    - [Respostas de Policy](#policy-responses)
    - [Métodos Sem Modelos](#methods-without-models)
    - [Usuários Visitantes](#guest-users)
    - [Filtros de Policy](#policy-filters)
- [Autorizando Ações Usando Policies](#authorizing-actions-using-policies)
    - [Via o Modelo User](#via-the-user-model)
    - [Via a Facade Gate](#via-the-gate-facade)
    - [Via Middleware](#via-middleware)
    - [Via Templates Blade](#via-blade-templates)
    - [Fornecendo Contexto Adicional](#supplying-additional-context)
- [Autorização & Inertia](#authorization-and-inertia)

<a id="introduction"></a>
## Introdução

Além de fornecer serviços de [autenticação](../authentication/) integrados, o Laravel também fornece uma forma simples de autorizar ações de usuários contra um determinado recurso. Por exemplo, mesmo que um usuário esteja autenticado, ele pode não estar autorizado a atualizar ou excluir determinados modelos Eloquent ou registros de banco de dados gerenciados pela sua aplicação. Os recursos de autorização do Laravel fornecem uma forma fácil e organizada de gerenciar esses tipos de verificações de autorização.

O Laravel fornece duas formas principais de autorizar ações: [gates](#gates) e [policies](#creating-policies). Pense em gates e policies como rotas e controllers. Gates fornecem uma abordagem simples, baseada em closures, para a autorização, enquanto policies, assim como controllers, agrupam a lógica em torno de um determinado modelo ou recurso. Nesta documentação, exploraremos primeiro os gates e depois examinaremos as policies.

Você não precisa escolher entre usar exclusivamente gates ou exclusivamente policies ao construir uma aplicação. A maioria das aplicações provavelmente conterá alguma mistura de gates e policies, e isso é perfeitamente aceitável! Gates são mais aplicáveis a ações que não estão relacionadas a nenhum modelo ou recurso, como visualizar um dashboard de administrador. Em contraste, policies devem ser usadas quando você deseja autorizar uma ação para um determinado modelo ou recurso.

<a id="gates"></a>
## Gates

<a id="writing-gates"></a>
### Escrevendo Gates

> **Warning:**
> Gates são uma ótima forma de aprender o básico dos recursos de autorização do Laravel; no entanto, ao construir aplicações Laravel robustas, você deve considerar o uso de [policies](#creating-policies) para organizar suas regras de autorização.

Gates são simplesmente closures que determinam se um usuário está autorizado a realizar uma determinada ação. Normalmente, gates são definidos dentro do método `boot` da classe `App\Providers\AppServiceProvider` usando a facade `Gate`. Gates sempre recebem uma instância de usuário como seu primeiro argumento e podem opcionalmente receber argumentos adicionais, como um modelo Eloquent relevante.

Neste exemplo, definiremos um gate para determinar se um usuário pode atualizar um determinado modelo `App\Models\Post`. O gate fará isso comparando o `id` do usuário com o `user_id` do usuário que criou o post:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

Assim como controllers, gates também podem ser definidos usando um array de callback de classe:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a id="authorizing-actions-via-gates"></a>
### Autorizando Ações

Para autorizar uma ação usando gates, você deve usar os métodos `allows` ou `denies` fornecidos pela facade `Gate`. Observe que você não é obrigado a passar o usuário autenticado no momento para esses métodos. O Laravel cuidará automaticamente de passar o usuário para a closure do gate. É comum chamar os métodos de autorização do gate dentro dos controllers da sua aplicação antes de realizar uma ação que exija autorização:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

Se você quiser determinar se um usuário diferente do usuário autenticado no momento está autorizado a realizar uma ação, você pode usar o método `forUser` na facade `Gate`:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

Você pode autorizar múltiplas ações de uma vez usando os métodos `any` ou `none`:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a id="authorizing-or-throwing-exceptions"></a>
#### Autorizando ou Lançando Exceções

Se você quiser tentar autorizar uma ação e lançar automaticamente uma `Illuminate\Auth\Access\AuthorizationException` se o usuário não tiver permissão para realizar a ação fornecida, você pode usar o método `authorize` da facade `Gate`. Instâncias de `AuthorizationException` são automaticamente convertidas em uma resposta HTTP 403 pelo Laravel:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a id="gates-supplying-additional-context"></a>
#### Fornecendo Contexto Adicional

Os métodos de gate para autorizar abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) e as [diretivas Blade](#via-blade-templates) de autorização (`@can`, `@cannot`, `@canany`) podem receber um array como seu segundo argumento. Esses elementos do array são passados como parâmetros para a closure do gate e podem ser usados para contexto adicional ao tomar decisões de autorização:

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, bool $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // The user can create the post...
}
```

<a id="gate-responses"></a>
### Respostas de Gate

Até agora, examinamos apenas gates que retornam valores booleanos simples. No entanto, às vezes você pode querer retornar uma resposta mais detalhada, incluindo uma mensagem de erro. Para fazer isso, você pode retornar uma `Illuminate\Auth\Access\Response` do seu gate:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('You must be an administrator.');
});
```

Mesmo quando você retorna uma resposta de autorização do seu gate, o método `Gate::allows` ainda retornará um valor booleano simples; no entanto, você pode usar o método `Gate::inspect` para obter a resposta completa de autorização retornada pelo gate:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

Ao usar o método `Gate::authorize`, que lança uma `AuthorizationException` se a ação não for autorizada, a mensagem de erro fornecida pela resposta de autorização será propagada para a resposta HTTP:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a id="customizing-gate-response-status"></a>
#### Personalizando o Status da Resposta HTTP

Quando uma ação é negada via um Gate, uma resposta HTTP `403` é retornada; no entanto, às vezes pode ser útil retornar um código de status HTTP alternativo. Você pode personalizar o código de status HTTP retornado para uma verificação de autorização malsucedida usando o construtor estático `denyWithStatus` na classe `Illuminate\Auth\Access\Response`:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```

Como ocultar recursos por meio de uma resposta `404` é um padrão tão comum em aplicações web, o método `denyAsNotFound` é oferecido por conveniência:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyAsNotFound();
});
```

<a id="intercepting-gate-checks"></a>
### Interceptando Verificações de Gate

Às vezes, você pode querer conceder todas as abilities a um usuário específico. Você pode usar o método `before` para definir uma closure que é executada antes de todas as outras verificações de autorização:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

Se a closure `before` retornar um resultado não nulo, esse resultado será considerado o resultado da verificação de autorização.

Você pode usar o método `after` para definir uma closure a ser executada após todas as outras verificações de autorização:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

Valores retornados por closures `after` não sobrescreverão o resultado da verificação de autorização, a menos que o gate ou a policy tenham retornado `null`.

<a id="inline-authorization"></a>
### Autorização Inline

Ocasionalmente, você pode querer determinar se o usuário autenticado no momento está autorizado a realizar uma determinada ação sem escrever um gate dedicado que corresponda à ação. O Laravel permite que você realize esses tipos de verificações de autorização "inline" por meio dos métodos `Gate::allowIf` e `Gate::denyIf`. A autorização inline não executa nenhum ["before" ou "after" hook de autorização](#intercepting-gate-checks) definido:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

Se a ação não for autorizada ou se nenhum usuário estiver autenticado no momento, o Laravel lançará automaticamente uma exceção `Illuminate\Auth\Access\AuthorizationException`. Instâncias de `AuthorizationException` são automaticamente convertidas em uma resposta HTTP 403 pelo exception handler do Laravel.

<a id="creating-policies"></a>
## Criando Policies

<a id="generating-policies"></a>
### Gerando Policies

Policies são classes que organizam a lógica de autorização em torno de um determinado modelo ou recurso. Por exemplo, se a sua aplicação for um blog, você pode ter um modelo `App\Models\Post` e uma `App\Policies\PostPolicy` correspondente para autorizar ações de usuários, como criar ou atualizar posts.

Você pode gerar uma policy usando o comando Artisan `make:policy`. A policy gerada será colocada no diretório `app/Policies`. Se esse diretório não existir na sua aplicação, o Laravel o criará para você:

```shell
php artisan make:policy PostPolicy
```

O comando `make:policy` gerará uma classe de policy vazia. Se você quiser gerar uma classe com métodos de policy de exemplo relacionados a visualizar, criar, atualizar e excluir o recurso, você pode fornecer uma opção `--model` ao executar o comando:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a id="registering-policies"></a>
### Registrando Policies

<a id="policy-discovery"></a>
#### Descoberta de Policy

Por padrão, o Laravel descobre policies automaticamente, desde que o modelo e a policy sigam as convenções de nomenclatura padrão do Laravel. Especificamente, as policies devem estar em um diretório `Policies` no mesmo nível ou acima do diretório que contém seus modelos. Então, por exemplo, os modelos podem ser colocados no diretório `app/Models`, enquanto as policies podem ser colocadas no diretório `app/Policies`. Nessa situação, o Laravel verificará policies em `app/Models/Policies` e depois em `app/Policies`. Além disso, o nome da policy deve corresponder ao nome do modelo e ter um sufixo `Policy`. Então, um modelo `User` corresponderia a uma classe de policy `UserPolicy`.

Se você quiser definir sua própria lógica de descoberta de policy, você pode registrar um callback de descoberta de policy personalizado usando o método `Gate::guessPolicyNamesUsing`. Normalmente, esse método deve ser chamado a partir do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a id="manually-registering-policies"></a>
#### Registrando Policies Manualmente

Usando a facade `Gate`, você pode registrar manualmente policies e seus modelos correspondentes dentro do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::policy(Order::class, OrderPolicy::class);
}
```

Alternativamente, você pode colocar o atributo `UsePolicy` em uma classe de modelo para informar ao Laravel sobre a policy correspondente do modelo:

```php
<?php

namespace App\Models;

use App\Policies\OrderPolicy;
use Illuminate\Database\Eloquent\Attributes\UsePolicy;
use Illuminate\Database\Eloquent\Model;

#[UsePolicy(OrderPolicy::class)]
class Order extends Model
{
    //
}
```

<a id="writing-policies"></a>
## Escrevendo Policies

<a id="policy-methods"></a>
### Métodos de Policy

Depois que a classe de policy tiver sido registrada, você pode adicionar métodos para cada ação que ela autoriza. Por exemplo, vamos definir um método `update` na nossa `PostPolicy` que determina se um determinado `App\Models\User` pode atualizar uma determinada instância de `App\Models\Post`.

O método `update` receberá uma instância de `User` e uma instância de `Post` como seus argumentos, e deve retornar `true` ou `false` indicando se o usuário está autorizado a atualizar o `Post` fornecido. Então, neste exemplo, verificaremos se o `id` do usuário corresponde ao `user_id` no post:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

Você pode continuar a definir métodos adicionais na policy conforme necessário para as várias ações que ela autoriza. Por exemplo, você pode definir métodos `view` ou `delete` para autorizar várias ações relacionadas a `Post`, mas lembre-se de que você tem a liberdade de dar aos seus métodos de policy qualquer nome que quiser.

Se você usou a opção `--model` ao gerar sua policy por meio do console Artisan, ela já conterá métodos para as ações `viewAny`, `view`, `create`, `update`, `delete`, `restore` e `forceDelete`.

> **Note:**
> Todas as policies são resolvidas por meio do [service container](../container/) do Laravel, permitindo que você faça type-hint de quaisquer dependências necessárias no construtor da policy para que elas sejam automaticamente injetadas.

<a id="policy-responses"></a>
### Respostas de Policy

Até agora, examinamos apenas métodos de policy que retornam valores booleanos simples. No entanto, às vezes você pode querer retornar uma resposta mais detalhada, incluindo uma mensagem de erro. Para fazer isso, você pode retornar uma instância de `Illuminate\Auth\Access\Response` do seu método de policy:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('You do not own this post.');
}
```

Ao retornar uma resposta de autorização da sua policy, o método `Gate::allows` ainda retornará um valor booleano simples; no entanto, você pode usar o método `Gate::inspect` para obter a resposta completa de autorização retornada pelo gate:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

Ao usar o método `Gate::authorize`, que lança uma `AuthorizationException` se a ação não for autorizada, a mensagem de erro fornecida pela resposta de autorização será propagada para a resposta HTTP:

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a id="customizing-policy-response-status"></a>
#### Personalizando o Status da Resposta HTTP

Quando uma ação é negada via um método de policy, uma resposta HTTP `403` é retornada; no entanto, às vezes pode ser útil retornar um código de status HTTP alternativo. Você pode personalizar o código de status HTTP retornado para uma verificação de autorização malsucedida usando o construtor estático `denyWithStatus` na classe `Illuminate\Auth\Access\Response`:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

Como ocultar recursos por meio de uma resposta `404` é um padrão tão comum em aplicações web, o método `denyAsNotFound` é oferecido por conveniência:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```

<a id="methods-without-models"></a>
### Métodos Sem Modelos

Alguns métodos de policy recebem apenas uma instância do usuário autenticado no momento. Essa situação é mais comum ao autorizar ações `create`. Por exemplo, se você estiver criando um blog, pode querer determinar se um usuário está autorizado a criar quaisquer posts. Nessas situações, seu método de policy deve esperar receber apenas uma instância de usuário:

```php
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a id="guest-users"></a>
### Usuários Visitantes

Por padrão, todos os gates e policies retornam automaticamente `false` se a requisição HTTP recebida não foi iniciada por um usuário autenticado. No entanto, você pode permitir que essas verificações de autorização passem para seus gates e policies declarando um type-hint "opcional" ou fornecendo um valor padrão `null` para a definição do argumento do usuário:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a id="policy-filters"></a>
### Filtros de Policy

Para determinados usuários, você pode querer autorizar todas as ações dentro de uma determinada policy. Para fazer isso, defina um método `before` na policy. O método `before` será executado antes de quaisquer outros métodos na policy, dando a você a oportunidade de autorizar a ação antes de o método de policy pretendido ser realmente chamado. Esse recurso é mais comumente usado para autorizar administradores da aplicação a realizar qualquer ação:

```php
use App\Models\User;

/**
 * Perform pre-authorization checks.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

Se você quiser negar todas as verificações de autorização para um determinado tipo de usuário, você pode retornar `false` do método `before`. Se `null` for retornado, a verificação de autorização passará para o método de policy.

> **Warning:**
> O método `before` de uma classe de policy não será chamado se a classe não contiver um método com um nome que corresponda ao nome da ability sendo verificada.

<a id="authorizing-actions-using-policies"></a>
## Autorizando Ações Usando Policies

<a id="via-the-user-model"></a>
### Via o Modelo User

O modelo `App\Models\User` que está incluído na sua aplicação Laravel inclui dois métodos úteis para autorizar ações: `can` e `cannot`. Os métodos `can` e `cannot` recebem o nome da ação que você deseja autorizar e o modelo relevante. Por exemplo, vamos determinar se um usuário está autorizado a atualizar um determinado modelo `App\Models\Post`. Normalmente, isso será feito dentro de um método de controller:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

Se uma [policy estiver registrada](#registering-policies) para o modelo fornecido, o método `can` chamará automaticamente a policy apropriada e retornará o resultado booleano. Se nenhuma policy estiver registrada para o modelo, o método `can` tentará chamar o Gate baseado em closure que corresponda ao nome da ação fornecido.

<a id="user-model-actions-that-dont-require-models"></a>
#### Ações Que Não Requerem Modelos

Lembre-se, algumas ações podem corresponder a métodos de policy como `create` que não requerem uma instância de modelo. Nessas situações, você pode passar um nome de classe para o método `can`. O nome da classe será usado para determinar qual policy usar ao autorizar a ação:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // Create the post...

        return redirect('/posts');
    }
}
```

<a id="via-the-gate-facade"></a>
### Via a Facade `Gate`

Além dos métodos úteis fornecidos ao modelo `App\Models\User`, você sempre pode autorizar ações por meio do método `authorize` da facade `Gate`.

Assim como o método `can`, esse método aceita o nome da ação que você deseja autorizar e o modelo relevante. Se a ação não for autorizada, o método `authorize` lançará uma exceção `Illuminate\Auth\Access\AuthorizationException` que o exception handler do Laravel converterá automaticamente em uma resposta HTTP com código de status 403:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // The current user can update the blog post...

        return redirect('/posts');
    }
}
```

<a id="controller-actions-that-dont-require-models"></a>
#### Ações Que Não Requerem Modelos

Conforme discutido anteriormente, alguns métodos de policy como `create` não requerem uma instância de modelo. Nessas situações, você deve passar um nome de classe para o método `authorize`. O nome da classe será usado para determinar qual policy usar ao autorizar a ação:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // The current user can create blog posts...

    return redirect('/posts');
}
```

<a id="via-middleware"></a>
### Via Middleware

O Laravel inclui um middleware que pode autorizar ações antes de a requisição recebida sequer chegar às suas rotas ou controllers. Por padrão, o middleware `Illuminate\Auth\Middleware\Authorize` pode ser anexado a uma rota usando o [middleware alias](../middleware/#middleware-aliases) `can`, que é automaticamente registrado pelo Laravel. Vamos explorar um exemplo de uso do middleware `can` para autorizar que um usuário pode atualizar um post:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

Neste exemplo, estamos passando dois argumentos ao middleware `can`. O primeiro é o nome da ação que desejamos autorizar e o segundo é o parâmetro de rota que desejamos passar para o método de policy. Neste caso, como estamos usando [implicit model binding](../routing/#implicit-binding), um modelo `App\Models\Post` será passado para o método de policy. Se o usuário não estiver autorizado a realizar a ação fornecida, uma resposta HTTP com código de status 403 será retornada pelo middleware.

Por conveniência, você também pode anexar o middleware `can` à sua rota usando o método `can`:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

Se você estiver usando [atributos de middleware de controller](../controllers/#middleware-attributes), você pode aplicar o middleware `can` por meio do atributo `Authorize`:

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;

#[Authorize('update', 'post')]
public function update(Post $post)
{
    // The current user may update the post...
}
```

<a id="middleware-actions-that-dont-require-models"></a>
#### Ações Que Não Requerem Modelos

Novamente, alguns métodos de policy como `create` não requerem uma instância de modelo. Nessas situações, você pode passar um nome de classe para o middleware. O nome da classe será usado para determinar qual policy usar ao autorizar a ação:

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

Especificar o nome completo da classe dentro de uma definição de middleware em string pode se tornar trabalhoso. Por essa razão, você pode optar por anexar o middleware `can` à sua rota usando o método `can`:

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a id="via-blade-templates"></a>
### Via Templates Blade

Ao escrever templates Blade, você pode querer exibir uma parte da página apenas se o usuário estiver autorizado a realizar uma determinada ação. Por exemplo, você pode querer mostrar um formulário de atualização para um post de blog apenas se o usuário puder realmente atualizar o post. Nessa situação, você pode usar as diretivas `@can` e `@cannot`:

```blade
@can('update', $post)
    <!-- The current user can update the post... -->
@elsecan('create', App\Models\Post::class)
    <!-- The current user can create new posts... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- The current user cannot update the post... -->
@elsecannot('create', App\Models\Post::class)
    <!-- The current user cannot create new posts... -->
@endcannot
```

Essas diretivas são atalhos convenientes para escrever instruções `@if` e `@unless`. As instruções `@can` e `@cannot` acima são equivalentes às seguintes instruções:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

Você também pode determinar se um usuário está autorizado a realizar qualquer ação a partir de um determinado array de ações. Para fazer isso, use a diretiva `@canany`:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a id="blade-actions-that-dont-require-models"></a>
#### Ações Que Não Requerem Modelos

Assim como a maioria dos outros métodos de autorização, você pode passar um nome de classe para as diretivas `@can` e `@cannot` se a ação não requerer uma instância de modelo:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```

<a id="supplying-additional-context"></a>
### Fornecendo Contexto Adicional

Ao autorizar ações usando policies, você pode passar um array como o segundo argumento para as várias funções e helpers de autorização. O primeiro elemento no array será usado para determinar qual policy deve ser invocada, enquanto o restante dos elementos do array é passado como parâmetros para o método de policy e pode ser usado para contexto adicional ao tomar decisões de autorização. Por exemplo, considere a seguinte definição de método `PostPolicy` que contém um parâmetro `$category` adicional:

```php
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

Ao tentar determinar se o usuário autenticado pode atualizar um determinado post, podemos invocar esse método de policy assim:

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // The current user can update the blog post...

    return redirect('/posts');
}
```

<a id="authorization-and-inertia"></a>
## Autorização & Inertia

Embora a autorização deva sempre ser tratada no servidor, muitas vezes pode ser conveniente fornecer à sua aplicação frontend dados de autorização para renderizar corretamente a UI da sua aplicação. O Laravel não define uma convenção obrigatória para expor informações de autorização a um frontend baseado em Inertia.

No entanto, se você estiver usando um dos [starter kits](../starter-kits/) baseados em Inertia do Laravel, a sua aplicação já contém um middleware `HandleInertiaRequests`. Dentro do método `share` desse middleware, você pode retornar dados compartilhados que serão fornecidos a todas as páginas Inertia na sua aplicação. Esses dados compartilhados podem servir como um local conveniente para definir informações de autorização para o usuário:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    // ...

    /**
     * Define the props that are shared by default.
     *
     * @return array<string, mixed>
     */
    public function share(Request $request)
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user(),
                'permissions' => [
                    'post' => [
                        'create' => $request->user()->can('create', Post::class),
                    ],
                ],
            ],
        ];
    }
}
```
