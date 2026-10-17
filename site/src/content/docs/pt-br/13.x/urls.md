---
title: "Geração de URLs"
---

- [Introdução](#introduction)
- [O Básico](#the-basics)
    - [Gerando URLs](#generating-urls)
    - [Acessando a URL Atual](#accessing-the-current-url)
- [URLs para Rotas Nomeadas](#urls-for-named-routes)
    - [URLs Assinadas](#signed-urls)
- [URLs para Ações de Controller](#urls-for-controller-actions)
- [Objetos URI Fluentes](#fluent-uri-objects)
- [Valores Padrão](#default-values)

<a id="introduction"></a>
## Introdução

O Laravel fornece vários helpers para auxiliá-lo a gerar URLs para sua aplicação. Esses helpers são primariamente úteis ao construir links em seus templates e respostas de API, ou ao gerar respostas de redirecionamento para outra parte da sua aplicação.

<a id="the-basics"></a>
## O Básico

<a id="generating-urls"></a>
### Gerando URLs

O helper `url` pode ser usado para gerar URLs arbitrárias para sua aplicação. A URL gerada usará automaticamente o esquema (HTTP ou HTTPS) e o host da requisição atual sendo tratada pela aplicação:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

Para gerar uma URL com parâmetros de query string, você pode usar o método `query`:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

Fornecer parâmetros de query string que já existem no caminho sobrescreverá seus valores existentes:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

Arrays de valores também podem ser passados como parâmetros de query. Esses valores serão adequadamente chaveados e codificados na URL gerada:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a id="accessing-the-current-url"></a>
### Acessando a URL Atual

Se nenhum caminho for fornecido ao helper `url`, uma instância de `Illuminate\Routing\UrlGenerator` é retornada, permitindo que você acesse informações sobre a URL atual:

```php
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();
```

Cada um desses métodos também pode ser acessado via a [facade](../facades/) `URL`:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a id="accessing-the-previous-url"></a>
#### Acessando a URL Anterior

Às vezes é útil saber a URL anterior de onde o usuário está vindo. Você pode acessar a URL anterior via os métodos `previous` e `previousPath` do helper `url`:

```php
// Get the full URL for the previous request...
echo url()->previous();

// Get the path for the previous request...
echo url()->previousPath();
```

Ou, via a [sessão](../session/), você pode acessar a URL anterior como uma instância de [URI fluente](#fluent-uri-objects):

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});
```

Também é possível recuperar o nome da rota para a URL visitada anteriormente via a sessão:

```php
$previousRoute = $request->session()->previousRoute();
```

<a id="urls-for-named-routes"></a>
## URLs para Rotas Nomeadas

O helper `route` pode ser usado para gerar URLs para [rotas nomeadas](../routing/#named-routes). Rotas nomeadas permitem gerar URLs sem estar acoplado à URL real definida na rota. Portanto, se a URL da rota mudar, nenhuma alteração precisa ser feita em suas chamadas à função `route`. Por exemplo, imagine que sua aplicação contém uma rota definida assim:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

Para gerar uma URL para esta rota, você pode usar o helper `route` assim:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

Claro, o helper `route` também pode ser usado para gerar URLs para rotas com múltiplos parâmetros:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

Quaisquer elementos de array adicionais que não correspondam aos parâmetros de definição da rota serão adicionados à query string da URL:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a id="eloquent-models"></a>
#### Modelos Eloquent

Você frequentemente estará gerando URLs usando a chave de rota (tipicamente a chave primária) de [modelos Eloquent](../eloquent/). Por esta razão, você pode passar modelos Eloquent como valores de parâmetros. O helper `route` extrairá automaticamente a chave de rota do modelo:

```php
echo route('post.show', ['post' => $post]);
```

<a id="signed-urls"></a>
### URLs Assinadas

O Laravel permite que você crie facilmente URLs "assinadas" para rotas nomeadas. Essas URLs têm um hash de "assinatura" anexado à query string que permite ao Laravel verificar que a URL não foi modificada desde que foi criada. URLs assinadas são especialmente úteis para rotas que são publicamente acessíveis, mas precisam de uma camada de proteção contra manipulação de URL.

Por exemplo, você pode usar URLs assinadas para implementar um link público de "descadastro" que é enviado por email para seus clientes. Para criar uma URL assinada para uma rota nomeada, use o método `signedRoute` da facade `URL`:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

Você pode excluir o domínio do hash da URL assinada fornecendo o argumento `absolute` ao método `signedRoute`:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

Se você gostaria de gerar uma URL de rota assinada temporária que expira após uma quantidade especificada de tempo, você pode usar o método `temporarySignedRoute`. Quando o Laravel valida uma URL de rota assinada temporária, ele garantirá que o timestamp de expiração que está codificado na URL assinada não tenha decorrido:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]
);
```

<a id="validating-signed-route-requests"></a>
#### Validando Requisições de Rotas Assinadas

Para verificar que uma requisição recebida tem uma assinatura válida, você deve chamar o método `hasValidSignature` na instância recebida de `Illuminate\Http\Request`:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

Às vezes, você pode precisar permitir que o frontend da sua aplicação anexe dados a uma URL assinada, como ao realizar paginação no lado do cliente. Portanto, você pode especificar parâmetros de query da requisição que devem ser ignorados ao validar uma URL assinada usando o método `hasValidSignatureWhileIgnoring`. Lembre-se, ignorar parâmetros permite que qualquer pessoa modifique esses parâmetros na requisição:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

Em vez de validar URLs assinadas usando a instância de requisição recebida, você pode atribuir o [middleware](../middleware/) `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) à rota. Se a requisição recebida não tiver uma assinatura válida, o middleware retornará automaticamente uma resposta HTTP `403`:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

Se suas URLs assinadas não incluírem o domínio no hash da URL, você deve fornecer o argumento `relative` ao middleware:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

> **Aviso:**
> Uma assinatura cobre apenas o caminho e a query string da URL. Qualquer outra input da requisição, como um formulário ou corpo de requisição JSON, não é assinada e pode ser livremente modificada pelo usuário. Como o Laravel mescla essas fontes de input juntas e dá precedência ao corpo da requisição sobre a query string, recuperar input com qualquer método além de `query`, como `input`, `all`, ou uma propriedade dinâmica da requisição, pode retornar valores não assinados que sobrescrevem seus valores assinados da query string. Portanto, você deve sempre recuperar valores assinados usando o método `query`, como `$request->query('email')`. Isso inclui requisições `GET`, pois uma requisição `GET` especialmente criada ainda pode conter um corpo de requisição JSON.

<a id="responding-to-invalid-signed-routes"></a>
#### Respondendo a Rotas Assinadas Inválidas

Quando alguém visita uma URL assinada que expirou, receberá uma página de erro genérica para o código de status HTTP `403`. No entanto, você pode personalizar este comportamento definindo um closure de "render" personalizado para a exceção `InvalidSignatureException` no arquivo `bootstrap/app.php` da sua aplicação:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a id="urls-for-controller-actions"></a>
## URLs para Ações de Controller

A função `action` gera uma URL para a ação de controller fornecida:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

Se o método do controller aceitar parâmetros de rota, você pode passar um array associativo de parâmetros de rota como segundo argumento à função:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a id="fluent-uri-objects"></a>
## Objetos URI Fluentes

A classe `Uri` do Laravel fornece uma interface conveniente e fluente para criar e manipular URIs via objetos. Esta classe encapsula a funcionalidade fornecida pelo pacote subjacente League URI e se integra perfeitamente com o sistema de roteamento do Laravel.

Você pode criar uma instância `Uri` facilmente usando métodos estáticos:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();

// Generate a URI instance from the previous request URL...
$uri = $request->session()->previousUri();
```

Uma vez que você tenha uma instância URI, você pode modificá-la fluentemente:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

Para mais informações sobre como trabalhar com objetos URI fluentes, consulte a [documentação de URI](../helpers/#uri).

<a id="default-values"></a>
## Valores Padrão

Para algumas aplicações, você pode desejar especificar valores padrão abrangentes para requisição para certos parâmetros de URL. Por exemplo, imagine que muitas das suas rotas definem um parâmetro `{locale}`:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

É trabalhoso sempre passar o `locale` toda vez que você chama o helper `route`. Então, você pode usar o método `URL::defaults` para definir um valor padrão para este parâmetro que será sempre aplicado durante a requisição atual. Você pode desejar chamar este método de um [middleware de rota](../middleware/#assigning-middleware-to-routes) para que tenha acesso à requisição atual:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;
use Symfony\Component\HttpFoundation\Response;

class SetDefaultLocaleForUrls
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

Uma vez que o valor padrão para o parâmetro `locale` tenha sido definido, você não é mais obrigado a passar seu valor ao gerar URLs via o helper `route`.

<a id="url-defaults-middleware-priority"></a>
#### Valores Padrão de URL e Prioridade de Middleware

Definir valores padrão de URL pode interferir com o tratamento de bindings implícitos de modelos pelo Laravel. Portanto, você deve [priorizar seus middleware](../middleware/#sorting-middleware) que definem valores padrão de URL para serem executados antes do próprio middleware `SubstituteBindings` do Laravel. Você pode conseguir isso usando o método de prioridade de middleware `priority` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```