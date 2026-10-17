---
title: "Respostas HTTP"
---

- [Criando Respostas](#creating-responses)
    - [Anexando Cabeçalhos às Respostas](#attaching-headers-to-responses)
    - [Anexando Cookies às Respostas](#attaching-cookies-to-responses)
    - [Cookies e Criptografia](#cookies-and-encryption)
- [Redirecionamentos](#redirects)
    - [Redirecionando para Rotas Nomeadas](#redirecting-named-routes)
    - [Redirecionando para Actions de Controller](#redirecting-controller-actions)
    - [Redirecionando para Domínios Externos](#redirecting-external-domains)
    - [Redirecionando com Dados de Sessão com Flash](#redirecting-with-flashed-session-data)
- [Outros Tipos de Resposta](#other-response-types)
    - [Respostas de View](#view-responses)
    - [Respostas JSON](#json-responses)
    - [Respostas Markdown](#markdown-responses)
    - [Downloads de Arquivo](#file-downloads)
    - [Respostas de Arquivo](#file-responses)
- [Respostas em Streaming](#streamed-responses)
    - [Consumindo Respostas em Streaming](#consuming-streamed-responses)
    - [Respostas JSON em Streaming](#streamed-json-responses)
    - [Event Streams (SSE)](#event-streams)
    - [Downloads em Streaming](#streamed-downloads)
- [Macros de Resposta](#response-macros)

<a id="creating-responses"></a>
## Criando Respostas

<a id="strings-arrays"></a>
#### Strings e Arrays

Todas as rotas e controllers devem retornar uma resposta para ser enviada de volta ao navegador do usuário. O Laravel fornece várias maneiras diferentes de retornar respostas. A resposta mais básica é retornar uma string de uma rota ou controller. O framework converterá automaticamente a string em uma resposta HTTP completa:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

Além de retornar strings de suas rotas e controllers, você também pode retornar arrays. O framework converterá automaticamente o array em uma resposta JSON:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> **Note:**
> Você sabia que também pode retornar [collections do Eloquent](../eloquent-collections/) de suas rotas ou controllers? Elas serão convertidas automaticamente para JSON. Experimente!

<a id="response-objects"></a>
#### Objetos de Resposta

Normalmente, você não estará apenas retornando strings ou arrays simples de suas actions de rota. Em vez disso, você estará retornando instâncias completas de `Illuminate\Http\Response` ou [views](../views/).

Retornar uma instância completa de `Response` permite que você personalize o código de status HTTP e os cabeçalhos da resposta. Uma instância de `Response` herda da classe `Symfony\Component\HttpFoundation\Response`, que fornece uma variedade de métodos para construir respostas HTTP:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a id="eloquent-models-and-collections"></a>
#### Models e Collections do Eloquent

Você também pode retornar models e collections do [Eloquent ORM](../eloquent/) diretamente de suas rotas e controllers. Quando você faz isso, o Laravel converterá automaticamente os models e collections em respostas JSON, respeitando os [atributos ocultos](../eloquent-serialization/#hiding-attributes-from-json) do model:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a id="attaching-headers-to-responses"></a>
### Anexando Cabeçalhos às Respostas

Tenha em mente que a maioria dos métodos de resposta é encadeável, permitindo a construção fluente de instâncias de resposta. Por exemplo, você pode usar o método `header` para adicionar uma série de cabeçalhos à resposta antes de enviá-la de volta ao usuário:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

Ou, você pode usar o método `withHeaders` para especificar um array de cabeçalhos a serem adicionados à resposta:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

Você pode remover cabeçalhos específicos de uma resposta de saída usando o método `withoutHeader`:

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a id="cache-control-middleware"></a>
#### Middleware de Cache Control

O Laravel inclui um middleware `cache.headers`, que pode ser usado para definir rapidamente o cabeçalho `Cache-Control` para um grupo de rotas. As diretivas devem ser fornecidas usando o equivalente em "snake case" da diretiva cache-control correspondente e devem ser separadas por ponto e vírgula. Se `etag` for especificado na lista de diretivas, um hash xxh128 do conteúdo da resposta será automaticamente definido como o identificador ETag:

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a id="attaching-cookies-to-responses"></a>
### Anexando Cookies às Respostas

Você pode anexar um cookie a uma instância de saída `Illuminate\Http\Response` usando o método `cookie`. Você deve passar a este método o nome, o valor e o número de minutos durante os quais o cookie deve ser considerado válido:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

O método `cookie` também aceita mais alguns argumentos que são usados com menos frequência. Geralmente, esses argumentos têm o mesmo propósito e significado dos argumentos que seriam fornecidos ao método nativo [setcookie](https://secure.php.net/manual/en/function.setcookie.php) do PHP:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

Se você quiser garantir que um cookie seja enviado com a resposta de saída, mas ainda não tiver uma instância dessa resposta, pode usar a facade `Cookie` para "enfileirar" cookies para anexação à resposta quando ela for enviada. O método `queue` aceita os argumentos necessários para criar uma instância de cookie. Esses cookies serão anexados à resposta de saída antes de ela ser enviada ao navegador:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a id="generating-cookie-instances"></a>
#### Gerando Instâncias de Cookie

Se você quiser gerar uma instância de `Symfony\Component\HttpFoundation\Cookie` que possa ser anexada a uma instância de resposta posteriormente, pode usar o helper global `cookie`. Esse cookie não será enviado de volta ao cliente, a menos que seja anexado a uma instância de resposta:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a id="expiring-cookies-early"></a>
#### Expirando Cookies Antecipadamente

Você pode remover um cookie expirando-o por meio do método `withoutCookie` ou `withoutCookies` de uma resposta de saída:

```php
return response('Hello World')->withoutCookie('name');

return response('Hello World')->withoutCookies([
    'name',
    'email',
    'preferences',
]);
```

Se você ainda não tiver uma instância da resposta de saída, pode usar o método `expire` da facade `Cookie` para expirar um cookie:

```php
Cookie::expire('name');
```

<a id="cookies-and-encryption"></a>
### Cookies e Criptografia

Por padrão, graças ao middleware `Illuminate\Cookie\Middleware\EncryptCookies`, todos os cookies gerados pelo Laravel são criptografados e assinados para que não possam ser modificados ou lidos pelo cliente. Se você quiser desativar a criptografia para um subconjunto de cookies gerados pela sua aplicação, pode usar o método `encryptCookies` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> **Note:**
> Em geral, a criptografia de cookies nunca deve ser desativada, pois isso expõe seus cookies a potencial exposição de dados e adulteração no lado do cliente.

<a id="redirects"></a>
## Redirecionamentos

Respostas de redirecionamento são instâncias da classe `Illuminate\Http\RedirectResponse` e contêm os cabeçalhos adequados necessários para redirecionar o usuário para outra URL. Há várias maneiras de gerar uma instância de `RedirectResponse`. O método mais simples é usar o helper global `redirect`:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

Às vezes, você pode desejar redirecionar o usuário para sua localização anterior, como quando um formulário enviado é inválido. Você pode fazer isso usando a função helper global `back`. Como esse recurso utiliza a [sessão](../session/), certifique-se de que a rota que chama a função `back` esteja usando o grupo de middleware `web`:

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a id="redirecting-named-routes"></a>
### Redirecionando para Rotas Nomeadas

Quando você chama o helper `redirect` sem parâmetros, uma instância de `Illuminate\Routing\Redirector` é retornada, permitindo que você chame qualquer método na instância de `Redirector`. Por exemplo, para gerar uma `RedirectResponse` para uma rota nomeada, você pode usar o método `route`:

```php
return redirect()->route('login');
```

Se sua rota tiver parâmetros, você pode passá-los como segundo argumento para o método `route`:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a id="populating-parameters-via-eloquent-models"></a>
#### Populando Parâmetros via Models do Eloquent

Se você estiver redirecionando para uma rota com um parâmetro "ID" que está sendo populado a partir de um model do Eloquent, você pode passar o próprio model. O ID será extraído automaticamente:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

Se você quiser personalizar o valor que é colocado no parâmetro de rota, pode especificar a coluna na definição do parâmetro de rota (`/profile/{id:slug}`) ou pode sobrescrever o método `getRouteKey` no seu model do Eloquent:

```php
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a id="redirecting-controller-actions"></a>
### Redirecionando para Actions de Controller

Você também pode gerar redirecionamentos para [actions de controller](../controllers/). Para fazer isso, passe o nome do controller e da action para o método `action`:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

Se sua rota de controller exigir parâmetros, você pode passá-los como segundo argumento para o método `action`:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a id="redirecting-external-domains"></a>
### Redirecionando para Domínios Externos

Às vezes, você pode precisar redirecionar para um domínio fora da sua aplicação. Você pode fazer isso chamando o método `away`, que cria uma `RedirectResponse` sem qualquer codificação, validação ou verificação adicional de URL:

```php
return redirect()->away('https://www.google.com');
```

<a id="redirecting-with-flashed-session-data"></a>
### Redirecionando com Dados de Sessão com Flash

Redirecionar para uma nova URL e [fazer flash de dados para a sessão](../session/#flash-data) geralmente são feitos ao mesmo tempo. Normalmente, isso é feito após executar uma action com sucesso, quando você faz flash de uma mensagem de sucesso para a sessão. Por conveniência, você pode criar uma instância de `RedirectResponse` e fazer flash de dados para a sessão em uma única cadeia de métodos fluente:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

Após o usuário ser redirecionado, você pode exibir a mensagem que teve flash a partir da [sessão](../session/). Por exemplo, usando a [sintaxe Blade](../blade/):

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a id="redirecting-with-input"></a>
#### Redirecionando com Entrada

Você pode usar o método `withInput` fornecido pela instância de `RedirectResponse` para fazer flash dos dados de entrada da requisição atual para a sessão antes de redirecionar o usuário para uma nova localização. Isso é normalmente feito se o usuário encontrou um erro de validação. Depois que a entrada tiver flash para a sessão, você pode facilmente [recuperá-la](../requests/#retrieving-old-input) durante a próxima requisição para repopular o formulário:

```php
return back()->withInput();
```

<a id="other-response-types"></a>
## Outros Tipos de Resposta

O helper `response` pode ser usado para gerar outros tipos de instâncias de resposta. Quando o helper `response` é chamado sem argumentos, uma implementação do [contract](../contracts/) `Illuminate\Contracts\Routing\ResponseFactory` é retornada. Esse contract fornece vários métodos úteis para gerar respostas.

<a id="view-responses"></a>
### Respostas de View

Se você precisar de controle sobre o status e os cabeçalhos da resposta, mas também precisar retornar uma [view](../views/) como conteúdo da resposta, você deve usar o método `view`:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

É claro que, se você não precisar passar um código de status HTTP personalizado ou cabeçalhos personalizados, pode usar a função helper global `view`.

<a id="json-responses"></a>
### Respostas JSON

O método `json` definirá automaticamente o cabeçalho `Content-Type` como `application/json`, bem como converterá o array fornecido em JSON usando a função PHP `json_encode`:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

Se você quiser criar uma resposta JSONP, pode usar o método `json` em combinação com o método `withCallback`:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a id="markdown-responses"></a>
### Respostas Markdown

O método `markdown` pode ser usado para retornar conteúdo Markdown com o cabeçalho `Content-Type` definido como `text/markdown`:

```php
return response()->markdown("# Hello\n\nWorld");
```

Você pode passar um código de status HTTP personalizado e um array de cabeçalhos adicionais como segundo e terceiro argumentos:

```php
return response()->markdown('# Not Found', 404, ['X-Custom-Header' => 'Value']);
```

<a id="file-downloads"></a>
### Downloads de Arquivo

O método `download` pode ser usado para gerar uma resposta que force o navegador do usuário a fazer o download do arquivo no caminho fornecido. O método `download` aceita um nome de arquivo como segundo argumento do método, que determinará o nome de arquivo visto pelo usuário que faz o download do arquivo. Por fim, você pode passar um array de cabeçalhos HTTP como terceiro argumento do método:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> **Warning:**
> O Symfony HttpFoundation, que gerencia os downloads de arquivo, exige que o arquivo a ser baixado tenha um nome de arquivo ASCII.

<a id="file-responses"></a>
### Respostas de Arquivo

O método `file` pode ser usado para exibir um arquivo, como uma imagem ou PDF, diretamente no navegador do usuário, em vez de iniciar um download. Este método aceita o caminho absoluto para o arquivo como seu primeiro argumento e um array de cabeçalhos como seu segundo argumento:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a id="streamed-responses"></a>
## Respostas em Streaming

Ao fazer streaming de dados para o cliente conforme eles são gerados, você pode reduzir significativamente o uso de memória e melhorar o desempenho, especialmente para respostas muito grandes. As respostas em streaming permitem que o cliente comece a processar os dados antes de o servidor ter terminado de enviá-los:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // Simulate delay between chunks...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

Por conveniência, se o closure que você fornecer ao método `stream` retornar um [Generator](https://www.php.net/manual/en/language.generators.overview.php), o Laravel fará automaticamente o flush do buffer de saída entre as strings retornadas pelo generator, bem como desativará o buffer de saída do Nginx:

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a id="consuming-streamed-responses"></a>
### Consumindo Respostas em Streaming

As respostas em streaming podem ser consumidas usando o pacote npm `stream` do Laravel, que fornece uma API conveniente para interagir com as respostas e os event streams do Laravel. Para começar, instale o pacote `@laravel/stream-react`, `@laravel/stream-vue` ou `@laravel/stream-svelte`:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

Em seguida, `useStream` pode ser usado para consumir o event stream. Depois de fornecer sua URL de stream, o hook atualizará automaticamente `data` com a resposta concatenada à medida que o conteúdo for retornado pela sua aplicação Laravel:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");

const sendMessage = () => {
    stream.send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<div>
    <div>{$stream.data}</div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
    <button onclick={sendMessage}>Send Message</button>
</div>
```

Ao enviar dados de volta para o stream via `send`, a conexão ativa com o stream é cancelada antes de enviar os novos dados. Todas as requisições são enviadas como requisições JSON `POST`.

> **Warning:**
> Como o hook `useStream` faz uma requisição `POST` à sua aplicação, é necessário um token CSRF válido. A maneira mais fácil de fornecer o token CSRF é [incluí-lo por meio de uma meta tag no head do layout da sua aplicação](../csrf/#csrf-x-csrf-token).

O segundo argumento fornecido a `useStream` é um objeto de opções que você pode usar para personalizar o comportamento de consumo do stream. Os valores padrão para esse objeto são mostrados abaixo:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response) => {},
    onData: (data) => {},
    onCancel: () => {},
    onFinish: () => {},
    onError: (error) => {},
});
</script>

<div>{$stream.data}</div>
```

`onResponse` é disparado após uma resposta inicial bem-sucedida do stream, e a [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) bruta é passada para o callback. `onData` é chamado à medida que cada chunk é recebido - o chunk atual é passado para o callback. `onFinish` é chamado quando um stream termina e quando um erro é lançado durante o ciclo de fetch / read.

Por padrão, nenhuma requisição é feita ao stream na inicialização. Você pode passar um payload inicial para o stream usando a opção `initialInput`:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<div>{$stream.data}</div>
```

Para cancelar um stream manualmente, você pode usar o método `cancel` retornado pelo hook:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <button onclick={() => stream.cancel()}>Cancel</button>
</div>
```

Cada vez que o hook `useStream` é usado, um `id` aleatório é gerado para identificar o stream. Esse valor é enviado de volta ao servidor a cada requisição no cabeçalho `X-STREAM-ID`. Ao consumir o mesmo stream a partir de múltiplos componentes, você pode ler e escrever no stream fornecendo seu próprio `id`:

```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```

```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

```svelte tab=Svelte
<!-- App.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";
import StreamStatus from "./StreamStatus.svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <StreamStatus id={stream.id} />
</div>

<!-- StreamStatus.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";

let { id } = $props();

const stream = useStream("chat", { id });
</script>

<div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
</div>
```

<a id="streamed-json-responses"></a>
### Respostas JSON em Streaming

Se você precisar fazer streaming de dados JSON de forma incremental, pode utilizar o método `streamJson`. Esse método é especialmente útil para grandes conjuntos de dados que precisam ser enviados progressivamente ao navegador em um formato que possa ser facilmente parseado por JavaScript:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

O hook `useJsonStream` é idêntico ao [hook useStream](#consuming-streamed-responses), exceto que ele tentará parsear os dados como JSON assim que o streaming terminar:

```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useJsonStream } from "@laravel/stream-svelte";

const stream = useJsonStream("users");

const loadUsers = () => {
    stream.send({
        query: "taylor",
    });
};
</script>

<div>
    <ul>
        {#if $stream.data?.users}
            {#each $stream.data.users as user (user.id)}
                <li>{user.id}: {user.name}</li>
            {/each}
        {/if}
    </ul>
    <button onclick={loadUsers}>Load Users</button>
</div>
```

<a id="event-streams"></a>
### Event Streams (SSE)

O método `eventStream` pode ser usado para retornar uma resposta em streaming de server-sent events (SSE) usando o content type `text/event-stream`. O método `eventStream` aceita um closure que deve [yield](https://www.php.net/manual/en/language.generators.overview.php) respostas para o stream à medida que as respostas ficam disponíveis:

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

Se você quiser personalizar o nome do evento, pode fazer yield de uma instância da classe `StreamedEvent`:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a id="consuming-event-streams"></a>
#### Consumindo Event Streams

Event streams podem ser consumidos usando o pacote npm `stream` do Laravel, que fornece uma API conveniente para interagir com os event streams do Laravel. Para começar, instale o pacote `@laravel/stream-react`, `@laravel/stream-vue` ou `@laravel/stream-svelte`:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

Em seguida, `useEventStream` pode ser usado para consumir o event stream. Depois de fornecer sua URL de stream, o hook atualizará automaticamente `message` com a resposta concatenada à medida que as mensagens forem retornadas pela sua aplicação Laravel:

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat");
</script>

<div>{$eventStream.message}</div>
```

O segundo argumento fornecido a `useEventStream` é um objeto de opções que você pode usar para personalizar o comportamento de consumo do stream. Os valores padrão para esse objeto são mostrados abaixo:

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  eventName: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat", {
    eventName: "update",
    onMessage: (event) => {
        //
    },
    onError: (error) => {
        //
    },
    onComplete: () => {
        //
    },
    endSignal: "</stream>",
    glue: " ",
    replace: false,
});
</script>
```

Event streams também podem ser consumidos manualmente por meio de um objeto [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) pelo frontend da sua aplicação. O método `eventStream` enviará automaticamente uma atualização `</stream>` ao event stream quando o stream estiver completo:

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```

Para personalizar o evento final que é enviado ao event stream, você pode fornecer uma instância de `StreamedEvent` ao argumento `endStreamWith` do método `eventStream`:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a id="streamed-downloads"></a>
### Downloads em Streaming

Às vezes, você pode desejar transformar a resposta string de uma determinada operação em uma resposta de download sem precisar escrever o conteúdo da operação em disco. Você pode usar o método `streamDownload` nesse cenário. Este método aceita um callback, um nome de arquivo e um array opcional de cabeçalhos como seus argumentos:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a id="response-macros"></a>
## Macros de Resposta

Se você quiser definir uma resposta personalizada que possa reutilizar em uma variedade de suas rotas e controllers, pode usar o método `macro` na facade `Response`. Normalmente, você deve chamar esse método a partir do método `boot` de um dos [service providers](../providers/) da sua aplicação, como o service provider `App\Providers\AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

A função `macro` aceita um nome como seu primeiro argumento e um closure como seu segundo argumento. O closure do macro será executado ao chamar o nome do macro a partir de uma implementação de `ResponseFactory` ou do helper `response`:

```php
return response()->caps('foo');
```
