---
title: "Laravel Dusk"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Gerenciando Instalações do ChromeDriver](#managing-chromedriver-installations)
    - [Usando Outros Navegadores](#using-other-browsers)
- [Primeiros Passos](#getting-started)
    - [Gerando Testes](#generating-tests)
    - [Resetando o Banco de Dados Após Cada Teste](#resetting-the-database-after-each-test)
    - [Executando Testes](#running-tests)
    - [Tratamento de Ambiente](#environment-handling)
- [Noções Básicas de Navegador](#browser-basics)
    - [Criando Navegadores](#creating-browsers)
    - [Navegação](#navigation)
    - [Redimensionando Janelas do Navegador](#resizing-browser-windows)
    - [Macros de Navegador](#browser-macros)
    - [Autenticação](#authentication)
    - [Cookies](#cookies)
    - [Executando JavaScript](#executing-javascript)
    - [Capturando uma Screenshot](#taking-a-screenshot)
    - [Armazenando a Saída do Console em Disco](#storing-console-output-to-disk)
    - [Armazenando o Código-Fonte da Página em Disco](#storing-page-source-to-disk)
- [Interagindo com Elementos](#interacting-with-elements)
    - [Seletores Dusk](#dusk-selectors)
    - [Texto, Valores e Atributos](#text-values-and-attributes)
    - [Interagindo com Formulários](#interacting-with-forms)
    - [Anexando Arquivos](#attaching-files)
    - [Pressionando Botões](#pressing-buttons)
    - [Clicando em Links](#clicking-links)
    - [Usando o Teclado](#using-the-keyboard)
    - [Usando o Mouse](#using-the-mouse)
    - [Diálogos JavaScript](#javascript-dialogs)
    - [Interagindo com Iframes Inline](#interacting-with-iframes)
    - [Escopo de Seletores](#scoping-selectors)
    - [Aguardando Elementos](#waiting-for-elements)
    - [Rolando um Elemento para a Visualização](#scrolling-an-element-into-view)
- [Asserções Disponíveis](#available-assertions)
- [Páginas](#pages)
    - [Gerando Páginas](#generating-pages)
    - [Configurando Páginas](#configuring-pages)
    - [Navegando para Páginas](#navigating-to-pages)
    - [Seletores Abreviados](#shorthand-selectors)
    - [Métodos de Página](#page-methods)
- [Componentes](#components)
    - [Gerando Componentes](#generating-components)
    - [Usando Componentes](#using-components)
- [Integração Contínua](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a id="introduction"></a>
## Introdução

> **Warning:**
> O [Pest 4](https://pestphp.com/) agora inclui testes automatizados de navegador, que oferecem melhorias significativas de desempenho e usabilidade em comparação com o Laravel Dusk. Para novos projetos, recomendamos usar o Pest para testes de navegador.

[Laravel Dusk](https://github.com/laravel/dusk) fornece uma API expressiva e fácil de usar para automação e testes de navegador. Por padrão, o Dusk não exige que você instale JDK ou Selenium no seu computador local. Em vez disso, o Dusk utiliza uma instalação independente do [ChromeDriver](https://sites.google.com/chromium.org/driver). No entanto, você é livre para utilizar qualquer outro driver compatível com Selenium que desejar.

<a id="installation"></a>
## Instalação

Para começar, você deve instalar o [Google Chrome](https://www.google.com/chrome) e adicionar a dependência do Composer `laravel/dusk` ao seu projeto:

```shell
composer require laravel/dusk --dev
```

> **Warning:**
> Se você estiver registrando manualmente o service provider do Dusk, **nunca** deve registrá-lo no seu ambiente de produção, pois isso pode permitir que usuários arbitrários se autentiquem na sua aplicação.

Após instalar o pacote Dusk, execute o comando Artisan `dusk:install`. O comando `dusk:install` criará um diretório `tests/Browser`, um teste de exemplo do Dusk e instalará o binário do Chrome Driver para o seu sistema operacional:

```shell
php artisan dusk:install
```

Em seguida, defina a variável de ambiente `APP_URL` no arquivo `.env` da sua aplicação. Este valor deve corresponder à URL que você utiliza para acessar a aplicação em um navegador.

> **Note:**
> Se você estiver usando o [Laravel Sail](../sail/) para gerenciar seu ambiente de desenvolvimento local, consulte também a documentação do Sail sobre [configuração e execução dos testes do Dusk](../sail/#laravel-dusk).

<a id="managing-chromedriver-installations"></a>
### Gerenciando Instalações do ChromeDriver

Se você quiser instalar uma versão do ChromeDriver diferente da que é instalada pelo Laravel Dusk através do comando `dusk:install`, pode usar o comando `dusk:chrome-driver`:

```shell
# Install the latest version of ChromeDriver for your OS...
php artisan dusk:chrome-driver

# Install a given version of ChromeDriver for your OS...
php artisan dusk:chrome-driver 86

# Install a given version of ChromeDriver for all supported OSs...
php artisan dusk:chrome-driver --all

# Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS...
php artisan dusk:chrome-driver --detect
```

> **Warning:**
> O Dusk exige que os binários `chromedriver` sejam executáveis. Se você estiver tendo problemas para executar o Dusk, deve garantir que os binários são executáveis usando o seguinte comando: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a id="using-other-browsers"></a>
### Usando Outros Navegadores

Por padrão, o Dusk utiliza o Google Chrome e uma instalação independente do [ChromeDriver](https://sites.google.com/chromium.org/driver) para executar seus testes de navegador. No entanto, você pode iniciar seu próprio servidor Selenium e executar seus testes contra qualquer navegador que desejar.

Para começar, abra o arquivo `tests/DuskTestCase.php`, que é a classe base de teste do Dusk para a sua aplicação. Dentro deste arquivo, você pode remover a chamada ao método `startChromeDriver`. Isso impedirá que o Dusk inicie automaticamente o ChromeDriver:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

Em seguida, você pode modificar o método `driver` para se conectar à URL e à porta de sua escolha. Além disso, pode modificar as "capacidades desejadas" (desired capabilities) que devem ser passadas ao WebDriver:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a id="getting-started"></a>
## Primeiros Passos

<a id="generating-tests"></a>
### Gerando Testes

Para gerar um teste do Dusk, use o comando Artisan `dusk:make`. O teste gerado será colocado no diretório `tests/Browser`:

```shell
php artisan dusk:make LoginTest
```

<a id="resetting-the-database-after-each-test"></a>
### Resetando o Banco de Dados Após Cada Teste

A maioria dos testes que você escrever interagirá com páginas que recuperam dados do banco de dados da sua aplicação; no entanto, seus testes do Dusk nunca devem usar a trait `RefreshDatabase`. A trait `RefreshDatabase` utiliza transações de banco de dados, que não serão aplicáveis nem disponíveis entre requisições HTTP. Em vez disso, você tem duas opções: a trait `DatabaseMigrations` e a trait `DatabaseTruncation`.

<a id="reset-migrations"></a>
#### Usando Migrations do Banco de Dados

A trait `DatabaseMigrations` executará as migrations do seu banco de dados antes de cada teste. No entanto, derrubar e recriar as tabelas do banco de dados para cada teste costuma ser mais lento do que truncar as tabelas:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;

pest()->use(DatabaseMigrations::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    //
}
```

> **Warning:**
> Bancos de dados SQLite em memória podem não ser utilizados ao executar os testes do Dusk. Como o navegador é executado em seu próprio processo, ele não conseguirá acessar os bancos de dados em memória de outros processos.

<a id="reset-truncation"></a>
#### Usando Truncamento do Banco de Dados

A trait `DatabaseTruncation` executará a migração do seu banco de dados no primeiro teste para garantir que as tabelas foram criadas corretamente. No entanto, nos testes subsequentes, as tabelas do banco de dados serão simplesmente truncadas, proporcionando ganho de velocidade em relação a executar novamente todas as migrations do banco de dados:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;

pest()->use(DatabaseTruncation::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;

    //
}
```

Por padrão, esta trait trunca todas as tabelas, exceto a tabela `migrations`. Se você quiser personalizar as tabelas que devem ser truncadas, pode definir a propriedade `$tablesToTruncate` na sua classe de teste:

> **Note:**
> Se você estiver usando o Pest, deve definir propriedades ou métodos na classe base `DuskTestCase` ou em qualquer classe que o seu arquivo de teste estenda.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

Alternativamente, você pode definir a propriedade `$exceptTables` na sua classe de teste para especificar quais tabelas devem ser excluídas do truncamento:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

Para especificar as conexões de banco de dados cujas tabelas devem ser truncadas, você pode definir a propriedade `$connectionsToTruncate` na sua classe de teste:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

Se você quiser executar código antes ou depois do truncamento do banco de dados, pode definir os métodos `beforeTruncatingDatabase` ou `afterTruncatingDatabase` na sua classe de teste:

```php
/**
 * Perform any work that should take place before the database has started truncating.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Perform any work that should take place after the database has finished truncating.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a id="running-tests"></a>
### Executando Testes

Para executar seus testes de navegador, execute o comando Artisan `dusk`:

```shell
php artisan dusk
```

Se você teve falhas nos testes na última vez que executou o comando `dusk`, pode economizar tempo reexecutando primeiro os testes que falharam, usando o comando `dusk:fails`:

```shell
php artisan dusk:fails
```

O comando `dusk` aceita qualquer argumento normalmente aceito pelo executor de testes Pest / PHPUnit, como permitir executar apenas os testes de um determinado [grupo](https://docs.phpunit.de/en/10.5/annotations.html#group):

```shell
php artisan dusk --group=foo
```

> **Note:**
> Se você estiver usando o [Laravel Sail](../sail/) para gerenciar seu ambiente de desenvolvimento local, consulte a documentação do Sail sobre [configuração e execução dos testes do Dusk](../sail/#laravel-dusk).

<a id="manually-starting-chromedriver"></a>
#### Iniciando o ChromeDriver Manualmente

Por padrão, o Dusk tentará iniciar automaticamente o ChromeDriver. Se isso não funcionar no seu sistema específico, você pode iniciar o ChromeDriver manualmente antes de executar o comando `dusk`. Se optar por iniciar o ChromeDriver manualmente, deve comentar a seguinte linha do arquivo `tests/DuskTestCase.php`:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

Além disso, se você iniciar o ChromeDriver em uma porta diferente de 9515, deve modificar o método `driver` da mesma classe para refletir a porta correta:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a id="environment-handling"></a>
### Tratamento de Ambiente

Para forçar o Dusk a usar seu próprio arquivo de ambiente ao executar os testes, crie um arquivo `.env.dusk.{environment}` na raiz do seu projeto. Por exemplo, se você for iniciar o comando `dusk` a partir do seu ambiente `local`, deve criar um arquivo `.env.dusk.local`.

Ao executar os testes, o Dusk fará backup do seu arquivo `.env` e renomeará o ambiente do Dusk para `.env`. Quando os testes forem concluídos, seu arquivo `.env` será restaurado.

<a id="browser-basics"></a>
## Noções Básicas de Navegador

<a id="creating-browsers"></a>
### Criando Navegadores

Para começar, vamos escrever um teste que verifica se conseguimos fazer login na nossa aplicação. Após gerar um teste, podemos modificá-lo para navegar até a página de login, inserir algumas credenciais e clicar no botão "Login". Para criar uma instância de navegador, você pode chamar o método `browse` dentro do seu teste do Dusk:

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $user = User::factory()->create([
        'email' => 'taylor@laravel.com',
    ]);

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/login')
            ->type('email', $user->email)
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * A basic browser test example.
     */
    public function test_basic_example(): void
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/home');
        });
    }
}
```

Como você pode ver no exemplo acima, o método `browse` aceita uma closure. Uma instância de navegador será automaticamente passada para essa closure pelo Dusk e é o principal objeto usado para interagir com a sua aplicação e fazer asserções sobre ela.

<a id="creating-multiple-browsers"></a>
#### Criando Múltiplos Navegadores

Às vezes, você pode precisar de múltiplos navegadores para executar corretamente um teste. Por exemplo, múltiplos navegadores podem ser necessários para testar uma tela de chat que interage com websockets. Para criar múltiplos navegadores, basta adicionar mais argumentos de navegador à assinatura da closure passada ao método `browse`:

```php
$this->browse(function (Browser $first, Browser $second) {
    $first->loginAs(User::find(1))
        ->visit('/home')
        ->waitForText('Message');

    $second->loginAs(User::find(2))
        ->visit('/home')
        ->waitForText('Message')
        ->type('message', 'Hey Taylor')
        ->press('Send');

    $first->waitForText('Hey Taylor')
        ->assertSee('Jeffrey Way');
});
```

<a id="navigation"></a>
### Navegação

O método `visit` pode ser usado para navegar até uma determinada URI dentro da sua aplicação:

```php
$browser->visit('/login');
```

Você pode usar o método `visitRoute` para navegar até uma [rota nomeada](../routing/#named-routes):

```php
$browser->visitRoute($routeName, $parameters);
```

Você pode navegar "para trás" e "para frente" usando os métodos `back` e `forward`:

```php
$browser->back();

$browser->forward();
```

Você pode usar o método `refresh` para atualizar a página:

```php
$browser->refresh();
```

<a id="resizing-browser-windows"></a>
### Redimensionando Janelas do Navegador

Você pode usar o método `resize` para ajustar o tamanho da janela do navegador:

```php
$browser->resize(1920, 1080);
```

O método `maximize` pode ser usado para maximizar a janela do navegador:

```php
$browser->maximize();
```

O método `fitContent` redimensionará a janela do navegador para corresponder ao tamanho do seu conteúdo:

```php
$browser->fitContent();
```

Quando um teste falha, o Dusk redimensionará automaticamente o navegador para se ajustar ao conteúdo antes de tirar uma screenshot. Você pode desabilitar este recurso chamando o método `disableFitOnFailure` dentro do seu teste:

```php
$browser->disableFitOnFailure();
```

Você pode usar o método `move` para mover a janela do navegador para outra posição na sua tela:

```php
$browser->move($x = 100, $y = 100);
```

<a id="browser-macros"></a>
### Macros de Navegador

Se você quiser definir um método de navegador personalizado que possa ser reutilizado em vários dos seus testes, pode usar o método `macro` na classe `Browser`. Normalmente, você deve chamar este método a partir do método `boot` de um [service provider](../providers/):

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Browser::macro('scrollToElement', function (string $element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

A função `macro` aceita um nome como primeiro argumento e uma closure como segundo. A closure da macro será executada ao chamar a macro como um método em uma instância de `Browser`:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a id="authentication"></a>
### Autenticação

Frequentemente, você testará páginas que exigem autenticação. Você pode usar o método `loginAs` do Dusk para evitar interagir com a tela de login da sua aplicação em cada teste. O método `loginAs` aceita a chave primária associada ao seu model autenticável ou uma instância de model autenticável:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> **Warning:**
> Após usar o método `loginAs`, a sessão do usuário será mantida para todos os testes do arquivo.

<a id="cookies"></a>
### Cookies

Você pode usar o método `cookie` para obter ou definir o valor de um cookie criptografado. Por padrão, todos os cookies criados pelo Laravel são criptografados:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

Você pode usar o método `plainCookie` para obter ou definir o valor de um cookie não criptografado:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

Você pode usar o método `deleteCookie` para excluir o cookie informado:

```php
$browser->deleteCookie('name');
```

<a id="executing-javascript"></a>
### Executando JavaScript

Você pode usar o método `script` para executar instruções JavaScript arbitrárias dentro do navegador:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a id="taking-a-screenshot"></a>
### Capturando uma Screenshot

Você pode usar o método `screenshot` para capturar uma screenshot e armazená-la com o nome de arquivo informado. Todas as screenshots serão armazenadas no diretório `tests/Browser/screenshots`:

```php
$browser->screenshot('filename');
```

O método `responsiveScreenshots` pode ser usado para capturar uma série de screenshots em vários breakpoints:

```php
$browser->responsiveScreenshots('filename');
```

O método `screenshotElement` pode ser usado para capturar uma screenshot de um elemento específico da página:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a id="storing-console-output-to-disk"></a>
### Armazenando a Saída do Console em Disco

Você pode usar o método `storeConsoleLog` para gravar a saída do console do navegador atual em disco com o nome de arquivo informado. A saída do console será armazenada no diretório `tests/Browser/console`:

```php
$browser->storeConsoleLog('filename');
```

<a id="storing-page-source-to-disk"></a>
### Armazenando o Código-Fonte da Página em Disco

Você pode usar o método `storeSource` para gravar o código-fonte da página atual em disco com o nome de arquivo informado. O código-fonte da página será armazenado no diretório `tests/Browser/source`:

```php
$browser->storeSource('filename');
```

<a id="interacting-with-elements"></a>
## Interagindo com Elementos

<a id="dusk-selectors"></a>
### Seletores Dusk

Escolher bons seletores CSS para interagir com elementos é uma das partes mais difíceis de escrever testes do Dusk. Com o tempo, mudanças no frontend podem fazer com que seletores CSS como os seguintes quebrem seus testes:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Os seletores Dusk permitem que você se concentre em escrever testes eficazes em vez de lembrar seletores CSS. Para definir um seletor, adicione um atributo `dusk` ao seu elemento HTML. Então, ao interagir com um navegador Dusk, prefixe o seletor com `@` para manipular o elemento associado dentro do seu teste:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

Se desejar, você pode personalizar o atributo HTML que o seletor Dusk utiliza através do método `selectorHtmlAttribute`. Normalmente, este método deve ser chamado a partir do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a id="text-values-and-attributes"></a>
### Texto, Valores e Atributos

<a id="retrieving-setting-values"></a>
#### Obtendo e Definindo Valores

O Dusk fornece vários métodos para interagir com o valor atual, o texto exibido e os atributos dos elementos da página. Por exemplo, para obter o "valor" de um elemento que corresponde a um seletor CSS ou Dusk informado, use o método `value`:

```php
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

Você pode usar o método `inputValue` para obter o "valor" de um elemento de input que possui um determinado nome de campo:

```php
$value = $browser->inputValue('field');
```

