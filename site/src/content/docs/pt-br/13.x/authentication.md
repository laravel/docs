---
title: "Autenticação"
---

- [Introdução](#introduction)
    - [Starter Kits](#starter-kits)
    - [Considerações sobre o Banco de Dados](#introduction-database-considerations)
    - [Visão Geral do Ecossistema](#ecosystem-overview)
- [Início Rápido de Autenticação](#authentication-quickstart)
    - [Instalar um Starter Kit](#install-a-starter-kit)
    - [Recuperando o Usuário Autenticado](#retrieving-the-authenticated-user)
    - [Protegendo Rotas](#protecting-routes)
    - [Limitação de Tentativas de Login](#login-throttling)
- [Autenticando Usuários Manualmente](#authenticating-users)
    - [Lembrando Usuários](#remembering-users)
    - [Outros Métodos de Autenticação](#other-authentication-methods)
- [Autenticação HTTP Basic](#http-basic-authentication)
    - [Autenticação HTTP Basic Sem Estado](#stateless-http-basic-authentication)
- [Encerrando a Sessão (Logout)](#logging-out)
    - [Invalidando Sessões em Outros Dispositivos](#invalidating-sessions-on-other-devices)
- [Confirmação de Senha](#password-confirmation)
    - [Configuração](#password-confirmation-configuration)
    - [Roteamento](#password-confirmation-routing)
    - [Protegendo Rotas](#password-confirmation-protecting-routes)
- [Adicionando Guards Personalizados](#adding-custom-guards)
    - [Guards de Requisição Baseados em Closure](#closure-request-guards)
- [Adicionando User Providers Personalizados](#adding-custom-user-providers)
    - [O Contract User Provider](#the-user-provider-contract)
    - [O Contract Authenticatable](#the-authenticatable-contract)
- [Re-hashing Automático de Senhas](#automatic-password-rehashing)
- [Autenticação Social](../socialite/)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

Muitas aplicações web oferecem uma forma de seus usuários se autenticarem na aplicação e fazerem "login". Implementar esse recurso em aplicações web pode ser uma tarefa complexa e potencialmente arriscada. Por essa razão, o Laravel se esforça para fornecer as ferramentas de que você precisa para implementar a autenticação de forma rápida, segura e fácil.

Em sua essência, os recursos de autenticação do Laravel são compostos por "guards" e "providers". Guards definem como os usuários são autenticados em cada requisição. Por exemplo, o Laravel vem com um guard `session` que mantém o estado usando o armazenamento de sessão e cookies.

Providers definem como os usuários são recuperados do seu armazenamento persistente. O Laravel vem com suporte para recuperar usuários usando o [Eloquent](../eloquent/) e o query builder do banco de dados. No entanto, você tem a liberdade de definir providers adicionais conforme necessário para a sua aplicação.

O arquivo de configuração de autenticação da sua aplicação está localizado em `config/auth.php`. Esse arquivo contém diversas opções bem documentadas para ajustar o comportamento dos serviços de autenticação do Laravel.

> **Note:**
> Guards e providers não devem ser confundidos com "roles" e "permissions". Para saber mais sobre a autorização de ações de usuários por meio de permissões, consulte a documentação de [autorização](../authorization/).

<a id="starter-kits"></a>
### Starter Kits

Quer começar rapidamente? Instale um [starter kit de aplicação Laravel](../starter-kits/) em uma aplicação Laravel nova. Após migrar seu banco de dados, navegue com seu navegador até `/register` ou qualquer outra URL atribuída à sua aplicação. Os starter kits cuidarão de estruturar todo o seu sistema de autenticação!

**Mesmo que você opte por não usar um starter kit na sua aplicação Laravel final, instalar um [starter kit](../starter-kits/) pode ser uma ótima oportunidade de aprender como implementar toda a funcionalidade de autenticação do Laravel em um projeto Laravel real.** Como os starter kits do Laravel contêm controllers, rotas e views de autenticação prontos, você pode examinar o código dentro desses arquivos para aprender como os recursos de autenticação do Laravel podem ser implementados.

<a id="introduction-database-considerations"></a>
### Considerações sobre o Banco de Dados

Por padrão, o Laravel inclui um [modelo Eloquent](../eloquent/) `App\Models\User` no seu diretório `app/Models`. Esse modelo pode ser usado com o driver de autenticação Eloquent padrão.

Se a sua aplicação não estiver usando o Eloquent, você pode usar o provider de autenticação `database`, que utiliza o query builder do Laravel. Se a sua aplicação estiver usando MongoDB, confira a [documentação oficial de autenticação de usuários Laravel do MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/).

Ao construir o esquema do banco de dados para o modelo `App\Models\User`, certifique-se de que a coluna de senha tenha pelo menos 60 caracteres de comprimento. Obviamente, a migration da tabela `users` que está incluída em novas aplicações Laravel já cria uma coluna que excede esse comprimento.

Além disso, você deve verificar se a sua tabela `users` (ou equivalente) contém uma coluna `remember_token` do tipo string, anulável, de 100 caracteres. Essa coluna será usada para armazenar um token para usuários que selecionarem a opção "remember me" ao fazer login na sua aplicação. Novamente, a migration padrão da tabela `users` incluída em novas aplicações Laravel já contém essa coluna.

<a id="ecosystem-overview"></a>
### Visão Geral do Ecossistema

O Laravel oferece diversos pacotes relacionados à autenticação. Antes de continuar, vamos revisar o ecossistema geral de autenticação no Laravel e discutir o propósito pretendido de cada pacote.

Primeiro, considere como a autenticação funciona. Ao usar um navegador web, um usuário fornecerá seu nome de usuário e senha por meio de um formulário de login. Se essas credenciais estiverem corretas, a aplicação armazenará informações sobre o usuário autenticado na [sessão](../session/) do usuário. Um cookie emitido para o navegador contém o ID da sessão, de modo que requisições subsequentes à aplicação possam associar o usuário à sessão correta. Depois que o cookie de sessão é recebido, a aplicação recuperará os dados da sessão com base no ID da sessão, notará que as informações de autenticação foram armazenadas na sessão e considerará o usuário como "autenticado".

Quando um serviço remoto precisa se autenticar para acessar uma API, cookies normalmente não são usados para autenticação, pois não há um navegador web. Em vez disso, o serviço remoto envia um token de API para a API a cada requisição. A aplicação pode validar o token recebido contra uma tabela de tokens de API válidos e "autenticar" a requisição como sendo realizada pelo usuário associado a esse token de API.

<a id="laravels-built-in-browser-authentication-services"></a>
#### Serviços de Autenticação de Navegador Integrados do Laravel

O Laravel inclui serviços de autenticação e de sessão integrados, que normalmente são acessados por meio das facades `Auth` e `Session`. Esses recursos fornecem autenticação baseada em cookies para requisições iniciadas a partir de navegadores web. Eles fornecem métodos que permitem verificar as credenciais de um usuário e autenticá-lo. Além disso, esses serviços armazenarão automaticamente os dados de autenticação adequados na sessão do usuário e emitirão o cookie de sessão do usuário. Uma discussão sobre como usar esses serviços está contida nesta documentação.

**Starter Kits de Aplicação**

Conforme discutido nesta documentação, você pode interagir com esses serviços de autenticação manualmente para construir a própria camada de autenticação da sua aplicação. No entanto, para ajudá-lo a começar mais rapidamente, lançamos [starter kits gratuitos](../starter-kits/) que fornecem uma estruturação robusta e moderna de toda a camada de autenticação.

<a id="laravels-api-authentication-services"></a>
#### Serviços de Autenticação de API do Laravel

O Laravel fornece dois pacotes opcionais para ajudá-lo a gerenciar tokens de API e autenticar requisições feitas com tokens de API: [Passport](../passport/) e [Sanctum](../sanctum/). Observe que essas bibliotecas e as bibliotecas de autenticação baseada em cookies integradas do Laravel não são mutuamente exclusivas. Essas bibliotecas focam principalmente na autenticação por token de API, enquanto os serviços de autenticação integrados focam na autenticação de navegador baseada em cookies. Muitas aplicações usarão tanto os serviços de autenticação baseada em cookies integrados do Laravel quanto um dos pacotes de autenticação de API do Laravel.

**Passport**

O Passport é um provider de autenticação OAuth2, oferecendo uma variedade de "grant types" do OAuth2 que permitem emitir diversos tipos de tokens. Em geral, este é um pacote robusto e complexo para autenticação de API. No entanto, a maioria das aplicações não requer os recursos complexos oferecidos pela especificação OAuth2, que podem ser confusos tanto para usuários quanto para desenvolvedores. Além disso, os desenvolvedores historicamente ficaram confusos sobre como autenticar aplicações SPA ou aplicações móveis usando providers de autenticação OAuth2 como o Passport.

**Sanctum**

Em resposta à complexidade do OAuth2 e à confusão dos desenvolvedores, decidimos construir um pacote de autenticação mais simples e simplificado, capaz de lidar tanto com requisições web de primeira parte a partir de um navegador quanto com requisições de API via tokens. Esse objetivo foi alcançado com o lançamento do [Laravel Sanctum](../sanctum/), que deve ser considerado o pacote de autenticação preferido e recomendado para aplicações que oferecerão uma UI web de primeira parte além de uma API, ou que serão alimentadas por uma single-page application (SPA) que existe separadamente da aplicação Laravel de backend, ou aplicações que oferecem um cliente móvel.

O Laravel Sanctum é um pacote híbrido de autenticação web / API que pode gerenciar todo o processo de autenticação da sua aplicação. Isso é possível porque, quando aplicações baseadas em Sanctum recebem uma requisição, o Sanctum primeiro determinará se a requisição inclui um cookie de sessão que referencia uma sessão autenticada. O Sanctum faz isso chamando os serviços de autenticação integrados do Laravel que discutimos anteriormente. Se a requisição não estiver sendo autenticada via cookie de sessão, o Sanctum inspecionará a requisição em busca de um token de API. Se um token de API estiver presente, o Sanctum autenticará a requisição usando esse token. Para saber mais sobre esse processo, consulte a documentação ["how it works"](../sanctum/#how-it-works) do Sanctum.

<a id="summary-choosing-your-stack"></a>
#### Resumo e Escolha da Sua Stack

Em resumo, se a sua aplicação for acessada usando um navegador e você estiver construindo uma aplicação Laravel monolítica, a sua aplicação usará os serviços de autenticação integrados do Laravel.

Em seguida, se a sua aplicação oferecer uma API que será consumida por terceiros, você escolherá entre o [Passport](../passport/) ou o [Sanctum](../sanctum/) para fornecer autenticação por token de API para a sua aplicação. Em geral, o Sanctum deve ser preferido sempre que possível, já que é uma solução simples e completa para autenticação de API, autenticação de SPA e autenticação móvel, incluindo suporte para "scopes" ou "abilities".

Se você estiver construindo uma single-page application (SPA) que será alimentada por um backend Laravel, você deve usar o [Laravel Sanctum](../sanctum/). Ao usar o Sanctum, você precisará [implementar manualmente suas próprias rotas de autenticação de backend](#authenticating-users) ou utilizar o [Laravel Fortify](../fortify/) como um serviço de backend de autenticação headless que fornece rotas e controllers para recursos como registro, redefinição de senha, verificação de e-mail e muito mais.

O Passport pode ser escolhido quando a sua aplicação absolutamente precisa de todos os recursos fornecidos pela especificação OAuth2. Além disso, se você estiver construindo um [servidor MCP](../mcp/) que será acessado por clientes de IA, você deve usar o Passport, já que clientes MCP normalmente esperam [se autenticar usando OAuth](../mcp/#oauth).

E, se você quiser começar rapidamente, temos o prazer de recomendar [nossos starter kits de aplicação](../starter-kits/) como uma forma rápida de iniciar uma nova aplicação Laravel que já usa nossa stack de autenticação preferida dos serviços de autenticação integrados do Laravel.

<a id="authentication-quickstart"></a>
## Início Rápido de Autenticação

> **Warning:**
> Esta parte da documentação discute a autenticação de usuários por meio dos [starter kits de aplicação Laravel](../starter-kits/), que incluem estruturação de UI para ajudá-lo a começar rapidamente. Se você quiser integrar diretamente com os sistemas de autenticação do Laravel, confira a documentação sobre [autenticação manual de usuários](#authenticating-users).

<a id="install-a-starter-kit"></a>
### Instalar um Starter Kit

Primeiro, você deve [instalar um starter kit de aplicação Laravel](../starter-kits/). Nossos starter kits oferecem pontos de partida lindamente projetados para incorporar autenticação na sua aplicação Laravel nova.

<a id="retrieving-the-authenticated-user"></a>
### Recuperando o Usuário Autenticado

Depois de criar uma aplicação a partir de um starter kit e permitir que os usuários se registrem e se autentiquem na sua aplicação, você frequentemente precisará interagir com o usuário autenticado no momento. Ao lidar com uma requisição recebida, você pode acessar o usuário autenticado por meio do método `user` da facade `Auth`:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

Alternativamente, uma vez que um usuário está autenticado, você pode acessar o usuário autenticado por meio de uma instância de `Illuminate\Http\Request`. Lembre-se, classes com type-hint serão injetadas automaticamente nos métodos dos seus controllers. Ao fazer type-hint do objeto `Illuminate\Http\Request`, você pode obter acesso conveniente ao usuário autenticado a partir de qualquer método de controller na sua aplicação por meio do método `user` da requisição:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a id="determining-if-the-current-user-is-authenticated"></a>
#### Determinando se o Usuário Atual Está Autenticado

Para determinar se o usuário que está fazendo a requisição HTTP recebida está autenticado, você pode usar o método `check` na facade `Auth`. Esse método retornará `true` se o usuário estiver autenticado:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> **Note:**
> Embora seja possível determinar se um usuário está autenticado usando o método `check`, você normalmente usará um middleware para verificar se o usuário está autenticado antes de permitir que ele acesse determinadas rotas / controllers. Para saber mais sobre isso, confira a documentação sobre [proteção de rotas](../authentication/#protecting-routes).

<a id="protecting-routes"></a>
### Protegendo Rotas

[Route middleware](../middleware/) pode ser usado para permitir que apenas usuários autenticados acessem uma determinada rota. O Laravel vem com um middleware `auth`, que é um [middleware alias](../middleware/#middleware-aliases) para a classe `Illuminate\Auth\Middleware\Authenticate`. Como esse middleware já tem um alias internamente definido pelo Laravel, tudo o que você precisa fazer é anexar o middleware a uma definição de rota:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a id="redirecting-unauthenticated-users"></a>
#### Redirecionando Usuários Não Autenticados

Quando o middleware `auth` detecta um usuário não autenticado, ele redirecionará o usuário para a [named route](../routing/#named-routes) `login`. Você pode modificar esse comportamento usando o método `redirectGuestsTo` dentro do arquivo `bootstrap/app.php` da sua aplicação:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a id="redirecting-authenticated-users"></a>
#### Redirecionando Usuários Autenticados

Quando o middleware `guest` detecta um usuário autenticado, ele redirecionará o usuário para a named route `dashboard` ou `home`. Você pode modificar esse comportamento usando o método `redirectUsersTo` dentro do arquivo `bootstrap/app.php` da sua aplicação:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a id="specifying-a-guard"></a>
#### Especificando um Guard

Ao anexar o middleware `auth` a uma rota, você também pode especificar qual "guard" deve ser usado para autenticar o usuário. O guard especificado deve corresponder a uma das chaves no array `guards` do seu arquivo de configuração `auth.php`:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a id="login-throttling"></a>
### Limitação de Tentativas de Login

Se você estiver usando um dos nossos [starter kits de aplicação](../starter-kits/), o rate limiting será automaticamente aplicado às tentativas de login. Por padrão, o usuário não conseguirá fazer login por um minuto se não fornecer as credenciais corretas após várias tentativas. A limitação é única para o nome de usuário / endereço de e-mail do usuário e para o endereço IP dele.

> **Note:**
> Se você quiser limitar a taxa de outras rotas na sua aplicação, confira a [documentação de rate limiting](../routing/#rate-limiting).

<a id="authenticating-users"></a>
## Autenticando Usuários Manualmente

Você não é obrigado a usar a estruturação de autenticação incluída nos [starter kits de aplicação](../starter-kits/) do Laravel. Se você optar por não usar essa estruturação, precisará gerenciar a autenticação de usuários usando diretamente as classes de autenticação do Laravel. Não se preocupe, é moleza!

Vamos acessar os serviços de autenticação do Laravel por meio da [facade](../facades/) `Auth`, então precisaremos nos certificar de importar a facade `Auth` no topo da classe. Em seguida, vamos conferir o método `attempt`. O método `attempt` é normalmente usado para lidar com tentativas de autenticação a partir do formulário de "login" da sua aplicação. Se a autenticação for bem-sucedida, você deve regenerar a [sessão](../session/) do usuário para evitar [fixação de sessão](https://en.wikipedia.org/wiki/Session_fixation):

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

O método `attempt` aceita um array de pares chave / valor como seu primeiro argumento. Os valores no array serão usados para encontrar o usuário na sua tabela de banco de dados. Então, no exemplo acima, o usuário será recuperado pelo valor da coluna `email`. Se o usuário for encontrado, a senha com hash armazenada no banco de dados será comparada com o valor de `password` passado ao método por meio do array. Você não deve fazer hash do valor de `password` da requisição recebida, já que o framework fará automaticamente o hash do valor antes de compará-lo com a senha com hash no banco de dados. Uma sessão autenticada será iniciada para o usuário se as duas senhas com hash corresponderem.

Lembre-se, os serviços de autenticação do Laravel recuperarão os usuários do seu banco de dados com base na configuração de "provider" do seu guard de autenticação. No arquivo de configuração `config/auth.php` padrão, o user provider Eloquent é especificado e é instruído a usar o modelo `App\Models\User` ao recuperar usuários. Você pode alterar esses valores dentro do seu arquivo de configuração com base nas necessidades da sua aplicação.

O método `attempt` retornará `true` se a autenticação for bem-sucedida. Caso contrário, `false` será retornado.

O método `intended` fornecido pelo redirector do Laravel redirecionará o usuário para a URL que ele estava tentando acessar antes de ser interceptado pelo middleware de autenticação. Uma URI de fallback pode ser fornecida a esse método caso o destino pretendido não esteja disponível.

<a id="specifying-additional-conditions"></a>
#### Especificando Condições Adicionais

Se desejar, você também pode adicionar condições extras de query à query de autenticação, além do e-mail e da senha do usuário. Para fazer isso, podemos simplesmente adicionar as condições de query ao array passado ao método `attempt`. Por exemplo, podemos verificar se o usuário está marcado como "active":

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

Para condições de query complexas, você pode fornecer uma closure no seu array de credenciais. Essa closure será invocada com a instância da query, permitindo que você personalize a query com base nas necessidades da sua aplicação:

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> **Warning:**
> Nesses exemplos, `email` não é uma opção obrigatória, sendo usada apenas como exemplo. Você deve usar o nome de coluna que corresponder a um "username" na sua tabela de banco de dados.

O método `attemptWhen`, que recebe uma closure como seu segundo argumento, pode ser usado para realizar uma inspeção mais extensa do usuário em potencial antes de realmente autenticá-lo. A closure recebe o usuário em potencial e deve retornar `true` ou `false` para indicar se o usuário pode ser autenticado:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a id="accessing-specific-guard-instances"></a>
#### Acessando Instâncias de Guard Específicas

Por meio do método `guard` da facade `Auth`, você pode especificar qual instância de guard gostaria de utilizar ao autenticar o usuário. Isso permite gerenciar a autenticação para partes separadas da sua aplicação usando modelos autenticáveis ou tabelas de usuários inteiramente separados.

O nome do guard passado ao método `guard` deve corresponder a um dos guards configurados no seu arquivo de configuração `auth.php`:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a id="remembering-users"></a>
### Lembrando Usuários

Muitas aplicações web fornecem uma caixa de seleção "remember me" no formulário de login. Se você quiser fornecer a funcionalidade "remember me" na sua aplicação, pode passar um valor booleano como segundo argumento para o método `attempt`.

Quando esse valor é `true`, o Laravel manterá o usuário autenticado indefinidamente ou até que ele faça logout manualmente. Sua tabela `users` deve incluir a coluna string `remember_token`, que será usada para armazenar o token "remember me". A migration da tabela `users` incluída em novas aplicações Laravel já inclui essa coluna:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

Se a sua aplicação oferecer a funcionalidade "remember me", você pode usar o método `viaRemember` para determinar se o usuário autenticado no momento foi autenticado usando o cookie "remember me":

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a id="other-authentication-methods"></a>
### Outros Métodos de Autenticação

<a id="authenticate-a-user-instance"></a>
#### Autenticar uma Instância de Usuário

Se você precisar definir uma instância de usuário existente como o usuário autenticado no momento, pode passar a instância do usuário para o método `login` da facade `Auth`. A instância de usuário fornecida deve ser uma implementação do [contract](../contracts/) `Illuminate\Contracts\Auth\Authenticatable`. O modelo `App\Models\User` incluído no Laravel já implementa essa interface. Esse método de autenticação é útil quando você já tem uma instância de usuário válida, como logo após um usuário se registrar na sua aplicação:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

Você pode passar um valor booleano como segundo argumento para o método `login`. Esse valor indica se a funcionalidade "remember me" é desejada para a sessão autenticada. Lembre-se, isso significa que a sessão será autenticada indefinidamente ou até que o usuário faça logout manualmente da aplicação:

```php
Auth::login($user, $remember = true);
```

Se necessário, você pode especificar um guard de autenticação antes de chamar o método `login`:

```php
Auth::guard('admin')->login($user);
```

<a id="authenticate-a-user-by-id"></a>
#### Autenticar um Usuário por ID

Para autenticar um usuário usando a chave primária do seu registro no banco de dados, você pode usar o método `loginUsingId`. Esse método aceita a chave primária do usuário que você deseja autenticar:

```php
Auth::loginUsingId(1);
```

Você pode passar um valor booleano ao argumento `remember` do método `loginUsingId`. Esse valor indica se a funcionalidade "remember me" é desejada para a sessão autenticada. Lembre-se, isso significa que a sessão será autenticada indefinidamente ou até que o usuário faça logout manualmente da aplicação:

```php
Auth::loginUsingId(1, remember: true);
```

<a id="authenticate-a-user-once"></a>
#### Autenticar um Usuário uma Única Vez

Você pode usar o método `once` para autenticar um usuário na aplicação por uma única requisição. Nenhuma sessão ou cookie será utilizado ao chamar esse método, e o evento `Login` não será disparado:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a id="http-basic-authentication"></a>
## Autenticação HTTP Basic

A [Autenticação HTTP Basic](https://en.wikipedia.org/wiki/Basic_access_authentication) fornece uma forma rápida de autenticar usuários da sua aplicação sem configurar uma página de "login" dedicada. Para começar, anexe o [middleware](../middleware/) `auth.basic` a uma rota. O middleware `auth.basic` está incluído no framework Laravel, então você não precisa defini-lo:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

Depois que o middleware for anexado à rota, você será automaticamente solicitado a fornecer credenciais ao acessar a rota no seu navegador. Por padrão, o middleware `auth.basic` assumirá que a coluna `email` na sua tabela de banco de dados `users` é o "username" do usuário.

<a id="a-note-on-fastcgi"></a>
#### Uma Observação sobre FastCGI

Se você estiver usando [PHP FastCGI](https://www.php.net/manual/en/install.fpm.php) e Apache para servir a sua aplicação Laravel, a autenticação HTTP Basic pode não funcionar corretamente. Para corrigir esses problemas, as seguintes linhas podem ser adicionadas ao arquivo `.htaccess` da sua aplicação:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a id="stateless-http-basic-authentication"></a>
### Autenticação HTTP Basic Sem Estado

Você também pode usar a Autenticação HTTP Basic sem definir um cookie de identificação de usuário na sessão. Isso é principalmente útil se você optar por usar a Autenticação HTTP para autenticar requisições à API da sua aplicação. Para fazer isso, [defina um middleware](../middleware/) que chame o método `onceBasic`. Se nenhuma resposta for retornada pelo método `onceBasic`, a requisição pode ser passada adiante na aplicação:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

Em seguida, anexe o middleware a uma rota:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a id="logging-out"></a>
## Encerrando a Sessão (Logout)

Para fazer logout manual dos usuários da sua aplicação, você pode usar o método `logout` fornecido pela facade `Auth`. Isso removerá as informações de autenticação da sessão do usuário, de modo que requisições subsequentes não sejam autenticadas.

Além de chamar o método `logout`, é recomendável que você invalide a sessão do usuário e regenere o [token CSRF](../csrf/) dele. Após fazer logout do usuário, você normalmente redirecionaria o usuário para a raiz da sua aplicação:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a id="invalidating-sessions-on-other-devices"></a>
### Invalidando Sessões em Outros Dispositivos

O Laravel também fornece um mecanismo para invalidar e fazer "logout" das sessões de um usuário que estão ativas em outros dispositivos, sem invalidar a sessão no dispositivo atual dele. Esse recurso é normalmente utilizado quando um usuário está alterando ou atualizando a senha e você gostaria de invalidar as sessões em outros dispositivos mantendo o dispositivo atual autenticado.

Antes de começar, você deve se certificar de que o middleware `Illuminate\Session\Middleware\AuthenticateSession` esteja incluído nas rotas que devem receber autenticação de sessão. Normalmente, você deve colocar esse middleware em uma definição de grupo de rotas para que ele possa ser aplicado à maioria das rotas da sua aplicação. Por padrão, o middleware `AuthenticateSession` pode ser anexado a uma rota usando o [middleware alias](../middleware/#middleware-aliases) `auth.session`:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

Então, você pode usar o método `logoutOtherDevices` fornecido pela facade `Auth`. Esse método exige que o usuário confirme a senha atual, que a sua aplicação deve aceitar por meio de um formulário de entrada:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

Quando o método `logoutOtherDevices` é invocado, as outras sessões do usuário serão totalmente invalidadas, o que significa que ele será "deslogado" de todos os guards pelos quais havia sido previamente autenticado.

<a id="password-confirmation"></a>
## Confirmação de Senha

Ao construir a sua aplicação, você pode ocasionalmente ter ações que devem exigir que o usuário confirme a senha antes de a ação ser realizada ou antes de o usuário ser redirecionado para uma área sensível da aplicação. O Laravel inclui um middleware integrado para tornar esse processo muito simples. Implementar esse recurso exigirá que você defina duas rotas: uma rota para exibir uma view pedindo ao usuário que confirme a senha e outra rota para confirmar que a senha é válida e redirecionar o usuário para o destino pretendido.

> **Note:**
> A documentação a seguir discute como integrar diretamente com os recursos de confirmação de senha do Laravel; no entanto, se você quiser começar mais rapidamente, os [starter kits de aplicação Laravel](../starter-kits/) incluem suporte para esse recurso!

<a id="password-confirmation-configuration"></a>
### Configuração

Após confirmar a senha, o usuário não será solicitado a confirmá-la novamente por três horas. No entanto, você pode configurar o período de tempo antes de o usuário ser solicitado novamente a fornecer a senha alterando o valor da configuração `password_timeout` dentro do arquivo de configuração `config/auth.php` da sua aplicação.

<a id="password-confirmation-routing"></a>
### Roteamento

<a id="the-password-confirmation-form"></a>
#### O Formulário de Confirmação de Senha

Primeiro, definiremos uma rota para exibir uma view que solicita ao usuário que confirme a senha:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

Como você pode esperar, a view retornada por essa rota deve ter um formulário contendo um campo `password`. Além disso, sinta-se à vontade para incluir um texto na view que explique que o usuário está entrando em uma área protegida da aplicação e deve confirmar a senha.

<a id="confirming-the-password"></a>
#### Confirmando a Senha

Em seguida, definiremos uma rota que lidará com a requisição do formulário da view "confirm password". Essa rota será responsável por validar a senha e redirecionar o usuário para o destino pretendido:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

Antes de prosseguir, vamos examinar essa rota com mais detalhes. Primeiro, o campo `password` da requisição é verificado para determinar se realmente corresponde à senha do usuário autenticado. Se a senha for válida, precisamos informar à sessão do Laravel que o usuário confirmou a senha. O método `passwordConfirmed` definirá um timestamp na sessão do usuário que o Laravel pode usar para determinar quando o usuário confirmou a senha pela última vez. Por fim, podemos redirecionar o usuário para o destino pretendido.

<a id="password-confirmation-protecting-routes"></a>
### Protegendo Rotas

Você deve garantir que qualquer rota que realize uma ação que exija confirmação de senha recente receba o middleware `password.confirm`. Esse middleware está incluído na instalação padrão do Laravel e armazenará automaticamente o destino pretendido do usuário na sessão, de modo que o usuário possa ser redirecionado para esse local após confirmar a senha. Após armazenar o destino pretendido do usuário na sessão, o middleware redirecionará o usuário para a [named route](../routing/#named-routes) `password.confirm`:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a id="adding-custom-guards"></a>
## Adicionando Guards Personalizados

Você pode definir seus próprios guards de autenticação usando o método `extend` na facade `Auth`. Você deve colocar sua chamada ao método `extend` dentro de um [service provider](../providers/). Como o Laravel já vem com um `AppServiceProvider`, podemos colocar o código nesse provider:

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

Como você pode ver no exemplo acima, o callback passado ao método `extend` deve retornar uma implementação de `Illuminate\Contracts\Auth\Guard`. Essa interface contém alguns métodos que você precisará implementar para definir um guard personalizado. Depois que o seu guard personalizado tiver sido definido, você pode referenciar o guard na configuração `guards` do seu arquivo de configuração `auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a id="closure-request-guards"></a>
### Guards de Requisição Baseados em Closure

A forma mais simples de implementar um sistema de autenticação personalizado baseado em requisições HTTP é usando o método `Auth::viaRequest`. Esse método permite definir rapidamente seu processo de autenticação usando uma única closure.

Para começar, chame o método `Auth::viaRequest` dentro do método `boot` do `AppServiceProvider` da sua aplicação. O método `viaRequest` aceita um nome de driver de autenticação como seu primeiro argumento. Esse nome pode ser qualquer string que descreva seu guard personalizado. O segundo argumento passado ao método deve ser uma closure que recebe a requisição HTTP recebida e retorna uma instância de usuário ou, se a autenticação falhar, `null`:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

Depois que o seu driver de autenticação personalizado tiver sido definido, você pode configurá-lo como um driver dentro da configuração `guards` do seu arquivo de configuração `auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

Por fim, você pode referenciar o guard ao atribuir o middleware de autenticação a uma rota:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a id="adding-custom-user-providers"></a>
## Adicionando User Providers Personalizados

Se você não estiver usando um banco de dados relacional tradicional para armazenar seus usuários, precisará estender o Laravel com seu próprio user provider de autenticação. Usaremos o método `provider` na facade `Auth` para definir um user provider personalizado. O resolver do user provider deve retornar uma implementação de `Illuminate\Contracts\Auth\UserProvider`:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

Depois de registrar o provider usando o método `provider`, você pode mudar para o novo user provider no seu arquivo de configuração `auth.php`. Primeiro, defina um `provider` que use seu novo driver:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

Por fim, você pode referenciar esse provider na sua configuração `guards`:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a id="the-user-provider-contract"></a>
### O Contract User Provider

As implementações de `Illuminate\Contracts\Auth\UserProvider` são responsáveis por buscar uma implementação de `Illuminate\Contracts\Auth\Authenticatable` a partir de um sistema de armazenamento persistente, como MySQL, MongoDB, etc. Essas duas interfaces permitem que os mecanismos de autenticação do Laravel continuem funcionando independentemente de como os dados do usuário são armazenados ou de que tipo de classe é usada para representar o usuário autenticado:

Vamos dar uma olhada no contract `Illuminate\Contracts\Auth\UserProvider`:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

A função `retrieveById` normalmente recebe uma chave que representa o usuário, como um ID de auto-incremento de um banco de dados MySQL. A implementação de `Authenticatable` correspondente ao ID deve ser recuperada e retornada pelo método.

A função `retrieveByToken` recupera um usuário por seu `$identifier` único e seu `$token` "remember me", normalmente armazenado em uma coluna do banco de dados como `remember_token`. Assim como no método anterior, a implementação de `Authenticatable` com um valor de token correspondente deve ser retornada por esse método.

O método `updateRememberToken` atualiza o `remember_token` da instância `$user` com o novo `$token`. Um token novo é atribuído aos usuários em uma tentativa de autenticação "remember me" bem-sucedida ou quando o usuário está fazendo logout.

O método `retrieveByCredentials` recebe o array de credenciais passado ao método `Auth::attempt` ao tentar autenticar em uma aplicação. O método deve então "consultar" o armazenamento persistente subjacente em busca do usuário que corresponde a essas credenciais. Normalmente, esse método executará uma query com uma condição "where" que procura por um registro de usuário com um "username" que corresponda ao valor de `$credentials['username']`. O método deve retornar uma implementação de `Authenticatable`. **Esse método não deve tentar realizar qualquer validação de senha ou autenticação.**

O método `validateCredentials` deve comparar o `$user` fornecido com as `$credentials` para autenticar o usuário. Por exemplo, esse método normalmente usará o método `Hash::check` para comparar o valor de `$user->getAuthPassword()` com o valor de `$credentials['password']`. Esse método deve retornar `true` ou `false` indicando se a senha é válida.

O método `rehashPasswordIfRequired` deve refazer o hash da senha do `$user` fornecido, se necessário e suportado. Por exemplo, esse método normalmente usará o método `Hash::needsRehash` para determinar se o valor de `$credentials['password']` precisa ter o hash refeito. Se a senha precisar ter o hash refeito, o método deve usar o método `Hash::make` para refazer o hash da senha e atualizar o registro do usuário no armazenamento persistente subjacente.

<a id="the-authenticatable-contract"></a>
### O Contract Authenticatable

Agora que exploramos cada um dos métodos no `UserProvider`, vamos dar uma olhada no contract `Authenticatable`. Lembre-se, os user providers devem retornar implementações dessa interface a partir dos métodos `retrieveById`, `retrieveByToken` e `retrieveByCredentials`:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

Essa interface é simples. O método `getAuthIdentifierName` deve retornar o nome da coluna "primary key" do usuário e o método `getAuthIdentifier` deve retornar a "primary key" do usuário. Ao usar um back-end MySQL, isso provavelmente seria a primary key de auto-incremento atribuída ao registro do usuário. O método `getAuthPasswordName` deve retornar o nome da coluna de senha do usuário. O método `getAuthPassword` deve retornar a senha com hash do usuário.

Essa interface permite que o sistema de autenticação funcione com qualquer classe de "usuário", independentemente de qual ORM ou camada de abstração de armazenamento você esteja usando. Por padrão, o Laravel inclui uma classe `App\Models\User` no diretório `app/Models` que implementa essa interface.

<a id="automatic-password-rehashing"></a>
## Re-hashing Automático de Senhas

O algoritmo de hashing de senha padrão do Laravel é o bcrypt. O "work factor" para hashes bcrypt pode ser ajustado por meio do arquivo de configuração `config/hashing.php` da sua aplicação ou da variável de ambiente `BCRYPT_ROUNDS`.

Normalmente, o work factor do bcrypt deve ser aumentado ao longo do tempo à medida que o poder de processamento de CPU / GPU aumenta. Se você aumentar o work factor do bcrypt para a sua aplicação, o Laravel refará o hash das senhas dos usuários de forma elegante e automática à medida que os usuários se autenticam na sua aplicação por meio dos starter kits do Laravel ou quando você [autentica usuários manualmente](#authenticating-users) por meio do método `attempt`.

Normalmente, o re-hashing automático de senhas não deve interromper a sua aplicação; no entanto, você pode desativar esse comportamento publicando o arquivo de configuração `hashing`:

```shell
php artisan config:publish hashing
```

Depois que o arquivo de configuração tiver sido publicado, você pode definir o valor de configuração `rehash_on_login` como `false`:

```php
'rehash_on_login' => false,
```

<a id="events"></a>
## Eventos

O Laravel dispara uma variedade de [eventos](../events/) durante o processo de autenticação. Você pode [definir listeners](../events/) para qualquer um dos seguintes eventos:

<div class="overflow-auto">

| Nome do Evento                                 |
| ---------------------------------------------- |
| `Illuminate\Auth\Events\Registered`            |
| `Illuminate\Auth\Events\Attempting`            |
| `Illuminate\Auth\Events\Authenticated`         |
| `Illuminate\Auth\Events\Login`                 |
| `Illuminate\Auth\Events\Failed`                |
| `Illuminate\Auth\Events\Validated`             |
| `Illuminate\Auth\Events\Verified`              |
| `Illuminate\Auth\Events\Logout`                |
| `Illuminate\Auth\Events\CurrentDeviceLogout`   |
| `Illuminate\Auth\Events\OtherDeviceLogout`     |
| `Illuminate\Auth\Events\Lockout`               |
| `Illuminate\Auth\Events\PasswordReset`         |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>
