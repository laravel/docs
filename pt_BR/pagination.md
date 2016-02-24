# Paginação

- [Introdução](#introduction)
- [Uso Básico](#basic-usage)
    - [Paginando Resultados De Uma Consulta](#paginating-query-builder-results)
    - [Paginando Resultados Do Eloquent](#paginating-eloquent-results)
    - [Criando Uma Paginação Manual](#manually-creating-a-paginator)
- [Exibindo Resultados Em Uma View](#displaying-results-in-a-view)
- [Convertendo Resultados Para JSON](#converting-results-to-json)

<a name="introduction"></a>
## Introdução

Em outros frameworks paginação pode ser algo cansativo. O Laravel torna esse trabalho extremamente fácil. O Laravel pode gerar rapidamente e de forma inteligente uma série de links baseando-se na página atual, além do HTML gerado ser compatível com o [framework CSS Bootstrap](http://getbootstrap.com/).

<a name="basic-usage"></a>
## Uso básico

<a name="paginating-query-builder-results"></a>
### Paginando Resultados De Uma Consulta

Existem várias maneiras de "paginar" itens. A mais fácil é utilizar o método `paginate` da [query builder](/docs/{{version}}/queries) ou de uma [consulta do Eloquent](/docs/{{version}}/eloquent). O método `paginate` fornecido pelo Laravel automaticamente lida com as páginas baseado na página atual vista pelo usuário. Por padrão, a página atual é reconhecida pelo valor do parâmetro `?page` na requisição HTTP. Essa página é automaticamente inserida nos links gerados pela paginação.

Inicialmente, vamos dar uma olhada em como chamar o método `paginate` em uma consulta. Neste exemplo, o único argumento passado para o `paginate` foi o número de itens que serão exibidos por página. Neste caso, especificamos `15` itens por página:

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show all of the users for the application.
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::table('users')->paginate(15);

            return view('user.index', ['users' => $users]);
        }
    }

> **Nota:** Atualmente operações de paginação utilizando o método `groupBy` não podem ser executadas corretamente no Laravel. Se você precisa utilizar o `groupBy` com os resultados de uma paginação, é recomendado que você execute a consulta ao banco e crie uma paginação manualmente.

#### Paginação Simples

Se você precisa somente exibir links para "Próximo" e "Anterior" na sua view utilizando paginação, você tem a opção de utilizar o método  `simplePaginate` e executar uma consulta mais eficiente. Isso é muito útil em consultas que retornam muitos registros e você não precisa exibir um link para cada página gerada:

    $users = DB::table('users')->simplePaginate(15);

<a name="paginating-eloquent-results"></a>
### Paginando Resultados Do Eloquent

Você tembém pode utilizar paginação nos resultados de consultas do [Eloquent](/docs/{{version}}/eloquent). Neste exemplo, nós iremos "paginar" o model `User` exibindo `15` itens por página. Como você pode ver, a sintaxe é idêntica a paginar resultados de uma consulta comum:

    $users = App\User::paginate(15);

Você também pode chamar o `paginate` depois de encadear outros métodos da query builder, como cláusulas `where` por exemplo:

    $users = User::where('votes', '>', 100)->paginate(15);

O método `simplePaginate` também está disponível ao "paginar" models do Eloquent:

    $users = User::where('votes', '>', 100)->simplePaginate(15);

<a name="manually-creating-a-paginator"></a>
### Criando Uma Paginação Manual

Algumas vezes você precisa criar uma paginação manualmente, passando um array de itens. Você pode utilizar uma instância de `Illuminate\Pagination\Paginator` ou `Illuminate\Pagination\LengthAwarePaginator`, dependendo das suas necessidades.

A classe `Paginator` não precisa ter conhecimento da quantidade de itens do resultado, por conta disso a classe não tem métodos para obter a primeira ou a última página. A classe `LengthAwarePaginator` aceita os mesmos argumentos que a classe `Paginator`, contudo ela  requer a quantidade de itens a serem paginados.

Em outras palavras, `Paginator` corresponde ao método `simplePaginate` das consultas, enquanto `LengthAwarePaginator` corresponde ao método `paginate`.

Ao criar manualmente uma instância para paginação você deve "dividir" o array de resultados que você passa a classe. Se você não sabe como fazer isso, dê uma olhada na função PHP [array_slice](http://php.net/manual/en/function.array-slice.php).

<a name="displaying-results-in-a-view"></a>
## Exibindo Resultados Em Uma View

Quando você chama os métodos `paginate` ou `simplePaginate` em uma consulta, você recebe uma instância da classe de paginação.  Ao utilizar o método `paginate`, você receberá uma instância de `Illuminate\Pagination\LengthAwarePaginator`. Ao chamar o método `simplePaginate`, você receberá uma instância de `Illuminate\Pagination\Paginator`. Estes objetos possuem uma série de métodos para exibir os resultados. Adicionalmente, as instâncias podem ser exibidas em um loop como um array.

Você pode exibir os resultados da paginação utilizando o [Blade](/docs/{{version}}/blade):

    <div class="container">
        @foreach ($users as $user)
            {{ $user->name }}
        @endforeach
    </div>

    {!! $users->render() !!}

O método `render` irá renderizar o restante dos links para as demais páginas dos resultados. Cada um desses links irá conter um parâmetro `?page` variável. Lembre-se, o HTML gerado pelo método `render` é compatível com o [framework CSS Bootstrap](https://getbootstrap.com).

> **Nota:** Ao chamar o método `render` de um template Blade, certifique-se de utilizar a sintaxe `{!! !!}`, caso contrário o HTML não será interpretado.

#### Customizando A URI Da Paginação

O método `setPath` possibilita que você customize a URI usada para gerar os links. Por exemplo, se você precisa que a paginação seja gerada com os links nesse padrão `http://example.com/custom/url?page=N`, passe `custom/url` como um parâmetro para o método `setPath`:

    Route::get('users', function () {
        $users = App\User::paginate(15);

        $users->setPath('custom/url');

        //
    });

#### Adicionando Parâmetros Para Os Links Da Paginação

Você pode adicionar parâmetros aos links da paginação utilizando o método `appends`. Neste exemplo, adicionamos `&sort=votes` para cada link da paginação:

    {!! $users->appends(['sort' => 'votes'])->render() !!}

Caso precise adicionar uma âncora para a url de paginação, utilize o método `fragment`. Por exemplo, para adicionar `#foo` no final de cada link:

    {!! $users->fragment('foo')->render() !!}

#### Métodos Úteis Adicionais

Você pode acessar informações adicionais da paginação através dos seguintes métodos em uma instância do paginator:

- `$results->count()`
- `$results->currentPage()`
- `$results->hasMorePages()`
- `$results->lastPage() (Not available when using simplePaginate)`
- `$results->nextPageUrl()`
- `$results->perPage()`
- `$results->previousPageUrl()`
- `$results->total() (Not available when using simplePaginate)`
- `$results->url($page)`

<a name="converting-results-to-json"></a>
## Convertendo Resultados Para JSON

As classes de paginação do Laravel implementam o contrato `Illuminate\Contracts\Support\JsonableInterface` e possuem o método `toJson`, sendo assim muito fácil converter seus resultados de paginação para JSON.

Você pode converter sua instância do paginator para JSON simplesmente retornando-a de uma rota ou ação do controller:

    Route::get('users', function () {
        return App\User::paginate();
    });

O JSON do paginator incluirá informações como `total`, `current_page`, `last_page` entre outras. O resultado estará disponível na chave `data` no array JSON. Aqui temos um exemplo de JSON criado retornando uma instância do paginator de uma rota:

#### Exemplo De Paginação Em JSON

    {
       "total": 50,
       "per_page": 15,
       "current_page": 1,
       "last_page": 4,
       "next_page_url": "http://laravel.app?page=2",
       "prev_page_url": null,
       "from": 1,
       "to": 15,
       "data":[
            {
                // Result Object
            },
            {
                // Result Object
            }
       ]
    }
