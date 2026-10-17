---
title: "Busca"
---

- [Introdução](#introduction)
    - [Busca Full-Text](#introduction-full-text-search)
    - [Busca Semântica / Vetorial](#introduction-semantic-vector-search)
    - [Reranking](#introduction-reranking)
    - [Mecanismos de Busca do Scout](#introduction-scout-search-engines)
- [Busca Full-Text](#full-text-search)
    - [Adicionando Índices Full-Text](#adding-full-text-indexes)
    - [Executando Consultas Full-Text](#running-full-text-queries)
- [Busca Semântica / Vetorial](#semantic-vector-search)
    - [Gerando Embeddings](#generating-embeddings)
    - [Armazenando e Indexando Vetores](#storing-and-indexing-vectors)
    - [Consultando por Similaridade](#querying-by-similarity)
- [Reordenando Resultados](#reranking-results)
- [Laravel Scout](#laravel-scout)
    - [Engine de Banco de Dados](#database-engine)
    - [Engines de Terceiros](#third-party-engines)
- [Combinando Técnicas](#combining-techniques)

<a id="introduction"></a>
## Introdução

Quase toda aplicação precisa de busca. Seja quando seus usuários pesquisam uma base de conhecimento por artigos relevantes, exploram um catálogo de produtos ou fazem perguntas em linguagem natural sobre um conjunto de documentos, o Laravel oferece ferramentas integradas para lidar com cada um desses cenários, e muitas vezes você não precisa de nenhum serviço externo para isso.

A maioria das aplicações descobrirá que as opções integradas, alimentadas pelo banco de dados, fornecidas pelo Laravel são mais do que suficientes. Serviços de busca externos só são necessários quando você precisa de recursos como tolerância a erros de digitação, filtragem por facetas ou busca geográfica em grande escala.

<a id="introduction-full-text-search"></a>
#### Busca Full-Text

Quando você precisa de ranqueamento por relevância de palavras-chave, em que o banco de dados pontua e ordena os resultados de acordo com o quão bem eles correspondem aos termos buscados, o método `whereFullText` do query builder do Laravel utiliza os índices full-text nativos do MariaDB, MySQL e PostgreSQL. A busca full-text entende limites de palavras e stemming, portanto uma busca por "running" pode encontrar registros que contenham "run". Nenhum serviço externo é necessário.

<a id="introduction-semantic-vector-search"></a>
#### Busca Semântica / Vetorial

Para uma busca semântica baseada em IA, que encontra resultados pelo *significado* em vez de palavras-chave exatas, o método `whereVectorSimilarTo` do query builder utiliza embeddings vetoriais armazenados no PostgreSQL com a extensão `pgvector` ou no MariaDB. Por exemplo, uma busca por "best wineries in Napa Valley" pode retornar um artigo intitulado "Top Vineyards to Visit", mesmo que as palavras não se sobreponham. A busca vetorial requer PostgreSQL com a extensão `pgvector` ou MariaDB 11.7 ou superior, além do [Laravel AI SDK](../ai-sdk/).

<a id="introduction-reranking"></a>
#### Reranking

O [AI SDK](../ai-sdk/) do Laravel oferece recursos de reranking que usam modelos de IA para reordenar qualquer conjunto de resultados de acordo com a relevância semântica para uma consulta. O reranking é especialmente poderoso como uma segunda etapa, após uma etapa inicial de recuperação rápida, como a busca full-text, combinando velocidade e precisão semântica.

<a id="introduction-scout-search-engines"></a>
#### Busca com Laravel Scout

Para aplicações que desejam uma trait `Searchable` que mantenha automaticamente os índices de busca sincronizados com os models Eloquent, o [Laravel Scout](../scout/) oferece tanto uma engine de banco de dados integrada quanto drivers para serviços de terceiros como Algolia, Meilisearch, Typesense e Turbopuffer.

<a id="full-text-search"></a>
## Busca Full-Text

Embora consultas `LIKE` funcionem bem para correspondências simples de substring, elas não entendem o idioma. Uma busca `LIKE` por "running" não encontrará um registro que contenha "run", e os resultados não são ranqueados por relevância: são simplesmente retornados na ordem em que o banco os encontra. A busca full-text resolve esses dois problemas usando índices especializados que entendem limites de palavras, stemming e pontuação de relevância, permitindo que o banco retorne primeiro os resultados mais relevantes.

A busca full-text rápida está integrada ao MariaDB, MySQL e PostgreSQL, sem a necessidade de um serviço de busca externo. Você só precisa adicionar um índice full-text às colunas que deseja pesquisar e, em seguida, usar o método `whereFullText` do query builder para pesquisar nelas.

> **Aviso:**
> A busca full-text é atualmente suportada pelo MariaDB, MySQL e PostgreSQL.

<a id="adding-full-text-indexes"></a>
### Adicionando Índices Full-Text

Para usar a busca full-text, primeiro adicione um índice full-text às colunas que deseja pesquisar. Você pode adicionar o índice a uma única coluna ou passar um array de colunas para criar um índice composto que pesquisa em vários campos de uma só vez:

```php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->timestamps();

    $table->fullText(['title', 'body']);
});
```

No PostgreSQL, você pode especificar uma configuração de idioma para o índice, que controla como as palavras são normalizadas por stemming:

```php
$table->fullText('body')->language('english');
```

Para mais informações sobre a criação de índices, consulte a [documentação de migrations](../migrations/#available-index-types).

<a id="running-full-text-queries"></a>
### Executando Consultas Full-Text

Com o índice criado, use o método `whereFullText` do query builder para pesquisar nele. O Laravel gerará o SQL apropriado para o driver do seu banco de dados. Por exemplo, `MATCH(...) AGAINST(...)` no MariaDB e MySQL, e `to_tsvector(...) @@ plainto_tsquery(...)` no PostgreSQL:

```php
$articles = Article::whereFullText('body', 'web developer')->get();
```

Ao usar MariaDB e MySQL, os resultados são automaticamente ordenados pela pontuação de relevância. No PostgreSQL, `whereFullText` filtra os registros correspondentes, mas não os ordena por relevância. Se você precisar de ordenação automática por relevância no PostgreSQL, considere usar a [engine de banco de dados do Scout](#database-engine), que faz isso por você.

Se você criou um índice full-text composto em várias colunas, pode pesquisar em todas elas passando o mesmo array de colunas para `whereFullText`:

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();
```

O método `orWhereFullText` pode ser usado para adicionar uma cláusula de busca full-text como uma condição "or". Para detalhes completos, consulte a [documentação do query builder](../queries/#full-text-where-clauses).

<a id="semantic-vector-search"></a>
## Busca Semântica / Vetorial

A busca full-text depende da correspondência de palavras-chave: as palavras da consulta devem aparecer (de alguma forma) nos dados. A busca semântica adota uma abordagem fundamentalmente diferente: ela usa embeddings vetoriais gerados por IA para representar o *significado* de um texto como arrays de números e, em seguida, encontra os resultados cujo significado é mais semelhante ao da consulta. Por exemplo, uma busca por "best wineries in Napa Valley" pode retornar um artigo intitulado "Top Vineyards to Visit", mesmo que as palavras não se sobreponham de forma alguma.

O fluxo básico da busca vetorial é: gerar um embedding (um array numérico) para cada conteúdo e armazená-lo junto aos seus dados; então, no momento da busca, gerar um embedding para a consulta do usuário e encontrar os embeddings armazenados que estão mais próximos dele no espaço vetorial.

> **Nota:**
> A busca vetorial requer o [Laravel AI SDK](../ai-sdk/) e é suportada pelo PostgreSQL (requer a extensão `pgvector`), MariaDB 11.7 ou superior e MongoDB (requer o [pacote Laravel MongoDB](https://laravel.com/docs/13.x/mongodb)). Todos os bancos PostgreSQL no [Laravel Cloud](https://laravel.com/cloud) já têm o `pgvector` instalado.

<a id="generating-embeddings"></a>
### Gerando Embeddings

Um embedding é um array numérico de alta dimensionalidade (normalmente centenas ou milhares de números) que representa o significado semântico de um trecho de texto. Você pode gerar embeddings para uma string usando o método `toEmbeddings`, disponível na classe `Stringable` do Laravel:

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

Para gerar embeddings para várias entradas de uma só vez, o que é mais eficiente do que gerá-los um por vez, pois exige apenas uma única chamada ao provedor de embeddings, use a classe `Embeddings`:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

Para mais detalhes sobre a configuração de provedores de embeddings, personalização de dimensões e cache, consulte a [documentação do AI SDK](../ai-sdk/#embeddings).

<a id="storing-and-indexing-vectors"></a>
### Armazenando e Indexando Vetores

Para armazenar embeddings vetoriais, defina uma coluna `vector` na sua migration, especificando o número de dimensões que corresponde à saída do seu provedor de embeddings (por exemplo, 1536 para o modelo `text-embedding-3-small` da OpenAI). Você também deve chamar `index` na coluna para criar um índice HNSW (Hierarchical Navigable Small World), que acelera drasticamente as buscas por similaridade em grandes conjuntos de dados:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536)->index();
    $table->timestamps();
});
```

O método `Schema::ensureVectorExtensionExists` garante que a extensão `pgvector` esteja habilitada no seu banco PostgreSQL antes de criar a tabela.

No seu model Eloquent, use o cast `AsVector` para que o Laravel trate automaticamente a conversão entre arrays PHP e o formato vetorial do banco de dados:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```

Para mais detalhes sobre colunas e índices vetoriais, consulte a [documentação de migrations](../migrations/#available-column-types).

<a id="querying-by-similarity"></a>
### Consultando por Similaridade

Depois de armazenar os embeddings do seu conteúdo, você pode buscar registros semelhantes usando o método `whereVectorSimilarTo`. Esse método compara o embedding informado com os vetores armazenados usando similaridade de cosseno, filtra os resultados abaixo do limite `minSimilarity` e ordena automaticamente os resultados por relevância, com os registros mais semelhantes primeiro. O limite deve ser um valor entre `0.0` e `1.0`, em que `1.0` significa que os vetores são idênticos:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

Como conveniência, quando uma string simples é fornecida no lugar de um array de embedding, o Laravel gera automaticamente o embedding para você usando o provedor de embeddings configurado. Isso significa que você pode passar a consulta do usuário diretamente, sem convertê-la manualmente em um embedding antes:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

Para um controle de nível mais baixo sobre consultas vetoriais, os métodos `whereVectorDistanceLessThan`, `selectVectorDistance` e `orderByVectorDistance` também estão disponíveis. Esses métodos permitem trabalhar diretamente com valores de distância em vez de pontuações de similaridade, selecionar a distância calculada como uma coluna nos resultados ou controlar manualmente a ordenação. Para detalhes completos, consulte a [documentação do query builder](../queries/#vector-similarity-clauses) e a [documentação do AI SDK](../ai-sdk/#querying-embeddings).

<a id="reranking-results"></a>
## Reordenando Resultados

Reranking é uma técnica em que um modelo de IA reordena um conjunto de resultados de acordo com a relevância semântica de cada resultado para uma determinada consulta. Diferentemente da busca vetorial, que exige que você pré-calcule e armazene embeddings, o reranking funciona com qualquer coleção de textos: ele recebe o conteúdo bruto e a consulta como entrada e retorna os itens ordenados por relevância.

O reranking é especialmente poderoso como uma segunda etapa após uma etapa inicial de recuperação rápida. Por exemplo, você pode usar a busca full-text para reduzir rapidamente milhares de registros aos 50 melhores candidatos e, em seguida, usar o reranking para colocar os resultados mais relevantes no topo. Esse padrão de "recuperar e depois reordenar" oferece tanto velocidade quanto precisão semântica.

Você pode reordenar um array de strings usando a classe `Reranking`:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

$response->first()->document; // "Laravel is a PHP web application framework."
```

As collections do Laravel também possuem uma macro `rerank` que aceita um nome de campo (ou uma closure) e uma consulta, facilitando o reranking de resultados Eloquent:

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');
```

Para detalhes completos sobre a configuração de provedores de reranking e as opções disponíveis, consulte a [documentação do AI SDK](../ai-sdk/#reranking).

<a id="laravel-scout"></a>
## Laravel Scout

As técnicas de busca descritas acima são todos métodos do query builder que você chama diretamente no seu código. O [Laravel Scout](../scout/) adota uma abordagem diferente: ele fornece uma trait `Searchable` que você adiciona aos seus models Eloquent, e o Scout mantém automaticamente seus índices de busca sincronizados conforme os registros são criados, atualizados e excluídos. Isso é especialmente conveniente quando você quer que seus models sejam sempre pesquisáveis, sem gerenciar manualmente as atualizações dos índices.

<a id="database-engine"></a>
### Engine de Banco de Dados

A engine de banco de dados integrada do Scout executa buscas full-text e buscas `LIKE` no seu banco de dados existente, sem nenhum serviço externo ou infraestrutura adicional. Basta adicionar a trait `Searchable` ao seu model e definir um método `toSearchableArray` que retorne as colunas que devem ser pesquisáveis.

Você pode usar atributos PHP para controlar a estratégia de busca de cada coluna. `SearchUsingFullText` usará o índice full-text do seu banco de dados, `SearchUsingPrefix` corresponderá apenas desde o início da string (`example%`), e quaisquer colunas sem atributo usarão uma estratégia `LIKE` padrão, com curingas em ambos os lados (`%example%`):

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;
use Laravel\Scout\Searchable;

class Article extends Model
{
    use Searchable;

    #[SearchUsingPrefix(['id'])]
    #[SearchUsingFullText(['title', 'body'])]
    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'body' => $this->body,
        ];
    }
}
```

> **Aviso:**
> Antes de especificar que uma coluna deve usar restrições de consulta full-text, verifique se a coluna possui um [índice full-text](../migrations/#available-index-types) atribuído.

Depois de adicionar a trait, você pode pesquisar no seu model usando o método `search` do Scout. A engine de banco de dados do Scout ordenará automaticamente os resultados por relevância, mesmo no PostgreSQL:

```php
$articles = Article::search('Laravel')->get();
```

A engine de banco de dados é uma ótima escolha quando suas necessidades de busca são moderadas e você quer a conveniência da sincronização automática de índices do Scout, sem implantar um serviço externo. Ela atende bem aos casos de uso mais comuns, incluindo filtragem, paginação e tratamento de registros excluídos com soft delete. Para detalhes completos, consulte a [documentação do Scout](../scout/#database-engine).

<a id="third-party-engines"></a>
### Engines de Terceiros

O Scout também oferece suporte a mecanismos de busca de terceiros, como [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com) e [Typesense](https://typesense.org). Esses serviços de busca dedicados oferecem recursos avançados como tolerância a erros de digitação, filtragem por facetas, busca geográfica e regras de ranqueamento personalizadas. Esses recursos se tornam importantes em escala muito grande ou quando você precisa de uma experiência de busca enquanto digita altamente refinada.

Como o Scout fornece uma API unificada em todos os seus drivers, migrar da engine de banco de dados para uma engine de terceiros depois exige poucas mudanças no código. Você pode começar com a engine de banco de dados e migrar para um serviço de terceiros apenas se as necessidades da sua aplicação ultrapassarem o que o banco pode oferecer.

Para detalhes completos sobre a configuração de engines de terceiros, consulte a [documentação do Scout](../scout/).

> **Nota:**
> Muitas aplicações nunca precisam de um mecanismo de busca externo. As técnicas integradas descritas nesta página cobrem a grande maioria dos casos de uso.

<a id="combining-techniques"></a>
## Combinando Técnicas

As técnicas de busca descritas nesta página não são mutuamente exclusivas, e combiná-las frequentemente produz os melhores resultados. Aqui estão dois padrões comuns que demonstram como essas ferramentas funcionam juntas.

**Recuperação Full-Text + Reranking**

Use a busca full-text para reduzir rapidamente um grande conjunto de dados a um conjunto de candidatos e, em seguida, aplique o reranking para ordenar esses candidatos por relevância semântica. Isso combina a velocidade da busca full-text nativa do banco com a precisão da pontuação de relevância baseada em IA:

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);
```

**Busca Vetorial + Filtros Tradicionais**

Combine a similaridade vetorial com cláusulas `where` padrão para restringir a busca semântica a um subconjunto de registros. Isso é útil quando você quer uma busca baseada em significado, mas precisa limitar os resultados por propriedade, categoria ou qualquer outro atributo:

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();
```
