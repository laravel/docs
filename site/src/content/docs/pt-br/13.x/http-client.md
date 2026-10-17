---
title: "Cliente HTTP"
---

- [Introdução](#introduction)
- [Fazendo Requisições](#making-requests)
    - [Dados da Requisição](#request-data)
    - [Cabeçalhos](#headers)
    - [Autenticação](#authentication)
    - [Timeout](#timeout)
    - [Novas Tentativas](#retries)
    - [Tratamento de Erros](#error-handling)
    - [Middleware do Guzzle](#guzzle-middleware)
    - [Opções do Guzzle](#guzzle-options)
- [Requisições Concorrentes](#concurrent-requests)
    - [Pool de Requisições](#request-pooling)
    - [Agrupamento de Requisições](#request-batching)
- [Macros](#macros)
- [Testes](#testing)
    - [Simulando Respostas](#faking-responses)
    - [Inspecionando Requisições](#inspecting-requests)
    - [Prevenindo Requisições Dispersas](#preventing-stray-requests)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

O Laravel fornece uma API expressiva e mínima em torno do [cliente HTTP Guzzle](http://docs.guzzlephp.org/en/stable/), permitindo que você faça rapidamente requisições HTTP de saída para se comunicar com outras aplicações web. O wrapper do Laravel em torno do Guzzle é focado nos casos de uso mais comuns e em uma experiência maravilhosa para o desenvolvedor.

<a id="making-requests"></a>
## Fazendo Requisições

Para fazer requisições, você pode usar os métodos `head`, `get`, `post`, `put`, `patch` e `delete` fornecidos pela facade `Http`. Primeiro, vamos examinar como fazer uma requisição `GET` básica para outra URL:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

O método `get` retorna uma instância de `Illuminate\Http\Client\Response`, que fornece uma variedade de métodos que podem ser usados para inspecionar a resposta:

```php
$response->body() : string;
$response->json($key = null, $default = null, $flags = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

O objeto `Illuminate\Http\Client\Response` também implementa a interface PHP `ArrayAccess`, permitindo que você acesse os dados JSON da resposta diretamente na resposta:

```php
return Http::get('http://example.com/users/1')['name'];
```

Além dos métodos de resposta listados acima, os seguintes métodos podem ser usados para determinar se a resposta possui um código de status específico:

```php
$response->ok() : bool;                  // 200 OK
$response->created() : bool;             // 201 Created
$response->accepted() : bool;            // 202 Accepted
$response->noContent() : bool;           // 204 No Content
$response->movedPermanently() : bool;    // 301 Moved Permanently
$response->found() : bool;               // 302 Found
$response->badRequest() : bool;          // 400 Bad Request
$response->unauthorized() : bool;        // 401 Unauthorized
$response->paymentRequired() : bool;     // 402 Payment Required
$response->forbidden() : bool;           // 403 Forbidden
$response->notFound() : bool;            // 404 Not Found
$response->requestTimeout() : bool;      // 408 Request Timeout
$response->conflict() : bool;            // 409 Conflict
$response->unprocessableEntity() : bool; // 422 Unprocessable Entity
$response->tooManyRequests() : bool;     // 429 Too Many Requests
$response->serverError() : bool;         // >= 500 Server Error
```

<a id="uri-templates"></a>
#### Templates de URI

O cliente HTTP também permite que você construa URLs de requisição usando a [especificação de template de URI](https://www.rfc-editor.org/rfc/rfc6570). Para definir os parâmetros de URL que podem ser expandidos pelo seu template de URI, você pode usar o método `withUrlParameters`:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '13.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a id="dumping-requests"></a>
#### Despejando Requisições

Se você quiser despejar a instância da requisição de saída antes de ela ser enviada e encerrar a execução do script, você pode adicionar o método `dd` ao início da definição da sua requisição:

```php
return Http::dd()->get('http://example.com');
```

<a id="request-data"></a>
### Dados da Requisição

Naturalmente, é comum ao fazer requisições `POST`, `PUT` e `PATCH` enviar dados adicionais com sua requisição, então esses métodos aceitam um array de dados como seu segundo argumento. Por padrão, os dados serão enviados usando o content type `application/json`:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a id="get-request-query-parameters"></a>
#### Parâmetros de Query em Requisições GET

Ao fazer requisições `GET`, você pode anexar uma query string diretamente à URL ou passar um array de pares chave / valor como o segundo argumento do método `get`:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

Alternativamente, o método `withQueryParameters` pode ser usado:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a id="sending-form-url-encoded-requests"></a>
#### Enviando Requisições Form URL Encoded

Se você quiser enviar dados usando o content type `application/x-www-form-urlencoded`, você deve chamar o método `asForm` antes de fazer sua requisição:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a id="sending-a-raw-request-body"></a>
#### Enviando um Corpo de Requisição Bruto

Você pode usar o método `withBody` se quiser fornecer um corpo de requisição bruto ao fazer uma requisição. O content type pode ser fornecido através do segundo argumento do método:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a id="multi-part-requests"></a>
#### Requisições Multi-Part

Se você quiser enviar arquivos como requisições multi-part, você deve chamar o método `attach` antes de fazer sua requisição. Este método aceita o nome do arquivo e seu conteúdo. Se necessário, você pode fornecer um terceiro argumento que será considerado o nome do arquivo, enquanto um quarto argumento pode ser usado para fornecer cabeçalhos associados ao arquivo:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

Em vez de passar o conteúdo bruto de um arquivo, você pode passar um recurso de stream:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a id="headers"></a>
### Cabeçalhos

Cabeçalhos podem ser adicionados às requisições usando o método `withHeaders`. Este método `withHeaders` aceita um array de pares chave / valor:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

Você pode usar o método `accept` para especificar o content type que sua aplicação espera em resposta à sua requisição:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

Por conveniência, você pode usar o método `acceptJson` para especificar rapidamente que sua aplicação espera o content type `application/json` em resposta à sua requisição:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

O método `withHeaders` mescla novos cabeçalhos aos cabeçalhos existentes da requisição. Se necessário, você pode substituir todos os cabeçalhos completamente usando o método `replaceHeaders`:

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<a id="authentication"></a>
### Autenticação

Você pode especificar credenciais de autenticação basic e digest usando os métodos `withBasicAuth` e `withDigestAuth`, respectivamente:

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a id="bearer-tokens"></a>
#### Bearer Tokens

Se você quiser adicionar rapidamente um bearer token ao cabeçalho `Authorization` da requisição, você pode usar o método `withToken`:

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a id="timeout"></a>
### Timeout

O método `timeout` pode ser usado para especificar o número máximo de segundos a aguardar por uma resposta. Por padrão, o cliente HTTP atingirá o timeout após 30 segundos:

```php
$response = Http::timeout(3)->get(/* ... */);
```

Se o timeout fornecido for excedido, uma instância de `Illuminate\Http\Client\ConnectionException` será lançada.

Você pode especificar o número máximo de segundos a aguardar ao tentar se conectar a um servidor usando o método `connectTimeout`. O padrão é 10 segundos:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a id="retries"></a>
### Novas Tentativas

Se você quiser que o cliente HTTP tente a requisição novamente automaticamente caso ocorra um erro de cliente ou servidor, você pode usar o método `retry`. O método `retry` aceita o número máximo de vezes que a requisição deve ser tentada e o número de milissegundos que o Laravel deve aguardar entre as tentativas:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

Se você quiser calcular manualmente o número de milissegundos a dormir entre as tentativas, você pode passar uma closure como o segundo argumento do método `retry`:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

Por conveniência, você também pode fornecer um array como o primeiro argumento do método `retry`. Este array será usado para determinar quantos milissegundos dormir entre as tentativas subsequentes:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

Se necessário, você pode passar um terceiro argumento ao método `retry`. O terceiro argumento deve ser um callable que determina se as novas tentativas devem realmente ser efetuadas. Por exemplo, você pode querer tentar a requisição novamente apenas se a requisição inicial encontrar uma `ConnectionException`:

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

Se uma tentativa de requisição falhar, você pode querer fazer uma alteração na requisição antes que uma nova tentativa seja feita. Você pode conseguir isso modificando o argumento de requisição fornecido ao callable que você passou ao método `retry`. Por exemplo, você pode querer tentar a requisição novamente com um novo token de autorização se a primeira tentativa retornar um erro de autenticação:

```php
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;
use Throwable;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Throwable $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

Se todas as requisições falharem, uma instância de `Illuminate\Http\Client\RequestException` será lançada. Se você quiser desabilitar esse comportamento, você pode fornecer um argumento `throw` com valor `false`. Quando desabilitado, a última resposta recebida pelo cliente será retornada após todas as novas tentativas terem sido efetuadas:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> **Aviso:**
> Se todas as requisições falharem devido a um problema de conexão, uma `Illuminate\Http\Client\ConnectionException` ainda será lançada mesmo quando o argumento `throw` estiver definido como `false`.

<a id="error-handling"></a>
### Tratamento de Erros

Diferentemente do comportamento padrão do Guzzle, o wrapper do cliente HTTP do Laravel não lança exceções em erros de cliente ou servidor (respostas de nível `400` e `500` dos servidores). Você pode determinar se um desses erros foi retornado usando os métodos `successful`, `clientError` ou `serverError`:

```php
// Determine if the status code is >= 200 and < 300...
$response->successful();

// Determine if the status code is >= 400...
$response->failed();

// Determine if the response has a 400 level status code...
$response->clientError();

// Determine if the response has a 500 level status code...
$response->serverError();

// Immediately execute the given callback if there was a client or server error...
$response->onError(callable $callback);
```

<a id="throwing-exceptions"></a>
#### Lançando Exceções

Se você tiver uma instância de resposta e quiser lançar uma instância de `Illuminate\Http\Client\RequestException` caso o código de status da resposta indique um erro de cliente ou servidor, você pode usar os métodos `throw` ou `throwIf`:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

// Throw an exception if an error occurred and the given closure resolves to true...
$response->throwIf(fn (Response $response) => true);

// Throw an exception if an error occurred and the given condition is false...
$response->throwUnless($condition);

// Throw an exception if an error occurred and the given closure resolves to false...
$response->throwUnless(fn (Response $response) => false);

// Throw an exception if the response has a specific status code...
$response->throwIfStatus(403);

// Throw an exception unless the response has a specific status code...
$response->throwUnlessStatus(200);

// Throw an exception if a server error occurred (status >= 500)...
$response->throwIfServerError();

// Throw an exception if a client error occurred (status >= 400 and < 500)...
$response->throwIfClientError();

return $response['user']['id'];
```

A instância `Illuminate\Http\Client\RequestException` possui uma propriedade pública `$response` que permitirá que você inspecione a resposta retornada.

O método `throw` retorna a instância de resposta caso nenhum erro tenha ocorrido, permitindo que você encadeie outras operações ao método `throw`:

```php
return Http::post(/* ... */)->throw()->json();
```

Se você quiser executar alguma lógica adicional antes que a exceção seja lançada, você pode passar uma closure ao método `throw`. A exceção será lançada automaticamente após a closure ser invocada, então você não precisa relançar a exceção de dentro da closure:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

Por padrão, as mensagens de `RequestException` são truncadas em 120 caracteres quando registradas em log ou reportadas. Para personalizar ou desabilitar esse comportamento, você pode utilizar os métodos `truncateAt` e `dontTruncate` ao configurar o comportamento registrado da sua aplicação no arquivo `bootstrap/app.php`:

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```

Alternativamente, você pode personalizar o comportamento de truncamento de exceções por requisição usando o método `truncateExceptionsAt`:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a id="guzzle-middleware"></a>
### Middleware do Guzzle

Como o cliente HTTP do Laravel é alimentado pelo Guzzle, você pode tirar proveito do [Middleware do Guzzle](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) para manipular a requisição de saída ou inspecionar a resposta de entrada. Para manipular a requisição de saída, registre um middleware do Guzzle através do método `withRequestMiddleware`:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

Da mesma forma, você pode inspecionar a resposta HTTP de entrada registrando um middleware através do método `withResponseMiddleware`:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```

<a id="global-middleware"></a>
#### Middleware Global

Às vezes, você pode querer registrar um middleware que se aplica a cada requisição de saída e resposta de entrada. Para conseguir isso, você pode usar os métodos `globalRequestMiddleware` e `globalResponseMiddleware`. Normalmente, esses métodos devem ser invocados no método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a id="guzzle-options"></a>
### Opções do Guzzle

Você pode especificar [opções de requisição do Guzzle](http://docs.guzzlephp.org/en/stable/request-options.html) adicionais para uma requisição de saída usando o método `withOptions`. O método `withOptions` aceita um array de pares chave / valor:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a id="global-options"></a>
#### Opções Globais

Para configurar opções padrão para cada requisição de saída, você pode utilizar o método `globalOptions`. Normalmente, este método deve ser invocado a partir do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a id="concurrent-requests"></a>
## Requisições Concorrentes

Às vezes, você pode querer fazer várias requisições HTTP concorrentemente. Em outras palavras, você quer que várias requisições sejam despachadas ao mesmo tempo em vez de emitir as requisições sequencialmente. Isso pode levar a melhorias substanciais de desempenho ao interagir com APIs HTTP lentas.

<a id="request-pooling"></a>
### Pool de Requisições

Felizmente, você pode conseguir isso usando o método `pool`. O método `pool` aceita uma closure que recebe uma instância de `Illuminate\Http\Client\Pool`, permitindo que você adicione facilmente requisições ao pool de requisições para despacho:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->get('http://localhost/first'),
    $pool->get('http://localhost/second'),
    $pool->get('http://localhost/third'),
]);

return $responses[0]->ok() &&
       $responses[1]->ok() &&
       $responses[2]->ok();
```

Como você pode ver, cada instância de resposta pode ser acessada com base na ordem em que foi adicionada ao pool. Se desejar, você pode nomear as requisições usando o método `as`, que permite acessar as respostas correspondentes pelo nome:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

A concorrência máxima do pool de requisições pode ser controlada fornecendo o argumento `concurrency` ao método `pool`. Esse valor determina o número máximo de requisições HTTP que podem estar em trânsito concorrentemente enquanto o pool de requisições é processado:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

Se uma requisição do pool falhar no nível de conexão (por exemplo, um timeout ou falha de DNS), a entrada correspondente no array `$responses` será uma instância de `Illuminate\Http\Client\ConnectionException` em vez de uma instância de `Response`:

```php
foreach ($responses as $response) {
    if ($response instanceof Throwable) {
        // The request failed to connect...
    } elseif ($response->failed()) {
        // The request connected but received an error response...
    }
}
```

<a id="customizing-concurrent-requests"></a>
#### Personalizando Requisições Concorrentes

O método `pool` não pode ser encadeado com outros métodos do cliente HTTP, como os métodos `withHeaders` ou `middleware`. Se você quiser aplicar cabeçalhos ou middleware personalizados às requisições do pool, você deve configurar essas opções em cada requisição no pool:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```

<a id="request-batching"></a>
### Agrupamento de Requisições

Outra forma de trabalhar com requisições concorrentes no Laravel é usar o método `batch`. Assim como o método `pool`, ele aceita uma closure que recebe uma instância de `Illuminate\Http\Client\Batch`, permitindo que você adicione facilmente requisições ao pool de requisições para despacho, mas também permite que você defina callbacks de conclusão:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // The batch has been created but no requests have been initialized...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // An individual request has completed successfully...
})->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // Batch request failure detected...
})->finally(function (Batch $batch, array $results) {
    // The batch has finished executing...
})->send();
```

Assim como o método `pool`, você pode usar o método `as` para nomear suas requisições:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

Depois que um `batch` é iniciado pela chamada do método `send`, você não pode adicionar novas requisições a ele. Tentar fazê-lo resultará no lançamento de uma exceção `Illuminate\Http\Client\BatchInProgressException`.

A concorrência máxima do batch de requisições pode ser controlada através do método `concurrency`. Esse valor determina o número máximo de requisições HTTP que podem estar em trânsito concorrentemente enquanto o batch de requisições é processado:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a id="inspecting-batches"></a>
#### Inspecionando Batches

A instância `Illuminate\Http\Client\Batch` que é fornecida aos callbacks de conclusão do batch possui uma variedade de propriedades e métodos para ajudá-lo a interagir com e inspecionar um determinado batch de requisições:

```php
// The number of requests assigned to the batch...
$batch->totalRequests;

// The number of requests that have not been processed yet...
$batch->pendingRequests;

// The number of requests that have failed...
$batch->failedRequests;

// The number of requests that have been processed thus far...
$batch->processedRequests();

// Indicates if the batch has finished executing...
$batch->finished();

// Indicates if the batch has request failures...
$batch->hasFailures();
```
<a id="deferring-batches"></a>
#### Adiando Batches

Quando o método `defer` é invocado, o batch de requisições não é executado imediatamente. Em vez disso, o Laravel executará o batch depois que a resposta HTTP da requisição atual da aplicação tiver sido enviada ao usuário, mantendo sua aplicação rápida e responsiva:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->defer();
```

<a id="macros"></a>
## Macros

O cliente HTTP do Laravel permite que você defina "macros", que podem servir como um mecanismo fluente e expressivo para configurar caminhos e cabeçalhos de requisição comuns ao interagir com serviços em toda a sua aplicação. Para começar, você pode definir a macro dentro do método `boot` da classe `App\Providers\AppServiceProvider` da sua aplicação:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

Uma vez que sua macro tenha sido configurada, você pode invocá-la de qualquer lugar da sua aplicação para criar uma requisição pendente com a configuração especificada:

```php
$response = Http::github()->get('/');
```

<a id="testing"></a>
## Testes

Muitos serviços do Laravel fornecem funcionalidade para ajudá-lo a escrever testes de forma fácil e expressiva, e o cliente HTTP do Laravel não é exceção. O método `fake` da facade `Http` permite que você instrua o cliente HTTP a retornar respostas stub / fictícias quando requisições forem feitas.

<a id="faking-responses"></a>
### Simulando Respostas

Por exemplo, para instruir o cliente HTTP a retornar respostas vazias com código de status `200` para cada requisição, você pode chamar o método `fake` sem argumentos:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a id="faking-specific-urls"></a>
#### Simulando URLs Específicas

Alternativamente, você pode passar um array ao método `fake`. As chaves do array devem representar padrões de URL que você deseja simular e suas respostas associadas. O caractere `*` pode ser usado como caractere curinga. Você pode usar o método `response` da facade `Http` para construir respostas stub / fictícias para esses endpoints:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

Quaisquer requisições feitas para URLs que não foram simuladas serão realmente executadas. Se você quiser especificar um padrão de URL de fallback que simulará todas as URLs não correspondidas, você pode usar um único caractere `*`:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

Por conveniência, respostas simples de string, JSON e vazias podem ser geradas fornecendo uma string, array ou inteiro como resposta:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a id="faking-connection-exceptions"></a>
#### Simulando Exceções

Às vezes você pode precisar testar o comportamento da sua aplicação caso o cliente HTTP encontre uma `Illuminate\Http\Client\ConnectionException` ao tentar fazer uma requisição. Você pode instruir o cliente HTTP a lançar uma exceção de conexão usando o método `failedConnection`:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

Para testar o comportamento da sua aplicação caso uma `Illuminate\Http\Client\RequestException` seja lançada, você pode usar o método `failedRequest`:

```php
$this->mock(GithubService::class)
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a id="faking-response-sequences"></a>
#### Simulando Sequências de Respostas

Às vezes você pode precisar especificar que uma única URL deve retornar uma série de respostas fictícias em uma ordem específica. Você pode conseguir isso usando o método `Http::sequence` para construir as respostas:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

Quando todas as respostas de uma sequência de respostas forem consumidas, quaisquer requisições adicionais farão com que a sequência de respostas lance uma exceção. Se você quiser especificar uma resposta padrão que deve ser retornada quando uma sequência estiver vazia, você pode usar o método `whenEmpty`:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

Se você quiser simular uma sequência de respostas mas não precisar especificar um padrão de URL específico que deve ser simulado, você pode usar o método `Http::fakeSequence`:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a id="fake-callback"></a>
#### Callback de Simulação

Se você precisar de uma lógica mais complicada para determinar quais respostas retornar para certos endpoints, você pode passar uma closure ao método `fake`. Esta closure receberá uma instância de `Illuminate\Http\Client\Request` e deve retornar uma instância de resposta. Dentro da sua closure, você pode executar qualquer lógica necessária para determinar que tipo de resposta retornar:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a id="inspecting-requests"></a>
### Inspecionando Requisições

Ao simular respostas, você pode ocasionalmente querer inspecionar as requisições que o cliente recebe para garantir que sua aplicação está enviando os dados ou cabeçalhos corretos. Você pode conseguir isso chamando o método `Http::assertSent` após chamar `Http::fake`.

O método `assertSent` aceita uma closure que receberá uma instância de `Illuminate\Http\Client\Request` e deve retornar um valor booleano indicando se a requisição corresponde às suas expectativas. Para que o teste passe, pelo menos uma requisição deve ter sido emitida correspondendo às expectativas fornecidas:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::withHeaders([
    'X-First' => 'foo',
])->post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertSent(function (Request $request) {
    return $request->hasHeader('X-First', 'foo') &&
           $request->url() == 'http://example.com/users' &&
           $request['name'] == 'Taylor' &&
           $request['role'] == 'Developer';
});
```

Se necessário, você pode afirmar que uma requisição específica não foi enviada usando o método `assertNotSent`:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```

Você pode usar o método `assertSentCount` para afirmar quantas requisições foram "enviadas" durante o teste:

```php
Http::fake();

Http::assertSentCount(5);
```

Ou, você pode usar o método `assertNothingSent` para afirmar que nenhuma requisição foi enviada durante o teste:

```php
Http::fake();

Http::assertNothingSent();
```

<a id="recording-requests-and-responses"></a>
#### Registrando Requisições / Respostas

Você pode usar o método `recorded` para reunir todas as requisições e suas respostas correspondentes. O método `recorded` retorna uma collection de arrays que contém instâncias de `Illuminate\Http\Client\Request` e `Illuminate\Http\Client\Response`:

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```

Adicionalmente, o método `recorded` aceita uma closure que receberá uma instância de `Illuminate\Http\Client\Request` e `Illuminate\Http\Client\Response` e pode ser usada para filtrar pares de requisição / resposta com base nas suas expectativas:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```

<a id="preventing-stray-requests"></a>
### Prevenindo Requisições Dispersas

Se você quiser garantir que todas as requisições enviadas através do cliente HTTP foram simuladas ao longo do seu teste individual ou da suíte de testes completa, você pode chamar o método `preventStrayRequests`. Após chamar este método, quaisquer requisições que não tenham uma resposta fictícia correspondente lançarão uma exceção em vez de fazer a requisição HTTP real:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// An "ok" response is returned...
Http::get('https://github.com/laravel/framework');

// An exception is thrown...
Http::get('https://laravel.com');
```

Às vezes, você pode querer prevenir a maioria das requisições dispersas enquanto ainda permite que requisições específicas sejam executadas. Para conseguir isso, você pode passar um array de padrões de URL ao método `allowStrayRequests`. Qualquer requisição que corresponda a um dos padrões fornecidos será permitida, enquanto todas as outras requisições continuarão a lançar uma exceção:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// This request is executed...
Http::get('http://127.0.0.1:5000/generate');

// An exception is thrown...
Http::get('https://laravel.com');
```

<a id="events"></a>
## Eventos

O Laravel dispara três eventos durante o processo de envio de requisições HTTP. O evento `RequestSending` é disparado antes de uma requisição ser enviada, enquanto o evento `ResponseReceived` é disparado após uma resposta ser recebida para uma determinada requisição. O evento `ConnectionFailed` é disparado se nenhuma resposta for recebida para uma determinada requisição.

Os eventos `RequestSending` e `ConnectionFailed` ambos contêm uma propriedade pública `$request` que você pode usar para inspecionar a instância `Illuminate\Http\Client\Request`. Da mesma forma, o evento `ResponseReceived` contém uma propriedade `$request` bem como uma propriedade `$response` que pode ser usada para inspecionar a instância `Illuminate\Http\Client\Response`. Você pode criar [listeners de evento](/en/events/) para esses eventos dentro da sua aplicação:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
