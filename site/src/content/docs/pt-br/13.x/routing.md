---
title: "Roteamento"
---

- [Roteamento Básico](#basic-routing)
    - [Os Arquivos de Rota Padrão](#the-default-route-files)
    - [Rotas de Redirecionamento](#redirect-routes)
    - [Rotas de View](#view-routes)
    - [Listando Suas Rotas](#listing-your-routes)
    - [Personalização de Roteamento](#routing-customization)
- [Parâmetros de Rota](#route-parameters)
    - [Parâmetros Obrigatórios](#required-parameters)
    - [Parâmetros Opcionais](#parameters-optional-parameters)
    - [Restrições com Expressões Regulares](#parameters-regular-expression-constraints)
- [Rotas Nomeadas](#named-routes)
- [Grupos de Rotas](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Controllers](#route-group-controllers)
    - [Roteamento de Subdomínio](#route-group-subdomain-routing)
    - [Prefixos de Rota](#route-group-prefixes)
    - [Prefixos de Nome de Rota](#route-group-name-prefixes)
- [Vinculação de Modelo de Rota](#route-model-binding)
    - [Vinculação Implícita](#implicit-binding)
    - [Vinculação Implícita de Enum](#implicit-enum-binding)
    - [Vinculação Explícita](#explicit-binding)
- [Rotas de Fallback](#fallback-routes)
- [Limitação de Taxa (Rate Limiting)](#rate-limiting)
    - [Definindo Limitadores de Taxa](#defining-rate-limiters)
    - [Anexando Limitadores de Taxa às Rotas](#attaching-rate-limiters-to-routes)
- [Falsificação de Método de Formulário](#form-method-spoofing)
- [Acessando a Rota Atual](#accessing-the-current-route)
- [Compartilhamento de Recursos entre Origens (CORS)](#cors)
- [Cache de Rotas](#route-caching)

<a id="basic-routing"></a>
## Roteamento Básico

As rotas mais básicas do Laravel aceitam uma URI e uma closure, fornecendo um método muito simples e expressivo de definir rotas e comportamento sem arquivos de configuração de roteamento complicados:

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a id="the-default-route-files"></a>
### Os Arquivos de Rota Padrão

Todas as rotas do Laravel são definidas nos seus arquivos de rota, que estão localizados no diretório `routes`. Esses arquivos são carregados automaticamente pelo Laravel usando a configuração especificada no arquivo `bootstrap/app.php` da sua aplicação. O arquivo `routes/web.php` define as rotas que são para sua interface web. Essas rotas são atribuídas ao [grupo de middleware](../middleware/#laravels-default-middleware-groups) `web`, que fornece funcionalidades como estado de sessão e proteção CSRF.

Para a maioria das aplicações, você começará definindo rotas no seu arquivo `routes/web.php`. As rotas definidas em `routes/web.php` podem ser acessadas digitando a URL da rota definida no seu navegador. Por exemplo, você pode acessar a seguinte rota navegando para `http://example.com/user` no seu navegador:

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a id="api-routes"></a>
#### Rotas de API

Se sua aplicação também oferecer uma API stateless, você pode habilitar o roteamento de API usando o comando Artisan `install:api`:

```shell
php artisan install:api
```

O comando `install:api` instala o [Laravel Sanctum](../sanctum/), que fornece um guard de autenticação de token de API robusto, porém simples, que pode ser usado para autenticar consumidores de API de terceiros, SPAs ou aplicações móveis. Além disso, o comando `install:api` cria o arquivo `routes/api.php`:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

É claro, você está livre para omitir o middleware `auth:sanctum` em rotas que devem ser acessíveis publicamente.

As rotas em `routes/api.php` são stateless e são atribuídas ao [grupo de middleware](../middleware/#laravels-default-middleware-groups) `api`. Além disso, o prefixo de URI `/api` é automaticamente aplicado a essas rotas, então você não precisa aplicá-lo manualmente a cada rota no arquivo. Você pode alterar o prefixo modificando o arquivo `bootstrap/app.php` da sua aplicação:

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a id="available-router-methods"></a>
#### Métodos de Router Disponíveis

O router permite que você registre rotas que respondem a qualquer verbo HTTP:

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
Route::query($uri, $callback);
```

O método `query` registra uma rota que responde ao verbo HTTP `QUERY`, permitindo que clientes enviem um corpo de requisição para uma consulta. Rotas `QUERY` no grupo de middleware `web` estão sujeitas à [proteção CSRF](../csrf/).

Às vezes você pode precisar registrar uma rota que responde a múltiplos verbos HTTP. Você pode fazer isso usando o método `match`. Ou, você pode até registrar uma rota que responde a todos os verbos HTTP, incluindo `QUERY`, usando o método `any`:

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> **Nota:**
> Ao definir múltiplas rotas que compartilham a mesma URI, rotas usando os métodos `get`, `post`, `put`, `patch`, `delete`, `options` e `query` devem ser definidas antes das rotas que usam os métodos `any`, `match` e `redirect`. Isso garante que a requisição recebida seja correspondida com a rota correta.

<a id="dependency-injection"></a>
#### Injeção de Dependência

Você pode fazer type-hint de quaisquer dependências exigidas pela sua rota na assinatura da callback da sua rota. As dependências declaradas serão automaticamente resolvidas e injetadas na callback pelo [service container](../container/) do Laravel. Por exemplo, você pode fazer type-hint da classe `Illuminate\Http\Request` para ter a requisição HTTP atual automaticamente injetada na callback da sua rota:

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a id="csrf-protection"></a>
#### Proteção CSRF

Lembre-se, quaisquer formulários HTML apontando para rotas `POST`, `PUT`, `PATCH` ou `DELETE` que são definidas no arquivo de rotas `web` devem incluir um campo de token CSRF. Caso contrário, a requisição será rejeitada. Você pode ler mais sobre proteção CSRF na [documentação de CSRF](../csrf/):

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a id="redirect-routes"></a>
### Rotas de Redirecionamento

Se você está definindo uma rota que redireciona para outra URI, você pode usar o método `Route::redirect`. Este método fornece um atalho conveniente para que você não tenha que definir uma rota ou controller completo para realizar um redirecionamento simples:

```php
Route::redirect('/here', '/there');
```

Por padrão, `Route::redirect` retorna um código de status `302`. Você pode personalizar o código de status usando o terceiro parâmetro opcional:

```php
Route::redirect('/here', '/there', 301);
```

Ou, você pode usar o método `Route::permanentRedirect` para retornar um código de status `301`:

```php
Route::permanentRedirect('/here', '/there');
```

> **Aviso:**
> Ao usar parâmetros de rota em rotas de redirecionamento, os seguintes parâmetros são reservados pelo Laravel e não podem ser usados: `destination` e `status`.

<a id="view-routes"></a>
### Rotas de View

Se sua rota só precisa retornar uma [view](../views/), você pode usar o método `Route::view`. Assim como o método `redirect`, este método fornece um atalho simples para que você não tenha que definir uma rota ou controller completo. O método `view` aceita uma URI como seu primeiro argumento e um nome de view como seu segundo argumento. Além disso, você pode fornecer um array de dados para passar para a view como um terceiro argumento opcional:

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> **Aviso:**
> Ao usar parâmetros de rota em rotas de view, os seguintes parâmetros são reservados pelo Laravel e não podem ser usados: `view`, `data`, `status` e `headers`.

<a id="listing-your-routes"></a>
### Listando Suas Rotas

O comando Artisan `route:list` pode facilmente fornecer uma visão geral de todas as rotas que são definidas pela sua aplicação:

```shell
php artisan route:list
```

Por padrão, o middleware de rota que é atribuído a cada rota não será exibido na saída do `route:list`; no entanto, você pode instruir o Laravel a exibir o middleware de rota e os nomes dos grupos de middleware adicionando a opção `-v` ao comando:

```shell
php artisan route:list -v

# Expand middleware groups...
php artisan route:list -vv
```

Você também pode instruir o Laravel a mostrar apenas rotas cuja URI contém uma string fornecida:

```shell
php artisan route:list --path=api
```

Além disso, você pode instruir o Laravel a ocultar quaisquer rotas que são definidas por pacotes de terceiros fornecendo a opção `--except-vendor` ao executar o comando `route:list`:

```shell
php artisan route:list --except-vendor
```

Da mesma forma, você também pode instruir o Laravel a mostrar apenas rotas que são definidas por pacotes de terceiros fornecendo a opção `--only-vendor` ao executar o comando `route:list`:

```shell
php artisan route:list --only-vendor
```

<a id="routing-customization"></a>
### Personalização de Roteamento

Por padrão, as rotas da sua aplicação são configuradas e carregadas pelo arquivo `bootstrap/app.php`:

```php
<?php

use Illuminate\Foundation\Application;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )->create();
```

No entanto, às vezes você pode querer definir um arquivo inteiramente novo para conter um subconjunto das rotas da sua aplicação. Para isso, você pode fornecer uma closure `then` ao método `withRouting`. Dentro dessa closure, você pode registrar quaisquer rotas adicionais que são necessárias para sua aplicação:

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
    then: function () {
        Route::middleware('api')
            ->prefix('webhooks')
            ->name('webhooks.')
            ->group(base_path('routes/webhooks.php'));
    },
)
```

Ou, você pode até assumir controle total sobre o registro de rotas fornecendo uma closure `using` ao método `withRouting`. Quando este argumento é passado, nenhuma rota HTTP será registrada pelo framework e você é responsável por registrar manualmente todas as rotas:

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    commands: __DIR__.'/../routes/console.php',
    using: function () {
        Route::middleware('api')
            ->prefix('api')
            ->group(base_path('routes/api.php'));

        Route::middleware('web')
            ->group(base_path('routes/web.php'));
    },
)
```

<a id="route-parameters"></a>
## Parâmetros de Rota

<a id="required-parameters"></a>
### Parâmetros Obrigatórios

Às vezes você precisará capturar segmentos da URI dentro da sua rota. Por exemplo, você pode precisar capturar o ID de um usuário a partir da URL. Você pode fazer isso definindo parâmetros de rota:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

Você pode definir quantos parâmetros de rota forem necessários para sua rota:

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

Os parâmetros de rota são sempre envolvidos entre chaves `{}` e devem consistir em caracteres alfabéticos. Underscores (`_`) também são aceitáveis dentro de nomes de parâmetros de rota. Os parâmetros de rota são injetados nas callbacks / controllers de rota com base na sua ordem - os nomes dos argumentos da callback / controller de rota não importam.

<a id="parameters-and-dependency-injection"></a>
#### Parâmetros e Injeção de Dependência

Se sua rota tem dependências que você gostaria que o service container do Laravel injetasse automaticamente na callback da sua rota, você deve listar seus parâmetros de rota após suas dependências:

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a id="parameters-optional-parameters"></a>
### Parâmetros Opcionais

Ocasionalmente você pode precisar especificar um parâmetro de rota que pode nem sempre estar presente na URI. Você pode fazer isso colocando uma marca `?` após o nome do parâmetro. Certifique-se de dar à variável correspondente da rota um valor padrão:

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a id="parameters-regular-expression-constraints"></a>
### Restrições com Expressões Regulares

Você pode restringir o formato dos seus parâmetros de rota usando o método `where` em uma instância de rota. O método `where` aceita o nome do parâmetro e uma expressão regular que define como o parâmetro deve ser restringido:

```php
Route::get('/user/{name}', function (string $name) {
    // ...
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function (string $id) {
    // ...
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

Por conveniência, alguns padrões de expressão regular comumente usados têm métodos auxiliares que permitem que você adicione rapidamente restrições de padrão às suas rotas:

```php
Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function (string $name) {
    // ...
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUuid('id');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUlid('id');

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', ['movie', 'song', 'painting']);

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', CategoryEnum::cases());
```

Se a requisição recebida não corresponder às restrições de padrão da rota, uma resposta HTTP 404 será retornada.

<a id="parameters-global-constraints"></a>
#### Restrições Globais

Se você gostaria que um parâmetro de rota fosse sempre restringido por uma determinada expressão regular, você pode usar o método `pattern`. Você deve definir esses padrões no método `boot` da classe `App\Providers\AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

Uma vez que o padrão tenha sido definido, ele é automaticamente aplicado a todas as rotas usando aquele nome de parâmetro:

```php
Route::get('/user/{id}', function (string $id) {
    // Only executed if {id} is numeric...
});
```

<a id="parameters-encoded-forward-slashes"></a>
#### Barras Codificadas

O componente de roteamento do Laravel permite que todos os caracteres, exceto `/`, estejam presentes dentro dos valores dos parâmetros de rota. Você deve permitir explicitamente que `/` seja parte do seu placeholder usando uma expressão regular de condição `where`:

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> **Aviso:**
> Barras codificadas só são suportadas dentro do último segmento da rota.

<a id="named-routes"></a>
## Rotas Nomeadas

Rotas nomeadas permitem a geração conveniente de URLs ou redirecionamentos para rotas específicas. Você pode especificar um nome para uma rota encadeando o método `name` na definição da rota:

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

Você também pode especificar nomes de rota para ações de controller:

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> **Aviso:**
> Nomes de rota devem sempre ser únicos.

<a id="generating-urls-to-named-routes"></a>
#### Gerando URLs para Rotas Nomeadas

Uma vez que você tenha atribuído um nome a uma determinada rota, você pode usar o nome da rota ao gerar URLs ou redirecionamentos por meio das funções auxiliares `route` e `redirect` do Laravel:

```php
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');

return to_route('profile');
```

Se a rota nomeada define parâmetros, você pode passar os parâmetros como o segundo argumento para a função `route`. Os parâmetros fornecidos serão automaticamente inseridos na URL gerada em suas posições corretas:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

Se você passar parâmetros adicionais no array, esses pares de chave / valor serão automaticamente adicionados à query string da URL gerada:

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> **Nota:**
> Às vezes, você pode desejar especificar valores padrão abrangentes à requisição para parâmetros de URL, como o locale atual. Para isso, você pode usar o [método URL::defaults](../urls/#default-values).

<a id="inspecting-the-current-route"></a>
#### Inspecionando a Rota Atual

Se você gostaria de determinar se a requisição atual foi roteada para uma determinada rota nomeada, você pode usar o método `named` em uma instância de Route. Por exemplo, você pode verificar o nome da rota atual a partir de um middleware de rota:

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Handle an incoming request.
 *
 * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
 */
public function handle(Request $request, Closure $next): Response
{
    if ($request->route()->named('profile')) {
        // ...
    }

    return $next($request);
}
```

<a id="route-groups"></a>
## Grupos de Rotas

Grupos de rotas permitem que você compartilhe atributos de rota, como middleware, entre um grande número de rotas sem precisar definir esses atributos em cada rota individual.

Grupos aninhados tentam de forma inteligente "mesclar" atributos com seu grupo pai. Middleware e condições `where` são mesclados, enquanto nomes e prefixos são anexados. Delimitadores de namespace e barras em prefixos de URI são automaticamente adicionados onde apropriado.

<a id="route-group-middleware"></a>
### Middleware

Para atribuir [middleware](../middleware/) a todas as rotas dentro de um grupo, você pode usar o método `middleware` antes de definir o grupo. O middleware é executado na ordem em que está listado no array:

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // Uses first & second middleware...
    });

    Route::get('/user/profile', function () {
        // Uses first & second middleware...
    });
});
```

<a id="route-group-controllers"></a>
### Controllers

Se um grupo de rotas utiliza o mesmo [controller](../controllers/), você pode usar o método `controller` para definir o controller comum para todas as rotas dentro do grupo. Então, ao definir as rotas, você só precisa fornecer o método do controller que elas invocam:

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a id="route-group-subdomain-routing"></a>
### Roteamento de Subdomínio

Grupos de rotas também podem ser usados para lidar com roteamento de subdomínio. Subdomínios podem receber parâmetros de rota assim como URIs de rota, permitindo que você capture uma parte do subdomínio para uso na sua rota ou controller. O subdomínio pode ser especificado chamando o método `domain` antes de definir o grupo:

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a id="route-group-prefixes"></a>
### Prefixos de Rota

O método `prefix` pode ser usado para prefixar cada rota no grupo com uma determinada URI. Por exemplo, você pode querer prefixar todas as URIs de rota dentro do grupo com `admin`:

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a id="route-group-name-prefixes"></a>
### Prefixos de Nome de Rota

O método `name` pode ser usado para prefixar cada nome de rota no grupo com uma determinada string. Por exemplo, você pode querer prefixar os nomes de todas as rotas no grupo com `admin`. A string fornecida é prefixada ao nome da rota exatamente como é especificada, então teremos o cuidado de fornecer o caractere `.` final no prefixo:

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a id="route-model-binding"></a>
## Vinculação de Modelo de Rota

Ao injetar um ID de modelo em uma rota ou ação de controller, você frequentemente consultará o banco de dados para recuperar o modelo que corresponde àquele ID. A vinculação de modelo de rota do Laravel fornece uma maneira conveniente de injetar automaticamente as instâncias de modelo diretamente nas suas rotas. Por exemplo, em vez de injetar o ID de um usuário, você pode injetar a instância inteira do modelo `User` que corresponde ao ID fornecido.

<a id="implicit-binding"></a>
### Vinculação Implícita

O Laravel resolve automaticamente modelos Eloquent definidos em rotas ou ações de controller cujos nomes de variáveis com type-hint correspondem a um nome de segmento de rota. Por exemplo:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

Como a variável `$user` tem type-hint do modelo Eloquent `App\Models\User` e o nome da variável corresponde ao segmento de URI `{user}`, o Laravel injetará automaticamente a instância de modelo que tem um ID correspondente ao valor correspondente da URI da requisição. Se uma instância de modelo correspondente não for encontrada no banco de dados, uma resposta HTTP 404 será gerada automaticamente.

É claro, a vinculação implícita também é possível ao usar métodos de controller. Novamente, observe que o segmento de URI `{user}` corresponde à variável `$user` no controller que contém um type-hint `App\Models\User`:

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// Route definition...
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller method definition...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a id="implicit-soft-deleted-models"></a>
#### Modelos Soft Deleted

Tipicamente, a vinculação implícita de modelo não recuperará modelos que foram [soft deleted](../eloquent/#soft-deleting). No entanto, você pode instruir a vinculação implícita a recuperar esses modelos encadeando o método `withTrashed` na definição da sua rota:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a id="customizing-the-default-key-name"></a>
#### Personalizando a Chave

Às vezes você pode desejar resolver modelos Eloquent usando uma coluna diferente de `id`. Para fazer isso, você pode especificar a coluna na definição do parâmetro de rota:

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

Se você gostaria que a vinculação de modelo sempre usasse uma coluna de banco de dados diferente de `id` ao recuperar uma determinada classe de modelo, você pode aplicar o atributo `RouteKey` ao modelo Eloquent:

```php
use Illuminate\Database\Eloquent\Attributes\RouteKey;
use Illuminate\Database\Eloquent\Model;

#[RouteKey('slug')]
class Post extends Model
{
    // ...
}
```

<a id="implicit-model-binding-scoping"></a>
#### Chaves Personalizadas e Escopo

Ao vincular implicitamente múltiplos modelos Eloquent em uma única definição de rota, você pode desejar restringir o escopo do segundo modelo Eloquent de modo que ele deva ser um filho do modelo Eloquent anterior. Por exemplo, considere esta definição de rota que recupera um post de blog por slug para um usuário específico:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

Ao usar uma vinculação implícita com chave personalizada como um parâmetro de rota aninhado, o Laravel automaticamente restringirá o escopo da consulta para recuperar o modelo aninhado por seu pai usando convenções para adivinhar o nome do relacionamento no pai. Neste caso, será assumido que o modelo `User` tem um relacionamento chamado `posts` (a forma plural do nome do parâmetro de rota) que pode ser usado para recuperar o modelo `Post`.

Se desejar, você pode instruir o Laravel a restringir o escopo das vinculações "filho" mesmo quando uma chave personalizada não é fornecida. Para fazer isso, você pode invocar o método `scopeBindings` ao definir sua rota:

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

Ou, você pode instruir um grupo inteiro de definições de rota a usar vinculações com escopo:

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

De forma similar, você pode instruir explicitamente o Laravel a não restringir o escopo das vinculações invocando o método `withoutScopedBindings`:

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a id="customizing-missing-model-behavior"></a>
#### Personalizando o Comportamento de Modelo Ausente

Tipicamente, uma resposta HTTP 404 será gerada se um modelo vinculado implicitamente não for encontrado. No entanto, você pode personalizar esse comportamento chamando o método `missing` ao definir sua rota. O método `missing` aceita uma closure que será invocada se um modelo vinculado implicitamente não puder ser encontrado:

```php
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->name('locations.view')
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

<a id="implicit-enum-binding"></a>
### Vinculação Implícita de Enum

O PHP 8.1 introduziu suporte para [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). Para complementar essa funcionalidade, o Laravel permite que você faça type-hint de um [Enum com backing de string](https://www.php.net/manual/en/language.enumerations.backed.php) na sua definição de rota e o Laravel só invocará a rota se aquele segmento de rota corresponder a um valor de Enum válido. Caso contrário, uma resposta HTTP 404 será retornada automaticamente. Por exemplo, dado o seguinte Enum:

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

Você pode definir uma rota que só será invocada se o segmento de rota `{category}` for `fruits` ou `people`. Caso contrário, o Laravel retornará uma resposta HTTP 404:

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a id="explicit-binding"></a>
### Vinculação Explícita

Você não é obrigado a usar a resolução de modelo implícita e baseada em convenção do Laravel para usar vinculação de modelo. Você também pode definir explicitamente como os parâmetros de rota correspondem a modelos. Para registrar uma vinculação explícita, use o método `model` do router para especificar a classe para um determinado parâmetro. Você deve definir suas vinculações de modelo explícitas no início do método `boot` da sua classe `AppServiceProvider`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

Em seguida, defina uma rota que contém um parâmetro `{user}`:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

Como vinculamos todos os parâmetros `{user}` ao modelo `App\Models\User`, uma instância dessa classe será injetada na rota. Então, por exemplo, uma requisição para `users/1` injetará a instância de `User` do banco de dados que tem um ID de `1`.

Se uma instância de modelo correspondente não for encontrada no banco de dados, uma resposta HTTP 404 será gerada automaticamente.

<a id="customizing-the-resolution-logic"></a>
#### Personalizando a Lógica de Resolução

Se você deseja definir sua própria lógica de resolução de vinculação de modelo, você pode usar o método `Route::bind`. A closure que você passa para o método `bind` receberá o valor do segmento de URI e deve retornar a instância da classe que deve ser injetada na rota. Novamente, essa personalização deve ocorrer no método `boot` do `AppServiceProvider` da sua aplicação:

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

Alternativamente, você pode sobrescrever o método `resolveRouteBinding` no seu modelo Eloquent. Este método receberá o valor do segmento de URI e deve retornar a instância da classe que deve ser injetada na rota:

```php
/**
 * Retrieve the model for a bound value.
 *
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

Se uma rota está utilizando [escopo de vinculação implícita](#implicit-model-binding-scoping), o método `resolveChildRouteBinding` será usado para resolver a vinculação filha do modelo pai:

```php
/**
 * Retrieve the child model for a bound value.
 *
 * @param  string  $childType
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

<a id="fallback-routes"></a>
## Rotas de Fallback

Usando o método `Route::fallback`, você pode definir uma rota que será executada quando nenhuma outra rota corresponder à requisição recebida. Tipicamente, requisições não tratadas renderizarão automaticamente uma página "404" por meio do manipulador de exceções da sua aplicação. No entanto, como você tipicamente definiria a rota `fallback` dentro do seu arquivo `routes/web.php`, todo o middleware no grupo de middleware `web` se aplicará à rota. Você está livre para adicionar middleware adicional a esta rota conforme necessário:

```php
Route::fallback(function () {
    // ...
});
```

<a id="rate-limiting"></a>
## Limitação de Taxa (Rate Limiting)

<a id="defining-rate-limiters"></a>
### Definindo Limitadores de Taxa

O Laravel inclui serviços de limitação de taxa poderosos e personalizáveis que você pode utilizar para restringir a quantidade de tráfego para uma determinada rota ou grupo de rotas. Para começar, você deve definir configurações de limitador de taxa que atendam às necessidades da sua aplicação.

Limitadores de taxa podem ser definidos dentro do método `boot` da classe `App\Providers\AppServiceProvider` da sua aplicação:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

Limitadores de taxa são definidos usando o método `for` do facade `RateLimiter`. O método `for` aceita um nome de limitador de taxa e uma closure que retorna a configuração de limite que deve se aplicar às rotas que são atribuídas ao limitador de taxa. As configurações de limite são instâncias da classe `Illuminate\Cache\RateLimiting\Limit`. Esta classe contém métodos "builder" úteis para que você possa definir rapidamente seu limite. O nome do limitador de taxa pode ser qualquer string que você desejar:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

Se a requisição recebida exceder o limite de taxa especificado, uma resposta com código de status HTTP 429 será automaticamente retornada pelo Laravel. Se você gostaria de definir sua própria resposta que deve ser retornada por um limite de taxa, você pode usar o método `response`:

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

Como as callbacks de limitador de taxa recebem a instância da requisição HTTP recebida, você pode construir o limite de taxa apropriado dinamicamente com base na requisição recebida ou no usuário autenticado:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()?->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a id="segmenting-rate-limits"></a>
#### Segmentando Limites de Taxa

Às vezes você pode desejar segmentar limites de taxa por algum valor arbitrário. Por exemplo, você pode desejar permitir que os usuários acessem uma determinada rota 100 vezes por minuto por endereço IP. Para isso, você pode usar o método `by` ao construir seu limite de taxa:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

Para ilustrar essa funcionalidade usando outro exemplo, podemos limitar o acesso à rota a 100 vezes por minuto por ID de usuário autenticado ou 10 vezes por minuto por endereço IP para visitantes:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a id="multiple-rate-limits"></a>
#### Múltiplos Limites de Taxa

Se necessário, você pode retornar um array de limites de taxa para uma determinada configuração de limitador de taxa. Cada limite de taxa será avaliado para a rota com base na ordem em que são colocados dentro do array:

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

Se você está atribuindo múltiplos limites de taxa segmentados por valores `by` idênticos, você deve garantir que cada valor `by` seja único. A maneira mais fácil de conseguir isso é prefixar os valores fornecidos ao método `by`:

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a id="response-base-rate-limiting"></a>
#### Limitação de Taxa Baseada em Resposta

Além de limitar a taxa de requisições recebidas, o Laravel permite que você limite a taxa com base na resposta usando o método `after`. Isso é útil quando você só quer contar certas respostas para o limite de taxa, como erros de validação, respostas 404 ou outros códigos de status HTTP específicos.

O método `after` aceita uma closure que recebe a resposta e deve retornar `true` se a resposta deve ser contada para o limite de taxa, ou `false` se ela deve ser ignorada. Isso é particularmente útil para prevenir ataques de enumeração limitando respostas 404 consecutivas, ou permitindo que usuários tentem novamente requisições que falham na validação sem esgotar seu limite de taxa em um endpoint que só deve limitar operações bem-sucedidas:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // Only count 404 responses toward the rate limit to prevent enumeration...
            return $response->status() === 404;
        });
});
```

<a id="attaching-rate-limiters-to-routes"></a>
### Anexando Limitadores de Taxa às Rotas

Limitadores de taxa podem ser anexados a rotas ou grupos de rotas usando o [middleware](../middleware/) `throttle`. O middleware throttle aceita o nome do limitador de taxa que você deseja atribuir à rota:

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        // ...
    });

    Route::post('/video', function () {
        // ...
    });
});
```

<a id="throttling-with-redis"></a>
#### Throttling Com Redis

Por padrão, o middleware `throttle` é mapeado para a classe `Illuminate\Routing\Middleware\ThrottleRequests`. No entanto, se você está usando o Redis como o driver de cache da sua aplicação, você pode desejar instruir o Laravel a usar o Redis para gerenciar a limitação de taxa. Para fazer isso, você deve usar o método `throttleWithRedis` no arquivo `bootstrap/app.php` da sua aplicação. Este método mapeia o middleware `throttle` para a classe de middleware `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a id="form-method-spoofing"></a>
## Falsificação de Método de Formulário

Formulários HTML não suportam ações `PUT`, `PATCH` ou `DELETE`. Então, ao definir rotas `PUT`, `PATCH` ou `DELETE` que são chamadas a partir de um formulário HTML, você precisará adicionar um campo `_method` oculto ao formulário. O valor enviado com o campo `_method` será usado como o método da requisição HTTP:

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

Por conveniência, você pode usar a [diretiva Blade](../blade/) `@method` para gerar o campo de input `_method`:

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a id="accessing-the-current-route"></a>
## Acessando a Rota Atual

Você pode usar os métodos `current`, `currentRouteName` e `currentRouteAction` no facade `Route` para acessar informações sobre a rota que está lidando com a requisição recebida:

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

Você pode consultar a documentação da API tanto para a [classe subjacente do facade Route](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Routing/Router.html) quanto para a [instância de Route](https://api.laravel.comhttps://laravel.com/docs/13.x/Illuminate/Routing/Route.html) para revisar todos os métodos que estão disponíveis nas classes router e route.

<a id="cors"></a>
## Compartilhamento de Recursos entre Origens (CORS)

O Laravel pode responder automaticamente a requisições HTTP `OPTIONS` de CORS com valores que você configura. As requisições `OPTIONS` serão automaticamente tratadas pelo [middleware](../middleware/) `HandleCors` que é automaticamente incluído na pilha de middleware global da sua aplicação.

Às vezes, você pode precisar personalizar os valores de configuração de CORS para sua aplicação. Você pode fazer isso publicando o arquivo de configuração `cors` usando o comando Artisan `config:publish`:

```shell
php artisan config:publish cors
```

Este comando colocará um arquivo de configuração `cors.php` dentro do diretório `config` da sua aplicação.

> **Nota:**
> Para mais informações sobre CORS e cabeçalhos CORS, por favor consulte a [documentação web da MDN sobre CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers).

<a id="route-caching"></a>
## Cache de Rotas

Ao implantar sua aplicação em produção, você deve aproveitar o cache de rotas do Laravel. Usar o cache de rotas diminuirá drasticamente a quantidade de tempo que leva para registrar todas as rotas da sua aplicação. Para gerar um cache de rotas, execute o comando Artisan `route:cache`:

```shell
php artisan route:cache
```

Após executar este comando, seu arquivo de rotas em cache será carregado em cada requisição. Lembre-se, se você adicionar quaisquer novas rotas, você precisará gerar um novo cache de rotas. Por causa disso, você só deve executar o comando `route:cache` durante a implantação do seu projeto.

Você pode usar o comando `route:clear` para limpar o cache de rotas:

```shell
php artisan route:clear
```
