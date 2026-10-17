---
title: "Controllers"
---

- [Introdução](#introduction)
- [Escrevendo Controllers](#writing-controllers)
    - [Controllers Básicos](#basic-controllers)
    - [Controllers de Ação Única](#single-action-controllers)
- [Middleware de Controller](#controller-middleware)
    - [Atributos de Middleware](#middleware-attributes)
    - [Atributos de Autorização](#authorization-attributes)
- [Controllers de Recurso](#resource-controllers)
    - [Rotas de Recurso Parciais](#restful-partial-resource-routes)
    - [Recursos Aninhados](#restful-nested-resources)
    - [Nomeando Rotas de Recurso](#restful-naming-resource-routes)
    - [Nomeando Parâmetros de Rota de Recurso](#restful-naming-resource-route-parameters)
    - [Aplicando Escopo a Rotas de Recurso](#restful-scoping-resource-routes)
    - [Localizando URIs de Recurso](#restful-localizing-resource-uris)
    - [Complementando Controllers de Recurso](#restful-supplementing-resource-controllers)
    - [Controllers de Recurso Singleton](#singleton-resource-controllers)
    - [Middleware e Controllers de Recurso](#middleware-and-resource-controllers)
- [Injeção de Dependência e Controllers](#dependency-injection-and-controllers)

<a id="introduction"></a>
## Introdução

Em vez de definir toda a sua lógica de tratamento de requisições como closures nos seus arquivos de rota, você pode desejar organizar esse comportamento usando classes "controller". Controllers podem agrupar lógica de tratamento de requisições relacionada em uma única classe. Por exemplo, uma classe `UserController` pode lidar com todas as requisições recebidas relacionadas a usuários, incluindo exibir, criar, atualizar e excluir usuários. Por padrão, os controllers são armazenados no diretório `app/Http/Controllers`.

<a id="writing-controllers"></a>
## Escrevendo Controllers

<a id="basic-controllers"></a>
### Controllers Básicos

Para gerar rapidamente um novo controller, você pode executar o comando Artisan `make:controller`. Por padrão, todos os controllers da sua aplicação são armazenados no diretório `app/Http/Controllers`:

```shell
php artisan make:controller UserController
```

Vamos dar uma olhada em um exemplo de um controller básico. Um controller pode ter qualquer número de métodos públicos que responderão às requisições HTTP recebidas:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Uma vez que você tenha escrito uma classe e um método de controller, você pode definir uma rota para o método do controller assim:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

Quando uma requisição recebida corresponde à URI de rota especificada, o método `show` na classe `App\Http\Controllers\UserController` será invocado e os parâmetros de rota serão passados para o método.

> **Nota:**
> Controllers **não são obrigados** a estender uma classe base. No entanto, às vezes é conveniente estender uma classe de controller base que contém métodos que devem ser compartilhados entre todos os seus controllers.

<a id="single-action-controllers"></a>
### Controllers de Ação Única

Se uma ação de controller é particularmente complexa, você pode achar conveniente dedicar uma classe de controller inteira a essa ação única. Para isso, você pode definir um único método `__invoke` dentro do controller:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     */
    public function __invoke()
    {
        // ...
    }
}
```

Ao registrar rotas para controllers de ação única, você não precisa especificar um método do controller. Em vez disso, você pode simplesmente passar o nome do controller para o router:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

Você pode gerar um controller invocável usando a opção `--invokable` do comando Artisan `make:controller`:

```shell
php artisan make:controller ProvisionServer --invokable
```

> **Nota:**
> Os stubs de controller podem ser personalizados usando [publicação de stubs](../artisan/#stub-customization).

<a id="controller-middleware"></a>
## Middleware de Controller

[Middleware](../middleware/) pode ser atribuído às rotas do controller nos seus arquivos de rota:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

Ou, você pode achar conveniente especificar middleware dentro da sua classe de controller. Para fazer isso, seu controller deve implementar a interface `HasMiddleware`, que determina que o controller deve ter um método estático `middleware`. A partir desse método, você pode retornar um array de middleware que deve ser aplicado às ações do controller:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    /**
     * Get the middleware that should be assigned to the controller.
     */
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }

    // ...
}
```

Você também pode definir middleware de controller como closures, o que fornece uma maneira conveniente de definir um middleware inline sem escrever uma classe de middleware inteira:

```php
use Closure;
use Illuminate\Http\Request;

/**
 * Get the middleware that should be assigned to the controller.
 */
public static function middleware(): array
{
    return [
        function (Request $request, Closure $next) {
            return $next($request);
        },
    ];
}
```

<a id="middleware-attributes"></a>
### Atributos de Middleware

Você também pode atribuir middleware a controllers usando atributos PHP:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
#[Middleware('log', only: ['index'])]
#[Middleware('subscribed', except: ['store'])]
class UserController
{
    // ...
}
```

Você pode colocar atributos de middleware em métodos individuais do controller também. Middleware atribuído a métodos será mesclado com o middleware atribuído no nível da classe:

```php
<?php

namespace App\Http\Controllers;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class UserController
{
    #[Middleware('log')]
    #[Middleware('subscribed')]
    public function index()
    {
        // ...
    }

    #[Middleware(static function (Request $request, Closure $next) {
        // ...

        return $next($request);
    })]
    public function store()
    {
        // ...
    }
}
```

Para excluir middleware de um controller ou de métodos individuais do controller, use o atributo `WithoutMiddleware`. Você pode usar os argumentos `only` e `except` para limitar um atributo de nível de classe a métodos específicos do controller:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Middleware\EnsureTokenIsValid;
use Illuminate\Routing\Attributes\Controllers\WithoutMiddleware;

#[WithoutMiddleware('subscribed', except: ['index'])]
class UserController
{
    #[WithoutMiddleware(EnsureTokenIsValid::class)]
    public function index()
    {
        // ...
    }

    public function show()
    {
        // ...
    }
}
```

Atributos `WithoutMiddleware` de nível de classe são herdados por controllers filhos. O atributo só pode remover middleware de rota e não se aplica a [middleware global](../middleware/#global-middleware).

<a id="authorization-attributes"></a>
### Atributos de Autorização

Se você está autorizando ações de controller por meio de policies, você pode usar o atributo `Authorize` como um atalho conveniente para o middleware `can`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;

class CommentController
{
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }

    #[Authorize('delete', 'comment')]
    public function destroy(Comment $comment)
    {
        // ...
    }
}
```

O primeiro argumento é a ability que você deseja autorizar. O segundo argumento é a classe de modelo, o parâmetro de rota, ou os parâmetros que devem ser passados para a policy.

<a id="resource-controllers"></a>
## Controllers de Recurso

Se você pensar em cada modelo Eloquent na sua aplicação como um "recurso", é típico realizar os mesmos conjuntos de ações contra cada recurso na sua aplicação. Por exemplo, imagine que sua aplicação contém um modelo `Photo` e um modelo `Movie`. É provável que os usuários possam criar, ler, atualizar ou excluir esses recursos.

Por causa desse caso de uso comum, o roteamento de recurso do Laravel atribui as rotas típicas de criar, ler, atualizar e excluir ("CRUD") a um controller com uma única linha de código. Para começar, podemos usar a opção `--resource` do comando Artisan `make:controller` para criar rapidamente um controller para lidar com essas ações:

```shell
php artisan make:controller PhotoController --resource
```

Este comando gerará um controller em `app/Http/Controllers/PhotoController.php`. O controller conterá um método para cada uma das operações de recurso disponíveis. Em seguida, você pode registrar uma rota de recurso que aponta para o controller:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

Esta única declaração de rota cria múltiplas rotas para lidar com uma variedade de ações no recurso. O controller gerado já terá métodos esboçados para cada uma dessas ações. Lembre-se, você sempre pode obter uma visão geral rápida das rotas da sua aplicação executando o comando Artisan `route:list`.

Você pode até registrar vários controllers de recurso de uma vez passando um array ao método `resources`:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

O método `softDeletableResources` registra vários controllers de recurso que todos usam o método `withTrashed`:

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a id="actions-handled-by-resource-controllers"></a>
#### Ações Tratadas por Controllers de Recurso

<div class="overflow-auto">

| Verbo     | URI                    | Ação    | Nome da Rota   |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

</div>

<a id="customizing-missing-model-behavior"></a>
#### Personalizando o Comportamento de Modelo Ausente

Tipicamente, uma resposta HTTP 404 será gerada se um modelo de recurso vinculado implicitamente não for encontrado. No entanto, você pode personalizar esse comportamento chamando o método `missing` ao definir sua rota de recurso. O método `missing` aceita uma closure que será invocada se um modelo vinculado implicitamente não puder ser encontrado para nenhuma das rotas do recurso:

```php
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
    ->missing(function (Request $request) {
        return Redirect::route('photos.index');
    });
```

<a id="soft-deleted-models"></a>
#### Modelos Soft Deleted

Tipicamente, a vinculação implícita de modelo não recuperará modelos que foram [soft deleted](../eloquent/#soft-deleting), e em vez disso retornará uma resposta HTTP 404. No entanto, você pode instruir o framework a permitir modelos soft deleted invocando o método `withTrashed` ao definir sua rota de recurso:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

Chamar `withTrashed` sem argumentos permitirá modelos soft deleted para as rotas de recurso `show`, `edit` e `update`. Você pode especificar um subconjunto dessas rotas passando um array ao método `withTrashed`:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a id="specifying-the-resource-model"></a>
#### Especificando o Modelo do Recurso

Se você está usando [vinculação de modelo de rota](../routing/#route-model-binding) e gostaria que os métodos do controller de recurso fizessem type-hint de uma instância de modelo, você pode usar a opção `--model` ao gerar o controller:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a id="generating-form-requests"></a>
#### Gerando Form Requests

Você pode fornecer a opção `--requests` ao gerar um controller de recurso para instruir o Artisan a gerar [classes de form request](../validation/#form-request-validation) para os métodos de armazenamento e atualização do controller:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a id="restful-partial-resource-routes"></a>
### Rotas de Recurso Parciais

Ao declarar uma rota de recurso, você pode especificar um subconjunto de ações que o controller deve tratar em vez do conjunto completo de ações padrão:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->only([
    'index', 'show'
]);

Route::resource('photos', PhotoController::class)->except([
    'create', 'store', 'update', 'destroy'
]);
```

<a id="api-resource-routes"></a>
#### Rotas de Recurso de API

Ao declarar rotas de recurso que serão consumidas por APIs, você comumente desejará excluir rotas que apresentam templates HTML, como `create` e `edit`. Por conveniência, você pode usar o método `apiResource` para excluir automaticamente essas duas rotas:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

Você pode registrar vários controllers de recurso de API de uma vez passando um array ao método `apiResources`:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

Para gerar rapidamente um controller de recurso de API que não inclua os métodos `create` ou `edit`, use a opção `--api` ao executar o comando `make:controller`:

```shell
php artisan make:controller PhotoController --api
```

<a id="restful-nested-resources"></a>
### Recursos Aninhados

Às vezes você pode precisar definir rotas para um recurso aninhado. Por exemplo, um recurso de foto pode ter múltiplos comentários que podem ser anexados à foto. Para aninhar os controllers de recurso, você pode usar a notação de "ponto" na sua declaração de rota:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

Esta rota registrará um recurso aninhado que pode ser acessado com URIs como a seguinte:

```text
/photos/{photo}/comments/{comment}
```

<a id="scoping-nested-resources"></a>
#### Aplicando Escopo a Recursos Aninhados

A funcionalidade de [vinculação implícita de modelo](../routing/#implicit-model-binding-scoping) do Laravel pode automaticamente aplicar escopo a vinculações aninhadas de modo que o modelo filho resolvido seja confirmado como pertencente ao modelo pai. Ao usar o método `scoped` ao definir seu recurso aninhado, você pode habilitar o escopo automático, bem como instruir o Laravel sobre por qual campo o recurso filho deve ser recuperado. Para mais informações sobre como fazer isso, por favor veja a documentação sobre [aplicação de escopo a rotas de recurso](#restful-scoping-resource-routes).

<a id="shallow-nesting"></a>
#### Aninhamento Raso

Frequentemente, não é inteiramente necessário ter tanto o ID pai quanto o filho dentro de uma URI, já que o ID do filho já é um identificador único. Ao usar identificadores únicos, como chaves primárias auto-incrementadas, para identificar seus modelos em segmentos de URI, você pode escolher usar "aninhamento raso":

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

Esta definição de rota definirá as seguintes rotas:

<div class="overflow-auto">

| Verbo     | URI                               | Ação    | Nome da Rota           |
| --------- | --------------------------------- | ------- | ---------------------- |
| GET       | `/photos/{photo}/comments`        | index   | photos.comments.index  |
| GET       | `/photos/{photo}/comments/create` | create  | photos.comments.create |
| POST      | `/photos/{photo}/comments`        | store   | photos.comments.store  |
| GET       | `/comments/{comment}`             | show    | comments.show          |
| GET       | `/comments/{comment}/edit`        | edit    | comments.edit          |
| PUT/PATCH | `/comments/{comment}`             | update  | comments.update        |
| DELETE    | `/comments/{comment}`             | destroy | comments.destroy       |

</div>

<a id="restful-naming-resource-routes"></a>
### Nomeando Rotas de Recurso

Por padrão, todas as ações de controller de recurso têm um nome de rota; no entanto, você pode sobrescrever esses nomes passando um array `names` com os nomes de rota desejados:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a id="restful-naming-resource-route-parameters"></a>
### Nomeando Parâmetros de Rota de Recurso

Por padrão, `Route::resource` criará os parâmetros de rota para suas rotas de recurso com base na versão "singularizada" do nome do recurso. Você pode facilmente sobrescrever isso por recurso usando o método `parameters`. O array passado ao método `parameters` deve ser um array associativo de nomes de recurso e nomes de parâmetro:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

O exemplo acima gera a seguinte URI para a rota `show` do recurso:

```text
/users/{admin_user}
```

<a id="restful-scoping-resource-routes"></a>
### Aplicando Escopo a Rotas de Recurso

A funcionalidade de [vinculação implícita de modelo com escopo](../routing/#implicit-model-binding-scoping) do Laravel pode automaticamente aplicar escopo a vinculações aninhadas de modo que o modelo filho resolvido seja confirmado como pertencente ao modelo pai. Ao usar o método `scoped` ao definir seu recurso aninhado, você pode habilitar o escopo automático, bem como instruir o Laravel sobre por qual campo o recurso filho deve ser recuperado:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

Esta rota registrará um recurso aninhado com escopo que pode ser acessado com URIs como a seguinte:

```text
/photos/{photo}/comments/{comment:slug}
```

Ao usar uma vinculação implícita com chave personalizada como um parâmetro de rota aninhado, o Laravel automaticamente restringirá o escopo da consulta para recuperar o modelo aninhado por seu pai usando convenções para adivinhar o nome do relacionamento no pai. Neste caso, será assumido que o modelo `Photo` tem um relacionamento chamado `comments` (o plural do nome do parâmetro de rota) que pode ser usado para recuperar o modelo `Comment`.

<a id="restful-localizing-resource-uris"></a>
### Localizando URIs de Recurso

Por padrão, `Route::resource` criará URIs de recurso usando verbos em inglês e regras de plural. Se você precisar localizar os verbos de ação `create` e `edit`, você pode usar o método `Route::resourceVerbs`. Isso pode ser feito no início do método `boot` dentro do `App\Providers\AppServiceProvider` da sua aplicação:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

O pluralizador do Laravel suporta [vários idiomas diferentes que você pode configurar com base nas suas necessidades](../localization/#pluralization-language). Uma vez que os verbos e o idioma de pluralização tenham sido personalizados, um registro de rota de recurso como `Route::resource('publicacion', PublicacionController::class)` produzirá as seguintes URIs:

```text
/publicacion/crear

/publicacion/{publicacion}/editar
```

<a id="restful-supplementing-resource-controllers"></a>
### Complementando Controllers de Recurso

Se você precisar adicionar rotas adicionais a um controller de recurso além do conjunto padrão de rotas de recurso, você deve definir essas rotas antes da sua chamada ao método `Route::resource`; caso contrário, as rotas definidas pelo método `resource` podem, não intencionalmente, ter precedência sobre suas rotas suplementares:

```php
use App\Http\Controllers\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> **Nota:**
> Lembre-se de manter seus controllers focados. Se você se encontrar rotineiramente precisando de métodos fora do conjunto típico de ações de recurso, considere dividir seu controller em dois controllers menores.

<a id="singleton-resource-controllers"></a>
### Controllers de Recurso Singleton

Às vezes, sua aplicação terá recursos que podem ter apenas uma única instância. Por exemplo, o "profile" de um usuário pode ser editado ou atualizado, mas um usuário não pode ter mais de um "profile". Da mesma forma, uma imagem pode ter um único "thumbnail". Esses recursos são chamados de "recursos singleton", significando que uma e apenas uma instância do recurso pode existir. Nesses cenários, você pode registrar um controller de recurso "singleton":

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

A definição de recurso singleton acima registrará as seguintes rotas. Como você pode ver, rotas de "criação" não são registradas para recursos singleton, e as rotas registradas não aceitam um identificador, já que apenas uma instância do recurso pode existir:

<div class="overflow-auto">

| Verbo     | URI             | Ação   | Nome da Rota   |
| --------- | --------------- | ------ | -------------- |
| GET       | `/profile`      | show   | profile.show   |
| GET       | `/profile/edit` | edit   | profile.edit   |
| PUT/PATCH | `/profile`      | update | profile.update |

</div>

Recursos singleton também podem ser aninhados dentro de um recurso padrão:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

Neste exemplo, o recurso `photos` receberia todas as [rotas de recurso padrão](#actions-handled-by-resource-controllers); no entanto, o recurso `thumbnail` seria um recurso singleton com as seguintes rotas:

<div class="overflow-auto">

| Verbo     | URI                              | Ação   | Nome da Rota            |
| --------- | -------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update |

</div>

<a id="creatable-singleton-resources"></a>
#### Recursos Singleton Criáveis

Ocasionalmente, você pode querer definir rotas de criação e armazenamento para um recurso singleton. Para isso, você pode invocar o método `creatable` ao registrar a rota de recurso singleton:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

Neste exemplo, as seguintes rotas serão registradas. Como você pode ver, uma rota `DELETE` também será registrada para recursos singleton criáveis:

<div class="overflow-auto">

| Verbo     | URI                                | Ação    | Nome da Rota             |
| --------- | ---------------------------------- | ------- | ------------------------ |
| GET       | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy |

</div>

Se você gostaria que o Laravel registrasse a rota `DELETE` para um recurso singleton, mas não registrasse as rotas de criação ou armazenamento, você pode utilizar o método `destroyable`:

```php
Route::singleton(...)->destroyable();
```

<a id="api-singleton-resources"></a>
#### Recursos Singleton de API

O método `apiSingleton` pode ser usado para registrar um recurso singleton que será manipulado por meio de uma API, tornando assim as rotas `create` e `edit` desnecessárias:

```php
Route::apiSingleton('profile', ProfileController::class);
```

É claro, recursos singleton de API também podem ser `creatable`, o que registrará rotas `store` e `destroy` para o recurso:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```
<a id="middleware-and-resource-controllers"></a>
### Middleware e Controllers de Recurso

O Laravel permite que você atribua middleware a todos, ou apenas a métodos específicos, das rotas de recurso usando os métodos `middleware`, `middlewareFor` e `withoutMiddlewareFor`. Esses métodos fornecem controle refinado sobre qual middleware é aplicado a cada ação de recurso.

#### Aplicando Middleware a Todos os Métodos

Você pode usar o método `middleware` para atribuir middleware a todas as rotas geradas por uma rota de recurso ou de recurso singleton:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### Aplicando Middleware a Métodos Específicos

Você pode usar o método `middlewareFor` para atribuir middleware a um ou mais métodos específicos de um determinado controller de recurso:

```php
Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```

O método `middlewareFor` também pode ser usado em conjunto com controllers de recurso singleton e de recurso singleton de API:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### Excluindo Middleware de Métodos Específicos

Você pode usar o método `withoutMiddlewareFor` para excluir middleware de métodos específicos de um controller de recurso:

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

<a id="dependency-injection-and-controllers"></a>
## Injeção de Dependência e Controllers

<a id="constructor-injection"></a>
#### Injeção no Construtor

O [service container](../container/) do Laravel é usado para resolver todos os controllers do Laravel. Como resultado, você é capaz de fazer type-hint de quaisquer dependências que seu controller possa precisar no seu construtor. As dependências declaradas serão automaticamente resolvidas e injetadas na instância do controller:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a id="method-injection"></a>
#### Injeção no Método

Além da injeção no construtor, você também pode fazer type-hint de dependências nos métodos do seu controller. Um caso de uso comum para injeção no método é injetar a instância de `Illuminate\Http\Request` nos métodos do seu controller:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // Store the user...

        return redirect('/users');
    }
}
```

Se seu método de controller também espera input de um parâmetro de rota, liste seus argumentos de rota após suas outras dependências. Por exemplo, se sua rota está definida assim:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

Você ainda pode fazer type-hint de `Illuminate\Http\Request` e acessar seu parâmetro `id` definindo seu método de controller da seguinte forma:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```
