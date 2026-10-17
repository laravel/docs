---
title: "Verificação de E-mail"
---

- [Introdução](#introduction)
    - [Preparação do Model](#model-preparation)
    - [Preparação do Banco de Dados](#database-preparation)
- [Rotas](#verification-routing)
    - [O Aviso de Verificação de E-mail](#the-email-verification-notice)
    - [O Handler de Verificação de E-mail](#the-email-verification-handler)
    - [Reenviando o E-mail de Verificação](#resending-the-verification-email)
    - [Protegendo Rotas](#protecting-routes)
- [Personalização](#customization)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

Muitas aplicações web exigem que os usuários verifiquem seus endereços de e-mail antes de usar a aplicação. Em vez de forçá-lo a reimplementar esse recurso manualmente para cada aplicação que você cria, o Laravel fornece serviços integrados convenientes para enviar e verificar solicitações de verificação de e-mail.

> **Nota:**
> Quer começar rápido? Instale um dos [Laravel application starter kits](/en/starter-kits/) em uma nova aplicação Laravel. Os starter kits cuidarão de toda a estruturação do seu sistema de autenticação, incluindo o suporte à verificação de e-mail.

<a id="model-preparation"></a>
### Preparação do Model

Antes de começar, verifique se o seu model `App\Models\User` implementa o contrato `Illuminate\Contracts\Auth\MustVerifyEmail`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}
```

Uma vez que essa interface tenha sido adicionada ao seu model, os usuários recém-registrados receberão automaticamente um e-mail contendo um link de verificação de e-mail. Isso acontece de forma transparente porque o Laravel registra automaticamente o [listener](/en/events/) `Illuminate\Auth\Listeners\SendEmailVerificationNotification` para o evento `Illuminate\Auth\Events\Registered`.

Se você estiver implementando manualmente o registro na sua aplicação em vez de usar [um starter kit](/en/starter-kits/), você deve garantir que está disparando o evento `Illuminate\Auth\Events\Registered` após o registro de um usuário ser bem-sucedido:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a id="database-preparation"></a>
### Preparação do Banco de Dados

Em seguida, a sua tabela `users` deve conter uma coluna `email_verified_at` para armazenar a data e a hora em que o endereço de e-mail do usuário foi verificado. Normalmente, isso está incluído na migration de banco de dados `0001_01_01_000000_create_users_table.php` padrão do Laravel.

<a id="verification-routing"></a>
## Rotas

Para implementar corretamente a verificação de e-mail, três rotas precisarão ser definidas. Primeiro, será necessária uma rota para exibir um aviso ao usuário de que ele deve clicar no link de verificação de e-mail no e-mail de verificação que o Laravel enviou após o registro.

Segundo, será necessária uma rota para lidar com as requisições geradas quando o usuário clica no link de verificação de e-mail no e-mail.

Terceiro, será necessária uma rota para reenviar um link de verificação caso o usuário acidentalmente perca o primeiro link de verificação.

<a id="the-email-verification-notice"></a>
### O Aviso de Verificação de E-mail

Como mencionado anteriormente, deve ser definida uma rota que retornará uma view instruindo o usuário a clicar no link de verificação de e-mail que lhe foi enviado por e-mail pelo Laravel após o registro. Essa view será exibida aos usuários quando eles tentarem acessar outras partes da aplicação sem antes verificar seu endereço de e-mail. Lembre-se, o link é enviado automaticamente por e-mail ao usuário desde que o seu model `App\Models\User` implemente a interface `MustVerifyEmail`:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

A rota que retorna o aviso de verificação de e-mail deve ser nomeada `verification.notice`. É importante que a rota receba exatamente esse nome, já que o middleware `verified` [incluído no Laravel](#protecting-routes) redirecionará automaticamente para esse nome de rota se um usuário não tiver verificado seu endereço de e-mail.

> **Nota:**
> Ao implementar manualmente a verificação de e-mail, você é obrigado a definir o conteúdo da view de aviso de verificação por conta própria. Se você quiser uma estruturação que inclua todas as views necessárias de autenticação e verificação, confira os [Laravel application starter kits](/en/starter-kits/).

<a id="the-email-verification-handler"></a>
### O Handler de Verificação de E-mail

Em seguida, precisamos definir uma rota que lidará com as requisições geradas quando o usuário clica no link de verificação de e-mail que lhe foi enviado por e-mail. Essa rota deve ser nomeada `verification.verify` e receber os middlewares `auth` e `signed`:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

Antes de prosseguir, vamos dar uma olhada mais atenta nessa rota. Primeiro, você notará que estamos usando um tipo de requisição `EmailVerificationRequest` em vez da típica instância `Illuminate\Http\Request`. O `EmailVerificationRequest` é um [form request](/en/validation/#form-request-validation) que está incluído no Laravel. Essa requisição cuidará automaticamente de validar os parâmetros `id` e `hash` da requisição.

Em seguida, podemos prosseguir diretamente para a chamada do método `fulfill` na requisição. Esse método chamará o método `markEmailAsVerified` no usuário autenticado e disparará o evento `Illuminate\Auth\Events\Verified`. O método `markEmailAsVerified` está disponível para o model `App\Models\User` padrão por meio da classe base `Illuminate\Foundation\Auth\User`. Uma vez que o endereço de e-mail do usuário tenha sido verificado, você pode redirecioná-lo para onde desejar.

<a id="resending-the-verification-email"></a>
### Reenviando o E-mail de Verificação

Às vezes, um usuário pode perder ou excluir acidentalmente o e-mail de verificação de endereço de e-mail. Para acomodar isso, você pode querer definir uma rota para permitir que o usuário solicite que o e-mail de verificação seja reenviado. Você pode então fazer uma requisição a essa rota colocando um simples botão de envio de formulário dentro da sua [view de aviso de verificação](#the-email-verification-notice):

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a id="protecting-routes"></a>
### Protegendo Rotas

[Middleware de rota](/en/middleware/) pode ser usado para permitir que apenas usuários verificados acessem uma determinada rota. O Laravel inclui um [alias de middleware](/en/middleware/#middleware-aliases) `verified`, que é um alias para a classe de middleware `Illuminate\Auth\Middleware\EnsureEmailIsVerified`. Como esse alias já é registrado automaticamente pelo Laravel, tudo o que você precisa fazer é anexar o middleware `verified` a uma definição de rota. Normalmente, esse middleware é combinado com o middleware `auth`:

```php
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);
```

Se um usuário não verificado tentar acessar uma rota que recebeu esse middleware, ele será automaticamente redirecionado para a [rota nomeada](/en/routing/#named-routes) `verification.notice`.

<a id="customization"></a>
## Personalização

<a id="verification-email-customization"></a>
#### Personalização do E-mail de Verificação

Embora a notificação de verificação de e-mail padrão deva satisfazer os requisitos da maioria das aplicações, o Laravel permite que você personalize como a mensagem de e-mail de verificação de e-mail é construída.

Para começar, passe uma closure para o método `toMailUsing` fornecido pela notificação `Illuminate\Auth\Notifications\VerifyEmail`. A closure receberá a instância do model notificável que está recebendo a notificação, bem como a URL de verificação de e-mail assinada que o usuário deve visitar para verificar seu endereço de e-mail. A closure deve retornar uma instância de `Illuminate\Notifications\Messages\MailMessage`. Normalmente, você deve chamar o método `toMailUsing` a partir do método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> **Nota:**
> Para saber mais sobre notificações por e-mail, consulte a [documentação de notificações por e-mail](/en/notifications/#mail-notifications).

<a id="events"></a>
## Eventos

Ao usar os [Laravel application starter kits](/en/starter-kits/), o Laravel dispara um [evento](/en/events/) `Illuminate\Auth\Events\Verified` durante o processo de verificação de e-mail. Se você estiver lidando manualmente com a verificação de e-mail para a sua aplicação, pode querer disparar manualmente esses eventos após a verificação ser concluída.