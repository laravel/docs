# Banco de dados: Query Builder

- [Introdução](#introduction)
- [Recuperando Resultados](#retrieving-results)
    - [Métodos Agregados](#aggregates)
- [Selects](#selects)
- [Joins](#joins)
- [Unions](#unions)
- [Cláusulas Where](#where-clauses)
    - [Cláusulas Where Avançadas](#advanced-where-clauses)
- [Ordenando, Agrupando, usando Limit e Offset](#ordering-grouping-limit-and-offset)
- [Inserts](#inserts)
- [Updates](#updates)
- [Deletes](#deletes)
- [Pessimistic Locking](#pessimistic-locking)

<a name="introduction"></a>
## Introdução

A query builder provê uma interface fluente para criar e executar instruções de banco de dados. Ela pode ser usada para realizar vários tipos de operações na base de dados da sua aplicação, funcionando em todos os bancos suportados.

> **Nota:** A query builder do Laravel utiliza PDO parameter binding para proteger sua aplicação contra ataques de SQL injection. Não há necessidade de filtrar strings para passá-las como parâmetros.

<a name="retrieving-results"></a>
## Recuperando Resultados

#### Recuperando Todos Os Registros De Uma Tabela

Para começar uma consulta utilize o método `table` do facade `DB`. O método `table` retorna uma instância de query builder fluente para a tabela solicitada, possibilitando que você adicione mais regras a consulta antes de obter o resultado final. Neste exemplo vamos utilizar o `get` para recuperar todos os registros da tabela:

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

Assim como utilizar [SQL puro](/docs/{{version}}/database), o método `get` retorna um `array` de resultados onde cada um é um objeto da classe PHP `StdClass`. Você pode acessar o valor de cada coluna da tabela como uma propriedade do objeto, que possui o mesmo nome da coluna:

    foreach ($users as $user) {
        echo $user->name;
    }

#### Recuperando Um Único Registro / Coluna De Uma Tabela

Se você precisar recuperar um único registro de uma tabela do banco, você pode utilizar o método `first` . Este método irá retornar um único objeto `StdClass`:

    $user = DB::table('users')->where('name', 'John')->first();

    echo $user->name;

Se você não precisa utilizar todas as colunas de um registro, você pode extrair uma única coluna utilizando o método `value`. Este método irá retornar o valor da coluna diretamente:

    $email = DB::table('users')->where('name', 'John')->value('email');

#### Recuperando parte dos resultados de uma tabela

Se você precisar trabalhar com uma tabela  que possui milhares de registros, considere a hipótese de utilizar o método `chunk`. Este método recupera uma pequena "parcela" dos resultados de cada vez, colocando cada parcela dentro de uma `Closure` para ser processada. Este método é muito útil para escrever [comandos do Artisan](/docs/{{version}}/artisan) que processam milhares de registros. Por exemplo, vamos usar a tabela `users` separada em partes de 100 registros por vez:

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

Por conveniência, se você quer simplesmente verificar se uma coluna é igual a um valor , pode passar o valor diretamente no segundo parâmetro do método `where`, suprimindo o operador:

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

#### Agrupando Parâmetros

Algumas vezes você precisa criar cláusulas where mais avançadas como "where exists" ou grupos de parâmetros alinhados. A query builder do Laravel pode lidar com esses casos. Para iniciar, vamos dar uma olhada em um exemplo de como agrupar regras dentro de parênteses:

    DB::table('users')
                ->where('name', '=', 'John')
                ->orWhere(function ($query) {
                    $query->where('votes', '>', 100)
                          ->where('title', '<>', 'Admin');
                })
                ->get();

Como pode ver, passar uma `Closure` dentro do método `orWhere`  diz a query builder para iniciar um grupo de regras. A `Closure` irá receber uma instância da query builder onde você pode colocar as regras que ficariam dentro dos parênteses. O exemplo abaixo irá produzir o seguinte código SQL:

    select * from users where name = 'John' or (votes > 100 and title <> 'Admin')

#### Cláusulas Exists

O método `whereExists` possibilita que você escreva cláusulas SQL `where exist`. O método `whereExists` aceita uma `Closure` como argumento, que irá receber uma instância da query builder possibilitando que você defina a consulta que deve ser passada dentro da cláusula "exists":

    DB::table('users')
                ->whereExists(function ($query) {
                    $query->select(DB::raw(1))
                          ->from('orders')
                          ->whereRaw('orders.user_id = users.id');
                })
                ->get();

A consulta abaixo produzirá o seguinte código SQL:

    select * from users
    where exists (
        select 1 from orders where orders.user_id = users.id
    )

<a name="ordering-grouping-limit-and-offset"></a>
## Ordenando, Agrupando, usando Limit e Offset

#### orderBy

O método `orderBy` possibilita que você ordene o resultado da consulta por uma coluna específica. O primeiro argumento para o método `orderBy` precisa ser o nome da coluna que será ordenada, enquanto o segundo parâmetro controla o tipo de ordenação, `asc` ou `desc`:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

#### groupBy / having / havingRaw

Os métodos `groupBy` e `having` podem ser usados para agrupar resultados da consulta. O uso do método `having` é muito similar ao método `where`:

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

O método `havingRaw` pode ser usado para executar um comando SQL passando-o como parâmetro da cláusula `having`. Por exemplo, nós podemos recuperar todos os departamentos com vendas maiores que $2,500:

    $users = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > 2500')
                    ->get();

#### skip / take

Para limitar o número de resultados retornados pela consulta ou para pular um determinado número de registros da consulta (`OFFSET`), você pode utilizar os métodos `skip` and `take`:

    $users = DB::table('users')->skip(10)->take(5)->get();

<a name="inserts"></a>
## Inserts

A query builder possui o método `insert` para inserir registros em uma tabela. Este método aceita um array de nomes de coluna e valores a serem inseridos:

    DB::table('users')->insert(
        ['email' => 'john@example.com', 'votes' => 0]
    );

Se precisar inserir muitos registros em uma tabela você pode chamar o método `insert` uma única vez, passando como argumento um array de arrays. Cada array representa um registro que será inserido na tabela:

    DB::table('users')->insert([
        ['email' => 'taylor@example.com', 'votes' => 0],
        ['email' => 'dayle@example.com', 'votes' => 0]
    ]);

#### IDs com Incremento Automático

Se a tabela possuir uma coluna id auto-increment, utilize o método `insertGetId` para inserir um registro e recuperar o id:

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

> **Nota:** Ao utilizar PostgreSQL o método insertGetId espera que a coluna com nome `id` seja auto increment. If you would like to retrieve the ID from a different "sequence", you may pass the sequence name as the second parameter to the `insertGetId` method.

<a name="updates"></a>
## Updates

Assim como inserir dados no banco, a query builder também pode atualizar registros usando o método `update`. O método `update`, assim como o método `insert`, aceita um array de colunas e valores a serem atualizados. Você pode criar regras em consultas `update` usando cláusulas `where`:

    DB::table('users')
                ->where('id', 1)
                ->update(['votes' => 1]);

#### Increment / Decrement

A query builder fornece muitos métodos para aumentar ou diminuir o valor de uma determinada coluna. Isto é simplesmente um atalho, provendo uma interface mais espressiva comparada a escrever manualmente uma condição `update`.

Ambos os métodos precisam de um argumento: a coluna a ser modificada. O segundo parâmetro é opcional e controla a quantia que a coluna será acrescida / diminuída.

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

Você pode também especificar colunas adicionais a serem atualizadas durante a operação:

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

<a name="deletes"></a>
## Deletes

A query builder também pode ser usada para deletar registros de uma tabela através do método `delete`:

    DB::table('users')->delete();

Você pode customizar as regras do `delete` acrescentando cláusulas `where` antes de chamar o método `delete`:

    DB::table('users')->where('votes', '<', 100)->delete();

Se precisar truncar uma tabela, remover todos os registros e resetar as colunas ID auto-increment para zero, você pode utilizar o método `truncate`:

    DB::table('users')->truncate();

<a name="pessimistic-locking"></a>
## Pessimistic Locking

A query builder inclui também algumas funções para ajudá-lo a "pessimistic locking" nas suas cláusulas `select`. Para executar uma cláusula com "shared lock" você pode utilizar o método `sharedLock` na consulta. A shared lock previne que os registros selecionados sejam modificados until your transaction commits:

    DB::table('users')->where('votes', '>', 100)->sharedLock()->get();

Alternativamente, você pode utilizar o método `lockForUpdate`. A "for update" lock previne que registros sejam modificados ou sejam selecionados em outra shared lock:

    DB::table('users')->where('votes', '>', 100)->lockForUpdate()->get();
