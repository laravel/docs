---
title: "Laravel Valet"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Atualizando o Valet](#upgrading-valet)
- [Servindo Sites](#serving-sites)
    - [O Comando "Park"](#the-park-command)
    - [O Comando "Link"](#the-link-command)
    - [Protegendo Sites Com TLS](#securing-sites)
    - [Servindo um Site Padrão](#serving-a-default-site)
    - [Versões de PHP por Site](#per-site-php-versions)
- [Compartilhando Sites](#sharing-sites)
    - [Compartilhando Sites na Sua Rede Local](#sharing-sites-on-your-local-network)
- [Variáveis de Ambiente Específicas por Site](#site-specific-environment-variables)
- [Fazendo Proxy de Serviços](#proxying-services)
- [Drivers Personalizados do Valet](#custom-valet-drivers)
    - [Drivers Locais](#local-drivers)
- [Outros Comandos do Valet](#other-valet-commands)
- [Diretórios e Arquivos do Valet](#valet-directories-and-files)
    - [Acesso ao Disco](#disk-access)

<a id="introduction"></a>
## Introdução

> **Note:**
> Procurando uma maneira ainda mais fácil de desenvolver aplicações Laravel no macOS ou no Windows? Confira o [Laravel Herd](https://herd.laravel.com). O Herd inclui tudo o que você precisa para começar a desenvolver com Laravel, incluindo Valet, PHP e Composer.

[Laravel Valet](https://github.com/laravel/valet) é um ambiente de desenvolvimento para minimalistas do macOS. O Laravel Valet configura seu Mac para sempre executar o [Nginx](https://www.nginx.com/) em segundo plano quando a máquina é iniciada. Em seguida, usando o [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), o Valet faz proxy de todas as requisições no domínio `*.test` para apontar para sites instalados na sua máquina local.

Em outras palavras, o Valet é um ambiente de desenvolvimento Laravel extremamente rápido que usa cerca de 7 MB de RAM. O Valet não é um substituto completo para o [Sail](/en/sail/) ou o [Homestead](/en/homestead/), mas oferece uma ótima alternativa se você quer uma base flexível, prefere velocidade extrema ou está trabalhando em uma máquina com uma quantidade limitada de RAM.

De forma nativa, o suporte do Valet inclui, mas não se limita a:

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- HTML Estático
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

No entanto, você pode estender o Valet com seus próprios [drivers personalizados](#custom-valet-drivers).

<a id="installation"></a>
## Instalação

> **Warning:**
> O Valet requer macOS e [Homebrew](https://brew.sh/). Antes da instalação, você deve certificar-se de que nenhum outro programa, como Apache ou Nginx, esteja ocupando a porta 80 da sua máquina local.

Para começar, você primeiro precisa garantir que o Homebrew esteja atualizado usando o comando `update`:

```shell
brew update
```

Em seguida, você deve usar o Homebrew para instalar o PHP:

```shell
brew install php
```

Após instalar o PHP, você está pronto para instalar o [gerenciador de pacotes Composer](https://getcomposer.org). Além disso, você deve certificar-se de que o diretório `$HOME/.composer/vendor/bin` esteja no "PATH" do seu sistema. Depois que o Composer for instalado, você pode instalar o Laravel Valet como um pacote global do Composer:

```shell
composer global require laravel/valet
```

Por fim, você pode executar o comando `install` do Valet. Isso vai configurar e instalar o Valet e o DnsMasq. Além disso, os daemons dos quais o Valet depende serão configurados para iniciar quando o seu sistema iniciar:

```shell
valet install
```

Uma vez que o Valet esteja instalado, tente dar um ping em qualquer domínio `*.test` no seu terminal usando um comando como `ping foobar.test`. Se o Valet estiver instalado corretamente, você deve ver esse domínio respondendo em `127.0.0.1`.

O Valet iniciará automaticamente seus serviços necessários sempre que sua máquina for inicializada.

<a id="php-versions"></a>
#### Versões do PHP

> **Note:**
> Em vez de modificar sua versão global do PHP, você pode instruir o Valet a usar versões de PHP por site por meio do [comando](#per-site-php-versions) `isolate`.

O Valet permite que você alterne versões do PHP usando o comando `valet use php@version`. O Valet instalará a versão de PHP especificada via Homebrew se ela ainda não estiver instalada:

```shell
valet use php@8.2

valet use php
```

Você também pode criar um arquivo `.valetrc` na raiz do seu projeto. O arquivo `.valetrc` deve conter a versão de PHP que o site deve usar:

```shell
php=php@8.2
```

Uma vez que esse arquivo tenha sido criado, você pode simplesmente executar o comando `valet use` e o comando determinará a versão de PHP preferida do site lendo o arquivo.

> **Warning:**
> O Valet serve apenas uma versão de PHP por vez, mesmo que você tenha várias versões de PHP instaladas.

<a id="database"></a>
#### Banco de Dados

Se sua aplicação precisar de um banco de dados, confira o [DBngin](https://dbngin.com), que fornece uma ferramenta de gerenciamento de banco de dados gratuita e completa que inclui MySQL, PostgreSQL e Redis. Depois que o DBngin for instalado, você pode se conectar ao seu banco de dados em `127.0.0.1` usando o nome de usuário `root` e uma string vazia como senha.

<a id="resetting-your-installation"></a>
#### Redefinindo Sua Instalação

Se você estiver tendo problemas para fazer sua instalação do Valet funcionar corretamente, executar o comando `composer global require laravel/valet` seguido de `valet install` redefinirá sua instalação e pode resolver uma variedade de problemas. Em casos raros, pode ser necessário fazer um "hard reset" do Valet executando `valet uninstall --force` seguido de `valet install`.

<a id="upgrading-valet"></a>
### Atualizando o Valet

Você pode atualizar sua instalação do Valet executando o comando `composer global require laravel/valet` no seu terminal. Após a atualização, é uma boa prática executar o comando `valet install` para que o Valet possa fazer atualizações adicionais em seus arquivos de configuração, se necessário.

<a id="upgrading-to-valet-4"></a>
#### Atualizando para o Valet 4

Se você estiver atualizando do Valet 3 para o Valet 4, siga os passos a seguir para atualizar corretamente sua instalação do Valet:

<div class="content-list" markdown="1">

- Se você adicionou arquivos `.valetphprc` para personalizar a versão de PHP do seu site, renomeie cada arquivo `.valetphprc` para `.valetrc`. Em seguida, acrescente `php=` no início do conteúdo existente do arquivo `.valetrc`.
- Atualize quaisquer drivers personalizados para corresponder ao namespace, extensão, type-hints e return type-hints do novo sistema de drivers. Você pode consultar o [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) do Valet como exemplo.
- Se você usa PHP 7.1 - 7.4 para servir seus sites, certifique-se de ainda usar o Homebrew para instalar uma versão do PHP 8.0 ou superior, pois o Valet usará essa versão, mesmo que não seja sua versão principal vinculada, para executar alguns de seus scripts.

</div>

<a id="serving-sites"></a>
## Servindo Sites

Uma vez que o Valet esteja instalado, você está pronto para começar a servir suas aplicações Laravel. O Valet fornece dois comandos para ajudá-lo a servir suas aplicações: `park` e `link`.

<a id="the-park-command"></a>
### O Comando `park`

O comando `park` registra um diretório na sua máquina que contém suas aplicações. Uma vez que o diretório tenha sido "parkeado" com o Valet, todos os diretórios dentro desse diretório ficarão acessíveis no seu navegador web em `http://<directory-name>.test`:

```shell
cd ~/Sites

valet park
```

É só isso. Agora, qualquer aplicação que você criar dentro do seu diretório "parkeado" será automaticamente servida usando a convenção `http://<directory-name>.test`. Então, se o seu diretório parkeado contém um diretório chamado "laravel", a aplicação dentro desse diretório ficará acessível em `http://laravel.test`. Além disso, o Valet permite automaticamente que você acesse o site usando subdomínios curinga (`http://foo.laravel.test`).

<a id="the-link-command"></a>
### O Comando `link`

O comando `link` também pode ser usado para servir suas aplicações Laravel. Este comando é útil se você quiser servir um único site em um diretório e não o diretório inteiro:

```shell
cd ~/Sites/laravel

valet link
```

Uma vez que uma aplicação tenha sido vinculada ao Valet usando o comando `link`, você pode acessar a aplicação usando o nome do seu diretório. Então, o site que foi vinculado no exemplo acima pode ser acessado em `http://laravel.test`. Além disso, o Valet permite automaticamente que você acesse o site usando subdomínios curinga (`http://foo.laravel.test`).

Se você quiser servir a aplicação em um hostname diferente, você pode passar o hostname para o comando `link`. Por exemplo, você pode executar o seguinte comando para disponibilizar uma aplicação em `http://application.test`:

```shell
cd ~/Sites/laravel

valet link application
```

Claro, você também pode servir aplicações em subdomínios usando o comando `link`:

```shell
valet link api.application
```

Você pode executar o comando `links` para exibir uma lista de todos os seus diretórios vinculados:

```shell
valet links
```

O comando `unlink` pode ser usado para destruir o link simbólico de um site:

```shell
cd ~/Sites/laravel

valet unlink
```

<a id="securing-sites"></a>
### Protegendo Sites Com TLS

Por padrão, o Valet serve sites via HTTP. No entanto, se você quiser servir um site via TLS criptografado usando HTTP/2, pode usar o comando `secure`. Por exemplo, se o seu site está sendo servido pelo Valet no domínio `laravel.test`, você deve executar o seguinte comando para protegê-lo:

```shell
valet secure laravel
```

Para "desproteger" um site e reverter para servir seu tráfego via HTTP simples, use o comando `unsecure`. Assim como o comando `secure`, este comando aceita o hostname que você deseja desproteger:

```shell
valet unsecure laravel
```

<a id="serving-a-default-site"></a>
### Servindo um Site Padrão

Às vezes, você pode querer configurar o Valet para servir um site "padrão" em vez de um `404` ao visitar um domínio `test` desconhecido. Para fazer isso, você pode adicionar uma opção `default` ao seu arquivo de configuração `~/.config/valet/config.json` contendo o caminho para o site que deve servir como seu site padrão:

    "default": "/Users/Sally/Sites/example-site",

<a id="per-site-php-versions"></a>
### Versões de PHP por Site

Por padrão, o Valet usa sua instalação global do PHP para servir seus sites. No entanto, se você precisar oferecer suporte a várias versões de PHP em diversos sites, pode usar o comando `isolate` para especificar qual versão de PHP um determinado site deve usar. O comando `isolate` configura o Valet para usar a versão de PHP especificada no site localizado no seu diretório de trabalho atual:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

Se o nome do seu site não corresponder ao nome do diretório que o contém, você pode especificar o nome do site usando a opção `--site`:

```shell
valet isolate php@8.0 --site="site-name"
```

Por conveniência, você pode usar os comandos `valet php`, `composer` e `which-php` para fazer proxy de chamadas para a CLI ou ferramenta de PHP apropriada com base na versão de PHP configurada do site:

```shell
valet php
valet composer
valet which-php
```

Você pode executar o comando `isolated` para exibir uma lista de todos os seus sites isolados e suas versões de PHP:

```shell
valet isolated
```

Para reverter um site de volta para a versão de PHP instalada globalmente do Valet, você pode invocar o comando `unisolate` a partir do diretório raiz do site:

```shell
valet unisolate
```

<a id="sharing-sites"></a>
## Compartilhando Sites

O Valet inclui um comando para compartilhar seus sites locais com o mundo, fornecendo uma maneira fácil de testar seu site em dispositivos móveis ou compartilhá-lo com membros da equipe e clientes.

De forma nativa, o Valet oferece suporte ao compartilhamento dos seus sites via ngrok ou Expose. Antes de compartilhar um site, você deve atualizar sua configuração do Valet usando o comando `share-tool`, especificando `ngrok`, `expose` ou `cloudflared`:

```shell
valet share-tool ngrok
```

Se você escolher uma ferramenta e não a tiver instalada via Homebrew (para ngrok e cloudflared) ou Composer (para o Expose), o Valet solicitará automaticamente que você a instale. Claro, ambas as ferramentas exigem que você autentique sua conta do ngrok ou do Expose antes de poder começar a compartilhar sites.

Para compartilhar um site, navegue até o diretório do site no seu terminal e execute o comando `share` do Valet. Uma URL publicamente acessível será colocada na sua área de transferência e estará pronta para ser colada diretamente no seu navegador ou compartilhada com sua equipe:

```shell
cd ~/Sites/laravel

valet share
```

Para parar de compartilhar seu site, você pode pressionar `Control + C`.

> **Warning:**
> Se você estiver usando um servidor DNS personalizado (como `1.1.1.1`), o compartilhamento via ngrok pode não funcionar corretamente. Se esse for o caso na sua máquina, abra as configurações de sistema do seu Mac, vá para as configurações de Rede, abra as configurações Avançadas, depois vá para a aba DNS e adicione `127.0.0.1` como seu primeiro servidor DNS.

<a id="sharing-sites-via-ngrok"></a>
#### Compartilhando Sites via Ngrok

Compartilhar seu site usando o ngrok requer que você [crie uma conta no ngrok](https://dashboard.ngrok.com/signup) e [configure um token de autenticação](https://dashboard.ngrok.com/get-started/your-authtoken). Uma vez que você tenha um token de autenticação, pode atualizar sua configuração do Valet com esse token:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> **Note:**
> Você pode passar parâmetros adicionais do ngrok para o comando share, como `valet share --region=eu`. Para mais informações, consulte a [documentação do ngrok](https://ngrok.com/docs).

<a id="sharing-sites-via-expose"></a>
#### Compartilhando Sites via Expose

Compartilhar seu site usando o Expose requer que você [crie uma conta no Expose](https://expose.dev/register) e [autentique com o Expose por meio do seu token de autenticação](https://expose.dev/docs/getting-started/getting-your-token).

Você pode consultar a [documentação do Expose](https://expose.dev/docs) para informações sobre os parâmetros de linha de comando adicionais que ele oferece suporte.

<a id="sharing-sites-on-your-local-network"></a>
### Compartilhando Sites na Sua Rede Local

O Valet restringe o tráfego de entrada à interface interna `127.0.0.1` por padrão, para que sua máquina de desenvolvimento não fique exposta a riscos de segurança vindos da Internet.

Se você quiser permitir que outros dispositivos na sua rede local acessem os sites do Valet na sua máquina por meio do endereço IP da máquina (ex.: `192.168.1.10/application.test`), você precisará editar manualmente o arquivo de configuração do Nginx apropriado para aquele site para remover a restrição na diretiva `listen`. Você deve remover o prefixo `127.0.0.1:` na diretiva `listen` para as portas 80 e 443.

Se você não executou `valet secure` no projeto, pode abrir o acesso de rede para todos os sites que não são HTTPS editando o arquivo `/usr/local/etc/nginx/valet/valet.conf`. No entanto, se você está servindo o site do projeto via HTTPS (você executou `valet secure` para o site), então deve editar o arquivo `~/.config/valet/Nginx/app-name.test`.

Uma vez que você tenha atualizado sua configuração do Nginx, execute o comando `valet restart` para aplicar as alterações de configuração.

<a id="site-specific-environment-variables"></a>
## Variáveis de Ambiente Específicas por Site

Algumas aplicações que usam outros frameworks podem depender de variáveis de ambiente do servidor, mas não fornecem uma maneira de configurar essas variáveis dentro do seu projeto. O Valet permite que você configure variáveis de ambiente específicas por site adicionando um arquivo `.valet-env.php` dentro da raiz do seu projeto. Este arquivo deve retornar um array de pares site / variável de ambiente que serão adicionados ao array global `$_SERVER` para cada site especificado no array:

```php
<?php

return [
    // Define $_SERVER['key'] como "value" para o site laravel.test...
    'laravel' => [
        'key' => 'value',
    ],

    // Define $_SERVER['key'] como "value" para todos os sites...
    '*' => [
        'key' => 'value',
    ],
];
```

<a id="proxying-services"></a>
## Fazendo Proxy de Serviços

Às vezes, você pode querer fazer proxy de um domínio do Valet para outro serviço na sua máquina local. Por exemplo, você pode ocasionalmente precisar executar o Valet enquanto também executa um site separado no Docker; no entanto, o Valet e o Docker não podem ambos se vincular à porta 80 ao mesmo tempo.

Para resolver isso, você pode usar o comando `proxy` para gerar um proxy. Por exemplo, você pode fazer proxy de todo o tráfego de `http://elasticsearch.test` para `http://127.0.0.1:9200`:

```shell
# Proxy via HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy via TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

Você pode remover um proxy usando o comando `unproxy`:

```shell
valet unproxy elasticsearch
```

Você pode usar o comando `proxies` para listar todas as configurações de site que têm proxy:

```shell
valet proxies
```

<a id="custom-valet-drivers"></a>
## Drivers Personalizados do Valet

Você pode escrever seu próprio "driver" do Valet para servir aplicações PHP que rodam em um framework ou CMS que não é nativamente suportado pelo Valet. Quando você instala o Valet, um diretório `~/.config/valet/Drivers` é criado, contendo um arquivo `SampleValetDriver.php`. Este arquivo contém uma implementação de driver de exemplo para demonstrar como escrever um driver personalizado. Escrever um driver requer apenas que você implemente três métodos: `serves`, `isStaticFile` e `frontControllerPath`.

Os três métodos recebem os valores `$sitePath`, `$siteName` e `$uri` como seus argumentos. O `$sitePath` é o caminho totalmente qualificado para o site sendo servido na sua máquina, como `/Users/Lisa/Sites/my-project`. O `$siteName` é a parte "host" / "nome do site" do domínio (`my-project`). O `$uri` é a URI da requisição de entrada (`/foo/bar`).

Uma vez que você tenha concluído seu driver personalizado do Valet, coloque-o no diretório `~/.config/valet/Drivers` usando a convenção de nomenclatura `FrameworkValetDriver.php`. Por exemplo, se você estiver escrevendo um driver valet personalizado para o WordPress, o nome do seu arquivo deve ser `WordPressValetDriver.php`.

Vamos dar uma olhada em uma implementação de exemplo de cada método que seu driver personalizado do Valet deve implementar.

<a id="the-serves-method"></a>
#### O Método `serves`

O método `serves` deve retornar `true` se o seu driver deve tratar a requisição de entrada. Caso contrário, o método deve retornar `false`. Então, dentro deste método, você deve tentar determinar se o `$sitePath` fornecido contém um projeto do tipo que você está tentando servir.

Por exemplo, vamos imaginar que estamos escrevendo um `WordPressValetDriver`. Nosso método `serves` pode se parecer com algo assim:

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a id="the-isstaticfile-method"></a>
#### O Método `isStaticFile`

O `isStaticFile` deve determinar se a requisição de entrada é para um arquivo que é "estático", como uma imagem ou uma folha de estilos. Se o arquivo for estático, o método deve retornar o caminho totalmente qualificado para o arquivo estático no disco. Se a requisição de entrada não for para um arquivo estático, o método deve retornar `false`:

```php
/**
 * Determine if the incoming request is for a static file.
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> **Warning:**
> O método `isStaticFile` só será chamado se o método `serves` retornar `true` para a requisição de entrada e a URI da requisição não for `/`.

<a id="the-frontcontrollerpath-method"></a>
#### O Método `frontControllerPath`

O método `frontControllerPath` deve retornar o caminho totalmente qualificado para o "front controller" da sua aplicação, que normalmente é um arquivo "index.php" ou equivalente:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a id="local-drivers"></a>
### Drivers Locais

Se você quiser definir um driver personalizado do Valet para uma única aplicação, crie um arquivo `LocalValetDriver.php` no diretório raiz da aplicação. Seu driver personalizado pode estender a classe base `ValetDriver` ou estender um driver específico de aplicação existente, como o `LaravelValetDriver`:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a id="other-valet-commands"></a>
## Outros Comandos do Valet

<div class="overflow-auto">

| Comando | Descrição |
| --- | --- |
| `valet list` | Exibe uma lista de todos os comandos do Valet. |
| `valet diagnose` | Gera diagnósticos para ajudar na depuração do Valet. |
| `valet directory-listing` | Determina o comportamento de listagem de diretórios. O padrão é "off", que renderiza uma página 404 para diretórios. |
| `valet forget` | Execute este comando a partir de um diretório "parkeado" para removê-lo da lista de diretórios parkeados. |
| `valet log` | Visualiza uma lista de logs que são escritos pelos serviços do Valet. |
| `valet paths` | Visualiza todos os seus caminhos "parkeados". |
| `valet restart` | Reinicia os daemons do Valet. |
| `valet start` | Inicia os daemons do Valet. |
| `valet stop` | Para os daemons do Valet. |
| `valet trust` | Adiciona arquivos sudoers para o Brew e o Valet para permitir que comandos do Valet sejam executados sem solicitar sua senha. |
| `valet uninstall` | Desinstala o Valet: mostra as instruções para desinstalação manual. Passe a opção `--force` para excluir agressivamente todos os recursos do Valet. |

</div>

<a id="valet-directories-and-files"></a>
## Diretórios e Arquivos do Valet

Você pode achar as informações de diretório e arquivo a seguir úteis ao solucionar problemas com seu ambiente do Valet:

#### `~/.config/valet`

Contém toda a configuração do Valet. Você pode querer manter um backup deste diretório.

#### `~/.config/valet/dnsmasq.d/`

Este diretório contém a configuração do DNSMasq.

#### `~/.config/valet/Drivers/`

Este diretório contém os drivers do Valet. Os drivers determinam como um determinado framework / CMS é servido.

#### `~/.config/valet/Nginx/`

Este diretório contém todas as configurações de site do Nginx do Valet. Esses arquivos são reconstruídos ao executar os comandos `install` e `secure`.

#### `~/.config/valet/Sites/`

Este diretório contém todos os links simbólicos para seus [projetos vinculados](#the-link-command).

#### `~/.config/valet/config.json`

Este arquivo é o arquivo de configuração mestre do Valet.

#### `~/.config/valet/valet.sock`

Este arquivo é o socket do PHP-FPM usado pela instalação do Nginx do Valet. Ele só existirá se o PHP estiver rodando corretamente.

#### `~/.config/valet/Log/fpm-php.www.log`

Este arquivo é o log de usuário para erros do PHP.

#### `~/.config/valet/Log/nginx-error.log`

Este arquivo é o log de usuário para erros do Nginx.

#### `/usr/local/var/log/php-fpm.log`

Este arquivo é o log de sistema para erros do PHP-FPM.

#### `/usr/local/var/log/nginx`

Este diretório contém os logs de acesso e de erro do Nginx.

#### `/usr/local/etc/php/X.X/conf.d`

Este diretório contém os arquivos `*.ini` para várias configurações do PHP.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

Este arquivo é o arquivo de configuração do pool do PHP-FPM.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

Este arquivo é a configuração padrão do Nginx usada para construir certificados SSL para seus sites.

<a id="disk-access"></a>
### Acesso ao Disco

Desde o macOS 10.14, [o acesso a alguns arquivos e diretórios é restrito por padrão](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). Essas restrições incluem os diretórios Desktop, Documents e Downloads. Além disso, o acesso a volumes de rede e volumes removíveis é restrito. Portanto, o Valet recomenda que suas pastas de site estejam localizadas fora dessas localizações protegidas.

No entanto, se você quiser servir sites a partir de uma dessas localizações, precisará conceder ao Nginx "Full Disk Access" (Acesso Total ao Disco). Caso contrário, você pode encontrar erros de servidor ou outro comportamento imprevisível do Nginx, especialmente ao servir assets estáticos. Normalmente, o macOS solicitará automaticamente que você conceda ao Nginx acesso total a essas localizações. Ou, você pode fazer isso manualmente via `System Preferences` > `Security & Privacy` > `Privacy` e selecionando `Full Disk Access`. Em seguida, habilite quaisquer entradas `nginx` no painel da janela principal.
