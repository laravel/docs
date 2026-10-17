---
title: "Deploy"
---

- [Introdução](#introduction)
- [Requisitos do Servidor](#server-requirements)
- [Configuração do Servidor](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [Permissões de Diretórios](#directory-permissions)
- [Otimização](#optimization)
    - [Cache de Configuração](#optimizing-configuration-loading)
    - [Cache de Eventos](#caching-events)
    - [Cache de Rotas](#optimizing-route-loading)
    - [Cache de Views](#optimizing-view-loading)
- [Recarregando Serviços](#reloading-services)
- [Modo Debug](#debug-mode)
- [A Rota de Health Check](#the-health-route)
- [Fazendo Deploy com Laravel Cloud ou Forge](#deploying-with-cloud-or-forge)

<a id="introduction"></a>
## Introdução

Quando você estiver pronto para fazer o deploy da sua aplicação Laravel em produção, existem algumas coisas importantes que você pode fazer para garantir que sua aplicação esteja rodando da maneira mais eficiente possível. Neste documento, abordaremos alguns ótimos pontos de partida para garantir que o deploy da sua aplicação Laravel seja feito corretamente.

<a id="server-requirements"></a>
## Requisitos do Servidor

O framework Laravel tem alguns requisitos de sistema. Você deve garantir que seu servidor web tenha a seguinte versão mínima do PHP e extensões:

<div class="content-list" markdown="1">

- PHP >= 8.3
- Extensão PHP Ctype
- Extensão PHP cURL
- Extensão PHP DOM
- Extensão PHP Fileinfo
- Extensão PHP Filter
- Extensão PHP Hash
- Extensão PHP Mbstring
- Extensão PHP OpenSSL
- Extensão PHP PCRE
- Extensão PHP PDO
- Extensão PHP Session
- Extensão PHP Tokenizer
- Extensão PHP XML

</div>

<a id="server-configuration"></a>
## Configuração do Servidor

<a id="nginx"></a>
### Nginx

Se você estiver fazendo o deploy da sua aplicação em um servidor que roda Nginx, pode usar o arquivo de configuração a seguir como ponto de partida para configurar seu servidor web. Muito provavelmente, esse arquivo precisará ser personalizado de acordo com a configuração do seu servidor. **Se você quiser ajuda para gerenciar seu servidor, considere usar uma plataforma Laravel totalmente gerenciada como o [Laravel Cloud](https://cloud.laravel.com).**

Certifique-se de que, como na configuração abaixo, seu servidor web direcione todas as requisições para o arquivo `public/index.php` da sua aplicação. Você nunca deve tentar mover o arquivo `index.php` para a raiz do seu projeto, pois servir a aplicação a partir da raiz do projeto exporá muitos arquivos de configuração sensíveis à Internet pública:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 8 32k;
        fastcgi_busy_buffers_size 64k;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a id="frankenphp"></a>
### FrankenPHP

O [FrankenPHP](https://frankenphp.dev/) também pode ser usado para servir suas aplicações Laravel. O FrankenPHP é um servidor de aplicações PHP moderno escrito em Go. Para servir uma aplicação PHP Laravel usando o FrankenPHP, você pode simplesmente invocar o comando `php-server`:

```shell
frankenphp php-server -r public/
```

Para aproveitar os recursos mais poderosos suportados pelo FrankenPHP, como sua integração com o [Laravel Octane](../octane/), HTTP/3, compressão moderna ou a capacidade de empacotar aplicações Laravel como binários standalone, consulte a [documentação do Laravel](https://frankenphp.dev/docs/laravel/) do FrankenPHP.

<a id="directory-permissions"></a>
### Permissões de Diretórios

O Laravel precisará escrever nos diretórios `bootstrap/cache` e `storage`, portanto você deve garantir que o dono do processo do servidor web tenha permissão de escrita nesses diretórios.

<a id="optimization"></a>
## Otimização

Ao fazer o deploy da sua aplicação em produção, há diversos arquivos que devem ser colocados em cache, incluindo sua configuração, eventos, rotas e views. O Laravel fornece um único e conveniente comando Artisan `optimize` que colocará todos esses arquivos em cache. Esse comando normalmente deve ser invocado como parte do processo de deploy da sua aplicação:

```shell
php artisan optimize
```

O método `optimize:clear` pode ser usado para remover todos os arquivos de cache gerados pelo comando `optimize`, bem como todas as chaves no driver de cache padrão:

```shell
php artisan optimize:clear
```

Na documentação a seguir, discutiremos cada um dos comandos de otimização granular que são executados pelo comando `optimize`.

<a id="optimizing-configuration-loading"></a>
### Cache de Configuração

Ao fazer o deploy da sua aplicação em produção, você deve garantir que execute o comando Artisan `config:cache` durante seu processo de deploy:

```shell
php artisan config:cache
```

Esse comando combinará todos os arquivos de configuração do Laravel em um único arquivo em cache, o que reduz bastante o número de acessos que o framework precisa fazer ao sistema de arquivos ao carregar seus valores de configuração.

> **Aviso:**
> Se você executar o comando `config:cache` durante seu processo de deploy, certifique-se de que está chamando a função `env` apenas de dentro dos seus arquivos de configuração. Depois que a configuração estiver em cache, o arquivo `.env` não será carregado e todas as chamadas à função `env` para variáveis do `.env` retornarão `null`.

<a id="caching-events"></a>
### Cache de Eventos

Você deve colocar em cache os mapeamentos de eventos para listeners descobertos automaticamente da sua aplicação durante seu processo de deploy. Isso pode ser feito invocando o comando Artisan `event:cache` durante o deploy:

```shell
php artisan event:cache
```

<a id="optimizing-route-loading"></a>
### Cache de Rotas

Se você estiver construindo uma aplicação grande com muitas rotas, deve garantir que está executando o comando Artisan `route:cache` durante seu processo de deploy:

```shell
php artisan route:cache
```

Esse comando reduz todos os seus registros de rota a uma única chamada de método dentro de um arquivo em cache, melhorando o desempenho do registro de rotas ao registrar centenas de rotas.

<a id="optimizing-view-loading"></a>
### Cache de Views

Ao fazer o deploy da sua aplicação em produção, você deve garantir que execute o comando Artisan `view:cache` durante seu processo de deploy:

```shell
php artisan view:cache
```

Esse comando pré-compila todas as suas views Blade para que não sejam compiladas sob demanda, melhorando o desempenho de cada requisição que retorna uma view.

<a id="reloading-services"></a>
## Recarregando Serviços

> **Nota:**
> Ao fazer o deploy no [Laravel Cloud](https://cloud.laravel.com), não é necessário usar o comando `reload`, pois o recarregamento elegante de todos os serviços é feito automaticamente.

Após fazer o deploy de uma nova versão da sua aplicação, quaisquer serviços de longa duração, como workers de fila, Laravel Reverb ou Laravel Octane, devem ser recarregados / reiniciados para usar o novo código. O Laravel fornece um único comando Artisan `reload` que encerrará esses serviços:

```shell
php artisan reload
```

Se você não estiver usando o [Laravel Cloud](https://cloud.laravel.com), deve configurar manualmente um monitor de processos que possa detectar quando seus processos recarregáveis são encerrados e reiniciá-los automaticamente.

<a id="debug-mode"></a>
## Modo Debug

A opção de debug no seu arquivo de configuração `config/app.php` determina quanta informação sobre um erro é realmente exibida ao usuário. Por padrão, essa opção está definida para respeitar o valor da variável de ambiente `APP_DEBUG`, que é armazenada no arquivo `.env` da sua aplicação.

> **Aviso:**
> **No seu ambiente de produção, esse valor deve ser sempre `false`. Se a variável `APP_DEBUG` estiver definida como `true` em produção, você corre o risco de expor valores de configuração sensíveis aos usuários finais da sua aplicação.**

<a id="the-health-route"></a>
## A Rota de Health Check

O Laravel inclui uma rota de health check embutida que pode ser usada para monitorar o status da sua aplicação. Em produção, essa rota pode ser usada para reportar o status da sua aplicação a um monitor de uptime, a um balanceador de carga ou a um sistema de orquestração como o Kubernetes.

Por padrão, a rota de health check é servida em `/up` e retornará uma resposta HTTP 200 se a aplicação tiver iniciado sem exceções. Caso contrário, uma resposta HTTP 500 será retornada. Você pode configurar a URI dessa rota no arquivo `bootstrap/app` da sua aplicação:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

Quando requisições HTTP são feitas para essa rota, o Laravel também despachará um evento `Illuminate\Foundation\Events\DiagnosingHealth`, permitindo que você execute health checks adicionais relevantes para sua aplicação. Dentro de um [listener](../events/) para esse evento, você pode verificar o status do banco de dados ou do cache da sua aplicação. Se você detectar um problema com sua aplicação, pode simplesmente lançar uma exceção a partir do listener.

<a id="deploying-with-cloud-or-forge"></a>
## Fazendo Deploy com Laravel Cloud ou Forge

<a id="laravel-cloud"></a>
#### Laravel Cloud

Se você quiser uma plataforma de deploy totalmente gerenciada, com auto-scaling e otimizada para Laravel, confira o [Laravel Cloud](https://cloud.laravel.com). O Laravel Cloud é uma plataforma de deploy robusta para Laravel, oferecendo computação gerenciada, bancos de dados, caches e armazenamento de objetos.

Lance sua aplicação Laravel no Cloud e se apaixone pela simplicidade escalável. O Laravel Cloud é finamente ajustado pelos criadores do Laravel para funcionar perfeitamente com o framework, para que você continue escrevendo suas aplicações Laravel exatamente como está acostumado.

<a id="laravel-forge"></a>
#### Laravel Forge

Se você prefere gerenciar seus próprios servidores, mas não se sente à vontade para configurar todos os diversos serviços necessários para rodar uma aplicação Laravel robusta, o [Laravel Forge](https://forge.laravel.com) é uma plataforma de gerenciamento de servidores VPS para aplicações Laravel.

O Laravel Forge pode criar servidores em diversos provedores de infraestrutura, como DigitalOcean, Linode, AWS e outros. Além disso, o Forge instala e gerencia todas as ferramentas necessárias para construir aplicações Laravel robustas, como Nginx, MySQL, Redis, Memcached, Beanstalk e outros.
