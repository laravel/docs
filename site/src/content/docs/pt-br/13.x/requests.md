---
title: "Requisições HTTP"
---

- [Introdução](#introduction)
- [Interagindo com a Requisição](#interacting-with-the-request)
    - [Acessando a Requisição](#accessing-the-request)
    - [Caminho, Host e Método da Requisição](#request-path-and-method)
    - [Cabeçalhos da Requisição](#request-headers)
    - [Endereço IP da Requisição](#request-ip-address)
    - [Negociação de Conteúdo](#content-negotiation)
    - [Requisições PSR-7](#psr7-requests)
- [Entrada](#input)
    - [Recuperando Entrada](#retrieving-input)
    - [Presença de Entrada](#input-presence)
    - [Mesclando Entrada Adicional](#merging-additional-input)
    - [Entrada Antiga](#old-input)
    - [Cookies](#cookies)
    - [Trimming e Normalização de Entrada](#input-trimming-and-normalization)
- [Arquivos](#files)
    - [Recuperando Arquivos Enviados](#retrieving-uploaded-files)
    - [Armazenando Arquivos Enviados](#storing-uploaded-files)
- [Configurando Proxies Confiáveis](#configuring-trusted-proxies)
- [Configurando Hosts Confiáveis](#configuring-trusted-hosts)

<a id="introduction"></a>
## Introdução

A classe `Illuminate\Http\Request` do Laravel fornece uma maneira orientada a objetos de interagir com a requisição HTTP atual sendo tratada pela sua aplicação, bem como de recuperar a entrada, os cookies e os arquivos que foram enviados com a requisição.

<a id="interacting-with-the-request"></a>
## Interagindo com a Requisição

<a id="accessing-the-request"></a>
### Acessando a Requisição

Para obter uma instância da requisição HTTP atual via injeção de dependência, você deve declarar o tipo (type-hint) da classe `Illuminate\Http\Request` no closure da sua rota ou no método do seu controller. A instância da requisição recebida será injetada automaticamente pelo [service container](../container/) do Laravel:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // Store the user...

        return redirect('/users');
    }
}
```

Como mencionado, você também pode declarar o tipo (type-hint) da classe `Illuminate\Http\Request` em um closure de rota. O service container injetará automaticamente a requisição recebida no closure quando ele for executado:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a id="dependency-injection-route-parameters"></a>
#### Injeção de Dependência e Parâmetros de Rota

Se o método do seu controller também estiver esperando entrada de um parâmetro de rota, você deve listar seus parâmetros de rota após suas outras dependências. Por exemplo, se sua rota estiver definida assim:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

Você ainda pode declarar o tipo (type-hint) de `Illuminate\Http\Request` e acessar seu parâmetro de rota `id` definindo seu método de controller da seguinte forma:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```

<a id="request-path-and-method"></a>
### Caminho, Host e Método da Requisição

A instância `Illuminate\Http\Request` fornece uma variedade de métodos para examinar a requisição HTTP recebida e estende a classe `Symfony\Component\HttpFoundation\Request`. Discutiremos alguns dos métodos mais importantes a seguir.

<a id="retrieving-the-request-path"></a>
#### Recuperando o Caminho da Requisição

O método `path` retorna as informações de caminho da requisição. Assim, se a requisição recebida for direcionada a `http://example.com/foo/bar`, o método `path` retornará `foo/bar`:

```php
$uri = $request->path();
```

<a id="inspecting-the-request-path"></a>
#### Inspecionando o Caminho / Rota da Requisição

O método `is` permite verificar se o caminho da requisição recebida corresponde a um determinado padrão. Você pode usar o caractere `*` como curinga ao utilizar este método:

```php
if ($request->is('admin/*')) {
    // ...
}
```

Usando o método `routeIs`, você pode determinar se a requisição recebida corresponde a uma [rota nomeada](../routing/#named-routes):

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a id="retrieving-the-request-url"></a>
#### Recuperando a URL da Requisição

Para recuperar a URL completa da requisição recebida, você pode usar os métodos `url` ou `fullUrl`. O método `url` retornará a URL sem a query string, enquanto o método `fullUrl` inclui a query string:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

Se você quiser anexar dados de query string à URL atual, pode chamar o método `fullUrlWithQuery`. Este método mescla o array de variáveis de query string fornecido com a query string atual:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

Se você quiser obter a URL atual sem um determinado parâmetro de query string, pode utilizar o método `fullUrlWithoutQuery`:

```php
$request->fullUrlWithoutQuery(['type']);
```

<a id="retrieving-the-request-host"></a>
#### Recuperando o Host da Requisição

Você pode recuperar o "host" da requisição recebida por meio dos métodos `host`, `httpHost` e `schemeAndHttpHost`:

```php
// http://localhost:8000
$request->host(); // localhost
$request->httpHost(); // localhost:8000
$request->schemeAndHttpHost(); // http://localhost:8000
```

<a id="retrieving-the-request-method"></a>
#### Recuperando o Método da Requisição

O método `method` retornará o verbo HTTP da requisição. Você pode usar o método `isMethod` para verificar se o verbo HTTP corresponde a uma determinada string:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a id="request-headers"></a>
### Cabeçalhos da Requisição

Você pode recuperar um cabeçalho de requisição a partir da instância `Illuminate\Http\Request` usando o método `header`. Se o cabeçalho não estiver presente na requisição, `null` será retornado. No entanto, o método `header` aceita um segundo argumento opcional que será retornado se o cabeçalho não estiver presente na requisição:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

O método `hasHeader` pode ser usado para determinar se a requisição contém um determinado cabeçalho:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

Por conveniência, o método `bearerToken` pode ser usado para recuperar um token bearer do cabeçalho `Authorization`. Se nenhum cabeçalho desse tipo estiver presente, uma string vazia será retornada:

```php
$token = $request->bearerToken();
```

<a id="request-ip-address"></a>
### Endereço IP da Requisição

O método `ip` pode ser usado para recuperar o endereço IP do cliente que fez a requisição à sua aplicação:

```php
$ipAddress = $request->ip();
```

Se você quiser recuperar um array de endereços IP, incluindo todos os endereços IP de clientes que foram encaminhados por proxies, pode usar o método `ips`. O endereço IP "original" do cliente estará no final do array:

```php
$ipAddresses = $request->ips();
```

Em geral, os endereços IP devem ser considerados entrada não confiável e controlada pelo usuário, e usados apenas para fins informativos.

<a id="content-negotiation"></a>
### Negociação de Conteúdo

O Laravel fornece vários métodos para inspecionar os tipos de conteúdo solicitados pela requisição recebida por meio do cabeçalho `Accept`. Primeiro, o método `getAcceptableContentTypes` retornará um array contendo todos os tipos de conteúdo aceitos pela requisição:

```php
$contentTypes = $request->getAcceptableContentTypes();
```

O método `accepts` aceita um array de tipos de conteúdo e retorna `true` se algum dos tipos de conteúdo for aceito pela requisição. Caso contrário, `false` será retornado:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

Você pode usar o método `prefers` para determinar qual tipo de conteúdo, dentre um determinado array de tipos de conteúdo, é mais preferido pela requisição. Se nenhum dos tipos de conteúdo fornecidos for aceito pela requisição, `null` será retornado:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

Como muitas aplicações servem apenas HTML ou JSON, você pode usar o método `expectsJson` para determinar rapidamente se a requisição recebida espera uma resposta JSON:

```php
if ($request->expectsJson()) {
    // ...
}
```

Se você precisar determinar se a requisição prefere especificamente Markdown ou aceitará Markdown entre outros tipos de conteúdo, como ao servir agentes de IA ou outros clientes que consomem respostas em Markdown, você pode usar os métodos `wantsMarkdown` e `acceptsMarkdown`:

```php
if ($request->wantsMarkdown()) {
    // The client's most preferred content type is text/markdown...
}

if ($request->acceptsMarkdown()) {
    // The client accepts Markdown responses...
}
```

<a id="psr7-requests"></a>
### Requisições PSR-7

O [padrão PSR-7](https://www.php-fig.org/psr/psr-7/) especifica interfaces para mensagens HTTP, incluindo requisições e respostas. Se você quiser obter uma instância de uma requisição PSR-7 em vez de uma requisição do Laravel, primeiro precisará instalar algumas bibliotecas. O Laravel usa o componente *Symfony HTTP Message Bridge* para converter requisições e respostas típicas do Laravel em implementações compatíveis com PSR-7:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

Depois de instalar essas bibliotecas, você pode obter uma requisição PSR-7 declarando o tipo (type-hint) da interface da requisição no closure da sua rota ou no método do seu controller:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> **Note:**
> Se você retornar uma instância de resposta PSR-7 de uma rota ou controller, ela será automaticamente convertida de volta para uma instância de resposta do Laravel e exibida pelo framework.

<a id="input"></a>
## Entrada

<a id="retrieving-input"></a>
### Recuperando Entrada

<a id="retrieving-all-input-data"></a>
#### Recuperando Todos os Dados de Entrada

Você pode recuperar todos os dados de entrada da requisição recebida como um `array` usando o método `all`. Este método pode ser usado independentemente de a requisição recebida ser de um formulário HTML ou de uma requisição XHR:

```php
$input = $request->all();
```

Usando o método `collect`, você pode recuperar todos os dados de entrada da requisição recebida como uma [collection](../collections/):

```php
$input = $request->collect();
```

O método `collect` também permite que você recupere um subconjunto da entrada da requisição recebida como uma collection:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a id="retrieving-an-input-value"></a>
#### Recuperando um Valor de Entrada

Usando alguns métodos simples, você pode acessar toda a entrada do usuário a partir da sua instância `Illuminate\Http\Request` sem se preocupar com qual verbo HTTP foi usado na requisição. Independentemente do verbo HTTP, o método `input` pode ser usado para recuperar a entrada do usuário:

```php
$name = $request->input('name');
```

Você pode passar um valor padrão como segundo argumento para o método `input`. Esse valor será retornado se o valor de entrada solicitado não estiver presente na requisição:

```php
$name = $request->input('name', 'Sally');
```

Ao trabalhar com formulários que contêm entradas em array, use a notação de "ponto" para acessar os arrays:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

Você pode chamar o método `input` sem nenhum argumento para recuperar todos os valores de entrada como um array associativo:

```php
$input = $request->input();
```

<a id="retrieving-input-from-the-query-string"></a>
#### Recuperando Entrada da Query String

Enquanto o método `input` recupera valores de todo o payload da requisição (incluindo a query string), o método `query` recuperará apenas valores da query string:

```php
$name = $request->query('name');
```

Se os dados do valor da query string solicitada não estiverem presentes, o segundo argumento deste método será retornado:

```php
$name = $request->query('name', 'Helen');
```

Você pode chamar o método `query` sem nenhum argumento para recuperar todos os valores da query string como um array associativo:

```php
$query = $request->query();
```

<a id="retrieving-json-input-values"></a>
#### Recuperando Valores de Entrada JSON

Ao enviar requisições JSON para sua aplicação, você pode acessar os dados JSON por meio do método `input`, desde que o cabeçalho `Content-Type` da requisição esteja devidamente definido como `application/json`. Você pode até usar a sintaxe de "ponto" para recuperar valores aninhados dentro de arrays / objetos JSON:

```php
$name = $request->input('user.name');
```

<a id="retrieving-stringable-input-values"></a>
#### Recuperando Valores de Entrada Stringable

Em vez de recuperar os dados de entrada da requisição como uma `string` primitiva, você pode usar o método `string` para recuperar os dados da requisição como uma instância de [Illuminate\Support\Stringable](../strings/):

```php
$name = $request->string('name')->trim();
```

<a id="retrieving-integer-input-values"></a>
#### Recuperando Valores de Entrada Inteiros

Para recuperar valores de entrada como inteiros, você pode usar o método `integer`. Este método tentará fazer o cast do valor de entrada para um inteiro. Se a entrada não estiver presente, ele retornará o valor padrão que você especificar. Isso é particularmente útil para paginação ou outras entradas numéricas:

```php
$perPage = $request->integer('per_page');
```

<a id="retrieving-boolean-input-values"></a>
#### Recuperando Valores de Entrada Booleanos

Ao lidar com elementos HTML como checkboxes, sua aplicação pode receber valores "truthy" que na verdade são strings. Por exemplo, "true" ou "on". Por conveniência, você pode usar o método `boolean` para recuperar esses valores como booleanos. O método `boolean` retorna `true` para 1, "1", true, "true", "on" e "yes". Todos os outros valores retornarão `false`:

```php
$archived = $request->boolean('archived');
```

<a id="retrieving-array-input-values"></a>
#### Recuperando Valores de Entrada em Array

Valores de entrada contendo arrays podem ser recuperados usando o método `array`. Este método sempre fará o cast do valor de entrada para um array. Se a requisição não contiver um valor de entrada com o nome fornecido, um array vazio será retornado:

```php
$versions = $request->array('versions');
```

<a id="retrieving-date-input-values"></a>
#### Recuperando Valores de Entrada de Data

Por conveniência, valores de entrada contendo datas / horas podem ser recuperados como instâncias de Carbon usando o método `date`. Se a requisição não contiver um valor de entrada com o nome fornecido, `null` será retornado:

```php
$birthday = $request->date('birthday');
```

O segundo e o terceiro argumentos aceitos pelo método `date` podem ser usados para especificar o formato e o fuso horário da data, respectivamente:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

Se o valor de entrada estiver presente, mas tiver um formato inválido, uma exceção `InvalidArgumentException` será lançada; portanto, é recomendável validar a entrada antes de invocar o método `date`.

<a id="retrieving-interval-input-values"></a>
#### Recuperando Valores de Entrada de Intervalo

Valores de entrada contendo durações podem ser recuperados como instâncias de `CarbonInterval` usando o método `interval`. Se a requisição não contiver um valor de entrada com o nome fornecido, `null` será retornado:

```php
$duration = $request->interval('duration');
```

Se o valor de entrada for numérico, você pode fornecer uma unidade como segundo argumento. A unidade pode ser uma string como `second`, `minute` ou `day`, ou uma instância da enum `Carbon\Unit`:

```php
use Carbon\Unit;

$timeout = $request->interval('timeout', 'second');

$delay = $request->interval('delay', Unit::Minute);
```

Se o valor de entrada estiver presente, mas tiver um formato inválido, uma exceção `InvalidArgumentException` será lançada; portanto, é recomendável validar a entrada antes de invocar o método `interval`.

<a id="retrieving-enum-input-values"></a>
#### Recuperando Valores de Entrada de Enum

Valores de entrada que correspondem a [enums do PHP](https://www.php.net/manual/en/language.types.enumerations.php) também podem ser recuperados da requisição. Se a requisição não contiver um valor de entrada com o nome fornecido ou a enum não tiver um valor de backing que corresponda ao valor de entrada, `null` será retornado. O método `enum` aceita o nome do valor de entrada e a classe da enum como seu primeiro e segundo argumentos:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

Você também pode fornecer um valor padrão que será retornado se o valor estiver ausente ou for inválido:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

Se o valor de entrada for um array de valores que correspondem a uma enum do PHP, você pode usar o método `enums` para recuperar o array de valores como instâncias de enum:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a id="retrieving-input-via-dynamic-properties"></a>
#### Recuperando Entrada via Propriedades Dinâmicas

Você também pode acessar a entrada do usuário usando propriedades dinâmicas na instância `Illuminate\Http\Request`. Por exemplo, se um dos formulários da sua aplicação contiver um campo `name`, você pode acessar o valor do campo assim:

```php
$name = $request->name;
```

Ao usar propriedades dinâmicas, o Laravel procurará primeiro o valor do parâmetro no payload da requisição. Se não estiver presente, o Laravel procurará o campo nos parâmetros da rota correspondente.

<a id="retrieving-a-portion-of-the-input-data"></a>
#### Recuperando uma Porção dos Dados de Entrada

Se você precisar recuperar um subconjunto dos dados de entrada, pode usar os métodos `only` e `except`. Ambos os métodos aceitam um único `array` ou uma lista dinâmica de argumentos:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> **Warning:**
> O método `only` retorna todos os pares chave / valor que você solicitar; no entanto, ele não retornará os pares chave / valor que não estiverem presentes na requisição.

<a id="input-presence"></a>
### Presença de Entrada

Você pode usar o método `has` para determinar se um valor está presente na requisição. O método `has` retorna `true` se o valor estiver presente na requisição:

```php
if ($request->has('name')) {
    // ...
}
```

Quando um array é fornecido, o método `has` determinará se todos os valores especificados estão presentes:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

O método `hasAny` retorna `true` se algum dos valores especificados estiver presente:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

O método `whenHas` executará o closure fornecido se um valor estiver presente na requisição:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

Um segundo closure pode ser passado ao método `whenHas`, que será executado se o valor especificado não estiver presente na requisição:

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

Se você quiser determinar se um valor está presente na requisição e não é uma string vazia, pode usar o método `filled`:

```php
if ($request->filled('name')) {
    // ...
}
```

Se você quiser determinar se um valor está ausente da requisição ou é uma string vazia, pode usar o método `isNotFilled`:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

Quando um array é fornecido, o método `isNotFilled` determinará se todos os valores especificados estão ausentes ou vazios:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

O método `anyFilled` retorna `true` se algum dos valores especificados não for uma string vazia:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

O método `whenFilled` executará o closure fornecido se um valor estiver presente na requisição e não for uma string vazia:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

Um segundo closure pode ser passado ao método `whenFilled`, que será executado se o valor especificado não estiver "filled":

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

Para determinar se uma determinada chave está ausente da requisição, você pode usar os métodos `missing` e `whenMissing`:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a id="merging-additional-input"></a>
### Mesclando Entrada Adicional

Às vezes, você pode precisar mesclar manualmente entrada adicional nos dados de entrada existentes da requisição. Para fazer isso, você pode usar o método `merge`. Se uma determinada chave de entrada já existir na requisição, ela será sobrescrita pelos dados fornecidos ao método `merge`:

```php
$request->merge(['votes' => 0]);
```

O método `mergeIfMissing` pode ser usado para mesclar entrada na requisição se as chaves correspondentes ainda não existirem nos dados de entrada da requisição:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a id="old-input"></a>
### Entrada Antiga

O Laravel permite que você mantenha a entrada de uma requisição durante a requisição seguinte. Esse recurso é particularmente útil para repopular formulários após detectar erros de validação. No entanto, se você estiver usando os [recursos de validação](../validation/) incluídos no Laravel, é possível que não precise usar manualmente esses métodos de flashing de entrada na sessão diretamente, pois alguns dos recursos de validação integrados do Laravel os chamarão automaticamente.

<a id="flashing-input-to-the-session"></a>
#### Flashing de Entrada na Sessão

O método `flash` na classe `Illuminate\Http\Request` fará o flash da entrada atual para a [sessão](../session/), de modo que ela fique disponível durante a próxima requisição do usuário à aplicação:

```php
$request->flash();
```

Você também pode usar os métodos `flashOnly` e `flashExcept` para fazer o flash de um subconjunto dos dados da requisição para a sessão. Esses métodos são úteis para manter informações sensíveis, como senhas, fora da sessão:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a id="flashing-input-then-redirecting"></a>
#### Flashing de Entrada e Redirecionamento

Como frequentemente você vai querer fazer o flash da entrada para a sessão e, em seguida, redirecionar para a página anterior, você pode encadear facilmente o flashing de entrada em um redirecionamento usando o método `withInput`:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a id="retrieving-old-input"></a>
#### Recuperando Entrada Antiga

Para recuperar a entrada que teve flash na requisição anterior, invoque o método `old` em uma instância de `Illuminate\Http\Request`. O método `old` extrairá os dados de entrada que tiveram flash anteriormente da [sessão](../session/):

```php
$username = $request->old('username');
```

O Laravel também fornece um helper global `old`. Se você estiver exibindo entrada antiga dentro de um [template Blade](../blade/), é mais conveniente usar o helper `old` para repopular o formulário. Se não existir entrada antiga para o campo fornecido, `null` será retornado:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a id="cookies"></a>
### Cookies

<a id="retrieving-cookies-from-requests"></a>
#### Recuperando Cookies das Requisições

Todos os cookies criados pelo framework Laravel são criptografados e assinados com um código de autenticação, o que significa que serão considerados inválidos se tiverem sido alterados pelo cliente. Para recuperar um valor de cookie da requisição, use o método `cookie` em uma instância de `Illuminate\Http\Request`:

```php
$value = $request->cookie('name');
```

<a id="input-trimming-and-normalization"></a>
## Trimming e Normalização de Entrada

Por padrão, o Laravel inclui os middleware `Illuminate\Foundation\Http\Middleware\TrimStrings` e `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` na pilha de middleware global da sua aplicação. Esses middleware aplicarão automaticamente trim a todos os campos string recebidos na requisição, bem como converterão quaisquer campos string vazios para `null`. Isso permite que você não precise se preocupar com essas questões de normalização em suas rotas e controllers.

#### Desativando a Normalização de Entrada

Se você quiser desativar esse comportamento para todas as requisições, pode remover os dois middleware da pilha de middleware da sua aplicação invocando o método `$middleware->remove` no arquivo `bootstrap/app.php` da sua aplicação:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

Se você quiser desativar o trimming de strings e a conversão de strings vazias para um subconjunto de requisições à sua aplicação, pode usar os métodos de middleware `trimStrings` e `convertEmptyStringsToNull` dentro do arquivo `bootstrap/app.php` da sua aplicação. Ambos os métodos aceitam um array de closures, que devem retornar `true` ou `false` para indicar se a normalização de entrada deve ser ignorada:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a id="files"></a>
## Arquivos

<a id="retrieving-uploaded-files"></a>
### Recuperando Arquivos Enviados

Você pode recuperar arquivos enviados a partir de uma instância `Illuminate\Http\Request` usando o método `file` ou usando propriedades dinâmicas. O método `file` retorna uma instância da classe `Illuminate\Http\UploadedFile`, que estende a classe `SplFileInfo` do PHP e fornece uma variedade de métodos para interagir com o arquivo:

```php
$file = $request->file('photo');

$file = $request->photo;
```

Você pode determinar se um arquivo está presente na requisição usando o método `hasFile`:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

Se o arquivo enviado for uma imagem que você precisa manipular antes de armazenar, você pode usar o método `image` para recuperar uma instância de `Illuminate\Image\Image`, ou `null` se o arquivo não estiver presente:

```php
$image = $request->image('photo');
```

Para mais informações sobre a manipulação de imagens, consulte a [documentação completa de manipulação de imagens](../images/).

<a id="validating-successful-uploads"></a>
#### Validando Uploads Bem-Sucedidos

Além de verificar se o arquivo está presente, você pode verificar se não houve problemas ao enviar o arquivo por meio do método `isValid`:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a id="file-paths-extensions"></a>
#### Caminhos e Extensões de Arquivo

A classe `UploadedFile` também contém métodos para acessar o caminho totalmente qualificado do arquivo e sua extensão. O método `extension` tentará adivinhar a extensão do arquivo com base em seu conteúdo. Essa extensão pode ser diferente da extensão fornecida pelo cliente:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a id="other-file-methods"></a>
#### Outros Métodos de Arquivo

Há uma variedade de outros métodos disponíveis nas instâncias de `UploadedFile`. Confira a [documentação da API da classe](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) para mais informações sobre esses métodos.

<a id="storing-uploaded-files"></a>
### Armazenando Arquivos Enviados

Para armazenar um arquivo enviado, você normalmente usará um dos seus [sistemas de arquivos](../filesystem/) configurados. A classe `UploadedFile` possui um método `store` que moverá um arquivo enviado para um dos seus discos, que pode ser um local no seu sistema de arquivos local ou um local de armazenamento em nuvem como o Amazon S3.

O método `store` aceita o caminho onde o arquivo deve ser armazenado em relação ao diretório raiz configurado do sistema de arquivos. Esse caminho não deve conter um nome de arquivo, pois um ID único será gerado automaticamente para servir como nome do arquivo.

O método `store` também aceita um segundo argumento opcional para o nome do disco que deve ser usado para armazenar o arquivo. O método retornará o caminho do arquivo em relação à raiz do disco:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

Se você não quiser que um nome de arquivo seja gerado automaticamente, pode usar o método `storeAs`, que aceita o caminho, o nome do arquivo e o nome do disco como seus argumentos:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> **Note:**
> Para mais informações sobre o armazenamento de arquivos no Laravel, confira a [documentação completa de armazenamento de arquivos](../filesystem/).

<a id="configuring-trusted-proxies"></a>
## Configurando Proxies Confiáveis

Ao executar suas aplicações atrás de um load balancer que termina certificados TLS / SSL, você pode notar que sua aplicação às vezes não gera links HTTPS ao usar o helper `url`. Normalmente, isso ocorre porque sua aplicação está recebendo tráfego encaminhado do seu load balancer na porta 80 e não sabe que deveria gerar links seguros.

Para resolver isso, você pode habilitar o middleware `Illuminate\Http\Middleware\TrustProxies` que está incluído na sua aplicação Laravel, o que permite personalizar rapidamente os load balancers ou proxies que devem ser confiáveis para sua aplicação. Seus proxies confiáveis devem ser especificados usando o método de middleware `trustProxies` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

Além de configurar os proxies confiáveis, você também pode configurar os cabeçalhos de proxy que devem ser confiáveis:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> **Note:**
> Se você estiver usando o AWS Elastic Load Balancing, o valor de `headers` deve ser `Request::HEADER_X_FORWARDED_AWS_ELB`. Se seu load balancer usar o cabeçalho padrão `Forwarded` da [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4), o valor de `headers` deve ser `Request::HEADER_FORWARDED`. Para mais informações sobre as constantes que podem ser usadas no valor de `headers`, confira a documentação do Symfony sobre [confiar em proxies](https://symfony.com/doc/current/deployment/proxies.html).

<a id="trusting-all-proxies"></a>
#### Confiando em Todos os Proxies

Se você estiver usando o Amazon AWS ou outro provedor de load balancer "na nuvem", pode não saber os endereços IP dos seus balanceadores reais. Nesse caso, você pode usar `*` para confiar em todos os proxies:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a id="configuring-trusted-hosts"></a>
## Configurando Hosts Confiáveis

Por padrão, o Laravel responderá a todas as requisições que receber, independentemente do conteúdo do cabeçalho `Host` da requisição HTTP. Além disso, o valor do cabeçalho `Host` será usado ao gerar URLs absolutas para sua aplicação durante uma requisição web.

Normalmente, você deve configurar seu servidor web, como Nginx ou Apache, para enviar à sua aplicação apenas requisições que correspondam a um determinado hostname. No entanto, se você não tiver a capacidade de personalizar seu servidor web diretamente e precisar instruir o Laravel a responder apenas a certos hostnames, pode fazê-lo habilitando o middleware `Illuminate\Http\Middleware\TrustHosts` para sua aplicação.

Para habilitar o middleware `TrustHosts`, você deve invocar o método de middleware `trustHosts` no arquivo `bootstrap/app.php` da sua aplicação. Usando o argumento `at` deste método, você pode especificar os hostnames aos quais sua aplicação deve responder. A string do hostname é tratada como uma expressão regular. Requisições recebidas com outros cabeçalhos `Host` serão rejeitadas:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

Por padrão, requisições provenientes de subdomínios da URL da aplicação também são automaticamente confiáveis. Se você quiser desativar esse comportamento, pode usar o argumento `subdomains`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

Se você precisar acessar os arquivos de configuração ou o banco de dados da sua aplicação para determinar seus hosts confiáveis, pode fornecer um closure ao argumento `at`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
