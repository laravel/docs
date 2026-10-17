---
title: "Laravel Sail"
---

- [Introdução](#introduction)
- [Instalação e Configuração](#installation)
    - [Reconstruindo as Imagens do Sail](#rebuilding-sail-images)
    - [Configurando um Alias de Shell](#configuring-a-shell-alias)
- [Iniciando e Parando o Sail](#starting-and-stopping-sail)
- [Executando Comandos](#executing-sail-commands)
    - [Executando Comandos PHP](#executing-php-commands)
    - [Executando Comandos do Composer](#executing-composer-commands)
    - [Executando Comandos do Artisan](#executing-artisan-commands)
    - [Executando Comandos do Node / NPM](#executing-node-npm-commands)
- [Interagindo Com Bancos de Dados](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [Armazenamento de Arquivos](#file-storage)
- [Executando Testes](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Pré-visualizando E-mails](#previewing-emails)
- [CLI do Contêiner](#sail-container-cli)
- [Versões do PHP](#sail-php-versions)
    - [Extensões Adicionais do PHP](#sail-php-extensions)
- [Versões do Node](#sail-node-versions)
- [Compartilhando Seu Site](#sharing-your-site)
- [Depurando Com o Xdebug](#debugging-with-xdebug)
    - [Uso do Xdebug via CLI](#xdebug-cli-usage)
    - [Uso do Xdebug via Navegador](#xdebug-browser-usage)
- [Personalização](#sail-customization)

<a id="introduction"></a>
## Introdução

[Laravel Sail](https://github.com/laravel/sail) é uma interface de linha de comando leve para interagir com o ambiente de desenvolvimento Docker padrão do Laravel. O Sail oferece um ótimo ponto de partida para construir uma aplicação Laravel usando PHP, MySQL e Redis sem exigir experiência prévia com Docker.

Em sua essência, o Sail é o arquivo `compose.yaml` e o script `sail` que ficam armazenados na raiz do seu projeto. O script `sail` fornece uma CLI com métodos convenientes para interagir com os contêineres Docker definidos pelo arquivo `compose.yaml`.

O Laravel Sail é compatível com macOS, Linux e Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)).

<a id="installation"></a>
## Instalação e Configuração

Você pode instalar o Sail usando o gerenciador de pacotes Composer:

```shell
composer require laravel/sail --dev
```

Depois que o Sail estiver instalado, você pode executar o comando Artisan `sail:install`. Esse comando publicará o arquivo `compose.yaml` do Sail na raiz da sua aplicação e modificará o arquivo `.env` com as variáveis de ambiente necessárias para se conectar aos serviços Docker:

```shell
php artisan sail:install
```

Por fim, você pode iniciar o Sail. Para continuar aprendendo a usar o Sail, por favor continue lendo o restante desta documentação:

```shell
./vendor/bin/sail up
```

> **Warning:**
> Se você estiver usando o Docker Desktop para Linux, deve usar o contexto Docker `default` executando o seguinte comando: `docker context use default`. Além disso, se você encontrar erros de permissão de arquivo dentro dos contêineres, pode ser necessário definir a variável de ambiente `SUPERVISOR_PHP_USER` como `root`.

<a id="adding-additional-services"></a>
#### Adicionando Serviços Adicionais

Se você quiser adicionar um serviço adicional à sua instalação existente do Sail, pode executar o comando Artisan `sail:add`:

```shell
php artisan sail:add
```

<a id="using-devcontainers"></a>
#### Usando Devcontainers

Se você quiser desenvolver dentro de um [Devcontainer](https://code.visualstudio.com/docs/remote/containers), pode fornecer a opção `--devcontainer` ao comando `sail:install`. A opção `--devcontainer` instruirá o comando `sail:install` a publicar um arquivo `.devcontainer/devcontainer.json ` padrão na raiz da sua aplicação:

```shell
php artisan sail:install --devcontainer
```

<a id="rebuilding-sail-images"></a>
### Reconstruindo as Imagens do Sail

Às vezes você pode querer reconstruir completamente suas imagens do Sail para garantir que todos os pacotes e softwares da imagem estejam atualizados. Você pode fazer isso usando o comando `build`:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a id="configuring-a-shell-alias"></a>
### Configurando um Alias de Shell

Por padrão, os comandos do Sail são invocados usando o script `vendor/bin/sail` que está incluído em todas as novas aplicações Laravel:

```shell
./vendor/bin/sail up
```

No entanto, em vez de digitar repetidamente `vendor/bin/sail` para executar os comandos do Sail, você pode querer configurar um alias de shell que permita executar os comandos do Sail mais facilmente:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

Para garantir que isso esteja sempre disponível, você pode adicioná-lo ao arquivo de configuração do seu shell no seu diretório home, como `~/.zshrc` ou `~/.bashrc`, e então reiniciar seu shell.

Depois que o alias de shell estiver configurado, você pode executar os comandos do Sail simplesmente digitando `sail`. O restante dos exemplos desta documentação assumirá que você configurou esse alias:

```shell
sail up
```

<a id="starting-and-stopping-sail"></a>
## Iniciando e Parando o Sail

O arquivo `compose.yaml` do Laravel Sail define uma variedade de contêineres Docker que trabalham juntos para ajudá-lo a construir aplicações Laravel. Cada um desses contêineres é uma entrada dentro da configuração `services` do seu arquivo `compose.yaml`. O contêiner `laravel.test` é o contêiner principal da aplicação que servirá sua aplicação.

Antes de iniciar o Sail, você deve garantir que nenhum outro servidor web ou banco de dados esteja em execução no seu computador local. Para iniciar todos os contêineres Docker definidos no arquivo `compose.yaml` da sua aplicação, você deve executar o comando `up`:

```shell
sail up
```

Para iniciar todos os contêineres Docker em segundo plano, você pode iniciar o Sail no modo "detached":

```shell
sail up -d
```

Depois que os contêineres da aplicação tiverem sido iniciados, você pode acessar o projeto no seu navegador web em: http://localhost.

Para parar todos os contêineres, você pode simplesmente pressionar Control + C para parar a execução do contêiner. Ou, se os contêineres estiverem em execução em segundo plano, você pode usar o comando `stop`:

```shell
sail stop
```

<a id="executing-sail-commands"></a>
## Executando Comandos

Ao usar o Laravel Sail, sua aplicação está sendo executada dentro de um contêiner Docker e está isolada do seu computador local. No entanto, o Sail fornece uma maneira conveniente de executar vários comandos na sua aplicação, como comandos PHP arbitrários, comandos do Artisan, comandos do Composer e comandos do Node / NPM.

**Ao ler a documentação do Laravel, você verá frequentemente referências a comandos do Composer, Artisan e Node / NPM que não mencionam o Sail.** Esses exemplos assumem que essas ferramentas estão instaladas no seu computador local. Se você estiver usando o Sail como seu ambiente de desenvolvimento local do Laravel, deve executar esses comandos usando o Sail:

```shell
# Executando comandos Artisan localmente...
php artisan queue:work

# Executando comandos Artisan dentro do Laravel Sail...
sail artisan queue:work
```

<a id="executing-php-commands"></a>
### Executando Comandos PHP

Comandos PHP podem ser executados usando o comando `php`. Naturalmente, esses comandos serão executados usando a versão do PHP que está configurada para sua aplicação. Para saber mais sobre as versões do PHP disponíveis para o Laravel Sail, consulte a [documentação de versões do PHP](#sail-php-versions):

```shell
sail php --version

sail php script.php
```

<a id="executing-composer-commands"></a>
### Executando Comandos do Composer

Comandos do Composer podem ser executados usando o comando `composer`. O contêiner da aplicação do Laravel Sail inclui uma instalação do Composer:

```shell
sail composer require laravel/sanctum
```

<a id="executing-artisan-commands"></a>
### Executando Comandos do Artisan

Comandos Artisan do Laravel podem ser executados usando o comando `artisan`:

```shell
sail artisan queue:work
```

<a id="executing-node-npm-commands"></a>
### Executando Comandos do Node / NPM

Comandos do Node podem ser executados usando o comando `node`, enquanto comandos do NPM podem ser executados usando o comando `npm`:

```shell
sail node --version

sail npm run dev
```

Se preferir, você pode usar o Yarn em vez do NPM:

```shell
sail yarn
```

<a id="interacting-with-sail-databases"></a>
## Interagindo Com Bancos de Dados

<a id="mysql"></a>
### MySQL

Como você já deve ter notado, o arquivo `compose.yaml` da sua aplicação contém uma entrada para um contêiner MySQL. Esse contêiner usa um [volume Docker](https://docs.docker.com/storage/volumes/) para que os dados armazenados no seu banco de dados sejam persistidos mesmo ao parar e reiniciar seus contêineres.

Além disso, na primeira vez em que o contêiner MySQL for iniciado, ele criará dois bancos de dados para você. O primeiro banco de dados é nomeado usando o valor da sua variável de ambiente `DB_DATABASE` e é destinado ao seu desenvolvimento local. O segundo é um banco de dados de testes dedicado chamado `testing` e garantirá que seus testes não interfiram nos seus dados de desenvolvimento.

Depois de iniciar seus contêineres, você pode se conectar à instância MySQL dentro da sua aplicação definindo sua variável de ambiente `DB_HOST` dentro do arquivo `.env` da sua aplicação como `mysql`.

Para se conectar ao banco de dados MySQL da sua aplicação a partir da sua máquina local, você pode usar uma aplicação gráfica de gerenciamento de banco de dados, como o [TablePlus](https://tableplus.com). Por padrão, o banco de dados MySQL é acessível em `localhost` na porta 3306 e as credenciais de acesso correspondem aos valores das suas variáveis de ambiente `DB_USERNAME` e `DB_PASSWORD`. Ou você pode se conectar como o usuário `root`, que também utiliza o valor da sua variável de ambiente `DB_PASSWORD` como sua senha.

<a id="mongodb"></a>
### MongoDB

Se você escolheu instalar o serviço [MongoDB](https://www.mongodb.com/) ao instalar o Sail, o arquivo `compose.yaml` da sua aplicação contém uma entrada para um contêiner [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) que fornece o banco de dados de documentos MongoDB com recursos do Atlas, como [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). Esse contêiner usa um [volume Docker](https://docs.docker.com/storage/volumes/) para que os dados armazenados no seu banco de dados sejam persistidos mesmo ao parar e reiniciar seus contêineres.

Depois de iniciar seus contêineres, você pode se conectar à instância MongoDB dentro da sua aplicação definindo sua variável de ambiente `MONGODB_URI` dentro do arquivo `.env` da sua aplicação como `mongodb://mongodb:27017`. A autenticação está desativada por padrão, mas você pode definir as variáveis de ambiente `MONGODB_USERNAME` e `MONGODB_PASSWORD` para habilitar a autenticação antes de iniciar o contêiner `mongodb`. Em seguida, adicione as credenciais à string de conexão:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

Para uma integração perfeita do MongoDB com sua aplicação, você pode instalar o [pacote oficial mantido pelo MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/).

Para se conectar ao banco de dados MongoDB da sua aplicação a partir da sua máquina local, você pode usar uma interface gráfica como o [Compass](https://www.mongodb.com/products/tools/compass). Por padrão, o banco de dados MongoDB é acessível em `localhost` na porta `27017`.

<a id="redis"></a>
### Redis

O arquivo `compose.yaml` da sua aplicação também contém uma entrada para um contêiner [Redis](https://redis.io). Esse contêiner usa um [volume Docker](https://docs.docker.com/storage/volumes/) para que os dados armazenados na sua instância Redis sejam persistidos mesmo ao parar e reiniciar seus contêineres. Depois de iniciar seus contêineres, você pode se conectar à instância Redis dentro da sua aplicação definindo sua variável de ambiente `REDIS_HOST` dentro do arquivo `.env` da sua aplicação como `redis`.

Para se conectar ao banco de dados Redis da sua aplicação a partir da sua máquina local, você pode usar uma aplicação gráfica de gerenciamento de banco de dados, como o [TablePlus](https://tableplus.com). Por padrão, o banco de dados Redis é acessível em `localhost` na porta 6379.

<a id="valkey"></a>
### Valkey

Se você escolher instalar o serviço Valkey ao instalar o Sail, o arquivo `compose.yaml` da sua aplicação conterá uma entrada para o [Valkey](https://valkey.io/). Esse contêiner usa um [volume Docker](https://docs.docker.com/storage/volumes/) para que os dados armazenados na sua instância Valkey sejam persistidos mesmo ao parar e reiniciar seus contêineres. Você pode se conectar a esse contêiner na sua aplicação definindo sua variável de ambiente `REDIS_HOST` dentro do arquivo `.env` da sua aplicação como `valkey`.

Para se conectar ao banco de dados Valkey da sua aplicação a partir da sua máquina local, você pode usar uma aplicação gráfica de gerenciamento de banco de dados, como o [TablePlus](https://tableplus.com). Por padrão, o banco de dados Valkey é acessível em `localhost` na porta 6379.

<a id="meilisearch"></a>
### Meilisearch

Se você escolheu instalar o serviço [Meilisearch](https://www.meilisearch.com) ao instalar o Sail, o arquivo `compose.yaml` da sua aplicação conterá uma entrada para esse poderoso motor de busca que é integrado com o [Laravel Scout](/en/scout/). Depois de iniciar seus contêineres, você pode se conectar à instância Meilisearch dentro da sua aplicação definindo sua variável de ambiente `MEILISEARCH_HOST` como `http://meilisearch:7700`.

A partir da sua máquina local, você pode acessar o painel de administração baseado na web do Meilisearch navegando para `http://localhost:7700` no seu navegador web.

<a id="typesense"></a>
### Typesense

Se você escolheu instalar o serviço [Typesense](https://typesense.org) ao instalar o Sail, o arquivo `compose.yaml` da sua aplicação conterá uma entrada para esse motor de busca extremamente rápido e de código aberto que é nativamente integrado com o [Laravel Scout](/en/scout/#typesense). Depois de iniciar seus contêineres, você pode se conectar à instância Typesense dentro da sua aplicação definindo as seguintes variáveis de ambiente:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

A partir da sua máquina local, você pode acessar a API do Typesense via `http://localhost:8108`.

<a id="file-storage"></a>
## Armazenamento de Arquivos

Se você planeja usar o Amazon S3 para armazenar arquivos ao executar sua aplicação em seu ambiente de produção, pode querer instalar o serviço [RustFS](https://rustfs.com) ao instalar o Sail. O RustFS fornece uma API compatível com S3 que você pode usar para desenvolver localmente usando o driver de armazenamento de arquivos `s3` do Laravel sem criar buckets de armazenamento de "teste" no seu ambiente S3 de produção. Se você escolher instalar o RustFS ao instalar o Sail, uma seção de configuração do RustFS será adicionada ao arquivo `compose.yaml` da sua aplicação.

Por padrão, o arquivo de configuração `filesystems` da sua aplicação já contém uma configuração de disco para o disco `s3`. Além de usar esse disco para interagir com o Amazon S3, você pode usá-lo para interagir com qualquer serviço de armazenamento de arquivos compatível com S3, como o RustFS, simplesmente modificando as variáveis de ambiente associadas que controlam sua configuração. Por exemplo, ao usar o RustFS, a configuração das variáveis de ambiente do seu sistema de arquivos deve ser definida da seguinte forma:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a id="running-tests"></a>
## Executando Testes

O Laravel fornece um suporte incrível a testes imediatamente, e você pode usar o comando `test` do Sail para executar os [testes de funcionalidade e unitários](/en/testing/) das suas aplicações. Quaisquer opções de CLI aceitas pelo Pest / PHPUnit também podem ser passadas ao comando `test`:

```shell
sail test

sail test --group orders
```

O comando `test` do Sail é equivalente a executar o comando Artisan `test`:

```shell
sail artisan test
```

Por padrão, o Sail criará um banco de dados `testing` dedicado para que seus testes não interfiram no estado atual do seu banco de dados. Em uma instalação padrão do Laravel, o Sail também configurará seu arquivo `phpunit.xml` para usar esse banco de dados ao executar seus testes:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a id="laravel-dusk"></a>
### Laravel Dusk

O [Laravel Dusk](/en/dusk/) fornece uma API expressiva e fácil de usar para automação e testes de navegador. Graças ao Sail, você pode executar esses testes sem nunca instalar o Selenium ou outras ferramentas no seu computador local. Para começar, descomente o serviço Selenium no arquivo `compose.yaml` da sua aplicação:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

Em seguida, garanta que o serviço `laravel.test` no arquivo `compose.yaml` da sua aplicação tenha uma entrada `depends_on` para `selenium`:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

Por fim, você pode executar sua suíte de testes do Dusk iniciando o Sail e executando o comando `dusk`:

```shell
sail dusk
```

<a id="selenium-on-apple-silicon"></a>
#### Selenium no Apple Silicon

Se sua máquina local contém um chip Apple Silicon, seu serviço `selenium` deve usar a imagem `selenium/standalone-chromium`:

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a id="previewing-emails"></a>
## Pré-visualizando E-mails

O arquivo `compose.yaml` padrão do Laravel Sail contém uma entrada de serviço para o [Mailpit](https://github.com/axllent/mailpit). O Mailpit intercepta os e-mails enviados pela sua aplicação durante o desenvolvimento local e fornece uma interface web conveniente para que você possa pré-visualizar suas mensagens de e-mail no seu navegador. Ao usar o Sail, o host padrão do Mailpit é `mailpit` e está disponível na porta 1025:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Quando o Sail estiver em execução, você pode acessar a interface web do Mailpit em: http://localhost:8025

Se você escolheu instalar o serviço [Mailtrap Local](https://github.com/mailtrap/mailtrap-local) ao instalar o Sail, ou o adicionou posteriormente usando o comando Artisan `sail:add`, o arquivo `compose.yaml` da sua aplicação conterá uma entrada para esse capturador de e-mails em vez disso. O host padrão do Mailtrap Local é `mailtrap-local` e está disponível na porta 3535:

```ini
MAIL_HOST=mailtrap-local
MAIL_PORT=3535
```

Quando o Sail estiver em execução, você pode acessar a interface web do Mailtrap Local em: http://localhost:3550

<a id="sail-container-cli"></a>
## CLI do Contêiner

Às vezes você pode querer iniciar uma sessão Bash dentro do contêiner da sua aplicação. Você pode usar o comando `shell` para se conectar ao contêiner da sua aplicação, permitindo inspecionar seus arquivos e serviços instalados, bem como executar comandos de shell arbitrários dentro do contêiner:

```shell
sail shell

sail root-shell
```

Para iniciar uma nova sessão do [Laravel Tinker](https://github.com/laravel/tinker), você pode executar o comando `tinker`:

```shell
sail tinker
```

<a id="sail-php-versions"></a>
## Versões do PHP

Atualmente o Sail suporta servir sua aplicação via PHP 8.5, 8.4, 8.3, 8.2, 8.1 ou PHP 8.0. A versão padrão do PHP usada pelo Sail atualmente é o PHP 8.5. Para alterar a versão do PHP usada para servir sua aplicação, você deve atualizar a definição `build` do contêiner `laravel.test` no arquivo `compose.yaml` da sua aplicação:

```yaml
# PHP 8.5
context: ./vendor/laravel/sail/runtimes/8.5

# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

Além disso, você pode querer atualizar o nome da sua `image` para refletir a versão do PHP que está sendo usada pela sua aplicação. Essa opção também é definida no arquivo `compose.yaml` da sua aplicação:

```yaml
image: sail-8.2/app
```

Depois de atualizar o arquivo `compose.yaml` da sua aplicação, você deve reconstruir suas imagens de contêiner:

```shell
sail build --no-cache

sail up
```

<a id="sail-php-extensions"></a>
### Extensões Adicionais do PHP

As imagens de runtime do Sail incluem um conjunto comum de extensões PHP. Se sua aplicação exigir extensões adicionais, você pode instalá-las ao construir a imagem adicionando um argumento de build `PHP_EXTENSIONS` separado por espaços ao serviço `laravel.test` no arquivo `compose.yaml` da sua aplicação:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        PHP_EXTENSIONS: 'gmp imagick'
```

Depois de atualizar o arquivo `compose.yaml` da sua aplicação, você deve reconstruir suas imagens de contêiner.

<a id="sail-node-versions"></a>
## Versões do Node

O Sail instala o Node 24 por padrão. Para alterar a versão do Node que é instalada ao construir suas imagens, você pode atualizar a definição `build.args` do serviço `laravel.test` no arquivo `compose.yaml` da sua aplicação:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

Depois de atualizar o arquivo `compose.yaml` da sua aplicação, você deve reconstruir suas imagens de contêiner:

```shell
sail build --no-cache

sail up
```

<a id="sharing-your-site"></a>
## Compartilhando Seu Site

Às vezes você pode precisar compartilhar seu site publicamente para pré-visualizá-lo para um colega ou para testar integrações de webhook com sua aplicação. Para compartilhar seu site, você pode usar o comando `share`. Depois de executar esse comando, você receberá uma URL aleatória `laravel-sail.site` que pode usar para acessar sua aplicação:

```shell
sail share
```

Ao compartilhar seu site via o comando `share`, você deve configurar os proxies confiáveis da sua aplicação usando o método de middleware `trustProxies` no arquivo `bootstrap/app.php` da sua aplicação. Caso contrário, os helpers de geração de URL, como `url` e `route`, não conseguirão determinar o host HTTP correto que deve ser usado durante a geração de URL:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

Se você quiser escolher o subdomínio para seu site compartilhado, pode fornecer a opção `subdomain` ao executar o comando `share`:

```shell
sail share --subdomain=my-sail-site
```

> **Note:**
> O comando `share` é alimentado pelo [Expose](https://github.com/beyondcode/expose), um serviço de túnel de código aberto da [BeyondCode](https://beyondco.de).

<a id="debugging-with-xdebug"></a>
## Depurando Com o Xdebug

A configuração Docker do Laravel Sail inclui suporte para o [Xdebug](https://xdebug.org/), um depurador popular e poderoso para PHP. Para habilitar o Xdebug, garanta que você tenha [publicado sua configuração do Sail](#sail-customization). Em seguida, adicione as seguintes variáveis ao arquivo `.env` da sua aplicação para configurar o Xdebug:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

Em seguida, garanta que seu arquivo `php.ini` publicado inclua a seguinte configuração para que o Xdebug seja ativado nos modos especificados:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

Depois de modificar o arquivo `php.ini`, lembre-se de reconstruir suas imagens Docker para que suas alterações no arquivo `php.ini` tenham efeito:

```shell
sail build --no-cache
```

#### Configuração do IP do Host Linux

Internamente, a variável de ambiente `XDEBUG_CONFIG` é definida como `client_host=host.docker.internal` para que o Xdebug seja configurado corretamente para Mac e Windows (WSL2). Se sua máquina local estiver executando Linux e você estiver usando o Docker 20.10+, `host.docker.internal` está disponível e nenhuma configuração manual é necessária.

Para versões do Docker anteriores à 20.10, `host.docker.internal` não é suportado no Linux, e você precisará definir manualmente o IP do host. Para fazer isso, configure um IP estático para seu contêiner definindo uma rede personalizada no seu arquivo `compose.yaml`:

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

Depois de definir o IP estático, defina a variável SAIL_XDEBUG_CONFIG dentro do arquivo .env da sua aplicação:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a id="xdebug-cli-usage"></a>
### Uso do Xdebug via CLI

Um comando `sail debug` pode ser usado para iniciar uma sessão de depuração ao executar um comando Artisan:

```shell
# Execute um comando Artisan sem o Xdebug...
sail artisan migrate

# Execute um comando Artisan com o Xdebug...
sail debug migrate
```

<a id="xdebug-browser-usage"></a>
### Uso do Xdebug via Navegador

Para depurar sua aplicação enquanto interage com ela via um navegador web, siga as [instruções fornecidas pelo Xdebug](https://xdebug.org/docs/step_debug#web-application) para iniciar uma sessão do Xdebug a partir do navegador web.

Se você estiver usando o PhpStorm, revise a documentação da JetBrains sobre [depuração sem configuração](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html).

> **Warning:**
> O Laravel Sail depende do `artisan serve` para servir sua aplicação. O comando `artisan serve` aceita apenas as variáveis `XDEBUG_CONFIG` e `XDEBUG_MODE` a partir da versão 8.53.0 do Laravel. Versões mais antigas do Laravel (8.52.0 e inferiores) não suportam essas variáveis e não aceitarão conexões de depuração.

<a id="sail-customization"></a>
## Personalização

Como o Sail é apenas Docker, você é livre para personalizar quase tudo nele. Para publicar os próprios Dockerfiles do Sail, você pode executar o comando `sail:publish`:

```shell
sail artisan sail:publish
```

Depois de executar esse comando, os Dockerfiles e outros arquivos de configuração usados pelo Laravel Sail serão colocados dentro de um diretório `docker` no diretório raiz da sua aplicação. Depois de personalizar sua instalação do Sail, você pode querer alterar o nome da imagem para o contêiner da aplicação no arquivo `compose.yaml` da sua aplicação. Depois de fazer isso, reconstrua os contêineres da sua aplicação usando o comando `build`. Atribuir um nome único à imagem da aplicação é particularmente importante se você estiver usando o Sail para desenvolver múltiplas aplicações Laravel em uma única máquina:

```shell
sail build --no-cache
```