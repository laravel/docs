---
title: "Banco de Dados: Paginação"
---

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)
    - [Paginando Resultados do Query Builder](#paginating-query-builder-results)
    - [Paginando Resultados do Eloquent](#paginating-eloquent-results)
    - [Paginação por Cursor](#cursor-pagination)
    - [Criando um Paginator Manualmente](#manually-creating-a-paginator)
    - [Personalizando URLs de Paginação](#customizing-pagination-urls)
- [Exibindo Resultados da Paginação](#displaying-pagination-results)
    - [Ajustando a Janela de Links de Paginação](#adjusting-the-pagination-link-window)
    - [Convertendo Resultados para JSON](#converting-results-to-json)
- [Personalizando a View de Paginação](#customizing-the-pagination-view)
    - [Usando o Bootstrap](#using-bootstrap)
- [Métodos de Instância do Paginator e LengthAwarePaginator](#paginator-instance-methods)
- [Métodos de Instância do Cursor Paginator](#cursor-paginator-instance-methods)

<a id="introduction"></a>
## Introdução

Em outros frameworks, a paginação pode ser muito dolorosa. Esperamos que a abordagem do Laravel para a paginação seja uma lufada de ar fresco. O paginator do Laravel é integrado com o [query builder](/en/queries/) e o [Eloquent ORM](/en/eloquent/) e fornece paginação de registros de banco de dados conveniente e fácil de usar sem configuração alguma.

Por padrão, o HTML gerado pelo paginator é compatível com o [framework Tailwind CSS](https://tailwindcss.com/); no entanto, suporte à paginação com Bootstrap também está disponível.

<a id="tailwind"></a>
#### Tailwind

Se você estiver usando as views de paginação padrão do Tailwind do Laravel com o Tailwind 4.x, o arquivo `resources/css/app.css` da sua aplicação já estará devidamente configurado para usar `@source` nas views de paginação do Laravel:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a id="basic-usage"></a>
## Uso Básico

<a id="paginating-query-builder-results"></a>
### Paginando Resultados do Query Builder

Existem várias maneiras de paginar itens. A mais simples é usando o método `paginate` no [query builder](/en/queries/) ou em uma [query do Eloquent](/en/eloquent/). O método `paginate` automaticamente cuida de definir o "limit" e o "offset" da query com base na página atual sendo visualizada pelo usuário. Por padrão, a página atual é detectada pelo valor do argumento de query string `page` na requisição HTTP. Esse valor é automaticamente detectado pelo Laravel, e também é automaticamente inserido nos links gerados pelo paginator.

Neste exemplo, o único argumento passado ao método `paginate` é o número de itens que você gostaria de exibir "por página". Neste caso, vamos especificar que gostaríamos de exibir `15` itens por página:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a id="simple-pagination"></a>
#### Paginação Simples

O método `paginate` conta o número total de registros correspondidos pela query antes de recuperar os registros do banco de dados. Isso é feito para que o paginator saiba quantas páginas de registros existem no total. No entanto, se você não planeja mostrar o número total de páginas na UI da sua aplicação, então a query de contagem de registros é desnecessária.

Portanto, se você só precisa exibir links simples de "Próximo" e "Anterior" na UI da sua aplicação, você pode usar o método `simplePaginate` para executar uma única query eficiente:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a id="paginating-eloquent-results"></a>
### Paginando Resultados do Eloquent

Você também pode paginar queries do [Eloquent](/en/eloquent/). Neste exemplo, vamos paginar o model `App\Models\User` e indicar que planejamos exibir 15 registros por página. Como você pode ver, a sintaxe é quase idêntica à paginação de resultados do query builder:

```php
use App\Models\User;

$users = User::paginate(15);
```

Naturalmente, você pode chamar o método `paginate` após definir outras restrições na query, como cláusulas `where`:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Você também pode usar o método `simplePaginate` ao paginar models do Eloquent:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

Da mesma forma, você pode usar o método `cursorPaginate` para paginar por cursor models do Eloquent:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a id="multiple-paginator-instances-per-page"></a>
#### Múltiplas Instâncias de Paginator por Página

Às vezes você pode precisar renderizar dois paginators separados em uma única tela que é renderizada pela sua aplicação. No entanto, se ambas as instâncias de paginator usarem o parâmetro de query string `page` para armazenar a página atual, os dois paginators entrarão em conflito. Para resolver esse conflito, você pode passar o nome do parâmetro de query string que deseja usar para armazenar a página atual do paginator através do terceiro argumento fornecido aos métodos `paginate`, `simplePaginate` e `cursorPaginate`:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a id="cursor-pagination"></a>
### Paginação por Cursor

Enquanto `paginate` e `simplePaginate` criam queries usando a cláusula SQL "offset", a paginação por cursor funciona construindo cláusulas "where" que comparam os valores das colunas ordenadas contidas na query, fornecendo o melhor desempenho de banco de dados disponível entre todos os métodos de paginação do Laravel. Este método de paginação é particularmente bem adequado para grandes conjuntos de dados e interfaces de usuário com rolagem "infinita".

Diferentemente da paginação baseada em offset, que inclui um número de página na query string das URLs geradas pelo paginator, a paginação baseada em cursor coloca uma string de "cursor" na query string. O cursor é uma string codificada contendo a localização em que a próxima query paginada deve começar a paginar e a direção em que deve paginar:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

Você pode criar uma instância de paginator baseado em cursor através do método `cursorPaginate` oferecido pelo query builder. Este método retorna uma instância de `Illuminate\Pagination\CursorPaginator`:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

Uma vez que você tenha recuperado uma instância de cursor paginator, você pode [exibir os resultados da paginação](#displaying-pagination-results) como normalmente faria ao usar os métodos `paginate` e `simplePaginate`. Para mais informações sobre os métodos de instância oferecidos pelo cursor paginator, consulte a [documentação de métodos de instância do cursor paginator](#cursor-paginator-instance-methods).

> **Aviso:**
> Sua query deve conter uma cláusula "order by" para aproveitar a paginação por cursor. Além disso, as colunas pelas quais a query é ordenada devem pertencer à tabela que você está paginando.

<a id="cursor-vs-offset-pagination"></a>
#### Paginação por Cursor vs. Offset

Para ilustrar as diferenças entre a paginação por offset e a paginação por cursor, vamos examinar algumas queries SQL de exemplo. Ambas as queries a seguir exibirão a "segunda página" de resultados de uma tabela `users` ordenada por `id`:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

A query de paginação por cursor oferece as seguintes vantagens sobre a paginação por offset:

- Para grandes conjuntos de dados, a paginação por cursor oferecerá melhor desempenho se as colunas do "order by" estiverem indexadas. Isso ocorre porque a cláusula "offset" escaneia todos os dados correspondidos anteriormente.
- Para conjuntos de dados com escritas frequentes, a paginação por offset pode pular registros ou mostrar duplicatas se resultados tiverem sido recentemente adicionados ou removidos da página que um usuário está visualizando atualmente.

No entanto, a paginação por cursor possui as seguintes limitações:

- Assim como `simplePaginate`, a paginação por cursor só pode ser usada para exibir links de "Próximo" e "Anterior" e não suporta a geração de links com números de página.
- Ela requer que a ordenação seja baseada em pelo menos uma coluna única ou uma combinação de colunas que seja única. Colunas com valores `null` não são suportadas.
- Expressões de query em cláusulas "order by" são suportadas apenas se forem aliasadas e adicionadas à cláusula "select" também.
- Expressões de query com parâmetros não são suportadas.

<a id="manually-creating-a-paginator"></a>
### Criando um Paginator Manualmente

Às vezes você pode querer criar uma instância de paginação manualmente, passando a ela um array de itens que você já tem em memória. Você pode fazer isso criando uma instância de `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator` ou `Illuminate\Pagination\CursorPaginator`, dependendo das suas necessidades.

As classes `Paginator` e `CursorPaginator` não precisam saber o número total de itens no conjunto de resultados; no entanto, por causa disso, essas classes não possuem métodos para recuperar o índice da última página. O `LengthAwarePaginator` aceita quase os mesmos argumentos que o `Paginator`; no entanto, ele requer uma contagem do número total de itens no conjunto de resultados.

Em outras palavras, o `Paginator` corresponde ao método `simplePaginate` no query builder, o `CursorPaginator` corresponde ao método `cursorPaginate`, e o `LengthAwarePaginator` corresponde ao método `paginate`.

> **Aviso:**
> Ao criar uma instância de paginator manualmente, você deve "fatiar" manualmente o array de resultados que você passa ao paginator. Se você não tem certeza de como fazer isso, confira a função PHP [array_slice](https://secure.php.net/manual/en/function.array-slice.php).

<a id="customizing-pagination-urls"></a>
### Personalizando URLs de Paginação

Por padrão, os links gerados pelo paginator corresponderão à URI da requisição atual. No entanto, o método `withPath` do paginator permite que você personalize a URI usada pelo paginator ao gerar links. Por exemplo, se você quiser que o paginator gere links como `http://example.com/admin/users?page=N`, você deve passar `/admin/users` ao método `withPath`:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a id="appending-query-string-values"></a>
#### Anexando Valores de Query String

Você pode anexar à query string dos links de paginação usando o método `appends`. Por exemplo, para anexar `sort=votes` a cada link de paginação, você deve fazer a seguinte chamada ao `appends`:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

Você pode usar o método `withQueryString` se quiser anexar todos os valores da query string da requisição atual aos links de paginação:

```php
$users = User::paginate(15)->withQueryString();
```

<a id="appending-hash-fragments"></a>
#### Anexando Fragmentos de Hash

Se você precisar anexar um "fragmento de hash" às URLs geradas pelo paginator, você pode usar o método `fragment`. Por exemplo, para anexar `#users` ao final de cada link de paginação, você deve invocar o método `fragment` assim:

```php
$users = User::paginate(15)->fragment('users');
```

<a id="displaying-pagination-results"></a>
## Exibindo Resultados da Paginação

Ao chamar o método `paginate`, você receberá uma instância de `Illuminate\Pagination\LengthAwarePaginator`, enquanto chamar o método `simplePaginate` retorna uma instância de `Illuminate\Pagination\Paginator`. E, finalmente, chamar o método `cursorPaginate` retorna uma instância de `Illuminate\Pagination\CursorPaginator`.

Esses objetos fornecem vários métodos que descrevem o conjunto de resultados. Além desses métodos auxiliares, as instâncias de paginator são iteradores e podem ser percorridas como um array. Então, uma vez que você tenha recuperado os resultados, você pode exibir os resultados e renderizar os links da página usando [Blade](/en/blade/):

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

O método `links` renderizará os links para o restante das páginas no conjunto de resultados. Cada um desses links já conterá a variável de query string `page` apropriada. Lembre-se, o HTML gerado pelo método `links` é compatível com o [framework Tailwind CSS](https://tailwindcss.com).

<a id="adjusting-the-pagination-link-window"></a>
### Ajustando a Janela de Links de Paginação

Quando o paginator exibe links de paginação, o número da página atual é exibido bem como links para as três páginas anteriores e posteriores à página atual. Usando o método `onEachSide`, você pode controlar quantos links adicionais são exibidos de cada lado da página atual dentro da janela deslizante do meio de links gerados pelo paginator:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a id="converting-results-to-json"></a>
### Convertendo Resultados para JSON

As classes de paginator do Laravel implementam o contrato de interface `Illuminate\Contracts\Support\Jsonable` e expõem o método `toJson`, então é muito fácil converter seus resultados de paginação para JSON. Você também pode converter uma instância de paginator para JSON retornando-a de uma rota ou ação de controller:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

O JSON do paginator incluirá meta informações como `total`, `current_page`, `last_page` e mais. Os registros de resultado estão disponíveis através da chave `data` no array JSON. Aqui está um exemplo do JSON criado ao retornar uma instância de paginator de uma rota:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a id="customizing-the-pagination-view"></a>
## Personalizando a View de Paginação

Por padrão, as views renderizadas para exibir os links de paginação são compatíveis com o framework [Tailwind CSS](https://tailwindcss.com). No entanto, se você não estiver usando o Tailwind, você é livre para definir suas próprias views para renderizar esses links. Ao chamar o método `links` em uma instância de paginator, você pode passar o nome da view como o primeiro argumento do método:

```blade
{{ $paginator->links('view.name') }}

<!-- Passing additional data to the view... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

No entanto, a maneira mais fácil de personalizar as views de paginação é exportando-as para o seu diretório `resources/views/vendor` usando o comando `vendor:publish`:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

Este comando colocará as views no diretório `resources/views/vendor/pagination` da sua aplicação. O arquivo `tailwind.blade.php` dentro deste diretório corresponde à view de paginação padrão. Você pode editar este arquivo para modificar o HTML da paginação.

Se você quiser designar um arquivo diferente como a view de paginação padrão, você pode invocar os métodos `defaultView` e `defaultSimpleView` do paginator dentro do método `boot` da sua classe `App\Providers\AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a id="using-bootstrap"></a>
### Usando o Bootstrap

O Laravel inclui views de paginação construídas usando o [Bootstrap CSS](https://getbootstrap.com/). Para usar essas views em vez das views padrão do Tailwind, você pode chamar os métodos `useBootstrapFour` ou `useBootstrapFive` do paginator dentro do método `boot` da sua classe `App\Providers\AppServiceProvider`:

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a id="paginator-instance-methods"></a>
## Métodos de Instância do Paginator / LengthAwarePaginator

Cada instância de paginator fornece informações adicionais de paginação através dos seguintes métodos:

<div class="overflow-auto">

| Método                                  | Descrição                                                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `$paginator->count()`                   | Obtém o número de itens para a página atual.                                                                 |
| `$paginator->currentPage()`             | Obtém o número da página atual.                                                                              |
| `$paginator->firstItem()`               | Obtém o número do resultado do primeiro item nos resultados.                                                 |
| `$paginator->getOptions()`              | Obtém as opções do paginator.                                                                                |
| `$paginator->getUrlRange($start, $end)` | Cria um intervalo de URLs de paginação.                                                                      |
| `$paginator->hasPages()`                | Determina se há itens suficientes para dividir em múltiplas páginas.                                         |
| `$paginator->hasMorePages()`            | Determina se há mais itens no data store.                                                                    |
| `$paginator->items()`                   | Obtém os itens para a página atual.                                                                          |
| `$paginator->lastItem()`                | Obtém o número do resultado do último item nos resultados.                                                   |
| `$paginator->lastPage()`                | Obtém o número da página da última página disponível. (Não disponível ao usar `simplePaginate`).             |
| `$paginator->nextPageUrl()`             | Obtém a URL para a próxima página.                                                                           |
| `$paginator->onFirstPage()`             | Determina se o paginator está na primeira página.                                                            |
| `$paginator->onLastPage()`              | Determina se o paginator está na última página.                                                              |
| `$paginator->perPage()`                 | O número de itens a serem exibidos por página.                                                               |
| `$paginator->previousPageUrl()`         | Obtém a URL para a página anterior.                                                                          |
| `$paginator->total()`                   | Determina o número total de itens correspondentes no data store. (Não disponível ao usar `simplePaginate`).  |
| `$paginator->url($page)`                | Obtém a URL para um determinado número de página.                                                            |
| `$paginator->getPageName()`             | Obtém a variável de query string usada para armazenar a página.                                              |
| `$paginator->setPageName($name)`        | Define a variável de query string usada para armazenar a página.                                             |
| `$paginator->through($callback)`        | Transforma cada item usando um callback.                                                                     |

</div>

<a id="cursor-paginator-instance-methods"></a>
## Métodos de Instância do Cursor Paginator

Cada instância de cursor paginator fornece informações adicionais de paginação através dos seguintes métodos:

<div class="overflow-auto">

| Método                          | Descrição                                                         |
| ------------------------------- | ----------------------------------------------------------------- |
| `$paginator->count()`           | Obtém o número de itens para a página atual.                      |
| `$paginator->cursor()`          | Obtém a instância de cursor atual.                                |
| `$paginator->getOptions()`      | Obtém as opções do paginator.                                     |
| `$paginator->hasPages()`        | Determina se há itens suficientes para dividir em múltiplas páginas. |
| `$paginator->hasMorePages()`    | Determina se há mais itens no data store.                         |
| `$paginator->getCursorName()`   | Obtém a variável de query string usada para armazenar o cursor.   |
| `$paginator->items()`           | Obtém os itens para a página atual.                               |
| `$paginator->nextCursor()`      | Obtém a instância de cursor para o próximo conjunto de itens.     |
| `$paginator->nextPageUrl()`     | Obtém a URL para a próxima página.                                |
| `$paginator->onFirstPage()`     | Determina se o paginator está na primeira página.                 |
| `$paginator->onLastPage()`      | Determina se o paginator está na última página.                   |
| `$paginator->perPage()`         | O número de itens a serem exibidos por página.                    |
| `$paginator->previousCursor()`  | Obtém a instância de cursor para o conjunto de itens anterior.    |
| `$paginator->previousPageUrl()` | Obtém a URL para a página anterior.                               |
| `$paginator->setCursorName()`   | Define a variável de query string usada para armazenar o cursor.  |
| `$paginator->url($cursor)`      | Obtém a URL para uma determinada instância de cursor.             |

</div>
