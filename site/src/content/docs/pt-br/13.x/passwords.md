---
title: "Redefinindo Senhas"
---

- [Introdução](#introduction)
    - [Configuração](#configuration)
    - [Pré-requisitos do Driver](#driver-prerequisites)
    - [Preparação do Model](#model-preparation)
    - [Configurando Hosts Confiáveis](#configuring-trusted-hosts)
- [Rotas](#routing)
    - [Solicitando o Link de Redefinição de Senha](#requesting-the-password-reset-link)
    - [Redefinindo a Senha](#resetting-the-password)
- [Excluindo Tokens Expirados](#deleting-expired-tokens)
- [Personalização](#password-customization)

<a id="introduction"></a>
## Introdução

A maioria das aplicações web oferece uma maneira de os usuários redefinirem suas senhas esquecidas. Em vez de forçá-lo a reimplementar isso manualmente para cada aplicação que você cria, o Laravel fornece serviços convenientes para enviar links de redefinição de senha e redefinir senhas com segurança.

> **Nota:**
> Quer começar rápido? Instale um [application starter kit](/en/starter-kits/) do Laravel em uma nova aplicação Laravel. Os starter kits do Laravel cuidarão de toda a estruturação do seu sistema de autenticação, incluindo a redefinição de senhas esquecidas.

<a id="configuration"></a>
### Configuração

O arquivo de configuração de redefinição de senha da sua aplicação é armazenado em `config/auth.php`. Certifique-se de revisar as opções disponíveis nesse arquivo. Por padrão, o Laravel é configurado para usar o driver de redefinição de senha `database`.

A opção de configuração `driver` de redefinição de senha define onde os dados de redefinição de senha serão armazenados. O Laravel inclui dois drivers:

<div class="content-list" markdown="1">

- `database` - os dados de redefinição de senha são armazenados em um banco de dados relacional.
- `cache` - os dados de redefinição de senha são armazenados em um dos seus stores baseados em cache.

</div>

<a id="driver-prerequisites"></a>
### Pré-requisitos do Driver

<a id="database"></a>
#### Database

Ao usar o driver `database` padrão, uma tabela deve ser criada para armazenar os tokens de redefinição de senha da sua aplicação. Normalmente, isso está incluído na migration de banco de dados `0001_01_01_000000_create_users_table.php` padrão do Laravel.

<a id="cache"></a>
#### Cache

Há também um driver de cache disponível para lidar com redefinições de senha, que não requer uma tabela de banco de dados dedicada. As entradas são indexadas por um hash SHA-256 do endereço de e-mail do usuário:

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // Optional...
        'expire' => 60,
        'throttle' => 60,
    ],
],
```

Para evitar que uma chamada a `artisan cache:clear` limpe os dados de redefinição de senha, você pode opcionalmente especificar um cache store separado com a chave de configuração `store`. O valor deve corresponder a um store configurado no seu valor de configuração `config/cache.php`.

<a id="model-preparation"></a>
### Preparação do Model

Antes de usar os recursos de redefinição de senha do Laravel, o model `App\Models\User` da sua aplicação deve usar a trait `Illuminate\Notifications\Notifiable`. Normalmente, essa trait já está incluída no model `App\Models\User` padrão que é criado com novas aplicações Laravel.

Em seguida, verifique se o seu model `App\Models\User` implementa o contrato `Illuminate\Contracts\Auth\CanResetPassword`. O model `App\Models\User` incluído no framework já implementa essa interface e usa a trait `Illuminate\Auth\Passwords\CanResetPassword` para incluir os métodos necessários para implementar a interface.

<a id="configuring-trusted-hosts"></a>
### Configurando Hosts Confiáveis

Por padrão, o Laravel responderá a todas as requisições que receber, independentemente do conteúdo do cabeçalho `Host` da requisição HTTP. Além disso, o valor do cabeçalho `Host` será usado ao gerar URLs absolutas para a sua aplicação durante uma requisição web.

Normalmente, você deve configurar seu servidor web, como Nginx ou Apache, para enviar à sua aplicação apenas as requisições que correspondem a um determinado hostname. No entanto, se você não tiver a capacidade de personalizar seu servidor web diretamente e precisar instruir o Laravel a responder apenas a certos hostnames, você pode fazer isso usando o método de middleware `trustHosts` no arquivo `bootstrap/app.php` da sua aplicação. Isso é particularmente importante quando sua aplicação oferece funcionalidade de redefinição de senha.

Para saber mais sobre esse método de middleware, consulte a [documentação do middleware TrustHosts](/en/requests/#configuring-trusted-hosts).

<a id="routing"></a>
## Rotas

Para implementar corretamente o suporte para permitir que os usuários redefinam suas senhas, precisaremos definir várias rotas. Primeiro, precisaremos de um par de rotas para lidar com a permissão de o usuário solicitar um link de redefinição de senha por meio do seu endereço de e-mail. Segundo, precisaremos de um par de rotas para lidar com a redefinição da senha propriamente dita, uma vez que o usuário visita o link de redefinição de senha que lhe foi enviado por e-mail e preenche o formulário de redefinição de senha.

<a id="requesting-the-password-reset-link"></a>
### Solicitando o Link de Redefinição de Senha

<a id="the-password-reset-link-request-form"></a>
#### O Formulário de Solicitação do Link de Redefinição de Senha

Primeiro, definiremos as rotas necessárias para solicitar os links de redefinição de senha. Para começar, definiremos uma rota que retorna uma view com o formulário de solicitação do link de redefinição de senha:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

A view retornada por essa rota deve ter um formulário contendo um campo `email`, que permitirá ao usuário solicitar um link de redefinição de senha para um determinado endereço de e-mail.

<a id="password-reset-link-handling-the-form-submission"></a>
#### Lidando com o Envio do Formulário

Em seguida, definiremos uma rota que lida com a requisição de envio do formulário da view "forgot password". Essa rota será responsável por validar o endereço de e-mail e enviar a solicitação de redefinição de senha para o usuário correspondente:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::ResetLinkSent
        ? back()->with(['status' => __($status)])
        : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');
```

Antes de prosseguir, vamos examinar essa rota em mais detalhes. Primeiro, o atributo `email` da requisição é validado. Em seguida, usaremos o "password broker" integrado do Laravel (por meio da facade `Password`) para enviar um link de redefinição de senha ao usuário. O password broker cuidará de recuperar o usuário pelo campo fornecido (nesse caso, o endereço de e-mail) e enviar ao usuário um link de redefinição de senha por meio do [sistema de notificações](/en/notifications/) integrado do Laravel.

O método `sendResetLink` retorna um "status" (slug). Esse status pode ser traduzido usando os helpers de [localização](/en/localization/) do Laravel para exibir uma mensagem amigável ao usuário sobre o status da sua solicitação. A tradução do status de redefinição de senha é determinada pelo arquivo de idioma `lang/{lang}/passwords.php` da sua aplicação. Uma entrada para cada valor possível do slug de status está localizada dentro do arquivo de idioma `passwords`.

> **Nota:**
> Por padrão, o esqueleto da aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los por meio do comando Artisan `lang:publish`.

Você pode estar se perguntando como o Laravel sabe recuperar o registro do usuário do banco de dados da sua aplicação ao chamar o método `sendResetLink` da facade `Password`. O password broker do Laravel utiliza os "user providers" do seu sistema de autenticação para recuperar registros do banco de dados. O user provider usado pelo password broker é configurado dentro do array de configuração `passwords` do seu arquivo de configuração `config/auth.php`. Para saber mais sobre a escrita de user providers personalizados, consulte a [documentação de autenticação](/en/authentication/#adding-custom-user-providers).

> **Nota:**
> Ao implementar manualmente as redefinições de senha, você é obrigado a definir o conteúdo das views e rotas por conta própria. Se você quiser uma estruturação que inclua toda a lógica necessária de autenticação e verificação, confira os [Laravel application starter kits](/en/starter-kits/).

<a id="resetting-the-password"></a>
### Redefinindo a Senha

<a id="the-password-reset-form"></a>
#### O Formulário de Redefinição de Senha

Em seguida, definiremos as rotas necessárias para efetivamente redefinir a senha, uma vez que o usuário clica no link de redefinição de senha que lhe foi enviado por e-mail e fornece uma nova senha. Primeiro, vamos definir a rota que exibirá o formulário de redefinição de senha que é mostrado quando o usuário clica no link de redefinição de senha. Essa rota receberá um parâmetro `token` que usaremos mais tarde para verificar a solicitação de redefinição de senha:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

A view retornada por essa rota deve exibir um formulário contendo um campo `email`, um campo `password`, um campo `password_confirmation` e um campo oculto `token`, que deve conter o valor do `$token` secreto recebido pela nossa rota.

<a id="password-reset-handling-the-form-submission"></a>
#### Lidando com o Envio do Formulário

Naturalmente, precisamos definir uma rota para efetivamente lidar com o envio do formulário de redefinição de senha. Essa rota será responsável por validar a requisição recebida e atualizar a senha do usuário no banco de dados:

```php
use App\Models\User;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

Route::post('/reset-password', function (Request $request) {
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8|confirmed',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'password_confirmation', 'token'),
        function (User $user, string $password) {
            $user->forceFill([
                'password' => Hash::make($password)
            ])->setRememberToken(Str::random(60));

            $user->save();

            event(new PasswordReset($user));
        }
    );

    return $status === Password::PasswordReset
        ? redirect()->route('login')->with('status', __($status))
        : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');
```

Antes de prosseguir, vamos examinar essa rota em mais detalhes. Primeiro, os atributos `token`, `email` e `password` da requisição são validados. Em seguida, usaremos o "password broker" integrado do Laravel (por meio da facade `Password`) para validar as credenciais da solicitação de redefinição de senha.

Se o token, o endereço de e-mail e a senha fornecidos ao password broker forem válidos, a closure passada ao método `reset` será invocada. Dentro dessa closure, que recebe a instância do usuário e a senha em texto puro fornecida ao formulário de redefinição de senha, podemos atualizar a senha do usuário no banco de dados.

O método `reset` retorna um "status" (slug). Esse status pode ser traduzido usando os helpers de [localização](/en/localization/) do Laravel para exibir uma mensagem amigável ao usuário sobre o status da sua solicitação. A tradução do status de redefinição de senha é determinada pelo arquivo de idioma `lang/{lang}/passwords.php` da sua aplicação. Uma entrada para cada valor possível do slug de status está localizada dentro do arquivo de idioma `passwords`. Se a sua aplicação não contiver um diretório `lang`, você pode criá-lo usando o comando Artisan `lang:publish`.

Antes de prosseguir, você pode estar se perguntando como o Laravel sabe recuperar o registro do usuário do banco de dados da sua aplicação ao chamar o método `reset` da facade `Password`. O password broker do Laravel utiliza os "user providers" do seu sistema de autenticação para recuperar registros do banco de dados. O user provider usado pelo password broker é configurado dentro do array de configuração `passwords` do seu arquivo de configuração `config/auth.php`. Para saber mais sobre a escrita de user providers personalizados, consulte a [documentação de autenticação](/en/authentication/#adding-custom-user-providers).

<a id="deleting-expired-tokens"></a>
## Excluindo Tokens Expirados

Se você estiver usando o driver `database`, os tokens de redefinição de senha que expiraram ainda estarão presentes no seu banco de dados. No entanto, você pode excluir facilmente esses registros usando o comando Artisan `auth:clear-resets`:

```shell
php artisan auth:clear-resets
```

Se você quiser automatizar esse processo, considere adicionar o comando ao [scheduler](/en/scheduling/) da sua aplicação:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a id="password-customization"></a>
## Personalização

<a id="reset-link-customization"></a>
#### Personalização do Link de Redefinição

Você pode personalizar a URL do link de redefinição de senha usando o método `createUrlUsing` fornecido pela classe de notificação `ResetPassword`. Esse método aceita uma closure que recebe a instância do usuário que está recebendo a notificação, bem como o token do link de redefinição de senha. Normalmente, você deve chamar esse método a partir do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    ResetPassword::createUrlUsing(function (User $user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a id="reset-email-customization"></a>
#### Personalização do E-mail de Redefinição

Você pode modificar facilmente a classe de notificação usada para enviar o link de redefinição de senha ao usuário. Para começar, sobrescreva o método `sendPasswordResetNotification` no seu model `App\Models\User`. Dentro desse método, você pode enviar a notificação usando qualquer [classe de notificação](/en/notifications/) de sua própria criação. O `$token` de redefinição de senha é o primeiro argumento recebido pelo método. Você pode usar esse `$token` para construir a URL de redefinição de senha de sua escolha e enviar sua notificação ao usuário:

```php
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```