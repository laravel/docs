---
title: "Laravel Socialite"
---

- [Introdução](#introduction)
- [Instalação](#installation)
- [Atualizando o Socialite](#upgrading-socialite)
- [Configuração](#configuration)
- [Autenticação](#authentication)
    - [Roteamento](#routing)
    - [Autenticação e Armazenamento](#authentication-and-storage)
    - [Escopos de Acesso](#access-scopes)
    - [Escopos de Bot do Slack](#slack-bot-scopes)
    - [Parâmetros Opcionais](#optional-parameters)
- [Recuperando Detalhes do Usuário](#retrieving-user-details)
- [Testes](#testing)

<a id="introduction"></a>
## Introdução

Além da autenticação tradicional baseada em formulários, o Laravel também oferece uma maneira simples e conveniente de autenticar com provedores OAuth usando o [Laravel Socialite](https://github.com/laravel/socialite). Atualmente, o Socialite oferece suporte à autenticação via Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket e Slack.

> **Nota:**
> Adaptadores para outras plataformas estão disponíveis através do site [Socialite Providers](https://socialiteproviders.com/), mantido pela comunidade.

<a id="installation"></a>
## Instalação

Para começar com o Socialite, use o gerenciador de pacotes Composer para adicionar o pacote às dependências do seu projeto:

```shell
composer require laravel/socialite
```

<a id="upgrading-socialite"></a>
## Atualizando o Socialite

Ao atualizar para uma nova versão major do Socialite, é importante revisar cuidadosamente [o guia de atualização](https://github.com/laravel/socialite/blob/master/UPGRADE.md).

<a id="configuration"></a>
## Configuração

Antes de usar o Socialite, você precisará adicionar as credenciais dos provedores OAuth que sua aplicação utiliza. Normalmente, essas credenciais podem ser obtidas criando uma "developer application" no painel do serviço com o qual você fará a autenticação.

Essas credenciais devem ser colocadas no arquivo de configuração `config/services.php` da sua aplicação, usando a chave `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack` ou `slack-openid`, dependendo dos provedores que sua aplicação necessita:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> **Nota:**
> Se a opção `redirect` contiver um caminho relativo, ele será automaticamente resolvido para uma URL totalmente qualificada.

<a id="authentication"></a>
## Autenticação

<a id="routing"></a>
### Roteamento

Para autenticar usuários usando um provedor OAuth, você precisará de duas rotas: uma para redirecionar o usuário ao provedor OAuth e outra para receber o callback do provedor após a autenticação. As rotas de exemplo abaixo demonstram a implementação de ambas:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

O método `redirect` fornecido pela facade `Socialite` cuida de redirecionar o usuário ao provedor OAuth, enquanto o método `user` examinará a requisição recebida e recuperará as informações do usuário no provedor depois que ele tiver aprovado a solicitação de autenticação.

<a id="authentication-and-storage"></a>
### Autenticação e Armazenamento

Depois que o usuário for recuperado do provedor OAuth, você pode verificar se o usuário existe no banco de dados da sua aplicação e [autenticar o usuário](../authentication/#authenticate-a-user-instance). Se o usuário não existir no banco de dados da sua aplicação, normalmente você criará um novo registro no banco para representá-lo:

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::updateOrCreate([
        'github_id' => $githubUser->id,
    ], [
        'name' => $githubUser->name,
        'email' => $githubUser->email,
        'github_token' => $githubUser->token,
        'github_refresh_token' => $githubUser->refreshToken,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
});
```

> **Nota:**
> Para mais informações sobre quais informações de usuário estão disponíveis em provedores OAuth específicos, consulte a documentação sobre [recuperação de detalhes do usuário](#retrieving-user-details).

<a id="access-scopes"></a>
### Escopos de Acesso

Antes de redirecionar o usuário, você pode usar o método `scopes` para especificar os "escopos" que devem ser incluídos na requisição de autenticação. Este método mesclará todos os escopos especificados anteriormente com os escopos que você informar:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

Você pode sobrescrever todos os escopos existentes na requisição de autenticação usando o método `setScopes`:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a id="slack-bot-scopes"></a>
### Escopos de Bot do Slack

A API do Slack fornece [diferentes tipos de access tokens](https://api.slack.com/authentication/token-types), cada um com seu próprio conjunto de [escopos de permissão](https://api.slack.com/scopes). O Socialite é compatível com ambos os tipos de access token do Slack a seguir:

<div class="content-list" markdown="1">

- Bot (prefixado com `xoxb-`)
- Usuário (prefixado com `xoxp-`)

</div>

Por padrão, o driver `slack` gerará um token de `user`, e invocar o método `user` do driver retornará os detalhes do usuário.

Tokens de bot são úteis principalmente se sua aplicação enviar notificações para workspaces externos do Slack que pertençam aos usuários da sua aplicação. Para gerar um token de bot, invoque o método `asBotUser` antes de redirecionar o usuário ao Slack para autenticação:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

Além disso, você deve invocar o método `asBotUser` antes de invocar o método `user`, depois que o Slack redirecionar o usuário de volta para sua aplicação após a autenticação:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

Ao gerar um token de bot, o método `user` ainda retornará uma instância de `Laravel\Socialite\Two\User`; no entanto, apenas a propriedade `token` será preenchida. Esse token pode ser armazenado para [enviar notificações aos workspaces do Slack do usuário autenticado](../notifications/#notifying-external-slack-workspaces).

<a id="optional-parameters"></a>
### Parâmetros Opcionais

Vários provedores OAuth suportam outros parâmetros opcionais na requisição de redirecionamento. Para incluir quaisquer parâmetros opcionais na requisição, chame o método `with` com um array associativo:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> **Aviso:**
> Ao usar o método `with`, tome cuidado para não passar palavras reservadas como `state` ou `response_type`.

<a id="retrieving-user-details"></a>
## Recuperando Detalhes do Usuário

Depois que o usuário for redirecionado de volta para a rota de callback de autenticação da sua aplicação, você pode recuperar os detalhes do usuário usando o método `user` do Socialite. O objeto de usuário retornado pelo método `user` fornece diversas propriedades e métodos que você pode usar para armazenar informações sobre o usuário no seu próprio banco de dados.

Propriedades e métodos diferentes podem estar disponíveis neste objeto, dependendo se o provedor OAuth com o qual você está autenticando oferece suporte a OAuth 1.0 ou OAuth 2.0:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 providers...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 providers...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All providers...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a id="retrieving-user-details-from-a-token-oauth2"></a>
#### Recuperando Detalhes do Usuário a Partir de um Token

Se você já possui um access token válido para um usuário, pode recuperar os detalhes dele usando o método `userFromToken` do Socialite:

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

Se você estiver usando o Facebook Limited Login por meio de um aplicativo iOS, o Facebook retornará um token OIDC em vez de um access token. Para recuperar os detalhes do usuário a partir do token OIDC, forneça o nonce usado para iniciar o login ao método `userFromToken`:

```php
$user = Socialite::driver('facebook')->userFromToken($token, $nonce);
```

<a id="stateless-authentication"></a>
#### Autenticação Stateless

O método `stateless` pode ser usado para desabilitar a verificação de estado da sessão. Isso é útil ao adicionar autenticação social a uma API stateless que não utiliza sessões baseadas em cookies:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a id="testing"></a>
## Testes

O Laravel Socialite oferece uma maneira conveniente de testar fluxos de autenticação OAuth sem fazer requisições reais aos provedores OAuth. O método `fake` permite mockar o comportamento do provedor OAuth e definir os dados do usuário que devem ser retornados.

<a id="faking-the-redirect"></a>
#### Simulando o Redirecionamento

Para testar se sua aplicação redireciona corretamente os usuários para um provedor OAuth, você pode invocar o método `fake` antes de fazer uma requisição à sua rota de redirecionamento. Isso fará com que o Socialite retorne um redirecionamento para uma URL de autorização falsa, em vez de redirecionar para o provedor OAuth real:

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a id="faking-the-callback"></a>
#### Simulando o Callback

Para testar a rota de callback da sua aplicação, você pode invocar o método `fake` e fornecer uma instância de `User` que deve ser retornada quando sua aplicação solicitar os detalhes do usuário ao provedor. A instância de `User` pode ser criada usando o método `fake`:

```php
use Laravel\Socialite\Socialite;
use Laravel\Socialite\Two\User;

test('user can login with github', function () {
    Socialite::fake('github', User::fake([
        'id' => 'github-123',
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
    ]));

    $response = $this->get('/auth/github/callback');

    $response->assertRedirect('/dashboard');

    $this->assertDatabaseHas('users', [
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
        'github_id' => 'github-123',
    ]);
});
```

Por padrão, a instância de `User` incluirá valores de token OAuth falsos. Se necessário, você pode sobrescrever esses valores passando atributos adicionais ao método `fake`:

```php
$fakeUser = User::fake([
    'id' => 'github-123',
    'name' => 'Jason Beggs',
    'email' => 'jason@example.com',
    'token' => 'fake-token',
    'refreshToken' => 'fake-refresh-token',
    'expiresIn' => 3600,
    'approvedScopes' => ['read', 'write'],
]);
```

Usuários OAuth 1 podem ser simulados usando a classe `Laravel\Socialite\One\User`.
