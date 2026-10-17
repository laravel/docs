---
title: "Desenvolvimento de Pacotes"
---

- [Introdução](#introduction)
    - [Criando um Pacote](#creating-a-package)
    - [Uma Observação Sobre Facades](#a-note-on-facades)
- [Descoberta de Pacotes](#package-discovery)
- [Service Providers](#service-providers)
- [Recursos](#resources)
    - [Configuração](#configuration)
    - [Rotas](#routes)
    - [Migrations](#migrations)
    - [Arquivos de Idioma](#language-files)
    - [Views](#views)
    - [Componentes de View](#view-components)
    - [Comando Artisan "About"](#about-artisan-command)
- [Comandos](#commands)
    - [Comandos de Otimização](#optimize-commands)
    - [Comandos de Recarregamento](#reload-commands)
- [Assets Públicos](#public-assets)
- [Publicando Grupos de Arquivos](#publishing-file-groups)

<a id="introduction"></a>
## Introdução

Pacotes são a principal forma de adicionar funcionalidades ao Laravel. Um pacote pode ser desde uma ótima forma de trabalhar com datas, como o [Carbon](https://github.com/briannesbitt/Carbon), até um pacote que permite associar arquivos a models Eloquent, como o [Laravel Media Library](https://github.com/spatie/laravel-medialibrary) da Spatie.

Existem diferentes tipos de pacotes. Alguns pacotes são independentes, o que significa que funcionam com qualquer framework PHP. Carbon e Pest são exemplos de pacotes independentes. Qualquer um desses pacotes pode ser usado com o Laravel bastando requisitá-lo no seu arquivo `composer.json`.

Por outro lado, outros pacotes são destinados especificamente ao uso com o Laravel. Esses pacotes podem ter rotas, controllers, views e configurações pensados para aprimorar uma aplicação Laravel. Este guia aborda principalmente o desenvolvimento desses pacotes específicos do Laravel.

<a id="creating-a-package"></a>
### Criando um Pacote

A forma mais fácil de começar a construir um novo pacote Laravel é usar o [esqueleto oficial de pacotes do Laravel](https://github.com/laravel/package-skeleton). O esqueleto fornece tudo o que você precisa para construir um pacote Laravel, incluindo um service provider, testes com Pest, análise estática com Larastan, formatação de código com Pint e uma aplicação workbench para o desenvolvimento de ponta a ponta do pacote. Você pode criar um novo pacote usando o comando `package` do [instalador CLI do Laravel](../installation/#creating-a-laravel-project):

```shell
laravel package my-package
```

Um script de configuração interativo personalizará o esqueleto para o seu pacote, configurando seu namespace, seu service provider e apenas os recursos de que você precisa, como arquivos de configuração, rotas, views, traduções, migrations, assets, comandos e uma facade.

<a id="a-note-on-facades"></a>
### Uma Observação Sobre Facades

Ao escrever uma aplicação Laravel, geralmente não importa se você usa contratos ou facades, já que ambos oferecem essencialmente o mesmo nível de testabilidade. No entanto, ao escrever pacotes, o seu pacote normalmente não terá acesso a todos os helpers de teste do Laravel. Se você quiser escrever os testes do seu pacote como se ele estivesse instalado dentro de uma aplicação Laravel típica, pode usar o pacote [Orchestral Testbench](https://github.com/orchestral/testbench).

<a id="package-discovery"></a>
## Descoberta de Pacotes

O arquivo `bootstrap/providers.php` de uma aplicação Laravel contém a lista de service providers que devem ser carregados pelo Laravel. No entanto, em vez de exigir que os usuários adicionem manualmente o seu service provider à lista, você pode definir o provider na seção `extra` do arquivo `composer.json` do seu pacote, para que ele seja carregado automaticamente pelo Laravel. Além dos service providers, você também pode listar quaisquer [facades](../facades/) que deseja registrar:

```json
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},
```

Depois que o seu pacote estiver configurado para descoberta, o Laravel registrará automaticamente seus service providers e facades quando ele for instalado, criando uma experiência de instalação prática para os usuários do seu pacote.

<a id="opting-out-of-package-discovery"></a>
#### Desativando a Descoberta de Pacotes

Se você é consumidor de um pacote e deseja desativar a descoberta de pacotes para ele, pode listar o nome do pacote na seção `extra` do arquivo `composer.json` da sua aplicação:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

Você pode desativar a descoberta de pacotes para todos os pacotes usando o caractere `*` dentro da diretiva `dont-discover` da sua aplicação:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a id="service-providers"></a>
## Service Providers

[Service providers](../providers/) são o ponto de conexão entre o seu pacote e o Laravel. Um service provider é responsável por registrar bindings no [service container](../container/) do Laravel e informar ao Laravel onde carregar os recursos do pacote, como views, arquivos de configuração e arquivos de idioma.

Um service provider estende a classe `Illuminate\Support\ServiceProvider` e contém dois métodos: `register` e `boot`. A classe base `ServiceProvider` está localizada no pacote Composer `illuminate/support`, que você deve adicionar às dependências do seu próprio pacote. Para saber mais sobre a estrutura e a finalidade dos service providers, consulte [a documentação deles](../providers/).

<a id="resources"></a>
## Recursos

<a id="configuration"></a>
### Configuração

Normalmente, você precisará publicar o arquivo de configuração do seu pacote no diretório `config` da aplicação. Isso permitirá que os usuários do seu pacote substituam facilmente as opções de configuração padrão. Para permitir que seus arquivos de configuração sejam publicados, chame o método `publishes` a partir do método `boot` do seu service provider:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

Agora, quando os usuários do seu pacote executarem o comando `vendor:publish` do Laravel, seu arquivo será copiado para o local de publicação especificado. Depois que sua configuração for publicada, seus valores poderão ser acessados como qualquer outro arquivo de configuração:

```php
$value = config('courier.option');
```

> **Aviso:**
> Você não deve definir closures nos seus arquivos de configuração. Elas não podem ser serializadas corretamente quando os usuários executam o comando Artisan `config:cache`.

<a id="default-package-configuration"></a>
#### Configuração Padrão do Pacote

Você também pode mesclar o seu próprio arquivo de configuração de pacote com a cópia publicada da aplicação. Isso permitirá que seus usuários definam apenas as opções que realmente desejam substituir na cópia publicada do arquivo de configuração. Para mesclar os valores do arquivo de configuração, use o método `mergeConfigFrom` dentro do método `register` do seu service provider.

O método `mergeConfigFrom` aceita como primeiro argumento o caminho do arquivo de configuração do seu pacote, e como segundo argumento o nome da cópia do arquivo de configuração da aplicação:

```php
/**
 * Register any package services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> **Aviso:**
> Este método mescla apenas o primeiro nível do array de configuração. Se seus usuários definirem parcialmente um array de configuração multidimensional, as opções ausentes não serão mescladas.

<a id="routes"></a>
### Rotas

Se o seu pacote contiver rotas, você pode carregá-las usando o método `loadRoutesFrom`. Este método determina automaticamente se as rotas da aplicação estão em cache e não carregará o arquivo de rotas do seu pacote se as rotas já estiverem em cache:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a id="migrations"></a>
### Migrations

Se o seu pacote contiver [migrations de banco de dados](../migrations/), você pode usar o método `publishesMigrations` para informar ao Laravel que o diretório ou arquivo fornecido contém migrations. Quando o Laravel publica as migrations, ele atualiza automaticamente o timestamp no nome do arquivo para refletir a data e hora atuais:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishesMigrations([
        __DIR__.'/../database/migrations' => database_path('migrations'),
    ]);
}
```

<a id="language-files"></a>
### Arquivos de Idioma

Se o seu pacote contiver [arquivos de idioma](../localization/), você pode usar o método `loadTranslationsFrom` para informar ao Laravel como carregá-los. Por exemplo, se o nome do seu pacote for `courier`, você deve adicionar o seguinte ao método `boot` do seu service provider:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

As linhas de tradução do pacote são referenciadas usando a convenção de sintaxe `package::file.line`. Assim, você pode carregar a linha `welcome` do arquivo `messages` do pacote `courier` da seguinte forma:

```php
echo trans('courier::messages.welcome');
```

Você pode registrar arquivos de tradução JSON para o seu pacote usando o método `loadJsonTranslationsFrom`. Este método aceita o caminho do diretório que contém os arquivos de tradução JSON do seu pacote:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a id="publishing-language-files"></a>
#### Publicando Arquivos de Idioma

Se você quiser publicar os arquivos de idioma do seu pacote no diretório `lang/vendor` da aplicação, pode usar o método `publishes` do service provider. O método `publishes` aceita um array de caminhos do pacote e seus locais de publicação desejados. Por exemplo, para publicar os arquivos de idioma do pacote `courier`, você pode fazer o seguinte:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

Agora, quando os usuários do seu pacote executarem o comando Artisan `vendor:publish` do Laravel, os arquivos de idioma do seu pacote serão publicados no local de publicação especificado.

<a id="views"></a>
### Views

Para registrar as [views](../views/) do seu pacote no Laravel, você precisa informar ao Laravel onde elas estão localizadas. Você pode fazer isso usando o método `loadViewsFrom` do service provider. O método `loadViewsFrom` aceita dois argumentos: o caminho para os templates de view e o nome do seu pacote. Por exemplo, se o nome do seu pacote for `courier`, você adicionaria o seguinte ao método `boot` do seu service provider:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

As views do pacote são referenciadas usando a convenção de sintaxe `package::view`. Assim, depois que o caminho das suas views estiver registrado em um service provider, você pode carregar a view `dashboard` do pacote `courier` da seguinte forma:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a id="overriding-package-views"></a>
#### Sobrescrevendo Views de Pacotes

Quando você usa o método `loadViewsFrom`, o Laravel na verdade registra dois locais para as suas views: o diretório `resources/views/vendor` da aplicação e o diretório que você especificar. Então, usando o pacote `courier` como exemplo, o Laravel verificará primeiro se uma versão personalizada da view foi colocada pelo desenvolvedor no diretório `resources/views/vendor/courier`. Em seguida, se a view não tiver sido personalizada, o Laravel procurará no diretório de views do pacote que você especificou na chamada a `loadViewsFrom`. Isso facilita que os usuários do pacote personalizem / sobrescrevam as views do seu pacote.

<a id="publishing-views"></a>
#### Publicando Views

Se você quiser disponibilizar suas views para publicação no diretório `resources/views/vendor` da aplicação, pode usar o método `publishes` do service provider. O método `publishes` aceita um array de caminhos de views do pacote e seus locais de publicação desejados:

```php
/**
 * Bootstrap the package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

Agora, quando os usuários do seu pacote executarem o comando Artisan `vendor:publish` do Laravel, as views do seu pacote serão copiadas para o local de publicação especificado.

<a id="view-components"></a>
### Componentes de View

Se você estiver construindo um pacote que utiliza componentes Blade ou coloca componentes em diretórios não convencionais, será necessário registrar manualmente a classe do componente e o alias da sua tag HTML para que o Laravel saiba onde encontrar o componente. Normalmente, você deve registrar seus componentes no método `boot` do service provider do seu pacote:

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

Depois que o componente estiver registrado, ele pode ser renderizado usando o seu alias de tag:

```blade
<x-package-alert/>
```

<a id="autoloading-package-components"></a>
#### Carregamento Automático de Componentes de Pacotes

Alternativamente, você pode usar o método `componentNamespace` para carregar automaticamente classes de componentes por convenção. Por exemplo, um pacote `Nightshade` pode ter os componentes `Calendar` e `ColorPicker`, que residem dentro do namespace `Nightshade\Views\Components`:

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

Isso permitirá o uso dos componentes do pacote pelo namespace do fornecedor, usando a sintaxe `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

O Blade detectará automaticamente a classe vinculada a este componente convertendo o nome do componente para PascalCase. Subdiretórios também são suportados usando a notação de "ponto".

<a id="anonymous-components"></a>
#### Componentes Anônimos

Se o seu pacote contiver componentes anônimos, eles devem ser colocados dentro de um diretório `components` do diretório de "views" do seu pacote (conforme especificado pelo [método loadViewsFrom](#views)). Então, você pode renderizá-los prefixando o nome do componente com o namespace de views do pacote:

```blade
<x-courier::alert />
```

<a id="about-artisan-command"></a>
### Comando Artisan "About"

O comando Artisan `about` nativo do Laravel fornece um resumo do ambiente e da configuração da aplicação. Pacotes podem adicionar informações extras à saída desse comando por meio da classe `AboutCommand`. Normalmente, essas informações podem ser adicionadas a partir do método `boot` do service provider do seu pacote:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a id="commands"></a>
## Comandos

Para registrar os comandos Artisan do seu pacote no Laravel, você pode usar o método `commands`. Este método espera um array de nomes de classes de comando. Depois que os comandos estiverem registrados, você poderá executá-los usando a [CLI do Artisan](../artisan/):

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a id="optimize-commands"></a>
### Comandos de Otimização

O comando [optimize](../deployment/#optimization) do Laravel armazena em cache a configuração, os eventos, as rotas e as views da aplicação. Usando o método `optimizes`, você pode registrar os comandos Artisan do seu próprio pacote que devem ser invocados quando os comandos `optimize` e `optimize:clear` forem executados:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->optimizes(
            optimize: 'package:optimize',
            clear: 'package:clear-optimizations',
        );
    }
}
```

<a id="reload-commands"></a>
### Comandos de Recarregamento

O comando [reload](../deployment/#reloading-services) do Laravel encerra os serviços em execução para que possam ser reiniciados automaticamente por um monitor de processos do sistema. Usando o método `reloads`, você pode registrar os comandos Artisan do seu próprio pacote que devem ser invocados quando o comando `reload` for executado:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->reloads('package:reload');
    }
}
```

<a id="public-assets"></a>
## Assets Públicos

Seu pacote pode ter assets como JavaScript, CSS e imagens. Para publicar esses assets no diretório `public` da aplicação, use o método `publishes` do service provider. Neste exemplo, também adicionaremos uma tag de grupo de assets `public`, que pode ser usada para publicar facilmente grupos de assets relacionados:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

Agora, quando os usuários do seu pacote executarem o comando `vendor:publish`, seus assets serão copiados para o local de publicação especificado. Como os usuários normalmente precisarão sobrescrever os assets sempre que o pacote for atualizado, eles podem usar a flag `--force`:

```shell
php artisan vendor:publish --tag=public --force
```

<a id="publishing-file-groups"></a>
## Publicando Grupos de Arquivos

Você pode querer publicar grupos de assets e recursos do pacote separadamente. Por exemplo, você pode querer permitir que seus usuários publiquem os arquivos de configuração do seu pacote sem serem obrigados a publicar os assets do pacote. Você pode fazer isso "marcando" os arquivos ao chamar o método `publishes` a partir do service provider do pacote. Por exemplo, vamos usar tags para definir dois grupos de publicação para o pacote `courier` (`courier-config` e `courier-migrations`) no método `boot` do service provider do pacote:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishesMigrations([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

Agora, seus usuários podem publicar esses grupos separadamente referenciando a tag deles ao executar o comando `vendor:publish`:

```shell
php artisan vendor:publish --tag=courier-config
```

Seus usuários também podem publicar todos os arquivos publicáveis definidos pelo service provider do seu pacote usando a flag `--provider`:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
