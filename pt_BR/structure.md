# Estrutura da Aplicação

- [Introdução](#introduction)
- [Diretório Root](#the-root-directory)
- [Diretório App](#the-app-directory)
- [Definindo o Namespace de sua Aplicação](#namespacing-your-application)

<a name="introduction"></a>
## Introdução

A estrutura padrão de uma aplicação Laravel se destina a fornecer um excelente ponto de partida tanto para as grandes como para as pequenas aplicações. Claro, sinta-se livre para organizar sua aplicação da forma como achar melhor. O Laravel não impõe quase que nenhuma restrição sobre onde as classes ficam localizadas - desde que o Composer possa carregar essas classes.

<a name="the-root-directory"></a>
## Diretório Root

O diretório root de uma nova instalação Laravel contém uma variedade de pastas:

O diretório `app`, como você deve esperar, contém o código "core" de sua aplicação. Nós vamos explorar com mais detalhes esta pasta em breve.

A pasta `bootstrap` contém alguns arquivos que inicializam o framework e configuram o autoloading, assim como a pasta `cache` que contém alguns arquivos gerados pelo framework para otimizar a performance na inicialização.

O diretório `config`, como o nome indica, contém todos os arquivos de configuração da sua aplicação.

A pasta `database` contém os arquivos de migration e seeds do seu banco de dados. Se desejar, você pode usar essa pasta também para guardar seu banco de dados SQLite.

O diretório `public` contém o front controller e os seus assets (imagens, JavaScript, CSS, etc.).

O diretório `resources` contém as suas views, raw assets (LESS, SASS, CoffeeScript), e arquivos de localização.

O diretório `storage` contém os templates compilados do Blade, arquivos de sessão, arquivos de cache, e outros arquivos gerados pelo framework. Esta pasta é dividida pelos diretórios `app`, `framework`, e `logs`. O diretório `app` pode ser usado para armazenar qualquer arquivo utilizado pelo seu aplicativo. O diretório `framework` é usado para armazenar os arquivos gerados pelo framework e caches. Finalmente, o diretório `logs` contém os arquivos de log da aplicação.

O diretório `tests` contém seus testes automatizados. Um exemplo [PHPUnit](https://phpunit.de/) é fornecido pronto para usar.

O diretório `vendor` contém as dependências do [Composer](https://getcomposer.org).

<a name="the-app-directory"></a>
## Diretório App

O "core" da sua aplicação fica no dirétório `app`. Por padrão, este diretório está sob o namespace `App` e é carregado pelo Composer usando o padrão [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/). **Você pode mudar este namespace usando o comando `app:name` do Artisan**.

O diretório `app` vem com uma variedade de diretórios adicionais, como `Console`, `Http`, e `Providers`. Pense nos diretórios `Console` e `Http` como provendo uma API dentro do "core" de sua aplicação. Os protocolos HTTP e CLI são, ambos, mecanismos que interagem com sua aplicação, mas não contém a lógica de aplicação. Em outras palavras, eles são simplesmente dois meios de enviarem comandos para sua aplicação. O diretório `Console` contém todos os seus comandos do Artisan, enquanto o diretório `Http` contém seus controllers, filters, e requests.

O diretório `Jobs`, é claro, guarda as [queueable jobs](/docs/{{version}}/queues) para sua aplicação. Jobs podem ser enfileirados pela aplicação, assim como podem rodar de forma sincronizada dentro do ciclo da request atual.

O diretório `Events`, como você deve esperar, guarda as [event classes](/docs/{{version}}/events). Events podem ser usados para alertar outras partes de sua aplicação que uma determinada ação ocorreu, provendo uma grande flexibilidade e dissociação.

O diretório `Listeners` contém as classes handler para seus events. Handlers recebem um evento e executam uma lógica em resposta ao evento disparado. Por exemplo, o evento `UserRegistered` pode disparar e ser tratado por um `SendWelcomeEmail` listener.

O diretório `Exceptions` contém as exceções de sua aplicação, e também um bom lugar para colocar qualquer exceção disparada pela aplicação.

> **Nota:** Muitas das classes dentro do diretório `app` podem ser geradas via comandos do Artisan. Para ver a lista de comandos disponíveis, rode o comando `php artisan list make` no seu terminal.

<a name="namespacing-your-application"></a>
## Definindo o Namespace de sua Aplicação

Conforme discutido acima, o namespace padrão para sua aplicação é `App`; entretanto, você pode mudar este namespace para que fique o mesmo nome da sua aplicação, o que pode ser facilmente feito através do comando `app:name` do Artisan. Por exemplo, se o nome de sua aplicação é "SocialNet", você pode executar o seguinte comando:

	php artisan app:name SocialNet

É claro, você está livre para usar simplesmente o namespace `App` padrão.
