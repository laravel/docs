---
title: "Templates Blade"
---

- [Introdução](#introduction)
    - [Turbinando o Blade com Livewire](#supercharging-blade-with-livewire)
- [Exibindo Dados](#displaying-data)
    - [Codificação de Entidades HTML](#html-entity-encoding)
    - [Blade e Frameworks JavaScript](#blade-and-javascript-frameworks)
- [Diretivas Blade](#blade-directives)
    - [Estruturas If](#if-statements)
    - [Estruturas Switch](#switch-statements)
    - [Laços de Repetição](#loops)
    - [A Variável de Laço](#the-loop-variable)
    - [Classes Condicionais](#conditional-classes)
    - [Atributos Adicionais](#additional-attributes)
    - [Incluindo Subviews](#including-subviews)
    - [A Diretiva `@once`](#the-once-directive)
    - [PHP Puro](#raw-php)
    - [Fontes](#fonts)
    - [Comentários](#comments)
- [Componentes](#components)
    - [Renderizando Componentes](#rendering-components)
    - [Componentes de Índice](#index-components)
    - [Passando Dados para Componentes](#passing-data-to-components)
    - [Atributos de Componentes](#component-attributes)
    - [Palavras-chave Reservadas](#reserved-keywords)
    - [Slots](#slots)
    - [Views de Componentes Inline](#inline-component-views)
    - [Componentes Dinâmicos](#dynamic-components)
    - [Registrando Componentes Manualmente](#manually-registering-components)
- [Componentes Anônimos](#anonymous-components)
    - [Componentes de Índice Anônimos](#anonymous-index-components)
    - [Propriedades de Dados / Atributos](#data-properties-attributes)
    - [Acessando Dados do Pai](#accessing-parent-data)
    - [Caminhos de Componentes Anônimos](#anonymous-component-paths)
- [Construindo Layouts](#building-layouts)
    - [Layouts Usando Componentes](#layouts-using-components)
    - [Layouts Usando Herança de Templates](#layouts-using-template-inheritance)
- [Formulários](#forms)
    - [Campo CSRF](#csrf-field)
    - [Campo de Método](#method-field)
    - [Erros de Validação](#validation-errors)
- [Stacks](#stacks)
- [Injeção de Serviços](#service-injection)
- [Renderizando Templates Blade Inline](#rendering-inline-blade-templates)
- [Renderizando Fragmentos Blade](#rendering-blade-fragments)
- [Estendendo o Blade](#extending-blade)
    - [Manipuladores de Echo Personalizados](#custom-echo-handlers)
    - [Estruturas If Personalizadas](#custom-if-statements)

<a id="introduction"></a>
## Introdução

Blade é o mecanismo de templates simples, porém poderoso, que acompanha o Laravel. Diferente de alguns mecanismos de templates PHP, o Blade não impede que você use código PHP puro em seus templates. Na verdade, todos os templates Blade são compilados para código PHP puro e armazenados em cache até serem modificados, o que significa que o Blade adiciona essencialmente zero sobrecarga à sua aplicação. Os arquivos de template Blade usam a extensão `.blade.php` e normalmente ficam armazenados no diretório `resources/views`.

As views Blade podem ser retornadas de rotas ou controllers usando o helper global `view`. Claro, como mencionado na documentação sobre [views](../views/), dados podem ser passados para a view Blade usando o segundo argumento do helper `view`:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a id="supercharging-blade-with-livewire"></a>
### Turbinando o Blade com Livewire

Quer levar seus templates Blade para o próximo nível e construir interfaces dinâmicas com facilidade? Conheça o [Laravel Livewire](https://livewire.laravel.com). O Livewire permite que você escreva componentes Blade aprimorados com funcionalidades dinâmicas que normalmente só seriam possíveis por meio de frameworks de frontend como React, Svelte ou Vue, oferecendo uma ótima abordagem para construir frontends modernos e reativos sem as complexidades, a renderização no lado do cliente ou as etapas de build de muitos frameworks JavaScript.

<a id="displaying-data"></a>
## Exibindo Dados

Você pode exibir dados passados para suas views Blade envolvendo a variável entre chaves duplas. Por exemplo, dada a seguinte rota:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

Você pode exibir o conteúdo da variável `name` assim:

```blade
Hello, {{ $name }}.
```

> **Nota:**
> As instruções de echo `{{ }}` do Blade são automaticamente enviadas pela função `htmlspecialchars` do PHP para prevenir ataques XSS.

Você não está limitado a exibir o conteúdo das variáveis passadas para a view. Você também pode imprimir o resultado de qualquer função PHP. Na verdade, você pode colocar qualquer código PHP que desejar dentro de uma instrução de echo do Blade:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a id="html-entity-encoding"></a>
### Codificação de Entidades HTML

Por padrão, o Blade (e a função `e` do Laravel) codificará novamente as entidades HTML. Se você quiser desativar a codificação dupla, chame o método `Blade::withoutDoubleEncoding` a partir do método `boot` do seu `AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a id="displaying-unescaped-data"></a>
#### Exibindo Dados Sem Escape

Por padrão, as instruções `{{ }}` do Blade são automaticamente enviadas pela função `htmlspecialchars` do PHP para prevenir ataques XSS. Se você não quiser que seus dados sejam escapados, pode usar a seguinte sintaxe:

```blade
Hello, {!! $name !!}.
```

> **Aviso:**
> Tenha muito cuidado ao exibir conteúdo fornecido pelos usuários da sua aplicação. Normalmente, você deve usar a sintaxe escapada com chaves duplas para prevenir ataques XSS ao exibir dados fornecidos pelo usuário.

<a id="blade-and-javascript-frameworks"></a>
### Blade e Frameworks JavaScript

Como muitos frameworks JavaScript também usam chaves para indicar que uma determinada expressão deve ser exibida no navegador, você pode usar o símbolo `@` para informar ao mecanismo de renderização do Blade que uma expressão deve permanecer intocada. Por exemplo:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

Neste exemplo, o símbolo `@` será removido pelo Blade; no entanto, a expressão `{{ name }}` permanecerá intocada pelo mecanismo Blade, permitindo que ela seja renderizada pelo seu framework JavaScript.

O símbolo `@` também pode ser usado para escapar diretivas Blade:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a id="rendering-json"></a>
#### Renderizando JSON

Às vezes, você pode passar um array para sua view com a intenção de renderizá-lo como JSON para inicializar uma variável JavaScript. Por exemplo:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

No entanto, em vez de chamar `json_encode` manualmente, você pode usar o método `Illuminate\Support\Js::from`. O método `from` aceita os mesmos argumentos da função `json_encode` do PHP; porém, ele garante que o JSON resultante foi devidamente escapado para inclusão dentro de aspas HTML. O método `from` retornará uma string com uma instrução JavaScript `JSON.parse` que converterá o objeto ou array fornecido em um objeto JavaScript válido:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

As versões mais recentes do esqueleto da aplicação Laravel incluem uma facade `Js`, que oferece acesso conveniente a essa funcionalidade dentro dos seus templates Blade:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> **Aviso:**
> Você deve usar o método `Js::from` apenas para renderizar variáveis existentes como JSON. O template Blade é baseado em expressões regulares, e tentar passar uma expressão complexa para a diretiva pode causar falhas inesperadas.

<a id="the-at-verbatim-directive"></a>
#### A Diretiva `@verbatim`

Se você estiver exibindo variáveis JavaScript em uma grande parte do seu template, pode envolver o HTML na diretiva `@verbatim` para não precisar prefixar cada instrução de echo do Blade com o símbolo `@`:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a id="blade-directives"></a>
## Diretivas Blade

Além da herança de templates e da exibição de dados, o Blade também oferece atalhos práticos para estruturas de controle PHP comuns, como instruções condicionais e laços de repetição. Esses atalhos oferecem uma forma muito limpa e concisa de trabalhar com estruturas de controle PHP, mantendo-se familiares em relação às suas equivalentes em PHP.

<a id="if-statements"></a>
### Estruturas If

Você pode construir estruturas `if` usando as diretivas `@if`, `@elseif`, `@else` e `@endif`. Essas diretivas funcionam de forma idêntica às suas equivalentes em PHP:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

Por conveniência, o Blade também oferece a diretiva `@unless`:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

Além das diretivas condicionais já discutidas, as diretivas `@isset` e `@empty` podem ser usadas como atalhos convenientes para suas respectivas funções PHP:

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a id="authentication-directives"></a>
#### Diretivas de Autenticação

As diretivas `@auth` e `@guest` podem ser usadas para determinar rapidamente se o usuário atual está [autenticado](../authentication/) ou é um visitante:

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

Se necessário, você pode especificar o guard de autenticação que deve ser verificado ao usar as diretivas `@auth` e `@guest`:

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a id="environment-directives"></a>
#### Diretivas de Ambiente

Você pode verificar se a aplicação está sendo executada no ambiente de produção usando a diretiva `@production`:

```blade
@production
    // Production specific content...
@endproduction
```

Ou, você pode determinar se a aplicação está sendo executada em um ambiente específico usando a diretiva `@env`:

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a id="section-directives"></a>
#### Diretivas de Seção

Você pode determinar se uma seção da herança de templates tem conteúdo usando a diretiva `@hasSection`:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

Você pode usar a diretiva `sectionMissing` para determinar se uma seção não tem conteúdo:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a id="session-directives"></a>
#### Diretivas de Sessão

A diretiva `@session` pode ser usada para determinar se um valor de [sessão](../session/) existe. Se o valor da sessão existir, o conteúdo do template dentro das diretivas `@session` e `@endsession` será avaliado. Dentro do conteúdo da diretiva `@session`, você pode imprimir a variável `$value` para exibir o valor da sessão:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a id="context-directives"></a>
#### Diretivas de Contexto

A diretiva `@context` pode ser usada para determinar se um valor de [contexto](../context/) existe. Se o valor do contexto existir, o conteúdo do template dentro das diretivas `@context` e `@endcontext` será avaliado. Dentro do conteúdo da diretiva `@context`, você pode imprimir a variável `$value` para exibir o valor do contexto:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a id="switch-statements"></a>
### Estruturas Switch

Estruturas switch podem ser construídas usando as diretivas `@switch`, `@case`, `@break`, `@default` e `@endswitch`:

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```

<a id="loops"></a>
### Laços de Repetição

Além das estruturas condicionais, o Blade oferece diretivas simples para trabalhar com as estruturas de laço do PHP. Novamente, cada uma dessas diretivas funciona de forma idêntica às suas equivalentes em PHP:

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

> **Nota:**
> Ao iterar por um laço `foreach`, você pode usar a [variável de laço](#the-loop-variable) para obter informações valiosas sobre o laço, como se você está na primeira ou na última iteração.

Ao usar laços de repetição, você também pode pular a iteração atual ou encerrar o laço usando as diretivas `@continue` e `@break`:

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

Você também pode incluir a condição de continuação ou de interrupção na declaração da diretiva:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a id="the-loop-variable"></a>
### A Variável de Laço

Enquanto itera por um laço `foreach`, uma variável `$loop` estará disponível dentro do seu laço. Essa variável fornece acesso a algumas informações úteis, como o índice atual do laço e se esta é a primeira ou a última iteração:

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

Se você estiver em um laço aninhado, pode acessar a variável `$loop` do laço pai por meio da propriedade `parent`:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

A variável `$loop` também contém uma variedade de outras propriedades úteis:

<div class="overflow-auto">

| Propriedade        | Descrição                                               |
| ------------------ | ------------------------------------------------------- |
| `$loop->index`     | O índice da iteração atual do laço (começa em 0).       |
| `$loop->iteration` | A iteração atual do laço (começa em 1).                 |
| `$loop->remaining` | As iterações restantes no laço.                         |
| `$loop->count`     | O número total de itens do array sendo iterado.         |
| `$loop->first`     | Se esta é a primeira iteração do laço.                  |
| `$loop->last`      | Se esta é a última iteração do laço.                    |
| `$loop->even`      | Se esta é uma iteração par do laço.                     |
| `$loop->odd`       | Se esta é uma iteração ímpar do laço.                   |
| `$loop->depth`     | O nível de aninhamento do laço atual.                   |
| `$loop->parent`    | Quando em um laço aninhado, a variável de laço do pai.  |

</div>

<a id="conditional-classes"></a>
### Classes e Estilos Condicionais

A diretiva `@class` compila condicionalmente uma string de classes CSS. A diretiva aceita um array de classes em que a chave do array contém a classe ou classes que você deseja adicionar, enquanto o valor é uma expressão booleana. Se o elemento do array tiver uma chave numérica, ele sempre será incluído na lista de classes renderizada:

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```

Da mesma forma, a diretiva `@style` pode ser usada para adicionar condicionalmente estilos CSS inline a um elemento HTML:

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```

<a id="additional-attributes"></a>
### Atributos Adicionais

Por conveniência, você pode usar a diretiva `@checked` para indicar facilmente se um determinado input de checkbox HTML está "marcado". Essa diretiva imprimirá `checked` se a condição fornecida for avaliada como `true`:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

Da mesma forma, a diretiva `@selected` pode ser usada para indicar se uma determinada opção de select deve estar "selecionada":

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

Além disso, a diretiva `@disabled` pode ser usada para indicar se um determinado elemento deve estar "desabilitado":

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

Ademais, a diretiva `@readonly` pode ser usada para indicar se um determinado elemento deve ser "somente leitura":

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

Adicionalmente, a diretiva `@required` pode ser usada para indicar se um determinado elemento deve ser "obrigatório":

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a id="including-subviews"></a>
### Incluindo Subviews

> **Nota:**
> Embora você seja livre para usar a diretiva `@include`, os [componentes](#components) Blade oferecem funcionalidade semelhante e vários benefícios em relação à diretiva `@include`, como vinculação de dados e atributos.

A diretiva `@include` do Blade permite incluir uma view Blade dentro de outra view. Todas as variáveis disponíveis para a view pai também ficarão disponíveis para a view incluída:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

Mesmo que a view incluída herde todos os dados disponíveis na view pai, você também pode passar um array com dados adicionais que devem ficar disponíveis para a view incluída:

```blade
@include('view.name', ['status' => 'complete'])
```

Se você tentar usar `@include` em uma view que não existe, o Laravel lançará um erro. Se você quiser incluir uma view que pode ou não estar presente, deve usar a diretiva `@includeIf`:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

Se você quiser usar `@include` em uma view caso uma determinada expressão booleana seja avaliada como `true` ou `false`, pode usar as diretivas `@includeWhen` e `@includeUnless`:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

Para incluir a primeira view que existir em um determinado array de views, você pode usar a diretiva `includeFirst`:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

Se você quiser incluir uma view sem herdar nenhuma variável da view pai, pode usar a diretiva `@includeIsolated`. A view incluída terá acesso apenas às variáveis que você passar explicitamente:

```blade
@includeIsolated('view.name', ['user' => $user])
```

> **Aviso:**
> Você deve evitar usar as constantes `__DIR__` e `__FILE__` em suas views Blade, pois elas farão referência à localização da view compilada armazenada em cache.

<a id="rendering-views-for-collections"></a>
#### Renderizando Views para Coleções

Você pode combinar laços e includes em uma única linha com a diretiva `@each` do Blade:

```blade
@each('view.name', $jobs, 'job')
```

O primeiro argumento da diretiva `@each` é a view a ser renderizada para cada elemento do array ou coleção. O segundo argumento é o array ou coleção que você deseja iterar, enquanto o terceiro argumento é o nome da variável que será atribuída à iteração atual dentro da view. Assim, por exemplo, se você estiver iterando sobre um array de `jobs`, normalmente desejará acessar cada job como uma variável `job` dentro da view. A chave do array da iteração atual estará disponível como a variável `key` dentro da view.

Você também pode passar um quarto argumento para a diretiva `@each`. Esse argumento determina a view que será renderizada caso o array fornecido esteja vazio.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> **Aviso:**
> Views renderizadas via `@each` não herdam as variáveis da view pai. Se a view filha precisar dessas variáveis, você deve usar as diretivas `@foreach` e `@include`.

<a id="the-once-directive"></a>
### A Diretiva `@once`

A diretiva `@once` permite definir uma parte do template que será avaliada apenas uma vez por ciclo de renderização. Isso pode ser útil para inserir um determinado trecho de JavaScript no cabeçalho da página usando [stacks](#stacks). Por exemplo, se você estiver renderizando um determinado [componente](#components) dentro de um laço, pode querer enviar o JavaScript para o cabeçalho apenas na primeira vez em que o componente for renderizado:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

Como a diretiva `@once` é frequentemente usada em conjunto com as diretivas `@push` ou `@prepend`, as diretivas `@pushOnce` e `@prependOnce` estão disponíveis para sua conveniência:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

Se você estiver enviando conteúdo duplicado a partir de dois templates Blade separados, deve fornecer um identificador único como segundo argumento da diretiva `@pushOnce` para garantir que o conteúdo seja renderizado apenas uma vez:

```blade
<!-- pie-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce

<!-- line-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce
```

<a id="raw-php"></a>
### PHP Puro

Em algumas situações, é útil incorporar código PHP em suas views. Você pode usar a diretiva `@php` do Blade para executar um bloco de PHP puro dentro do seu template:

```blade
@php
    $counter = 1;
@endphp
```

Ou, se você só precisar usar PHP para importar uma classe, pode usar a diretiva `@use`:

```blade
@use('App\Models\Flight')
```

Um segundo argumento pode ser fornecido à diretiva `@use` para criar um alias para a classe importada:

```blade
@use('App\Models\Flight', 'FlightModel')
```

Se você tiver várias classes dentro do mesmo namespace, pode agrupar as importações dessas classes:

```blade
@use('App\Models\{Flight, Airport}')
```

A diretiva `@use` também oferece suporte à importação de funções e constantes PHP, prefixando o caminho de importação com os modificadores `function` ou `const`:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

Assim como nas importações de classes, aliases também são suportados para funções e constantes:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

Importações agrupadas também são suportadas com os modificadores `function` e `const`, permitindo importar vários símbolos do mesmo namespace em uma única diretiva:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a id="fonts"></a>
### Fontes

Ao usar a [otimização de fontes do Vite do Laravel](../vite/#working-with-fonts), você pode usar a diretiva `@fonts` para renderizar os links de preload das fontes configuradas e o CSS inline das fontes no layout da sua aplicação:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @fonts
    @vite('resources/js/app.js')
</head>
```

A diretiva `@fonts` renderiza todas as famílias de fontes configuradas no seu arquivo `vite.config.js`. Normalmente, a diretiva deve ser colocada no `<head>` do layout raiz da sua aplicação, antes de qualquer conteúdo que use essas fontes.

Se uma página precisar apenas de algumas das suas fontes configuradas, você pode passar um ou mais aliases de fontes para a diretiva:

```blade
{{-- Load a single font alias... --}}
@fonts('sans')

{{-- Load multiple font aliases... --}}
@fonts(['sans', 'mono'])
```

Os aliases de fontes são configurados usando a opção `alias` ao definir fontes na sua configuração do Vite. A diretiva `@fonts` chama o método `fonts` fornecido pela facade `Vite`, que também pode ser invocado diretamente:

```blade
{{ Vite::fonts(['sans', 'mono']) }}
```

<a id="comments"></a>
### Comentários

O Blade também permite definir comentários nas suas views. No entanto, diferente dos comentários HTML, os comentários Blade não são incluídos no HTML retornado pela sua aplicação:

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a id="components"></a>
## Componentes

Componentes e slots oferecem benefícios semelhantes aos de seções, layouts e includes; no entanto, alguns podem achar o modelo mental de componentes e slots mais fácil de entender. Há duas abordagens para escrever componentes: componentes baseados em classes e componentes anônimos.

Para criar um componente baseado em classe, você pode usar o comando Artisan `make:component`. Para ilustrar como usar componentes, vamos criar um componente simples `Alert`. O comando `make:component` colocará o componente no diretório `app/View/Components`:

```shell
php artisan make:component Alert
```

O comando `make:component` também criará um template de view para o componente. A view será colocada no diretório `resources/views/components`. Ao escrever componentes para a sua própria aplicação, os componentes são descobertos automaticamente nos diretórios `app/View/Components` e `resources/views/components`, então normalmente não é necessário registrar componentes adicionais.

Você também pode criar componentes em subdiretórios:

```shell
php artisan make:component Forms/Input
```

O comando acima criará um componente `Input` no diretório `app/View/Components/Forms` e a view será colocada no diretório `resources/views/components/forms`.

<a id="manually-registering-package-components"></a>
#### Registrando Componentes de Pacotes Manualmente

Ao escrever componentes para a sua própria aplicação, os componentes são descobertos automaticamente nos diretórios `app/View/Components` e `resources/views/components`.

No entanto, se você estiver construindo um pacote que utiliza componentes Blade, precisará registrar manualmente a sua classe de componente e o seu alias de tag HTML. Normalmente, você deve registrar seus componentes no método `boot` do service provider do seu pacote:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

Depois que seu componente for registrado, ele poderá ser renderizado usando seu alias de tag:

```blade
<x-package-alert/>
```

Alternativamente, você pode usar o método `componentNamespace` para carregar automaticamente as classes de componentes por convenção. Por exemplo, um pacote `Nightshade` pode ter os componentes `Calendar` e `ColorPicker` localizados no namespace `Nightshade\Views\Components`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

Isso permitirá o uso dos componentes do pacote pelo seu namespace de fornecedor, usando a sintaxe `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

O Blade detectará automaticamente a classe vinculada a este componente convertendo o nome do componente para PascalCase. Subdiretórios também são suportados usando a notação de "ponto".

<a id="rendering-components"></a>
### Renderizando Componentes

Para exibir um componente, você pode usar uma tag de componente Blade em um dos seus templates Blade. As tags de componentes Blade começam com a string `x-` seguida do nome da classe do componente em kebab case:

```blade
<x-alert/>

<x-user-profile/>
```

Se a classe do componente estiver aninhada mais profundamente dentro do diretório `app/View/Components`, você pode usar o caractere `.` para indicar o aninhamento de diretórios. Por exemplo, supondo que um componente esteja localizado em `app/View/Components/Inputs/Button.php`, podemos renderizá-lo assim:

```blade
<x-inputs.button/>
```

Se você quiser renderizar seu componente condicionalmente, pode definir um método `shouldRender` na sua classe de componente. Se o método `shouldRender` retornar `false`, o componente não será renderizado:

```php
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a id="index-components"></a>
### Componentes de Índice

Às vezes, os componentes fazem parte de um grupo de componentes e você pode querer agrupar os componentes relacionados em um único diretório. Por exemplo, imagine um componente "card" com a seguinte estrutura de classes:

```text
App\View\Components\Card\Card
App\View\Components\Card\Header
App\View\Components\Card\Body
```

Como o componente `Card` raiz está aninhado dentro de um diretório `Card`, você pode esperar que precise renderizar o componente via `<x-card.card>`. No entanto, quando o nome do arquivo de um componente corresponde ao nome do diretório do componente, o Laravel assume automaticamente que esse componente é o componente "raiz" e permite renderizar o componente sem repetir o nome do diretório:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a id="passing-data-to-components"></a>
### Passando Dados para Componentes

Você pode passar dados para componentes Blade usando atributos HTML. Valores primitivos fixos podem ser passados para o componente usando strings de atributos HTML simples. Expressões PHP e variáveis devem ser passadas para o componente por meio de atributos que usam o caractere `:` como prefixo:

```blade
<x-alert type="error" :message="$message"/>
```

Você deve definir todos os atributos de dados do componente no construtor da sua classe. Todas as propriedades públicas de um componente ficarão automaticamente disponíveis para a view do componente. Não é necessário passar os dados para a view a partir do método `render` do componente:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

Quando o seu componente for renderizado, você pode exibir o conteúdo das variáveis públicas do componente imprimindo as variáveis pelo nome:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a id="casing"></a>
#### Capitalização

Os argumentos do construtor do componente devem ser especificados em `camelCase`, enquanto `kebab-case` deve ser usado ao referenciar os nomes dos argumentos nos seus atributos HTML. Por exemplo, dado o seguinte construtor de componente:

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

O argumento `$alertType` pode ser fornecido ao componente assim:

```blade
<x-alert alert-type="danger" />
```

<a id="short-attribute-syntax"></a>
#### Sintaxe Curta de Atributos

Ao passar atributos para componentes, você também pode usar a sintaxe de "atributo curto". Isso costuma ser conveniente, já que os nomes dos atributos frequentemente correspondem aos nomes das variáveis às quais se referem:

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a id="escaping-attribute-rendering"></a>
#### Escapando a Renderização de Atributos

Como alguns frameworks JavaScript, como o Alpine.js, também usam atributos prefixados por dois-pontos, você pode usar um prefixo de dois-pontos duplo (`::`) para informar ao Blade que o atributo não é uma expressão PHP. Por exemplo, dado o seguinte componente:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

O seguinte HTML será renderizado pelo Blade:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a id="component-methods"></a>
#### Métodos de Componentes

Além de as variáveis públicas estarem disponíveis para o template do seu componente, quaisquer métodos públicos do componente podem ser invocados. Por exemplo, imagine um componente que possui um método `isSelected`:

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

Você pode executar este método a partir do template do seu componente invocando a variável com o mesmo nome do método:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a id="using-attributes-slots-within-component-class"></a>
#### Acessando Atributos e Slots Dentro das Classes de Componentes

Componentes Blade também permitem acessar o nome do componente, os atributos e o slot dentro do método render da classe. No entanto, para acessar esses dados, você deve retornar uma closure a partir do método `render` do seu componente:

```php
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

A closure retornada pelo método `render` do seu componente também pode receber um array `$data` como seu único argumento. Este array conterá vários elementos que fornecem informações sobre o componente:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
};
```

> **Aviso:**
> Os elementos do array `$data` nunca devem ser incorporados diretamente na string Blade retornada pelo seu método `render`, pois isso pode permitir execução remota de código por meio de conteúdo malicioso em atributos.

O `componentName` é igual ao nome usado na tag HTML após o prefixo `x-`. Assim, o `componentName` de `<x-alert />` será `alert`. O elemento `attributes` conterá todos os atributos presentes na tag HTML. O elemento `slot` é uma instância de `Illuminate\View\ComponentSlot` com o conteúdo do slot do componente.

A closure deve retornar uma string. Se a string retornada corresponder a uma view existente, essa view será renderizada; caso contrário, a string retornada será avaliada como uma view Blade inline.

<a id="additional-dependencies"></a>
#### Dependências Adicionais

Se o seu componente exigir dependências do [service container](../container/) do Laravel, você pode listá-las antes de quaisquer atributos de dados do componente e elas serão injetadas automaticamente pelo container:

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a id="hiding-attributes-and-methods"></a>
#### Ocultando Atributos / Métodos

Se você quiser impedir que alguns métodos ou propriedades públicos sejam expostos como variáveis ao template do seu componente, pode adicioná-los a uma propriedade de array `$except` no seu componente:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a id="component-attributes"></a>
### Atributos de Componentes

Já examinamos como passar atributos de dados para um componente; no entanto, às vezes você pode precisar especificar atributos HTML adicionais, como `class`, que não fazem parte dos dados necessários para o funcionamento do componente. Normalmente, você quer passar esses atributos adicionais para o elemento raiz do template do componente. Por exemplo, imagine que queremos renderizar um componente `alert` assim:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

Todos os atributos que não fazem parte do construtor do componente serão automaticamente adicionados ao "attribute bag" do componente. Esse attribute bag fica automaticamente disponível para o componente por meio da variável `$attributes`. Todos os atributos podem ser renderizados dentro do componente imprimindo esta variável:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> **Aviso:**
> Usar diretivas como `@env` dentro de tags de componentes não é suportado no momento. Por exemplo, `<x-alert :live="@env('production')"/>` não será compilado.

<a id="default-merged-attributes"></a>
#### Atributos Padrão / Mesclados

Às vezes, você pode precisar especificar valores padrão para atributos ou mesclar valores adicionais em alguns dos atributos do componente. Para isso, você pode usar o método `merge` do attribute bag. Esse método é particularmente útil para definir um conjunto de classes CSS padrão que devem sempre ser aplicadas a um componente:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

Se assumirmos que este componente é utilizado assim:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

O HTML final renderizado do componente ficará parecido com o seguinte:

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a id="conditionally-merge-classes"></a>
#### Mesclando Classes Condicionalmente

Às vezes, você pode querer mesclar classes se uma determinada condição for `true`. Você pode fazer isso por meio do método `class`, que aceita um array de classes em que a chave do array contém a classe ou classes que deseja adicionar, enquanto o valor é uma expressão booleana. Se o elemento do array tiver uma chave numérica, ele sempre será incluído na lista de classes renderizada:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

Se você precisar mesclar outros atributos ao seu componente, pode encadear o método `merge` após o método `class`:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> **Nota:**
> Se você precisar compilar classes condicionalmente em outros elementos HTML que não devem receber atributos mesclados, pode usar a [diretiva @class](#conditional-classes).

<a id="non-class-attribute-merging"></a>
#### Mesclagem de Atributos que Não São Class

Ao mesclar atributos que não são atributos `class`, os valores fornecidos ao método `merge` serão considerados os valores "padrão" do atributo. No entanto, diferente do atributo `class`, esses atributos não serão mesclados com os valores injetados. Em vez disso, eles serão sobrescritos. Por exemplo, a implementação de um componente `button` pode ser parecida com a seguinte:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

Para renderizar o componente button com um `type` personalizado, ele pode ser especificado ao utilizar o componente. Se nenhum type for especificado, o tipo `button` será usado:

```blade
<x-button type="submit">
    Submit
</x-button>
```

O HTML renderizado do componente `button` neste exemplo seria:

```blade
<button type="submit">
    Submit
</button>
```

Se você quiser que um atributo diferente de `class` tenha seu valor padrão e os valores injetados unidos, pode usar o método `prepends`. Neste exemplo, o atributo `data-controller` sempre começará com `profile-controller` e quaisquer valores adicionais de `data-controller` injetados serão colocados após este valor padrão:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a id="filtering-attributes"></a>
#### Recuperando e Filtrando Atributos

Você pode filtrar atributos usando o método `filter`. Este método aceita uma closure que deve retornar `true` se você quiser manter o atributo no attribute bag:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

Por conveniência, você pode usar o método `whereStartsWith` para recuperar todos os atributos cujas chaves começam com uma determinada string:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

Inversamente, o método `whereDoesntStartWith` pode ser usado para excluir todos os atributos cujas chaves começam com uma determinada string:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

Usando o método `first`, você pode renderizar o primeiro atributo de um determinado attribute bag:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

Se você quiser verificar se um atributo está presente no componente, pode usar o método `has`. Este método aceita o nome do atributo como seu único argumento e retorna um booleano indicando se o atributo está presente:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

Se um array for passado para o método `has`, o método determinará se todos os atributos fornecidos estão presentes no componente:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

O método `hasAny` pode ser usado para determinar se algum dos atributos fornecidos está presente no componente:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

Você pode recuperar o valor de um atributo específico usando o método `get`:

```blade
{{ $attributes->get('class') }}
```

O método `only` pode ser usado para recuperar apenas os atributos com as chaves fornecidas:

```blade
{{ $attributes->only(['class']) }}
```

O método `except` pode ser usado para recuperar todos os atributos, exceto aqueles com as chaves fornecidas:

```blade
{{ $attributes->except(['class']) }}
```

<a id="reserved-keywords"></a>
### Palavras-chave Reservadas

Por padrão, algumas palavras-chave são reservadas para uso interno do Blade a fim de renderizar componentes. As seguintes palavras-chave não podem ser definidas como propriedades públicas ou nomes de métodos dentro dos seus componentes:

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a id="slots"></a>
### Slots

Você frequentemente precisará passar conteúdo adicional para o seu componente por meio de "slots". Os slots de componentes são renderizados imprimindo a variável `$slot`. Para explorar esse conceito, vamos imaginar que um componente `alert` tenha a seguinte marcação:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

Podemos passar conteúdo para o `slot` injetando conteúdo no componente:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Às vezes, um componente pode precisar renderizar vários slots diferentes em locais diferentes dentro do componente. Vamos modificar nosso componente alert para permitir a injeção de um slot "title":

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

Você pode definir o conteúdo do slot nomeado usando a tag `x-slot`. Qualquer conteúdo que não esteja dentro de uma tag `x-slot` explícita será passado para o componente na variável `$slot`:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Você pode invocar o método `isEmpty` de um slot para determinar se ele contém conteúdo:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```

Além disso, o método `hasActualContent` pode ser usado para determinar se o slot contém algum conteúdo "real" que não seja um comentário HTML:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a id="scoped-slots"></a>
#### Slots com Escopo

Se você já usou um framework JavaScript como o Vue, pode estar familiarizado com "scoped slots", que permitem acessar dados ou métodos do componente dentro do seu slot. Você pode obter um comportamento semelhante no Laravel definindo métodos ou propriedades públicos no seu componente e acessando o componente dentro do seu slot pela variável `$component`. Neste exemplo, vamos supor que o componente `x-alert` tenha um método público `formatAlert` definido na sua classe de componente:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a id="slot-attributes"></a>
#### Atributos de Slots

Assim como nos componentes Blade, você pode atribuir [atributos](#component-attributes) adicionais aos slots, como nomes de classes CSS:

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```

Para interagir com os atributos do slot, você pode acessar a propriedade `attributes` da variável do slot. Para mais informações sobre como interagir com atributos, consulte a documentação sobre [atributos de componentes](#component-attributes):

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

<a id="inline-component-views"></a>
### Views de Componentes Inline

Para componentes muito pequenos, pode parecer trabalhoso gerenciar tanto a classe do componente quanto o template da view do componente. Por essa razão, você pode retornar a marcação do componente diretamente do método `render`:

```php
/**
 * Get the view / contents that represent the component.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```

<a id="generating-inline-view-components"></a>
#### Gerando Componentes com View Inline

Para criar um componente que renderiza uma view inline, você pode usar a opção `inline` ao executar o comando `make:component`:

```shell
php artisan make:component Alert --inline
```

<a id="dynamic-components"></a>
### Componentes Dinâmicos

Às vezes, você pode precisar renderizar um componente, mas não saber qual componente deve ser renderizado até o momento da execução. Nessa situação, você pode usar o componente integrado `dynamic-component` do Laravel para renderizar o componente com base em um valor ou variável de tempo de execução:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a id="manually-registering-components"></a>
### Registrando Componentes Manualmente

> **Aviso:**
> A documentação a seguir sobre o registro manual de componentes se aplica principalmente a quem está escrevendo pacotes Laravel que incluem componentes de view. Se você não estiver escrevendo um pacote, esta parte da documentação de componentes pode não ser relevante para você.

Ao escrever componentes para a sua própria aplicação, os componentes são descobertos automaticamente nos diretórios `app/View/Components` e `resources/views/components`.

No entanto, se você estiver construindo um pacote que utiliza componentes Blade ou colocando componentes em diretórios não convencionais, precisará registrar manualmente a sua classe de componente e o seu alias de tag HTML para que o Laravel saiba onde encontrar o componente. Normalmente, você deve registrar seus componentes no método `boot` do service provider do seu pacote:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

Depois que seu componente for registrado, ele poderá ser renderizado usando seu alias de tag:

```blade
<x-package-alert/>
```

#### Carregamento Automático de Componentes de Pacotes

Alternativamente, você pode usar o método `componentNamespace` para carregar automaticamente as classes de componentes por convenção. Por exemplo, um pacote `Nightshade` pode ter os componentes `Calendar` e `ColorPicker` localizados no namespace `Nightshade\Views\Components`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

Isso permitirá o uso dos componentes do pacote pelo seu namespace de fornecedor, usando a sintaxe `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

O Blade detectará automaticamente a classe vinculada a este componente convertendo o nome do componente para PascalCase. Subdiretórios também são suportados usando a notação de "ponto".

<a id="anonymous-components"></a>
## Componentes Anônimos

Semelhantes aos componentes inline, os componentes anônimos oferecem um mecanismo para gerenciar um componente por meio de um único arquivo. No entanto, os componentes anônimos utilizam um único arquivo de view e não possuem uma classe associada. Para definir um componente anônimo, você só precisa colocar um template Blade no seu diretório `resources/views/components`. Por exemplo, supondo que você tenha definido um componente em `resources/views/components/alert.blade.php`, você pode simplesmente renderizá-lo assim:

```blade
<x-alert/>
```

Você pode usar o caractere `.` para indicar se um componente está aninhado mais profundamente dentro do diretório `components`. Por exemplo, supondo que o componente esteja definido em `resources/views/components/inputs/button.blade.php`, você pode renderizá-lo assim:

```blade
<x-inputs.button/>
```

Para criar um componente anônimo via Artisan, você pode usar a flag `--view` ao invocar o comando `make:component`:

```shell
php artisan make:component forms.input --view
```

O comando acima criará um arquivo Blade em `resources/views/components/forms/input.blade.php`, que pode ser renderizado como componente via `<x-forms.input />`.

<a id="anonymous-index-components"></a>
### Componentes de Índice Anônimos

Às vezes, quando um componente é composto por vários templates Blade, você pode querer agrupar os templates do componente em um único diretório. Por exemplo, imagine um componente "accordion" com a seguinte estrutura de diretórios:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

Essa estrutura de diretórios permite renderizar o componente accordion e seu item assim:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

No entanto, para renderizar o componente accordion via `x-accordion`, fomos forçados a colocar o template do componente accordion "índice" no diretório `resources/views/components`, em vez de aninhá-lo dentro do diretório `accordion` junto com os demais templates relacionados ao accordion.

Felizmente, o Blade permite colocar um arquivo com o mesmo nome do diretório do componente dentro do próprio diretório do componente. Quando esse template existe, ele pode ser renderizado como o elemento "raiz" do componente, mesmo estando aninhado em um diretório. Assim, podemos continuar usando a mesma sintaxe Blade do exemplo acima; porém, ajustaremos a estrutura de diretórios assim:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a id="data-properties-attributes"></a>
### Propriedades de Dados / Atributos

Como os componentes anônimos não possuem nenhuma classe associada, você pode se perguntar como diferenciar quais dados devem ser passados para o componente como variáveis e quais atributos devem ser colocados no [attribute bag](#component-attributes) do componente.

Você pode especificar quais atributos devem ser considerados variáveis de dados usando a diretiva `@props` no topo do template Blade do seu componente. Todos os outros atributos do componente estarão disponíveis por meio do attribute bag do componente. Se quiser atribuir um valor padrão a uma variável de dados, pode especificar o nome da variável como chave do array e o valor padrão como valor do array:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

Dada a definição do componente acima, podemos renderizar o componente assim:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a id="accessing-parent-data"></a>
### Acessando Dados do Pai

Às vezes, você pode querer acessar dados de um componente pai dentro de um componente filho. Nesses casos, você pode usar a diretiva `@aware`. Por exemplo, imagine que estamos construindo um componente de menu complexo composto por um `<x-menu>` pai e um `<x-menu.item>` filho:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

O componente `<x-menu>` pode ter uma implementação como a seguinte:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

Como a propriedade `color` foi passada apenas para o pai (`<x-menu>`), ela não estará disponível dentro de `<x-menu.item>`. No entanto, se usarmos a diretiva `@aware`, podemos torná-la disponível também dentro de `<x-menu.item>`:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> **Aviso:**
> A diretiva `@aware` não pode acessar dados do pai que não tenham sido passados explicitamente ao componente pai por meio de atributos HTML. Valores padrão de `@props` que não foram passados explicitamente ao componente pai não podem ser acessados pela diretiva `@aware`.

<a id="anonymous-component-paths"></a>
### Caminhos de Componentes Anônimos

Como discutido anteriormente, componentes anônimos normalmente são definidos colocando um template Blade no seu diretório `resources/views/components`. No entanto, você pode, ocasionalmente, querer registrar outros caminhos de componentes anônimos no Laravel, além do caminho padrão.

O método `anonymousComponentPath` aceita como primeiro argumento o "caminho" para o local dos componentes anônimos e, como segundo argumento opcional, um "namespace" sob o qual os componentes devem ser colocados. Normalmente, este método deve ser chamado a partir do método `boot` de um dos [service providers](../providers/) da sua aplicação:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

Quando caminhos de componentes são registrados sem um prefixo especificado, como no exemplo acima, eles também podem ser renderizados nos seus componentes Blade sem um prefixo correspondente. Por exemplo, se um componente `panel.blade.php` existir no caminho registrado acima, ele pode ser renderizado assim:

```blade
<x-panel />
```

Prefixos de "namespace" podem ser fornecidos como segundo argumento do método `anonymousComponentPath`:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

Quando um prefixo é fornecido, os componentes dentro desse "namespace" podem ser renderizados prefixando o namespace do componente ao nome do componente na hora da renderização:

```blade
<x-dashboard::panel />
```

<a id="building-layouts"></a>
## Construindo Layouts

<a id="layouts-using-components"></a>
### Layouts Usando Componentes

A maioria das aplicações web mantém o mesmo layout geral em diversas páginas. Seria extremamente trabalhoso e difícil de manter nossa aplicação se tivéssemos que repetir todo o HTML do layout em cada view que criamos. Felizmente, é conveniente definir esse layout como um único [componente Blade](#components) e, em seguida, usá-lo em toda a aplicação.

<a id="defining-the-layout-component"></a>
#### Definindo o Componente de Layout

Por exemplo, imagine que estamos construindo uma aplicação de lista de "tarefas". Podemos definir um componente `layout` com a seguinte aparência:

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a id="applying-the-layout-component"></a>
#### Aplicando o Componente de Layout

Depois que o componente `layout` for definido, podemos criar uma view Blade que utiliza o componente. Neste exemplo, definiremos uma view simples que exibe nossa lista de tarefas:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

Lembre-se de que o conteúdo injetado em um componente será fornecido à variável `$slot` padrão dentro do nosso componente `layout`. Como você deve ter notado, nosso `layout` também respeita um slot `$title`, caso seja fornecido; caso contrário, um título padrão é exibido. Podemos injetar um título personalizado a partir da nossa view de lista de tarefas usando a sintaxe padrão de slots discutida na [documentação de componentes](#components):

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

Agora que definimos nossas views de layout e de lista de tarefas, só precisamos retornar a view `task` a partir de uma rota:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a id="layouts-using-template-inheritance"></a>
### Layouts Usando Herança de Templates

<a id="defining-a-layout"></a>
#### Definindo um Layout

Layouts também podem ser criados por meio de "herança de templates". Essa era a principal forma de construir aplicações antes da introdução de [componentes](#components).

Para começar, vamos examinar um exemplo simples. Primeiro, analisaremos um layout de página. Como a maioria das aplicações web mantém o mesmo layout geral em diversas páginas, é conveniente definir esse layout como uma única view Blade:

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

Como você pode ver, este arquivo contém marcação HTML típica. No entanto, preste atenção nas diretivas `@section` e `@yield`. A diretiva `@section`, como o nome sugere, define uma seção de conteúdo, enquanto a diretiva `@yield` é usada para exibir o conteúdo de uma determinada seção.

Agora que definimos um layout para a nossa aplicação, vamos definir uma página filha que herda o layout.

<a id="extending-a-layout"></a>
#### Estendendo um Layout

Ao definir uma view filha, use a diretiva Blade `@extends` para especificar de qual layout a view filha deve "herdar". Views que estendem um layout Blade podem injetar conteúdo nas seções do layout usando as diretivas `@section`. Lembre-se de que, como visto no exemplo acima, o conteúdo dessas seções será exibido no layout usando `@yield`:

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

Neste exemplo, a seção `sidebar` utiliza a diretiva `@@parent` para anexar (em vez de sobrescrever) conteúdo à sidebar do layout. A diretiva `@@parent` será substituída pelo conteúdo do layout quando a view for renderizada.

> **Nota:**
> Diferente do exemplo anterior, esta seção `sidebar` termina com `@endsection` em vez de `@show`. A diretiva `@endsection` apenas define uma seção, enquanto `@show` define a seção e a **retorna imediatamente**.

A diretiva `@yield` também aceita um valor padrão como seu segundo parâmetro. Esse valor será renderizado se a seção solicitada não estiver definida:

```blade
@yield('content', 'Default content')
```

<a id="forms"></a>
## Formulários

<a id="csrf-field"></a>
### Campo CSRF

Sempre que você definir um formulário HTML na sua aplicação, deve incluir um campo oculto de token CSRF no formulário para que o middleware de [proteção CSRF](../csrf/) possa validar a requisição. Você pode usar a diretiva Blade `@csrf` para gerar o campo de token:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a id="method-field"></a>
### Campo de Método

Como formulários HTML não podem realizar requisições `PUT`, `PATCH` ou `DELETE`, você precisará adicionar um campo oculto `_method` para simular esses verbos HTTP. A diretiva Blade `@method` pode criar esse campo para você:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a id="validation-errors"></a>
### Erros de Validação

A diretiva `@error` pode ser usada para verificar rapidamente se [mensagens de erro de validação](../validation/#quick-displaying-the-validation-errors) existem para um determinado atributo. Dentro de uma diretiva `@error`, você pode imprimir a variável `$message` para exibir a mensagem de erro:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

Como a diretiva `@error` é compilada para uma estrutura "if", você pode usar a diretiva `@else` para renderizar conteúdo quando não houver erro para um atributo:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

Você pode passar [o nome de um bag de erros específico](../validation/#named-error-bags) como segundo parâmetro da diretiva `@error` para recuperar mensagens de erro de validação em páginas que contêm vários formulários:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror"
/>

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a id="stacks"></a>
## Stacks

O Blade permite adicionar conteúdo a stacks nomeadas que podem ser renderizadas em outro lugar, em outra view ou layout. Isso pode ser especialmente útil para especificar quaisquer bibliotecas JavaScript exigidas pelas suas views filhas:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

Se você quiser usar `@push` para adicionar conteúdo caso uma determinada expressão booleana seja avaliada como `true`, pode usar a diretiva `@pushIf`:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

Você pode adicionar conteúdo a uma stack quantas vezes for necessário. Para renderizar o conteúdo completo da stack, passe o nome da stack para a diretiva `@stack`:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

A diretiva `@stack` renderiza o conteúdo que foi adicionado até o momento em que é alcançada. Conteúdo adicionado depois, como o de um componente renderizado abaixo da diretiva `@stack` no mesmo componente de layout, não será incluído. Se você precisar adicionar conteúdo a partir de tais componentes, posicione a diretiva `@stack` depois deles, por exemplo, no final da tag `<body>`.

Se você quiser adicionar conteúdo no início de uma stack, deve usar a diretiva `@prepend`:

```blade
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

A diretiva `@hasstack` pode ser usada para determinar se uma stack está vazia:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a id="service-injection"></a>
## Injeção de Serviços

A diretiva `@inject` pode ser usada para recuperar um serviço do [service container](../container/) do Laravel. O primeiro argumento passado para `@inject` é o nome da variável na qual o serviço será colocado, enquanto o segundo argumento é o nome da classe ou interface do serviço que você deseja resolver:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a id="rendering-inline-blade-templates"></a>
## Renderizando Templates Blade Inline

Às vezes, pode ser necessário transformar uma string bruta de template Blade em HTML válido. Você pode fazer isso usando o método `render` fornecido pela facade `Blade`. O método `render` aceita a string do template Blade e um array opcional de dados para fornecer ao template:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

O Laravel renderiza templates Blade inline gravando-os no diretório `storage/framework/views`. Se você quiser que o Laravel remova esses arquivos temporários após renderizar o template Blade, pode fornecer o argumento `deleteCachedView` ao método:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a id="rendering-blade-fragments"></a>
## Renderizando Fragmentos Blade

Ao usar frameworks de frontend como [Turbo](https://turbo.hotwired.dev/) e [htmx](https://htmx.org/), você pode, ocasionalmente, precisar retornar apenas uma parte de um template Blade na sua resposta HTTP. Os "fragmentos" Blade permitem fazer exatamente isso. Para começar, coloque uma parte do seu template Blade dentro das diretivas `@fragment` e `@endfragment`:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

Em seguida, ao renderizar a view que utiliza este template, você pode invocar o método `fragment` para especificar que apenas o fragmento indicado deve ser incluído na resposta HTTP enviada:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

O método `fragmentIf` permite retornar condicionalmente um fragmento de uma view com base em uma determinada condição. Caso contrário, a view inteira será retornada:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

Os métodos `fragments` e `fragmentsIf` permitem retornar vários fragmentos de view na resposta. Os fragmentos serão concatenados entre si:

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```

<a id="extending-blade"></a>
## Estendendo o Blade

O Blade permite definir suas próprias diretivas personalizadas usando o método `directive`. Quando o compilador Blade encontra a diretiva personalizada, ele chama o callback fornecido com a expressão que a diretiva contém.

O exemplo a seguir cria uma diretiva `@datetime($var)` que formata uma determinada `$var`, que deve ser uma instância de `DateTime`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

Como você pode ver, encadearemos o método `format` a qualquer expressão passada para a diretiva. Assim, neste exemplo, o PHP final gerado por esta diretiva será:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> **Aviso:**
> Após atualizar a lógica de uma diretiva Blade, você precisará excluir todas as views Blade armazenadas em cache. As views Blade em cache podem ser removidas usando o comando Artisan `view:clear`.

<a id="custom-echo-handlers"></a>
### Manipuladores de Echo Personalizados

Se você tentar "imprimir" um objeto usando o Blade, o método `__toString` do objeto será invocado. O método [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) é um dos "métodos mágicos" integrados do PHP. No entanto, às vezes você pode não ter controle sobre o método `__toString` de uma determinada classe, como quando a classe com a qual você está interagindo pertence a uma biblioteca de terceiros.

Nesses casos, o Blade permite registrar um manipulador de echo personalizado para aquele tipo específico de objeto. Para isso, você deve invocar o método `stringable` do Blade. O método `stringable` aceita uma closure. Essa closure deve tipar o tipo de objeto pelo qual é responsável pela renderização. Normalmente, o método `stringable` deve ser invocado dentro do método `boot` da sua classe `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

Depois que seu manipulador de echo personalizado for definido, você pode simplesmente imprimir o objeto no seu template Blade:

```blade
Cost: {{ $money }}
```

<a id="custom-if-statements"></a>
### Estruturas If Personalizadas

Criar uma diretiva personalizada às vezes é mais complexo do que o necessário ao definir estruturas condicionais personalizadas simples. Por esse motivo, o Blade oferece o método `Blade::if`, que permite definir rapidamente diretivas condicionais personalizadas usando closures. Por exemplo, vamos definir uma condicional personalizada que verifica o "disco" padrão configurado para a aplicação. Podemos fazer isso no método `boot` do nosso `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

Depois que a condicional personalizada for definida, você poderá usá-la nos seus templates:

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```
