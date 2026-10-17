---
title: "Views"
---

- [Introdução](#introduction)
    - [Escrevendo Views em React / Svelte / Vue](#writing-views-in-react-svelte-or-vue)
- [Criando e Renderizando Views](#creating-and-rendering-views)
    - [Diretórios de View Aninhados](#nested-view-directories)
    - [Criando a Primeira View Disponível](#creating-the-first-available-view)
    - [Determinando se uma View Existe](#determining-if-a-view-exists)
- [Passando Dados para as Views](#passing-data-to-views)
    - [Compartilhando Dados com Todas as Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
    - [View Creators](#view-creators)
- [Otimizando Views](#optimizing-views)

<a id="introduction"></a>
## Introdução

É claro que não é prático retornar strings de documentos HTML inteiros diretamente das suas rotas e controllers. Felizmente, as views fornecem uma maneira conveniente de colocar todo o nosso HTML em arquivos separados.

As views separam a lógica do seu controller / aplicação da sua lógica de apresentação e são armazenadas no diretório `resources/views`. Ao usar o Laravel, os templates de view normalmente são escritos usando a [linguagem de templates Blade](../blade/). Uma view simples pode ser parecida com esta:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

Como esta view é armazenada em `resources/views/greeting.blade.php`, podemos retorná-la usando o helper global `view` assim:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> **Nota:**
> Procurando por mais informações sobre como escrever templates Blade? Confira a [documentação completa do Blade](../blade/) para começar.

<a id="writing-views-in-react-svelte-or-vue"></a>
### Escrevendo Views em React / Svelte / Vue

Em vez de escrever seus templates de frontend em PHP via Blade, muitos desenvolvedores passaram a preferir escrever seus templates usando React, Svelte ou Vue. O Laravel torna isso indolor graças ao [Inertia](https://inertiajs.com/), uma biblioteca que facilita conectar seu frontend React / Svelte / Vue ao seu backend Laravel sem as complexidades típicas de construir uma SPA.

Nossos [starter kits de aplicação para React, Svelte e Vue](../starter-kits/) oferecem um ótimo ponto de partida para sua próxima aplicação Laravel impulsionada pelo Inertia.

<a id="creating-and-rendering-views"></a>
## Criando e Renderizando Views

Você pode criar uma view colocando um arquivo com a extensão `.blade.php` no diretório `resources/views` da sua aplicação ou usando o comando Artisan `make:view`:

```shell
php artisan make:view greeting
```

A extensão `.blade.php` informa ao framework que o arquivo contém um [template Blade](../blade/). Os templates Blade contêm HTML, bem como diretivas Blade que permitem que você facilmente exiba valores, crie declarações "if", itere sobre dados e muito mais.

Depois de criar uma view, você pode retorná-la de uma das rotas ou controllers da sua aplicação usando o helper global `view`:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

As views também podem ser retornadas usando a facade `View`:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

Como você pode ver, o primeiro argumento passado ao helper `view` corresponde ao nome do arquivo de view no diretório `resources/views`. O segundo argumento é um array de dados que deve ser disponibilizado para a view. Neste caso, estamos passando a variável `name`, que é exibida na view usando a [sintaxe Blade](../blade/).

<a id="nested-view-directories"></a>
### Diretórios de View Aninhados

As views também podem ser aninhadas dentro de subdiretórios do diretório `resources/views`. A notação de "ponto" pode ser usada para referenciar views aninhadas. Por exemplo, se a sua view estiver armazenada em `resources/views/admin/profile.blade.php`, você pode retorná-la de uma das rotas / controllers da sua aplicação assim:

```php
return view('admin.profile', $data);
```

> **Aviso:**
> Os nomes dos diretórios de view não devem conter o caractere `.`.

<a id="creating-the-first-available-view"></a>
### Criando a Primeira View Disponível

Usando o método `first` da facade `View`, você pode criar a primeira view que existe em um determinado array de views. Isso pode ser útil se a sua aplicação ou pacote permitir que as views sejam personalizadas ou sobrescritas:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a id="determining-if-a-view-exists"></a>
### Determinando se uma View Existe

Se você precisar determinar se uma view existe, você pode usar a facade `View`. O método `exists` retornará `true` se a view existir:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a id="passing-data-to-views"></a>
## Passando Dados para as Views

Como você viu nos exemplos anteriores, você pode passar um array de dados para as views para disponibilizar esses dados para a view:

```php
return view('greetings', ['name' => 'Victoria']);
```

Ao passar informações desta maneira, os dados devem ser um array com pares chave / valor. Depois de fornecer dados para uma view, você pode então acessar cada valor dentro da sua view usando as chaves dos dados, como `<?php echo $name; ?>`.

Como alternativa a passar um array completo de dados para a função helper `view`, você pode usar o método `with` para adicionar pedaços individuais de dados à view. O método `with` retorna uma instância do objeto de view para que você possa continuar encadeando métodos antes de retornar a view:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a id="sharing-data-with-all-views"></a>
### Compartilhando Dados com Todas as Views

Ocasionalmente, você pode precisar compartilhar dados com todas as views que são renderizadas pela sua aplicação. Você pode fazer isso usando o método `share` da facade `View`. Normalmente, você deve colocar as chamadas ao método `share` dentro do método `boot` de um provedor de serviço. Você está livre para adicioná-las à classe `App\Providers\AppServiceProvider` ou gerar um provedor de serviço separado para abrigá-las:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
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
        View::share('key', 'value');
    }
}
```

<a id="view-composers"></a>
## View Composers

Os view composers são callbacks ou métodos de classe que são chamados quando uma view é renderizada. Se você tiver dados que deseja vincular a uma view toda vez que essa view for renderizada, um view composer pode ajudá-lo a organizar essa lógica em um único local. Os view composers podem ser particularmente úteis se a mesma view for retornada por múltiplas rotas ou controllers dentro da sua aplicação e sempre precisar de um determinado pedaço de dados.

Normalmente, os view composers serão registrados dentro de um dos [provedores de serviço](../providers/) da sua aplicação. Neste exemplo, vamos assumir que o `App\Providers\AppServiceProvider` abrigará essa lógica.

Usaremos o método `composer` da facade `View` para registrar o view composer. O Laravel não inclui um diretório padrão para view composers baseados em classes, então você está livre para organizá-los como quiser. Por exemplo, você poderia criar um diretório `app/View/Composers` para abrigar todos os view composers da sua aplicação:

```php
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

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
        // Using class-based composers...
        Facades\View::composer('profile', ProfileComposer::class);

        // Using closure-based composers...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

Agora que registramos o composer, o método `compose` da classe `App\View\Composers\ProfileComposer` será executado toda vez que a view `profile` estiver sendo renderizada. Vamos dar uma olhada em um exemplo da classe composer:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * Create a new profile composer.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Bind data to the view.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

Como você pode ver, todos os view composers são resolvidos via [container de serviço](../container/), então você pode fazer type-hint de quaisquer dependências que precisar dentro do construtor de um composer.

<a id="attaching-a-composer-to-multiple-views"></a>
#### Anexando um Composer a Múltiplas Views

Você pode anexar um view composer a múltiplas views de uma vez passando um array de views como primeiro argumento ao método `composer`:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

O método `composer` também aceita o caractere `*` como curinga, permitindo que você anexe um composer a todas as views:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a id="view-creators"></a>
### View Creators

Os view "creators" são muito semelhantes aos view composers; no entanto, eles são executados imediatamente após a view ser instanciada, em vez de esperar até que a view esteja prestes a ser renderizada. Para registrar um view creator, use o método `creator`:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a id="optimizing-views"></a>
## Otimizando Views

Por padrão, as views de template Blade são compiladas sob demanda. Quando uma requisição é executada e renderiza uma view, o Laravel determinará se existe uma versão compilada da view. Se o arquivo existir, o Laravel então determinará se a view não compilada foi modificada mais recentemente do que a view compilada. Se a view compilada não existir, ou se a view não compilada tiver sido modificada, o Laravel recompilará a view.

Compilar views durante a requisição pode ter um pequeno impacto negativo no desempenho, então o Laravel fornece o comando Artisan `view:cache` para pré-compilar todas as views utilizadas pela sua aplicação. Para aumentar o desempenho, você pode querer executar este comando como parte do seu processo de deploy:

```shell
php artisan view:cache
```

Você pode usar o comando `view:clear` para limpar o cache de views:

```shell
php artisan view:clear
```
