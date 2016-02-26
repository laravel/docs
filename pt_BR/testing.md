# Testando

- [Introdução](#introduction)
- [Testando a Aplicação](#application-testing)
    - [Interagindo com sua Aplicação](#interacting-with-your-application)
    - [Testand APIs JSON](#testing-json-apis)
    - [Sessões / Autênticação](#sessions-and-authentication)
    - [Desativando Middleware](#disabling-middleware)
    - [Requisições HTTP customizadas](#custom-http-requests)
- [Trabalhando com Banco de Dados](#working-with-databases)
    - [Resetando o Banco de Dados após cada teste](#resetting-the-database-after-each-test)
    - [Model Factories](#model-factories)
- [Mocking](#mocking)
    - [Mocking Events](#mocking-events)
    - [Mocking Jobs](#mocking-jobs)
    - [Mocking Facades](#mocking-facades)

<a name="introduction"></a>
## Introdução

Laravel foi construido com testes em mente. O suporte aos testes com PHPUnit já está incluso e um arquivo `phpunit.xml` já está configurado para sua aplicação. O framework também conta com diversos helpers (métodos de ajuda) permitindo que você teste sua aplicação.

O arquivo chamado `ExampleTest.php` está dentro do diretório  `tests`. Após criar uma nova aplicação com o Laravel, simplesmente execute `phpunit` na linha de comando para rodar seus testes.

### Ambiente de Teste

Quando estiver rodando os testes o Laravel irá automaticamente mudar a configuração de ambiente para `testing`. Enquanto estiver testando o Laravel automaticamente configura a sessão e o cache para o driver `array` garantindo que nenhuma informação irá persistir.

Você é livre para criar outra configuração para o ambiente de teste caso ache necessário. As variáveis do ambiente quando `testing` podem ser configuradas no arquivo `phpunit.xml`.

### Definindo e Rodando os Testes

Para criar um teste, simplesmente crie um novo arquivo no diretório `tests`. A classe de teste pode extender `TestCase`. Você então pode definir os métodos de teste como normalmente faria usando PHPUnit. Para rodar seus testes simplesmente execute `phpunit` na linha de comando:

    <?php

    class FooTest extends TestCase
    {
        public function testSomethingIsTrue()
        {
            $this->assertTrue(true);
        }
    }

> **Nota:** Se você definir seu próprio método `setUp` lembre-se de chamar `parent::setUp`.

<a name="application-testing"></a>
## Testando a Aplicação

O Laravel contém uma excelente API para fazer requisições HTTP, examinando o retorno da requisição e preenchendo formulário. Por exemplo, dê uma olhada no arquivo `ExampleTeste.php` que está no diretório `tests`:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5')
                 ->dontSee('Rails');
        }
    }

O método `visit` faz uma requisição `GET` dentro da aplicação. O método `see` verifica se o texto determinado está na resposta da aplicação. O método `dontSee` verifica se o texto determinado não foi retornado pela resposta da requisição.
Este é o teste mais básico que você pode fazer com o Laravel.

<a name="interacting-with-your-application"></a>
### Interagindo com sua Aplicação

Claro que você pode fazer muito mais que uma simples verificação se o algum texto existe ou não. Vamos ver alguns exemplos de como clicar em links e preencher formulários:

#### Clicando em Links

Neste teste nós iremos fazer uma requisição para a aplicação, clicar em um link na resposta e verificar que você foi enviado para a página correta através da URI. Por exemplo, vamos assumir que este é o link da sua aplicação com o conteúdo "About Us":

    <a href="/about-us">About Us</a>

Agora vamos escrever um teste para clicar no link e verificar se o usuário foi para a página correta.

    public function testBasicExample()
    {
        $this->visit('/')
             ->click('About Us')
             ->seePageIs('/about-us');
    }

#### Trabalhando com Formulários

Laravel também conta com diversos métodos para testar formulário. Métodos como `type`, `select`, `check`, `attach` e `press` permitem que você interaja com todos os campos do formulário. Por exemplo, vamos imaginar que este formulário é o formulário da página de cadastro da sua aplicação:

    <form action="/register" method="POST">
        {!! csrf_field() !!}

        <div>
            Name: <input type="text" name="name">
        </div>

        <div>
            <input type="checkbox" value="yes" name="terms"> Accept Terms
        </div>

        <div>
            <input type="submit" value="Register">
        </div>
    </form>

Nós podemos escrever um teste para completar este formulário e verificar o resultado:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

Claro que se o formulário conter outros campos como radio buttons ou dropdowns, você pode facilmente preencher estes campos normalmente. Aqui está uma lista para cada método de manipulação:

Método  | Descrição
------------- | -------------
`$this->type($text, $elementName)`  |  "Escreve" o texto dentro do campo determinado.
`$this->select($value, $elementName)`  |  "Seleciona" um campo de dropdown ou radio button.
`$this->check($elementName)`  |  "Marca" um checkbox.
`$this->attach($pathToFile, $elementName)`  |  "Anexa" um arquivo no formulário.
`$this->press($buttonTextOrElementName)`  |  "Aperta" o botão com o valor determinado.

#### Trabalhando com Anexos

Se o seu formulário contem campos do tipo `file`, você poderá anexar arquivos usando o método `attach`:

    public function testPhotoCanBeUploaded()
    {
        $this->visit('/upload')
             ->name('File Name', 'name')
             ->attach($absolutePathToFile, 'photo')
             ->press('Upload')
             ->see('Upload Successful!');
    }

<a name="testing-json-apis"></a>
### Testando APIs em JSON

O Laravel também conta com diversos helpers para testar APIs em JSON e suas respostas. Por exemplo os métodos `get`, `post`, `put`, `patch` e `delete` podem ser usados para criar vários tipos de requisições HTTP. Você pode facilmente enviar dados e cabeçalhos para estes métodos. Para começar vamos escrever um teste para fazer uma requisição `POST` em `/user` e verificar se o array foi retornado no formato JSON:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->post('/user', ['name' => 'Sally'])
                 ->seeJson([
                     'created' => true,
                 ]);
        }
    }

O método `seeJson` converte o array fornecido em JSON e então verifica se ele está em **qualquer** parte do JSON retornado pela aplicação. Então caso a resposta possua outras propriedades no JSON de resposta, os testes passarão sem problemas enquanto esse fragmento do JSON for fornecido.

#### Verificar um JSON exato

Se você deseja verificar se o array fornecido é **exatamente** igual ao JSON retornado pela aplicação, você precisará usar o método `seeJsonEquals`:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->post('/user', ['name' => 'Sally'])
                 ->seeJsonEquals([
                     'created' => true,
                 ]);
        }
    }

<a name="sessions-and-authentication"></a>
### Sessão / Autênticação

O Laravel conta com diversos helpers para trabalhar com a sessão durante os testes. Primeiro você precisa determinar os dados da sessão usando o método `withSession`. Ele é muito útil para carregar dados na sessão antes de testar uma requisição na sua aplicação.

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $this->withSession(['foo' => 'bar'])
                 ->visit('/');
        }
    }

Uma das utilizações mais comuns da sessão é para armazenar a informação do usuário, como se ele está autênticado. O helper `actingAs` provê uma maneira simples para autênticar um determinado usuário. Por exemplo, você pode utilizar uma [fábrica de model](#model-factories) para gerar e autênticar um usuário:

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $user = factory('App\User')->create();

            $this->actingAs($user)
                 ->withSession(['foo' => 'bar'])
                 ->visit('/')
                 ->see('Hello, '.$user->name);
        }
    }

<a name="disabling-middleware"></a>
### Desativando Middleware

Durante os testes você pode desejar desativar qualquer [middleware](/docs/{{version}}/middleware) para alguns testes. Isso permite que você teste as rotas e controllers isoladamente de qualquer middleware. O Laravel incluí uma trait chamada `WithoutMiddleware` que você pode usar para desativar automaticamente todos os middlewares para a classe de testes:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use WithoutMiddleware;

        //
    }

Se você desejar desativar os middlewares apenas para alguns métodos você pode chamar `withoutMiddleware` dentro do método de teste:

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->withoutMiddleware();

            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="custom-http-requests"></a>
### Requisições HTTP Customizadas

Se você deseja fazer uma requisição HTTP customizada na sua aplicação e receber um objeto `Illuminate\Http\Response` você pode utilizar o método `call`:

    public function testApplication()
    {
        $response = $this->call('GET', '/');

        $this->assertEquals(200, $response->status());
    }

Se você está fazendo uma requisição como `POST`, `PUT` ou `PATCH` você pode informar um array com os dados para esta requisição. Estes dados estarão disponíveis nas rotas e controllers através do [instancia da Requisição](/docs/{{version}}/requests):

       $response = $this->call('POST', '/user', ['name' => 'Taylor']);

<a name="working-with-databases"></a>
## Trabalhando com Banco de Dados

O Laravel também possuí uma variedade de ferramentás úteis para facilitar os testes da aplicação com banco de dados. Primeiramente você pode usar o médoto `seeInDatabase` que verificará se os dados informados existem na base de dados de acordo com seus critérios. Por exemplo, se você deseja verificar se um determinado usuário existe na tabela `users` com o valor do campo `email` igual a `sally@example.com` você pode fazer o seguinte:

    public function testDatabase()
    {
        // Make call to application...

        $this->seeInDatabase('users', ['email' => 'sally@foo.com']);
    }

Claro que o método `seeInDatabase` e outros métodos helpers como este existem por conveniêncie. Você é livre para utilizar qualquer método de verificação do PHPUnit para suprir a necessidade dos testes.

<a name="resetting-the-database-after-each-test"></a>
### Resetando o Banco de Dados após cada teste

Isso é útil quando você acha que é necessário resetar (limpar) a base de dados após cada teste para não atrapalhar outros testes.

#### Usando Migrations

Uma opção é fazer um rollback no banco de dados após cada teste e migrar novamente para o próximo teste. O Laravel conta com uma simples trait chamada `DatabaseMigrations` que automaticamente faz isso para você. Simplesmente use a trait na sua classe de teste:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseMigrations;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

#### Usando Transactions

Outra opção é agrupar cada teste em uma transação para a base de dados. Novamente o Laravel provê uma trait chamada `DatabaseTransactions` que fará isso automaticamente:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseTransactions;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="model-factories"></a>
### Model Factories

Durante os testes uma coisa comum é inserir alguns registros na base de dados antes de executar seu teste. Ao invés de manualmente especificar o valor de cada coluna para criar estes dados de teste, o Laravel permite que você defina alguns valores padrão para cada [Eloquent models](/docs/{{version}}/eloquent) usando "factories". Para começar vamos dar uma olhada no arquivo `database/factories/ModelFactory.php`. Este arquivo contém uma única definição de factory:

    $factory->define(App\User::class, function (Faker\Generator $faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => bcrypt(str_random(10)),
            'remember_token' => str_random(10),
        ];
    });

Com a Closure servindo de definição para a factory, você pode retornar os valores padrão para cada atributo no model. A Closure irá receber uma instância da library [Faker](https://github.com/fzaninotto/Faker) que permite você gerar diversos valores randômicos para testar.

Lembrando que você é livre para adicionar seus próprios factories ao arquivo `ModelFactory.php`.

#### Multiplos tipos de Factory

Em algum momento você pode desejar múltiplos factories para o mesmo model. Por exemplo, talvez você queira uma factory para usuários "Administradores" ao invés de usuários comuns. Você pode definir estas factories usando o método `defineAs`:

    $factory->defineAs(App\User::class, 'admin', function ($faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => str_random(10),
            'remember_token' => str_random(10),
            'admin' => true,
        ];
    });

Ao invés de duplicar todos os atributos do seu usuário normal, você pode utilizar o médoto `raw` para pré-preencher os atributos comuns, após preenchidos estes atributos simplesmente complete com os valores adicionais que você precisa:

    $factory->defineAs(App\User::class, 'admin', function ($faker) use ($factory) {
        $user = $factory->raw(App\User::class);

        return array_merge($user, ['admin' => true]);
    });

#### Usando Factories Nos Tests

Uma vez que foram definidos suas factories, você pode utiliza-las em seus testes ou seeds da base de dados para gerar instâncias do model usando a função `factory`. Bom, vamos dar uma olhada em alguns exemplos de criação de models. Primeiramente vamos utilizar o médoto `make` que cria os models mas não os salva na base de dados:

    public function testDatabase()
    {
        $user = factory(App\User::class)->make();

        // Use model in tests...
    }

Se você desejar sobrescrever algum valor padrão do seu model, você precisa passar um array para o método `make`. Somente os valores informados serão substituídos os demais valores permanecerão intactos como definidos por padrão na factory:

    $user = factory(App\User::class)->make([
        'name' => 'Abigail',
       ]);

Você também pode criar uma Collection de vários models ou criar models de um determinado tipo:

    // Create three App\User instances...
    $users = factory(App\User::class, 3)->make();

    // Create an App\User "admin" instance...
    $user = factory(App\User::class, 'admin')->make();

    // Create three App\User "admin" instances...
    $users = factory(App\User::class, 'admin', 3)->make();

#### Persistindo Factory Models

O método `create` não cria somente instância do model, mas também salva eles na base de dados usando o método `save` do Eloquent:

    public function testDatabase()
    {
        $user = factory(App\User::class)->create();

        // Use model in tests...
    }

Novamente você pode sobrescrever os atributos do model passando um array para o médoto `create`:

    $user = factory(App\User::class)->create([
        'name' => 'Abigail',
       ]);

#### Adicionando Relações Aos Models

Talvez você deseje persistir diversos models na base de dados. Neste exemplo nós iremos anexar uma relação aos models criados. Quando usamos o método `create` para criar multiplos models uma [collection instance](/docs/{{version}}/eloquent-collections) é retornada permitindo que você use as funções pertencentas a coleção como `each`:

    $users = factory(App\User::class, 3)
               ->create()
               ->each(function($u) {
                    $u->posts()->save(factory(App\Post::class)->make());
                });

<a name="mocking"></a>
## Mocking

<a name="mocking-events"></a>
### Mocking Events

Se você está fazendo muito uso do sistema de evento do Laravel você pode desejar silenciar ou "falsificar" alguns eventos durante os testes. Por exemplo, se você está testando o cadastro de usuário você provavelmente não quer que todo os eventos de `UserRegistered` sejam acionados, como envio de emails, etc.

O Laravel contém um médoto chamado `expectsEvents` que verifica o acionamento do evento, mas impede qualquer execução deste evento durante os testes:

    <?php

    class ExampleTest extends TestCase
    {
        public function testUserRegistration()
        {
            $this->expectsEvents(App\Events\UserRegistered::class);

            // Test user registration code...
        }
    }

Se você deseja impedir todos os eventos de executarem você pode utilizar o médodo `wihoutEvents`:

    <?php

    class ExampleTest extends TestCase
    {
        public function testUserRegistration()
        {
            $this->withoutEvents();

            // Test user registration code...
        }
    }

<a name="mocking-jobs"></a>
### Mocking Jobs

Algumas vezes você precisa em um simples teste verificar se um job foi executado pelos seus controller durante uma requisição da aplicação. Isso permite que você teste suas rotas / controllers isoladamente - separadamente da lógica do job. Claro que você pode testa-lo em uma classe de teste separada.

O Laravel contém um método chamado `expectsJobs` que irá verificar se aquele determinado job foi executado mas o job em si não será executado:

    <?php

    class ExampleTest extends TestCase
    {
        public function testPurchasePodcast()
        {
            $this->expectsJobs(App\Jobs\PurchasePodcast::class);

            // Test purchase podcast code...
        }
    }

> **Nota:** Este método somente detecta jobs que foram executados através dos métodos da trait `DispatchesJobs`. Ele não detecta jobs executados diretamente para `Queue::push`.

<a name="mocking-facades"></a>
### Mocking Facades

Durante os testes você pode querer "falsificar" uma chamada para um 
[facade](/docs/{{version}}/facades). Por exemplo, considerando o método do controller a seguir:

    <?php

    namespace App\Http\Controllers;

    use Cache;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * Show a list of all users of the application.
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

Nós podemos enganar a chamada para a facade `Cache` usando o método `shouldReceive` que irá retornar uma instância da classe [Mockery](https://github.com/padraic/mockery). Como as facades são atualmente resolvidas e gerenciadas pelo Laravel [service container](/docs/{{version}}/container) elas possuem muito mais testabilidade do que classes estáticas comuns. Por exemplo, vamos enganar uma chamada para a facade `Cache`:

    <?php

    class FooTest extends TestCase
    {
        public function testGetIndex()
        {
            Cache::shouldReceive('get')
                        ->once()
                        ->with('key')
                        ->andReturn('value');

            $this->visit('/users')->see('value');
        }
    }

> **Nota:** Você não deve enganar a facade `Request`. Ao invés, pode passar o que você deseja através dos helpers como `call` e `post` durante os testes.
