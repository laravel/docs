# Instalação

- [Instalação](#installation)
- [Configuração](#configuration)
	- [Configração Básicas](#basic-configuration)
	- [Configuração do Ambiente](#environment-configuration)
	- [Cache das Configurações](#configuration-caching)
	- [Acessando Valores Configurados](#accessing-configuration-values)
	- [Nomeando Sua Aplicação](#naming-your-application)
- [Modo de Manutenção](#maintenance-mode)

<a name="installation"></a>
## Instalação

### Requisitos do Servidor

O framework Laravel pede alguns requerimentos no sistema. E é claro, todas esses requerimentos já vem configurados na máquina virtual [Laravel Homestead](/docs/{{version}}/homestead):

<div class="content-list" markdown="1">
- PHP >= 5.5.9
- Extensão PHP OpenSSL
- Extensão PHP PDO
- Extensão PHP Mbstring
- Extensão PHP Tokenizer
</div>

<a name="install-laravel"></a>
### Instalando o Laravel

Laravel utiliza o [Composer](http://getcomposer.org) para gerenciar suas dependências. Então, antes de usar o Laravel, certifique-se de ter o Composer instalado na sua máquina.

#### Através do Instalador do Laravel

Primeiro baixe o instalador usando o Composer:

	composer global require "laravel/installer=~1.1"

Certifique-se de que o diretório `~/.composer/vendor/bin` esteja no PATH do sistema e então o executável `laravel` poderá ser localizado pelo seu sistema.

Uma vez instalado, um simples comando `laravel new` criará uma nova instalação do Laravel no diretório que você especificou. Por exemplo, `laravel new blog` criará um diretório chamado blog contendo os arquivos da instalação inicial do Laravel com todas as suas dependências instaladas. Esse método de instalação é muito mais rápido do que a instalação via Composer:

	laravel new blog

#### Instalação pelo Composer Create-Project

Você também pode instalar o Laravel usando o comando `composer create-project` no seu terminal:

	composer create-project laravel/laravel --prefer-dist

<a name="configuration"></a>
## Configuração

<a name="basic-configuration"></a>
### Configuração Básica

Todos os arquivos de configuração do framework Laravel são localizados no diretório `config`. Cada opção é documentada, então seja livre para olhar os arquivos e se familiarizar com as opções disponíveis para você.

#### Permissões de Diretório

Após instalar o Laravel, você pode precisar configurar algumas permissões. Diretórios dentro de `storage` e `bootstrap/cache` devem ter permissão de escrita pelo servidor web. Se você está usando a máquina virtual [Homestead](/docs/{{version}}/homestead) , essas permissões já vem configuradas.

#### Chave da Aplicação

A próxima coisa que você deve fazer após instalar o Laravel é configurar a chave da aplicação com uma string aleatória. Se você instalou o Laravel via Composer ou via Instalador do Laravel, a chave da aplicação já deve ter sido configurada pelo comando `key:generate`. Tipicamente, essa string deve conter 32 caracteres. Ela pode ser configurada no arquivo de ambiente `.env`. Se você não renomeou o arquivo `.env.example` para `.env`, você deve fazer isso agora. **Se a a chave da aplicação não for configurada, as sessões dos seus usuários e outros dados encriptados não serão seguros!**


#### Configuração Adicional

O Laravel não precisa de nenhuma outra configuração, você já pode começar a desenvolver! Entretanto, caso precise, revise o arquivo `config/app.php` e sua documentação. Ele contem algumas opções como `timezone` e `locale` que você pode querer configurar de acordo com sua aplicação.

Você pode também configurar alguns componentes adicionais do Laravel, dentre eles:

- [Cache](/docs/{{version}}/cache#configuration)
- [Database](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)

Depois de instalar o Laravel, você também deve [Configurar o Ambiente de Desenvolvimento](/docs/{{version}}/installation#environment-configuration).

<a name="pretty-urls"></a>
#### URLs amigáveis

**Apache**

O Laravel vem com o arquivo `public/.htaccess` que é usado para permitir URLs sem o prefixo `index.php`. Se você usa o servidor Apache, certifique-se te ativar o módulo `mod_rewrite`.

Se o arquivo `.htaccess` não funcionar corretamente na sua instalação do Apache, tente esse aqui:

	Options +FollowSymLinks
	RewriteEngine On
    
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

**Nginx**

No Nginx, a seguinte diretiva nas configurações do seu site permitirão URLs amigáveis:

	location / {
		try_files $uri $uri/ /index.php?$query_string;
	}

E é claro, se está usando [Homestead](/docs/{{version}}/homestead), as URLs amigáveis serão configuradas automaticamente.

<a name="environment-configuration"></a>
### Configurações do Ambiente

É muito útil ter diferentes valores de configuração baseado no ambiente em que a aplicação está rodando. Por exemplo, você pode querer usar diferentes drivers de cache localmente e outro no servidor de produção. Isso é muito fácil usando as configurações baseadas em ambiente.

Para tornar isso fácil, o Laravel utiliza a Biblioteca PHP [DotEnv](https://github.com/vlucas/phpdotenv) do Vance Lucas (vlucas). Numa instalação inicial do Laravel, no diretório principal da aplicação conterá o arquivo `env.example`. Se você instalou o Laravel via Composer, esse arquivo será automaticamente copiado para `.env`. Entretanto, você pode copiar ou renomeá-lo manualmente.

Todas as variáveis listadas nesse arquivo serão carregadas a variável super global do PHP `$_ENV` quando sua aplicação receber uma requisição. Você pode usar a função utilitária `env` para pegar esses valores. Se você revisou os arquivos de configuração do Laravel, você deve ter percebido que muitas das opções já utilizam essa função utilitária.

Você é livre para modificar suas variáveis de ambiente como quiser, para sua aplicação local ou para seu servidor de produção. Entretanto, seu arquivo `.env` não deve ser versionado, por que cada desenvolvedor / servidor podem precisar de uma configuração diferente desse arquivo.

Se você está desenvolvendo em equipe, você pode incluir o arquivo `.env.example` e adicionar lá alguns comentários sobre a configuração do arquivo, para que cada desenvolvedor entenda claramente quais configurações eles devem fazer em seus próprios `.env` para rodar sua aplicação.

#### Acessando o Ambiente da Aplicação Atual

Você pode acessar o ambiente atual da sua aplicação pelo método `environment`do facade `App`:

	$environment = App::environment();

Você também pode passar arguementos para o método `environment` para verificar se o ambiente atual é o que foi passado por argumento. Você pode até passar multiplos ambientes ou fazer a chamada ao método múltiplas vezes, se necessário:

	if (App::environment('local')) {
		// Aqui instruções para rodar no ambiente local
	}

	if (App::environment('local', 'staging')) {
		// Aqui instruções para rodar no ambiente local OU staging
	}

Uma instancia da aplicação também pode ser acessada pela função utilitária `app`:

	$environment = app()->environment();

<a name="configuration-caching"></a>
### Cache das Configurações

Para que sua aplicação tenha maior velocidade, você pode fazer cache de todos os arquivos de configuração em um único arquivo usando o comando Artisan `config:cache`. Ele irá combinar todas as opções de configuração da sua aplicação em um único arquivo que pode ser carregado mais rapidamente pelo framework.

Você pode natualmente rodar o comando `config:cache` como parte da sua rotina de deploy.

<a name="accessing-configuration-values"></a>
### Acessando Valores de Configuração

Você pode facilmente acessar seus valores de configuração usando a função utilitária global `config`. Os valores de configuração devem ser acessados usando a sintaxe "dot" (ponto), que inclue o nome do arquivo e a configuração que deseja acessar. Você também pode especificar um valor padrão, caso a configuração não exista:

	$value = config('app.timezone');

Para inserir valores de configuração em tempo de execução, passe um array para o utilitário `config`: 

	config(['app.timezone' => 'America/Chicago']);

> **Nota:** Esses valores não serão persistidos nos arquivos de configuração.

<a name="naming-your-installation"></a>
### Nomeando Sua Aplicação

Após instalar o Laravel, você pode querer dar um "nome" para sua aplicação. Por padrão, o diretório `app` estará com o namespace `App`, e é carregado pelo Composer usando o [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/). Entretanto, você pode mudar o namespace para que fique igual ao nome da sua aplicação, o que você pode fazer facilmente com o comando Artisan `app:name`.

Por exemplo, se sua aplicação se chama "Codecasts" (sem espaços ou caracteres especiais), você pode pode rodar o seguinte comando no diretório principal da sua instalação:

	php artisan app:name Codecasts

Renomear sua aplicação é completamente opcional, você pode mander o namespace `App` se assim desejar.

<a name="maintenance-mode"></a>
## Modo de Manutenção

Quando sua aplicação está em modo de manutenção, uma view será exibida para todos as requisições na sua aplicação. Isso torna fácil "desativar" sua aplicação enquanto esta atualizando ou quando você está fazendo alguma manutenção. O modo de manutenção é verificado num middleware padrão da sua aplicação. Se sua aplicação está no modo de manutenção, um `HttpException` será exibida com o código 503.

Para ativar o modo de manutenção, simplesmente execute o comando Artisan `down`:

	php artisan down

Para desativar, use o comando `up`:

	php artisan up

### Template do Modo de Manutenção

O template padrão do modo de manutenção está localizado em `resources/views/errors/503.blade.php`.

### Modo de Manutenção & Filas de Tarefas

Enquanto sua aplicação estiver no modo de manutenção, nenhuma [Fila de Tarefa](/docs/{{version}}/queues) será executada. A tarefa continuará normalmente assim que sua aplicação sair do modo de manutenção.
