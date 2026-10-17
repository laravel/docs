---
title: "Estrutura de Diretórios"
---

- [Introdução](#introduction)
- [O Diretório Raiz](#the-root-directory)
    - [O Diretório `app`](#the-root-app-directory)
    - [O Diretório `bootstrap`](#the-bootstrap-directory)
    - [O Diretório `config`](#the-config-directory)
    - [O Diretório `database`](#the-database-directory)
    - [O Diretório `public`](#the-public-directory)
    - [O Diretório `resources`](#the-resources-directory)
    - [O Diretório `routes`](#the-routes-directory)
    - [O Diretório `storage`](#the-storage-directory)
    - [O Diretório `tests`](#the-tests-directory)
    - [O Diretório `vendor`](#the-vendor-directory)
- [O Diretório App](#the-app-directory)
    - [O Diretório `Broadcasting`](#the-broadcasting-directory)
    - [O Diretório `Console`](#the-console-directory)
    - [O Diretório `Events`](#the-events-directory)
    - [O Diretório `Exceptions`](#the-exceptions-directory)
    - [O Diretório `Http`](#the-http-directory)
    - [O Diretório `Jobs`](#the-jobs-directory)
    - [O Diretório `Listeners`](#the-listeners-directory)
    - [O Diretório `Mail`](#the-mail-directory)
    - [O Diretório `Models`](#the-models-directory)
    - [O Diretório `Notifications`](#the-notifications-directory)
    - [O Diretório `Policies`](#the-policies-directory)
    - [O Diretório `Providers`](#the-providers-directory)
    - [O Diretório `Rules`](#the-rules-directory)

<a id="introduction"></a>
## Introdução

A estrutura padrão de uma aplicação Laravel tem como objetivo oferecer um excelente ponto de partida tanto para aplicações grandes quanto para pequenas. Mas você é livre para organizar sua aplicação como preferir. O Laravel impõe quase nenhuma restrição sobre onde uma determinada classe está localizada — desde que o Composer consiga fazer o autoload da classe.

<a id="the-root-directory"></a>
## O Diretório Raiz

<a id="the-root-app-directory"></a>
### O Diretório App

O diretório `app` contém o código principal da sua aplicação. Exploraremos este diretório com mais detalhes em breve; no entanto, quase todas as classes da sua aplicação estarão neste diretório.

<a id="the-bootstrap-directory"></a>
### O Diretório Bootstrap

O diretório `bootstrap` contém o arquivo `app.php`, que faz o bootstrap do framework. Este diretório também abriga um diretório `cache`, que contém arquivos gerados pelo framework para otimização de desempenho, como os arquivos de cache de rotas e de serviços.

<a id="the-config-directory"></a>
### O Diretório Config

O diretório `config`, como o nome sugere, contém todos os arquivos de configuração da sua aplicação. É uma ótima ideia ler todos esses arquivos e se familiarizar com todas as opções disponíveis para você.

<a id="the-database-directory"></a>
### O Diretório Database

O diretório `database` contém suas migrations do banco de dados, model factories e seeds. Se desejar, você também pode usar este diretório para armazenar um banco de dados SQLite.

<a id="the-public-directory"></a>
### O Diretório Public

O diretório `public` contém o arquivo `index.php`, que é o ponto de entrada de todas as requisições que entram na sua aplicação e configura o autoloading. Este diretório também abriga seus assets, como imagens, JavaScript e CSS.

<a id="the-resources-directory"></a>
### O Diretório Resources

O diretório `resources` contém suas [views](../views/), bem como seus assets brutos e não compilados, como CSS ou JavaScript.

<a id="the-routes-directory"></a>
### O Diretório Routes

O diretório `routes` contém todas as definições de rotas da sua aplicação. Por padrão, dois arquivos de rotas são incluídos no Laravel: `web.php` e `console.php`.

O arquivo `web.php` contém rotas que o Laravel coloca no grupo de middleware `web`, que fornece estado de sessão, proteção CSRF e criptografia de cookies. Se a sua aplicação não oferece uma API RESTful stateless, então todas as suas rotas muito provavelmente serão definidas no arquivo `web.php`.

O arquivo `console.php` é onde você pode definir todos os seus comandos de console baseados em closure. Cada closure é vinculada a uma instância de comando, permitindo uma abordagem simples para interagir com os métodos de IO de cada comando. Embora este arquivo não defina rotas HTTP, ele define pontos de entrada (rotas) baseados em console para a sua aplicação. Você também pode [agendar](../scheduling/) tarefas no arquivo `console.php`.

Opcionalmente, você pode instalar arquivos de rotas adicionais para rotas de API (`api.php`) e canais de broadcasting (`channels.php`), por meio dos comandos Artisan `install:api` e `install:broadcasting`.

O arquivo `api.php` contém rotas que são destinadas a ser stateless, de modo que as requisições que entram na aplicação por meio dessas rotas devem ser autenticadas [via tokens](../sanctum/) e não terão acesso ao estado da sessão.

O arquivo `channels.php` é onde você pode registrar todos os canais de [broadcasting de eventos](../broadcasting/) suportados pela sua aplicação.

<a id="the-storage-directory"></a>
### O Diretório Storage

O diretório `storage` contém seus logs, templates Blade compilados, sessões baseadas em arquivo, caches de arquivo e outros arquivos gerados pelo framework. Este diretório é segregado nos diretórios `app`, `framework` e `logs`. O diretório `app` pode ser usado para armazenar quaisquer arquivos gerados pela sua aplicação. O diretório `framework` é usado para armazenar arquivos e caches gerados pelo framework. Por fim, o diretório `logs` contém os arquivos de log da sua aplicação.

O diretório `storage/app/public` pode ser usado para armazenar arquivos gerados por usuários, como avatares de perfil, que devem ser acessíveis publicamente. Você deve criar um link simbólico em `public/storage` que aponte para este diretório. Você pode criar o link usando o comando Artisan `php artisan storage:link`.

<a id="the-tests-directory"></a>
### O Diretório Tests

O diretório `tests` contém seus testes automatizados. Exemplos de testes unitários e testes de feature com [Pest](https://pestphp.com) ou [PHPUnit](https://phpunit.de/) são fornecidos prontos para uso. Cada classe de teste deve ter a palavra `Test` como sufixo. Você pode executar seus testes usando os comandos `/vendor/bin/pest` ou `/vendor/bin/phpunit`. Ou, se você quiser uma representação mais detalhada e bonita dos resultados dos seus testes, pode executar seus testes usando o comando Artisan `php artisan test`.

<a id="the-vendor-directory"></a>
### O Diretório Vendor

O diretório `vendor` contém suas dependências do [Composer](https://getcomposer.org).

<a id="the-app-directory"></a>
## O Diretório App

A maior parte da sua aplicação está no diretório `app`. Por padrão, este diretório está no namespace `App` e é carregado automaticamente pelo Composer usando o [padrão de autoloading PSR-4](https://www.php-fig.org/psr/psr-4/).

Por padrão, o diretório `app` contém os diretórios `Http`, `Models` e `Providers`. No entanto, com o tempo, diversos outros diretórios serão gerados dentro do diretório `app` à medida que você usar os comandos make do Artisan para gerar classes. Por exemplo, o diretório `app/Console` não existirá até que você execute o comando Artisan `make:command` para gerar uma classe de comando.

Os diretórios `Console` e `Http` são explicados em mais detalhes nas respectivas seções abaixo, mas pense nos diretórios `Console` e `Http` como fornecedores de uma API para o núcleo da sua aplicação. O protocolo HTTP e a CLI são ambos mecanismos para interagir com a sua aplicação, mas não contêm, de fato, a lógica da aplicação. Em outras palavras, são duas maneiras de emitir comandos para a sua aplicação. O diretório `Console` contém todos os seus comandos Artisan, enquanto o diretório `Http` contém seus controladores, middleware e requisições.

> **Nota:**
> Muitas das classes no diretório `app` podem ser geradas pelo Artisan por meio de comandos. Para ver os comandos disponíveis, execute o comando `php artisan list make` no seu terminal.

<a id="the-broadcasting-directory"></a>
### O Diretório Broadcasting

O diretório `Broadcasting` contém todas as classes de canal de broadcast da sua aplicação. Essas classes são geradas usando o comando `make:channel`. Este diretório não existe por padrão, mas será criado para você quando você criar o seu primeiro canal. Para saber mais sobre canais, confira a documentação sobre [broadcasting de eventos](../broadcasting/).

<a id="the-console-directory"></a>
### O Diretório Console

O diretório `Console` contém todos os comandos Artisan personalizados da sua aplicação. Esses comandos podem ser gerados usando o comando `make:command`.

<a id="the-events-directory"></a>
### O Diretório Events

Este diretório não existe por padrão, mas será criado para você pelos comandos Artisan `event:generate` e `make:event`. O diretório `Events` abriga as [classes de evento](../events/). Eventos podem ser usados para alertar outras partes da sua aplicação de que uma determinada ação ocorreu, proporcionando grande flexibilidade e desacoplamento.

<a id="the-exceptions-directory"></a>
### O Diretório Exceptions

O diretório `Exceptions` contém todas as exceções personalizadas da sua aplicação. Essas exceções podem ser geradas usando o comando `make:exception`.

<a id="the-http-directory"></a>
### O Diretório Http

O diretório `Http` contém seus controladores, middleware e form requests. Quase toda a lógica para tratar as requisições que entram na sua aplicação será colocada neste diretório.

<a id="the-jobs-directory"></a>
### O Diretório Jobs

Este diretório não existe por padrão, mas será criado para você se você executar o comando Artisan `make:job`. O diretório `Jobs` abriga os [jobs enfileiráveis](../queues/) da sua aplicação. Jobs podem ser enfileirados pela sua aplicação ou executados de forma síncrona dentro do ciclo de vida da requisição atual. Jobs que executam de forma síncrona durante a requisição atual são algumas vezes chamados de "commands", pois são uma implementação do [command pattern](https://en.wikipedia.org/wiki/Command_pattern).

<a id="the-listeners-directory"></a>
### O Diretório Listeners

Este diretório não existe por padrão, mas será criado para você se você executar os comandos Artisan `event:generate` ou `make:listener`. O diretório `Listeners` contém as classes que tratam seus [eventos](../events/). Os listeners de evento recebem uma instância de evento e executam lógica em resposta ao disparo do evento. Por exemplo, um evento `UserRegistered` pode ser tratado por um listener `SendWelcomeEmail`.

<a id="the-mail-directory"></a>
### O Diretório Mail

Este diretório não existe por padrão, mas será criado para você se você executar o comando Artisan `make:mail`. O diretório `Mail` contém todas as suas [classes que representam e-mails](../mail/) enviados pela sua aplicação. Os objetos de mail permitem que você encapsule toda a lógica de construção de um e-mail em uma única classe simples, que pode ser enviada usando o método `Mail::send`.

<a id="the-models-directory"></a>
### O Diretório Models

O diretório `Models` contém todas as suas [classes de modelo Eloquent](../eloquent/). O ORM Eloquent incluído no Laravel fornece uma implementação de ActiveRecord simples e elegante para trabalhar com o seu banco de dados. Cada tabela do banco de dados tem um "Model" correspondente, que é usado para interagir com aquela tabela. Modelos permitem que você consulte dados nas suas tabelas, bem como insira novos registros na tabela.

<a id="the-notifications-directory"></a>
### O Diretório Notifications

Este diretório não existe por padrão, mas será criado para você se você executar o comando Artisan `make:notification`. O diretório `Notifications` contém todas as [notificações](../notifications/) "transacionais" enviadas pela sua aplicação, como notificações simples sobre eventos que acontecem dentro da sua aplicação. O recurso de notificações do Laravel abstrai o envio de notificações por uma variedade de drivers, como e-mail, Slack, SMS ou armazenamento em um banco de dados.

<a id="the-policies-directory"></a>
### O Diretório Policies

Este diretório não existe por padrão, mas será criado para você se você executar o comando Artisan `make:policy`. O diretório `Policies` contém as [classes de policy de autorização](../authorization/) da sua aplicação. Policies são usadas para determinar se um usuário pode executar uma determinada ação em um recurso.

<a id="the-providers-directory"></a>
### O Diretório Providers

O diretório `Providers` contém todos os [service providers](../providers/) da sua aplicação. Os service providers fazem o bootstrap da sua aplicação vinculando serviços no service container, registrando eventos ou executando quaisquer outras tarefas para preparar a sua aplicação para requisições recebidas.

Em uma aplicação Laravel recém-criada, este diretório já conterá o `AppServiceProvider`. Você é livre para adicionar os seus próprios provedores a este diretório conforme necessário.

<a id="the-rules-directory"></a>
### O Diretório Rules

Este diretório não existe por padrão, mas será criado para você se você executar o comando Artisan `make:rule`. O diretório `Rules` contém os objetos de regra de validação personalizados da sua aplicação. Rules são usadas para encapsular lógica de validação complicada em um objeto simples. Para mais informações, confira a [documentação de validação](../validation/).
