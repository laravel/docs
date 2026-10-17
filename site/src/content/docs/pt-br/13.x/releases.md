---
title: "Notas de Lançamento"
---

- [Esquema de Versionamento](#versioning-scheme)
- [Política de Suporte](#support-policy)
- [Laravel 13](#laravel-13)

<a id="versioning-scheme"></a>
## Esquema de Versionamento

O Laravel e seus outros pacotes first-party seguem o [Versionamento Semântico](https://semver.org). Versões major do framework são lançadas anualmente (por volta do primeiro trimestre), enquanto versões minor e patch podem ser lançadas com a frequência de uma vez por semana. Versões minor e patch **nunca** devem conter mudanças que quebram compatibilidade.

Ao referenciar o framework Laravel ou seus componentes na sua aplicação ou pacote, você deve sempre usar uma restrição de versão como `^13.0`, pois versões major do Laravel incluem mudanças que quebram compatibilidade. No entanto, nos esforçamos para sempre garantir que você possa atualizar para uma nova versão major em um dia ou menos.

<a id="named-arguments"></a>
#### Argumentos Nomeados

[Argumentos nomeados](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) não são cobertos pelas diretrizes de compatibilidade retroativa do Laravel. Podemos optar por renomear argumentos de funções quando necessário para melhorar a base de código do Laravel. Portanto, o uso de argumentos nomeados ao chamar métodos do Laravel deve ser feito com cautela e com a compreensão de que os nomes dos parâmetros podem mudar no futuro.

<a id="support-policy"></a>
## Política de Suporte

Para todas as versões do Laravel, correções de bugs são fornecidas por 18 meses e correções de segurança por 2 anos. Para todas as bibliotecas adicionais, apenas a versão major mais recente recebe correções de bugs. Além disso, revise as versões de banco de dados [suportadas pelo Laravel](../database/#introduction).

<div class="overflow-auto">

| Versão  | PHP (*)   | Lançamento              | Correções de Bugs Até   | Correções de Segurança Até |
| ------- |-----------| ----------------------- | ----------------------- | -------------------------- |
| 10      | 8.1 - 8.3 | 14 de fevereiro de 2023 | 6 de agosto de 2024     | 4 de fevereiro de 2025     |
| 11      | 8.2 - 8.4 | 12 de março de 2024     | 3 de setembro de 2025   | 12 de março de 2026        |
| 12      | 8.2 - 8.5 | 24 de fevereiro de 2025 | 13 de agosto de 2026    | 24 de fevereiro de 2027    |
| 13      | 8.3 - 8.5 | 17 de março de 2026     | 3º trimestre de 2027    | 17 de março de 2028        |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>Fim de vida útil</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Apenas correções de segurança</div>
    </div>
</div>

(*) Versões do PHP suportadas

<a id="laravel-13"></a>
## Laravel 13

O Laravel 13 dá continuidade ao ciclo anual de lançamentos do Laravel, com foco em fluxos de trabalho nativos de IA, padrões mais robustos e APIs para desenvolvedores mais expressivas. Esta versão inclui primitivas de IA first-party, recursos JSON:API, capacidades de busca semântica / vetorial e melhorias incrementais em filas, cache e segurança.

<a id="minimal-breaking-changes"></a>
### Mudanças Mínimas que Quebram Compatibilidade

Grande parte do nosso foco neste ciclo de lançamento foi minimizar mudanças que quebram compatibilidade. Em vez disso, nos dedicamos a entregar melhorias contínuas de qualidade de vida ao longo do ano que não quebram aplicações existentes.

Portanto, o Laravel 13 é uma atualização relativamente pequena em termos de esforço, ao mesmo tempo que entrega novas capacidades substanciais. Diante disso, a maioria das aplicações Laravel pode ser atualizada para o Laravel 13 sem alterar muito o código da aplicação.

<a id="php-8"></a>
### PHP 8.3

O Laravel 13.x requer uma versão mínima do PHP 8.3.

<a id="ai-sdk"></a>
### Laravel AI SDK

O Laravel 13 introduz o [Laravel AI SDK](https://laravel.com/ai), de primeira parte, fornecendo uma API unificada para geração de texto, agentes com chamada de ferramentas, embeddings, áudio, imagens e integrações com vector stores.

Com o AI SDK, você pode criar funcionalidades de IA independentes de provedor, mantendo uma experiência de desenvolvimento consistente e nativa do Laravel.

Por exemplo, um agente básico pode ser acionado com uma única chamada:

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;
```

O Laravel AI SDK também pode gerar imagens, áudio e embeddings:

Para casos de uso de geração visual, o SDK oferece uma API limpa para criar imagens a partir de prompts em linguagem natural:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

Para experiências de voz, você pode sintetizar áudio com som natural a partir de texto para assistentes, narrações e recursos de acessibilidade:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

E para fluxos de busca semântica e recuperação, você pode gerar embeddings diretamente a partir de strings:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

<a id="json-api"></a>
### Recursos JSON:API

O Laravel agora inclui [recursos JSON:API](../eloquent-resources/#jsonapi-resources) de primeira parte, tornando simples retornar respostas em conformidade com a especificação JSON:API.

Os recursos JSON:API cuidam da serialização de objetos de recurso, inclusão de relacionamentos, sparse fieldsets, links e cabeçalhos de resposta em conformidade com JSON:API.

<a id="request-forgery-protection"></a>
### Proteção Contra Falsificação de Requisições

Por segurança, o middleware de [proteção contra falsificação de requisições](../csrf/#preventing-csrf-requests) do Laravel foi aprimorado e formalizado como `PreventRequestForgery`, adicionando verificação de requisições com reconhecimento de origem e mantendo a compatibilidade com a proteção CSRF baseada em token.

<a id="queue-routing"></a>
### Roteamento de Filas

O Laravel 13 adiciona [roteamento de filas por classe](../queues/#queue-routing) via `Queue::route(...)`, permitindo definir regras padrão de roteamento de fila / conexão para jobs específicos em um único local central:

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

<a id="php-attributes"></a>
### Atributos PHP Expandidos

O Laravel 13 continua expandindo o suporte nativo a atributos PHP em todo o framework, tornando preocupações comuns de configuração e comportamento mais declarativas e co-localizadas com suas classes e métodos.

Adições notáveis incluem atributos de controller e de autorização como [`#[Middleware]`](../controllers/#controller-middleware) e [`#[Authorize]`](../controllers/#authorization-attributes), bem como controles de job voltados para filas como [`#[Tries]`](../queues/#max-job-attempts-and-timeout), [`#[Backoff]`](../queues/#dealing-with-failed-jobs), [`#[Timeout]`](../queues/#max-job-attempts-and-timeout) e [`#[FailOnTimeout]`](../queues/#failing-on-timeout).

Por exemplo, middleware de controller e verificações de policy agora podem ser declarados diretamente em classes e métodos:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}
```

Atributos adicionais também foram introduzidos nas APIs de Eloquent, eventos, notificações, validação, testes e serialização de recursos, oferecendo uma opção consistente com atributos em mais áreas do framework.

<a id="cache-touch"></a>
### Extensão de TTL do Cache

O Laravel agora inclui [`Cache::touch(...)`](../cache/), que permite estender o TTL de um item de cache existente sem recuperar e armazenar novamente o seu valor.

<a id="semantic-search"></a>
### Busca Semântica / Vetorial

O Laravel 13 aprofunda sua proposta de busca semântica com suporte nativo a consultas vetoriais, fluxos de trabalho com embeddings e APIs relacionadas documentadas em [busca](../search/#semantic-vector-search), [consultas](../queries/#vector-similarity-clauses) e no [AI SDK](../ai-sdk/#embeddings).

Esses recursos tornam simples construir experiências de busca com IA usando PostgreSQL + `pgvector`, incluindo buscas por similaridade contra embeddings gerados diretamente a partir de strings.

Por exemplo, você pode executar buscas de similaridade semântica diretamente pelo query builder:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```
