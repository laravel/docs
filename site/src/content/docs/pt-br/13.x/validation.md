---
title: "Validação"
---

- [Introdução](#introduction)
- [Início Rápido de Validação](#validation-quickstart)
    - [Definindo as Rotas](#quick-defining-the-routes)
    - [Criando o Controlador](#quick-creating-the-controller)
    - [Escrevendo a Lógica de Validação](#quick-writing-the-validation-logic)
    - [Exibindo os Erros de Validação](#quick-displaying-the-validation-errors)
    - [Repopulando Formulários](#repopulating-forms)
    - [Uma Observação Sobre Campos Opcionais](#a-note-on-optional-fields)
    - [Formato da Resposta de Erro de Validação](#validation-error-response-format)
- [Validação de Form Requests](#form-request-validation)
    - [Criando Form Requests](#creating-form-requests)
    - [Autorizando Form Requests](#authorizing-form-requests)
    - [Personalizando as Mensagens de Erro](#customizing-the-error-messages)
    - [Preparando a Entrada para Validação](#preparing-input-for-validation)
- [Criando Validadores Manualmente](#manually-creating-validators)
    - [Redirecionamento Automático](#automatic-redirection)
    - [Bags de Erros Nomeados](#named-error-bags)
    - [Personalizando as Mensagens de Erro](#manual-customizing-the-error-messages)
    - [Realizando Validação Adicional](#performing-additional-validation)
- [Trabalhando Com a Entrada Validada](#working-with-validated-input)
- [Trabalhando Com Mensagens de Erro](#working-with-error-messages)
    - [Especificando Mensagens Personalizadas em Arquivos de Idioma](#specifying-custom-messages-in-language-files)
    - [Especificando Atributos em Arquivos de Idioma](#specifying-attribute-in-language-files)
    - [Especificando Valores em Arquivos de Idioma](#specifying-values-in-language-files)
- [Regras de Validação Disponíveis](#available-validation-rules)
    - [Construtores de Regras](#rule-builders)
- [Adicionando Regras Condicionalmente](#conditionally-adding-rules)
- [Validando Arrays](#validating-arrays)
    - [Validando Entrada de Array Aninhado](#validating-nested-array-input)
    - [Índices e Posições nas Mensagens de Erro](#error-message-indexes-and-positions)
- [Validando Arquivos](#validating-files)
- [Validando Senhas](#validating-passwords)
- [Regras de Validação Personalizadas](#custom-validation-rules)
    - [Usando Objetos de Regra](#using-rule-objects)
    - [Usando Closures](#using-closures)
    - [Regras Implícitas](#implicit-rules)

<a id="introduction"></a>
## Introdução

O Laravel oferece várias abordagens diferentes para validar os dados recebidos pela sua aplicação. O mais comum é usar o método `validate`, disponível em todas as requisições HTTP recebidas. No entanto, também discutiremos outras abordagens de validação.

O Laravel inclui uma grande variedade de regras de validação práticas que você pode aplicar aos dados, inclusive a capacidade de validar se valores são únicos em uma determinada tabela do banco de dados. Abordaremos cada uma dessas regras de validação em detalhes para que você conheça todos os recursos de validação do Laravel.

<a id="validation-quickstart"></a>
## Início Rápido de Validação

Para conhecer os poderosos recursos de validação do Laravel, vejamos um exemplo completo de validação de um formulário e de exibição das mensagens de erro de volta ao usuário. Ao ler esta visão geral de alto nível, você terá uma boa compreensão geral de como validar os dados de requisições recebidas usando o Laravel:

<a id="quick-defining-the-routes"></a>
### Definindo as Rotas

Primeiro, vamos supor que temos as seguintes rotas definidas no nosso arquivo `routes/web.php`:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

A rota `GET` exibirá um formulário para o usuário criar uma nova postagem de blog, enquanto a rota `POST` armazenará a nova postagem de blog no banco de dados.

<a id="quick-creating-the-controller"></a>
### Criando o Controlador

Em seguida, vamos ver um controlador simples que trata as requisições recebidas para essas rotas. Por enquanto, deixaremos o método `store` vazio:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a id="quick-writing-the-validation-logic"></a>
### Escrevendo a Lógica de Validação

Agora estamos prontos para preencher nosso método `store` com a lógica para validar a nova postagem de blog. Para isso, usaremos o método `validate` fornecido pelo objeto `Illuminate\Http\Request`. Se as regras de validação passarem, seu código continuará sendo executado normalmente; porém, se a validação falhar, uma exceção `Illuminate\Validation\ValidationException` será lançada e a resposta de erro apropriada será enviada automaticamente de volta ao usuário.

Se a validação falhar durante uma requisição HTTP tradicional, será gerada uma resposta de redirecionamento para a URL anterior. Se a requisição recebida for uma requisição XHR, uma [resposta JSON contendo as mensagens de erro de validação](#validation-error-response-format) será retornada.

Para entender melhor o método `validate`, vamos voltar ao método `store`:

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```

Como você pode ver, as regras de validação são passadas para o método `validate`. Não se preocupe - todas as regras de validação disponíveis estão [documentadas](#available-validation-rules). Novamente, se a validação falhar, a resposta apropriada será gerada automaticamente. Se a validação passar, nosso controlador continuará sendo executado normalmente.

Além disso, você pode usar o método `validateWithBag` para validar uma requisição e armazenar quaisquer mensagens de erro dentro de um [bag de erros nomeado](#named-error-bags):

```php
$validated = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a id="stopping-on-first-validation-failure"></a>
#### Parando na Primeira Falha de Validação

Às vezes, você pode querer parar de executar as regras de validação de um atributo após a primeira falha de validação. Para isso, atribua a regra `bail` ao atributo:

```php
$request->validate([
    'title' => ['bail', 'required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

Neste exemplo, se a regra `unique` no atributo `title` falhar, a regra `max` não será verificada. As regras serão validadas na ordem em que forem atribuídas.

<a id="a-note-on-nested-attributes"></a>
#### Uma Observação Sobre Atributos Aninhados

Se a requisição HTTP recebida contiver dados de campos "aninhados", você pode especificar esses campos nas suas regras de validação usando a sintaxe de "ponto":

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'author.name' => ['required'],
    'author.description' => ['required'],
]);
```

Por outro lado, se o nome do seu campo contiver um ponto literal, você pode impedir explicitamente que ele seja interpretado como sintaxe de "ponto", escapando o ponto com uma barra invertida:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'v1\.0' => ['required'],
]);
```

<a id="quick-displaying-the-validation-errors"></a>
### Exibindo os Erros de Validação

E se os campos da requisição recebida não atenderem às regras de validação fornecidas? Como mencionado anteriormente, o Laravel redirecionará automaticamente o usuário de volta ao local anterior. Além disso, todos os erros de validação e a [entrada da requisição](../requests/#retrieving-old-input) serão automaticamente [armazenados na sessão (flash)](../session/#flash-data).

Uma variável `$errors` é compartilhada com todas as views da sua aplicação pelo middleware `Illuminate\View\Middleware\ShareErrorsFromSession`, fornecido pelo grupo de middleware `web`. Quando esse middleware é aplicado, a variável `$errors` sempre estará disponível nas suas views, permitindo que você presuma de forma conveniente que a variável `$errors` está sempre definida e pode ser usada com segurança. A variável `$errors` será uma instância de `Illuminate\Support\MessageBag`. Para mais informações sobre como trabalhar com esse objeto, [consulte a documentação dele](#working-with-error-messages).

Então, no nosso exemplo, o usuário será redirecionado para o método `create` do nosso controlador quando a validação falhar, permitindo que exibamos as mensagens de erro na view:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a id="quick-customizing-the-error-messages"></a>
#### Personalizando as Mensagens de Erro

Cada uma das regras de validação integradas do Laravel possui uma mensagem de erro, localizada no arquivo `lang/en/validation.php` da sua aplicação. Se a sua aplicação não tiver um diretório `lang`, você pode instruir o Laravel a criá-lo usando o comando Artisan `lang:publish`.

Dentro do arquivo `lang/en/validation.php`, você encontrará uma entrada de tradução para cada regra de validação. Você é livre para alterar ou modificar essas mensagens de acordo com as necessidades da sua aplicação.

Além disso, você pode copiar este arquivo para outro diretório de idioma para traduzir as mensagens para o idioma da sua aplicação. Para saber mais sobre a localização no Laravel, consulte a [documentação completa de localização](../localization/).

> **Aviso:**
> Por padrão, o esqueleto de aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los via o comando Artisan `lang:publish`.

<a id="quick-xhr-requests-and-validation"></a>
#### Requisições XHR e Validação

Neste exemplo, usamos um formulário tradicional para enviar dados para a aplicação. No entanto, muitas aplicações recebem requisições XHR de um frontend alimentado por JavaScript. Ao usar o método `validate` durante uma requisição XHR, o Laravel não gera uma resposta de redirecionamento. Em vez disso, o Laravel gera uma [resposta JSON contendo todos os erros de validação](#validation-error-response-format). Essa resposta JSON será enviada com o código de status HTTP 422.

<a id="the-at-error-directive"></a>
#### A Diretiva `@error`

Você pode usar a diretiva [Blade](../blade/) `@error` para determinar rapidamente se existem mensagens de erro de validação para um determinado atributo. Dentro de uma diretiva `@error`, você pode imprimir a variável `$message` para exibir a mensagem de erro:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

Se você estiver usando [bags de erros nomeados](#named-error-bags), pode passar o nome do bag de erros como segundo argumento para a diretiva `@error`:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a id="repopulating-forms"></a>
### Repopulando Formulários

Quando o Laravel gera uma resposta de redirecionamento devido a um erro de validação, o framework automaticamente [armazena na sessão (flash) toda a entrada da requisição](../session/#flash-data). Isso é feito para que você possa acessar a entrada convenientemente durante a próxima requisição e repopular o formulário que o usuário tentou enviar.

Para recuperar a entrada armazenada (flash) da requisição anterior, invoque o método `old` em uma instância de `Illuminate\Http\Request`. O método `old` buscará os dados de entrada armazenados anteriormente na [sessão](../session/):

```php
$title = $request->old('title');
```

O Laravel também fornece o helper global `old`. Se você estiver exibindo a entrada antiga dentro de um [template Blade](../blade/), é mais conveniente usar o helper `old` para repopular o formulário. Se não existir entrada antiga para o campo informado, `null` será retornado:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a id="a-note-on-optional-fields"></a>
### Uma Observação Sobre Campos Opcionais

Por padrão, o Laravel inclui os middlewares `TrimStrings` e `ConvertEmptyStringsToNull` na pilha de middlewares globais da sua aplicação. Por causa disso, você frequentemente precisará marcar seus campos de requisição "opcionais" como `nullable` se não quiser que o validador considere valores `null` como inválidos. Por exemplo:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
    'publish_at' => ['nullable', 'date'],
]);
```

Neste exemplo, estamos especificando que o campo `publish_at` pode ser `null` ou uma representação de data válida. Se o modificador `nullable` não for adicionado à definição da regra, o validador consideraria `null` uma data inválida.

<a id="validation-error-response-format"></a>
### Formato da Resposta de Erro de Validação

Quando sua aplicação lança uma exceção `Illuminate\Validation\ValidationException` e a requisição HTTP recebida espera uma resposta JSON, o Laravel formatará automaticamente as mensagens de erro para você e retornará uma resposta HTTP `422 Unprocessable Entity`.

Abaixo, você pode conferir um exemplo do formato de resposta JSON para erros de validação. Observe que as chaves de erro aninhadas são achatadas no formato de "ponto":

```json
{
    "message": "The team name field must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name field must be a string.",
            "The team name field must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email field must be a valid email address."
        ]
    }
}
```

<a id="form-request-validation"></a>
## Validação de Form Requests

<a id="creating-form-requests"></a>
### Criando Form Requests

Para cenários de validação mais complexos, você pode querer criar um "form request". Form requests são classes de requisição personalizadas que encapsulam sua própria lógica de validação e autorização. Para criar uma classe de form request, você pode usar o comando Artisan `make:request`:

```shell
php artisan make:request StorePostRequest
```

A classe de form request gerada será colocada no diretório `app/Http/Requests`. Se esse diretório não existir, ele será criado quando você executar o comando `make:request`. Cada form request gerado pelo Laravel possui dois métodos: `authorize` e `rules`.

Como você deve ter imaginado, o método `authorize` é responsável por determinar se o usuário autenticado atualmente pode executar a ação representada pela requisição, enquanto o método `rules` retorna as regras de validação que devem ser aplicadas aos dados da requisição:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ];
}
```

> **Nota:**
> Você pode fazer type-hint de quaisquer dependências necessárias na assinatura do método `rules`. Elas serão resolvidas automaticamente via o [service container](../container/) do Laravel.

Então, como as regras de validação são avaliadas? Tudo o que você precisa fazer é fazer type-hint da requisição no método do seu controlador. A form request recebida é validada antes de o método do controlador ser chamado, o que significa que você não precisa poluir seu controlador com nenhuma lógica de validação:

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```

Se a validação falhar, uma resposta de redirecionamento será gerada para enviar o usuário de volta ao local anterior. Os erros também serão armazenados na sessão (flash) para que estejam disponíveis para exibição. Se a requisição for uma requisição XHR, uma resposta HTTP com código de status 422 será retornada ao usuário, incluindo uma [representação JSON dos erros de validação](#validation-error-response-format).

> **Nota:**
> Precisa adicionar validação de form request em tempo real ao seu frontend Laravel alimentado pelo Inertia? Confira o [Laravel Precognition](../precognition/).

<a id="performing-additional-validation-on-form-requests"></a>
#### Realizando Validação Adicional

Às vezes, você precisa realizar validação adicional após a conclusão da validação inicial. Você pode fazer isso usando o método `after` da form request.

O método `after` deve retornar um array de callables ou closures que serão invocados após a conclusão da validação. Os callables fornecidos receberão uma instância de `Illuminate\Validation\Validator`, permitindo que você adicione mensagens de erro adicionais, se necessário:

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```

Como observado, o array retornado pelo método `after` também pode conter classes invocáveis. O método `__invoke` dessas classes receberá uma instância de `Illuminate\Validation\Validator`:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```

<a id="request-stopping-on-first-validation-rule-failure"></a>
#### Parando na Primeira Falha de Validação

Ao adicionar o atributo `StopOnFirstFailure` à sua classe de requisição, você pode informar ao validador que ele deve parar de validar todos os atributos assim que ocorrer uma única falha de validação:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a id="request-failing-on-unknown-fields"></a>
#### Falhando em Campos Desconhecidos

Ao adicionar o atributo `FailOnUnknownFields` à sua classe de requisição, você pode instruir o Laravel a rejeitar quaisquer campos recebidos que não sejam definidos pelas regras de validação da sua requisição:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;
use Illuminate\Foundation\Http\FormRequest;

#[FailOnUnknownFields]
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string'],
            'body' => ['required', 'string'],
        ];
    }
}
```

Você também pode habilitar esse comportamento globalmente para todas as form requests a partir do seu `AppServiceProvider`:

```php
use Illuminate\Foundation\Http\FormRequest;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    FormRequest::failOnUnknownFields();
}
```

Se necessário, você pode desabilitar esse comportamento para uma requisição específica passando `false` para o atributo:

```php
#[FailOnUnknownFields(false)]
class PublicWebhookRequest extends FormRequest
{
    // ...
}
```

Rejeitar campos desconhecidos pode oferecer proteção adicional contra problemas do tipo mass-assignment, impedindo que chaves de entrada inesperadas avancem mais profundamente na sua aplicação. No entanto, você ainda deve configurar as propriedades `$fillable` / `$guarded` do seu model e persistir apenas entradas confiáveis e validadas.

<a id="customizing-the-redirect-location"></a>
#### Personalizando o Local de Redirecionamento

Quando a validação de form request falha, uma resposta de redirecionamento será gerada para enviar o usuário de volta ao local anterior. No entanto, você é livre para personalizar esse comportamento. Para isso, você pode usar o atributo `RedirectTo` na sua form request:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectTo;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectTo('/dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

Ou, se você quiser redirecionar os usuários para uma rota nomeada, pode usar o atributo `RedirectToRoute`:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectToRoute;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectToRoute('dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a id="customizing-the-error-bag"></a>
#### Personalizando o Bag de Erros

Quando a validação de form request falha, os erros são armazenados na sessão (flash) no bag de erros `default`. Se você precisar armazenar os erros em um [bag de erros nomeado](#named-error-bags) diferente, pode usar o atributo `ErrorBag` na sua form request:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\ErrorBag;
use Illuminate\Foundation\Http\FormRequest;

#[ErrorBag('login')]
class LoginRequest extends FormRequest
{
    // ...
}
```

<a id="authorizing-form-requests"></a>
### Autorizando Form Requests

A classe de form request também contém um método `authorize`. Dentro desse método, você pode determinar se o usuário autenticado realmente tem autoridade para atualizar um determinado recurso. Por exemplo, você pode determinar se um usuário realmente é o dono de um comentário de blog que está tentando atualizar. Muito provavelmente, você interagirá com suas [gates e policies de autorização](../authorization/) dentro desse método:

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

Como todas as form requests estendem a classe base de requisição do Laravel, podemos usar o método `user` para acessar o usuário autenticado atualmente. Além disso, observe a chamada ao método `route` no exemplo acima. Esse método dá acesso aos parâmetros de URI definidos na rota chamada, como o parâmetro `{comment}` no exemplo abaixo:

```php
Route::post('/comment/{comment}');
```

Portanto, se sua aplicação estiver aproveitando o [route model binding](../routing/#route-model-binding), seu código pode ficar ainda mais conciso acessando o model resolvido como uma propriedade da requisição:

```php
return $this->user()->can('update', $this->comment);
```

Se o método `authorize` retornar `false`, uma resposta HTTP com código de status 403 será retornada automaticamente e o método do seu controlador não será executado.

Se você planeja tratar a lógica de autorização da requisição em outra parte da sua aplicação, pode remover o método `authorize` por completo ou simplesmente retornar `true`:

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> **Nota:**
> Você pode fazer type-hint de quaisquer dependências necessárias na assinatura do método `authorize`. Elas serão resolvidas automaticamente via o [service container](../container/) do Laravel.

<a id="customizing-the-error-messages"></a>
### Personalizando as Mensagens de Erro

Você pode personalizar as mensagens de erro usadas pela form request sobrescrevendo o método `messages`. Esse método deve retornar um array de pares atributo / regra e suas respectivas mensagens de erro:

```php
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a id="customizing-the-validation-attributes"></a>
#### Personalizando os Atributos de Validação

Muitas das mensagens de erro das regras de validação integradas do Laravel contêm um placeholder `:attribute`. Se você quiser que o placeholder `:attribute` da sua mensagem de validação seja substituído por um nome de atributo personalizado, pode especificar os nomes personalizados sobrescrevendo o método `attributes`. Esse método deve retornar um array de pares atributo / nome:

```php
/**
 * Get custom attributes for validator errors.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```

<a id="preparing-input-for-validation"></a>
### Preparando a Entrada para Validação

Se você precisar preparar ou sanitizar algum dado da requisição antes de aplicar suas regras de validação, pode usar o método `prepareForValidation`:

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

Da mesma forma, se você precisar normalizar algum dado da requisição após a conclusão da validação, pode usar o método `passedValidation`:

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a id="manually-creating-validators"></a>
## Criando Validadores Manualmente

Se você não quiser usar o método `validate` na requisição, pode criar uma instância de validador manualmente usando a [facade](../facades/) `Validator`. O método `make` da facade gera uma nova instância de validador:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => ['required', 'unique:posts', 'max:255'],
            'body' => ['required'],
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```

O primeiro argumento passado ao método `make` são os dados sob validação. O segundo argumento é um array das regras de validação que devem ser aplicadas aos dados.

Após determinar se a validação da requisição falhou, você pode usar o método `withErrors` para armazenar as mensagens de erro na sessão (flash). Ao usar esse método, a variável `$errors` será automaticamente compartilhada com suas views após o redirecionamento, permitindo que você as exiba facilmente para o usuário. O método `withErrors` aceita um validador, um `MessageBag` ou um `array` do PHP.

#### Parando na Primeira Falha de Validação

O método `stopOnFirstFailure` informará ao validador que ele deve parar de validar todos os atributos assim que ocorrer uma única falha de validação:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a id="automatic-redirection"></a>
### Redirecionamento Automático

Se você quiser criar uma instância de validador manualmente, mas ainda aproveitar o redirecionamento automático oferecido pelo método `validate` da requisição HTTP, pode chamar o método `validate` em uma instância de validador existente. Se a validação falhar, o usuário será redirecionado automaticamente ou, no caso de uma requisição XHR, [uma resposta JSON será retornada](#validation-error-response-format):

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validate();
```

Você pode usar o método `validateWithBag` para armazenar as mensagens de erro em um [bag de erros nomeado](#named-error-bags) caso a validação falhe:

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validateWithBag('post');
```

<a id="named-error-bags"></a>
### Bags de Erros Nomeados

Se você tiver vários formulários em uma única página, pode querer nomear o `MessageBag` que contém os erros de validação, permitindo que você recupere as mensagens de erro de um formulário específico. Para isso, passe um nome como segundo argumento para `withErrors`:

```php
return redirect('/register')->withErrors($validator, 'login');
```

Você pode então acessar a instância nomeada de `MessageBag` a partir da variável `$errors`:

```blade
{{ $errors->login->first('email') }}
```

<a id="manual-customizing-the-error-messages"></a>
### Personalizando as Mensagens de Erro

Se necessário, você pode fornecer mensagens de erro personalizadas que uma instância de validador deve usar no lugar das mensagens de erro padrão fornecidas pelo Laravel. Há várias formas de especificar mensagens personalizadas. Primeiro, você pode passar as mensagens personalizadas como terceiro argumento para o método `Validator::make`:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

Neste exemplo, o placeholder `:attribute` será substituído pelo nome real do campo sob validação. Você também pode utilizar outros placeholders nas mensagens de validação. Por exemplo:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a id="specifying-a-custom-message-for-a-given-attribute"></a>
#### Especificando uma Mensagem Personalizada para um Atributo Específico

Às vezes, você pode querer especificar uma mensagem de erro personalizada apenas para um atributo específico. Você pode fazer isso usando a notação de "ponto". Especifique primeiro o nome do atributo, seguido pela regra:

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a id="specifying-custom-attribute-values"></a>
#### Especificando Valores Personalizados de Atributos

Muitas das mensagens de erro integradas do Laravel incluem um placeholder `:attribute` que é substituído pelo nome do campo ou atributo sob validação. Para personalizar os valores usados para substituir esses placeholders em campos específicos, você pode passar um array de atributos personalizados como quarto argumento para o método `Validator::make`:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a id="performing-additional-validation"></a>
### Realizando Validação Adicional

Às vezes, você precisa realizar validação adicional após a conclusão da validação inicial. Você pode fazer isso usando o método `after` do validador. O método `after` aceita um closure ou um array de callables que serão invocados após a conclusão da validação. Os callables fornecidos receberão uma instância de `Illuminate\Validation\Validator`, permitindo que você adicione mensagens de erro adicionais, se necessário:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

Como observado, o método `after` também aceita um array de callables, o que é particularmente conveniente se sua lógica de "validação posterior" estiver encapsulada em classes invocáveis, que receberão uma instância de `Illuminate\Validation\Validator` através do método `__invoke`:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```

<a id="working-with-validated-input"></a>
## Trabalhando Com a Entrada Validada

Após validar os dados da requisição recebida usando uma form request ou uma instância de validador criada manualmente, você pode querer recuperar os dados da requisição que de fato passaram pela validação. Isso pode ser feito de várias maneiras. Primeiro, você pode chamar o método `validated` em uma form request ou instância de validador. Esse método retorna um array com os dados que foram validados:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

Alternativamente, você pode chamar o método `safe` em uma form request ou instância de validador. Esse método retorna uma instância de `Illuminate\Support\ValidatedInput`. Esse objeto expõe os métodos `only`, `except` e `all` para recuperar um subconjunto dos dados validados ou o array completo de dados validados:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

Além disso, a instância de `Illuminate\Support\ValidatedInput` pode ser iterada e acessada como um array:

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

Se você quiser adicionar campos adicionais aos dados validados, pode chamar o método `merge`:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

Se você quiser recuperar os dados validados como uma instância de [coleção](../collections/), pode chamar o método `collect`:

```php
$collection = $request->safe()->collect();
```

<a id="working-with-error-messages"></a>
## Trabalhando Com Mensagens de Erro

Após chamar o método `errors` em uma instância de `Validator`, você receberá uma instância de `Illuminate\Support\MessageBag`, que possui uma variedade de métodos práticos para trabalhar com mensagens de erro. A variável `$errors`, que é disponibilizada automaticamente para todas as views, também é uma instância da classe `MessageBag`.

<a id="retrieving-the-first-error-message-for-a-field"></a>
#### Recuperando a Primeira Mensagem de Erro de um Campo

Para recuperar a primeira mensagem de erro de um determinado campo, use o método `first`:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a id="retrieving-all-error-messages-for-a-field"></a>
#### Recuperando Todas as Mensagens de Erro de um Campo

Se você precisar recuperar um array com todas as mensagens de um determinado campo, use o método `get`:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

Se você estiver validando um campo de formulário do tipo array, pode recuperar todas as mensagens de cada um dos elementos do array usando o caractere `*`:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a id="retrieving-all-error-messages-for-all-fields"></a>
#### Recuperando Todas as Mensagens de Erro de Todos os Campos

Para recuperar um array com todas as mensagens de todos os campos, use o método `all`:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a id="determining-if-messages-exist-for-a-field"></a>
#### Verificando se Existem Mensagens Para um Campo

O método `has` pode ser usado para verificar se existe alguma mensagem de erro para um determinado campo:

```php
if ($errors->has('email')) {
    // ...
}
```

<a id="specifying-custom-messages-in-language-files"></a>
### Especificando Mensagens Personalizadas em Arquivos de Idioma

Cada uma das regras de validação integradas do Laravel possui uma mensagem de erro, localizada no arquivo `lang/en/validation.php` da sua aplicação. Se a sua aplicação não tiver um diretório `lang`, você pode instruir o Laravel a criá-lo usando o comando Artisan `lang:publish`.

Dentro do arquivo `lang/en/validation.php`, você encontrará uma entrada de tradução para cada regra de validação. Você é livre para alterar ou modificar essas mensagens de acordo com as necessidades da sua aplicação.

Além disso, você pode copiar este arquivo para outro diretório de idioma para traduzir as mensagens para o idioma da sua aplicação. Para saber mais sobre a localização no Laravel, consulte a [documentação completa de localização](../localization/).

> **Aviso:**
> Por padrão, o esqueleto de aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los via o comando Artisan `lang:publish`.

<a id="custom-messages-for-specific-attributes"></a>
#### Mensagens Personalizadas Para Atributos Específicos

Você pode personalizar as mensagens de erro usadas para combinações específicas de atributo e regra dentro dos arquivos de idioma de validação da sua aplicação. Para isso, adicione suas personalizações de mensagem ao array `custom` do seu arquivo de idioma `lang/xx/validation.php`:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a id="specifying-attribute-in-language-files"></a>
### Especificando Atributos em Arquivos de Idioma

Muitas das mensagens de erro integradas do Laravel incluem um placeholder `:attribute` que é substituído pelo nome do campo ou atributo sob validação. Se você quiser que a parte `:attribute` da sua mensagem de validação seja substituída por um valor personalizado, pode especificar o nome personalizado do atributo no array `attributes` do seu arquivo de idioma `lang/xx/validation.php`:

```php
'attributes' => [
    'email' => 'email address',
],
```

> **Aviso:**
> Por padrão, o esqueleto de aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los via o comando Artisan `lang:publish`.

<a id="specifying-values-in-language-files"></a>
### Especificando Valores em Arquivos de Idioma

Algumas das mensagens de erro integradas das regras de validação do Laravel contêm um placeholder `:value` que é substituído pelo valor atual do atributo da requisição. No entanto, você pode eventualmente precisar que a parte `:value` da sua mensagem de validação seja substituída por uma representação personalizada do valor. Por exemplo, considere a regra a seguir, que especifica que um número de cartão de crédito é obrigatório se o `payment_type` tiver o valor `cc`:

```php
Validator::make($request->all(), [
    'credit_card_number' => ['required_if:payment_type,cc']
]);
```

Se esta regra de validação falhar, ela produzirá a seguinte mensagem de erro:

```text
The credit card number field is required when payment type is cc.
```

Em vez de exibir `cc` como valor do tipo de pagamento, você pode especificar uma representação de valor mais amigável para o usuário no seu arquivo de idioma `lang/xx/validation.php`, definindo um array `values`:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> **Aviso:**
> Por padrão, o esqueleto de aplicação Laravel não inclui o diretório `lang`. Se você quiser personalizar os arquivos de idioma do Laravel, pode publicá-los via o comando Artisan `lang:publish`.

Após definir esse valor, a regra de validação produzirá a seguinte mensagem de erro:

```text
The credit card number field is required when payment type is credit card.
```

<a id="available-validation-rules"></a>
## Regras de Validação Disponíveis

Abaixo está uma lista de todas as regras de validação disponíveis e suas funções:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

#### Booleanos

<div class="collection-method-list" markdown="1">

[Aceito](#rule-accepted)
[Aceito Se](#rule-accepted-if)
[Booleano](#rule-boolean)
[Recusado](#rule-declined)
[Recusado Se](#rule-declined-if)

</div>

#### Strings

<div class="collection-method-list" markdown="1">

[URL Ativa](#rule-active-url)
[Alfa](#rule-alpha)
[Alfa Traço](#rule-alpha-dash)
[Alfanumérico](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmado](#rule-confirmed)
[Senha Atual](#rule-current-password)
[Diferente](#rule-different)
[Não Começa Com](#rule-doesnt-start-with)
[Não Termina Com](#rule-doesnt-end-with)
[E-mail](#rule-email)
[Termina Com](#rule-ends-with)
[Enum](#rule-enum)
[Cor Hexadecimal](#rule-hex-color)
[Em](#rule-in)
[Endereço IP](#rule-ip)
[JSON](#rule-json)
[Minúsculas](#rule-lowercase)
[Endereço MAC](#rule-mac)
[Máximo](#rule-max)
[Mínimo](#rule-min)
[Não Em](#rule-not-in)
[Expressão Regular](#rule-regex)
[Não Expressão Regular](#rule-not-regex)
[Igual](#rule-same)
[Tamanho](#rule-size)
[Começa Com](#rule-starts-with)
[String](#rule-string)
[Maiúsculas](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### Números

<div class="collection-method-list" markdown="1">

[Entre](#rule-between)
[Decimal](#rule-decimal)
[Diferente](#rule-different)
[Dígitos](#rule-digits)
[Dígitos Entre](#rule-digits-between)
[Maior Que](#rule-gt)
[Maior Ou Igual](#rule-gte)
[Inteiro](#rule-integer)
[Menor Que](#rule-lt)
[Menor Ou Igual](#rule-lte)
[Máximo](#rule-max)
[Máximo de Dígitos](#rule-max-digits)
[Mínimo](#rule-min)
[Mínimo de Dígitos](#rule-min-digits)
[Múltiplo De](#rule-multiple-of)
[Numérico](#rule-numeric)
[Igual](#rule-same)
[Tamanho](#rule-size)

</div>

#### Arrays

<div class="collection-method-list" markdown="1">

[Array](#rule-array)
[Chaves de Array](#rule-array-keys)
[Entre](#rule-between)
[Contém](#rule-contains)
[Não Contém](#rule-doesnt-contain)
[Distinto](#rule-distinct)
[Em Array](#rule-in-array)
[Em Chaves de Array](#rule-in-array-keys)
[Lista](#rule-list)
[Máximo](#rule-max)
[Mínimo](#rule-min)
[Tamanho](#rule-size)

</div>

#### Datas

<div class="collection-method-list" markdown="1">

[Depois De](#rule-after)
[Depois Ou Igual](#rule-after-or-equal)
[Antes De](#rule-before)
[Antes Ou Igual](#rule-before-or-equal)
[Data](#rule-date)
[Data Igual](#rule-date-equals)
[Formato de Data](#rule-date-format)
[Diferente](#rule-different)
[Fuso Horário](#rule-timezone)

</div>

#### Arquivos

<div class="collection-method-list" markdown="1">

[Entre](#rule-between)
[Dimensões](#rule-dimensions)
[Codificação](#rule-encoding)
[Extensões](#rule-extensions)
[Arquivo](#rule-file)
[Imagem](#rule-image)
[Máximo](#rule-max)
[Mínimo](#rule-min)
[Tipos MIME](#rule-mimetypes)
[Tipo MIME Pela Extensão do Arquivo](#rule-mimes)
[Tamanho](#rule-size)

</div>

#### Banco de Dados

<div class="collection-method-list" markdown="1">

[Existe](#rule-exists)
[Único](#rule-unique)

</div>

#### Utilitários

<div class="collection-method-list" markdown="1">

[Qualquer Um De](#rule-anyof)
[Bail](#rule-bail)
[Excluir](#rule-exclude)
[Excluir Se](#rule-exclude-if)
[Excluir A Menos Que](#rule-exclude-unless)
[Excluir Com](#rule-exclude-with)
[Excluir Sem](#rule-exclude-without)
[Preenchido](#rule-filled)
[Ausente](#rule-missing)
[Ausente Se](#rule-missing-if)
[Ausente A Menos Que](#rule-missing-unless)
[Ausente Com](#rule-missing-with)
[Ausente Com Todos](#rule-missing-with-all)
[Anulável](#rule-nullable)
[Presente](#rule-present)
[Presente Se](#rule-present-if)
[Presente A Menos Que](#rule-present-unless)
[Presente Com](#rule-present-with)
[Presente Com Todos](#rule-present-with-all)
[Proibido](#rule-prohibited)
[Proibido Se](#rule-prohibited-if)
[Proibido Se Aceito](#rule-prohibited-if-accepted)
[Proibido Se Recusado](#rule-prohibited-if-declined)
[Proibido A Menos Que](#rule-prohibited-unless)
[Proíbe](#rule-prohibits)
[Obrigatório](#rule-required)
[Obrigatório Se](#rule-required-if)
[Obrigatório Se Aceito](#rule-required-if-accepted)
[Obrigatório Se Recusado](#rule-required-if-declined)
[Obrigatório A Menos Que](#rule-required-unless)
[Obrigatório Com](#rule-required-with)
[Obrigatório Com Todos](#rule-required-with-all)
[Obrigatório Sem](#rule-required-without)
[Obrigatório Sem Todos](#rule-required-without-all)
[Chaves de Array Obrigatórias](#rule-required-array-keys)
[Às Vezes](#validating-when-present)

</div>

<a id="rule-builders"></a>
### Construtores de Regras

Além de strings, muitas regras de validação podem ser definidas usando métodos da classe `Illuminate\Validation\Rule`. Esses métodos oferecem autocompletar na IDE e podem ser combinados com regras em formato string:

```php
use Illuminate\Validation\Rule;

'name' => [Rule::required(), Rule::string()->max(255)],
'terms' => [Rule::accepted()],
'enabled' => [Rule::boolean()],
'website' => [Rule::nullable(), Rule::activeUrl()],
```

Os nomes dos métodos usam camel case, como `Rule::hexColor()`, `Rule::macAddress()` e `Rule::requiredArrayKeys(['name', 'email'])`. Regras que dependem de outros campos aceitam os nomes dos campos ou os valores de comparação como argumentos:

```php
'terms' => [Rule::acceptedIf('account_type', ['personal', 'business'])],
'nickname' => [Rule::excludeWith('name')],
'email' => [Rule::requiredWithout(['phone', 'mobile'])],
'settings' => [Rule::presentIf('account_type', 'business')],
```

Os métodos `acceptedIf`, `declinedIf`, `missingIf`, `missingUnless`, `presentIf` e `presentUnless` aceitam um valor de comparação ou um array de valores de comparação. Métodos como `requiredWith`, `requiredWithAll`, `requiredWithout`, `requiredWithoutAll`, `missingWith`, `missingWithAll`, `presentWith`, `presentWithAll` e `prohibits` aceitam um array de nomes de campos ou múltiplos argumentos com nomes de campos.

Expressões regulares também podem ser definidas usando os métodos `regex` e `notRegex`:

```php
'username' => [Rule::required(), Rule::regex('/^[a-z]+$/i')],
'code' => [Rule::notRegex('/^test-/i')],
```

<a id="rule-accepted"></a>
#### accepted

O campo sob validação deve ser `"yes"`, `"on"`, `1`, `"1"`, `true` ou `"true"`. Isso é útil para validar a aceitação de "Termos de Serviço" ou campos semelhantes.

<a id="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

O campo sob validação deve ser `"yes"`, `"on"`, `1`, `"1"`, `true` ou `"true"` se outro campo sob validação for igual a um valor especificado. Isso é útil para validar a aceitação de "Termos de Serviço" ou campos semelhantes.

<a id="rule-active-url"></a>
#### active_url

O campo sob validação deve ter um registro A ou AAAA válido de acordo com a função PHP `dns_get_record`. O nome de host da URL fornecida é extraído usando a função PHP `parse_url` antes de ser passado para `dns_get_record`.

Ao testar regras de validação que realizam consultas DNS, como `active_url` e `email:dns`, você pode usar o método `Validator::fakeDnsLookups`. Ele simula as consultas DNS, preservando o restante do comportamento de validação das regras:

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```

<a id="rule-after"></a>
#### after:_date_

O campo sob validação deve ser um valor posterior a uma determinada data. As datas serão passadas para a função PHP `strtotime` para serem convertidas em uma instância válida de `DateTime`:

```php
'start_date' => ['required', 'date', 'after:tomorrow']
```

Em vez de passar uma string de data para ser avaliada por `strtotime`, você pode especificar outro campo para comparar com a data:

```php
'finish_date' => ['required', 'date', 'after:start_date']
```

Por conveniência, regras baseadas em data podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

Os métodos `afterToday` e `todayOrAfter` podem ser usados para expressar de forma fluente que a data deve ser posterior a hoje, ou igual ou posterior a hoje, respectivamente:

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a id="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

O campo sob validação deve ser um valor posterior ou igual à data informada. Para mais informações, consulte a regra [after](#rule-after).

Por conveniência, regras baseadas em data podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a id="rule-anyof"></a>
#### anyOf

A regra de validação `Rule::anyOf` permite especificar que o campo sob validação deve satisfazer qualquer um dos conjuntos de regras fornecidos. Por exemplo, a regra a seguir validará que o campo `username` é um endereço de e-mail ou uma string alfanumérica (incluindo traços) com pelo menos 6 caracteres:

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```

<a id="rule-alpha"></a>
#### alpha

O campo sob validação deve conter apenas caracteres alfabéticos Unicode contidos em [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) e [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=).

Para restringir esta regra de validação a caracteres da faixa ASCII (`a-z` e `A-Z`), você pode fornecer a opção `ascii` à regra de validação:

```php
'username' => ['alpha:ascii'],
```

<a id="rule-alpha-dash"></a>
#### alpha_dash

O campo sob validação deve conter apenas caracteres alfanuméricos Unicode contidos em [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), além de traços ASCII (`-`) e sublinhados ASCII (`_`).

Para restringir esta regra de validação a caracteres da faixa ASCII (`a-z`, `A-Z` e `0-9`), você pode fornecer a opção `ascii` à regra de validação:

```php
'username' => ['alpha_dash:ascii'],
```

<a id="rule-alpha-num"></a>
#### alpha_num

O campo sob validação deve conter apenas caracteres alfanuméricos Unicode contidos em [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) e [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=).

Para restringir esta regra de validação a caracteres da faixa ASCII (`a-z`, `A-Z` e `0-9`), você pode fornecer a opção `ascii` à regra de validação:

```php
'username' => ['alpha_num:ascii'],
```

<a id="rule-array"></a>
#### array

O campo sob validação deve ser um `array` do PHP.

Quando valores adicionais são fornecidos à regra `array`, cada chave do array de entrada deve estar presente na lista de valores fornecida à regra. No exemplo a seguir, a chave `admin` do array de entrada é inválida, pois não está contida na lista de valores fornecida à regra `array`:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

Em geral, você deve sempre especificar as chaves de array que podem estar presentes no seu array.

<a id="rule-array-keys"></a>
#### array_keys:_foo_,_bar_,...

O campo sob validação deve ser um `array` do PHP cujas chaves estejam todas incluídas na lista informada. Pelo menos uma chave deve ser fornecida:

```php
'user' => ['array_keys:name,username'],
```

Por conveniência, você pode usar o método `Rule::arrayKeys`:

```php
'user' => [Rule::arrayKeys('name', 'username')],
```

<a id="rule-ascii"></a>
#### ascii

O campo sob validação deve conter apenas caracteres ASCII de 7 bits.

<a id="rule-bail"></a>
#### bail

Interrompe a execução das regras de validação para o campo após a primeira falha de validação.

Enquanto a regra `bail` interromperá a validação de um campo específico apenas quando encontrar uma falha de validação, o método `stopOnFirstFailure` informará ao validador que ele deve parar de validar todos os atributos assim que ocorrer uma única falha de validação:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a id="rule-before"></a>
#### before:_date_

O campo sob validação deve ser um valor anterior à data informada. As datas serão passadas para a função PHP `strtotime` para serem convertidas em uma instância válida de `DateTime`. Além disso, assim como na regra [after](#rule-after), o nome de outro campo sob validação pode ser informado como valor de `date`.

Por conveniência, regras baseadas em data também podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

Os métodos `beforeToday` e `todayOrBefore` podem ser usados para expressar de forma fluente que a data deve ser anterior a hoje, ou igual ou anterior a hoje, respectivamente:

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a id="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

O campo sob validação deve ser um valor anterior ou igual à data informada. As datas serão passadas para a função PHP `strtotime` para serem convertidas em uma instância válida de `DateTime`. Além disso, assim como na regra [after](#rule-after), o nome de outro campo sob validação pode ser informado como valor de `date`.

Por conveniência, regras baseadas em data também podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a id="rule-between"></a>
#### between:_min_,_max_

O campo sob validação deve ter um tamanho entre _min_ e _max_ (inclusive). Strings, números, arrays e arquivos são avaliados da mesma forma que a regra [size](#rule-size).

<a id="rule-boolean"></a>
#### boolean

O campo sob validação deve poder ser convertido para booleano. As entradas aceitas são `true`, `false`, `1`, `0`, `"1"` e `"0"`.

Você pode usar o parâmetro `strict` para considerar o campo válido somente se seu valor for `true` ou `false`:

```php
'foo' => ['boolean:strict']
```

Alternativamente, você pode usar o método `Rule::boolean`, passando `true` para habilitar a validação estrita:

```php
'foo' => [Rule::boolean(true)],
```

<a id="rule-confirmed"></a>
#### confirmed

O campo sob validação deve ter um campo correspondente de `{campo}_confirmation`. Por exemplo, se o campo sob validação for `password`, um campo `password_confirmation` correspondente deve estar presente na entrada.

Você também pode informar um nome personalizado para o campo de confirmação. Por exemplo, `confirmed:repeat_username` esperará que o campo `repeat_username` corresponda ao campo sob validação.

Você também pode usar o método `Rule::confirmed`, especificando um campo de confirmação personalizado pelo método `customField`:

```php
'username' => [Rule::confirmed()->customField('repeat_username')],
```

<a id="rule-contains"></a>
#### contains:_foo_,_bar_,...

O campo sob validação deve ser um array que contenha todos os valores de parâmetro informados. Como essa regra geralmente exige que você use `implode` em um array, o método `Rule::contains` pode ser usado para construir a regra de forma fluente:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```

<a id="rule-doesnt-contain"></a>
#### doesnt_contain:_foo_,_bar_,...

O campo sob validação deve ser um array que não contenha nenhum dos valores de parâmetro informados. Como essa regra geralmente exige que você use `implode` em um array, o método `Rule::doesntContain` pode ser usado para construir a regra de forma fluente:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::doesntContain(['admin', 'editor']),
    ],
]);
```

<a id="rule-current-password"></a>
#### current_password

O campo sob validação deve corresponder à senha do usuário autenticado. Você pode especificar um [guard de autenticação](../authentication/) usando o primeiro parâmetro da regra:

```php
'password' => ['current_password:api']
```

Alternativamente, você pode usar o método `Rule::currentPassword` e especificar o guard de autenticação pelo método `guard`:

```php
'password' => [Rule::currentPassword()->guard('api')],
```

<a id="rule-date"></a>
#### date

O campo sob validação deve ser uma data válida e não relativa, de acordo com a função PHP `strtotime`.

<a id="rule-date-equals"></a>
#### date_equals:_date_

O campo sob validação deve ser igual à data informada. As datas serão passadas para a função PHP `strtotime` para serem convertidas em uma instância válida de `DateTime`.

Por conveniência, regras baseadas em data podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [Rule::date()->equals('2026-01-01')],
```

O método `equals` aceita uma string de data, uma instância de `DateTimeInterface` ou o nome de outro campo para comparação.

<a id="rule-date-format"></a>
#### date_format:_format_,...

O campo sob validação deve corresponder a um dos _formatos_ informados. Você deve usar **ou** `date` **ou** `date_format` ao validar um campo, não ambos. Esta regra de validação suporta todos os formatos suportados pela classe [DateTime](https://www.php.net/manual/en/class.datetime.php) do PHP.

Por conveniência, regras baseadas em data podem ser construídas usando o construtor fluente de regras `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a id="rule-decimal"></a>
#### decimal:_min_,_max_

O campo sob validação deve ser numérico e deve conter o número especificado de casas decimais:

```php
// Must have exactly two decimal places (9.99)...
'price' => ['decimal:2']

// Must have between 2 and 4 decimal places...
'price' => ['decimal:2,4']
```

<a id="rule-declined"></a>
#### declined

O campo sob validação deve ser `"no"`, `"off"`, `0`, `"0"`, `false` ou `"false"`.

<a id="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

O campo sob validação deve ser `"no"`, `"off"`, `0`, `"0"`, `false` ou `"false"` se outro campo sob validação for igual a um valor especificado.

<a id="rule-different"></a>
#### different:_field_

O campo sob validação deve ter um valor diferente de _field_.

<a id="rule-digits"></a>
#### digits:_value_

O inteiro sob validação deve ter exatamente _value_ de comprimento.

<a id="rule-digits-between"></a>
#### digits_between:_min_,_max_

O inteiro sob validação deve ter um comprimento entre _min_ e _max_.

<a id="rule-dimensions"></a>
#### dimensions

O arquivo sob validação deve ser uma imagem que atenda às restrições de dimensão especificadas pelos parâmetros da regra:

```php
'avatar' => ['dimensions:min_width=100,min_height=200']
```

As restrições disponíveis são: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_, _min\_ratio_, _max\_ratio_.

Uma restrição _ratio_ deve ser representada como largura dividida pela altura. Ela pode ser especificada por uma fração, como `3/2`, ou por um float, como `1.5`:

```php
'avatar' => ['dimensions:ratio=3/2']
```

As restrições _min\_ratio_ e _max\_ratio_ podem ser usadas para definir um intervalo de proporções aceitáveis:

```php
'avatar' => ['dimensions:min_ratio=1/2,max_ratio=3/2']
```

Como esta regra exige vários argumentos, geralmente é mais conveniente usar o método `Rule::dimensions` para construir a regra de forma fluente:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```

Você também pode usar os métodos `minRatio`, `maxRatio` e `ratioBetween` para definir restrições de proporção de forma fluente:

```php
Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2);
```

<a id="rule-distinct"></a>
#### distinct

Ao validar arrays, o campo sob validação não pode ter valores duplicados:

```php
'foo.*.id' => ['distinct']
```

Por padrão, `distinct` usa comparações de variáveis não estritas. Para usar comparações estritas, você pode adicionar o parâmetro `strict` à definição da regra de validação:

```php
'foo.*.id' => ['distinct:strict']
```

Você pode adicionar `ignore_case` aos argumentos da regra de validação para que ela ignore diferenças de maiúsculas e minúsculas:

```php
'foo.*.id' => ['distinct:ignore_case']
```

Alternativamente, você pode usar o método `Rule::distinct`, encadeando os métodos `strict` e `ignoreCase` conforme necessário:

```php
'foo.*.id' => [Rule::distinct()->strict()->ignoreCase()],
```

<a id="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

O campo sob validação não pode começar com nenhum dos valores informados.

<a id="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

O campo sob validação não pode terminar com nenhum dos valores informados.

<a id="rule-email"></a>
#### email

O campo sob validação deve estar formatado como um endereço de e-mail. Esta regra de validação utiliza o pacote [egulias/email-validator](https://github.com/egulias/EmailValidator) para validar o endereço de e-mail. Por padrão, o validador `RFCValidation` é aplicado, mas você também pode aplicar outros estilos de validação:

```php
'email' => ['email:rfc,dns']
```

O exemplo acima aplicará as validações `RFCValidation` e `DNSCheckValidation`. Aqui está a lista completa de estilos de validação que você pode aplicar:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - Valida o endereço de e-mail de acordo com as [RFCs suportadas](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs).
- `strict`: `NoRFCWarningsValidation` - Valida o e-mail de acordo com as [RFCs suportadas](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), falhando quando forem encontrados avisos (por exemplo, pontos no final e múltiplos pontos consecutivos).
- `dns`: `DNSCheckValidation` - Garante que o domínio do endereço de e-mail possua um registro MX válido.
- `spoof`: `SpoofCheckValidation` - Garante que o endereço de e-mail não contenha caracteres Unicode homógrafos ou enganosos.
- `filter`: `FilterEmailValidation` - Garante que o endereço de e-mail seja válido de acordo com a função `filter_var` do PHP.
- `filter_unicode`: `FilterEmailValidation::unicode()` - Garante que o endereço de e-mail seja válido de acordo com a função `filter_var` do PHP, permitindo alguns caracteres Unicode.

</div>

Por conveniência, as regras de validação de e-mail podem ser construídas usando o construtor fluente de regras:

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```

O validador `dns` executa uma consulta DNS real para confirmar que o domínio do endereço possui um registro MX válido. Ele não determina se uma caixa de correio individual existe.

Como os seus testes não devem depender de consultas DNS reais, você pode usar o método `Validator::fakeDnsLookups` para [simular consultas DNS](#rule-active-url), enquanto quaisquer outras validações solicitadas, como `rfc`, continuam sendo executadas:

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```

Isso permite que sua aplicação continue usando suas regras de validação existentes durante os testes:

```php
'email' => ['required', 'email:rfc,dns'],
```

> **Aviso:**
> Os validadores `dns` e `spoof` exigem a extensão `intl` do PHP.

<a id="rule-encoding"></a>
#### encoding:*encoding_type*

O campo sob validação deve corresponder à codificação de caracteres especificada. Esta regra usa a função `mb_check_encoding` do PHP para verificar a codificação do arquivo ou valor string informado. Por conveniência, a regra `encoding` pode ser construída usando o construtor fluente de regras de arquivo do Laravel:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['csv'])
            ->encoding('utf-8'),
    ],
]);
```

<a id="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

O campo sob validação deve terminar com um dos valores informados.

<a id="rule-enum"></a>
#### enum

A regra `Enum` é uma regra baseada em classe que valida se o campo sob validação contém um valor de enum válido. A regra `Enum` aceita o nome do enum como seu único argumento do construtor. Ao validar valores primitivos, um enum com backing deve ser fornecido à regra `Enum`:

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

Os métodos `only` e `except` da regra `Enum` podem ser usados para limitar quais casos do enum devem ser considerados válidos:

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

O método `when` pode ser usado para modificar condicionalmente a regra `Enum`:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```

<a id="rule-exclude"></a>
#### exclude

O campo sob validação será excluído dos dados da requisição retornados pelos métodos `validate` e `validated`.

<a id="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

O campo sob validação será excluído dos dados da requisição retornados pelos métodos `validate` e `validated` se o campo _anotherfield_ for igual a _value_.

Se for necessária uma lógica condicional de exclusão mais complexa, você pode utilizar o método `Rule::excludeIf`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação deve ser excluído:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf(fn () => $request->user()->is_admin)],
]);
```

<a id="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

O campo sob validação será excluído dos dados da requisição retornados pelos métodos `validate` e `validated`, a menos que o campo _anotherfield_ seja igual a _value_. Se _value_ for `null` (`exclude_unless:name,null`), o campo sob validação será excluído, a menos que o campo de comparação seja `null` ou não esteja presente nos dados da requisição.

Se for necessária uma lógica condicional de exclusão mais complexa, você pode utilizar o método `Rule::excludeUnless`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação não deve ser excluído:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless(fn () => $request->user()->is_admin)],
]);
```

<a id="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

O campo sob validação será excluído dos dados da requisição retornados pelos métodos `validate` e `validated` se o campo _anotherfield_ estiver presente.

<a id="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

O campo sob validação será excluído dos dados da requisição retornados pelos métodos `validate` e `validated` se o campo _anotherfield_ não estiver presente.

<a id="rule-exists"></a>
#### exists:_table_,_column_

O campo sob validação deve existir em uma determinada tabela do banco de dados.

<a id="basic-usage-of-exists-rule"></a>
#### Uso Básico da Regra Exists

```php
'state' => ['exists:states']
```

Se a opção `column` não for especificada, o nome do campo será usado. Assim, neste caso, a regra validará que a tabela `states` do banco de dados contém um registro com o valor da coluna `state` correspondente ao valor do atributo `state` da requisição.

<a id="specifying-a-custom-column-name"></a>
#### Especificando um Nome de Coluna Personalizado

Você pode especificar explicitamente o nome da coluna do banco de dados que deve ser usada pela regra de validação, colocando-o após o nome da tabela:

```php
'state' => ['exists:states,abbreviation']
```

Ocasionalmente, você pode precisar especificar uma conexão de banco de dados específica a ser usada na consulta `exists`. Você pode fazer isso prefixando o nome da conexão ao nome da tabela:

```php
'email' => ['exists:connection.staff,email']
```

Em vez de especificar o nome da tabela diretamente, você pode especificar o model Eloquent que deve ser usado para determinar o nome da tabela:

```php
'user_id' => ['exists:App\Models\User,id']
```

Se você quiser personalizar a consulta executada pela regra de validação, pode usar a classe `Rule` para definir a regra de forma fluente.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```

Você pode especificar explicitamente o nome da coluna do banco de dados que deve ser usada pela regra `exists` gerada pelo método `Rule::exists`, informando o nome da coluna como segundo argumento para o método `exists`:

```php
'state' => [Rule::exists('states', 'abbreviation')],
```

Às vezes, você pode querer validar se um array de valores existe no banco de dados. Para isso, adicione as regras `exists` e [array](#rule-array) ao campo sob validação:

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

Quando ambas as regras são atribuídas a um campo, o Laravel construirá automaticamente uma única consulta para determinar se todos os valores informados existem na tabela especificada.

<a id="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

O arquivo sob validação deve ter uma extensão atribuída pelo usuário correspondente a uma das extensões listadas:

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> **Aviso:**
> Você nunca deve depender apenas da validação de um arquivo pela extensão atribuída pelo usuário. Esta regra normalmente deve ser usada sempre em combinação com as regras [mimes](#rule-mimes) ou [mimetypes](#rule-mimetypes).

<a id="rule-file"></a>
#### file

O campo sob validação deve ser um arquivo enviado com sucesso.

<a id="rule-filled"></a>
#### filled

O campo sob validação não pode estar vazio quando estiver presente.

<a id="rule-gt"></a>
#### gt:_field_

O campo sob validação deve ser maior que o _field_ ou _value_ informado. Os dois campos devem ser do mesmo tipo. Strings, números, arrays e arquivos são avaliados usando as mesmas convenções da regra [size](#rule-size).

<a id="rule-gte"></a>
#### gte:_field_

O campo sob validação deve ser maior ou igual ao _field_ ou _value_ informado. Os dois campos devem ser do mesmo tipo. Strings, números, arrays e arquivos são avaliados usando as mesmas convenções da regra [size](#rule-size).

<a id="rule-hex-color"></a>
#### hex_color

O campo sob validação deve conter um valor de cor válido no formato [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color).

<a id="rule-image"></a>
#### image

O arquivo sob validação deve ser uma imagem (jpg, jpeg, png, bmp, gif, webp, avif, heic ou heif).

> **Aviso:**
> Por padrão, a regra `image` não permite arquivos SVG devido à possibilidade de vulnerabilidades XSS. Se você precisar permitir arquivos SVG, pode fornecer a diretiva `allow_svg` à regra `image` (`image:allow_svg`).

<a id="rule-in"></a>
#### in:_foo_,_bar_,...

O campo sob validação deve estar incluído na lista de valores informada. Como esta regra geralmente exige que você use `implode` em um array, o método `Rule::in` pode ser usado para construir a regra de forma fluente:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

Quando a regra `in` é combinada com a regra `array`, cada valor do array de entrada deve estar presente na lista de valores fornecida à regra `in`. No exemplo a seguir, o código de aeroporto `LAS` do array de entrada é inválido, pois não está contido na lista de aeroportos fornecida à regra `in`:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

<a id="rule-in-array"></a>
#### in_array:_anotherfield_.*

O campo sob validação deve existir nos valores de _anotherfield_.

<a id="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

O campo sob validação deve ser um array que possua pelo menos um dos _values_ informados como chave dentro do array:

```php
'config' => ['array', 'in_array_keys:timezone']
```

<a id="rule-integer"></a>
#### integer

O campo sob validação deve ser um inteiro.

Você pode usar o parâmetro `strict` para considerar o campo válido somente se o seu tipo for `integer`. Strings com valores inteiros serão consideradas inválidas:

```php
'age' => ['integer:strict']
```

> **Aviso:**
> Esta regra de validação não verifica se a entrada é do tipo de variável "integer", apenas se a entrada é de um tipo aceito pela regra `FILTER_VALIDATE_INT` do PHP. Se você precisar validar a entrada como um número, use esta regra em combinação com [a regra de validação `numeric`](#rule-numeric).

<a id="rule-ip"></a>
#### ip

O campo sob validação deve ser um endereço IP.

Você também pode usar o método `Rule::ip`, opcionalmente restringindo a versão do IP para `4` ou `6`:

```php
'ip_address' => [Rule::ip()],
'ipv4_address' => [Rule::ip()->version(4)],
'ipv6_address' => [Rule::ip()->version(6)],
```

<a id="ipv4"></a>
#### ipv4

O campo sob validação deve ser um endereço IPv4.

<a id="ipv6"></a>
#### ipv6

O campo sob validação deve ser um endereço IPv6.

<a id="rule-json"></a>
#### json

O campo sob validação deve ser uma string JSON válida.

<a id="rule-lt"></a>
#### lt:_field_

O campo sob validação deve ser menor que o _field_ informado. Os dois campos devem ser do mesmo tipo. Strings, números, arrays e arquivos são avaliados usando as mesmas convenções da regra [size](#rule-size).

<a id="rule-lte"></a>
#### lte:_field_

O campo sob validação deve ser menor ou igual ao _field_ informado. Os dois campos devem ser do mesmo tipo. Strings, números, arrays e arquivos são avaliados usando as mesmas convenções da regra [size](#rule-size).

<a id="rule-lowercase"></a>
#### lowercase

O campo sob validação deve estar em letras minúsculas.

<a id="rule-list"></a>
#### list

O campo sob validação deve ser um array que seja uma lista. Um array é considerado uma lista se suas chaves forem números consecutivos de 0 a `count($array) - 1`.

<a id="rule-mac"></a>
#### mac_address

O campo sob validação deve ser um endereço MAC.

<a id="rule-max"></a>
#### max:_value_

O campo sob validação deve ser menor ou igual a um _value_ máximo. Strings, números, arrays e arquivos são avaliados da mesma forma que a regra [size](#rule-size).

<a id="rule-max-digits"></a>
#### max_digits:_value_

O inteiro sob validação deve ter um comprimento máximo de _value_.

<a id="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

O arquivo sob validação deve corresponder a um dos tipos MIME informados:

```php
'video' => ['mimetypes:video/avi,video/mpeg,video/quicktime'],

'media' => ['mimetypes:image/*,video/*'],
```

Para determinar o tipo MIME do arquivo enviado, o conteúdo do arquivo será lido e o framework tentará adivinhar o tipo MIME, que pode ser diferente do tipo MIME informado pelo cliente.

<a id="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

O arquivo sob validação deve ter um tipo MIME correspondente a uma das extensões listadas:

```php
'photo' => ['mimes:jpg,bmp,png']
```

Embora você só precise especificar as extensões, esta regra realmente valida o tipo MIME do arquivo lendo o conteúdo do arquivo e adivinhando o seu tipo MIME. Uma lista completa de tipos MIME e suas extensões correspondentes pode ser encontrada no seguinte local:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a id="mime-types-and-extensions"></a>
#### Tipos MIME e Extensões

Esta regra de validação não verifica a correspondência entre o tipo MIME e a extensão que o usuário atribuiu ao arquivo. Por exemplo, a regra de validação `mimes:png` consideraria um arquivo com conteúdo PNG válido como uma imagem PNG válida, mesmo que o arquivo se chame `photo.txt`. Se você quiser validar a extensão do arquivo atribuída pelo usuário, pode usar a regra [extensions](#rule-extensions).

<a id="rule-min"></a>
#### min:_value_

O campo sob validação deve ter um _value_ mínimo. Strings, números, arrays e arquivos são avaliados da mesma forma que a regra [size](#rule-size).

<a id="rule-min-digits"></a>
#### min_digits:_value_

O inteiro sob validação deve ter um comprimento mínimo de _value_.

<a id="rule-multiple-of"></a>
#### multiple_of:_value_

O campo sob validação deve ser um múltiplo de _value_.

<a id="rule-missing"></a>
#### missing

O campo sob validação não pode estar presente nos dados de entrada.

<a id="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

O campo sob validação não pode estar presente se o campo _anotherfield_ for igual a qualquer _value_.

<a id="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

O campo sob validação não pode estar presente, a menos que o campo _anotherfield_ seja igual a qualquer _value_.

<a id="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

O campo sob validação não pode estar presente _somente se_ algum dos outros campos especificados estiver presente.

<a id="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

O campo sob validação não pode estar presente _somente se_ todos os outros campos especificados estiverem presentes.

<a id="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

O campo sob validação não pode estar incluído na lista de valores informada. O método `Rule::notIn` pode ser usado para construir a regra de forma fluente:

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a id="rule-not-regex"></a>
#### not_regex:_pattern_

O campo sob validação não pode corresponder à expressão regular informada.

Internamente, esta regra usa a função `preg_match` do PHP. O padrão especificado deve obedecer à mesma formatação exigida por `preg_match` e, portanto, também incluir delimitadores válidos. Por exemplo: `'email' => ['not_regex:/^.+$/i']`.

<a id="rule-nullable"></a>
#### nullable

O campo sob validação pode ser `null`.

<a id="rule-numeric"></a>
#### numeric

O campo sob validação deve ser [numérico](https://www.php.net/manual/en/function.is-numeric.php).

Você pode usar o parâmetro `strict` para considerar o campo válido somente se o seu valor for do tipo inteiro ou float. Strings numéricas serão consideradas inválidas:

```php
'amount' => ['numeric:strict']
```

<a id="rule-present"></a>
#### present

O campo sob validação deve existir nos dados de entrada.

<a id="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

O campo sob validação deve estar presente se o campo _anotherfield_ for igual a qualquer _value_.

<a id="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

O campo sob validação deve estar presente, a menos que o campo _anotherfield_ seja igual a qualquer _value_.

<a id="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

O campo sob validação deve estar presente _somente se_ algum dos outros campos especificados estiver presente.

<a id="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

O campo sob validação deve estar presente _somente se_ todos os outros campos especificados estiverem presentes.

<a id="rule-prohibited"></a>
#### prohibited

O campo sob validação deve estar ausente ou vazio. Um campo é "vazio" se atender a um dos seguintes critérios:

<div class="content-list" markdown="1">

- O valor é `null`.
- O valor é uma string vazia.
- O valor é um array vazio ou um objeto `Countable` vazio.
- O valor é um arquivo enviado com um caminho vazio.

</div>

<a id="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

O campo sob validação deve estar ausente ou vazio se o campo _anotherfield_ for igual a qualquer _value_. Um campo é "vazio" se atender a um dos seguintes critérios:

<div class="content-list" markdown="1">

- O valor é `null`.
- O valor é uma string vazia.
- O valor é um array vazio ou um objeto `Countable` vazio.
- O valor é um arquivo enviado com um caminho vazio.

</div>

Se for necessária uma lógica condicional de proibição mais complexa, você pode utilizar o método `Rule::prohibitedIf`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação deve ser proibido:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf(fn () => $request->user()->is_admin)],
]);
```
<a id="rule-prohibited-if-accepted"></a>
#### prohibited_if_accepted:_anotherfield_,...

O campo sob validação deve estar ausente ou vazio se o campo _anotherfield_ for igual a `"yes"`, `"on"`, `1`, `"1"`, `true` ou `"true"`.

<a id="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

O campo sob validação deve estar ausente ou vazio se o campo _anotherfield_ for igual a `"no"`, `"off"`, `0`, `"0"`, `false` ou `"false"`.

<a id="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

O campo sob validação deve estar ausente ou vazio, a menos que o campo _anotherfield_ seja igual a qualquer _value_. Um campo é "vazio" se atender a um dos seguintes critérios:

<div class="content-list" markdown="1">

- O valor é `null`.
- O valor é uma string vazia.
- O valor é um array vazio ou um objeto `Countable` vazio.
- O valor é um arquivo enviado com um caminho vazio.

</div>

Se for necessária uma lógica condicional de proibição mais complexa, você pode utilizar o método `Rule::prohibitedUnless`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação não deve ser proibido:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless(fn () => $request->user()->is_admin)],
]);
```

<a id="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

Se o campo sob validação não estiver ausente ou vazio, todos os campos em _anotherfield_ devem estar ausentes ou vazios. Um campo é "vazio" se atender a um dos seguintes critérios:

<div class="content-list" markdown="1">

- O valor é `null`.
- O valor é uma string vazia.
- O valor é um array vazio ou um objeto `Countable` vazio.
- O valor é um arquivo enviado com um caminho vazio.

</div>

<a id="rule-regex"></a>
#### regex:_pattern_

O campo sob validação deve corresponder à expressão regular informada.

Internamente, esta regra usa a função `preg_match` do PHP. O padrão especificado deve obedecer à mesma formatação exigida por `preg_match` e, portanto, também incluir delimitadores válidos. Por exemplo: `'email' => ['regex:/^.+@.+$/i']`.

<a id="rule-required"></a>
#### required

O campo sob validação deve estar presente nos dados de entrada e não pode estar vazio. Um campo é "vazio" se atender a um dos seguintes critérios:

<div class="content-list" markdown="1">

- O valor é `null`.
- O valor é uma string vazia.
- O valor é um array vazio ou um objeto `Countable` vazio.
- O valor é um arquivo enviado sem caminho.

</div>

<a id="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

O campo sob validação deve estar presente e não pode estar vazio se o campo _anotherfield_ for igual a qualquer _value_.

Se você quiser construir uma condição mais complexa para a regra `required_if`, pode usar o método `Rule::requiredIf`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação é obrigatório:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf(fn () => $request->user()->is_admin)],
]);
```

<a id="rule-required-if-accepted"></a>
#### required_if_accepted:_anotherfield_,...

O campo sob validação deve estar presente e não pode estar vazio se o campo _anotherfield_ for igual a `"yes"`, `"on"`, `1`, `"1"`, `true` ou `"true"`.

<a id="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

O campo sob validação deve estar presente e não pode estar vazio se o campo _anotherfield_ for igual a `"no"`, `"off"`, `0`, `"0"`, `false` ou `"false"`.

<a id="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

O campo sob validação deve estar presente e não pode estar vazio, a menos que o campo _anotherfield_ seja igual a qualquer _value_. Isso também significa que _anotherfield_ deve estar presente nos dados da requisição, a menos que _value_ seja `null`. Se _value_ for `null` (`required_unless:name,null`), o campo sob validação será obrigatório, a menos que o campo de comparação seja `null` ou não esteja presente nos dados da requisição.

Se você quiser construir uma condição mais complexa para a regra `required_unless`, pode usar o método `Rule::requiredUnless`. Esse método aceita um booleano ou um closure. Quando recebe um closure, o closure deve retornar `true` ou `false` para indicar se o campo sob validação não é obrigatório:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless(fn () => $request->user()->is_admin)],
]);
```

<a id="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

O campo sob validação deve estar presente e não pode estar vazio _somente se_ algum dos outros campos especificados estiver presente e não vazio.

<a id="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

O campo sob validação deve estar presente e não pode estar vazio _somente se_ todos os outros campos especificados estiverem presentes e não vazios.

<a id="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

O campo sob validação deve estar presente e não pode estar vazio _somente quando_ algum dos outros campos especificados estiver vazio ou não estiver presente.

<a id="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

O campo sob validação deve estar presente e não pode estar vazio _somente quando_ todos os outros campos especificados estiverem vazios ou não estiverem presentes.

<a id="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

O campo sob validação deve ser um array e deve conter pelo menos as chaves especificadas.

<a id="rule-same"></a>
#### same:_field_

O _field_ informado deve corresponder ao campo sob validação.

<a id="rule-size"></a>
#### size:_value_

O campo sob validação deve ter um tamanho correspondente ao _value_ informado. Para dados de string, _value_ corresponde ao número de caracteres. Para dados numéricos, _value_ corresponde a um valor inteiro informado (o atributo também deve ter a regra `numeric` ou `integer`). Para um array, _size_ corresponde ao `count` do array. Para arquivos, _size_ corresponde ao tamanho do arquivo em kilobytes. Vejamos alguns exemplos:

```php
// Validate that a string is exactly 12 characters long...
'title' => ['size:12'];

// Validate that a provided integer equals 10...
'seats' => ['integer', 'size:10'];

// Validate that an array has exactly 5 elements...
'tags' => ['array', 'size:5'];

// Validate that an uploaded file is exactly 512 kilobytes...
'image' => ['file', 'size:512'];
```

<a id="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

O campo sob validação deve começar com um dos valores informados.

<a id="rule-string"></a>
#### string

O campo sob validação deve ser uma string. Se você quiser permitir que o campo também seja `null`, deve atribuir a regra `nullable` ao campo.

Por conveniência, as regras de validação de string também podem ser construídas usando o construtor fluente de regras `Rule::string()`:

```php
use Illuminate\Validation\Rule;

'title' => [
    'required',
    Rule::string()
        ->min(3)
        ->max(255)
        ->alphaDash(ascii: true),
],
```

O construtor de regras de string oferece métodos para restrições comuns de string, incluindo `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith` e `uppercase`. Como o construtor de regras é condicionável, você também pode usar os métodos `when` e `unless` para aplicar restrições condicionalmente.

<a id="rule-timezone"></a>
#### timezone

O campo sob validação deve ser um identificador de fuso horário válido de acordo com o método `DateTimeZone::listIdentifiers`.

Os argumentos [aceitos pelo método `DateTimeZone::listIdentifiers`](https://www.php.net/manual/en/datetimezone.listidentifiers.php) também podem ser informados a esta regra de validação:

```php
'timezone' => ['required', 'timezone:all'];

'timezone' => ['required', 'timezone:Africa'];

'timezone' => ['required', 'timezone:per_country,US'];
```

Alternativamente, você pode usar o método `Rule::timezone`, passando quaisquer argumentos de `listIdentifiers` como um array:

```php
'timezone' => [Rule::timezone(['per_country', 'US'])],
```

<a id="rule-unique"></a>
#### unique:_table_,_column_

O campo sob validação não pode existir na tabela do banco de dados informada.

**Especificando um Nome Personalizado de Tabela / Coluna:**

Em vez de especificar o nome da tabela diretamente, você pode especificar o model Eloquent que deve ser usado para determinar o nome da tabela:

```php
'email' => ['unique:App\Models\User,email_address']
```

A opção `column` pode ser usada para especificar a coluna correspondente do banco de dados. Se a opção `column` não for especificada, o nome do campo sob validação será usado.

```php
'email' => ['unique:users,email_address']
```

**Especificando uma Conexão Personalizada de Banco de Dados**

Ocasionalmente, você pode precisar definir uma conexão personalizada para as consultas ao banco de dados feitas pelo validador. Para isso, você pode prefixar o nome da conexão ao nome da tabela:

```php
'email' => ['unique:connection.users,email_address']
```

**Forçando a Regra Unique a Ignorar um ID Informado:**

Às vezes, você pode querer ignorar um determinado ID durante a validação de unicidade. Por exemplo, considere uma tela de "atualizar perfil" que inclui o nome, o endereço de e-mail e a localização do usuário. Provavelmente você vai querer verificar se o endereço de e-mail é único. No entanto, se o usuário alterar apenas o campo de nome e não o campo de e-mail, você não quer que um erro de validação seja lançado, pois o usuário já é o dono desse endereço de e-mail.

Para instruir o validador a ignorar o ID do usuário, usaremos a classe `Rule` para definir a regra de forma fluente.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> **Aviso:**
> Você nunca deve passar qualquer entrada da requisição controlada pelo usuário para o método `ignore`. Em vez disso, passe apenas um ID gerado pelo sistema, como um ID autoincremental ou um UUID de uma instância de model Eloquent. Caso contrário, sua aplicação ficará vulnerável a um ataque de SQL injection.

Em vez de passar o valor da chave do model para o método `ignore`, você também pode passar a instância inteira do model. O Laravel extrairá automaticamente a chave do model:

```php
Rule::unique('users')->ignore($user);
```

Se a sua tabela usar um nome de coluna de chave primária diferente de `id`, você pode especificar o nome da coluna ao chamar o método `ignore`:

```php
Rule::unique('users')->ignore($user->id, 'user_id');
```

Por padrão, a regra `unique` verificará a unicidade da coluna que corresponde ao nome do atributo sob validação. No entanto, você pode passar um nome de coluna diferente como segundo argumento para o método `unique`:

```php
Rule::unique('users', 'email_address')->ignore($user->id);
```

**Adicionando Cláusulas Where Adicionais:**

Você pode especificar condições de consulta adicionais personalizando a consulta com o método `where`. Por exemplo, vamos adicionar uma condição que restrinja a consulta a registros cujo valor da coluna `account_id` seja `1`:

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Ignorando Registros Excluídos Softly nas Verificações de Unicidade:**

Por padrão, a regra unique inclui registros excluídos softly ao determinar a unicidade. Para excluir registros excluídos softly da verificação de unicidade, você pode invocar o método `withoutTrashed`:

```php
Rule::unique('users')->withoutTrashed();
```

Se o seu model usar um nome de coluna diferente de `deleted_at` para registros excluídos softly, você pode informar o nome da coluna ao invocar o método `withoutTrashed`:

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a id="rule-uppercase"></a>
#### uppercase

O campo sob validação deve estar em letras maiúsculas.

<a id="rule-url"></a>
#### url

O campo sob validação deve ser uma URL válida.

Se você quiser especificar os protocolos de URL que devem ser considerados válidos, pode informar os protocolos como parâmetros da regra de validação:

```php
'url' => ['url:http,https'],

'game' => ['url:minecraft,steam'],
```

Alternativamente, você pode usar o método `Rule::url`, especificando os protocolos permitidos pelo método `protocols`:

```php
'url' => [Rule::url()->protocols(['http', 'https'])],
```

<a id="rule-ulid"></a>
#### ulid

O campo sob validação deve ser um [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID) válido.

<a id="rule-uuid"></a>
#### uuid

O campo sob validação deve ser um identificador único universal (UUID) válido, conforme a RFC 9562 (versão 1, 3, 4, 5, 6, 7 ou 8).

Você também pode validar se o UUID informado corresponde a uma especificação de UUID pela versão:

```php
'uuid' => ['uuid:4']
```

Alternativamente, você pode usar o método `Rule::uuid` e especificar a versão do UUID pelo método `version`:

```php
'uuid' => [Rule::uuid()->version(4)],
```

<a id="conditionally-adding-rules"></a>
## Adicionando Regras Condicionalmente

<a id="skipping-validation-when-fields-have-certain-values"></a>
#### Ignorando a Validação Quando os Campos Têm Certos Valores

Às vezes, você pode querer não validar um determinado campo se outro campo tiver um determinado valor. Você pode fazer isso usando a regra de validação `exclude_if`. Neste exemplo, os campos `appointment_date` e `doctor_name` não serão validados se o campo `has_appointment` tiver o valor `false`:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],
    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],
]);
```

Alternativamente, você pode usar a regra `exclude_unless` para não validar um determinado campo, a menos que outro campo tenha um determinado valor:

```php
$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_unless:has_appointment,true', 'required', 'date'],
    'doctor_name' => ['exclude_unless:has_appointment,true', 'required', 'string'],
]);
```

<a id="validating-when-present"></a>
#### Validando Quando Presente

Em algumas situações, você pode querer executar verificações de validação em um campo **somente** se esse campo estiver presente nos dados validados. Para realizar isso rapidamente, adicione a regra `sometimes` à sua lista de regras:

```php
$validator = Validator::make($data, [
    'email' => ['sometimes', 'required', 'email'],
]);
```

No exemplo acima, o campo `email` só será validado se estiver presente no array `$data`.

> **Nota:**
> Se você estiver tentando validar um campo que sempre deve estar presente, mas que pode estar vazio, confira [esta observação sobre campos opcionais](#a-note-on-optional-fields).

<a id="complex-conditional-validation"></a>
#### Validação Condicional Complexa

Às vezes, você pode querer adicionar regras de validação com base em uma lógica condicional mais complexa. Por exemplo, você pode querer exigir um determinado campo somente se outro campo tiver um valor maior que 100. Ou pode precisar que dois campos tenham um determinado valor somente quando outro campo estiver presente. Adicionar essas regras de validação não precisa ser complicado. Primeiro, crie uma instância de `Validator` com suas _regras estáticas_, que nunca mudam:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => ['required', 'email'],
    'games' => ['required', 'integer', 'min:0'],
]);
```

Vamos supor que nossa aplicação web seja para colecionadores de jogos. Se um colecionador de jogos se registrar na nossa aplicação e possuir mais de 100 jogos, queremos que ele explique por que possui tantos jogos. Por exemplo, talvez ele administre uma loja de revenda de jogos ou talvez apenas goste de colecionar jogos. Para adicionar essa exigência condicionalmente, podemos usar o método `sometimes` na instância de `Validator`.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {
    return $input->games >= 100;
});
```

O primeiro argumento passado ao método `sometimes` é o nome do campo que estamos validando condicionalmente. O segundo argumento é a lista de regras que queremos adicionar. Se o closure passado como terceiro argumento retornar `true`, as regras serão adicionadas. Este método facilita a criação de validações condicionais complexas. Você pode até adicionar validações condicionais para vários campos de uma só vez:

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> **Nota:**
> O parâmetro `$input` passado ao seu closure será uma instância de `Illuminate\Support\Fluent` e poderá ser usado para acessar a sua entrada e os arquivos sob validação.

<a id="complex-conditional-array-validation"></a>
#### Validação Condicional Complexa de Arrays

Às vezes, você pode querer validar um campo com base em outro campo do mesmo array aninhado cujo índice você não conhece. Nessas situações, você pode permitir que seu closure receba um segundo argumento, que será o item individual atual do array sendo validado:

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

Assim como o parâmetro `$input` passado ao closure, o parâmetro `$item` será uma instância de `Illuminate\Support\Fluent` quando os dados do atributo forem um array; caso contrário, será uma string.

<a id="validating-arrays"></a>
## Validando Arrays

Como discutido na [documentação da regra de validação array](#rule-array), a regra `array` aceita uma lista de chaves de array permitidas. Se houver chaves adicionais dentro do array, a validação falhará:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

Em geral, você deve sempre especificar as chaves de array que podem estar presentes no seu array. Caso contrário, os métodos `validate` e `validated` do validador retornarão todos os dados validados, incluindo o array e todas as suas chaves, mesmo que essas chaves não tenham sido validadas pelas outras regras de validação de array aninhado.

<a id="validating-nested-array-input"></a>
### Validando Entrada de Array Aninhado

Validar campos de formulário com entrada de array aninhado não precisa ser complicado. Você pode usar a "notação de ponto" para validar atributos dentro de um array. Por exemplo, se a requisição HTTP recebida contiver um campo `photos[profile]`, você pode validá-lo assim:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => ['required', 'image'],
]);
```

Você também pode validar cada elemento de um array. Por exemplo, para validar que cada e-mail de um determinado campo de entrada do tipo array é único, você pode fazer o seguinte:

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => ['email', 'unique:users'],
    'users.*.first_name' => ['required_with:users.*.last_name'],
]);
```

Da mesma forma, você pode usar o caractere `*` ao especificar [mensagens de validação personalizadas nos seus arquivos de idioma](#custom-messages-for-specific-attributes), facilitando o uso de uma única mensagem de validação para campos baseados em array:

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a id="accessing-nested-array-data"></a>
#### Acessando Dados de Array Aninhado

Às vezes, você pode precisar acessar o valor de um determinado elemento de array aninhado ao atribuir regras de validação ao atributo. Você pode fazer isso usando o método `Rule::forEach`. O método `forEach` aceita um closure que será invocado para cada iteração do atributo do tipo array sob validação e receberá o valor do atributo e o nome explícito e totalmente expandido do atributo. O closure deve retornar um array de regras a serem atribuídas ao elemento do array:

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a id="error-message-indexes-and-positions"></a>
### Índices e Posições nas Mensagens de Erro

Ao validar arrays, você pode querer fazer referência ao índice ou à posição de um item específico que falhou na validação, dentro da mensagem de erro exibida pela sua aplicação. Para isso, você pode incluir os placeholders `:index` (começa em `0`), `:position` (começa em `1`) ou `:ordinal-position` (começa em `1st`) na sua [mensagem de validação personalizada](#manual-customizing-the-error-messages):

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => ['required'],
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

Com base no exemplo acima, a validação falhará e o usuário verá o seguinte erro: _"Please describe photo #2."_

Se necessário, você pode fazer referência a índices e posições mais profundamente aninhados por meio de `second-index`, `second-position`, `third-index`, `third-position` etc.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a id="validating-files"></a>
## Validando Arquivos

O Laravel oferece uma variedade de regras de validação que podem ser usadas para validar arquivos enviados, como `mimes`, `image`, `min` e `max`. Embora você possa especificar essas regras individualmente ao validar arquivos, o Laravel também oferece um construtor fluente de regras de validação de arquivo que pode ser conveniente:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```

<a id="validating-files-file-types"></a>
#### Validando Tipos de Arquivo

Embora você só precise especificar as extensões ao invocar o método `types`, esse método realmente valida o tipo MIME do arquivo lendo o conteúdo do arquivo e adivinhando o seu tipo MIME. Uma lista completa de tipos MIME e suas extensões correspondentes pode ser encontrada no seguinte local:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a id="validating-files-file-sizes"></a>
#### Validando Tamanhos de Arquivo

Por conveniência, tamanhos mínimos e máximos de arquivo podem ser especificados como uma string com um sufixo indicando a unidade de tamanho do arquivo. Os sufixos `kb`, `mb`, `gb` e `tb` são suportados:

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a id="validating-files-image-files"></a>
#### Validando Arquivos de Imagem

Se a sua aplicação aceitar imagens enviadas pelos seus usuários, você pode usar o método construtor `image` da regra `File` para garantir que o arquivo sob validação seja uma imagem (jpg, jpeg, png, bmp, gif, webp, avif, heic ou heif).

Além disso, a regra `dimensions` pode ser usada para limitar as dimensões da imagem:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```

> **Nota:**
> Mais informações sobre a validação de dimensões de imagem podem ser encontradas na [documentação da regra dimensions](#rule-dimensions).

> **Aviso:**
> Por padrão, a regra `image` não permite arquivos SVG devido à possibilidade de vulnerabilidades XSS. Se você precisar permitir arquivos SVG, pode passar `allowSvg: true` à regra `image`: `File::image(allowSvg: true)`.

<a id="validating-files-image-dimensions"></a>
#### Validando Dimensões de Imagem

Você também pode validar as dimensões de uma imagem. Por exemplo, para validar que uma imagem enviada tem pelo menos 1000 pixels de largura e 500 pixels de altura, você pode usar a regra `dimensions`:

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
);
```

> **Nota:**
> Mais informações sobre a validação de dimensões de imagem podem ser encontradas na [documentação da regra dimensions](#rule-dimensions).

<a id="validating-passwords"></a>
## Validando Senhas

Para garantir que as senhas tenham um nível adequado de complexidade, você pode usar o objeto de regra `Password` do Laravel:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

O objeto de regra `Password` permite personalizar facilmente os requisitos de complexidade de senha da sua aplicação, como exigir que as senhas tenham pelo menos uma letra, um número, um símbolo ou caracteres com maiúsculas e minúsculas misturadas:

```php
// Require at least 8 characters...
Password::min(8);

// Require at most 256 characters...
Password::min(16)->max(256);

// Require at least one letter...
Password::min(8)->letters();

// Require at least one uppercase and one lowercase letter...
Password::min(8)->mixedCase();

// Require at least one number...
Password::min(8)->numbers();

// Require at least one symbol...
Password::min(8)->symbols();
```

Além disso, você pode garantir que uma senha não tenha sido comprometida em um vazamento público de dados de senhas usando o método `uncompromised`:

```php
Password::min(8)->uncompromised();
```

Internamente, o objeto de regra `Password` usa o modelo [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) para determinar se uma senha foi vazada pelo serviço [haveibeenpwned.com](https://haveibeenpwned.com) sem comprometer a privacidade ou a segurança do usuário.

Por padrão, se uma senha aparecer pelo menos uma vez em um vazamento de dados, ela será considerada comprometida. Você pode personalizar esse limite usando o primeiro argumento do método `uncompromised`:

```php
// Ensure the password appears no more than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

Claro, você pode encadear todos os métodos dos exemplos acima:

```php
Password::min(8)
    ->max(256)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised();
```

Você pode converter um objeto de regra `Password` em uma string adequada para o atributo HTML `passwordrules` usando o método `toPasswordRulesString`:

```blade
<input
    type="password"
    name="password"
    autocomplete="new-password"
    passwordrules="{{ Password::defaults()->toPasswordRulesString() }}"
/>
```

<a id="defining-default-password-rules"></a>
#### Definindo Regras Padrão de Senha

Você pode achar conveniente especificar as regras de validação padrão para senhas em um único local da sua aplicação. Você pode fazer isso facilmente usando o método `Password::defaults`, que aceita um closure. O closure fornecido ao método `defaults` deve retornar a configuração padrão da regra Password. Normalmente, o método `defaults` deve ser chamado dentro do método `boot` de um dos provedores de serviço da sua aplicação:

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```

Então, quando quiser aplicar as regras padrão a uma determinada senha em validação, você pode invocar o método `defaults` sem argumentos:

```php
'password' => ['required', Password::defaults()],
```

Ocasionalmente, você pode querer anexar regras de validação adicionais às suas regras padrão de validação de senha. Você pode usar o método `rules` para isso:

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a id="custom-validation-rules"></a>
## Regras de Validação Personalizadas

<a id="using-rule-objects"></a>
### Usando Objetos de Regra

O Laravel oferece uma variedade de regras de validação úteis; no entanto, você pode querer especificar algumas regras próprias. Um dos métodos para registrar regras de validação personalizadas é usar objetos de regra. Para gerar um novo objeto de regra, você pode usar o comando Artisan `make:rule`. Vamos usar esse comando para gerar uma regra que verifica se uma string está em letras maiúsculas. O Laravel colocará a nova regra no diretório `app/Rules`. Se esse diretório não existir, o Laravel o criará quando você executar o comando Artisan para criar sua regra:

```shell
php artisan make:rule Uppercase
```

Depois que a regra for criada, estamos prontos para definir seu comportamento. Um objeto de regra contém um único método: `validate`. Esse método recebe o nome do atributo, seu valor e um callback que deve ser invocado em caso de falha, com a mensagem de erro de validação:

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

Depois que a regra for definida, você pode anexá-la a um validador passando uma instância do objeto de regra junto com suas outras regras de validação:

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### Traduzindo Mensagens de Validação

Em vez de fornecer uma mensagem de erro literal ao closure `$fail`, você também pode fornecer uma [chave de string de tradução](../localization/) e instruir o Laravel a traduzir a mensagem de erro:

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

Se necessário, você pode fornecer substituições de placeholders e o idioma preferido como primeiro e segundo argumentos do método `translate`:

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### Acessando Dados Adicionais

Se a sua classe de regra de validação personalizada precisar acessar todos os outros dados sob validação, ela pode implementar a interface `Illuminate\Contracts\Validation\DataAwareRule`. Essa interface exige que sua classe defina um método `setData`. Esse método será invocado automaticamente pelo Laravel (antes de a validação prosseguir) com todos os dados sob validação:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```

Ou, se a sua regra de validação precisar acessar a instância do validador que está executando a validação, você pode implementar a interface `ValidatorAwareRule`:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a id="using-closures"></a>
### Usando Closures

Se você só precisar da funcionalidade de uma regra personalizada uma vez em toda a sua aplicação, pode usar um closure em vez de um objeto de regra. O closure recebe o nome do atributo, o valor do atributo e um callback `$fail` que deve ser chamado caso a validação falhe:

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```

<a id="implicit-rules"></a>
### Regras Implícitas

Por padrão, quando um atributo sob validação não está presente ou contém uma string vazia, as regras de validação normais, incluindo as regras personalizadas, não são executadas. Por exemplo, a regra [unique](#rule-unique) não será executada em uma string vazia:

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => ['unique:users,name']];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

Para que uma regra personalizada seja executada mesmo quando um atributo está vazio, a regra deve implicar que o atributo é obrigatório. Para gerar rapidamente um novo objeto de regra implícita, você pode usar o comando Artisan `make:rule` com a opção `--implicit`:

```shell
php artisan make:rule Uppercase --implicit
```

> **Aviso:**
> Uma regra "implícita" apenas _implica_ que o atributo é obrigatório. Cabe a você decidir se ela realmente invalida um atributo ausente ou vazio.
