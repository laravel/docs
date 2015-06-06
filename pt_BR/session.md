# Sessão

- [Introdução](#introduction)
- [O Básico](#basic-usage)
    - [Dados Flash](#flash-data)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)

<a name="introduction"></a>
## Introdução

Visto que aplicações HTTP são stateless, as sessões fornecem uma forma de armazenar informações sobre o usuário durante as requisições. O Laravel já vem com uma variedade de back-ends de sessão para um uso limpo, a partir de uma API unificada. Tem suporte para back-ends populares tais como [Memcached](http://memcached.org), [Redis](http://redis.io) e banco de dados.

### Configuração

O arquivo de configuração da sessão está localizado em `config/session.php`. Certifique-se de revisar as opcões disponíveis, bem documentadas, neste arquivo (em inglês). Por padrão, o Laravel vem configurado para usar o driver de sessão em arquivos (`file`), que irá funcionar bem para a maioria das aplicações. Em aplicações de produção, você deve considerar usar os drivers `memcached` ou `redis` para obter melhor performance.

O `driver` de sessão define onde os dados da sessão serão armazenados para cada requisição. O Laravel já vem com vários bons drivers:

<div class="content-list" markdown="1">
- `file` - sessões são armazenadas na pasta `storage/framework/sessions`.
- `cookie` - sessões são armazenadas em cookies seguros e criptografados.
- `database` - sessões são armazenadas em um banco de dados usado por sua aplicação.
- `memcached` / `redis` - sessões são armazenadas em uma destas rápidas ferramentas, em memória.
- `array` - sessões são armazenadas em um simples array PHP e não irá persistir durante as requisições.
</div>

> **Note:** O driver array é utilizado para rodar [testes](/docs/{{version}}/testing) para evitar que os dados da sessão sejam persistidos/salvos.

### Pré-requisitos dos Drivers

#### Banco de dados

Quando estiver utilizando o driver de sessão `database`, você precisará configurar uma tabela para popular os items de sessão. Abaixo está um exemplo de declaração do `Schema` para a tabela:

    Schema::create('sessions', function ($table) {
        $table->string('id')->unique();
        $table->text('payload');
        $table->integer('last_activity');
    });

Você pode utilizar comando Artisan `session:table` para gerar este arquivo de migration para você!

    php artisan session:table

    composer dump-autoload

    php artisan migrate

#### Redis

Antes de utilizar sessões com Redis no Laravel, você precisará instalar o pacote `predis/predis` (~1.0) via Composer.

### Outras Considerações Sobre Sessão

O framework Laravel utiliza sessões `flash` internamente, então você não deve adicionar um item na sessão com este nome.

Se você precisar armazenar dados na sessão criptografados, configure a opção `encrypt` como `true`.

<a name="basic-usage"></a>
## O Básico

#### Acessando A Sessão

Primeiro, vamos acessar a sessão. Nós podemos acessar uma instância da sessão da requisição HTTP, que pode ser type-hinted em um método do controller. Lembre-se, as dependências de um método do controller são injetados pelo [service container](/docs/{{version}}/container) do Laravel:

    <?php namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Exibe o perfil de determinado usuário
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function showProfile(Request $request, $id)
        {
            $valor = $request->session()->get('chave');

            //
        }
    }

Quando você tenta pegar um valor da sessão, você também pode passar um valor padrão como segundo argumento para o método `get`. Este valor padrão será retornado se a chave que você está buscando não existir na sessão. Se você passar uma `Closure` como valor padrão para o método `get`, a `Closure` será executada e seu valor retornado:

    $valor = $request->session()->get('chave', 'padrao');

    $valor = $request->session()->get('chave', function() {
        return 'padrao';
    });

Caso você queira pegar todos os dados da sessão, você pode usar o método `all`:

    $dados = $request->session()->all();

Você também pode usar a função global `session` para pegar e armazenar dados na sessão:

    Route::get('home', function () {
        // Obtém algum dado da sessão...
        $valor = session('chave');

        // Armazena algum dado na sessão
        session(['chave' => 'valor']);
    });

#### Verificando Se Um Item Existe na Sessão

O método `has` pode ser usado para verificar se um item existe na sessão. Este método irá retornar `true` se o item existir:

    if ($request->session()->has('usuarios')) {
        //
    }

#### Armazenando Dados Na Sessão

Uma vez que você acessa a instância de sessão, você pode chamar uma variedade de funções para interagir com seus dados. Por exemplo, o método `put` armazena um novo dado na sessão:

    $request->session()->put('chave', 'valor');

#### Adicionando Valor para Arrays na Sessão

O método `push` pode ser usado para adicionar um novo valor em um item da sessão que seja um array. Por exemplo, se a chave `usuario.times` contém um array com os nomes dos times, você pode adicionar um novo item no array da seguinte forma:

    $request->session()->push('usuario.times', 'desenvolvedores');

#### Retornando E Deletando um Item

O método `pull` irá retornar e apagar um item da sessão:

    $valor = $request->session()->pull('chave', 'padrão');

#### Deletando Itens Da Sessão

O método `forget` irá remover um dado da sessão. Se você precisar remover todos os dados da sessão, você pode utilizar o método `flush`:

    $request->session()->forget('chave');

    $request->session()->flush();

#### Gerando Um Novo ID de Sessão

Se você precisa gerar um novo ID para sessão, você pode utilizar o método `regenerate`:

    $request->session()->regenerate();

<a name="flash-data"></a>
### Dados Flash

As vezes você precisará gravar itens na sessão apenas até a próxima requisição. Você pode fazer isto utilizando o método `flash`. Utilizando este método os dados estarão disponíveis apenas até a próxima requisição HTTP, e então será apagado. Dados flash são úteis para mensagens de status:

    $request->session()->flash('status', 'Usuário cadastrado com sucesso!');

Se você precisar manter seus dados flash para mais requisições, você pode utilizar o método `reflash`, que irá manter todos os dados até  mais uma requisição. Se você precisar manter apenas um dado específico, você pode utilizar o método `keep`:

    $request->session()->reflash();

    $request->session()->keep(['usuario', 'email']);

<a name="adding-custom-session-drivers"></a>
## Adicionando Drivers de Sessão Personalizados

Para adicionar back-ends de drivers de sessão do Laravel, você deve utilizar o método `extend` no [facade](/docs/{{version}}/session) `Session`. Você pode chamar o método `extend` a partir do método `boot` de um [service provider](/docs/{{version}}/providers):

    <?php namespace App\Providers;

    use Session;
    use App\Extensions\MongoSessionStore;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * Ações após inicio dos serviços
         *
         * @return void
         */
        public function boot()
        {
            Session::extend('mongo', function($app) {
                // Returna a implementação da interface SessionHandlerInterface...
                return new MongoSessionStore;
            });
        }

        /**
         * Registrar bindings no container
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

Observe que seu driver personalizado deve implementar a interface `SessionHandlerInterface`. Esta interface contém apenas alguns poucos métodos necessários para a implementação. Uma implementação para MongoDB ficaria com os seguintes métodos:

    <?php namespace App\Extensions;

    class MongoHandler implements SessionHandlerInterface
    {
        public function open($savePath, $sessionName) {}
        public function close() {}
        public function read($sessionId) {}
        public function write($sessionId, $data) {}
        public function destroy($sessionId) {}
        public function gc($lifetime) {}
    }

Visto que estes métodos não são tão legíveis quanto a interface de cache `StoreInterface`, vamos explicar o que cada método faz:

<div class="content-list" markdown="1">
- O método `open` seria usado tipicamente em armazenamentos baseados em arquivos. Como o Laravel vem com o  driver de sessão `file`, você provavelmente nunca precisará colocar nada neste método. Você pode deixá-lo em branco. Este é o simples caso de um design de interface pobre (que iremos discutir mais tarde) que o PHP nos obriga a implementar.
- O método `close`, como o método `open`, também pode geralmente ser desconsiderado. Para a maioria dos drivers, ele não é necessário.
- O método `read` deve retornar uma string com a versão dos dados de sessão associados a chave `$sessionId`. Não é necessário fazer nenhuma serialização ou qualquer outro codifição quando estiver retornando ou armazenando dados na sessão no seu driver, já que o Laravel irá fazer a serialização para você.
- O método `write` deve escrever o valor de `$data` associado a `$sessionId` em algum sistema de armazenamento persistente, tal como MongoDB, Dynamo, etc.
- O método `destroy` deve remover um dado associado com a `$sessionId` do armazenamento persistente.
- O método `gc` deve remover todos os dados da sessão que é mais antigo do que `$lifetime`, que é um timestamp UNIX. Para mecanismos que gerenciam expiração automaticamente, tais como Memcached e Redis, este método pode ser deixado vazio.
</div>

Uma vez que o driver for registrado, você pode usar o driver `mongo` driver no seu arquivo de configuração `config/session.php`.
