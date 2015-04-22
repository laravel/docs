# Configuration

- [Introdução](#introduction)
- [After Installation](#after-installation)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Environment Configuration](#environment-configuration)
- [Configuration Caching](#configuration-caching)
- [Maintenance Mode](#maintenance-mode)
- [Pretty URLs](#pretty-urls)

<a name="introduction"></a>
## Introdução

Todos os arquivos de configuração para o framework Laravel são armazenados no diretório `config`. Cada opção é documentada, então sinta-se livre para dar uma olhada nos arquivos
e se famialirizar com as opções disponíves pra você.

<a name="after-installation"></a>
## Depois Da Instalação

### Nomeando sua aplicação

Depois de instalar Laravel, você pode querer nomear a sua aplicação. Por padrão, o diretório `app` tem o namespace `App`, e é carregado automaticamente pelo Composer usando a [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/). Contudo, você pode mudar o namespace para o mesmo da sua aplicação, que você pode facilmente fazer por meio do comando Artisan `app:name`.

Por exemplo, se sua aplicação é nomeada "Horsefly", você pode executar o seguinte comando a partir do diretório root da sua instalação:

	php artisan app:name Horsefly

Renomear sua aplicação é totalmente opcional, e você é livre para manter o namespace `App` se você desejar.

### Outras Configurações

Laravel precisa de poucas configurações de fora da caixa. Você é livre para começar a desenvolver! No entanto, você pode desejar revisar o arquivo `config/app.php` e sua documentação. Nela, contém várias opções como as de `timezone` (fuso-horário) e `locale` (localização) que você pode desejar mudar de acordo com a sua localização.

Uma vez que o Laravel é instalado, você deve tambeḿ [configure your local environment](/docs/5.0/configuration#environment-configuration).

> **Nota:** Você nunca deve ter a configuração `app.debug` definida como "true" no ambiente de produção da sua aplicação.

<a name="permissions"></a>
### Permissões

Laravel pode requerir um conjunto de permissões para ser configurado: pastas dentro do diretório `storage` requerem permissões de acesso a escrita no servidor. 

<a name="accessing-configuration-values"></a>
## Accessing Configuration Values

You may easily access your configuration values using the `Config` facade:

	$value = Config::get('app.timezone');

	Config::set('app.timezone', 'America/Chicago');

You may also use the `config` helper function:

	$value = config('app.timezone');

<a name="environment-configuration"></a>
## Environment Configuration

It is often helpful to have different configuration values based on the environment the application is running in. For example, you may wish to use a different cache driver locally than you do on your production server. It's easy using environment based configuration.

To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file. If you install Laravel via Composer, this file will automatically be renamed to `.env`. Otherwise, you should rename the file manually.

All of the variables listed in this file will be loaded into the `$_ENV` PHP super-global when your application receives a request. You may use the `env` helper to retrieve values from these variables. In fact, if you review the Laravel configuration files, you will notice several of the options already using this helper!

Feel free to modify your environment variables as needed for your own local server, as well as your production environment. However, your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration.

If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting place-holder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application.

#### Accessing The Current Application Environment

You may access the current application environment via the `environment` method on the `Application` instance:

	$environment = $app->environment();

You may also pass arguments to the `environment` method to check if the environment matches a given value:

	if ($app->environment('local'))
	{
		// The environment is local
	}

	if ($app->environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

To obtain an instance of the application, resolve the `Illuminate\Contracts\Foundation\Application` contract via the [service container](/docs/5.0/container). Of course, if you are within a [service provider](/docs/5.0/providers), the application instance is available via the `$this->app` instance variable.

An application instance may also be accessed via the `app` helper of the `App` facade:

	$environment = app()->environment();

	$environment = App::environment();

<a name="configuration-caching"></a>
## Configuration Caching

To give your application a little speed boost, you may cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be loaded quickly by the framework.

You should typically run the `config:cache` command as part of your deployment routine.

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

While your application is in maintenance mode, no [queued jobs](/docs/5.0/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.

<a name="pretty-urls"></a>
## Pretty URLs

### Apache

The framework ships with a `public/.htaccess` file that is used to allow URLs without `index.php`. If you use Apache to serve your Laravel application, be sure to enable the `mod_rewrite` module.

If the `.htaccess` file that ships with Laravel does not work with your Apache installation, try this one:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

On Nginx, the following directive in your site configuration will allow "pretty" URLs:

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

Of course, when using [Homestead](/docs/5.0/homestead), pretty URLs will be configured automatically.
