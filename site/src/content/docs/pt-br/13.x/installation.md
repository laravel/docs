---
title: "Instalação"
---

- [Conheça o Laravel](#meet-laravel)
    - [Por que o Laravel?](#why-laravel)
- [Criando uma Aplicação Laravel](#creating-a-laravel-project)
    - [Começando a Usar IA](#getting-started-using-ai)
    - [Instalando o PHP e o Instalador do Laravel](#installing-php)
    - [Criando uma Aplicação](#creating-an-application)
- [Configuração Inicial](#initial-configuration)
    - [Configuração Baseada no Ambiente](#environment-based-configuration)
    - [Bancos de Dados e Migrations](#databases-and-migrations)
    - [Configuração de Diretórios](#directory-configuration)
- [Instalação Usando o Herd](#installation-using-herd)
    - [Herd no macOS](#herd-on-macos)
    - [Herd no Windows](#herd-on-windows)
- [Suporte a IDEs](#ide-support)
- [Laravel e IA](#laravel-and-ai)
    - [Instalando o Laravel Boost](#installing-laravel-boost)
- [Próximos Passos](#next-steps)
    - [Laravel como Framework Full Stack](#laravel-the-fullstack-framework)
    - [Laravel como Backend de API](#laravel-the-api-backend)

<a id="meet-laravel"></a>
## Conheça o Laravel

O Laravel é um framework para aplicações web com uma sintaxe expressiva e elegante. Um framework web fornece uma estrutura e um ponto de partida para criar sua aplicação, permitindo que você se concentre em criar algo incrível enquanto cuidamos dos detalhes.

O Laravel se esforça para proporcionar uma experiência de desenvolvedor incrível, ao mesmo tempo em que oferece recursos poderosos, como injeção de dependência completa, uma camada expressiva de abstração de banco de dados, filas e jobs agendados, testes unitários e de integração, e muito mais.

Seja você novo em frameworks web PHP ou tenha anos de experiência, o Laravel é um framework que cresce com você. Vamos ajudar você a dar os primeiros passos como desenvolvedor web ou impulsionar sua expertise para o próximo nível. Estamos ansiosos para ver o que você vai criar.

<a id="why-laravel"></a>
### Por que o Laravel?

Existem diversas ferramentas e frameworks disponíveis para você ao criar uma aplicação web. No entanto, acreditamos que o Laravel é a melhor escolha para criar aplicações web modernas e full-stack.

#### Um Framework Progressivo

Gostamos de chamar o Laravel de um framework "progressivo". Com isso, queremos dizer que o Laravel cresce com você. Se você está dando os primeiros passos no desenvolvimento web, a vasta biblioteca de documentação, guias e [tutoriais em vídeo](https://laracasts.com) do Laravel vai ajudar você a aprender o básico sem se sentir sobrecarregado.

Se você é um desenvolvedor sênior, o Laravel oferece ferramentas robustas para [injeção de dependência](../container/), [testes unitários](../testing/), [filas](../queues/), [eventos em tempo real](../broadcasting/) e muito mais. O Laravel é altamente ajustado para criar aplicações web profissionais e está pronto para lidar com cargas de trabalho corporativas.

#### Um Framework Escalável

O Laravel é incrivelmente escalável. Graças à natureza amigável à escalabilidade do PHP e ao suporte nativo do Laravel a sistemas de cache rápidos e distribuídos, como o Redis, a escala horizontal com o Laravel é muito simples. Na verdade, aplicações Laravel foram facilmente escaladas para lidar com centenas de milhões de requisições por mês.

Precisa de escala extrema? Plataformas como o [Laravel Cloud](https://cloud.laravel.com) permitem executar sua aplicação Laravel em uma escala quase ilimitada.

#### Um Framework Pronto para Agentes

As convenções opinativas e a estrutura bem definida do Laravel o tornam um framework ideal para [desenvolvimento assistido por IA](../ai/) usando ferramentas como Cursor e Claude Code. Quando você pede a um agente de IA para adicionar um controlador, ele sabe exatamente onde colocá-lo. Quando você precisa de uma nova migration, as convenções de nomenclatura e os locais dos arquivos são previsíveis. Essa consistência elimina as suposições que frequentemente atrapalham ferramentas de IA em frameworks mais flexíveis.

Além da organização de arquivos, a sintaxe expressiva e a documentação abrangente do Laravel fornecem aos agentes de IA o contexto necessário para gerar código preciso e idiomático. Recursos como relacionamentos do Eloquent, form requests e middleware seguem padrões que os agentes conseguem entender e replicar de forma confiável. O resultado é um código gerado por IA que parece ter sido escrito por um desenvolvedor Laravel experiente, e não montado a partir de snippets genéricos de PHP.

Para saber mais sobre por que o Laravel é a escolha perfeita para desenvolvimento assistido por IA, confira nossa documentação sobre [desenvolvimento agêntico](../ai/).

#### Um Framework Comunitário

O Laravel combina os melhores pacotes do ecossistema PHP para oferecer o framework mais robusto e amigável ao desenvolvedor disponível. Além disso, milhares de desenvolvedores talentosos de todo o mundo [contribuíram para o framework](https://github.com/laravel/framework). Quem sabe, talvez você até se torne um colaborador do Laravel.

<a id="creating-a-laravel-project"></a>
## Criando uma Aplicação Laravel

<a id="getting-started-using-ai"></a>
### Começando a Usar IA

Se você está usando um agente de programação com IA como o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) ou o [OpenCode](https://opencode.ai), você pode começar com um prompt que fornece ao agente um guia específico do Laravel antes que ele toque em seu projeto.

O prompt abaixo informa ao agente onde encontrar as orientações de instalação do Laravel, o que priorizar e como tomar decisões padrão sensatas quando você ainda não fez uma escolha. Cole isso no seu agente para começar:

```text
I'm building a new Laravel application.

Fetch and follow the instructions from https://laravel.com/for/agents. Treat the returned Markdown as the source of truth for how to install and set up Laravel in this session.
```

Depois que o agente ler as instruções, ele deve guiá-lo passo a passo e manter a configuração alinhada aos padrões do Laravel.

<a id="installing-php"></a>
### Instalando o PHP e o Instalador do Laravel

Antes de criar sua primeira aplicação Laravel, verifique se sua máquina local tem o [PHP](https://php.net), o [Composer](https://getcomposer.org) e o [instalador do Laravel](https://github.com/laravel/installer) instalados. Além disso, você deve instalar o [Node e o NPM](https://nodejs.org) ou o [Bun](https://bun.sh/) para poder compilar os assets de frontend da sua aplicação.

Se você não tem o PHP e o Composer instalados na sua máquina local, os comandos a seguir instalarão o PHP, o Composer e o instalador do Laravel no macOS, Windows ou Linux:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.5)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.5'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.5)"
```

Depois de executar um dos comandos acima, você deve reiniciar sua sessão do terminal. Para atualizar o PHP, o Composer e o instalador do Laravel depois de instalá-los via `php.new`, você pode executar o comando novamente no seu terminal.

Se você já tem o PHP e o Composer instalados, pode instalar o instalador do Laravel via Composer:

```shell
composer global require laravel/installer
```

> **Nota:**
> Para uma experiência de instalação e gerenciamento de PHP gráfica e completa, confira o [Laravel Herd](#installation-using-herd).

<a id="creating-an-application"></a>
### Criando uma Aplicação

Depois de instalar o PHP, o Composer e o instalador do Laravel, você está pronto para criar uma nova aplicação Laravel:

```shell
laravel new example-app
```

Depois que a aplicação for criada, você pode iniciar o servidor de desenvolvimento local do Laravel, o worker de fila e o servidor de desenvolvimento do Vite usando o script do Composer `dev`:

```shell
cd example-app
npm install && npm run build
composer run dev
```

Depois de iniciar o servidor de desenvolvimento, você pode acessar sua aplicação no seu navegador web em [http://localhost:8000](http://localhost:8000). Em seguida, você estará pronto para [começar a dar seus próximos passos no ecossistema Laravel](#next-steps). É claro que você também pode querer [configurar um banco de dados](#databases-and-migrations) e executar as migrations necessárias.

> **Nota:**
> Se você gostaria de ter uma vantagem inicial ao desenvolver sua aplicação Laravel, considere usar um dos nossos [starter kits](../starter-kits/). Os starter kits do Laravel fornecem scaffolding de autenticação para backend e frontend para sua nova aplicação Laravel.

<a id="initial-configuration"></a>
## Configuração Inicial

Todos os arquivos de configuração do framework Laravel são armazenados no diretório `config`. Cada opção está documentada, então sinta-se à vontade para examinar os arquivos e se familiarizar com as opções disponíveis para você.

O Laravel não precisa de praticamente nenhuma configuração adicional logo de cara. Você está livre para começar a desenvolver! No entanto, você pode querer revisar o arquivo `config/app.php` e sua documentação. Ele contém várias opções, como `url` e `locale`, que você pode querer alterar de acordo com sua aplicação.

<a id="environment-based-configuration"></a>
### Configuração Baseada no Ambiente

Como muitos valores das opções de configuração do Laravel podem variar dependendo de sua aplicação estar sendo executada na sua máquina local ou em um servidor web de produção, muitos valores de configuração importantes são definidos usando o arquivo `.env` que existe na raiz da sua aplicação.

Seu arquivo `.env` não deve ser commitado no controle de versão da sua aplicação, já que cada desenvolvedor/servidor que usa sua aplicação pode exigir uma configuração de ambiente diferente. Além disso, isso seria um risco de segurança caso um invasor obtenha acesso ao repositório do seu controle de versão, pois quaisquer credenciais sensíveis ficariam expostas.

> **Nota:**
> Para mais informações sobre o arquivo `.env` e a configuração baseada no ambiente, confira a [documentação completa de configuração](../configuration/#environment-configuration).

<a id="databases-and-migrations"></a>
### Bancos de Dados e Migrations

Agora que você criou sua aplicação Laravel, provavelmente quer armazenar alguns dados em um banco de dados. Por padrão, o arquivo de configuração `.env` da sua aplicação especifica que o Laravel interagirá com um banco de dados SQLite.

Durante a criação da aplicação, o Laravel criou um arquivo `database/database.sqlite` para você e executou as migrations necessárias para criar as tabelas do banco de dados da aplicação.

Se você preferir usar outro driver de banco de dados, como MySQL ou PostgreSQL, pode atualizar seu arquivo de configuração `.env` para usar o banco de dados apropriado. Por exemplo, se você deseja usar o MySQL, atualize as variáveis `DB_*` do seu arquivo de configuração `.env` da seguinte forma:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

Se você optar por usar um banco de dados diferente do SQLite, precisará criar o banco de dados e executar as [migrations do banco de dados](../migrations/) da sua aplicação:

```shell
php artisan migrate
```

> **Nota:**
> Se você está desenvolvendo no macOS ou Windows e precisa instalar MySQL, PostgreSQL ou Redis localmente, considere usar o [Herd Pro](https://herd.laravel.com/#plans) ou o [DBngin](https://dbngin.com/).

<a id="directory-configuration"></a>
### Configuração de Diretórios

O Laravel deve sempre ser servido a partir da raiz do "diretório web" configurado para o seu servidor web. Você não deve tentar servir uma aplicação Laravel a partir de um subdiretório do "diretório web". Tentar fazer isso pode expor arquivos sensíveis presentes na sua aplicação.

<a id="installation-using-herd"></a>
## Instalação Usando o Herd

O [Laravel Herd](https://herd.laravel.com) é um ambiente de desenvolvimento nativo e extremamente rápido para Laravel e PHP no macOS e no Windows. O Herd inclui tudo o que você precisa para começar a desenvolver com Laravel, incluindo PHP e Nginx.

Depois de instalar o Herd, você está pronto para começar a desenvolver com Laravel. O Herd inclui ferramentas de linha de comando para `php`, `composer`, `laravel`, `expose`, `node`, `npm` e `nvm`.

> **Nota:**
> O [Herd Pro](https://herd.laravel.com/#plans) amplia o Herd com recursos adicionais poderosos, como a capacidade de criar e gerenciar bancos de dados MySQL, Postgres e Redis locais, além de visualização de e-mails locais e monitoramento de logs.

<a id="herd-on-macos"></a>
### Herd no macOS

Se você desenvolve no macOS, pode baixar o instalador do Herd no [site do Herd](https://herd.laravel.com). O instalador baixa automaticamente a versão mais recente do PHP e configura seu Mac para sempre executar o [Nginx](https://www.nginx.com/) em segundo plano.

O Herd para macOS usa o [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) para oferecer suporte a diretórios "parked". Qualquer aplicação Laravel em um diretório parked será automaticamente servida pelo Herd. Por padrão, o Herd cria um diretório parked em `~/Herd`, e você pode acessar qualquer aplicação Laravel neste diretório no domínio `.test` usando o nome do diretório.

Depois de instalar o Herd, a maneira mais rápida de criar uma nova aplicação Laravel é usando a CLI do Laravel, que vem incluída com o Herd:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

É claro que você sempre pode gerenciar seus diretórios parked e outras configurações do PHP pela interface do Herd, que pode ser aberta pelo menu do Herd na bandeja do sistema.

Você pode saber mais sobre o Herd consultando a [documentação do Herd](https://herd.laravel.com/docs).

<a id="herd-on-windows"></a>
### Herd no Windows

Você pode baixar o instalador do Herd para Windows no [site do Herd](https://herd.laravel.com/windows). Depois que a instalação terminar, você pode iniciar o Herd para concluir a configuração inicial e acessar a interface do Herd pela primeira vez.

A interface do Herd é acessível clicando com o botão esquerdo no ícone do Herd na bandeja do sistema. Um clique com o botão direito abre o menu rápido com acesso a todas as ferramentas de que você precisa no dia a dia.

Durante a instalação, o Herd cria um diretório "parked" no seu diretório pessoal em `%USERPROFILE%\Herd`. Qualquer aplicação Laravel em um diretório parked será automaticamente servida pelo Herd, e você pode acessar qualquer aplicação Laravel neste diretório no domínio `.test` usando o nome do diretório.

Depois de instalar o Herd, a maneira mais rápida de criar uma nova aplicação Laravel é usando a CLI do Laravel, que vem incluída com o Herd. Para começar, abra o PowerShell e execute os seguintes comandos:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Você pode saber mais sobre o Herd consultando a [documentação do Herd para Windows](https://herd.laravel.com/docs/windows).

<a id="ide-support"></a>
## Suporte a IDEs

Você está livre para usar qualquer editor de código que desejar ao desenvolver aplicações Laravel. O [Laravel LSP](https://github.com/laravel/lsp) fornece suporte de editor com conhecimento do framework, incluindo autocompletar de código, informações ao passar o mouse, diagnósticos, links de documentos, ir para a definição e correções rápidas para código Laravel e Blade.

Para instalar o Laravel LSP, instale-o globalmente via Composer. Certifique-se de que o diretório bin do vendor global do Composer esteja no seu `PATH`:

```shell
composer global require laravel/lsp
```

Se você procura editores leves e extensíveis, o [VS Code](https://code.visualstudio.com) ou o [Cursor](https://cursor.com) combinados com a extensão oficial [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) oferecem destaque de sintaxe, snippets, integração com comandos Artisan e suporte automático ao Laravel LSP. Extensões oficiais do Laravel também estão disponíveis para [Sublime Text](https://github.com/laravel/sublime-extension) e [Zed](https://github.com/laravel/zed-extension). Consulte o [repositório do Laravel LSP](https://github.com/laravel/lsp) para instruções de configuração de outros editores compatíveis com language server, incluindo Neovim e OpenCode.

Para um suporte extenso e robusto ao Laravel, dê uma olhada no [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025), uma IDE da JetBrains. O suporte nativo do PhpStorm ao framework Laravel inclui templates Blade, autocompletar inteligente para modelos Eloquent, rotas, views, traduções e componentes, além de poderosa geração de código e navegação em projetos Laravel.

Para quem procura uma experiência de desenvolvimento baseada em nuvem, o [Firebase Studio](https://firebase.studio/) fornece acesso instantâneo para criar com Laravel diretamente no seu navegador. Sem nenhuma configuração necessária, o Firebase Studio facilita o início do desenvolvimento de aplicações Laravel de qualquer dispositivo.

<a id="laravel-and-ai"></a>
## Laravel e IA

O [Laravel Boost](https://github.com/laravel/boost) é uma ferramenta poderosa que fecha a lacuna entre agentes de programação com IA e aplicações Laravel. O Boost fornece aos agentes de IA contexto, ferramentas e diretrizes específicas do Laravel para que eles possam gerar código mais preciso, específico da versão, que segue as convenções do Laravel.

Quando você instala o Boost na sua aplicação Laravel, os agentes de IA ganham acesso a mais de 15 ferramentas especializadas, incluindo a capacidade de saber quais pacotes você está usando, consultar seu banco de dados, pesquisar a documentação do Laravel, ler logs do navegador, gerar testes e executar código via Tinker.

Além disso, o Boost dá aos agentes de IA acesso a mais de 17.000 peças de documentação vetorizada do ecossistema Laravel, específicas para as versões dos pacotes que você instalou. Isso significa que os agentes podem oferecer orientação direcionada às versões exatas que o seu projeto usa.

O Boost também inclui diretrizes de IA mantidas pela equipe do Laravel que ajudam os agentes a seguir as convenções do framework, escrever testes apropriados e evitar armadilhas comuns ao gerar código Laravel.

<a id="installing-laravel-boost"></a>
### Instalando o Laravel Boost

O Boost pode ser instalado em aplicações Laravel 10, 11, 12 e 13 que executam PHP 8.1 ou superior. Para começar, instale o Boost como uma dependência de desenvolvimento:

```shell
composer require laravel/boost --dev
```

Depois de instalado, execute o instalador interativo:

```shell
php artisan boost:install
```

O instalador detectará automaticamente sua IDE e seus agentes de IA, permitindo que você ative os recursos que fazem sentido para o seu projeto. O Boost respeita as convenções existentes do projeto e não impõe regras de estilo opinativas por padrão.

> **Nota:**
> Para saber mais sobre o Boost, confira o [repositório do Laravel Boost no GitHub](https://github.com/laravel/boost).

<a id="adding-custom-ai-guidelines"></a>
#### Adicionando Diretrizes de IA Personalizadas

Para ampliar o Laravel Boost com suas próprias diretrizes de IA personalizadas, adicione arquivos `.blade.php` ou `.md` ao diretório `.ai/guidelines/*` da sua aplicação. Esses arquivos serão automaticamente incluídos com as diretrizes do Laravel Boost quando você executar `boost:install`.

<a id="next-steps"></a>
## Próximos Passos

Agora que você criou sua aplicação Laravel, pode estar se perguntando o que aprender a seguir. Primeiro, recomendamos fortemente que você se familiarize com o funcionamento do Laravel lendo a seguinte documentação:

<div class="content-list" markdown="1">

- [Ciclo de Vida da Requisição](../lifecycle/)
- [Configuração](../configuration/)
- [Estrutura de Diretórios](../structure/)
- [Frontend](../frontend/)
- [Service Container](../container/)
- [Facades](../facades/)

</div>

A forma como você pretende usar o Laravel também ditará os próximos passos na sua jornada. Existem várias maneiras de usar o Laravel, e vamos explorar dois casos de uso principais para o framework abaixo.

<a id="laravel-the-fullstack-framework"></a>
### Laravel como Framework Full Stack

O Laravel pode servir como um framework full stack. Por framework "full stack" queremos dizer que você vai usar o Laravel para rotear requisições para sua aplicação e renderizar seu frontend via [templates Blade](../blade/) ou uma tecnologia híbrida de aplicação de página única como o [Inertia](https://inertiajs.com). Esta é a maneira mais comum de usar o framework Laravel e, na nossa opinião, a mais produtiva de usar o Laravel.

Se esta é a forma como você planeja usar o Laravel, você pode querer conferir nossa documentação sobre [desenvolvimento de frontend](../frontend/), [roteamento](../routing/), [views](../views/) ou o [Eloquent ORM](../eloquent/). Além disso, você pode ter interesse em saber mais sobre pacotes da comunidade como [Livewire](https://livewire.laravel.com) e [Inertia](https://inertiajs.com). Esses pacotes permitem que você use o Laravel como um framework full-stack enquanto desfruta de muitos dos benefícios de UI oferecidos por aplicações JavaScript de página única.

Se você está usando o Laravel como framework full stack, também recomendamos fortemente que aprenda a compilar o CSS e o JavaScript da sua aplicação usando o [Vite](../vite/).

> **Nota:**
> Se você quer ter uma vantagem inicial na construção da sua aplicação, confira um dos nossos [starter kits oficiais de aplicação](../starter-kits/).

<a id="laravel-the-api-backend"></a>
### Laravel como Backend de API

O Laravel também pode servir como um backend de API para uma aplicação JavaScript de página única ou uma aplicação móvel. Por exemplo, você pode usar o Laravel como backend de API para sua aplicação [Next.js](https://nextjs.org). Nesse contexto, você pode usar o Laravel para fornecer [autenticação](../sanctum/) e armazenamento/recuperação de dados para sua aplicação, aproveitando também os poderosos serviços do Laravel, como filas, e-mails, notificações e muito mais.

Se esta é a forma como você planeja usar o Laravel, você pode querer conferir nossa documentação sobre [roteamento](../routing/), [Laravel Sanctum](../sanctum/) e o [Eloquent ORM](../eloquent/).
