# Autenticação

- [Introdução](#introduction)
- [Autenticação rápida](#authentication-quickstart)
     - [Rotas](#included-routing)
     - [Views](#included-views)
     - [Autenticação](#included-authenticating)
     - [Recuperando o Usuário Autenticado](#retrieving-the-authenticated-user)
     - [Protegendo as Rotas](#protecting-routes)
- [Autenticando Usuários Manualmente](#authenticating-users)
     - [Lembrando Usuários](#remembering-users)
     - [Outros Métodos de Autenticação](#other-authentication-methods)
- [Autenticação Básica HTTP](#http-basic-authentication)
     - [Autenticação Básica HTTP Stateless](#stateless-http-basic-authentication)
- [Resetando Senhas](#resetting-passwords)
     - [Considerações de Banco de Dados](#resetting-database)
     - [Rotas](#resetting-routing)
     - [Views](#resetting-views)
     - [Após Resetar a Senha](#after-resetting-passwords)
- [Autenticação Social](#social-authentication)
- [Adicionando Drivers de Auteticação Personalizado](#adding-custom-authentication-drivers)

<a name="introduction"></a>
## Introdução

Laravel faz implementação de autenticação de forma muito simples. De fato, quase tudo é configurado automagicamente para você. O arquivo onde é setado as configurações está em `config/auth.php`, onde contém várias opções bem documentadas para melhorar o comportamento dos serviços de autenticação.

### Considerações de Banco de Dados

Por padrão, o Laravel inclui um `App\User` [Eloquent model](/docs/{{version}}/eloquent) no seu diretório `app`. Esse modelo deve ser usado com o driver padrão de autenticação Eloquent. Se sua aplicação não está usando Eloquent, você deve usar o  driver de autenticação `database` que usa o Laravel query builder.

Quando estiver construindo o esquema de banco de dados para o model `App\User`, certifique-se que a coluna password têm pelo menos 60 caracteres no tamanho.

Também, você deve verificar que sua tabela de `users` (ou equivalente) contém um nullable, string `remember_token` coluna de 100 caracteres. Essa coluna será usada para guardar um token para sessões de "Lembrar meus dados" que serão mantidas por sua aplicação. Isso pode ser feito usando `$table->rememberToken();` na migration.

<a name="authentication-quickstart"></a>
## Autenticação rápida

Laravel é fornecido com dois controllers de autenticação já configurados, que estão localizados no namespace `App\Http\Controllers\Auth`. O `AuthController` que lida com registro e autenticação de um novo usuário, enquanto o `PasswordController` contém a lógica para ajudar usuários existentes para resetar as senhas que foram esquecidas. Esses controllers usam uma trait para incluir seus métodos necessários. Para a maioria das aplicações, você não precisará modificar esses controllers.

<a name="included-routing"></a>
### Rotas

Por padrão, nas [rotas](/docs/{{version}}/routing) estão inclusos os pontos de acesso para os controllers de autenticação. Você deve manualmente adicioná-los no seu arquivo `app/Http/routes.php`:

    // Authentication routes...
    Route::get('auth/login', 'Auth\AuthController@getLogin');
    Route::post('auth/login', 'Auth\AuthController@postLogin');
    Route::get('auth/logout', 'Auth\AuthController@getLogout');

    // Registration routes...
    Route::get('auth/register', 'Auth\AuthController@getRegister');
    Route::post('auth/register', 'Auth\AuthController@postRegister');

<a name="included-views"></a>
### Views

Embora os controllers de autenticação estarem inclusos com o framework, você precisará prover  as [views](/docs/{{version}}/views) para serem renderizadas. As views devem estar no diretório `resources/views/auth`. Você é livre para modificar essas views sempre que desejar. A view para login deverá estar em `resources/views/auth/login.blade.php` e a de cadastro em `resources/views/auth/register.blade.php`.

#### Formulário Simples de Login

    <!-- resources/views/auth/login.blade.php -->

    <form method="POST" action="/auth/login">
        {!! csrf_field() !!}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password" id="password">
        </div>

        <div>
            <input type="checkbox" name="remember"> Remember Me
        </div>

        <div>
            <button type="submit">Login</button>
        </div>
    </form>

#### Formulário Simples de Cadastro

    <!-- resources/views/auth/register.blade.php -->

    <form method="POST" action="/auth/register">
        {!! csrf_field() !!}

        <div class="col-md-6">
            Name
            <input type="text" name="name" value="{{ old('name') }}">
        </div>

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div class="col-md-6">
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">Register</button>
        </div>
    </form>

<a name="included-authenticating"></a>
### Autenticação

Agora que você tem rotas e views configuradas para o controller de autenticação incluído, vocẽ está pronto para cadastrar e autenticar novos usuários para sua aplicação. Você pode simplesmente acessar suas rotas definidas no navegador.

Quando um usuário for autenticado, ele será redirecionado para a URI `/home`. Você pode customizar o local de redirecionamento definindo a propriedade `redirectTo` no `AuthController`:

     protected $redirectTo = '/dashboard';

#### Customizações

Para modificar os campos do formulários que são necessários para o cadastro de usuário, ou para modificar como os registros de novos usuários são inseridos em sua base de dados, você pode modificar a classe `AuthController`. Essa classe é responsável por validar e criar novos usuários para sua aplicação.

O método `validator` do `AuthController` contém as regras de validação para novos usuários. Você é livre para modificar essse método da forma que desejar.

O método `create` do `AuthController` é responsável por criar um novo registro de `App\User` em sua base de dados usando o [Eloquent ORM](/docs/{{version}}/eloquent). Você é livre para modificar esse método de acordo com suas necessidades.

<a name="retrieving-the-authenticated-user"></a>
### Recuperando o usuário autenticado

Você pode acessar o usuário autenticado pelo facade `Auth`:

     $user = Auth::user();

Alternativamente, uma vez que seu usuário estiver autenticado, você pode acessá-lo usando uma instância do `Illuminate\Http\Request`:

    <?php namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class ProfileController extends Controller
    {
        /**
         * Update the user's profile.
         *
         * @param  Request  $request
         * @return Response
         */
        public function updateProfile(Request $request)
        {
            if ($request->user()) {
                // $request->user() returns an instance of the authenticated user...
            }
        }
    }

#### Verificando se o usuário atual está autenticado

Para verificar se o usuário já está logado em sua aplicação, você pode usar o método `check` no facade `Auth`, onde será retornado `true` se o usuário estiver autenticado:

     if (Auth::check()) {
          // O usuário está logado...
     }

No entando, vocẽ deve usar um middleware para verificaar se o usuário está autenticado antes de liberar o acesso a certas rotas/controllers. Para aprender mais sobre isso, veja a documentação em [protecting routes](/docs/{{version}}/authentication#protecting-routes).

<a name="protecting-routes"></a>
### Protegendo as Rotas

[Rotas intermediárias(Route Middleware)](/docs/{{version}}/middleware) podem ser usadas para habilitar acesso a rota somente para usuários autenticados. Laravel já vem com o middleware `auth`, que está definido em `app\Http\Middleware\Authenticate.php`. Tudo o que você precisará é setar o middleware na definição da rota:

    // Usando uma Função Anônima...

    Route::get('profile', ['middleware' => 'auth', function() {
        // Somente usuários autenticados entram aqui...
    }]);

    // Usando um Controller...

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'ProfileController@show'
    ]);

É claro que, se você estiver usando [controles de acesso](/docs/{{version}}/controllers), deverá ser usado o método `middleware` no construtor do controller ao invés de setar na rota diretamente:

    public function __construct()
    {
        $this->middleware('auth');
    }

<a name="authenticating-users"></a>
## Autenticando Usuários Manualmente

Como você já sabe, você não é obrigado a usar os controllers que estão incluidos no Laravel. Se você optar por remover esses controllers, será necessário gerenciar a autenticação de usuário usando as classes de autenticação do Laravel diretamente. Não se preocupe, é fácil!

Nós acessamos os serviçs de autenticação do Laravel pelo [facade](/docs/{{version}}/facades) `Auth`, então teremos que importá-lo no topo da class. Em seguida, verificamos com o método `attempt`:

    <?php namespace App\Http\Controllers;

    use Auth;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Handle an authentication attempt.
         *
         * @return Response
         */
        public function authenticate()
        {
            if (Auth::attempt(['email' => $email, 'password' => $password])) {
                // Authentication passed...
                return redirect()->intended('dashboard');
            }
        }
    }

O método `attempt` aceita um array de chave/valor no primeiro parâmetro. Os valores no array serão usados para procurar o usuário na sua tabela do banco de dados. Então, no exemplo acima, o usuário será procurado pelo valor da columa `email`. Se o usuário for encontrado, o valor da senha no banco de dados será comparado com o `password` passado pelo método no array. Se tudo correr bem, uma sessão será iniciada para esse usuário.

O método `attempt` irá retornar `true` se a autenticação for feita. Em outro caso, `false` será retornado.

O método `intended` levará o usuário de volta a URL que estava acessando antes do filtro de autenticação ser acionado. Uma URI de retorno pode ser dada a este método no caso de o destino pretendido não estiver disponível.

Se você desejar, também pode ser adicionado condições extras para a consulta além do email e senha do usuário. Por exemplo, você pode verificar se o usuário está marcado como "active(ativo)":

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        // O usuário existe e está ativo.
    }

Para deslogar os usuários de sua aplicação, vocẽ deve usaar o método `logout` no facade `Auth`. Isso vai limpar as informações de autenticação na sessão do usuário.

     Auth::logout();

> **Nota:** Nesses exemplos, `email` não é uma opção obrigatório, é meramente usado como um exemplo. Você deve usar qualquer coluna que corresponda a um "username(nome de usuário)" em seu banco de dados.

<a name="remembering-users"></a>
## Lembrando Usuários

Se você quiser prover uma funcionalidade de "Lembrar meus dados" na sua aplicação, você pode passar um valor boleano como segundo argumento no método `attempt`, onde você mantém o usuário autenticado indefinitivamente, or até o logout ser feito manualmente. É claro, sua tabela de `users` deve incluir uma coluna `remember_token` como string, que será usada para guardar o token.

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // The user is being remembered...
    }

Se você está "lembrando" usuários, pode usar o método `viaRemember` para determinar se o usuário foi autenticado usando o cookie "lembrar meus dados":

    if (Auth::viaRemember()) {
        //
    }

<a name="other-authentication-methods"></a>
### Outros Métodos de Autenticação

#### Uma instância do usuário autenticado

Se você precisar logar um usuário existente em sua aplicação, você pode chamar o método `login` com a instância user. O objeto deve ser uma implementação do `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/{{version}}/contracts). Lembrando que o model `App\User` incluido com o Laravel já implementa essa interface:

     Auth::login($user);

#### Usuário autenticado por ID

Para logar um usuário na aplicação pelo IR, você pode usar o método `loginUsingID`. Esse método simplesmente aceita a chave primária do usuário que você deseja autenticar:

     Auth::loginUsingId(1);

#### Usuario autenticado uma vez

Você pode usar o método `once` para logar um usuário na aplicação com uma única requisição. Sessões e cookies não serão utilizados. Isso pode ser bastante útil quando estiver sendo construído uma API stateless. O método `once` tem a mesma assinatura que o `attempt`:

    if (Auth::once($credentials)) {
        //
    }

<a name="http-basic-authentication"></a>
## Autenticação Básica HTTP

[Autenticação Básica HTTP](http://en.wikipedia.org/wiki/Basic_access_authentication) provê uma maneira rápida de autenticar usuários na sua aplicação sem configurar uma página dedicada de "login". Para começar, adicione o [middleware](/docs/{{version}}/middleware) `auth.basic` na sua rota:

     Route::get('profile', ['middleware' => 'auth.basic', function() {
        // Somente usuários autenticados devem entrar...
    }]);

Uma vez que o middleware estiver setado, você será automaticamente solicitado a fornecer credenciais ao acessar a rota no navegador. Por padrão, o middleware `auth.basic` vai usar a coluna `email` no registro do usuário como "username"

#### Um recado sobre FastCGI

Se você está usando PHP FastCGI, a autenticação básica HTTP pode não funcionar corretamente. As seguintes linhas devem ser adicionadas no seu arquivo `.htaccess`:

    RewriteCond %{HTTP:Authorization} ^(.+)$
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="stateless-http-basic-authentication"></a>
### Autenticação Básica HTTP Stateless

Você também pode usar a autenticação básica HTTP sem configurar um cookie identificador de usuário na sessão, o que é particularmente útil para autenticação em API. Para fazer isso, [defina um middleware](/docs/{{version}}/middleware) que chame o método `onceBasic`, a requisição pode ser transmitida na aplicação:

    <?php namespace Illuminate\Auth\Middleware;

    use Auth;
    use Closure;
    use Illuminate\Contracts\Routing\Middleware;

    class AuthenticateOnceWithBasicAuth implements Middleware
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return Auth::onceBasic() ?: $next($request);
        }

    }

Em seguida, [registre outro middleware](/docs/{{version}}/middleware#registering-middleware) e registre na rota:

    Route::get('api/user', ['middleware' => 'auth.basic.once', function() {
        // Only authenticated users may enter...
    }]);

<a name="resetting-passwords"></a>
## Resetando Senhas

<a name="resetting-database"></a>
### Considerações de Banco de Dados

A maioria das aplicações web fornecem formas do usuário resetar sua senha. Ao invés de forçá-lo a ré-implementar essa funcionalidade em cada aplicação, o laravel provê métodos convenientes para enviar lembretes e redefinição de senha.

Para iniciar, verifique se seu model `App\User` implementa o contract `Illuminate\Contracts\Auth\CanResetPassword`. É claro que o model `App\User` que vem com o Laravel já implementa essa interface, e usa a trait `Illuminate\Auth\Passwords\CanResetPassword` para incluir os métodos necessários para implementar a interface.

#### Gerando o Token de Reset na Tabela Migration

Em seguida, a tabela deve ser criada para guardar os tokens de reset de senhas. A migration para essa tabela já vem incluída no Laravel, e se encontra na pasta `database/migrations`. Então você precisa executar esse comando no terminal:

    php artisan migrate

<a name="resetting-routing"></a>
### Rotas

Laravel inclui um `Auth\PasswordController` que contém a lógica necessária para reser as senhas. No entanto, você terá que definir rotas para apontar as requisições para este controller:

    // Rotas para solicitar trocar de senha...
    Route::get('password/email', 'PasswordController@getEmail');
    Route::post('password/email', 'PasswordController@postEmail');

    // Rotas para trocar a senha...
    Route::get('password/reset/{token}', 'PasswordController@getReset');
    Route::post('password/reset', 'PasswordController@postReset');

<a name="resetting-views"></a>
### Views

Definindo as rotas para o `PasswordController`, você terá que provê views que devem ser retornadas do controller. Não se preocupe, nós já temos algumas views de exemplo que te ajudarão a iniciar. Você é livre para estilizar os formulários da forma que desejar.

#### Exemplo de Formulário para Solicitar Troca de Senha

Você precisa fornecer uma view em HTML para o formulário de troca de senha. Essa view deve ser salva em `resources/views/auth/password.blade.php`. Esse formulário tem um único campo para o usuário digitar seu email:

    <!-- resources/views/auth/password.blade.php -->

    <form method="POST" action="/password/email">
        {!! csrf_field() !!}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <button type="submit">
                Send Password Reset Link
            </button>
        </div>
    </form>

Quando um usuário envia a requisição para trocar de senha, ele receberá um e-mail com um link que aponta para o método `getReset` (rota `/password/reset`) no controller `PasswordController`. Você precisa criar uma view para o email em: `resources/views/emails/password/blade.php`. Essa view receberá a variável `$token` que contem o token que será comparado com o enviado por email. Aqui está um exemplo da view para você entender:

    <!-- resources/views/emails/password.blade.php -->

    Click here to reset your password: {{ url('password/reset/'.$token) }}

#### Exemplo de Formulário para Trocar a Senha

Quando o usuário clickar no link enviado por email, ele será enviado para um formulário para cadastrar uma nova senha. Esse formulário deverá ser salvo em `resources/views/auth/reset.blade.php`.

Aqui está um simples formulário para troca de senha:

    <!-- resources/views/auth/reset.blade.php -->

    <form method="POST" action="/password/reset">
        {!! csrf_field() !!}
        <input type="hidden" name="token" value="{{ $token }}">

        <div>
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <input type="password" name="password">
        </div>

        <div>
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">
                Reset Password
            </button>
        </div>
    </form>

<a name="after-resetting-passwords"></a>
### Após Resetar a Senha

Uma vez que estiver definido as rotas e formulários para trocar a senha do usuário, você precisa simplesmente acessar essas rotas no seu navegador. O `PasswordController` incluído com o Laravel já inclui a lógica para enviar o email com link para reset e também atualização da senha no banco de dados.

Após a senha estiver resetada, o usuário deverá estar logado na aplicação e redirecionado para o `/home`. Você pode editar essa página que está definida na pripriedade `redirectTo` no `PasswordController`:

    protected $redirectTo = '/dashboard';

> **Nota:** Por padrão, o token enviado por email expira depois de uma hora. Você pode mudar isso na opção `reminder.expire` no arquivo `config/auth.php`.

<a name="social-authentication"></a>
## Autenticação Social

Além disso, o Laravel também fornece uma forma simples e conveninente de autenticaçao com providers OAuth usando [Laravel Socialite](https://github.com/laravel/socialite). Socialite atualmente suporta autenticação com Facebook, Twitter, Google, GitHub e Bitbucket.

Para iniciar com Socialite, adicione essa dependência no seu arquivo `composer.json`:

    composer require laravel/socialite

### Configuração

Após instalar a biblioteca, registre o `Laravel\Socialite\SocialiteServiceProvider` no seu arquivo de configuração `config/app.php`:

    'providers' => [
        // Other service providers...

        'Laravel\Socialite\SocialiteServiceProvider',
    ],

Também adicione o facade `Socialite` ao array de `aliases` no mesmo arquivo:

    'Socialite' => 'Laravel\Socialite\Facades\Socialite',

Você também precisa adicionar as credenciais de acesso para os serviços de OAuth utilizado na sua aplicação. Essas credenciais devem ficar no arquivo `config/services.php`, e deve ser usado a chave `facebook`, `twitter`, `google`, or `github`, dependendo da sua necessidade. Por exemplo:

    'github' => [
        'client_id' => 'your-github-app-id',
        'client_secret' => 'your-github-app-secret',
        'redirect' => 'http://your-callback-url',
    ],

### Uso Básico

Em seguida, você precisará de duas rotas: uma para redirecionar o usuário ao provider selecionado, e outra para receber o retorno depois da autenticação. Nós vamos acessar o Socialite usando o [facade](/docs/{{version}}/facades) `Socialite`:

    <?php namespace App\Http\Controllers;

    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Redirect the user to the GitHub authentication page.
         *
         * @return Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * Obtain the user information from GitHub.
         *
         * @return Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

O método `redirect` cuida de enviar o usuário para provider selecionado, enquanto o `user` irá receber a solicitação e recuperar as informações do usuário. Antes de redirecionar o usuário, você pode também setar os "escopos" na requisição usando o método `scope`. Esse método vai sobrescrever todos os escopos existentes:

    return Socialite::driver('github')
                ->scopes(['scope1', 'scope2'])->redirect();

#### Recuperando as Informações do Usuário

Uma vez que estiver o usuário instanciado, você pode pegar mais detalhes sobre o usuário:

    $user = Socialite::driver('github')->user();

    // OAuth Two Providers
    $token = $user->token;

    // OAuth One Providers
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All Providers
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

<a name="adding-custom-authentication-drivers"></a>
## Adicionando Drivers de Auteticação Personalizado

Se você não estiver usando o tradicional banco de dados relacional para gravar seus usuários, você pode precisar extender o Laravel com seu próprio driver. Nós usaremos o método `extend` no facade `Auth` para definir um driver personalizado. Você pode fazer essa chamada ao `extend` com um [service provider](/docs/{{version}}/providers):

    <?php namespace App\Providers;

    use Auth;
    use App\Extensions\RiakUserProvider;
    use Illuminate\Support\ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Auth::extend('riak', function($app) {
                // Return an instance of Illuminate\Contracts\Auth\UserProvider...
                return new RiakUserProvider($app['riak.connection']);
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

Após registar o driver, você pode configurar o seu driver no arquivo de configuração `config/auth.php`.

### O User Provider Contract

As implementações no `Illuminate\Contracts\Auth\UserProvider` são somente responsáveis por uma implementação de `Illuminate\Contracts\Auth\Authenticatable` fora de um sistema de armazenamento persistente, como MySQL, Riak, etc. Essas duas interfaces habilitam o mecanismo de autenticação do Laraval para continuar funcionando independente de como os dados do usuário serão salvos ou que tipo de classe é usada para representar.

Vamos dar uma olhada no contract `Illuminate\Contracts\Auth\UserProvider`:

    <?php namespace Illuminate\Contracts\Auth;

    interface UserProvider {

        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);

    }

A função `retrieveById` recebe tipicamente uma chave repesentando o usuário, como um campo auto-increment ID de um banco de dados MySQL. A implementação `Authenticatetable` combinando o ID deve ser recuperado e retornado pelo método.

A função `retrieveByToken` recupera um usário pelo seu `$identificador` único e "lembrar meus dados", salvo em um campo `remember_token`. Tal como acontece o método anterior,  a implementação `Authenticatable` deve ser retornada.

O método `updateRememberToken` atualiza o `$user` campo `remember_token` com o novo `$token`. O novo token pode ser atualizado, atribuido quando o "lembrar meus dados" for marcado no login, ou nulo quando o usuário deslogar.

O método `retrieveByCredentials` recebe um array de credenciais passado para o método `Auth::attempt` ao tentar logar na aplicação. O método deve "query" (consultar) o armazenamento persistente para o usuário com essas credenciais. Tipicamente, esse método vai rodar uma consulta com uma condição "where" em `$credentials['username']`. O método deve então retornar uma implementação de `UserInterface`. **Esse método não deve tentar fazer qualquer validação ou autenticação.**

O método `validateCredentials` deve comparar o `$user` com as `$credentials` para autenticar o usuário. Por exemplo, esse método pode comparar a string `$user->getAuthPassword()` para o `Hash::make` de `$credentials['password']. Esse método pode somente validar as credenciais do usuário e retornar boolean.

### O Authenticatable Contract

Agora que exploramos cada um dos métodos do `UserProvider`, vamos dar uma olhar no `Authenticatable`. Lembre-se, o provedor deve retornar implementações da interface dos métodos `retrieveById` e `retrieveByCredentials`:

    <?php namespace Illuminate\Contracts\Auth;

    interface Authenticatable {

        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();

    }

Essa interface é simples. O método `getAuthIdentifier` deve retornar o ID do usuário. no MySQL, novamente, isso seria a chave primária do usuário. O `getAuthPassword` retorna a senha do usuário. Essa interface habilita o sistema de autenticação para trabalhar com qualquer classe User, independentemente de ORM ou qualquer camada de abstração para banco de dados que você estiver usando. Por padrão, Laravel inclui uma classe `User` no diretório `app` que implementa essa interface, então você pode consultar para ter um exemplo de implementação.
