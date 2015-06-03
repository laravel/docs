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

### Requerimentos do Server

O framework Laravel pede alguns requerimentos no sistema. E é claro, todas esses requerimentos já vem satisfeitos na máquina virtual [Laravel Homestead](/docs/{{version}}/homestead):

<div class="content-list" markdown="1">
- PHP >= 5.5.9
- Mcrypt
- OpenSSL
- Mbstring 
- Tokenizer
</div>

<a name="install-laravel"></a>
### Instalando o Laravel

Laravel utiliza [Composer](http://getcomposer.org) para gerenciar suas dependências. Então, antes de usar o Laravel, certifique-se de ter o Composer instalado na sua máquina.

#### Instação pelo Instalador do Laravel

Primeiro baixe o instalador usando o Composer:

	composer global require "laravel/installer=~1.1"

Certifique-se de que o diretório `~/.composer/vendor/bin` esteja no PATH do sistema e então o executável `laravel` poderá ser localizado pelo seu sistema.

Uma vez instlado, um simples comando  `laravel new` criará uma instalação do Laravel do princípio no diretório que você especificou. Por exemplo, `laravel new blog` criará um diretório chamado blog contendo os arquivos da instalação inicial do Laravel com todas as suas dependências instaladas. Esse método de instalação é muito mais rápido do que a instalação via Composer:

	laravel new blog

#### Instalação pelo Composer Create-Project

Você também pode instalar o Laravel usando o comando `composer create-project` no seu terminal:

	composer create-project laravel/laravel --prefer-dist

<a name="configuration"></a>
## Configuração

<a name="basic-configuration"></a>
### Configuração Básica

Todos os arqivos de configuração do framework Laravel são armazenados no diretório `config`. Cada opção é documentada, então seja livre para olhar os arquivos e se familiarizar com as opções disponíveis para você.

#### Permissões de Diretório

Após instalar o Laravel, você pode precisar configurar algumas permissões. Diretórios dentro de `storage` e `bootstrap/cache` devem ter permissão de escrita pelo servidor web. Se você está usando a máquina virtual [Homestead](/docs/{{version}}/homestead) , essas permissões já vem configuradas.

#### Chave da Aplicação

A próxima coisa que você deve fazer após instalar o Laravel é configurar uma chave da aplicação com uma string aleatória. Se você instalou o Laravel via Composer ou via Instalador do Laravel, a chave da aplicação já deve ter sido configurada pelo comando `key:generate`. Tipicamente, essa string deve conter 32 caracteres. Ela pode configurada em no arquivo de ambiente `.env`. Se você não renomeou o arquivo `.env.example` para `.env`, você deve fazer isso agora. **Se a a chave da aplicação não for configurada, as sessões dos seus usuários e outros dados encriptados não serão seguros!**


#### Configuração Adicional

Laravel needs almost no other configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

You may also want to configure a few additional components of Laravel, such as:

- [Cache](/docs/{{version}}/cache#configuration)
- [Database](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)

Once Laravel is installed, you should also [configure your local environment](/docs/{{version}}/installation#environment-configuration).

<a name="pretty-urls"></a>
#### Pretty URLs

**Apache**

The framework ships with a `public/.htaccess` file that is used to allow URLs without `index.php`. If you use Apache to serve your Laravel application, be sure to enable the `mod_rewrite` module.

If the `.htaccess` file that ships with Laravel does not work with your Apache installation, try this one:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

**Nginx**

On Nginx, the following directive in your site configuration will allow "pretty" URLs:

	location / {
		try_files $uri $uri/ /index.php?$query_string;
	}

Of course, when using [Homestead](/docs/{{version}}/homestead), pretty URLs will be configured automatically.

<a name="environment-configuration"></a>
### Environment Configuration

It is often helpful to have different configuration values based on the environment the application is running in. For example, you may wish to use a different cache driver locally than you do on your production server. It's easy using environment based configuration.

To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file. If you install Laravel via Composer, this file will automatically be renamed to `.env`. Otherwise, you should rename the file manually.

All of the variables listed in this file will be loaded into the `$_ENV` PHP super-global when your application receives a request. You may use the `env` helper to retrieve values from these variables. In fact, if you review the Laravel configuration files, you will notice several of the options already using this helper!

Feel free to modify your environment variables as needed for your own local server, as well as your production environment. However, your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration.

If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting place-holder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application.

#### Accessing The Current Application Environment

You may access the current application environment via the `environment` method on the `App` facade:

	$environment = App::environment();

You may also pass arguments to the `environment` method to check if the environment matches a given value. You may even pass multiple values if necessary:

	if (App::environment('local')) {
		// The environment is local
	}

	if (App::environment('local', 'staging')) {
		// The environment is either local OR staging...
	}

An application instance may also be accessed via the `app` helper method:

	$environment = app()->environment();

<a name="configuration-caching"></a>
### Configuration Caching

To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be loaded quickly by the framework.

You should typically run the `config:cache` command as part of your deployment routine.

<a name="accessing-configuration-values"></a>
### Accessing Configuration Values

You may easily access your configuration values using the global `config` helper function. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you with to access. A default value may also be specified and will be returned if the configuration option does not exist:

	$value = config('app.timezone');

To set configuration values at runtime, pass an array to the `config` helper:

	config(['app.timezone' => 'America/Chicago']);

<a name="naming-your-installation"></a>
### Naming Your Application

After installing Laravel, you may wish to "name" your application. By default, the `app` directory is namespaced under `App`, and autoloaded by Composer using the [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/). However, you may change the namespace to match the name of your application, which you can easily do via the `app:name` Artisan command.

For example, if your application is named "Horsefly", you could run the following command from the root of your installation:

	php artisan app:name Horsefly

Renaming your application is entirely optional, and you are free to keep the `App` namespace if you wish.

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, an `HttpException` will be thrown with a status code of 503.

To enable maintenance mode, simply execute the `down` Artisan command:

	php artisan down

To disable maintenance mode, use the `up` command:

	php artisan up

### Maintenance Mode Response Template

The default template for maintenance mode responses is located in `resources/views/errors/503.blade.php`.

### Maintenance Mode & Queues

While your application is in maintenance mode, no [queued jobs](/docs/{{version}}/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.
