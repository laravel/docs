---
title: "Laravel Folio"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Caminhos de Páginas / URIs](#page-paths-uris)
    - [Roteamento de Subdomínio](#subdomain-routing)
- [Criando Rotas](#creating-routes)
    - [Rotas Aninhadas](#nested-routes)
    - [Rotas de Índice](#index-routes)
- [Parâmetros de Rota](#route-parameters)
- [Vinculação de Modelo de Rota](#route-model-binding)
    - [Modelos Soft Deleted](#soft-deleted-models)
- [Render Hooks](#render-hooks)
- [Rotas Nomeadas](#named-routes)
- [Middleware](#middleware)
- [Cache de Rotas](#route-caching)

<a id="introduction"></a>
## Introdução

[Laravel Folio](https://github.com/laravel/folio) é um roteador baseado em páginas, poderoso e projetado para simplificar o roteamento em aplicações Laravel. Com o Laravel Folio, gerar uma rota se torna tão simples quanto criar um template Blade dentro do diretório `resources/views/pages` da sua aplicação.

Por exemplo, para criar uma página acessível pela URL `/greeting`, basta criar um arquivo `greeting.blade.php` no diretório `resources/views/pages` da sua aplicação:

```blade
<div>
    Hello World
</div>
```

<a id="installation"></a>
## Instalação

Para começar, instale o Folio no seu projeto usando o gerenciador de pacotes Composer:

```shell
composer require laravel/folio
```

Após instalar o Folio, você pode executar o comando Artisan `folio:install`, que instalará o service provider do Folio na sua aplicação. Este service provider registra o diretório onde o Folio buscará as rotas / páginas:

```shell
php artisan folio:install
```

<a id="page-paths-uris"></a>
### Caminhos de Páginas / URIs

Por padrão, o Folio serve páginas a partir do diretório `resources/views/pages` da sua aplicação, mas você pode personalizar esses diretórios no método `boot` do seu service provider do Folio.

Por exemplo, às vezes pode ser conveniente especificar múltiplos caminhos do Folio na mesma aplicação Laravel. Você pode querer ter um diretório separado de páginas do Folio para a área "admin" da sua aplicação, enquanto usa outro diretório para as demais páginas.

Você pode fazer isso usando os métodos `Folio::path` e `Folio::uri`. O método `path` registra um diretório que o Folio irá varrer em busca de páginas ao rotear requisições HTTP recebidas, enquanto o método `uri` especifica a "URI base" para esse diretório de páginas:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages/guest'))->uri('/');

Folio::path(resource_path('views/pages/admin'))
    ->uri('/admin')
    ->middleware([
        '*' => [
            'auth',
            'verified',

            // ...
        ],
    ]);
```

<a id="subdomain-routing"></a>
### Roteamento de Subdomínio

Você também pode rotear para páginas com base no subdomínio da requisição recebida. Por exemplo, você pode querer rotear requisições de `admin.example.com` para um diretório de páginas diferente do restante das suas páginas do Folio. Isso pode ser feito invocando o método `domain` após invocar o método `Folio::path`:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

O método `domain` também permite capturar partes do domínio ou subdomínio como parâmetros. Esses parâmetros serão injetados no template da sua página:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a id="creating-routes"></a>
## Criando Rotas

Você pode criar uma rota do Folio colocando um template Blade em qualquer um dos diretórios montados pelo Folio. Por padrão, o Folio monta o diretório `resources/views/pages`, mas você pode personalizar esses diretórios no método `boot` do seu service provider do Folio.

Assim que um template Blade for colocado em um diretório montado pelo Folio, você poderá acessá-lo imediatamente pelo navegador. Por exemplo, uma página colocada em `pages/schedule.blade.php` poderá ser acessada no navegador em `http://example.com/schedule`.

Para visualizar rapidamente a lista de todas as suas páginas / rotas do Folio, você pode invocar o comando Artisan `folio:list`:

```shell
php artisan folio:list
```

<a id="nested-routes"></a>
### Rotas Aninhadas

Você pode criar uma rota aninhada criando um ou mais diretórios dentro de um dos diretórios do Folio. Por exemplo, para criar uma página acessível em `/user/profile`, crie um template `profile.blade.php` dentro do diretório `pages/user`:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a id="index-routes"></a>
### Rotas de Índice

Às vezes, você pode querer tornar uma determinada página o "índice" de um diretório. Ao colocar um template `index.blade.php` dentro de um diretório do Folio, todas as requisições para a raiz desse diretório serão roteadas para essa página:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a id="route-parameters"></a>
## Parâmetros de Rota

Frequentemente, você precisará que segmentos da URL da requisição recebida sejam injetados na sua página para que você possa interagir com eles. Por exemplo, você pode precisar acessar o "ID" do usuário cujo perfil está sendo exibido. Para isso, você pode envolver um segmento do nome do arquivo da página entre colchetes:

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

Os segmentos capturados podem ser acessados como variáveis dentro do seu template Blade:

```html
<div>
    User {{ $id }}
</div>
```

Para capturar múltiplos segmentos, você pode prefixar o segmento envolvido com três pontos `...`:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

Ao capturar múltiplos segmentos, os segmentos capturados serão injetados na página como um array:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a id="route-model-binding"></a>
## Vinculação de Modelo de Rota

Se um segmento curinga do nome do arquivo do seu template de página corresponder a um dos models Eloquent da sua aplicação, o Folio aproveitará automaticamente os recursos de vinculação de modelo de rota do Laravel e tentará injetar a instância do model resolvido na sua página:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

Os models capturados podem ser acessados como variáveis dentro do seu template Blade. O nome da variável do model será convertido para "camel case":

```html
<div>
    User {{ $user->id }}
</div>
```

#### Personalizando a Chave

Às vezes, você pode querer resolver models Eloquent vinculados usando uma coluna diferente de `id`. Para isso, você pode especificar a coluna no nome do arquivo da página. Por exemplo, uma página com o nome de arquivo `[Post:slug].blade.php` tentará resolver o model vinculado pela coluna `slug` em vez da coluna `id`.

No Windows, você deve usar `-` para separar o nome do model da chave: `[Post-slug].blade.php`.

#### Localização do Model

Por padrão, o Folio buscará seu model dentro do diretório `app/Models` da sua aplicação. No entanto, se necessário, você pode especificar o nome completo da classe do model no nome do arquivo do seu template:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a id="soft-deleted-models"></a>
### Modelos Soft Deleted

Por padrão, models que foram soft deleted não são recuperados ao resolver vinculações implícitas de models. No entanto, se desejar, você pode instruir o Folio a recuperar models soft deleted invocando a função `withTrashed` dentro do template da página:

```php
<?php

use function Laravel\Folio\{withTrashed};

withTrashed();

?>

<div>
    User {{ $user->id }}
</div>
```

<a id="render-hooks"></a>
## Render Hooks

Por padrão, o Folio retornará o conteúdo do template Blade da página como resposta à requisição recebida. No entanto, você pode personalizar a resposta invocando a função `render` dentro do template da página.

A função `render` aceita uma closure que receberá a instância de `View` que está sendo renderizada pelo Folio, permitindo que você adicione dados adicionais à view ou personalize toda a resposta. Além de receber a instância de `View`, quaisquer parâmetros de rota adicionais ou vinculações de model também serão fornecidos à closure de `render`:

```php
<?php

use App\Models\Post;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

use function Laravel\Folio\render;

render(function (View $view, Post $post) {
    if (! Auth::user()->can('view', $post)) {
        return response('Unauthorized', 403);
    }

    return $view->with('photos', $post->author->photos);
}); ?>

<div>
    {{ $post->content }}
</div>

<div>
    This author has also taken {{ count($photos) }} photos.
</div>
```

<a id="named-routes"></a>
## Rotas Nomeadas

Você pode especificar um nome para a rota de uma determinada página usando a função `name`:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Assim como as rotas nomeadas do Laravel, você pode usar a função `route` para gerar URLs para páginas do Folio que receberam um nome:

```blade
<a href="{{ route('users.index') }}">
    All Users
</a>
```

Se a página tiver parâmetros, basta passar seus valores para a função `route`:

```php
route('users.show', ['user' => $user]);
```

<a id="middleware"></a>
## Middleware

Você pode aplicar middleware a uma página específica invocando a função `middleware` dentro do template da página:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

Ou, para atribuir middleware a um grupo de páginas, você pode encadear o método `middleware` após invocar o método `Folio::path`.

Para especificar em quais páginas o middleware deve ser aplicado, o array de middleware pode ser indexado usando os padrões de URL correspondentes às páginas às quais eles devem ser aplicados. O caractere `*` pode ser utilizado como curinga:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        // ...
    ],
]);
```

Você pode incluir closures no array de middleware para definir middleware anônimo inline:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        function (Request $request, Closure $next) {
            // ...

            return $next($request);
        },
    ],
]);
```

<a id="route-caching"></a>
## Cache de Rotas

Ao usar o Folio, você deve sempre aproveitar os [recursos de cache de rotas do Laravel](../routing/#route-caching). O Folio escuta o comando Artisan `route:cache` para garantir que as definições de páginas do Folio e os nomes de rotas sejam devidamente armazenados em cache para máximo desempenho.
