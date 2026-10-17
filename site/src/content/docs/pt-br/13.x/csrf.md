---
title: "Proteção CSRF"
---

- [Introdução](#csrf-introduction)
- [Prevenindo Requisições CSRF](#preventing-csrf-requests)
    - [Verificação de Origem](#origin-verification)
    - [Excluindo URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a id="csrf-introduction"></a>
## Introdução

Cross-site request forgeries (falsificação de requisição entre sites) são um tipo de exploração maliciosa na qual comandos não autorizados são executados em nome de um usuário autenticado. Felizmente, o Laravel torna fácil proteger sua aplicação contra ataques de [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF).

<a id="csrf-explanation"></a>
#### Uma Explicação da Vulnerabilidade

Caso você não esteja familiarizado com cross-site request forgeries, vamos discutir um exemplo de como essa vulnerabilidade pode ser explorada. Imagine que sua aplicação tem uma rota `/user/email` que aceita uma requisição `POST` para mudar o endereço de email do usuário autenticado. Muito provavelmente, esta rota espera que um campo de input `email` contenha o endereço de email que o usuário gostaria de começar a usar.

Sem proteção CSRF, um site malicioso poderia criar um formulário HTML que aponta para a rota `/user/email` da sua aplicação e submete o próprio endereço de email do usuário malicioso:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

Se o site malicioso submete automaticamente o formulário quando a página é carregada, o usuário malicioso apenas precisa atrair um usuário desprevenido da sua aplicação para visitar seu site e o endereço de email será alterado na sua aplicação.

Para prevenir essa vulnerabilidade, precisamos inspecionar cada requisição `POST`, `PUT`, `PATCH`, `DELETE` ou `QUERY` recebida em busca de um valor secreto de sessão que a aplicação maliciosa é incapaz de acessar.

<a id="preventing-csrf-requests"></a>
## Prevenindo Requisições CSRF

O [middleware](../middleware/) `Illuminate\Foundation\Http\Middleware\PreventRequestForgery`, que está incluído no grupo de middleware `web` por padrão, protege sua aplicação contra falsificações de requisição entre sites usando uma abordagem de duas camadas.

Primeiro, o middleware verifica o header `Sec-Fetch-Site` do navegador. Navegadores modernos definem automaticamente este header em cada requisição, indicando se ela se originou da mesma origem, do mesmo site ou de uma fonte cross-site. Se o header indicar que a requisição veio da mesma origem, a requisição é permitida imediatamente sem qualquer verificação de token.

Se a verificação de origem não passar — por exemplo, porque a requisição vem de um navegador mais antigo que não envia o header `Sec-Fetch-Site` ou porque a conexão não é segura — o middleware volta à validação tradicional de token CSRF.

O Laravel gera automaticamente um "token" CSRF para cada [sessão de usuário](../session/) ativa gerenciada pela aplicação. Este token é usado para verificar que o usuário autenticado é a pessoa que realmente está fazendo as requisições à aplicação. Como este token é armazenado na sessão do usuário e muda cada vez que a sessão é regenerada, uma aplicação maliciosa é incapaz de acessá-lo.

O token CSRF da sessão atual pode ser acessado via a sessão da requisição ou via a função auxiliar `csrf_token`:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

Sempre que você definir um formulário HTML "POST", "PUT", "PATCH" ou "DELETE" na sua aplicação, você deve incluir um campo oculto CSRF `_token` no formulário para que o middleware de proteção CSRF possa validar a requisição. Para conveniência, você pode usar a diretiva Blade `@csrf` para gerar o campo oculto de input do token:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a id="csrf-tokens-and-spas"></a>
#### Tokens CSRF e SPAs

Se você está construindo uma SPA que utiliza o Laravel como backend de API, você deve consultar a [documentação do Laravel Sanctum](../sanctum/) para informações sobre autenticação com sua API e proteção contra vulnerabilidades CSRF.

<a id="origin-verification"></a>
### Verificação de Origem

Como discutido acima, o middleware de falsificação de requisição do Laravel primeiro verifica o header `Sec-Fetch-Site` para determinar se a requisição é da mesma origem. Por padrão, se esta verificação não passar, o middleware volta à validação de token CSRF.

No entanto, se você gostaria de confiar apenas na verificação de origem e desabilitar completamente o fallback de token CSRF, você pode fazer isso usando o método `preventRequestForgery` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

Ao usar o modo apenas origem, requisições que falharem na verificação de origem receberão uma resposta HTTP `403` em vez da resposta `419` tipicamente associada a incompatibilidades de token CSRF.

> **Aviso:**
> O header `Sec-Fetch-Site` é enviado apenas por navegadores sobre conexões seguras (HTTPS). Se sua aplicação não for servida sobre HTTPS, a verificação de origem não estará disponível e o middleware voltará à validação de token CSRF.

Se sua aplicação precisa aceitar requisições de subdomínios (por exemplo, `dashboard.example.com` aceitando requisições de `example.com`), você pode permitir requisições same-site além de requisições same-origin:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a id="csrf-excluding-uris"></a>
### Excluindo URIs da Proteção CSRF

Às vezes, você pode desejar excluir um conjunto de URIs da proteção CSRF. Por exemplo, se você está usando [Stripe](https://stripe.com) para processar pagamentos e está utilizando o sistema de webhook deles, você precisará excluir a rota do handler de webhook do Stripe da proteção CSRF, já que o Stripe não saberá qual token CSRF enviar para suas rotas.

Tipicamente, você deve colocar esses tipos de rotas fora do grupo de middleware `web` que o Laravel aplica a todas as rotas no arquivo `routes/web.php`. No entanto, você também pode excluir rotas específicas fornecendo suas URIs ao método `preventRequestForgery` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> **Nota:**
> Para conveniência, o middleware CSRF é automaticamente desabilitado para todas as rotas ao [executar testes](../testing/).

<a id="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

Além de verificar o token CSRF como um parâmetro POST, o middleware `PreventRequestForgery` também verificará o header de requisição `X-CSRF-TOKEN`. Você poderia, por exemplo, armazenar o token em uma tag `meta` HTML:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

Então, você pode instruir uma biblioteca como jQuery a adicionar automaticamente o token a todos os headers de requisição. Isso fornece proteção CSRF simples e conveniente para suas aplicações baseadas em AJAX usando tecnologia JavaScript legada:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a id="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

O Laravel armazena o token CSRF atual em um cookie criptografado `XSRF-TOKEN` que é incluído com cada resposta gerada pelo framework. Você pode usar o valor do cookie para definir o header de requisição `X-XSRF-TOKEN`.

Este cookie é enviado principalmente como uma conveniência para o desenvolvedor, já que alguns frameworks e bibliotecas JavaScript, como Angular e Axios, colocam automaticamente seu valor no header `X-XSRF-TOKEN` em requisições same-origin.