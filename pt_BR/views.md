# Views

- [Uso Básico](#basic-usage)
    - [Passando Dados Para as Views](#passing-data-to-views)
    - [Compartilhando Dados Com Todas As Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)

<a name="basic-usage"></a>
## Uso Básico

Views contém o HTML fornecido pela sua aplicação e separa a lógica do seu Controller / aplicação da lógica de apresentação. Views são armazenadas na pasta `resources/views` .

Uma simples view pode ser algo assim:

    <!-- View armazenada em resources/views/greeting.php -->

    <html>
        <body>
            <h1>Hello, <?php echo $name; ?></h1>
        </body>
    </html>

Uma vez que esta view está armazenada em `resources/views/greeting.php`, nós podemos retorna-la usando a função helper global `view` :

    Route::get('/', function ()    {
        return view('greeting', ['name' => 'James']);
    });

Como você pode ver, o primeiro argumento passado para o helper `view` corresponde ao nome do arquivo da view no diretório `resources/views`. O segundo argumento passado para o helper é um array de dados que devem ser disponibilizados para a view. Neste caso, nós estamos passando a variável `name`, que é exibida na view executando simplesmente `echo` na variável.

Claro, views também podem ser encadeadas dentro de sub-diretórios de `resources/views`. A notação "Ponto" pode ser usada para fazer referência em views encadeadas. Por exemplo, se sua view está armazenada em `resources/views/admin/profile` , você pode fazer a referência assim:

    return view('admin.profile', $data);

#### Determinando Se Uma View Existe

Se você precisa determinar se uma view existe, você pode usar o método `exists` depois de chamar o helper `view` sem nenhum argumento. Este método irá retornar `true` se a view existir no disco.

    if (view()->exists('emails.customer')) {
        //
    }

Quando o helper `view` é chamado sem argumentos, uma instância de `Illuminate\Contracts\View\Factory` é retornada, dando a você o acesso à qualquer método da factory.

<a name="view-data"></a>
### Dados Da View

<a name="passing-data-to-views"></a>
#### Passando Dados Para Views

Como você viu nos exemplos anteriores, você pode facilmente passar um array de dados para as views:

    return view('greetings', ['name' => 'Victoria']);

Quando passamos informações desta maneira, `$data` deveria ser um array com pares de chave/valor. Dentro da sua view, você pode então acessar cada valor usando sua chave correspondente, tal como `<?php echo $chave; ?>` . Como uma alternativa para passar um array completo de dados para a funcão helper `view`, você pode usar o método `with` para adicionar pedaços individuais de dados para a view:

    $view = view('greeting')->with('name', 'Victoria');

<a name="sharing-data-with-all-views"></a>
#### Compartilhando Dados Com Todas As Views

Ocasionalmente, você pode precisar compartilhar pedaços de dados com todas as views que são renderizadas pela sua aplicação. Você pode fazer isso usando o método `share` da factory. Tipicamente, você colocaria as chamadas para `share` dentro do método `boot` do service provider. Você está livre para adiciona-los ao `AppServiceProvider` ou gerar um service provider para abrigá-los.

    <?php

    namespace App\Providers;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Inicialização de qualquer serviço da aplicação.
         *
         * @return void
         */
        public function boot()
        {
            view()->share('key', 'value');
        }

        /**
         * Registra o service provider.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

<a name="view-composers"></a>
## View Composers

View composers são callbacks ou métodos de classes que são chamados quando uma view é rendezirada. Se você tem dados que deseja ficar vinculado com a view cada vez que essa view é renderizada, um view composer pode lhe ajudar a organizar essa lógica em um só local.

Vamos registrar nossos views composers dentro de um [service provider](/docs/{{version}}/providers). Nós vamos usar o helper `view` para acessar a implementação do contrato `Illuminate\Contracts\View\Factory` subjacente. Lembre-se, o Laravel não inclui um diretório padrão para os view composers. Você está livre para organiza-los de qualquer jeito que deseja. Por exemplo, você poderia criar um diretório `App\Http\ViewComposers`:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;

    class ComposerServiceProvider extends ServiceProvider
    {
        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function boot()
        {
            // Using class based composers...
            view()->composer(
                'profile', 'App\Http\ViewComposers\ProfileComposer'
            );

            // Using Closure based composers...
            view()->composer('dashboard', function ($view) {

            });
        }

        /**
         * Register the service provider.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

Lembre-se, se você criar um novo service provider para conter os registros do seu view composer, você vai precisar adicionar o service provider no array `providers` no arquivo de configuração `config/app.php`.

Agora que nós registramos o composer, o método `ProfileComposer@compose` vai ser executado cada vez que a view `profile` é renderizada. Então, vamos definir a classe composer:

    <?php

    namespace App\Http\ViewComposers;

    use Illuminate\Contracts\View\View;
    use Illuminate\Users\Repository as UserRepository;

    class ProfileComposer
    {
        /**
         * Implementação do repositório user.
         *
         * @var UserRepository
         */
        protected $users;

        /**
         * Cria um novo profile composer.
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            // Dependências resolvidas automaticamente pelo service container...
            $this->users = $users;
        }

        /**
         * Vincula dados a view.
         *
         * @param  View  $view
         * @return void
         */
        public function compose(View $view)
        {
            $view->with('count', $this->users->count());
        }
    }

Pouco antes da view ser renderizada, o método `compose` de composer é chamado com a instância `Illuminate\Contracts\View\View`. Você pode usar o método `with` para vincular dados para a view.

> **Nota:** Todos os view composers são resolvidor via [service container](/docs/{{version}}/container), então você pode usar "type-hint" de qualquer dependência que você precisar dentro do construtor de um composer.

#### Anexando Um Composer Para Multiplas Views

Você pode anexar um view composer a multiplas views imediatamente, passando um array de views como o primeiro argumento do método `composer`:

    view()->composer(
        ['profile', 'dashboard'],
        'App\Http\ViewComposers\MyViewComposer'
    );

O método `composer` aceita o caractere `*` como carta curinga, permitindo a você anexar um composer para todas as views:

    view()->composer('*', function ($view) {
        //
    });

### View Creators

View **creators** são muitos similares aos view composers; entretanto, eles são disparatos imediatamente quando a view é instanciada em vez de esperar que a view esteja prestes a renderizar. Para registrar um view creator, user o método `creator`:

    view()->creator('profile', 'App\Http\ViewCreators\ProfileCreator');
