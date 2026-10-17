---
title: "Configuração"
---

- [Introdução](#introduction)
- [Configuração de Ambiente](#environment-configuration)
    - [Tipos de Variáveis de Ambiente](#environment-variable-types)
    - [Recuperando a Configuração de Ambiente](#retrieving-environment-configuration)
    - [Determinando o Ambiente Atual](#determining-the-current-environment)
    - [Criptografando Arquivos de Ambiente](#encrypting-environment-files)
- [Acessando Valores de Configuração](#accessing-configuration-values)
- [Cache de Configuração](#configuration-caching)
- [Publicação de Configuração](#configuration-publishing)
- [Modo Debug](#debug-mode)
- [Modo de Manutenção](#maintenance-mode)

<a id="introduction"></a>
## Introdução

Todos os arquivos de configuração do framework Laravel estão armazenados no diretório `config`. Cada opção está documentada, então fique à vontade para examinar os arquivos e se familiarizar com as opções disponíveis para você.

Esses arquivos de configuração permitem que você configure coisas como as informações de conexão do seu banco de dados, as informações do seu servidor de e-mail, bem como vários outros valores de configuração principais, como a URL da sua aplicação e a chave de criptografia.

<a id="the-about-command"></a>
#### O Comando `about`

O Laravel pode exibir uma visão geral da configuração, dos drivers e do ambiente da sua aplicação por meio do comando Artisan `about`.

```shell
php artisan about
```

Se você estiver interessado apenas em uma seção específica da saída da visão geral da aplicação, pode filtrar por essa seção usando a opção `--only`:

```shell
php artisan about --only=environment
```

Ou, para explorar em detalhes os valores de um arquivo de configuração específico, você pode usar o comando Artisan `config:show`:

```shell
php artisan config:show database
```

<a id="environment-configuration"></a>
## Configuração de Ambiente

Frequentemente é útil ter valores de configuração diferentes com base no ambiente em que a aplicação está em execução. Por exemplo, você pode desejar usar um driver de cache diferente localmente do que no seu servidor de produção.

Para facilitar isso, o Laravel utiliza a biblioteca PHP [DotEnv](https://github.com/vlucas/phpdotenv). Em uma instalação nova do Laravel, o diretório raiz da sua aplicação conterá um arquivo `.env.example` que define muitas variáveis de ambiente comuns. Durante o processo de instalação do Laravel, esse arquivo será copiado automaticamente para `.env`.

O arquivo `.env` padrão do Laravel contém alguns valores de configuração comuns que podem diferir dependendo de a sua aplicação estar em execução localmente ou em um servidor de produção na web. Esses valores são então lidos pelos arquivos de configuração dentro do diretório `config` usando a função `env` do Laravel.

Se você estiver desenvolvendo com uma equipe, pode desejar continuar incluindo e atualizando o arquivo `.env.example` junto com sua aplicação. Ao colocar valores de espaço reservado no arquivo de configuração de exemplo, outros desenvolvedores da sua equipe poderão ver claramente quais variáveis de ambiente são necessárias para executar sua aplicação.

> **Nota:**
> Qualquer variável no seu arquivo `.env` pode ser sobrescrita por variáveis de ambiente externas, como variáveis de ambiente no nível do servidor ou do sistema.

<a id="environment-file-security"></a>
#### Segurança do Arquivo de Ambiente

Seu arquivo `.env` não deve ser commitado no controle de versão da sua aplicação, pois cada desenvolvedor / servidor que usa sua aplicação pode exigir uma configuração de ambiente diferente. Além disso, isso representaria um risco de segurança caso um invasor obtivesse acesso ao seu repositório de controle de versão, já que quaisquer credenciais sensíveis ficariam expostas.

No entanto, é possível criptografar seu arquivo de ambiente usando a [criptografia de ambiente](#encrypting-environment-files) integrada ao Laravel. Arquivos de ambiente criptografados podem ser colocados no controle de versão com segurança.

<a id="additional-environment-files"></a>
#### Arquivos de Ambiente Adicionais

Antes de carregar as variáveis de ambiente da sua aplicação, o Laravel determina se uma variável de ambiente `APP_ENV` foi fornecida externamente ou se o argumento de CLI `--env` foi especificado. Se for o caso, o Laravel tentará carregar um arquivo `.env.[APP_ENV]` caso ele exista. Se não existir, o arquivo `.env` padrão será carregado.

<a id="environment-variable-types"></a>
### Tipos de Variáveis de Ambiente

Todas as variáveis nos seus arquivos `.env` são normalmente interpretadas como strings, então alguns valores reservados foram criados para permitir que você retorne uma gama mais ampla de tipos da função `env()`:

<div class="overflow-auto">

| Valor do `.env` | Valor de `env()` |
| ------------ | ------------- |
| true         | (bool) true   |
| (true)       | (bool) true   |
| false        | (bool) false  |
| (false)      | (bool) false  |
| empty        | (string) ''   |
| (empty)      | (string) ''   |
| null         | (null) null   |
| (null)       | (null) null   |

</div>

Se você precisar definir uma variável de ambiente com um valor que contenha espaços, pode fazê-lo envolvendo o valor entre aspas duplas:

```ini
APP_NAME="My Application"
```

<a id="retrieving-environment-configuration"></a>
### Recuperando a Configuração de Ambiente

Todas as variáveis listadas no arquivo `.env` serão carregadas na superglobal `$_ENV` do PHP quando sua aplicação receber uma requisição. No entanto, você pode usar a função `env` para recuperar valores dessas variáveis nos seus arquivos de configuração. Na verdade, se você examinar os arquivos de configuração do Laravel, notará que muitas das opções já estão usando esta função:

```php
'debug' => (bool) env('APP_DEBUG', false),
```

O segundo valor passado para a função `env` é o "valor padrão". Esse valor será retornado se não existir nenhuma variável de ambiente para a chave informada.

<a id="determining-the-current-environment"></a>
### Determinando o Ambiente Atual

O ambiente atual da aplicação é determinado pela variável `APP_ENV` do seu arquivo `.env`. Você pode acessar esse valor pelo método `environment` da [facade](../facades/) `App`:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

Você também pode passar argumentos para o método `environment` para determinar se o ambiente corresponde a um determinado valor. O método retornará `true` se o ambiente corresponder a qualquer um dos valores informados:

```php
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> **Nota:**
> A detecção do ambiente atual da aplicação pode ser sobrescrita definindo uma variável de ambiente `APP_ENV` no nível do servidor.

<a id="encrypting-environment-files"></a>
### Criptografando Arquivos de Ambiente

Arquivos de ambiente não criptografados nunca devem ser armazenados no controle de versão. No entanto, o Laravel permite que você criptografe seus arquivos de ambiente para que eles possam ser adicionados com segurança ao controle de versão junto com o restante da sua aplicação.

<a id="encryption"></a>
#### Criptografia

Para criptografar um arquivo de ambiente, você pode usar o comando `env:encrypt`:

```shell
php artisan env:encrypt
```

Executar o comando `env:encrypt` criptografará seu arquivo `.env` e colocará o conteúdo criptografado em um arquivo `.env.encrypted`. A chave de descriptografia é apresentada na saída do comando e deve ser armazenada em um gerenciador de senhas seguro. Se você quiser fornecer sua própria chave de criptografia, pode usar a opção `--key` ao invocar o comando:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> **Nota:**
> O tamanho da chave fornecida deve corresponder ao tamanho de chave exigido pela cifra de criptografia em uso. Por padrão, o Laravel usará a cifra `AES-256-CBC`, que exige uma chave de 32 caracteres. Você pode usar qualquer cifra suportada pelo [encrypter](../encryption/) do Laravel passando a opção `--cipher` ao invocar o comando.

Se sua aplicação tiver múltiplos arquivos de ambiente, como `.env` e `.env.staging`, você pode especificar o arquivo de ambiente que deve ser criptografado fornecendo o nome do ambiente pela opção `--env`:

```shell
php artisan env:encrypt --env=staging
```

<a id="readable-variable-names"></a>
#### Nomes de Variáveis Legíveis

Ao criptografar seu arquivo de ambiente, você pode usar a opção `--readable` para manter visíveis os nomes das variáveis enquanto criptografa seus valores:

```shell
php artisan env:encrypt --readable
```

Isso produzirá um arquivo criptografado com o seguinte formato:

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...
```

Usar o formato legível permite que você veja quais variáveis de ambiente existem sem expor dados sensíveis. Isso também torna a revisão de pull requests muito mais fácil, pois você pode ver quais variáveis foram adicionadas, removidas ou renomeadas sem precisar descriptografar o arquivo.

Ao descriptografar arquivos de ambiente, o Laravel detecta automaticamente qual formato foi usado, então nenhuma opção adicional é necessária para o comando `env:decrypt`.

> **Nota:**
> Ao usar a opção `--readable`, comentários e linhas em branco do arquivo de ambiente original não são incluídos na saída criptografada.

<a id="updating-readable-environment-files"></a>
#### Atualizando Arquivos de Ambiente Legíveis

Ao atualizar um arquivo de ambiente criptografado legível, o Laravel preserva os valores inalterados e remove as variáveis que não existem mais no arquivo de ambiente de origem:

```shell
php artisan env:encrypt --readable --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

O arquivo criptografado será criado se não existir. Ao atualizar um arquivo existente, forneça a mesma chave de criptografia e cifra usadas para criá-lo. Se o arquivo não puder ser descriptografado, o comando falhará sem sobrescrevê-lo.

Para criptografar todos os valores novamente, use a opção `--force`. Isso permite que você altere a chave de criptografia ou substitua um arquivo criptografado inválido:

```shell
php artisan env:encrypt --readable --force --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<a id="decryption"></a>
#### Descriptografia

Para descriptografar um arquivo de ambiente, você pode usar o comando `env:decrypt`. Esse comando requer uma chave de descriptografia, que o Laravel obterá da variável de ambiente `LARAVEL_ENV_ENCRYPTION_KEY`:

```shell
php artisan env:decrypt
```

Ou, a chave pode ser fornecida diretamente ao comando pela opção `--key`:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

Quando o comando `env:decrypt` é invocado, o Laravel descriptografa o conteúdo do arquivo `.env.encrypted` e coloca o conteúdo descriptografado no arquivo `.env`.

A opção `--cipher` pode ser fornecida ao comando `env:decrypt` para usar uma cifra de criptografia personalizada:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

Se sua aplicação tiver múltiplos arquivos de ambiente, como `.env` e `.env.staging`, você pode especificar o arquivo de ambiente que deve ser descriptografado fornecendo o nome do ambiente pela opção `--env`:

```shell
php artisan env:decrypt --env=staging
```

Para sobrescrever um arquivo de ambiente existente, você pode fornecer a opção `--force` ao comando `env:decrypt`:

```shell
php artisan env:decrypt --force
```

<a id="accessing-configuration-values"></a>
## Acessando Valores de Configuração

Você pode facilmente acessar seus valores de configuração usando a facade `Config` ou a função global `config` de qualquer lugar da sua aplicação. Os valores de configuração podem ser acessados usando a sintaxe de "ponto", que inclui o nome do arquivo e da opção que você deseja acessar. Um valor padrão também pode ser especificado e será retornado se a opção de configuração não existir:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

Para definir valores de configuração em tempo de execução, você pode invocar o método `set` da facade `Config` ou passar um array para a função `config`:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

Para auxiliar a análise estática, a facade `Config` também fornece métodos de recuperação de configuração tipados. Se o valor de configuração recuperado não corresponder ao tipo esperado, uma exceção será lançada:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a id="configuration-caching"></a>
## Cache de Configuração

Para dar mais velocidade à sua aplicação, você deve armazenar em cache todos os seus arquivos de configuração em um único arquivo usando o comando Artisan `config:cache`. Isso combinará todas as opções de configuração da sua aplicação em um único arquivo que pode ser carregado rapidamente pelo framework.

Normalmente, você deve executar o comando `php artisan config:cache` como parte do processo de deploy da sua produção. O comando não deve ser executado durante o desenvolvimento local, pois as opções de configuração frequentemente precisarão ser alteradas ao longo do desenvolvimento da sua aplicação.

Depois que a configuração tiver sido armazenada em cache, o arquivo `.env` da sua aplicação não será carregado pelo framework durante requisições ou comandos Artisan; portanto, a função `env` retornará apenas variáveis de ambiente externas, no nível do sistema.

Por esse motivo, você deve garantir que esteja chamando a função `env` apenas de dentro dos arquivos de configuração (`config`) da sua aplicação. Você pode ver muitos exemplos disso examinando os arquivos de configuração padrão do Laravel. Os valores de configuração podem ser acessados de qualquer lugar da sua aplicação usando a função `config` [descrita acima](#accessing-configuration-values).

O comando `config:clear` pode ser usado para limpar a configuração armazenada em cache:

```shell
php artisan config:clear
```

> **Aviso:**
> Se você executar o comando `config:cache` durante seu processo de deploy, deve ter certeza de que está chamando a função `env` apenas de dentro dos seus arquivos de configuração. Depois que a configuração tiver sido armazenada em cache, o arquivo `.env` não será carregado; portanto, a função `env` retornará apenas variáveis de ambiente externas, no nível do sistema.

<a id="configuration-publishing"></a>
## Publicação de Configuração

A maioria dos arquivos de configuração do Laravel já é publicada no diretório `config` da sua aplicação; no entanto, certos arquivos de configuração, como `cors.php` e `view.php`, não são publicados por padrão, já que a maioria das aplicações nunca precisará modificá-los.

No entanto, você pode usar o comando Artisan `config:publish` para publicar quaisquer arquivos de configuração que não sejam publicados por padrão:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a id="debug-mode"></a>
## Modo Debug

A opção `debug` no seu arquivo de configuração `config/app.php` determina quanta informação sobre um erro é realmente exibida para o usuário. Por padrão, essa opção é definida para respeitar o valor da variável de ambiente `APP_DEBUG`, que é armazenada no seu arquivo `.env`.

> **Aviso:**
> Para desenvolvimento local, você deve definir a variável de ambiente `APP_DEBUG` como `true`. **No seu ambiente de produção, esse valor deve ser sempre `false`. Se a variável estiver definida como `true` em produção, você corre o risco de expor valores de configuração sensíveis aos usuários finais da sua aplicação.**

<a id="maintenance-mode"></a>
## Modo de Manutenção

Quando sua aplicação está em modo de manutenção, uma view personalizada será exibida para todas as requisições feitas à sua aplicação. Isso facilita "desabilitar" sua aplicação enquanto ela está atualizando ou quando você está realizando manutenção. Uma verificação de modo de manutenção está incluída na pilha de middleware padrão da sua aplicação. Se a aplicação estiver em modo de manutenção, uma instância de `Symfony\Component\HttpKernel\Exception\HttpException` será lançada com o código de status 503.

Para ativar o modo de manutenção, execute o comando Artisan `down`:

```shell
php artisan down
```

Se você quiser que o cabeçalho HTTP `Refresh` seja enviado com todas as respostas do modo de manutenção, pode fornecer a opção `refresh` ao invocar o comando `down`. O cabeçalho `Refresh` instruirá o navegador a atualizar automaticamente a página após o número de segundos especificado:

```shell
php artisan down --refresh=15
```

Você também pode fornecer uma opção `retry` ao comando `down`, que será definida como o valor do cabeçalho HTTP `Retry-After`, embora os navegadores geralmente ignorem esse cabeçalho:

```shell
php artisan down --retry=60
```

<a id="bypassing-maintenance-mode"></a>
#### Contornando o Modo de Manutenção

Para permitir que o modo de manutenção seja contornado usando um token secreto, você pode usar a opção `secret` para especificar um token de bypass do modo de manutenção:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

Depois de colocar a aplicação em modo de manutenção, você pode navegar até a URL da aplicação correspondente a esse token e o Laravel emitirá um cookie de bypass do modo de manutenção para o seu navegador:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Se você quiser que o Laravel gere o token secreto para você, pode usar a opção `with-secret`. O segredo será exibido assim que a aplicação estiver em modo de manutenção:

```shell
php artisan down --with-secret
```

Ao acessar essa rota oculta, você será redirecionado para a rota `/` da aplicação. Depois que o cookie tiver sido emitido no seu navegador, você poderá navegar pela aplicação normalmente, como se ela não estivesse em modo de manutenção.

> **Nota:**
> O segredo do seu modo de manutenção deve normalmente consistir em caracteres alfanuméricos e, opcionalmente, hífens. Você deve evitar usar caracteres que têm significado especial em URLs, como `?` ou `&`.

<a id="maintenance-mode-on-multiple-servers"></a>
#### Modo de Manutenção em Múltiplos Servidores

Por padrão, o Laravel determina se sua aplicação está em modo de manutenção usando um sistema baseado em arquivos. Isso significa que, para ativar o modo de manutenção, o comando `php artisan down` precisa ser executado em cada servidor que hospeda sua aplicação.

Como alternativa, o Laravel oferece um método baseado em cache para lidar com o modo de manutenção. Esse método requer a execução do comando `php artisan down` em apenas um servidor. Para usar essa abordagem, modifique as variáveis do modo de manutenção no arquivo `.env` da sua aplicação. Você deve selecionar um `store` de cache que seja acessível por todos os seus servidores. Isso garante que o status do modo de manutenção seja mantido de forma consistente em todos os servidores:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a id="pre-rendering-the-maintenance-mode-view"></a>
#### Pré-renderizando a View do Modo de Manutenção

Se você utilizar o comando `php artisan down` durante o deploy, seus usuários ainda poderão ocasionalmente encontrar erros se acessarem a aplicação enquanto suas dependências do Composer ou outros componentes de infraestrutura estiverem sendo atualizados. Isso ocorre porque uma parte significativa do framework Laravel precisa ser inicializada para determinar que sua aplicação está em modo de manutenção e renderizar a view do modo de manutenção usando o mecanismo de templates.

Por esse motivo, o Laravel permite que você pré-renderize uma view do modo de manutenção que será retornada logo no início do ciclo de requisição. Essa view é renderizada antes de qualquer uma das dependências da sua aplicação ter sido carregada. Você pode pré-renderizar um template de sua escolha usando a opção `render` do comando `down`:

```shell
php artisan down --render="errors::503"
```

<a id="redirecting-maintenance-mode-requests"></a>
#### Redirecionando Requisições do Modo de Manutenção

Enquanto estiver em modo de manutenção, o Laravel exibirá a view do modo de manutenção para todas as URLs da aplicação que o usuário tentar acessar. Se desejar, você pode instruir o Laravel a redirecionar todas as requisições para uma URL específica. Isso pode ser feito usando a opção `redirect`. Por exemplo, você pode desejar redirecionar todas as requisições para o URI `/`:

```shell
php artisan down --redirect=/
```

<a id="disabling-maintenance-mode"></a>
#### Desativando o Modo de Manutenção

Para desativar o modo de manutenção, use o comando `up`:

```shell
php artisan up
```

> **Nota:**
> Você pode personalizar o template padrão do modo de manutenção definindo seu próprio template em `resources/views/errors/503.blade.php`.

<a id="maintenance-mode-queues"></a>
#### Modo de Manutenção e Filas

Enquanto sua aplicação estiver em modo de manutenção, nenhum [job enfileirado](../queues/) será processado. Os jobs continuarão a ser processados normalmente assim que a aplicação sair do modo de manutenção.

<a id="alternatives-to-maintenance-mode"></a>
#### Alternativas ao Modo de Manutenção

Como o modo de manutenção exige que sua aplicação fique indisponível por alguns segundos, considere executar suas aplicações em uma plataforma totalmente gerenciada como o [Laravel Cloud](https://cloud.laravel.com) para realizar deploy sem downtime com o Laravel.
