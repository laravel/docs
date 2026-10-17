---
title: "Laravel Sanctum"
---

- [Introdução](#introduction)
    - [Como Funciona](#how-it-works)
- [Instalação](#installation)
- [Configuração](#configuration)
    - [Sobrescrevendo os Modelos Padrão](#overriding-default-models)
- [Autenticação com Tokens de API](#api-token-authentication)
    - [Emitindo Tokens de API](#issuing-api-tokens)
    - [Habilidades dos Tokens](#token-abilities)
    - [Protegendo Rotas](#protecting-routes)
    - [Revogando Tokens](#revoking-tokens)
    - [Expiração de Tokens](#token-expiration)
- [Autenticação de SPA](#spa-authentication)
    - [Configuração](#spa-configuration)
    - [Autenticando](#spa-authenticating)
    - [Protegendo Rotas](#protecting-spa-routes)
    - [Autorizando Canais de Broadcast Privados](#authorizing-private-broadcast-channels)
- [Autenticação de Aplicações Mobile](#mobile-application-authentication)
    - [Emitindo Tokens de API](#issuing-mobile-api-tokens)
    - [Protegendo Rotas](#protecting-mobile-api-routes)
    - [Revogando Tokens](#revoking-mobile-api-tokens)
- [Testes](#testing)

<a id="introduction"></a>
## Introdução

[Laravel Sanctum](https://github.com/laravel/sanctum) fornece um sistema de autenticação ultraleve para SPAs (aplicações de página única), aplicações mobile e APIs simples baseadas em tokens. O Sanctum permite que cada usuário da sua aplicação gere múltiplos tokens de API para sua conta. Esses tokens podem receber habilidades / escopos que especificam quais ações os tokens têm permissão para realizar.

<a id="how-it-works"></a>
### Como Funciona

O Laravel Sanctum existe para resolver dois problemas distintos. Vamos discutir cada um antes de nos aprofundarmos na biblioteca.

<a id="how-it-works-api-tokens"></a>
#### Tokens de API

Primeiro, o Sanctum é um pacote simples que você pode usar para emitir tokens de API para seus usuários sem a complexidade do OAuth. Esse recurso é inspirado no GitHub e em outras aplicações que emitem "tokens de acesso pessoal". Por exemplo, imagine que as "configurações de conta" da sua aplicação tenham uma tela onde um usuário pode gerar um token de API para sua conta. Você pode usar o Sanctum para gerar e gerenciar esses tokens. Esses tokens normalmente têm um tempo de expiração muito longo (anos), mas podem ser revogados manualmente pelo usuário a qualquer momento.

O Laravel Sanctum oferece esse recurso armazenando os tokens de API dos usuários em uma única tabela de banco de dados e autenticando as requisições HTTP recebidas via o cabeçalho `Authorization`, que deve conter um token de API válido.

<a id="how-it-works-spa-authentication"></a>
#### Autenticação de SPA

Segundo, o Sanctum existe para oferecer uma maneira simples de autenticar aplicações de página única (SPAs) que precisam se comunicar com uma API alimentada pelo Laravel. Essas SPAs podem existir no mesmo repositório da sua aplicação Laravel ou podem estar em um repositório totalmente separado, como uma SPA criada usando Next.js ou Nuxt.

Para esse recurso, o Sanctum não usa tokens de nenhum tipo. Em vez disso, o Sanctum usa os serviços de autenticação de sessão baseada em cookies integrados ao Laravel. Normalmente, o Sanctum utiliza o guard de autenticação `web` do Laravel para fazer isso. Isso fornece os benefícios da proteção CSRF, da autenticação de sessão, além de proteger contra o vazamento das credenciais de autenticação via XSS.

O Sanctum só tentará autenticar usando cookies quando a requisição recebida se originar do seu próprio frontend SPA. Quando o Sanctum examina uma requisição HTTP recebida, ele primeiro verificará a presença de um cookie de autenticação e, se nenhum estiver presente, o Sanctum então examinará o cabeçalho `Authorization` em busca de um token de API válido.

> **Note:**
> É perfeitamente adequado usar o Sanctum apenas para autenticação com tokens de API ou apenas para autenticação de SPA. Só porque você usa o Sanctum não significa que você é obrigado a usar os dois recursos que ele oferece.

<a id="installation"></a>
## Instalação

Você pode instalar o Laravel Sanctum via o comando Artisan `install:api`:

```shell
php artisan install:api
```

Em seguida, se você planeja utilizar o Sanctum para autenticar uma SPA, por favor consulte a seção [Autenticação de SPA](#spa-authentication) desta documentação.

<a id="configuration"></a>
## Configuração

<a id="overriding-default-models"></a>
### Sobrescrevendo os Modelos Padrão

Embora normalmente não seja necessário, você é livre para estender o modelo `PersonalAccessToken` usado internamente pelo Sanctum:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

Então, você pode instruir o Sanctum a usar seu modelo personalizado via o método `usePersonalAccessTokenModel` fornecido pelo Sanctum. Normalmente, você deve chamar esse método no método `boot` do arquivo `AppServiceProvider` da sua aplicação:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a id="api-token-authentication"></a>
## Autenticação com Tokens de API

> **Note:**
> Você não deve usar tokens de API para autenticar sua própria SPA de primeira parte. Em vez disso, use os [recursos de autenticação de SPA](#spa-authentication) integrados ao Sanctum.

<a id="issuing-api-tokens"></a>
### Emitindo Tokens de API

O Sanctum permite que você emita tokens de API / tokens de acesso pessoal que podem ser usados para autenticar requisições de API à sua aplicação. Ao fazer requisições usando tokens de API, o token deve ser incluído no cabeçalho `Authorization` como um token `Bearer`.

Para começar a emitir tokens para os usuários, seu modelo User deve usar a trait `Laravel\Sanctum\HasApiTokens`:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

Para emitir um token, você pode usar o método `createToken`. O método `createToken` retorna uma instância de `Laravel\Sanctum\NewAccessToken`. Os tokens de API passam por hash usando o algoritmo SHA-256 antes de serem armazenados no seu banco de dados, mas você pode acessar o valor em texto puro do token usando a propriedade `plainTextToken` da instância `NewAccessToken`. Você deve exibir esse valor ao usuário imediatamente após o token ter sido criado:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

Você pode acessar todos os tokens do usuário usando o relacionamento Eloquent `tokens` fornecido pela trait `HasApiTokens`:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a id="token-abilities"></a>
### Habilidades dos Tokens

O Sanctum permite que você atribua "habilidades" aos tokens. As habilidades têm uma finalidade semelhante aos "escopos" do OAuth. Você pode passar um array de habilidades em formato de string como segundo argumento para o método `createToken`:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Ao tratar uma requisição recebida autenticada pelo Sanctum, você pode determinar se o token possui uma habilidade específica usando os métodos `tokenCan` ou `tokenCant`:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a id="token-ability-middleware"></a>
#### Middleware de Habilidade de Token

O Sanctum também inclui dois middlewares que podem ser usados para verificar se uma requisição recebida está autenticada com um token ao qual foi concedida uma determinada habilidade. Para começar, defina os seguintes aliases de middleware no arquivo `bootstrap/app.php` da sua aplicação:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

O middleware `abilities` pode ser atribuído a uma rota para verificar se o token da requisição recebida possui todas as habilidades listadas:

```php
Route::get('/orders', function () {
    // O token possui ambas as habilidades "check-status" e "place-orders"...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

O middleware `ability` pode ser atribuído a uma rota para verificar se o token da requisição recebida possui *pelo menos uma* das habilidades listadas:

```php
Route::get('/orders', function () {
    // O token possui a habilidade "check-status" ou "place-orders"...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a id="first-party-ui-initiated-requests"></a>
#### Requisições Iniciadas pela UI de Primeira Parte

Por conveniência, o método `tokenCan` sempre retornará `true` se a requisição autenticada recebida veio da sua SPA de primeira parte e você estiver usando a [autenticação de SPA](#spa-authentication) integrada ao Sanctum.

No entanto, isso não significa necessariamente que sua aplicação deva permitir que o usuário realize a ação. Normalmente, as [policies de autorização](/en/authorization/#creating-policies) da sua aplicação determinarão se o token recebeu permissão para realizar as habilidades, além de verificar se a própria instância do usuário deve ter permissão para realizar a ação.

Por exemplo, se imaginarmos uma aplicação que gerencia servidores, isso pode significar verificar se o token está autorizado a atualizar servidores **e** que o servidor pertence ao usuário:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update');
```

À primeira vista, permitir que o método `tokenCan` seja chamado e sempre retorne `true` para requisições iniciadas pela UI de primeira parte pode parecer estranho; no entanto, é conveniente poder sempre assumir que um token de API está disponível e pode ser inspecionado via o método `tokenCan`. Ao adotar essa abordagem, você pode sempre chamar o método `tokenCan` dentro das policies de autorização da sua aplicação sem se preocupar com o fato de a requisição ter sido disparada a partir da UI da sua aplicação ou iniciada por um dos consumidores de terceiros da sua API.

<a id="protecting-routes"></a>
### Protegendo Rotas

Para proteger rotas de modo que todas as requisições recebidas precisem ser autenticadas, você deve anexar o guard de autenticação `sanctum` às suas rotas protegidas dentro dos arquivos de rotas `routes/web.php` e `routes/api.php`. Esse guard garantirá que as requisições recebidas sejam autenticadas tanto como requisições stateful autenticadas por cookie quanto que contenham um cabeçalho de token de API válido, caso a requisição seja de um terceiro.

Você pode estar se perguntando por que sugerimos que você autentique as rotas dentro do arquivo `routes/web.php` da sua aplicação usando o guard `sanctum`. Lembre-se de que o Sanctum primeiro tentará autenticar as requisições recebidas usando o típico cookie de autenticação de sessão do Laravel. Se esse cookie não estiver presente, o Sanctum tentará autenticar a requisição usando um token no cabeçalho `Authorization` da requisição. Além disso, autenticar todas as requisições usando o Sanctum garante que possamos sempre chamar o método `tokenCan` na instância do usuário atualmente autenticado:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a id="revoking-tokens"></a>
### Revogando Tokens

Você pode "revogar" tokens excluindo-os do seu banco de dados usando o relacionamento `tokens` fornecido pela trait `Laravel\Sanctum\HasApiTokens`:

```php
// Revogar todos os tokens...
$user->tokens()->delete();

// Revogar o token que foi usado para autenticar a requisição atual...
$request->user()->currentAccessToken()->delete();

// Revogar um token específico...
$user->tokens()->where('id', $tokenId)->delete();
```

<a id="token-expiration"></a>
### Expiração de Tokens

Por padrão, os tokens do Sanctum nunca expiram e só podem ser invalidados [revogando o token](#revoking-tokens). No entanto, se você quiser configurar um tempo de expiração para os tokens de API da sua aplicação, pode fazê-lo via a opção de configuração `expiration` definida no arquivo de configuração `sanctum` da sua aplicação. Essa opção de configuração define o número de minutos até que um token emitido seja considerado expirado:

```php
'expiration' => 525600,
```

Se você quiser especificar o tempo de expiração de cada token individualmente, pode fazê-lo fornecendo o tempo de expiração como terceiro argumento ao método `createToken`:

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

Se você configurou um tempo de expiração de token para sua aplicação, pode também querer [agendar uma tarefa](/en/scheduling/) para limpar os tokens expirados da sua aplicação. Felizmente, o Sanctum inclui um comando Artisan `sanctum:prune-expired` que você pode usar para fazer isso. Por exemplo, você pode configurar uma tarefa agendada para excluir todos os registros de token do banco de dados que estejam expirados há pelo menos 24 horas:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a id="spa-authentication"></a>
## Autenticação de SPA

O Sanctum também existe para fornecer um método simples de autenticar aplicações de página única (SPAs) que precisam se comunicar com uma API alimentada pelo Laravel. Essas SPAs podem existir no mesmo repositório da sua aplicação Laravel ou podem estar em um repositório totalmente separado.

Para esse recurso, o Sanctum não usa tokens de nenhum tipo. Em vez disso, o Sanctum usa os serviços de autenticação de sessão baseada em cookies integrados ao Laravel. Essa abordagem de autenticação fornece os benefícios da proteção CSRF, da autenticação de sessão, além de proteger contra o vazamento das credenciais de autenticação via XSS.

> **Warning:**
> Para autenticar, sua SPA e sua API devem compartilhar o mesmo domínio de nível superior. No entanto, elas podem ser colocadas em subdomínios diferentes. Além disso, você deve garantir que envie o cabeçalho `Accept: application/json` e também o cabeçalho `Referer` ou `Origin` com sua requisição.

<a id="spa-configuration"></a>
### Configuração

<a id="configuring-your-first-party-domains"></a>
#### Configurando Seus Domínios de Primeira Parte

Primeiro, você deve configurar de quais domínios sua SPA fará requisições. Você pode configurar esses domínios usando a opção de configuração `stateful` no seu arquivo de configuração `sanctum`. Essa configuração determina quais domínios manterão a autenticação "stateful" usando cookies de sessão do Laravel ao fazer requisições à sua API.

Para ajudá-lo a configurar seus domínios stateful de primeira parte, o Sanctum fornece duas funções auxiliares que você pode incluir na configuração. Primeiro, `Sanctum::currentApplicationUrlWithPort()` retornará a URL atual da aplicação a partir da variável de ambiente `APP_URL`, e `Sanctum::currentRequestHost()` injetará um placeholder na lista de domínios stateful que, em tempo de execução, será substituído pelo host da requisição atual, de modo que todas as requisições com o mesmo domínio sejam consideradas stateful.

> **Warning:**
> Se você estiver acessando sua aplicação via uma URL que inclui uma porta (`127.0.0.1:8000`), você deve garantir que inclua o número da porta junto ao domínio.

<a id="sanctum-middleware"></a>
#### Middleware do Sanctum

Em seguida, você deve instruir o Laravel de que as requisições recebidas da sua SPA podem autenticar usando os cookies de sessão do Laravel, ao mesmo tempo que ainda permite que requisições de terceiros ou de aplicações mobile autentiquem usando tokens de API. Isso pode ser facilmente realizado invocando o método de middleware `statefulApi` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a id="cors-and-cookies"></a>
#### CORS e Cookies

Se você estiver tendo problemas para autenticar com sua aplicação a partir de uma SPA que é executada em um subdomínio separado, provavelmente configurou incorretamente suas configurações de CORS (Cross-Origin Resource Sharing) ou de cookie de sessão.

O arquivo de configuração `config/cors.php` não é publicado por padrão. Se você precisar personalizar as opções de CORS do Laravel, deve publicar o arquivo de configuração `cors` completo usando o comando Artisan `config:publish`:

```shell
php artisan config:publish cors
```

Em seguida, você deve garantir que a configuração de CORS da sua aplicação esteja retornando o cabeçalho `Access-Control-Allow-Credentials` com um valor de `True`. Isso pode ser realizado definindo a opção `supports_credentials` dentro do arquivo de configuração `config/cors.php` da sua aplicação como `true`.

Além disso, você deve habilitar as opções `withCredentials` e `withXSRFToken` na instância global `axios` da sua aplicação. Isso pode ser feito no seu arquivo `resources/js/app.js`. Se você não estiver usando o Axios para fazer requisições HTTP a partir do seu frontend, deve realizar a configuração equivalente no seu próprio cliente HTTP:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

Por fim, você deve garantir que a configuração de domínio do cookie de sessão da sua aplicação suporte qualquer subdomínio do seu domínio raiz. Você pode fazer isso prefixando o domínio com um `.` inicial dentro do arquivo de configuração `config/session.php` da sua aplicação:

```php
'domain' => '.domain.com',
```

<a id="spa-authenticating"></a>
### Autenticando

<a id="csrf-protection"></a>
#### Proteção CSRF

Para autenticar sua SPA, a página de "login" da sua SPA deve primeiro fazer uma requisição ao endpoint `/sanctum/csrf-cookie` para inicializar a proteção CSRF da aplicação:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

Durante essa requisição, o Laravel definirá um cookie `XSRF-TOKEN` contendo o token CSRF atual. Esse token deve então ser decodificado da URL e passado em um cabeçalho `X-XSRF-TOKEN` nas requisições subsequentes, o que algumas bibliotecas de cliente HTTP, como o Axios e o HttpClient do Angular, farão automaticamente para você. Se sua biblioteca HTTP JavaScript não definir o valor para você, será necessário definir manualmente o cabeçalho `X-XSRF-TOKEN` para corresponder ao valor decodificado da URL do cookie `XSRF-TOKEN` que é definido por essa rota.

<a id="logging-in"></a>
#### Fazendo Login

Depois que a proteção CSRF tiver sido inicializada, você deve fazer uma requisição `POST` à rota `/login` da sua aplicação Laravel. Essa rota `/login` pode ser [implementada manualmente](/en/authentication/#authenticating-users) ou usando um pacote de autenticação headless como o [Laravel Fortify](/en/fortify/).

Se a requisição de login for bem-sucedida, você será autenticado e as requisições subsequentes às rotas da sua aplicação serão automaticamente autenticadas via o cookie de sessão que a aplicação Laravel emitiu ao seu cliente. Além disso, como sua aplicação já fez uma requisição à rota `/sanctum/csrf-cookie`, as requisições subsequentes devem receber automaticamente a proteção CSRF, desde que seu cliente HTTP JavaScript envie o valor do cookie `XSRF-TOKEN` no cabeçalho `X-XSRF-TOKEN`.

É claro que, se a sessão do seu usuário expirar por falta de atividade, as requisições subsequentes à aplicação Laravel podem receber uma resposta de erro HTTP 401 ou 419. Nesse caso, você deve redirecionar o usuário para a página de login da sua SPA.

Como essa abordagem de autenticação de SPA é baseada em sessão, você pode usar os serviços de autenticação padrão do Laravel, incluindo a funcionalidade ["remember me"](/en/authentication/#remembering-users).

> **Warning:**
> Você é livre para escrever seu próprio endpoint `/login`; no entanto, você deve garantir que ele autentique o usuário usando os [serviços de autenticação baseada em sessão padrão que o Laravel fornece](/en/authentication/#authenticating-users). Normalmente, isso significa usar o guard de autenticação `web`.

<a id="protecting-spa-routes"></a>
### Protegendo Rotas

Para proteger rotas de modo que todas as requisições recebidas precisem ser autenticadas, você deve anexar o guard de autenticação `sanctum` às suas rotas de API dentro do arquivo `routes/api.php`. Esse guard garantirá que as requisições recebidas sejam autenticadas tanto como requisições autenticadas stateful da sua SPA quanto que contenham um cabeçalho de token de API válido, caso a requisição seja de um terceiro:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a id="authorizing-private-broadcast-channels"></a>
### Autorizando Canais de Broadcast Privados

Se sua SPA precisar autenticar com [canais de broadcast privados / de presença](/en/broadcasting/#authorizing-channels), você deve remover a entrada `channels` do método `withRouting` contido no arquivo `bootstrap/app.php` da sua aplicação. Em vez disso, você deve invocar o método `withBroadcasting` para que possa especificar o middleware correto para as rotas de broadcasting da sua aplicação:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
    ->create();
```

Em seguida, para que as requisições de autorização do Pusher sejam bem-sucedidas, você precisará fornecer um `authorizer` personalizado do Pusher ao inicializar o [Laravel Echo](/en/broadcasting/#client-side-installation). Isso permite que sua aplicação configure o Pusher para usar a instância `axios` que está [devidamente configurada para requisições cross-domain](#cors-and-cookies):

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a id="mobile-application-authentication"></a>
## Autenticação de Aplicações Mobile

Você também pode usar tokens do Sanctum para autenticar as requisições da sua aplicação mobile à sua API. O processo para autenticar requisições de aplicações mobile é semelhante ao de autenticar requisições de API de terceiros; no entanto, há pequenas diferenças em como você emitirá os tokens de API.

<a id="issuing-mobile-api-tokens"></a>
### Emitindo Tokens de API

Para começar, crie uma rota que aceite o e-mail / nome de usuário, a senha e o nome do dispositivo do usuário, e então troque essas credenciais por um novo token do Sanctum. O "nome do dispositivo" fornecido a esse endpoint é para fins informativos e pode ser qualquer valor que você desejar. Em geral, o valor do nome do dispositivo deve ser um nome que o usuário reconheceria, como "iPhone 17 do Nuno".

Normalmente, você fará uma requisição ao endpoint de token a partir da tela de "login" da sua aplicação mobile. O endpoint retornará o token de API em texto puro, que pode então ser armazenado no dispositivo mobile e usado para fazer requisições de API adicionais:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

Quando a aplicação mobile usar o token para fazer uma requisição de API à sua aplicação, ela deve passar o token no cabeçalho `Authorization` como um token `Bearer`.

> **Note:**
> Ao emitir tokens para uma aplicação mobile, você também é livre para especificar [habilidades dos tokens](#token-abilities).

<a id="protecting-mobile-api-routes"></a>
### Protegendo Rotas

Como documentado anteriormente, você pode proteger rotas de modo que todas as requisições recebidas precisem ser autenticadas anexando o guard de autenticação `sanctum` às rotas:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a id="revoking-mobile-api-tokens"></a>
### Revogando Tokens

Para permitir que os usuários revoguem tokens de API emitidos para dispositivos mobile, você pode listá-los por nome, junto com um botão "Revogar", dentro de uma parte de "configurações de conta" da UI da sua aplicação web. Quando o usuário clicar no botão "Revogar", você pode excluir o token do banco de dados. Lembre-se de que você pode acessar os tokens de API de um usuário via o relacionamento `tokens` fornecido pela trait `Laravel\Sanctum\HasApiTokens`:

```php
// Revogar todos os tokens...
$user->tokens()->delete();

// Revogar um token específico...
$user->tokens()->where('id', $tokenId)->delete();
```

<a id="testing"></a>
## Testes

Durante os testes, o método `Sanctum::actingAs` pode ser usado para autenticar um usuário e especificar quais habilidades devem ser concedidas ao seu token:

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

Se você quiser conceder todas as habilidades ao token, deve incluir `*` na lista de habilidades fornecida ao método `actingAs`:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```