---
title: "Tratamento de Erros"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
- [Tratando Exceções](#handling-exceptions)
    - [Reportando Exceções](#reporting-exceptions)
    - [Níveis de Log de Exceções](#exception-log-levels)
    - [Ignorando Exceções por Tipo](#ignoring-exceptions-by-type)
    - [Renderizando Exceções](#rendering-exceptions)
    - [Exceções Reportáveis e Renderizáveis](#renderable-exceptions)
- [Limitando a Taxa de Exceções Reportadas](#throttling-reported-exceptions)
- [Exceções HTTP](#http-exceptions)
    - [Páginas de Erro HTTP Personalizadas](#custom-http-error-pages)

<a id="introduction"></a>
## Introdução

Quando você inicia um novo projeto Laravel, o tratamento de erros e exceções já está configurado para você; no entanto, a qualquer momento, você pode usar o método `withExceptions` no arquivo `bootstrap/app.php` da sua aplicação para gerenciar como as exceções são reportadas e renderizadas pela sua aplicação.

O objeto `$exceptions` fornecido à closure `withExceptions` é uma instância de `Illuminate\Foundation\Configuration\Exceptions` e é responsável por gerenciar o tratamento de exceções na sua aplicação. Vamos nos aprofundar neste objeto ao longo desta documentação.

<a id="configuration"></a>
## Configuração

A opção `debug` no seu arquivo de configuração `config/app.php` determina quanta informação sobre um erro é efetivamente exibida ao usuário. Por padrão, esta opção está configurada para respeitar o valor da variável de ambiente `APP_DEBUG`, que está armazenada no seu arquivo `.env`.

Durante o desenvolvimento local, você deve definir a variável de ambiente `APP_DEBUG` como `true`.

> **Aviso:**
> No seu ambiente de produção, o valor de `APP_DEBUG` deve sempre ser `false`. Se o valor for definido como `true` em produção, você corre o risco de expor valores de configuração sensíveis aos usuários finais da sua aplicação.

<a id="handling-exceptions"></a>
## Tratando Exceções

<a id="reporting-exceptions"></a>
### Reportando Exceções

No Laravel, o reporte de exceções é usado para registrar exceções em log ou enviá-las a um serviço externo como [Laravel Nightwatch](https://nightwatch.laravel.com), [Sentry](https://github.com/getsentry/sentry-laravel), ou [Flare](https://flareapp.io). Por padrão, as exceções serão registradas em log com base na sua configuração de [logging](../logging/). No entanto, você é livre para registrar exceções em log como desejar.

Se você precisar reportar diferentes tipos de exceções de maneiras diferentes, você pode usar o método de exceção `report` no arquivo `bootstrap/app.php` da sua aplicação para registrar uma closure que deve ser executada quando uma exceção de um determinado tipo precisar ser reportada. O Laravel determinará qual tipo de exceção a closure reporta examinando o type-hint da closure:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

Quando você registra um callback de reporte de exceção personalizado usando o método `report`, o Laravel ainda registrará a exceção em log usando a configuração de logging padrão da aplicação. Se você deseja interromper a propagação da exceção para a pilha de logging padrão, você pode usar o método `stop` ao definir seu callback de reporte ou retornar `false` a partir do callback:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```

> **Nota:**
> Para personalizar o reporte de exceção para uma determinada exceção, você também pode utilizar [exceções reportáveis](#renderable-exceptions).

<a id="global-log-context"></a>
#### Contexto Global de Log

Se disponível, o Laravel adiciona automaticamente o ID do usuário atual à mensagem de log de cada exceção como dados contextuais. Você pode definir seus próprios dados contextuais globais usando o método de exceção `context` no arquivo `bootstrap/app.php` da sua aplicação. Essas informações serão incluídas na mensagem de log de cada exceção escrita pela sua aplicação:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a id="exception-log-context"></a>
#### Contexto de Log da Exceção

Embora adicionar contexto a cada mensagem de log possa ser útil, às vezes uma exceção específica pode ter um contexto único que você gostaria de incluir nos seus logs. Ao definir um método `context` em uma das exceções da sua aplicação, você pode especificar quaisquer dados relevantes a essa exceção que devem ser adicionados à entrada de log da exceção:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * Get the exception's context information.
     *
     * @return array<string, mixed>
     */
    public function context(): array
    {
        return ['order_id' => $this->orderId];
    }
}
```

<a id="the-report-helper"></a>
#### O Helper `report`

Às vezes você pode precisar reportar uma exceção mas continuar tratando a requisição atual. A função helper `report` permite que você reporte rapidamente uma exceção sem renderizar uma página de erro para o usuário:

```php
public function isValid(string $value): bool
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a id="deduplicating-reported-exceptions"></a>
#### Deduplicando Exceções Reportadas

Se você estiver usando a função `report` ao longo da sua aplicação, você pode ocasionalmente reportar a mesma exceção várias vezes, criando entradas duplicadas nos seus logs.

Se você gostaria de garantir que uma única instância de uma exceção seja reportada apenas uma vez, você pode invocar o método de exceção `dontReportDuplicates` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

Agora, quando o helper `report` for chamado com a mesma instância de uma exceção, apenas a primeira chamada será reportada:

```php
$original = new RuntimeException('Whoops!');

report($original); // reported

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // ignored
}

report($original); // ignored
report($caught); // ignored
```

<a id="exception-log-levels"></a>
### Níveis de Log de Exceções

Quando mensagens são escritas nos [logs](../logging/) da sua aplicação, as mensagens são escritas em um [nível de log](../logging/#log-levels) especificado, que indica a severidade ou importância da mensagem sendo registrada.

Como observado acima, mesmo quando você registra um callback de reporte de exceção personalizado usando o método `report`, o Laravel ainda registrará a exceção em log usando a configuração de logging padrão da aplicação; no entanto, como o nível de log pode às vezes influenciar os canais nos quais uma mensagem é registrada, você pode desejar configurar o nível de log em que certas exceções são registradas.

Para fazer isso, você pode usar o método de exceção `level` no arquivo `bootstrap/app.php` da sua aplicação. Este método recebe o tipo da exceção como seu primeiro argumento e o nível de log como seu segundo argumento:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a id="ignoring-exceptions-by-type"></a>
### Ignorando Exceções por Tipo

Ao construir sua aplicação, haverá alguns tipos de exceções que você nunca vai querer reportar. Para ignorar essas exceções, você pode usar o método de exceção `dontReport` no arquivo `bootstrap/app.php` da sua aplicação. Qualquer classe fornecida a este método nunca será reportada; no entanto, elas ainda podem ter lógica de renderização personalizada:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

Alternativamente, você pode simplesmente "marcar" uma classe de exceção com a interface `Illuminate\Contracts\Debug\ShouldntReport`. Quando uma exceção é marcada com esta interface, ela nunca será reportada pelo handler de exceções do Laravel:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Contracts\Debug\ShouldntReport;

class PodcastProcessingException extends Exception implements ShouldntReport
{
    //
}
```

Se você precisar de ainda mais controle sobre quando um tipo específico de exceção é ignorado, você pode fornecer uma closure ao método `dontReportWhen`:

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```

Internamente, o Laravel já ignora alguns tipos de erros para você, como exceções resultantes de erros HTTP 404, respostas HTTP 403 geradas por incompatibilidades de origem, ou respostas HTTP 419 geradas por tokens CSRF inválidos. Se você gostaria de instruir o Laravel a parar de ignorar um determinado tipo de exceção, você pode usar o método de exceção `stopIgnoring` no arquivo `bootstrap/app.php` da sua aplicação:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a id="rendering-exceptions"></a>
### Renderizando Exceções

Por padrão, o handler de exceções do Laravel converterá exceções em uma resposta HTTP para você. No entanto, você é livre para registrar uma closure de renderização personalizada para exceções de um determinado tipo. Você pode fazer isso usando o método de exceção `render` no arquivo `bootstrap/app.php` da sua aplicação.

A closure passada ao método `render` deve retornar uma instância de `Illuminate\Http\Response`, que pode ser gerada através do helper `response`. O Laravel determinará qual tipo de exceção a closure renderiza examinando o type-hint da closure:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

Você também pode usar o método `render` para sobrescrever o comportamento de renderização de exceções nativas do Laravel ou do Symfony, como `NotFoundHttpException`. Se a closure fornecida ao método `render` não retornar um valor, a renderização de exceção padrão do Laravel será utilizada:

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
})
```

<a id="rendering-exceptions-as-json"></a>
#### Renderizando Exceções como JSON

Ao renderizar uma exceção, o Laravel determinará automaticamente se a exceção deve ser renderizada como uma resposta HTML ou JSON com base no cabeçalho `Accept` da requisição. Se você gostaria de personalizar como o Laravel determina se deve renderizar respostas de exceção HTML ou JSON, você pode utilizar o método `shouldRenderJsonWhen`:

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```

<a id="customizing-the-exception-response"></a>
#### Personalizando a Resposta de Exceção

Raramente, você pode precisar personalizar toda a resposta HTTP renderizada pelo handler de exceções do Laravel. Para fazer isso, você pode registrar uma closure de personalização de resposta usando o método `respond`:

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
})
```

<a id="renderable-exceptions"></a>
### Exceções Reportáveis e Renderizáveis

Em vez de definir comportamento de reporte e renderização personalizado no arquivo `bootstrap/app.php` da sua aplicação, você pode definir métodos `report` e `render` diretamente nas exceções da sua aplicação. Quando esses métodos existem, eles serão automaticamente chamados pelo framework:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * Render the exception as an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

Se sua exceção estende uma exceção que já é renderizável, como uma exceção nativa do Laravel ou do Symfony, você pode retornar `false` a partir do método `render` da exceção para renderizar a resposta HTTP padrão da exceção:

```php
/**
 * Render the exception as an HTTP response.
 */
public function render(Request $request): Response|bool
{
    if (/** Determine if the exception needs custom rendering */) {

        return response(/* ... */);
    }

    return false;
}
```

Se sua exceção contém lógica de reporte personalizada que só é necessária quando certas condições são atendidas, você pode precisar instruir o Laravel a às vezes reportar a exceção usando a configuração padrão de tratamento de exceções. Para fazer isso, você pode retornar `false` a partir do método `report` da exceção:

```php
/**
 * Report the exception.
 */
public function report(): bool
{
    if (/** Determine if the exception needs custom reporting */) {

        // ...

        return true;
    }

    return false;
}
```

> **Nota:**
> Você pode fazer type-hint de quaisquer dependências requeridas pelo método `report` e elas serão automaticamente injetadas no método pelo [service container](../container/) do Laravel.

<a id="throttling-reported-exceptions"></a>
### Limitando a Taxa de Exceções Reportadas

Se sua aplicação reporta um número muito grande de exceções, você pode querer limitar a taxa de quantas exceções são efetivamente registradas em log ou enviadas ao serviço externo de rastreamento de erros da sua aplicação.

Para obter uma taxa de amostragem aleatória de exceções, você pode usar o método de exceção `throttle` no arquivo `bootstrap/app.php` da sua aplicação. O método `throttle` recebe uma closure que deve retornar uma instância de `Lottery`:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

Também é possível amostrar condicionalmente com base no tipo da exceção. Se você gostaria de amostrar apenas instâncias de uma classe de exceção específica, você pode retornar uma instância de `Lottery` apenas para essa classe:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```

Você também pode limitar a taxa de exceções registradas em log ou enviadas a um serviço externo de rastreamento de erros retornando uma instância de `Limit` em vez de uma `Lottery`. Isso é útil se você quiser proteger contra picos repentinos de exceções inundando seus logs, por exemplo, quando um serviço de terceiros usado pela sua aplicação está fora do ar:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```

Por padrão, os limites usarão a classe da exceção como a chave de limite de taxa. Você pode personalizar isso especificando sua própria chave usando o método `by` no `Limit`:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```

Naturalmente, você pode retornar uma mistura de instâncias de `Lottery` e `Limit` para diferentes exceções:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return match (true) {
            $e instanceof BroadcastException => Limit::perMinute(300),
            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
            default => Limit::none(),
        };
    });
})
```

<a id="http-exceptions"></a>
## Exceções HTTP

Algumas exceções descrevem códigos de erro HTTP do servidor. Por exemplo, isso pode ser um erro de "página não encontrada" (404), um "erro de não autorizado" (401), ou até mesmo um erro 500 gerado pelo desenvolvedor. Para gerar tal resposta de qualquer lugar da sua aplicação, você pode usar o helper `abort`:

```php
abort(404);
```

<a id="custom-http-error-pages"></a>
### Páginas de Erro HTTP Personalizadas

O Laravel facilita a exibição de páginas de erro personalizadas para vários códigos de status HTTP. Por exemplo, para personalizar a página de erro para códigos de status HTTP 404, crie um template de view `resources/views/errors/404.blade.php`. Esta view será renderizada para todos os erros 404 gerados pela sua aplicação. As views dentro deste diretório devem ser nomeadas para corresponder ao código de status HTTP ao qual correspondem. A instância `Symfony\Component\HttpKernel\Exception\HttpException` levantada pela função `abort` será passada à view como uma variável `$exception`:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Você pode publicar os templates de página de erro padrão do Laravel usando o comando Artisan `vendor:publish`. Uma vez que os templates tenham sido publicados, você pode personalizá-los ao seu gosto:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a id="fallback-http-error-pages"></a>
#### Páginas de Erro HTTP de Fallback

Você também pode definir uma página de erro de "fallback" para uma determinada série de códigos de status HTTP. Esta página será renderizada se não houver uma página correspondente para o código de status HTTP específico que ocorreu. Para fazer isso, defina um template `4xx.blade.php` e um template `5xx.blade.php` no diretório `resources/views/errors` da sua aplicação.

Ao definir páginas de erro de fallback, as páginas de fallback não afetarão as respostas de erro `401`, `402`, `403`, `404`, `419`, `429`, `500`, e `503`, pois o Laravel tem páginas internas dedicadas para esses códigos de status. Para personalizar as páginas renderizadas para esses códigos de status, você deve definir uma página de erro personalizada para cada um deles individualmente.
