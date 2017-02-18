# Banco de dados: Query Builder

- [Introdução](#introduction)
- [Recuperando Resultados](#retrieving-results)
    - [Aggregates](#aggregates)
- [Selects](#selects)
- [Joins](#joins)
- [Unions](#unions)
- [Cláusulas Where](#where-clauses)
    - [Cláusulas Where Avançadas](#advanced-where-clauses)
- [Ordenando, Agrupando, usando Limit e Offset](#ordering-grouping-limit-and-offset)
- [Inserts](#inserts)
- [Updates](#updates)
- [Deletes](#deletes)
- [Bloqueio Pessimista](#pessimistic-locking)

<a name="introduction"></a>
## Introdução

O query builder provê uma interface fluente para criar e executar instruções de banco de dados. Ele pode ser usado para realizar vários tipos de operações de base de dados na sua aplicação, funcionando em todos os bancos suportados.

> **Nota:** O query builder do Laravel utiliza PDO parameter binding para proteger sua aplicação contra ataques de SQL injection. Não há necessidade de filtrar strings para passá-las como parâmetros.

<a name="retrieving-results"></a>
## Recuperando Resultados

#### Recuperando Todos Os Registros De Uma Tabela

Ao começar uma query, utilize o método `table` da facade `DB`. O método `table` retorna uma instância de query builder fluente para a tabela solicitada, possibilitando que você adicione mais regras a query antes de obter o resultado final. Neste exemplo vamos utilizar o `get` para recuperar todos os registros da tabela:

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show a list of all of the application's users.
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::table('users')->get();

            return view('user.index', ['users' => $users]);
        }
    }

Assim como utilizar [SQL puro](/docs/{{version}}/database), o método `get` retorna um`array` de resultados onde cada um é um objeto da classe PHP `StdClass`. Você pode acessar o valor de cada coluna da tabela como uma propriedade do objeto, que possui o mesmo nome da coluna:

    foreach ($users as $user) {
        echo $user->name;
    }

#### Recuperando Um Único Registro / Coluna De Uma Tabela

Se você somente precisar recuperar um único registro de uma tabela do banco, você pode utilizar o método `first` . Este método irá retornar um único objeto `StdClass`:

    $user = DB::table('users')->where('name', 'John')->first();

    echo $user->name;

Se você não precisa utilizar todas as colunas de um registro, você pode extrair uma única coluna utilizando o método value. Este método irá retornar o valor da coluna diretamente:

    $email = DB::table('users')->where('name', 'John')->value('email');

#### Recuperando parte dos resultados de uma tabela

Se você precisa trabalhar com uma tabela  que possui milhares de registros, considere a hipótese de utilizar o método `chunk`. Este método recupera uma pequena "parcela" dos resultados de cada vez, e coloca cada parcela dentro de uma `Closure` para ser processada. Este método é muito útil para escrever [comandos do Artisan](/docs/{{version}}/artisan) que processam milhares de registros. Por exemplo, vamos usar a tabela `users` separada em partes de 100 registros por vez:

    DB::table('users')->chunk(100, function($users) {
        foreach ($users as $user) {
            //
        }
    });

Você pode parar o processamento das "parcelas" retornando `false` dentro da `Closure`:

    DB::table('users')->chunk(100, function($users) {
        // Process the records...

        return false;
    });

#### Recuperando Uma Lista De Valores De Coluna

Se você precisa recuperar um array contendo os valores de uma única coluna, você pode utilizar o método `lists`. Neste exemplo, nós recuperamos um array de títulos de permissões:

    $titles = DB::table('roles')->lists('title');

    foreach ($titles as $title) {
        echo $title;
    }

 
Você também pode especificar uma custom key  para a coluna no array retornado:

    $roles = DB::table('roles')->lists('title', 'name');

    foreach ($roles as $name => $title) {
        echo $title;
    }

<a name="aggregates"></a>
### Métodos Agregados

O query builder provê uma variedade de métodos agregados, como `count`, `max`, `min`, `avg` e `sum`. Você pode chamar qualquer um destes métodos após construir sua query:

    $users = DB::table('users')->count();

    $price = DB::table('orders')->max('price');

Alternativamente, você pode combinar esses métodos com outras cláusulas para montar sua query:

    $price = DB::table('orders')
                    ->where('finalized', 1)
                    ->avg('price');

<a name="selects"></a>
## Selects

#### Especificando Uma Regra Para O Select

Você nem sempre precisará recuperar todas as colunas de sua tabela. Usando o método `select` pode ser especificada uma regra para recuperar os dados:

    $users = DB::table('users')->select('name', 'email as user_email')->get();

O método `distinct` possibilita que você obrigue a query a retornar resultados distintos:

    $users = DB::table('users')->distinct()->get();

Se já possuir uma instância de query builder e precisar adicionar uma coluna para ser incluída no select, você pode utilizar o método `addSelect`:

    $query = DB::table('users')->select('name');

    $users = $query->addSelect('age')->get();

#### Instruções SQL

Em alguns momentos você talvez precise utilizar instruções com SQL puro em uma query. Essas instruções serão injetadas dentro da query como uma string, logo tenha muito cuidado para não criar brechas para ataques SQL Injection! Para utilizar essas instruções use o método `DB::raw`:

    $users = DB::table('users')
                         ->select(DB::raw('count(*) as user_count, status'))
                         ->where('status', '<>', 1)
                         ->groupBy('status')
                         ->get();

<a name="joins"></a>
## Joins

#### Utilizando Inner Join

A query builder pode ser utilizada para escrever sentenças join. Para executar um "inner join" você pode utilizar o método `join` em uma instância da query builder. O primeiro argumento passado para o método `join` é o nome da tabela que você precisa realizar a junção enquanto que os demais argumentos especificam as restrições de coluna para a junção. Como pode ver, você pode executar o join com várias tabelas em uma única consulta:    

    $users = DB::table('users')
                ->join('contacts', 'users.id', '=', 'contacts.user_id')
                ->join('orders', 'users.id', '=', 'orders.user_id')
                ->select('users.*', 'contacts.phone', 'orders.price')
                ->get();

#### Utilizando Left Join

Se você precisa executar um "left join" ao invés de um "inner join", utilize o método `leftJoin`. Este método aceita os mesmos parâmetros do `join`:

    $users = DB::table('users')
                ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

#### Sentenças Join Avançadas

Você pode especificar regras mais avançadas para o join. Inicialmente, passe uma `Closure` como segundo argumento no método `join`. A `Closure`  irá receber um objeto `JoinClause` que lhe possibilitará especificar regras `join` mais complexas:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')->orOn(...);
            })
            ->get();

Caso seja necessário utilizar cláusulas "where" com os seus joins, você pode utilizar os métodos `where` e `orWhere` com o join. Ao invés de comparar duas colunas estes métodos vão comparar a coluna com o valor especificado:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')
                     ->where('contacts.user_id', '>', 5);
            })
            ->get();

<a name="unions"></a>
## Unions

A query builder provê uma forma rápida de "unir" duas consultas. Por exemplo, você pode criar uma consulta inicial e posteriormente utilizar o método `union` para anexar uma segunda consulta:

    $first = DB::table('users')
                ->whereNull('first_name');

    $users = DB::table('users')
                ->whereNull('last_name')
                ->union($first)
                ->get();

O método `unionAll` também está disponível e funciona da mesma forma que o `union`.

<a name="where-clauses"></a>
## Cláusulas Where

#### Cláusulas Where Simples

Para adicionar cláusulas `where` a sua consulta, utilize o método `where` em uma instância da query builder. A foma mais básica de utilização do `where` requer três argumentos. O primeiro argumento é o nome da coluna. O segundo um operador, que pode ser qualquer um dos operadores suportados por banco de dados. O terceiro argumento é o valor que será comparado com a coluna.

Por exemplo, aqui temos uma consulta que verifica se o valor da coluna "votes" é igual a 100:

    $users = DB::table('users')->where('votes', '=', 100)->get();

Por conveniência, se você quer simplesmente verificar se uma coluna é igual a um valor , pode passar o valor diretamente no segundo parâmetro do método where `where`, suprimindo o operador:

    $users = DB::table('users')->where('votes', 100)->get();

Existe uma variedade de operadores que podem ser usados ao escrever uma cláusula `where`:

    $users = DB::table('users')
                    ->where('votes', '>=', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('votes', '<>', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('name', 'like', 'T%')
                    ->get();

#### Cláusulas Or

Assim como você pode encadear condições where, também é possível adicionar cláusulas `or` na consulta. O método `orWhere` aceita os mesmos argumentos do método `where`:

    $users = DB::table('users')
                        ->where('votes', '>', 100)
                        ->orWhere('name', 'John')
                        ->get();

#### Cláusulas Where Adicionais

**whereBetween**

O método `whereBetween` verifica se o valor de uma coluna está entre dois valores:

    $users = DB::table('users')
                        ->whereBetween('votes', [1, 100])->get();

**whereNotBetween**

O método `whereNotBetween` verifica se o valor de uma coluna **não** está entre dois valores:

    $users = DB::table('users')
                        ->whereNotBetween('votes', [1, 100])
                        ->get();

**whereIn / whereNotIn**

O método `whereIn` verifica se o valor da coluna informada existe no array passado no segundo parâmetro:

    $users = DB::table('users')
                        ->whereIn('id', [1, 2, 3])
                        ->get();

O método `whereNotIn` verifica se o valor da coluna informada **não** existe no array passado no segundo parâmetro:

    $users = DB::table('users')
                        ->whereNotIn('id', [1, 2, 3])
                        ->get();

**whereNull / whereNotNull**

O método `whereNull` verifica se o valor da coluna informada é `NULL`:

    $users = DB::table('users')
                        ->whereNull('updated_at')
                        ->get();

O método `whereNotNull` verifica se o valor da coluna informada **not** é `NULL`:

    $users = DB::table('users')
                        ->whereNotNull('updated_at')
                        ->get();

<a name="advanced-where-clauses"></a>
## Cláusulas Where Avançadas

#### Agrupar parâmetros

Algumas vezes você pode precisar criar cláusulas where mais avançadas, como as "where exists", ou o criar agrupamentos de parâmetros. O Laravel query builder tem a capacidade de realizar isso também. Para iniciar, vamos ver um exemplo de agrupamento de restrições dentro de parênteses:

    DB::table('users')
                ->where('name', '=', 'John')
                ->orWhere(function ($query) {
                    $query->where('votes', '>', 100)
                          ->where('title', '<>', 'Admin');
                })
                ->get();

Como você pode ver, passando uma `Closure` para o método `orWhere` instrui o query builder a iniciar um agrupamento de restrições de restrições. A `Closure` receberá uma instância da query builder a qual você poderá utilizar para definir as restrições que deverão estar contidas no agrupamento entre parênteses. O exemplo acima produzirá a seguinte comando SQL:

    select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Sentença Exists 

O método `whereExists` permite que você escreva uma cláusula SQL `where exist`. O método `whereExists` aceita um argumento `Closure`, que receberá uma instância de query builder, permitindo que você defina a query que deverá ser colocada dentro da cláusula "exists":

    DB::table('users')
                ->whereExists(function ($query) {
                    $query->select(DB::raw(1))
                          ->from('orders')
                          ->whereRaw('orders.user_id = users.id');
                })
                ->get();

A query acima produzirá o seguinte SQL:

    select * from users
    where exists (
        select 1 from orders where orders.user_id = users.id
    )

<a name="ordering-grouping-limit-and-offset"></a>
## Ordenando, Agrupando, usando Limit e Offset

#### orderBy

O método `orderBy` permite que você ordene o resultado de uma query por uma determinada coluna. O primeiro argumento para o método `orderBy` será a coluna que você utilizará para ordenar, enquanto que o segundo argumento controlará a direção da ordem e pode ser `asc` ou `desc`:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

#### groupBy / having / havingRaw

Os métodos `groupBy` e `having` podem ser utilizados para agrupar os resultados da query. A assinatura do método `having` é similar à do método `where`:

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();


O método `havingRaw` pode ser utilizado para definir um texto puro como um valor para a cláusula `having`. Por exemplo, nós podemos encontrar todos os departamentos com vendas acima de $2.500:

    $users = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > 2500')
                    ->get();

#### skip / take

Para limitar o número de resultados retornados da query, ou para saltar uma quantidade definida de resultados na query (`OFFSET`), você pode utilizar os métodos `skip` e `take`:

    $users = DB::table('users')->skip(10)->take(5)->get();

<a name="inserts"></a>
## Inserts

A query builder também provê um método `insert` para adicionar registros à tabela do banco de dados. O método `insert` aceita um array de nomes de colunas e valores que desejamos incluir:

    DB::table('users')->insert(
        ['email' => 'john@example.com', 'votes' => 0]
    );

Você pode até inserir vários registros na tabela com uma única chamada ao método `insert` passando um array de arrays. Cada array representa uma linha a ser incluída na tabela:

    DB::table('users')->insert([
        ['email' => 'taylor@example.com', 'votes' => 0],
        ['email' => 'dayle@example.com', 'votes' => 0]
    ]);

#### IDs auto-incrementadas

Se a tabela possui uma id auto-incrementada, utilize o método `insertGetId` para inserir o registro e então retornar a ID:

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

> **Nota:** Quando estiver usando o PostgreSQL o método `insertGetId` espera uma coluna auto-incrementada com o nome `id`. Se você gostaria de recuperar a ID de uma "sequence" diferente, você deve passar o nome da "sequence" como o segundo parâmetro do método `insertGetId`.

<a name="updates"></a>
## Updates

Claro, complementarmente à inserção de registros no banco de dados, a query builder também pode atualizar registros existentes com o método `update`. O método `update`, da mesma forma que o método `insert`, aceita um array de pares de colunas e valores contendo as colunas a serem atualizadas. Você pode restringir a query de `update` utilizando uma cláusula `where`:

    DB::table('users')
                ->where('id', 1)
                ->update(['votes' => 1]);

#### Incremento / Decremento

A query builder também provê métodos convenientes para incrementar e decrementar o valor de uma determinada coluna. Isso é apenas um atalho, fornecendo uma interface mais expressiva e concisa quando comparada a manualmente escrever uma cláusula `update`.

Ambos os métodos aceitam pelo menos um argumento: a coluna que se deseja modificar. Um segundo argumento pode ser passado opcionalmente para se informar o valor com o qual a coluna deverá ser incrementada / decrementada.

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

Você pode também especificar colunas adicionais para serem atualizadas durante a operação:

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="deletes"></a>
## Exclusões

Naturalmente, a query builder pode também ser utilizada para excluir registros de uma tabela através do método `delete`:

    DB::table('users')->delete();

Você pode restringir as sentenças `delete` adicionando cláusulas `where` antes de chamar o método `delete`:

    DB::table('users')->where('votes', '<', 100)->delete();

Se você deseja truncar a tabela inteira, o que removerá todas as linhas e reinicializará a ID auto-incrementada para zero, você poderá utilizar o método `truncate`:

    DB::table('users')->truncate();

<a name="pessimistic-locking"></a>
## Bloqueio Pessimista

A query builder também inclui algumas funções para lhe ajudar a realizar um "bloqueio pessimista" nas suas declarações `select`. Para executar uma sentença com um "bloqueio compartilhado", você pode usar o método `sharedLock` na query. Um bloqueio compartilhado previne que as linhas selecionadas sejam modificadas até que a sua transação seja efetivada (commited):

    DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

Alternativamente, você pode utilizar o método `lockForUpdate`. Um bloqueio "para atualização" previne que as linhas sejam modificadas ou de serem selecionadas através de outro bloqueio compartilhado:

    DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
