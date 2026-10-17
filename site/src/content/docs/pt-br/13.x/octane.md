---
title: "Laravel Octane"
---

- [Introdução](#introduction)
- [Instalação](#installation)
- [Pré-requisitos do Servidor](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Servindo Sua Aplicação](#serving-your-application)
    - [Servindo Sua Aplicação via HTTPS](#serving-your-application-via-https)
    - [Servindo Sua Aplicação via Nginx](#serving-your-application-via-nginx)
    - [Monitorando Alterações de Arquivos](#watching-for-file-changes)
    - [Especificando a Quantidade de Workers](#specifying-the-worker-count)
    - [Especificando a Quantidade Máxima de Requisições](#specifying-the-max-request-count)
    - [Especificando o Tempo Máximo de Execução](#specifying-the-max-execution-time)
    - [Recarregando os Workers](#reloading-the-workers)
    - [Parando o Servidor](#stopping-the-server)
- [Injeção de Dependências e Octane](#dependency-injection-and-octane)
    - [Injeção do Container](#container-injection)
    - [Injeção da Requisição](#request-injection)
    - [Injeção do Repositório de Configuração](#configuration-repository-injection)
- [Gerenciando Vazamentos de Memória](#managing-memory-leaks)
- [Tarefas Concorrentes](#concurrent-tasks)
- [Ticks e Intervalos](#ticks-and-intervals)
- [O Cache do Octane](#the-octane-cache)
    - [Intervalos de Cache](#cache-intervals)
- [Tabelas](#tables)

<a id="introduction"></a>
## Introdução

[Laravel Octane](https://github.com/laravel/octane) potencializa o desempenho da sua aplicação servindo-a por meio de servidores de aplicação de alta performance, incluindo [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src) e [RoadRunner](https://roadrunner.dev). O Octane inicializa sua aplicação uma única vez, mantém-na em memória e, em seguida, a alimenta com requisições em velocidade supersônica.

<a id="installation"></a>
## Instalação

O Octane pode ser instalado através do gerenciador de pacotes Composer:

```shell
composer require laravel/octane
```

Após instalar o Octane, você pode executar o comando Artisan `octane:install`, que instalará o arquivo de configuração do Octane na sua aplicação:

```shell
php artisan octane:install
```

<a id="server-prerequisites"></a>
## Pré-requisitos do Servidor

<a id="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev) é um servidor de aplicação PHP, escrito em Go, que oferece suporte a recursos web modernos como early hints, compressão Brotli e Zstandard. Quando você instala o Octane e escolhe o FrankenPHP como servidor, o Octane fará automaticamente o download e a instalação do binário do FrankenPHP para você.

<a id="frankenphp-via-laravel-sail"></a>
#### FrankenPHP via Laravel Sail

Se você planeja desenvolver sua aplicação usando o [Laravel Sail](/en/sail/), deve executar os seguintes comandos para instalar o Octane e o FrankenPHP:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

Em seguida, você deve usar o comando Artisan `octane:install` para instalar o binário do FrankenPHP:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

Por fim, adicione uma variável de ambiente `SUPERVISOR_PHP_COMMAND` à definição do serviço `laravel.test` no arquivo `docker-compose.yml` da sua aplicação. Essa variável de ambiente conterá o comando que o Sail usará para servir sua aplicação via Octane, em vez do servidor de desenvolvimento do PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

Para habilitar HTTPS, HTTP/2 e HTTP/3, aplique estas modificações:

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

Normalmente, você deve acessar sua aplicação Sail com FrankenPHP via `https://localhost`, pois usar `https://127.0.0.1` requer configuração adicional e é [desencorajado](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a id="frankenphp-via-docker"></a>
#### FrankenPHP via Docker

Usar as imagens Docker oficiais do FrankenPHP pode oferecer melhor desempenho e o uso de extensões adicionais não incluídas nas instalações estáticas do FrankenPHP. Além disso, as imagens Docker oficiais oferecem suporte para executar o FrankenPHP em plataformas que ele não suporta nativamente, como o Windows. As imagens Docker oficiais do FrankenPHP são adequadas tanto para desenvolvimento local quanto para uso em produção.

Você pode usar o seguinte Dockerfile como ponto de partida para containerizar sua aplicação Laravel com FrankenPHP:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

Em seguida, durante o desenvolvimento, você pode utilizar o seguinte arquivo Docker Compose para executar sua aplicação:

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

Se a opção `--log-level` for passada explicitamente ao comando `php artisan octane:start`, o Octane usará o logger nativo do FrankenPHP e, a menos que configurado de outra forma, produzirá logs JSON estruturados.

Você pode consultar [a documentação oficial do FrankenPHP](https://frankenphp.dev/docs/docker/) para mais informações sobre como executar o FrankenPHP com Docker.

<a id="frankenphp-caddyfile"></a>
#### Configuração Personalizada do Caddyfile

Ao usar o FrankenPHP, você pode especificar um Caddyfile personalizado usando a opção `--caddyfile` ao iniciar o Octane:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

Isso permite que você personalize a configuração do FrankenPHP além das configurações padrão, como adicionar middlewares personalizados, configurar roteamento avançado ou definir diretivas personalizadas. Você pode consultar a [documentação oficial do Caddy](https://caddyserver.com/docs/caddyfile) para mais informações sobre a sintaxe e as opções de configuração do Caddyfile.

<a id="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev) é alimentado pelo binário do RoadRunner, que é construído usando Go. Na primeira vez que você iniciar um servidor Octane baseado em RoadRunner, o Octane oferecerá para fazer o download e a instalação do binário do RoadRunner para você.

<a id="roadrunner-via-laravel-sail"></a>
#### RoadRunner via Laravel Sail

Se você planeja desenvolver sua aplicação usando o [Laravel Sail](/en/sail/), deve executar os seguintes comandos para instalar o Octane e o RoadRunner:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

Em seguida, você deve iniciar um shell do Sail e usar o executável `rr` para obter a build mais recente do binário do RoadRunner para Linux:

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

Depois, adicione uma variável de ambiente `SUPERVISOR_PHP_COMMAND` à definição do serviço `laravel.test` no arquivo `docker-compose.yml` da sua aplicação. Essa variável de ambiente conterá o comando que o Sail usará para servir sua aplicação via Octane, em vez do servidor de desenvolvimento do PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

Por fim, garanta que o binário `rr` seja executável e construa as imagens do Sail:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a id="swoole"></a>
### Swoole

Se você planeja usar o servidor de aplicação Swoole para servir sua aplicação Laravel Octane, deve instalar a extensão PHP Swoole. Normalmente, isso pode ser feito via PECL:

```shell
pecl install swoole
```

<a id="openswoole"></a>
#### Open Swoole

Se você deseja usar o servidor de aplicação Open Swoole para servir sua aplicação Laravel Octane, deve instalar a extensão PHP Open Swoole. Normalmente, isso pode ser feito via PECL:

```shell
pecl install openswoole
```

Usar o Laravel Octane com Open Swoole oferece a mesma funcionalidade fornecida pelo Swoole, como tarefas concorrentes, ticks e intervalos.

<a id="swoole-via-laravel-sail"></a>
#### Swoole via Laravel Sail

> **Aviso:**
> Antes de servir uma aplicação Octane via Sail, certifique-se de ter a versão mais recente do Laravel Sail e execute `./vendor/bin/sail build --no-cache` no diretório raiz da sua aplicação.

Alternativamente, você pode desenvolver sua aplicação Octane baseada em Swoole usando o [Laravel Sail](/en/sail/), o ambiente de desenvolvimento oficial baseado em Docker para o Laravel. O Laravel Sail inclui a extensão Swoole por padrão. No entanto, você ainda precisará ajustar o arquivo `docker-compose.yml` usado pelo Sail.

Para começar, adicione uma variável de ambiente `SUPERVISOR_PHP_COMMAND` à definição do serviço `laravel.test` no arquivo `docker-compose.yml` da sua aplicação. Essa variável de ambiente conterá o comando que o Sail usará para servir sua aplicação via Octane, em vez do servidor de desenvolvimento do PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

Por fim, construa as imagens do Sail:

```shell
./vendor/bin/sail build --no-cache
```

<a id="swoole-configuration"></a>
#### Configuração do Swoole

O Swoole oferece suporte a algumas opções de configuração adicionais que você pode adicionar ao arquivo de configuração `octane` caso necessário. Como raramente precisam ser modificadas, essas opções não são incluídas no arquivo de configuração padrão:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a id="serving-your-application"></a>
## Servindo Sua Aplicação

O servidor Octane pode ser iniciado através do comando Artisan `octane:start`. Por padrão, este comando utilizará o servidor especificado pela opção de configuração `server` do arquivo de configuração `octane` da sua aplicação:

```shell
php artisan octane:start
```

Por padrão, o Octane iniciará o servidor na porta 8000, então você pode acessar sua aplicação em um navegador web via `http://localhost:8000`.

<a id="keeping-octane-running-in-production"></a>
#### Mantendo o Octane em Execução em Produção

Se você estiver implantando sua aplicação Octane em produção, deve usar um monitor de processos como o Supervisor para garantir que o servidor Octane continue em execução. Um exemplo de arquivo de configuração do Supervisor para o Octane pode ser semelhante ao seguinte:

```ini
[program:octane]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/example.com/artisan octane:start --server=frankenphp --host=127.0.0.1 --port=8000
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/storage/logs/octane.log
stopwaitsecs=3600
```

<a id="serving-your-application-via-https"></a>
### Servindo Sua Aplicação via HTTPS

Por padrão, aplicações executadas via Octane geram links com o prefixo `http://`. A variável de ambiente `OCTANE_HTTPS`, usada no arquivo de configuração `config/octane.php` da sua aplicação, pode ser definida como `true` ao servir sua aplicação via HTTPS. Quando este valor de configuração é `true`, o Octane instruirá o Laravel a adicionar o prefixo `https://` a todos os links gerados:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a id="serving-your-application-via-nginx"></a>
### Servindo Sua Aplicação via Nginx

> **Nota:**
> Se você ainda não estiver pronto para gerenciar sua própria configuração de servidor ou não se sentir confortável em configurar todos os vários serviços necessários para executar uma aplicação Laravel Octane robusta, conheça o [Laravel Cloud](https://cloud.laravel.com), que oferece suporte totalmente gerenciado para o Laravel Octane.

Em ambientes de produção, você deve servir sua aplicação Octane por trás de um servidor web tradicional, como Nginx ou Apache. Isso permitirá que o servidor web sirva seus assets estáticos, como imagens e folhas de estilo, além de gerenciar a terminação do seu certificado SSL.

No exemplo de configuração do Nginx abaixo, o Nginx servirá os assets estáticos do site e fará o proxy das requisições para o servidor Octane que está em execução na porta 8000:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```

<a id="watching-for-file-changes"></a>
### Monitorando Alterações de Arquivos

Como sua aplicação é carregada na memória uma única vez quando o servidor Octane é iniciado, quaisquer alterações nos arquivos da sua aplicação não serão refletidas quando você atualizar o navegador. Por exemplo, definições de rotas adicionadas ao seu arquivo `routes/web.php` não serão refletidas até que o servidor seja reiniciado. Por conveniência, você pode usar a flag `--watch` para instruir o Octane a reiniciar automaticamente o servidor sempre que houver alterações de arquivos na sua aplicação:

```shell
php artisan octane:start --watch
```

Antes de usar este recurso, você deve garantir que o [Node](https://nodejs.org) esteja instalado no seu ambiente de desenvolvimento local. Além disso, você deve instalar a biblioteca de monitoramento de arquivos [Chokidar](https://github.com/paulmillr/chokidar) no seu projeto:

```shell
npm install --save-dev chokidar
```

Você pode configurar os diretórios e arquivos que devem ser monitorados usando a opção de configuração `watch` no arquivo `config/octane.php` da sua aplicação.

<a id="specifying-the-worker-count"></a>
### Especificando a Quantidade de Workers

Por padrão, o Octane iniciará um worker de requisições da aplicação para cada núcleo de CPU disponível na sua máquina. Esses workers serão então usados para atender às requisições HTTP recebidas pela sua aplicação. Você pode especificar manualmente quantos workers deseja iniciar usando a opção `--workers` ao invocar o comando `octane:start`:

```shell
php artisan octane:start --workers=4
```

Se você estiver usando o servidor de aplicação Swoole, também pode especificar quantos ["task workers"](#concurrent-tasks) deseja iniciar:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a id="specifying-the-max-request-count"></a>
### Especificando a Quantidade Máxima de Requisições

Para ajudar a prevenir vazamentos de memória pontuais, o Octane reinicia graciosamente qualquer worker assim que ele tiver processado 500 requisições. Para ajustar este número, você pode usar a opção `--max-requests`:

```shell
php artisan octane:start --max-requests=250
```

<a id="specifying-the-max-execution-time"></a>
### Especificando o Tempo Máximo de Execução

Por padrão, o Laravel Octane define um tempo máximo de execução de 30 segundos para as requisições recebidas, através da opção `max_execution_time` no arquivo de configuração `config/octane.php` da sua aplicação:

```php
'max_execution_time' => 30,
```

Esta configuração define o número máximo de segundos que uma requisição recebida pode executar antes de ser encerrada. Definir este valor como `0` desabilitará completamente o limite de tempo de execução. Esta opção de configuração é particularmente útil para aplicações que lidam com requisições de longa duração, como uploads de arquivos, processamento de dados ou chamadas de API para serviços externos.

> **Aviso:**
> Ao modificar a configuração `max_execution_time`, você deve reiniciar o servidor Octane para que as alterações tenham efeito.

<a id="reloading-the-workers"></a>
### Recarregando os Workers

Você pode reiniciar graciosamente os workers da aplicação do servidor Octane usando o comando `octane:reload`. Normalmente, isso deve ser feito após a implantação para que o código recém-implantado seja carregado na memória e utilizado para atender às requisições seguintes:

```shell
php artisan octane:reload
```

<a id="stopping-the-server"></a>
### Parando o Servidor

Você pode parar o servidor Octane usando o comando Artisan `octane:stop`:

```shell
php artisan octane:stop
```

<a id="checking-the-server-status"></a>
#### Verificando o Status do Servidor

Você pode verificar o status atual do servidor Octane usando o comando Artisan `octane:status`:

```shell
php artisan octane:status
```

<a id="dependency-injection-and-octane"></a>
## Injeção de Dependências e Octane

Como o Octane inicializa sua aplicação uma única vez e a mantém em memória enquanto atende às requisições, há algumas ressalvas que você deve considerar ao construir sua aplicação. Por exemplo, os métodos `register` e `boot` dos service providers da sua aplicação serão executados apenas uma vez, quando o worker de requisições for inicializado. Nas requisições seguintes, a mesma instância da aplicação será reutilizada.

Diante disso, você deve ter um cuidado especial ao injetar o container de serviços ou a requisição da aplicação no construtor de qualquer objeto. Ao fazer isso, esse objeto pode ter uma versão desatualizada do container ou da requisição nas requisições seguintes.

O Octane tratará automaticamente de redefinir qualquer estado do framework de primeira parte entre as requisições. No entanto, o Octane nem sempre sabe como redefinir o estado global criado pela sua aplicação. Portanto, você deve estar ciente de como construir sua aplicação de forma compatível com o Octane. A seguir, discutiremos as situações mais comuns que podem causar problemas ao usar o Octane.

<a id="container-injection"></a>
### Injeção do Container

Em geral, você deve evitar injetar o container de serviços da aplicação ou a instância da requisição HTTP nos construtores de outros objetos. Por exemplo, o seguinte binding injeta o container de serviços inteiro da aplicação em um objeto registrado como singleton:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```

Neste exemplo, se a instância de `Service` for resolvida durante o processo de inicialização da aplicação, o container será injetado no serviço e esse mesmo container será mantido pela instância de `Service` nas requisições seguintes. Isso **pode** não ser um problema para a sua aplicação específica; no entanto, pode fazer com que o container não encontre inesperadamente bindings que foram adicionados posteriormente no ciclo de inicialização ou por uma requisição subsequente.

Como solução alternativa, você poderia deixar de registrar o binding como singleton ou injetar no serviço uma closure resolvedora do container que sempre resolva a instância atual do container:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

O helper global `app` e o método `Container::getInstance()` sempre retornarão a versão mais recente do container da aplicação.

<a id="request-injection"></a>
### Injeção da Requisição

Em geral, você deve evitar injetar o container de serviços da aplicação ou a instância da requisição HTTP nos construtores de outros objetos. Por exemplo, o seguinte binding injeta a instância inteira da requisição em um objeto registrado como singleton:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```

Neste exemplo, se a instância de `Service` for resolvida durante o processo de inicialização da aplicação, a requisição HTTP será injetada no serviço e essa mesma requisição será mantida pela instância de `Service` nas requisições seguintes. Portanto, todos os headers, dados de entrada e da query string, bem como todos os outros dados da requisição, ficarão incorretos.

Como solução alternativa, você poderia deixar de registrar o binding como singleton ou injetar no serviço uma closure resolvedora da requisição que sempre resolva a instância atual da requisição. Ou, a abordagem mais recomendada é simplesmente passar as informações específicas da requisição de que o seu objeto precisa para um dos métodos do objeto em tempo de execução:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```

O helper global `request` sempre retornará a requisição que a aplicação está tratando no momento e, portanto, é seguro de usar dentro da sua aplicação.

> **Aviso:**
> É aceitável fazer type-hint da instância `Illuminate\Http\Request` nos métodos dos seus controllers e nas closures de rotas.

<a id="configuration-repository-injection"></a>
### Injeção do Repositório de Configuração

Em geral, você deve evitar injetar a instância do repositório de configuração nos construtores de outros objetos. Por exemplo, o seguinte binding injeta o repositório de configuração em um objeto registrado como singleton:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```

Neste exemplo, se os valores de configuração mudarem entre as requisições, esse serviço não terá acesso aos novos valores, pois depende da instância original do repositório.

Como solução alternativa, você poderia deixar de registrar o binding como singleton ou injetar na classe uma closure resolvedora do repositório de configuração:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

O helper global `config` sempre retornará a versão mais recente do repositório de configuração e, portanto, é seguro de usar dentro da sua aplicação.

<a id="managing-memory-leaks"></a>
### Gerenciando Vazamentos de Memória

Lembre-se: o Octane mantém sua aplicação em memória entre as requisições; portanto, adicionar dados a um array mantido estaticamente resultará em um vazamento de memória. Por exemplo, o seguinte controller tem um vazamento de memória, pois cada requisição para a aplicação continuará adicionando dados ao array estático `$data`:

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```

Ao construir sua aplicação, você deve ter um cuidado especial para evitar a criação desses tipos de vazamentos de memória. Recomenda-se que você monitore o uso de memória da sua aplicação durante o desenvolvimento local para garantir que não esteja introduzindo novos vazamentos de memória na aplicação.

<a id="concurrent-tasks"></a>
## Tarefas Concorrentes

> **Aviso:**
> Este recurso requer o [Swoole](#swoole).

Ao usar o Swoole, você pode executar operações de forma concorrente por meio de tarefas leves em segundo plano. Você pode fazer isso usando o método `concurrently` do Octane. Você pode combinar este método com a desestruturação de arrays do PHP para obter os resultados de cada operação:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

As tarefas concorrentes processadas pelo Octane utilizam os "task workers" do Swoole e são executadas em um processo completamente diferente daquele da requisição recebida. A quantidade de workers disponíveis para processar tarefas concorrentes é determinada pela diretiva `--task-workers` no comando `octane:start`:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

Ao invocar o método `concurrently`, você não deve fornecer mais de 1024 tarefas devido às limitações impostas pelo sistema de tarefas do Swoole.

<a id="ticks-and-intervals"></a>
## Ticks e Intervalos

> **Aviso:**
> Este recurso requer o [Swoole](#swoole).

Ao usar o Swoole, você pode registrar operações "tick" que serão executadas a cada número especificado de segundos. Você pode registrar callbacks "tick" através do método `tick`. O primeiro argumento fornecido ao método `tick` deve ser uma string que represente o nome do ticker. O segundo argumento deve ser um callable que será invocado no intervalo especificado.

Neste exemplo, registraremos uma closure para ser invocada a cada 10 segundos. Normalmente, o método `tick` deve ser chamado dentro do método `boot` de um dos service providers da sua aplicação:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

Usando o método `immediate`, você pode instruir o Octane a invocar imediatamente o callback do tick quando o servidor Octane for inicializado e, em seguida, a cada N segundos:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a id="the-octane-cache"></a>
## O Cache do Octane

> **Aviso:**
> Este recurso requer o [Swoole](#swoole).

Ao usar o Swoole, você pode aproveitar o driver de cache do Octane, que oferece velocidades de leitura e escrita de até 2 milhões de operações por segundo. Portanto, este driver de cache é uma excelente escolha para aplicações que precisam de velocidades extremas de leitura / escrita na sua camada de cache.

Este driver de cache é alimentado por [tabelas Swoole](https://www.swoole.co.uk/docs/modules/swoole-table). Todos os dados armazenados no cache estão disponíveis para todos os workers do servidor. No entanto, os dados em cache serão descartados quando o servidor for reiniciado:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> **Nota:**
> O número máximo de entradas permitidas no cache do Octane pode ser definido no arquivo de configuração `octane` da sua aplicação.

<a id="cache-intervals"></a>
### Intervalos de Cache

Além dos métodos típicos fornecidos pelo sistema de cache do Laravel, o driver de cache do Octane oferece caches baseados em intervalos. Esses caches são atualizados automaticamente no intervalo especificado e devem ser registrados dentro do método `boot` de um dos service providers da sua aplicação. Por exemplo, o seguinte cache será atualizado a cada cinco segundos:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a id="tables"></a>
## Tabelas

> **Aviso:**
> Este recurso requer o [Swoole](#swoole).

Ao usar o Swoole, você pode definir e interagir com suas próprias [tabelas Swoole](https://www.swoole.co.uk/docs/modules/swoole-table) arbitrárias. As tabelas Swoole oferecem um throughput de desempenho extremo, e os dados dessas tabelas podem ser acessados por todos os workers do servidor. No entanto, os dados contidos nelas serão perdidos quando o servidor for reiniciado.

As tabelas devem ser definidas dentro do array de configuração `tables` do arquivo de configuração `octane` da sua aplicação. Um exemplo de tabela que permite no máximo 1000 linhas já está configurado para você. O tamanho máximo de colunas de string pode ser configurado especificando o tamanho da coluna após o tipo da coluna, como visto abaixo:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

Para acessar uma tabela, você pode usar o método `Octane::table`:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> **Aviso:**
> Os tipos de coluna suportados pelas tabelas Swoole são: `string`, `int` e `float`.
